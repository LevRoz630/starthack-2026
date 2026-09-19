"""Market state and what a market move does to each client.

A feed delivers Bloomberg-shaped ticks ({ticker, field, value}); `TICKERS` maps
each ticker onto a bucket our holdings can be matched to. The demo feed is a
replayable scenario file in data/scenarios/, marked simulated; a real feed plugs
into `MarketState.apply()` with the same tick shape.

`impact()` walks every holding: equity funds through their look-through rows,
direct holdings through their own classification, cash through its currency.
Currency-hedged share classes get no currency move — that is what hedging does.
Holdings nothing maps to are counted as 'not modelled' rather than guessed.
"""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .data import ROOT, items, portfolios
from .facts import HEDGED, INDUSTRY_ALIASES, short_name

SCENARIO_DIR = ROOT / 'data' / 'scenarios'

# ticker -> (dimension, bucket). Industry moves are S&P 500 sector indices.
TICKERS = {
    'S5INFT Index': ('industry', 'Information Technology'),
    'S5HLTH Index': ('industry', 'Health Care'),
    'S5FINL Index': ('industry', 'Financials'),
    'S5INDU Index': ('industry', 'Industrials'),
    'S5COND Index': ('industry', 'Consumer Discretionary'),
    'S5CONS Index': ('industry', 'Consumer Staples'),
    'S5MATR Index': ('industry', 'Raw materials'),
    'S5TELS Index': ('industry', 'Communication Services'),
    'S5RLST Index': ('industry', 'Real Estate'),
    'S5UTIL Index': ('industry', 'Utilities'),
    'S5ENRS Index': ('industry', 'Energy'),
    'USDCHF Curncy': ('fx', 'USD'),
    'EURCHF Curncy': ('fx', 'EUR'),
    'GBPCHF Curncy': ('fx', 'GBP'),
    'XAU Curncy': ('commodity', 'Gold'),
    'XAG Curncy': ('commodity', 'Silver'),
    'XPD Curncy': ('commodity', 'Palladium'),
    'XPT Curncy': ('commodity', 'Platinum'),
    'HG1 Comdty': ('commodity', 'Copper'),
    'SBR14T Index': ('bonds', 'CHF'),
    'LEGATRUU Index': ('bonds', 'Global'),
    'XBTUSD Curncy': ('crypto', 'BTC'),
    'XETUSD Curncy': ('crypto', 'ETH'),
    'VIX Index': ('volatility', 'VIX'),
    'VSMI Index': ('volatility', 'VSMI'),
    'SMI Index': ('index', 'SMI'),
    'SPX Index': ('index', 'S&P 500'),
}

CURRENCY_GROUPS = {'US-Dollar': 'USD', 'Euro': 'EUR', 'British pound': 'GBP', 'Swiss francs': 'CHF'}
COMMODITY_WORDS = {'gold': 'Gold', 'silver': 'Silver', 'palladium': 'Palladium', 'platinum': 'Platinum',
                   'copper': 'Copper'}

# What to call a bucket when speaking about it.
LABELS = {
    ('fx', 'USD'): 'the dollar', ('fx', 'EUR'): 'the euro', ('fx', 'GBP'): 'the pound',
    ('bonds', 'CHF'): 'Swiss franc bonds', ('bonds', 'Global'): 'foreign bonds',
    ('crypto', 'BTC'): 'Bitcoin', ('crypto', 'ETH'): 'Ether',
}


def label(dimension, bucket):
    return LABELS.get((dimension, bucket), bucket)


@dataclass
class Move:
    dimension: str
    bucket: str
    change: float          # 1-day change as a fraction, e.g. -0.048
    ticker: str
    level: float = None
    origin: str = ''       # where the tick came from, if not the ticker itself (e.g. a proxy symbol)


@dataclass
class MarketState:
    name: str = 'empty'
    description: str = ''
    simulated: bool = True
    as_of: str = ''
    moves: dict = field(default_factory=dict)       # (dimension, bucket) -> Move
    headlines: list = field(default_factory=list)

    def apply(self, ticks):
        """Fold Bloomberg-shaped ticks into the state; unknown tickers are ignored."""
        for t in ticks:
            key = TICKERS.get(t.get('ticker'))
            if not key:
                continue
            move = self.moves.get(key) or Move(*key, 0.0, t['ticker'])
            move.origin = t.get('origin') or move.origin
            if t.get('field') == 'CHG_PCT_1D':
                move.change = float(t['value']) / 100
            elif t.get('field') == 'PX_LAST':
                move.level = float(t['value'])
            self.moves[key] = move

    def change(self, dimension, bucket):
        move = self.moves.get((dimension, bucket))
        return move.change if move else None

    def source(self, dimension, bucket):
        move = self.moves.get((dimension, bucket))
        kind = 'market feed'
        if not move:
            return ''
        via = f' via {move.origin}' if move.origin else ''
        return f'{kind} "{self.name}": {move.ticker} CHG_PCT_1D{via}'


