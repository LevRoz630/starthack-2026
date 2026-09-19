import asyncio
import base64
import json
import os
import time

import pytest
from starlette.testclient import TestClient

from backend import listener
from backend.listener import (Session, is_question, parse_twilio, pcm16_to_ulaw, twiml, ulaw_to_pcm16,
                              _ulaw_decode, _ulaw_encode)


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


# --- mu-law ---------------------------------------------------------------------------

def test_ulaw_code_round_trip():
    for u in range(256):
        if u == 0x7F:   # negative zero decodes to 0, which encodes as 0xFF
            continue
        assert _ulaw_encode(_ulaw_decode(u)) == u


def test_pcm_survives_ulaw_within_quantisation():
    samples = [0, 1, -1, 100, -100, 1000, -1000, 8000, -8000, 32000, -32000]
    pcm = b''.join(s.to_bytes(2, 'little', signed=True) for s in samples)
    back = ulaw_to_pcm16(pcm16_to_ulaw(pcm))
    decoded = [int.from_bytes(back[i:i + 2], 'little', signed=True) for i in range(0, len(back), 2)]
    for original, got in zip(samples, decoded):
        assert abs(original - got) <= max(8, abs(original) // 16)


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


# --- Twilio ---------------------------------------------------------------------------

def test_parse_twilio_messages():
    start = parse_twilio(json.dumps({'event': 'start', 'streamSid': 'MZ1', 'start': {
        'streamSid': 'MZ1', 'callSid': 'CA1', 'customParameters': {'client': 'CASE-043'}}}))
    assert start == {'event': 'start', 'stream_sid': 'MZ1', 'client': 'CASE-043', 'call_sid': 'CA1'}
    media = parse_twilio(json.dumps({'event': 'media', 'streamSid': 'MZ1', 'media': {
        'track': 'inbound', 'payload': base64.b64encode(b'\xff\x7f').decode()}}))
    assert media['audio'] == b'\xff\x7f' and media['track'] == 'inbound'
    assert parse_twilio(json.dumps({'event': 'stop', 'streamSid': 'MZ1'}))['event'] == 'stop'
    assert parse_twilio('not json') == {'event': None}


def test_twiml_streams_the_caller_and_dials_the_advisor():
    xml = twiml('wss://example.org/twilio/media', 'CASE-043', '+41790000000')
    assert '<Stream url="wss://example.org/twilio/media"' in xml
    assert '<Parameter name="client" value="CASE-043"/>' in xml
    assert '<Dial>+41790000000</Dial>' in xml and listener.RECORDING_NOTICE in xml
    unknown = twiml(None, None, None)
    assert '<Stream' not in unknown and '<Hangup/>' in unknown
    assert '&lt;' in twiml('wss://x/y', 'A<B', None)


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
        await s.send_audio(b'\xff' * 800)          # one 100 ms batch of mu-law
        for _ in range(50):
            if any(e['type'] == 'answer' for e in events):
                break
            await asyncio.sleep(0.01)
        await s.close()

    run(scenario())
    url, kwargs, ws = opened[0]
    assert 'audio_format=ulaw_8000' in url and kwargs['additional_headers']['xi-api-key'] == 'test'
    assert ws.sent[0]['sample_rate'] == 8000 and base64.b64decode(ws.sent[0]['audio_base_64']) == b'\xff' * 800
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


def test_twilio_voice_webhook(client, monkeypatch):
    monkeypatch.delenv('ADVISOR_NUMBER', raising=False)
    unknown = client.post('/twilio/voice', data={'From': '+41 79 999 99 99', 'CallSid': 'CA1'})
    assert unknown.headers['content-type'].startswith('application/xml')
    assert '<Stream' not in unknown.text and '<Hangup/>' in unknown.text

    monkeypatch.setenv('ADVISOR_NUMBER', '+41790000000')
    with client.websocket_connect('/ws') as ws:
        ws.receive_json()   # hello
        r = client.post('/twilio/voice', data={'From': '+41000', 'CallSid': 'CA2', 'client': 'CASE-043'},
                        headers={'X-Forwarded-Proto': 'https', 'X-Forwarded-Host': 'demo.example.org'})
        event = ws.receive_json()
    assert event['type'] == 'incoming_call' and event['briefing']['client'] == 'CASE-043'
    assert '<Stream url="wss://demo.example.org/twilio/media"' in r.text
    assert 'value="CASE-043"' in r.text and '<Dial>+41790000000</Dial>' in r.text


def _twilio_frames(audio, client_ref):
    yield {'event': 'connected', 'protocol': 'Call', 'version': '1.0.0'}
    yield {'event': 'start', 'streamSid': 'MZ1', 'start': {'streamSid': 'MZ1', 'callSid': 'CA1',
                                                           'tracks': ['inbound'],
                                                           'customParameters': {'client': client_ref}}}
    for i in range(0, len(audio), 160):     # 20 ms of mu-law 8 kHz per frame, as Twilio sends
        yield {'event': 'media', 'streamSid': 'MZ1',
               'media': {'track': 'inbound', 'payload': base64.b64encode(audio[i:i + 160]).decode()}}


def _events_until_stopped(ws):
    events = []
    while True:
        e = ws.receive_json()
        events.append(e)
        if e['type'] in ('listening_stopped',):
            return events


def test_twilio_media_stream_pushes_transcript_and_answer(client, monkeypatch):
    monkeypatch.setenv('ELEVENLABS_KEY', os.getenv('ELEVENLABS_KEY') or 'test')
    monkeypatch.setattr(listener, 'connect_stt', fake_connect(COMMITTED))
    client.post('/market/events', json={'scenario': 'tech-selloff'})
    with client.websocket_connect('/ws') as phone:
        phone.receive_json()   # hello
        with client.websocket_connect('/twilio/media') as twilio:
            for frame in _twilio_frames(b'\xff' * 1600, 'CASE-043'):
                twilio.send_text(json.dumps(frame))
            time.sleep(0.3)
            twilio.send_text(json.dumps({'event': 'stop', 'streamSid': 'MZ1'}))
        events = _events_until_stopped(phone)
    answer = next(e for e in events if e['type'] == 'answer')
    assert answer['client'] == 'CASE-043' and 'Information Technology' in answer['answers'][0]['text']
    assert any(e['type'] == 'transcript' and e['final'] for e in events)


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


# --- live, end to end (ElevenLabs TTS -> Twilio socket -> ElevenLabs STT -> answer) ------------

@pytest.mark.skipif(os.getenv('RUN_NETWORK_TESTS') != '1', reason='set RUN_NETWORK_TESTS=1 to call ElevenLabs')
def test_live_question_through_twilio_socket(client):
    import requests
    from backend.voice import DEFAULT_VOICE, _key
    tts = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{DEFAULT_VOICE}?output_format=ulaw_8000',
                        headers={'xi-api-key': _key()},
                        json={'text': 'How much have I lost on tech?', 'model_id': 'eleven_flash_v2_5'}, timeout=30)
    tts.raise_for_status()
    speech = tts.content
    client.post('/market/events', json={'scenario': 'tech-selloff'})
    with client.websocket_connect('/ws') as phone:
        phone.receive_json()
        with client.websocket_connect('/twilio/media') as twilio:
            frames = list(_twilio_frames(speech, 'CASE-043'))
            for frame in frames:                       # real time: 20 ms per frame
                twilio.send_text(json.dumps(frame))
                if frame['event'] == 'media':
                    time.sleep(0.02)
            end_of_speech = time.time()
            silence = base64.b64encode(b'\xff' * 160).decode()
            for _ in range(100):                       # 2 s of line silence after the question
                twilio.send_text(json.dumps({'event': 'media', 'streamSid': 'MZ1',
                                             'media': {'track': 'inbound', 'payload': silence}}))
                time.sleep(0.02)
            twilio.send_text(json.dumps({'event': 'stop', 'streamSid': 'MZ1'}))
        events = _events_until_stopped(phone)
    errors = [e for e in events if e['type'] == 'listener_error']
    assert not errors, errors
    answer = next(e for e in events if e['type'] == 'answer')
    assert 'Information Technology' in answer['answers'][0]['text']
    print(f'\nlive: question "{answer["question"]}" answered {answer["at"] - end_of_speech:.2f} s after speech ended')
