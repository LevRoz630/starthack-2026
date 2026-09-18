# Plan — "Your phone is ringing"

## The case, from the kickoff slides

Slides are in [case-slides/](case-slides/). Transcribed:

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
is a phone call.** The advisor picks up and hears the briefing, interrupts with
questions, and gets grounded answers — while a card on screen highlights each fact
and its source as it is spoken.

## The stage moment

1. The jury hands us the test client. We drop the file in; a 60-second countdown
   starts on screen.
2. A juror's phone rings (agreed beforehand at the booth — fallback: our presenter's
   phone on speaker). The voice briefs them on the client.
3. They interrupt ("which fund?"); the agent answers from the data and stops.
4. On screen, each fact lights up with its source as it is spoken.
5. The countdown stops well under 60.

## Architecture

```
client file ──> fact engine (deterministic) ──> briefing facts + sources
                                                   │
                        ┌──────────────────────────┼──────────────────────┐
                        v                          v                      v
                 briefing card (UI)     ElevenLabs agent (outbound    news / CIO view
                 karaoke highlighting   call via Twilio; facts         hooks
                                        injected as dynamic vars;
                                        follow-ups via server tools)
```

- **Fact engine first.** Performance, allocation drift vs. strategic asset allocation,
  fund look-through exposure, suitability violations, recent transactions, notes. All
  computed in code, each fact carrying its source row. Must run on any file of the
  `clients.json` shape — the test client is unseen.
- **The LLM only phrases facts.** It never produces a number that isn't in the fact set.
- **The call gets its facts up front** as dynamic variables, so the core briefing needs
  no lookups after pick-up. Follow-up questions hit our API as server tools (public via
  a tunnel).
- **The card and the call share one fact set** — nothing is built twice.

## Build order

1. Fact engine + source tracking over `clients.json` / `reference.json`.
2. Briefing card with per-claim sources and one-click trigger.
3. Outbound call: Twilio number imported into ElevenLabs, agent reading the facts.
4. Karaoke sync between call and card.
5. Follow-up questions via server tools (covers the chatbot bonus).
6. Stretch, pick at most two: rehearsal mode (agent plays the client and pushes back),
   suitability objection ("that fund breaches her ESG exclusion"), German/French
   switching, post-meeting voice note → CRM note and follow-up email, ex-custody PDF
   import.

## Setup and risks

- [ ] ElevenLabs key works (Growing Business tier, 5.4M chars/month). Conversational AI
      is available; **no phone number attached yet** — buy a Twilio number (paid, not
      trial, so it can call unverified numbers) and import it. Do this early.
- [ ] Ask at the booth whether a juror will take the call. Never call anyone without
      their agreement.
- [ ] Test calling on venue reception; record a fallback video of the full flow.
- [ ] No cloned voices of real people.
- [ ] The account has an unrelated agent ("CallKeep – Thames Valley Plumbing") — leave it
      alone; create a separate demo agent.
