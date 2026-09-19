"""Chains of facts: grounded answers to "why" and "where did it go" questions.

The engine builds a small graph per client and market. Nodes are facts, each with a
source; edges are dependencies the code actually computed — a holding is part of an
industry's impact, the industry impacts add up to the book's, a hedge takes the dollar
move out, a proposal bought a holding. A chain is a path through that graph, so every
step is a fact and every "so"/"because" between steps is an edge the engine knows.

Three chains are built by code for the questions a panicking client asks:
- breakdown:  where did the loss go — the total, the largest parts, what they came
              through, what held up. The parts add up, including "everything else".
- vs_index:   why the book moved less (or more) than the S&P 500 / SMI — asset mix,
              hedges, what rose.
- proposal:   what last week's changes have to do with today — which holdings the
              last proposal bought and what they did today. No counterfactual claims.
For other questions Apertus may choose a path; it is accepted only if every step is a
known node and every consecutive pair is joined by an edge. Nothing is ever written by
the model: step texts are the nodes' own sentences.
"""

import json
import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeout
from dataclasses import dataclass, field

from .data import items, portfolios
from .facts import _trades, day, fmt_day, money, pct, relabel, short_name, signed_pct
from .facts import Fact
from .llm import LLMUnavailable, chat
from .market import label, impact

LLM_TIMEOUT = 5.0
_POOL = ThreadPoolExecutor(max_workers=2)
MIN_SHARE = 0.001          # impacts under 0.1% of the book are folded into "everything else"


def llm_json(messages, key, timeout, max_tokens=600):
    """chat(), bounded by a wall-clock timeout, parsed as {key: ...} from the first
    {...} in the reply. None on any failure (timeout, no key, bad JSON) — every
    caller (here and backend/answers.py) falls back to its own rule-based answer."""
    try:
        raw, _ = _POOL.submit(chat, messages, 0.0, max_tokens).result(timeout=timeout)
        return json.loads(raw[raw.find('{'):raw.rfind('}') + 1])[key]
    except (FutureTimeout, LLMUnavailable, ValueError, KeyError, TypeError):
        return None

# How to read an edge between consecutive steps: (relation, previous step is the edge's source).
LINK_WORDS = {
    ('part_of', True): 'adding up to', ('part_of', False): 'made up of',
    ('via', True): 'within', ('via', False): 'mostly through',
    ('offsets', True): 'which offsets', ('offsets', False): 'except',
    ('compared_with', True): 'so', ('compared_with', False): 'compared with',
    ('explains', True): 'which is why', ('explains', False): 'because',
    ('bought', True): 'which bought', ('bought', False): 'bought by',
    ('reported', True): 'which hit', ('reported', False): 'reported as',
}


def signed_money(x, ccy):
    """One decimal in thousands, so the steps of a breakdown visibly add up to its total."""
    x_abs = abs(x)
    amount = (f'{ccy} {x_abs / 1e6:.2f}m' if x_abs >= 1e6 else f'{ccy} {x_abs / 1e3:.1f}k' if x_abs >= 1e3
              else f'{ccy} {x_abs:.0f}')
    return f'{"+" if x >= 0 else "−"}{amount}'


@dataclass
class Graph:
    nodes: dict = field(default_factory=dict)            # id -> Fact
    edges: set = field(default_factory=set)               # (src, dst, relation)
    values: dict = field(default_factory=dict)            # id -> the node's amount (impact, or index move)

    def add(self, fact, value=None):
        self.nodes[fact.id] = fact
        if value is not None:
            self.values[fact.id] = value
        return fact.id

    def link(self, src, dst, relation):
        if src in self.nodes and dst in self.nodes:
            self.edges.add((src, dst, relation))

    def relation(self, a, b):
        """The edge joining a and b, in either direction, or None (the most specific one if several)."""
        rels = {rel for src, dst, rel in self.edges if {src, dst} == {a, b}}
        return next((r for r in ('explains', 'offsets', 'bought', 'via', 'reported', 'compared_with', 'part_of')
                     if r in rels), None)

    def direction(self, a, b):
        """(relation, a is the source) for the edge joining a and b, or (None, None)."""
        rel = self.relation(a, b)
        if rel is None:
            return None, None
        return rel, (a, b, rel) in self.edges

    def around(self, node, relation=None):
        return [s if d == node else d for s, d, r in self.edges
                if node in (s, d) and (relation is None or r == relation)]


