"""Write every client's briefings to one English Markdown file, for checking by hand.

    python -m backend.report                      # docs/verification/briefings-en.md, tech-selloff
    python -m backend.report --scenario chf-spike --out /tmp/chf.md

Uses the fact sentences as they are (no LLM), so what you read is exactly what the
engine computed; Apertus only rephrases these under the checker in phrasing.py.
"""

import argparse
from datetime import date
from pathlib import Path

from .callmode import build_call
from .data import ROOT, load
from .facts import SLOTS, client_name, compute, money, risk_profile
from .market import load_scenario
from .phrasing import select

OUT = ROOT / 'docs' / 'verification' / 'briefings-en.md'

SLOT_TITLES = {'who': 'Who', 'development': 'Development', 'health': 'Health check', 'watch': 'Watch',
               'actions': 'Next best actions'}


def client_section(store, ref, market, as_of):
    client = store.client(ref)
    facts = compute(client, store, as_of)
    chosen = select(facts)
    ccy = client.get('ReportingCurrency') or 'CHF'
    esg = 'yes' if client.get('EsgProfileName') == 'Yes' else 'no'
    lines = [f'## {ref} — {client_name(client)}', '',
             f'{risk_profile(client)} · {money(client.get("AssetsUnderManagementInDefaultCurrency") or 0, ccy)} · '
             f'ESG preference: {esg}', '',
             '### 60-second briefing (dashboard)', '']
    n = 0
    for slot in SLOTS:
        for f in chosen[slot]:
            n += 1
            lines.append(f'{n}. **{SLOT_TITLES[slot]}.** {f.text}  \n   <sub>{f.source}</sub>')
    call = build_call(store, ref, market, as_of)
    tag = 'simulated' if market.simulated else 'real'
    lines += ['', f'### Incoming call during "{market.name}" ({tag} market)', '']
    for i, s in enumerate(call['sentences'], 1):
        lines.append(f'{i}. **{s["slot"]}.** {s["text"]}  \n   <sub>{s["sources"][0]}</sub>')
    spoken = {f.id for slot in SLOTS for f in chosen[slot]}
    rest = [f for f in sorted(facts, key=lambda f: (SLOTS.index(f.slot), -f.weight)) if f.id not in spoken]
    if rest:
        lines += ['', '<details><summary>Other facts on the card</summary>', '']
        lines += [f'- **{SLOT_TITLES[f.slot]}** ({f.weight:.2f}): {f.text}  \n  <sub>{f.source}</sub>' for f in rest]
        lines += ['', '</details>']
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--scenario', default='tech-selloff')
    parser.add_argument('--out', type=Path, default=OUT)
    parser.add_argument('--as-of', type=date.fromisoformat, default=date.today())
    args = parser.parse_args(argv)

    store = load()
    market = load_scenario(args.scenario)
    head = [
        '# Briefings for every client (English, for verification)', '',
        f'Generated {args.as_of.isoformat()} by `python -m backend.report --scenario {args.scenario}`. '
        f'Market: **{market.name}** — {market.description}', '',
        'Each sentence is computed from the data and shows where it came from. Check a few against '
        '`data/core-case/portfolio-data/clients.json` and `reference.json`; report anything wrong with '
        'the client number and the sentence.', '',
        'German display names are translated: *Anlageprofil n* → *Investor profile n* (the data\'s own '
        'English strategy name), portfolio names such as *Konto / Depot* → *Account / Custody*. Suitability '
        'rule names are the data\'s own English `RuleCode`s.', '',
        '**Contents:** ' + ' · '.join(f'[{ref}](#{ref.lower()}--{client_name(store.clients[ref]).lower().replace(" ", "-")})'
                                       for ref in sorted(store.clients)), '',
    ]
    body = [client_section(store, ref, market, args.as_of) for ref in sorted(store.clients)]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text('\n'.join(head) + '\n' + '\n\n---\n\n'.join(body) + '\n', encoding='utf-8')
    print(f'wrote {args.out} ({len(body)} clients)')


if __name__ == '__main__':
    main()
