"""Answer a client's question during a call with the facts that fit it — never new text.

Four layers, first one that finds something wins (the first needs a fact graph):

0. A chain of facts for why / where-did-it-go / versus-the-market / did-the-changes
   questions (backend/reasoning.py): every step a fact, every link a known dependency.

1. Question type, instant. Open questions ("what happened", "why", "explain", "tell me
   more") get the market headline, the largest hit and what held up. Advice questions
   ("should I sell") get the playbook's guidance and what held up — the advisor
   answers those, the card only prepares them.
2. Apertus picks fact ids. It sees the question and the numbered facts and may only
   return numbers, so it chooses but never writes; unknown numbers are dropped.
   Skipped when the LLM is off, and bounded by a timeout so it never stalls the call.
3. Keywords, with everyday words mapped to the words the facts use.
"""

import re

from . import reasoning

MAX_ANSWERS = 3
LLM_TIMEOUT = 4.0

SYNONYMS = {
    'tech': 'information technology', 'technology': 'information technology',
    'lost': 'about', 'lose': 'about', 'loss': 'about', 'losses': 'about', 'down': 'about',
    'cost': 'about', 'lost?': 'about',
    'dollar': 'dollar', 'usd': 'dollar', 'euro': 'euro', 'franc': 'franc', 'currency': 'dollar',
    'gold': 'gold', 'bonds': 'bonds', 'bond': 'bonds', 'cash': 'cash', 'risk': 'volatility',
    'rules': 'suitability', 'compliance': 'suitability', 'hedged': 'hedged', 'hedge': 'hedged',
    'safe': 'holding', 'held': 'holding', 'performance': 'value', 'year': '12 months',
    'pharma': 'health care', 'health': 'health care', 'banks': 'financials', 'crypto': 'bitcoin',
    'proposal': 'proposal', 'orders': 'orders', 'esg': 'esg', 'sustainable': 'esg',
    # Withdrawals are the second most common reason clients call, after a follow-up.
    # 'take', 'money', 'pay' and 'available' are deliberately left out: WITHDRAWAL_QUESTION
    # already classifies by phrase below, and these words are common enough in an
    # unrelated question (e.g. an advice question that just mentions "losing money") that
    # mapping them to 'cash' made only_on_topic() wrongly treat the question as being
    # about cash and drop a correct answer that never says the word.
    'withdraw': 'cash', 'withdrawal': 'cash', 'liquidity': 'cash',
}
STOP = {'the', 'a', 'an', 'my', 'i', 'is', 'are', 'was', 'were', 'what', 'how', 'did', 'do', 'does', 'on', 'in',
        'of', 'to', 'have', 'has', 'me', 'we', 'you', 'and', 'or', 'about', 'today', 'with', 'for', "it's", 'it',
        'there', 'this', 'that', 'these', 'be', 'any', 'more', 'much', 'can', 'could', 'would', 'please', 'tell',
        'explain', 'explanation', 'depth', 'in-depth', 'detail', 'details', 'happened', 'happening', 'going',
        'why', 'so', 'just', 'really', 'also', 'well', 'as', 'at', 'its', 'our', 'your', 'get', 'got'}
WORD = re.compile(r"[a-z][a-z'-]*")

# Deliberately loose: a worried client swears, abbreviates and mistypes, and
# "what the fuck is going on" must land on the same answer as "what happened?".
OPEN_QUESTION = re.compile(r"\b(going on|goin on|happening|happened|what'?s up|why|explain|explanation|in[- ]depth|"
                           r"tell me more|more detail|what'?s behind|what caused|how bad|what now)", re.IGNORECASE)
CHANGES_QUESTION = re.compile(r'\b(chang\w*|proposal|bought|sold|trades?|traded|orders?|rebalanc\w*|last week|'
                              r'what did you do)\b', re.IGNORECASE)
WITHDRAWAL_QUESTION = re.compile(r'\b(withdraw\w*|take (?:out|some|money)|pay ?out|cash out|'
                                 r'how much cash|liquidity|available cash)\b', re.IGNORECASE)
