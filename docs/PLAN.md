# Plan — "Your phone is ringing"

## The case, from the kickoff slides

Slides were transcribed below, then deleted (still in git history):

**Main challenge: From Ping to Pitch in 60 Seconds — AI Briefing Assistant.** One click
gives the advisor a briefing readable in ~60 seconds: development, health check,
outlook, next best actions.

| Weight | Criterion | What they wrote |
| --- | --- | --- |
| 25% | Problem fit & business value | Solves the advisor's 60-second prep need? Could it be piloted with a few relationship managers right after the hackathon? |
| 25% | Implementation quality & robustness | End-to-end working demo, stable data flows, sensible error handling and latency; clean, modular APIs with hooks for news, CIO view etc. |
| 20% | AI quality: relevance & grounding | Concise, client-specific briefing with practical next best actions — fact-based, no generic or hallucinated content. |
| 15% | User experience | Readable in ~60 seconds, clear structure and highlights, one-click trigger that fits the existing advisor workflow. |
| 15% | Bonus | Ex-custody import, follow-up chatbot, originality in how the briefing experience is designed. |

"A working prototype beats a slide-ware concept." **On stage:** live end-to-end demo,
a short deck, and a test client handed to us shortly before.

**Provided:** sample portfolios, securities data, URO Advisor Pro UI screenshots, the
Git repo. **We source:** free news feeds (Yahoo Finance, cash.ch) and public CIO /
house-view reports from major banks.

