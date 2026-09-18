import pytest

from backend import reasoning
from backend.data import load
from backend.market import MarketState, load_scenario, scenarios


@pytest.fixture(scope='module')
def store():
    return load()


@pytest.fixture(scope='module')
def graph(store):
    return reasoning.build(store.client('CASE-043'), store, load_scenario('tech-selloff'))


def test_breakdown_adds_up_for_every_client(store):
    for name in scenarios():
        market = load_scenario(name)
        for ref, client in store.clients.items():
            g = reasoning.build(client, store, market)
            chain = reasoning.breakdown(g)
            if not chain:
                continue
            parts = [n for n in chain if n.startswith('topic.') or n == 'rest']
            assert sum(g.values[n] for n in parts) == pytest.approx(g.values['total'], abs=0.01), (name, ref)


def test_every_link_word_stands_for_a_real_edge(graph):
    for question in ('Where did the 12k go?', 'Why am I only down 1.4% when the S&P fell 3.2%?',
                     'Did the changes you made last week make this worse?', 'What happened?'):
        steps = reasoning.chain_answer(graph, question, use_llm=False)['answers']
        for i, step in enumerate(steps):
            if step['link']:   # joined by a real edge to some earlier step
                assert any(graph.relation(e['fact'], step['fact']) for e in steps[:i]), step


def test_versus_the_index_says_less_or_more_correctly(graph):
    r = reasoning.chain_answer(graph, 'Why am I only down 1.4% when the S&P fell 3.2%?', use_llm=False)
    assert r['method'] == 'chain:vs_index'
    texts = [s['text'] for s in r['answers']]
    assert any('moved less than the S&P 500' in t for t in texts)


def test_proposal_chain_ties_todays_loss_to_last_weeks_trades(graph):
    r = reasoning.chain_answer(graph, 'Did the changes you made last week make this worse?', use_llm=False)
    ids = [s['fact'] for s in r['answers']]
    assert ids[0] == 'proposal' and 'proposal.today' in ids
    assert not any('worse' in s['text'] or 'better' in s['text'] for s in r['answers'])   # no counterfactual claim


def test_open_questions_start_with_the_headline(graph):
    r = reasoning.chain_answer(graph, 'Is there more in-depth explanation of what happened?', use_llm=False)
    assert r['answers'][0]['fact'].startswith('news.') and r['answers'][1]['fact'] == 'total'


def test_llm_paths_must_follow_edges(graph, monkeypatch):
    monkeypatch.setattr(reasoning, 'chat', lambda *a, **kw: ('{"path": ["mix", "proposal"]}', 'apertus'))
    assert reasoning.by_llm(graph, 'why?') == []
    monkeypatch.setattr(reasoning, 'chat', lambda *a, **kw: ('{"path": ["hedged", "topic.fx.USD", "total"]}', 'apertus'))
    assert reasoning.by_llm(graph, 'why?') == ['hedged', 'topic.fx.USD', 'total']
    monkeypatch.setattr(reasoning, 'chat', lambda *a, **kw: ('{"path": ["hedged", "made-up"]}', 'apertus'))
    assert reasoning.by_llm(graph, 'why?') == []


def test_no_market_no_chain(store):
    g = reasoning.build(store.client('CASE-043'), store, MarketState())
    assert reasoning.chain_answer(g, 'Where did the money go?', use_llm=False) is None


def test_ask_endpoint_returns_a_chain(monkeypatch):
    monkeypatch.setenv('BRIEFING_LLM', '0')
    from starlette.testclient import TestClient

    from backend.api import app
    with TestClient(app) as c:
        c.post('/market/events', json={'scenario': 'tech-selloff'})
        r = c.post('/ask', json={'client': 'CASE-043', 'question': 'Where did the 12k go?'}).json()
        assert r['chain'] and r['method'] == 'chain:breakdown' and r['answers'][0]['fact'] == 'total'


def test_a_named_holding_gets_its_own_chain(graph):
    r = reasoning.chain_answer(graph, 'Why did I lose money on the NASDAQ fund?', use_llm=False)
    assert r['method'] == 'chain:holding'
    assert 'NASDAQ' in r['answers'][0]['text'] and r['answers'][1]['fact'].startswith('topic.')
