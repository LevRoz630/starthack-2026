import asyncio
import json

import pytest

from backend import listener, utterance
from backend.data import ROOT

CASES = json.loads((ROOT / 'data' / 'eval' / 'utterances.json').read_text(encoding='utf-8'))['cases']


@pytest.mark.parametrize('case', CASES, ids=[c['text'][:40] for c in CASES])
def test_each_sentence_is_sorted_as_expected(case):
    assert utterance.classify(case['text']) == case['kind']


def _heard(text, answer_result):
    """What a live call pushes to the phone for one finished sentence."""
    events = []

    async def on_event(e):
        events.append(e)

    async def scenario():
        s = listener.Session('CASE-045', on_event, lambda q: answer_result, fmt='pcm_16000', key='test')
        await s._handle(json.dumps({'message_type': 'committed_transcript', 'text': text}))
        if s.answer_tasks:
            await asyncio.wait(s.answer_tasks)
    asyncio.run(scenario())
    return [e for e in events if e['type'] != 'transcript']


FOUND = {'answers': [{'text': 'About −CHF 2k today.', 'source': 's', 'fact': 'digest.total'}], 'found': True,
         'method': 'type'}
NOTHING = {'answers': [], 'found': False, 'method': 'none'}


def test_a_request_becomes_a_to_do_not_a_card():
    events = _heard('Can you send me the tax statement?', FOUND)
    assert [(e['type'], e['kind']) for e in events] == [('heard', 'request')]


def test_an_instruction_is_noted_and_never_answered():
    events = _heard('Sell the Novartis.', FOUND)
    assert [(e['type'], e['kind']) for e in events] == [('heard', 'instruction')]


def test_an_unanswerable_question_becomes_a_follow_up():
    events = _heard('What is the tax treatment of my pension fund?', NOTHING)
    assert [(e['type'], e['kind']) for e in events] == [('heard', 'follow_up')]


def test_an_answerable_question_is_a_card_and_small_talk_is_nothing():
    assert [e['type'] for e in _heard('How much did today cost me?', FOUND)] == ['answer']
    assert _heard('How are you?', FOUND) == []


def test_starting_a_call_ends_the_one_before(monkeypatch):
    monkeypatch.setenv('BRIEFING_LLM', '0')
    from starlette.testclient import TestClient

    from backend.api import app
    with TestClient(app) as c:
        first = c.post('/demo/run', json={'script': 'walter', 'mode': 'replay'})
        second = c.post('/demo/run', json={'script': 'walter', 'mode': 'replay'})
        assert first.status_code == 200 and second.status_code == 200
        c.post('/demo/stop')
