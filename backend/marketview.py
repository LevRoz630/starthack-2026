"""'What do you think about the copper market?' -- ready for every market, for every client.

Three cards, all sourced, none of them our own opinion:
1. what that market did today (the feed; marked simulated when it is),
2. what this client holds in it, or that they hold none,
3. a bank's house view on it, quoted word for word, or else a tagged headline.
The advisor gives the opinion; the card gives them what to base it on.
"""

import re

from .facts import signed_pct
from .market import label as move_label

VIEW_QUESTION = re.compile(
    r"\bwhat (?:do|would|did) you (?:think|say|expect|make)\b|\b(?:outlook|views?|opinion|forecast|prospects?)\b"
    r"|\bhow(?:'s| is| are| was| were| did| does) (?:the )?[\w&' ]{1,30}(?:market|doing|going|today|performing)\b"
    r"|\bwhat(?:'s| is| was) (?:going on|happening|up) (?:with|in)\b"
    r"|\bshould (?:i|we) (?:buy|get into|invest in|add)\b|\bis (?:now )?a good time (?:to|for)\b"
    r"|\bwhat about (?:the )?[\w&' ]{1,30}(?:market|sector)\b", re.IGNORECASE)

# (question pattern, what to call it, feed moves, the client's holding fact, house-view tags).
# Specific markets first; the general "the market" last.
MARKETS = [
    (r'\bcopper\b', 'copper', [('commodity', 'Copper')], 'expo.holding.Copper', ['Raw materials']),
    (r'\bgold\b', 'gold', [('commodity', 'Gold')], 'expo.holding.Gold', ['Gold']),
    (r'\bsilver\b', 'silver', [('commodity', 'Silver')], 'expo.holding.Silver', ['Gold']),
    (r'\b(?:commodit\w*|metals?|raw materials?|mining)\b', 'commodities',
     [('commodity', 'Gold'), ('commodity', 'Copper'), ('commodity', 'Silver')],
     'expo.asset.Specialties andCommodities', ['Raw materials', 'Gold']),
    (r'\b(?:oil|energy|crude|gas)\b', 'energy', [('industry', 'Energy')], 'expo.industry.Energy', ['Energy']),
    (r'\b(?:tech\w*|ai|chips?|semiconductors?|nasdaq)\b', 'tech', [('industry', 'Information Technology')],
     'expo.industry.Information Technology', ['Information Technology']),
    (r'\b(?:health ?care|pharma\w*|biotech\w*|drug\w*)\b', 'health care', [('industry', 'Health Care')],
     'expo.industry.Health Care', ['Health Care']),
    (r'\b(?:banks?|banking|financials?|insurers?|insurance)\b', 'financials', [('industry', 'Financials')],
     'expo.industry.Financials', ['Financials']),
    (r'\bindustrials?\b', 'industrials', [('industry', 'Industrials')], 'expo.industry.Industrials', ['Industrials']),
    (r'\butilit\w+\b', 'utilities', [('industry', 'Utilities')], 'expo.industry.Utilities', ['Utilities']),
    (r'\b(?:real estate|property market|housing market)\b', 'real estate', [('industry', 'Real Estate')],
     'expo.industry.Real Estate', ['Real Estate']),
    (r'\b(?:consumer|retail|luxury)\b', 'consumer stocks',
     [('industry', 'Consumer Discretionary'), ('industry', 'Consumer Staples')],
     'expo.industry.Consumer Discretionary', ['Consumer Discretionary', 'Consumer Staples']),
    (r'\b(?:bonds?|fixed income|interest rates?|yields?)\b', 'bonds', [('bonds', 'CHF'), ('bonds', 'Global')],
     'expo.asset.Bonds', ['Bonds']),
    (r'\b(?:dollar|usd|greenback)\b', 'the dollar', [('fx', 'USD')], 'expo.currency.US-Dollar', ['USD']),
    (r'\beuros?\b', 'the euro', [('fx', 'EUR')], 'expo.currency.Euro', ['EUR']),
    (r'\b(?:franc|chf)\b', 'the franc', [('fx', 'USD'), ('fx', 'EUR')], 'expo.currency.Swiss francs', ['CHF']),
    (r'\b(?:crypto\w*|bitcoin|ether\w*)\b', 'crypto', [('crypto', 'BTC'), ('crypto', 'ETH')], 'expo.holding.Crypto', []),
    (r'\bemerging markets?\b', 'emerging markets', [], None, ['Emerging markets']),
    (r'\b(?:swiss (?:market|stocks|shares|equities)|smi)\b', 'the Swiss market', [('index', 'SMI')], None, ['Equities']),
    (r'\b(?:s ?& ?p|us (?:market|stocks|equities)|wall street|american (?:market|stocks))\b', 'the US market',
     [('index', 'S&P 500')], 'expo.currency.US-Dollar', ['Equities']),
    (r'\b(?:volatility|vix|fear index)\b', 'volatility', [('volatility', 'VIX'), ('volatility', 'VSMI')], None, []),
    (r'\b(?:stock ?market|equit\w+|stocks|shares|the markets?|markets)\b', 'equities',
     [('index', 'S&P 500'), ('index', 'SMI')], 'expo.asset.Shares', ['Equities']),
]


