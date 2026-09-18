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

Every team will read "ping" as a dashboard notification. We make it literal: **the ping
is a phone call.** The advisor's phone rings, they pick up and hear the briefing,
interrupt with questions, and get grounded answers — while a card on screen highlights
each fact and its source as it is spoken.

The call is real and live, but it runs in the browser, not over the phone network: a
phone web page that looks like an incoming call, talking to an ElevenLabs agent over
WebRTC. No phone number, no telecom costs, no calling anyone who hasn't agreed to it.

## The stage moment

1. The jury hands us the test client. We drop the file in; a 60-second countdown
   starts on screen.
2. The advisor's phone (a teammate playing the advisor) rings: incoming-call screen,
   ringtone, vibration. They press green. The voice briefs them on the client.
3. They interrupt ("which fund?"); the agent answers from the data and stops.
4. On screen, each fact lights up with its source as it is spoken.
5. The countdown stops well under 60.

The role-play is theatre; the voice and the facts are live. A pre-recorded call is only
the fallback video — it can't be about the test client, and the jury would notice.

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

## Architecture

```
client file ──> fact engine (deterministic) ──> briefing facts + sources
                                                   │
                        ┌──────────────────────────┼──────────────────────┐
                        v                          v                      v
                 briefing card (UI)     incoming-call page (phone)    news / CIO view
                 karaoke highlighting   ElevenLabs agent over          hooks
                                        WebRTC; facts injected as
                                        dynamic vars; follow-ups
                                        via client tools
```

- **Fact engine first.** Performance, allocation drift vs. strategic asset allocation,
  fund look-through exposure, suitability violations, recent transactions, notes. All
  computed in code, each fact carrying its source row. Must run on any file of the
  `clients.json` shape — the test client is unseen.
- **The LLM only phrases facts.** It never produces a number that isn't in the fact set.
- **The ring is pushed from our server.** Dropping in a client file triggers the fact
  engine, then a push (WebSocket) to the call page, which starts ringing.
- **The call gets its facts up front** as dynamic variables, so the core briefing needs
  no lookups after pick-up. Follow-up questions go through client tools in the page,
  which call our API — no public tunnel needed.
- **The card and the call share one fact set** — nothing is built twice. The card
  follows the agent's transcript events to highlight each fact as it is spoken.

## Build order

1. Fact engine + source tracking over `clients.json` / `reference.json`.
2. Briefing card with per-claim sources and one-click trigger.
3. Incoming-call page: ringing screen, pushed ring, ElevenLabs agent over WebRTC
   reading the facts.
4. Karaoke sync between call and card.
5. Follow-up questions via client tools (covers the chatbot bonus).
6. Stretch, pick at most two: rehearsal mode (agent plays the client and pushes back),
   suitability objection ("that fund breaches her ESG exclusion"), German/French
   switching, post-meeting voice note → CRM note and follow-up email, ex-custody PDF
   import.
7. Optional upgrade, only with time and a juror who agrees at the booth: a real phone
   call to their phone via a Twilio number imported into ElevenLabs.

## Submission

Due 15:00 in the Hack App, by the team leader: title, description, GitHub link,
demo video, ZIP, thumbnail. The video is the one that takes real time — it is
budgeted above, not left to the last ten minutes.

## Robustness

25% of the score, and the test client is unseen.

- Hold five clients out of `clients.json` as our own unseen test file. Never load
  them during development.
- Every field is absent-not-null; whole reference collections can be missing. The
  engine returns a shorter briefing, never an error.
- Malformed or unreadable file → the card says so plainly and the call does not ring.
- Before designing the Outlook slot, spend ten minutes checking whether the news
  feeds actually return anything for these ISINs. 226 of 504 securities are
  investment funds. If coverage is thin, Outlook carries a house-view line or is
  dropped.

## Setup and risks

- [ ] ElevenLabs key works (Growing Business tier, 5.4M chars/month). Conversational AI
      is available; browser calls need no phone number.
- [ ] **Audio routing is the biggest risk.** Speakerphone into a handheld mic sounds bad
      and the agent can hear itself through the venue speakers and cut itself off.
      Plan: the advisor wears earbuds on the phone; the laptop joins the same session
      and plays the agent through venue audio while the card is on the projector.
      Test it in the room during the partner slot.
- [ ] The call page needs mic permission over HTTPS on the phone — test on the venue
      WiFi, with a hotspot as backup.
- [ ] Record a fallback video of the full flow.
- [ ] No cloned voices of real people.
- [ ] The account has an unrelated agent ("CallKeep – Thames Valley Plumbing") — leave it
      alone; create a separate demo agent.
