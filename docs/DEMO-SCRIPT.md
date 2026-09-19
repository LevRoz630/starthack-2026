# The two demo calls

Two clients with different risk appetites, ringing for different reasons. Every question
below was run through `POST /ask` first, and every number in the advisor's replies is on
the card that is on screen at that moment. Nothing here is invented. If a card does not
come, say the thing without the number rather than filling the gap.

---

## Call 1 — Superman (CASE-026)

**Who.** Investor profile 6, CHF 2.38m, CHF 115k cash. His file says he is comfortable
with higher volatility given a long time horizon, wants no defence or tobacco, asked for
a benchmark comparison at the next review, and prefers phone contact twice a year with
no unannounced visits. He does not panic. He rings because the number is big, not
because he is frightened.

**Market.** tech-selloff.

### 1

**SUPERMAN:** How much did I lose today?

*Card: Probably the market move: Information Technology −4.8% today, 8.3% of the book;
about −CHF 30k (−1.3%) overall. — The dollar −1.2% against the franc: 15.7% of the book
is exposed, about −CHF 4k. — Financials −0.9% today: 16.8% of the book, about −CHF 4k,
mostly via Zurich Insurance Group AG and Helvetia Holding AG.*

**ADVISOR:** About thirty thousand. One point three percent. Tech took most of it, down
four point eight on the day. The dollar's another four, and your insurers about the
same.

### 2

**SUPERMAN:** Why did it drop?

*Chain: Behind the move: "Chip stocks slide after export-control headlines" — the book is
about −CHF 30.2k today (−1.3%) on CHF 2.38m — Information Technology −4.8% on 8.3% after
look-through: about −CHF 9.5k — iShares NASDAQ 100 UCITS ETF: CHF 47k of that exposure,
about −CHF 2.3k of it — the dollar −1.2% on 15.7%: about −CHF 4.5k — Financials −0.9% on
16.8%: about −CHF 3.6k — everything else together (12 smaller moves): about −CHF 12.7k.*

**ADVISOR:** Chip stocks sold off. Export-control headlines. Nine and a half of it is
tech, and two and a half of that is the NASDAQ fund on its own. Dollar, four and a half.
Insurers, three and a half. The rest is twelve smaller moves adding up.

### 3

**SUPERMAN:** Am I breaking any of your rules?

*Card: 5 suitability errors and 4 warnings open; most serious: "Volatility range
undershot (portfolio risk too low)".*

**ADVISOR:** Five errors, four warnings. The top one will amuse you. Your portfolio is
too *low* risk for your own profile. You told us you can sit through volatility, and
we've got you below it.

### 4

**SUPERMAN:** What held up?

*Card: Holding up today: Consumer Staples +0.3% (8.6% of the book).*

**ADVISOR:** Staples. Up a fraction. Eight point six percent of the book. Nothing else
much was green.

### 5

**SUPERMAN:** Fine. Send me the numbers and we'll talk at the review.

**ADVISOR:** Will do. We'll speak then.

*No card here — it isn't a question, and the system knows it.*

---

## Call 2 — Holden Caulfield (CASE-021)

**Who.** Investor profile 3, the only conservative client in the book, CHF 759k, and CHF
259k of that, a third, sitting in cash. No open violations. His file says he wants to go
into Swiss small caps, wants a call before anything changes on the standing order, and
is working out a charitable donation from the portfolio.

What he does not know is that one holding, VZ Holding AG, is 65.8% of his book and
drives all of its volatility, and that it sits above the product risk limit for a
profile 3 client. This call is not about a market drop. It is the call the product is
actually for.

**Market.** tech-selloff.

### 1

**HOLDEN:** How much did today cost me?

*Card: Possibly the market move: Financials −0.9% today, 65.8% of the book; about −CHF 4k
(−0.6%) overall.*

**ADVISOR:** About four thousand. Six tenths of a percent. It's the financials, down
under one percent today.

### 2

**HOLDEN:** Why did it barely move?

*Chain: the book is about −CHF 4.5k today (−0.6%) on CHF 759k — the book moved less than
the SMI: −0.6% against −1.3% — the SMI moved −1.3% today.*

**ADVISOR:** The cash, mostly. Swiss market was down one point three. You were down six
tenths. So about half of it.

### 3

**HOLDEN:** How much is just sitting in cash?

*Card: Cash on hand is CHF 259k, 34.2% of the book. — Deploy idle liquidity: 34.2% of
the book (CHF 259k) is cash.*

**ADVISOR:** Two hundred and fifty-nine thousand. A third of what you hold with us. It
kept you out of trouble today. The rest of the time it's doing nothing.

### 4

**HOLDEN:** Is my portfolio too cautious?

*Card: 1 holding above the product risk class limit of Investor profile 3 (maximum 4):
VZ Holding AG, 65.8% of the book. — VZ Holding AG drives 100.0% of the volatility of
Account / Custody (CASE-021-01).*

**ADVISOR:** No. If anything it's the other way round. A third is in cash and nearly all
the rest is one share. VZ Holding, sixty-five point eight percent of the book. All of
the movement you see comes from that. And it sits above the risk limit for your profile.

### 5

**HOLDEN:** What about Swiss small caps?

*Card: Note from 22 Nov 2025: "Wants to invest more heavily in Swiss small caps going
forward."*

**ADVISOR:** You raised that in November. It's on the file. I'd want to deal with the
concentration first. There's enough cash to do both.

### 6

**HOLDEN:** Right. Call me before you change anything.

**ADVISOR:** That's on your file too. Nothing moves without a call.

*No card — not a question.*

---

## For whoever plays the client

- Say the lines as written; the system is listening for these questions.
- Leave the gap. The advisor is talking in it, and rushing makes it look like a chatbot
  instead of a phone call.
- The last line in each call is a sign-off, not a question. Do not turn it into one.

## For the advisor

- Look at the card, then look up. Do not read it off the screen word for word.
- Never say a number that is not on the card in front of you.
- Earbuds, and step away from anyone else — that is the point of the scene.
