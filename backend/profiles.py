"""Client profiles: what kind of person is calling, built once from the notes.

Apertus reads each client's notes once and fills a fixed profile. Everything it
returns is validated: enums must be allowed values, every quoted phrase must be a
substring of one of the client's notes, every angle must exist in the playbook,
and evidence must point at real notes. Anything else and the whole profile falls
back to keyword rules, so nothing in a profile is invented. Facts that need no
reading (interest tags, age, risk profile, ESG, profile age) are computed in code.

Profiles are cached in data/profiles/profiles.json, keyed by ClientRef with a hash
of the inputs, so rebuilding only calls the LLM for clients whose notes changed.

    python -m backend.profiles build                 # all clients
    python -m backend.profiles build --refs CASE-043 CASE-001
    python -m backend.profiles show CASE-043
"""

import argparse
import hashlib
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date

from .data import ROOT, items, load
from .facts import day, risk_profile
from .llm import LLMUnavailable, chat

CACHE = ROOT / 'data' / 'profiles' / 'profiles.json'
PLAYBOOK = ROOT / 'data' / 'playbook.json'

TEMPERAMENTS = ('calm', 'patient', 'anxious', 'detail-oriented', 'unknown')
WANTS = ('short', 'detailed', 'unknown')

# Keyword rules, used when the LLM is unavailable or its answer fails validation.
TEMPERAMENT_WORDS = {
    'anxious': ('nervous', 'anxious', 'worr', 'uneasy', 'concerned', 'cautious', 'panic'),
    'patient': ('patient', 'long view', 'long-term', 'unconcerned', 'disciplined'),
    'detail-oriented': ('detail-oriented', 'thorough', 'comparison', 'benchmark', 'analys', 'philosophical'),
    'calm': ('calm', 'relaxed', 'composed', 'pragmatic'),
}
WANTS_WORDS = {
    'short': ('brief', 'concise', 'to the point', 'keep it short', 'short call', 'short update', 'little time'),
    'detailed': ('in detail', 'detailed', 'thorough', 'comparison', 'in-depth', 'explain', 'report'),
}
LIQUIDITY_WORDS = ('property', 'house', 'tax', 'retire', 'inherit', 'withdraw', 'donation', 'purchase',
                   'liquid', 'cash reserve', 'medical')
CONTACT_WORDS = ('contact', 'call', 'e-mail', 'email', 'business hours', 'phone', 'meeting', 'weekend',
                 'letter', 'in person')

SYSTEM = """You read a Swiss private-banking client's advisor notes and fill a fixed profile.

Return JSON only, exactly this shape:
{"temperament": "calm|patient|anxious|detail-oriented|unknown",
 "wants": "short|detailed|unknown",
 "liquidity_needs": [<note number>, ...],
 "contact_preferences": [<note number>, ...],
 "angles": ["<angle id>", ...],
 "evidence": {"temperament": [<note number>, ...], "wants": [<note number>, ...]}}

Rules:
- Use only what the notes say. If the notes do not say it, use "unknown" or an empty list.
- temperament: only if a note describes how the client reacts to markets, losses or risk.
- wants: "short" or "detailed" only if a note says how much detail or time the client wants when talking
  to the advisor. Investment preferences (sectors, ESG, dividends) say nothing about this: use "unknown".
- liquidity_needs: numbers of the notes that mention a coming need for cash (purchases, taxes, retirement,
  donations, a cash reserve).
- contact_preferences: numbers of the notes about how or when the client wants to be contacted.
- angles: pick from the given angle ids only those the notes support.
- evidence: numbers of the notes that justify temperament and wants; empty if unknown.
- Refer to notes only by their numbers."""


def playbook_angles():
    with open(PLAYBOOK, encoding='utf-8') as f:
        return {a['id']: a for a in json.load(f)['angles']}


def notes_of(client):
    return [(n.get('Note') or '').strip() for n in sorted(items(client, 'ClientNotes'),
                                                           key=lambda n: n.get('CreatedByDateUTC') or '')]


