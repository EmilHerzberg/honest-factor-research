# Factor Taxonomy and Validity

> **Living document.** Classifies the 28 factors used in this repo by
> **derivation directness** and documents **index-purity issues** with each
> proxy ETF. Foundation for the trust-stratified R² decomposition in
> [Analysis 6](../honest_factor_research/analysis/trust_stratified.py).

## 1. Motivation

The standard approach to factor models treats all factors as equivalent
dimensions: LLM (or analyst) proposes an event-factor mapping, regression
multiplies asset×factor exposure, gate engine decides based on the
aggregate impact score.

**The problem:** factors are NOT equivalent in their derivability from
events. Three very different situations collapse into the same data
structure:

1. **"Strait of Hormuz is blocked"** → effect on `energy_oil` is
   **mechanically direct** (physical supply shock). Brent futures react
   in minutes. No interpretation needed — a lookup rule suffices.

2. **"FOMC raises rates 25bp against expectation"** → effect on `rates` is
   **historically calibratable**. We have 250+ FOMC dates since 2000 with
   measured reactions; isotonic regression on historical data gives a real
   probability.

3. **"ChatGPT is launched"** → effect on which of our 28 factors? `growth`?
   `semiconductors`? `quality`? The LLM **guesses** plausibly — but we
   can't calibrate, because there's no historical analog.

When we treat all three classes identically, imprecision at the factor end
translates to **hallucination at the gate end**. The model makes
self-confident predictions about things it actually knows nothing about.

## 2. Three directness classes

### Class A — DIRECT_PHYSICAL

**Definition:** the factor corresponds to a **real-world price** or a
**directly measurable macroeconomic quantity**. Event-to-factor effect is
mechanical and in many cases derivable without LLM interpretation.

**Characteristics:**
- There's a "truth" behind the proxy (Brent spot, CPI YoY, 10Y yield, VIX)
- The ETF proxy is an approximation with its own measurement artifacts
  (e.g. VXX contango), but the underlying quantity is unambiguous
- Known event types have **deterministic** effect directions (CPI up
  → inflation factor positive, no debate)

**Implication:** these factors can be fed with **hardcoded rules** instead
of LLM interpretation for known event types. Default confidence HIGH.

### Class B — STATISTICAL_FACTOR

**Definition:** academically-validated factor construct with a **long
empirical history**. Premium and risk characteristics are broadly
documented in literature and practice. Event reactions are
statistically measurable.

**Characteristics:**
- Construct has been established in quant literature for ≥20 years
- Has a clear methodological definition (e.g. "Russell-1000-Value-Score",
  "MSCI-Momentum 12-1m")
- Multiple competing proxies exist — they typically correlate ≥0.9
- Event reaction can be calibrated via historical-outcome library

**Implication:** LLM mapping is legitimate, but confidence should come
from **historically-calibrated Brier-score stratification**, not LLM
self-assessment.

### Class C — DERIVED_THEME

**Definition:** ETF basket construct designed to represent a **sector or
theme**, but whose contents are **heterogeneous**. Multiple distinct
economic mechanisms are bundled in the same ETF. There's no single
"truth" behind the factor.

**Characteristics:**
- ETF consists of 30-100 stocks across different sub-industries
- Top holdings are often concentrated (Berkshire is 13% of XLF, UNH is
  10% of XLV)
- "What this factor MEASURES" is semantically unclear
- Event reaction is guess — LLM produces plausible-sounding explanations
  without empirical validation

**Implication:** LLM mapping is speculation. Default LOW confidence —
PROBE gates allowed but no BLOCK. These factors are better as R²-boosters
for the regression than as event-mapping targets.

## 3. Classification of the 28 factors in this repo

