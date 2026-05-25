# Risks and Improvements

> **Living document.** Tracks identified weaknesses in the current
> methodology with their possible mitigations, trade-offs, and rationale
> for current choices. Each entry follows the structure:
> Problem → Options → Pros/Cons → Current decision → Action items.
>
> **Append-only.** New risks are appended below, old ones not edited (only
> status updates allowed).

---

## Risk #1 — Single-Sample R² Bias

**Status:** Mitigated by Block-Bootstrap CI (V3.5). See
[`docs/06-fat-tails-mitigation.md`](06-fat-tails-mitigation.md).

### The problem

Ridge L2-loss minimizes squared errors, implicitly assuming Gauß residuals.
Daily-return residuals have kurtosis 3-10 (vs Gauß = 3). Point R² is biased
toward "normal" days; extreme days (COVID-crash, SVB-collapse) are
underweighted as noise.

A window that contains an extreme period reports R² that's a mean across
"normal" days and "crisis" days where the model fits differently — the
reported R² has high variance across resamples.

### Mitigation (V3.5, implemented)

Stationary block-bootstrap (Politis-Romano) produces a non-parametric 90%
CI for R²:
- `r_squared_p05` = 5th percentile across 200 resamples
- `r_squared_p95` = 95th percentile

Wide CI = high uncertainty (don't trust the point estimate).
Narrow CI = low uncertainty (point estimate is reliable).

See [`exposure/bootstrap.py`](../honest_factor_research/exposure/bootstrap.py).

---

## Risk #2 — Static Beta Hides Regime Dependence

**Status:** Mitigated by Regime-Switching Betas (V3.5). See
[`docs/05-regime-switching.md`](05-regime-switching.md).

### The problem

Ridge over a 252-day window produces ONE beta per (asset, factor) — a mean
across all market regimes in the window. Analysis 10 showed that **18.3%
of asset-factor pairs** have |t_diff| ≥ 2.5 between high-VIX (>25) and
low-VIX (<15) regimes. Most extreme: GE × value flips +2.94 → -0.15.

Static beta is a mean — in any specific regime it can be substantially
wrong, and the gap is largest in the regimes where you most need accuracy
(crisis events).

### Mitigation (V3.5, implemented)

Pipeline now computes `exposure_value_low_vix` and `exposure_value_high_vix`
in addition to unconditional `exposure_value`. Skipped when subset < 60
days (consumer falls back to unconditional).

Downstream code (e.g. event impact propagators) can read current VIX-spot
at decision time and select the appropriate beta column.

### Open

- Adding regime stratification for Rates and Bull-Bear regimes (currently
  only VIX-regimes are stored — the others are diagnostic-only in
  Analysis 10)
- Combining multiple regimes at decision time (tie-breaker logic)
- Validating regime betas against out-of-sample outcomes (requires
  outcome library — see Risk #4)

---

## Risk #3 — Factor-Orthogonality Failure (e.g. growth↔value ρ=-0.925)

**Status:** Phase 1 fixed (re-ordered residualization tier).

### The problem

The original residualization order had `growth` at tier 3 alongside
`value`, both residualized against `market_beta` + `rates` but NEVER
against each other. Empirical correlation: ρ=-0.925 (catastrophic
anti-correlation, basically double-counting style information).

### Mitigation (implemented)

Moved `growth` to tier 4 with `residualized_against=[market_beta, rates,
value]`. Result: `growth × value = +0.000`, max |ρ| off-diagonal dropped
from 0.925 to 0.558.

See the config in [`config/factors.yaml`](../honest_factor_research/config/factors.yaml)
and the diagnostic in [`analysis/orthogonality.py`](../honest_factor_research/analysis/orthogonality.py).

### Open

- Remaining defensive-sector cluster: `xl_real_estate ↔ xl_utilities`
  ρ=0.558, `xl_consumer_defensive ↔ xl_utilities` ρ=0.547. Could be
  fixed with another tier-residualization round, but these are
  structurally related (bond-proxy sectors) so we accept the residual
  correlation.

---

## Risk #4 — Sector Factors Missing for Several GICS Sectors

**Status:** Resolved by V3.3 expansion (6 GICS sector factors added) +
V3.4 Option B (sector-conditional factors).

### The problem

The original V3.2 MVP catalog had only 2 sector factors (`semiconductors`,
`energy_oil`) + 1 geo (`china_exposure`). The 11 GICS sectors were only
partially covered. Sectors like Financials, Healthcare, Utilities, Real
Estate had no dedicated factor.

### Mitigation (V3.3 implemented)

Added 6 GICS sector factors as universal: XLF, XLV, XLI, XLP, XLU, XLRE.

### Further Mitigation (V3.4 Option B implemented)

Added 6 sector-conditional factors for sub-industries that the broad
sector ETFs don't capture well: `gold` (Basic Materials), `copper`
(Basic Materials), `natural_gas` (Energy), `biotech` (Health Care),
`defense` (Industrials), `china_a_shares` (Materials/Industrials/Energy).

See [`docs/04-sector-conditional.md`](04-sector-conditional.md).

---

## Risk #5 — Index-Purity (Proxies Don't Match Their Labels)

**Status:** Identified for 3 fundamentally_different proxies + 2
different_proxy via Analysis 5. Phase 1 mitigations implemented.

### The problem

Some factor-ETF proxies don't measure what their name suggests:

| Factor | Issue |
|---|---|
| `inflation` (TIP-IEF) | ρ=0.73 vs VTIP-IEF (different inflation concept) |
| `xl_healthcare` (XLV) | ρ=0.76 vs IBB (XLV includes UnitedHealth, not pure pharma/biotech) |
| `china_exposure` (FXI) | ρ=0.79 vs ASHR (FXI is HK-tech-biased) |
| `usd_strength` (UUP) | ρ=0.81 vs USDU (DXY-basket vs trade-weighted) |
| `xl_industrials` (XLI) | ρ=0.90 vs ITA (XLI pollutes with transport/machinery) |

See [`analysis/index_purity.py`](../honest_factor_research/analysis/index_purity.py)
and [`docs/02-factor-taxonomy.md`](02-factor-taxonomy.md) for details.

### Mitigation (V3.4 implemented)

Added biotech (IBB), defense (ITA), china_a_shares (ASHR) as
sector-conditional factors. Other index-purity issues are accepted but
documented — using the original proxies with explicit caveats.

### Open

- inflation factor needs a cleaner FRED-based breakeven series (out of
  scope: this repo intentionally uses only yfinance-accessible data for
  reproducibility)
- A proper survivorship-bias-free constituent universe (out of scope:
  would require Bloomberg/Refinitiv)
