import json

import pytest
from starlette.testclient import TestClient

from backend.data import DATA_DIR


@pytest.fixture(scope='module')
def client():
    import os
    os.environ['BRIEFING_LLM'] = '0'
    os.environ.pop('DEMO_SCENARIO', None)
    from backend.api import app
    with TestClient(app) as c:
        yield c


def test_health_and_clients(client):
    assert client.get('/health').json()['clients'] >= 47
    rows = client.get('/clients').json()
    assert any(r['client'] == 'CASE-043' for r in rows)


def test_briefing_and_unknown_client(client):
    b = client.get('/briefing/CASE-043').json()
    assert b['phrasing'] == 'off' and b['sentences']
    assert client.get('/briefing/NOPE').status_code == 404


def test_market_event_reranks_and_pushes_to_the_phone(client):
    with client.websocket_connect('/ws') as ws:
        assert ws.receive_json()['type'] == 'hello'
        r = client.post('/market/events', json={'scenario': 'tech-selloff'}).json()
        assert r['market']['simulated'] and r['callers'][0]['share'] < 0
        assert ws.receive_json()['type'] == 'market'

        call = client.post('/call/incoming', json={'client': 'CASE-043'}).json()
        assert call['sentences'][0]['slot'] == 'caller'
        event = ws.receive_json()
        assert event['type'] == 'incoming_call' and event['briefing']['client'] == 'CASE-043'
    assert client.post('/market/events', json={'scenario': 'nope'}).status_code == 404
    assert client.post('/market/events', json={}).status_code == 400


def test_twilio_form_post_with_unknown_number(client):
    r = client.post('/call/incoming', data={'From': '+41 79 999 99 99', 'CallSid': 'CA123'})
    assert r.status_code == 404 and 'phonebook' in r.json()['error']


def test_ask_answers_from_facts(client):
    client.post('/market/events', json={'scenario': 'tech-selloff'})
    r = client.post('/ask', json={'client': 'CASE-043', 'question': 'How much have I lost on tech?'}).json()
    assert r['found'] and 'Information Technology' in r['answers'][0]['text']
    assert all(a['source'] for a in r['answers'])
    assert client.post('/ask', json={'client': 'CASE-043'}).status_code == 400


def test_upload_adds_a_test_client_and_rejects_junk(client):
    with open(DATA_DIR / 'clients.json', encoding='utf-8') as f:
        test_client = dict(json.load(f)[42], ClientRef='TEST-001')
    r = client.post('/clients', files={'file': ('test.json', json.dumps([test_client]), 'application/json')})
    assert r.json()['added'] == ['TEST-001']
    assert client.get('/briefing/TEST-001').status_code == 200
    assert client.get('/call/TEST-001').status_code == 200
    assert client.post('/clients', content=b'not json').status_code == 400
    assert client.post('/clients', json=[{'no': 'ref'}]).status_code == 400


def test_phone_app_is_served(client):
    r = client.get('/phone/')
    assert r.status_code == 200 and 'app.js' in r.text
    assert client.get('/phone/app.js').status_code == 200


def test_external_custody_clients_are_loaded(client):
    refs = {r['client'] for r in client.get('/clients').json()}
    assert {'EXT-01', 'EXT-10'} <= refs
    assert client.get('/briefing/EXT-01').status_code == 200


def test_profile_endpoint(client):
    p = client.get('/profile/CASE-001').json()
    assert p['temperament'] in ('calm', 'patient', 'anxious', 'detail-oriented', 'unknown')
    assert client.get('/profile/NOPE').status_code == 404


def test_audio_and_transcribe_without_network(client, monkeypatch):
    from backend import voice
    monkeypatch.setattr(voice, 'speak', lambda text, **kw: (b'ID3fake', 0.1))
    r = client.get('/call/CASE-043/audio')
    assert r.status_code == 200 and r.headers['content-type'] == 'audio/mpeg'
    assert client.get('/briefing/CASE-043/audio').status_code == 200
    monkeypatch.setattr(voice, 'transcribe', lambda audio, **kw: ('How much have I lost on tech?', 0.4))
    client.post('/market/events', json={'scenario': 'tech-selloff'})
    r = client.post('/transcribe', files={'file': ('q.mp3', b'fake', 'audio/mpeg')}, data={'client': 'CASE-043'}).json()
    assert r['text'].startswith('How much') and r['found']


def test_voice_failure_degrades_to_503(client, monkeypatch):
    from backend import voice

    def boom(*a, **kw):
        raise RuntimeError('no network')
    monkeypatch.setattr(voice, 'speak', boom)
    assert client.get('/call/CASE-043/audio').status_code == 503
