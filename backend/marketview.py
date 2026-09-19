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


def named_market(question):
    """The specific market a question names, or None for 'the market' in general."""
    found = subject(question)
    return found if found and found[0] != 'equities' else None


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


BUY_INTENT = re.compile(r'\b(?:buy\w*|invest\w*|add(?:ing)?|get into|put (?:money|some) in|increase|more)\b', re.IGNORECASE)


def risk_card(pattern, name, store, client):
    """How risky products in this market are, from the bank's own product data, against
    what the client's risk profile allows."""
    if store is None:
        return None
    products = [s for s in store.securities.values()
                if s.get('PRC') and re.search(pattern, ' '.join(str(s.get(k) or '') for k in
                                                                ('Name', 'AssetClassName', 'IndustryName')), re.IGNORECASE)]
    if not products:
        return None
    classes = sorted(s['PRC'] for s in products)
    vols = sorted(s['Volatility'] for s in products if s.get('Volatility'))
    span = f'{classes[0]}' if classes[0] == classes[-1] else f'{classes[0]}–{classes[-1]}'
    vol = ''
    if vols:
        lo, hi = round(vols[0] * 100), round(vols[-1] * 100)
        vol = f', volatility about {lo}%' + (f'–{hi}%' if hi != lo else '') + ' a year'
    text = f'Risk: {name} products in the bank\'s data are risk class {span} of 7{vol}.'
    profile = store.risk_profiles.get((client or {}).get('RiskProfileId'), {})
    if profile.get('MaxPRC'):
        from .facts import risk_profile
        allowed = profile['MaxPRC']
        verdict = ('within' if classes[-1] <= allowed else 'partly above' if classes[0] <= allowed else 'above')
        text += f' {risk_profile(client)} allows up to class {allowed}: {verdict} it.'
    return {'text': text, 'fact': 'risk.product', 'slot': 'risk',
            'source': f'reference.json Securities.PRC, Volatility ({len(products)} products) × RiskProfiles.MaxPRC'}


def ask_first_card(client):
    """Before anything is bought: the suitability questions, as something to say."""
    from .facts import risk_profile
    profile = risk_profile(client) if client else 'their profile'
    return {'text': f'Ask first: what the money is for and when they might need it, whether anything has changed in '
                    f'their situation, and whether their risk appetite is still {profile}.',
            'fact': 'suggest.ask_first', 'slot': 'suggest',
            'source': 'suitability check before any recommendation (FIDLEG)'}


_BANK = {}


def fact_bank(facts, market, store, client):
    """Every market's cards for this client as facts, computed once per client and market,
    so the model can pick from all of them when no rule fits the question."""
    from .facts import Fact, _outlook_sources
    key = (client.get('Id') or client.get('ClientId') or id(client), getattr(market, 'name', id(market)))
    if key in _BANK:
        return _BANK[key]
    news, views = _outlook_sources()
    known = {f.id for f in facts}
    out, seen = [], set()
    for pattern, name, moves, holding_id, tags in MARKETS:
        # "What do you think about X?" makes view_cards return X's full set of cards.
        word = re.sub(r'\\b|\(\?:|\)|\?|\\w\*|\\w\+|s\?|\|.*', '', pattern).strip() or name
        for c in view_cards(f'what do you think about {word}?', facts, market, views, news, store, client):
            if c['fact'] in known or c['text'] in seen:
                continue
            seen.add(c['text'])
            fid = c['fact'] if c['fact'] not in ('expo.none', 'risk.product') else f'{c["fact"]}.{name}'
            out.append(Fact(fid, c['slot'], c['text'], c['source'], 0.0))
    ask = ask_first_card(client)
    out.append(Fact(ask['fact'], ask['slot'], ask['text'], ask['source'], 0.0))
    _BANK[key] = out
    return out


def view_cards(question, facts, market, views, news, store=None, client=None):
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
    if name not in ('equities', 'volatility', 'the dollar', 'the euro', 'the franc'):
        risk = risk_card(pattern, name, store, client)
        if risk:
            cards.append(risk)
    if BUY_INTENT.search(question):
        cards.append(ask_first_card(client))
    return cards
