"""The live call listener: the client's voice in, answer cards out.

Audio from the call goes to ElevenLabs realtime speech-to-text. Each finished
utterance that looks like a question is answered from the facts (api.answer), and
both the running transcript and the answer are pushed to the advisor's phone.

Audio arrives as 16-bit PCM at 16 kHz (pcm_16000), from either the phone page's
microphone (WS /listen) or the recorded demo pipeline (backend/demo.py). Both drive
the same Session, so an answer card is built the same way whichever fed it.

In production this sits on the advisor's line, which banks already route and record --
that is where the caller ID before the first ring comes from. Demos here are scripted.

Measured on this key: with a 0.5 s silence threshold the committed transcript
arrives ~0.6 s after the client stops speaking; the answer event reaches the phone
~0.85 s after (tests/test_listener.py, RUN_NETWORK_TESTS=1).
"""

import asyncio
import base64
import json
import re
import time

import websockets

import os
from datetime import datetime

from . import utterance
from .answers import LIQUIDITY_NEED, small_talk_only
from .data import env

STT_URL = ('wss://api.elevenlabs.io/v1/speech-to-text/realtime?model_id=scribe_v2_realtime'
           '&audio_format={fmt}&commit_strategy=vad&vad_silence_threshold_secs=0.5')
SAMPLE_RATES = {'pcm_16000': 16000}
BYTES_PER_SECOND = {'pcm_16000': 32000}
BATCH_SECONDS = 0.1          # send audio in 100 ms batches rather than per-frame


# How sessions open the speech-to-text socket; tests replace this with a fake.
connect_stt = websockets.connect

# Utterances that are not worth answering.
FILLER = {'yes', 'yeah', 'no', 'okay', 'ok', 'hello', 'hi', 'thanks', 'thank you', 'bye', 'goodbye', 'right',
          'sure', 'mhm', 'uh', 'um', 'hmm', 'alright', 'good', 'great', 'fine'}
QUESTION_WORDS = ('how', 'what', 'why', 'when', 'where', 'which', 'who', 'is', 'are', 'did', 'do', 'does', 'can',
                  'could', 'should', 'will', 'would', 'have', 'has')
# Not questions, but the client is still asking to be told something.
REQUEST_WORDS = ('tell', 'explain', 'show')


# --- what to answer ---------------------------------------------------------------

def is_question(text):
    """Worth answering: a question mark, a question word, or a request to be told something.

    A plain statement is not worth answering. The advisor reads these cards mid-call, so a
    card they did not ask for costs them the seconds they have. The recorded golf call shows
    the STT punctuates: every real question ended in '?' and the sign-off did not.
    """
    clean = re.sub(r'[^\w\s?]', '', (text or '').lower()).strip()
    if not clean or clean.rstrip('?').strip() in FILLER or small_talk_only(text):
        return False
    if clean.endswith('?'):
        return True
    words = clean.rstrip('?').split()
    return len(words) >= 3 and words[0] in QUESTION_WORDS + REQUEST_WORDS


# --- the session ----------------------------------------------------------------------