def load_scenario(name_or_path):
    path = Path(name_or_path)
    if not path.suffix:
        path = SCENARIO_DIR / f'{name_or_path}.json'
    with open(path, encoding='utf-8') as f:
        raw = json.load(f)
    state = MarketState(raw.get('name', path.stem), raw.get('description', ''), raw.get('simulated', True),
                        raw.get('as_of', ''), headlines=raw.get('headlines') or [])
    state.apply(raw.get('ticks') or [])
    return state


def scenarios():
    return sorted(p.stem for p in SCENARIO_DIR.glob('*.json'))


@dataclass
class Topic:
    dimension: str
    bucket: str
    exposure: float = 0.0     # reporting currency
    impact: float = 0.0       # reporting currency, today
    change: float = 0.0
    positions: dict = field(default_factory=lambda: defaultdict(float))  # short name -> exposure
    position_impact: dict = field(default_factory=lambda: defaultdict(float))  # short name -> impact


def _commodity(name):
    lower = (name or '').lower()
    return next((c for word, c in COMMODITY_WORDS.items() if word in lower), None)


def impact(client, store, market):
    """Today's estimated impact on one client, per topic.

    Returns {'topics': {(dimension, bucket): Topic}, 'total': book value,
    'impact': summed impact, 'not_modelled': value no move applies to,
    'hedged': {short name: exposure} of currency-hedged holdings,
    'hedged_chf': the same for holdings hedged to the franc, read from the full name,
    'position_impact': {short name: impact} across all topics}.
    An equity holding in USD appears in both its industry topic and the USD topic;
    the two moves are separate and add up.
    """
    topics, hedged, hedged_chf = {}, defaultdict(float), defaultdict(float)
    position_impact = defaultdict(float)
    total = not_modelled = 0.0

    def hit(dimension, bucket, amount, name):
        change = market.change(dimension, bucket)
        if change is None:
            return False
        t = topics.setdefault((dimension, bucket), Topic(dimension, bucket, change=change))
        t.exposure += amount
        t.impact += amount * change
        t.positions[name] += amount
        t.position_impact[name] += amount * change
        position_impact[name] += amount * change
        return True

    for p in portfolios(client):
        aum = p.get('AssetsUnderManagementInDefaultCurrency') or 0
        total += aum
        for sp in items(p, 'SecurityPositions'):
            amount = (sp.get('PortfolioValuePercentage') or 0) * aum
            sec = store.securities.get(sp.get('SecurityId'), {})
            full = sp.get('SecurityName') or sec.get('Name') or ''
            name = short_name(full)
            is_hedged = bool(HEDGED.search(full))
            if is_hedged:
                hedged[name] += amount
                if 'chf' in full.lower():
                    hedged_chf[name] += amount
            rows = store.fund_rows.get(sp.get('SecurityId'))
            if rows:
                modelled = False
                for row in rows:
                    part = amount * (row.get('Weight') or 0) / 100
                    industry = INDUSTRY_ALIASES.get(row.get('IndustryName'), row.get('IndustryName'))
                    modelled |= hit('industry', industry, part, name)
                    if not is_hedged:
                        hit('fx', CURRENCY_GROUPS.get(row.get('CurrencyGroupName'), ''), part, name)
                not_modelled += 0 if modelled else amount
                continue
            asset_class = sec.get('SAA_AssetClassName') or ''
            currency = CURRENCY_GROUPS.get(sec.get('SAA_CurrencyGroupName'), '')
            commodity = _commodity(full)
            if commodity:
                modelled = hit('commodity', commodity, amount, name)
            elif asset_class == 'Bonds':
                modelled = hit('bonds', 'CHF' if currency == 'CHF' else 'Global', amount, name)
            elif asset_class == 'Shares' and sec.get('SAA_IndustryName'):
                industry = sec['SAA_IndustryName']
                modelled = hit('industry', INDUSTRY_ALIASES.get(industry, industry), amount, name)
            else:
                modelled = False
            if not is_hedged and currency not in ('', 'CHF'):
                hit('fx', currency, amount, name)
            not_modelled += 0 if modelled else amount
        for ap in items(p, 'AccountPositions'):
            amount = (ap.get('PortfolioValuePercentage') or 0) * aum
            ccy = ap.get('Currency') or ''
            if ccy in ('BTC', 'ETH'):
                hit('crypto', ccy, amount, ccy)
            elif ccy != 'CHF':
                hit('fx', ccy, amount, f'{ccy} account')
    topics.pop(('fx', ''), None)
    return {'topics': topics, 'total': total, 'impact': sum(t.impact for t in topics.values()),
            'not_modelled': not_modelled, 'hedged': dict(hedged), 'hedged_chf': dict(hedged_chf),
            'position_impact': dict(position_impact)}
