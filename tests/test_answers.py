import pytest

from backend import answers, reasoning
from backend.callmode import call_facts
from backend.data import load
from backend.facts import compute
from backend.market import load_scenario


@pytest.fixture(scope='module')
def store():
    return load()


@pytest.fixture(scope='module')
def facts():
    store = load()
    client = store.client('CASE-043')
    return call_facts(client, store, load_scenario('tech-selloff'))[0] + \
        [f for f in compute(client, store) if f.slot != 'who']


def ids(result):
    return [a['fact'] for a in result['answers']]


@pytest.mark.parametrize('question', [
    'Is there more in-depth explanation of what happened?', 'Why is this happening?',
    "What's going on with my portfolio?", 'Can you explain this?',
    'what the fuck is going on', 'how bad is it?'])
def test_open_questions_lead_with_what_it_cost_then_why(facts, question):
    """The advisor is asked for a number first, and the reason after it."""
    r = answers.answer(facts, question, use_llm=False)
    assert r['method'] == 'type'
    assert ids(r)[0].startswith('reason')
    assert any(i.startswith(('digest.', 'news.')) for i in ids(r)[1:])


@pytest.mark.parametrize('question', [
    'Should I sell everything?', 'so we are losing money what do we do',
    'what should we do now?'])
def test_advice_questions_answer_with_facts_not_a_script(facts, question):
    """"What do we do" is answered with this client's own record and holdings.
    The playbook line is worth at most one card, and never the first."""
    r = answers.answer(facts, question, use_llm=False)
    slots = [i.split('.')[0] for i in ids(r)]
    assert slots[0] != 'talk', f'coaching led the answer: {ids(r)}'
    assert slots.count('talk') <= 1, f'more than one coaching card: {ids(r)}'
    assert 'development' in slots, f'the long record was not offered: {ids(r)}'


def test_no_two_headlines_say_the_same_event_twice(facts):
    r = answers.answer(facts, 'what the fuck is going on', use_llm=False)
    assert len([i for i in ids(r) if i.startswith('news')]) <= 1


def test_change_questions_get_the_last_proposal(facts):
    r = answers.answer(facts, 'What did you change for me last week?', use_llm=False)
    assert ids(r)[0] == 'watch.last_proposal'


def test_the_open_issue_copy_is_not_answered_twice(facts):
    r = answers.answer(facts, 'Did the orders go through?', use_llm=False)
    texts = [a['text'].replace('Open issue: ', '') for a in r['answers']]
    assert len(texts) == len(set(texts))


def test_llm_may_only_pick_listed_facts(facts, monkeypatch):
    monkeypatch.setattr(reasoning, 'chat', lambda *a, **kw: ('{"facts": [999, "x", 3]}', 'apertus'))
    chosen = answers.by_llm([f for f in facts if f.slot != 'caller'], 'How much have I lost on tech?')
    assert len(chosen) == 1


def test_off_topic_llm_picks_are_dropped(facts, monkeypatch):
    # Apertus picks the portfolio value for an ESG question: nothing about ESG, so no answer.
    development = next(i for i, f in enumerate([f for f in facts if f.slot != 'caller'], 1) if f.slot == 'development')
    monkeypatch.setattr(reasoning, 'chat', lambda *a, **kw: (f'{{"facts": [{development}]}}', 'apertus'))
    r = answers.answer(facts, 'Is my portfolio sustainable enough?', use_llm=True)
    assert r == {'answers': [], 'found': False, 'method': 'none'}


def test_llm_failure_falls_back_to_keywords(facts, monkeypatch):
    def down(*a, **kw):
        raise reasoning.LLMUnavailable('no key')
    monkeypatch.setattr(reasoning, 'chat', down)
    r = answers.answer(facts, 'How much have I lost on tech?', use_llm=True)
    assert r['method'] == 'keywords' and 'Information Technology' in r['answers'][0]['text']


@pytest.mark.parametrize('question', [
    'Can I withdraw 50000?', 'How much cash do I have?', 'I want to take some money out.'])
def test_withdrawal_questions_get_the_cash_on_hand(facts, question):
    # Withdrawals are the second most common reason clients call; before this the
    # question fell through to the keyword layer and answered with performance.
    r = answers.answer(facts, question, use_llm=False)
    assert ids(r)[0] == 'watch.liquidity'


def test_a_named_subject_drops_the_cards_that_miss_it(facts):
    # CASE-043 holds no gold: better to say so than to answer with the generic
    # what-happened chain, which is what the subject-less layers would have returned.
    r = answers.answer(facts, 'What happened to my gold?', use_llm=False)
    assert r['found'] is False


def test_a_named_subject_is_answered_about_that_subject(facts, store):
    graph = reasoning.build(store.client('CASE-043'), store, load_scenario('tech-selloff'))
    r = answers.answer(facts, 'What about my health care funds?', use_llm=False, graph=graph)
    assert 'health care' in r['answers'][0]['text'].lower()