def _topic_text(t, total, ccy):
    share = pct(t.exposure / total)
    if t.dimension == 'fx':
        return (f'{label(t.dimension, t.bucket).capitalize()} {signed_pct(t.change)} against the franc, '
                f'on {share} of the book: about {signed_money(t.impact, ccy)}.')
    look = ' after fund look-through' if t.dimension == 'industry' else ''
    return f'{label(t.dimension, t.bucket)} {signed_pct(t.change)} today, on {share} of the book{look}: about {signed_money(t.impact, ccy)}.'


def build(client, store, market, as_of=None):
    """The fact graph for one client under one market."""
    g = Graph()
    ref = client['ClientRef']
    ccy = client.get('ReportingCurrency') or 'CHF'
    hit = impact(client, store, market)
    total = hit['total'] or 1
    feed = f'{"simulated feed" if market.simulated else "market feed"} "{market.name}"'
    if not market.moves:
        return g
    book = hit['impact']
    g.add(Fact('total', 'chain', f'The book is about {signed_money(book, ccy)} today ({signed_pct(book / total)}) '
                                 f'on {money(total, ccy)}.', f'{feed} × clients.json {ref} holdings'), book)

    # The parts: each topic's impact, largest first; small ones are summed into "everything else".
    topics = sorted(hit['topics'].values(), key=lambda t: t.impact)
    shown = [t for t in topics if abs(t.impact) / total >= MIN_SHARE]
    for t in shown:
        tid = g.add(Fact(f'topic.{t.dimension}.{t.bucket}', 'chain', _topic_text(t, total, ccy),
                         f'{market.source(t.dimension, t.bucket)} × clients.json {ref} holdings'), t.impact)
        g.link(tid, 'total', 'part_of')
        if t.dimension == 'industry':
            for i, (name, amount) in enumerate(sorted(t.positions.items(), key=lambda kv: -kv[1])[:2]):
                vid = g.add(Fact(f'via.{t.bucket}.{i}', 'chain',
                                 f'{name}: {money(amount, ccy)} of that exposure, about '
                                 f'{signed_money(t.position_impact[name], ccy)} of it.',
                                 f'clients.json {ref} holdings × reference.json FundUnbundlingMappings'))
                g.link(vid, tid, 'via')
    # The same three the breakdown shows: the largest losses among the shown topics.
    top = [t for t in shown if t.impact < 0][:3]
    rest = book - sum(t.impact for t in top)
    if abs(rest) >= 0.01:
        # Computed as the remainder, so the breakdown adds up to the total exactly.
        g.add(Fact('rest', 'chain', f'Everything else together ({len(topics) - len(top)} smaller moves, '
                                    f'up and down): about {signed_money(rest, ccy)}.',
                   f'{feed} × clients.json {ref} holdings'), rest)
        g.link('rest', 'total', 'part_of')

    # What held up and what the hedges kept out.
    for t in shown:
        if t.impact > 0:
            g.link(f'topic.{t.dimension}.{t.bucket}', 'total', 'offsets')
    usd = market.change('fx', 'USD')
    if usd is not None and usd < 0 and hit['hedged_chf']:
        names = list(hit['hedged_chf'])
        hedged = sum(hit['hedged_chf'].values())
        g.add(Fact('hedged', 'chain', f'{" and ".join(names)} ({pct(hedged / total)} of the book) '
                                      f'{"are" if len(names) > 1 else "is"} hedged to the franc, so the dollar move '
                                      f'({signed_pct(usd)}) does not reach {"them" if len(names) > 1 else "it"}.',
                   f'clients.json {ref}: SecurityPositions.SecurityName (hedged share class); {market.source("fx", "USD")}'))
        g.link('hedged', 'topic.fx.USD', 'offsets')

    # Headlines behind the moves.
    for i, h in enumerate(market.headlines):
        tid = f'topic.{h.get("dimension")}.{h.get("bucket")}'
        if tid in g.nodes and h.get('text'):
            g.add(Fact(f'news.{i}', 'chain', f'Behind the move: "{h["text"]}"', f'{feed} headline'))
            g.link(f'news.{i}', tid, 'reported')

    # Compared with the market: the index moves in the feed.
    mix = defaultdict(float)
    for p in portfolios(client):
        aum = p.get('AssetsUnderManagementInDefaultCurrency') or 0
        for sp in items(p, 'SecurityPositions'):
            mix[store.securities.get(sp.get('SecurityId'), {}).get('SAA_AssetClassName') or 'Other'] += \
                (sp.get('PortfolioValuePercentage') or 0) * aum
        for ap in items(p, 'AccountPositions'):
            mix['Liquidity'] += (ap.get('PortfolioValuePercentage') or 0) * aum
    parts = sorted(mix.items(), key=lambda kv: -kv[1])
    g.add(Fact('mix', 'chain', 'The book is ' + ', '.join(f'{pct(v / total)} {k.replace("andC", "and C").lower()}'
                                                          for k, v in parts if v / total >= 0.01) + '.',
               f'clients.json {ref} holdings × reference.json Securities.SAA_AssetClassName'))
    for (dim, bucket), move in market.moves.items():
        if dim != 'index':
            continue
        iid = g.add(Fact(f'index.{bucket}', 'chain', f'The {bucket} moved {signed_pct(move.change)} today.',
                         market.source(dim, bucket)), move.change)
        less = abs(book / total) < abs(move.change)
        cid = g.add(Fact(f'compare.{bucket}', 'chain',
                         f'The book moved {"less" if less else "more"} than the {bucket}: '
                         f'{signed_pct(book / total)} against {signed_pct(move.change)}.',
                         f'{market.source(dim, bucket)} × clients.json {ref} holdings'))
        g.link(iid, cid, 'compared_with')
        g.link('total', cid, 'compared_with')
        if less:
            g.link('mix', cid, 'explains')
            g.link('hedged', cid, 'explains')
            for t in shown:
                if t.impact > 0:
                    g.link(f'topic.{t.dimension}.{t.bucket}', cid, 'explains')

    # Holdings: the largest movers today, each tied to the topics it is part of.
    amounts = _holdings(client)
    for i, name in enumerate(sorted(hit['position_impact'], key=lambda n: -abs(hit['position_impact'][n]))[:12]):
        hid = g.add(Fact(f'holding.{i}', 'chain',
                         f'{name}: {money(amounts.get(name, 0), ccy)} in the book, about '
                         f'{signed_money(hit["position_impact"][name], ccy)} today.',
                         f'clients.json {ref}: SecurityPositions × {feed}'), hit['position_impact'][name])
        for t in shown:
            if name in t.positions:
                g.link(hid, f'topic.{t.dimension}.{t.bucket}', 'part_of')

    # The last finalised proposal: what it bought, and what those holdings did today.
    finalised = [p for p in items(client, 'Proposals')
                 if p.get('ProposalStatusName') == 'Final' and p.get('FinalizedDateUTC')]
    if finalised:
        latest = max(finalised, key=lambda p: p['FinalizedDateUTC'])
        _, buys, _ = _trades(client, latest)
        held = {name: amount for name, amount in _holdings(client).items() if name in buys}
        if held:
            when = fmt_day(day(latest['FinalizedDateUTC']))
            pid = g.add(Fact('proposal', 'chain',
                             f'The proposal of {when} (reason: {latest.get("Reason") or "not given"}) bought '
                             f'{len(buys)} holding{"s" if len(buys) != 1 else ""}; {len(held)} of them are still in the book.',
                             f'clients.json {ref}: Proposals[{latest.get("ProposalId")}] × Transactions'))
            moved = sorted(held, key=lambda n: hit['position_impact'].get(n, 0))
            summed = sum(hit['position_impact'].get(n, 0) for n in held)
            sid = g.add(Fact('proposal.today', 'chain',
                             f'Together, the holdings bought on {when} are about {signed_money(summed, ccy)} today, '
                             f'of the book\'s {signed_money(book, ccy)}.',
                             f'clients.json {ref}: Transactions × holdings × {feed}'))
            g.link(pid, sid, 'bought')
            g.link(sid, 'total', 'part_of')
            for i, name in enumerate(moved[:3]):
                bid = g.add(Fact(f'bought.{i}', 'chain',
                                 f'{name}, bought on {when}: {money(held[name], ccy)} in the book, about '
                                 f'{signed_money(hit["position_impact"].get(name, 0), ccy)} today.',
                                 f'clients.json {ref}: Transactions × SecurityPositions × {feed}'))
                g.link(pid, bid, 'bought')
                g.link(bid, sid, 'part_of')
                for t in shown:
                    if name in t.positions:
                        g.link(bid, f'topic.{t.dimension}.{t.bucket}', 'part_of')
            for hid in [i for i, f in g.nodes.items() if i.startswith('holding.') and f.text.split(':')[0] in held]:
                g.link(pid, hid, 'bought')
    relabel(list(g.nodes.values()), client)
    return g


