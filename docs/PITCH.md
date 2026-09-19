# Pitch — "Your phone is ringing"

Five minutes on stage, Saturday from 15:15. This file is the deck's content and the
spoken script. `docs/PLAN.md` has the reasoning behind the product; this has what we
say, in order, and the numbers we are allowed to say.

**One sentence:** the advisor's phone rings, and before they pick up it already says
why the client is calling, what today did to their book, and what to say — every line
computed from the client's own data, with its source.

---

## Run of show (5:00)

| Time | Slide | Who | What happens |
| --- | --- | --- | --- |
| 0:00–0:20 | 1. Cold open | — | The golf video starts on the ringtone. No talking. |
| 0:20–1:45 | (video) | — | The golf scene plays to the end. Still no talking. |
| 1:45–2:15 | 2. The problem | A | "That call arrives 200 times a year and there is no time to prepare." |
| 2:15–2:55 | 3. How it works | A | One architecture slide, the three latencies. |
| 2:55–3:50 | 4. Live | B | Dashboard, the jury's test client, one click, 60-second briefing. |
| 3:50–4:25 | 5. Why it is real | A | Sourcing, the claim checker, Swiss-hosted model, the advice record. |
| 4:25–5:00 | 6. Pilot Monday | A | What a pilot looks like; ask. |

Two speakers. **A** narrates, **B** drives the laptop and never speaks while A speaks.
The video plays with sound; everything else is silent on screen.

---

## Slide 1 — cold open (video, 0:00–1:45)

No slide, no introduction. The video opens on the ringtone. The scene:

1. The advisor is putting, chatting with a client.
2. The phone rings. The lock screen already reads: *"Waldo calling — probably the tech
   drop: Information Technology −4.8% today, 9.6% of the book, about −CHF 12k."*
3. "Excuse me a moment." They step away, earbuds in — **never on speaker next to
   another client** (Art. 47 BankG). The card shows what fell, what held up, two
   talking points.
4. They answer. The client asks how much they lost on tech. About a second later the
   answer card appears; the advisor reads it and answers calmly.
5. A second question, a second card. They agree on a follow-up.
6. They hang up: the call note and the follow-up email are drafted. One tap approves.
7. They walk back and sink the putt.

**On the last frame, before A speaks:** the words *simulated market data · acted
scene · the system is real and running* stay on screen.

---

## Slide 2 — the problem (0:20 of talking)

> Every relationship manager knows this call. The market moves, the client rings, and
> you have somewhere between zero and ten seconds to remember what they hold, what it
> did today, and what you promised them in March. In the data we were given, "client
> called" and "market volatility follow-up" are 22 of 206 consultations — and a
> withdrawal request, a rejected proposal or a new deposit is most of the rest. So we
> did not build a panic-call tool. We built the 60 seconds before any call.

Slide content:

- 206 consultations in the case data, by reason: follow-up 26 · withdrawal 19 · risk
  tolerance 18 · new deposit 17 · strategy change 15 · **market volatility 11**
- The point: a market-shock-only assistant covers 5% of real calls.

---

## Slide 3 — how it works (0:40)

One diagram, three arrows, three numbers. Do not read the boxes out loud.

```
 client dials the advisor's number ──> caller ID before it rings
                                          │
 clients.json (any file of that shape)    │
        │                                 v
   FACT ENGINE ──> EXPOSURE STORE ──> BRIEFING CACHE ──> the phone, while ringing
   look-through,    weights, hedges,    ranked by                    ^
   drift, rules     drift, violations   CHF impact                   │
        │                                                            │
        └──> the same facts answer questions ──> live transcript ────┘
                                                 (speech to text)

   the same cache serves the laptop dashboard — one click, 60 seconds
```

**The three numbers, all measured on this build:**

| | |
| --- | --- |
| Briefing on the screen while the phone is still ringing | **2 ms** median to build, cached before the call |
| Question heard → answer card on the phone | **~0.85 s** |
| Answer chosen from the fact set | **~30 ms** |

> Everything slow happens before the call. Exposures at upload, ranking and phrasing
> whenever the market moves. When the phone rings we are doing a lookup.

**The telephony line** (say only if asked, or in one breath): a phone app cannot
listen to a normal call — iOS forbids it. So the advisor's business number runs
through our telephony: the client calls that number, we get the caller ID before
anyone answers, the call is forwarded to their mobile, and we receive a copy of the
audio. That is how bank advisor lines are already routed and recorded.

---

## Slide 4 — live on the laptop (0:55)

**B drives. A narrates. Do this exactly:**

1. Dashboard is already open, market scenario already loaded. **Do not reload.**
2. Upload the jury's test client file — "Upload test client…".
3. The client appears and is selected automatically. One click was the whole
   interaction.
4. Read one line out loud from each of two sections, then point at the grey line
   underneath it: *that is the row in their file it came from.*
5. Point at the left panel: **Call first** — who this morning's move hit hardest,
   ranked, each with the reason they are likely to call. Click the top one.

> This is the one-click, 60-second briefing the case asks for. Six sections: who they
> are, how the portfolio developed, the health check, what to watch, the outlook, and
> the next best actions. 128 words on the median client — call it 40 seconds of
> reading. Every sentence carries the row it was computed from.

**If the upload fails:** click any client and carry on; say "we will do the test
client in the Q&A." Do not debug on stage.

---

## Slide 5 — why this is real, not a demo (0:35)

Four claims, each with its number:

| Claim | Evidence to say out loud |
| --- | --- |
| Nothing is invented | **465 briefing sentences across 57 clients, none without a source.** The model rephrases facts; a claim checker rejects any sentence that adds a number, a cause or a severity word. |
| It says nothing rather than guess | 4 of 57 briefings are missing a section — because we had nothing real for it. Ask the phone about gold a client does not own and it answers "nothing in the data answers this." |
| It can run in a Swiss bank | The model is **Apertus, hosted by Swisscom in Switzerland** — client data never leaves. OpenAI is only a fallback. |
| It produces the record the regulator wants | The call note and the follow-up email are drafted from the facts that were actually shown during the call. The advisor approves; the email carries nothing advisor-only in it. |

> The honest limits, said before anyone asks: the market move is simulated and
> labelled simulated everywhere, including in the sources. Sector-level moves stand in
> for each security's own move. We do not have bond duration, so we never claim a bond
> price move.

---

## Slide 6 — pilot on Monday (0:35)

> Everything you have seen runs on the file you gave us, unchanged. Point it at a
> second file and it works — we added the ten German custody PDFs from the side
> challenge as ten more clients, read out of the PDFs, reconciled to the statements,
> and they get the same briefing from the same engine.
>
> A pilot is three relationship managers, their real book, and one number routed
> through us for two weeks. What we would measure: how often the briefing is open when
> the call starts, and how often the advisor has to look anything up during the call.
>
> We are Look Mom I am Quant. Thank you.

---

## What is on the screen behind us (asset checklist)

- [ ] Slide 1: black, the video embedded, sound checked at the venue.
- [ ] Slide 2: the reason table, six rows.
- [ ] Slide 3: the diagram above, redrawn cleanly, and the three-number table.
- [ ] Slide 4: nothing — the laptop's live screen.
- [ ] Slide 5: the four-row claims table.
- [ ] Slide 6: one line — "Pilot: 3 RMs, one routed number, two weeks" — and the team name.

---

## Q&A — the answers we already have

**"Is the market data real?"** The two scenario files are simulated and say so on
every card and in every source line. `python -m backend.yahoo` snapshots real Yahoo
moves into the same shape, and the adapter is the one a Bloomberg feed plugs into.

**"What if the client asks something you have no fact for?"** The card says "nothing
in the data answers this". That is deliberate: an advisor who reads a wrong number off
a screen is worse off than one who reads nothing.

**"Does the LLM write the briefing?"** It rephrases sentences we computed. It may not
introduce a number, a cause, a forecast or a new claim, and the claim checker rejects
the sentence if it does — the dashboard shows what was rejected. Turn the model off
entirely with `BRIEFING_LLM=0` and the briefing still works, in fact text.

**"Is recording the call legal?"** Transcribing without consent is a criminal offence
in Switzerland (StGB 179bis/179ter). The line announces that calls are recorded, as
bank lines already do. The transcript is the advice record FIDLEG asks for.

**"Banking secrecy on a golf course?"** Earbuds, and step away — that is in the video
on purpose. The assistant only ever talks to the advisor, never to the client.

**"How do you handle a new client file?"** `POST /clients` with any clients.json-shaped
file. Exposures are recomputed on upload; a malformed client fails on its own without
taking the upload down. That is the button we press live.

**"What about the ten PDFs?"** `backend/excustody.py` reads them into the same client
shape (EXT-01…EXT-10), matches ISINs to the securities reference, and reconciles to
each statement's totals. They appear in the client list marked *ex-custody*.

**"What does it cost to run?"** One Apertus call per briefing (~1.6 s, phrased in the
background), one speech-to-text stream per call. Everything else is local computation.

**"Why not just use the existing dashboard?"** The existing dashboard is where the
data already is. This is the 60 seconds before the advisor can reach it.

---

## Numbers we may say (all measured on this build, `python -m pytest -q tests`: 113 pass)

| Number | What it is |
| --- | --- |
| 57 clients | 47 from the case file + 10 read out of the side-challenge PDFs |
| 465 sentences, 0 unsourced | every briefing sentence across all 57 clients |
| 86–177 words, median 128 | briefing length → **26–54 seconds** to read |
| 53 of 57 get all six sections | the other 4 are missing one, because we had nothing real for it |
| 2 ms median | to build a briefing from the fact engine |
| ~0.85 s | end of the client's question → answer card on the phone |
| ~1.6 s | Apertus phrasing a briefing (in the background, never on the critical path) |
| 0.17 s | ElevenLabs Flash to first audio for the spoken briefing |
| 48 101 look-through rows | how a fund's positions become industry exposure |
| 54 suitability rules, 180 violations | the health check, with the rule text in English |
| 311 headlines, 16 verbatim house-view lines | the outlook slot: Pictet, Vontobel, BlackRock, Standard Chartered |

**Never say:** a forecast, a guarantee, "don't worry", "you're safe", or any number
that is not in the table above or on the screen.

---

## Before we go on stage

- [ ] Laptop on the venue projector, resolution checked, browser zoom at 125%.
- [ ] `DEMO_SCENARIO=tech-selloff uvicorn backend.api:app --port 8000` running, and the
      dashboard open on a client **other** than the test client.
- [ ] Phone on the same tunnel URL, on the idle screen, screen timeout off,
      notifications off, do-not-disturb on.
- [ ] Video file local on the presenting laptop — never streamed.
- [ ] `data/demo/runs/golf-latest.json` present, so **Replay offline** works with no network.
- [ ] Test-client file copied to the desktop the moment the jury hands it over.
- [ ] One rehearsal with a timer. If we are over 5:00, cut slide 2 to one sentence.