# "How much did today cost me" is the single most common opening on a call: the number
# first, then what it came from. Without this it fell through to keyword matching, which
# has no idea that "lose", "cost" and "down" all mean the same request.
AMOUNT_QUESTION = re.compile(r'\b(how much (?:did|have|has|is|was)|how bad|what (?:did|has) (?:it|today|this) cost|'
                             r'how much (?:did|have) i (?:lose|lost)|what.{0,12}(?:lost|cost me))\b', re.IGNORECASE)

# Whether the portfolio still fits the person. Risk is asked about from both directions --
# "am I too exposed" and "am I being too careful" -- and both want the same facts: what
# breaches the profile, and what the book is actually concentrated in.
RISK_FIT_QUESTION = re.compile(r'\b(too (?:cautious|careful|safe|conservative|risky|aggressive|exposed|concentrated)|'
                               r'right (?:risk|profile) for me|still (?:right|suitable)|how concentrated|'
                               r'biggest (?:position|holding)|over[- ]?exposed|'
                               r'(?:within|inside|over|above|outside) (?:my )?(?:risk )?(?:profile|limits?)|risk limits?)\b',
                               re.IGNORECASE)

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
    return {'text': f.text, 'source': f.source, 'fact': f.id, 'slot': f.slot}


# "What's my whole portfolio?" -- the client wants the picture, not today's move.
OVERVIEW_QUESTION = re.compile(
    r"\b(?:entire|whole|overall|full|total) (?:portfolio|book|picture|position|holdings?|wealth)\b"
    r"|\bwhat(?:'s| is| do i have) in my (?:portfolio|account)\b|\bwhat do i (?:own|hold|have with you)\b"
    r"|\b(?:overview|summary|summari[sz]e|big picture)\b|\bmy portfolio (?:look like|in general)\b",
    re.IGNORECASE)

FUND_NOISE = re.compile(r' UCITS ETF(?: \((?:Acc|Dist)\))?| \((?:Acc|Dist)\)|,? A/S| AG\b| SA\b| Inc\.?\b| PLC\b', re.I)


def sayable(text):
    """The card as the advisor would say it: the client's words, short fund names, the
    same numbers. The full sentence stays available as 'detail'."""
    t = FUND_NOISE.sub('', text)
    m = re.match(r'^(?:Combined )?[Pp]ortfolio value ([+−][\d.]+%) over the 12 months to \w+ \d{4} and '
                 r'([+−][\d.]+%) since (\w+ \d{4}), now (CHF [\d.,]+[km]?)', t)
    if m:
        return (f'Worth {m.group(4)} now: {m.group(1)} over the last 12 months, {m.group(2)} since {m.group(3)} '
                f'(including deposits and withdrawals).')
    m = re.match(r'^The last finalised proposal \((\d+ \w+ \d{4}), reason: [^)]*\) ordered to (.+)$', t)
    if m:
        return f'The last change was on {m.group(1)}: we agreed to {m.group(2)}'
    m = re.match(r'^(\d+) suitability errors? and (\d+) warnings? open; most serious: ', t)
    if m:
        n = int(m.group(1)) + int(m.group(2))
        return f'{n} open suitability point{"s" if n != 1 else ""} to review on the account (details on the dashboard).'
    m = re.match(r'^(\d+) of (\d+) orders from the proposal of (\d+ \w+ \d{4}) were forwarded with a warning\.?$', t)
    if m:
        return (f'{m.group(1)} of {m.group(2)} orders from the {m.group(3)} change were flagged when sent to the bank; '
                f'worth checking with operations.')
    t = t.replace(' after fund look-through', '')
    t = re.sub(r'\bof the book\b', 'of the portfolio', t)
    t = re.sub(r'^The book (is|moved)', r'The portfolio \1', t)
    t = re.sub(r'; value change including deposits and withdrawals\.$', ' (including deposits and withdrawals).', t)
    t = re.sub(r'^Risk engine for [^,]+, (\d+ \w+ \d{4}): ', r'Risk figures (\1): ', t)
    return re.sub(r'\s{2,}', ' ', t).strip()


