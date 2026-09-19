"""The live call listener: the client's voice in, answer cards out.

Audio from the call goes to ElevenLabs realtime speech-to-text. Each finished
utterance that looks like a question is answered from the facts (api.answer), and
both the running transcript and the answer are pushed to the advisor's phone.

Two ways audio arrives, one Session for both:

- Twilio Media Streams: mu-law 8 kHz, which ElevenLabs accepts as-is (ulaw_8000),
  so phone audio is forwarded without conversion.
- The phone page's microphone: 16-bit PCM at 16 kHz (pcm_16000), for demos without
  a Twilio number.

Measured on this key: with a 0.5 s silence threshold the committed transcript
arrives ~0.6 s after the client stops speaking; the answer event reaches the phone
~0.85 s after (tests/test_listener.py, RUN_NETWORK_TESTS=1).

Going live with Twilio:
1. Run the API behind HTTPS: `uvicorn backend.api:app --port 8000` and
   `cloudflared tunnel --url http://localhost:8000` (or `ngrok http 8000`). The tunnel
   host changes every restart, so step 3 has to be redone each time.
2. Map the calling numbers to clients in data/phonebook.json. ADVISOR_NUMBER (the
   advisor's mobile, E.164) is optional -- see the two shapes below.
3. In the Twilio console, on the number: "A call comes in" -> Webhook, HTTP POST,
   https://<tunnel host>/twilio/voice. The TwiML it returns streams the caller's audio
   to wss://<tunnel host>/twilio/media.
4. Open https://<tunnel host>/phone/ wherever the advisor will read the cards.

Two shapes, same pipeline:

- Two phones. ADVISOR_NUMBER set: the TwiML dials the advisor after starting the stream,
  so the client and the advisor are on a real forwarded call. This is the production
  story and what the video shows.
- One phone. ADVISOR_NUMBER unset: nothing is dialled and a <Pause> holds the caller's
  line open, so their audio keeps streaming while the advisor watches the phone page in
  a browser. Nobody speaks back to the client, so this is for testing the pipeline --
  and for a trial account, where every number on the call has to be verified first.
"""

import asyncio
import base64
import json
import re
import time
from xml.sax.saxutils import escape, quoteattr

import websockets

from .data import env

STT_URL = ('wss://api.elevenlabs.io/v1/speech-to-text/realtime?model_id=scribe_v2_realtime'
           '&audio_format={fmt}&commit_strategy=vad&vad_silence_threshold_secs=0.5')
SAMPLE_RATES = {'ulaw_8000': 8000, 'pcm_16000': 16000}
BYTES_PER_SECOND = {'ulaw_8000': 8000, 'pcm_16000': 32000}
BATCH_SECONDS = 0.1          # send audio in 100 ms batches rather than Twilio's 20 ms frames

RECORDING_NOTICE = 'This call is recorded for advice documentation.'
# How long the line is held open when there is no advisor number to dial. Twilio caps a
# trial call at 10 minutes anyway, and a demo call is over in two.
HOLD_SECONDS = 600

# How sessions open the speech-to-text socket; tests replace this with a fake.
connect_stt = websockets.connect

# Utterances that are not worth answering.
FILLER = {'yes', 'yeah', 'no', 'okay', 'ok', 'hello', 'hi', 'thanks', 'thank you', 'bye', 'goodbye', 'right',
          'sure', 'mhm', 'uh', 'um', 'hmm', 'alright', 'good', 'great', 'fine'}
QUESTION_WORDS = ('how', 'what', 'why', 'when', 'where', 'which', 'who', 'is', 'are', 'did', 'do', 'does', 'can',
                  'could', 'should', 'will', 'would', 'have', 'has')
# Not questions, but the client is still asking to be told something.
REQUEST_WORDS = ('tell', 'explain', 'show')


# --- mu-law (G.711), since Python 3.13 removed audioop ---------------------------

def _ulaw_decode(u):
    u = ~u & 0xFF
    sample = (((u & 0x0F) << 3) + 0x84) << ((u >> 4) & 0x07)
    return 0x84 - sample if u & 0x80 else sample - 0x84


ULAW_TO_PCM = [_ulaw_decode(u) for u in range(256)]


def _ulaw_encode(sample):
    sign = 0x80 if sample < 0 else 0
    magnitude = min(abs(sample), 32635) + 0x84
    exponent = max(magnitude.bit_length() - 8, 0)
    mantissa = (magnitude >> (exponent + 3)) & 0x0F
    return ~(sign | (exponent << 4) | mantissa) & 0xFF


