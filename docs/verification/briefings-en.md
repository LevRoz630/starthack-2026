# Briefings for every client (English, for verification)

Generated 2026-09-19 by `python -m backend.report --scenario tech-selloff`. Market: **tech-selloff** — US tech sell-off; the dollar weakens against the franc, gold is bid.

Each sentence is computed from the data and shows where it came from. Check a few against `data/core-case/portfolio-data/clients.json` and `reference.json`; report anything wrong with the client number and the sentence.

German display names are translated: *Anlageprofil n* → *Investor profile n* (the data's own English strategy name), portfolio names such as *Konto / Depot* → *Account / Custody*. Suitability rule names are the data's own English `RuleCode`s. EXT-01 to EXT-10 are the external custody statements read from `data/side-challenge/` (no risk profile, targets or notes, so fewer facts).

**Contents:** [CASE-001](#case-001--yoda) · [CASE-002](#case-002--joker) · [CASE-003](#case-003--ron-burgundy) · [CASE-004](#case-004--rocky-balboa) · [CASE-005](#case-005--norman-bates) · [CASE-006](#case-006--spock) · [CASE-007](#case-007--mary-poppins) · [CASE-008](#case-008--betty-boop) · [CASE-009](#case-009--dorothy-gale) · [CASE-010](#case-010--son-goku) · [CASE-011](#case-011--ellen-ripley) · [CASE-012](#case-012--company-001-ag) · [CASE-013](#case-013--thomas) · [CASE-014](#case-014--katniss-everdeen) · [CASE-015](#case-015--porky-pig) · [CASE-016](#case-016--holly-golightly) · [CASE-017](#case-017--hulk) · [CASE-018](#case-018--company-002-ag) · [CASE-019](#case-019--pikachu) · [CASE-020](#case-020--tom-joad) · [CASE-021](#case-021--holden-caulfield) · [CASE-022](#case-022--company-003-ag) · [CASE-023](#case-023--frodo-beutlin) · [CASE-024](#case-024--vito-corleone) · [CASE-025](#case-025--john-mcclane) · [CASE-026](#case-026--superman) · [CASE-027](#case-027--buzz-lightyear) · [CASE-028](#case-028--charles-foster-kane) · [CASE-029](#case-029--scarlett-o'hara) · [CASE-030](#case-030--darth-vader) · [CASE-031](#case-031--wolverine) · [CASE-032](#case-032--popeye) · [CASE-033](#case-033--eric-cartman) · [CASE-034](#case-034--travis-bickle) · [CASE-035](#case-035--spongebob-squarepants) · [CASE-036](#case-036--peter-pan) · [CASE-037](#case-037--grinch) · [CASE-038](#case-038--charlie-brown) · [CASE-039](#case-039--rooster-cogburn) · [CASE-040](#case-040--sam-malone) · [CASE-041](#case-041--company-004-ag) · [CASE-042](#case-042--zorro) · [CASE-043](#case-043--waldo) · [CASE-044](#case-044--ralph-kramden) · [CASE-045](#case-045--walter-white) · [CASE-046](#case-046--tony-montana) · [CASE-047](#case-047--jon-snow) · [EXT-01](#ext-01--max-muster) · [EXT-02](#ext-02--anna-beispiel) · [EXT-03](#ext-03--weber-brunner-family) · [EXT-04](#ext-04--peter-keller) · [EXT-05](#ext-05--laura-steiner) · [EXT-06](#ext-06--muster-holding-ag) · [EXT-07](#ext-07--daniel-frey) · [EXT-08](#ext-08--nicole-baumann) · [EXT-09](#ext-09--pensionskasse-fiktiva) · [EXT-10](#ext-10--thomas-gerber)

## CASE-001 — Yoda

Investor profile 5 · CHF 726k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Yoda, Investor profile 5, ESG preference, CHF 726k across 1 portfolio.  
   <sub>clients.json CASE-001: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +30.3% over the 12 months to Jul 2026 and +58.5% since Oct 2021, now CHF 720k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-001: PerformanceHistory of CASE-001-01</sub>
3. **Health check.** 5 suitability errors and 0 warnings open; most serious: "Volatility range undershot (portfolio risk too low)".  
   <sub>clients.json CASE-001: SuitabilityViolations</sub>
4. **Health check.** Liquidity at 100.0%, outside its 0.0%–60.0% band, target 3.0%.  
   <sub>clients.json CASE-001: Portfolios[CASE-001-01] positions; reference.json StrategicAssetAllocations[92] AssetClass "Liquidity"</sub>
5. **Watch.** Note from 5 Sep 2026: "Also manages a family member's portfolio under a power of attorney."  
   <sub>clients.json CASE-001: ClientNotes</sub>
6. **Watch.** Note from 20 Jun 2026: "Extremely patient investor; unconcerned by short-term volatility, takes the long view."  
   <sub>clients.json CASE-001: ClientNotes</sub>
7. **Next best actions.** Rebalance Liquidity down toward 3.0%.  
   <sub>clients.json CASE-001: Portfolios[CASE-001-01] positions; reference.json StrategicAssetAllocations[92] AssetClass "Liquidity"</sub>
8. **Next best actions.** Rebalance Shares up toward 45.0%.  
   <sub>clients.json CASE-001: Portfolios[CASE-001-01] positions; reference.json StrategicAssetAllocations[92] AssetClass "Shares"</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Yoda is calling: Investor profile 5, ESG preference, CHF 726k across 1 portfolio.  
   <sub>clients.json CASE-001: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: calm temperament, wants it detailed. From the notes: "Extremely patient investor; unconcerned by short-term volatility, takes the long view."  
   <sub>data/profiles/profiles.json CASE-001 (apertus) from clients.json ClientNotes</sub>
3. **reason.** Probably the proposal of 6 Jul 2026 that was rejected (reason: Client relocation).  
   <sub>clients.json CASE-001: Proposals[20409]</sub>
4. **reason.** Possibly idle cash: 100.0% of the book (CHF 726k) is cash.  
   <sub>clients.json CASE-001: LiquidityInDefaultCurrency</sub>
5. **digest.** About −CHF 444 today, −0.1% of the book.  
   <sub>impact of the market feed on clients.json CASE-001 holdings</sub>
6. **digest.** About −CHF 444 from Bitcoin, −6.5% today on 0.9% of the book.  
   <sub>market feed "tech-selloff": XBTUSD Curncy CHG_PCT_1D × clients.json CASE-001 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (1.00): Shares at 0.0%, outside its 20.0%–85.0% band, target 45.0%.  
  <sub>clients.json CASE-001: Portfolios[CASE-001-01] positions; reference.json StrategicAssetAllocations[92] AssetClass "Shares"</sub>
- **Health check** (0.50): Bonds at 0.0%, outside its 10.0%–70.0% band, target 47.0%.  
  <sub>clients.json CASE-001: Portfolios[CASE-001-01] positions; reference.json StrategicAssetAllocations[92] AssetClass "Bonds"</sub>
- **Health check** (0.15): 2 of 2 orders from the proposal of 7 Sep 2026 were forwarded with a warning.  
  <sub>clients.json CASE-001: Transactions[ProposalId=25156].ForwardState = 2</sub>
- **Health check** (0.00): "Compliance with maximum volatility" means: For retail clients with financial services Comprehensive investment advisory or discretionary mandate must be PF Vola < max client profile Vola.  
  <sub>clients.json CASE-001: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Minimum limit shares" means: Minimum Limit Stocks  
  <sub>clients.json CASE-001: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Maximum limit liquidity" means: Maximum liquidity limits  
  <sub>clients.json CASE-001: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.08): The last finalised proposal (7 Sep 2026, reason: Estate planning discussion) ordered to sell Short-Term Money Market CHF and Short-Term Money Market USD.  
  <sub>clients.json CASE-001: Proposals[25156] × Transactions</sub>
- **Watch** (0.00): Cash on hand is CHF 726k, 100.0% of the book.  
  <sub>clients.json CASE-001: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Cash is 100.0% of the portfolio (CHF 726k).  
  <sub>clients.json CASE-001: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Swiss francs: 99.1% of the portfolio (CHF 720k).  
  <sub>clients.json CASE-001: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): BTC: 0.9% of the portfolio (CHF 7k).  
  <sub>clients.json CASE-001: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Crypto: CHF 7k, 0.9% of the portfolio.  
  <sub>clients.json CASE-001: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (1.00): Resolve "Compliance with maximum volatility".  
  <sub>clients.json CASE-001: SuitabilityViolations[Id=313155]</sub>
- **Next best actions** (1.00): Resolve "Volatility range undershot (portfolio risk too low)".  
  <sub>clients.json CASE-001: SuitabilityViolations[Id=915347]</sub>
- **Next best actions** (1.00): Resolve "Minimum limit shares".  
  <sub>clients.json CASE-001: SuitabilityViolations[Id=915348]</sub>
- **Next best actions** (0.50): Rebalance Bonds up toward 47.0%.  
  <sub>clients.json CASE-001: Portfolios[CASE-001-01] positions; reference.json StrategicAssetAllocations[92] AssetClass "Bonds"</sub>
- **Next best actions** (0.50): Follow up on the proposal of 6 Jul 2026 that was rejected (reason: Client relocation); it would have had the client buy Global Bond Fund, Global Investment Grade Credit Fund and 5 more and sell CMCI Ex-Agriculture SF UCITS ETF, Silver and 6 more.  
  <sub>clients.json CASE-001: Proposals[20409] × Transactions</sub>
- **Next best actions** (0.30): Keep the 100.0% cash (CHF 726k) in view of the note from 17 Sep 2024: "Prefers to keep a cash reserve on hand for unexpected medical expenses."  
  <sub>clients.json CASE-001: LiquidityInDefaultCurrency, ClientNotes</sub>
- **Next best actions** (0.25): Clear the warnings on the 2 flagged orders from the proposal of 7 Sep 2026.  
  <sub>clients.json CASE-001: Transactions[ProposalId=25156].ForwardState = 2</sub>
- **Next best actions** (0.20): Candidates from the recommendation list for Shares: ABB Ltd and Kuehne + Nagel International AG (Shares is under its band).  
  <sub>reference.json RecommendationLists "Recommendation list free assets", not held, CHF first, ordered by SustainabilityScore</sub>

</details>

---

## CASE-002 — Joker

Investor profile 5 · CHF 185k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Joker, Investor profile 5, CHF 185k across 1 portfolio.  
   <sub>clients.json CASE-002: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +17.7% over the 12 months to Jul 2026 and +19.9% since Oct 2021, now CHF 183k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-002: PerformanceHistory of CASE-002-01</sub>
3. **Health check.** 1 suitability error and 2 warnings open; most serious: "Volatility range undershot (portfolio risk too low)".  
   <sub>clients.json CASE-002: SuitabilityViolations</sub>
4. **Health check.** Risk profile last assessed 31 Jul 2022, 4 years ago.  
   <sub>clients.json CASE-002: ProfilingDateUtc</sub>
5. **Watch.** MSCI World Socially Responsible UCITS ETF drives 22.2% of the volatility of Investment advisory (CASE-002-01).  
   <sub>clients.json CASE-002: Portfolios[CASE-002-01].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Note from 12 Sep 2026: "No direct positions in fossil fuels, please."  
   <sub>clients.json CASE-002: ClientNotes</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Resolve "Volatility range undershot (portfolio risk too low)".  
   <sub>clients.json CASE-002: SuitabilityViolations[Id=929601]</sub>
9. **Next best actions.** Follow up on the proposal of 28 Jul 2026 that was rejected (reason: Client called); it would have had the client buy SPDR MSCI World Health Care UCITS ETF and sell iShares Listed Private Equity UCITS ETF.  
   <sub>clients.json CASE-002: Proposals[24210] × Transactions</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Joker is calling: Investor profile 5, CHF 185k across 1 portfolio.  
   <sub>clients.json CASE-002: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: calm temperament, wants it detailed. From the notes: "Mentioned a possible change of address next year; account details to be confirmed then."  
   <sub>data/profiles/profiles.json CASE-002 (apertus) from clients.json ClientNotes</sub>
3. **reason.** Probably the proposal of 28 Jul 2026 that was rejected (reason: Client called).  
   <sub>clients.json CASE-002: Proposals[24210]</sub>
4. **reason.** Possibly the market: about −CHF 2k today, −0.9% of the book. Mostly Information Technology, −4.8% on 6.1% of it.  
   <sub>impact of the market feed on clients.json CASE-002 holdings</sub>
5. **digest.** About −CHF 2k today, −0.9% of the book.  
   <sub>impact of the market feed on clients.json CASE-002 holdings</sub>
6. **digest.** About −CHF 541 from Information Technology, −4.8% today on 6.1% of the book, mostly MSCI World Socially Responsible UCITS ETF and Global Clean Energy UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-002 holdings</sub>
7. **digest.** About −CHF 431 from the dollar, −1.2% against the franc on 19.5% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-002 holdings</sub>
8. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
10. **digest.** About −CHF 177 from Ether, −8.1% today on 1.2% of the book.  
   <sub>market feed "tech-selloff": XETUSD Curncy CHG_PCT_1D × clients.json CASE-002 holdings</sub>
11. **digest.** 5.7% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-002 holdings without a mapped market move</sub>
12. **holding.** Global Investment Grade Credit Fund and SPDR Bloomberg Global Aggregate Bond UCITS ETF (17.7% of the book) are hedged to the franc, so the dollar move (−1.2%) does not reach them.  
   <sub>clients.json CASE-002: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>
13. **holding.** Holding up today: Swiss franc bonds +0.2% (34.2% of the book); foreign bonds +0.3% (6.4% of the book); Consumer Staples +0.3% (4.6% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-002 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): "Overweight in the equity sector "Industrials"" means: Overweight (+/- 5% of the benchmark’s SAA target) in the ‘Industrials’ equity sector  
  <sub>clients.json CASE-002: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Underweight in the equity sector "Consumer Staples"" means: Underweight (+/- 5% of the benchmark’s SAA target) in the Basic Consumer Goods equity sector  
  <sub>clients.json CASE-002: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.14): Health Care is 14.2% of the book (CHF 26k) after fund look-through, mostly via CSIF (CH) Equity Switzerland Large Cap Blue and SPDR MSCI World Health Care UCITS ETF.  
  <sub>clients.json CASE-002: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.13): Financials is 13.2% of the book (CHF 24k) after fund look-through, mostly via Swisscanto (CH) Real Estate Fund Responsible IFCA and CSIF (CH) Equity Switzerland Large Cap Blue.  
  <sub>clients.json CASE-002: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 12 Apr 2025: "Mentioned a possible change of address next year; account details to be confirmed then."  
  <sub>clients.json CASE-002: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (20 May 2025, reason: Market volatility follow-up) ordered to buy FTSE All-World High Dividend Yield UCITS ETF and iShares USD Treasury Bond UCITS ETF and sell iShares Global Water UCITS ETF and USD Treasury Bond 1-3 UCITS ETF.  
  <sub>clients.json CASE-002: Proposals[14820] × Transactions</sub>
- **Watch** (0.06): 11.2% of the book is in holdings on none of the bank's recommendation lists, largest MSCI World Socially Responsible UCITS ETF.  
  <sub>reference.json Securities.InRecommendationList; clients.json CASE-002 positions</sub>
- **Watch** (0.05): Currency-hedged holdings: Global Investment Grade Credit Fund, SPDR Bloomberg Global Aggregate Bond UCITS ETF (17.7% of the book).  
  <sub>clients.json CASE-002: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Investment advisory (CASE-002-01), 3 Sep 2026: expected return 4.5%, value at risk 14.0%.  
  <sub>clients.json CASE-002: Portfolios[CASE-002-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 40.6% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-002: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 3k, 1.7% of the book.  
  <sub>clients.json CASE-002: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 52.0% of the portfolio (CHF 96k).  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 40.6% of the portfolio (CHF 75k).  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 5.7% of the portfolio (CHF 10k).  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 1.7% of the portfolio (CHF 3k).  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 14.2% of the portfolio (CHF 26k) after fund look-through.  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 13.2% of the portfolio (CHF 24k) after fund look-through.  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 8.2% of the portfolio (CHF 15k) after fund look-through.  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 6.1% of the portfolio (CHF 11k) after fund look-through.  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 4.6% of the portfolio (CHF 8k) after fund look-through.  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 3.3% of the portfolio (CHF 6k) after fund look-through.  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 3.0% of the portfolio (CHF 6k) after fund look-through.  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 3.0% of the portfolio (CHF 5k) after fund look-through.  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 1.2% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.9% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.1% of the portfolio (CHF 211) after fund look-through.  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 67.1% of the portfolio (CHF 124k).  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 28.4% of the portfolio (CHF 53k).  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 3.3% of the portfolio (CHF 6k).  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): ETH: 1.2% of the portfolio (CHF 2k).  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Crypto: CHF 12k, 6.3% of the portfolio.  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: CSIF (CH) Equity Switzerland Large Cap Blue, CHF 27k (14.6% of the portfolio).  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 15 holdings; the largest: CSIF (CH) Equity Switzerland Large Cap Blue (CHF 27k), MSCI World Socially Responsible UCITS ETF (CHF 21k), SPDR Bloomberg Global Aggregate Bond UCITS ETF (CHF 19k), Short Duration High Yield Portfolio (CHF 16k).  
  <sub>clients.json CASE-002: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.40): Book a review: the last finalised proposal was on 20 May 2025.  
  <sub>clients.json CASE-002: Proposals.FinalizedDateUTC</sub>
- **Next best actions** (0.30): Resolve "Overweight in the equity sector "Industrials"".  
  <sub>clients.json CASE-002: SuitabilityViolations[Id=601143]</sub>
- **Next best actions** (0.30): Resolve "Underweight in the equity sector "Consumer Staples"".  
  <sub>clients.json CASE-002: SuitabilityViolations[Id=789376]</sub>

</details>

---

## CASE-003 — Ron Burgundy

Investor profile 5 · CHF 141k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Ron Burgundy, Investor profile 5, CHF 141k across 1 portfolio.  
   <sub>clients.json CASE-003: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +12.1% over the 12 months to Jul 2026 and −18.8% since Oct 2021, now CHF 141k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-003: PerformanceHistory of CASE-003-01</sub>
3. **Health check.** Volatility is 20.0%, above the 12.0% maximum of Investor profile 5.  
   <sub>clients.json CASE-003: Portfolios[CASE-003-01].Volatility; reference.json RiskProfiles.MaxVola</sub>
4. **Health check.** Risk profile last assessed 28 Sep 2022, 4 years ago.  
   <sub>clients.json CASE-003: ProfilingDateUtc</sub>
5. **Watch.** Consumer Staples is 73.4% of the book (CHF 103k) after fund look-through, mostly via Chocoladefabriken Lindt & Spruengli AG.  
   <sub>clients.json CASE-003: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Watch.** Chocoladefabriken Lindt & Spruengli AG alone is 73.4% of the book.  
   <sub>clients.json CASE-003: Portfolios[CASE-003-01].SecurityPositions</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "We remain Underweight real estate and consumer staples amid weak sentiment and low visibility on the housing recovery."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-003: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Ron Burgundy is calling: Investor profile 5, CHF 141k across 1 portfolio.  
   <sub>clients.json CASE-003: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably a withdrawal: note from 1 May 2026: "Plans to retire in the next two years, increasing liquidity needs expected."  
   <sub>clients.json CASE-003: ClientNotes</sub>
3. **reason.** Possibly the market: about −CHF 1k today, −0.9% of the book. Mostly Information Technology, −4.8% on 23.6% of it.  
   <sub>impact of the market feed on clients.json CASE-003 holdings</sub>
4. **digest.** About −CHF 1k today, −0.9% of the book.  
   <sub>impact of the market feed on clients.json CASE-003 holdings</sub>
5. **digest.** About −CHF 2k from Information Technology, −4.8% today on 23.6% of the book, mostly Sensirion Holding AG.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-003 holdings</sub>
6. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
7. **holding.** Holding up today: Consumer Staples +0.3% (73.4% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × clients.json CASE-003 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.66): Chocoladefabriken Lindt & Spruengli AG drives 65.9% of the volatility of Account / Custody (CASE-003-01).  
  <sub>clients.json CASE-003: Portfolios[CASE-003-01].SecurityPositions.ContributionVolatility</sub>
- **Watch** (0.50): Note from 1 May 2026: "Plans to retire in the next two years, increasing liquidity needs expected."  
  <sub>clients.json CASE-003: ClientNotes</sub>
- **Watch** (0.24): Information Technology is 23.6% of the book (CHF 33k) after fund look-through, mostly via Sensirion Holding AG.  
  <sub>clients.json CASE-003: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.24): Sensirion Holding AG alone is 23.6% of the book.  
  <sub>clients.json CASE-003: Portfolios[CASE-003-01].SecurityPositions</sub>
- **Watch** (0.15): Note from 10 Sep 2026: "Prefers ESG-compliant investments, no defense or tobacco holdings."  
  <sub>clients.json CASE-003: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Account / Custody (CASE-003-01), 3 Sep 2026: expected return 6.4%, value at risk 19.0%.  
  <sub>clients.json CASE-003: Portfolios[CASE-003-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 4k, 3.0% of the book.  
  <sub>clients.json CASE-003: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 97.0% of the portfolio (CHF 136k).  
  <sub>clients.json CASE-003: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 3.0% of the portfolio (CHF 4k).  
  <sub>clients.json CASE-003: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Consumer Staples is 73.4% of the portfolio (CHF 103k) after fund look-through.  
  <sub>clients.json CASE-003: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 23.6% of the portfolio (CHF 33k) after fund look-through.  
  <sub>clients.json CASE-003: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 141k).  
  <sub>clients.json CASE-003: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Chocoladefabriken Lindt & Spruengli AG, CHF 103k (73.4% of the portfolio).  
  <sub>clients.json CASE-003: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 2 holdings; the largest: Chocoladefabriken Lindt & Spruengli AG (CHF 103k), Sensirion Holding AG (CHF 33k).  
  <sub>clients.json CASE-003: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-004 — Rocky Balboa

Investor profile 5 · CHF 534k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Rocky Balboa, Investor profile 5, CHF 534k across 1 portfolio.  
   <sub>clients.json CASE-004: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +16.4% over the 12 months to Jul 2026 and +33.0% since Oct 2021, now CHF 530k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-004: PerformanceHistory of CASE-004-01</sub>
3. **Health check.** 2 suitability errors and 0 warnings open; most serious: "Overweight in the equity sector "Energy"".  
   <sub>clients.json CASE-004: SuitabilityViolations</sub>
4. **Health check.** 7 of 7 orders from the proposal of 22 Jul 2026 were forwarded with a warning.  
   <sub>clients.json CASE-004: Transactions[ProposalId=23993].ForwardState = 2</sub>
5. **Watch.** Note from 9 Jun 2026: "Plans to retire in the next two years, increasing liquidity needs expected."  
   <sub>clients.json CASE-004: ClientNotes</sub>
6. **Watch.** Health Care is 15.9% of the book (CHF 85k) after fund look-through, mostly via SPDR MSCI World Health Care UCITS ETF and Roche Holding AG.  
   <sub>clients.json CASE-004: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Resolve "Overweight in the equity sector "Energy"".  
   <sub>clients.json CASE-004: SuitabilityViolations[Id=725778]</sub>
9. **Next best actions.** Resolve "Significant overweight in the equity region "Japan"".  
   <sub>clients.json CASE-004: SuitabilityViolations[Id=743203]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Rocky Balboa is calling: Investor profile 5, CHF 534k across 1 portfolio.  
   <sub>clients.json CASE-004: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably a withdrawal: note from 9 Jun 2026: "Plans to retire in the next two years, increasing liquidity needs expected."  
   <sub>clients.json CASE-004: ClientNotes</sub>
3. **reason.** Possibly the proposal of 4 Aug 2026 that was rejected (reason: Client relocation).  
   <sub>clients.json CASE-004: Proposals[24385]</sub>
4. **reason.** Possibly the market: about −CHF 5k today, −0.9% of the book. Mostly the dollar, −1.2% on 25.1% of it.  
   <sub>impact of the market feed on clients.json CASE-004 holdings</sub>
5. **digest.** About −CHF 5k today, −0.9% of the book.  
   <sub>impact of the market feed on clients.json CASE-004 holdings</sub>
6. **digest.** About −CHF 2k from the dollar, −1.2% against the franc on 25.1% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-004 holdings</sub>
7. **digest.** About −CHF 2k from Information Technology, −4.8% today on 6.2% of the book, mostly iShares Edge MSCI USA Quality Factor UCITS ETF and iShares Edge MSCI World Value Factor UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-004 holdings</sub>
8. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
10. **digest.** About −CHF 517 from Financials, −0.9% today on 10.7% of the book, mostly Swiss Life Holding AG and iShares Swiss Dividend ETF (CH).  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-004 holdings</sub>
11. **digest.** 14.1% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-004 holdings without a mapped market move</sub>
12. **holding.** Glob.High Yield Corp Bd CHF UCITS ETF (Dist) and SPDR Bloomberg Global Aggregate Bond UCITS ETF (10.2% of the book) are hedged to the franc, so the dollar move (−1.2%) does not reach them.  
   <sub>clients.json CASE-004: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>
13. **holding.** Holding up today: Swiss franc bonds +0.2% (17.3% of the book); Consumer Staples +0.3% (11.0% of the book); foreign bonds +0.3% (3.2% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-004 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): "Overweight in the equity sector "Energy"" means: Overweight (+/- 5% of the benchmark’s SAA target) in the Energy equity sector  
  <sub>clients.json CASE-004: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Significant overweight in the equity region "Japan"" means: Significant overweight (+/- 10% of the benchmark’s SAA target) in the ‘Japan’ equity region  
  <sub>clients.json CASE-004: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.14): Financials is 13.9% of the book (CHF 74k) after fund look-through, mostly via Swisscanto (CH) Real Estate Fund Responsible IFCA and Swiss Life Holding AG.  
  <sub>clients.json CASE-004: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 8 May 2025: "Has expressed interest in consolidating multiple accounts."  
  <sub>clients.json CASE-004: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (22 Jul 2026, reason: Life event (retirement)) ordered to buy iShares Core S&P 500 UCITS ETF, iShares Edge MSCI USA Quality Factor UCITS ETF and 2 more and sell SPDR MSCI World Energy UCITS ETF, SPDR MSCI World Small Cap UCITS ETF and 1 more.  
  <sub>clients.json CASE-004: Proposals[23993] × Transactions</sub>
- **Watch** (0.07): 14.3% of the book is in holdings on none of the bank's recommendation lists, largest 6.81 % Reverse Convertible UBS London 2023-23.09.24 on Lonza Gr/Geberit/Sika, 7.1 % Reverse Convertible UBS London 2023-23.09.24 on ABB/CieFinRichemont/Alcon and 2 more.  
  <sub>reference.json Securities.InRecommendationList; clients.json CASE-004 positions</sub>
- **Watch** (0.05): Currency-hedged holdings: Glob.High Yield Corp Bd CHF UCITS ETF (Dist), SPDR Bloomberg Global Aggregate Bond UCITS ETF (10.2% of the book).  
  <sub>clients.json CASE-004: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-004-01), 3 Sep 2026: expected return 5.4%, value at risk 10.5%.  
  <sub>clients.json CASE-004: Portfolios[CASE-004-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 28.3% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-004: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 9k, 1.6% of the book.  
  <sub>clients.json CASE-004: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 63.7% of the portfolio (CHF 340k).  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 20.5% of the portfolio (CHF 110k).  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 11.0% of the portfolio (CHF 59k).  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 3.1% of the portfolio (CHF 17k).  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 1.6% of the portfolio (CHF 9k).  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 15.9% of the portfolio (CHF 85k) after fund look-through.  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 13.9% of the portfolio (CHF 74k) after fund look-through.  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 11.0% of the portfolio (CHF 59k) after fund look-through.  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 7.5% of the portfolio (CHF 40k) after fund look-through.  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 6.2% of the portfolio (CHF 33k) after fund look-through.  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 5.5% of the portfolio (CHF 29k) after fund look-through.  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 3.5% of the portfolio (CHF 19k) after fund look-through.  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 3.3% of the portfolio (CHF 18k) after fund look-through.  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 2.1% of the portfolio (CHF 11k) after fund look-through.  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.7% of the portfolio (CHF 4k) after fund look-through.  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.6% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 62.0% of the portfolio (CHF 331k).  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 37.2% of the portfolio (CHF 199k).  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): SOL: 0.8% of the portfolio (CHF 4k).  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Crypto: CHF 4k, 0.8% of the portfolio.  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares Edge MSCI World Value Factor UCITS ETF, CHF 44k (8.1% of the portfolio).  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 24 holdings; the largest: iShares Edge MSCI World Value Factor UCITS ETF (CHF 44k), iShares SMI(R) Equity Index Fund (CH) (CHF 41k), SPDR Bloomberg Global Aggregate Bond UCITS ETF (CHF 40k), iShares Edge MSCI USA Quality Factor UCITS ETF (CHF 35k).  
  <sub>clients.json CASE-004: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.50): Follow up on the proposal of 4 Aug 2026 that was rejected (reason: Client relocation); it would have had the client buy Xtrackers MSCI World UCITS ETF, FTSE All-World High Dividend Yield UCITS ETF and 25 more and sell iShares Edge MSCI World Value Factor UCITS ETF and SPDR MSCI World Energy UCITS ETF.  
  <sub>clients.json CASE-004: Proposals[24385] × Transactions</sub>
- **Next best actions** (0.25): Clear the warnings on the 7 flagged orders from the proposal of 22 Jul 2026.  
  <sub>clients.json CASE-004: Transactions[ProposalId=23993].ForwardState = 2</sub>

</details>

---

## CASE-005 — Norman Bates

Investor profile 6 · CHF 480k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Norman Bates, Investor profile 6, ESG preference, CHF 480k across 2 portfolios.  
   <sub>clients.json CASE-005: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Combined portfolio value +20.0% over the 12 months to Jul 2026 and +56.3% since Oct 2021, now CHF 480k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-005: PerformanceHistory of CASE-005-01, CASE-005-02</sub>
3. **Health check.** ESG client: average sustainability score 6.3 of 10 against a minimum of 5.7; 3 holdings below the per-position minimum (GQG Partners Emerging Markets Equity Fund, Biotechnology Fund and 1 more, 15.1% of the book); 33.5% of the book has no score.  
   <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-005 positions</sub>
4. **Health check.** 2 of 4 orders from the proposal of 24 Jan 2026 were forwarded with a warning.  
   <sub>clients.json CASE-005: Transactions[ProposalId=20030].ForwardState = 2</sub>
5. **Watch.** Precious Metals Fund drives 31.1% of the volatility of Individual pension (CASE-005-02).  
   <sub>clients.json CASE-005: Portfolios[CASE-005-02].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Note from 14 Mar 2026: "Would like a follow-up call before any changes to the standing order."  
   <sub>clients.json CASE-005: ClientNotes</sub>
7. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "That means maintaining an overweight position in technology stocks."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
8. **Next best actions.** Deploy idle liquidity: 25.9% of the book (CHF 124k) is cash.  
   <sub>clients.json CASE-005: LiquidityInDefaultCurrency</sub>
9. **Next best actions.** Candidates from the recommendation list for Shares: ABB Ltd and Kuehne + Nagel International AG (cash is above 10% of the book).  
   <sub>reference.json RecommendationLists "Recommendation list free assets", not held, CHF first, ordered by SustainabilityScore</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Norman Bates is calling: Investor profile 6, ESG preference, CHF 480k across 2 portfolios.  
   <sub>clients.json CASE-005: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: calm temperament, wants it short. From the notes: "Also manages a family member's portfolio under a power of attorney."  
   <sub>data/profiles/profiles.json CASE-005 (apertus) from clients.json ClientNotes</sub>
3. **caller.** Contact preference: "Would like a follow-up call before any changes to the standing order"  
   <sub>data/profiles/profiles.json CASE-005 from clients.json ClientNotes</sub>
4. **reason.** Probably a sustainability concern: ESG client: average sustainability score 6.3 of 10 against a minimum of 5.7; 3 holdings below the per-position minimum (GQG Partners Emerging Markets Equity Fund, Biotechnology Fund and 1 more, 15.1% of the book); 33.5% of the book has no score.  
   <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-005 positions</sub>
5. **reason.** Possibly the market: about −CHF 2k today, −0.5% of the book. Mostly Information Technology, −4.8% on 7.6% of it.  
   <sub>impact of the market feed on clients.json CASE-005 holdings</sub>
6. **reason.** Possibly idle cash: 25.9% of the book (CHF 124k) is cash.  
   <sub>clients.json CASE-005: LiquidityInDefaultCurrency</sub>
7. **digest.** About −CHF 2k today, −0.5% of the book.  
   <sub>impact of the market feed on clients.json CASE-005 holdings</sub>
8. **digest.** About −CHF 2k from Information Technology, −4.8% today on 7.6% of the book, mostly Smart Energy Fund and GQG Partners Emerging Markets Equity Fund.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-005 holdings</sub>
9. **digest.** About −CHF 1k from the dollar, −1.2% against the franc on 20.7% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-005 holdings</sub>
10. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
11. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
12. **digest.** About −CHF 267 from Raw materials, −0.6% today on 9.3% of the book, mostly Precious Metals Fund and Smart Energy Fund.  
   <sub>market feed "tech-selloff": S5MATR Index CHG_PCT_1D × clients.json CASE-005 holdings</sub>
13. **digest.** 7.0% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-005 holdings without a mapped market move</sub>
14. **holding.** Holding up today: Gold +1.4% (20.5% of the book); Silver +0.8% (6.1% of the book); Utilities +0.5% (3.3% of the book).  
   <sub>market feed "tech-selloff": XAU Curncy CHG_PCT_1D × clients.json CASE-005 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.13): 26.8% of the book is in holdings on none of the bank's recommendation lists, largest GQG Partners Emerging Markets Equity Fund, Precious Metals Fund and 3 more.  
  <sub>reference.json Securities.InRecommendationList; clients.json CASE-005 positions</sub>
- **Watch** (0.10): Note from 8 Nov 2024: "Also manages a family member's portfolio under a power of attorney."  
  <sub>clients.json CASE-005: ClientNotes</sub>
- **Watch** (0.09): Raw materials is 9.3% of the book (CHF 45k) after fund look-through, mostly via Precious Metals Fund and Smart Energy Fund.  
  <sub>clients.json CASE-005: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.08): The last finalised proposal (24 Jan 2026, reason: Client relocation) ordered to sell Swiss Small & Mid Cap Equity, GAM Star Disruptive Growth and 2 more.  
  <sub>clients.json CASE-005: Proposals[20030] × Transactions</sub>
- **Watch** (0.08): Information Technology is 7.6% of the book (CHF 36k) after fund look-through, mostly via Smart Energy Fund and GQG Partners Emerging Markets Equity Fund.  
  <sub>clients.json CASE-005: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.07): CSIF (CH) I Equity World ex CH Blue drives 32.9% of the volatility of Pension (CASE-005-01).  
  <sub>clients.json CASE-005: Portfolios[CASE-005-01].SecurityPositions.ContributionVolatility</sub>
- **Watch** (0.03): Risk engine for Pension (CASE-005-01), 3 Sep 2026: expected return 5.3%, value at risk 13.9%.  
  <sub>clients.json CASE-005: Portfolios[CASE-005-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.03): Risk engine for Individual pension (CASE-005-02), 3 Sep 2026: expected return 2.7%, value at risk 9.3%.  
  <sub>clients.json CASE-005: Portfolios[CASE-005-02].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 33.5% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-005: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 124k, 25.9% of the book.  
  <sub>clients.json CASE-005: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 40.6% of the portfolio (CHF 195k).  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 30.8% of the portfolio (CHF 147k).  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 25.9% of the portfolio (CHF 124k).  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 2.8% of the portfolio (CHF 13k).  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Raw materials is 9.3% of the portfolio (CHF 45k) after fund look-through.  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 7.6% of the portfolio (CHF 36k) after fund look-through.  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 7.0% of the portfolio (CHF 34k) after fund look-through.  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 4.1% of the portfolio (CHF 20k) after fund look-through.  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 3.7% of the portfolio (CHF 18k) after fund look-through.  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 3.3% of the portfolio (CHF 16k) after fund look-through.  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 2.2% of the portfolio (CHF 10k) after fund look-through.  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 1.4% of the portfolio (CHF 7k) after fund look-through.  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 1.0% of the portfolio (CHF 5k) after fund look-through.  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 0.7% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.4% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 67.6% of the portfolio (CHF 324k).  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 27.1% of the portfolio (CHF 130k).  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 5.3% of the portfolio (CHF 25k).  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Gold: CHF 98k, 20.5% of the portfolio.  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Silver: CHF 29k, 6.1% of the portfolio.  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: CSIF (CH) II Gold Blue, CHF 98k (20.5% of the portfolio).  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 13 holdings; the largest: CSIF (CH) II Gold Blue (CHF 98k), GQG Partners Emerging Markets Equity Fund (CHF 40k), Precious Metals Fund (CHF 36k), CSIF (CH) I Equity World ex CH Blue (CHF 31k).  
  <sub>clients.json CASE-005: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.12): Clear the warnings on the 2 flagged orders from the proposal of 24 Jan 2026.  
  <sub>clients.json CASE-005: Transactions[ProposalId=20030].ForwardState = 2</sub>

</details>

---

## CASE-006 — Spock

Investor profile 5 · CHF 700k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Spock, Investor profile 5, CHF 700k across 3 portfolios.  
   <sub>clients.json CASE-006: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Combined portfolio value +17.5% over the 12 months to Jul 2026 and +18.9% since Oct 2021, now CHF 700k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-006: PerformanceHistory of CASE-006-01, CASE-006-02, CASE-006-03</sub>
3. **Health check.** Risk profile last assessed 5 Sep 2022, 4 years ago.  
   <sub>clients.json CASE-006: ProfilingDateUtc</sub>
4. **Health check.** Volatility in Account / Custody (CASE-006-01) is 12.6%, above the 12.0% maximum of Investor profile 5.  
   <sub>clients.json CASE-006: Portfolios[CASE-006-01].Volatility; reference.json RiskProfiles.MaxVola</sub>
5. **Watch.** Sika AG drives 31.2% of the volatility of Account / Custody (CASE-006-01).  
   <sub>clients.json CASE-006: Portfolios[CASE-006-01].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Consumer Staples is 18.7% of the book (CHF 131k) after fund look-through, mostly via Nestle SA and Anheuser-Busch InBev SA/NV.  
   <sub>clients.json CASE-006: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "We remain Underweight real estate and consumer staples amid weak sentiment and low visibility on the housing recovery."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Deploy idle liquidity: 41.5% of the book (CHF 290k) is cash.  
   <sub>clients.json CASE-006: LiquidityInDefaultCurrency</sub>
9. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-006: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Spock is calling: Investor profile 5, CHF 700k across 3 portfolios.  
   <sub>clients.json CASE-006: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Contact preference: "Prefers email communication, hard to reach by phone"  
   <sub>data/profiles/profiles.json CASE-006 from clients.json ClientNotes</sub>
3. **reason.** Probably a withdrawal: note from 27 Jul 2026: "Considering a charitable donation from the portfolio, details being clarified."  
   <sub>clients.json CASE-006: ClientNotes</sub>
4. **digest.** About −CHF 2k today, −0.3% of the book.  
   <sub>impact of the market feed on clients.json CASE-006 holdings</sub>
5. **digest.** About −CHF 920 from Consumer Discretionary, −2.2% today on 6.0% of the book, mostly adidas AG and The Swatch Group AG.  
   <sub>market feed "tech-selloff": S5COND Index CHG_PCT_1D × clients.json CASE-006 holdings</sub>
6. **digest.** About −CHF 698 from Financials, −0.9% today on 11.1% of the book, mostly Zurich Insurance Group AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-006 holdings</sub>
7. **digest.** About −CHF 474 from Raw materials, −0.6% today on 11.3% of the book, mostly Sika AG.  
   <sub>market feed "tech-selloff": S5MATR Index CHG_PCT_1D × clients.json CASE-006 holdings</sub>
8. **holding.** Holding up today: Consumer Staples +0.3% (18.7% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × clients.json CASE-006 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.17): Nestle SA alone is 17.3% of the book.  
  <sub>clients.json CASE-006: Portfolios[CASE-006-01].SecurityPositions</sub>
- **Watch** (0.15): Note from 27 Jul 2026: "Considering a charitable donation from the portfolio, details being clarified."  
  <sub>clients.json CASE-006: ClientNotes</sub>
- **Watch** (0.11): Raw materials is 11.3% of the book (CHF 79k) after fund look-through, mostly via Sika AG.  
  <sub>clients.json CASE-006: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.11): Sika AG alone is 11.3% of the book.  
  <sub>clients.json CASE-006: Portfolios[CASE-006-01].SecurityPositions</sub>
- **Watch** (0.11): Zurich Insurance Group AG alone is 11.1% of the book.  
  <sub>clients.json CASE-006: Portfolios[CASE-006-01].SecurityPositions</sub>
- **Watch** (0.10): Note from 1 Sep 2025: "Wants exposure limited to developed markets only, no emerging markets."  
  <sub>clients.json CASE-006: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Account / Custody (CASE-006-01), 3 Sep 2026: expected return 5.6%, value at risk 13.3%.  
  <sub>clients.json CASE-006: Portfolios[CASE-006-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 290k, 41.5% of the book.  
  <sub>clients.json CASE-006: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 58.5% of the portfolio (CHF 410k).  
  <sub>clients.json CASE-006: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 41.5% of the portfolio (CHF 290k).  
  <sub>clients.json CASE-006: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Consumer Staples is 18.7% of the portfolio (CHF 131k) after fund look-through.  
  <sub>clients.json CASE-006: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 11.3% of the portfolio (CHF 79k) after fund look-through.  
  <sub>clients.json CASE-006: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 11.1% of the portfolio (CHF 78k) after fund look-through.  
  <sub>clients.json CASE-006: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 9.2% of the portfolio (CHF 64k) after fund look-through.  
  <sub>clients.json CASE-006: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 6.0% of the portfolio (CHF 42k) after fund look-through.  
  <sub>clients.json CASE-006: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 2.3% of the portfolio (CHF 16k) after fund look-through.  
  <sub>clients.json CASE-006: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 86.9% of the portfolio (CHF 609k).  
  <sub>clients.json CASE-006: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 13.1% of the portfolio (CHF 91k).  
  <sub>clients.json CASE-006: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Nestle SA, CHF 121k (17.3% of the portfolio).  
  <sub>clients.json CASE-006: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 10 holdings; the largest: Nestle SA (CHF 121k), Sika AG (CHF 79k), Zurich Insurance Group AG (CHF 78k), Roche Holding AG (CHF 49k).  
  <sub>clients.json CASE-006: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.20): Candidates from the recommendation list for Shares: ABB Ltd and Kuehne + Nagel International AG (cash is above 10% of the book).  
  <sub>reference.json RecommendationLists "Recommendation list free assets", not held, CHF first, ordered by SustainabilityScore</sub>

</details>

---

## CASE-007 — Mary Poppins

Investor profile 5 · CHF 905k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Mary Poppins, Investor profile 5, ESG preference, CHF 905k across 1 portfolio.  
   <sub>clients.json CASE-007: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +15.2% over the 12 months to Jul 2026 and +59.0% since Oct 2021, now CHF 905k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-007: PerformanceHistory of CASE-007-01</sub>
3. **Health check.** 1 suitability error and 0 warnings open; most serious: "Compliance with maximum volatility".  
   <sub>clients.json CASE-007: SuitabilityViolations</sub>
4. **Health check.** Risk profile last assessed 31 Jul 2022, 4 years ago.  
   <sub>clients.json CASE-007: ProfilingDateUtc</sub>
5. **Watch.** Note from 1 Jan 2026: "Requested a comparison against the benchmark at the next review."  
   <sub>clients.json CASE-007: ClientNotes</sub>
6. **Watch.** Health Care is 10.7% of the book (CHF 97k) after fund look-through, mostly via iShares Swiss Dividend ETF (CH) and Equities Switzerland Passive Leader.  
   <sub>clients.json CASE-007: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Resolve "Compliance with maximum volatility".  
   <sub>clients.json CASE-007: SuitabilityViolations[Id=231263]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Mary Poppins is calling: Investor profile 5, ESG preference, CHF 905k across 1 portfolio.  
   <sub>clients.json CASE-007: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Contact preference: "Hard to reach during the day, best contacted after 6pm"  
   <sub>data/profiles/profiles.json CASE-007 from clients.json ClientNotes</sub>
3. **reason.** Probably the market: about −CHF 7k today, −0.7% of the book. Mostly Information Technology, −4.8% on 6.6% of it.  
   <sub>impact of the market feed on clients.json CASE-007 holdings</sub>
4. **reason.** Possibly a sustainability concern: ESG client: average sustainability score 7.1 of 10 against a minimum of 5.7; 2 holdings below the per-position minimum (iShares Core MSCI EM IMI UCITS ETF and ams-OSRAM AG, 3.0% of the book).  
   <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-007 positions</sub>
5. **digest.** About −CHF 7k today, −0.7% of the book.  
   <sub>impact of the market feed on clients.json CASE-007 holdings</sub>
6. **digest.** About −CHF 3k from Information Technology, −4.8% today on 6.6% of the book, mostly Edge MSCI World Momentum Factor UCITS ETF and iShares MSCI World CHF Hedged UCITS ETF (Acc).  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-007 holdings</sub>
7. **digest.** About −CHF 934 from the dollar, −1.2% against the franc on 8.6% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-007 holdings</sub>
8. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
10. **digest.** About −CHF 853 from Financials, −0.9% today on 10.5% of the book, mostly iShares Swiss Dividend ETF (CH) and Equities Switzerland Passive Leader.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-007 holdings</sub>
11. **digest.** 6.8% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-007 holdings without a mapped market move</sub>
12. **holding.** Global Investment Grade Credit Fund and iShares MSCI World CHF Hedged UCITS ETF (Acc) and US Short Duration High Yield (18.0% of the book) are hedged to the franc, so the dollar move (−1.2%) does not reach them.  
   <sub>clients.json CASE-007: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>
13. **holding.** Holding up today: Swiss franc bonds +0.2% (35.2% of the book); Consumer Staples +0.3% (9.4% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-007 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.15): 1 of 1 order from the proposal of 14 Jan 2026 were forwarded with a warning.  
  <sub>clients.json CASE-007: Transactions[ProposalId=19898].ForwardState = 2</sub>
- **Health check** (0.06): ESG client: average sustainability score 7.1 of 10 against a minimum of 5.7; 2 holdings below the per-position minimum (iShares Core MSCI EM IMI UCITS ETF and ams-OSRAM AG, 3.0% of the book).  
  <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-007 positions</sub>
- **Health check** (0.00): "Compliance with maximum volatility" means: For retail clients with financial services Comprehensive investment advisory or discretionary mandate must be PF Vola < max client profile Vola.  
  <sub>clients.json CASE-007: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.10): Financials is 10.5% of the book (CHF 95k) after fund look-through, mostly via iShares Swiss Dividend ETF (CH) and Equities Switzerland Passive Leader.  
  <sub>clients.json CASE-007: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 27 May 2025: "Prefers to avoid any exposure to fossil-fuel energy in the portfolio."  
  <sub>clients.json CASE-007: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (11 May 2026, reason: Follow-up from prior meeting) ordered to buy Global Investment Grade Credit Fund, Credit Suisse (CH) Corporate CHF Bond Fund and 4 more.  
  <sub>clients.json CASE-007: Proposals[22465] × Transactions</sub>
- **Watch** (0.05): Currency-hedged holdings: Global Investment Grade Credit Fund, iShares MSCI World CHF Hedged UCITS ETF (Acc), US Short Duration High Yield (18.0% of the book).  
  <sub>clients.json CASE-007: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-007-01), 3 Sep 2026: expected return 4.9%, value at risk 14.3%.  
  <sub>clients.json CASE-007: Portfolios[CASE-007-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 42.8% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-007: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 4k, 0.5% of the book.  
  <sub>clients.json CASE-007: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 56.7% of the portfolio (CHF 513k).  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 35.2% of the portfolio (CHF 319k).  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 7.6% of the portfolio (CHF 69k).  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 0.5% of the portfolio (CHF 4k).  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 10.7% of the portfolio (CHF 97k) after fund look-through.  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 10.5% of the portfolio (CHF 95k) after fund look-through.  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 9.4% of the portfolio (CHF 85k) after fund look-through.  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 7.6% of the portfolio (CHF 69k) after fund look-through.  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 6.6% of the portfolio (CHF 60k) after fund look-through.  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 4.1% of the portfolio (CHF 37k) after fund look-through.  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 2.8% of the portfolio (CHF 26k) after fund look-through.  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 2.5% of the portfolio (CHF 23k) after fund look-through.  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 1.4% of the portfolio (CHF 13k) after fund look-through.  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.7% of the portfolio (CHF 6k) after fund look-through.  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.6% of the portfolio (CHF 5k) after fund look-through.  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 78.5% of the portfolio (CHF 711k).  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 14.7% of the portfolio (CHF 134k).  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 6.8% of the portfolio (CHF 61k).  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Palladium: CHF 8k, 0.9% of the portfolio.  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares Swiss Dividend ETF (CH), CHF 106k (11.7% of the portfolio).  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 20 holdings; the largest: iShares Swiss Dividend ETF (CH) (CHF 106k), Equities Switzerland Passive Leader (CHF 93k), Edge MSCI World Momentum Factor UCITS ETF (CHF 62k), iShares MSCI World CHF Hedged UCITS ETF (Acc) (CHF 59k).  
  <sub>clients.json CASE-007: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-008 — Betty Boop

Investor profile 7 · CHF 308k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Betty Boop, Investor profile 7, ESG preference, CHF 308k across 1 portfolio.  
   <sub>clients.json CASE-008: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +17.7% over the 12 months to Jul 2026 and +53.8% since Oct 2021, now CHF 308k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-008: PerformanceHistory of CASE-008-01</sub>
3. **Health check.** 5 suitability errors and 7 warnings open; most serious: "Foreign currency exposure exceeds 50%".  
   <sub>clients.json CASE-008: SuitabilityViolations</sub>
4. **Watch.** Equities Switzerland Passive Leader drives 26.0% of the volatility of Pension (CASE-008-01).  
   <sub>clients.json CASE-008: Portfolios[CASE-008-01].SecurityPositions.ContributionVolatility</sub>
5. **Watch.** Health Care is 18.5% of the book (CHF 57k) after fund look-through, mostly via Equities Switzerland Passive Leader and iShares Swiss Dividend ETF (CH).  
   <sub>clients.json CASE-008: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
7. **Next best actions.** Resolve "Significant underweight in the equity sector "Consumer Staples"".  
   <sub>clients.json CASE-008: SuitabilityViolations[Id=893743]</sub>
8. **Next best actions.** Resolve "Significant overweight in the equity sector "Information Technology"".  
   <sub>clients.json CASE-008: SuitabilityViolations[Id=893757]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Betty Boop is calling: Investor profile 7, ESG preference, CHF 308k across 1 portfolio.  
   <sub>clients.json CASE-008: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 6k today, −1.8% of the book. Mostly Information Technology, −4.8% on 13.9% of it.  
   <sub>impact of the market feed on clients.json CASE-008 holdings</sub>
3. **digest.** About −CHF 6k today, −1.8% of the book.  
   <sub>impact of the market feed on clients.json CASE-008 holdings</sub>
4. **digest.** About −CHF 2k from Information Technology, −4.8% today on 13.9% of the book, mostly CSIF (CH) I Equity World ex CH Blue and CSIF (CH) Equity World ex CH ESG Blue.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-008 holdings</sub>
5. **digest.** About −CHF 1k from the dollar, −1.2% against the franc on 31.7% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-008 holdings</sub>
6. **digest.** About −CHF 574 from Consumer Discretionary, −2.2% today on 8.5% of the book, mostly CSIF (CH) I Equity World ex CH Blue and Equities Switzerland Passive Leader.  
   <sub>market feed "tech-selloff": S5COND Index CHG_PCT_1D × clients.json CASE-008 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **holding.** Holding up today: Consumer Staples +0.3% (8.6% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × clients.json CASE-008 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): ESG client: average sustainability score 7.5 of 10 against a minimum of 5.7.  
  <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-008 positions</sub>
- **Health check** (0.00): "Significant underweight in the equity sector "Consumer Staples"" means: Significant underweight (+/- 10% of the benchmark’s SAA target) in the ‘Basic Consumer Goods’ equity sector  
  <sub>clients.json CASE-008: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Significant overweight in the equity sector "Information Technology"" means: Significant overweight (+/- 10% of the benchmark’s SAA target) in the Information Technology sector  
  <sub>clients.json CASE-008: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Foreign currency cluster risk EUR" means: For private customers, the EUR share should be < 9%.  
  <sub>clients.json CASE-008: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.18): Financials is 18.5% of the book (CHF 57k) after fund look-through, mostly via Equities Switzerland Passive Leader and iShares Swiss Dividend ETF (CH).  
  <sub>clients.json CASE-008: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.15): Note from 2 Feb 2026: "Has expressed interest in consolidating multiple accounts."  
  <sub>clients.json CASE-008: ClientNotes</sub>
- **Watch** (0.10): Note from 17 Oct 2024: "Wants as high a weighting of sustainable funds as possible at the next rebalancing."  
  <sub>clients.json CASE-008: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Pension (CASE-008-01), 3 Sep 2026: expected return 6.3%, value at risk 16.3%.  
  <sub>clients.json CASE-008: Portfolios[CASE-008-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 9k, 2.9% of the book.  
  <sub>clients.json CASE-008: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 97.1% of the portfolio (CHF 299k).  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 2.9% of the portfolio (CHF 9k).  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 18.5% of the portfolio (CHF 57k) after fund look-through.  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 18.5% of the portfolio (CHF 57k) after fund look-through.  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 13.9% of the portfolio (CHF 43k) after fund look-through.  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 13.0% of the portfolio (CHF 40k) after fund look-through.  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 8.6% of the portfolio (CHF 26k) after fund look-through.  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 8.5% of the portfolio (CHF 26k) after fund look-through.  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 5.6% of the portfolio (CHF 17k) after fund look-through.  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 5.4% of the portfolio (CHF 17k) after fund look-through.  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 2.0% of the portfolio (CHF 6k) after fund look-through.  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 2.0% of the portfolio (CHF 6k) after fund look-through.  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 1.1% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 308k).  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: CSIF (CH) I Equity World ex CH Blue, CHF 76k (24.6% of the portfolio).  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 6 holdings; the largest: CSIF (CH) I Equity World ex CH Blue (CHF 76k), Equities Switzerland Passive Leader (CHF 74k), CSIF (CH) Equity World ex CH ESG Blue (CHF 58k), Index Equity Fund Small & Mid Caps Switzerland (CHF 37k).  
  <sub>clients.json CASE-008: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (1.00): Resolve "Foreign currency cluster risk EUR".  
  <sub>clients.json CASE-008: SuitabilityViolations[Id=893795]</sub>

</details>

---

## CASE-009 — Dorothy Gale

Investor profile 5 · CHF 665k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Dorothy Gale, Investor profile 5, CHF 665k across 1 portfolio.  
   <sub>clients.json CASE-009: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +25.9% over the 12 months to Jul 2026 and +15.5% since Oct 2021, now CHF 665k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-009: PerformanceHistory of CASE-009-01</sub>
3. **Health check.** Risk profile last assessed 5 Sep 2022, 4 years ago.  
   <sub>clients.json CASE-009: ProfilingDateUtc</sub>
4. **Watch.** Financials is 94.3% of the book (CHF 627k) after fund look-through, mostly via VZ Holding AG.  
   <sub>clients.json CASE-009: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
5. **Watch.** VZ Holding AG alone is 94.3% of the book.  
   <sub>clients.json CASE-009: Portfolios[CASE-009-01].SecurityPositions</sub>
6. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-009: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Dorothy Gale is calling: Investor profile 5, CHF 665k across 1 portfolio.  
   <sub>clients.json CASE-009: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 6k today, −0.9% of the book. Mostly Financials, −0.9% on 94.3% of it.  
   <sub>impact of the market feed on clients.json CASE-009 holdings</sub>
3. **digest.** About −CHF 6k today, −0.9% of the book.  
   <sub>impact of the market feed on clients.json CASE-009 holdings</sub>
4. **digest.** About −CHF 6k from Financials, −0.9% today on 94.3% of the book, mostly VZ Holding AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-009 holdings</sub>
5. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
6. **digest.** About −CHF 49 from the dollar, −1.2% against the franc on 0.6% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-009 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.15): Note from 2 May 2025: "Mentioned a possible change of address next year; account details to be confirmed then."  
  <sub>clients.json CASE-009: ClientNotes</sub>
- **Watch** (0.10): Note from 3 Mar 2025: "Open to increasing the equity allocation if markets remain stable."  
  <sub>clients.json CASE-009: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Account / Custody (CASE-009-01): expected return 6.4%, value at risk 21.2%.  
  <sub>clients.json CASE-009: Portfolios[CASE-009-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 34k, 5.1% of the book.  
  <sub>clients.json CASE-009: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 94.3% of the portfolio (CHF 627k).  
  <sub>clients.json CASE-009: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 5.1% of the portfolio (CHF 34k).  
  <sub>clients.json CASE-009: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 0.6% of the portfolio (CHF 4k).  
  <sub>clients.json CASE-009: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 94.3% of the portfolio (CHF 627k) after fund look-through.  
  <sub>clients.json CASE-009: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 99.4% of the portfolio (CHF 661k).  
  <sub>clients.json CASE-009: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 0.6% of the portfolio (CHF 4k).  
  <sub>clients.json CASE-009: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: VZ Holding AG, CHF 627k (94.3% of the portfolio).  
  <sub>clients.json CASE-009: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 2 holdings; the largest: VZ Holding AG (CHF 627k), FIM Long-Invest Portfolio Ltd (CHF 4k).  
  <sub>clients.json CASE-009: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-010 — Son Goku

Investor profile 5 · CHF 371k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Son Goku, Investor profile 5, ESG preference, CHF 371k across 1 portfolio.  
   <sub>clients.json CASE-010: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +25.2% over the 12 months to Jul 2026 and +92.9% since Oct 2021, now CHF 371k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-010: PerformanceHistory of CASE-010-01</sub>
3. **Health check.** Risk profile last assessed 12 Oct 2022, 4 years ago.  
   <sub>clients.json CASE-010: ProfilingDateUtc</sub>
4. **Health check.** ESG client: average sustainability score 7.8 of 10 against a minimum of 5.7; 1 holding below the per-position minimum (Sandoz Group AG, 4.2% of the book).  
   <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-010 positions</sub>
5. **Watch.** Novartis AG drives 86.5% of the volatility of Account / Custody (CASE-010-01).  
   <sub>clients.json CASE-010: Portfolios[CASE-010-01].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Health Care is 80.1% of the book (CHF 297k) after fund look-through, mostly via Novartis AG and Alcon AG.  
   <sub>clients.json CASE-010: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** News (CNBC Finance, 18 Sep): "Stocks making the biggest moves premarket: Netflix, Nucor, Xenon Pharmaceuticals & more"  
   <sub>CNBC Finance: https://www.cnbc.com/2026/09/18/stocks-making-the-biggest-moves-premarket-nflx-nue-xene.html</sub>
8. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-010: Proposals</sub>
9. **Next best actions.** Deploy idle liquidity: 19.9% of the book (CHF 74k) is cash.  
   <sub>clients.json CASE-010: LiquidityInDefaultCurrency</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Son Goku is calling: Investor profile 5, ESG preference, CHF 371k across 1 portfolio.  
   <sub>clients.json CASE-010: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: calm temperament, wants it detailed. From the notes: "Comfortable with higher volatility given a long time horizon."  
   <sub>data/profiles/profiles.json CASE-010 (apertus) from clients.json ClientNotes</sub>
3. **reason.** Probably a sustainability concern: ESG client: average sustainability score 7.8 of 10 against a minimum of 5.7; 1 holding below the per-position minimum (Sandoz Group AG, 4.2% of the book).  
   <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-010 positions</sub>
4. **reason.** Possibly idle cash: 19.9% of the book (CHF 74k) is cash.  
   <sub>clients.json CASE-010: LiquidityInDefaultCurrency</sub>
5. **digest.** About −CHF 1k today, −0.3% of the book.  
   <sub>impact of the market feed on clients.json CASE-010 holdings</sub>
6. **digest.** About −CHF 1k from Health Care, −0.4% today on 80.1% of the book, mostly Novartis AG and Alcon AG.  
   <sub>market feed "tech-selloff": S5HLTH Index CHG_PCT_1D × clients.json CASE-010 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.08): Volatility is 12.8%, above the 12.0% maximum of Investor profile 5.  
  <sub>clients.json CASE-010: Portfolios[CASE-010-01].Volatility; reference.json RiskProfiles.MaxVola</sub>
- **Watch** (0.65): Novartis AG alone is 64.8% of the book.  
  <sub>clients.json CASE-010: Portfolios[CASE-010-01].SecurityPositions</sub>
- **Watch** (0.15): Note from 27 Apr 2026: "Wants as high a weighting of sustainable funds as possible at the next rebalancing."  
  <sub>clients.json CASE-010: ClientNotes</sub>
- **Watch** (0.11): Alcon AG alone is 11.2% of the book.  
  <sub>clients.json CASE-010: Portfolios[CASE-010-01].SecurityPositions</sub>
- **Watch** (0.10): Note from 16 Dec 2025: "Mentioned a possible change of address next year; account details to be confirmed then."  
  <sub>clients.json CASE-010: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Account / Custody (CASE-010-01), 3 Sep 2026: expected return 5.3%, value at risk 3.5%.  
  <sub>clients.json CASE-010: Portfolios[CASE-010-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 74k, 19.9% of the book.  
  <sub>clients.json CASE-010: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 80.1% of the portfolio (CHF 297k).  
  <sub>clients.json CASE-010: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 19.9% of the portfolio (CHF 74k).  
  <sub>clients.json CASE-010: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 80.1% of the portfolio (CHF 297k) after fund look-through.  
  <sub>clients.json CASE-010: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 371k).  
  <sub>clients.json CASE-010: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Novartis AG, CHF 240k (64.8% of the portfolio).  
  <sub>clients.json CASE-010: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 3 holdings; the largest: Novartis AG (CHF 240k), Alcon AG (CHF 41k), Sandoz Group AG (CHF 16k).  
  <sub>clients.json CASE-010: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.20): Candidates from the recommendation list for Shares: ABB Ltd and Kuehne + Nagel International AG (cash is above 10% of the book).  
  <sub>reference.json RecommendationLists "Recommendation list free assets", not held, CHF first, ordered by SustainabilityScore</sub>

</details>

---

## CASE-011 — Ellen Ripley

Investor profile 6 · CHF 101k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Ellen Ripley, Investor profile 6, CHF 101k across 1 portfolio.  
   <sub>clients.json CASE-011: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +22.0% over the 12 months to Jul 2026 and +28.1% since Oct 2021, now CHF 101k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-011: PerformanceHistory of CASE-011-01</sub>
3. **Health check.** Volatility is 60.6%, above the 15.0% maximum of Investor profile 6.  
   <sub>clients.json CASE-011: Portfolios[CASE-011-01].Volatility; reference.json RiskProfiles.MaxVola</sub>
4. **Health check.** Risk profile last assessed 5 Sep 2022, 4 years ago.  
   <sub>clients.json CASE-011: ProfilingDateUtc</sub>
5. **Watch.** SIG Group AG drives 92.4% of the volatility of Account / Custody (CASE-011-01).  
   <sub>clients.json CASE-011: Portfolios[CASE-011-01].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Industrials is 58.5% of the book (CHF 59k) after fund look-through, mostly via ABB Ltd and Rieter Holding AG.  
   <sub>clients.json CASE-011: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "The AI-driven capex boom, and the need for infrastructure to support it, should support the outlook for industrials, another sector on which we have an overweight stance."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
8. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-011: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Ellen Ripley is calling: Investor profile 6, CHF 101k across 1 portfolio.  
   <sub>clients.json CASE-011: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: wants it detailed. From the notes: "Asked for more detail on transaction fees at the next meeting."  
   <sub>data/profiles/profiles.json CASE-011 (apertus) from clients.json ClientNotes</sub>
3. **caller.** Contact preference: "Prefers email communication, hard to reach by phone"  
   <sub>data/profiles/profiles.json CASE-011 from clients.json ClientNotes</sub>
4. **reason.** Probably the market: about −CHF 1k today, −1.1% of the book. Mostly Industrials, −1.1% on 58.5% of it.  
   <sub>impact of the market feed on clients.json CASE-011 holdings</sub>
5. **digest.** About −CHF 1k today, −1.1% of the book.  
   <sub>impact of the market feed on clients.json CASE-011 holdings</sub>
6. **digest.** About −CHF 648 from Industrials, −1.1% today on 58.5% of the book, mostly ABB Ltd and Rieter Holding AG.  
   <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-011 holdings</sub>
7. **digest.** About −CHF 207 from the dollar, −1.2% against the franc on 17.1% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-011 holdings</sub>
8. **digest.** About −CHF 154 from Financials, −0.9% today on 16.9% of the book, mostly UBS Group AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-011 holdings</sub>
9. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.42): ABB Ltd alone is 41.9% of the book.  
  <sub>clients.json CASE-011: Portfolios[CASE-011-01].SecurityPositions</sub>
- **Watch** (0.17): Financials is 16.9% of the book (CHF 17k) after fund look-through, mostly via UBS Group AG.  
  <sub>clients.json CASE-011: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.17): UBS Group AG alone is 16.9% of the book.  
  <sub>clients.json CASE-011: Portfolios[CASE-011-01].SecurityPositions</sub>
- **Watch** (0.15): Note from 19 Oct 2025: "Succession planning within the company underway, contact person may change."  
  <sub>clients.json CASE-011: ClientNotes</sub>
- **Watch** (0.11): Galenica AG alone is 10.5% of the book.  
  <sub>clients.json CASE-011: Portfolios[CASE-011-01].SecurityPositions</sub>
- **Watch** (0.10): Note from 22 May 2025: "Prefers email communication, hard to reach by phone."  
  <sub>clients.json CASE-011: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Account / Custody (CASE-011-01), 3 Sep 2026: expected return 6.1%, value at risk 15.2%.  
  <sub>clients.json CASE-011: Portfolios[CASE-011-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 7k, 7.1% of the book.  
  <sub>clients.json CASE-011: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 92.7% of the portfolio (CHF 93k).  
  <sub>clients.json CASE-011: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 7.1% of the portfolio (CHF 7k).  
  <sub>clients.json CASE-011: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 0.2% of the portfolio (CHF 152).  
  <sub>clients.json CASE-011: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Industrials is 58.5% of the portfolio (CHF 59k) after fund look-through.  
  <sub>clients.json CASE-011: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 16.9% of the portfolio (CHF 17k) after fund look-through.  
  <sub>clients.json CASE-011: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 10.5% of the portfolio (CHF 11k) after fund look-through.  
  <sub>clients.json CASE-011: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 6.8% of the portfolio (CHF 7k) after fund look-through.  
  <sub>clients.json CASE-011: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 82.9% of the portfolio (CHF 84k).  
  <sub>clients.json CASE-011: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 17.1% of the portfolio (CHF 17k).  
  <sub>clients.json CASE-011: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: ABB Ltd, CHF 42k (41.9% of the portfolio).  
  <sub>clients.json CASE-011: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 9 holdings; the largest: ABB Ltd (CHF 42k), UBS Group AG (CHF 17k), Galenica AG (CHF 11k), SIG Group AG (CHF 7k).  
  <sub>clients.json CASE-011: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-012 — Company 001 AG

Investor profile 6 · CHF 44k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Company 001 AG, Investor profile 6, CHF 44k across 1 portfolio.  
   <sub>clients.json CASE-012: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +19.6% over the 12 months to Jul 2026 and +22.5% since Oct 2021, now CHF 44k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-012: PerformanceHistory of CASE-012-01</sub>
3. **Health check.** 13 suitability errors and 8 warnings open; most serious: "Volatility range exceeded (portfolio risk too high)".  
   <sub>clients.json CASE-012: SuitabilityViolations</sub>
4. **Health check.** Volatility is 18.4%, above the 15.0% maximum of Investor profile 6.  
   <sub>clients.json CASE-012: Portfolios[CASE-012-01].Volatility; reference.json RiskProfiles.MaxVola</sub>
5. **Watch.** Note from 20 Mar 2026: "Needs approximately CHF 15,000 in liquid funds for the Q1 tax payment."  
   <sub>clients.json CASE-012: ClientNotes</sub>
6. **Watch.** Alphabet Inc drives 35.2% of the volatility of Investment advisory (CASE-012-01).  
   <sub>clients.json CASE-012: Portfolios[CASE-012-01].SecurityPositions.ContributionVolatility</sub>
7. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "That means maintaining an overweight position in technology stocks."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
8. **Next best actions.** Resolve "Volatility range exceeded (portfolio risk too high)".  
   <sub>clients.json CASE-012: SuitabilityViolations[Id=171628]</sub>
9. **Next best actions.** Resolve "Foreign currency cluster risk USD".  
   <sub>clients.json CASE-012: SuitabilityViolations[Id=171630]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Company 001 AG is calling: Investor profile 6, CHF 44k across 1 portfolio.  
   <sub>clients.json CASE-012: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 2k today, −3.5% of the book. Mostly Information Technology, −4.8% on 23.7% of it.  
   <sub>impact of the market feed on clients.json CASE-012 holdings</sub>
3. **reason.** Possibly a withdrawal: note from 20 Mar 2026: "Needs approximately CHF 15,000 in liquid funds for the Q1 tax payment."  
   <sub>clients.json CASE-012: ClientNotes</sub>
4. **reason.** Possibly investing new money: a deposit was noted on 30 Aug 2026.  
   <sub>clients.json CASE-012: Proposals[25001].Reason</sub>
5. **digest.** About −CHF 2k today, −3.5% of the book.  
   <sub>impact of the market feed on clients.json CASE-012 holdings</sub>
6. **digest.** About −CHF 504 from Information Technology, −4.8% today on 23.7% of the book, mostly Apple Inc and ETF USD iShares III PLC- iShares Core MSCI World UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-012 holdings</sub>
7. **digest.** About −CHF 401 from the dollar, −1.2% against the franc on 75.3% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-012 holdings</sub>
8. **digest.** About −CHF 385 from Communication Services, −3.1% today on 28.0% of the book, mostly Alphabet Inc and ETF USD iShares III PLC- iShares Core MSCI World UCITS ETF.  
   <sub>market feed "tech-selloff": S5TELS Index CHG_PCT_1D × clients.json CASE-012 holdings</sub>
9. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
10. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
11. **holding.** Holding up today: Consumer Staples +0.3% (4.2% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × clients.json CASE-012 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.21): Risk profile last assessed 31 Jul 2022, 4 years ago.  
  <sub>clients.json CASE-012: ProfilingDateUtc</sub>
- **Health check** (0.15): 5 of 6 orders from the proposal of 30 Aug 2026 were forwarded with a warning.  
  <sub>clients.json CASE-012: Transactions[ProposalId=25001].ForwardState = 2</sub>
- **Health check** (0.00): "Volatility range exceeded (portfolio risk too high)" means: For retail clients with financial services Comprehensive investment advisory or discretionary mandate must be PF Vola < max SAA Vola.  
  <sub>clients.json CASE-012: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Foreign currency cluster risk USD" means: For private customers, the USD share should be < 35.5%.  
  <sub>clients.json CASE-012: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Cluster risk of a single financial instrument" means: For retail clients with financial services, comprehensive investment advisory or trx-based investment advisory must be single title share < x% (x varies with instrument type)  
  <sub>clients.json CASE-012: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.28): Communication Services is 28.0% of the book (CHF 12k) after fund look-through, mostly via Alphabet Inc and ETF USD iShares III PLC- iShares Core MSCI World UCITS ETF.  
  <sub>clients.json CASE-012: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.25): Alphabet Inc alone is 25.5% of the book.  
  <sub>clients.json CASE-012: Portfolios[CASE-012-01].SecurityPositions</sub>
- **Watch** (0.24): Information Technology is 23.7% of the book (CHF 11k) after fund look-through, mostly via Apple Inc and ETF USD iShares III PLC- iShares Core MSCI World UCITS ETF.  
  <sub>clients.json CASE-012: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.18): Apple Inc alone is 17.8% of the book.  
  <sub>clients.json CASE-012: Portfolios[CASE-012-01].SecurityPositions</sub>
- **Watch** (0.15): Amazon.Com Inc alone is 15.1% of the book.  
  <sub>clients.json CASE-012: Portfolios[CASE-012-01].SecurityPositions</sub>
- **Watch** (0.15): Note from 27 Aug 2026: "Was informed of the risks of structured products and explicitly accepts them."  
  <sub>clients.json CASE-012: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (30 Aug 2026, reason: New deposit received) ordered to sell Amazon.Com Inc, iShares Swiss Dividend ETF (CH) and 3 more.  
  <sub>clients.json CASE-012: Proposals[25001] × Transactions</sub>
- **Watch** (0.03): Risk engine for Investment advisory (CASE-012-01), 3 Sep 2026: expected return 6.5%, value at risk 20.8%.  
  <sub>clients.json CASE-012: Portfolios[CASE-012-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 328, 0.7% of the book.  
  <sub>clients.json CASE-012: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 99.3% of the portfolio (CHF 44k).  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 0.7% of the portfolio (CHF 328).  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Communication Services is 28.0% of the portfolio (CHF 12k) after fund look-through.  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 23.7% of the portfolio (CHF 11k) after fund look-through.  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 17.6% of the portfolio (CHF 8k) after fund look-through.  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 10.0% of the portfolio (CHF 4k) after fund look-through.  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 8.0% of the portfolio (CHF 4k) after fund look-through.  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 4.5% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 4.2% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 1.1% of the portfolio (CHF 494) after fund look-through.  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 1.0% of the portfolio (CHF 460) after fund look-through.  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.6% of the portfolio (CHF 254) after fund look-through.  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.5% of the portfolio (CHF 235) after fund look-through.  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): US-Dollar: 82.2% of the portfolio (CHF 36k).  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Swiss francs: 17.8% of the portfolio (CHF 8k).  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Alphabet Inc, CHF 11k (25.5% of the portfolio).  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 5 holdings; the largest: Alphabet Inc (CHF 11k), ETF USD iShares III PLC- iShares Core MSCI World UCITS ETF (CHF 11k), Apple Inc (CHF 8k), iShares Swiss Dividend ETF (CH) (CHF 8k).  
  <sub>clients.json CASE-012: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (1.00): Resolve "Cluster risk of a single financial instrument" on iShares Swiss Dividend ETF (CH).  
  <sub>clients.json CASE-012: SuitabilityViolations[Id=171637]</sub>
- **Next best actions** (0.21): Clear the warnings on the 5 flagged orders from the proposal of 30 Aug 2026.  
  <sub>clients.json CASE-012: Transactions[ProposalId=25001].ForwardState = 2</sub>

</details>

---

## CASE-013 — Thomas

Investor profile 4 · CHF 58k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Thomas, Investor profile 4, CHF 58k across 1 portfolio.  
   <sub>clients.json CASE-013: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +20.2% over the 12 months to Jul 2026 and +101.2% since Oct 2021, now CHF 58k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-013: PerformanceHistory of CASE-013-01</sub>
3. **Health check.** Risk profile last assessed 1 Oct 2022, 4 years ago.  
   <sub>clients.json CASE-013: ProfilingDateUtc</sub>
4. **Health check.** Volatility is 11.9%, above the 10.0% maximum of Investor profile 4.  
   <sub>clients.json CASE-013: Portfolios[CASE-013-01].Volatility; reference.json RiskProfiles.MaxVola</sub>
5. **Watch.** WWZ AG drives 85.8% of the volatility of Account / Custody (CASE-013-01).  
   <sub>clients.json CASE-013: Portfolios[CASE-013-01].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** WWZ AG alone is 68.4% of the book.  
   <sub>clients.json CASE-013: Portfolios[CASE-013-01].SecurityPositions</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-013: Proposals</sub>
9. **Next best actions.** Deploy idle liquidity: 19.2% of the book (CHF 11k) is cash.  
   <sub>clients.json CASE-013: LiquidityInDefaultCurrency</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Thomas is calling: Investor profile 4, CHF 58k across 1 portfolio.  
   <sub>clients.json CASE-013: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably idle cash: 19.2% of the book (CHF 11k) is cash.  
   <sub>clients.json CASE-013: LiquidityInDefaultCurrency</sub>
3. **digest.** About −CHF 46 today, −0.1% of the book.  
   <sub>impact of the market feed on clients.json CASE-013 holdings</sub>
4. **digest.** About −CHF 31 from Financials, −0.9% today on 6.0% of the book, mostly Helvetia Holding AG and VZ Holding AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-013 holdings</sub>
5. **digest.** About −CHF 14 from Industrials, −1.1% today on 2.3% of the book, mostly Daetwyler Holding AG and Stadler Rail AG.  
   <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-013 holdings</sub>
6. **digest.** 72.5% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-013 holdings without a mapped market move</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.04): 1 holding above the product risk class limit of Investor profile 4 (maximum 6): Daetwyler Holding AG, 1.8% of the book.  
  <sub>reference.json Securities.PRC vs RiskProfiles.MaxPRC; clients.json CASE-013 positions</sub>
- **Watch** (0.36): 72.5% of the book is in holdings on none of the bank's recommendation lists, largest WWZ AG and Stanserhorn-Bahn-Aktiengesellschaft.  
  <sub>reference.json Securities.InRecommendationList; clients.json CASE-013 positions</sub>
- **Watch** (0.15): Note from 19 Jun 2025: "Wants exposure limited to developed markets only, no emerging markets."  
  <sub>clients.json CASE-013: ClientNotes</sub>
- **Watch** (0.10): Note from 10 Oct 2024: "Was informed of the risks of structured products and explicitly accepts them."  
  <sub>clients.json CASE-013: ClientNotes</sub>
- **Watch** (0.06): Financials is 6.0% of the book (CHF 3k) after fund look-through, mostly via Helvetia Holding AG and VZ Holding AG.  
  <sub>clients.json CASE-013: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.03): Risk engine for Account / Custody (CASE-013-01), 3 Sep 2026: expected return 5.3%, value at risk 19.0%.  
  <sub>clients.json CASE-013: Portfolios[CASE-013-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.02): Industrials is 2.3% of the book (CHF 1k) after fund look-through, mostly via Daetwyler Holding AG and Stadler Rail AG.  
  <sub>clients.json CASE-013: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.00): 72.5% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-013: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 11k, 19.2% of the book.  
  <sub>clients.json CASE-013: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 80.8% of the portfolio (CHF 47k).  
  <sub>clients.json CASE-013: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 19.2% of the portfolio (CHF 11k).  
  <sub>clients.json CASE-013: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 6.0% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-013: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 2.3% of the portfolio (CHF 1k) after fund look-through.  
  <sub>clients.json CASE-013: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 58k).  
  <sub>clients.json CASE-013: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: WWZ AG, CHF 40k (68.4% of the portfolio).  
  <sub>clients.json CASE-013: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 6 holdings; the largest: WWZ AG (CHF 40k), Helvetia Holding AG (CHF 2k), Stanserhorn-Bahn-Aktiengesellschaft (CHF 2k), VZ Holding AG (CHF 1k).  
  <sub>clients.json CASE-013: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.20): Candidates from the recommendation list for Shares: ABB Ltd and Kuehne + Nagel International AG (cash is above 10% of the book).  
  <sub>reference.json RecommendationLists "Recommendation list free assets", not held, CHF first, ordered by SustainabilityScore</sub>

</details>

---

## CASE-014 — Katniss Everdeen

Investor profile 4 · CHF 109k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Katniss Everdeen, Investor profile 4, CHF 109k across 2 portfolios.  
   <sub>clients.json CASE-014: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Combined portfolio value +21.5% over the 12 months to Jul 2026 and +62.0% since Oct 2021, now CHF 109k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-014: PerformanceHistory of CASE-014-01, CASE-014-02</sub>
3. **Health check.** Volatility in Account / Custody (CASE-014-02) is 22.0%, above the 10.0% maximum of Investor profile 4.  
   <sub>clients.json CASE-014: Portfolios[CASE-014-02].Volatility; reference.json RiskProfiles.MaxVola</sub>
4. **Health check.** Risk profile last assessed 1 Oct 2022, 4 years ago.  
   <sub>clients.json CASE-014: ProfilingDateUtc</sub>
5. **Watch.** VZ Holding AG drives 99.9% of the volatility of Account / Custody (CASE-014-02).  
   <sub>clients.json CASE-014: Portfolios[CASE-014-02].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Financials is 67.5% of the book (CHF 74k) after fund look-through, mostly via VZ Holding AG.  
   <sub>clients.json CASE-014: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Deploy idle liquidity: 32.2% of the book (CHF 35k) is cash.  
   <sub>clients.json CASE-014: LiquidityInDefaultCurrency</sub>
9. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-014: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Katniss Everdeen is calling: Investor profile 4, CHF 109k across 2 portfolios.  
   <sub>clients.json CASE-014: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Contact preference: "Prefers not to be contacted during business hours on weekdays"  
   <sub>data/profiles/profiles.json CASE-014 from clients.json ClientNotes</sub>
3. **reason.** Probably the market: about −CHF 665 today, −0.6% of the book. Mostly Financials, −0.9% on 67.5% of it.  
   <sub>impact of the market feed on clients.json CASE-014 holdings</sub>
4. **reason.** Possibly idle cash: 32.2% of the book (CHF 35k) is cash.  
   <sub>clients.json CASE-014: LiquidityInDefaultCurrency</sub>
5. **digest.** About −CHF 665 today, −0.6% of the book.  
   <sub>impact of the market feed on clients.json CASE-014 holdings</sub>
6. **digest.** About −CHF 662 from Financials, −0.9% today on 67.5% of the book, mostly VZ Holding AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-014 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.68): VZ Holding AG alone is 67.5% of the book.  
  <sub>clients.json CASE-014: Portfolios[CASE-014-02].SecurityPositions</sub>
- **Watch** (0.15): Note from 16 Dec 2025: "Prefers not to be contacted during business hours on weekdays."  
  <sub>clients.json CASE-014: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Account / Custody (CASE-014-02), 3 Sep 2026: expected return 6.3%, value at risk 21.1%.  
  <sub>clients.json CASE-014: Portfolios[CASE-014-02].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Industrials is 0.3% of the book (CHF 307) after fund look-through, mostly via Stadler Rail AG.  
  <sub>clients.json CASE-014: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.00): Cash on hand is CHF 35k, 32.2% of the book.  
  <sub>clients.json CASE-014: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 67.8% of the portfolio (CHF 74k).  
  <sub>clients.json CASE-014: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 32.2% of the portfolio (CHF 35k).  
  <sub>clients.json CASE-014: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 67.5% of the portfolio (CHF 74k) after fund look-through.  
  <sub>clients.json CASE-014: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 0.3% of the portfolio (CHF 307) after fund look-through.  
  <sub>clients.json CASE-014: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 109k).  
  <sub>clients.json CASE-014: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: VZ Holding AG, CHF 74k (67.5% of the portfolio).  
  <sub>clients.json CASE-014: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 2 holdings; the largest: VZ Holding AG (CHF 74k), Stadler Rail AG (CHF 307).  
  <sub>clients.json CASE-014: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.20): Candidates from the recommendation list for Shares: ABB Ltd and Kuehne + Nagel International AG (cash is above 10% of the book).  
  <sub>reference.json RecommendationLists "Recommendation list free assets", not held, CHF first, ordered by SustainabilityScore</sub>

</details>

---

## CASE-015 — Porky Pig

Investor profile 6 · CHF 304k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Porky Pig, Investor profile 6, ESG preference, CHF 304k across 1 portfolio.  
   <sub>clients.json CASE-015: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +13.4% over the 12 months to Jul 2026 and +31.0% since Oct 2021, now CHF 304k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-015: PerformanceHistory of CASE-015-01</sub>
3. **Health check.** Volatility is 29.3%, above the 15.0% maximum of Investor profile 6.  
   <sub>clients.json CASE-015: Portfolios[CASE-015-01].Volatility; reference.json RiskProfiles.MaxVola</sub>
4. **Health check.** Risk profile last assessed 5 Sep 2022, 4 years ago.  
   <sub>clients.json CASE-015: ProfilingDateUtc</sub>
5. **Watch.** Edisun Power Europe AG drives 99.8% of the volatility of Account / Custody (CASE-015-01).  
   <sub>clients.json CASE-015: Portfolios[CASE-015-01].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Utilities is 88.1% of the book (CHF 268k) after fund look-through, mostly via Edisun Power Europe AG.  
   <sub>clients.json CASE-015: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "We therefore downgrade utilities to neutral."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
8. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-015: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Porky Pig is calling: Investor profile 6, ESG preference, CHF 304k across 1 portfolio.  
   <sub>clients.json CASE-015: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: anxious temperament. From the notes: "Very risk-averse since the last market downturn, prefers defensive positioning."  
   <sub>data/profiles/profiles.json CASE-015 (apertus) from clients.json ClientNotes</sub>
3. **caller.** Contact preference: "Prefers not to be contacted during business hours on weekdays"  
   <sub>data/profiles/profiles.json CASE-015 from clients.json ClientNotes</sub>
4. **digest.** About +CHF 1k today, +0.4% of the book.  
   <sub>impact of the market feed on clients.json CASE-015 holdings</sub>
5. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
6. **digest.** About −CHF 42 from the dollar, −1.2% against the franc on 1.1% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-015 holdings</sub>
7. **digest.** About −CHF 31 from Financials, −0.9% today on 1.1% of the book, mostly UBS Group AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-015 holdings</sub>
8. **holding.** Holding up today: Utilities +0.5% (88.1% of the book).  
   <sub>market feed "tech-selloff": S5UTIL Index CHG_PCT_1D × clients.json CASE-015 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): ESG client: average sustainability score 8.5 of 10 against a minimum of 5.7; 89.7% of the book has no score.  
  <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-015 positions</sub>
- **Watch** (0.88): Edisun Power Europe AG alone is 88.1% of the book.  
  <sub>clients.json CASE-015: Portfolios[CASE-015-01].SecurityPositions</sub>
- **Watch** (0.15): Note from 24 Sep 2025: "Prefers not to be contacted during business hours on weekdays."  
  <sub>clients.json CASE-015: ClientNotes</sub>
- **Watch** (0.10): Note from 8 Jan 2025: "Very risk-averse since the last market downturn, prefers defensive positioning."  
  <sub>clients.json CASE-015: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Account / Custody (CASE-015-01), 3 Sep 2026: expected return 6.0%, value at risk 53.1%.  
  <sub>clients.json CASE-015: Portfolios[CASE-015-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.01): Financials is 1.1% of the book (CHF 3k) after fund look-through, mostly via UBS Group AG.  
  <sub>clients.json CASE-015: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.00): Cash on hand is CHF 28k, 9.1% of the book.  
  <sub>clients.json CASE-015: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 90.9% of the portfolio (CHF 276k).  
  <sub>clients.json CASE-015: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 9.1% of the portfolio (CHF 28k).  
  <sub>clients.json CASE-015: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Utilities is 88.1% of the portfolio (CHF 268k) after fund look-through.  
  <sub>clients.json CASE-015: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 1.1% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-015: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 98.9% of the portfolio (CHF 300k).  
  <sub>clients.json CASE-015: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 1.1% of the portfolio (CHF 3k).  
  <sub>clients.json CASE-015: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Edisun Power Europe AG, CHF 268k (88.1% of the portfolio).  
  <sub>clients.json CASE-015: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 3 holdings; the largest: Edisun Power Europe AG (CHF 268k), Grand Resort Bad Ragaz AG (CHF 5k), UBS Group AG (CHF 3k).  
  <sub>clients.json CASE-015: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-016 — Holly Golightly

Investor profile 5 · CHF 364k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Holly Golightly, Investor profile 5, ESG preference, CHF 364k across 1 portfolio.  
   <sub>clients.json CASE-016: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +9.9% over the 12 months to Jul 2026 and −22.4% since Oct 2021, now CHF 364k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-016: PerformanceHistory of CASE-016-01</sub>
3. **Health check.** ESG client: average sustainability score 3.1 of 10 against a minimum of 5.7; 1 holding below the per-position minimum (VZ Holding AG, 58.6% of the book).  
   <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-016 positions</sub>
4. **Health check.** Risk profile last assessed 5 Oct 2022, 4 years ago.  
   <sub>clients.json CASE-016: ProfilingDateUtc</sub>
5. **Watch.** Financials is 58.6% of the book (CHF 213k) after fund look-through, mostly via VZ Holding AG.  
   <sub>clients.json CASE-016: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Watch.** VZ Holding AG alone is 58.6% of the book.  
   <sub>clients.json CASE-016: Portfolios[CASE-016-01].SecurityPositions</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-016: Proposals</sub>
9. **Next best actions.** Keep the 41.4% cash (CHF 151k) in view of the note from 12 Sep 2025: "Needs approximately CHF 15,000 in liquid funds for the Q1 tax payment."  
   <sub>clients.json CASE-016: LiquidityInDefaultCurrency, ClientNotes</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Holly Golightly is calling: Investor profile 5, ESG preference, CHF 364k across 1 portfolio.  
   <sub>clients.json CASE-016: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably a withdrawal: note from 25 Apr 2026: "Considering a charitable donation from the portfolio, details being clarified."  
   <sub>clients.json CASE-016: ClientNotes</sub>
3. **reason.** Possibly a sustainability concern: ESG client: average sustainability score 3.1 of 10 against a minimum of 5.7; 1 holding below the per-position minimum (VZ Holding AG, 58.6% of the book).  
   <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-016 positions</sub>
4. **reason.** Possibly the market: about −CHF 2k today, −0.5% of the book. Mostly Financials, −0.9% on 58.6% of it.  
   <sub>impact of the market feed on clients.json CASE-016 holdings</sub>
5. **digest.** About −CHF 2k today, −0.5% of the book.  
   <sub>impact of the market feed on clients.json CASE-016 holdings</sub>
6. **digest.** About −CHF 2k from Financials, −0.9% today on 58.6% of the book, mostly VZ Holding AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-016 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.50): Note from 12 Sep 2025: "Needs approximately CHF 15,000 in liquid funds for the Q1 tax payment."  
  <sub>clients.json CASE-016: ClientNotes</sub>
- **Watch** (0.15): Note from 25 Apr 2026: "Considering a charitable donation from the portfolio, details being clarified."  
  <sub>clients.json CASE-016: ClientNotes</sub>
- **Watch** (0.00): Cash on hand is CHF 151k, 41.4% of the book.  
  <sub>clients.json CASE-016: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 58.6% of the portfolio (CHF 213k).  
  <sub>clients.json CASE-016: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 41.4% of the portfolio (CHF 151k).  
  <sub>clients.json CASE-016: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 58.6% of the portfolio (CHF 213k) after fund look-through.  
  <sub>clients.json CASE-016: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 364k).  
  <sub>clients.json CASE-016: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: VZ Holding AG, CHF 213k (58.6% of the portfolio).  
  <sub>clients.json CASE-016: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 1 holdings; the largest: VZ Holding AG (CHF 213k).  
  <sub>clients.json CASE-016: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.20): Candidates from the recommendation list for Shares: ABB Ltd and Kuehne + Nagel International AG (cash is above 10% of the book).  
  <sub>reference.json RecommendationLists "Recommendation list free assets", not held, CHF first, ordered by SustainabilityScore</sub>

</details>

---

## CASE-017 — Hulk

Investor profile 6 · CHF 1.11m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Hulk, Investor profile 6, CHF 1.11m across 1 portfolio.  
   <sub>clients.json CASE-017: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +24.2% over the 12 months to Jul 2026 and +75.0% since Oct 2021, now CHF 1.11m; value change including deposits and withdrawals.  
   <sub>clients.json CASE-017: PerformanceHistory of CASE-017-01</sub>
3. **Health check.** 0 suitability errors and 2 warnings open; most serious: "Share is not part of the investment universe for individual shares and therefore not monitored." on American Dep.Share Repr 2 Shs -A- EHang Holdings Ltd.  
   <sub>clients.json CASE-017: SuitabilityViolations</sub>
4. **Health check.** 2 of 2 orders from the proposal of 19 Oct 2025 were forwarded with a warning.  
   <sub>clients.json CASE-017: Transactions[ProposalId=17977].ForwardState = 2</sub>
5. **Watch.** Health Care is 16.2% of the book (CHF 180k) after fund look-through, mostly via SPDR MSCI World Health Care UCITS ETF and Roche Holding AG.  
   <sub>clients.json CASE-017: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Watch.** Note from 19 Jul 2026: "Interested in structured products, initial consultation already held."  
   <sub>clients.json CASE-017: ClientNotes</sub>
7. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "That means maintaining an overweight position in technology stocks."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
8. **Next best actions.** Resolve "Share is not part of the investment universe for individual shares and therefore not monitored." on American Dep.Share Repr 2 Shs -A- EHang Holdings Ltd.  
   <sub>clients.json CASE-017: SuitabilityViolations[Id=397714]</sub>
9. **Next best actions.** Resolve "Underweight in the equity region "Asia/Pacific (ex Japan)"".  
   <sub>clients.json CASE-017: SuitabilityViolations[Id=608682]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Hulk is calling: Investor profile 6, CHF 1.11m across 1 portfolio.  
   <sub>clients.json CASE-017: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 15k today, −1.4% of the book. Mostly Information Technology, −4.8% on 11.3% of it.  
   <sub>impact of the market feed on clients.json CASE-017 holdings</sub>
3. **digest.** About −CHF 15k today, −1.4% of the book.  
   <sub>impact of the market feed on clients.json CASE-017 holdings</sub>
4. **digest.** About −CHF 6k from Information Technology, −4.8% today on 11.3% of the book, mostly iShares Automation & Robotics UCITS ETF and iShares NASDAQ 100 UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-017 holdings</sub>
5. **digest.** About −CHF 4k from the dollar, −1.2% against the franc on 27.2% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-017 holdings</sub>
6. **digest.** About −CHF 2k from Consumer Discretionary, −2.2% today on 6.5% of the book, mostly mobilezone holding ag and Amazon.Com Inc.  
   <sub>market feed "tech-selloff": S5COND Index CHG_PCT_1D × clients.json CASE-017 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** 5.5% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-017 holdings without a mapped market move</sub>
10. **holding.** Global Investment Grade Credit Fund and iShares MSCI World CHF Hedged UCITS ETF (Acc) and US Short Duration High Yield (11.2% of the book) are hedged to the franc, so the dollar move (−1.2%) does not reach them.  
   <sub>clients.json CASE-017: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>
11. **holding.** Holding up today: Swiss franc bonds +0.2% (12.8% of the book); Consumer Staples +0.3% (8.6% of the book); foreign bonds +0.3% (4.7% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-017 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): "Underweight in the equity region "Asia/Pacific (ex Japan)"" means: Underweight (+/- 5% of the benchmark’s SAA target) in the ‘Asia/Pacific (ex Japan)’ equity region  
  <sub>clients.json CASE-017: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.11): Information Technology is 11.3% of the book (CHF 125k) after fund look-through, mostly via iShares Automation & Robotics UCITS ETF and iShares NASDAQ 100 UCITS ETF.  
  <sub>clients.json CASE-017: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 21 Nov 2025: "No direct positions in fossil fuels, please."  
  <sub>clients.json CASE-017: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (19 Oct 2025, reason: Annual review meeting) ordered to sell Novartis AG and Swissquote Group Holding SA.  
  <sub>clients.json CASE-017: Proposals[17977] × Transactions</sub>
- **Watch** (0.05): Currency-hedged holdings: Global Investment Grade Credit Fund, iShares MSCI World CHF Hedged UCITS ETF (Acc), US Short Duration High Yield (11.2% of the book).  
  <sub>clients.json CASE-017: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Investment advisory (CASE-017-01), 3 Sep 2026: expected return 5.5%, value at risk 14.9%.  
  <sub>clients.json CASE-017: Portfolios[CASE-017-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 20.6% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-017: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 49k, 4.4% of the book.  
  <sub>clients.json CASE-017: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 72.6% of the portfolio (CHF 807k).  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 17.4% of the portfolio (CHF 194k).  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 4.4% of the portfolio (CHF 49k).  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 3.7% of the portfolio (CHF 41k).  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 1.9% of the portfolio (CHF 21k).  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 16.2% of the portfolio (CHF 180k) after fund look-through.  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 11.3% of the portfolio (CHF 125k) after fund look-through.  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 9.9% of the portfolio (CHF 110k) after fund look-through.  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 8.6% of the portfolio (CHF 95k) after fund look-through.  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 8.2% of the portfolio (CHF 91k) after fund look-through.  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 6.8% of the portfolio (CHF 75k) after fund look-through.  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 6.5% of the portfolio (CHF 72k) after fund look-through.  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 4.2% of the portfolio (CHF 47k) after fund look-through.  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 2.2% of the portfolio (CHF 24k) after fund look-through.  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 1.1% of the portfolio (CHF 13k) after fund look-through.  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.1% of the portfolio (CHF 1k) after fund look-through.  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 65.2% of the portfolio (CHF 724k).  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 30.2% of the portfolio (CHF 335k).  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 4.7% of the portfolio (CHF 52k).  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Crypto: CHF 8k, 0.8% of the portfolio.  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Nestle SA, CHF 69k (6.2% of the portfolio).  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 36 holdings; the largest: Nestle SA (CHF 69k), iShares MSCI World CHF Hedged UCITS ETF (Acc) (CHF 56k), SPDR MSCI World Health Care UCITS ETF (CHF 52k), iShares NASDAQ 100 UCITS ETF (CHF 52k).  
  <sub>clients.json CASE-017: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.25): Clear the warnings on the 2 flagged orders from the proposal of 19 Oct 2025.  
  <sub>clients.json CASE-017: Transactions[ProposalId=17977].ForwardState = 2</sub>

</details>

---

## CASE-018 — Company 002 AG

Investor profile 6 · CHF 3.10m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Company 002 AG, Investor profile 6, CHF 3.10m across 1 portfolio.  
   <sub>clients.json CASE-018: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +18.2% over the 12 months to Jul 2026 and +33.6% since Oct 2021, now CHF 3.10m; value change including deposits and withdrawals.  
   <sub>clients.json CASE-018: PerformanceHistory of CASE-018-01</sub>
3. **Health check.** 13 suitability errors and 6 warnings open; most serious: "Volatility range exceeded (portfolio risk too high)".  
   <sub>clients.json CASE-018: SuitabilityViolations</sub>
4. **Health check.** Volatility is 29.3%, above the 15.0% maximum of Investor profile 6.  
   <sub>clients.json CASE-018: Portfolios[CASE-018-01].Volatility; reference.json RiskProfiles.MaxVola</sub>
5. **Watch.** SIG Group AG drives 83.1% of the volatility of Depository advisory (CASE-018-01).  
   <sub>clients.json CASE-018: Portfolios[CASE-018-01].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Raw materials is 49.5% of the book (CHF 1.53m) after fund look-through, mostly via Linde PLC and Holcim AG.  
   <sub>clients.json CASE-018: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Resolve "Foreign currency cluster risk EUR".  
   <sub>clients.json CASE-018: SuitabilityViolations[Id=161414]</sub>
9. **Next best actions.** Resolve "Cluster risk of a single financial instrument" on Zurich Insurance Group AG.  
   <sub>clients.json CASE-018: SuitabilityViolations[Id=161420]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Company 002 AG is calling: Investor profile 6, CHF 3.10m across 1 portfolio.  
   <sub>clients.json CASE-018: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 22k today, −0.7% of the book. Mostly Raw materials, −0.6% on 49.5% of it.  
   <sub>impact of the market feed on clients.json CASE-018 holdings</sub>
3. **digest.** About −CHF 22k today, −0.7% of the book.  
   <sub>impact of the market feed on clients.json CASE-018 holdings</sub>
4. **digest.** About −CHF 9k from Raw materials, −0.6% today on 49.5% of the book, mostly Linde PLC and Holcim AG.  
   <sub>market feed "tech-selloff": S5MATR Index CHG_PCT_1D × clients.json CASE-018 holdings</sub>
5. **digest.** About −CHF 8k from Financials, −0.9% today on 28.5% of the book, mostly Zurich Insurance Group AG and Swiss Re AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-018 holdings</sub>
6. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
7. **digest.** About −CHF 3k from Industrials, −1.1% today on 8.2% of the book, mostly Geberit AG.  
   <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-018 holdings</sub>
8. **holding.** Holding up today: Consumer Staples +0.3% (4.5% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × clients.json CASE-018 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.21): Risk profile last assessed 31 Jul 2022, 4 years ago.  
  <sub>clients.json CASE-018: ProfilingDateUtc</sub>
- **Health check** (0.15): 1 of 1 order from the proposal of 23 Sep 2025 were forwarded with a warning.  
  <sub>clients.json CASE-018: Transactions[ProposalId=17405].ForwardState = 2</sub>
- **Health check** (0.00): "Foreign currency cluster risk EUR" means: For private customers, the EUR share should be < 9%.  
  <sub>clients.json CASE-018: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Cluster risk of a single financial instrument" means: For retail clients with financial services, comprehensive investment advisory or trx-based investment advisory must be single title share < x% (x varies with instrument type)  
  <sub>clients.json CASE-018: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Volatility range exceeded (portfolio risk too high)" means: For retail clients with financial services Comprehensive investment advisory or discretionary mandate must be PF Vola < max SAA Vola.  
  <sub>clients.json CASE-018: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.28): Financials is 28.5% of the book (CHF 883k) after fund look-through, mostly via Zurich Insurance Group AG and Swiss Re AG.  
  <sub>clients.json CASE-018: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.23): Linde PLC alone is 22.5% of the book.  
  <sub>clients.json CASE-018: Portfolios[CASE-018-01].SecurityPositions</sub>
- **Watch** (0.15): Holcim AG alone is 15.3% of the book.  
  <sub>clients.json CASE-018: Portfolios[CASE-018-01].SecurityPositions</sub>
- **Watch** (0.15): Note from 15 Nov 2024: "Also manages a family member's portfolio under a power of attorney."  
  <sub>clients.json CASE-018: ClientNotes</sub>
- **Watch** (0.15): Zurich Insurance Group AG alone is 14.6% of the book.  
  <sub>clients.json CASE-018: Portfolios[CASE-018-01].SecurityPositions</sub>
- **Watch** (0.14): Swiss Re AG alone is 13.8% of the book.  
  <sub>clients.json CASE-018: Portfolios[CASE-018-01].SecurityPositions</sub>
- **Watch** (0.08): The last finalised proposal (23 Sep 2025, reason: Change of investment strategy) ordered to buy Geberit AG.  
  <sub>clients.json CASE-018: Proposals[17405] × Transactions</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-018-01), 3 Sep 2026: expected return 5.9%, value at risk 5.2%.  
  <sub>clients.json CASE-018: Portfolios[CASE-018-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 292k, 9.4% of the book.  
  <sub>clients.json CASE-018: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 90.6% of the portfolio (CHF 2.81m).  
  <sub>clients.json CASE-018: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 9.4% of the portfolio (CHF 292k).  
  <sub>clients.json CASE-018: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Raw materials is 49.5% of the portfolio (CHF 1.53m) after fund look-through.  
  <sub>clients.json CASE-018: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 28.5% of the portfolio (CHF 883k) after fund look-through.  
  <sub>clients.json CASE-018: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 8.2% of the portfolio (CHF 254k) after fund look-through.  
  <sub>clients.json CASE-018: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 4.5% of the portfolio (CHF 139k) after fund look-through.  
  <sub>clients.json CASE-018: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 77.2% of the portfolio (CHF 2.40m).  
  <sub>clients.json CASE-018: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 22.5% of the portfolio (CHF 698k).  
  <sub>clients.json CASE-018: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 0.2% of the portfolio (CHF 8k).  
  <sub>clients.json CASE-018: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Linde PLC, CHF 698k (22.5% of the portfolio).  
  <sub>clients.json CASE-018: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 8 holdings; the largest: Linde PLC (CHF 698k), Holcim AG (CHF 476k), Zurich Insurance Group AG (CHF 454k), Swiss Re AG (CHF 430k).  
  <sub>clients.json CASE-018: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (1.00): Resolve "Cluster risk of a single financial instrument" on Holcim AG.  
  <sub>clients.json CASE-018: SuitabilityViolations[Id=161421]</sub>

</details>

---

## CASE-019 — Pikachu

Investor profile 7 · CHF 699k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Pikachu, Investor profile 7, CHF 699k across 1 portfolio.  
   <sub>clients.json CASE-019: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +24.0% over the 12 months to Jul 2026 and +45.0% since Oct 2021, now CHF 699k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-019: PerformanceHistory of CASE-019-01</sub>
3. **Health check.** 7 suitability errors and 6 warnings open; most serious: "Significant overweight in the equity region "Switzerland"".  
   <sub>clients.json CASE-019: SuitabilityViolations</sub>
4. **Health check.** Risk profile last assessed 20 Aug 2023, 3 years ago.  
   <sub>clients.json CASE-019: ProfilingDateUtc</sub>
5. **Watch.** Note from 4 Sep 2026: "Prefers to keep a cash reserve on hand for unexpected medical expenses."  
   <sub>clients.json CASE-019: ClientNotes</sub>
6. **Watch.** Comet Holding AG drives 48.6% of the volatility of Depository advisory (CASE-019-01).  
   <sub>clients.json CASE-019: Portfolios[CASE-019-01].SecurityPositions.ContributionVolatility</sub>
7. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "That means maintaining an overweight position in technology stocks."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
8. **Next best actions.** Resolve "Cluster risk of a single financial instrument" on Nestle SA.  
   <sub>clients.json CASE-019: SuitabilityViolations[Id=200558]</sub>
9. **Next best actions.** Resolve "Cluster risk of a single financial instrument" on Comet Holding AG.  
   <sub>clients.json CASE-019: SuitabilityViolations[Id=200559]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Pikachu is calling: Investor profile 7, CHF 699k across 1 portfolio.  
   <sub>clients.json CASE-019: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Contact preference: "Hard to reach during the day, best contacted after 6pm"  
   <sub>data/profiles/profiles.json CASE-019 from clients.json ClientNotes</sub>
3. **reason.** Probably the market: about −CHF 12k today, −1.7% of the book. Mostly Information Technology, −4.8% on 26.0% of it.  
   <sub>impact of the market feed on clients.json CASE-019 holdings</sub>
4. **reason.** Possibly a withdrawal: note from 15 Aug 2025: "Considering a charitable donation from the portfolio, details being clarified."  
   <sub>clients.json CASE-019: ClientNotes</sub>
5. **digest.** About −CHF 12k today, −1.7% of the book.  
   <sub>impact of the market feed on clients.json CASE-019 holdings</sub>
6. **digest.** About −CHF 9k from Information Technology, −4.8% today on 26.0% of the book, mostly Comet Holding AG and Global Clean Energy UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-019 holdings</sub>
7. **digest.** About −CHF 1k from the dollar, −1.2% against the franc on 17.2% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-019 holdings</sub>
8. **digest.** About −CHF 987 from Health Care, −0.4% today on 35.3% of the book, mostly Ypsomed Holding AG and Roche Holding AG.  
   <sub>market feed "tech-selloff": S5HLTH Index CHG_PCT_1D × clients.json CASE-019 holdings</sub>
9. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
10. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
11. **holding.** Holding up today: Consumer Staples +0.3% (9.6% of the book); Utilities +0.5% (5.3% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × clients.json CASE-019 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): "Cluster risk of a single financial instrument" means: For retail clients with financial services, comprehensive investment advisory or trx-based investment advisory must be single title share < x% (x varies with instrument type)  
  <sub>clients.json CASE-019: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Significant overweight in the equity region "Switzerland"" means: Significant overweight (+/- 10% of the benchmark’s SAA target) in the ‘Switzerland’ equity region  
  <sub>clients.json CASE-019: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Significant underweight in the equity region "North America"" means: Significant underweight (+/- 10% of the SAA target for the ‘North America’ equity region)  
  <sub>clients.json CASE-019: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.35): Health Care is 35.3% of the book (CHF 247k) after fund look-through, mostly via Ypsomed Holding AG and Roche Holding AG.  
  <sub>clients.json CASE-019: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.26): Information Technology is 26.0% of the book (CHF 182k) after fund look-through, mostly via Comet Holding AG and Global Clean Energy UCITS ETF.  
  <sub>clients.json CASE-019: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.22): Comet Holding AG alone is 21.9% of the book.  
  <sub>clients.json CASE-019: Portfolios[CASE-019-01].SecurityPositions</sub>
- **Watch** (0.16): Ypsomed Holding AG alone is 15.5% of the book.  
  <sub>clients.json CASE-019: Portfolios[CASE-019-01].SecurityPositions</sub>
- **Watch** (0.10): Note from 8 Jun 2026: "Hard to reach during the day, best contacted after 6pm."  
  <sub>clients.json CASE-019: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (21 Aug 2023, reason: Tax year-end rebalancing) ordered to buy Underlying Tracker Bk Vontobel 2020-open end o/SOLVALOR HYDROGEN TOP SEL and Underlying Tracker Vontobel Financial Products Ltd 2017-open end on Sol.Battery Energy Storage Perf..  
  <sub>clients.json CASE-019: Proposals[1960] × Transactions</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-019-01), 3 Sep 2026: expected return 6.5%, value at risk 19.4%.  
  <sub>clients.json CASE-019: Portfolios[CASE-019-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 4k, 0.6% of the book.  
  <sub>clients.json CASE-019: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 96.1% of the portfolio (CHF 671k).  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 3.4% of the portfolio (CHF 24k).  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 0.6% of the portfolio (CHF 4k).  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 35.3% of the portfolio (CHF 247k) after fund look-through.  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 26.0% of the portfolio (CHF 182k) after fund look-through.  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 9.6% of the portfolio (CHF 67k) after fund look-through.  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 8.5% of the portfolio (CHF 59k) after fund look-through.  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 7.3% of the portfolio (CHF 51k) after fund look-through.  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 5.3% of the portfolio (CHF 37k) after fund look-through.  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 2.3% of the portfolio (CHF 16k) after fund look-through.  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 0.7% of the portfolio (CHF 5k) after fund look-through.  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 0.3% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.2% of the portfolio (CHF 1k) after fund look-through.  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.1% of the portfolio (CHF 459) after fund look-through.  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 74.6% of the portfolio (CHF 522k).  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 25.4% of the portfolio (CHF 177k).  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Comet Holding AG, CHF 153k (21.9% of the portfolio).  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 20 holdings; the largest: Comet Holding AG (CHF 153k), Ypsomed Holding AG (CHF 109k), Nestle SA (CHF 65k), Roche Holding AG (CHF 47k).  
  <sub>clients.json CASE-019: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (1.00): Resolve "Cluster risk of a single financial instrument" on Ypsomed Holding AG.  
  <sub>clients.json CASE-019: SuitabilityViolations[Id=285004]</sub>
- **Next best actions** (0.40): Book a review: the last finalised proposal was on 21 Aug 2023.  
  <sub>clients.json CASE-019: Proposals.FinalizedDateUTC</sub>

</details>

---

## CASE-020 — Tom Joad

Investor profile 4 · CHF 486k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Tom Joad, Investor profile 4, CHF 486k across 1 portfolio.  
   <sub>clients.json CASE-020: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +9.3% over the 12 months to Jul 2026 and −18.9% since Oct 2021, now CHF 486k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-020: PerformanceHistory of CASE-020-01</sub>
3. **Health check.** 1 suitability error and 0 warnings open; most serious: "Volatility range undershot (portfolio risk too low)".  
   <sub>clients.json CASE-020: SuitabilityViolations</sub>
4. **Health check.** Risk profile last assessed 31 Jul 2022, 4 years ago.  
   <sub>clients.json CASE-020: ProfilingDateUtc</sub>
5. **Watch.** SMI (R) drives 20.1% of the volatility of Investment advisory (CASE-020-01).  
   <sub>clients.json CASE-020: Portfolios[CASE-020-01].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Note from 14 Apr 2026: "Mentioned a possible change of address next year; account details to be confirmed then."  
   <sub>clients.json CASE-020: ClientNotes</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Resolve "Volatility range undershot (portfolio risk too low)".  
   <sub>clients.json CASE-020: SuitabilityViolations[Id=843572]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Tom Joad is calling: Investor profile 4, CHF 486k across 1 portfolio.  
   <sub>clients.json CASE-020: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably a withdrawal: note from 18 May 2025: "Expects an inheritance in the coming years, strategy to be reviewed at that point."  
   <sub>clients.json CASE-020: ClientNotes</sub>
3. **reason.** Possibly the market: about −CHF 4k today, −0.8% of the book. Mostly the dollar, −1.2% on 31.8% of it.  
   <sub>impact of the market feed on clients.json CASE-020 holdings</sub>
4. **digest.** About −CHF 4k today, −0.8% of the book.  
   <sub>impact of the market feed on clients.json CASE-020 holdings</sub>
5. **digest.** About −CHF 2k from the dollar, −1.2% against the franc on 31.8% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-020 holdings</sub>
6. **digest.** About −CHF 977 from Information Technology, −4.8% today on 4.2% of the book, mostly iShares MSCI World Minimum Volatility UCITS ETF and MSCI USA Select Factor Mix UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-020 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** About −CHF 416 from Communication Services, −3.1% today on 2.8% of the book, mostly iShares MSCI World Minimum Volatility UCITS ETF and CSIF (CH) Equity SPI ESG Multi Premia Blue.  
   <sub>market feed "tech-selloff": S5TELS Index CHG_PCT_1D × clients.json CASE-020 holdings</sub>
10. **holding.** SPDR Bloomberg Global Aggregate Bond UCITS ETF (5.6% of the book) is hedged to the franc, so the dollar move (−1.2%) does not reach it.  
   <sub>clients.json CASE-020: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>
11. **holding.** Holding up today: Swiss franc bonds +0.2% (31.4% of the book); foreign bonds +0.3% (12.5% of the book); Consumer Staples +0.3% (5.8% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-020 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.13): Health Care is 12.5% of the book (CHF 61k) after fund look-through, mostly via SMI (R) and MIV Global Medtech Fund.  
  <sub>clients.json CASE-020: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 3 Jul 2025: "Wants to invest more heavily in Swiss small caps going forward."  
  <sub>clients.json CASE-020: ClientNotes</sub>
- **Watch** (0.08): Financials is 7.9% of the book (CHF 38k) after fund look-through, mostly via SMI (R) and CSIF (CH) Equity SPI ESG Multi Premia Blue.  
  <sub>clients.json CASE-020: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.05): Currency-hedged holdings: SPDR Bloomberg Global Aggregate Bond UCITS ETF (5.6% of the book).  
  <sub>clients.json CASE-020: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Investment advisory (CASE-020-01), 3 Sep 2026: expected return 4.2%, value at risk 11.2%.  
  <sub>clients.json CASE-020: Portfolios[CASE-020-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 43.9% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-020: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 30k, 6.2% of the book.  
  <sub>clients.json CASE-020: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 49.9% of the portfolio (CHF 242k).  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 43.9% of the portfolio (CHF 213k).  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 6.2% of the portfolio (CHF 30k).  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 12.5% of the portfolio (CHF 61k) after fund look-through.  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 7.9% of the portfolio (CHF 38k) after fund look-through.  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 7.1% of the portfolio (CHF 34k) after fund look-through.  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 5.8% of the portfolio (CHF 28k) after fund look-through.  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 4.2% of the portfolio (CHF 20k) after fund look-through.  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 3.0% of the portfolio (CHF 15k) after fund look-through.  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 2.8% of the portfolio (CHF 14k) after fund look-through.  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 2.8% of the portfolio (CHF 13k) after fund look-through.  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 1.9% of the portfolio (CHF 9k) after fund look-through.  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 1.1% of the portfolio (CHF 5k) after fund look-through.  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.7% of the portfolio (CHF 4k) after fund look-through.  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 61.8% of the portfolio (CHF 300k).  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 35.0% of the portfolio (CHF 170k).  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 3.2% of the portfolio (CHF 15k).  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares MSCI World Minimum Volatility UCITS ETF, CHF 56k (11.4% of the portfolio).  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 15 holdings; the largest: iShares MSCI World Minimum Volatility UCITS ETF (CHF 56k), SMI (R) (CHF 55k), CSIF (CH) Equity SPI ESG Multi Premia Blue (CHF 46k), Credit Suisse (CH) Corporate CHF Bond Fund (CHF 46k).  
  <sub>clients.json CASE-020: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-021 — Holden Caulfield

Investor profile 3 · CHF 759k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Holden Caulfield, Investor profile 3, CHF 759k across 2 portfolios.  
   <sub>clients.json CASE-021: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Combined portfolio value +29.0% over the 12 months to Jul 2026 and +54.1% since Oct 2021, now CHF 759k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-021: PerformanceHistory of CASE-021-01, CASE-021-02</sub>
3. **Health check.** Volatility in Account / Custody (CASE-021-01) is 21.6%, above the 7.5% maximum of Investor profile 3.  
   <sub>clients.json CASE-021: Portfolios[CASE-021-01].Volatility; reference.json RiskProfiles.MaxVola</sub>
4. **Health check.** 1 holding above the product risk class limit of Investor profile 3 (maximum 4): VZ Holding AG, 65.8% of the book.  
   <sub>reference.json Securities.PRC vs RiskProfiles.MaxPRC; clients.json CASE-021 positions</sub>
5. **Watch.** VZ Holding AG drives 100.0% of the volatility of Account / Custody (CASE-021-01).  
   <sub>clients.json CASE-021: Portfolios[CASE-021-01].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Financials is 65.8% of the book (CHF 500k) after fund look-through, mostly via VZ Holding AG.  
   <sub>clients.json CASE-021: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Deploy idle liquidity: 34.2% of the book (CHF 259k) is cash.  
   <sub>clients.json CASE-021: LiquidityInDefaultCurrency</sub>
9. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-021: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Holden Caulfield is calling: Investor profile 3, CHF 759k across 2 portfolios.  
   <sub>clients.json CASE-021: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Contact preference: "Would like a follow-up call before any changes to the standing order"  
   <sub>data/profiles/profiles.json CASE-021 from clients.json ClientNotes</sub>
3. **reason.** Probably a withdrawal: note from 2 Nov 2025: "Considering a charitable donation from the portfolio, details being clarified."  
   <sub>clients.json CASE-021: ClientNotes</sub>
4. **reason.** Possibly the market: about −CHF 4k today, −0.6% of the book. Mostly Financials, −0.9% on 65.8% of it.  
   <sub>impact of the market feed on clients.json CASE-021 holdings</sub>
5. **digest.** About −CHF 4k today, −0.6% of the book.  
   <sub>impact of the market feed on clients.json CASE-021 holdings</sub>
6. **digest.** About −CHF 4k from Financials, −0.9% today on 65.8% of the book, mostly VZ Holding AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-021 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.20): Risk profile last assessed 5 Oct 2022, 4 years ago.  
  <sub>clients.json CASE-021: ProfilingDateUtc</sub>
- **Watch** (0.66): VZ Holding AG alone is 65.8% of the book.  
  <sub>clients.json CASE-021: Portfolios[CASE-021-01].SecurityPositions</sub>
- **Watch** (0.15): Note from 22 Nov 2025: "Wants to invest more heavily in Swiss small caps going forward."  
  <sub>clients.json CASE-021: ClientNotes</sub>
- **Watch** (0.10): Note from 20 Nov 2025: "Would like a follow-up call before any changes to the standing order."  
  <sub>clients.json CASE-021: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Account / Custody (CASE-021-01), 3 Sep 2026: expected return 6.2%, value at risk 20.7%.  
  <sub>clients.json CASE-021: Portfolios[CASE-021-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 259k, 34.2% of the book.  
  <sub>clients.json CASE-021: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 65.8% of the portfolio (CHF 500k).  
  <sub>clients.json CASE-021: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 34.2% of the portfolio (CHF 259k).  
  <sub>clients.json CASE-021: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 65.8% of the portfolio (CHF 500k) after fund look-through.  
  <sub>clients.json CASE-021: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 759k).  
  <sub>clients.json CASE-021: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: VZ Holding AG, CHF 500k (65.8% of the portfolio).  
  <sub>clients.json CASE-021: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 1 holdings; the largest: VZ Holding AG (CHF 500k).  
  <sub>clients.json CASE-021: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.20): Candidates from the recommendation list for Shares: ABB Ltd and Kuehne + Nagel International AG (cash is above 10% of the book).  
  <sub>reference.json RecommendationLists "Recommendation list free assets", not held, CHF first, ordered by SustainabilityScore</sub>

</details>

---

## CASE-022 — Company 003 AG

Investor profile 5 · CHF 6.38m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Company 003 AG, Investor profile 5, CHF 6.38m across 1 portfolio.  
   <sub>clients.json CASE-022: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +19.1% over the 12 months to Jul 2026 and +69.9% since Oct 2021, now CHF 6.38m; value change including deposits and withdrawals.  
   <sub>clients.json CASE-022: PerformanceHistory of CASE-022-01</sub>
3. **Health check.** 6 suitability errors and 7 warnings open; most serious: "Significant overweight in the equity sector "Materials"".  
   <sub>clients.json CASE-022: SuitabilityViolations</sub>
4. **Health check.** 14 of 14 orders from the proposal of 5 Oct 2025 were forwarded with a warning.  
   <sub>clients.json CASE-022: Transactions[ProposalId=17579].ForwardState = 2</sub>
5. **Watch.** Note from 26 Nov 2024: "Expects an inheritance in the coming years, strategy to be reviewed at that point."  
   <sub>clients.json CASE-022: ClientNotes</sub>
6. **Watch.** Financials is 19.3% of the book (CHF 1.23m) after fund look-through, mostly via Swiss Re AG and Zurich Insurance Group AG.  
   <sub>clients.json CASE-022: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Resolve "Foreign currency cluster risk EUR".  
   <sub>clients.json CASE-022: SuitabilityViolations[Id=315680]</sub>
9. **Next best actions.** Resolve "Cluster risk of a single financial instrument" on Holcim AG.  
   <sub>clients.json CASE-022: SuitabilityViolations[Id=584357]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Company 003 AG is calling: Investor profile 5, CHF 6.38m across 1 portfolio.  
   <sub>clients.json CASE-022: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 63k today, −1.0% of the book. Mostly Information Technology, −4.8% on 6.9% of it.  
   <sub>impact of the market feed on clients.json CASE-022 holdings</sub>
3. **reason.** Possibly reinvestment: RC Notes Lehman Brothers Treasury Bv 2006-12.5.09 on Zurich Insur Grp Shs -In Default- matures on 19 Sep 2026 (CHF 0).  
   <sub>clients.json CASE-022: SecurityPositions × reference.json Securities.MaturityDateUtc</sub>
4. **reason.** Possibly idle cash: 14.7% of the book (CHF 939k) is cash.  
   <sub>clients.json CASE-022: LiquidityInDefaultCurrency</sub>
5. **digest.** About −CHF 63k today, −1.0% of the book.  
   <sub>impact of the market feed on clients.json CASE-022 holdings</sub>
6. **digest.** About −CHF 21k from Information Technology, −4.8% today on 6.9% of the book, mostly Apple Inc and Logitech International SA.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-022 holdings</sub>
7. **digest.** About −CHF 11k from Financials, −0.9% today on 19.3% of the book, mostly Swiss Re AG and Zurich Insurance Group AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-022 holdings</sub>
8. **digest.** About −CHF 11k from Industrials, −1.1% today on 15.3% of the book, mostly ABB Ltd and SGS Ltd.  
   <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-022 holdings</sub>
9. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
10. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
11. **holding.** Holding up today: Consumer Staples +0.3% (5.5% of the book); Utilities +0.5% (5.5% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × clients.json CASE-022 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.11): Risk profile last assessed 12 Aug 2023, 3 years ago.  
  <sub>clients.json CASE-022: ProfilingDateUtc</sub>
- **Health check** (0.00): "Foreign currency cluster risk EUR" means: For private customers, the EUR share should be < 9%.  
  <sub>clients.json CASE-022: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Cluster risk of a single financial instrument" means: For retail clients with financial services, comprehensive investment advisory or trx-based investment advisory must be single title share < x% (x varies with instrument type)  
  <sub>clients.json CASE-022: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Significant overweight in the equity region "Switzerland"" means: Significant overweight (+/- 10% of the benchmark’s SAA target) in the ‘Switzerland’ equity region  
  <sub>clients.json CASE-022: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.15): Industrials is 15.3% of the book (CHF 978k) after fund look-through, mostly via ABB Ltd and SGS Ltd.  
  <sub>clients.json CASE-022: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.08): The last finalised proposal (5 Oct 2025, reason: Life event (retirement)) ordered to buy ABB Ltd, Allianz SE and 7 more and sell iShares DivDAX (R) UCITS ETF (DE), BB Biotech AG and 3 more.  
  <sub>clients.json CASE-022: Proposals[17579] × Transactions</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-022-01), 3 Sep 2026: expected return 5.5%, value at risk 5.9%.  
  <sub>clients.json CASE-022: Portfolios[CASE-022-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 939k, 14.7% of the book.  
  <sub>clients.json CASE-022: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 84.0% of the portfolio (CHF 5.36m).  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 14.7% of the portfolio (CHF 939k).  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 1.3% of the portfolio (CHF 83k).  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 19.3% of the portfolio (CHF 1.23m) after fund look-through.  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 15.3% of the portfolio (CHF 978k) after fund look-through.  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 15.0% of the portfolio (CHF 957k) after fund look-through.  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 12.6% of the portfolio (CHF 802k) after fund look-through.  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 6.9% of the portfolio (CHF 441k) after fund look-through.  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 5.5% of the portfolio (CHF 354k) after fund look-through.  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 5.5% of the portfolio (CHF 351k) after fund look-through.  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 3.9% of the portfolio (CHF 246k) after fund look-through.  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 80.6% of the portfolio (CHF 5.14m).  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 11.6% of the portfolio (CHF 738k).  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 6.4% of the portfolio (CHF 410k).  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): OZG: 1.5% of the portfolio (CHF 93k).  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Gold: CHF 83k, 1.3% of the portfolio.  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Holcim AG, CHF 568k (8.9% of the portfolio).  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 18 holdings; the largest: Holcim AG (CHF 568k), Swiss Re AG (CHF 532k), Zurich Insurance Group AG (CHF 467k), Novartis AG (CHF 415k).  
  <sub>clients.json CASE-022: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (1.00): Resolve "Cluster risk of a single financial instrument" on Swiss Re AG.  
  <sub>clients.json CASE-022: SuitabilityViolations[Id=593831]</sub>
- **Next best actions** (0.30): Keep the 14.7% cash (CHF 939k) in view of the note from 26 Nov 2024: "Expects an inheritance in the coming years, strategy to be reviewed at that point."  
  <sub>clients.json CASE-022: LiquidityInDefaultCurrency, ClientNotes</sub>
- **Next best actions** (0.25): Clear the warnings on the 14 flagged orders from the proposal of 5 Oct 2025.  
  <sub>clients.json CASE-022: Transactions[ProposalId=17579].ForwardState = 2</sub>
- **Next best actions** (0.20): Candidates from the recommendation list for Shares: Kuehne + Nagel International AG and Lonza Group AG (cash is above 10% of the book).  
  <sub>reference.json RecommendationLists "Recommendation list free assets", not held, CHF first, ordered by SustainabilityScore</sub>

</details>

---

## CASE-023 — Frodo Beutlin

Investor profile 7 · CHF 258k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Frodo Beutlin, Investor profile 7, CHF 258k across 1 portfolio.  
   <sub>clients.json CASE-023: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +35.6% over the 12 months to Jul 2026 and +213.1% since Oct 2021, now CHF 136k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-023: PerformanceHistory of CASE-023-01</sub>
3. **Health check.** Volatility is 24.5%, above the 18.5% maximum of Investor profile 7.  
   <sub>clients.json CASE-023: Portfolios[CASE-023-01].Volatility; reference.json RiskProfiles.MaxVola</sub>
4. **Health check.** Bonds at 0.0%, outside its 10.0%–70.0% band, target 42.0%.  
   <sub>clients.json CASE-023: Portfolios[CASE-023-01] positions; reference.json StrategicAssetAllocations[44] AssetClass "Bonds"</sub>
5. **Watch.** Communication Services is 17.3% of the book (CHF 45k) after fund look-through, mostly via Alphabet Inc and Swisscom AG.  
   <sub>clients.json CASE-023: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Watch.** Note from 20 Aug 2026: "Mentioned wanting to keep a small reserve on hand at all times, 'just in case'."  
   <sub>clients.json CASE-023: ClientNotes</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "We remain Underweight real estate and consumer staples amid weak sentiment and low visibility on the housing recovery."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Deploy idle liquidity: 52.0% of the book (CHF 134k) is cash.  
   <sub>clients.json CASE-023: LiquidityInDefaultCurrency</sub>
9. **Next best actions.** Rebalance Bonds up toward 42.0%.  
   <sub>clients.json CASE-023: Portfolios[CASE-023-01] positions; reference.json StrategicAssetAllocations[44] AssetClass "Bonds"</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Frodo Beutlin is calling: Investor profile 7, CHF 258k across 1 portfolio.  
   <sub>clients.json CASE-023: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: calm temperament, wants it short. From the notes: "Comfortable with high concentration risk and significant volatility, including in digital assets."  
   <sub>data/profiles/profiles.json CASE-023 (apertus) from clients.json ClientNotes</sub>
3. **reason.** Probably the market: about −CHF 3k today, −1.3% of the book. Mostly Communication Services, −3.1% on 17.3% of it.  
   <sub>impact of the market feed on clients.json CASE-023 holdings</sub>
4. **reason.** Possibly idle cash: 52.0% of the book (CHF 134k) is cash.  
   <sub>clients.json CASE-023: LiquidityInDefaultCurrency</sub>
5. **digest.** About −CHF 3k today, −1.3% of the book.  
   <sub>impact of the market feed on clients.json CASE-023 holdings</sub>
6. **digest.** About −CHF 1k from Communication Services, −3.1% today on 17.3% of the book, mostly Alphabet Inc and Swisscom AG.  
   <sub>market feed "tech-selloff": S5TELS Index CHG_PCT_1D × clients.json CASE-023 holdings</sub>
7. **digest.** About −CHF 856 from Ether, −8.1% today on 4.1% of the book.  
   <sub>market feed "tech-selloff": XETUSD Curncy CHG_PCT_1D × clients.json CASE-023 holdings</sub>
8. **digest.** About −CHF 526 from Information Technology, −4.8% today on 4.2% of the book, mostly International Business Machines Corp IBM.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-023 holdings</sub>
9. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
10. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
11. **holding.** Holding up today: Consumer Staples +0.3% (10.3% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × clients.json CASE-023 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.11): Health Care is 10.8% of the book (CHF 28k) after fund look-through, mostly via Roche Holding AG and Basilea Pharmaceutica AG.  
  <sub>clients.json CASE-023: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 27 Jun 2026: "Prefers to carry the decisions on his own portfolio rather than delegate them -- politely declines most proposals."  
  <sub>clients.json CASE-023: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Investment advisory (CASE-023-01), 3 Sep 2026: expected return 9.8%, value at risk 34.2%.  
  <sub>clients.json CASE-023: Portfolios[CASE-023-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 134k, 52.0% of the book.  
  <sub>clients.json CASE-023: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Cash is 52.0% of the portfolio (CHF 134k).  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Shares are 47.8% of the portfolio (CHF 123k).  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Communication Services is 17.3% of the portfolio (CHF 45k) after fund look-through.  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 10.8% of the portfolio (CHF 28k) after fund look-through.  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 10.3% of the portfolio (CHF 27k) after fund look-through.  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 5.1% of the portfolio (CHF 13k) after fund look-through.  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 4.2% of the portfolio (CHF 11k) after fund look-through.  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 74.9% of the portfolio (CHF 193k).  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 13.8% of the portfolio (CHF 36k).  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Andere: 7.0% of the portfolio (CHF 18k).  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): ETH: 4.1% of the portfolio (CHF 11k).  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Crypto: CHF 11k, 4.1% of the portfolio.  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Alphabet Inc, CHF 25k (9.5% of the portfolio).  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 9 holdings; the largest: Alphabet Inc (CHF 25k), Swisscom AG (CHF 20k), Imperial Brands PLC (CHF 18k), Roche Holding AG (CHF 18k).  
  <sub>clients.json CASE-023: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.40): Book a review: no finalised proposal on record.  
  <sub>clients.json CASE-023: Proposals</sub>
- **Next best actions** (0.20): Candidates from the recommendation list for Bonds: 0.1525 % Cembra Money Bank AG 2019-14.10.26 and 2.875 % OC Oerlikon Corporation AG, Pfaeffikon 2023-19.03.29 Tranche 1 (Bonds is under its band).  
  <sub>reference.json RecommendationLists "Recommendation list free assets", not held, CHF first, ordered by SustainabilityScore</sub>

</details>

---

## CASE-024 — Vito Corleone

Investor profile 5 · CHF 503k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Vito Corleone, Investor profile 5, ESG preference, CHF 503k across 1 portfolio.  
   <sub>clients.json CASE-024: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +18.8% over the 12 months to Jul 2026 and +50.1% since Oct 2021, now CHF 503k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-024: PerformanceHistory of CASE-024-01</sub>
3. **Health check.** ESG client: average sustainability score 7.0 of 10 against a minimum of 5.7; 2 holdings below the per-position minimum (1.625 % Alpiq Holding AG 2022-30.05.25 and 0.26 % Hyundai Capital Services Inc 2020-11.02.25, 9.9% of the book); 10.0% of the book has no score.  
   <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-024 positions</sub>
4. **Health check.** 16 of 16 orders from the proposal of 30 Jun 2026 were forwarded with a warning.  
   <sub>clients.json CASE-024: Transactions[ProposalId=23263].ForwardState = 2</sub>
5. **Watch.** MSCI ACWI SF UCITS ETF drives 19.1% of the volatility of Investment advisory (CASE-024-01).  
   <sub>clients.json CASE-024: Portfolios[CASE-024-01].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Note from 22 Aug 2026: "Comfortable with higher volatility given a long time horizon."  
   <sub>clients.json CASE-024: ClientNotes</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Clear the warnings on the 16 flagged orders from the proposal of 30 Jun 2026.  
   <sub>clients.json CASE-024: Transactions[ProposalId=23263].ForwardState = 2</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Vito Corleone is calling: Investor profile 5, ESG preference, CHF 503k across 1 portfolio.  
   <sub>clients.json CASE-024: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: calm temperament. From the notes: "Comfortable with higher volatility given a long time horizon."  
   <sub>data/profiles/profiles.json CASE-024 (apertus) from clients.json ClientNotes</sub>
3. **reason.** Probably a sustainability concern: ESG client: average sustainability score 7.0 of 10 against a minimum of 5.7; 2 holdings below the per-position minimum (1.625 % Alpiq Holding AG 2022-30.05.25 and 0.26 % Hyundai Capital Services Inc 2020-11.02.25, 9.9% of the book); 10.0% of the book has no score.  
   <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-024 positions</sub>
4. **digest.** About −CHF 665 today, −0.1% of the book.  
   <sub>impact of the market feed on clients.json CASE-024 holdings</sub>
5. **digest.** About −CHF 670 from Information Technology, −4.8% today on 2.8% of the book, mostly MSCI ACWI SF UCITS ETF and iShares Core SPI(R) ETF (CH).  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-024 holdings</sub>
6. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
7. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** About −CHF 197 from Consumer Discretionary, −2.2% today on 1.8% of the book, mostly MSCI ACWI SF UCITS ETF and iShares Core SPI(R) ETF (CH).  
   <sub>market feed "tech-selloff": S5COND Index CHG_PCT_1D × clients.json CASE-024 holdings</sub>
9. **digest.** About −CHF 133 from Industrials, −1.1% today on 2.4% of the book, mostly iShares Core SPI(R) ETF (CH) and MSCI ACWI SF UCITS ETF.  
   <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-024 holdings</sub>
10. **digest.** 5.2% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-024 holdings without a mapped market move</sub>
11. **holding.** Holding up today: Swiss franc bonds +0.2% (72.3% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-024 holdings</sub>
12. **holding.** Global Investment Grade Credit Fund and MSCI ACWI SF UCITS ETF and SPDR Bloomberg Global Aggregate Bond UCITS ETF (28.5% of the book) are hedged to the franc, so the dollar move (−1.2%) does not reach them.  
   <sub>clients.json CASE-024: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.13): Financials is 13.3% of the book (CHF 67k) after fund look-through, mostly via 0.2 % Luzerner Kantonalbank AG 2017-11.04.25 and 0.3 % National Australia Bank Ltd 2017-31.10.25 Global.  
  <sub>clients.json CASE-024: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.12): 24.5% of the book is in holdings on none of the bank's recommendation lists, largest 1.375 % Grande Dixence SA 2015-18.02.25, 1.5 % TEMENOS AG 2019-28.11.25 and 3 more.  
  <sub>reference.json Securities.InRecommendationList; clients.json CASE-024 positions</sub>
- **Watch** (0.12): Industrials is 12.2% of the book (CHF 61k) after fund look-through, mostly via 0.8 % Sulzer AG 2020-23.09.25 and 0.375 % OC Oerlikon Corporation AG, Pfaeffikon 2021-27.11.25 Reg S.  
  <sub>clients.json CASE-024: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 8 Apr 2025: "Risk profile discussed again after the market downturn, client keeps current classification."  
  <sub>clients.json CASE-024: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (30 Jun 2026, reason: Periodic portfolio review) ordered to buy iShares Core SPI(R) ETF (CH), MSCI ACWI SF UCITS ETF and 14 more.  
  <sub>clients.json CASE-024: Proposals[23263] × Transactions</sub>
- **Watch** (0.05): Currency-hedged holdings: Global Investment Grade Credit Fund, MSCI ACWI SF UCITS ETF, SPDR Bloomberg Global Aggregate Bond UCITS ETF (28.5% of the book).  
  <sub>clients.json CASE-024: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Investment advisory (CASE-024-01), 3 Sep 2026: expected return 2.9%, value at risk 15.3%.  
  <sub>clients.json CASE-024: Portfolios[CASE-024-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 48.0% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-024: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 8k, 1.7% of the book.  
  <sub>clients.json CASE-024: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Bonds are 72.3% of the portfolio (CHF 364k).  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Shares are 20.9% of the portfolio (CHF 105k).  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 5.2% of the portfolio (CHF 26k).  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 1.7% of the portfolio (CHF 8k).  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 13.3% of the portfolio (CHF 67k) after fund look-through.  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 12.2% of the portfolio (CHF 61k) after fund look-through.  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 7.7% of the portfolio (CHF 39k) after fund look-through.  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 7.5% of the portfolio (CHF 38k) after fund look-through.  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 4.5% of the portfolio (CHF 22k) after fund look-through.  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 1.8% of the portfolio (CHF 9k) after fund look-through.  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 1.3% of the portfolio (CHF 7k) after fund look-through.  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 0.9% of the portfolio (CHF 4k) after fund look-through.  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.5% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.4% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.3% of the portfolio (CHF 1k) after fund look-through.  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 503k).  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares Core SPI(R) ETF (CH), CHF 53k (10.5% of the portfolio).  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 16 holdings; the largest: iShares Core SPI(R) ETF (CH) (CHF 53k), MSCI ACWI SF UCITS ETF (CHF 52k), SPDR Bloomberg Global Aggregate Bond UCITS ETF (CHF 46k), Global Investment Grade Credit Fund (CHF 46k).  
  <sub>clients.json CASE-024: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-025 — John McClane

Investor profile 7 · CHF 259k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** John McClane, Investor profile 7, CHF 259k across 2 portfolios.  
   <sub>clients.json CASE-025: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Combined portfolio value +13.1% over the 12 months to Jul 2026 and +26.1% since Oct 2021, now CHF 259k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-025: PerformanceHistory of CASE-025-01, CASE-025-02</sub>
3. **Health check.** Risk profile last assessed 5 Sep 2022, 4 years ago.  
   <sub>clients.json CASE-025: ProfilingDateUtc</sub>
4. **Watch.** Chocoladefabriken Lindt & Spruengli AG drives 94.2% of the volatility of Account / Custody (CASE-025-02).  
   <sub>clients.json CASE-025: Portfolios[CASE-025-02].SecurityPositions.ContributionVolatility</sub>
5. **Watch.** Consumer Staples is 79.8% of the book (CHF 206k) after fund look-through, mostly via Chocoladefabriken Lindt & Spruengli AG.  
   <sub>clients.json CASE-025: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "We remain Underweight real estate and consumer staples amid weak sentiment and low visibility on the housing recovery."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-025: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** John McClane is calling: Investor profile 7, CHF 259k across 2 portfolios.  
   <sub>clients.json CASE-025: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: calm temperament. From the notes: "Risk profile discussed again after the market downturn, client keeps current classification."  
   <sub>data/profiles/profiles.json CASE-025 (apertus) from clients.json ClientNotes</sub>
3. **digest.** About +CHF 370 today, +0.1% of the book.  
   <sub>impact of the market feed on clients.json CASE-025 holdings</sub>
4. **digest.** About −CHF 240 from Financials, −0.9% today on 10.3% of the book, mostly VZ Holding AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-025 holdings</sub>
5. **holding.** Holding up today: Consumer Staples +0.3% (79.8% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × clients.json CASE-025 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.80): Chocoladefabriken Lindt & Spruengli AG alone is 79.8% of the book.  
  <sub>clients.json CASE-025: Portfolios[CASE-025-02].SecurityPositions</sub>
- **Watch** (0.15): Note from 17 Jul 2026: "Watching technology stocks in the portfolio closely, interested in expanding further."  
  <sub>clients.json CASE-025: ClientNotes</sub>
- **Watch** (0.10): Financials is 10.3% of the book (CHF 27k) after fund look-through, mostly via VZ Holding AG.  
  <sub>clients.json CASE-025: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): VZ Holding AG alone is 10.3% of the book.  
  <sub>clients.json CASE-025: Portfolios[CASE-025-02].SecurityPositions</sub>
- **Watch** (0.10): Note from 31 Dec 2025: "Does not want investments in companies with human-rights controversies."  
  <sub>clients.json CASE-025: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Account / Custody (CASE-025-02), 3 Sep 2026: expected return 6.3%, value at risk 21.3%.  
  <sub>clients.json CASE-025: Portfolios[CASE-025-02].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 25k, 9.8% of the book.  
  <sub>clients.json CASE-025: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 90.2% of the portfolio (CHF 233k).  
  <sub>clients.json CASE-025: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 9.8% of the portfolio (CHF 25k).  
  <sub>clients.json CASE-025: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Consumer Staples is 79.8% of the portfolio (CHF 206k) after fund look-through.  
  <sub>clients.json CASE-025: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 10.3% of the portfolio (CHF 27k) after fund look-through.  
  <sub>clients.json CASE-025: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 0.1% of the portfolio (CHF 307) after fund look-through.  
  <sub>clients.json CASE-025: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 259k).  
  <sub>clients.json CASE-025: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Chocoladefabriken Lindt & Spruengli AG, CHF 206k (79.8% of the portfolio).  
  <sub>clients.json CASE-025: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 3 holdings; the largest: Chocoladefabriken Lindt & Spruengli AG (CHF 206k), VZ Holding AG (CHF 27k), TX Group AG (CHF 307).  
  <sub>clients.json CASE-025: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-026 — Superman

Investor profile 6 · CHF 2.38m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Superman, Investor profile 6, CHF 2.38m across 1 portfolio.  
   <sub>clients.json CASE-026: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +0.7% over the 12 months to Jul 2026 and −17.0% since Oct 2021, now CHF 2.36m; value change including deposits and withdrawals.  
   <sub>clients.json CASE-026: PerformanceHistory of CASE-026-01</sub>
3. **Health check.** 5 suitability errors and 4 warnings open; most serious: "Volatility range undershot (portfolio risk too low)".  
   <sub>clients.json CASE-026: SuitabilityViolations</sub>
4. **Health check.** Risk profile last assessed 22 May 2023, 3 years ago.  
   <sub>clients.json CASE-026: ProfilingDateUtc</sub>
5. **Watch.** Raw materials is 20.1% of the book (CHF 479k) after fund look-through, mostly via Holcim AG and Sika AG.  
   <sub>clients.json CASE-026: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Watch.** Health Care is 20.0% of the book (CHF 475k) after fund look-through, mostly via Novartis AG and Straumann Holding AG.  
   <sub>clients.json CASE-026: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Resolve "Foreign currency cluster risk EUR".  
   <sub>clients.json CASE-026: SuitabilityViolations[Id=77332]</sub>
9. **Next best actions.** Resolve "Cluster risk of a single financial instrument" on Holcim AG.  
   <sub>clients.json CASE-026: SuitabilityViolations[Id=561851]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Superman is calling: Investor profile 6, CHF 2.38m across 1 portfolio.  
   <sub>clients.json CASE-026: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: wants it detailed. From the notes: "Requested a comparison against the benchmark at the next review."  
   <sub>data/profiles/profiles.json CASE-026 (apertus) from clients.json ClientNotes</sub>
3. **caller.** Contact preference: "Prefers semi-annual phone contact, no unannounced visits"  
   <sub>data/profiles/profiles.json CASE-026 from clients.json ClientNotes</sub>
4. **reason.** Probably the market: about −CHF 30k today, −1.3% of the book. Mostly Information Technology, −4.8% on 8.3% of it.  
   <sub>impact of the market feed on clients.json CASE-026 holdings</sub>
5. **digest.** About −CHF 30k today, −1.3% of the book.  
   <sub>impact of the market feed on clients.json CASE-026 holdings</sub>
6. **digest.** About −CHF 9k from Information Technology, −4.8% today on 8.3% of the book, mostly iShares NASDAQ 100 UCITS ETF and Logitech International SA.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-026 holdings</sub>
7. **digest.** About −CHF 4k from the dollar, −1.2% against the franc on 15.7% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-026 holdings</sub>
8. **digest.** About −CHF 4k from Financials, −0.9% today on 16.8% of the book, mostly Zurich Insurance Group AG and Helvetia Holding AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-026 holdings</sub>
9. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
10. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
11. **holding.** Holding up today: Consumer Staples +0.3% (8.6% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × clients.json CASE-026 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): "Foreign currency cluster risk EUR" means: For private customers, the EUR share should be < 9%.  
  <sub>clients.json CASE-026: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Cluster risk of a single financial instrument" means: For retail clients with financial services, comprehensive investment advisory or trx-based investment advisory must be single title share < x% (x varies with instrument type)  
  <sub>clients.json CASE-026: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Significant overweight in the equity region "Switzerland"" means: Significant overweight (+/- 10% of the benchmark’s SAA target) in the ‘Switzerland’ equity region  
  <sub>clients.json CASE-026: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.15): Note from 27 Apr 2026: "Prefers semi-annual phone contact, no unannounced visits."  
  <sub>clients.json CASE-026: ClientNotes</sub>
- **Watch** (0.11): Holcim AG alone is 11.0% of the book.  
  <sub>clients.json CASE-026: Portfolios[CASE-026-01].SecurityPositions</sub>
- **Watch** (0.10): Note from 2 Oct 2025: "Comfortable with higher volatility given a long time horizon."  
  <sub>clients.json CASE-026: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-026-01), 3 Sep 2026: expected return 6.2%, value at risk 12.1%.  
  <sub>clients.json CASE-026: Portfolios[CASE-026-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 115k, 4.9% of the book.  
  <sub>clients.json CASE-026: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 94.0% of the portfolio (CHF 2.23m).  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 4.9% of the portfolio (CHF 115k).  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 1.2% of the portfolio (CHF 27k).  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Raw materials is 20.1% of the portfolio (CHF 479k) after fund look-through.  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 20.0% of the portfolio (CHF 475k) after fund look-through.  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 16.8% of the portfolio (CHF 400k) after fund look-through.  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 9.5% of the portfolio (CHF 227k) after fund look-through.  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 8.6% of the portfolio (CHF 204k) after fund look-through.  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 8.3% of the portfolio (CHF 198k) after fund look-through.  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 3.6% of the portfolio (CHF 85k) after fund look-through.  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 2.4% of the portfolio (CHF 57k) after fund look-through.  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 2.1% of the portfolio (CHF 51k) after fund look-through.  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 2.0% of the portfolio (CHF 48k) after fund look-through.  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.5% of the portfolio (CHF 11k) after fund look-through.  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 68.6% of the portfolio (CHF 1.63m).  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 17.7% of the portfolio (CHF 422k).  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 10.8% of the portfolio (CHF 256k).  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Andere: 2.0% of the portfolio (CHF 47k).  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): BTC: 0.9% of the portfolio (CHF 20k).  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Gold: CHF 42k, 1.8% of the portfolio.  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Crypto: CHF 20k, 0.9% of the portfolio.  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Holcim AG, CHF 262k (11.0% of the portfolio).  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 36 holdings; the largest: Holcim AG (CHF 262k), Zurich Insurance Group AG (CHF 136k), Sika AG (CHF 128k), Novartis AG (CHF 127k).  
  <sub>clients.json CASE-026: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (1.00): Resolve "Significant overweight in the equity region "Switzerland"".  
  <sub>clients.json CASE-026: SuitabilityViolations[Id=602319]</sub>
- **Next best actions** (0.40): Book a review: no finalised proposal on record.  
  <sub>clients.json CASE-026: Proposals</sub>

</details>

---

## CASE-027 — Buzz Lightyear

Investor profile 5 · CHF 172k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Buzz Lightyear, Investor profile 5, ESG preference, CHF 172k across 1 portfolio.  
   <sub>clients.json CASE-027: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +22.8% over the 12 months to Jul 2026 and +78.2% since Oct 2021, now CHF 170k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-027: PerformanceHistory of CASE-027-01</sub>
3. **Health check.** Risk profile last assessed 1 Oct 2022, 4 years ago.  
   <sub>clients.json CASE-027: ProfilingDateUtc</sub>
4. **Health check.** Volatility is 12.2%, above the 12.0% maximum of Investor profile 5.  
   <sub>clients.json CASE-027: Portfolios[CASE-027-01].Volatility; reference.json RiskProfiles.MaxVola</sub>
5. **Watch.** Industrials is 97.9% of the book (CHF 168k) after fund look-through, mostly via SpaceX and Union Pacific Corp.  
   <sub>clients.json CASE-027: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Watch.** SpaceX alone is 68.5% of the book.  
   <sub>clients.json CASE-027: Portfolios[CASE-027-01].SecurityPositions</sub>
7. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "The AI-driven capex boom, and the need for infrastructure to support it, should support the outlook for industrials, another sector on which we have an overweight stance."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
8. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-027: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Buzz Lightyear is calling: Investor profile 5, ESG preference, CHF 172k across 1 portfolio.  
   <sub>clients.json CASE-027: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: calm temperament, wants it detailed. From the notes: "Comfortable with a long time horizon; not concerned by short-term volatility in thematic growth positions."  
   <sub>data/profiles/profiles.json CASE-027 (apertus) from clients.json ClientNotes</sub>
3. **reason.** Probably the market: about −CHF 4k today, −2.3% of the book. Mostly the dollar, −1.2% on 97.9% of it.  
   <sub>impact of the market feed on clients.json CASE-027 holdings</sub>
4. **digest.** About −CHF 4k today, −2.3% of the book.  
   <sub>impact of the market feed on clients.json CASE-027 holdings</sub>
5. **digest.** About −CHF 2k from the dollar, −1.2% against the franc on 97.9% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-027 holdings</sub>
6. **digest.** About −CHF 2k from Industrials, −1.1% today on 97.9% of the book, mostly SpaceX and Union Pacific Corp.  
   <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-027 holdings</sub>
7. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): ESG client: average sustainability score 7.3 of 10 against a minimum of 5.7; 68.5% of the book has no score.  
  <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-027 positions</sub>
- **Watch** (0.18): Union Pacific Corp alone is 17.6% of the book.  
  <sub>clients.json CASE-027: Portfolios[CASE-027-01].SecurityPositions</sub>
- **Watch** (0.15): Note from 20 Jul 2026: "Very enthusiastic about space travel, follows private spaceflight companies with great interest."  
  <sub>clients.json CASE-027: ClientNotes</sub>
- **Watch** (0.12): Caterpillar Inc alone is 11.7% of the book.  
  <sub>clients.json CASE-027: Portfolios[CASE-027-01].SecurityPositions</sub>
- **Watch** (0.10): Note from 4 Jul 2026: "Asked for more detail on how private spaceflight and aerospace exposure could be expanded further."  
  <sub>clients.json CASE-027: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Account / Custody (CASE-027-01), 3 Sep 2026: expected return 6.5%, value at risk 8.8%.  
  <sub>clients.json CASE-027: Portfolios[CASE-027-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 4k, 2.1% of the book.  
  <sub>clients.json CASE-027: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 97.9% of the portfolio (CHF 168k).  
  <sub>clients.json CASE-027: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 2.1% of the portfolio (CHF 4k).  
  <sub>clients.json CASE-027: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Industrials is 97.9% of the portfolio (CHF 168k) after fund look-through.  
  <sub>clients.json CASE-027: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): US-Dollar: 97.9% of the portfolio (CHF 168k).  
  <sub>clients.json CASE-027: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Swiss francs: 1.1% of the portfolio (CHF 2k).  
  <sub>clients.json CASE-027: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): SOL: 1.0% of the portfolio (CHF 2k).  
  <sub>clients.json CASE-027: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Crypto: CHF 2k, 1.0% of the portfolio.  
  <sub>clients.json CASE-027: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: SpaceX, CHF 118k (68.5% of the portfolio).  
  <sub>clients.json CASE-027: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 3 holdings; the largest: SpaceX (CHF 118k), Union Pacific Corp (CHF 30k), Caterpillar Inc (CHF 20k).  
  <sub>clients.json CASE-027: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-028 — Charles Foster Kane

Investor profile 5 · CHF 197k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Charles Foster Kane, Investor profile 5, CHF 197k across 1 portfolio.  
   <sub>clients.json CASE-028: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +22.6% over the 12 months to Jul 2026 and +43.3% since Oct 2021, now CHF 197k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-028: PerformanceHistory of CASE-028-01</sub>
3. **Health check.** Volatility is 22.0%, above the 12.0% maximum of Investor profile 5.  
   <sub>clients.json CASE-028: Portfolios[CASE-028-01].Volatility; reference.json RiskProfiles.MaxVola</sub>
4. **Health check.** Risk profile last assessed 28 Sep 2022, 4 years ago.  
   <sub>clients.json CASE-028: ProfilingDateUtc</sub>
5. **Watch.** VZ Holding AG drives 100.0% of the volatility of Account / Custody (CASE-028-01).  
   <sub>clients.json CASE-028: Portfolios[CASE-028-01].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Financials is 95.9% of the book (CHF 189k) after fund look-through, mostly via VZ Holding AG.  
   <sub>clients.json CASE-028: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-028: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Charles Foster Kane is calling: Investor profile 5, CHF 197k across 1 portfolio.  
   <sub>clients.json CASE-028: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: wants it detailed. From the notes: "Appreciates a detailed written summary after every meeting."  
   <sub>data/profiles/profiles.json CASE-028 (apertus) from clients.json ClientNotes</sub>
3. **reason.** Probably the market: about −CHF 2k today, −0.9% of the book. Mostly Financials, −0.9% on 95.9% of it.  
   <sub>impact of the market feed on clients.json CASE-028 holdings</sub>
4. **digest.** About −CHF 2k today, −0.9% of the book.  
   <sub>impact of the market feed on clients.json CASE-028 holdings</sub>
5. **digest.** About −CHF 2k from Financials, −0.9% today on 95.9% of the book, mostly VZ Holding AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-028 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.96): VZ Holding AG alone is 95.9% of the book.  
  <sub>clients.json CASE-028: Portfolios[CASE-028-01].SecurityPositions</sub>
- **Watch** (0.15): Note from 26 Aug 2025: "Appreciates a detailed written summary after every meeting."  
  <sub>clients.json CASE-028: ClientNotes</sub>
- **Watch** (0.10): Note from 12 Jun 2025: "Wants exposure limited to developed markets only, no emerging markets."  
  <sub>clients.json CASE-028: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Account / Custody (CASE-028-01), 3 Sep 2026: expected return 6.3%, value at risk 21.1%.  
  <sub>clients.json CASE-028: Portfolios[CASE-028-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 8k, 4.1% of the book.  
  <sub>clients.json CASE-028: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 95.9% of the portfolio (CHF 189k).  
  <sub>clients.json CASE-028: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 4.2% of the portfolio (CHF 8k).  
  <sub>clients.json CASE-028: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 95.9% of the portfolio (CHF 189k) after fund look-through.  
  <sub>clients.json CASE-028: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 197k).  
  <sub>clients.json CASE-028: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: VZ Holding AG, CHF 189k (95.9% of the portfolio).  
  <sub>clients.json CASE-028: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 1 holdings; the largest: VZ Holding AG (CHF 189k).  
  <sub>clients.json CASE-028: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-029 — Scarlett O'Hara

no risk profile · CHF 102k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Scarlett O'Hara, no risk profile, CHF 102k across 1 portfolio.  
   <sub>clients.json CASE-029: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +21.0% over the 12 months to Jul 2026 and +78.0% since Oct 2021, now CHF 102k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-029: PerformanceHistory of CASE-029-01</sub>
3. **Health check.** Nothing open: no suitability violation, and every asset class is inside its band.  
   <sub>clients.json CASE-029: SuitabilityViolations (none open); reference.json StrategicAssetAllocations bands</sub>
4. **Watch.** Global Aggregate Bond Index Fund drives 20.8% of the volatility of Pension (CASE-029-01).  
   <sub>clients.json CASE-029: Portfolios[CASE-029-01].SecurityPositions.ContributionVolatility</sub>
5. **Watch.** Note from 9 Jul 2026: "Very risk-averse since the last market downturn, prefers defensive positioning."  
   <sub>clients.json CASE-029: ClientNotes</sub>
6. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-029: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Scarlett O'Hara is calling: no risk profile, CHF 102k across 1 portfolio.  
   <sub>clients.json CASE-029: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably a withdrawal: note from 13 May 2026: "Plans to retire in the next two years, increasing liquidity needs expected."  
   <sub>clients.json CASE-029: ClientNotes</sub>
3. **reason.** Possibly the market: about −CHF 582 today, −0.6% of the book. Mostly Information Technology, −4.8% on 5.2% of it.  
   <sub>impact of the market feed on clients.json CASE-029 holdings</sub>
4. **digest.** About −CHF 582 today, −0.6% of the book.  
   <sub>impact of the market feed on clients.json CASE-029 holdings</sub>
5. **digest.** About −CHF 256 from Information Technology, −4.8% today on 5.2% of the book, mostly CSIF (CH) I Equity World ex CH Blue and CSIF (CH) Equity World ex CH ESG Blue.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-029 holdings</sub>
6. **digest.** About −CHF 146 from the dollar, −1.2% against the franc on 11.9% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-029 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** About −CHF 70 from Consumer Discretionary, −2.2% today on 3.1% of the book, mostly CSIF (CH) I Equity World ex CH Blue and Equities Switzerland Passive Leader.  
   <sub>market feed "tech-selloff": S5COND Index CHG_PCT_1D × clients.json CASE-029 holdings</sub>
10. **digest.** 5.1% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-029 holdings without a mapped market move</sub>
11. **holding.** Holding up today: Swiss franc bonds +0.2% (56.5% of the book); Consumer Staples +0.3% (3.3% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-029 holdings</sub>
12. **holding.** Vanguard Global Bond Index Fund (11.2% of the book) is hedged to the franc, so the dollar move (−1.2%) does not reach it.  
   <sub>clients.json CASE-029: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.10): Note from 19 May 2026: "Was informed of the risks of structured products and explicitly accepts them."  
  <sub>clients.json CASE-029: ClientNotes</sub>
- **Watch** (0.07): Financials is 7.1% of the book (CHF 7k) after fund look-through, mostly via iShares Swiss Dividend ETF (CH) and Equities Switzerland Passive Leader.  
  <sub>clients.json CASE-029: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.07): Health Care is 6.9% of the book (CHF 7k) after fund look-through, mostly via Equities Switzerland Passive Leader and iShares Swiss Dividend ETF (CH).  
  <sub>clients.json CASE-029: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.05): Currency-hedged holdings: Vanguard Global Bond Index Fund (11.2% of the book).  
  <sub>clients.json CASE-029: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Pension (CASE-029-01), 3 Sep 2026: expected return 3.6%, value at risk 13.8%.  
  <sub>clients.json CASE-029: Portfolios[CASE-029-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 61.6% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-029: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 2k, 1.8% of the book.  
  <sub>clients.json CASE-029: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Bonds are 56.5% of the portfolio (CHF 58k).  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Shares are 36.6% of the portfolio (CHF 37k).  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 5.1% of the portfolio (CHF 5k).  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 1.8% of the portfolio (CHF 2k).  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 7.1% of the portfolio (CHF 7k) after fund look-through.  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 6.9% of the portfolio (CHF 7k) after fund look-through.  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 5.2% of the portfolio (CHF 5k) after fund look-through.  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 5.0% of the portfolio (CHF 5k) after fund look-through.  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 3.3% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 3.1% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 2.0% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 2.0% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.8% of the portfolio (CHF 795) after fund look-through.  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.7% of the portfolio (CHF 765) after fund look-through.  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.4% of the portfolio (CHF 444) after fund look-through.  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 102k).  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Global Aggregate Bond Index Fund, CHF 11k (11.2% of the portfolio).  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 13 holdings; the largest: Global Aggregate Bond Index Fund (CHF 11k), CSIF (CH) Bond Aggregate Global ex CHF ESG Blue (CHF 11k), Vanguard Global Bond Index Fund (CHF 11k), CSIF (CH) I Equity World ex CH Blue (CHF 10k).  
  <sub>clients.json CASE-029: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-030 — Darth Vader

no risk profile · CHF 28k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Darth Vader, no risk profile, CHF 28k across 1 portfolio.  
   <sub>clients.json CASE-030: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +27.7% over the 12 months to Jul 2026 and +94.3% since Oct 2021, now CHF 28k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-030: PerformanceHistory of CASE-030-01</sub>
3. **Health check.** Nothing open: no suitability violation, and every asset class is inside its band.  
   <sub>clients.json CASE-030: SuitabilityViolations (none open); reference.json StrategicAssetAllocations bands</sub>
4. **Watch.** Global Aggregate Bond Index Fund drives 20.7% of the volatility of Pension (CASE-030-01).  
   <sub>clients.json CASE-030: Portfolios[CASE-030-01].SecurityPositions.ContributionVolatility</sub>
5. **Watch.** Note from 12 Aug 2025: "Requested a comparison against the benchmark at the next review."  
   <sub>clients.json CASE-030: ClientNotes</sub>
6. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-030: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Darth Vader is calling: no risk profile, CHF 28k across 1 portfolio.  
   <sub>clients.json CASE-030: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 159 today, −0.6% of the book. Mostly Information Technology, −4.8% on 5.2% of it.  
   <sub>impact of the market feed on clients.json CASE-030 holdings</sub>
3. **digest.** About −CHF 159 today, −0.6% of the book.  
   <sub>impact of the market feed on clients.json CASE-030 holdings</sub>
4. **digest.** About −CHF 70 from Information Technology, −4.8% today on 5.2% of the book, mostly CSIF (CH) I Equity World ex CH Blue and CSIF (CH) Equity World ex CH ESG Blue.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-030 holdings</sub>
5. **digest.** About −CHF 40 from the dollar, −1.2% against the franc on 11.8% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-030 holdings</sub>
6. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
7. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** About −CHF 19 from Consumer Discretionary, −2.2% today on 3.1% of the book, mostly CSIF (CH) I Equity World ex CH Blue and Equities Switzerland Passive Leader.  
   <sub>market feed "tech-selloff": S5COND Index CHG_PCT_1D × clients.json CASE-030 holdings</sub>
9. **digest.** 5.4% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-030 holdings without a mapped market move</sub>
10. **holding.** Holding up today: Swiss franc bonds +0.2% (56.2% of the book); Consumer Staples +0.3% (3.3% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-030 holdings</sub>
11. **holding.** Vanguard Global Bond Index Fund (11.2% of the book) is hedged to the franc, so the dollar move (−1.2%) does not reach it.  
   <sub>clients.json CASE-030: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.10): Note from 1 Feb 2025: "Watching technology stocks in the portfolio closely, interested in expanding further."  
  <sub>clients.json CASE-030: ClientNotes</sub>
- **Watch** (0.07): Financials is 7.1% of the book (CHF 2k) after fund look-through, mostly via iShares Swiss Dividend ETF (CH) and Equities Switzerland Passive Leader.  
  <sub>clients.json CASE-030: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.07): Health Care is 7.0% of the book (CHF 2k) after fund look-through, mostly via Equities Switzerland Passive Leader and iShares Swiss Dividend ETF (CH).  
  <sub>clients.json CASE-030: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.05): Currency-hedged holdings: Vanguard Global Bond Index Fund (11.2% of the book).  
  <sub>clients.json CASE-030: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Pension (CASE-030-01), 3 Sep 2026: expected return 3.6%, value at risk 13.8%.  
  <sub>clients.json CASE-030: Portfolios[CASE-030-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 61.5% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-030: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 518, 1.8% of the book.  
  <sub>clients.json CASE-030: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Bonds are 56.2% of the portfolio (CHF 16k).  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Shares are 36.6% of the portfolio (CHF 10k).  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 5.4% of the portfolio (CHF 2k).  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 1.8% of the portfolio (CHF 519).  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 7.1% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 7.0% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 5.2% of the portfolio (CHF 1k) after fund look-through.  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 5.0% of the portfolio (CHF 1k) after fund look-through.  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 3.3% of the portfolio (CHF 927) after fund look-through.  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 3.1% of the portfolio (CHF 883) after fund look-through.  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 2.0% of the portfolio (CHF 574) after fund look-through.  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 2.0% of the portfolio (CHF 565) after fund look-through.  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.8% of the portfolio (CHF 219) after fund look-through.  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.7% of the portfolio (CHF 208) after fund look-through.  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.4% of the portfolio (CHF 121) after fund look-through.  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 28k).  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Global Aggregate Bond Index Fund, CHF 3k (11.2% of the portfolio).  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 13 holdings; the largest: Global Aggregate Bond Index Fund (CHF 3k), Vanguard Global Bond Index Fund (CHF 3k), CSIF (CH) Bond Aggregate Global ex CHF ESG Blue (CHF 3k), CSIF (CH) I Equity World ex CH Blue (CHF 3k).  
  <sub>clients.json CASE-030: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-031 — Wolverine

no risk profile · CHF 35k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Wolverine, no risk profile, ESG preference, CHF 35k across 1 portfolio.  
   <sub>clients.json CASE-031: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +25.4% over the 12 months to Jul 2026 and +84.1% since Oct 2021, now CHF 35k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-031: PerformanceHistory of CASE-031-01</sub>
3. **Watch.** Equities Switzerland Passive Leader drives 16.9% of the volatility of Pension (CASE-031-01).  
   <sub>clients.json CASE-031: Portfolios[CASE-031-01].SecurityPositions.ContributionVolatility</sub>
4. **Watch.** Note from 11 Jan 2026: "Wants to invest more heavily in Swiss small caps going forward."  
   <sub>clients.json CASE-031: ClientNotes</sub>
5. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
6. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-031: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Wolverine is calling: no risk profile, ESG preference, CHF 35k across 1 portfolio.  
   <sub>clients.json CASE-031: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Contact preference: "Prefers email communication, hard to reach by phone"  
   <sub>data/profiles/profiles.json CASE-031 from clients.json ClientNotes</sub>
3. **reason.** Probably the market: about −CHF 270 today, −0.8% of the book. Mostly Information Technology, −4.8% on 6.6% of it.  
   <sub>impact of the market feed on clients.json CASE-031 holdings</sub>
4. **digest.** About −CHF 270 today, −0.8% of the book.  
   <sub>impact of the market feed on clients.json CASE-031 holdings</sub>
5. **digest.** About −CHF 111 from Information Technology, −4.8% today on 6.6% of the book, mostly CSIF (CH) I Equity World ex CH Blue and CSIF (CH) Equity World ex CH ESG Blue.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-031 holdings</sub>
6. **digest.** About −CHF 63 from the dollar, −1.2% against the franc on 14.8% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-031 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** About −CHF 31 from Consumer Discretionary, −2.2% today on 4.0% of the book, mostly CSIF (CH) I Equity World ex CH Blue and Equities Switzerland Passive Leader.  
   <sub>market feed "tech-selloff": S5COND Index CHG_PCT_1D × clients.json CASE-031 holdings</sub>
10. **digest.** 5.0% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-031 holdings without a mapped market move</sub>
11. **holding.** Holding up today: Swiss franc bonds +0.2% (46.5% of the book); Consumer Staples +0.3% (4.1% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-031 holdings</sub>
12. **holding.** Vanguard Global Bond Index Fund (9.1% of the book) is hedged to the franc, so the dollar move (−1.2%) does not reach it.  
   <sub>clients.json CASE-031: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): ESG client: average sustainability score 7.1 of 10 against a minimum of 5.7; 5.0% of the book has no score.  
  <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-031 positions</sub>
- **Watch** (0.10): Note from 27 Jun 2025: "Prefers email communication, hard to reach by phone."  
  <sub>clients.json CASE-031: ClientNotes</sub>
- **Watch** (0.09): Financials is 8.9% of the book (CHF 3k) after fund look-through, mostly via iShares Swiss Dividend ETF (CH) and Equities Switzerland Passive Leader.  
  <sub>clients.json CASE-031: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.09): Health Care is 8.9% of the book (CHF 3k) after fund look-through, mostly via Equities Switzerland Passive Leader and iShares Swiss Dividend ETF (CH).  
  <sub>clients.json CASE-031: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.05): Currency-hedged holdings: Vanguard Global Bond Index Fund (9.1% of the book).  
  <sub>clients.json CASE-031: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Pension (CASE-031-01), 3 Sep 2026: expected return 4.1%, value at risk 14.2%.  
  <sub>clients.json CASE-031: Portfolios[CASE-031-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 51.5% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-031: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 711, 2.0% of the book.  
  <sub>clients.json CASE-031: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Bonds are 46.5% of the portfolio (CHF 16k).  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Shares are 46.4% of the portfolio (CHF 16k).  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 5.0% of the portfolio (CHF 2k).  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 2.0% of the portfolio (CHF 711).  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 8.9% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 8.9% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 6.6% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 6.3% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 4.1% of the portfolio (CHF 1k) after fund look-through.  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 4.0% of the portfolio (CHF 1k) after fund look-through.  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 2.7% of the portfolio (CHF 940) after fund look-through.  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 2.6% of the portfolio (CHF 907) after fund look-through.  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 1.0% of the portfolio (CHF 339) after fund look-through.  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.9% of the portfolio (CHF 327) after fund look-through.  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.5% of the portfolio (CHF 189) after fund look-through.  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 35k).  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Equities Switzerland Passive Leader, CHF 4k (11.3% of the portfolio).  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 13 holdings; the largest: Equities Switzerland Passive Leader (CHF 4k), CSIF (CH) I Equity World ex CH Blue (CHF 4k), Global Aggregate Bond Index Fund (CHF 3k), CSIF (CH) Bond Aggregate Global ex CHF ESG Blue (CHF 3k).  
  <sub>clients.json CASE-031: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-032 — Popeye

no risk profile · CHF 23k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Popeye, no risk profile, ESG preference, CHF 23k across 1 portfolio.  
   <sub>clients.json CASE-032: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +8.7% over the 12 months to Jul 2026 and −4.9% since Oct 2021, now CHF 23k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-032: PerformanceHistory of CASE-032-01</sub>
3. **Watch.** CSIF (CH) I Equity World ex CH Blue drives 21.3% of the volatility of Pension (CASE-032-01).  
   <sub>clients.json CASE-032: Portfolios[CASE-032-01].SecurityPositions.ContributionVolatility</sub>
4. **Watch.** Note from 29 Jul 2026: "Interested in a broader diversification across currencies."  
   <sub>clients.json CASE-032: ClientNotes</sub>
5. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
6. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>clients.json CASE-032: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Popeye is calling: no risk profile, ESG preference, CHF 23k across 1 portfolio.  
   <sub>clients.json CASE-032: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 321 today, −1.4% of the book. Mostly Information Technology, −4.8% on 10.8% of it.  
   <sub>impact of the market feed on clients.json CASE-032 holdings</sub>
3. **digest.** About −CHF 321 today, −1.4% of the book.  
   <sub>impact of the market feed on clients.json CASE-032 holdings</sub>
4. **digest.** About −CHF 121 from Information Technology, −4.8% today on 10.8% of the book, mostly CSIF (CH) I Equity World ex CH Blue and CSIF (CH) Equity World ex CH ESG Blue.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-032 holdings</sub>
5. **digest.** About −CHF 69 from the dollar, −1.2% against the franc on 24.4% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-032 holdings</sub>
6. **digest.** About −CHF 34 from Consumer Discretionary, −2.2% today on 6.5% of the book, mostly CSIF (CH) I Equity World ex CH Blue and Equities Switzerland Passive Leader.  
   <sub>market feed "tech-selloff": S5COND Index CHG_PCT_1D × clients.json CASE-032 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **holding.** Holding up today: Swiss franc bonds +0.2% (19.4% of the book); Consumer Staples +0.3% (6.8% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-032 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): ESG client: average sustainability score 7.3 of 10 against a minimum of 5.7; 2.9% of the book has no score.  
  <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-032 positions</sub>
- **Watch** (0.15): Financials is 14.5% of the book (CHF 3k) after fund look-through, mostly via iShares Swiss Dividend ETF (CH) and Equities Switzerland Passive Leader.  
  <sub>clients.json CASE-032: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.14): Health Care is 14.4% of the book (CHF 3k) after fund look-through, mostly via Equities Switzerland Passive Leader and iShares Swiss Dividend ETF (CH).  
  <sub>clients.json CASE-032: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 10 Sep 2025: "Annual review meeting held, no change to strategy desired."  
  <sub>clients.json CASE-032: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Pension (CASE-032-01), 3 Sep 2026: expected return 5.3%, value at risk 15.6%.  
  <sub>clients.json CASE-032: Portfolios[CASE-032-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 22.2% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-032: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 494, 2.1% of the book.  
  <sub>clients.json CASE-032: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 75.7% of the portfolio (CHF 18k).  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 19.4% of the portfolio (CHF 5k).  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 2.9% of the portfolio (CHF 678).  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 2.1% of the portfolio (CHF 494).  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 14.5% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 14.4% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 10.8% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 10.2% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 6.8% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 6.5% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 4.3% of the portfolio (CHF 999) after fund look-through.  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 4.2% of the portfolio (CHF 987) after fund look-through.  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 1.6% of the portfolio (CHF 370) after fund look-through.  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 1.5% of the portfolio (CHF 358) after fund look-through.  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.9% of the portfolio (CHF 207) after fund look-through.  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 23k).  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: CSIF (CH) I Equity World ex CH Blue, CHF 4k (18.7% of the portfolio).  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 11 holdings; the largest: CSIF (CH) I Equity World ex CH Blue (CHF 4k), Equities Switzerland Passive Leader (CHF 4k), CSIF (CH) Equity World ex CH ESG Blue (CHF 3k), iShares Swiss Dividend ETF (CH) (CHF 2k).  
  <sub>clients.json CASE-032: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-033 — Eric Cartman

Investor profile 5 · CHF 89k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Eric Cartman, Investor profile 5, CHF 89k across 1 portfolio.  
   <sub>clients.json CASE-033: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +19.7% over the 12 months to Jul 2026 and +38.7% since Oct 2021, now CHF 89k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-033: PerformanceHistory of CASE-033-01</sub>
3. **Health check.** 0 suitability errors and 3 warnings open; most serious: "Underweight in the equity sector "Consumer Staples"".  
   <sub>clients.json CASE-033: SuitabilityViolations</sub>
4. **Watch.** iShares Core S&P 500 UCITS ETF drives 22.9% of the volatility of Investment advisory (CASE-033-01).  
   <sub>clients.json CASE-033: Portfolios[CASE-033-01].SecurityPositions.ContributionVolatility</sub>
5. **Watch.** Note from 6 Jun 2025: "Prefers ESG-compliant investments, no defense or tobacco holdings."  
   <sub>clients.json CASE-033: ClientNotes</sub>
6. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "That means maintaining an overweight position in technology stocks."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
7. **Next best actions.** Follow up on the proposal of 29 Jun 2026 that was rejected (reason: Risk profile update); it would have had the client buy iShares Swiss Dividend ETF (CH) and sell CSIF (CH) Equity SPI ESG Multi Premia Blue.  
   <sub>clients.json CASE-033: Proposals[23490] × Transactions</sub>
8. **Next best actions.** Book a review: the last finalised proposal was on 7 Apr 2024.  
   <sub>clients.json CASE-033: Proposals.FinalizedDateUTC</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Eric Cartman is calling: Investor profile 5, CHF 89k across 1 portfolio.  
   <sub>clients.json CASE-033: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 979 today, −1.1% of the book. Mostly Information Technology, −4.8% on 10.7% of it.  
   <sub>impact of the market feed on clients.json CASE-033 holdings</sub>
3. **reason.** Possibly the proposal of 29 Jun 2026 that was rejected (reason: Risk profile update).  
   <sub>clients.json CASE-033: Proposals[23490]</sub>
4. **digest.** About −CHF 979 today, −1.1% of the book.  
   <sub>impact of the market feed on clients.json CASE-033 holdings</sub>
5. **digest.** About −CHF 459 from Information Technology, −4.8% today on 10.7% of the book, mostly iShares Core S&P 500 UCITS ETF and Credit Suisse (Lux) Robotics Equity Fund.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-033 holdings</sub>
6. **digest.** About −CHF 268 from the dollar, −1.2% against the franc on 25.0% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-033 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** About −CHF 78 from Consumer Discretionary, −2.2% today on 3.9% of the book, mostly iShares Core S&P 500 UCITS ETF and SLI (R).  
   <sub>market feed "tech-selloff": S5COND Index CHG_PCT_1D × clients.json CASE-033 holdings</sub>
10. **holding.** Global Investment Grade Credit Fund and Glob.High Yield Corp Bd CHF UCITS ETF (Dist) (17.7% of the book) are hedged to the franc, so the dollar move (−1.2%) does not reach them.  
   <sub>clients.json CASE-033: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>
11. **holding.** Holding up today: Swiss franc bonds +0.2% (35.3% of the book); foreign bonds +0.3% (7.7% of the book); Consumer Staples +0.3% (3.6% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-033 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): "Underweight in the equity sector "Consumer Staples"" means: Underweight (+/- 5% of the benchmark’s SAA target) in the Basic Consumer Goods equity sector  
  <sub>clients.json CASE-033: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Overweight in the equity sector "Information Technology"" means: Overweight (+/- 5% of the benchmark’s SAA target) in the Information Technology sector  
  <sub>clients.json CASE-033: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Overweight in the equity region "North America"" means: Overweight (+/- 5% of the benchmark’s SAA target) in the ‘North America’ equity region  
  <sub>clients.json CASE-033: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.11): Health Care is 11.2% of the book (CHF 10k) after fund look-through, mostly via SLI (R) and Credit Suisse (Lux) Digital Health Equity Fund.  
  <sub>clients.json CASE-033: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.11): Information Technology is 10.7% of the book (CHF 10k) after fund look-through, mostly via iShares Core S&P 500 UCITS ETF and Credit Suisse (Lux) Robotics Equity Fund.  
  <sub>clients.json CASE-033: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.05): Currency-hedged holdings: Global Investment Grade Credit Fund, Glob.High Yield Corp Bd CHF UCITS ETF (Dist) (17.7% of the book).  
  <sub>clients.json CASE-033: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Investment advisory (CASE-033-01), 3 Sep 2026: expected return 4.6%, value at risk 17.2%.  
  <sub>clients.json CASE-033: Portfolios[CASE-033-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 43.0% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-033: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 3k, 3.8% of the book.  
  <sub>clients.json CASE-033: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 53.2% of the portfolio (CHF 48k).  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 43.0% of the portfolio (CHF 38k).  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 3.8% of the portfolio (CHF 3k).  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 11.2% of the portfolio (CHF 10k) after fund look-through.  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 10.7% of the portfolio (CHF 10k) after fund look-through.  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 7.7% of the portfolio (CHF 7k) after fund look-through.  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 7.4% of the portfolio (CHF 7k) after fund look-through.  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 3.9% of the portfolio (CHF 4k) after fund look-through.  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 3.6% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 3.2% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 2.3% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 1.7% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.9% of the portfolio (CHF 760) after fund look-through.  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.5% of the portfolio (CHF 486) after fund look-through.  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 63.9% of the portfolio (CHF 57k).  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 33.4% of the portfolio (CHF 30k).  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 2.5% of the portfolio (CHF 2k).  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): SHIB: 0.3% of the portfolio (CHF 228).  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Crypto: CHF 228, 0.3% of the portfolio.  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares Core S&P 500 UCITS ETF, CHF 13k (14.4% of the portfolio).  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 12 holdings; the largest: iShares Core S&P 500 UCITS ETF (CHF 13k), BCV Swiss Franc Bonds (CHF 11k), SLI (R) (CHF 11k), Global Investment Grade Credit Fund (CHF 11k).  
  <sub>clients.json CASE-033: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.30): Resolve "Underweight in the equity sector "Consumer Staples"".  
  <sub>clients.json CASE-033: SuitabilityViolations[Id=610083]</sub>
- **Next best actions** (0.30): Resolve "Overweight in the equity sector "Information Technology"".  
  <sub>clients.json CASE-033: SuitabilityViolations[Id=610084]</sub>
- **Next best actions** (0.30): Resolve "Overweight in the equity region "North America"".  
  <sub>clients.json CASE-033: SuitabilityViolations[Id=865450]</sub>

</details>

---

## CASE-034 — Travis Bickle

Investor profile 6 · CHF 698k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Travis Bickle, Investor profile 6, CHF 698k across 1 portfolio.  
   <sub>clients.json CASE-034: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +25.5% over the 12 months to Jul 2026 and +28.7% since Oct 2021, now CHF 698k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-034: PerformanceHistory of CASE-034-01</sub>
3. **Health check.** 1 suitability error and 3 warnings open; most serious: "Volatility range undershot (portfolio risk too low)".  
   <sub>clients.json CASE-034: SuitabilityViolations</sub>
4. **Health check.** 5 of 6 orders from the proposal of 23 Dec 2025 were forwarded with a warning.  
   <sub>clients.json CASE-034: Transactions[ProposalId=19458].ForwardState = 2</sub>
5. **Watch.** Note from 22 Aug 2026: "Prefers semi-annual phone contact, no unannounced visits."  
   <sub>clients.json CASE-034: ClientNotes</sub>
6. **Watch.** Industrials is 12.8% of the book (CHF 89k) after fund look-through, mostly via Global Climate and Environment Fund and iShares Global Water UCITS ETF.  
   <sub>clients.json CASE-034: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "The AI-driven capex boom, and the need for infrastructure to support it, should support the outlook for industrials, another sector on which we have an overweight stance."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
8. **Next best actions.** Resolve "Volatility range undershot (portfolio risk too low)".  
   <sub>clients.json CASE-034: SuitabilityViolations[Id=920507]</sub>
9. **Next best actions.** Resolve "Underweight in the equity sector "Consumer Staples"".  
   <sub>clients.json CASE-034: SuitabilityViolations[Id=603413]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Travis Bickle is calling: Investor profile 6, CHF 698k across 1 portfolio.  
   <sub>clients.json CASE-034: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Contact preference: "Prefers semi-annual phone contact, no unannounced visits"  
   <sub>data/profiles/profiles.json CASE-034 from clients.json ClientNotes</sub>
3. **reason.** Probably the market: about −CHF 8k today, −1.1% of the book. Mostly Information Technology, −4.8% on 8.8% of it.  
   <sub>impact of the market feed on clients.json CASE-034 holdings</sub>
4. **digest.** About −CHF 8k today, −1.1% of the book.  
   <sub>impact of the market feed on clients.json CASE-034 holdings</sub>
5. **digest.** About −CHF 3k from Information Technology, −4.8% today on 8.8% of the book, mostly Xtrackers MSCI World ESG UCITS ETF and Global Climate and Environment Fund.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-034 holdings</sub>
6. **digest.** About −CHF 2k from the dollar, −1.2% against the franc on 27.3% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-034 holdings</sub>
7. **digest.** About −CHF 982 from Industrials, −1.1% today on 12.8% of the book, mostly Global Climate and Environment Fund and iShares Global Water UCITS ETF.  
   <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-034 holdings</sub>
8. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
10. **digest.** 9.5% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-034 holdings without a mapped market move</sub>
11. **holding.** Glob.High Yield Corp Bd CHF UCITS ETF (Dist) and SPDR Bloomberg Global Aggregate Bond UCITS ETF (7.2% of the book) are hedged to the franc, so the dollar move (−1.2%) does not reach them.  
   <sub>clients.json CASE-034: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>
12. **holding.** Holding up today: Swiss franc bonds +0.2% (26.2% of the book); Consumer Staples +0.3% (5.6% of the book); Utilities +0.5% (3.2% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-034 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): "Underweight in the equity sector "Consumer Staples"" means: Underweight (+/- 5% of the benchmark’s SAA target) in the Basic Consumer Goods equity sector  
  <sub>clients.json CASE-034: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Underweight in the equity sector "Health Care"" means: Underweight (+/- 5% of the SAA target for the Healthcare sector)  
  <sub>clients.json CASE-034: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Significant overweight in the equity sector "Industrials"" means: Significant overweight (+/- 10% of the SAA target for the ‘Industry’ equity sector)  
  <sub>clients.json CASE-034: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.11): Health Care is 11.0% of the book (CHF 77k) after fund look-through, mostly via MSCI Switzerland IMI Socially Responsible and SLI (R).  
  <sub>clients.json CASE-034: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 23 May 2026: "No direct positions in fossil fuels, please."  
  <sub>clients.json CASE-034: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (23 Dec 2025, reason: Change of investment strategy) ordered to buy Xtrackers MSCI World ESG UCITS ETF and BCV Swiss Franc Bonds and sell SPDR MSCI World Financials UCITS ETF, Rize Sustainable Future of Food UCITS ETF and 1 more.  
  <sub>clients.json CASE-034: Proposals[19458] × Transactions</sub>
- **Watch** (0.05): Currency-hedged holdings: Glob.High Yield Corp Bd CHF UCITS ETF (Dist), SPDR Bloomberg Global Aggregate Bond UCITS ETF (7.2% of the book).  
  <sub>clients.json CASE-034: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Individual pension (CASE-034-01), 3 Sep 2026: expected return 5.4%, value at risk 14.3%.  
  <sub>clients.json CASE-034: Portfolios[CASE-034-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.02): The rule "Sustainable investments only" is waived for this client by an individual override.  
  <sub>clients.json CASE-034: IndividualRuleOverrides</sub>
- **Watch** (0.00): 35.7% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-034: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 8k, 1.2% of the book.  
  <sub>clients.json CASE-034: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 63.2% of the portfolio (CHF 441k).  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 26.2% of the portfolio (CHF 183k).  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 7.7% of the portfolio (CHF 54k).  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 1.7% of the portfolio (CHF 12k).  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 1.2% of the portfolio (CHF 8k).  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Industrials is 12.8% of the portfolio (CHF 89k) after fund look-through.  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 11.0% of the portfolio (CHF 77k) after fund look-through.  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 9.2% of the portfolio (CHF 64k) after fund look-through.  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 8.8% of the portfolio (CHF 61k) after fund look-through.  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 5.6% of the portfolio (CHF 39k) after fund look-through.  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 4.7% of the portfolio (CHF 33k) after fund look-through.  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 3.9% of the portfolio (CHF 27k) after fund look-through.  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 3.2% of the portfolio (CHF 22k) after fund look-through.  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 2.0% of the portfolio (CHF 14k) after fund look-through.  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 1.9% of the portfolio (CHF 13k) after fund look-through.  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.1% of the portfolio (CHF 522) after fund look-through.  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 60.7% of the portfolio (CHF 424k).  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 29.2% of the portfolio (CHF 203k).  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 10.1% of the portfolio (CHF 71k).  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Crypto: CHF 36k, 5.1% of the portfolio.  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: MSCI Switzerland IMI Socially Responsible, CHF 56k (8.0% of the portfolio).  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 22 holdings; the largest: MSCI Switzerland IMI Socially Responsible (CHF 56k), iShares Listed Private Equity UCITS ETF (CHF 54k), SLI (R) (CHF 52k), CSIF (CH) Equity SPI ESG Multi Premia Blue (CHF 45k).  
  <sub>clients.json CASE-034: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.30): Resolve "Underweight in the equity sector "Health Care"".  
  <sub>clients.json CASE-034: SuitabilityViolations[Id=603414]</sub>
- **Next best actions** (0.21): Clear the warnings on the 5 flagged orders from the proposal of 23 Dec 2025.  
  <sub>clients.json CASE-034: Transactions[ProposalId=19458].ForwardState = 2</sub>

</details>

---

## CASE-035 — SpongeBob SquarePants

Investor profile 6 · CHF 741k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** SpongeBob SquarePants, Investor profile 6, CHF 741k across 1 portfolio.  
   <sub>clients.json CASE-035: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +27.7% over the 12 months to Jul 2026 and +59.5% since Oct 2021, now CHF 741k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-035: PerformanceHistory of CASE-035-01</sub>
3. **Health check.** 0 suitability errors and 1 warning open; most serious: "Underweight in the equity sector "Consumer Staples"".  
   <sub>clients.json CASE-035: SuitabilityViolations</sub>
4. **Health check.** 3 of 3 orders from the proposal of 3 May 2026 were forwarded with a warning.  
   <sub>clients.json CASE-035: Transactions[ProposalId=22110].ForwardState = 2</sub>
5. **Watch.** Health Care is 16.2% of the book (CHF 120k) after fund look-through, mostly via iShares Swiss Dividend ETF (CH) and iShares Core SPI(R) ETF (CH).  
   <sub>clients.json CASE-035: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Watch.** Note from 4 Feb 2026: "Prefers ESG-compliant investments, no defense or tobacco holdings."  
   <sub>clients.json CASE-035: ClientNotes</sub>
7. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "The AI-driven capex boom, and the need for infrastructure to support it, should support the outlook for industrials, another sector on which we have an overweight stance."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
8. **Next best actions.** Resolve "Underweight in the equity sector "Consumer Staples"".  
   <sub>clients.json CASE-035: SuitabilityViolations[Id=898024]</sub>
9. **Next best actions.** Clear the warnings on the 3 flagged orders from the proposal of 3 May 2026.  
   <sub>clients.json CASE-035: Transactions[ProposalId=22110].ForwardState = 2</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** SpongeBob SquarePants is calling: Investor profile 6, CHF 741k across 1 portfolio.  
   <sub>clients.json CASE-035: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Contact preference: "Prefers email communication, hard to reach by phone"  
   <sub>data/profiles/profiles.json CASE-035 from clients.json ClientNotes</sub>
3. **reason.** Probably the market: about −CHF 9k today, −1.2% of the book. Mostly Information Technology, −4.8% on 9.7% of it.  
   <sub>impact of the market feed on clients.json CASE-035 holdings</sub>
4. **reason.** Possibly reinvestment: 0.1525 % Cembra Money Bank AG 2019-14.10.26 matures on 14 Oct 2026 (CHF 14k).  
   <sub>clients.json CASE-035: SecurityPositions × reference.json Securities.MaturityDateUtc</sub>
5. **digest.** About −CHF 9k today, −1.2% of the book.  
   <sub>impact of the market feed on clients.json CASE-035 holdings</sub>
6. **digest.** About −CHF 3k from Information Technology, −4.8% today on 9.7% of the book, mostly iShares NASDAQ 100 UCITS ETF and iShares MSCI World CHF Hedged UCITS ETF (Acc).  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-035 holdings</sub>
7. **digest.** About −CHF 2k from the dollar, −1.2% against the franc on 20.5% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-035 holdings</sub>
8. **digest.** About −CHF 809 from Financials, −0.9% today on 12.1% of the book, mostly iShares Swiss Dividend ETF (CH) and iShares Core SPI(R) ETF (CH).  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-035 holdings</sub>
9. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
10. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
11. **holding.** Global Investment Grade Credit Fund and iShares MSCI World CHF Hedged UCITS ETF (Acc) and SPDR Bloomberg Global Aggregate Bond UCITS ETF (13.0% of the book) are hedged to the franc, so the dollar move (−1.2%) does not reach them.  
   <sub>clients.json CASE-035: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>
12. **holding.** Holding up today: Swiss franc bonds +0.2% (17.6% of the book); Consumer Staples +0.3% (8.1% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-035 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): "Underweight in the equity sector "Consumer Staples"" means: Underweight (+/- 5% of the benchmark’s SAA target) in the Basic Consumer Goods equity sector  
  <sub>clients.json CASE-035: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.14): Industrials is 14.1% of the book (CHF 105k) after fund look-through, mostly via 1.6 % Sulzer AG 2018-22.10.24 and 2 % Implenia AG 2021-26.11.25 Reg S.  
  <sub>clients.json CASE-035: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 10 Feb 2025: "Prefers semi-annual phone contact, no unannounced visits."  
  <sub>clients.json CASE-035: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (3 May 2026, reason: Risk profile update) ordered to buy iShares Swiss Dividend ETF (CH), SMIM (R) and 1 more.  
  <sub>clients.json CASE-035: Proposals[22110] × Transactions</sub>
- **Watch** (0.06): 11.3% of the book is in holdings on none of the bank's recommendation lists, largest 8.78 % Reverse Convertible UBS London 2023-19.08.24 on Straumann/Lonza Grp/VATGroup, 1.6 % Sulzer AG 2018-22.10.24 and 4 more.  
  <sub>reference.json Securities.InRecommendationList; clients.json CASE-035 positions</sub>
- **Watch** (0.05): Currency-hedged holdings: Global Investment Grade Credit Fund, iShares MSCI World CHF Hedged UCITS ETF (Acc), SPDR Bloomberg Global Aggregate Bond UCITS ETF (13.0% of the book).  
  <sub>clients.json CASE-035: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-035-01), 3 Sep 2026: expected return 5.4%, value at risk 12.6%.  
  <sub>clients.json CASE-035: Portfolios[CASE-035-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 27k, 3.7% of the book.  
  <sub>clients.json CASE-035: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 74.8% of the portfolio (CHF 554k).  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 17.6% of the portfolio (CHF 130k).  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 3.9% of the portfolio (CHF 29k).  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 3.7% of the portfolio (CHF 27k).  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 16.2% of the portfolio (CHF 120k) after fund look-through.  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 14.1% of the portfolio (CHF 105k) after fund look-through.  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 14.1% of the portfolio (CHF 104k) after fund look-through.  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 9.7% of the portfolio (CHF 72k) after fund look-through.  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 8.1% of the portfolio (CHF 60k) after fund look-through.  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 5.9% of the portfolio (CHF 44k) after fund look-through.  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 4.4% of the portfolio (CHF 33k) after fund look-through.  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 3.3% of the portfolio (CHF 24k) after fund look-through.  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 3.0% of the portfolio (CHF 22k) after fund look-through.  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 2.9% of the portfolio (CHF 22k) after fund look-through.  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 1.1% of the portfolio (CHF 8k) after fund look-through.  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 72.2% of the portfolio (CHF 534k).  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 27.8% of the portfolio (CHF 206k).  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares Swiss Dividend ETF (CH), CHF 100k (13.5% of the portfolio).  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 28 holdings; the largest: iShares Swiss Dividend ETF (CH) (CHF 100k), iShares MSCI World CHF Hedged UCITS ETF (Acc) (CHF 70k), iShares Core SPI(R) ETF (CH) (CHF 69k), iShares Edge MSCI World Value Factor UCITS ETF (CHF 58k).  
  <sub>clients.json CASE-035: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-036 — Peter Pan

Investor profile 7 · CHF 122k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Peter Pan, Investor profile 7, ESG preference, CHF 122k across 2 portfolios.  
   <sub>clients.json CASE-036: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Combined portfolio value +4.1% over the 12 months to Jul 2026 and −9.6% since Oct 2021, now CHF 122k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-036: PerformanceHistory of CASE-036-01, CASE-036-02</sub>
3. **Health check.** 4 suitability errors and 0 warnings open; most serious: "Volatility range undershot (portfolio risk too low)".  
   <sub>clients.json CASE-036: SuitabilityViolations</sub>
4. **Health check.** Liquidity in Investment advisory (CASE-036-02) at 100.0%, outside its 0.0%–60.0% band, target 3.0%.  
   <sub>clients.json CASE-036: Portfolios[CASE-036-02] positions; reference.json StrategicAssetAllocations[44] AssetClass "Liquidity"</sub>
5. **Watch.** Note from 26 Jul 2026: "Prefers CHF-hedged investments for foreign-currency positions."  
   <sub>clients.json CASE-036: ClientNotes</sub>
6. **Watch.** Note from 2 Sep 2025: "Prefers semi-annual phone contact, no unannounced visits."  
   <sub>clients.json CASE-036: ClientNotes</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Deploy idle liquidity: 82.2% of the book (CHF 100k) is cash.  
   <sub>clients.json CASE-036: LiquidityInDefaultCurrency</sub>
9. **Next best actions.** Rebalance Liquidity in Investment advisory (CASE-036-02) down toward 3.0%.  
   <sub>clients.json CASE-036: Portfolios[CASE-036-02] positions; reference.json StrategicAssetAllocations[44] AssetClass "Liquidity"</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Peter Pan is calling: Investor profile 7, ESG preference, CHF 122k across 2 portfolios.  
   <sub>clients.json CASE-036: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: wants it short. From the notes: "Prefers semi-annual phone contact, no unannounced visits."  
   <sub>data/profiles/profiles.json CASE-036 (apertus) from clients.json ClientNotes</sub>
3. **caller.** Contact preference: "Prefers semi-annual phone contact, no unannounced visits"  
   <sub>data/profiles/profiles.json CASE-036 from clients.json ClientNotes</sub>
4. **reason.** Probably idle cash: 82.2% of the book (CHF 100k) is cash.  
   <sub>clients.json CASE-036: LiquidityInDefaultCurrency</sub>
5. **digest.** About −CHF 408 today, −0.3% of the book.  
   <sub>impact of the market feed on clients.json CASE-036 holdings</sub>
6. **digest.** About −CHF 151 from Information Technology, −4.8% today on 2.6% of the book, mostly CSIF (CH) I Equity World ex CH Blue and CSIF (CH) Equity World ex CH ESG Blue.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-036 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** About −CHF 86 from the dollar, −1.2% against the franc on 5.9% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-036 holdings</sub>
10. **digest.** About −CHF 37 from Financials, −0.9% today on 3.4% of the book, mostly Equities Switzerland Passive Leader and iShares Swiss Dividend ETF (CH).  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-036 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (1.00): Shares in Investment advisory (CASE-036-02) at 0.0%, outside its 20.0%–85.0% band, target 50.0%.  
  <sub>clients.json CASE-036: Portfolios[CASE-036-02] positions; reference.json StrategicAssetAllocations[44] AssetClass "Shares"</sub>
- **Health check** (0.50): Bonds in Investment advisory (CASE-036-02) at 0.0%, outside its 10.0%–70.0% band, target 42.0%.  
  <sub>clients.json CASE-036: Portfolios[CASE-036-02] positions; reference.json StrategicAssetAllocations[44] AssetClass "Bonds"</sub>
- **Health check** (0.00): ESG client: average sustainability score 7.5 of 10 against a minimum of 5.7.  
  <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-036 positions</sub>
- **Health check** (0.00): "Minimum limit fixed income" means: Minimum limits interest rates  
  <sub>clients.json CASE-036: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Minimum limit shares" means: Minimum Limit Stocks  
  <sub>clients.json CASE-036: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Maximum limit liquidity" means: Maximum liquidity limits  
  <sub>clients.json CASE-036: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.05): Equities Switzerland Passive Leader drives 25.9% of the volatility of Pension (CASE-036-01).  
  <sub>clients.json CASE-036: Portfolios[CASE-036-01].SecurityPositions.ContributionVolatility</sub>
- **Watch** (0.03): Health Care is 3.4% of the book (CHF 4k) after fund look-through, mostly via Equities Switzerland Passive Leader and iShares Swiss Dividend ETF (CH).  
  <sub>clients.json CASE-036: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.03): Financials is 3.4% of the book (CHF 4k) after fund look-through, mostly via Equities Switzerland Passive Leader and iShares Swiss Dividend ETF (CH).  
  <sub>clients.json CASE-036: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.03): Risk engine for Pension (CASE-036-01), 3 Sep 2026: expected return 6.2%, value at risk 16.3%.  
  <sub>clients.json CASE-036: Portfolios[CASE-036-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 100k, 82.2% of the book.  
  <sub>clients.json CASE-036: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Cash is 82.2% of the portfolio (CHF 100k).  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Shares are 17.8% of the portfolio (CHF 22k).  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 3.4% of the portfolio (CHF 4k) after fund look-through.  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 3.4% of the portfolio (CHF 4k) after fund look-through.  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 2.6% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 2.4% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 1.6% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 1.6% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 1.0% of the portfolio (CHF 1k) after fund look-through.  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 1.0% of the portfolio (CHF 1k) after fund look-through.  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.4% of the portfolio (CHF 444) after fund look-through.  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.4% of the portfolio (CHF 440) after fund look-through.  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.2% of the portfolio (CHF 254) after fund look-through.  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 122k).  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: CSIF (CH) I Equity World ex CH Blue, CHF 5k (4.4% of the portfolio).  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 6 holdings; the largest: CSIF (CH) I Equity World ex CH Blue (CHF 5k), Equities Switzerland Passive Leader (CHF 5k), CSIF (CH) Equity World ex CH ESG Blue (CHF 4k), Index Equity Fund Small & Mid Caps Switzerland (CHF 3k).  
  <sub>clients.json CASE-036: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (1.00): Rebalance Shares in Investment advisory (CASE-036-02) up toward 50.0%.  
  <sub>clients.json CASE-036: Portfolios[CASE-036-02] positions; reference.json StrategicAssetAllocations[44] AssetClass "Shares"</sub>
- **Next best actions** (1.00): Resolve "Minimum limit fixed income".  
  <sub>clients.json CASE-036: SuitabilityViolations[Id=515472]</sub>
- **Next best actions** (1.00): Resolve "Minimum limit shares".  
  <sub>clients.json CASE-036: SuitabilityViolations[Id=515473]</sub>
- **Next best actions** (1.00): Resolve "Maximum limit liquidity".  
  <sub>clients.json CASE-036: SuitabilityViolations[Id=537182]</sub>
- **Next best actions** (0.50): Rebalance Bonds in Investment advisory (CASE-036-02) up toward 42.0%.  
  <sub>clients.json CASE-036: Portfolios[CASE-036-02] positions; reference.json StrategicAssetAllocations[44] AssetClass "Bonds"</sub>
- **Next best actions** (0.40): Book a review: no finalised proposal on record.  
  <sub>clients.json CASE-036: Proposals</sub>
- **Next best actions** (0.20): Candidates from the recommendation list for Shares: ABB Ltd and Kuehne + Nagel International AG (Shares is under its band).  
  <sub>reference.json RecommendationLists "Recommendation list free assets", not held, CHF first, ordered by SustainabilityScore</sub>

</details>

---

## CASE-037 — Grinch

Investor profile 5 · CHF 1.21m · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Grinch, Investor profile 5, ESG preference, CHF 1.21m across 2 portfolios.  
   <sub>clients.json CASE-037: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Combined portfolio value +31.2% over the 12 months to Jul 2026 and +76.5% since Oct 2021, now CHF 1.21m; value change including deposits and withdrawals.  
   <sub>clients.json CASE-037: PerformanceHistory of CASE-037-01, CASE-037-02</sub>
3. **Health check.** 0 suitability errors and 3 warnings open; most serious: "Underweight in the equity region "North America"".  
   <sub>clients.json CASE-037: SuitabilityViolations</sub>
4. **Health check.** ESG client: average sustainability score 7.1 of 10 against a minimum of 5.7; 4 holdings below the per-position minimum (1.878 % Hyundai Capital Services Inc 2022-14.06.27 Global, 0.875 % Hyundai Capital America Inc 2021-14.06.24 Reg S and 2 more, 8.4% of the book); 4.6% of the book has no score.  
   <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-037 positions</sub>
5. **Watch.** Note from 31 May 2026: "Also manages a family member's portfolio under a power of attorney."  
   <sub>clients.json CASE-037: ClientNotes</sub>
6. **Watch.** Financials is 14.4% of the book (CHF 174k) after fund look-through, mostly via iShares Swiss Dividend ETF (CH) and 0.395 % Macquarie Group Ltd 2021-20.07.28 Reg S.  
   <sub>clients.json CASE-037: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Resolve "Underweight in the equity region "North America"".  
   <sub>clients.json CASE-037: SuitabilityViolations[Id=598704]</sub>
9. **Next best actions.** Resolve "Overweight in the equity region "Rest of Europe"".  
   <sub>clients.json CASE-037: SuitabilityViolations[Id=608515]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Grinch is calling: Investor profile 5, ESG preference, CHF 1.21m across 2 portfolios.  
   <sub>clients.json CASE-037: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Contact preference: "Would like a follow-up call before any changes to the standing order"  
   <sub>data/profiles/profiles.json CASE-037 from clients.json ClientNotes</sub>
3. **reason.** Probably the market: about −CHF 10k today, −0.8% of the book. Mostly the dollar, −1.2% on 24.6% of it.  
   <sub>impact of the market feed on clients.json CASE-037 holdings</sub>
4. **reason.** Possibly reinvestment: 0.1525 % Cembra Money Bank AG 2019-14.10.26 matures on 14 Oct 2026 (CHF 19k).  
   <sub>clients.json CASE-037: SecurityPositions × reference.json Securities.MaturityDateUtc</sub>
5. **reason.** Possibly a sustainability concern: ESG client: average sustainability score 7.1 of 10 against a minimum of 5.7; 4 holdings below the per-position minimum (1.878 % Hyundai Capital Services Inc 2022-14.06.27 Global, 0.875 % Hyundai Capital America Inc 2021-14.06.24 Reg S and 2 more, 8.4% of the book); 4.6% of the book has no score.  
   <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-037 positions</sub>
6. **digest.** About −CHF 10k today, −0.8% of the book.  
   <sub>impact of the market feed on clients.json CASE-037 holdings</sub>
7. **digest.** About −CHF 4k from the dollar, −1.2% against the franc on 24.6% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-037 holdings</sub>
8. **digest.** About −CHF 3k from Information Technology, −4.8% today on 5.5% of the book, mostly iShares Edge MSCI World Value Factor UCITS ETF and iShares NASDAQ 100 UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-037 holdings</sub>
9. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
10. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
11. **digest.** About −CHF 1k from Financials, −0.9% today on 9.3% of the book, mostly iShares Swiss Dividend ETF (CH) and UBS Group AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-037 holdings</sub>
12. **digest.** 5.6% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-037 holdings without a mapped market move</sub>
13. **holding.** Vanguard Global Bond Index Fund and SPDR Bloomberg Global Aggregate Bond UCITS ETF (6.4% of the book) are hedged to the franc, so the dollar move (−1.2%) does not reach them.  
   <sub>clients.json CASE-037: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>
14. **holding.** Holding up today: Swiss franc bonds +0.2% (31.0% of the book); foreign bonds +0.3% (9.0% of the book); Consumer Staples +0.3% (8.3% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-037 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.15): 1 of 2 orders from the proposal of 19 Aug 2026 were forwarded with a warning.  
  <sub>clients.json CASE-037: Transactions[ProposalId=24779].ForwardState = 2</sub>
- **Health check** (0.00): "Underweight in the equity region "North America"" means: Underweight (+/- 5% of the SAA target for the ‘North America’ equity region)  
  <sub>clients.json CASE-037: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Overweight in the equity region "Rest of Europe"" means: Overweight (+/- 5% of the benchmark’s SAA target) in the ‘Rest of Europe’ equity region  
  <sub>clients.json CASE-037: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Underweight in the equity region "Asia/Pacific (ex Japan)"" means: Underweight (+/- 5% of the benchmark’s SAA target) in the ‘Asia/Pacific (ex Japan)’ equity region  
  <sub>clients.json CASE-037: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.14): iShares Edge MSCI World Value Factor UCITS ETF drives 17.1% of the volatility of Depository advisory (CASE-037-02).  
  <sub>clients.json CASE-037: Portfolios[CASE-037-02].SecurityPositions.ContributionVolatility</sub>
- **Watch** (0.14): Health Care is 13.9% of the book (CHF 169k) after fund look-through, mostly via SPDR MSCI World Health Care UCITS ETF and iShares Swiss Dividend ETF (CH).  
  <sub>clients.json CASE-037: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 26 Mar 2026: "No direct positions in fossil fuels, please."  
  <sub>clients.json CASE-037: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (19 Aug 2026, reason: Client called) ordered to buy iShares Edge MSCI World Value Factor UCITS ETF.  
  <sub>clients.json CASE-037: Proposals[24779] × Transactions</sub>
- **Watch** (0.08): 15.0% of the book is in holdings on none of the bank's recommendation lists, largest 1.878 % Hyundai Capital Services Inc 2022-14.06.27 Global, 2 % Implenia AG 2021-26.11.25 Reg S and 6 more.  
  <sub>reference.json Securities.InRecommendationList; clients.json CASE-037 positions</sub>
- **Watch** (0.05): Currency-hedged holdings: Vanguard Global Bond Index Fund, SPDR Bloomberg Global Aggregate Bond UCITS ETF (6.4% of the book).  
  <sub>clients.json CASE-037: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Pension (CASE-037-01), 3 Sep 2026: expected return 4.1%, value at risk 14.2%.  
  <sub>clients.json CASE-037: Portfolios[CASE-037-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-037-02), 3 Sep 2026: expected return 4.7%, value at risk 12.4%.  
  <sub>clients.json CASE-037: Portfolios[CASE-037-02].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.03): CSIF (CH) I Equity World ex CH Blue drives 17.1% of the volatility of Pension (CASE-037-01).  
  <sub>clients.json CASE-037: Portfolios[CASE-037-01].SecurityPositions.ContributionVolatility</sub>
- **Watch** (0.02): The rule "No structured products" is waived for this client by an individual override.  
  <sub>clients.json CASE-037: IndividualRuleOverrides</sub>
- **Watch** (0.00): 32.5% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-037: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 10k, 0.8% of the book.  
  <sub>clients.json CASE-037: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 53.7% of the portfolio (CHF 650k).  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 39.9% of the portfolio (CHF 483k).  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 4.6% of the portfolio (CHF 55k).  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 1.0% of the portfolio (CHF 13k).  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 0.8% of the portfolio (CHF 10k).  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 14.4% of the portfolio (CHF 174k) after fund look-through.  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 13.9% of the portfolio (CHF 169k) after fund look-through.  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 10.5% of the portfolio (CHF 127k) after fund look-through.  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 8.3% of the portfolio (CHF 101k) after fund look-through.  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 7.8% of the portfolio (CHF 94k) after fund look-through.  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 3.4% of the portfolio (CHF 41k) after fund look-through.  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 2.7% of the portfolio (CHF 32k) after fund look-through.  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 2.3% of the portfolio (CHF 28k) after fund look-through.  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 2.0% of the portfolio (CHF 24k) after fund look-through.  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.9% of the portfolio (CHF 10k) after fund look-through.  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.5% of the portfolio (CHF 7k) after fund look-through.  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 67.0% of the portfolio (CHF 811k).  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 29.1% of the portfolio (CHF 352k).  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 3.9% of the portfolio (CHF 48k).  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares Edge MSCI World Value Factor UCITS ETF, CHF 105k (8.7% of the portfolio).  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 48 holdings; the largest: iShares Edge MSCI World Value Factor UCITS ETF (CHF 105k), iShares Swiss Dividend ETF (CH) (CHF 81k), SPDR Bloomberg Global Aggregate Bond UCITS ETF (CHF 58k), iShares Core SPI(R) ETF (CH) (CHF 48k).  
  <sub>clients.json CASE-037: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.30): Resolve "Underweight in the equity region "Asia/Pacific (ex Japan)"".  
  <sub>clients.json CASE-037: SuitabilityViolations[Id=608516]</sub>
- **Next best actions** (0.12): Clear the warnings on the 1 flagged orders from the proposal of 19 Aug 2026.  
  <sub>clients.json CASE-037: Transactions[ProposalId=24779].ForwardState = 2</sub>

</details>

---

## CASE-038 — Charlie Brown

Investor profile 6 · CHF 1.62m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Charlie Brown, Investor profile 6, CHF 1.62m across 1 portfolio.  
   <sub>clients.json CASE-038: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +29.7% over the 12 months to Jul 2026 and +107.7% since Oct 2021, now CHF 1.62m; value change including deposits and withdrawals.  
   <sub>clients.json CASE-038: PerformanceHistory of CASE-038-02</sub>
3. **Health check.** 12 suitability errors and 6 warnings open; most serious: "Foreign currency cluster risk USD".  
   <sub>clients.json CASE-038: SuitabilityViolations</sub>
4. **Health check.** 3 of 6 orders from the proposal of 24 Aug 2026 were forwarded with a warning.  
   <sub>clients.json CASE-038: Transactions[ProposalId=23779].ForwardState = 2</sub>
5. **Watch.** Health Care is 20.5% of the book (CHF 332k) after fund look-through, mostly via Roche Holding AG and Novartis AG.  
   <sub>clients.json CASE-038: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Watch.** Novo Nordisk A/S drives 20.4% of the volatility of Depository advisory (CASE-038-02).  
   <sub>clients.json CASE-038: Portfolios[CASE-038-02].SecurityPositions.ContributionVolatility</sub>
7. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "The AI-driven capex boom, and the need for infrastructure to support it, should support the outlook for industrials, another sector on which we have an overweight stance."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
8. **Next best actions.** Resolve "Foreign currency cluster risk EUR".  
   <sub>clients.json CASE-038: SuitabilityViolations[Id=504883]</sub>
9. **Next best actions.** Resolve "Cluster risk of a single financial instrument" on iShares Core S&P 500 UCITS ETF.  
   <sub>clients.json CASE-038: SuitabilityViolations[Id=504884]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Charlie Brown is calling: Investor profile 6, CHF 1.62m across 1 portfolio.  
   <sub>clients.json CASE-038: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 19k today, −1.2% of the book. Mostly Information Technology, −4.8% on 8.7% of it.  
   <sub>impact of the market feed on clients.json CASE-038 holdings</sub>
3. **digest.** About −CHF 19k today, −1.2% of the book.  
   <sub>impact of the market feed on clients.json CASE-038 holdings</sub>
4. **digest.** About −CHF 7k from Information Technology, −4.8% today on 8.7% of the book, mostly iShares Core S&P 500 UCITS ETF and iShares NASDAQ 100 UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-038 holdings</sub>
5. **digest.** About −CHF 6k from the dollar, −1.2% against the franc on 29.1% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-038 holdings</sub>
6. **digest.** About −CHF 2k from Industrials, −1.1% today on 11.4% of the book, mostly Sulzer AG and Accelleron Industries AG.  
   <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-038 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** 6.3% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-038 holdings without a mapped market move</sub>
10. **holding.** iShares MSCI World CHF Hedged UCITS ETF (Acc) and SPDR Bloomberg Global Aggregate Bond UCITS ETF (3.4% of the book) are hedged to the franc, so the dollar move (−1.2%) does not reach them.  
   <sub>clients.json CASE-038: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>
11. **holding.** Holding up today: Consumer Staples +0.3% (11.6% of the book); Swiss franc bonds +0.2% (9.3% of the book); Gold +1.4% (5.9% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × clients.json CASE-038 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): "Foreign currency cluster risk EUR" means: For private customers, the EUR share should be < 9%.  
  <sub>clients.json CASE-038: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Cluster risk of a single financial instrument" means: For retail clients with financial services, comprehensive investment advisory or trx-based investment advisory must be single title share < x% (x varies with instrument type)  
  <sub>clients.json CASE-038: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Foreign currency exposure exceeds 50%" means: The entire foreign currency share in the portfolio is greater than 50%  
  <sub>clients.json CASE-038: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.16): Industrials is 15.7% of the book (CHF 255k) after fund look-through, mostly via Sulzer AG and Accelleron Industries AG.  
  <sub>clients.json CASE-038: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.15): Note from 11 Jul 2026: "Wants as high a weighting of sustainable funds as possible at the next rebalancing."  
  <sub>clients.json CASE-038: ClientNotes</sub>
- **Watch** (0.10): Note from 16 Jun 2026: "Requested a comparison against the benchmark at the next review."  
  <sub>clients.json CASE-038: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (24 Aug 2026, reason: Tax year-end rebalancing) ordered to buy iShares Core S&P 500 UCITS ETF, Kuehne + Nagel International AG and 2 more and sell SPDR MSCI World Financials UCITS ETF.  
  <sub>clients.json CASE-038: Proposals[23779] × Transactions</sub>
- **Watch** (0.07): 14.3% of the book is in holdings on none of the bank's recommendation lists, largest iShares Gold ETF (CH), Protection Participation Goldman Sachs International 2022-09.09.24 on SMI and 7 more.  
  <sub>reference.json Securities.InRecommendationList; clients.json CASE-038 positions</sub>
- **Watch** (0.05): Currency-hedged holdings: iShares MSCI World CHF Hedged UCITS ETF (Acc), SPDR Bloomberg Global Aggregate Bond UCITS ETF (3.4% of the book).  
  <sub>clients.json CASE-038: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-038-02), 3 Sep 2026: expected return 5.6%, value at risk 12.2%.  
  <sub>clients.json CASE-038: Portfolios[CASE-038-02].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 34k, 2.1% of the book.  
  <sub>clients.json CASE-038: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 76.3% of the portfolio (CHF 1.24m).  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 9.3% of the portfolio (CHF 151k).  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 9.0% of the portfolio (CHF 147k).  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 3.2% of the portfolio (CHF 53k).  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 2.1% of the portfolio (CHF 34k).  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 20.5% of the portfolio (CHF 332k) after fund look-through.  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 15.7% of the portfolio (CHF 255k) after fund look-through.  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 12.7% of the portfolio (CHF 206k) after fund look-through.  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 11.6% of the portfolio (CHF 187k) after fund look-through.  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 9.7% of the portfolio (CHF 156k) after fund look-through.  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 5.3% of the portfolio (CHF 85k) after fund look-through.  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 3.2% of the portfolio (CHF 52k) after fund look-through.  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 2.9% of the portfolio (CHF 47k) after fund look-through.  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 1.3% of the portfolio (CHF 21k) after fund look-through.  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 1.1% of the portfolio (CHF 17k) after fund look-through.  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.8% of the portfolio (CHF 14k) after fund look-through.  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 57.3% of the portfolio (CHF 928k).  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 33.9% of the portfolio (CHF 548k).  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 7.0% of the portfolio (CHF 114k).  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Andere: 1.8% of the portfolio (CHF 29k).  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Gold: CHF 96k, 5.9% of the portfolio.  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares Core S&P 500 UCITS ETF, CHF 237k (14.6% of the portfolio).  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 42 holdings; the largest: iShares Core S&P 500 UCITS ETF (CHF 237k), iShares Edge MSCI World Value Factor UCITS ETF (CHF 87k), Nestle SA (CHF 82k), iShares Swiss Dividend ETF (CH) (CHF 80k).  
  <sub>clients.json CASE-038: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (1.00): Resolve "Cluster risk of a single financial instrument" on Zurich Insurance Group AG.  
  <sub>clients.json CASE-038: SuitabilityViolations[Id=505015]</sub>
- **Next best actions** (0.12): Clear the warnings on the 3 flagged orders from the proposal of 24 Aug 2026.  
  <sub>clients.json CASE-038: Transactions[ProposalId=23779].ForwardState = 2</sub>

</details>

---

## CASE-039 — Rooster Cogburn

Investor profile 5 · CHF 170k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Rooster Cogburn, Investor profile 5, CHF 170k across 1 portfolio.  
   <sub>clients.json CASE-039: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +19.6% over the 12 months to Jul 2026 and +68.5% since Oct 2021, now CHF 170k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-039: PerformanceHistory of CASE-039-01</sub>
3. **Health check.** 0 suitability errors and 3 warnings open; most serious: "Underweight in the equity region "Switzerland"".  
   <sub>clients.json CASE-039: SuitabilityViolations</sub>
4. **Health check.** 6 of 8 orders from the proposal of 10 Feb 2026 were forwarded with a warning.  
   <sub>clients.json CASE-039: Transactions[ProposalId=20322].ForwardState = 2</sub>
5. **Watch.** Xtrackers MSCI World ESG UCITS ETF drives 21.6% of the volatility of Depository advisory (CASE-039-01).  
   <sub>clients.json CASE-039: Portfolios[CASE-039-01].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Health Care is 15.3% of the book (CHF 26k) after fund look-through, mostly via MSCI Switzerland IMI Socially Responsible and SPDR MSCI World Health Care UCITS ETF.  
   <sub>clients.json CASE-039: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Resolve "Underweight in the equity region "Switzerland"".  
   <sub>clients.json CASE-039: SuitabilityViolations[Id=719405]</sub>
9. **Next best actions.** Resolve "Underweight in the equity sector "Consumer Staples"".  
   <sub>clients.json CASE-039: SuitabilityViolations[Id=746362]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Rooster Cogburn is calling: Investor profile 5, CHF 170k across 1 portfolio.  
   <sub>clients.json CASE-039: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: wants it detailed. From the notes: "Appreciates a detailed written summary after every meeting."  
   <sub>data/profiles/profiles.json CASE-039 (apertus) from clients.json ClientNotes</sub>
3. **reason.** Probably the market: about −CHF 2k today, −1.2% of the book. Mostly Information Technology, −4.8% on 9.7% of it.  
   <sub>impact of the market feed on clients.json CASE-039 holdings</sub>
4. **digest.** About −CHF 2k today, −1.2% of the book.  
   <sub>impact of the market feed on clients.json CASE-039 holdings</sub>
5. **digest.** About −CHF 786 from Information Technology, −4.8% today on 9.7% of the book, mostly Xtrackers MSCI World ESG UCITS ETF and S&P 500 ESG ELITE UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-039 holdings</sub>
6. **digest.** About −CHF 487 from the dollar, −1.2% against the franc on 23.9% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-039 holdings</sub>
7. **digest.** About −CHF 176 from Financials, −0.9% today on 11.5% of the book, mostly Swiss Life Holding AG and MSCI Switzerland IMI Socially Responsible.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-039 holdings</sub>
8. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
10. **holding.** Holding up today: Swiss franc bonds +0.2% (34.4% of the book); Consumer Staples +0.3% (5.9% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-039 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): "Underweight in the equity region "Switzerland"" means: Underweight (+/- 5% of the benchmark’s SAA target) in the ‘Switzerland’ equity region  
  <sub>clients.json CASE-039: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Underweight in the equity sector "Consumer Staples"" means: Underweight (+/- 5% of the benchmark’s SAA target) in the Basic Consumer Goods equity sector  
  <sub>clients.json CASE-039: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Overweight in the equity region "North America"" means: Overweight (+/- 5% of the benchmark’s SAA target) in the ‘North America’ equity region  
  <sub>clients.json CASE-039: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.15): Note from 1 May 2026: "Prefers to avoid any exposure to fossil-fuel energy in the portfolio."  
  <sub>clients.json CASE-039: ClientNotes</sub>
- **Watch** (0.12): Financials is 11.5% of the book (CHF 20k) after fund look-through, mostly via Swiss Life Holding AG and MSCI Switzerland IMI Socially Responsible.  
  <sub>clients.json CASE-039: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 23 Oct 2025: "Prefers CHF-hedged investments for foreign-currency positions."  
  <sub>clients.json CASE-039: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (10 Feb 2026, reason: New deposit received) ordered to buy CHF Short Mid Term Bonds, iShares Core CHF Corporate Bond ETF (CH) and 4 more.  
  <sub>clients.json CASE-039: Proposals[20322] × Transactions</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-039-01), 3 Sep 2026: expected return 4.7%, value at risk 10.5%.  
  <sub>clients.json CASE-039: Portfolios[CASE-039-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.02): The rule "Sustainable investments only" is waived for this client by an individual override.  
  <sub>clients.json CASE-039: IndividualRuleOverrides</sub>
- **Watch** (0.00): 34.4% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-039: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 3k, 1.8% of the book.  
  <sub>clients.json CASE-039: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 63.8% of the portfolio (CHF 108k).  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 34.4% of the portfolio (CHF 58k).  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 1.8% of the portfolio (CHF 3k).  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 15.3% of the portfolio (CHF 26k) after fund look-through.  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 11.5% of the portfolio (CHF 20k) after fund look-through.  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 9.7% of the portfolio (CHF 16k) after fund look-through.  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 6.7% of the portfolio (CHF 11k) after fund look-through.  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 6.7% of the portfolio (CHF 11k) after fund look-through.  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 5.9% of the portfolio (CHF 10k) after fund look-through.  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 2.9% of the portfolio (CHF 5k) after fund look-through.  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 2.5% of the portfolio (CHF 4k) after fund look-through.  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 1.3% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 1.2% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.0% of the portfolio (CHF 39) after fund look-through.  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 64.2% of the portfolio (CHF 109k).  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 35.8% of the portfolio (CHF 61k).  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Xtrackers MSCI World ESG UCITS ETF, CHF 23k (13.8% of the portfolio).  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 15 holdings; the largest: Xtrackers MSCI World ESG UCITS ETF (CHF 23k), MSCI Switzerland IMI Socially Responsible (CHF 20k), CHF Short Mid Term Bonds (CHF 19k), iShares Core CHF Corporate Bond ETF (CH) (CHF 19k).  
  <sub>clients.json CASE-039: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.30): Resolve "Overweight in the equity region "North America"".  
  <sub>clients.json CASE-039: SuitabilityViolations[Id=854520]</sub>
- **Next best actions** (0.19): Clear the warnings on the 6 flagged orders from the proposal of 10 Feb 2026.  
  <sub>clients.json CASE-039: Transactions[ProposalId=20322].ForwardState = 2</sub>

</details>

---

## CASE-040 — Sam Malone

Investor profile 6 · CHF 800k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Sam Malone, Investor profile 6, CHF 800k across 1 portfolio.  
   <sub>clients.json CASE-040: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +13.9% over the 12 months to Jul 2026 and +60.8% since Oct 2021, now CHF 800k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-040: PerformanceHistory of CASE-040-01</sub>
3. **Health check.** 4 suitability errors and 1 warning open; most serious: "Knowledge of structured products" on 10.19 % Reverse Convertible UBS London 2023-26.08.24 on Straumann/Sonova/Lonza Grp.  
   <sub>clients.json CASE-040: SuitabilityViolations</sub>
4. **Health check.** 4 of 4 orders from the proposal of 8 Aug 2026 were forwarded with a warning.  
   <sub>clients.json CASE-040: Transactions[ProposalId=24401].ForwardState = 2</sub>
5. **Watch.** Health Care is 20.6% of the book (CHF 165k) after fund look-through, mostly via Lonza Group AG and Roche Holding AG.  
   <sub>clients.json CASE-040: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Watch.** Note from 5 May 2025: "Prefers to avoid any exposure to fossil-fuel energy in the portfolio."  
   <sub>clients.json CASE-040: ClientNotes</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Resolve "Significant overweight in the equity sector "Utilities"".  
   <sub>clients.json CASE-040: SuitabilityViolations[Id=609260]</sub>
9. **Next best actions.** Resolve "Underweight in the equity sector "Consumer Discretionary"".  
   <sub>clients.json CASE-040: SuitabilityViolations[Id=609262]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Sam Malone is calling: Investor profile 6, CHF 800k across 1 portfolio.  
   <sub>clients.json CASE-040: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Contact preference: "Hard to reach during the day, best contacted after 6pm"  
   <sub>data/profiles/profiles.json CASE-040 from clients.json ClientNotes</sub>
3. **reason.** Probably the market: about −CHF 11k today, −1.4% of the book. Mostly Information Technology, −4.8% on 10.8% of it.  
   <sub>impact of the market feed on clients.json CASE-040 holdings</sub>
4. **reason.** Possibly reinvestment: 0.1525 % Cembra Money Bank AG 2019-14.10.26 matures on 14 Oct 2026 (CHF 14k).  
   <sub>clients.json CASE-040: SecurityPositions × reference.json Securities.MaturityDateUtc</sub>
5. **digest.** About −CHF 11k today, −1.4% of the book.  
   <sub>impact of the market feed on clients.json CASE-040 holdings</sub>
6. **digest.** About −CHF 4k from Information Technology, −4.8% today on 10.8% of the book, mostly iShares NASDAQ 100 UCITS ETF and iShares Digital Security UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-040 holdings</sub>
7. **digest.** About −CHF 3k from the dollar, −1.2% against the franc on 35.0% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-040 holdings</sub>
8. **digest.** About −CHF 802 from Financials, −0.9% today on 11.1% of the book, mostly Swiss Re AG and Zurich Insurance Group AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-040 holdings</sub>
9. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
10. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
11. **holding.** SPDR Bloomberg Global Aggregate Bond UCITS ETF (4.4% of the book) is hedged to the franc, so the dollar move (−1.2%) does not reach it.  
   <sub>clients.json CASE-040: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>
12. **holding.** Holding up today: Swiss franc bonds +0.2% (11.7% of the book); Consumer Staples +0.3% (9.1% of the book); foreign bonds +0.3% (8.9% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-040 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): "Significant overweight in the equity sector "Utilities"" means: Significant overweight (+/- 10% of the benchmark’s SAA target) in the Utilities sector  
  <sub>clients.json CASE-040: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Underweight in the equity sector "Consumer Discretionary"" means: Underweight (+/- 5% of the benchmark’s SAA target) in the non-basic consumer goods equity sector  
  <sub>clients.json CASE-040: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Knowledge of structured products" means: For retail clients with financial services, comprehensive investment advisory or trx-based investment advisory must be available from K&E.  
  <sub>clients.json CASE-040: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.13): Financials is 12.9% of the book (CHF 104k) after fund look-through, mostly via Swiss Re AG and Zurich Insurance Group AG.  
  <sub>clients.json CASE-040: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 9 Dec 2024: "No direct positions in fossil fuels, please."  
  <sub>clients.json CASE-040: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (8 Aug 2026, reason: Change of risk tolerance) ordered to buy SPDR MSCI World Health Care UCITS ETF and BB Biotech AG and sell MIV Global Medtech Fund and Galenica AG.  
  <sub>clients.json CASE-040: Proposals[24401] × Transactions</sub>
- **Watch** (0.05): Currency-hedged holdings: SPDR Bloomberg Global Aggregate Bond UCITS ETF (4.4% of the book).  
  <sub>clients.json CASE-040: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-040-01), 3 Sep 2026: expected return 5.5%, value at risk 11.8%.  
  <sub>clients.json CASE-040: Portfolios[CASE-040-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 12k, 1.5% of the book.  
  <sub>clients.json CASE-040: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 75.4% of the portfolio (CHF 603k).  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 20.6% of the portfolio (CHF 164k).  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 2.5% of the portfolio (CHF 20k).  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 1.5% of the portfolio (CHF 12k).  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 20.6% of the portfolio (CHF 165k) after fund look-through.  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 12.9% of the portfolio (CHF 104k) after fund look-through.  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 11.2% of the portfolio (CHF 90k) after fund look-through.  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 11.0% of the portfolio (CHF 88k) after fund look-through.  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 10.8% of the portfolio (CHF 87k) after fund look-through.  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 4.6% of the portfolio (CHF 37k) after fund look-through.  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 3.1% of the portfolio (CHF 25k) after fund look-through.  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 2.5% of the portfolio (CHF 20k) after fund look-through.  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 1.7% of the portfolio (CHF 14k) after fund look-through.  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 1.2% of the portfolio (CHF 9k) after fund look-through.  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 1.1% of the portfolio (CHF 9k) after fund look-through.  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 54.2% of the portfolio (CHF 434k).  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 45.8% of the portfolio (CHF 367k).  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares Core S&P 500 UCITS ETF, CHF 64k (8.0% of the portfolio).  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 28 holdings; the largest: iShares Core S&P 500 UCITS ETF (CHF 64k), iShares NASDAQ 100 UCITS ETF (CHF 47k), FTSE All-World High Dividend Yield UCITS ETF (CHF 47k), iShares Edge MSCI World Value Factor UCITS ETF (CHF 46k).  
  <sub>clients.json CASE-040: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (1.00): Resolve "Knowledge of structured products" on 10.19 % Reverse Convertible UBS London 2023-26.08.24 on Straumann/Sonova/Lonza Grp.  
  <sub>clients.json CASE-040: SuitabilityViolations[Id=700639]</sub>
- **Next best actions** (0.25): Clear the warnings on the 4 flagged orders from the proposal of 8 Aug 2026.  
  <sub>clients.json CASE-040: Transactions[ProposalId=24401].ForwardState = 2</sub>

</details>

---

## CASE-041 — Company 004 AG

Investor profile 5 · CHF 608k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Company 004 AG, Investor profile 5, CHF 608k across 1 portfolio.  
   <sub>clients.json CASE-041: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +24.9% over the 12 months to Jul 2026 and +33.0% since Oct 2021, now CHF 608k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-041: PerformanceHistory of CASE-041-01</sub>
3. **Health check.** 6 suitability errors and 6 warnings open; most serious: "Significant underweight in the equity region "North America"".  
   <sub>clients.json CASE-041: SuitabilityViolations</sub>
4. **Health check.** 3 of 3 orders from the proposal of 15 Apr 2026 were forwarded with a warning.  
   <sub>clients.json CASE-041: Transactions[ProposalId=21880].ForwardState = 2</sub>
5. **Watch.** 1.25 % National Australia Bank Ltd 2016-18.05.26 Guaranteed Global Series 957 Reg S drives 586060588.5% of the volatility of Depository advisory (CASE-041-01).  
   <sub>clients.json CASE-041: Portfolios[CASE-041-01].SecurityPositions.ContributionVolatility</sub>
6. **Watch.** Financials is 23.4% of the book (CHF 142k) after fund look-through, mostly via 0.125 % Goldman Sachs Group Inc 2019-19.08.24 Reg S and 1.25 % National Australia Bank Ltd 2016-18.05.26 Guaranteed Global Series 957 Reg S.  
   <sub>clients.json CASE-041: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Resolve "Significant underweight in the equity region "North America"".  
   <sub>clients.json CASE-041: SuitabilityViolations[Id=617811]</sub>
9. **Next best actions.** Resolve "Foreign currency cluster risk EUR".  
   <sub>clients.json CASE-041: SuitabilityViolations[Id=617812]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Company 004 AG is calling: Investor profile 5, CHF 608k across 1 portfolio.  
   <sub>clients.json CASE-041: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably reinvestment: 0.25 % E.ON SE 2019-24.10.26 matures on 24 Oct 2026 (CHF 36k).  
   <sub>clients.json CASE-041: SecurityPositions × reference.json Securities.MaturityDateUtc</sub>
3. **digest.** About −CHF 1k today, −0.2% of the book.  
   <sub>impact of the market feed on clients.json CASE-041 holdings</sub>
4. **digest.** About −CHF 1k from the euro, −0.3% against the franc on 65.9% of the book.  
   <sub>market feed "tech-selloff": EURCHF Curncy CHG_PCT_1D × clients.json CASE-041 holdings</sub>
5. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
6. **digest.** About −CHF 595 from Financials, −0.9% today on 10.9% of the book, mostly Swiss Life Holding AG and Swiss Re AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-041 holdings</sub>
7. **digest.** About −CHF 354 from Industrials, −1.1% today on 5.3% of the book, mostly ABB Ltd and SMIM (R).  
   <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-041 holdings</sub>
8. **holding.** Holding up today: foreign bonds +0.3% (53.4% of the book); Gold +1.4% (6.3% of the book); Consumer Staples +0.3% (4.5% of the book).  
   <sub>market feed "tech-selloff": LEGATRUU Index CHG_PCT_1D × clients.json CASE-041 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): "Significant underweight in the equity region "North America"" means: Significant underweight (+/- 10% of the SAA target for the ‘North America’ equity region)  
  <sub>clients.json CASE-041: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Foreign currency cluster risk EUR" means: For private customers, the EUR share should be < 9%.  
  <sub>clients.json CASE-041: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Foreign currency exposure exceeds 50%" means: The entire foreign currency share in the portfolio is greater than 50%  
  <sub>clients.json CASE-041: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.19): Health Care is 19.4% of the book (CHF 118k) after fund look-through, mostly via 1.875 % Fresenius SE & Co. KGaA 2019-15.02.25 and Lonza Group AG.  
  <sub>clients.json CASE-041: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.19): 37.3% of the book is in holdings on none of the bank's recommendation lists, largest 1.5 % Volkswagen Financial Services AG 2019-01.10.24 Series F05/19, 1.875 % Fresenius SE & Co. KGaA 2019-15.02.25 and 6 more.  
  <sub>reference.json Securities.InRecommendationList; clients.json CASE-041 positions</sub>
- **Watch** (0.15): Note from 6 May 2025: "Annual review meeting held, no change to strategy desired."  
  <sub>clients.json CASE-041: ClientNotes</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-041-01), 3 Sep 2026: expected return 4.2%, value at risk 13.4%.  
  <sub>clients.json CASE-041: Portfolios[CASE-041-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 32.0% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-041: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 19k, 3.1% of the book.  
  <sub>clients.json CASE-041: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Bonds are 59.8% of the portfolio (CHF 363k).  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Shares are 37.2% of the portfolio (CHF 226k).  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 3.1% of the portfolio (CHF 19k).  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Financials is 23.4% of the portfolio (CHF 142k) after fund look-through.  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 19.4% of the portfolio (CHF 118k) after fund look-through.  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 6.7% of the portfolio (CHF 41k) after fund look-through.  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 5.3% of the portfolio (CHF 32k) after fund look-through.  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 4.5% of the portfolio (CHF 27k) after fund look-through.  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 4.0% of the portfolio (CHF 24k) after fund look-through.  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 0.8% of the portfolio (CHF 5k) after fund look-through.  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.4% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 0.3% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 0.2% of the portfolio (CHF 947) after fund look-through.  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.1% of the portfolio (CHF 458) after fund look-through.  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Euro: 65.9% of the portfolio (CHF 401k).  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Swiss francs: 34.1% of the portfolio (CHF 207k).  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Gold: CHF 38k, 6.3% of the portfolio.  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares EUR Corp Bond Large Cap UCITS ETF, CHF 59k (9.8% of the portfolio).  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 23 holdings; the largest: iShares EUR Corp Bond Large Cap UCITS ETF (CHF 59k), 1.5 % Volkswagen Financial Services AG 2019-01.10.24 Series F05/19 (CHF 39k), 0.125 % Nordic Investment Bank 2016-10.06.24 Reg S (CHF 39k), 0.125 % Goldman Sachs Group Inc 2019-19.08.24 Reg S (CHF 38k).  
  <sub>clients.json CASE-041: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (1.00): Resolve "Foreign currency exposure exceeds 50%".  
  <sub>clients.json CASE-041: SuitabilityViolations[Id=617813]</sub>
- **Next best actions** (0.25): Clear the warnings on the 3 flagged orders from the proposal of 15 Apr 2026.  
  <sub>clients.json CASE-041: Transactions[ProposalId=21880].ForwardState = 2</sub>

</details>

---

## CASE-042 — Zorro

Investor profile 4 · CHF 528k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Zorro, Investor profile 4, CHF 528k across 1 portfolio.  
   <sub>clients.json CASE-042: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +21.5% over the 12 months to Jul 2026 and +82.6% since Oct 2021, now CHF 528k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-042: PerformanceHistory of CASE-042-01</sub>
3. **Health check.** 2 suitability errors and 4 warnings open; most serious: "Cluster risk of a single financial instrument" on BB Biotech AG.  
   <sub>clients.json CASE-042: SuitabilityViolations</sub>
4. **Health check.** Volatility is 11.9%, above the 10.0% maximum of Investor profile 4.  
   <sub>clients.json CASE-042: Portfolios[CASE-042-01].Volatility; reference.json RiskProfiles.MaxVola</sub>
5. **Watch.** Health Care is 26.5% of the book (CHF 140k) after fund look-through, mostly via BB Biotech AG and GSK PLC.  
   <sub>clients.json CASE-042: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Watch.** BB Biotech AG drives 23.3% of the volatility of Depository advisory (CASE-042-01).  
   <sub>clients.json CASE-042: Portfolios[CASE-042-01].SecurityPositions.ContributionVolatility</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Resolve "Cluster risk of a single financial instrument" on BB Biotech AG.  
   <sub>clients.json CASE-042: SuitabilityViolations[Id=670470]</sub>
9. **Next best actions.** Resolve "Cluster risk of a single financial instrument" on GSK PLC.  
   <sub>clients.json CASE-042: SuitabilityViolations[Id=694946]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Zorro is calling: Investor profile 4, CHF 528k across 1 portfolio.  
   <sub>clients.json CASE-042: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 6k today, −1.2% of the book. Mostly Information Technology, −4.8% on 8.4% of it.  
   <sub>impact of the market feed on clients.json CASE-042 holdings</sub>
3. **reason.** Possibly reinvestment: 0.1525 % Cembra Money Bank AG 2019-14.10.26 matures on 14 Oct 2026 (CHF 14k).  
   <sub>clients.json CASE-042: SecurityPositions × reference.json Securities.MaturityDateUtc</sub>
4. **digest.** About −CHF 6k today, −1.2% of the book.  
   <sub>impact of the market feed on clients.json CASE-042 holdings</sub>
5. **digest.** About −CHF 2k from Information Technology, −4.8% today on 8.4% of the book, mostly iShares Automation & Robotics UCITS ETF and iShares Core S&P 500 UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-042 holdings</sub>
6. **digest.** About −CHF 2k from the dollar, −1.2% against the franc on 26.8% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-042 holdings</sub>
7. **digest.** About −CHF 725 from Consumer Discretionary, −2.2% today on 6.2% of the book, mostly mobilezone holding ag and iShares Core EURO STOXX 50 UCITS ETF.  
   <sub>market feed "tech-selloff": S5COND Index CHG_PCT_1D × clients.json CASE-042 holdings</sub>
8. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
10. **holding.** Holding up today: Consumer Staples +0.3% (9.8% of the book); foreign bonds +0.3% (8.5% of the book); Swiss franc bonds +0.2% (8.4% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × clients.json CASE-042 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.15): 21 of 22 orders from the proposal of 29 Dec 2025 were forwarded with a warning.  
  <sub>clients.json CASE-042: Transactions[ProposalId=19562].ForwardState = 2</sub>
- **Health check** (0.04): 1 holding above the product risk class limit of Investor profile 4 (maximum 6): Global Clean Energy UCITS ETF, 2.0% of the book.  
  <sub>reference.json Securities.PRC vs RiskProfiles.MaxPRC; clients.json CASE-042 positions</sub>
- **Health check** (0.00): "Cluster risk of a single financial instrument" means: For retail clients with financial services, comprehensive investment advisory or trx-based investment advisory must be single title share < x% (x varies with instrument type)  
  <sub>clients.json CASE-042: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Compliance with maximum volatility" means: For retail clients with financial services Comprehensive investment advisory or discretionary mandate must be PF Vola < max client profile Vola.  
  <sub>clients.json CASE-042: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Overweight in the equity region "Switzerland"" means: Overweight (+/- 5% of the benchmark’s SAA target) in the ‘Switzerland’ equity region  
  <sub>clients.json CASE-042: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.15): Financials is 15.0% of the book (CHF 79k) after fund look-through, mostly via Swiss Life Holding AG and Zurich Insurance Group AG.  
  <sub>clients.json CASE-042: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.15): Note from 4 Feb 2026: "Open to increasing the equity allocation if markets remain stable."  
  <sub>clients.json CASE-042: ClientNotes</sub>
- **Watch** (0.14): BB Biotech AG alone is 13.8% of the book.  
  <sub>clients.json CASE-042: Portfolios[CASE-042-01].SecurityPositions</sub>
- **Watch** (0.10): Note from 3 Sep 2025: "Was informed of the risks of structured products and explicitly accepts them."  
  <sub>clients.json CASE-042: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (29 Dec 2025, reason: New deposit received) ordered to buy BB Biotech AG, GSK PLC and 19 more.  
  <sub>clients.json CASE-042: Proposals[19562] × Transactions</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-042-01), 3 Sep 2026: expected return 5.6%, value at risk 11.7%.  
  <sub>clients.json CASE-042: Portfolios[CASE-042-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 14k, 2.6% of the book.  
  <sub>clients.json CASE-042: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 80.5% of the portfolio (CHF 425k).  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 16.9% of the portfolio (CHF 89k).  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 2.6% of the portfolio (CHF 14k).  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 26.5% of the portfolio (CHF 140k) after fund look-through.  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 15.0% of the portfolio (CHF 79k) after fund look-through.  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 9.8% of the portfolio (CHF 52k) after fund look-through.  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 8.8% of the portfolio (CHF 47k) after fund look-through.  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 8.4% of the portfolio (CHF 45k) after fund look-through.  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 6.0% of the portfolio (CHF 32k) after fund look-through.  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 5.4% of the portfolio (CHF 29k) after fund look-through.  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 1.8% of the portfolio (CHF 10k) after fund look-through.  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 1.6% of the portfolio (CHF 8k) after fund look-through.  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 1.5% of the portfolio (CHF 8k) after fund look-through.  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.8% of the portfolio (CHF 4k) after fund look-through.  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 52.9% of the portfolio (CHF 279k).  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 33.6% of the portfolio (CHF 177k).  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Andere: 8.6% of the portfolio (CHF 45k).  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 5.0% of the portfolio (CHF 26k).  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: BB Biotech AG, CHF 73k (13.8% of the portfolio).  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 21 holdings; the largest: BB Biotech AG (CHF 73k), GSK PLC (CHF 45k), iShares Core S&P 500 UCITS ETF (CHF 40k), SMIM (R) (CHF 39k).  
  <sub>clients.json CASE-042: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.30): Resolve "Compliance with maximum volatility".  
  <sub>clients.json CASE-042: SuitabilityViolations[Id=657307]</sub>
- **Next best actions** (0.24): Clear the warnings on the 21 flagged orders from the proposal of 29 Dec 2025.  
  <sub>clients.json CASE-042: Transactions[ProposalId=19562].ForwardState = 2</sub>

</details>

---

## CASE-043 — Waldo

Investor profile 6 · CHF 891k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Waldo, Investor profile 6, CHF 891k across 1 portfolio.  
   <sub>clients.json CASE-043: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +18.5% over the 12 months to Jul 2026 and +42.2% since Oct 2021, now CHF 891k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-043: PerformanceHistory of CASE-043-01</sub>
3. **Health check.** 21 of 22 orders from the proposal of 15 Sep 2026 were forwarded with a warning.  
   <sub>clients.json CASE-043: Transactions[ProposalId=25304].ForwardState = 2</sub>
4. **Watch.** Health Care is 18.1% of the book (CHF 161k) after fund look-through, mostly via SPDR MSCI World Health Care UCITS ETF and Lonza Group AG.  
   <sub>clients.json CASE-043: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
5. **Watch.** Note from 22 Apr 2026: "Interested in structured products, initial consultation already held."  
   <sub>clients.json CASE-043: ClientNotes</sub>
6. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "The AI-driven capex boom, and the need for infrastructure to support it, should support the outlook for industrials, another sector on which we have an overweight stance."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
7. **Next best actions.** Clear the warnings on the 21 flagged orders from the proposal of 15 Sep 2026.  
   <sub>clients.json CASE-043: Transactions[ProposalId=25304].ForwardState = 2</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Waldo is calling: Investor profile 6, CHF 891k across 1 portfolio.  
   <sub>clients.json CASE-043: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 12k today, −1.4% of the book. Mostly Information Technology, −4.8% on 9.6% of it.  
   <sub>impact of the market feed on clients.json CASE-043 holdings</sub>
3. **digest.** About −CHF 12k today, −1.4% of the book.  
   <sub>impact of the market feed on clients.json CASE-043 holdings</sub>
4. **digest.** About −CHF 4k from Information Technology, −4.8% today on 9.6% of the book, mostly iShares NASDAQ 100 UCITS ETF and iShares Core S&P 500 UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-043 holdings</sub>
5. **digest.** About −CHF 3k from the dollar, −1.2% against the franc on 25.3% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-043 holdings</sub>
6. **digest.** About −CHF 1k from Consumer Discretionary, −2.2% today on 6.9% of the book, mostly CIE FINANCIERE RICHEMONT SA and iShares MSCI World CHF Hedged UCITS ETF (Acc).  
   <sub>market feed "tech-selloff": S5COND Index CHG_PCT_1D × clients.json CASE-043 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **holding.** iShares MSCI World CHF Hedged UCITS ETF (Acc) and SPDR Bloomberg Global Aggregate Bond UCITS ETF (14.8% of the book) are hedged to the franc, so the dollar move (−1.2%) does not reach them.  
   <sub>clients.json CASE-043: SecurityPositions.SecurityName (hedged share class); market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D</sub>
10. **holding.** Holding up today: Swiss franc bonds +0.2% (16.9% of the book); Consumer Staples +0.3% (8.4% of the book); foreign bonds +0.3% (5.6% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-043 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.14): Industrials is 13.9% of the book (CHF 124k) after fund look-through, mostly via ABB Ltd and 2.875 % OC Oerlikon Corporation AG, Pfaeffikon 2023-02.06.26 Tranche 1.  
  <sub>clients.json CASE-043: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Note from 27 Nov 2025: "Wants a focus on high-dividend stocks for ongoing income generation."  
  <sub>clients.json CASE-043: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (15 Sep 2026, reason: Change of risk tolerance) ordered to buy iShares MSCI World CHF Hedged UCITS ETF (Acc), iShares NASDAQ 100 UCITS ETF and 17 more and sell Galenica AG and Orior AG.  
  <sub>clients.json CASE-043: Proposals[25304] × Transactions</sub>
- **Watch** (0.05): Currency-hedged holdings: iShares MSCI World CHF Hedged UCITS ETF (Acc), SPDR Bloomberg Global Aggregate Bond UCITS ETF (14.8% of the book).  
  <sub>clients.json CASE-043: SecurityPositions.SecurityName</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-043-01), 3 Sep 2026: expected return 5.5%, value at risk 14.3%.  
  <sub>clients.json CASE-043: Portfolios[CASE-043-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 5k, 0.6% of the book.  
  <sub>clients.json CASE-043: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 77.0% of the portfolio (CHF 686k).  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 22.4% of the portfolio (CHF 200k).  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 0.6% of the portfolio (CHF 5k).  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 18.1% of the portfolio (CHF 161k) after fund look-through.  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 13.9% of the portfolio (CHF 124k) after fund look-through.  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 9.6% of the portfolio (CHF 86k) after fund look-through.  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 8.7% of the portfolio (CHF 77k) after fund look-through.  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 8.4% of the portfolio (CHF 75k) after fund look-through.  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 6.9% of the portfolio (CHF 61k) after fund look-through.  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 6.4% of the portfolio (CHF 57k) after fund look-through.  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 4.9% of the portfolio (CHF 44k) after fund look-through.  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 1.3% of the portfolio (CHF 11k) after fund look-through.  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.9% of the portfolio (CHF 8k) after fund look-through.  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.8% of the portfolio (CHF 8k) after fund look-through.  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 62.8% of the portfolio (CHF 560k).  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 32.3% of the portfolio (CHF 287k).  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 4.9% of the portfolio (CHF 44k).  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares MSCI World CHF Hedged UCITS ETF (Acc), CHF 83k (9.4% of the portfolio).  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 24 holdings; the largest: iShares MSCI World CHF Hedged UCITS ETF (Acc) (CHF 83k), iShares Core S&P 500 UCITS ETF (CHF 74k), iShares Core SPI(R) ETF (CH) (CHF 55k), SMIM (R) (CHF 52k).  
  <sub>clients.json CASE-043: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-044 — Ralph Kramden

Investor profile 6 · CHF 172k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Ralph Kramden, Investor profile 6, ESG preference, CHF 172k across 1 portfolio.  
   <sub>clients.json CASE-044: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +18.1% over the 12 months to Jul 2026 and +50.8% since Oct 2021, now CHF 172k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-044: PerformanceHistory of CASE-044-01</sub>
3. **Health check.** 4 suitability errors and 8 warnings open; most serious: "Cluster risk of a single financial instrument" on GSC Green Tech ESG Fund.  
   <sub>clients.json CASE-044: SuitabilityViolations</sub>
4. **Health check.** 6 of 6 orders from the proposal of 8 Jul 2026 were forwarded with a warning.  
   <sub>clients.json CASE-044: Transactions[ProposalId=22767].ForwardState = 2</sub>
5. **Watch.** Note from 20 Mar 2026: "Prefers to keep a cash reserve on hand for unexpected medical expenses."  
   <sub>clients.json CASE-044: ClientNotes</sub>
6. **Watch.** Industrials is 25.5% of the book (CHF 44k) after fund look-through, mostly via GSC Green Tech ESG Fund and Georg Fischer AG.  
   <sub>clients.json CASE-044: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "The AI-driven capex boom, and the need for infrastructure to support it, should support the outlook for industrials, another sector on which we have an overweight stance."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
8. **Next best actions.** Resolve "Compliance with maximum volatility".  
   <sub>clients.json CASE-044: SuitabilityViolations[Id=797846]</sub>
9. **Next best actions.** Resolve "Knowledge of portfolio funds and mixed funds" on Shs Global X Data Center REITs & Digital Infrastructure ETF.  
   <sub>clients.json CASE-044: SuitabilityViolations[Id=797859]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Ralph Kramden is calling: Investor profile 6, ESG preference, CHF 172k across 1 portfolio.  
   <sub>clients.json CASE-044: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: wants it detailed. From the notes: "Asked for more detail on transaction fees at the next meeting."  
   <sub>data/profiles/profiles.json CASE-044 (apertus) from clients.json ClientNotes</sub>
3. **caller.** Contact preference: "Prefers not to be contacted during business hours on weekdays"  
   <sub>data/profiles/profiles.json CASE-044 from clients.json ClientNotes</sub>
4. **reason.** Probably the market: about −CHF 1k today, −0.8% of the book. Mostly Industrials, −1.1% on 25.5% of it.  
   <sub>impact of the market feed on clients.json CASE-044 holdings</sub>
5. **reason.** Possibly a sustainability concern: ESG client: average sustainability score 7.6 of 10 against a minimum of 5.7; 1 holding below the per-position minimum (Meyer Burger Technology AG, 0.0% of the book); 29.3% of the book has no score.  
   <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-044 positions</sub>
6. **reason.** Possibly idle cash: 22.6% of the book (CHF 39k) is cash.  
   <sub>clients.json CASE-044: LiquidityInDefaultCurrency</sub>
7. **digest.** About −CHF 1k today, −0.8% of the book.  
   <sub>impact of the market feed on clients.json CASE-044 holdings</sub>
8. **digest.** About −CHF 484 from Industrials, −1.1% today on 25.5% of the book, mostly GSC Green Tech ESG Fund and Georg Fischer AG.  
   <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-044 holdings</sub>
9. **digest.** About −CHF 468 from the dollar, −1.2% against the franc on 22.6% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-044 holdings</sub>
10. **digest.** About −CHF 270 from Information Technology, −4.8% today on 3.3% of the book, mostly GSC Green Tech ESG Fund and SMI (R).  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-044 holdings</sub>
11. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
12. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
13. **digest.** 26.8% of the book has no matching market move and is not included.  
   <sub>clients.json CASE-044 holdings without a mapped market move</sub>
14. **holding.** Holding up today: Consumer Staples +0.3% (5.4% of the book); Utilities +0.5% (3.2% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × clients.json CASE-044 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): ESG client: average sustainability score 7.6 of 10 against a minimum of 5.7; 1 holding below the per-position minimum (Meyer Burger Technology AG, 0.0% of the book); 29.3% of the book has no score.  
  <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-044 positions</sub>
- **Health check** (0.00): "Compliance with maximum volatility" means: For retail clients with financial services Comprehensive investment advisory or discretionary mandate must be PF Vola < max client profile Vola.  
  <sub>clients.json CASE-044: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Knowledge of portfolio funds and mixed funds" means: For retail clients with financial services, comprehensive investment advisory or trx-based investment advisory must be available from K&E.  
  <sub>clients.json CASE-044: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Knowledge of structured products" means: For retail clients with financial services, comprehensive investment advisory or trx-based investment advisory must be available from K&E.  
  <sub>clients.json CASE-044: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.19): GSC Green Tech ESG Fund drives 19.2% of the volatility of Investment advisory (CASE-044-01).  
  <sub>clients.json CASE-044: Portfolios[CASE-044-01].SecurityPositions.ContributionVolatility</sub>
- **Watch** (0.15): Note from 14 Sep 2026: "Would like a follow-up call before any changes to the standing order."  
  <sub>clients.json CASE-044: ClientNotes</sub>
- **Watch** (0.10): Health Care is 9.7% of the book (CHF 17k) after fund look-through, mostly via Sonova Holding AG and NASDAQ US Biotechnology UCITS ETF.  
  <sub>clients.json CASE-044: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.08): The last finalised proposal (8 Jul 2026, reason: Annual review meeting) ordered to buy SMI (R), Xtrackers MSCI World Consumer Staples UCITS ETF and 1 more and sell Georg Fischer AG, Sonova Holding AG and 1 more.  
  <sub>clients.json CASE-044: Proposals[22767] × Transactions</sub>
- **Watch** (0.03): Risk engine for Investment advisory (CASE-044-01), 3 Sep 2026: expected return 4.6%, value at risk 15.4%.  
  <sub>clients.json CASE-044: Portfolios[CASE-044-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): 26.8% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>clients.json CASE-044: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 39k, 22.6% of the book.  
  <sub>clients.json CASE-044: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 50.6% of the portfolio (CHF 87k).  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 22.6% of the portfolio (CHF 39k).  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 14.1% of the portfolio (CHF 24k).  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 12.7% of the portfolio (CHF 22k).  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Industrials is 25.5% of the portfolio (CHF 44k) after fund look-through.  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 9.7% of the portfolio (CHF 17k) after fund look-through.  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 5.4% of the portfolio (CHF 9k) after fund look-through.  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 3.3% of the portfolio (CHF 6k) after fund look-through.  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 3.2% of the portfolio (CHF 5k) after fund look-through.  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 1.2% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 1.1% of the portfolio (CHF 2k) after fund look-through.  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.7% of the portfolio (CHF 1k) after fund look-through.  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 0.4% of the portfolio (CHF 726) after fund look-through.  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 0.1% of the portfolio (CHF 110) after fund look-through.  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 85.7% of the portfolio (CHF 148k).  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 14.3% of the portfolio (CHF 25k).  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: GSC Green Tech ESG Fund, CHF 26k (15.2% of the portfolio).  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 12 holdings; the largest: GSC Green Tech ESG Fund (CHF 26k), SF Sustainable Property Fund (CHF 24k), Shs Global X Data Center REITs & Digital Infrastructure ETF (CHF 12k), Georg Fischer AG (CHF 11k).  
  <sub>clients.json CASE-044: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (1.00): Resolve "Knowledge of structured products" on Underlying Tracker Bk Vontobel 2020-open end o/SOLVALOR HYDROGEN TOP SEL.  
  <sub>clients.json CASE-044: SuitabilityViolations[Id=797860]</sub>
- **Next best actions** (0.30): Keep the 22.6% cash (CHF 39k) in view of the note from 20 Mar 2026: "Prefers to keep a cash reserve on hand for unexpected medical expenses."  
  <sub>clients.json CASE-044: LiquidityInDefaultCurrency, ClientNotes</sub>
- **Next best actions** (0.25): Clear the warnings on the 6 flagged orders from the proposal of 8 Jul 2026.  
  <sub>clients.json CASE-044: Transactions[ProposalId=22767].ForwardState = 2</sub>
- **Next best actions** (0.20): Candidates from the recommendation list for Shares: ABB Ltd and Kuehne + Nagel International AG (cash is above 10% of the book).  
  <sub>reference.json RecommendationLists "Recommendation list free assets", not held, CHF first, ordered by SustainabilityScore</sub>

</details>

---

## CASE-045 — Walter White

Investor profile 6 · CHF 340k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Walter White, Investor profile 6, ESG preference, CHF 340k across 1 portfolio.  
   <sub>clients.json CASE-045: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +20.9% over the 12 months to Jul 2026 and +47.9% since Oct 2021, now CHF 340k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-045: PerformanceHistory of CASE-045-01</sub>
3. **Health check.** 0 suitability errors and 1 warning open; most serious: "Share is not part of the investment universe for individual shares and therefore not monitored.".  
   <sub>clients.json CASE-045: SuitabilityViolations</sub>
4. **Health check.** 19 of 20 orders from the proposal of 30 Aug 2026 were forwarded with a warning.  
   <sub>clients.json CASE-045: Transactions[ProposalId=24828].ForwardState = 2</sub>
5. **Watch.** Health Care is 63.0% of the book (CHF 214k) after fund look-through, mostly via Novartis AG and BB Biotech AG.  
   <sub>clients.json CASE-045: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Watch.** Novartis AG alone is 41.0% of the book.  
   <sub>clients.json CASE-045: Portfolios[CASE-045-01].SecurityPositions</sub>
7. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "Financial sector an attractive route to broadening exposure."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
8. **Next best actions.** Resolve "Share is not part of the investment universe for individual shares and therefore not monitored.".  
   <sub>clients.json CASE-045: SuitabilityViolations[Id=910188]</sub>
9. **Next best actions.** Clear the warnings on the 19 flagged orders from the proposal of 30 Aug 2026.  
   <sub>clients.json CASE-045: Transactions[ProposalId=24828].ForwardState = 2</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Walter White is calling: Investor profile 6, ESG preference, CHF 340k across 1 portfolio.  
   <sub>clients.json CASE-045: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: wants it short. From the notes: "Values discretion; prefers minimal written correspondence about portfolio specifics."  
   <sub>data/profiles/profiles.json CASE-045 (apertus) from clients.json ClientNotes</sub>
3. **caller.** Contact preference: "Values discretion; prefers minimal written correspondence about portfolio specifics"  
   <sub>data/profiles/profiles.json CASE-045 from clients.json ClientNotes</sub>
4. **reason.** Probably the market: about −CHF 2k today, −0.7% of the book. Mostly Financials, −0.9% on 29.3% of it.  
   <sub>impact of the market feed on clients.json CASE-045 holdings</sub>
5. **digest.** About −CHF 2k today, −0.7% of the book.  
   <sub>impact of the market feed on clients.json CASE-045 holdings</sub>
6. **digest.** About −CHF 896 from Financials, −0.9% today on 29.3% of the book, mostly Cembra Money Bank AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × clients.json CASE-045 holdings</sub>
7. **digest.** About −CHF 856 from Health Care, −0.4% today on 63.0% of the book, mostly Novartis AG and BB Biotech AG.  
   <sub>market feed "tech-selloff": S5HLTH Index CHG_PCT_1D × clients.json CASE-045 holdings</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** About −CHF 274 from Industrials, −1.1% today on 7.3% of the book, mostly A1A Car Wash.  
   <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-045 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.00): ESG client: average sustainability score 8.5 of 10 against a minimum of 5.7; 29.3% of the book has no score.  
  <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-045 positions</sub>
- **Watch** (0.29): Financials is 29.3% of the book (CHF 100k) after fund look-through, mostly via Cembra Money Bank AG.  
  <sub>clients.json CASE-045: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.29): Cembra Money Bank AG alone is 29.3% of the book.  
  <sub>clients.json CASE-045: Portfolios[CASE-045-01].SecurityPositions</sub>
- **Watch** (0.22): BB Biotech AG alone is 22.0% of the book.  
  <sub>clients.json CASE-045: Portfolios[CASE-045-01].SecurityPositions</sub>
- **Watch** (0.15): Note from 9 Sep 2026: "Recent health concerns have prompted a review of estate and succession planning."  
  <sub>clients.json CASE-045: ClientNotes</sub>
- **Watch** (0.10): Note from 29 Jul 2026: "Former chemistry teacher, strongly interested in chemistry and the pharmaceutical industry."  
  <sub>clients.json CASE-045: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (30 Aug 2026, reason: Follow-up from prior meeting) ordered to buy SMI (R), SPDR Bloomberg Global Aggregate Bond UCITS ETF and 17 more.  
  <sub>clients.json CASE-045: Proposals[24828] × Transactions</sub>
- **Watch** (0.03): Risk engine for Investment advisory (CASE-045-01), 3 Sep 2026: expected return 5.5%, value at risk 14.7%.  
  <sub>clients.json CASE-045: Portfolios[CASE-045-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.00): Cash on hand is CHF 1k, 0.4% of the book.  
  <sub>clients.json CASE-045: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 99.7% of the portfolio (CHF 338k).  
  <sub>clients.json CASE-045: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 0.4% of the portfolio (CHF 1k).  
  <sub>clients.json CASE-045: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 63.0% of the portfolio (CHF 214k) after fund look-through.  
  <sub>clients.json CASE-045: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 29.3% of the portfolio (CHF 100k) after fund look-through.  
  <sub>clients.json CASE-045: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 7.3% of the portfolio (CHF 25k) after fund look-through.  
  <sub>clients.json CASE-045: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 92.7% of the portfolio (CHF 315k).  
  <sub>clients.json CASE-045: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 7.3% of the portfolio (CHF 25k).  
  <sub>clients.json CASE-045: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Novartis AG, CHF 139k (41.0% of the portfolio).  
  <sub>clients.json CASE-045: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 4 holdings; the largest: Novartis AG (CHF 139k), Cembra Money Bank AG (CHF 100k), BB Biotech AG (CHF 75k), A1A Car Wash (CHF 25k).  
  <sub>clients.json CASE-045: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## CASE-046 — Tony Montana

Investor profile 5 · CHF 534k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Tony Montana, Investor profile 5, ESG preference, CHF 534k across 1 portfolio.  
   <sub>clients.json CASE-046: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +25.0% over the 12 months to Jul 2026 and +14.6% since Oct 2021, now CHF 534k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-046: PerformanceHistory of CASE-046-01</sub>
3. **Health check.** 4 suitability errors and 0 warnings open; most serious: "Maximum limit liquidity".  
   <sub>clients.json CASE-046: SuitabilityViolations</sub>
4. **Health check.** Liquidity at 100.0%, outside its 0.0%–60.0% band, target 3.0%.  
   <sub>clients.json CASE-046: Portfolios[CASE-046-01] positions; reference.json StrategicAssetAllocations[92] AssetClass "Liquidity"</sub>
5. **Watch.** Note from 24 Jan 2026: "Interested in a broader diversification across currencies."  
   <sub>clients.json CASE-046: ClientNotes</sub>
6. **Watch.** Note from 23 Jul 2025: "Watching technology stocks in the portfolio closely, interested in expanding further."  
   <sub>clients.json CASE-046: ClientNotes</sub>
7. **Next best actions.** Deploy idle liquidity: 100.0% of the book (CHF 534k) is cash.  
   <sub>clients.json CASE-046: LiquidityInDefaultCurrency</sub>
8. **Next best actions.** Rebalance Liquidity down toward 3.0%.  
   <sub>clients.json CASE-046: Portfolios[CASE-046-01] positions; reference.json StrategicAssetAllocations[92] AssetClass "Liquidity"</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Tony Montana is calling: Investor profile 5, ESG preference, CHF 534k across 1 portfolio.  
   <sub>clients.json CASE-046: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Contact preference: "Prefers not to be contacted during business hours on weekdays"  
   <sub>data/profiles/profiles.json CASE-046 from clients.json ClientNotes</sub>
3. **reason.** Probably the proposal of 19 Sep 2026 that was rejected (reason: Client called).  
   <sub>clients.json CASE-046: Proposals[25042]</sub>
4. **reason.** Possibly idle cash: 100.0% of the book (CHF 534k) is cash.  
   <sub>clients.json CASE-046: LiquidityInDefaultCurrency</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (1.00): Shares at 0.0%, outside its 20.0%–85.0% band, target 45.0%.  
  <sub>clients.json CASE-046: Portfolios[CASE-046-01] positions; reference.json StrategicAssetAllocations[92] AssetClass "Shares"</sub>
- **Health check** (0.50): Bonds at 0.0%, outside its 10.0%–70.0% band, target 47.0%.  
  <sub>clients.json CASE-046: Portfolios[CASE-046-01] positions; reference.json StrategicAssetAllocations[92] AssetClass "Bonds"</sub>
- **Health check** (0.00): "Minimum limit fixed income" means: Minimum limits interest rates  
  <sub>clients.json CASE-046: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Minimum limit shares" means: Minimum Limit Stocks  
  <sub>clients.json CASE-046: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Maximum limit liquidity" means: Maximum liquidity limits  
  <sub>clients.json CASE-046: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.00): Cash on hand is CHF 534k, 100.0% of the book.  
  <sub>clients.json CASE-046: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Cash is 100.0% of the portfolio (CHF 534k).  
  <sub>clients.json CASE-046: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Swiss francs: 100.0% of the portfolio (CHF 534k).  
  <sub>clients.json CASE-046: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (1.00): Rebalance Shares up toward 45.0%.  
  <sub>clients.json CASE-046: Portfolios[CASE-046-01] positions; reference.json StrategicAssetAllocations[92] AssetClass "Shares"</sub>
- **Next best actions** (1.00): Resolve "Minimum limit fixed income".  
  <sub>clients.json CASE-046: SuitabilityViolations[Id=902900]</sub>
- **Next best actions** (1.00): Resolve "Minimum limit shares".  
  <sub>clients.json CASE-046: SuitabilityViolations[Id=902901]</sub>
- **Next best actions** (1.00): Resolve "Volatility range undershot (portfolio risk too low)".  
  <sub>clients.json CASE-046: SuitabilityViolations[Id=918829]</sub>
- **Next best actions** (0.50): Rebalance Bonds up toward 47.0%.  
  <sub>clients.json CASE-046: Portfolios[CASE-046-01] positions; reference.json StrategicAssetAllocations[92] AssetClass "Bonds"</sub>
- **Next best actions** (0.50): Follow up on the proposal of 19 Sep 2026 that was rejected (reason: Client called); it would have had the client buy D- LO Funds (CH)- Swiss Franc Credit Bond, CHF Short Mid Term Bonds and 20 more.  
  <sub>clients.json CASE-046: Proposals[25042] × Transactions</sub>
- **Next best actions** (0.40): Book a review: no finalised proposal on record.  
  <sub>clients.json CASE-046: Proposals</sub>
- **Next best actions** (0.20): Candidates from the recommendation list for Shares: ABB Ltd and Kuehne + Nagel International AG (Shares is under its band).  
  <sub>reference.json RecommendationLists "Recommendation list free assets", not held, CHF first, ordered by SustainabilityScore</sub>

</details>

---

## CASE-047 — Jon Snow

Investor profile 6 · CHF 762k · ESG preference: yes

### 60-second briefing (dashboard)

1. **Who.** Jon Snow, Investor profile 6, ESG preference, CHF 762k across 2 portfolios.  
   <sub>clients.json CASE-047: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Combined portfolio value +22.9% over the 12 months to Jul 2026 and +22.0% since Oct 2021, now CHF 762k; value change including deposits and withdrawals.  
   <sub>clients.json CASE-047: PerformanceHistory of CASE-047-01, CASE-047-02</sub>
3. **Health check.** 0 suitability errors and 3 warnings open; most serious: "Underweight in the equity sector "Consumer Discretionary"".  
   <sub>clients.json CASE-047: SuitabilityViolations</sub>
4. **Health check.** 26 of 28 orders from the proposal of 8 Jul 2026 were forwarded with a warning.  
   <sub>clients.json CASE-047: Transactions[ProposalId=23727].ForwardState = 2</sub>
5. **Watch.** Health Care is 17.4% of the book (CHF 133k) after fund look-through, mostly via Lonza Group AG and Novartis AG.  
   <sub>clients.json CASE-047: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Watch.** Information Technology is 15.5% of the book (CHF 118k) after fund look-through, mostly via Comet Holding AG and 2.5 % Apple Inc 2015-9.2.25 Global.  
   <sub>clients.json CASE-047: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
7. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "That means maintaining an overweight position in technology stocks."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
8. **Next best actions.** Resolve "Underweight in the equity sector "Consumer Discretionary"".  
   <sub>clients.json CASE-047: SuitabilityViolations[Id=854529]</sub>
9. **Next best actions.** Resolve "Overweight in the equity sector "Industrials"".  
   <sub>clients.json CASE-047: SuitabilityViolations[Id=854530]</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Jon Snow is calling: Investor profile 6, ESG preference, CHF 762k across 2 portfolios.  
   <sub>clients.json CASE-047: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **caller.** Profile: calm temperament. From the notes: "Comfortable with higher volatility given a long time horizon."  
   <sub>data/profiles/profiles.json CASE-047 (apertus) from clients.json ClientNotes</sub>
3. **reason.** Probably the market: about −CHF 11k today, −1.5% of the book. Mostly Information Technology, −4.8% on 13.2% of it.  
   <sub>impact of the market feed on clients.json CASE-047 holdings</sub>
4. **reason.** Possibly a sustainability concern: ESG client: average sustainability score 7.4 of 10 against a minimum of 5.7; 2 holdings below the per-position minimum (iShares Core MSCI EM IMI UCITS ETF and 2.5 % Apple Inc 2015-9.2.25 Global, 6.3% of the book); 2.6% of the book has no score.  
   <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-047 positions</sub>
5. **digest.** About −CHF 11k today, −1.5% of the book.  
   <sub>impact of the market feed on clients.json CASE-047 holdings</sub>
6. **digest.** About −CHF 5k from Information Technology, −4.8% today on 13.2% of the book, mostly Comet Holding AG and iShares Automation & Robotics UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × clients.json CASE-047 holdings</sub>
7. **digest.** About −CHF 3k from the dollar, −1.2% against the franc on 34.7% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × clients.json CASE-047 holdings</sub>
8. **digest.** About −CHF 1k from Industrials, −1.1% today on 12.0% of the book, mostly Accelleron Industries AG and ABB Ltd.  
   <sub>market feed "tech-selloff": S5INDU Index CHG_PCT_1D × clients.json CASE-047 holdings</sub>
9. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
10. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
11. **holding.** Holding up today: Swiss franc bonds +0.2% (11.4% of the book); foreign bonds +0.3% (10.5% of the book); Consumer Staples +0.3% (10.1% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × clients.json CASE-047 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Health check** (0.13): ESG client: average sustainability score 7.4 of 10 against a minimum of 5.7; 2 holdings below the per-position minimum (iShares Core MSCI EM IMI UCITS ETF and 2.5 % Apple Inc 2015-9.2.25 Global, 6.3% of the book); 2.6% of the book has no score.  
  <sub>reference.json Securities.SustainabilityScore (0–10) vs EsgProfiles[1] MinimumLevel / MinimumPositionLevel; clients.json CASE-047 positions</sub>
- **Health check** (0.00): "Underweight in the equity sector "Consumer Discretionary"" means: Underweight (+/- 5% of the benchmark’s SAA target) in the non-basic consumer goods equity sector  
  <sub>clients.json CASE-047: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Overweight in the equity sector "Industrials"" means: Overweight (+/- 5% of the benchmark’s SAA target) in the ‘Industrials’ equity sector  
  <sub>clients.json CASE-047: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Health check** (0.00): "Overweight in the equity sector "Information Technology"" means: Overweight (+/- 5% of the benchmark’s SAA target) in the Information Technology sector  
  <sub>clients.json CASE-047: SuitabilityViolations.RuleDescription, translated by Supertext (data/translations/rules-en.json)</sub>
- **Watch** (0.15): Note from 3 Nov 2025: "Wants as high a weighting of sustainable funds as possible at the next rebalancing."  
  <sub>clients.json CASE-047: ClientNotes</sub>
- **Watch** (0.10): Note from 18 Jun 2025: "Requested a comparison against the benchmark at the next review."  
  <sub>clients.json CASE-047: ClientNotes</sub>
- **Watch** (0.08): The last finalised proposal (8 Jul 2026, reason: Risk profile update) ordered to buy iShares Core S&P 500 UCITS ETF, Nestle SA and 24 more.  
  <sub>clients.json CASE-047: Proposals[23727] × Transactions</sub>
- **Watch** (0.03): Risk engine for Pension (CASE-047-01), 3 Sep 2026: expected return 6.3%, value at risk 16.3%.  
  <sub>clients.json CASE-047: Portfolios[CASE-047-01].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.03): Risk engine for Depository advisory (CASE-047-02), 3 Sep 2026: expected return 5.5%, value at risk 14.5%.  
  <sub>clients.json CASE-047: Portfolios[CASE-047-02].ExpectedReturn, ValueAtRisk</sub>
- **Watch** (0.01): Equities Switzerland Passive Leader drives 26.0% of the volatility of Pension (CASE-047-01).  
  <sub>clients.json CASE-047: Portfolios[CASE-047-01].SecurityPositions.ContributionVolatility</sub>
- **Watch** (0.00): Cash on hand is CHF 11k, 1.4% of the book.  
  <sub>clients.json CASE-047: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 76.7% of the portfolio (CHF 584k).  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 21.9% of the portfolio (CHF 167k).  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 1.4% of the portfolio (CHF 11k).  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 17.4% of the portfolio (CHF 133k) after fund look-through.  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 15.5% of the portfolio (CHF 118k) after fund look-through.  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 14.6% of the portfolio (CHF 111k) after fund look-through.  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 13.5% of the portfolio (CHF 103k) after fund look-through.  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 10.1% of the portfolio (CHF 77k) after fund look-through.  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 5.4% of the portfolio (CHF 41k) after fund look-through.  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 3.2% of the portfolio (CHF 25k) after fund look-through.  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 2.4% of the portfolio (CHF 18k) after fund look-through.  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.9% of the portfolio (CHF 7k) after fund look-through.  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.5% of the portfolio (CHF 4k) after fund look-through.  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.4% of the portfolio (CHF 3k) after fund look-through.  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 55.0% of the portfolio (CHF 419k).  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 40.9% of the portfolio (CHF 312k).  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 4.0% of the portfolio (CHF 31k).  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares Core S&P 500 UCITS ETF, CHF 49k (6.5% of the portfolio).  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 32 holdings; the largest: iShares Core S&P 500 UCITS ETF (CHF 49k), Lonza Group AG (CHF 40k), Nestle SA (CHF 38k), Accelleron Industries AG (CHF 35k).  
  <sub>clients.json CASE-047: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Next best actions** (0.30): Resolve "Overweight in the equity sector "Information Technology"".  
  <sub>clients.json CASE-047: SuitabilityViolations[Id=857255]</sub>
- **Next best actions** (0.23): Clear the warnings on the 26 flagged orders from the proposal of 8 Jul 2026.  
  <sub>clients.json CASE-047: Transactions[ProposalId=23727].ForwardState = 2</sub>

</details>

---

## EXT-01 — Max Muster

no risk profile · CHF 2.05m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Max Muster, no risk profile, CHF 2.05m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +9.9% over the 12 months to Dec 2025 and +48.3% since Dec 2022, now CHF 2.05m; value change including deposits and withdrawals.  
   <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: PerformanceHistory of EXT-01-01</sub>
3. **Health check.** Nothing open: no suitability violation, and every asset class is inside its band.  
   <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SuitabilityViolations (none open); reference.json StrategicAssetAllocations bands</sub>
4. **Watch.** 69.0% of the book is in holdings on none of the bank's recommendation lists, largest Vanguard S&P 500 UCITS ETF, 3.625% TotalEnergies SE 2023-2033 and 11 more.  
   <sub>reference.json Securities.InRecommendationList; custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01 positions</sub>
5. **Watch.** Health Care is 8.7% of the book (CHF 178k) after fund look-through, mostly via Lonza Group AG and Roche Holding AG.  
   <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "We remain Underweight real estate and consumer staples amid weak sentiment and low visibility on the housing recovery."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Max Muster is calling: no risk profile, CHF 2.05m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 12k today, −0.6% of the book. Mostly the dollar, −1.2% on 44.9% of it.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01 holdings</sub>
3. **digest.** About −CHF 12k today, −0.6% of the book.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01 holdings</sub>
4. **digest.** About −CHF 11k from the dollar, −1.2% against the franc on 44.9% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01 holdings</sub>
5. **digest.** About −CHF 3k from Consumer Discretionary, −2.2% today on 5.6% of the book, mostly Amazon.com Inc..  
   <sub>market feed "tech-selloff": S5COND Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01 holdings</sub>
6. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
7. **digest.** About −CHF 1k from the euro, −0.3% against the franc on 20.8% of the book.  
   <sub>market feed "tech-selloff": EURCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01 holdings</sub>
8. **digest.** 34.1% of the book has no matching market move and is not included.  
   <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01 holdings without a mapped market move</sub>
9. **holding.** Holding up today: foreign bonds +0.3% (20.4% of the book); Swiss franc bonds +0.2% (9.6% of the book); Consumer Staples +0.3% (6.4% of the book).  
   <sub>market feed "tech-selloff": LEGATRUU Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.06): Consumer Staples is 6.4% of the book (CHF 131k) after fund look-through, mostly via Nestlé AG and Unilever PLC.  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.00): 69.0% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 100k, 4.9% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 54.3% of the portfolio (CHF 1.11m).  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 30.1% of the portfolio (CHF 616k).  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 9.3% of the portfolio (CHF 191k).  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 4.9% of the portfolio (CHF 100k).  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 1.4% of the portfolio (CHF 30k).  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Health Care is 8.7% of the portfolio (CHF 178k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 6.4% of the portfolio (CHF 131k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 5.6% of the portfolio (CHF 115k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 5.4% of the portfolio (CHF 110k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): US-Dollar: 44.9% of the portfolio (CHF 920k).  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Swiss francs: 31.5% of the portfolio (CHF 647k).  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 20.8% of the portfolio (CHF 427k).  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Andere: 2.7% of the portfolio (CHF 56k).  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Gold: CHF 99k, 4.8% of the portfolio.  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Vanguard S&P 500 UCITS ETF, CHF 267k (13.0% of the portfolio).  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 19 holdings; the largest: Vanguard S&P 500 UCITS ETF (CHF 267k), 3.625% TotalEnergies SE 2023-2033 (CHF 200k), 2.250% Swisscom AG 2023-2031 (CHF 198k), iShares MSCI Emerging Mkts UCITS (CHF 158k).  
  <sub>custody statement Quartalsreporting_Q4_2025_01_Herr_Max_Muster.pdf (Privatbank Helvetia AG) EXT-01: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## EXT-02 — Anna Beispiel

no risk profile · CHF 3.41m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Anna Beispiel, no risk profile, CHF 3.41m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +6.1% over the 12 months to Dec 2025 and +40.5% since Dec 2022, now CHF 3.41m; value change including deposits and withdrawals.  
   <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: PerformanceHistory of EXT-02-01</sub>
3. **Health check.** Nothing open: no suitability violation, and every asset class is inside its band.  
   <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SuitabilityViolations (none open); reference.json StrategicAssetAllocations bands</sub>
4. **Watch.** 72.1% of the book is in holdings on none of the bank's recommendation lists, largest Vanguard S&P 500 UCITS ETF, iShares STOXX Europe 600 UCITS and 11 more.  
   <sub>reference.json Securities.InRecommendationList; custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02 positions</sub>
5. **Watch.** Raw materials is 6.1% of the book (CHF 206k) after fund look-through, mostly via Sika AG.  
   <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "That means maintaining an overweight position in technology stocks."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Anna Beispiel is calling: no risk profile, CHF 3.41m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 30k today, −0.9% of the book. Mostly the dollar, −1.2% on 44.5% of it.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02 holdings</sub>
3. **digest.** About −CHF 30k today, −0.9% of the book.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02 holdings</sub>
4. **digest.** About −CHF 18k from the dollar, −1.2% against the franc on 44.5% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02 holdings</sub>
5. **digest.** About −CHF 9k from Information Technology, −4.8% today on 5.3% of the book, mostly Apple Inc..  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02 holdings</sub>
6. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
7. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** About −CHF 2k from the euro, −0.3% against the franc on 17.2% of the book.  
   <sub>market feed "tech-selloff": EURCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02 holdings</sub>
9. **digest.** 50.9% of the book has no matching market move and is not included.  
   <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02 holdings without a mapped market move</sub>
10. **holding.** Holding up today: Swiss franc bonds +0.2% (12.4% of the book); foreign bonds +0.3% (8.8% of the book); Consumer Staples +0.3% (3.8% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.05): Information Technology is 5.3% of the book (CHF 180k) after fund look-through, mostly via Apple Inc..  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.00): 72.1% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 151k, 4.4% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 65.1% of the portfolio (CHF 2.22m).  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 21.2% of the portfolio (CHF 723k).  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 6.9% of the portfolio (CHF 234k).  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 4.4% of the portfolio (CHF 151k).  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 2.4% of the portfolio (CHF 80k).  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Raw materials is 6.1% of the portfolio (CHF 206k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 5.3% of the portfolio (CHF 180k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 4.5% of the portfolio (CHF 152k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 3.9% of the portfolio (CHF 132k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 3.8% of the portfolio (CHF 129k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): US-Dollar: 44.5% of the portfolio (CHF 1.52m).  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Swiss francs: 28.8% of the portfolio (CHF 980k).  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 17.2% of the portfolio (CHF 585k).  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Andere: 7.4% of the portfolio (CHF 251k).  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): British pound: 2.1% of the portfolio (CHF 73k).  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: Vanguard S&P 500 UCITS ETF, CHF 620k (18.2% of the portfolio).  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 18 holdings; the largest: Vanguard S&P 500 UCITS ETF (CHF 620k), iShares STOXX Europe 600 UCITS (CHF 433k), 1.750% Kanton Zürich 2023-2033 (CHF 271k), NVIDIA Corp. (CHF 245k).  
  <sub>custody statement Quartalsreporting_Q4_2025_02_Frau_Anna_Beispiel.pdf (Privatbank Helvetia AG) EXT-02: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## EXT-03 — Weber-Brunner family

no risk profile · CHF 1.25m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Weber-Brunner family, no risk profile, CHF 1.25m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +8.2% over the 12 months to Dec 2025 and +31.6% since Dec 2022, now CHF 1.25m; value change including deposits and withdrawals.  
   <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: PerformanceHistory of EXT-03-01</sub>
3. **Health check.** Nothing open: no suitability violation, and every asset class is inside its band.  
   <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SuitabilityViolations (none open); reference.json StrategicAssetAllocations bands</sub>
4. **Watch.** 76.5% of the book is in holdings on none of the bank's recommendation lists, largest 4.625% JPMorgan Chase & Co. 2023-2030, 1.900% Roche Kapitalmarkt AG 2022-2029 and 6 more.  
   <sub>reference.json Securities.InRecommendationList; custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03 positions</sub>
5. **Watch.** 4.625% JPMorgan Chase & Co. 2023-2030 alone is 22.5% of the book.  
   <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: Portfolios[EXT-03-01].SecurityPositions</sub>
6. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "We remain Underweight real estate and consumer staples amid weak sentiment and low visibility on the housing recovery."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Weber-Brunner family is calling: no risk profile, CHF 1.25m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 7k today, −0.6% of the book. Mostly the dollar, −1.2% on 38.3% of it.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03 holdings</sub>
3. **digest.** About −CHF 7k today, −0.6% of the book.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03 holdings</sub>
4. **digest.** About −CHF 6k from the dollar, −1.2% against the franc on 38.3% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03 holdings</sub>
5. **digest.** About −CHF 1k from Communication Services, −3.1% today on 3.7% of the book, mostly Swisscom AG and iShares Core MSCI World UCITS ETF.  
   <sub>market feed "tech-selloff": S5TELS Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03 holdings</sub>
6. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
7. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** About −CHF 709 from the pound, −0.4% against the franc on 14.2% of the book.  
   <sub>market feed "tech-selloff": GBPCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03 holdings</sub>
9. **digest.** 17.1% of the book has no matching market move and is not included.  
   <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03 holdings without a mapped market move</sub>
10. **holding.** Holding up today: foreign bonds +0.3% (46.0% of the book); Swiss franc bonds +0.2% (13.3% of the book); Consumer Staples +0.3% (4.3% of the book).  
   <sub>market feed "tech-selloff": LEGATRUU Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.13): 1.900% Roche Kapitalmarkt AG 2022-2029 alone is 13.3% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: Portfolios[EXT-03-01].SecurityPositions</sub>
- **Watch** (0.12): 4.125% AstraZeneca PLC 2023-2029 alone is 12.2% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: Portfolios[EXT-03-01].SecurityPositions</sub>
- **Watch** (0.11): 3.000% Nestlé Finance Intl 2022-2030 alone is 11.3% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: Portfolios[EXT-03-01].SecurityPositions</sub>
- **Watch** (0.04): Consumer Staples is 4.3% of the book (CHF 54k) after fund look-through, mostly via Unilever PLC and Nestlé AG.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.04): Communication Services is 3.7% of the book (CHF 47k) after fund look-through, mostly via Swisscom AG and iShares Core MSCI World UCITS ETF.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.00): 76.5% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 83k, 6.7% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Bonds are 59.3% of the portfolio (CHF 743k).  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Shares are 23.1% of the portfolio (CHF 289k).  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 10.9% of the portfolio (CHF 136k).  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 6.7% of the portfolio (CHF 83k).  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Consumer Staples is 4.3% of the portfolio (CHF 54k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 3.7% of the portfolio (CHF 47k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 3.6% of the portfolio (CHF 45k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 1.8% of the portfolio (CHF 22k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 1.7% of the portfolio (CHF 22k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 0.9% of the portfolio (CHF 11k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 0.4% of the portfolio (CHF 5k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.2% of the portfolio (CHF 2k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 0.1% of the portfolio (CHF 2k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.1% of the portfolio (CHF 1k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.1% of the portfolio (CHF 985) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): US-Dollar: 39.4% of the portfolio (CHF 493k).  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Swiss francs: 24.8% of the portfolio (CHF 310k).  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): British pound: 14.0% of the portfolio (CHF 176k).  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 12.6% of the portfolio (CHF 158k).  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Andere: 9.2% of the portfolio (CHF 115k).  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: 4.625% JPMorgan Chase & Co. 2023-2030, CHF 282k (22.5% of the portfolio).  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 15 holdings; the largest: 4.625% JPMorgan Chase & Co. 2023-2030 (CHF 282k), 1.900% Roche Kapitalmarkt AG 2022-2029 (CHF 166k), 4.125% AstraZeneca PLC 2023-2029 (CHF 153k), 3.000% Nestlé Finance Intl 2022-2030 (CHF 141k).  
  <sub>custody statement Quartalsreporting_Q4_2025_03_Familie_Weber_Brunner.pdf (Privatbank Helvetia AG) EXT-03: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## EXT-04 — Peter Keller

no risk profile · CHF 4.80m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Peter Keller, no risk profile, CHF 4.80m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +7.9% over the 12 months to Dec 2025 and +37.6% since Dec 2022, now CHF 4.80m; value change including deposits and withdrawals.  
   <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: PerformanceHistory of EXT-04-01</sub>
3. **Health check.** Nothing open: no suitability violation, and every asset class is inside its band.  
   <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SuitabilityViolations (none open); reference.json StrategicAssetAllocations bands</sub>
4. **Watch.** 43.6% of the book is in holdings on none of the bank's recommendation lists, largest iShares MSCI Emerging Mkts UCITS, NVIDIA Corp. and 10 more.  
   <sub>reference.json Securities.InRecommendationList; custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04 positions</sub>
5. **Watch.** Communication Services is 12.6% of the book (CHF 607k) after fund look-through, mostly via Swisscom AG and Alphabet Inc. Cl A.  
   <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "We remain Underweight real estate and consumer staples amid weak sentiment and low visibility on the housing recovery."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Peter Keller is calling: no risk profile, CHF 4.80m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 69k today, −1.4% of the book. Mostly the dollar, −1.2% on 53.1% of it.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04 holdings</sub>
3. **digest.** About −CHF 69k today, −1.4% of the book.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04 holdings</sub>
4. **digest.** About −CHF 31k from the dollar, −1.2% against the franc on 53.1% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04 holdings</sub>
5. **digest.** About −CHF 19k from Communication Services, −3.1% today on 12.6% of the book, mostly Swisscom AG and Alphabet Inc. Cl A.  
   <sub>market feed "tech-selloff": S5TELS Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04 holdings</sub>
6. **digest.** About −CHF 14k from Information Technology, −4.8% today on 6.1% of the book, mostly Apple Inc..  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** 36.8% of the book has no matching market move and is not included.  
   <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04 holdings without a mapped market move</sub>
10. **holding.** Holding up today: Consumer Staples +0.3% (10.5% of the book); Swiss franc bonds +0.2% (4.7% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.11): NVIDIA Corp. alone is 11.3% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: Portfolios[EXT-04-01].SecurityPositions</sub>
- **Watch** (0.11): Consumer Staples is 10.5% of the book (CHF 506k) after fund look-through, mostly via Unilever PLC.  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.11): Unilever PLC alone is 10.5% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: Portfolios[EXT-04-01].SecurityPositions</sub>
- **Watch** (0.00): 43.6% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 148k, 3.1% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 82.0% of the portfolio (CHF 3.94m).  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 6.8% of the portfolio (CHF 326k).  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 5.0% of the portfolio (CHF 240k).  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 3.2% of the portfolio (CHF 152k).  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 3.1% of the portfolio (CHF 148k).  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Communication Services is 12.6% of the portfolio (CHF 607k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 10.5% of the portfolio (CHF 506k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 8.7% of the portfolio (CHF 417k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 8.0% of the portfolio (CHF 386k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 7.4% of the portfolio (CHF 353k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 6.1% of the portfolio (CHF 293k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): US-Dollar: 53.1% of the portfolio (CHF 2.55m).  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Swiss francs: 34.1% of the portfolio (CHF 1.64m).  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Andere: 10.5% of the portfolio (CHF 506k).  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): British pound: 2.2% of the portfolio (CHF 108k).  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares MSCI Emerging Mkts UCITS, CHF 636k (13.2% of the portfolio).  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 20 holdings; the largest: iShares MSCI Emerging Mkts UCITS (CHF 636k), NVIDIA Corp. (CHF 545k), Unilever PLC (CHF 506k), UBS Group AG (CHF 417k).  
  <sub>custody statement Quartalsreporting_Q4_2025_04_Herr_Peter_Keller.pdf (Privatbank Helvetia AG) EXT-04: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## EXT-05 — Laura Steiner

no risk profile · CHF 948k · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Laura Steiner, no risk profile, CHF 948k across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +8.4% over the 12 months to Dec 2025 and +39.1% since Dec 2022, now CHF 948k; value change including deposits and withdrawals.  
   <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: PerformanceHistory of EXT-05-01</sub>
3. **Health check.** Nothing open: no suitability violation, and every asset class is inside its band.  
   <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SuitabilityViolations (none open); reference.json StrategicAssetAllocations bands</sub>
4. **Watch.** 65.2% of the book is in holdings on none of the bank's recommendation lists, largest 3.375% Siemens Finance BV 2023-2031, 2.100% Pfandbriefzentrale 2023-2029 and 9 more.  
   <sub>reference.json Securities.InRecommendationList; custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05 positions</sub>
5. **Watch.** Consumer Discretionary is 12.3% of the book (CHF 117k) after fund look-through, mostly via 0.500% Schweiz. Eidgenossenschaft 2020-2032 and LVMH Moët Hennessy SE.  
   <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "We remain Underweight real estate and consumer staples amid weak sentiment and low visibility on the housing recovery."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Laura Steiner is calling: no risk profile, CHF 948k across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 8k today, −0.8% of the book. Mostly the dollar, −1.2% on 26.3% of it.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05 holdings</sub>
3. **digest.** About −CHF 8k today, −0.8% of the book.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05 holdings</sub>
4. **digest.** About −CHF 3k from the dollar, −1.2% against the franc on 26.3% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05 holdings</sub>
5. **digest.** About −CHF 2k from Information Technology, −4.8% today on 5.1% of the book, mostly SAP SE and Microsoft Corp..  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05 holdings</sub>
6. **digest.** About −CHF 2k from Consumer Discretionary, −2.2% today on 7.8% of the book, mostly LVMH Moët Hennessy SE and Amazon.com Inc..  
   <sub>market feed "tech-selloff": S5COND Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** 24.7% of the book has no matching market move and is not included.  
   <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05 holdings without a mapped market move</sub>
10. **holding.** Holding up today: Swiss franc bonds +0.2% (24.2% of the book); foreign bonds +0.3% (9.2% of the book); Consumer Staples +0.3% (7.5% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.07): Consumer Staples is 7.5% of the book (CHF 71k) after fund look-through, mostly via Unilever PLC and Nestlé AG.  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.00): 60.7% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 44k, 4.6% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 46.9% of the portfolio (CHF 445k).  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 33.4% of the portfolio (CHF 316k).  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 15.1% of the portfolio (CHF 143k).  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 4.6% of the portfolio (CHF 44k).  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Consumer Discretionary is 12.3% of the portfolio (CHF 117k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 7.5% of the portfolio (CHF 71k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 5.1% of the portfolio (CHF 48k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 5.1% of the portfolio (CHF 48k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 4.7% of the portfolio (CHF 45k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 42.8% of the portfolio (CHF 405k).  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 26.3% of the portfolio (CHF 249k).  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 21.8% of the portfolio (CHF 207k).  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Andere: 9.2% of the portfolio (CHF 87k).  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Gold: CHF 68k, 7.2% of the portfolio.  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: 3.375% Siemens Finance BV 2023-2031, CHF 87k (9.2% of the portfolio).  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 20 holdings; the largest: 3.375% Siemens Finance BV 2023-2031 (CHF 87k), 2.100% Pfandbriefzentrale 2023-2029 (CHF 80k), 1.400% Kanton Waadt 2022-2030 (CHF 75k), 1.250% Schweiz. Eidgenossenschaft 2021-2031 (CHF 74k).  
  <sub>custody statement Quartalsreporting_Q4_2025_05_Frau_Laura_Steiner.pdf (Privatbank Helvetia AG) EXT-05: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## EXT-06 — Muster Holding AG

no risk profile · CHF 7.60m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Muster Holding AG, no risk profile, CHF 7.60m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +12.3% over the 12 months to Dec 2025 and +55.2% since Dec 2022, now CHF 7.60m; value change including deposits and withdrawals.  
   <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: PerformanceHistory of EXT-06-01</sub>
3. **Health check.** Nothing open: no suitability violation, and every asset class is inside its band.  
   <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SuitabilityViolations (none open); reference.json StrategicAssetAllocations bands</sub>
4. **Watch.** Consumer Staples is 20.6% of the book (CHF 1.56m) after fund look-through, mostly via Unilever PLC and Nestlé AG.  
   <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
5. **Watch.** 41.1% of the book is in holdings on none of the bank's recommendation lists, largest JPMorgan Chase & Co., UBS CMCI Commodity Index Fonds and 11 more.  
   <sub>reference.json Securities.InRecommendationList; custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06 positions</sub>
6. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "We remain Underweight real estate and consumer staples amid weak sentiment and low visibility on the housing recovery."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Muster Holding AG is calling: no risk profile, CHF 7.60m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 84k today, −1.1% of the book. Mostly Information Technology, −4.8% on 10.2% of it.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06 holdings</sub>
3. **digest.** About −CHF 84k today, −1.1% of the book.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06 holdings</sub>
4. **digest.** About −CHF 37k from Information Technology, −4.8% today on 10.2% of the book, mostly iShares Core MSCI World UCITS ETF and Microsoft Corp..  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06 holdings</sub>
5. **digest.** About −CHF 35k from the dollar, −1.2% against the franc on 38.1% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06 holdings</sub>
6. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
7. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** About −CHF 4k from Financials, −0.9% today on 6.5% of the book, mostly Zurich Insurance Group AG and iShares Core MSCI World UCITS ETF.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06 holdings</sub>
9. **digest.** 26.8% of the book has no matching market move and is not included.  
   <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06 holdings without a mapped market move</sub>
10. **holding.** Holding up today: Consumer Staples +0.3% (20.6% of the book); foreign bonds +0.3% (7.6% of the book); Swiss franc bonds +0.2% (6.7% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.11): Unilever PLC alone is 10.5% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: Portfolios[EXT-06-01].SecurityPositions</sub>
- **Watch** (0.10): Information Technology is 10.2% of the book (CHF 772k) after fund look-through, mostly via iShares Core MSCI World UCITS ETF and Microsoft Corp..  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): JPMorgan Chase & Co. alone is 10.1% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: Portfolios[EXT-06-01].SecurityPositions</sub>
- **Watch** (0.00): 38.3% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 322k, 4.2% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 68.3% of the portfolio (CHF 5.19m).  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 14.3% of the portfolio (CHF 1.09m).  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 9.7% of the portfolio (CHF 738k).  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 4.2% of the portfolio (CHF 322k).  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 3.5% of the portfolio (CHF 262k).  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Consumer Staples is 20.6% of the portfolio (CHF 1.56m) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 10.2% of the portfolio (CHF 772k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 6.5% of the portfolio (CHF 495k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 4.9% of the portfolio (CHF 374k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 4.6% of the portfolio (CHF 349k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 4.3% of the portfolio (CHF 327k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 4.0% of the portfolio (CHF 308k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 1.1% of the portfolio (CHF 82k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.7% of the portfolio (CHF 50k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.3% of the portfolio (CHF 26k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.3% of the portfolio (CHF 24k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): US-Dollar: 42.2% of the portfolio (CHF 3.21m).  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Swiss francs: 38.0% of the portfolio (CHF 2.89m).  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Andere: 10.5% of the portfolio (CHF 799k).  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 6.3% of the portfolio (CHF 481k).  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): British pound: 2.9% of the portfolio (CHF 224k).  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares Core MSCI World UCITS ETF, CHF 1.07m (14.0% of the portfolio).  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 22 holdings; the largest: iShares Core MSCI World UCITS ETF (CHF 1.07m), Unilever PLC (CHF 799k), JPMorgan Chase & Co. (CHF 768k), Nestlé AG (CHF 697k).  
  <sub>custody statement Quartalsreporting_Q4_2025_06_Muster_Holding_AG.pdf (Privatbank Helvetia AG) EXT-06: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## EXT-07 — Daniel Frey

no risk profile · CHF 1.80m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Daniel Frey, no risk profile, CHF 1.80m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +5.4% over the 12 months to Dec 2025 and +33.5% since Dec 2022, now CHF 1.80m; value change including deposits and withdrawals.  
   <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: PerformanceHistory of EXT-07-01</sub>
3. **Health check.** Nothing open: no suitability violation, and every asset class is inside its band.  
   <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SuitabilityViolations (none open); reference.json StrategicAssetAllocations bands</sub>
4. **Watch.** 71.1% of the book is in holdings on none of the bank's recommendation lists, largest 4.125% AstraZeneca PLC 2023-2029, 3.000% Nestlé Finance Intl 2022-2030 and 9 more.  
   <sub>reference.json Securities.InRecommendationList; custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07 positions</sub>
5. **Watch.** 4.125% AstraZeneca PLC 2023-2029 alone is 18.0% of the book.  
   <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: Portfolios[EXT-07-01].SecurityPositions</sub>
6. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "That means maintaining an overweight position in technology stocks."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Daniel Frey is calling: no risk profile, CHF 1.80m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 15k today, −0.8% of the book. Mostly Information Technology, −4.8% on 8.6% of it.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07 holdings</sub>
3. **digest.** About −CHF 15k today, −0.8% of the book.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07 holdings</sub>
4. **digest.** About −CHF 7k from Information Technology, −4.8% today on 8.6% of the book, mostly Apple Inc. and Microsoft Corp..  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07 holdings</sub>
5. **digest.** About −CHF 6k from the dollar, −1.2% against the franc on 29.5% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07 holdings</sub>
6. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
7. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** About −CHF 1k from the pound, −0.4% against the franc on 18.2% of the book.  
   <sub>market feed "tech-selloff": GBPCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07 holdings</sub>
9. **digest.** 10.7% of the book has no matching market move and is not included.  
   <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07 holdings without a mapped market move</sub>
10. **holding.** Holding up today: foreign bonds +0.3% (44.8% of the book); Swiss franc bonds +0.2% (11.9% of the book); Gold +1.4% (3.7% of the book).  
   <sub>market feed "tech-selloff": LEGATRUU Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.15): 3.000% Nestlé Finance Intl 2022-2030 alone is 15.0% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: Portfolios[EXT-07-01].SecurityPositions</sub>
- **Watch** (0.12): 1.400% Kanton Waadt 2022-2030 alone is 11.9% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: Portfolios[EXT-07-01].SecurityPositions</sub>
- **Watch** (0.12): 4.625% JPMorgan Chase & Co. 2023-2030 alone is 11.8% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: Portfolios[EXT-07-01].SecurityPositions</sub>
- **Watch** (0.09): Information Technology is 8.6% of the book (CHF 155k) after fund look-through, mostly via Apple Inc. and Microsoft Corp..  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.05): Industrials is 4.8% of the book (CHF 86k) after fund look-through, mostly via ABB Ltd and Siemens AG.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.00): 71.1% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 124k, 6.9% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Bonds are 56.7% of the portfolio (CHF 1.02m).  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Shares are 25.7% of the portfolio (CHF 463k).  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 6.9% of the portfolio (CHF 124k).  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 6.1% of the portfolio (CHF 109k).  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 4.7% of the portfolio (CHF 84k).  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Information Technology is 8.6% of the portfolio (CHF 155k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 4.8% of the portfolio (CHF 86k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 3.3% of the portfolio (CHF 60k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 1.6% of the portfolio (CHF 28k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 1.4% of the portfolio (CHF 26k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 0.8% of the portfolio (CHF 15k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 0.7% of the portfolio (CHF 12k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 0.4% of the portfolio (CHF 8k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 0.2% of the portfolio (CHF 4k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.1% of the portfolio (CHF 2k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.1% of the portfolio (CHF 2k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): US-Dollar: 31.1% of the portfolio (CHF 561k).  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Swiss francs: 27.5% of the portfolio (CHF 496k).  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 23.4% of the portfolio (CHF 421k).  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): British pound: 18.0% of the portfolio (CHF 324k).  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Gold: CHF 67k, 3.7% of the portfolio.  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: 4.125% AstraZeneca PLC 2023-2029, CHF 324k (18.0% of the portfolio).  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 20 holdings; the largest: 4.125% AstraZeneca PLC 2023-2029 (CHF 324k), 3.000% Nestlé Finance Intl 2022-2030 (CHF 270k), 1.400% Kanton Waadt 2022-2030 (CHF 215k), 4.625% JPMorgan Chase & Co. 2023-2030 (CHF 213k).  
  <sub>custody statement Quartalsreporting_Q4_2025_07_Herr_Daniel_Frey.pdf (Privatbank Helvetia AG) EXT-07: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## EXT-08 — Nicole Baumann

no risk profile · CHF 2.70m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Nicole Baumann, no risk profile, CHF 2.70m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +9.2% over the 12 months to Dec 2025 and +56.8% since Dec 2022, now CHF 2.70m; value change including deposits and withdrawals.  
   <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: PerformanceHistory of EXT-08-01</sub>
3. **Health check.** Nothing open: no suitability violation, and every asset class is inside its band.  
   <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SuitabilityViolations (none open); reference.json StrategicAssetAllocations bands</sub>
4. **Watch.** 43.6% of the book is in holdings on none of the bank's recommendation lists, largest iShares STOXX Europe 600 UCITS, JPMorgan Chase & Co. and 10 more.  
   <sub>reference.json Securities.InRecommendationList; custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08 positions</sub>
5. **Watch.** Information Technology is 10.7% of the book (CHF 290k) after fund look-through, mostly via SAP SE.  
   <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "That means maintaining an overweight position in technology stocks."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Nicole Baumann is calling: no risk profile, CHF 2.70m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 32k today, −1.2% of the book. Mostly Information Technology, −4.8% on 10.7% of it.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08 holdings</sub>
3. **digest.** About −CHF 32k today, −1.2% of the book.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08 holdings</sub>
4. **digest.** About −CHF 14k from Information Technology, −4.8% today on 10.7% of the book, mostly SAP SE.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08 holdings</sub>
5. **digest.** About −CHF 8k from the dollar, −1.2% against the franc on 24.8% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08 holdings</sub>
6. **digest.** About −CHF 3k from the euro, −0.3% against the franc on 42.1% of the book.  
   <sub>market feed "tech-selloff": EURCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** 35.7% of the book has no matching market move and is not included.  
   <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08 holdings without a mapped market move</sub>
10. **holding.** Holding up today: Consumer Staples +0.3% (6.3% of the book); foreign bonds +0.3% (3.7% of the book).  
   <sub>market feed "tech-selloff": S5CONS Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.11): SAP SE alone is 10.7% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: Portfolios[EXT-08-01].SecurityPositions</sub>
- **Watch** (0.10): Financials is 10.4% of the book (CHF 280k) after fund look-through, mostly via Zurich Insurance Group AG.  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.10): Zurich Insurance Group AG alone is 10.4% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: Portfolios[EXT-08-01].SecurityPositions</sub>
- **Watch** (0.00): 42.8% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 74k, 2.7% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 83.9% of the portfolio (CHF 2.27m).  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 6.4% of the portfolio (CHF 173k).  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 5.0% of the portfolio (CHF 135k).  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 2.7% of the portfolio (CHF 74k).  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 1.9% of the portfolio (CHF 52k).  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Information Technology is 10.7% of the portfolio (CHF 290k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 10.4% of the portfolio (CHF 280k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 8.2% of the portfolio (CHF 223k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 7.8% of the portfolio (CHF 210k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 6.3% of the portfolio (CHF 169k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 6.1% of the portfolio (CHF 166k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 4.9% of the portfolio (CHF 134k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Euro: 42.1% of the portfolio (CHF 1.14m).  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Swiss francs: 26.8% of the portfolio (CHF 724k).  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 24.8% of the portfolio (CHF 670k).  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Andere: 6.3% of the portfolio (CHF 169k).  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Gold: CHF 80k, 2.9% of the portfolio.  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares STOXX Europe 600 UCITS, CHF 600k (22.2% of the portfolio).  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 19 holdings; the largest: iShares STOXX Europe 600 UCITS (CHF 600k), SAP SE (CHF 290k), Zurich Insurance Group AG (CHF 280k), ABB Ltd (CHF 223k).  
  <sub>custody statement Quartalsreporting_Q4_2025_08_Frau_Nicole_Baumann.pdf (Privatbank Helvetia AG) EXT-08: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## EXT-09 — Pensionskasse Fiktiva

no risk profile · CHF 9.20m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Pensionskasse Fiktiva, no risk profile, CHF 9.20m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +7.2% over the 12 months to Dec 2025 and +46.6% since Dec 2022, now CHF 9.20m; value change including deposits and withdrawals.  
   <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: PerformanceHistory of EXT-09-01</sub>
3. **Health check.** Nothing open: no suitability violation, and every asset class is inside its band.  
   <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SuitabilityViolations (none open); reference.json StrategicAssetAllocations bands</sub>
4. **Watch.** 67.2% of the book is in holdings on none of the bank's recommendation lists, largest iShares STOXX Europe 600 UCITS, 1.400% Kanton Waadt 2022-2030 and 14 more.  
   <sub>reference.json Securities.InRecommendationList; custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09 positions</sub>
5. **Watch.** Consumer Staples is 8.4% of the book (CHF 772k) after fund look-through, mostly via Nestlé AG and Procter & Gamble Co..  
   <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Outlook.** Standard Chartered (Global Market Outlook, Sep 2026): "We remain Underweight real estate and consumer staples amid weak sentiment and low visibility on the housing recovery."  
   <sub>https://www.sc.com/en/uploads/sites/66/content/docs/wm-global-market-outlook-its-all-about-the-yield-28-august-2026.pdf</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Pensionskasse Fiktiva is calling: no risk profile, CHF 9.20m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 68k today, −0.7% of the book. Mostly the dollar, −1.2% on 30.9% of it.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09 holdings</sub>
3. **digest.** About −CHF 68k today, −0.7% of the book.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09 holdings</sub>
4. **digest.** About −CHF 34k from the dollar, −1.2% against the franc on 30.9% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09 holdings</sub>
5. **digest.** About −CHF 11k from Information Technology, −4.8% today on 2.6% of the book, mostly iShares Core MSCI World UCITS ETF.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09 holdings</sub>
6. **digest.** About −CHF 10k from Communication Services, −3.1% today on 3.5% of the book, mostly Swisscom AG and iShares Core MSCI World UCITS ETF.  
   <sub>market feed "tech-selloff": S5TELS Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09 holdings</sub>
7. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
9. **digest.** 35.4% of the book has no matching market move and is not included.  
   <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09 holdings without a mapped market move</sub>
10. **holding.** Holding up today: Swiss franc bonds +0.2% (22.3% of the book); Consumer Staples +0.3% (8.4% of the book); foreign bonds +0.3% (7.5% of the book).  
   <sub>market feed "tech-selloff": SBR14T Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.07): Consumer Discretionary is 7.2% of the book (CHF 659k) after fund look-through, mostly via 0.500% Schweiz. Eidgenossenschaft 2020-2032 and LVMH Moët Hennessy SE.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.00): 63.9% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 411k, 4.5% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 53.4% of the portfolio (CHF 4.91m).  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 29.8% of the portfolio (CHF 2.75m).  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 10.6% of the portfolio (CHF 980k).  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 4.5% of the portfolio (CHF 411k).  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 1.7% of the portfolio (CHF 153k).  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Consumer Staples is 8.4% of the portfolio (CHF 772k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Discretionary is 7.2% of the portfolio (CHF 659k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 5.8% of the portfolio (CHF 533k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Communication Services is 3.5% of the portfolio (CHF 324k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Information Technology is 2.6% of the portfolio (CHF 238k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 1.6% of the portfolio (CHF 144k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 1.2% of the portfolio (CHF 114k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 0.5% of the portfolio (CHF 45k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Raw materials is 0.4% of the portfolio (CHF 36k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Utilities is 0.3% of the portfolio (CHF 23k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Real Estate is 0.2% of the portfolio (CHF 21k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 38.4% of the portfolio (CHF 3.53m).  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 33.9% of the portfolio (CHF 3.12m).  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 26.5% of the portfolio (CHF 2.44m).  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): British pound: 1.2% of the portfolio (CHF 108k).  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Gold: CHF 185k, 2.0% of the portfolio.  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares STOXX Europe 600 UCITS, CHF 1.07m (11.6% of the portfolio).  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 22 holdings; the largest: iShares STOXX Europe 600 UCITS (CHF 1.07m), iShares Core MSCI World UCITS ETF (CHF 964k), 1.400% Kanton Waadt 2022-2030 (CHF 758k), 3.000% Nestlé Finance Intl 2022-2030 (CHF 695k).  
  <sub>custody statement Quartalsreporting_Q4_2025_09_Pensionskasse_Fiktiva.pdf (Privatbank Helvetia AG) EXT-09: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>

---

## EXT-10 — Thomas Gerber

no risk profile · CHF 1.45m · ESG preference: no

### 60-second briefing (dashboard)

1. **Who.** Thomas Gerber, no risk profile, CHF 1.45m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **Development.** Portfolio value +8.6% over the 12 months to Dec 2025 and +45.6% since Dec 2022, now CHF 1.45m; value change including deposits and withdrawals.  
   <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: PerformanceHistory of EXT-10-01</sub>
3. **Health check.** Nothing open: no suitability violation, and every asset class is inside its band.  
   <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SuitabilityViolations (none open); reference.json StrategicAssetAllocations bands</sub>
4. **Watch.** 49.9% of the book is in holdings on none of the bank's recommendation lists, largest iShares MSCI Emerging Mkts UCITS, Sony Group Corp. and 13 more.  
   <sub>reference.json Securities.InRecommendationList; custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10 positions</sub>
5. **Watch.** Information Technology is 11.2% of the book (CHF 162k) after fund look-through, mostly via ASML Holding NV and SAP SE.  
   <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
6. **Outlook.** Pictet Asset Management (Barometer, Sep 2026): "That means maintaining an overweight position in technology stocks."  
   <sub>https://am.pictet.com/ch/en/investment-views/multi-asset/2026/september-barometer-of-financial-markets-outlook</sub>
7. **Next best actions.** Book a review: no finalised proposal on record.  
   <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: Proposals</sub>

### Incoming call during "tech-selloff" (simulated market)

1. **caller.** Thomas Gerber is calling: no risk profile, CHF 1.45m across 1 portfolio.  
   <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: RiskProfileName, EsgProfileName, AssetsUnderManagementInDefaultCurrency</sub>
2. **reason.** Probably the market: about −CHF 14k today, −1.0% of the book. Mostly Information Technology, −4.8% on 11.2% of it.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10 holdings</sub>
3. **digest.** About −CHF 14k today, −1.0% of the book.  
   <sub>impact of the market feed on custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10 holdings</sub>
4. **digest.** About −CHF 8k from Information Technology, −4.8% today on 11.2% of the book, mostly ASML Holding NV and SAP SE.  
   <sub>market feed "tech-selloff": S5INFT Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10 holdings</sub>
5. **digest.** About −CHF 4k from the dollar, −1.2% against the franc on 20.5% of the book.  
   <sub>market feed "tech-selloff": USDCHF Curncy CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10 holdings</sub>
6. **digest.** Behind the move: "Chip stocks slide after export-control headlines"  
   <sub>market feed "tech-selloff" headline</sub>
7. **digest.** Behind the move: "Dollar weakens as rate-cut bets rise"  
   <sub>market feed "tech-selloff" headline</sub>
8. **digest.** About −CHF 1k from Financials, −0.9% today on 10.8% of the book, mostly Zurich Insurance Group AG and UBS Group AG.  
   <sub>market feed "tech-selloff": S5FINL Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10 holdings</sub>
9. **digest.** 30.9% of the book has no matching market move and is not included.  
   <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10 holdings without a mapped market move</sub>
10. **holding.** Holding up today: foreign bonds +0.3% (9.8% of the book); Consumer Staples +0.3% (7.9% of the book); Swiss franc bonds +0.2% (6.9% of the book).  
   <sub>market feed "tech-selloff": LEGATRUU Index CHG_PCT_1D × custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10 holdings</sub>

<details><summary>Other facts on the card</summary>

- **Watch** (0.11): Financials is 10.8% of the book (CHF 156k) after fund look-through, mostly via Zurich Insurance Group AG and UBS Group AG.  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions × reference.json FundUnbundlingMappings, Securities.SAA_IndustryName</sub>
- **Watch** (0.00): 49.9% of the book has no industry breakdown (bonds, funds without look-through).  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions; reference.json FundUnbundlingMappings</sub>
- **Watch** (0.00): Cash on hand is CHF 60k, 4.1% of the book.  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: LiquidityInDefaultCurrency</sub>
- **Watch** (0.00): Shares are 69.9% of the portfolio (CHF 1.01m).  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Bonds are 16.7% of the portfolio (CHF 242k).  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Alternatives and commodities are 7.5% of the portfolio (CHF 108k).  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Cash is 4.1% of the portfolio (CHF 60k).  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Real estate are 1.8% of the portfolio (CHF 27k).  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Information Technology is 11.2% of the portfolio (CHF 162k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Financials is 10.8% of the portfolio (CHF 156k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Consumer Staples is 7.9% of the portfolio (CHF 115k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Energy is 7.9% of the portfolio (CHF 115k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Industrials is 5.7% of the portfolio (CHF 83k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Health Care is 2.5% of the portfolio (CHF 36k) after fund look-through.  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities × FundUnbundlingMappings</sub>
- **Watch** (0.00): Swiss francs: 38.9% of the portfolio (CHF 565k).  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Euro: 28.6% of the portfolio (CHF 416k).  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): US-Dollar: 20.5% of the portfolio (CHF 297k).  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Andere: 12.0% of the portfolio (CHF 173k).  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Gold: CHF 33k, 2.3% of the portfolio.  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): Largest holding: iShares MSCI Emerging Mkts UCITS, CHF 174k (12.0% of the portfolio).  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities</sub>
- **Watch** (0.00): 23 holdings; the largest: iShares MSCI Emerging Mkts UCITS (CHF 174k), Nestlé AG (CHF 115k), TotalEnergies SE (CHF 115k), Zurich Insurance Group AG (CHF 110k).  
  <sub>custody statement Quartalsreporting_Q4_2025_10_Herr_Thomas_Gerber.pdf (Privatbank Helvetia AG) EXT-10: SecurityPositions, AccountPositions × reference.json Securities</sub>

</details>
