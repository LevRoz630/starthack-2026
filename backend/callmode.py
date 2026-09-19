"""The briefing for an incoming client call.

Order: who is calling, why they are probably calling, what today's market did to
their book (largest impact first) and what held up. The advisor is given the
client's own numbers to speak from, not a script and not a repeat of the
dashboard's health check. Everything is computed ahead of the call; at ring
time this is a lookup, so sentences are the facts' own text rather than LLM output.

    python -m backend.callmode CASE-019 --scenario tech-selloff
    python -m backend.callmode --rank --scenario tech-selloff
"""

import argparse
import json
import sys
from dataclasses import asdict
from datetime import date, timedelta

from .data import DATA_DIR, ROOT, items, load, portfolios
from .facts import (Fact, relabel, client_name, compute, day, fmt_day, money, pct, short_name,
                    signed_pct)
from .market import MarketState, impact, label, load_scenario
from . import profiles

CALL_SLOTS = ('caller', 'reason', 'digest', 'holding')

TEMPERAMENT_WORDS = ('patient', 'nervous', 'anxious', 'worr', 'cautious', 'long view', 'unconcerned',
                     'simple', 'philosophical')
# A coming need for cash, as opposed to a general preference for holding some.
WITHDRAWAL_WORDS = ('property', 'house', 'tax payment', 'retire', 'inherit', 'withdraw', 'donation', 'purchase',
                    'liquidity need', 'needs approximately')

MIN_SHARE = 0.005     # topics under 0.5% of the book are not worth a sentence
MIN_CHANGE = 0.003    # nor moves under 0.3%
MARKET_REASON = 0.005  # a book move of 0.5% or more makes the market a likely reason to call


_PROFILES = None


def profile_of(client):
    """The Apertus-built profile from data/profiles/, or a keyword profile if the notes changed."""
    global _PROFILES
    if _PROFILES is None:
        _PROFILES = profiles.load_cache()
    return profiles.get(client, _PROFILES)


def signed_money(x, ccy):
    return f'{"+" if x >= 0 else "−"}{money(abs(x), ccy)}'


def _notes(client):
    return sorted(items(client, 'ClientNotes'), key=lambda n: n.get('CreatedByDateUTC') or '', reverse=True)


def reasons(client, store, hit, as_of, base=None):
    """Likely reasons for the call, most likely first, each as a Fact naming its signal."""
    ref = client['ClientRef']
    ccy = client.get('ReportingCurrency') or 'CHF'
    found = []
    base = base if base is not None else compute(client, store, as_of)
    esg = next((f for f in base if f.id == 'health.esg'), None)
    if esg and esg.weight > 0:
        first_word = esg.text.split(' ', 1)[0]
        text = esg.text if first_word.isupper() else esg.text[0].lower() + esg.text[1:]
        found.append((0.7, f'a sustainability concern: {text}', esg.source))
    total = hit['total'] or 1
    book_move = hit['impact'] / total
    losers = sorted((t for t in hit['topics'].values() if t.impact < 0), key=lambda t: t.impact)
    if abs(book_move) >= MARKET_REASON and losers:
        t = losers[0]
        found.append((abs(book_move) * 100,
                      f'the market move: {label(t.dimension, t.bucket)} {signed_pct(t.change)} today, '
                      f'{pct(t.exposure / total)} of the book; about {signed_money(hit["impact"], ccy)} '
                      f'({signed_pct(book_move)}) overall',
                      f'impact of the market feed on clients.json {ref} holdings'))

    cutoff = as_of - timedelta(days=548)
    for note in _notes(client):
        text = (note.get('Note') or '').strip()
        if any(w in text.lower() for w in WITHDRAWAL_WORDS) and day(note['CreatedByDateUTC']) >= cutoff:
            found.append((1.2, f'a withdrawal: note from {fmt_day(day(note["CreatedByDateUTC"]))}: "{text}"',
                          f'clients.json {ref}: ClientNotes'))
            break

    proposals = items(client, 'Proposals')
    rejected = [p for p in proposals if p.get('ProposalStatusName') == 'Abgelehnt' and p.get('ProposedDateUTC')
                and 0 <= (as_of - day(p['ProposedDateUTC'])).days <= 90]
    if rejected:
        p = max(rejected, key=lambda p: p['ProposedDateUTC'])
        found.append((1.0, f'the proposal of {fmt_day(day(p["ProposedDateUTC"]))} that was rejected '
                           f'(reason: {p.get("Reason") or "not given"})',
                      f'clients.json {ref}: Proposals[{p.get("ProposalId")}]'))
    deposits = [p for p in proposals if p.get('Reason') == 'New deposit received' and p.get('ProposedDateUTC')
                and 0 <= (as_of - day(p['ProposedDateUTC'])).days <= 60]
    if deposits:
        p = max(deposits, key=lambda p: p['ProposedDateUTC'])
        found.append((0.9, f'investing new money: a deposit was noted on {fmt_day(day(p["ProposedDateUTC"]))}',
                      f'clients.json {ref}: Proposals[{p.get("ProposalId")}].Reason'))

    maturing = []
    for p in portfolios(client):
        aum = p.get('AssetsUnderManagementInDefaultCurrency') or 0
        for sp in items(p, 'SecurityPositions'):
            m = store.securities.get(sp.get('SecurityId'), {}).get('MaturityDateUtc')
            if m and 0 <= (day(m) - as_of).days <= 60:
                maturing.append((day(m), short_name(sp.get('SecurityName')), (sp.get('PortfolioValuePercentage') or 0) * aum))
    if maturing:
        when, name, amount = min(maturing)
        found.append((0.8, f'reinvestment: {name} matures on {fmt_day(when)} ({money(amount, ccy)})',
                      f'clients.json {ref}: SecurityPositions × reference.json Securities.MaturityDateUtc'))
    aum = client.get('AssetsUnderManagementInDefaultCurrency') or 0
    cash = client.get('LiquidityInDefaultCurrency') or 0
    if aum and cash / aum > 0.1 and not any('withdrawal' in f[1] for f in found):
        found.append((0.5, f'idle cash: {pct(cash / aum)} of the book ({money(cash, ccy)}) is cash',
                      f'clients.json {ref}: LiquidityInDefaultCurrency'))

    found.sort(key=lambda f: -f[0])
    end = lambda text: '' if text.endswith(('.', '"')) else '.'
    return [Fact(f'reason.{i}', 'reason', f'{"Probably" if i == 0 else "Possibly"} {text}{end(text)}', source, score)
            for i, (score, text, source) in enumerate(found[:3])]