def subject(question):
    for pattern, name, moves, holding, tags in MARKETS:
        if re.search(pattern, question, re.IGNORECASE):
            return name, moves, holding, tags, pattern
    return None


def _move_card(market, dim, bucket):
    move = market.moves.get((dim, bucket)) if market else None
    if not move:
        return None
    name = move_label(dim, bucket)
    name = name[0].upper() + name[1:]
    if dim == 'volatility':
        level = f' at {move.level:g}' if move.level is not None else ''
        text = f'{name}{level} today' + (f', {signed_pct(move.change)}' if move.change else '') + '.'
    elif dim == 'fx':
        text = f'{name} {signed_pct(move.change)} against the franc today.'
    else:
        text = f'{name} {signed_pct(move.change)} today.'
    return {'text': text, 'source': market.source(dim, bucket), 'fact': f'market.{dim}.{bucket}', 'slot': 'market'}


def _view_card(tags, views, news, pattern, name):
    """A house view on this market (one whose text names it first), else a headline that names it."""
    tagged = [v for v in (views or {}).get('items', []) if set(v.get('tags', [])) & set(tags)]
    stem = name.split()[-1][:4].lower()
    tagged.sort(key=lambda v: (stem not in v['text'].lower(),
                               -len(re.findall(pattern, v['text'], re.IGNORECASE))))
    if tagged:
        v = tagged[0]
        return {'text': f'{v["source"]} ({v["label"]}): "{v["text"]}"', 'source': v['url'],
                'fact': f'view.{v["id"]}', 'slot': 'outlook'}
    # A headline only counts if it names the market: a raw-materials story about a trader's
    # staff is not an answer about copper.
    items = [n for n in (news or {}).get('items', []) if re.search(pattern, n.get('title', ''), re.IGNORECASE)]
    if items:
        n = sorted(items, key=lambda n: n.get('published') or '', reverse=True)[0]
        return {'text': f'News ({n["source"]}): "{n["title"]}"', 'source': n['link'], 'fact': f'news.{n["id"]}',
                'slot': 'outlook'}
    return None


def view_cards(question, facts, market, views, news):
    """Cards for 'what do you think about <market>?', or [] when no market is named."""
    if not VIEW_QUESTION.search(question):
        return []
    found = subject(question)
    if not found:
        return []
    name, moves, holding_id, tags, pattern = found
    cards = [c for c in (_move_card(market, d, b) for d, b in moves) if c][:2]
    by_id = {f.id: f for f in facts}
    if holding_id and holding_id in by_id:
        f = by_id[holding_id]
        cards.append({'text': f.text, 'source': f.source, 'fact': f.id, 'slot': f.slot})
    elif holding_id and any(f.id.startswith('expo.') for f in facts):
        cards.append({'text': f'No {name} in the portfolio.', 'source': 'all holdings checked, including fund look-through',
                      'fact': 'expo.none', 'slot': 'watch'})
    view = _view_card(tags, views, news, pattern, name)
    if view:
        cards.append(view)
    return cards
