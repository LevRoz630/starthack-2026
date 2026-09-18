# What the UI screenshots tell us

Read out of `data/core-case/GUI-screenshots/`. These are the product as it exists
today, which is the best evidence we have of what the case is really about.

## Client_Advisor_DB.png — the advisor's day

Header counters for one advisor: **215 pending advisories, 114 rule violations, 21
warnings**, CHF 52,618,933 under advice. The client list is triaged through saved
filter tabs, which is effectively their own statement of what matters:

- Liquidity > 10% (112)
- Maturities (0)
- Last consultation > 12 months (191)
- Rule violations, urgent (28)
- Birthdays (13)

Columns: client number, name, address, birthday, last profiling, last changed,
last consultation. Red and amber dots mark violation and warning states per row.

**Read:** the advisor is drowning and triaging by hand-built saved searches. 191
clients unseen for a year is the number that should embarrass them.

## Client_DB.png — one client, several banks

Client view (Tanja Bauer, CHF 1,497,989) with tabs: all portfolios, own portfolios,
**other banks (Fremdbanken)**, **consolidation**, **relationships**. Three portfolio
cards, one of which is held at ZKB — so the product consolidates holdings it does
not itself manage.

Below that, a **Beratungen** (advisory sessions) table, 16 pages for this one
client: advisory service, container, type (investment proposal / portfolio meeting
/ phone advice), dated session, number, status (proposed / draft), changed by, last
changed.

**Read:** this is the pending-advisory entity that the data pack does not ship.
Also note "relationships" — which is what the client note about managing a family
member's portfolio under power of attorney refers to.

## Portfolio_DB.png — the analytics they already have

SAA table with Min / Soll / Max / Portfolio / **Aktion**, where Aktion is the move
back to target in percentage points (Aktien 59.1% against a 25% target reads
-34.1%). Beside it, fifteen analytics tiles:

suitability · risk/return · scenarios (-30.5% global financial crisis) · product
risk (PRC) · countries · sectors · currencies · maturities · restrictions ·
performance · sustainability (ESG rating) · goal attainment · issuer risk ·
positions list

The positions list has a **Fondssplitting** toggle — fund look-through on and off.

**Read:** they compute everything already. We will not beat their risk engine in 17
hours. The gap is above it: deciding which of the 114 violations matters today and
saying it in a sentence a client understands.

## Consequences for what we build

1. The triage objects (Beratungen, warnings, last-consultation dates) exist in the
   product but **not in our data**. Any triage demo has to synthesise them or work
   from the violations we do have.
2. External-bank holdings and consolidation exist in the product, not in our data.
3. Fund look-through is a first-class, user-toggleable concept for them — so a
   look-through-aware answer will read as native rather than clever.