def _digest(client, hit, market):
    ref = client['ClientRef']
    ccy = client.get('ReportingCurrency') or 'CHF'
    total = hit['total'] or 1
    interests = {t.get('TagName') for t in items(client, 'Tags')}
    falls = [t for t in hit['topics'].values()
             if t.impact < 0 and t.exposure / total >= MIN_SHARE and abs(t.change) >= MIN_CHANGE]
    falls.sort(key=lambda t: t.impact * (1.5 if t.bucket in interests else 1))
    for t in falls[:3]:
        share = pct(t.exposure / total)
        via = sorted(t.positions.items(), key=lambda kv: -kv[1])[:2]
        if t.dimension == 'fx':
            text = (f'{label(t.dimension, t.bucket).capitalize()} {signed_pct(t.change)} against the franc: '
                    f'{share} of the book is exposed, about {signed_money(t.impact, ccy)}.')
        else:
            names = f', mostly via {" and ".join(n for n, _ in via)}' if t.dimension == 'industry' else ''
            text = (f'{label(t.dimension, t.bucket)} {signed_pct(t.change)} today: {share} of the book, '
                    f'about {signed_money(t.impact, ccy)}{names}.')
        yield Fact(f'digest.{t.dimension}.{t.bucket}', 'digest', text,
                   f'{market.source(t.dimension, t.bucket)} × clients.json {ref} holdings', -t.impact / total)
    if falls and hit['not_modelled'] / total >= 0.05:
        yield Fact('digest.not_modelled', 'digest',
                   f'{pct(hit["not_modelled"] / total)} of the book has no matching market move and is not included.',
                   f'clients.json {ref} holdings without a mapped market move', 0.0)


def _headlines(hit, market):
    """The feed's headlines on what this client was hit by: the 'what happened' behind the numbers."""
    hit_buckets = {(t.dimension, t.bucket) for t in hit['topics'].values() if t.impact < 0}
    kind = 'market feed'
    for i, h in enumerate(market.headlines):
        if (h.get('dimension'), h.get('bucket')) in hit_buckets and h.get('text'):
            yield Fact(f'news.{i}', 'digest', f'Behind the move: "{h["text"]}"',
                       f'{kind} "{market.name}" headline', 0.001)


def _holding(client, hit, market):
    ref = client['ClientRef']
    total = hit['total'] or 1
    up = [t for t in hit['topics'].values()
          if t.dimension != 'fx' and t.change >= 0 and t.exposure / total >= 0.03]
    up.sort(key=lambda t: -t.exposure)
    if up:
        parts = [f'{label(t.dimension, t.bucket)} {signed_pct(t.change)} ({pct(t.exposure / total)} of the book)'
                 for t in up[:3]]
        yield Fact('holding.up', 'holding', f'Holding up today: {"; ".join(parts)}.',
                   f'{market.source(up[0].dimension, up[0].bucket)} × clients.json {ref} holdings',
                   sum(t.exposure for t in up[:3]) / total)
    usd = market.change('fx', 'USD')
    chf_hedged = hit['hedged_chf']
    if usd is not None and usd <= -MIN_CHANGE and chf_hedged:
        yield Fact('holding.hedged', 'holding',
                   f'{" and ".join(chf_hedged)} ({pct(sum(chf_hedged.values()) / total)} of the book) '
                   f'{"are" if len(chf_hedged) > 1 else "is"} hedged to the franc, '
                   f'so the dollar move ({signed_pct(usd)}) does not reach {"them" if len(chf_hedged) > 1 else "it"}.',
                   f'clients.json {ref}: SecurityPositions.SecurityName (hedged share class); '
                   f'{market.source("fx", "USD")}', 0.5)


