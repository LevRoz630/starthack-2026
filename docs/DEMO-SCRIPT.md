# The two demo calls

Generated from the recorded runs in `data/demo/runs/`, so this is what actually happens on
the phone rather than what was intended. The client's lines are in `data/demo/*.json`.

Every number an advisor says out loud must be on the card above it. If a card does not
come, say the thing without the number.

---

## Call 1 — the silent one, for filming: Walter White (CASE-045)

**Who.** A former chemistry teacher. His file says he runs a small family car-wash business on the side and occasionally asks about reinvesting its proceeds, prefers to settle smaller amounts in cash where possible, and values discretion -- minimal written correspondence about portfolio specifics. Recent health concerns have prompted a review of estate and succession planning. He is 63% health care through Novartis and BB Biotech, and Novartis alone is 41% of his book.

**Market.** tech-selloff.  **Length.** 101 seconds, 7 answered questions.

### 1

**WALTER:** Morning. It's Walter. Quick one before my first lesson. How much did today cost me?

> About −CHF 2k today, −0.7% of the book.
> About −CHF 896 from Financials, −0.9% today on 29.3% of the book, mostly Cembra Money Bank AG.

### 2

**WALTER:** I still follow the chemistry side. How much of my portfolio is in pharma?

> Health Care is 63.0% of the book (CHF 214k) after fund look-through, mostly via Novartis AG and BB Biotech AG.

### 3

**WALTER:** Hmm. Am I too concentrated in one thing?

> Novartis AG alone is 41.0% of the book.
> 0 suitability errors and 1 warning open; most serious: "Share is not part of the investment universe for individual shares and therefore not monitored.".

### 4

**WALTER:** And how has it done over the year?

> Portfolio value +20.9% over the 12 months to Jul 2026 and +47.9% since Oct 2021, now CHF 340k; value change including deposits and withdrawals.

### 5

**WALTER:** How risky is the portfolio overall?

> Risk engine for Investment advisory (CASE-045-01), 3 Sep 2026: expected return 5.5%, value at risk 14.7%.

### 6

**WALTER:** Right. And how much cash do I have with you?

> Cash on hand is CHF 1k, 0.4% of the book.

### 7

**WALTER:** When did we last actually change anything?

> The last finalised proposal (30 Aug 2026, reason: Follow-up from prior meeting) ordered to buy SMI (R), SPDR Bloomberg Global Aggregate Bond UCITS ETF and 17 more.
> 19 of 20 orders from the proposal of 30 Aug 2026 were forwarded with a warning.

### Sign-off

**WALTER:** Good. Keep it off paper where you can. I'll call you.

*No card. It is not a question, and the system knows that.*

---

## Call 2 — the voiced one: Buzz Lightyear (CASE-027)

**Who.** Very enthusiastic about space travel; his file records that he follows private spaceflight companies with great interest and has asked for more detail on how that exposure could be expanded further. He prefers forward-looking, high-conviction positions over defensive ones. He is 97.9% industrials, SpaceX alone is 68.5% of his book, and his volatility is running above the ceiling for his profile.

**Market.** tech-selloff.  **Length.** 94 seconds, 7 answered questions.

### 1

**BUZZ:** Hello, I saw the launch got pushed again. How much did I lose today?

> About −CHF 4k today, −2.3% of the book.
> About −CHF 2k from Industrials, −1.1% today on 97.9% of the book, mostly SpaceX and Union Pacific Corp.
> About −CHF 2k from the dollar, −1.2% against the franc on 97.9% of the book.

### 2

**BUZZ:** Why did it drop?

> Behind the move: "Dollar weakens as rate-cut bets rise"
> The dollar −1.2% against the franc, on 97.9% of the book: about −CHF 2.0k.
> The book is about −CHF 3.9k today (−2.3%) on CHF 172k.

### 3

**BUZZ:** And how much space exposure do I actually have?

> About −CHF 2k from Industrials, −1.1% today on 97.9% of the book, mostly SpaceX and Union Pacific Corp.

### 4

**BUZZ:** Am I too concentrated?

> SpaceX alone is 68.5% of the book.

### 5

**BUZZ:** How has it done over the year, though?

> Portfolio value +22.8% over the 12 months to Jul 2026 and +78.2% since Oct 2021, now CHF 170k; value change including deposits and withdrawals.

### 6

**BUZZ:** What's my sustainability score like?

> ESG client: average sustainability score 7.3 of 10 against a minimum of 5.7; 68.5% of the book has no score.

### 7

**BUZZ:** And am I over my risk limit?

> Volatility is 12.2%, above the 12.0% maximum of Investor profile 5.

### Sign-off

**BUZZ:** Understood. I'd still rather be early than safe. Talk soon.

*No card. It is not a question, and the system knows that.*

---

## For whoever plays the client

- Say the lines as written. The speech-to-text is listening for these words.
- **End every line on the question.** A line that finishes with a statement is committed as
  a statement and gets no card.
- Leave the gap. The advisor is answering the client in it.
- The last line is a sign-off, not a question. Do not turn it into one.

## For the advisor

- Look at the card, then look up. Do not read it off the screen word for word.
- Never say a number that is not on the card in front of you.
