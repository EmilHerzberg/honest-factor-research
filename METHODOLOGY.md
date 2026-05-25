# Methodology — The Model-Honesty Principle

> **Core principle:** prefer a lower-but-honest R² over a higher-but-inflated
> R² that comes from mirror artifacts, regime-averaged betas, or
> distributional-assumption violations.

This document explains the methodological choices behind the code in this
repo. The goal is not to maximize R² — it is to **maximize the amount of
variance we can honestly defend**.

> ⚠️ **Important.** This methodology measures *correlations* in historical
> data. It does not claim that any factor *causes* any asset's return.
> Empirical patterns documented here may not generalize to future periods,
> different universes, or different preprocessing choices. This is
> **research and evaluation tooling, not an investment system.**

## Scope of claims

What this methodology *does* support:

- Detecting when an R² is inflated by sector-mirror effects
- Quantifying R² uncertainty via non-parametric resampling
- Identifying regime-dependent factor relationships
- Comparing proxy ETFs to alternative measurements of the same concept

What this methodology *does NOT* support:

- Predicting future returns
- Generating trading signals
- Establishing causal relationships
- Making claims that generalize to markets or periods not in the data
- Substituting for proper out-of-sample backtesting in a production
  investment process

## Why "honest" R² matters

A factor model that reports R²=0.85 sounds impressive. But that single
number hides four things that determine whether the model is actually
useful:

1. **How much of the R² comes from real-world-priced factors** (rates,
   inflation, oil-spot, VIX-spot) vs **academic style factors** (value,
   momentum) vs **sector basket ETFs** (XLF, XLV)?
2. **Whether the asset itself is a meaningful constituent of the factor
   basket** (e.g. XOM is 22% of XLE — regressing XOM against XLE is
   partially regressing XOM against itself)?
3. **Whether the same beta holds in a market crisis vs a calm regime?**
4. **How uncertain the R² is** given fat-tailed daily returns?

If R²=0.85 looks great but is 60% sector-mirror, regime-specific is ±0.4 in
either direction, and the 90% CI is [0.55, 0.92], you have a model that
*sounds* explanatory but is actually unreliable.

## The four design principles

### Principle 1 — Empirical validation before factor inclusion

Every factor proposal is tested via **marginal Δr²** against a broad
universe (>1,000 stocks) before being added to the catalog.

Implemented in: [`honest_factor_research/analysis/replacement_test.py`](honest_factor_research/analysis/replacement_test.py)
+ [`honest_factor_research/analysis/broad_universe.py`](honest_factor_research/analysis/broad_universe.py).

**Counterintuitive result we found:** Gold (which theory says is essential
for safe-haven hedging) delivered only Δr²=+0.005 on a 2,241-asset universe.
Lithium (which I expected to be niche) delivered Δr²=+0.010 — more than
double Gold's contribution. The lesson: **brainstorm intuition is unreliable
without empirical validation**.

### Principle 2 — Factor classification (DIRECT / STATISTICAL / DERIVED)

Not all factors are epistemically equal:

| Class | Definition | Examples |
|---|---|---|
| **DIRECT_PHYSICAL** | Has a real-world price or measurable macro quantity | rates, inflation, VIX-spot, Brent, gold, copper, USD-DXY |
| **STATISTICAL_FACTOR** | Academic premium with long literature + multiple valid proxies | market_beta, value, growth, momentum, quality |
| **DERIVED_THEME** | ETF-basket constructed by index methodology; heterogeneous components | semiconductors, XLF (Financials), XLV (Healthcare), country ETFs |

When the LLM (or human analyst) maps an event to a DIRECT factor, the
mechanism is verifiable. When mapping to a DERIVED factor, the explanation
is "this event affects this sector basket" — which may be true, but the
sector basket itself is heterogeneous (XLV is 10% UnitedHealth which is
basically a health insurer, not a pharma company).

Implemented in: [`docs/02-factor-taxonomy.md`](docs/02-factor-taxonomy.md).

### Principle 3 — Trust-stratified R² decomposition

Run three separate regressions per asset×window:

1. R² with DIRECT factors only → `r²_direct`
2. R² with DIRECT + STATISTICAL factors → `r²_+statistical`
3. R² with all factors (including DERIVED) → `r²_total`

Compute `derived_share = (r²_total − r²_+statistical) / r²_total`.

A high derived_share means most of the model's "explanation" comes from
sector baskets — possibly mirroring the asset's own contribution to those
baskets. Examples we found in our 60-asset universe:

- DUK (Utility): r²_total=0.735 looks great, but r²_direct=0.174,
  derived_share=62.5%. The DUK exposure is mostly xl_utilities mirroring
  itself.
- XOM (Energy): r²_total=0.753, r²_direct=0.185, derived_share=57.4%.
  XOM is 22% of XLE — half the apparent fit is self-mirror.
- JPM (Bank): r²_total=0.85 BUT r²_direct=0.20, derived_share=65%.
  The mirror artifact is huge.

Implemented in: [`honest_factor_research/analysis/trust_stratified.py`](honest_factor_research/analysis/trust_stratified.py).

