# starthack-2026

Team **Look Mom I am Quant** — START Hack Tour St. Gallen 2026.

Case: **UNRISKOMEGA** — [github.com/START-Hack/unriskomega-2026](https://github.com/START-Hack/unriskomega-2026).

- [docs/PLAN.md](docs/PLAN.md) — the case brief from the kickoff slides, and what we are building.
- [docs/JUDGES.md](docs/JUDGES.md) — partner contacts from the kickoff.
- [docs/screenshots.md](docs/screenshots.md) — what the URO Advisor UI screenshots show.
- [docs/RULES.md](docs/RULES.md) — the official Hacker Guidebook, converted to markdown.

## Run the briefing

```
pip install -r requirements.txt
python -m backend.briefing CASE-038            # phrased by Apertus (SWISSCOM_KEY in .env)
python -m backend.briefing CASE-038 --no-llm   # fact sentences only, no API call
python -m backend.briefing CASE-038 --json     # everything, incl. all facts and sources
python -m pytest tests                          # offline, no API calls
```

API — what the dashboard and the phone talk to:

```
DEMO_SCENARIO=tech-selloff uvicorn backend.api:app --port 8000
```

| Endpoint | What |
| --- | --- |
| `GET /clients`, `POST /clients` | list; upload a clients.json-shaped file (multipart `file`) — the jury's test client |
| `GET /briefing/{ref}` | the 60-second briefing; `phrasing: pending` until Apertus has phrased it in the background |
| `GET /market/scenarios`, `GET /market/state` | scenarios; current moves |
| `POST /market/events` | `{"scenario": "tech-selloff"}` or `{"ticks": [...]}` — re-ranks and pushes to `/ws` |
| `GET /callers` | who the move hit hardest, with their likely reason to call |
| `GET /call/{ref}` | the incoming-call briefing |
| `POST /call/incoming` | `{"from": "+41..."}` (JSON or Twilio form) or `{"client": ref}` — pushes the briefing to `/ws` |
| `POST /ask` | `{"client", "question"}` → the facts that answer it, with sources |
| `WS /ws` | events: `hello`, `market`, `incoming_call`, `answer` (pushed answers from the Twilio media stream) |

Also: `POST /transcribe` (audio → text → answers, ElevenLabs Scribe), `GET /profile/{ref}`,
`GET /call/{ref}/audio` and `GET /briefing/{ref}/audio` (spoken, ElevenLabs Flash).

**UNTESTED, written from documented protocols but never run against a real call — review before
a demo relies on them.** `POST /twilio/incoming` and `WS /call/{ref}/twilio-media`
(`backend/twilio_media.py`) are the real telephony path: set a Twilio number's "a call comes in"
webhook to `/twilio/incoming` (`ADVISOR_NUMBER` env var forwards the call); it returns TwiML that
also starts a media stream, resampled and relayed to ElevenLabs realtime STT the same way
`WS /call/{ref}/listen` (`backend/listener.py`) does for the phone app's own microphone (the
"Enable live listening" button mid-call). Until verified, `POST /call/incoming` plus a second
device on the phone app remains the reliable fallback docs/PLAN.md already treats as acceptable.

`GET /dashboard/` — the one-click 60-second briefing (`web/dashboard/`): pick a client, see the
briefing with every sentence's source, word count and reading-time estimate, section-coverage
("5/6 have data"), what the claim checker rejected, and a Listen button. Also uploads the jury's
test client (`POST /clients`).

More modules:

- `backend/outlook.py` — real news (10 feeds) and verbatim bank house views, matched to the client's largest exposures. `python -m backend.outlook refresh`.
- `backend/translate.py` — Supertext with a cache; `data/translations/rules-en.json` has every suitability rule in English.
- `backend/profiles.py` — Apertus reads each client's notes once into a validated profile (`data/profiles/profiles.json`).
- `backend/voice.py` — ElevenLabs speech (Flash) and transcription (Scribe; realtime URL for the call listener). `--dialect gsw-u-sd-chzh`/`gsw-u-sd-chbe` on `brief`/`say` speaks Swiss German (Supertext translation + a German voice, `language_code: "de"`) — untested by ear, see docs/PLAN.md "Swiss German option".
- `backend/excustody.py` — the ten side-challenge custody PDFs as clients EXT-01..EXT-10 (bonus case), reconciled to the statements.
- `python -m backend.report` — every client's briefings in English, with sources, in `docs/verification/briefings-en.md`.

Caller numbers map to clients in `data/phonebook.json` (gitignored; copy `data/phonebook.example.json`).
`BRIEFING_LLM=0` turns Apertus off.

Call mode — the briefing when a client calls during a market move:

```
python -m backend.callmode CASE-043 --scenario tech-selloff   # the golf-video client
python -m backend.callmode --rank --scenario tech-selloff     # who the move hit hardest
python -m backend.yahoo                                        # snapshot real moves to data/scenarios/live-<date>.json
```

- `backend/market.py` — Bloomberg-shaped ticks → market state; `impact()` applies moves to every holding (funds through look-through, hedged share classes get no currency move, unmapped holdings reported as not modelled).
- `backend/callmode.py` — caller, likely reason for the call, ranked impact, what held up, playbook talking points, one open issue.
- `data/scenarios/` — `tech-selloff` and `chf-spike` are **simulated**; `live-*` are real Yahoo snapshots.
- `data/playbook.json` — the talking points and when each applies. Edit freely; tests keep numbers and banned phrases out.

- `backend/data.py` — loads `clients.json` + `reference.json`; extra client files via `--clients-file`.
- `backend/facts.py` — the fact engine: every sentence the briefing may say, computed in code, with its source.
- `backend/phrasing.py` — picks the top facts per slot, has the LLM rephrase them, and rejects any sentence with an added number, cause, severity word or altered rule name / note.
- `backend/llm.py` — Apertus on Swisscom first, OpenAI (`OPENAI_API_KEY`) as fallback.

Guidebook source: <https://startglobal1920.notion.site/Hacker-Guidebook-START-Hack-Tour-St-Gallen-3b84da13be328082a75fc33a4a0eb9c5> (fetched 2026-09-18). Notion is authoritative; this copy is a snapshot.

## What the case ships

Data only — no brief, no judging criteria, no partner contacts. Those came at the kickoff; see [docs/PLAN.md](docs/PLAN.md).

| | |
| --- | --- |
| `core-case/portfolio-data/clients.json` | 47 clients, 57 portfolios, 703 security positions, 206 proposals, 1274 transactions, 180 suitability violations, 153 client notes |
| `core-case/portfolio-data/reference.json` | 504 securities, 48101 fund look-through rows, 54 suitability rules, risk/ESG profiles, 16 strategic asset allocations |
| `core-case/GUI-screenshots/` | The current advisor, client, and portfolio dashboards |
| `side-challenge/` | Ten 8-page German quarterly client reports (Q4 2025), from a separate fictional bank — not joinable to `clients.json` |

Three further client-data files arrive later for the live presentation, so the solution has to accept new files of the same shape rather than hardcoding the one we have.
