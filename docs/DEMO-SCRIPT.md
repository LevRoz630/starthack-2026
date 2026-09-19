# The two demo calls

Generated from the recorded runs in `data/demo/runs/`, so this is what actually happens on
the phone rather than what was intended. The client's lines are in `data/demo/*.json`; the
cards below are what the fact engine returned through the real speech-to-text.

Every number an advisor says out loud must be on the card above it. If a card does not
come, say the thing without the number.

---

## Call 1 — the silent one, for filming: Walter White (CASE-045)

**Who.** A former chemistry teacher. His file says he runs a small family car-wash business on the side and occasionally asks about reinvesting its proceeds, prefers to settle smaller amounts in cash where possible, and values discretion -- minimal written correspondence about portfolio specifics. Recent health concerns have prompted a review of estate and succession planning. He is 63% health care through Novartis and BB Biotech, and Novartis alone is 41% of his book.

**Market.** tech-selloff.  **Length.** 76 seconds.

### 1

**WALTER:** Morning. It's Walter. Quick one before my first lesson. How much did today cost me?

> About −CHF 2k today, −0.7% of the book.
>
> <sub>impact of the market feed on clients.json CASE-045 holdings</sub>

> About −CHF 896 from Financials, −0.9% today on 29.3% of the book, mostly Cembra Money Bank AG.
>
> <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-045 holdings</sub>

### 2

**WALTER:** I still follow the chemistry side. How much of my portfolio is in pharma?

> Health Care is 63.0% of the book (CHF 214k) after fund look-through, mostly via Novartis AG and BB Biotech AG.
>
> <sub>clients.json CASE-045: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>

### 3

**WALTER:** Hmm. Am I too concentrated in one thing?

> Novartis AG alone is 41.0% of the book.
>
> <sub>clients.json CASE-045: Portfolios[CASE-045-01].SecurityPositions</sub>

> 0 suitability errors and 1 warning open; most serious: "Share is not part of the investment universe for individual shares and therefore not monitored.".
>
> <sub>clients.json CASE-045: SuitabilityViolations</sub>

### 4

**WALTER:** Right. And how much cash do I have with you?

> Cash on hand is CHF 1k, 0.4% of the book.
>
> <sub>clients.json CASE-045: LiquidityInDefaultCurrency</sub>

### Sign-off

**WALTER:** Good. Keep it off paper where you can. I'll call you.

*No card. It is not a question, and the system knows that.*

---

## Call 2 — the voiced one: Buzz Lightyear (CASE-027)

**Who.** Very enthusiastic about space travel; his file records that he follows private spaceflight companies with great interest and has asked for more detail on how that exposure could be expanded further. He prefers forward-looking, high-conviction positions over defensive ones and is not concerned by short-term volatility in thematic growth positions. He is 97.9% industrials, and SpaceX alone is 68.5% of his book.

**Market.** tech-selloff.  **Length.** 73 seconds.

### 1

**BUZZ:** Hello, I saw the launch got pushed again. How much did I lose today?

> About −CHF 4k today, −2.3% of the book.
>
> <sub>impact of the market feed on clients.json CASE-027 holdings</sub>

> About −CHF 2k from Industrials, −1.1% today on 97.9% of the book, mostly SpaceX and Union Pacific Corp.
>
> <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-027 holdings</sub>

> About −CHF 2k from the dollar, −1.2% against the franc on 97.9% of the book.
>
> <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-027 holdings</sub>

### 2

**BUZZ:** Why did it drop?

> Behind the move: "Dollar weakens as rate-cut bets rise"
>
> <sub>market feed "tech-selloff" headline</sub>

> The dollar −1.2% against the franc, on 97.9% of the book: about −CHF 2.0k.
>
> <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-027 holdings</sub>

> The book is about −CHF 3.9k today (−2.3%) on CHF 172k.
>
> <sub>market feed "tech-selloff" × clients.json CASE-027 holdings</sub>

### 3

**BUZZ:** And how much space exposure do I actually have?

> About −CHF 2k from Industrials, −1.1% today on 97.9% of the book, mostly SpaceX and Union Pacific Corp.
>
> <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-027 holdings</sub>

### 4

**BUZZ:** Am I too concentrated?

> SpaceX alone is 68.5% of the book.
>
> <sub>clients.json CASE-027: Portfolios[CASE-027-01].SecurityPositions</sub>

### Sign-off

**BUZZ:** Understood. I'd still rather be early than safe. Talk soon.

*No card. It is not a question, and the system knows that.*

---

## For whoever plays the client

- Say the lines as written. The speech-to-text is listening for these words.
- **End every line on the question.** A line that finishes with a statement is committed
  as a statement and gets no card: Walter's pharma line first ended "that's the part I
  actually follow" and produced nothing.
- Leave the gap. The advisor is answering the client in it.
- The last line is a sign-off, not a question. Do not turn it into one.

## For the advisor

- Look at the card, then look up. Do not read it off the screen word for word.
- Never say a number that is not on the card in front of you.
