"""Answer a client's question during a call with the facts that fit it — never new text.

Three layers, first one that finds something wins:

1. Question type, instant. Open questions ("what happened", "why", "explain", "tell me
   more") get the market headline, the largest hit and what held up. Advice questions
   ("should I sell") get the playbook's guidance and what held up — the advisor
   answers those, the card only prepares them.
2. Apertus picks fact ids. It sees the question and the numbered facts and may only
   return numbers, so it chooses but never writes; unknown numbers are dropped.
   Skipped when the LLM is off, and bounded by a timeout so it never stalls the call.
3. Keywords, with everyday words mapped to the words the facts use.
"""

import json
import re
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeout

from .llm import LLMUnavailable, chat

MAX_ANSWERS = 3
LLM_TIMEOUT = 4.0
_POOL = ThreadPoolExecutor(max_workers=2)

SYNONYMS = {
    'tech': 'information technology', 'technology': 'information technology',
    'lost': 'about', 'lose': 'about', 'loss': 'about', 'losses': 'about', 'down': 'about',
    'dollar': 'dollar', 'usd': 'dollar', 'euro': 'euro', 'franc': 'franc', 'currency': 'dollar',
    'gold': 'gold', 'bonds': 'bonds', 'bond': 'bonds', 'cash': 'cash', 'risk': 'volatility',
    'rules': 'suitability', 'compliance': 'suitability', 'hedged': 'hedged', 'hedge': 'hedged',
    'safe': 'holding', 'held': 'holding', 'performance': 'value', 'year': '12 months',
    'pharma': 'health care', 'health': 'health care', 'banks': 'financials', 'crypto': 'bitcoin',
    'proposal': 'proposal', 'orders': 'orders', 'esg': 'esg', 'sustainable': 'esg',
}
STOP = {'the', 'a', 'an', 'my', 'i', 'is', 'are', 'was', 'were', 'what', 'how', 'did', 'do', 'does', 'on', 'in',
        'of', 'to', 'have', 'has', 'me', 'we', 'you', 'and', 'or', 'about', 'today', 'with', 'for', "it's", 'it',
        'there', 'this', 'that', 'these', 'be', 'any', 'more', 'much', 'can', 'could', 'would', 'please', 'tell',
        'explain', 'explanation', 'depth', 'in-depth', 'detail', 'details', 'happened', 'happening', 'going',
        'why', 'so', 'just', 'really', 'also', 'well', 'as', 'at', 'its', 'our', 'your', 'get', 'got'}
WORD = re.compile(r"[a-z][a-z'-]*")

OPEN_QUESTION = re.compile(r"\b(what(?:'s| is| has)? (?:happen|going on)|why|explain|explanation|in[- ]depth|"
                           r"tell me more|more detail|what'?s behind|what caused|what happened)", re.IGNORECASE)
CHANGES_QUESTION = re.compile(r'\b(chang\w*|proposal|bought|sold|trades?|traded|orders?|rebalanc\w*|last week|'
                              r'what did you do)\b', re.IGNORECASE)
ADVICE_QUESTION = re.compile(r'\b(should i|shall i|do i need to|must i|sell|buy|get out|move (?:it|everything)|'
                             r'what (?:do|should) (?:i|we) do)\b', re.IGNORECASE)

SYSTEM = """You help a Swiss private-banking advisor who is on the phone with a client.
You get the client's question and a numbered list of facts about this client.
Pick the facts that directly answer the question, most relevant first, at most 3.
An unrelated fact is worse than none: if no fact is about what was asked, return an empty list.
- "What happened", "why", "explain" questions: the market headline, the largest losses, what held up.
- Advice questions ("should I sell?"): the talking points and what held up; never pick a fact as advice itself.
- If nothing answers the question, pick nothing.
Return JSON only: {"facts": [<numbers>]}"""


def _card(f):
    return {'text': f.text, 'source': f.source, 'fact': f.id}