# The bank's own bookkeeping: order routing flags, suitability rule texts, the call's open
# issue. True, and on the dashboard, but nothing an advisor can say to a client -- so they
# never answer a client's question, except an explicit "any problems with my account?".
INTERNAL = re.compile(r'^(?:health\.order_warnings|health\.violations|health\.rule|actions\.violation|issue)(?:\.|$)')


def _client_facing(result, question):
    if result.get('method') == 'problems' or PROBLEMS_QUESTION.search(question):
        return result
    kept = [a for a in result.get('answers') or [] if not INTERNAL.match(a.get('fact') or '')]
    if kept or not result.get('answers'):
        return {**result, 'answers': kept}
    return {'answers': [], 'found': False, 'method': 'none'}


def _say(result):
    for a in result.get('answers') or []:
        if a.get('text'):
            a['detail'] = a['text']
            a['text'] = sayable(a['text'])
    return result


def overview(facts, graph=None):
    """The whole portfolio in four lines: value and record, what it is made of, the
    biggest exposure, and the cash on hand."""
    cards = [_card(f) for f in _pick(facts, [('development', 1)])]
    if graph is not None and 'mix' in graph.nodes:
        mix = graph.nodes['mix']
        cards.append({'text': mix.text, 'source': mix.source, 'fact': 'mix', 'slot': 'watch'})
    cards += [_card(f) for f in _pick(facts, [('watch.concentration', 1)]) or _pick(facts, [('watch.industry', 1)])]
    cards += [_card(f) for f in _pick(facts, [('watch.liquidity', 1)])]
    return cards


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
    picked = reasoning.llm_json(messages, 'facts', LLM_TIMEOUT, max_tokens=60)
    if picked is None:
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
    if AMOUNT_QUESTION.search(question) and not topics(question):
        # Asked what it cost with no subject named: the book's number, then the two
        # biggest things inside it. With a subject named, the subject's own line is the
        # answer and by_keywords finds it.
        return _pick(facts, [('digest.total', 1), ('digest.industry', 1), ('digest.fx', 1),
                             ('digest.assetclass', 1)])
    if RISK_FIT_QUESTION.search(question):
        # Concentration questions lead with the concentration; limit questions with the
        # volatility against the profile's maximum, breached or not. Suitability rule
        # texts are compliance language and never answer a client.
        if re.search(r'concentrat\w*|one thing|single|all (?:my )?eggs', question, re.IGNORECASE):
            return _pick(facts, [('watch.concentration', 1), ('watch.industry', 1), ('health.volok', 1),
                                 ('health.vol', 1)])
        return _pick(facts, [('health.vol', 1), ('health.volok', 1), ('watch.concentration', 1),
                             ('health.prc', 1), ('health.saa', 1)])
    if ADVICE_QUESTION.search(question):
        # A client who asks "what do we do" is frightened by one day. The strongest
        # honest answer is the long record, then what is actually protecting them,
        # then what was already decided and what is still open. Coaching comes last
        # and only once: the advisor needs facts to say, not a reminder to say them.
        return _pick(facts, [('development', 1), ('holding.up', 1), ('watch.last_proposal', 1),
                             ('health.order_warnings', 1)])
    if OPEN_QUESTION.search(question):
        # What it cost comes before why: the advisor is asked for a number first.
        # One headline only — two "Behind the move" cards say nothing twice.
        return _pick(facts, [('digest.total', 1), ('digest.industry', 1), ('news', 1), ('holding.up', 1)])
    if CHANGES_QUESTION.search(question):
        return _pick(facts, [('watch.last_proposal', 1), ('actions.rejected', 1), ('health.order_warnings', 1)])
    if WITHDRAWAL_QUESTION.search(question):
        # Cash first, then what a sale would have to respect.
        return _pick(facts, [('watch.liquidity', 1), ('actions.cash', 1), ('health.violation', 1)])
    return []