class Session:
    """One call's audio -> ElevenLabs realtime STT -> transcript and answer events.

    on_event: async callable taking an event dict (e.g. state.broadcast).
    answer:   callable(text) -> {'answers': [...], 'found': bool}, run in a thread.
    Never raises into the caller: connection problems become 'listener_error' events and
    the audio is dropped, so a failing listener cannot take the call or the API down.
    """

    def __init__(self, client_ref, on_event, answer, fmt='pcm_16000', source='browser', key=None,
                 connect=None, open_timeout=10):
        if fmt not in SAMPLE_RATES:
            raise ValueError(f'unsupported audio format {fmt}')
        self.client = client_ref
        self.on_event = on_event
        self.answer = answer
        self.fmt = fmt
        self.source = source
        self.key = key or env('ELEVENLABS_KEY')
        self.connect = connect or connect_stt
        self.open_timeout = open_timeout
        self.ws = None
        self.reader = None
        self.buffer = bytearray()
        self.batch = int(BYTES_PER_SECOND[fmt] * BATCH_SECONDS)
        self.reconnects = 0
        self.closed = False
        self.failed = False
        self.last_answered = None
        self.answer_tasks = set()
        self.log = None if os.getenv('PYTEST_CURRENT_TEST') else \
            utterance.SessionLog(client_ref, source, datetime.now())

    async def emit(self, event):
        try:
            await self.on_event({'client': self.client, 'at': round(time.time(), 3), **event})
        except Exception:  # a broken subscriber must not stop the listener
            pass

    async def start(self):
        if not self.key:
            self.failed = True
            await self.emit({'type': 'listener_error', 'error': 'ELEVENLABS_KEY is not set'})
            return False
        try:
            self.ws = await asyncio.wait_for(
                self.connect(STT_URL.format(fmt=self.fmt), additional_headers={'xi-api-key': self.key}),
                self.open_timeout)
        except Exception as e:
            self.failed = True
            await self.emit({'type': 'listener_error', 'error': f'speech-to-text connection failed: {type(e).__name__}'})
            return False
        self.reader = asyncio.create_task(self._read())
        await self.emit({'type': 'listening', 'source': self.source})
        return True

    async def send_audio(self, chunk):
        if self.closed or self.failed or not chunk:
            return
        self.buffer += chunk
        if len(self.buffer) >= self.batch:
            await self._flush()

    async def _flush(self):
        if not self.buffer or self.ws is None:
            return
        payload = json.dumps({'message_type': 'input_audio_chunk',
                              'audio_base_64': base64.b64encode(bytes(self.buffer)).decode('ascii'),
                              'sample_rate': SAMPLE_RATES[self.fmt], 'commit': False})
        self.buffer.clear()
        try:
            await self.ws.send(payload)
        except Exception:
            await self._reconnect()

    async def _reconnect(self):
        if self.closed or self.reconnects >= 1:
            self.failed = True
            await self.emit({'type': 'listener_error', 'error': 'speech-to-text connection lost'})
            return
        self.reconnects += 1
        old = self.ws
        self.ws = None
        try:
            await old.close()
        except Exception:
            pass
        if self.reader and self.reader is not asyncio.current_task():
            self.reader.cancel()
        await self.start()

    async def _read(self):
        try:
            async for message in self.ws:
                await self._handle(message)
        except asyncio.CancelledError:
            raise
        except Exception:
            pass
        if not self.closed:
            await self._reconnect()

    async def _handle(self, message):
        try:
            data = json.loads(message)
        except (json.JSONDecodeError, TypeError):
            return
        kind = data.get('message_type') or ''
        text = (data.get('text') or '').strip()
        if kind == 'partial_transcript' and text:
            await self.emit({'type': 'transcript', 'text': text, 'final': False})
        elif kind.startswith('committed_transcript') and text:
            await self.emit({'type': 'transcript', 'text': text, 'final': True})
            said = utterance.classify(text)
            if said in ('instruction', 'request', 'info'):
                # Not a card: a line for the call note. Nothing is ever acted on.
                await self.emit({'type': 'heard', 'kind': said, 'label': utterance.LABELS[said], 'text': text})
                self._log(text, said, 'noted')
                if said == 'info' and LIQUIDITY_NEED.search(text) and text != self.last_answered:
                    # "I want to buy a house" is noted and answered: what cash there is.
                    self.last_answered = text
                    task = asyncio.create_task(self._answer(text))
                    self.answer_tasks.add(task)
                    task.add_done_callback(self.answer_tasks.discard)
            elif said == 'question' and is_question(text) and text != self.last_answered:
                self.last_answered = text
                task = asyncio.create_task(self._answer(text))
                self.answer_tasks.add(task)
                task.add_done_callback(self.answer_tasks.discard)
            else:
                self._log(text, said, 'nothing')
        elif 'error' in kind:
            await self.emit({'type': 'listener_error', 'error': data.get('error') or kind})

    async def _answer(self, text):
        try:
            result = await asyncio.to_thread(self.answer, text)
        except Exception as e:
            await self.emit({'type': 'listener_error', 'error': f'answering failed: {type(e).__name__}'})
            return
        if not result.get('found') and result.get('method') != 'small_talk':
            # Nothing in the data answers it: an empty card mid-call is clutter, a follow-up is useful.
            await self.emit({'type': 'heard', 'kind': 'follow_up', 'label': utterance.LABELS['follow_up'], 'text': text})
            self._log(text, 'question', 'follow_up', method=result.get('method'))
            return
        await self.emit({'type': 'answer', 'question': text, **result})
        self._log(text, 'question', 'card', method=result.get('method'),
                  shown=(result.get('answers') or [{}])[0].get('text', ''),
                  facts=[a.get('fact') for a in result.get('answers') or []])

    def _log(self, text, kind, decision, **extra):
        if self.log:
            self.log.write(at=round(time.time(), 3), client=self.client, source=self.source,
                           text=text, kind=kind, decision=decision, **extra)

    async def close(self):
        if self.closed:
            return
        await self._flush()
        if self.answer_tasks:
            await asyncio.wait(self.answer_tasks, timeout=5)
        self.closed = True
        # Tell the phone first: closing the upstream socket can wait on its handshake.
        await self.emit({'type': 'listening_stopped', 'source': self.source})
        if self.reader:
            self.reader.cancel()
        if self.ws is not None:
            try:
                await asyncio.wait_for(self.ws.close(), 2)
            except Exception:
                pass
