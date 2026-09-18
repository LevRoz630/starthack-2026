import re

import pytest

from backend.data import items, load, portfolios
from backend.facts import compute, exposures, short_name
from backend.phrasing import Sentence, check, resolve, select, template

IBAN = re.compile(r'\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b')


@pytest.fixture(scope='module')
def store():
    return load()


def test_every_client_gets_sourced_facts(store):
    for ref, client in store.clients.items():
        facts = compute(client, store)
        assert {f.slot for f in facts} >= {'who', 'development'}, ref
        assert all(f.source for f in facts), ref


def test_no_iban_leaks_into_facts(store):
    ibans = {ap.get('IBAN') for c in store.clients.values() for p in items(c, 'Portfolios')
             for ap in items(p, 'AccountPositions') if ap.get('IBAN')}
    for client in store.clients.values():
        for f in compute(client, store):
            assert not IBAN.search(f.text) and not any(i in f.text for i in ibans)


def test_exposure_matches_client_aum(store):
    for ref, client in store.clients.items():
        exp = exposures(client, store)
        aum = client.get('AssetsUnderManagementInDefaultCurrency') or 0
        assert exp['total'] == pytest.approx(aum, rel=0.01, abs=1), ref
        assert sum(exp['industry'].values()) <= exp['total'] * 1.01, ref


def test_consolidated_portfolio_is_not_double_counted(store):
    names = [p.get('InvestmentServiceName') for p in portfolios(store.client('CASE-038'))]
    assert 'Consolidated' not in names


def test_short_names():
    assert short_name('Na. u. Inh. Ti.-Aktie -B Novo Nordisk A/S') == 'Novo Nordisk A/S'
    assert short_name('Anteile -R- USD Polar Capital Funds PLC - Smart Energy Fund') == 'Smart Energy Fund'
    assert short_name('Namen-Aktie Nestle SA') == 'Nestle SA'


def test_checker_rejects_invented_numbers_and_causes(store):
    chosen = select(compute(store.client('CASE-038'), store))
    by_id = {f.id: f for fs in chosen.values() for f in fs}
    fact = chosen['development'][0]
    assert check(Sentence('development', fact.text, [fact.id]), by_id) is None
    assert 'numbers' in check(Sentence('development', 'Up 99.9% this year.', [fact.id]), by_id)
    assert 'adds' in check(Sentence('development', 'It grew because of tech.', [fact.id]), by_id)
    assert check(Sentence('development', 'Some text.', ['nope']), by_id) == 'cites no known fact'
    violation = next(f for f in by_id.values() if f.id == 'health.violations')
    assert 'quoted' in check(Sentence('health', '12 errors and 6 warnings, mostly currency.', [violation.id]), by_id)


def test_resolve_accepts_the_ways_llms_cite(store):
    chosen = select(compute(store.client('CASE-038'), store))
    by_id = {f.id: f for fs in chosen.values() for f in fs}
    fact = chosen['who'][0]
    assert resolve(fact.id, by_id) == fact.id
    assert resolve(f'[{fact.id}] {fact.text}', by_id) == fact.id
    assert resolve(fact.text.rstrip('.'), by_id) == fact.id


def test_template_speaks_every_chosen_fact(store):
    chosen = select(compute(store.client('CASE-001'), store))
    assert len(template(chosen)) == sum(len(v) for v in chosen.values())