def topics(question):
    """The subject words of a question, in the facts' vocabulary (e.g. 'sustainable' -> 'esg')."""
    return {SYNONYMS[w] for w in WORD.findall(question.lower()) if w in SYNONYMS and SYNONYMS[w] != 'about'}


def on_topic(chosen, question):
    """False when the question names a subject and none of the chosen facts mention it."""
    wanted = topics(question)
    return not wanted or any(t in f.text.lower() for f in chosen for t in wanted)


NUMBER = re.compile(r"\d[\d.,'\u2019]*\s*%?")


def _numbers(text):
    """The figures a sentence actually carries, normalised enough to compare."""
    return {n.replace(' ', '').rstrip('.').lstrip('0') or '0' for n in NUMBER.findall(text)}


def presentable(chosen, question=''):
    """The cards as the advisor should see them, whichever layer chose them.

    Rules the advisor's screen keeps no matter how the facts were picked.

    The reason line never answers. It is a guess at why the client is ringing, made
    before they said a word, and it is worth reading on the ringing screen. Once they
    have asked an actual question, "probably the market" is a hedge about something
    they have already told you.

    Two headlines from the same feed restate one event twice.

    And a card that carries no figure the advisor has not already read is a card
    spent for nothing: "Deploy idle liquidity: 34.2% of the book (CHF 259k) is cash"
    under "Cash on hand is CHF 259k, 34.2% of the book" is the same sentence twice.
    """
    out, headlines, seen = [], 0, set()
    for f in chosen:
        if f.slot == 'reason':
            continue
        if f.id.startswith('news'):
            headlines += 1
            if headlines > 1:
                continue
        figures = _numbers(f.text)
        if figures and figures <= seen:
            continue
        seen |= figures
        out.append(f)
    return out


def only_on_topic(chosen, question):
    """The chosen facts that actually mention what was asked about.

    on_topic() judges the set, so one matching fact used to carry unrelated ones
    onto the screen with it — "is my world fund hit by the dollar?" answered with
    the hedged share classes *and* a Health Care exposure. A card the client did
    not ask for reads as a non-sequitur during a call, so drop it: one right
    answer beats a right one next to a wrong one.
    """
    wanted = topics(question)
    if not wanted:
        return chosen
    return [f for f in chosen if any(t in f.text.lower() for t in wanted)]


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


# Pleasantries a call is full of. Stripped before deciding whether anything was asked, so
# "Morning, it's Walter. How much did today cost me?" is still answered, and "How are you?"
# gets no card at all.
SMALL_TALK = re.compile(
    r"\b(?:hi|hello|hey|morning|good (?:morning|afternoon|evening)|afternoon|evening)\b"
    r"|\bit'?s \w+(?: here| calling)?\b"
    r"|\bhow (?:are|r) (?:you|things|u)(?: doing)?(?: today)?\b"
    r"|\bhow(?:'s| is) (?:it going|life|the family|your (?:day|game|round|family)|the weather|the golf|golf|business)\b"
    r"|\bhow (?:have|'ve) you been\b|\bhow was (?:the|your) (?:weekend|day|holiday|drive|trip|flight|journey|round|game|golf|meeting)\b"
    r"|\b(?:is this|is now) a (?:good|bad) time\b|\bdo you have a (?:minute|second|moment)\b"
    r"|\bcan you hear me\b|\bare you there\b"
    r"|\bhow can i help(?: you)?(?: today)?\b|\bwhat can i do for you\b"
    r"|\bnice (?:to (?:hear from|meet|talk to) you|weather)\b"
    r"|\b(?:thanks?|thank you)(?: (?:so|very) much)?\b|\bcheers\b"
    r"|\b(?:have a )?(?:good|nice|great) (?:day|weekend|one|evening)\b"
    r"|\btalk (?:soon|later)\b|\b(?:bye|goodbye|see you)\b|\bquick one\b",
    re.IGNORECASE)