def inputs_hash(client):
    """Changes whenever anything the profile is built from changes."""
    parts = [*notes_of(client), *sorted(t.get('TagName') or '' for t in items(client, 'Tags')),
             client.get('RiskProfileName') or '', client.get('EsgProfileName') or '',
             client.get('Birthday') or '', client.get('ProfilingDateUtc') or '']
    return hashlib.sha256('\n'.join(parts).encode('utf-8')).hexdigest()[:16]


def computed_fields(client, as_of):
    """The parts of a profile that need no reading."""
    age = None
    if client.get('Birthday'):
        b = day(client['Birthday'])
        age = as_of.year - b.year - ((as_of.month, as_of.day) < (b.month, b.day))
    profiled = day(client['ProfilingDateUtc']) if client.get('ProfilingDateUtc') else None
    return {
        'interests': sorted(t.get('TagName') for t in items(client, 'Tags') if t.get('TagName')),
        'age': age,
        'risk_profile': risk_profile(client),
        'esg_preference': client.get('EsgProfileName') == 'Yes',
        'profile_assessed': profiled.isoformat() if profiled else None,
        'profile_age_years': round((as_of - profiled).days / 365.25, 1) if profiled else None,
    }


def _matching(notes, words):
    """Notes containing one of the words at a word start ('concerned' must not match 'unconcerned')."""
    pattern = re.compile(r'\b(?:' + '|'.join(re.escape(w) for w in words) + ')', re.IGNORECASE)
    return [n for n in notes if pattern.search(n)]


def keyword_profile(notes):
    """The fallback: every field comes from a note containing a keyword, or is unknown."""
    evidence, temperament, wants = {}, 'unknown', 'unknown'
    for value, words in TEMPERAMENT_WORDS.items():
        hits = _matching(notes, words)
        if hits:
            temperament, evidence['temperament'] = value, hits
            break
    for value, words in WANTS_WORDS.items():
        hits = _matching(notes, words)
        if hits:
            wants, evidence['wants'] = value, hits
            break
    liquidity = [n.rstrip('.') for n in _matching(notes, LIQUIDITY_WORDS)]
    contact = [n.rstrip('.') for n in _matching(notes, CONTACT_WORDS)]
    return {'temperament': temperament, 'wants': wants, 'liquidity_needs': liquidity,
            'contact_preferences': contact, 'angles': angles_for(temperament, liquidity), 'evidence': evidence}


def angles_for(temperament, liquidity):
    angles = []
    if temperament == 'anxious':
        angles.append('acknowledge')
    if liquidity:
        angles.append('cash_need')
    if temperament in ('patient', 'calm'):
        angles.append('long_term')
    return angles


def validate(raw, notes, known_angles):
    """The LLM's profile if every part checks out against the notes, else None and why."""
    if not isinstance(raw, dict):
        return None, 'not an object'
    if raw.get('temperament') not in TEMPERAMENTS:
        return None, f'temperament {raw.get("temperament")!r}'
    if raw.get('wants') not in WANTS:
        return None, f'wants {raw.get("wants")!r}'
    def note_refs(value):
        return isinstance(value, list) and all(isinstance(i, int) and 1 <= i <= len(notes) for i in value)

    quoted = {}
    for field in ('liquidity_needs', 'contact_preferences'):
        refs = raw.get(field) or []
        if not note_refs(refs):
            return None, f'{field} points at no note: {refs!r}'
        quoted[field] = [notes[i - 1].rstrip('.') for i in dict.fromkeys(refs)]
    angles = raw.get('angles') or []
    if not isinstance(angles, list) or any(a not in known_angles for a in angles):
        return None, f'unknown angle in {angles!r}'
    evidence = {}
    for field in ('temperament', 'wants'):
        refs = (raw.get('evidence') or {}).get(field) or []
        if not note_refs(refs):
            return None, f'evidence for {field} points at no note: {refs!r}'
        if raw[field] != 'unknown' and not refs:
            raw[field] = 'unknown'   # a claim with no note behind it is dropped, not trusted
        if refs and raw[field] != 'unknown':
            evidence[field] = [notes[i - 1] for i in refs]
    return {'temperament': raw['temperament'], 'wants': raw['wants'],
            'liquidity_needs': quoted['liquidity_needs'],
            'contact_preferences': quoted['contact_preferences'],
            'angles': angles, 'evidence': evidence}, None


