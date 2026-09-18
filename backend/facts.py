"""The fact engine: everything a briefing may say, computed in code.

Each Fact carries one advisor-facing sentence with its numbers already formatted,
where it came from, and a weight for ranking within its slot. The LLM only
rephrases these sentences; it never sees raw data.
"""

import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date

from .data import items, portfolios

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
    name = (name or '').strip()
    if ' - ' in name:
        name = name.rsplit(' - ', 1)[1]
    return NAME_PREFIX.sub('', name).strip() or name


def portfolio_label(p):
    return f'{(p.get("Name") or "").strip()} ({p.get("PortfolioNr")})'


def asset_class_label(name):
    return name.replace('andC', 'and C')


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
    profile = client.get('RiskProfileName') or 'no risk profile'
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
                       f'Volatility{where} is {pct(vol)}, above the {pct(max_vol)} maximum of {client.get("RiskProfileName")}.',
                       f'clients.json {ref}: Portfolios[{p.get("PortfolioNr")}].Volatility; reference.json RiskProfiles.MaxVola',
                       (vol - max_vol) * 10)

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
        for m in bands:
            share, lo, hi = actual.get(m['Category'], 0), m['MinPercentage'], m['MaxPercentage']
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

    violations = items(client, 'SuitabilityViolations')
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

    if client.get('ProfilingDateUtc'):
        assessed = day(client['ProfilingDateUtc'])
        years = (as_of - assessed).days / 365.25
        if years >= 3:
            yield Fact('health.profile_age', 'health',
                       f'Risk profile last assessed {fmt_day(assessed)}, {years:.0f} years ago.',
                       f'clients.json {ref}: ProfilingDateUtc', 0.1 * (years - 2))


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
        yield Fact('actions.rejected', 'actions',
                   f'Follow up on the proposal of {fmt_day(day(latest["ProposedDateUTC"]))} that was rejected '
                   f'(reason: {latest.get("Reason") or "not given"}).',
                   f'clients.json {ref}: Proposals[{latest.get("ProposalId")}]', 0.5)


def compute(client, store, as_of=None):
    """All facts for one client, unranked."""
    as_of = as_of or date.today()
    ccy = client.get('ReportingCurrency') or 'CHF'
    exp = exposures(client, store)
    return [*_who(client, store, ccy), *_development(client), *_health(client, store, as_of),
            *_watch(client, store, exp, ccy), *_actions(client, as_of, ccy)]
