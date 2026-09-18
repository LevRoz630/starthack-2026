"""The fact engine: everything a briefing may say, computed in code.

Each Fact carries one advisor-facing sentence with its numbers already formatted,
where it came from, and a weight for ranking within its slot. The LLM only
rephrases these sentences; it never sees raw data.
"""

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from functools import lru_cache

from .data import DATA_DIR, items, portfolios

SLOTS = ('who', 'development', 'health', 'watch', 'actions')

# Fund look-through rows and security master data name some industries differently.
INDUSTRY_ALIASES = {
    'Materials': 'Raw materials',
    'Telecommunication Services': 'Communication Services',
    'Banks': 'Financials',
}
LIQUIDITY_WORDS = ('property', 'house', 'tax', 'retire', 'inherit', 'withdraw', 'liquid', 'cash')
# Share-type prefixes and class markers in the bank's security names, e.g.
# "Namen-Aktie Nestle SA", "Na. u. Inh. Ti.-Aktie -B Novo Nordisk A/S", "Anteile -W- UBS ...".
NAME_PREFIX = re.compile(
    r'^(?:Namen-Aktie|Inhaber-Aktie|Genussschein|Partizipationsschein|Na\. u\. Inh\. Ti\.-Aktie|'
    r'Anteile|Accum Shs|Exchange Traded Product)\s*(?:Class\s*)?(?:-[^-]{1,20}-|-\w\b)?\s*')
HEDGED = re.compile(r'(?<!un)hedged', re.IGNORECASE)

# The export keeps some display names in German; briefings are in English.
PORTFOLIO_NAMES = {
    'Konto / Depot': 'Account / Custody', 'Depotberatung': 'Depository advisory',
    'Anlageberatung': 'Investment advisory', 'Vorsorge': 'Pension', 'Vorsorge Indiv': 'Individual pension',
    'Vorsorge indiv': 'Individual pension', 'Zahlen': 'Payments', 'Konsolidierte': 'Consolidated',
}
NAME_WORDS = [(re.compile(r'\s+Aktie$'), ''), (re.compile(r'^Goldbarren\b'), 'Gold bar'),
              (re.compile(r'\bGramm\b'), 'g'), (re.compile(r'\bfein$'), 'fine')]


@dataclass
class Fact:
    id: str
    slot: str
    text: str
    source: str
    weight: float = 0.0


def pct(x):
    return f'{x * 100:.1f}%'


def signed_pct(x):
    return f'{"+" if x >= 0 else "−"}{abs(x) * 100:.1f}%'


def money(x, ccy):
    if abs(x) >= 1e6:
        return f'{ccy} {x / 1e6:.2f}m'
    if abs(x) >= 1e3:
        return f'{ccy} {x / 1e3:.0f}k'
    return f'{ccy} {x:.0f}'


def day(iso):
    return date.fromisoformat(iso[:10])


def fmt_day(d):
    return f'{d.day} {d:%b %Y}'


def client_name(client):
    name = ' '.join(filter(None, [client.get('FirstName'), client.get('LastName')])).strip()
    return name or client.get('Company') or client['ClientRef']


def short_name(name):
    """A security name an advisor can say out loud: the fund after the last
    " - " separator, without share-type prefixes and class markers."""
    name = ' '.join((name or '').split())
    if ' - ' in name:
        name = name.rsplit(' - ', 1)[1]
    name = NAME_PREFIX.sub('', name).strip() or name
    for pattern, english in NAME_WORDS:
        name = pattern.sub(english, name)
    return name


def risk_profile(client):
    """'Anlageprofil 5' as the data's own English strategies call it: 'Investor profile 5'."""
    name = client.get('RiskProfileName') or ''
    return re.sub(r'^Anlageprofil (\d+)$', r'Investor profile \1', name) or 'no risk profile'


def portfolio_label(p):
    name = (p.get('Name') or '').strip()
    return f'{PORTFOLIO_NAMES.get(name, name)} ({p.get("PortfolioNr")})'


