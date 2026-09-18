import json
import re

import pytest

from backend.data import load
from backend.excustody import CLIENTS_OUT, SECURITIES_OUT, SOURCES_OUT, load_external, parse_row
from backend.facts import compute


@pytest.fixture(scope='module')
def external():
    with open(CLIENTS_OUT, encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture(scope='module')
def store():
    s = load()
    load_external(s)
    return s


def test_all_ten_reports_imported(external):
    assert [c['ClientRef'] for c in external] == [f'EXT-{n:02d}' for n in range(1, 11)]
    for c in external:
        p = c['Portfolios'][0]
        assert p['SecurityPositions'] and p['AccountPositions'], c['ClientRef']
        assert p['InvestmentServiceName'] == 'External custody'


def test_weights_sum_to_one_and_totals_reconcile(external):
    for c in external:
        p = c['Portfolios'][0]
        rows = p['SecurityPositions'] + p['AccountPositions']
        assert sum(r['PortfolioValuePercentage'] for r in rows) == pytest.approx(1, abs=0.001), c['ClientRef']
        summed = sum(r['TotalAmountInPortfolioCurrency'] for r in rows)
        assert summed == pytest.approx(c['AssetsUnderManagementInDefaultCurrency'], rel=0.005), c['ClientRef']
        # The report's own weights agree with ours to rounding.
        for r in rows:
            assert r['PortfolioValuePercentage'] == pytest.approx(r['ReportedWeight'], abs=0.0006)


def test_every_position_has_a_source(external):
    with open(SOURCES_OUT, encoding='utf-8') as f:
        sources = json.load(f)
    for c in external:
        p = c['Portfolios'][0]
        assert len(sources[c['ClientRef']]['positions']) == len(p['SecurityPositions']) + len(p['AccountPositions'])
        assert not sources[c['ClientRef']]['unparsed']


def test_no_iban_is_carried_over():
    for path in (CLIENTS_OUT, SOURCES_OUT, SECURITIES_OUT):
        text = path.read_text(encoding='utf-8')
        assert not re.search(r'\b[A-Z]{2}\d{2}(?: [A-Z0-9]{4}){3,}', text), path


def test_synthetic_securities_do_not_clash_with_reference(store):
    with open(SECURITIES_OUT, encoding='utf-8') as f:
        synthetic = json.load(f)
    assert all(s['Id'] < 0 for s in synthetic)
    assert all(store.securities[s['Id']]['Isin'] == s['Isin'] for s in synthetic)


def test_briefing_engine_runs_on_every_external_client(store):
    for n in range(1, 11):
        facts = compute(store.client(f'EXT-{n:02d}'), store)
        assert {'who', 'development'} <= {f.slot for f in facts}
        assert all(f.source for f in facts)


def test_row_parser_handles_accounts_and_securities():
    account = ['EUR', "34'775.43", 'Privatkonto EUR', 'CH66 0483 5012 3456 7814 5', '0.9420', '31.12.25', "32'758",
               '1.60 %']
    row = parse_row(account)
    assert row['is_account'] and row['value'] == 32758 and row['weight'] == 0.016
    security = ['USD', '570', 'Akt Amazon.com Inc.', '2 000 654 / US0231351067', '202.27', '235.64', '31.12.25',
                "114'638", '5.59 %']
    row = parse_row(security)
    assert row['isin'] == 'US0231351067' and row['valor'] == '2000654' and row['numbers'] == [202.27, 235.64]
    assert parse_row(['USD', '570', 'broken row', '5.59 %']) is None
