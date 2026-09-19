import re

import pytest

from backend.data import items, load
from backend.facts import compute

GERMAN = re.compile(r'\b(Anlage\w*|Vorsorge\w*|Depot\w*|Konto|Zahlen|Konsolid\w*|Abgelehnt|Entwurf|Aktie|Anteile|'
                    r'Investitionskonto|Freizügigkeit\w*)\b')
NEW = ('health.prc', 'health.esg', 'health.vol_low', 'health.order_warnings', 'watch.off_list',
       'watch.risk_engine', 'watch.last_proposal', 'watch.override', 'actions.candidates')


@pytest.fixture(scope='module')
def store():
    return load()


@pytest.fixture(scope='module')
def all_facts(store):
    return {ref: compute(client, store) for ref, client in store.clients.items()}


def test_new_facts_appear_and_are_sourced(all_facts):
    found = {prefix for facts in all_facts.values() for f in facts for prefix in NEW if f.id.startswith(prefix)}
    assert found >= {'health.esg', 'watch.risk_engine', 'watch.last_proposal', 'actions.candidates', 'watch.override'}
    for facts in all_facts.values():
        for f in facts:
            assert f.source and f.text.strip(), f


def test_overridden_rules_are_not_actions(store, all_facts):
    for ref, client in store.clients.items():
        waived = {o.get('RuleCode') for o in items(client, 'IndividualRuleOverrides')}
        for f in all_facts[ref]:
            if f.slot in ('actions', 'health') and not f.id.startswith('watch.override'):
                assert not any(f'"{code}"' in f.text for code in waived), (ref, f.text)


def test_no_blank_names_or_german(all_facts):
    for facts in all_facts.values():
        for f in facts:
            assert not re.search(r'\b(buy|sell) ,', f.text) and ', ,' not in f.text, f.text
            assert not GERMAN.search(f.text), f.text


def test_esg_fact_only_for_esg_clients(store, all_facts):
    for ref, client in store.clients.items():
        if client.get('EsgProfileName') != 'Yes':
            assert not any(f.id == 'health.esg' for f in all_facts[ref]), ref


def test_candidates_are_not_already_held(store, all_facts):
    for ref, client in store.clients.items():
        held = {sp.get('SecurityName') for p in items(client, 'Portfolios') for sp in items(p, 'SecurityPositions')}
        for f in all_facts[ref]:
            if f.id == 'actions.candidates':
                assert not any(name and name in f.text for name in held if len(name) > 25), (ref, f.text)


def test_external_clients_cite_their_custody_statement():
    from backend.data import load
    from backend.excustody import load_external
    from backend.facts import compute
    store = load()
    load_external(store)
    for f in compute(store.client('EXT-01'), store):
        assert 'clients.json' not in f.source, f
    assert any('custody statement' in f.source for f in compute(store.client('EXT-01'), store))


def test_rule_explanations_are_card_only_and_english():
    from backend.data import load
    from backend.facts import compute
    store = load()
    rules = [f for f in compute(store.client('CASE-038'), store) if f.id.startswith('health.rule.')]
    assert rules and all(f.weight == 0 and 'means:' in f.text for f in rules)


def test_every_client_gets_a_next_best_action(all_facts):
    # "Next best actions" is one of the four sections the case asks for: it may never
    # be padded, but with 54 rules and 47 clients it should also never be empty.
    without = sorted(ref for ref, facts in all_facts.items() if not any(f.slot == 'actions' for f in facts))
    assert without == []


def test_order_warning_actions_only_fire_on_a_mostly_warned_proposal(all_facts):
    warned = [f for facts in all_facts.values() for f in facts if f.id == 'actions.order_warnings']
    assert warned and len(warned) < len(all_facts) / 2
    assert all('Clear the warnings on' in f.text and 'ForwardState = 2' in f.source for f in warned)