def asset_class_label(name):
    return name.replace('andC', 'and C')


def names(ns, limit=2):
    """'A and B', or 'A, B and 3 more'."""
    ns = list(dict.fromkeys(ns))
    shown = ' and '.join(ns[:limit]) if len(ns) <= limit else ', '.join(ns[:limit])
    return shown + (f' and {len(ns) - limit} more' if len(ns) > limit else '')


@lru_cache(maxsize=1)
def _reference():
    """Reference collections the Store does not index: recommendation list, ESG profiles, strategies."""
    with open(DATA_DIR / 'reference.json', encoding='utf-8') as f:
        ref = json.load(f)
    return {
        'recommended': [s['SecurityId'] for lst in items(ref, 'RecommendationLists') for s in items(lst, 'Securities')],
        'esg': {e['Id']: e for e in items(ref, 'EsgProfiles')},
        'strategies': {s['Id']: s for s in items(ref, 'Strategies')},
    }


def _bands(p, store):
    """A portfolio's SAA and its asset-class bands with the actual share of each: (saa, [(mapping, share)])."""
    saa = store.saas.get(p.get('StrategicAssetAllocationId'), {})
    bands = [m for m in items(saa, 'Mappings')
             if m.get('Dimension') == 'AssetClass' and m.get('MinPercentage') is not None
             and m.get('MaxPercentage') is not None]
    actual = defaultdict(float)
    for sp in items(p, 'SecurityPositions'):
        sec = store.securities.get(sp.get('SecurityId'), {})
        actual[sec.get('SAA_AssetClassName') or 'Unclassified'] += sp.get('PortfolioValuePercentage') or 0
    for ap in items(p, 'AccountPositions'):
        actual['Liquidity'] += ap.get('PortfolioValuePercentage') or 0
    return saa, [(m, actual.get(m['Category'], 0)) for m in bands]


def _holdings(client, store):
    """(position, security, amount in reporting currency) for every security position."""
    for p in portfolios(client):
        aum = p.get('AssetsUnderManagementInDefaultCurrency') or 0
        for sp in items(p, 'SecurityPositions'):
            yield sp, store.securities.get(sp.get('SecurityId'), {}), (sp.get('PortfolioValuePercentage') or 0) * aum


def _book(client):
    return sum(p.get('AssetsUnderManagementInDefaultCurrency') or 0 for p in portfolios(client)) or 1


def _overridden(client):
    return {o.get('RuleCode') for o in items(client, 'IndividualRuleOverrides')}


def _trades(client, proposal):
    """A proposal's orders, and its buy and sell names, largest first.

    A proposal's SecurityPositions are the whole target portfolio (never negative);
    the trades are its Transactions, signed. Expiry records are not orders.
    """
    orders = [t for t in items(client, 'Transactions')
              if t.get('ProposalId') == proposal.get('ProposalId') and not t.get('IsExpiry')]
    # Cash movements have no security; they are orders but not something to name.
    by_size = sorted((t for t in orders if t.get('SecurityName')), key=lambda t: -abs(t.get('TotalAmount') or 0))
    buys = [short_name(t['SecurityName']) for t in by_size if (t.get('QuantityForTransaction') or 0) > 0]
    sells = [short_name(t['SecurityName']) for t in by_size if (t.get('QuantityForTransaction') or 0) < 0]
    return orders, buys, sells


def _trade_text(buys, sells):
    return ' and '.join(([f'buy {names(buys)}'] if buys else []) + ([f'sell {names(sells)}'] if sells else []))


