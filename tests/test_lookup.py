import pytest

from backend import lookup
from backend.data import load
from backend.excustody import load_external


@pytest.fixture(scope='module')
def store():
    s = load()
    load_external(s)
    return s


@pytest.mark.parametrize('typed, expected', [
    ('waldo', 'CASE-043'), ('Wald', 'CASE-043'), ('Waldoo', 'CASE-043'), ('43', 'CASE-043'),
    ('case-043', 'CASE-043'), ('case43', 'CASE-043'), ('ext 4', 'EXT-04'), ('peter keller', 'EXT-04'),
    ('Brwn', 'CASE-038'), ('Buzz', 'CASE-027')])
def test_what_an_advisor_types_finds_the_client(store, typed, expected):
    assert lookup.best(lookup.find(store, typed)) == expected


def test_ambiguous_names_ask_instead_of_guessing(store):
    matches = lookup.find(store, 'Muster')
    assert lookup.best(matches) is None
    assert {'EXT-01', 'EXT-06'} <= {m['client'] for m in matches}


def test_nonsense_finds_nothing(store):
    assert lookup.find(store, 'xyz') == [] and lookup.find(store, '  ') == []


@pytest.fixture(scope='module')
def api():
    import os
    os.environ['BRIEFING_LLM'] = '0'
    from starlette.testclient import TestClient

    from backend.api import app
    with TestClient(app) as c:
        yield c


def test_prepare_returns_the_briefings_for_a_typed_name(api):
    api.post('/market/events', json={'scenario': 'tech-selloff'})
    r = api.get('/prepare', params={'q': 'waldo'}).json()
    assert r['client'] == 'CASE-043' and r['name'] == 'Waldo'
    assert r['briefing']['sentences'] and r['call']['sentences'] and 'temperament' in r['profile']


def test_prepare_lists_matches_when_ambiguous_and_404s_on_nothing(api):
    r = api.get('/prepare', params={'q': 'Muster'})
    assert r.status_code == 200 and r.json()['client'] is None and len(r.json()['matches']) >= 2
    picked = api.get('/prepare', params={'q': 'Muster', 'client': 'EXT-06'}).json()
    assert picked['client'] == 'EXT-06'
    assert api.get('/prepare', params={'q': 'xyz'}).status_code == 404
    assert api.get('/lookup', params={'q': '43'}).json()['best'] == 'CASE-043'
