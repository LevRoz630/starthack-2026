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


@pytest.fixture(scope='module')
def ask_market():
    store = load()
    market = load_scenario('tech-selloff')
    client = store.client('CASE-043')
    facts = call_facts(client, store, market)[0] + [f for f in compute(client, store) if f.slot != 'who']
    graph = reasoning.build(client, store, market)
    return lambda q: answer(facts, q, use_llm=False, graph=graph, market=market)


@pytest.mark.parametrize('question, first', [
    ('What do you think about the copper market?', 'Copper −1.9% today.'),
    ('What do you think about gold?', 'Gold +1.4% today.'),
    ('How is oil doing?', 'Energy −0.3% today.'),
    ("How's the dollar doing?", 'The dollar −1.2% against the franc today.'),
    ('What do you think about crypto?', 'Bitcoin −6.5% today.'),
])
def test_market_views_are_ready_for_every_market(ask_market, question, first):
    r = ask_market(question)
    assert r['method'] == 'market_view' and r['answers'][0]['text'] == first
    assert all(a['source'] for a in r['answers'])


@pytest.mark.parametrize('question', ['Is there any way we can get more cash?', 'I want to buy a new house',
                                      'Can I take out 50000 francs?'])
def test_cash_needs_get_cash_on_hand_and_what_could_be_freed(ask_market, question):
    r = ask_market(question)
    assert r['method'] == 'liquidity'
    assert r['answers'][0]['text'].startswith('Cash on hand')
    assert any('could be freed by selling' in a['text'] for a in r['answers'])


def test_portfolio_today_is_the_clients_day_not_a_market_view():
    facts, s, m, c, g = _waldo()
    r = answer(facts, "Hey, how's my portfolio doing, anything interesting that happened in the market today?",
               use_llm=False, graph=g, market=m, store=s, client=c)
    assert r['method'] == 'portfolio_today'
    assert 'today' in r['answers'][0]['text']


def test_buying_a_market_shows_its_risk_and_what_to_ask_first():
    facts, s, m, c, g = _waldo()
    r = answer(facts, 'What do you think about buying gold?', use_llm=False, graph=g, market=m, store=s, client=c)
    texts = [a['text'] for a in r['answers']]
    assert any(t.startswith('Risk: gold products') and 'risk class' in t for t in texts)
    assert any(t.startswith('Ask first:') for t in texts)


def test_fact_bank_covers_every_market_once():
    from backend.marketview import fact_bank
    facts, s, m, c, g = _waldo()
    bank = fact_bank(facts, m, s, c)
    ids = [f.id for f in bank]
    assert len(ids) == len(set(ids))
    assert 'risk.product.copper' in ids and 'suggest.ask_first' in ids


def _waldo():
    s = load()
    m = load_scenario('tech-selloff')
    c = s.client('CASE-043')
    facts = call_facts(c, s, m)[0] + [f for f in compute(c, s) if f.slot != 'who']
    return facts, s, m, c, reasoning.build(c, s, m)


@pytest.mark.parametrize('question, first', [
    ("What's the bank's house view?", 'The banks favour'),
    ('What are the banks saying at the moment?', 'The banks favour'),
    ("What's your view on gold?", 'House views on gold: overweight'),
    ('What do the experts think about tech?', 'House views on tech'),
    ("What's your outlook for the US market?", 'House views on the US market'),
    ('What do the experts say about China?', 'House views on China'),
])
def test_house_views_are_quoted_with_the_banks_positions(question, first):
    facts, s, m, c, g = _waldo()
    r = answer(facts, question, use_llm=False, graph=g, market=m, store=s, client=c)
    assert r['method'] == 'house_view'
    assert r['answers'][0]['text'].startswith(first)
    assert all('Latin American' not in a['text'] for a in r['answers'])


def test_where_to_invest_gets_the_positioning_and_what_to_ask_first():
    facts, s, m, c, g = _waldo()
    r = answer(facts, 'Where should I invest right now?', use_llm=False, graph=g, market=m, store=s, client=c)
    assert r['answers'][0]['text'].startswith('The banks favour')
    assert r['answers'][-1]['text'].startswith('Ask first:')


def test_the_view_on_banks_is_about_the_sector():
    facts, s, m, c, g = _waldo()
    r = answer(facts, "What's the view on banks?", use_llm=False, graph=g, market=m, store=s, client=c)
    assert 'Financials' in r['answers'][0]['text']


def test_house_views_state_a_stance():
    from backend.outlook import cio, stance
    assert stance('We therefore downgrade utilities to neutral.') == 'neutral'
    assert stance('We remain Underweight real estate and consumer staples.') == 'underweight'
    assert stance('This is one of the reasons why we’ve upgraded gold to overweight.') == 'overweight'
    assert len(cio()['items']) >= 40


@pytest.mark.parametrize('said, wanted', [
    ('Hey how is my portfolio doing', True),
    ("I'm thinking about buying gold", True),
    ('Give me the house view on tech', True),
    ('I would like to hear your house view', True),
    ('I want to buy a new house', True),
    ('I played golf in Germany last week', False),
    ('Send me the statement by email', False),
])
def test_statements_that_still_want_a_card_mid_call(said, wanted):
    from backend.answers import worth_a_card
    assert worth_a_card(said) is wanted


def test_the_listener_answers_a_spoken_statement_that_wants_a_card():
    import asyncio
    import json
    from backend.listener import Session
    events, asked = [], []

    async def emit(e):
        events.append(e)

    async def run():
        s = Session('CASE-043', emit, lambda t: asked.append(t) or {'answers': [], 'found': True}, key='x')
        for text in ["I'm thinking about buying gold", 'Give me the house view on tech', 'Nice weather today']:
            await s._handle(json.dumps({'message_type': 'committed_transcript', 'text': text}))
            await asyncio.sleep(0.05)

    asyncio.run(run())
    assert asked == ["I'm thinking about buying gold", 'Give me the house view on tech']