def exposures(client, store):
    """Client-level exposure in reporting currency, with funds looked through.

    Returns {'industry': {bucket: amount}, 'asset_class': ..., 'currency': ...,
    'industry_positions': {bucket: {position name: amount}}, 'total': amount}.
    Asset class and currency use the SAA taxonomy of the holding itself, as the
    bank's own allocation checks do; industry goes through fund breakdowns where
    they exist and is 'Not classified' otherwise.
    """
    out = {'industry': defaultdict(float), 'asset_class': defaultdict(float),
           'currency': defaultdict(float), 'industry_positions': defaultdict(lambda: defaultdict(float)),
           'total': 0.0}
    for p in portfolios(client):
        aum = p.get('AssetsUnderManagementInDefaultCurrency') or 0
        out['total'] += aum
        for sp in items(p, 'SecurityPositions'):
            amount = (sp.get('PortfolioValuePercentage') or 0) * aum
            sec = store.securities.get(sp.get('SecurityId'), {})
            name = short_name(sp.get('SecurityName') or sec.get('Name') or sp.get('Isin'))
            out['asset_class'][sec.get('SAA_AssetClassName') or 'Unclassified'] += amount
            out['currency'][sec.get('SAA_CurrencyGroupName') or sp.get('Currency') or 'Unknown'] += amount
            rows = store.fund_rows.get(sp.get('SecurityId'))
            if rows:
                for row in rows:
                    bucket = INDUSTRY_ALIASES.get(row.get('IndustryName'), row.get('IndustryName') or 'Not classified')
                    part = amount * (row.get('Weight') or 0) / 100
                    out['industry'][bucket] += part
                    out['industry_positions'][bucket][name] += part
            else:
                industry = sec.get('SAA_IndustryName')
                bucket = INDUSTRY_ALIASES.get(industry, industry) if industry else 'Not classified'
                out['industry'][bucket] += amount
                out['industry_positions'][bucket][name] += amount
        for ap in items(p, 'AccountPositions'):
            amount = (ap.get('PortfolioValuePercentage') or 0) * aum
            out['asset_class']['Liquidity'] += amount
            out['currency'][ap.get('Currency') or 'Unknown'] += amount
    return out


def _who(client, store, ccy):
    ref = client['ClientRef']
    profile = risk_profile(client)
    esg = ', ESG preference' if client.get('EsgProfileName') == 'Yes' else ''
    n = len(portfolios(client))
    aum = client.get('AssetsUnderManagementInDefaultCurrency') or 0
    yield Fact('who', 'who',
               f'{client_name(client)}, {profile}{esg}, {money(aum, ccy)} across {n} portfolio{"s" if n != 1 else ""}.',
               f'clients.json {ref}: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency', 1.0)


def _development(client):
    ref = client['ClientRef']
    ports = [p for p in portfolios(client) if items(p, 'PerformanceHistory')]
    if not ports:
        return
    if len({p.get('PortfolioCurrency') for p in ports}) > 1:
        ports = [max(ports, key=lambda p: p.get('AssetsUnderManagementInDefaultCurrency') or 0)]
    series = [{pt['Date']: pt.get('Value') or 0 for pt in items(p, 'PerformanceHistory')} for p in ports]
    dates = sorted(set.intersection(*(set(s) for s in series)))
    if len(dates) < 2:
        return
    value = {d: sum(s[d] for s in series) for d in dates}
    ccy = ports[0].get('PortfolioCurrency') or ''
    last, first = day(dates[-1]), day(dates[0])
    year_ago = last.replace(year=last.year - 1).isoformat()
    parts = []
    if year_ago in value and value[year_ago]:
        parts.append(f'{signed_pct(value[dates[-1]] / value[year_ago] - 1)} over the 12 months to {last:%b %Y}')
    if value[dates[0]]:
        parts.append(f'{signed_pct(value[dates[-1]] / value[dates[0]] - 1)} since {first:%b %Y}')
    scope = 'Portfolio value' if len(ports) == 1 else 'Combined portfolio value'
    yield Fact('development', 'development',
               f'{scope} {" and ".join(parts)}, now {money(value[dates[-1]], ccy)}; '
               f'value change including deposits and withdrawals.',
               f'clients.json {ref}: PerformanceHistory of {", ".join(p.get("PortfolioNr") for p in ports)}', 1.0)


