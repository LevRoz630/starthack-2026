"""Build the 60-second briefing for a client.

    python -m backend.briefing CASE-038
    python -m backend.briefing CASE-038 --no-llm --json
    python -m backend.briefing CASE-101 --clients path/to/test-client.json
"""

import argparse
import json
import sys
import time
from dataclasses import asdict
from datetime import date

from .data import DATA_DIR, load
from .facts import client_name, compute
from .phrasing import phrase, select


def build(store, ref, as_of=None, use_llm=True):
    client = store.client(ref)
    facts = compute(client, store, as_of)
    chosen = select(facts)
    started = time.perf_counter()
    sentences, provider, rejected = phrase(chosen, use_llm)
    by_id = {f.id: f for f in facts}
    return {
        'client': ref,
        'name': client_name(client),
        'as_of': (as_of or date.today()).isoformat(),
        'provider': provider,
        'phrasing_seconds': round(time.perf_counter() - started, 2),
        'words': sum(len(s.text.split()) for s in sentences),
        'sentences': [{**asdict(s), 'sources': [by_id[i].source for i in s.facts if i in by_id]} for s in sentences],
        'rejected': [{'text': s.text, 'reason': reason} for s, reason in rejected],
        'facts': [asdict(f) for f in sorted(facts, key=lambda f: -f.weight)],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('clients', nargs='+', help='ClientRef, e.g. CASE-038')
    parser.add_argument('--clients-file', dest='files', action='append',
                        help='extra clients.json-shaped file (repeatable)')
    parser.add_argument('--no-llm', action='store_true', help='use the fact sentences as they are')
    parser.add_argument('--json', action='store_true', help='print the full briefing as JSON')
    parser.add_argument('--as-of', type=date.fromisoformat, help='reference date, default today')
    args = parser.parse_args(argv)

    store = load([DATA_DIR / 'clients.json', *(args.files or [])])
    for ref in args.clients:
        b = build(store, ref, args.as_of, not args.no_llm)
        if args.json:
            print(json.dumps(b, ensure_ascii=False, indent=2))
            continue
        print(f'== {ref}  ({b["provider"]}, {b["phrasing_seconds"]} s, {b["words"]} words)')
        for s in b['sentences']:
            print(f'  [{s["slot"]}] {s["text"]}')
            for source in s['sources']:
                print(f'      <- {source}')
        for r in b['rejected']:
            print(f'  rejected ({r["reason"]}): {r["text"]}')


if __name__ == '__main__':
    sys.exit(main())
