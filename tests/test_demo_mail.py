import asyncio
import json

import pytest

from backend import demo, mailer

SMTP_VARS = ('SMTP_USER', 'SMTP_PASSWORD', 'EMAIL_TO', 'EMAIL_FROM')


@pytest.fixture
def no_smtp(monkeypatch, tmp_path):
    for var in SMTP_VARS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setattr(mailer, 'OUTBOX', tmp_path / 'outbox')
    monkeypatch.setattr(mailer, 'ROOT', tmp_path)
    return tmp_path


def test_without_settings_mail_goes_to_the_outbox(no_smtp):
    result = mailer.send('Follow-up', 'Dear Waldo,\n\nThank you.')
    assert result['sent'] is False
    eml = (no_smtp / result['outbox']).read_text(encoding='utf-8')
    assert 'Subject: Follow-up' in eml and 'Dear Waldo' in eml


def test_with_settings_mail_goes_through_smtp(monkeypatch):
    sent = {}

    class FakeSMTP:
        def __init__(self, host, port, timeout):
            sent['server'] = (host, port)

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def starttls(self):
            sent['tls'] = True

        def login(self, user, password):
            sent['login'] = user

        def send_message(self, msg):
            sent['to'] = msg['To']

    monkeypatch.setenv('SMTP_USER', 'advisor@gmail.com')
    monkeypatch.setenv('SMTP_PASSWORD', 'app-password')
    monkeypatch.setenv('EMAIL_TO', 'inbox@example.com')
    monkeypatch.setattr(mailer.smtplib, 'SMTP', FakeSMTP)
    result = mailer.send('Call note', 'Body')
    assert result == {'sent': True, 'to': 'in***@example.com'}
    assert sent == {'server': ('smtp.gmail.com', 587), 'tls': True, 'login': 'advisor@gmail.com', 'to': 'inbox@example.com'}


@pytest.fixture
def api(no_smtp, monkeypatch):
    monkeypatch.setenv('BRIEFING_LLM', '0')
    from starlette.testclient import TestClient

    from backend.api import app
    with TestClient(app) as c:
        yield c


def test_followup_send_endpoint(api):
    r = api.post('/followup/send', json={'client': 'CASE-043', 'kind': 'email', 'body': 'Dear Waldo'})
    assert r.status_code == 200 and r.json()['sent'] is False and 'Waldo' in r.json()['subject']
    assert api.post('/followup/send', json={'client': 'CASE-043', 'kind': 'fax', 'body': 'x'}).status_code == 400
    assert api.post('/followup/send', json={'client': 'NOPE', 'kind': 'note', 'body': 'x'}).status_code == 404


def test_followup_send_reports_smtp_failure(api, monkeypatch):
    def boom(*a, **kw):
        raise OSError('connection refused')
    monkeypatch.setattr(mailer, 'send', boom)
    r = api.post('/followup/send', json={'client': 'CASE-043', 'kind': 'note', 'body': 'Note'})
    assert r.status_code == 502 and 'not sent' in r.json()['error']


class FakeSession:
    def __init__(self, on_event):
        self.on_event = on_event
        self.audio = 0

    async def start(self):
        await self.on_event({'type': 'listening', 'source': 'recorded'})

    async def send_audio(self, chunk):
        self.audio += len(chunk)

    async def close(self):
        await self.on_event({'type': 'answer', 'question': 'How much have I lost on tech?', 'answers': [], 'found': False})
        await self.on_event({'type': 'listening_stopped', 'source': 'recorded'})


def test_recorded_run_and_offline_replay(monkeypatch, tmp_path):
    pcm = tmp_path / 'line.pcm'
    pcm.write_bytes(bytes(3200))
    script = {'client': 'CASE-043', 'scenario': 'tech-selloff', 'client_voice': 'v', 'hangup_after': 0,
              'ring_timeout': 5, 'lines': [{'text': 'How much have I lost on tech?', 'pause_before': 0}]}
    monkeypatch.setattr(demo, 'load_script', lambda name: script)
    monkeypatch.setattr(demo, 'prepare', lambda s: [{**s['lines'][0], 'pcm': pcm, 'mp3': tmp_path / ('a' * 20 + '.mp3'), 'seconds': 0.1}])
    monkeypatch.setattr(demo, 'RUNS_DIR', tmp_path / 'runs')

    async def no_silence(session, seconds, stop):
        return None
    monkeypatch.setattr(demo, '_silence', no_silence)

    async def scenario():
        events, answered, stop = [], asyncio.Event(), asyncio.Event()

        async def broadcast(e):
            events.append(e)
            if e['type'] == 'incoming_call':
                asyncio.get_running_loop().call_later(0.05, answered.set)

        sessions = []
        path = await demo.run('golf', broadcast=broadcast, ring=lambda ref: {'client': ref},
                              make_session=lambda ref, on_event: sessions.append(FakeSession(on_event)) or sessions[-1],
                              set_market=lambda name: {'scenario': name}, answered=answered, stop=stop,
                              audio_url=lambda p: f'/demo/audio/{p.name}')
        types = [e['type'] for e in events]
        assert types[:3] == ['demo_started', 'market', 'incoming_call']
        assert {'demo_audio', 'answer', 'call_ended', 'demo_finished'} <= set(types)
        assert sessions[0].audio == 3200
        saved = json.loads(path.read_text(encoding='utf-8'))
        assert any(item['event']['type'] == '_answered' for item in saved['events'])

        replayed = []

        async def collect(e):
            replayed.append(e)
            if e['type'] == 'incoming_call':
                asyncio.get_running_loop().call_later(0.05, answered.set)
        await demo.replay('golf', broadcast=collect, answered=answered, stop=stop)
        assert [e['type'] for e in replayed] == [t for t in types if not t.startswith('_')]
        assert all(e['replayed'] for e in replayed)

    asyncio.run(scenario())


def test_unanswered_run_does_not_replace_the_saved_replay(monkeypatch, tmp_path):
    script = {'client': 'CASE-043', 'client_voice': 'v', 'ring_timeout': 0.05, 'lines': []}
    monkeypatch.setattr(demo, 'load_script', lambda name: script)
    monkeypatch.setattr(demo, 'prepare', lambda s: [])
    monkeypatch.setattr(demo, 'RUNS_DIR', tmp_path)
    (tmp_path / 'golf-latest.json').write_text('{"events": []}', encoding='utf-8')

    async def broadcast(e):
        pass

    asyncio.run(demo.run('golf', broadcast=broadcast, ring=lambda ref: {}, make_session=None,
                         set_market=None, answered=asyncio.Event(), stop=asyncio.Event(), audio_url=str))
    assert (tmp_path / 'golf-latest.json').read_text(encoding='utf-8') == '{"events": []}'