def _health(client, store, as_of):
    ref = client['ClientRef']
    ports = portfolios(client)
    many = len(ports) > 1
    profile = store.risk_profiles.get(client.get('RiskProfileId'), {})

    for p in ports:
        where = f' in {portfolio_label(p)}' if many else ''
        vol, max_vol = p.get('Volatility') or 0, profile.get('MaxVola')
        if max_vol and vol > max_vol:
            yield Fact(f'health.vol.{p.get("PortfolioNr")}', 'health',
                       f'Volatility{where} is {pct(vol)}, above the {pct(max_vol)} maximum of {risk_profile(client)}.',
                       f'clients.json {ref}: Portfolios[{p.get("PortfolioNr")}].Volatility; reference.json RiskProfiles.MaxVola',
                       (vol - max_vol) * 10)

        saa, bands = _bands(p, store)
        for m, share in bands:
            lo, hi = m['MinPercentage'], m['MaxPercentage']
            gap = lo - share if share < lo else share - hi if share > hi else 0
            if gap <= 0:
                continue
            label = asset_class_label(m['Category'])
            target = m.get('TargetPercentage')
            target_text = f', target {pct(target)}' if target is not None else ''
            source = (f'clients.json {ref}: Portfolios[{p.get("PortfolioNr")}] positions; '
                      f'reference.json StrategicAssetAllocations[{saa.get("Id")}] AssetClass "{m["Category"]}"')
            yield Fact(f'health.saa.{p.get("PortfolioNr")}.{m["Category"]}', 'health',
                       f'{label}{where} at {pct(share)}, outside its {pct(lo)}–{pct(hi)} band{target_text}.',
                       source, gap * 5)
            direction = 'down' if share > hi else 'up'
            yield Fact(f'actions.saa.{p.get("PortfolioNr")}.{m["Category"]}', 'actions',
                       f'Rebalance {label}{where} {direction} toward {pct(target if target is not None else (lo + hi) / 2)}.',
                       source, gap * 5)

    # Rules the bank has waived for this client are neither counted nor turned into actions.
    violations = [v for v in items(client, 'SuitabilityViolations') if v.get('RuleCode') not in _overridden(client)]
    if violations:
        names = {sp.get('Isin'): short_name(sp.get('SecurityName')) for p in ports for sp in items(p, 'SecurityPositions')}
        errors = [v for v in violations if v.get('Severity') == 'Error']
        warnings = [v for v in violations if v.get('Severity') != 'Error']
        worst = max(violations, key=lambda v: (v.get('Severity') == 'Error', v.get('LastViolatedDateUTC') or ''))
        on = f' on {names[worst["SecurityIsin"]]}' if names.get(worst.get('SecurityIsin')) else ''
        yield Fact('health.violations', 'health',
                   f'{len(errors)} suitability error{"s" if len(errors) != 1 else ""} and '
                   f'{len(warnings)} warning{"s" if len(warnings) != 1 else ""} open; '
                   f'most serious: "{worst.get("RuleCode")}"{on}.',
                   f'clients.json {ref}: SuitabilityViolations', 1.0 * len(errors) + 0.3 * len(warnings))
        for i, v in enumerate(sorted(violations, key=lambda v: v.get('Severity') != 'Error')[:3]):
            on = f' on {names[v["SecurityIsin"]]}' if names.get(v.get('SecurityIsin')) else ''
            yield Fact(f'actions.violation.{i}', 'actions',
                       f'Resolve "{v.get("RuleCode")}"{on}.',
                       f'clients.json {ref}: SuitabilityViolations[Id={v.get("Id")}]',
                       1.0 if v.get('Severity') == 'Error' else 0.3)

    yield from _health_extra(client, store, violations)

    if client.get('ProfilingDateUtc'):
        assessed = day(client['ProfilingDateUtc'])
        years = (as_of - assessed).days / 365.25
        if years >= 3:
            yield Fact('health.profile_age', 'health',
                       f'Risk profile last assessed {fmt_day(assessed)}, {years:.0f} years ago.',
                       f'clients.json {ref}: ProfilingDateUtc', 0.1 * (years - 2))


