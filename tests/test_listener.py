import asyncio
import base64
import json
import os
import time

import pytest
from starlette.testclient import TestClient

from backend import listener
from backend.listener import Session, is_question


# --- a fake ElevenLabs realtime socket ------------------------------------------------

class FakeSTT:
    """Replies with `script` once the first audio chunk arrives; closes when told to."""

    def __init__(self, script):
        self.script = script
        self.sent = []
        self.queue = asyncio.Queue()

    async def send(self, message):
        self.sent.append(json.loads(message))
        if len(self.sent) == 1:
            for m in self.script:
                await self.queue.put(json.dumps(m))

    def __aiter__(self):
        return self

    async def __anext__(self):
        m = await self.queue.get()
        if m is None:
            raise StopAsyncIteration
        return m

    async def close(self):
        await self.queue.put(None)


def fake_connect(script, opened=None):
    async def connect(url, **kwargs):
        ws = FakeSTT(script)
        if opened is not None:
            opened.append((url, kwargs, ws))
        return ws
    return connect


COMMITTED = [{'message_type': 'session_started'},
             {'message_type': 'partial_transcript', 'text': 'How much have I'},
             {'message_type': 'committed_transcript', 'text': 'How much have I lost on tech?'}]


# --- what to answer -------------------------------------------------------------------

@pytest.mark.parametrize('text,expected', [
    # A question mark is the strongest signal, and the recorded golf call shows the STT
    # punctuates reliably: all three real questions ended in '?', the sign-off did not.
    ('How much have I lost on tech?', True),
    ('And my world fund, is that hit by the dollar as well?', True),
    ('What about my bonds? Are they holding up?', True),
    # No question mark: a question word or a request to be told something still counts.
    ('is my world fund hit by the dollar', True),
    ('Tell me about the bonds', True),
    # A statement is not a question. This one used to fire on the old five-word rule and
    # spent one of the advisor's cards mid-call saying nothing they had asked for.
    ('I am quite worried about all of this today', False),
    ('Great. Thanks. Talk soon.', False),
    ('okay', False), ('Thank you.', False), ('yes?', False), ('', False), ('Hmm, right', False),
])
def test_is_question(text, expected):
    assert is_question(text) is expected


# --- the session ------------------------------------------------------------------------

def run(coro):
    return asyncio.run(coro)


def test_session_answers_a_committed_question():
    events, opened = [], []

    async def on_event(e):
        events.append(e)

    async def scenario():
        s = Session('CASE-043', on_event, lambda text: {'answers': [{'text': 'IT −4.8%', 'source': 's'}],
                                                         'found': True},
                    key='test', connect=fake_connect(COMMITTED, opened))
        assert await s.start()
        await s.send_audio(b'\xff' * 3200)         # one 100 ms batch of 16 kHz PCM16
        for _ in range(50):
            if any(e['type'] == 'answer' for e in events):
                break
            await asyncio.sleep(0.01)
        await s.close()

    run(scenario())
    url, kwargs, ws = opened[0]
    assert 'audio_format=pcm_16000' in url and kwargs['additional_headers']['xi-api-key'] == 'test'
    assert ws.sent[0]['sample_rate'] == 16000 and base64.b64decode(ws.sent[0]['audio_base_64']) == b'\xff' * 3200
    kinds = [e['type'] for e in events]
    assert kinds[0] == 'listening' and kinds[-1] == 'listening_stopped'
    finals = [e for e in events if e['type'] == 'transcript' and e['final']]
    assert finals[0]['text'] == 'How much have I lost on tech?'
    answer = next(e for e in events if e['type'] == 'answer')
    assert answer['client'] == 'CASE-043' and answer['question'].startswith('How much') and answer['found']


def test_session_skips_filler_and_duplicates():
    script = [{'message_type': 'committed_transcript', 'text': 'Okay.'},
              {'message_type': 'committed_transcript', 'text': 'What about gold?'},
              {'message_type': 'committed_transcript', 'text': 'What about gold?'}]
    asked = []

    async def on_event(e):
        pass

    async def scenario():
        s = Session('CASE-043', on_event, lambda text: asked.append(text) or {'answers': [], 'found': False},
                    fmt='pcm_16000', key='test', connect=fake_connect(script))
        await s.start()
        await s.send_audio(b'\x00' * 3200)
        await asyncio.sleep(0.2)
        await s.close()

    run(scenario())
    assert asked == ['What about gold?']