def ulaw_to_pcm16(data):
    """mu-law bytes -> little-endian 16-bit PCM bytes."""
    out = bytearray()
    for u in data:
        out += ULAW_TO_PCM[u].to_bytes(2, 'little', signed=True)
    return bytes(out)


def pcm16_to_ulaw(data):
    """Little-endian 16-bit PCM bytes -> mu-law bytes."""
    return bytes(_ulaw_encode(int.from_bytes(data[i:i + 2], 'little', signed=True))
                 for i in range(0, len(data) - 1, 2))


# --- what to answer ---------------------------------------------------------------

def is_question(text):
    """Worth answering: a question mark, a question word, or a request to be told something.

    A plain statement is not worth answering. The advisor reads these cards mid-call, so a
    card they did not ask for costs them the seconds they have. The recorded golf call shows
    the STT punctuates: every real question ended in '?' and the sign-off did not.
    """
    clean = re.sub(r'[^\w\s?]', '', (text or '').lower()).strip()
    if not clean or clean.rstrip('?').strip() in FILLER:
        return False
    if clean.endswith('?'):
        return True
    words = clean.rstrip('?').split()
    return len(words) >= 3 and words[0] in QUESTION_WORDS + REQUEST_WORDS


# --- Twilio -------------------------------------------------------------------------

def parse_twilio(message):
    """One Twilio Media Streams message -> {'event', 'stream_sid', 'client', 'track', 'audio'}.

    Events: connected, start (customParameters carry the client), media (base64 mu-law
    8 kHz), mark, stop. Unknown or malformed messages come back as {'event': None}.
    """
    try:
        data = json.loads(message)
    except (json.JSONDecodeError, TypeError):
        return {'event': None}
    event = data.get('event')
    out = {'event': event, 'stream_sid': data.get('streamSid')}
    if event == 'start':
        start = data.get('start') or {}
        out['stream_sid'] = start.get('streamSid') or out['stream_sid']
        out['client'] = (start.get('customParameters') or {}).get('client')
        out['call_sid'] = start.get('callSid')
    elif event == 'media':
        media = data.get('media') or {}
        out['track'] = media.get('track', 'inbound')
        try:
            out['audio'] = base64.b64decode(media.get('payload') or '')
        except (ValueError, TypeError):
            out['audio'] = b''
    return out


def twiml(stream_url=None, client=None, advisor_number=None):
    """TwiML for an incoming call: recording notice, media stream to us, then ring the advisor."""
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<Response>', f'<Say>{escape(RECORDING_NOTICE)}</Say>']
    if stream_url and client:
        parts += ['<Start>', f'<Stream url={quoteattr(stream_url)} track="inbound_track">',
                  f'<Parameter name="client" value={quoteattr(client)}/>', '</Stream>', '</Start>']
    if advisor_number:
        parts.append(f'<Dial>{escape(advisor_number)}</Dial>')
    elif stream_url and client:
        # One-phone demo: no advisor line to dial, the advisor reads the cards in a browser.
        # <Start><Stream> does not block, so without a verb here Twilio would disconnect at
        # once and the audio would stop; the Pause is what holds the caller's line open.
        parts.append(f'<Pause length="{HOLD_SECONDS}"/>')
    else:
        parts += ['<Say>Your advisor cannot take the call right now. Please try again later.</Say>', '<Hangup/>']
    parts.append('</Response>')
    return '\n'.join(parts)


# --- the session ----------------------------------------------------------------------

class Session:
    """One call's audio -> ElevenLabs realtime STT -> transcript and answer events.

    on_event: async callable taking an event dict (e.g. state.broadcast).
    answer:   callable(text) -> {'answers': [...], 'found': bool}, run in a thread.
    Never raises into the caller: connection problems become 'listener_error' events and
    the audio is dropped, so a failing listener cannot take the call or the API down.
    """

    def __init__(self, client_ref, on_event, answer, fmt='ulaw_8000', source='twilio', key=None,
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
            if is_question(text) and text != self.last_answered:
                self.last_answered = text
                task = asyncio.create_task(self._answer(text))
                self.answer_tasks.add(task)
                task.add_done_callback(self.answer_tasks.discard)
        elif 'error' in kind:
            await self.emit({'type': 'listener_error', 'error': data.get('error') or kind})

    async def _answer(self, text):
        try:
            result = await asyncio.to_thread(self.answer, text)
        except Exception as e:
            await self.emit({'type': 'listener_error', 'error': f'answering failed: {type(e).__name__}'})
            return
        await self.emit({'type': 'answer', 'question': text, **result})

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
