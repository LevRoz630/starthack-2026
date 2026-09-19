# Handoff — state of the build (Sat 19 Sep 2026, ~02:30)

Read this, then `docs/PLAN.md` (the idea, the stage plan, the claim rules) and `README.md`
(commands and endpoints). Submission is **Saturday 15:00**; pitches from 15:15.

## The product in one paragraph

An advisor's phone rings when a client calls. Before they pick up, the phone shows why the
client is probably calling and what today's market did to their book, largest hit first.
During the call the client's voice is transcribed live and each question gets an answer
card built only from computed, sourced facts — including chains of facts for "why" and
"where did the money go". After the call, the call note and follow-up email are drafted;
Approve sends them. The same backend serves a 60-second dashboard briefing (the rubric).

## Run it

```
pip install -r requirements.txt
DEMO_SCENARIO=tech-selloff uvicorn backend.api:app --port 8000
# phone app:  http://localhost:8000/phone/?demo=CASE-043
python -m pytest -q tests          # 105 pass, 2 live tests skipped (RUN_NETWORK_TESTS=1)
python -m backend.report           # every client's briefings in English -> docs/verification/briefings-en.md
```

Keys live in `.env` (gitignored): `ELEVENLABS_KEY`, `SWISSCOM_KEY`, `SUPERTEXT_API_KEY`;
for email `SMTP_USER`, `SMTP_PASSWORD` (Gmail app password), `EMAIL_TO` — **not set yet**,
so Approve writes to `data/outbox/`. The server reads `.env` at start: restart after edits.

## What is built (all on `main`, tested)

| Area | Files | Notes |
| --- | --- | --- |
| Fact engine | `backend/facts.py`, `data.py` | Every sentence computed in code with a source. Fund look-through, SAA bands, violations (+ English rule text), ESG, product risk, recommendation list, proposals and their trades, order warnings, risk engine, notes, outlook. German display names translated. |
| Dashboard briefing | `briefing.py`, `phrasing.py`, `llm.py` | Six slots; Apertus rephrases under a claim checker. **`phrasing.py` / `llm.py` belong to the teammate (LevRoz630)** — coordinate before editing. |
| Market | `market.py`, `yahoo.py`, `data/scenarios/` | Bloomberg-shaped ticks. `tech-selloff`, `chf-spike` are **simulated**; `live-*` are real Yahoo snapshots. Hedged share classes get no FX move. |
| Call briefing | `callmode.py`, `data/playbook.json`, `profiles.py` | Caller + profile, likely reason, ranked impact, headline, what held up, talking points, open issue. |
| Answers during the call | `answers.py`, `reasoning.py` | Chains first (breakdown / vs index / proposal / named holding / Apertus path along real edges), then question type, Apertus picking fact numbers, keywords. Never new text. |
| Live listener | `listener.py`, API `/listen` | ElevenLabs realtime STT; ~0.85 s from end of question to answer card. Fed by the phone's microphone or the recorded call; both are the same Session. |
| Demo pipelines | `demo.py`, `data/demo/golf.json`, `data/demo/runs/golf-latest.json` | Recorded golf call through the real STT; offline replay of the saved run. |
| Email | `mailer.py`, `/followup/send` | Gmail SMTP or outbox. |
| Voice | `voice.py` | Spoken briefings (Flash, ~0.3–0.6 s to first audio), transcription. |
| Outlook | `outlook.py`, `translate.py`, `data/outlook/` | 311 real headlines; 16 verbatim house-view lines (Pictet, Vontobel, BlackRock, StanChart). UBS/Julius Bär block scripts. |
| Ex-custody bonus | `excustody.py`, `data/excustody/` | The 10 German PDFs as EXT-01..10, reconciled to the statements. |
| Phone app | `web/phone/` | Functional, URO-coloured first pass. **Styling waits for the user's Nano Banana mockups.** |

## Open items, in priority order

1. ~~Dashboard web page~~ **done**: one-click briefing with per-sentence sources, word count,
   reading time, section coverage, claim-checker rejections, Listen, test-client upload, and
   the **Call first** panel (`GET /callers`, re-ranks live on a `market` event).
2. ~~Real browser click-through~~ **done** (headless Chromium, both apps): idle → ringing →
   Answer → ask → chain card → End call → note + email → Approve, no console errors except
   the missing `ringtone.mp3`. Screenshots were taken at 390x844 and 1440x900.
3. **Phone styling** to the user's Nano Banana mockups (tokens are CSS variables in `app.css`).
4. **Email:** once the user adds the Gmail settings, restart and send one test.
5. **Ringtone:** the user's "your phone linging" meme as `web/phone/ringtone.mp3` (not in repo).
6. **Golf video** (hard deadline ~12:00 Sat): run "Play recorded call" on a real phone over
   a tunnel (`cloudflared tunnel --url http://localhost:8000`), screen-record, composite.
8. Deck: `docs/deck/index.html` is built. The written pitch script was removed; it is in
   git history (`git show 9f1e13a:docs/PITCH.md`) if it is wanted back.

## Rules the code keeps (keep them)

- Every fact has a source; the LLM never introduces a number, cause, forecast or new text.
  Answers are existing facts; chains only link facts joined by an edge the engine computed.
- Simulated market data is labelled simulated everywhere, including sources.
- Never output IBANs (real ones exist in the data). Never commit `.env`, `data/phonebook.json`,
  audio caches or the outbox.
- Run `python -m pytest -q tests` and check **pytest's own exit code** before every push
  (a pipe to `tail` hides failures).

## Changed on Sat 19 Sep, ~00:30 (all tested, 113 pass)

- Every client now gets a **next best action**: a proposal whose orders were mostly
  forwarded with a warning is one (fires for 19 of 57), and a client with nothing open
  gets "Nothing open: no suitability violation, and every asset class is inside its band."
  53 of 57 briefings now fill all six sections, the other 4 are short one on purpose.
- **Cash on hand** is a fact for every client (`watch.liquidity`, weight 0), and
  withdrawal questions are their own question type — "can I withdraw 50'000?" used to be
  answered with the performance history.
- **A question that names a subject is only answered about that subject**, in every
  layer including the chain: "what happened to my gold?" on a client who holds no gold
  now says nothing in the data answers it, instead of the generic explanation.
- The **follow-up email is client-safe**: the reason we guessed, the playbook wording and
  the (simulated) market headline are advisor-only and never reach the client's inbox;
  near-duplicate lines are collapsed; at most six points.
- `[hidden]` now beats a component's own `display` (the dashboard's "Pick a client" card
  stayed on screen behind the briefing), the briefing carries the client's `name`, and
  ex-custody clients are marked in the client list.

## Gotchas

- The data mixes absent keys with explicit nulls; always `items()` / `.get()`.
- CASE-038 has a "Consolidated" portfolio that double counts — `data.portfolios()` skips it.
- CASE-043 (the demo client) is 16 years old by its birthday in the data; never state age.
- On this Windows box, shell heredocs mangle regex escapes (`\b` became a backspace twice);
  edit regexes with the editor tool, not via `python - <<EOF` string replacement.
- Only a *completed* recorded call replaces `golf-latest.json`; an unanswered one is kept
  only as a timestamped run.