def _health_extra(client, store, violations):
    ref = client['ClientRef']
    total = _book(client)
    held = list(_holdings(client, store))
    profile = store.risk_profiles.get(client.get('RiskProfileId'), {})

    max_prc = profile.get('MaxPRC')
    if max_prc is not None:
        above = defaultdict(float)
        for sp, sec, amount in held:
            if sec.get('PRC') is not None and sec['PRC'] > max_prc:
                above[short_name(sp.get('SecurityName'))] += amount
        if above:
            share = sum(above.values()) / total
            ranked = sorted(above, key=lambda n: -above[n])
            yield Fact('health.prc', 'health',
                       f'{len(above)} holding{"s" if len(above) != 1 else ""} above the product risk class limit of '
                       f'{risk_profile(client)} (maximum {max_prc}): {names(ranked)}, {pct(share)} of the book.',
                       f'reference.json Securities.PRC vs RiskProfiles.MaxPRC; clients.json {ref} positions',
                       share * 2)

    esg = _reference()['esg'].get(client.get('EsgProfileId'), {})
    if client.get('EsgProfileName') == 'Yes' and esg.get('MinimumPositionLevel') is not None:
        floor, minimum = esg['MinimumPositionLevel'], esg.get('MinimumLevel', esg['MinimumPositionLevel'])
        scored = [(sp, sec, a) for sp, sec, a in held if sec.get('SustainabilityScore') is not None]
        weight = sum(a for _, _, a in scored)
        if weight:
            below = defaultdict(float)
            for sp, sec, amount in scored:
                if sec['SustainabilityScore'] < floor:
                    below[short_name(sp.get('SecurityName'))] += amount
            average = sum(sec['SustainabilityScore'] * a for _, sec, a in scored) / weight
            unscored = sum(a for _, sec, a in held if sec.get('SustainabilityScore') is None) / total
            below_text = ''
            if below:
                ranked = sorted(below, key=lambda n: -below[n])
                below_text = (f'; {len(below)} holding{"s" if len(below) != 1 else ""} below the per-position '
                              f'minimum ({names(ranked)}, {pct(sum(below.values()) / total)} of the book)')
            unscored_text = f'; {pct(unscored)} of the book has no score' if unscored >= 0.01 else ''
            yield Fact('health.esg', 'health',
                       f'ESG client: average sustainability score {average:.1f} of 10 against a minimum of '
                       f'{minimum:.1f}{below_text}{unscored_text}.',
                       f'reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[{esg.get("Id")}] '
                       f'MinimumLevel / MinimumPositionLevel; clients.json {ref} positions',
                       sum(below.values()) / total * 2 + (0.5 if average < minimum else 0))

    strategies = _reference()['strategies']
    has_vol_rule = any('volatil' in (v.get('RuleCode') or '').lower() for v in violations)
    for p in portfolios(client):
        strategy = strategies.get(p.get('StrategyId'), {})
        vol, low = p.get('Volatility') or 0, strategy.get('VolatilityMinimum')
        if not has_vol_rule and vol > 0 and low and vol < low:
            yield Fact(f'health.vol_low.{p.get("PortfolioNr")}', 'health',
                       f'Volatility of {portfolio_label(p)} is {pct(vol)}, below the {pct(low)} minimum of '
                       f'{strategy.get("Name")}.',
                       f'clients.json {ref}: Portfolios[{p.get("PortfolioNr")}].Volatility; reference.json Strategies',
                       (low - vol) * 10)

    submitted = [p for p in items(client, 'Proposals') if p.get('ProposalStatusName') == 'Final'
                 and p.get('TransactionsSubmittedDateUTC')]
    if submitted:
        latest = max(submitted, key=lambda p: p['TransactionsSubmittedDateUTC'])
        orders, _, _ = _trades(client, latest)
        warned = [t for t in orders if t.get('ForwardState') == 2]
        if warned:
            yield Fact('health.order_warnings', 'health',
                       f'{len(warned)} of {len(orders)} order{"s" if len(orders) != 1 else ""} from the proposal of '
                       f'{fmt_day(day(latest["TransactionsSubmittedDateUTC"]))} were forwarded with a warning.',
                       f'clients.json {ref}: Transactions[ProposalId={latest.get("ProposalId")}].ForwardState = 2',
                       # Most finalised orders in the data carry this state, so it ranks low.
                       0.15)


