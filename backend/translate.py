"""German → English through Supertext (Swiss-hosted), with a local cache.

Every translation is cached in data/translations/cache.json, keyed by
sha256(source|target|text), so reruns and tests cost nothing and work offline.

    python -m backend.translate rules     # writes data/translations/rules-en.json
"""

import hashlib
import json
import sys

import requests

from .data import DATA_DIR, ROOT, env, items

URL = 'https://api.supertext.com/v1/translate/ai/text'
DIR = ROOT / 'data' / 'translations'
CACHE = DIR / 'cache.json'
RULES = DIR / 'rules-en.json'
ENGLISH = 'en-GB'
BATCH = 40

# Finance terms Supertext gets wrong on its own ("Aktienanteil" is not company equity).
GLOSSARY = {
    'Aktienanteil': 'equity share',
    'Aktienquote': 'equity allocation',
    'Anlageprofil': 'investor profile',
    'Kundenprofil': 'client profile',
    'Klumpenrisiko': 'concentration risk',
    'Fremdwährung': 'foreign currency',
    'Vermögensverwaltung': 'discretionary mandate',
    'Anlageberatung': 'investment advisory',
    'Depotberatung': 'depository advisory',
    'Vorsorge': 'pension',
    'Sollwert': 'target value',
}


class TranslationUnavailable(RuntimeError):
    pass


def _key(source, target, text):
    return hashlib.sha256(f'{source}|{target}|{text}'.encode('utf-8')).hexdigest()


def _load_cache():
    if CACHE.exists():
        with open(CACHE, encoding='utf-8') as f:
            return json.load(f)
    return {}


def _save_cache(cache):
    DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=1, sort_keys=True)


def _request(texts, source, target):
    key = env('SUPERTEXT_API_KEY')
    if not key:
        raise TranslationUnavailable('SUPERTEXT_API_KEY is not set')
    body = {'source_lang': source, 'target_lang': target, 'text': texts}
    glossary = {k: v for k, v in GLOSSARY.items() if any(k.lower() in t.lower() for t in texts)}
    if glossary and source == 'de':
        body['glossary'] = glossary
    try:
        resp = requests.post(URL, headers={'Authorization': f'Supertext-Auth-Key {key}',
                                           'Content-Type': 'application/json'},
                             data=json.dumps(body, ensure_ascii=False).encode('utf-8'), timeout=60)
        resp.raise_for_status()
        out = resp.json()['translated_text']
    except (requests.RequestException, KeyError, ValueError) as e:
        raise TranslationUnavailable(str(e)) from e
    if len(out) != len(texts):
        raise TranslationUnavailable(f'expected {len(texts)} translations, got {len(out)}')
    return out


def translate(texts, source='de', target=ENGLISH, offline=False):
    """Translate a list of strings; cached ones never hit the API.

    With offline=True, or when the API fails, uncached texts come back unchanged
    rather than raising, so a briefing never breaks on a missing translation.
    """
    cache = _load_cache()
    out, missing = [], []
    for t in texts:
        hit = cache.get(_key(source, target, t))
        out.append(hit)
        if hit is None and t and t.strip():
            missing.append(t)
    missing = list(dict.fromkeys(missing))
    if missing and not offline:
        try:
            for i in range(0, len(missing), BATCH):
                chunk = missing[i:i + BATCH]
                for src, dst in zip(chunk, _request(chunk, source, target)):
                    cache[_key(source, target, src)] = dst
        finally:
            _save_cache(cache)
    return [o if o is not None else cache.get(_key(source, target, t), t) for o, t in zip(out, texts)]


def rule_translations(clients_path=None, reference_path=None):
    """English for every suitability rule description, keyed by RuleCode."""
    with open(reference_path or DATA_DIR / 'reference.json', encoding='utf-8') as f:
        ref = json.load(f)
    with open(clients_path or DATA_DIR / 'clients.json', encoding='utf-8') as f:
        clients = json.load(f)
    german = {}
    for rule in items(ref, 'SuitabilityRules'):
        if rule.get('Description'):
            german[rule['RuleCode']] = rule['Description']
    # Violation descriptions can be more specific than the rule's (region, sector filled in).
    by_violation, seen = {}, set()
    for c in clients:
        for v in items(c, 'SuitabilityViolations'):
            seen.add(v['RuleCode'])
            if v.get('RuleDescription'):
                by_violation.setdefault(v['RuleCode'], v['RuleDescription'])
    codes = sorted(set(german) | set(by_violation) | seen)
    rule_texts = [german.get(c, '') for c in codes]
    violation_texts = [by_violation.get(c, '') for c in codes]
    rule_en = translate(rule_texts)
    violation_en = translate(violation_texts)
    out = {}
    for code, de_rule, en_rule, de_v, en_v in zip(codes, rule_texts, rule_en, violation_texts, violation_en):
        entry = {}
        if de_rule:
            entry['rule_de'], entry['rule_en'] = de_rule, en_rule
        if de_v:
            entry['violation_de'], entry['violation_en'] = de_v, en_v
        if not entry:
            entry['note'] = 'no description in the data; the rule code is the only text'
        out[code] = entry
    return out


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if argv[:1] != ['rules']:
        print(__doc__)
        return 2
    rules = rule_translations()
    DIR.mkdir(parents=True, exist_ok=True)
    with open(RULES, 'w', encoding='utf-8') as f:
        json.dump(rules, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f'wrote {RULES.relative_to(ROOT)}: {len(rules)} rule codes')
    return 0


if __name__ == '__main__':
    sys.exit(main())