def test_session_reports_connection_failure_instead_of_raising():
    events = []

    async def on_event(e):
        events.append(e)

    async def broken(url, **kwargs):
        raise OSError('no network')

    async def scenario():
        s = Session('CASE-043', on_event, lambda t: {}, key='test', connect=broken)
        assert not await s.start()
        await s.send_audio(b'\xff' * 1600)   # dropped silently
        await s.close()

    run(scenario())
    assert events[0]['type'] == 'listener_error'


def test_session_without_key_reports_error():
    events = []

    async def on_event(e):
        events.append(e)

    async def scenario():
        s = Session('CASE-043', on_event, lambda t: {}, key='', connect=fake_connect([]))
        s.key = ''
        assert not await s.start()

    run(scenario())
    assert events[0]['type'] == 'listener_error'


# --- through the API --------------------------------------------------------------------

@pytest.fixture(scope='module')
def client():
    os.environ['BRIEFING_LLM'] = '0'
    os.environ.pop('DEMO_SCENARIO', None)
    from backend.api import app
    with TestClient(app) as c:
        yield c


def _events_until_stopped(ws):
    events = []
    while True:
        e = ws.receive_json()
        events.append(e)
        if e['type'] in ('listening_stopped',):
            return events


def test_browser_listen_socket(client, monkeypatch):
    monkeypatch.setenv('ELEVENLABS_KEY', os.getenv('ELEVENLABS_KEY') or 'test')
    opened = []
    monkeypatch.setattr(listener, 'connect_stt', fake_connect(COMMITTED, opened))
    client.post('/market/events', json={'scenario': 'tech-selloff'})
    with client.websocket_connect('/ws') as phone:
        phone.receive_json()
        with client.websocket_connect('/listen?client=CASE-043') as mic:
            mic.send_bytes(b'\x00' * 3200)
            mic.send_text(json.dumps({'audio_base_64': base64.b64encode(b'\x00' * 3200).decode()}))
            time.sleep(0.3)
            mic.send_text(json.dumps({'type': 'stop'}))
        events = _events_until_stopped(phone)
    assert 'audio_format=pcm_16000' in opened[0][0]
    assert any(e['type'] == 'answer' for e in events)


def test_listen_rejects_unknown_client(client):
    from starlette.websockets import WebSocketDisconnect
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect('/listen?client=NOPE') as ws:
            ws.receive_text()


# --- live, end to end (ElevenLabs TTS -> /listen -> ElevenLabs STT -> answer) ------------

@pytest.mark.skipif(os.getenv('RUN_NETWORK_TESTS') != '1', reason='set RUN_NETWORK_TESTS=1 to call ElevenLabs')
def test_live_question_through_the_listen_socket(client):
    """A spoken question, at speaking speed, all the way to an answer card."""
    import requests
    from backend.voice import DEFAULT_VOICE, _key
    tts = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{DEFAULT_VOICE}?output_format=pcm_16000',
                        headers={'xi-api-key': _key()},
                        json={'text': 'How much have I lost on tech?', 'model_id': 'eleven_flash_v2_5'}, timeout=30)
    tts.raise_for_status()
    speech = tts.content
    client.post('/market/events', json={'scenario': 'tech-selloff'})
    with client.websocket_connect('/ws') as phone:
        phone.receive_json()
        with client.websocket_connect('/listen?client=CASE-043') as mic:
            chunk = 3200                                # 100 ms of 16 kHz PCM16
            for i in range(0, len(speech), chunk):      # real time, as the microphone sends
                mic.send_bytes(speech[i:i + chunk])
                time.sleep(0.1)
            for _ in range(20):                         # 2 s of silence closes the utterance
                mic.send_bytes(b'\x00' * chunk)
                time.sleep(0.1)
            mic.send_text(json.dumps({'type': 'stop'}))
        events = _events_until_stopped(phone)
    errors = [e for e in events if e['type'] == 'listener_error']
    assert not errors, errors
    answer = next(e for e in events if e['type'] == 'answer')
    assert 'Information Technology' in answer['answers'][0]['text']