def _watch_extra(client, store):
    ref = client['ClientRef']
    total = _book(client)
    off_list = defaultdict(float)
    for sp, sec, amount in _holdings(client, store):
        if sec and not sec.get('InRecommendationList'):
            off_list[short_name(sp.get('SecurityName'))] += amount
    share = sum(off_list.values()) / total
    if share >= 0.1:
        ranked = sorted(off_list, key=lambda n: -off_list[n])
        yield Fact('watch.off_list', 'watch',
                   f'{pct(share)} of the book is in holdings on none of the bank\'s recommendation lists, '
                   f'largest {names(ranked)}.',
                   f'reference.json Securities.InRecommendationList; clients.json {ref} positions', share * 0.5)

    for p in portfolios(client):
        er, var = p.get('ExpectedReturn'), p.get('ValueAtRisk')
        if er or var:
            when = f', {fmt_day(day(p["FactoryDateUtc"]))}' if p.get('FactoryDateUtc') else ''
            yield Fact(f'watch.risk_engine.{p.get("PortfolioNr")}', 'watch',
                       f'Risk engine for {portfolio_label(p)}{when}: expected return {pct(er or 0)}, '
                       f'value at risk {pct(var or 0)}.',
                       f'clients.json {ref}: Portfolios[{p.get("PortfolioNr")}].ExpectedReturn, ValueAtRisk', 0.03)

    finalised = [p for p in items(client, 'Proposals') if p.get('ProposalStatusName') == 'Final'
                 and p.get('FinalizedDateUTC')]
    if finalised:
        latest = max(finalised, key=lambda p: p['FinalizedDateUTC'])
        _, buys, sells = _trades(client, latest)
        if buys or sells:
            yield Fact('watch.last_proposal', 'watch',
                       f'The last finalised proposal ({fmt_day(day(latest["FinalizedDateUTC"]))}, '
                       f'reason: {latest.get("Reason") or "not given"}) ordered to {_trade_text(buys, sells)}.',
                       f'clients.json {ref}: Proposals[{latest.get("ProposalId")}] × Transactions', 0.08)

    for code in sorted(c for c in _overridden(client) if c):
        yield Fact(f'watch.override.{code}', 'watch',
                   f'The rule "{code}" is waived for this client by an individual override.',
                   f'clients.json {ref}: IndividualRuleOverrides', 0.02)


