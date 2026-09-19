"""Find clients by what an advisor would type: a name, part of one, a company, or a number.

"waldo", "Wald", "Waldoo", "43", "case-043" and "Muster" all work. Accents and case are
ignored; small typos are tolerated, but weak matches are left out rather than guessed.
"""

import difflib
import re
import unicodedata

from .facts import client_name

MIN_SCORE = 0.6
SURE = 0.8      # a best match at least this good, and clearly ahead of the next, is taken as meant


def _words(text):
    ascii_text = unicodedata.normalize('NFKD', text or '').encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', ' ', ascii_text.lower()).split()


def _score(query, ref, name):
    q = ' '.join(_words(query))
    full = ' '.join(_words(name))
    ref_words = ' '.join(_words(ref))                 # 'case 043'
    number = re.search(r'(\d+)$', ref)
    if q in (full, ref_words) or q.replace(' ', '') == ref_words.replace(' ', ''):
        return 1.0
    typed, stored = re.fullmatch(r'([a-z]+) ?(\d+)', q), re.fullmatch(r'([a-z]+) (\d+)', ref_words)
    if typed and stored and typed.group(1) == stored.group(1) and int(typed.group(2)) == int(stored.group(2)):
        return 1.0                                    # 'ext 4', 'case43' -> EXT-04, CASE-043
    if number and q.isdigit() and int(q) == int(number.group(1)):
        return 0.95
    if q and (full.startswith(q) or f' {q}' in f' {full}'):
        return 0.9
    ratio = difflib.SequenceMatcher(None, q, full).ratio()
    per_word = max((difflib.SequenceMatcher(None, a, b).ratio() for a in q.split() for b in full.split()), default=0)
    return max(ratio, per_word * 0.95)


def find(store, query, limit=5):
    """[{client, name, score}] best first; [] when nothing is close enough."""
    if not _words(query):
        return []
    scored = []
    for ref, client in store.clients.items():
        name = client_name(client)
        score = _score(query, ref, name)
        if score >= MIN_SCORE:
            scored.append((score, ref, name))
    scored.sort(key=lambda s: (-s[0], s[1]))
    return [{'client': ref, 'name': name, 'score': round(score, 2)} for score, ref, name in scored[:limit]]


def best(matches):
    """The match the advisor surely meant, or None when it is ambiguous or weak."""
    if not matches or matches[0]['score'] < SURE:
        return None
    if matches[0]['score'] == 1.0 and (len(matches) == 1 or matches[1]['score'] < 1.0):
        return matches[0]['client']                   # an exact name or number wins outright
    if len(matches) > 1 and matches[1]['score'] >= matches[0]['score'] - 0.05:
        return None
    return matches[0]['client']
