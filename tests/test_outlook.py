"""Offline: everything here reads the cached files in data/outlook/ and data/translations/."""

import json

import pytest

from backend import translate as tr
from backend.data import load
from backend.facts import exposures
from backend.outlook import DOCS, VIEW, cio, extract_views, latest_news, outlook_facts, tag


@pytest.fixture(scope='module')
def store():
    return load()


def test_cached_translations_need_no_network(monkeypatch):
    def no_network(*a, **k):
        raise AssertionError('translate() called the API for a cached text')
    monkeypatch.setattr(tr, '_request', no_network)
    with open(tr.RULES, encoding='utf-8') as f:
        rules = json.load(f)
    code, entry = next((c, e) for c, e in rules.items() if e.get('rule_de'))
    assert tr.translate([entry['rule_de']]) == [entry['rule_en']]


def test_uncached_text_comes_back_unchanged_offline():
    assert tr.translate(['Ein Satz, den niemand übersetzt hat 4711.'], offline=True) == \
        ['Ein Satz, den niemand übersetzt hat 4711.']


def test_rule_translations_cover_every_violation_code(store):
    with open(tr.RULES, encoding='utf-8') as f:
        rules = json.load(f)
    codes = {v['RuleCode'] for c in store.clients.values() for v in (c.get('SuitabilityViolations') or [])}
    assert codes <= set(rules)
    for entry in rules.values():
        if entry.get('rule_de'):
            assert entry['rule_en']
        if entry.get('violation_de'):
            assert entry['violation_en']


def test_house_view_lines_are_copied_from_fetched_documents():
    views = cio()
    ok = {s['url'] for s in views['sources'] if s['ok']}
    assert views['items'], 'no house views cached'
    for item in views['items']:
        assert item['url'] in ok
        text = (DOCS / f'{item["doc"]}.txt').read_text(encoding='utf-8')
        assert item['text'] in text
        assert VIEW.search(item['text'])


def test_news_items_come_from_feeds_that_answered():
    news = latest_news()
    ok = {s['url'] for s in news['sources'] if s['ok']}
    assert news['items']
    for item in news['items']:
        assert item['feed'] in ok and item['link'].startswith('http')
        if item['lang'] == 'de':
            assert item['title_de']


def test_outlook_facts_quote_real_items(store):
    news, views = latest_news(), cio()
    real = {v['text'] for v in views['items']} | {n['title'] for n in news['items']}
    for ref, client in store.clients.items():
        exp = exposures(client, store)
        for fact in outlook_facts(exp['industry'], exp['total'], limit=2):
            assert fact['slot'] == 'outlook' and fact['source']
            quoted = fact['text'].split(': "', 1)[1].rstrip('"')
            assert quoted in real, (ref, fact)


def test_outlook_facts_are_empty_without_exposure():
    assert outlook_facts({}, 0) == []
    assert outlook_facts({'Information Technology': 1}, 1, news={'items': []}, views={'items': []}) == []


def test_tags_near_the_view_word_only():
    s = 'Strong fundamentals, favourable terms of trade and resilience to oil prices support emerging nations.'
    assert extract_views(s) == []
    assert tag('We therefore downgrade utilities to neutral.') == ['Utilities']
