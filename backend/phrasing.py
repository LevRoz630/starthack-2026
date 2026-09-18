"""Turn ranked facts into a short spoken briefing, and check what the LLM wrote.

The LLM only rephrases fact sentences. Every sentence it returns must cite facts,
may only contain numbers that appear in those facts, and must not use banned
phrasing; any sentence that fails is replaced by the cited facts' own text.
"""

import hashlib
import json
import re
from dataclasses import dataclass, field

from .facts import SLOTS
from .llm import LLMUnavailable, chat

# How many facts per slot make it into the spoken briefing; the rest go on the card.
SPOKEN = {'who': 1, 'development': 1, 'health': 2, 'watch': 2, 'actions': 2}

NUMBER = re.compile(r'\d+(?:[.,]\d+)?')
QUOTED = re.compile(r'"([^"]+)"')
CITED_ID = re.compile(r'\[([^\]]+)\]')
BANNED = re.compile(r"worry|guarantee|will (?:recover|rebound)|promise|\byour (?:portfolio|holdings|investments)\b",
                    re.IGNORECASE)
# Words that add severity or causality; allowed only when the cited facts use them.
LOADED = ('critical', 'urgent', 'severe', 'alarming', 'significant', 'major', 'due to', 'because', 'caused', 'driven by')
# Qualifiers a fact carries to stay honest. If a cited fact has one, the sentence
# must keep it word for word — dropping it overstates what we measured.
CAVEATS = ('value change including deposits and withdrawals',)

SYSTEM = """You write a spoken pre-call briefing for a Swiss private-banking relationship manager about one of their clients.

Rules:
- Speak to the advisor. Refer to the client in the third person, by name.
- Use only the facts given. Add no causes, explanations, forecasts or advice beyond the listed actions.
- Copy every number exactly as written in the facts. Never compute or add numbers.
- A band and a target are different things. Keep them apart: "Liquidity is at 100.0%, outside its 0.0%-60.0% band; the target is 3.0%." Never fold one into the other, and never write a band "of" a single number.
- Keep any qualifying clause word for word, in particular "value change including deposits and withdrawals". Dropping it overstates the figure.
- One or two short sentences per section, at most 160 words in total. No markdown.
- Keep security names short, as given.

Return JSON only, in this shape:
{"sentences": [{"slot": "<section>", "text": "<sentence>", "facts": ["<fact id>", ...]}]}"""


@dataclass
class Sentence:
    slot: str
    text: str
    facts: list = field(default_factory=list)
    origin: str = 'template'


def select(facts):
    """The facts to speak, per slot, most important first."""
    chosen = {}
    for slot in SLOTS:
        ranked = sorted((f for f in facts if f.slot == slot and f.weight > 0), key=lambda f: -f.weight)
        chosen[slot] = ranked[:SPOKEN[slot]]
    return chosen


def template(chosen):
    return [Sentence(slot, f.text, [f.id]) for slot in SLOTS for f in chosen[slot]]


def numbers(text):
    return {f'{float(n.replace(",", ".")):g}' for n in NUMBER.findall(text)}


def check(sentence, by_id):
    """Why a sentence fails, or None if it may be spoken."""
    cited = [by_id[i] for i in sentence.facts if i in by_id]
    if not cited:
        return 'cites no known fact'
    extra = numbers(sentence.text) - set().union(*(numbers(f.text) for f in cited))
    if extra:
        return f'numbers not in its facts: {", ".join(sorted(extra))}'
    if BANNED.search(sentence.text):
        return 'banned phrasing'
    source_text = ' '.join(f.text for f in cited).lower()
    loaded = [w for w in LOADED if w in sentence.text.lower() and w not in source_text]
    if loaded:
        return f'adds {", ".join(loaded)}'
    # Rule names and client notes are quoted in facts and must survive word for word.
    missing = [q for f in cited for q in QUOTED.findall(f.text) if q.lower() not in sentence.text.lower()]
    if missing:
        return f'changes quoted text: {missing[0]}'
    dropped = [c for c in CAVEATS if c in source_text and c not in sentence.text.lower()]
    if dropped:
        return f'drops caveat: {dropped[0]}'
    return None


def resolve(citation, by_id):
    """Map what the LLM cited to a fact id: the id itself, "[id] text", or the fact's text."""
    if citation in by_id:
        return citation
    m = CITED_ID.search(citation)
    if m and m.group(1) in by_id:
        return m.group(1)
    text = citation.strip().rstrip('.')
    return next((i for i, f in by_id.items() if text and f.text.startswith(text)), None)


def _parse(raw, by_id):
    body = raw[raw.find('{'):raw.rfind('}') + 1]
    out = []
    for s in json.loads(body)['sentences']:
        ids = [resolve(str(c), by_id) for c in (s.get('facts') or [])]
        out.append(Sentence(s.get('slot', ''), (s.get('text') or '').strip(), [i for i in ids if i], 'llm'))
    return out


# Phrasing is deterministic in the facts, so it is worth keeping. Cleared by tests.
_CACHE = {}


def cache_key(chosen):
    """Identity of a briefing: the facts picked to be spoken, in order."""
    parts = [f'{f.id}|{f.text}' for slot in SLOTS for f in chosen[slot]]
    return hashlib.sha256('\n'.join(parts).encode('utf-8')).hexdigest()


def phrase(chosen, use_llm=True):
    """Return (sentences, provider, rejected) where rejected lists (sentence, reason)."""
    fallback = template(chosen)
    if not use_llm:
        return fallback, 'template', []
    key = cache_key(chosen)
    if key in _CACHE:
        return _CACHE[key]
    by_id = {f.id: f for slot in SLOTS for f in chosen[slot]}
    prompt = '\n'.join(f'Section "{slot}":\n' + '\n'.join(f'  [{f.id}] {f.text}' for f in chosen[slot])
                       for slot in SLOTS if chosen[slot])
    try:
        raw, provider = chat([{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': prompt}])
        drafted = _parse(raw, by_id)
    except (LLMUnavailable, ValueError, KeyError, TypeError):
        return fallback, 'template', []

    out, rejected, covered = [], [], set()
    for s in drafted:
        reason = check(s, by_id)
        if reason:
            rejected.append((s, reason))
            out.extend(Sentence(by_id[i].slot, by_id[i].text, [i]) for i in s.facts if i in by_id and i not in covered)
        else:
            out.append(s)
        covered.update(i for i in s.facts if i in by_id)
    # Facts the LLM dropped are still spoken, in their own words.
    out.extend(Sentence(f.slot, f.text, [f.id]) for f in (by_id[i] for i in by_id) if f.id not in covered)
    order = {slot: n for n, slot in enumerate(SLOTS)}
    out.sort(key=lambda s: order.get(s.slot, len(SLOTS)))
    _CACHE[key] = (out, provider, rejected)
    return _CACHE[key]
