# Demo runbook (16:15)

## 30 minutes before

1. `git pull`, then start the server on the demo laptop:
   `DEMO_SCENARIO=tech-selloff uvicorn backend.api:app --port 8000`
2. `python -m backend.preflight` must end in **READY**. Warnings are fine (email, ringtone).
3. Open the phone app **on the laptop**: `http://localhost:8000/phone/` in Chrome, narrow window
   (or DevTools device mode, iPhone size), and mirror it on the projector. Localhost is what lets
   the browser use the microphone; a real phone over `http://` on the Wi-Fi is **not** allowed to.
4. Click anywhere on the page once (browsers block sound until the first click).
5. Allow the microphone when asked. Dashboard, if shown: `http://localhost:8000/dashboard/`.

## Demo 1: the recorded call

**Button: Start the call with voice** (Buzz Lightyear; `?voiced=walter` for Walter).

- It rings: read the ringing screen out loud (why they are calling, the loss, what held up).
- **Answer.** The client asks; the card arrives about a second after the question.
- Answer him out loud; when you stop talking he asks the next one. If he does not continue:
  double-tap the call timer (or press Space).
- After his sign-off the call ends by itself: call note and follow-up email, **Approve**.
- To start over at any moment: **End call**, then Start the call with voice again.
- No network? **Start the call** replays Walter's saved call offline (silent: read his lines aloud).

Say once: *"The market move is simulated; everything else is the real system on your data."*

## Demo 2: live questions from the judges

1. **Who is calling?** box: type `waldo` → **Find** → prepared briefing → **Ring as this client**.
2. **Answer.** The microphone listens; the judge speaks as the client, close to the laptop.
3. If the room is loud: the ⌨ button on the call screen, type the judge's question.
4. **End call** → note and email → **Approve**.

Waldo (CASE-043) answers well. What to expect:

| The judge asks | The card says |
| --- | --- |
| What's my entire portfolio? | Worth CHF 891k, +18.5% in 12 months · 77% shares, 22% bonds · health care 18% · cash CHF 5k |
| How much did I lose today? | About −CHF 12k today, −1.4% |
| Why? / What happened? | The headline, then tech −4.8% on 9.6% of the portfolio, mostly the NASDAQ fund |
| Is my world fund hit by the dollar? | Hedged to the franc: the dollar move does not reach it |
| How much do I have in bonds? · Do I have any gold? | Bonds 22.4% (CHF 200k) · No gold in the portfolio |
| What's my biggest risk? · Am I within my risk profile? | Risk figures · volatility 10.8%, within the 15.0% maximum |
| Did the changes you made last week make it worse? | The 15 Sep change bought 19 holdings; together about −CHF 11k of today's −CHF 12k |
| Why am I only down 1.4% when the S&P fell 3.2%? | Chain: S&P −3.2% → portfolio −1.4% → 77% shares, 22% bonds, hedged world fund |
| Should I sell everything? | The 12-month record, what held up, the last change |
| Can you send me the tax statement? · Sell the Novartis. | No card: a quiet *To do* / *Instruction, confirm in writing* line, into the call note |
| How are you? | Nothing |

For Walter (CASE-045): *Novartis alone is 41% of the portfolio*, *no bonds*, *volatility within the maximum*.

## If something goes wrong

| Problem | Do this |
| --- | --- |
| "Market: no market move loaded" | `curl -X POST localhost:8000/market/events -H "content-type: application/json" -d "{\"scenario\":\"tech-selloff\"}"` |
| No microphone | Check the page is on `localhost`; otherwise type with ⌨ |
| A card is wrong or empty | Say "let me check that and come back to you"; it is logged in `data/sessions/` |
| The voiced call stalls | End call, start again (always allowed) |
| Network gone | **Start the call** (offline replay) |
| Server gone | Restart it; the phone reconnects by itself |

## Known limits (say them if asked, do not hide them)

- The market move is simulated; sector moves stand in for single-stock prices.
- One microphone hears both of you: keep your own side to statements.
- Email goes to `data/outbox/` until the Gmail settings are in `.env`.
- No ringtone file: the ring is silent unless `web/phone/ringtone.mp3` is added.
- After the demo: `python -m backend.utterance review` shows what the last live call heard and did.
