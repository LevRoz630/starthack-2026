import asyncio
import json

import pytest

from backend import demo
from backend.answers import answer, small_talk_only
from backend.listener import is_question


@pytest.mark.parametrize('text', ['How are you?', 'Hi, how are you doing today?', 'Is this a good time?',
                                  'How can I help you today?', 'Thanks so much, talk soon.', 'Can you hear me?',
                                  'Nice weather today, how is the golf?'])
def test_small_talk_gets_no_card(text):
    assert small_talk_only(text) and not is_question(text)
    assert answer([], text) == {'answers': [], 'found': False, 'method': 'small_talk'}


@pytest.mark.parametrize('text', ["Morning, it's Walter. Quick one before my first lesson. How much did today cost me?",
                                  'Right. And how much cash do I have with you?', 'How is my portfolio doing?'])
def test_a_question_inside_small_talk_is_still_answered(text):
    assert not small_talk_only(text) and is_question(text)


class FakeSession:
    def __init__(self, on_event):
        self.on_event = on_event

    async def start(self):
        pass

    async def send_audio(self, chunk):
        pass

    async def close(self):
        pass


@pytest.fixture
def two_lines(monkeypatch, tmp_path):
    pcm = tmp_path / 'line.pcm'
    pcm.write_bytes(bytes(640))
    script = {'client': 'CASE-045', 'client_voice': 'v', 'hangup_after': 0, 'ring_timeout': 5, 'turn_timeout': 5,
              'answer_wait': 0.05,
              'lines': [{'text': 'How much did today cost me?', 'pause_before': 0},
                        {'text': 'And how much cash do I have with you?', 'pause_before': 0}]}
    monkeypatch.setattr(demo, 'load_script', lambda name: script)
    monkeypatch.setattr(demo, 'prepare', lambda s: [{**line, 'pcm': pcm, 'mp3': tmp_path / ('a' * 20 + '.mp3'),
                                                      'seconds': 0.02} for line in s['lines']])
    monkeypatch.setattr(demo, 'RUNS_DIR', tmp_path / 'runs')
    monkeypatch.setattr(demo, 'CHUNK_SECONDS', 0.005)
    return tmp_path


def _run(events, answered, stop, next_turn, on_turn):
    async def broadcast(e):
        events.append(e)
        if e['type'] == 'incoming_call':
            asyncio.get_running_loop().call_later(0.01, answered.set)
        if e['type'] == 'demo_turn':
            on_turn()
    return demo.run('walter', broadcast=broadcast, ring=lambda ref: {'client': ref},
                    make_session=lambda ref, on_event: FakeSession(on_event), set_market=None,
                    answered=answered, stop=stop, audio_url=lambda p: p.name, next_turn=next_turn)


def test_the_client_waits_for_the_advisors_turn(two_lines):
    async def scenario():
        events, answered, stop, nxt = [], asyncio.Event(), asyncio.Event(), asyncio.Event()
        turn_at = {}

        def on_turn():
            turn_at['n'] = len(events)
            asyncio.get_running_loop().call_later(0.2, nxt.set)   # the advisor talks, then stops
        path = await _run(events, answered, stop, nxt, on_turn)
        types = [e['type'] for e in events]
        audio = [i for i, t in enumerate(types) if t == 'demo_audio']
        assert len(audio) == 2 and audio[0] < turn_at['n'] - 1 < audio[1]
        saved = json.loads(path.read_text(encoding='utf-8'))['events']
        assert any(e['event']['type'] == '_turn' for e in saved)
        assert types[-1] == 'demo_finished' and events[-1]['result'] == 'done'
    asyncio.run(scenario())


def test_end_call_during_the_turn_stops_at_once_and_keeps_the_replay(two_lines):
    (two_lines / 'runs').mkdir()
    (two_lines / 'runs' / 'walter-latest.json').write_text('{"events": []}', encoding='utf-8')

    async def scenario():
        events, answered, stop, nxt = [], asyncio.Event(), asyncio.Event(), asyncio.Event()

        def on_turn():   # End call: what POST /demo/stop does
            stop.set()
            nxt.set()
        await asyncio.wait_for(_run(events, answered, stop, nxt, on_turn), 3)
        assert [e['type'] for e in events].count('demo_audio') == 1
        assert events[-1]['result'] == 'stopped'
    asyncio.run(scenario())
    assert (two_lines / 'runs' / 'walter-latest.json').read_text(encoding='utf-8') == '{"events": []}'


def test_replay_waits_at_the_advisors_turn(two_lines):
    runs = two_lines / 'runs'
    runs.mkdir()
    saved = {'events': [
        {'t': 0.0, 'event': {'type': 'incoming_call', 'briefing': {}}},
        {'t': 0.01, 'event': {'type': '_answered'}},
        {'t': 0.02, 'event': {'type': 'demo_turn', 'client': 'CASE-045'}},
        {'t': 0.03, 'event': {'type': '_turn'}},
        {'t': 0.04, 'event': {'type': 'demo_audio', 'client': 'CASE-045', 'url': 'x', 'text': 'second line'}}]}
    (runs / 'walter-latest.json').write_text(json.dumps(saved), encoding='utf-8')

    async def scenario():
        out, answered, stop, nxt = [], asyncio.Event(), asyncio.Event(), asyncio.Event()

        async def broadcast(e):
            out.append((asyncio.get_running_loop().time(), e['type']))
            if e['type'] == 'incoming_call':
                answered.set()
        loop = asyncio.get_running_loop()
        loop.call_later(0.3, nxt.set)
        start = loop.time()
        await demo.replay('walter', broadcast=broadcast, answered=answered, stop=stop, next_turn=nxt)
        second = next(t for t, kind in out if kind == 'demo_audio')
        assert second - start >= 0.28      # held until the advisor's turn was handed back
    asyncio.run(scenario())
