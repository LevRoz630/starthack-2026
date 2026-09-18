"""Snapshot today's real market moves from Yahoo Finance into a scenario file.

Yahoo has no S&P sector indices, so the SPDR sector ETFs stand in for them; each
tick records the symbol it came from. The snapshot is written once and replayed
like any scenario, so a demo never depends on Yahoo being up.

    python -m backend.yahoo            # writes data/scenarios/live-<date>.json
"""

import json
import sys
from datetime import datetime, timezone

import requests

from .market import SCENARIO_DIR

# Yahoo symbol -> the ticker our market model understands.
SYMBOLS = {
    'XLK': 'S5INFT Index', 'XLV': 'S5HLTH Index', 'XLF': 'S5FINL Index', 'XLI': 'S5INDU Index',
    'XLY': 'S5COND Index', 'XLP': 'S5CONS Index', 'XLB': 'S5MATR Index', 'XLC': 'S5TELS Index',
    'XLRE': 'S5RLST Index', 'XLU': 'S5UTIL Index', 'XLE': 'S5ENRS Index',
    'USDCHF=X': 'USDCHF Curncy', 'EURCHF=X': 'EURCHF Curncy', 'GBPCHF=X': 'GBPCHF Curncy',
    'GC=F': 'XAU Curncy', 'SI=F': 'XAG Curncy', 'PA=F': 'XPD Curncy', 'PL=F': 'XPT Curncy', 'HG=F': 'HG1 Comdty',
    'BTC-USD': 'XBTUSD Curncy', 'ETH-USD': 'XETUSD Curncy',
    '^VIX': 'VIX Index', '^SSMI': 'SMI Index', '^GSPC': 'SPX Index',
}
URL = 'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=5d&interval=1d'


def fetch(symbol):
    resp = requests.get(URL.format(symbol=symbol), headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    resp.raise_for_status()
    meta = resp.json()['chart']['result'][0]['meta']
    return meta['regularMarketPrice'], meta['regularMarketChangePercent']


def snapshot():
    ticks, missing = [], []
    for symbol, ticker in SYMBOLS.items():
        try:
            price, change = fetch(symbol)
        except (requests.RequestException, KeyError, IndexError, TypeError, ValueError):
            missing.append(symbol)
            continue
        origin = f'Yahoo Finance {symbol}'
        ticks += [{'ticker': ticker, 'field': 'CHG_PCT_1D', 'value': round(change, 3), 'origin': origin},
                  {'ticker': ticker, 'field': 'PX_LAST', 'value': price, 'origin': origin}]
    now = datetime.now(timezone.utc)
    return {
        'name': f'live-{now:%Y-%m-%d}',
        'description': f'Real daily moves from Yahoo Finance, taken {now:%Y-%m-%d %H:%M} UTC. '
                       f'Sector moves are SPDR sector ETFs. Missing: {", ".join(missing) or "none"}.',
        'simulated': False,
        'as_of': now.isoformat(timespec='seconds'),
        'ticks': ticks,
        'headlines': [],
    }, missing


def main():
    data, missing = snapshot()
    path = SCENARIO_DIR / f'{data["name"]}.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f'wrote {path.relative_to(SCENARIO_DIR.parent.parent)}: {len(data["ticks"]) // 2} symbols, '
          f'missing: {", ".join(missing) or "none"}')
    return 1 if len(missing) == len(SYMBOLS) else 0


if __name__ == '__main__':
    sys.exit(main())
