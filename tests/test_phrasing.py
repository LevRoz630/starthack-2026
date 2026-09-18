import json

import pytest

from backend import phrasing
from backend.data import load
from backend.facts import compute
from backend.phrasing import CAVEATS, Sentence, cache_key, check, phrase, select

CAVEAT = CAVEATS[0]


@pytest.fixture(scope='module')
def store():
    return load()


@pytest.fixture
def chosen(store):
    return select(compute(store.client('CASE-038'), store))


@pytest.fixture
def by_id(chosen):
    return {f.id: f for facts in chosen.values() for f in facts}


def test_development_sentence_must_keep_its_caveat(chosen, by_id):
    fact = chosen['development'][0]
    assert CAVEAT in fact.text, 'the development fact should carry the caveat'

    kept = Sentence('development', fact.text, [fact.id])
    assert check(kept, by_id) is None

    dropped = fact.text.split(';')[0] + '.'
    assert CAVEAT not in dropped
    assert check(Sentence('development', dropped, [fact.id]), by_id) == f'drops caveat: {CAVEAT}'


def test_caveat_check_ignores_facts_that_have_none(by_id):
    fact = next(f for f in by_id.values() if CAVEAT not in f.text)
    assert check(Sentence(fact.slot, fact.text, [fact.id]), by_id) is None


def test_cache_key_follows_the_chosen_facts(chosen):
    before = cache_key(chosen)
    assert cache_key(chosen) == before
    chosen['development'][0].text += ' Extra.'
    assert cache_key(chosen) != before


def test_phrase_calls_the_llm_once_per_distinct_fact_set(chosen, monkeypatch):
    calls = []

    def fake_chat(messages, **kwargs):
        calls.append(messages)
        spoken = [{'slot': f.slot, 'text': f.text, 'facts': [f.id]}
                  for facts in chosen.values() for f in facts]
        return json.dumps({'sentences': spoken}), 'apertus'

    monkeypatch.setattr(phrasing, 'chat', fake_chat)
    phrasing._CACHE.clear()

    first, provider, _ = phrase(chosen)
    assert provider == 'apertus' and len(calls) == 1

    again, _, _ = phrase(chosen)
    assert again == first and len(calls) == 1, 'unchanged facts should not hit the LLM'

    chosen['development'][0].text += ' Extra.'
    phrase(chosen)
    assert len(calls) == 2, 'changed facts should be phrased again'

    phrasing._CACHE.clear()
