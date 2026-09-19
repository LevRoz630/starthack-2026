import json
import re

import pytest

from backend.callmode import build_call, rank_callers
from backend.profiles import PLAYBOOK   # call mode no longer reads it; profiles still does
from backend.data import load
from backend.market import MarketState, impact, load_scenario, scenarios
from backend.phrasing import BANNED

IBAN = re.compile(r'\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b')


@pytest.fixture(scope='module')
def store():
    return load()


def test_scenarios_load_and_say_whether_they_are_simulated():
    assert {'tech-selloff', 'chf-spike'} <= set(scenarios())
    for name in scenarios():
        m = load_scenario(name)
        assert m.moves
        # Only real snapshots may claim to be real.
        assert m.simulated == (not name.startswith('live-')), name


def test_unknown_tickers_are_ignored():
    m = MarketState()
    m.apply([{'ticker': 'NOPE Index', 'field': 'CHG_PCT_1D', 'value': -50}])
    assert not m.moves


def test_no_market_means_no_impact(store):
    for client in store.clients.values():
        assert impact(client, store, MarketState())['impact'] == 0


def test_hedged_holdings_take_no_currency_move(store):
    usd_only = MarketState()
    usd_only.apply([{'ticker': 'USDCHF Curncy', 'field': 'CHG_PCT_1D', 'value': -10}])
    hit = impact(store.client('CASE-043'), store, usd_only)
    assert hit['hedged']
    hedged = set(hit['hedged'])
    usd = hit['topics'][('fx', 'USD')]
    assert not hedged & set(usd.positions)


def test_call_briefings_are_sourced_and_clean(store):
    for name in [None, *scenarios()]:
        market = load_scenario(name) if name else MarketState()
        for ref in store.clients:
            b = build_call(store, ref, market)
            assert b['sentences'][0]['slot'] == 'caller'
            for s in b['sentences']:
                assert all(s['sources']), (ref, s)
                assert not IBAN.search(s['text'])


def test_playbook_texts_follow_the_claim_rules():
    with open(PLAYBOOK, encoding='utf-8') as f:
        for angle in json.load(f)['angles']:
            assert not re.search(r'\d', angle['text']), angle
            assert not BANNED.search(angle['text']), angle


def test_rank_puts_hardest_hit_first(store):
    rows = rank_callers(store, load_scenario('tech-selloff'))
    assert [r['share'] for r in rows] == sorted(r['share'] for r in rows)
    assert rows[0]['share'] < 0


GERMAN = re.compile(r'\b(Anlage\w*|Vorsorge\w*|Depot\w*|Konto|Zahlen|Konsolid\w*|Abgelehnt|Entwurf|Aktie|Anteile)\b')


def test_briefings_are_in_english(store):
    from backend.facts import compute
    market = load_scenario('tech-selloff')
    for ref, client in store.clients.items():
        texts = [f.text for f in compute(client, store)] + [s['text'] for s in build_call(store, ref, market)['sentences']]
        assert not any(GERMAN.search(t) for t in texts), ref


def test_hedging_to_chf_is_read_from_the_full_name(store):
    # "Anteile -A- Hedged CHF UBS (Irl) ... - MSCI ACWI SF UCITS ETF": the hedge is only in the prefix.
    hit = impact(store.client('CASE-043'), store, load_scenario('tech-selloff'))
    assert 'SPDR Bloomberg Global Aggregate Bond UCITS ETF' in hit['hedged_chf']


def test_the_call_carries_no_playbook_lines_or_repeated_health_check(store):
    """The advisor gets the client's own numbers, not a script telling them how to
    speak, and not the dashboard's health check repeated on the phone."""
    market = load_scenario('tech-selloff')
    for ref in list(store.clients)[:12]:
        slots = {s['slot'] for s in build_call(store, ref, market)['sentences']}
        assert 'talk' not in slots, ref
        assert 'issue' not in slots, ref
