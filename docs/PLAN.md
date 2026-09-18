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

Every team will read "ping" as a dashboard notification. We make it literal: **the
client calling is the ping.** A client phones in — say after a tech sell-off — and
before the advisor picks up, the advisor's own phone rings with a briefing: what moved,
how much of this client's book it touches, in order of impact, what this particular
client wants to hear, and what the advisor can truthfully say to steady them. The
advisor can interrupt with questions and gets grounded answers, while a card on screen
highlights each fact and its source as it is spoken.

The voice only ever talks to the advisor, never to the client. The advisor stays in
charge of what gets said.

The call is real and live, but it runs in the browser, not over the phone network: a
phone web page that looks like an incoming call, talking to an ElevenLabs agent over
WebRTC. No phone number, no telecom costs, no calling anyone who hasn't agreed to it.

The same engine serves the calm case too: a scheduled meeting triggers the six-slot
briefing below without a market event.

## The stage moment

1. The jury hands us the test client. We load the file; exposures are computed on
   the spot.
2. We fire a market alert from the (synthetic) feed: "Tech −4.8%, USD/CHF −1.2%".
   The precompute job re-ranks every client's briefing; the dashboard shows it
   finishing.
3. "Incoming call: [test client]". A 60-second countdown starts. The advisor's phone
   (a teammate playing the advisor) rings; they press green.
4. The voice, for example: *"Anna Keller is calling. Tech is down 4.8% today; it's 18%
   of her book, about CHF 41k. Her bonds and gold, 40% together, didn't move, and the
   gold is the CHF-hedged class, so the dollar drop doesn't reach it. Her notes say
   she's patient and wants it short — lead with the long-term plan. One open issue:
   equities are 6 points over her risk profile."*
5. The advisor interrupts ("which tech funds?"); the agent answers from the data and
   stops. On screen, each fact lights up with its source as it is spoken.
6. The countdown stops well under 60.

The role-play is theatre; the voice and the facts are live. The market move is
simulated and we say so. A pre-recorded call is only the fallback video — it can't be
about the test client, and the jury would notice.

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

## Architecture

```
 SOURCES
 ┌──────────────────────────────────┐  ┌─────────────────────────────────────────┐
 │ Market feed, Bloomberg-shaped    │  │ Public sources                          │
 │ (synthetic, replayable scenarios)│  │ Yahoo Finance, SIX, SNB, ECB FX, FRED,  │
 │ prices, sector moves, FX, vol,   │  │ news RSS, bank CIO house views          │
 │ headlines                        │  │                                         │
 └────────────────┬─────────────────┘  └───────────────────┬─────────────────────┘
                  └──────────────┬──────────────────────────┘
                                 v
                       market ingest ──> MARKET STATE
                                         moves by industry / region / asset class /
                                         currency / commodity, tagged headlines
                                 │
       scheduler (06:00 + every 15 min) ──┤
       alert rules (sector or FX move over threshold, vol spike) ──┤
                                 v
 client files ──> FACT ENGINE ──> EXPOSURE STORE (per client, built at upload)
 (clients.json     look-through   weights by industry / region / asset class /
  shape, incl.     via fund       currency; risk contribution per position;
  test client)     breakdowns     hedged share classes; SAA drift; violations
                                 │
                                 v
                        PRECOMPUTE JOB ──> BRIEFING CACHE (keyed by client id)
                        impact = exposure × move      ranked digest, facts + sources,
                        rank, drop, attach sources    talking points, open issues
                                 ^
          PROFILE BUILDER ───────┤          advisor-playbook.md ──┘
          notes, tags, risk/ESG
          profile -> tone, topics
                                 │
                                 v
             PHRASING (Apertus; OpenAI fallback) + CLAIM CHECKER
             every number and every "hedged/offset" must match a fact,
             otherwise fall back to a template sentence
                                 │
   incoming client call ──> RING ROUTER ──> advisor phone page (ElevenLabs agent over
   (simulated on stage)       lookup only,  WebRTC; briefing injected as dynamic vars)
                              no compute    + briefing card on screen (karaoke sync)
                                 │
                   follow-ups: client tools ──> our API (exposure store, market state)
                   after the call: call note + follow-up email draft
```

**Latency budget.** Everything slow happens before the call: exposures at upload,
ranking and phrasing whenever the market moves. When the client calls, the ring
router only does a cache lookup (milliseconds), the agent starts with the briefing
already in its variables, and Flash TTS starts speaking in ~0.2 s.

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
- **Ring router and call page.** Lookup only; pushes the ring over WebSocket.
- **API.** Clean endpoints with the hooks the judges asked for:
  `POST /clients` (upload), `GET /briefing/{client}`, `POST /market/events`
  (feed or alert in), `GET /market/state`, `POST /call/incoming`.

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
5. Briefing card with per-claim sources.
6. Call page: ringing screen, ring router, ElevenLabs agent over WebRTC.
7. Karaoke sync, follow-up questions via client tools (covers the chatbot bonus),
   call note and follow-up email after the call.
8. Stretch, pick at most two: rehearsal mode (agent plays the client and pushes back),
   suitability objection ("that fund breaches her ESG exclusion"), German/French
   switching or a Swiss German briefing, ex-custody PDF import, more public sources
   (CIO views, news).
9. Optional upgrade, only with time and a juror who agrees at the booth: a real phone
   call to their phone via a Twilio number imported into ElevenLabs.

## Setup and risks

- [ ] ElevenLabs key works (Growing Business tier, 5.4M chars/month). Conversational AI
      is available; browser calls need no phone number.
- [ ] Swisscom guide says "Authorization Bearer expires in 60 minutes" — re-test the key
      an hour after first use; if it expires, the server has to refresh it.
- [ ] Claim the OpenAI credit for the fallback LLM.
- [ ] Have a native speaker judge the Swiss German TTS sample.
- [ ] **Audio routing is the biggest risk.** Speakerphone into a handheld mic sounds bad
      and the agent can hear itself through the venue speakers and cut itself off.
      Plan: the advisor wears earbuds on the phone; the laptop joins the same session
      and plays the agent through venue audio while the card is on the projector.
      Test it in the room during the partner slot.
- [ ] The call page needs mic permission over HTTPS on the phone — test on the venue
      WiFi, with a hotspot as backup.
- [ ] The call page needs a tunnel (cloudflared or ngrok) or hosting: the phone must
      load it over HTTPS for mic access and receive the ring from the laptop.
- [ ] Say on stage that the market move is simulated.
- [ ] Sector-level moves approximate each security's move — say so if asked.
- [ ] Record a fallback video of the full flow.
- [ ] No cloned voices of real people.
- [ ] The account has an unrelated agent ("CallKeep – Thames Valley Plumbing") — leave it
      alone; create a separate demo agent.