**Bonus cases:** ex-custody import (external custody PDF → virtual portfolio included in
the briefing), chatbot (follow-up questions mid-call), creativity ("voice, visual card,
chat bubble — anything the advisor can absorb in seconds"). Main challenge first for
the first 12 hours; bonus cases after, via Saturday's partner slot.

**Contacts (UNRISKOMEGA):** Marc Aeberhard (CEO), Michael Nutter, CFA (Chief Product
Officer), Frédéric Altorfer (Head Solution Integration & Support).

## The idea

Two products on one backend:

- **The dashboard satisfies the criteria.** One click, a 60-second briefing on the
  laptop, exactly what the slides ask for. Plain and solid.
- **The phone is what wins.** A relationship manager is on the golf course with one
  client when another client calls in a panic. Before they even pick up, the briefing
  is on their phone. During the call, an agent listens and puts the answer to each
  question on the screen within about two seconds. The advisor is never caught off
  guard, and never needs to be in front of a laptop.

What we claim, in two lines:

1. **Instant, and never caught off guard.** The briefing arrives while the phone is
   still ringing; the answers arrive while the client is still asking.
2. **Portable.** It works wherever the advisor is, not only at a desk.

**Discretion is part of the story.** The advisor never puts the client on speaker in
front of another client — that would breach banking secrecy (Art. 47 BankG). They
excuse themselves, step away, and take the call on earbuds, reading the phone.

**How the phone hears the call.** A phone app cannot hear a normal phone call (iOS
never allows it; Android blocks it for third-party apps). So the advisor's business
number runs through our telephony (Twilio): clients call that number, Twilio forwards
the call to the advisor's mobile, tells us the caller ID before anyone answers, and
streams us a copy of the audio. That is also how it would run at a bank, where advisor
lines are already routed and recorded.

The voice only ever talks to the advisor, never to the client.

## The pitch and demo

About 5 minutes. **The demo is pre-recorded first**, so the pitch cannot fail on venue
WiFi or phone reception. Live testing comes after, with the jury's test client.

| Time | What | How |
| --- | --- | --- |
| 0:00–0:15 | Cold open: the "your phone linging" meme ringtone, on a golf course | Video |
| 0:15–1:45 | The golf scene (below) | Video |
| 1:45–2:45 | How it works: one architecture slide, measured latencies, "the same backend powers the dashboard" | Slide |
| 2:45–3:45 | Live: we load the jury's test client, one click, the 60-second briefing on the dashboard | Live, laptop |
| 3:45–4:30 | Why it's real: every fact sourced and checked, Swiss-hosted model, the call note doubles as the advice record | Slide |
| 4:30–5:00 | Close: pilot with a few relationship managers on Monday | Slide |

If there is time or the jury asks, a live phone call: a teammate dials the Twilio
number as the test client, and the advisor's phone screen is mirrored on the
projector.

### The golf scene (the video)

1. The advisor is putting, chatting with a client.
2. Their phone rings with the meme ringtone. The lock screen already shows: *"Anna
   Keller calling — probably the tech drop (−4.8%, 18% of her book). Patient, wants it
   short."*
3. "Excuse me a moment." They step away and put in earbuds, glancing at the card:
   exposure ranked by impact, what held up, two talking points.
4. They answer. Anna: "How much have I lost on tech?" About two seconds later the
   answer card shows: *"CHF 41k today, tech funds X and Y."* The advisor reads it and
   answers calmly.
5. She asks something else; the next card appears. They agree on a follow-up.
6. They hang up. The phone shows the call note and a draft follow-up email; one tap
   approves both.
7. They walk back and sink the putt.

The scene is acted; the system in it is real and running. The market move is
simulated and we say so.

## The briefing itself

Six slots, ~160 words, in this order. Fixed structure is what makes it readable in
60 seconds and gradeable against "concise, client-specific, fact-based".

| Slot | Content | Source |
| --- | --- | --- |
| Who | Name, risk profile, AUM, portfolios, reporting currency | `clients.json` |
| Development | Performance over 12m and since inception | `PerformanceHistory` (58 monthly NAV points) |
| Health check | Worst 1–2 SAA drifts, count and worst suitability violation | SAA `Mappings` + `SuitabilityViolations` |
| Watch | Concentration, look-through exposure, or a note that conflicts with a holding | `FundUnbundlingMappings`, `ClientNotes` |
| Outlook | One news or house-view line — **omitted entirely if we have nothing real** | news feed / CIO PDF |
| Next best actions | Two, each tied to a fact above | derived, see below |

Every slot carries the row it came from. An empty slot is dropped, never padded —
padding is exactly what "no generic content" is scoring against.

**Next best actions.** The Beratungen objects from their UI are not in the data, so
actions are derived, not read:

- allocation outside its Min/Max band → rebalance that class toward target
- open suitability violation → address rule *n*
- client note contradicted by a holding → raise it with the client
- cash above 10% → deploy idle liquidity
- no finalised proposal in 12 months → book a review

Ranked by size of the breach, top two spoken, the rest on the card.

### In call mode

When the trigger is an incoming client call during a market move, the order changes:
the ranked market digest comes first, then talking points, then the rest.

| Order | Content | Source |
| --- | --- | --- |
| 1 | Who is calling, profile in one line ("patient, wants it short") | client profile |
| 2 | Ranked digest: each moved topic with the client's exposure and CHF impact, largest first, at most three | exposure store × market state |
| 3 | What is holding up: diversification and hedge facts (only if they exist) | fact engine |
| 4 | Two talking points, picked from the playbook to fit this client | playbook × profile |
| 5 | One open issue if any (violation, drift) | fact engine |

**Ranking.** Impact of a topic = client's look-through weight in it × today's move,
expressed in CHF. Topics the client has tagged as an interest get a boost; topics under
0.5% of the book or with no meaningful move are dropped. So a client heavy in tech and
light in gold hears tech first and gold later, or not at all.

## Why clients call

The data records why each consultation happened (`Proposals[].Reason`, 206 proposals):

| Count | Reason |
| --- | --- |
| 26 | Follow-up from prior meeting |
| 19 | Withdrawal request |
| 18 | Change of risk tolerance |
| 17 | New deposit received |
| 15 | Change of investment strategy |
| 15 | Risk profile update |
| 15 | Client relocation |
| 14 | Annual review meeting |
| 13 | Periodic portfolio review |
| 11 | Estate planning discussion |
| 11 | Client called |
| 11 | Market volatility follow-up |
| 9 | Portfolio rebalancing |
| 9 | Tax year-end rebalancing |
| 3 | Life event (retirement) |

Market volatility is 11 of 206. A panic-call-only tool covers ~5% of real calls. The
client notes point the same way: an expected inheritance, retirement within two years,
a property purchase within 12 months, CHF 15,000 needed for the Q1 tax payment, a wish
for more sustainable funds.

### Scenarios

| Scenario | What the advisor needs in 60 s | Data behind it | Priority |
| --- | --- | --- | --- |
| Market shock | Exposure ranked by impact, what held up, calming points | Look-through, market feed | Headline |
| Withdrawal request | Cash on hand, which positions to sell so the portfolio still fits the risk profile, whether a note anticipated it | `Liquidity…`, positions, suitability rules, notes | Build |
| Rejected-proposal follow-up | What was proposed, when it was rejected, the note on it | 76 rejected (`Abgelehnt`) proposals with notes | Build |
| New deposit | Where it goes to close the gap to target allocation, recommendation-list funds, ESG preference | SAA gaps, `InRecommendationList`, ESG profile | Stretch |
| Change of risk tolerance | What changes from profile *n* to *m*: new target mix, holdings that would then breach rules | `RiskProfiles`, `StrategicAssetAllocations` | Stretch |
| Maturity / idle cash (advisor calls out) | What matures when, where it could go | 15 bond positions maturing within 180 days; 13 clients above 10% cash | Stretch |
| Life event | Liquidity needs from the notes, what is actually liquid, age of the risk profile | Notes, `ProfilingDateUtc`, `Birthday` | Stretch |
| Sustainability question | ESG score of holdings, ESG violations, the client's stated wish | `SustainabilityScore`, ESG profiles (28 clients) | Stretch |
| Relocation, tax, estate | Cross-border rules, tax lots | **Not in the data** | Flag for a specialist, never guess |

### Likely reason for the call

The advisor doesn't know why the client is calling. The briefing opens with the
likely reason, ranked from signals we already compute, each naming its signal:

| Signal | Likely reason |
| --- | --- |
| A market move hits a large share of the book | Market volatility |
| A note mentions a coming liquidity need (property, tax, retirement) | Withdrawal |
| A proposal was rejected recently | Follow-up |
| A bond matures soon, or cash is above 10% | Reinvestment |
| A new deposit shows in the data | Investing new money |
| Risk profile older than 3 years | Not a reason to call, but raise it on the call |

*"She's probably calling about the tech drop — or possibly the house purchase you
noted in March."* If the advisor says "she wants to withdraw", the agent switches to
that scenario's briefing.

## Architecture

```
 SOURCES: Bloomberg-shaped feed (synthetic) + public (Yahoo, SIX, SNB, ECB, FRED,
          news RSS, CIO house views)
                 │
                 v
          MARKET STATE ──┐   scheduler (06:00 + every 15 min), alert rules
                         v
 client files ──> FACT ENGINE ──> EXPOSURE STORE ──> PRECOMPUTE JOB ──> BRIEFING CACHE
 (any clients.json)  (fund           (weights, risk      impact ranking,     per client:
                     look-through)   contribution,       reason predictor,   likely reason,
                                     hedges, drift,      profile, playbook,  ranked digest,
                                     violations)         phrasing + claim    talking points
                                                         checker
                                                              │
            ┌─────────────────────────────────────────────────┼───────────────────────┐
            v                                                 v                       │
   DASHBOARD (laptop)                    client dials advisor's number (Twilio)       │
   one-click 60-second                     │ caller ID, before anyone answers         │
   briefing — the rubric                   ├──> client lookup ──> push briefing ──> ADVISOR PHONE
                                           │                      while ringing        (card, answers,
                                           │ call forwarded to advisor's mobile         call note)
                                           └──> live audio copy ──> speech-to-text          ^
                                                                    │                      │
                                                     question detection ──> our API ───────┘
                                                                            (same facts)
                                         after the call: call note + follow-up email draft
```

**Latency budget.** Everything slow happens before the call: exposures at upload,
ranking and phrasing whenever the market moves. When the phone rings, the backend
only looks up the cached briefing (milliseconds) and pushes it. During the call:
speech-to-text, question detection and a fact lookup — target about two seconds from
the end of the client's question to the answer card.

**Components**

- **Fact engine.** Runs on any file of the `clients.json` shape. 290 of 504 securities
  have no industry of their own (funds, bonds), so fund look-through via
  `FundUnbundlingMappings` is required, not optional. Outputs per client: exposure by
  industry, region, asset class and currency; `ContributionVolatility` per position
  (what drives the risk); hedged share classes (from the security name, e.g. "Gold
  (CHF) hedged"); SAA drift; open violations. Every fact carries its source row.
- **Market state.** One normalised shape regardless of source:
  `{dimension, bucket, move_1d, move_5d, level, as_of, source}` plus headlines tagged
  with dimension and bucket. Securities map to moves through their industry, region
  and asset class; single-stock prices are a later refinement. We don't have bond
  duration, so we don't claim bond price moves.
- **Precompute job.** Runs on the schedule, on any alert, and on every client upload.
  Recomputes impact for every client, ranks, phrases, stores the result. Idempotent,
  so re-running it is always safe.
- **Reason predictor.** Part of the precompute job: ranks the likely reasons for a
  call from the signals in [Why clients call](#why-clients-call) and stores them with
  the briefing. Each scenario is its own fact set plus playbook entries.
- **Profile builder.** Turns the 153 client notes (English), tags (73, industries and
  regions the client cares about), risk profile (3–7) and ESG profile (28 clients) into
  a fixed profile: tone, length preference, interests, and which playbook angles suit
  them. Uses the LLM once at build time; each field shows the note it came from; the
  advisor can override.
- **Advisor playbook** (`advisor-playbook.md`). Global, written by us. Approved
  calming angles with the condition for using each (long-term plan; diversification
  when a diversification fact exists; no selling into a panic; offer a follow-up
  meeting), phrasing guidance by risk profile, and banned phrases: guarantees,
  forecasts, "don't worry", "you're safe".
- **Claim checker.** The gate between the LLM and anything spoken or shown.
- **Call router** (Twilio). Incoming-call webhook: caller ID → client → push the
  cached briefing to the advisor's phone, then forward the call. A media stream sends
  a copy of the call audio to the listener.
- **Listener.** Streaming speech-to-text on the client's side of the call, question
  detection, a lookup against the API, an answer card pushed to the phone. Answers
  use the same facts and the same claim checker as everything else.
- **Advisor phone app.** A web app on the phone: the ringing briefing, answer cards
  during the call, the call note and follow-up email after. Earbud whisper and a
  spoken summary before picking up are optional extras (ElevenLabs).
- **Dashboard.** The one-click 60-second briefing on the laptop, from the same cache.
- **API.** Clean endpoints with the hooks the judges asked for:
  `POST /clients` (upload), `GET /briefing/{client}`, `POST /market/events`
  (feed or alert in), `GET /market/state`, `POST /call/incoming`, `POST /ask`.

## Market data and sources

We assume a Bloomberg-type feed, and simulate it: a replayable file of ticks in a
Bloomberg-like shape (`ticker`, `field` such as `PX_LAST` / `CHG_PCT_1D`, `value`,
`ts`), covering sector indices, regions, FX (USD/CHF, EUR/CHF), commodities (gold,
silver, palladium, copper), volatility (VIX, VSMI) and headlines tagged by sector.
Scenario files (e.g. `tech-selloff.json`, `chf-spike.json`) replay on a button press.
**On stage we say it's simulated.** The adapter interface is the one a real Bloomberg
connection would plug into — that is the production story.

Public sources behind the same interface, in order of usefulness:

| Source | What we take | Notes |
| --- | --- | --- |
| Yahoo Finance | Daily moves of sector and region ETFs / indices, FX, commodities | Unofficial API; cache results, don't depend on it live |
| SIX Swiss Exchange | SMI and Swiss sector index levels | Swiss angle for the jury |
| SNB data portal | Policy rate, CHF FX | Official |
| ECB reference rates | EUR FX | Official, daily |
| FRED | US rates, VIX history | Official |
| News RSS (finews.ch, cash.ch, NZZ Wirtschaft) | Headlines, tagged to sectors by us | For the Outlook slot |
| Bank CIO house views (UBS House View, Julius Bär, Pictet, Vontobel) | One-line outlook per sector | Public PDFs; the slides ask for a CIO-view hook |

Anything we can't source for real is left out of the briefing rather than invented —
the Outlook slot is already defined that way.

## What the agent may claim

The calming talking points are the most useful part and the easiest place to lose
the grounding score or say something a bank's compliance team would forbid.

- **Diversification in numbers — allowed when computed:** "Tech is 18% of her book;
  bonds and gold, 40%, didn't move."
- **Currency hedges — allowed when a hedged share class is held:** "Her gold is the
  CHF-hedged class, so the dollar move doesn't reach it."
- **Risk share — allowed:** "Tech drives 45% of her portfolio's volatility."
- **"Offset" / "hedged" in general — only with a fact behind it.** Only 1 of 681
  positions in the data actually reduces portfolio risk, so a broad "you're hedged"
  is almost never true. Without a fact, the agent states the exposure plainly.
- **Never:** guarantees, forecasts, "don't worry", advice to the client directly.

## Services (tested 2026-09-18)

From the [Tech Goodies](https://startglobal1920.notion.site/Tech-Goodies-3bf4da13be32804f84d2c8938a4c1407)
page, keys claimed via the [Keymaker](https://keymaker.ai-weeks.ch/). Keys live in
`.env` (`ELEVENLABS_KEY`, `SWISSCOM_KEY`, `SUPERTEXT_API_KEY`), which is gitignored.

| Service | Use | Measured |
| --- | --- | --- |
| **Apertus 1.5 70B** (Swisscom) | Main LLM: phrases the facts | ~0.15 s to first streamed byte, ~1.6 s for a 3-sentence briefing |
| **OpenAI** ($50 credit) | Fallback LLM | Not claimed yet — redeem the credit link into an org |
| **ElevenLabs** | Call agent, TTS | Flash v2.5: 0.17 s to first audio. Multilingual v2: 3.1 s — too slow for the call |
| **Supertext** | Translation, incl. Swiss German dialects | ~1.7 s per sentence |

**Apertus is the main LLM because the data stays in Switzerland.** Banks can't send
client data to US-hosted models; "the briefing is written by a Swiss model on Swisscom"
is our answer to "how does this reach production". Put the LLM behind one interface
with OpenAI as fallback.

**Apertus needs guardrails.** On a test briefing it addressed the client ("your
portfolio") instead of the advisor, and invented a cause ("may have amplified losses").
Strict prompt, plus a check that every number in its output is in the fact set —
otherwise fall back to a template.

**Supertext request quirks** (differ from their docs):

- `text` must be a list: `"text": ["..."]`.
- Targets need a region: `de-CH`, `fr-CH`, not `de`, `fr`. Dialects:
  `gsw-u-sd-chzh` (Zurich), `gsw-u-sd-chbe` (Bern). Full list: `GET /v1/features`.
- Auth header: `Authorization: Supertext-Auth-Key <key>`.
- It translated "equity share" as *Eigenkapitalanteil* (company equity) instead of
  *Aktienanteil*. Use its glossary for finance terms.

**Swiss German option.** Supertext → Zurich German → ElevenLabs Flash with
`language_code: "de"` produces audio (no Swiss German voice exists; it is a German voice
reading dialect text). If a native speaker says it sounds right, a briefing in
Züritüütsch is a strong stage moment for a Swiss jury. If not, stay with standard
German and French.

## Build order

1. Fact engine: look-through exposures, risk contribution, hedged classes, SAA drift,
   violations, each with its source. Tested on a client we haven't looked at.
2. Synthetic market feed and two scenario files; market-state shape; one real public
   adapter (Yahoo Finance, cached).
3. Precompute job, impact ranking, briefing cache, API endpoints.
4. Profile builder, `advisor-playbook.md`, phrasing with Apertus, claim checker.
5. Reason predictor, plus the withdrawal and rejected-proposal scenarios.
6. Dashboard: one-click 60-second briefing with per-claim sources. This is what the
   rubric scores — done before the phone gets polish.
7. Advisor phone app: briefing pushed while ringing, answer cards, call note and
   follow-up email.
8. Twilio: number, incoming-call webhook, forwarding, media stream; listener with
   streaming speech-to-text and question detection.
9. **Record the golf video** once 6–8 work end to end. Hard deadline: by ~12:00
   Saturday, so there is time to edit before the 15:00 submission. It is also the
   required submission video.
10. Stretch, pick at most two: more scenarios (new deposit, risk-tolerance change,
    maturity), earbud whisper, spoken summary before pickup, suitability objection,
    German/French or Swiss German, ex-custody PDF import, more public sources.

If Twilio fights us, the fallback for the video is the call on a second device next
to the advisor's phone, listening through our web app — same backend, same cards.
Say so if asked; the production path is the telephony route.

## Setup and risks

- [ ] ElevenLabs key works (Growing Business tier, 5.4M chars/month).
- [ ] Swisscom guide says "Authorization Bearer expires in 60 minutes" — re-test the key
      an hour after first use; if it expires, the server has to refresh it.
- [ ] Claim the OpenAI credit for the fallback LLM.
- [ ] **Twilio tonight:** paid account (trial can only call verified numbers), a UK or
      US number (Swiss numbers need an address bundle), incoming-call webhook and
      media stream reaching our server through a tunnel (cloudflared or ngrok).
- [ ] Verify streaming speech-to-text latency (ElevenLabs realtime or an alternative)
      on phone-quality audio, Swiss accents included.
- [ ] **Consent.** Transcribing a call without consent is a criminal offence in
      Switzerland (StGB Art. 179bis/179ter). The line plays "calls are recorded",
      as bank lines do. Pitch it as a plus: the transcript is the advice record
      FIDLEG asks for.
- [ ] **Banking secrecy.** Never on speaker near other people — earbuds, step away. The
      video must show this.
- [ ] Phone web app over HTTPS (tunnel or hosting) for push and mic permissions.
- [ ] Get the "your phone linging" meme ringtone for the video. Fine for the pitch;
      check the rights before the video goes anywhere public (e.g. the ElevenLabs
      showcase).
- [ ] Film only teammates; a quiet spot with a putting green or park.
- [ ] Say on stage that the market move is simulated and the scene is acted.
- [ ] Sector-level moves approximate each security's move — say so if asked.
- [ ] Have a native speaker judge the Swiss German TTS sample (only if we do that stretch).
- [ ] No cloned voices of real people.
- [ ] The ElevenLabs account has an unrelated agent ("CallKeep – Thames Valley
      Plumbing") — leave it alone.