def small_talk_only(text):
    """True when nothing is left to answer once the pleasantries are taken out."""
    rest = SMALL_TALK.sub(' ', text or '')
    filler = r'\b(?:and|so|well|okay|ok|right|yes|yeah|oh|um|uh|just|you|i|today|there|again)\b'
    return not re.search(r'[a-z]{3,}', re.sub(filler, ' ', rest.lower()))


def answer(facts, question, use_llm=True, graph=None):
    """{'answers': [{text, source, fact}], 'found': bool, 'method': ...}.

    With a fact graph (backend/reasoning.py), "why / where did it go / compared with the
    market / did the changes" questions get a chain of facts first ('chain': True, and
    each step carries the link word to the previous one). Small talk gets nothing.
    """
    return _say(_client_facing(_answer(facts, question, use_llm, graph), question))


# Questions about what the client holds, answered from the holdings facts (facts.py,
# expo.*). A named subject the client does not hold gets "no gold in the portfolio": the
# holdings list is complete, so that is a fact, not a guess.
HOLDINGS_LIST = re.compile(r"\bwhich (?:funds|stocks|shares|holdings|positions|investments) do i (?:own|have|hold)\b"
                           r"|\bwhat do i (?:own|hold)\b|\bwhat(?:'s| is| are) my (?:holdings|positions)\b"
                           r"|\blist (?:my|the) (?:holdings|positions|funds)\b", re.IGNORECASE)
LARGEST = re.compile(r"\b(?:largest|biggest|main|top) (?:holding|position|investment|stock|fund|share)s?\b", re.IGNORECASE)
HOLDING_AMOUNT = re.compile(r"\bhow much (?:do i have |have i got |is |of my \w+ is |money is )?(?:in|on)\b"
                            r"|\bdo i (?:have|own|hold) (?:any )?\w|\bhow much \w+(?: \w+)? do i (?:have|own|hold)\b"
                            r"|\bwhat(?:'s| is) my (?:exposure|allocation|position) (?:to|in)\b"
                            r"|\bam i (?:in|invested in|exposed to)\b|\bhow exposed am i to\b", re.IGNORECASE)
SUBJECTS = [(r'\bbonds?\b', 'expo.asset.Bonds', 'bonds'),
            (r'\b(?:shares|stocks|equit\w*)\b', 'expo.asset.Shares', 'shares'),
            (r'\b(?:cash|liquidity)\b', 'watch.liquidity', 'cash'),
            (r'\b(?:real estate|property)\b', 'expo.asset.Real estate', 'real estate'),
            (r'\bgold\b', 'expo.holding.Gold', 'gold'), (r'\bsilver\b', 'expo.holding.Silver', 'silver'),
            (r'\b(?:crypto\w*|bitcoin|ether)\b', 'expo.holding.Crypto', 'crypto'),
            (r'\btech\w*\b', 'expo.industry.Information Technology', 'tech'),
            (r'\b(?:health ?care|pharma\w*)\b', 'expo.industry.Health Care', 'health care'),
            (r'\b(?:banks?|financials?)\b', 'expo.industry.Financials', 'financials'),
            (r'\b(?:energy|oil)\b', 'expo.industry.Energy', 'energy'),
            (r'\bindustrials?\b', 'expo.industry.Industrials', 'industrials'),
            (r'\butilit\w+\b', 'expo.industry.Utilities', 'utilities'),
            (r'\b(?:dollars?|usd)\b', 'expo.currency.US-Dollar', 'dollars'),
            (r'\beuros?\b', 'expo.currency.Euro', 'euros')]
RISK_QUESTION = re.compile(r"\b(?:biggest|main|largest|key) risks?\b|\bhow risky\b|\bvolatil\w*\b"
                           r"|\brisk(?:iness| level)? (?:of|in) my\b|\bmy risk\b", re.IGNORECASE)