| Factor | Proxy ETF | Class | What's the "truth"? | Direct event-mapping possible? |
|---|---|---|---|---|
| `market_beta` | SPY | STATISTICAL | S&P 500 Index | No (market reacts to everything) |
| `rates` | IEF | **DIRECT** | 10Y Treasury Yield (^TNX) | **Yes** — FOMC, CPI, NFP have mechanical effects |
| `rates_30y` | TLT | **DIRECT** | 30Y Treasury Yield | **Yes** |
| `inflation` | TIP-IEF spread | **DIRECT** | CPI YoY, 5Y/10Y Breakeven | **Yes** — CPI print directly mappable |
| `usd_strength` | UUP | **DIRECT** | DXY | **Yes** — Fed interventions, EUR crisis |
| `volatility` | ^VIX | **DIRECT** | VIX spot | **Yes** — vol-spike events |
| `credit_hy_spread` | HYG-IEF spread | **DIRECT** | HY-OAS | **Yes** — credit-stress events |
| `energy_oil` | Brent (BZ=F) | **DIRECT** | Brent crude price | **Yes** — Hormuz, OPEC |
| `value` | IWD | STATISTICAL | Russell-1000-Value | Partial — via style-rotation events |
| `growth` | IWF | STATISTICAL *(weak)* | Russell-1000-Growth | Difficult — definitionally anti-value |
| `momentum` | MTUM | STATISTICAL | MSCI USA Momentum | Mechanically slow (12mo window) |
| `quality` | QUAL | STATISTICAL | MSCI USA Quality | Limited — earnings-driven |
| `semiconductors` | SOXX | **DERIVED_THEME** | Chip industry (AI? Memory? Foundry?) | Only partially |
| `xl_*` (six) | XLF/V/I/P/U/RE | DERIVED_THEME | Heterogeneous sector baskets | No |
| `lithium` | LIT | DERIVED_THEME | Battery/EV thematic basket | No |
| `uranium` | URA | DERIVED_THEME | Nuclear thematic basket | No |
| `china_exposure` | FXI | DERIVED_THEME *(biased)* | HK-listed China large-caps (≠ China economy) | Geo events partially |
| `gold` (cond.) | GLD | **DIRECT** | Gold spot | **Yes** |
| `copper` (cond.) | CPER | **DIRECT** | Copper futures | **Yes** |
| `natural_gas` (cond.) | UNG | **DIRECT** | Henry Hub natgas | **Yes** |
| `biotech` (cond.) | IBB | DERIVED_THEME | Biotech sub-industry | Limited |
| `defense` (cond.) | ITA | DERIVED_THEME | Defense sub-industry | Limited |
| `china_a_shares` (cond.) | ASHR | DERIVED_THEME | Mainland China | Limited |

**Distribution:**
- **DIRECT** (10-11): market-foundational + macro physical + commodities
- **STATISTICAL** (5): the academic style factors
- **DERIVED_THEME** (12-13): all the sector and theme baskets

## 4. Index-purity issues per factor

Here documented per factor where our proxy **does NOT measure what its
name claims to measure**. Tested empirically in
[Analysis 5](../honest_factor_research/analysis/index_purity.py).

### `rates` (IEF) — DIRECT with caveat

**What we want to measure:** general interest-rate sensitivity.

**What IEF actually is:** 7-10Y Treasury Bond ETF. Returns ≈ Duration ×
Yield-Change. Only ONE point on the yield curve. Front-end (Fed Funds)
moves differently than long-end (term premium).

**Better proxies:** ^TNX (yield directly), or split into SHY/IEF/TLT for
yield-curve coverage.

### `inflation` (TIP-IEF spread) — DIRECT with large caveat

**What we want:** inflation surprise / inflation expectations.

**What we measure:** daily return spread between TIP (TIPS basket) and
IEF (nominal basket). In theory a proxy for breakeven inflation.

**Problems:**
- TIP and IEF have different duration → spread contains
  duration-difference artifacts
- TIPS market is less liquid than nominal Treasuries → TIP returns are
  noisy
- No direct CPI link — we measure market-implied breakeven, not realized
  inflation

**Empirical finding (Analysis 5):** correlation of TIP-IEF vs VTIP-IEF
(short-TIPS spread) was only ρ=0.73 — these measure substantially
different inflation concepts.