def _candidates(client, store):
    """Recommendation-list securities for the asset class furthest under its band, or for idle cash."""
    under = []
    for p in portfolios(client):
        _, bands = _bands(p, store)
        under += [(m['MinPercentage'] - share, m['Category']) for m, share in bands
                  if share < m['MinPercentage'] and m['Category'] != 'Liquidity']
    aum = client.get('AssetsUnderManagementInDefaultCurrency') or 0
    idle_cash = bool(aum) and (client.get('LiquidityInDefaultCurrency') or 0) / aum > 0.1
    if not under and not idle_cash:
        return
    category = max(under)[1] if under else 'Shares'
    held = {sp.get('SecurityId') for sp, _, _ in _holdings(client, store)}
    ccy = client.get('ReportingCurrency') or 'CHF'
    pool = [store.securities[i] for i in _reference()['recommended'] if i in store.securities and i not in held]
    pool = [s for s in pool if s.get('SAA_AssetClassName') == category]
    pool.sort(key=lambda s: (s.get('Currency') != ccy, -(s.get('SustainabilityScore') or 0), s.get('Name') or ''))
    picks = list(dict.fromkeys(short_name(s.get('Name')) for s in pool))[:2]
    if picks:
        why = f'{asset_class_label(category)} is under its band' if under else 'cash is above 10% of the book'
        yield Fact('actions.candidates', 'actions',
                   f'Candidates from the recommendation list for {asset_class_label(category)}: '
                   f'{" and ".join(picks)} ({why}).',
                   f'reference.json RecommendationLists "Recommendation list free assets", not held, '
                   f'{ccy} first, ordered by SustainabilityScore', 0.2)


def _watch(client, store, exp, ccy):
    ref = client['ClientRef']
    total = exp['total'] or 1
    ranked = sorted(((k, v) for k, v in exp['industry'].items() if k != 'Not classified'),
                    key=lambda kv: kv[1], reverse=True)
    for bucket, amount in ranked[:2]:
        via = sorted(exp['industry_positions'][bucket].items(), key=lambda kv: kv[1], reverse=True)[:2]
        yield Fact(f'watch.industry.{bucket}', 'watch',
                   f'{bucket} is {pct(amount / total)} of the book ({money(amount, ccy)}) after fund look-through, '
                   f'mostly via {" and ".join(name for name, _ in via)}.',
                   f'clients.json {ref}: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName',
                   amount / total)
    unclassified = exp['industry'].get('Not classified', 0)
    if unclassified / total > 0.2:
        yield Fact('watch.unclassified', 'watch',
                   f'{pct(unclassified / total)} of the book has no industry breakdown (bonds, funds without look-through).',
                   f'clients.json {ref}: SecurityPositions; reference.json FundUnbundlingMappings', 0.0)

    for p in portfolios(client):
        aum = p.get('AssetsUnderManagementInDefaultCurrency') or 0
        for sp in items(p, 'SecurityPositions'):
            sec = store.securities.get(sp.get('SecurityId'), {})
            share = (sp.get('PortfolioValuePercentage') or 0) * aum / total
            if share > 0.1 and sec.get('SecurityTypeName') != 'Investment fund':
                yield Fact(f'watch.concentration.{sp.get("SecurityId")}', 'watch',
                           f'{short_name(sp.get("SecurityName"))} alone is {pct(share)} of the book.',
                           f'clients.json {ref}: Portfolios[{p.get("PortfolioNr")}].SecurityPositions', share)
        vol = p.get('Volatility') or 0
        positions = items(p, 'SecurityPositions')
        if vol > 0 and positions:
            top = max(positions, key=lambda sp: sp.get('ContributionVolatility') or 0)
            share = (top.get('ContributionVolatility') or 0) / vol
            if share >= 0.15:
                yield Fact(f'watch.risk.{p.get("PortfolioNr")}', 'watch',
                           f'{short_name(top.get("SecurityName"))} drives {pct(share)} of the volatility of {portfolio_label(p)}.',
                           f'clients.json {ref}: Portfolios[{p.get("PortfolioNr")}].SecurityPositions.ContributionVolatility',
                           share * aum / total)

    hedged = defaultdict(float)
    for p in portfolios(client):
        aum = p.get('AssetsUnderManagementInDefaultCurrency') or 0
        for sp in items(p, 'SecurityPositions'):
            if HEDGED.search(sp.get('SecurityName') or ''):
                hedged[short_name(sp['SecurityName'])] += (sp.get('PortfolioValuePercentage') or 0) * aum
    if hedged:
        yield Fact('watch.hedged', 'watch',
                   f'Currency-hedged holdings: {", ".join(hedged)} ({pct(sum(hedged.values()) / total)} of the book).',
                   f'clients.json {ref}: SecurityPositions.SecurityName', 0.05)

    notes = sorted(items(client, 'ClientNotes'), key=lambda n: n.get('CreatedByDateUTC') or '', reverse=True)
    for i, note in enumerate(notes[:2]):
        text = (note.get('Note') or '').strip()
        liquidity = any(w in text.lower() for w in LIQUIDITY_WORDS)
        yield Fact(f'watch.note.{i}', 'watch',
                   f'Note from {fmt_day(day(note["CreatedByDateUTC"]))}: "{text}"',
                   f'clients.json {ref}: ClientNotes', 0.5 if liquidity else 0.15 - 0.05 * i)