RISK_LIMIT = re.compile(r'\b(?:limit|profile|allowed|suitab\w*|within|over|above|exceed\w*)\b', re.IGNORECASE)
PROBLEMS_QUESTION = re.compile(r"\b(?:problems?|issues?|anything wrong|wrong with|warnings?|compliance|violations?|"
                               r"red flags?)\b", re.IGNORECASE)
DIVERSIFIED = re.compile(r'\bdiversif\w*\b', re.IGNORECASE)
LOGISTICS = re.compile(r"\bwhen (?:should|shall|can|could) we (?:meet|talk|speak)\b"
                       r"|\b(?:appointment|lunch|coffee|schedule a)\b|\bnext meeting\b", re.IGNORECASE)


def _holdings_answer(facts, question):
    by_id = {f.id: f for f in facts}
    if HOLDINGS_LIST.search(question) and 'expo.holdings' in by_id:
        return [_card(by_id['expo.holdings'])]
    if LARGEST.search(question) and 'expo.largest' in by_id:
        return [_card(by_id['expo.largest'])]
    if HOLDING_AMOUNT.search(question):
        for pattern, fact_id, label in SUBJECTS:
            if re.search(pattern, question, re.IGNORECASE):
                if fact_id in by_id:
                    return [_card(by_id[fact_id])]
                if any(f.id.startswith('expo.') for f in facts):   # the holdings were checked
                    return [{'text': f'No {label} in the portfolio.', 'fact': 'expo.none', 'slot': 'watch',
                             'source': 'all holdings checked, including fund look-through'}]
    return []


def _answer(facts, question, use_llm=True, graph=None):
    if small_talk_only(question):
        return {'answers': [], 'found': False, 'method': 'small_talk'}
    if LOGISTICS.search(question):
        # Diary questions are the advisor's to answer; a card here would be noise.
        return {'answers': [], 'found': False, 'method': 'logistics'}
    if OVERVIEW_QUESTION.search(question) or DIVERSIFIED.search(question):
        cards = overview(facts, graph)
        if cards:
            return {'answers': cards, 'found': True, 'method': 'overview'}
    held = _holdings_answer(facts, question)
    if held:
        return {'answers': held, 'found': True, 'method': 'holdings'}
    # "Am I over my risk limit?" is about fit with the profile: by_type's risk-fit rule owns it.
    if RISK_QUESTION.search(question) and not RISK_LIMIT.search(question) and not RISK_FIT_QUESTION.search(question):
        picked = _pick(facts, [('watch.risk', 1), ('watch.concentration', 1), ('watch.risk_engine', 1),
                               ('health.vol', 1)]) or _pick(facts, [('expo.largest', 1)])
        if picked:
            return {'answers': [_card(f) for f in picked], 'found': True, 'method': 'risk'}
    if PROBLEMS_QUESTION.search(question):
        picked = _pick(facts, [('health.violations', 1), ('health.order_warnings', 1), ('health.saa', 1),
                               ('health.esg', 1), ('health.prc', 1), ('health.clear', 1)])
        if picked:
            return {'answers': [_card(f) for f in picked], 'found': True, 'method': 'problems'}
    if graph is not None:
        chained = reasoning.chain_answer(graph, question, use_llm=use_llm)
        # A chain that never mentions what was asked about ("what happened to my gold?")
        # is the generic explanation: let the later layers look for the subject instead.
        wanted = topics(question)
        if chained and (not wanted or any(t in c['text'].lower() for c in chained['answers'] for t in wanted)):
            return chained
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
        chosen = only_on_topic(finder(unique, question), question)
        if chosen and (method == 'type' or on_topic(chosen, question)):
            if method != 'type':
                chosen = only_on_topic(chosen, question)
            chosen = presentable(chosen, question)
            return {'answers': [_card(f) for f in chosen], 'found': True, 'method': method}
    return {'answers': [], 'found': False, 'method': 'none'}