def _holdings(client):
    out = defaultdict(float)
    for p in portfolios(client):
        aum = p.get('AssetsUnderManagementInDefaultCurrency') or 0
        for sp in items(p, 'SecurityPositions'):
            out[short_name(sp.get('SecurityName'))] += (sp.get('PortfolioValuePercentage') or 0) * aum
    return out


# --- chains ------------------------------------------------------------------

def _existing(g, ids):
    return [i for i in ids if i in g.nodes]


def breakdown(g, with_headline=False):
    """The total, its three largest losses (the largest with the holding it came through),
    everything else, and what the hedges kept out. The amounts add up to the total."""
    losses = sorted((i for i in g.around('total', 'part_of') if i.startswith('topic.') and g.values.get(i, 0) < 0),
                    key=lambda i: g.values[i])[:3]
    if not losses:
        return []
    chain = ['total', losses[0]] + sorted(g.around(losses[0], 'via'))[:1] + losses[1:] + ['rest']
    if 'hedged' in g.nodes and 'topic.fx.USD' in losses:
        chain.append('hedged')
    if with_headline:
        chain = sorted(g.around(losses[0], 'reported'))[:1] + chain
    return _existing(g, chain)


def vs_index(g, question=''):
    wanted = next((i for i in g.nodes if i.startswith('compare.') and i.split('.', 1)[1].lower().replace(' ', '')
                   in question.lower().replace(' ', '')), None)
    compares = [i for i in g.nodes if i.startswith('compare.')]
    if not compares:
        return []
    cid = wanted or max(compares, key=lambda i: abs(g.values.get('index.' + i.split('.', 1)[1], 0)))
    iid = 'index.' + cid.split('.', 1)[1]
    reasons = [i for i in g.around(cid, 'explains')]
    order = ['mix', 'hedged'] + [i for i in reasons if i.startswith('topic.')]
    return _existing(g, [iid, 'total', cid] + [i for i in order if i in reasons][:3])


