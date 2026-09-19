import pytest

from backend import reasoning
from backend.answers import answer
from backend.callmode import call_facts
from backend.data import load
from backend.facts import compute
from backend.market import load_scenario


@pytest.fixture(scope='module')
def ask():
    store = load()
    market = load_scenario('tech-selloff')
    cache = {}

    def run(ref, question):
        if ref not in cache:
            client = store.client(ref)
            facts = call_facts(client, store, market)[0] + [f for f in compute(client, store) if f.slot != 'who']
            cache[ref] = (facts, reasoning.build(client, store, market))
        facts, graph = cache[ref]
        return answer(facts, question, use_llm=False, graph=graph)
    return run


@pytest.mark.parametrize('ref, question, expected', [
    ('CASE-043', 'How much do I have in bonds?', 'Bonds are 22.4% of the portfolio'),
    ('CASE-043', 'Do I have any gold?', 'No gold in the portfolio.'),
    ('CASE-045', 'How much do I have in bonds?', 'No bonds in the portfolio.'),
    ('CASE-045', 'What is my largest holding?', 'Largest holding: Novartis'),
    ('CASE-045', "What's my biggest risk?", 'Novartis alone is 41.0% of the portfolio.'),
    ('CASE-043', 'Which funds do I own?', '24 holdings; the largest'),
])
def test_questions_about_what_the_client_holds(ask, ref, question, expected):
    r = ask(ref, question)
    assert r['found'] and r['answers'][0]['text'].startswith(expected), r['answers'][:1]


def test_problems_diversification_and_diary_questions(ask):
    assert ask('CASE-043', 'Are there any problems with my account?')['method'] == 'problems'
    assert ask('CASE-043', 'Am I diversified?')['method'] == 'overview'
    assert ask('CASE-043', 'When should we meet next?') == {'answers': [], 'found': False, 'method': 'logistics'}


@pytest.mark.parametrize('ref, question, expected', [
    ('CASE-045', 'Hm. Am I too concentrated in one thing?', 'Novartis alone is 41.0%'),
    ('CASE-045', 'When did we last actually change anything?', 'The last change was on 30 Aug 2026'),
    ('CASE-045', 'Am I within my risk profile?', 'Volatility is 11.3%, within the 15.0% maximum'),
    ('CASE-027', 'And am I over my risk limit?', 'Volatility is 12.2%, above the 12.0% maximum'),
])
def test_client_questions_get_sayable_answers(ask, ref, question, expected):
    r = ask(ref, question)
    assert r['answers'][0]['text'].startswith(expected), r['answers'][:1]
    # the bank's bookkeeping never answers a client's question
    assert not any('forwarded with a warning' in a['text'] or 'suitability error' in a['text'] for a in r['answers'])