def llm_profile(notes, known_angles):
    """(profile, None) from Apertus, or (None, reason) when it can't be trusted."""
    prompt = ('Angle ids: ' + ', '.join(f'{i} ("{a["text"]}")' for i, a in known_angles.items()) + '\n\nNotes:\n' +
              '\n'.join(f'{i}. {n}' for i, n in enumerate(notes, 1)))
    try:
        raw, _ = chat([{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': prompt}],
                      temperature=0.0, max_tokens=500)
        parsed = json.loads(raw[raw.find('{'):raw.rfind('}') + 1])
    except (LLMUnavailable, ValueError) as e:
        return None, f'{type(e).__name__}: {e}'[:200]
    return validate(parsed, notes, known_angles)


def build_one(client, as_of=None, use_llm=True):
    as_of = as_of or date.today()
    notes = notes_of(client)
    known = playbook_angles()
    started = time.perf_counter()
    profile, why = None, None
    if not notes:
        source = 'no-notes'
    elif use_llm:
        profile, why = llm_profile(notes, known)
        source = 'apertus' if profile else 'keywords'
    else:
        source = 'keywords'
    if profile is None:
        profile = keyword_profile(notes)
    return {'client': client['ClientRef'], 'hash': inputs_hash(client), 'source': source,
            'fallback_reason': why, 'seconds': round(time.perf_counter() - started, 2),
            **profile, **computed_fields(client, as_of)}


def load_cache():
    if not CACHE.exists():
        return {}
    with open(CACHE, encoding='utf-8') as f:
        return json.load(f)


def save_cache(cache):
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE, 'w', encoding='utf-8') as f:
        json.dump(dict(sorted(cache.items())), f, ensure_ascii=False, indent=1)


def get(client, cache=None):
    """The cached profile if its inputs are unchanged, else a keyword profile (no LLM call)."""
    cache = load_cache() if cache is None else cache
    hit = cache.get(client['ClientRef'])
    if hit and hit.get('hash') == inputs_hash(client):
        return hit
    return build_one(client, use_llm=False)


def build(store, refs=None, workers=3, use_llm=True):
    """Build profiles for refs (default all), reusing cached ones whose inputs are unchanged."""
    cache = load_cache()
    todo = [store.client(r) for r in (refs or sorted(store.clients))]
    todo = [c for c in todo if cache.get(c['ClientRef'], {}).get('hash') != inputs_hash(c)
            or (use_llm and cache[c['ClientRef']].get('source') == 'keywords' and notes_of(c))]
    # Three workers at a few seconds per call stays well under Swisscom's 5 requests/s.
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for profile in pool.map(lambda c: build_one(c, use_llm=use_llm), todo):
            cache[profile['client']] = profile
    save_cache(cache)
    return cache, [c['ClientRef'] for c in todo]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('build')
    b.add_argument('--refs', nargs='*')
    b.add_argument('--no-llm', action='store_true')
    s = sub.add_parser('show')
    s.add_argument('ref')
    args = parser.parse_args(argv)

    store = load()
    if args.cmd == 'show':
        print(json.dumps(get(store.client(args.ref)), ensure_ascii=False, indent=2))
        return 0
    started = time.perf_counter()
    cache, built = build(store, args.refs, use_llm=not args.no_llm)
    rows = [cache[r] for r in built]
    llm_rows = [r for r in rows if r['source'] != 'no-notes'] if not args.no_llm else []
    fallbacks = [r for r in rows if r['source'] == 'keywords']
    print(f'built {len(rows)} profiles in {time.perf_counter() - started:.1f} s; '
          f'apertus {sum(r["source"] == "apertus" for r in rows)}, keyword fallback {len(fallbacks)}, '
          f'no notes {sum(r["source"] == "no-notes" for r in rows)}')
    if llm_rows:
        secs = sorted(r['seconds'] for r in llm_rows)
        print(f'LLM seconds per client: median {secs[len(secs) // 2]}, max {secs[-1]}')
    for r in fallbacks:
        print(f'  fallback {r["client"]}: {r["fallback_reason"]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