### Principle 4 — Quantify uncertainty empirically

Two sources of uncertainty Ridge-regression hides:

**(a) Fat-tailed daily returns.** Ridge minimizes squared errors —
implicitly assumes Gauß errors. But daily-return kurtosis is 3-10
(vs Gauß-value 3). R² gets pulled to "normal" days; crisis days are
underweighted as noise.

**Solution:** stationary block-bootstrap (Politis-Romano 1994). Resample
random-length contiguous blocks from the window (with wraparound).
Geometric-distributed block lengths preserve autocorrelation. Refit Ridge
500 times, report the 5th and 95th percentile of R² as a 90% CI.

WMT 2021-02-26: R²=0.64, CI=[0.39, 0.82] → 0.43 spread → don't trust the
point estimate; AAPL 2023-06: R²=0.62, CI=[0.59, 0.65] → 0.06 spread → trust.

Implemented in: [`honest_factor_research/exposure/bootstrap.py`](honest_factor_research/exposure/bootstrap.py).

**(b) Regime-dependent betas.** The same regression on the same factor can
produce very different betas in High-VIX vs Low-VIX days:
- GE × value: +2.94 (VIX>25) vs -0.15 (VIX<15) — sign reversal
- O (Realty Income) × rates_30y: +1.43 (rising rates) vs -1.33 (falling)

The Ridge-fit on the full 252-day window averages over these regimes,
producing a beta that's wrong in BOTH regimes when the asset has
regime-dependence.

**Solution:** refit Ridge on VIX-stratified subsets of the same window.
Store `exposure_value_low_vix` and `exposure_value_high_vix` alongside the
unconditional `exposure_value`. Skip when the regime has <60 days in the
window (caller falls back to unconditional).

Implemented in: [`honest_factor_research/exposure/regime.py`](honest_factor_research/exposure/regime.py).

## Key design decisions

### Why sequential Gram-Schmidt residualization?

The 18+ factor ETFs are heavily multicollinear (SOXX-QQQ ρ≈0.85, IWF-SPY
ρ≈0.70). Running Ridge on the raw matrix gives unstable betas with mixed
signs.

Sequential residualization (Barra-Axioma convention):
- Tier 1: `market_beta` = raw SPY return
- Tier 2: `rates` = OLS-residual of IEF on `market_beta`
- Tier 3: `value` = residual of IWD on (market_beta, rates)
- Tier 4: `growth` = residual of IWF on (market_beta, rates, value)
- Tier 5: sector and geo factors

After residualization, ρ between any pair of factors is typically <0.30.
The tier order encodes economic priority: market beta first, then macro
factors, then style, then sector, then geo.

**Caveat we documented:** the original V3.2 design had `growth` at tier 3
(same as `value`), producing growth↔value ρ=-0.925 (near-perfect
anti-correlation, basically double-counting style information). Fix: move
growth to tier 4 with value as additional regressor → ρ=0.000.

This is a real example of the methodology catching its own mistakes —
documented in [`docs/risks-and-improvements.md`](docs/risks-and-improvements.md)
as Risk #3.

### Why sector-conditional factors?

Adding 12 new sector-specific factors universally would bloat the regression
for assets that don't need them. Instead, factors can declare
`applicable_sectors: [...]` and the pipeline only loads them for assets
whose GICS sector matches.

Implemented in: [`honest_factor_research/exposure/pipeline.py`](honest_factor_research/exposure/pipeline.py).

Examples we use:
- `gold` (GLD): only Basic Materials
- `natural_gas` (UNG): only Energy
- `biotech` (IBB): only Health Care (because XLV includes UnitedHealth which
  isn't biotech)
- `defense` (ITA): only Industrials (XLI includes transport/machinery)

Documented in: [`docs/04-sector-conditional.md`](docs/04-sector-conditional.md).

### Why yfinance + NASDAQ-screener instead of paid data?

Reproducibility for an open-source project. Anyone can clone this repo and
re-run the analysis with the same data sources we used. Limitations are
documented (survivorship bias, occasional bad ticks); a production system
would use Bloomberg/Refinitiv with proper survivorship-bias-free historical
data.

## What this methodology does NOT solve

- **Trading-signal generation**: this is exposure research, not strategy
  backtest. R² improvements don't directly translate to alpha.
- **Survivorship bias**: limited to today's listed universe.
- **Regime detection at decision-time**: the regime-stratified betas are
  computed offline; a production system would need a current-regime
  classifier.
- **Distributional shift over time**: assumes 5-year stationary structure
  per 252-day window. Major regime breaks (2008, 2020) cause window
  contamination.
- **Outcome calibration**: high R² doesn't mean predictions are calibrated.
  That requires real outcome data over time — out of scope for this repo.

These limitations are explicitly tracked in
[`docs/future-investigations.md`](docs/future-investigations.md) so the
research doesn't pretend to be more complete than it is.

---

*This is an evolving methodology. The principles above represent the
state of thinking after several weeks of empirical iteration. Future
revisions will be tracked in [`docs/risks-and-improvements.md`](docs/risks-and-improvements.md)
as new findings emerge.*