def _actions(client, as_of, ccy):
    ref = client['ClientRef']
    aum = client.get('AssetsUnderManagementInDefaultCurrency') or 0
    cash = client.get('LiquidityInDefaultCurrency') or 0
    if aum and cash / aum > 0.1:
        needs = [n for n in items(client, 'ClientNotes') if any(w in (n.get('Note') or '').lower() for w in LIQUIDITY_WORDS)]
        if needs:
            latest = max(needs, key=lambda n: n.get('CreatedByDateUTC') or '')
            yield Fact('actions.cash', 'actions',
                       f'Keep the {pct(cash / aum)} cash ({money(cash, ccy)}) in view of the note from '
                       f'{fmt_day(day(latest["CreatedByDateUTC"]))}: "{latest.get("Note", "").strip()}"',
                       f'clients.json {ref}: LiquidityInDefaultCurrency, ClientNotes', 0.3)
        else:
            yield Fact('actions.cash', 'actions',
                       f'Deploy idle liquidity: {pct(cash / aum)} of the book ({money(cash, ccy)}) is cash.',
                       f'clients.json {ref}: LiquidityInDefaultCurrency', (cash / aum - 0.1) * 3)

    proposals = items(client, 'Proposals')
    finalised = [p for p in proposals if p.get('FinalizedDateUTC')]
    if finalised:
        last = max(day(p['FinalizedDateUTC']) for p in finalised)
        if (as_of - last).days > 365:
            yield Fact('actions.review', 'actions',
                       f'Book a review: the last finalised proposal was on {fmt_day(last)}.',
                       f'clients.json {ref}: Proposals.FinalizedDateUTC', 0.4)
    else:
        yield Fact('actions.review', 'actions', 'Book a review: no finalised proposal on record.',
                   f'clients.json {ref}: Proposals', 0.4)

    rejected = [p for p in proposals if p.get('ProposalStatusName') == 'Abgelehnt' and p.get('ProposedDateUTC')
                and 0 <= (as_of - day(p['ProposedDateUTC'])).days <= 90]
    if rejected:
        latest = max(rejected, key=lambda p: p['ProposedDateUTC'])
        _, buys, sells = _trades(client, latest)
        wanted = f'; it would have had the client {_trade_text(buys, sells)}' if buys or sells else ''
        yield Fact('actions.rejected', 'actions',
                   f'Follow up on the proposal of {fmt_day(day(latest["ProposedDateUTC"]))} that was rejected '
                   f'(reason: {latest.get("Reason") or "not given"}){wanted}.',
                   f'clients.json {ref}: Proposals[{latest.get("ProposalId")}] × Transactions', 0.5)


def compute(client, store, as_of=None):
    """All facts for one client, unranked."""
    as_of = as_of or date.today()
    ccy = client.get('ReportingCurrency') or 'CHF'
    exp = exposures(client, store)
    return [*_who(client, store, ccy), *_development(client), *_health(client, store, as_of),
            *_watch(client, store, exp, ccy), *_watch_extra(client, store),
            *_actions(client, as_of, ccy), *_candidates(client, store)]