def proposal(g):
    if 'proposal' not in g.nodes:
        return []
    bought = sorted(g.around('proposal', 'bought'), key=lambda i: i)
    return _existing(g, ['proposal'] + [i for i in bought if i.startswith('bought.')] + ['proposal.today', 'total'])


def _amount(g, node):
    return g.values.get(node, 0.0)


PROPOSAL_Q = re.compile(r'\b(chang\w*|proposal|trades?|bought|rebalanc\w*|what you did)\b.*'
                        r'\b(worse|better|hurt|help\w*|cost|affect\w*|impact\w*|responsible|to do with|because)\b'
                        r'|\bdid (?:the|your|you|those) \w+.*\b(worse|hurt|cost|help)', re.IGNORECASE)
INDEX_Q = re.compile(r'\b(market|s&p|s & p|spx|smi|index|benchmark|everyone)\b', re.IGNORECASE)
COMPARE_Q = re.compile(r'\b(less|more|than|compared?|vs\.?|versus|only|so little|so much|worse|better)\b', re.IGNORECASE)
BREAKDOWN_Q = re.compile(r'\bwhere (?:did|has|have|is)\b.*\b(go|gone|went|from)\b|\bbreak ?(?:it )?down\b|'
                         r'\bmade up\b|\bwhich (?:positions|funds|holdings|parts?)\b|\bhow did (?:i|we) lose\b|'
                         r'\bwhat (?:is|was) (?:behind|driving)\b|\bwhere .*\bloss', re.IGNORECASE)
OPEN_Q = re.compile(r"\b(why|explain|explanation|in[- ]depth|what(?:'s| is| has)? (?:happen\w*|going on)|"
                    r"tell me more|more detail)", re.IGNORECASE)
# Open questions about the day as a whole; any other "why" names something specific.
GENERAL_Q = re.compile(r"what(?:'s| is| has)? (?:happen\w*|going on)|in[- ]depth|tell me more|more detail|"
                       r"why is this happening|why (?:am i|are we|is (?:my|the) (?:book|portfolio)) (?:down|losing)",
                       re.IGNORECASE)
SPECIFIC_Q = re.compile(r'\b(why|how come)\b', re.IGNORECASE)


