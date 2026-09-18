"""Load client files and the reference file, and index them for lookups.

The export mixes absent keys with explicit nulls, so every read goes through
`items()` / `.get()` rather than assuming a key or a list exists.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / 'data' / 'core-case' / 'portfolio-data'


def items(obj, key):
    """A list-valued field, or [] when it is absent or null."""
    return (obj or {}).get(key) or []


def portfolios(client):
    """The client's portfolios without double counting.

    A 'Consolidated' portfolio is an overlapping view of other holdings (CASE-038's is
    worth more than the client's whole AUM), so it is skipped whenever the client has
    other portfolios.
    """
    ports = items(client, 'Portfolios')
    own = [p for p in ports if p.get('InvestmentServiceName') != 'Consolidated']
    return own or ports


@dataclass
class Store:
    clients: dict = field(default_factory=dict)       # ClientRef -> client
    securities: dict = field(default_factory=dict)    # Id -> security
    fund_rows: dict = field(default_factory=dict)     # FundSecurityId -> [rows]
    saas: dict = field(default_factory=dict)          # Id -> SAA
    risk_profiles: dict = field(default_factory=dict)  # Id -> profile
    rules: dict = field(default_factory=dict)         # RuleCode -> rule

    def add_clients(self, path):
        """Add every client in a clients.json-shaped file; later files win on ClientRef."""
        with open(path, encoding='utf-8') as f:
            for client in json.load(f):
                self.clients[client['ClientRef']] = client

    def client(self, ref):
        try:
            return self.clients[ref]
        except KeyError:
            raise KeyError(f'unknown client {ref!r}; known: {", ".join(sorted(self.clients))}') from None


def load(client_paths=None, reference_path=None):
    store = Store()
    with open(reference_path or DATA_DIR / 'reference.json', encoding='utf-8') as f:
        ref = json.load(f)
    store.securities = {s['Id']: s for s in items(ref, 'Securities')}
    for row in items(ref, 'FundUnbundlingMappings'):
        store.fund_rows.setdefault(row['FundSecurityId'], []).append(row)
    store.saas = {s['Id']: s for s in items(ref, 'StrategicAssetAllocations')}
    store.risk_profiles = {p['Id']: p for p in items(ref, 'RiskProfiles')}
    store.rules = {r['RuleCode']: r for r in items(ref, 'SuitabilityRules')}
    for path in client_paths or [DATA_DIR / 'clients.json']:
        store.add_clients(path)
    return store
