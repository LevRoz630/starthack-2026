# starthack-2026

Team **Look Mom I am Quant** — START Hack Tour St. Gallen 2026.

Case: **UNRISKOMEGA** — [github.com/START-Hack/unriskomega-2026](https://github.com/START-Hack/unriskomega-2026).

- [RULES.md](RULES.md) — the official Hacker Guidebook, converted to markdown.
- [PITCH.md](PITCH.md) — pitch prep todos.
- [PLAN.md](PLAN.md) — the case brief from the kickoff slides, and what we are building.
- [case-slides/](case-slides/) — photos of the kickoff slides: judging criteria, what we get, contacts.

Guidebook source: <https://startglobal1920.notion.site/Hacker-Guidebook-START-Hack-Tour-St-Gallen-3b84da13be328082a75fc33a4a0eb9c5> (fetched 2026-09-18). Notion is authoritative; this copy is a snapshot.

## What the case ships

Data only — no brief, no judging criteria, no partner contacts. Those came at the kickoff; see [PLAN.md](PLAN.md).

| | |
| --- | --- |
| `core-case/portfolio-data/clients.json` | 47 clients, 57 portfolios, 703 security positions, 206 proposals, 1274 transactions, 180 suitability violations, 153 client notes |
| `core-case/portfolio-data/reference.json` | 504 securities, 48101 fund look-through rows, 54 suitability rules, risk/ESG profiles, 16 strategic asset allocations |
| `core-case/GUI-screenshots/` | The current advisor, client, and portfolio dashboards |
| `side-challenge/` | Ten 8-page German quarterly client reports (Q4 2025), from a separate fictional bank — not joinable to `clients.json` |

Three further client-data files arrive later for the live presentation, so the solution has to accept new files of the same shape rather than hardcoding the one we have.