def call_facts(client, store, market, as_of=None):
    as_of = as_of or date.today()
    base = compute(client, store, as_of)
    hit = impact(client, store, market)
    who = next(f for f in base if f.slot == 'who')
    name = client_name(client)
    details = who.text[len(name):].lstrip(', ') if who.text.startswith(name) else who.text
    out = [Fact('caller', 'caller', f'{name} is calling: {details}', who.source, 1.0)]
    ref = client['ClientRef']
    profile = profile_of(client)
    traits = [f'{profile["temperament"]} temperament' if profile.get('temperament') not in (None, 'unknown') else '',
              f'wants it {profile["wants"]}' if profile.get('wants') not in (None, 'unknown') else '']
    evidence = next((q for key in ('temperament', 'wants') for q in profile.get('evidence', {}).get(key, [])), None)
    if any(traits) and evidence:
        out.append(Fact('caller.profile', 'caller',
                        f'Profile: {", ".join(t for t in traits if t)}. From the notes: "{evidence.strip()}"',
                        f'data/profiles/profiles.json {ref} ({profile.get("source")}) from clients.json ClientNotes', 0.9))
    else:
        note = next((n for n in _notes(client)
                     if any(w in (n.get('Note') or '').lower() for w in TEMPERAMENT_WORDS)), None)
        if note:
            out.append(Fact('caller.profile', 'caller', f'Profile note: "{note["Note"].strip()}"',
                            f'clients.json {ref}: ClientNotes', 0.9))
    for i, pref in enumerate(profile.get('contact_preferences', [])[:1]):
        out.append(Fact(f'caller.contact.{i}', 'caller', f'Contact preference: "{pref.strip()}"',
                        f'data/profiles/profiles.json {ref} from clients.json ClientNotes', 0.8))
    why = reasons(client, store, hit, as_of, base)
    out += why
    digest = list(_digest(client, hit, market)) + list(_headlines(hit, market))
    holding = list(_holding(client, hit, market)) if digest else []
    out += digest + holding
    return relabel(out, client), hit


def build_call(store, ref, market=None, as_of=None):
    market = market or MarketState()
    client = store.client(ref)
    facts, hit = call_facts(client, store, market, as_of)
    order = {slot: i for i, slot in enumerate(CALL_SLOTS)}
    facts.sort(key=lambda f: (order[f.slot], -f.weight))
    total = hit['total'] or 1
    return {
        'client': ref,
        'name': client_name(client),
        'as_of': (as_of or date.today()).isoformat(),
        'market': {'scenario': market.name, 'simulated': market.simulated, 'description': market.description},
        'impact': {'amount': round(hit['impact'], 2), 'share': round(hit['impact'] / total, 5),
                   'not_modelled_share': round(hit['not_modelled'] / total, 5)},
        'words': sum(len(f.text.split()) for f in facts),
        'sentences': [{'slot': f.slot, 'text': f.text, 'facts': [f.id], 'sources': [f.source]} for f in facts],
        'facts': [asdict(f) for f in facts],
    }


def rank_callers(store, market, as_of=None):
    """Clients the market hit hardest, with their most likely reason to call: who to call first."""
    rows = []
    for ref, client in store.clients.items():
        hit = impact(client, store, market)
        why = reasons(client, store, hit, as_of or date.today())
        rows.append({'client': ref, 'name': client_name(client), 'impact': round(hit['impact'], 2),
                     'share': round(hit['impact'] / (hit['total'] or 1), 5),
                     'reason': why[0].text if why else None})
    return sorted(rows, key=lambda r: r['share'])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('clients', nargs='*', help='ClientRef, e.g. CASE-019')
    parser.add_argument('--scenario', help='scenario name in data/scenarios/ or a path; default: no market move')
    parser.add_argument('--rank', action='store_true', help='list the clients most affected, most first')
    parser.add_argument('--clients-file', dest='files', action='append', help='extra clients.json-shaped file')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--as-of', type=date.fromisoformat)
    args = parser.parse_args(argv)

    store = load([DATA_DIR / 'clients.json', *(args.files or [])])
    market = load_scenario(args.scenario) if args.scenario else MarketState()
    if args.rank:
        rows = rank_callers(store, market, args.as_of)[:10]
        if args.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        for r in [] if args.json else rows:
            print(f'{r["client"]}  {r["share"] * 100:+.2f}%  {r["impact"]:+,.0f}  {r["name"]}: {r["reason"] or "-"}')
    for ref in args.clients:
        b = build_call(store, ref, market, args.as_of)
        if args.json:
            print(json.dumps(b, ensure_ascii=False, indent=2))
            continue
        simulated = ' SIMULATED' if market.simulated and market.moves else ''
        print(f'== {ref}  (market: {market.name}{simulated}, {b["words"]} words)')
        for s in b['sentences']:
            print(f'  [{s["slot"]}] {s["text"]}')


if __name__ == '__main__':
    sys.exit(main())