def holding(g, question):
    """A question naming a holding: the holding, the topics it is part of (largest first), the
    headline behind the first, and when it was bought if the last proposal bought it."""
    words = {w for w in re.findall(r"[a-z0-9&]{4,}", question.lower())} - HOLDING_STOP
    node = next((i for i, f in g.nodes.items() if i.startswith('holding.')
                 and words & set(re.findall(r"[a-z0-9&]{4,}", f.text.split(':')[0].lower()))), None)
    if node is None:
        return []
    topics = sorted(g.around(node, 'part_of'), key=lambda i: g.values.get(i, 0))[:2]
    name = g.nodes[node].text.split(':')[0]
    bought = [i for i in g.nodes if i.startswith('bought.') and g.nodes[i].text.startswith(name + ',')]
    chain = [node] + topics[:1] + (sorted(g.around(topics[0], 'reported'))[:1] if topics else []) + topics[1:2]
    return _existing(g, chain + (['proposal'] if bought else []))


# Words too common in fund names to identify a holding.
HOLDING_STOP = {'fund', 'ishares', 'ucits', 'shares', 'what', 'about', 'with', 'from', 'money', 'lose', 'lost',
                'down', 'today', 'this', 'that', 'much', 'have', 'does', 'hedged', 'world', 'core', 'index', 'why'}


def by_rules(g, question):
    """(kind, chain) for questions whose chain the code knows how to build, else (None, [])."""
    if PROPOSAL_Q.search(question):
        return 'proposal', proposal(g)
    named = holding(g, question)
    if len(named) >= 2:
        return 'holding', named
    if INDEX_Q.search(question) and COMPARE_Q.search(question):
        return 'vs_index', vs_index(g, question)
    if BREAKDOWN_Q.search(question):
        return 'breakdown', breakdown(g)
    if OPEN_Q.search(question):
        return 'explain', breakdown(g, with_headline=True)
    return None, []


SYSTEM = """You answer a client's question for a Swiss private-banking advisor by choosing a path through a graph of facts.
Each fact has an id. Edges say how facts are connected. Choose 2 to 5 fact ids, in order, that together answer the
question; every consecutive pair in your path MUST be joined by an edge. If no path answers it, return an empty list.
Return JSON only: {"path": ["id", ...]}"""


def by_llm(g, question):
    """A path chosen by Apertus, accepted only if every step is joined to the next by an edge."""
    nodes = '\n'.join(f'{i}: {f.text}' for i, f in g.nodes.items())
    edges = '\n'.join(f'{s} -[{r}]-> {d}' for s, d, r in sorted(g.edges))
    messages = [{'role': 'system', 'content': SYSTEM},
                {'role': 'user', 'content': f'Question: {question}\n\nFacts:\n{nodes}\n\nEdges:\n{edges}'}]
    path = llm_json(messages, 'path', LLM_TIMEOUT, max_tokens=120)
    if path is None:
        return []
    if not isinstance(path, list) or not 2 <= len(path) <= 5 or len(set(map(str, path))) != len(path):
        return []
    if any(str(p) not in g.nodes for p in path):
        return []
    if any(g.relation(str(a), str(b)) is None for a, b in zip(path, path[1:])):
        return []
    return [str(p) for p in path]


def render(g, chain):
    """Steps as answer cards: each the node's own sentence, source, and its link to the previous step."""
    steps = []
    for node in chain:
        # The link word comes from the nearest earlier step this one is joined to.
        rel, forward = None, None
        for earlier in reversed(chain[:chain.index(node)]):
            rel, forward = g.direction(earlier, node)
            if rel:
                break
        f = g.nodes[node]
        steps.append({'text': f.text, 'source': f.source, 'fact': f.id,
                      'link': LINK_WORDS.get((rel, forward)) if rel else None})
    return steps


def chain_answer(g, question, use_llm=True):
    """{'answers': steps, 'found', 'method': 'chain:<kind>', 'chain': True} or None."""
    if not g.nodes:
        return None
    kind, chain = by_rules(g, question)
    specific_why = SPECIFIC_Q.search(question) and not GENERAL_Q.search(question)
    if use_llm and specific_why and kind in (None, 'explain'):
        # A pointed "why" ("why wasn't my world fund hit?") gets its own path if Apertus finds a valid one;
        # otherwise it falls back to the general explanation.
        path = by_llm(g, question)
        if len(path) >= 2:
            kind, chain = 'llm', path
    if len(chain) < 2:
        return None
    return {'answers': render(g, chain), 'found': True, 'method': f'chain:{kind}', 'chain': True}
