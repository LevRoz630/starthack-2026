"""Read external custody statements (PDF) into clients.json-shaped clients.

The Q4 2025 reports in data/side-challenge/ ("Privatbank Helvetia AG") share one
layout: page 1 client and totals, page 2 yearly values, page 5 breakdowns, pages
6-7 positions, page 8 transactions. pypdf returns one table cell per line in
reading order, which parses deterministically. A position row that does not fit
the pattern goes to Apertus; its answer is kept only if every number in it
appears on the page.

Each report becomes one client (EXT-01 ...) with a single 'External custody'
portfolio, so the briefing engine treats it like a native one. Securities are
matched to reference.json by ISIN (and currency share class where possible);
the rest get synthetic negative ids with the classification the report gives.

    python -m backend.excustody build          # parse the PDFs, write data/excustody/*.json
    python -m backend.excustody show EXT-01    # the client and its briefing facts
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

from .data import ROOT, load

PDF_DIR = ROOT / 'data' / 'side-challenge'
OUT_DIR = ROOT / 'data' / 'excustody'
CLIENTS_OUT = OUT_DIR / 'clients-external.json'
SECURITIES_OUT = OUT_DIR / 'securities-external.json'
SOURCES_OUT = OUT_DIR / 'sources.json'

logging.getLogger('pypdf').setLevel(logging.ERROR)

SECTIONS = {'Liquidität / Geldmarkt': 'Liquidity', 'Obligationen': 'Bonds', 'Aktien': 'Shares',
            'Alternative Anlagen': 'Alternatives'}
CURRENCY_GROUPS = {'CHF': 'Swiss francs', 'USD': 'US-Dollar', 'EUR': 'Euro', 'GBP': 'British pound'}
MANDATES = {'Ausgewogen': 'Balanced', 'Wachstum': 'Growth', 'Einkommen': 'Income', 'Aktien': 'Equities',
            'Konservativ': 'Conservative', 'Rendite': 'Yield'}
# Share-type prefix in the report's security names -> the data's SecurityTypeName.
PREFIXES = {'N-Akt': 'Shares', 'Inh-Akt': 'Shares', 'Akt': 'Shares', 'GS': 'Dividend right certificates',
            'PS': 'Participation certificate', 'Ant': 'Investment fund'}
ACCOUNT_WORDS = {'Privatkonto': 'Private account', 'Kontokorrent': 'Current account',
                 'Sparkonto': 'Savings account', 'Festgeld': 'Time deposit', 'Geldmarkt': 'Money market'}
BREAKDOWNS = {
    'Portfolio nach Anlagekategoriengruppen': 'asset_classes', 'Portfolio nach Währungen': 'currencies',
    'Aktien nach Ländergruppen': 'equity_regions', 'Nachhaltigkeitseinschätzungen Portfolio': 'sustainability',
    'Aufteilung Aktien/Obligationen nach MSCI ESG Ratings': 'esg_ratings',
    'Aktien nach Branchengruppen': 'equity_sectors',
}
LABELS = {
    'Liqu. / Geldmarkt': 'Liquidity / money market', 'Obligationen': 'Bonds', 'Aktien': 'Equities',
    'Alternative Anlagen': 'Alternative investments', 'Schweizer Franken (CHF)': 'Swiss franc (CHF)',
    'Britisches Pfund (GBP)': 'British pound (GBP)', 'Europa': 'Europe', 'Nordamerika': 'North America',
    'Divers': 'Diversified', 'Schweiz': 'Switzerland', 'Nachhaltig': 'Sustainable',
    'Nicht bewertet': 'Not rated', 'BB und tiefer (Laggard)': 'BB and below (Laggard)', 'Ohne Rating': 'No rating',
    'Übrige': 'Other', 'Basiskonsum': 'Consumer Staples', 'Industrie': 'Industrials',
    'Zyklischer Konsum': 'Consumer Discretionary', 'Kommunikationsdienste': 'Communication Services',
    'Finanzwesen': 'Financials', 'IT': 'Information Technology', 'Gesundheitswesen': 'Health Care',
    'Energie': 'Energy', 'Versorger': 'Utilities', 'Immobilien': 'Real Estate', 'Roh-/Grundstoffe': 'Raw materials',
    'Materialien': 'Raw materials', 'Asien/Pazifik': 'Asia/Pacific',
}
TRANSACTION_KINDS = {'Dividende': 'Dividend', 'Kauf': 'Buy', 'Verkauf': 'Sell', 'Coupon': 'Coupon',
                     'Vermögenszufluss': 'Inflow', 'Vermögensabfluss': 'Outflow', 'Rückzahlung': 'Redemption'}

CCY = re.compile(r'^[A-Z]{3}$')
PCT = re.compile(r'^-?\d+(?:\.\d+)? %$')
NUM = re.compile(r"^[+-]?\d[\d']*(?:\.\d+)?$")
DATE = re.compile(r'^\d\d\.\d\d\.\d\d$')
DATE_PAIR = re.compile(r'^(\d\d)\.(\d\d)\.(\d{4}) / \d\d\.\d\d\.\d{4}$')
SEC_ID = re.compile(r'^(?P<valor>\d[\d ]*) / (?P<isin>[A-Z]{2}[A-Z0-9]{9}\d)$')
IBAN = re.compile(r'^[A-Z]{2}\d{2}(?: [A-Z0-9]{1,4}){3,8}$')
YEAR_ROW = re.compile(r'^(?:ab \d\d\.\d\d\.(\d{4})|(\d{4}))$')


def num(s):
    return float(s.replace("'", '').replace('+', ''))


def pct(s):
    return round(float(s.replace('%', '').strip()) / 100, 6)


def read_pages(path):
    from pypdf import PdfReader
    return [p.extract_text() or '' for p in PdfReader(str(path), strict=False).pages]


def lines_of(text):
    return [l.strip() for l in text.splitlines() if l.strip()]


def after(lines, label):
    return lines[lines.index(label) + 1] if label in lines else None


def parse_row(tokens):
    """One position row: ccy, quantity, name..., id, [cost], [price or fx], date, value, weight."""
    try:
        at = next(i for i, t in enumerate(tokens) if i >= 2 and (SEC_ID.match(t) or IBAN.match(t)))
        rest = tokens[at + 1:]
        d = next(i for i, t in enumerate(rest) if DATE.match(t))
    except StopIteration:
        return None
    if len(rest) != d + 3 or not all(NUM.match(t) for t in rest[:d]) or not NUM.match(rest[d + 1]):
        return None
    m = SEC_ID.match(tokens[at])
    return {'currency': tokens[0], 'quantity': num(tokens[1]), 'name': ' '.join(tokens[2:at]),
            'valor': m['valor'].replace(' ', '') if m else None, 'isin': m['isin'] if m else None,
            'is_account': not m, 'numbers': [num(t) for t in rest[:d]], 'value': num(rest[d + 1]),
            'weight': pct(rest[d + 2])}


def llm_row(tokens, page_text):
    """Fallback for a row the pattern missed: Apertus reads it, every number must be on the page."""
    from .llm import LLMUnavailable, chat
    prompt = ('Extract this one row of a custody statement as JSON with keys currency, quantity, name, valor, '
              'isin, price, value, weight_percent. Use numbers without thousands separators. Row cells, in order:\n'
              + '\n'.join(tokens))
    try:
        raw, _ = chat([{'role': 'user', 'content': prompt}], temperature=0, max_tokens=300)
        row = json.loads(raw[raw.find('{'):raw.rfind('}') + 1])
    except (LLMUnavailable, ValueError):
        return None
    page_numbers = {num(n) for n in re.findall(r"\d[\d']*(?:\.\d+)?", page_text)}
    values = [row.get(k) for k in ('quantity', 'price', 'value', 'weight_percent')]
    if not all(isinstance(v, (int, float)) and float(v) in page_numbers for v in values):
        return None
    return {'currency': row.get('currency'), 'quantity': float(row['quantity']), 'name': row.get('name') or '',
            'valor': row.get('valor'), 'isin': row.get('isin'), 'is_account': not row.get('isin'),
            'numbers': [float(row['price'])], 'value': float(row['value']),
            'weight': float(row['weight_percent']) / 100, 'via': 'apertus'}


def parse_positions(pages):
    """Rows, section totals and the grand total from the 'Detailpositionen' pages."""
    rows, totals, unparsed = [], {}, []
    for number, text in enumerate(pages, 1):
        if 'Detailpositionen' not in text:
            continue
        lines, section, i = lines_of(text), None, 0
        while i < len(lines):
            line = lines[i]
            if line in SECTIONS:
                section = SECTIONS[line]
            elif line.startswith('Total ') and i + 2 < len(lines):
                totals[line[6:]] = (num(lines[i + 1]), pct(lines[i + 2]))
                i += 2
            elif section and CCY.match(line):
                j = next((k for k in range(i + 1, len(lines)) if PCT.match(lines[k])), None)
                if j is None:
                    break
                tokens = lines[i:j + 1]
                row = parse_row(tokens) or llm_row(tokens, text)
                if row:
                    rows.append({**row, 'section': section, 'page': number})
                else:
                    unparsed.append({'page': number, 'cells': tokens})
                i = j
            i += 1
    return rows, totals, unparsed


def parse_header(pages):
    lines = lines_of(pages[0])
    portfolio = after(lines, 'Portfolio') or ''
    mandate = re.search(r'«(.+?)»', portfolio)
    depot = re.search(r'Depot-Nr\. ([\d.]+)', portfolio)
    twr = next((lines[i + 1] for i, l in enumerate(lines[:-1]) if l.startswith('Performance ') and 'TWR' in l), None)
    valuation = after(lines, 'Stichtag Bewertung')
    return {'bank': lines[0], 'client': after(lines, 'Kunde'), 'currency': after(lines, 'Referenzwährung'),
            'valuation_date': '-'.join(reversed(valuation.split('.'))) if valuation else None,
            'total': num((after(lines, 'Vermögen per Stichtag') or '0').split()[-1]),
            'mandate': MANDATES.get(mandate[1], mandate[1]) if mandate else None,
            'depot': depot[1] if depot else None, 'twr': pct(twr) if twr else None}


def parse_history(pages):
    """Yearly rows (year, start, flow, end, result, TWR) from the page with 'Performance vergangene Jahre TWR'."""
    text = next((t for t in pages if 'Performance vergangene Jahre TWR' in t), '')
    lines, out = lines_of(text), []
    for i, line in enumerate(lines):
        m = YEAR_ROW.match(line)
        if m and i + 6 < len(lines) and CCY.match(lines[i + 1]) and PCT.match(lines[i + 6]):
            start, flow, end, result = (num(x) for x in lines[i + 2:i + 6])
            out.append({'year': int(m[1] or m[2]), 'start': start, 'flow': flow, 'end': end, 'result': result,
                        'twr': pct(lines[i + 6])})
    return out


def parse_breakdowns(pages):
    text = next((t for t in pages if 'Grafische Portfoliostruktur' in t), '')
    lines, out, key = lines_of(text), {}, None
    for i, line in enumerate(lines):
        if line in BREAKDOWNS:
            key = BREAKDOWNS[line]
            out[key] = {}
        elif key and i + 1 < len(lines) and PCT.match(lines[i + 1]) and not PCT.match(line):
            out[key][LABELS.get(line, line)] = pct(lines[i + 1])
    return out


def parse_transactions(pages):
    text = next((t for t in pages if t.find('Transaktionen vom') >= 0), '')
    lines = lines_of(text)
    start = next((i + 1 for i, l in enumerate(lines) if l == 'Ertrag'), len(lines))
    rows, current = [], []
    for line in lines[start:] + ['END']:
        if (CCY.match(line) or line == 'END') and current and any(DATE_PAIR.match(c) for c in current):
            rows.append(current)
            current = []
        if line != 'END':
            current.append(line)
    out = []
    for cells in rows:
        d = next(i for i, c in enumerate(cells) if DATE_PAIR.match(c))
        head, nums = cells[1:d], [c for c in cells[d + 1:] if NUM.match(c)]
        if len(nums) < 2:
            continue
        qty = num(head[0]) if head and NUM.match(head[0]) else None
        head = head[1:] if qty is not None else head
        ident = next((SEC_ID.match(c) for c in head if SEC_ID.match(c)), None)
        text_cells = [c for c in head if not SEC_ID.match(c) and not IBAN.match(c)]
        kind = text_cells[0] if text_cells else ''
        kind = next((v for k, v in TRANSACTION_KINDS.items() if kind.startswith(k)),
                    'Custody fees' if kind.startswith('Depotgebühren') else kind)
        dm = DATE_PAIR.match(cells[d])
        out.append({'Currency': cells[0], 'Quantity': qty, 'Kind': kind,
                    'Description': clean_name(text_cells[1]) if len(text_cells) > 1 else '',
                    'Isin': ident['isin'] if ident else None, 'BookingDate': f'{dm[3]}-{dm[2]}-{dm[1]}',
                    'Price': num(nums[0]) if len(nums) == 3 else None, 'AmountCHF': num(nums[-2]),
                    'CostsCHF': num(nums[-1])})
    return out


def clean_name(name):
    """Drop the share-type prefix and the German 'je Titel'."""
    parts = name.split(' ', 1)
    if len(parts) == 2 and parts[0] in PREFIXES:
        name = parts[1]
    return name.replace(' je Titel', ' per share').replace('Übertrag Kontokorrent', 'Transfer from current account').replace('Verwaltungs- und Depotgebühren',
                                                           'Management and custody fees')


def security_type(name, section):
    prefix = name.split(' ', 1)[0]
    if section == 'Bonds':
        return 'Bonds, debt register claims'
    return PREFIXES.get(prefix, 'Investment fund' if section == 'Alternatives' else 'Shares')


def asset_class(section, name):
    if section == 'Alternatives':
        return 'Real estate' if re.search(r'immo|real estate|property', name, re.I) else 'Specialties andCommodities'
    return {'Liquidity': 'Liquidity', 'Bonds': 'Bonds', 'Shares': 'Shares'}[section]


def account_name(name):
    for german, english in ACCOUNT_WORDS.items():
        name = name.replace(german, english)
    return name


def person(name):
    """'Herr Max Muster' -> first/last; companies and families become Company / LastName."""
    if re.search(r'\b(AG|GmbH|SA|Stiftung|Pensionskasse)\b', name):
        return {'Company': name, 'IsClientACompany': True}
    parts = name.split()
    if parts[0] == 'Familie':
        return {'LastName': f'{" ".join(parts[1:])} family', 'IsClientACompany': False}
    if parts[0] in ('Herr', 'Frau'):
        parts = parts[1:]
    return {'FirstName': parts[0], 'LastName': ' '.join(parts[1:]), 'IsClientACompany': False}


def build(pdf_dir=PDF_DIR, reference_store=None):
    store = reference_store or load()
    by_isin_ccy = {(s.get('Isin'), s.get('Currency')): s for s in store.securities.values()}
    by_isin = {}
    for s in store.securities.values():
        by_isin.setdefault(s.get('Isin'), s)
    synthetic, clients, sources, report = {}, [], {}, []

    for n, path in enumerate(sorted(Path(pdf_dir).glob('*.pdf')), 1):
        pages = read_pages(path)
        head = parse_header(pages)
        rows, totals, unparsed = parse_positions(pages)
        history = parse_history(pages)
        ref = f'EXT-{n:02d}'
        ccy = head['currency'] or 'CHF'
        grand = totals.get('Vermögen', (head['total'], 1.0))[0]
        positions, accounts, row_sources, matched = [], [], [], 0
        for r in rows:
            weight = r['value'] / grand if grand else 0
            if r['is_account']:
                accounts.append({'AccountName': account_name(r['name']), 'Currency': r['currency'],
                                 'TotalAmountInPortfolioCurrency': r['value'], 'PortfolioValuePercentage': weight,
                                 'ReportedWeight': r['weight']})
                row_sources.append({'name': account_name(r['name']), 'source': f'{path.name}, page {r["page"]}'})
                continue
            sec = by_isin_ccy.get((r['isin'], r['currency'])) or by_isin.get(r['isin'])
            if sec:
                matched += 1
                sec_id = sec['Id']
            else:
                if r['isin'] not in synthetic:
                    synthetic[r['isin']] = {
                        'Id': -(len(synthetic) + 1), 'Isin': r['isin'], 'Valor': r['valor'],
                        'Name': clean_name(r['name']), 'Currency': r['currency'],
                        'SecurityTypeName': security_type(r['name'], r['section']),
                        'SAA_AssetClassName': asset_class(r['section'], r['name']),
                        'SAA_CurrencyGroupName': CURRENCY_GROUPS.get(r['currency'], 'Andere'),
                        'External': True}
                sec_id = synthetic[r['isin']]['Id']
            price = r['numbers'][-1] if r['numbers'] else None
            cost = r['numbers'][0] if len(r['numbers']) == 2 else None
            positions.append({'SecurityId': sec_id, 'Isin': r['isin'], 'Valor': r['valor'],
                              'SecurityName': clean_name(r['name']), 'Currency': r['currency'],
                              'Quantity': r['quantity'], 'PricePerUnit': price, 'CostPrice': cost,
                              'TotalAmountInPortfolioCurrency': r['value'], 'PortfolioValuePercentage': weight,
                              'ReportedWeight': r['weight'], 'Section': r['section']})
            row_sources.append({'isin': r['isin'], 'name': clean_name(r['name']),
                                'source': f'{path.name}, page {r["page"]}' + (' (Apertus)' if r.get('via') else '')})

        liquidity = sum(a['TotalAmountInPortfolioCurrency'] for a in accounts)
        portfolio = {
            'PortfolioId': 990000 + n, 'PortfolioNr': f'{ref}-01', 'Name': f'External custody ({head["bank"]})',
            'PortfolioCurrency': ccy, 'InvestmentServiceName': 'External custody',
            'StrategyName': f'Mandate: {head["mandate"]}' if head['mandate'] else None, 'ReferenceCurrency': ccy,
            'AssetsUnderManagementInDefaultCurrency': grand, 'LiquidityInDefaultCurrency': liquidity,
            'SecurityPositions': positions, 'AccountPositions': accounts,
            'PerformanceHistory': [{'Date': f'{h["year"]}-12-31', 'Value': h['end']} for h in history if h['end']],
            'ReportedPerformance': history, 'ReportedBreakdowns': parse_breakdowns(pages),
        }
        clients.append({
            'ClientId': -n, 'ClientRef': ref, **person(head['client']),
            'RegulatoryClientTypeName': 'External custody client', 'ReportingCurrency': ccy,
            'AssetsUnderManagementInDefaultCurrency': grand, 'LiquidityInDefaultCurrency': liquidity,
            'Portfolios': [portfolio], 'Proposals': [], 'Transactions': [], 'SuitabilityViolations': [],
            'ClientNotes': [], 'Tags': [],
            'ExternalSource': {'bank': head['bank'], 'file': path.name, 'depot': head['depot'],
                               'mandate': head['mandate'], 'valuation_date': head['valuation_date'],
                               'twr_last_year': head['twr'], 'client_as_reported': head['client']},
            'ExternalTransactions': parse_transactions(pages),
        })
        sources[ref] = {'file': path.name, 'client': 'page 1', 'performance': 'page 2', 'breakdowns': 'page 5',
                        'transactions': 'page 8', 'positions': row_sources, 'unparsed': unparsed}
        summed = sum(p['TotalAmountInPortfolioCurrency'] for p in positions) + liquidity
        section_gaps = {SECTIONS[name]: round(total - sum(r['value'] for r in rows if r['section'] == SECTIONS[name]))
                        for name, (total, _) in totals.items() if name in SECTIONS}
        report.append({'client': ref, 'name': head['client'], 'positions': len(positions), 'accounts': len(accounts),
                       'sum': summed, 'report_total': grand, 'page1_total': head['total'],
                       'diff_pct': (summed - grand) / grand * 100 if grand else None,
                       'isin_matched': matched, 'unparsed': len(unparsed),
                       'via_apertus': sum(1 for r in rows if r.get('via')), 'section_gaps': section_gaps,
                       'years': len(history), 'transactions': len(clients[-1]['ExternalTransactions'])})
    return clients, list(synthetic.values()), sources, report


def write(clients, securities, sources):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for path, data in ((CLIENTS_OUT, clients), (SECURITIES_OUT, securities), (SOURCES_OUT, sources)):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)


def load_external(store, clients_path=CLIENTS_OUT, securities_path=SECURITIES_OUT):
    """Add the external clients to a Store, registering their synthetic securities first."""
    with open(securities_path, encoding='utf-8') as f:
        for sec in json.load(f):
            store.securities.setdefault(sec['Id'], sec)
    before = set(store.clients)
    store.add_clients(clients_path)
    return sorted(set(store.clients) - before)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('build', help='parse the PDFs and write data/excustody/')
    b.add_argument('--dir', type=Path, default=PDF_DIR)
    s = sub.add_parser('show', help='print one external client and its briefing facts')
    s.add_argument('ref')
    args = parser.parse_args(argv)

    if args.cmd == 'build':
        clients, securities, sources, report = build(args.dir)
        write(clients, securities, sources)
        print(f'{"client":7} {"positions":>9} {"accts":>5} {"sum":>12} {"report":>12} {"diff%":>7} '
              f'{"ISIN hit":>8} {"years":>5} {"tx":>3} unparsed')
        for r in report:
            print(f'{r["client"]:7} {r["positions"]:9} {r["accounts"]:5} {r["sum"]:12,.0f} {r["report_total"]:12,.0f} '
                  f'{r["diff_pct"]:7.3f} {r["isin_matched"]:4}/{r["positions"]:<3} {r["years"]:5} '
                  f'{r["transactions"]:3} {r["unparsed"]}  {r["name"]}')
        total, hit = sum(r['positions'] for r in report), sum(r['isin_matched'] for r in report)
        print(f'ISINs matched to reference.json: {hit}/{total} ({hit / total:.0%}); '
              f'synthetic securities: {len(securities)}; wrote {CLIENTS_OUT.relative_to(ROOT)}')
        return 0

    from .facts import compute
    store = load()
    load_external(store)
    client = store.client(args.ref)
    print(json.dumps({k: v for k, v in client.items() if k not in ('Portfolios', 'ExternalTransactions')},
                     ensure_ascii=False, indent=1))
    for f in sorted(compute(client, store), key=lambda f: (f.slot, -f.weight)):
        print(f'[{f.slot} {f.weight:.2f}] {f.text}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
