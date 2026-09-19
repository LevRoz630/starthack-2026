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
    (r'\bchina\b|\bchinese (?:market|stocks|equities)\b', 'China', [], None, ['Equities']),
    (r'\b(?:asia\w*|taiwan|japan\w*)\b|\baxj\b', 'Asia', [], None, ['Equities', 'Emerging markets']),
    (r'\b(?:europe\w*|uk|british|germany|german)\b(?! (?:bonds?|rates))', 'Europe', [], None, ['Equities', 'Industrials']),
    (r'\b(?:s ?& ?p|u\.?s\.? (?:market|stocks|equities|technology)|wall street|(?<!latin )american (?:market|stocks|companies))\b',
     'the US market',
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
    best = _market_views(views, tags, pattern, name, limit=1)
    if best:
        return best[0]
    # A headline only counts if it names the market: a raw-materials story about a trader's
    # staff is not an answer about copper.
    items = [n for n in (news or {}).get('items', []) if re.search(pattern, n.get('title', ''), re.IGNORECASE)]
    if items:
        n = sorted(items, key=lambda n: n.get('published') or '', reverse=True)[0]
        return {'text': f'News ({n["source"]}): "{n["title"]}"', 'source': n['link'], 'fact': f'news.{n["id"]}',
                'slot': 'outlook'}
    return None


# "I'm thinking about buying gold" is a question without a question mark.
INTEREST = re.compile(r'\b(?:thinking (?:about|of)|considering|interested in|looking at|want to (?:buy|invest)'
                      r'|would like to (?:buy|invest)|(?:should|could|can) (?:i|we) (?:buy|invest|add))\b', re.IGNORECASE)
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


HOUSE_VIEW = re.compile(
    r"\bhouse views?\b|\b(?:cio|strategists?|analysts?|experts?|economists?|research)\b"
    r"|\bwhat (?:do|are|is) (?:the )?(?:other |big |major )?banks?\b"
    r"|\b(?:banks?|bank's|banks'|your|the bank) (?:views?|outlook|positioning|position|recommend\w*|strategy|stance|calls?"
    r"|think\w*|say\w*)\b|\bwhat (?:do|would) you recommend\b|\b(?:overweight|underweight|bullish|bearish)\b"
    r"|\bwhere (?:should|would|do) (?:i|we|you) (?:invest|put)\b|\bwhat (?:is|are) (?:the )?(?:professionals|smart money)\b",
    re.IGNORECASE)

# What a view's tag is called when said out loud. Currency tags are too mixed to summarise.
PLAIN = {'Information Technology': 'tech', 'Emerging markets': 'emerging markets', 'Equities': 'equities',
         'Bonds': 'bonds', 'Gold': 'gold', 'Financials': 'financials', 'Industrials': 'industrials',
         'Utilities': 'utilities', 'Real Estate': 'real estate', 'Consumer Staples': 'consumer staples',
         'Consumer Discretionary': 'consumer stocks', 'Health Care': 'health care', 'Energy': 'energy',
         'Raw materials': 'raw materials', 'Communication Services': 'communication services'}


def _short(source):
    return source.replace(' Asset Management', '').replace(' Investment Institute', '')


def positions(views):
    """{tag: {bank: 'overweight' | 'neutral' | 'underweight' | 'mixed'}} from the views' stated stances."""
    seen = {}
    for v in (views or {}).get('items', []):
        if not v.get('stance'):
            continue
        for t in v['tags']:
            if t in PLAIN:
                seen.setdefault(t, {}).setdefault(_short(v['source']), set()).add(v['stance'])
    return {t: {b: (s.pop() if len(s) == 1 else 'mixed') for b, s in banks.items()} for t, banks in seen.items()}


def _names(banks):
    banks = sorted(banks)
    return banks[0] if len(banks) == 1 else ', '.join(banks[:-1]) + ' and ' + banks[-1]


def positioning_cards(views):
    """Where the banks lean, in two lines: what they favour, and what they are neutral or cautious on."""
    pos = positions(views)
    sources = ', '.join(f'{s["name"]} ({s["label"]})' for s in (views or {}).get('sources', []) if s.get('ok'))
    over = sorted(((t, [b for b, s in banks.items() if s == 'overweight']) for t, banks in pos.items()),
                  key=lambda tb: -len(tb[1]))
    over = [f'{PLAIN[t]} ({_names(b)})' for t, b in over if b]
    cards = []
    if over:
        cards.append({'text': 'The banks favour ' + ', '.join(over[:5]) + '.', 'slot': 'outlook',
                      'fact': 'view.positioning.over', 'source': f'house views: {sources}'})
    rest = [f'{PLAIN[t]} ({", ".join(f"{b} {s}" for b, s in sorted(banks.items()) if s != "overweight")})'
            for t, banks in pos.items() if any(s != 'overweight' for s in banks.values())]
    if rest:
        cards.append({'text': 'More careful on ' + '; '.join(rest[:4]) + '.', 'slot': 'outlook',
                      'fact': 'view.positioning.careful', 'source': f'house views: {sources}'})
    return cards


def _market_views(views, tags, pattern, name, limit=3):
    """Views on one market, the ones naming it first, one per bank."""
    items = [v for v in (views or {}).get('items', []) if set(v.get('tags', [])) & set(tags)]
    # Views whose own words name the market, the shortest (clean single sentences) first;
    # the rest of the tag only when none names it.
    named = [v for v in items if re.search(pattern, v['text'], re.IGNORECASE)]
    items = sorted(named or items, key=lambda v: len(v['text']))
    out, banks = [], set()
    for v in items:
        if v['source'] in banks:
            continue
        banks.add(v['source'])
        out.append({'text': f'{_short(v["source"])} ({v["label"]}): "{v["text"]}"', 'source': v['url'],
                    'fact': f'view.{v["id"]}', 'slot': 'outlook'})
        if len(out) == limit:
            break
    return out


RECOMMEND = re.compile(r'\brecommend\w*\b|\bwhere (?:should|would|do) (?:i|we|you) (?:invest|put)\b'
                       r'|\bshould (?:i|we)\b', re.IGNORECASE)
# "the banks think", "the bank's view": the banks as the speaker, not the banking sector.
BANK_SPEAKER = re.compile(r"\b(?:the |your |other |big |major )?banks?(?:'s|')?(?= (?:house |own )?(?:views?|think\w*|"
                          r"say\w*|outlook|positioning|position|stance|recommend\w*|strategy|calls?|are|is|bullish|"
                          r"bearish)\b)", re.IGNORECASE)


def house_view_cards(question, facts, views, client=None):
    """'What's the bank's view on gold?' / 'What are the banks saying?': quoted house views,
    or the banks' positioning when no market is named. [] when it is not a house-view question."""
    if not HOUSE_VIEW.search(question):
        return []
    cards = _house_view_cards(BANK_SPEAKER.sub(' ', question), facts, views)
    if cards and RECOMMEND.search(question):
        cards.append(ask_first_card(client))
    return cards


def _house_view_cards(question, facts, views):
    found = subject(question)
    if found:
        name, _, holding_id, tags, pattern = found
        pos = positions(views)
        # Stances from the views that name this market; the whole tag only when none does.
        named = [v for v in (views or {}).get('items', []) if v.get('stance') and set(v['tags']) & set(tags)
                 and re.search(pattern, v['text'], re.IGNORECASE)]
        if named:
            stances = {}
            for v in named:
                stances.setdefault(_short(v['source']), set()).add(v['stance'])
            stances = {b: (s.pop() if len(s) == 1 else 'mixed') for b, s in stances.items()}
        else:
            stances = {b: s for t in tags for b, s in pos.get(t, {}).items()}
        cards = []
        if stances:
            by = {}
            for b, s in stances.items():
                by.setdefault(s, []).append(b)
            text = '; '.join(f'{s} at {_names(b)}' for s, b in sorted(by.items(), key=lambda sb: -len(sb[1])))
            cards.append({'text': f'House views on {name}: {text}.', 'slot': 'outlook',
                          'fact': f'view.stance.{name}', 'source': 'house views, stated positions'})
        cards += _market_views(views, tags, pattern, name, limit=2 if cards else 3)
        by_id = {f.id: f for f in facts}
        if cards and holding_id in by_id:
            f = by_id[holding_id]
            cards.append({'text': f.text, 'source': f.source, 'fact': f.id, 'slot': f.slot})
        return cards
    cards = positioning_cards(views)
    # And the one view that touches this client's largest exposure, as the briefing picked it.
    mine = next((f for f in facts if f.id.startswith('outlook.cio.')), None)
    if mine:
        cards.append({'text': mine.text, 'source': mine.source, 'fact': mine.id, 'slot': mine.slot})
    return cards


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
    # Every house view, quoted, and where the banks lean overall.
    for c in positioning_cards(views):
        out.append(Fact(c['fact'], c['slot'], c['text'], c['source'], 0.0))
    for v in (views or {}).get('items', []):
        text = f'{_short(v["source"])} ({v["label"]}): "{v["text"]}"'
        if f'view.{v["id"]}' not in known and text not in seen:
            seen.add(text)
            out.append(Fact(f'view.{v["id"]}', 'outlook', text, v['url'], 0.0))
    ask = ask_first_card(client)
    out.append(Fact(ask['fact'], ask['slot'], ask['text'], ask['source'], 0.0))
    _BANK[key] = out
    return out


def view_cards(question, facts, market, views, news, store=None, client=None):
    """Cards for 'what do you think about <market>?', or [] when no market is named."""
    if not (VIEW_QUESTION.search(question) or INTEREST.search(question)):
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