def _pick(facts, plan):
    """plan: [(slot or id prefix, how many)] -> the highest-weight facts of each, in plan order."""
    out = []
    for key, n in plan:
        matching = [f for f in facts if (f.slot == key or f.id == key or f.id.startswith(key + '.')) and f not in out]
        out += sorted(matching, key=lambda f: -f.weight)[:n]
    return out[:MAX_ANSWERS]


def by_llm(facts, question):
    """Fact ids chosen by Apertus, validated against the list; [] on any failure."""
    listing = '\n'.join(f'{i}. [{f.slot}] {f.text}' for i, f in enumerate(facts, 1))
    messages = [{'role': 'system', 'content': SYSTEM},
                {'role': 'user', 'content': f'Question: {question}\n\nFacts:\n{listing}'}]
    try:
        raw, _ = _POOL.submit(chat, messages, 0.0, 60).result(timeout=LLM_TIMEOUT)
        picked = json.loads(raw[raw.find('{'):raw.rfind('}') + 1])['facts']
    except (FutureTimeout, LLMUnavailable, ValueError, KeyError, TypeError):
        return []
    out = []
    for n in picked if isinstance(picked, list) else []:
        try:
            f = facts[int(n) - 1]
        except (ValueError, TypeError, IndexError):
            continue
        if int(n) >= 1 and f not in out:
            out.append(f)
    return out[:MAX_ANSWERS]


def by_type(facts, question):
    if OPEN_QUESTION.search(question):
        # The headline first: it is the only fact that says what happened, not just what it did.
        return _pick(facts, [('news', 1), ('digest', 1), ('holding', 1)]) or _pick(facts, [('reason', 1)])
    if CHANGES_QUESTION.search(question):
        return _pick(facts, [('watch.last_proposal', 1), ('actions.rejected', 1), ('health.order_warnings', 1)])
    if ADVICE_QUESTION.search(question):
        return _pick(facts, [('talk', 2), ('holding', 1)])
    return []


def topics(question):
    """The subject words of a question, in the facts' vocabulary (e.g. 'sustainable' -> 'esg')."""
    return {SYNONYMS[w] for w in WORD.findall(question.lower()) if w in SYNONYMS and SYNONYMS[w] != 'about'}


def on_topic(chosen, question):
    """False when the question names a subject and none of the chosen facts mention it."""
    wanted = topics(question)
    return not wanted or any(t in f.text.lower() for f in chosen for t in wanted)


def by_keywords(facts, question):
    terms = {SYNONYMS.get(w, w) for w in WORD.findall(question.lower()) if w not in STOP and len(w) > 2}
    scored = []
    for f in facts:
        text = f.text.lower()
        score = sum(2 if ' ' in t else 1 for t in terms if t in text)
        if score:
            scored.append((score, f.slot in ('digest', 'holding', 'reason'), f))
    scored.sort(key=lambda s: (-s[0], not s[1]))
    out = []
    for _, _, f in scored:
        if f not in out:
            out.append(f)
    return out[:2]


def answer(facts, question, use_llm=True):
    """{'answers': [{text, source, fact}], 'found': bool, 'method': 'type' | 'llm' | 'keywords' | 'none'}."""
    seen, unique = set(), []
    for f in facts:
        # The call's "Open issue: ..." repeats a health fact word for word; keep one of them.
        key = re.sub(r'^Open issue:\s*', '', f.text)
        if f.id not in seen and key not in seen and f.slot != 'caller':
            seen.update((f.id, key))
            unique.append(f)
    for method, finder in (('type', by_type), ('llm', by_llm if use_llm else None), ('keywords', by_keywords)):
        if finder is None:
            continue
        chosen = finder(unique, question)
        if chosen and (method == 'type' or on_topic(chosen, question)):
            return {'answers': [_card(f) for f in chosen], 'found': True, 'method': method}
    return {'answers': [], 'found': False, 'method': 'none'}
