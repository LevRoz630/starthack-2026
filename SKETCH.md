# Sketch — UNRISKOMEGA case

> **Superseded by [PLAN.md](PLAN.md).** This was written before the case
> presentation, when the brief was still unknown. The actual case is "From Ping to
> Pitch in 60 Seconds — AI Briefing Assistant", not the constraint checker guessed
> at below. Kept for the data notes, which still hold.

## The clock

Hacking opens 20:00 Friday. Submission closes 15:00 Saturday. That is 19 hours,
and the pitch has to be rehearsed inside it — realistically feature-freeze at
13:00, leaving ~17 hours of build.

## What we know

Data only, no brief. 47 clients, 57 portfolios, 703 security positions, 206
proposals, 1274 transactions, 180 precomputed suitability violations, 153 free-text
client notes. Reference data: 504 securities, 48101 fund look-through rows, 54
rule definitions, risk/ESG profiles, 16 strategic asset allocations.

Their existing product already computes drift, risk contribution, scenarios, ESG
and concentration. We are not going to beat their risk engine in 17 hours. The
opening is the layer above it: deciding what matters and saying it in words.

## What we don't know

Answered at 18:15, or at the partner booth (Sat 9:00–12:00) / mentor slot (10:00–12:00):

1. What are we actually meant to build — advisor tool, client-facing thing, or analysis?
2. Are the 54 suitability rules meant to be executable? They ship as German prose
   with no thresholds. We get 180 precomputed violations but no way to evaluate a
   hypothetical trade.
3. Do the advisor-triage objects exist anywhere? Their dashboard shows 215 pending
   advisories, 21 warnings and last-consultation dates. None of that is in the data.
4. Is the side challenge separately judged? It looks separately prized.

## Shape of the data

```
Client ──┬── Portfolios ──┬── SecurityPositions ──> Securities (SecurityId)
         │                ├── AccountPositions   (cash; Currency may be a crypto ticker)
         │                └── PerformanceHistory (58 monthly NAV points)
         ├── Proposals ────── SecurityPositions  (proposed target state)
         ├── Transactions ──> Securities         (no trade date; time via ProposalId)
         ├── SuitabilityViolations               (precomputed, with ViolationPath)
         ├── ClientNotes                         (free text, English)
         └── Tags

Portfolio.StrategicAssetAllocationId ──> StrategicAssetAllocations[].Mappings
                                         (Dimension, Category, Min/Target/Max)
Securities[].SAA_*Name ──────────────────> Mappings[].Category
```

Four SAA dimensions: AssetClass, Industry, CountryGroup, CurrencyGroup. Targets sum
to 1.0 on each.

Three things that are easy to get wrong here:

- **Only AssetClass mappings carry Min/Max.** Industry, country and currency carry a
  target alone, so "breach" on those dimensions needs a tolerance we have to infer
  or ask for.
- **The sector and region rules are worded "equity sector" / "equity region".** So
  their denominator is probably the equity sleeve, not the whole portfolio. Worth
  confirming — it changes every number on those two dimensions.
- **Look-through rows use the fine taxonomy, SAA targets use the coarse one.**
  Securities carry both, so securities are the translation table between them.
  Look-through gives bucket weights only — no underlying issuer names.

## The seam worth attacking

Client notes carry constraints the rule engine does not encode:

> "No direct positions in fossil fuels, please."
> "Prefers ESG-compliant investments, no defense or tobacco holdings."

ESG exists in the schema only as a Yes/No profile with a minimum score. Meanwhile
504 securities carry sustainability scores, `Energy` is a first-class SAA industry
category, and look-through reaches inside 141 funds. So a stated client wish can be
checked against actual exposure — including exposure held indirectly through funds —
and no existing rule does that today.

That gives a demo with a shape: *the client asked for this in writing, the system
agreed, and here is the exposure that contradicts it — including the part hidden
inside a fund.*

## Build order

One data layer, then a thin head on top. The data layer is brief-independent —
every candidate below needs it — so it is the only safe thing to start before 18:45.

**Layer 1 — read and join.** Load both files, index securities, resolve portfolios
to their SAA, translate fine categories to coarse. Defensive on absent keys
throughout: a missing field is absent, not null, and whole reference collections
can vanish.

**Layer 2 — measure.** Exposure per dimension with and without look-through; drift
against Min/Target/Max; surface the precomputed violations with their ViolationPath
so we can explain *why*, not just *that*.

**Layer 3 — pick one head** once the brief lands:

| Head | If the brief is about | Extra needs |
| --- | --- | --- |
| Advisor triage | productivity, "which client today" | the pending-advisory objects we don't have |
| Constraint checker | suitability, compliance, client intent | notes → checkable constraints |
| Report generator | the side challenge | PDF layout, German prose |

The constraint checker is the one that needs nothing we haven't got, and it is the
one that produces the demo above. Default to it unless the brief points elsewhere.

## Tonight

- 18:15 case presentation — take the four questions above in written form.
- 18:45 matchmaking.
- 20:00 hacking opens. Layer 1 and 2 first; head chosen before anyone writes UI.