### `volatility` (VXX) — DISTORTED (we replaced it)

**Original problem:** VXX is a 30-day rolling VIX-futures ETN. Suffers
**systematic contango decay** — returns trend toward zero independent of
the actual vol regime. Returns ≠ VIX moves.

**V3.5 fix:** swapped to ^VIX-Spot log-changes. Empirically much cleaner
regime signal.

### `energy_oil` (XLE) — fundamentally wrong proxy (replaced)

**Original problem:** XLE = US Energy Sector Stocks (XOM 22%, CVX 17%,
COP 5%, SLB 4%). These react to oil-price changes with LAG and
operating-leverage distortion. XLE is Equity REACTION to oil, NOT oil.

**V3.5 fix:** swapped to BZ=F (Brent crude futures). Empirical result:
r²_direct for energy stocks (XOM, COP, SLB, CVX) **doubled**.

### `xl_healthcare` (XLV) — fundamentally heterogeneous

**Problem:** UNH (UnitedHealth) is 10% of XLV — that's a **health insurer**,
not a pharma company. Plus big pharma 40%, biotech 10%, devices 15%,
services 15%.

**Empirical (Analysis 5):** XLV vs IBB (biotech only) ρ=0.76. They're
measuring substantially different things despite both being "healthcare".

**V3.5 mitigation:** added `biotech` (IBB) as sector-conditional factor
for Healthcare assets.

### `china_exposure` (FXI) — fundamentally biased

**Problem:** FXI = FTSE China 50 = 50 largest **Hong-Kong-listed** Chinese
companies. Tencent + Alibaba + Meituan + JD make up ~30% (Tech bias).
A-Shares (Shanghai/Shenzhen) contain the "real" mainland China economy.

**Empirical (Analysis 5):** FXI vs ASHR (A-Shares) ρ=0.79.

**V3.5 mitigation:** added `china_a_shares` (ASHR) as sector-conditional
factor for assets with mainland-China exposure.

## 5. Trust-stratified R² decomposition — the headline

Instead of reporting a single R² per asset, decompose into three trust tiers:

```
r²_direct       = explanation from DIRECT factors only
r²_+statistical = + STATISTICAL factors
r²_total        = + DERIVED_THEME factors
1 − r²_total    = idiosyncratic
```

**Key derived metric:**
```
derived_share = (r²_total − r²_+statistical) / r²_total
```

High `derived_share` = the model's "explanation" mostly comes from sector
baskets, which (for stocks IN those baskets) may be mirror-fitting.

**Empirical example:** AAPL hypothetical
- `r²_direct`        = 0.18 (DIRECT explains 18%)
- `r²_+statistical`  = 0.42 (STATISTICAL adds 24%)
- `r²_total`         = 0.62 (DERIVED adds another 20%)
- idiosyncratic     = 0.38

Honest statement: **AAPL: 18% sure-explained, 24% half-explained, 20%
mirror-suspect, 38% noise** — much more informative than "R²=0.62".

See [Analysis 6](../honest_factor_research/analysis/trust_stratified.py)
for implementation.

## 6. Concrete research-step suggestions

When evaluating a new factor proposal:

1. **Index-purity test (Analysis 5):** correlate the proposed proxy
   against 2-3 alternatives. If ρ<0.90, your proxy IS its methodology.
2. **Marginal Δr² test (Analysis 7):** add the factor to a baseline set,
   measure mean improvement across the asset universe.
3. **Broad-universe replay (Analysis 8):** validate the result on
   ≥1,000 stocks (not just your small MVP universe).
4. **Trust-stratified test (Analysis 6):** if the proposed factor is
   DERIVED, check whether it raises `r²_direct` (real explanation) or just
   `r²_total` (mirror artifact).

If a factor only improves `r²_total` and the improvement is concentrated
in stocks that ARE in the proposed ETF: it's a mirror artifact. Don't add.
