# Trust-Stratified R² Decomposition

> **The headline methodology of this repo.** A single R² hides where the
> explanation comes from. This document explains what we decompose, why,
> and how to read the output.

## The problem

A factor model reports R²=0.85. Sounds great. But it could be one of two
very different things:

**Scenario A:** the R² comes from rates, inflation, market beta, and a
robust value factor — all things that are real-world-priced and where the
relationship has decades of empirical history.

**Scenario B:** the R² comes mostly from a sector ETF in which the asset
itself is a major constituent. The model is fitting the asset against a
basket that contains it. The "explanation" is partially the asset
explaining itself.

A single R² number can't distinguish these. So we decompose.

## The decomposition

For each (asset, snapshot, 252-day window) we run THREE separate Ridge
regressions:

| # | Regression | What it captures |
|---|---|---|
| 1 | y ~ DIRECT only | Explanation from real-world-priced factors only |
| 2 | y ~ DIRECT + STATISTICAL | + Academic style factors |
| 3 | y ~ ALL factors | + Sector basket factors |

```
r²_direct       = R² of regression #1
r²_+statistical = R² of regression #2
r²_total        = R² of regression #3   (= the usual "R²")
1 − r²_total    = honest idiosyncratic variance
```

### Derived metric

```
derived_share = (r²_total − r²_+statistical) / r²_total
```

This is **the fraction of explanation that comes from DERIVED-tier
factors** (sector baskets). High derived_share is the warning sign.

## How to read the output

For one asset, the report tells you four things:

> **AAPL (hypothetical):**
> - r²_direct = 0.18 (DIRECT factors explain 18% of variance)
> - r²_+statistical = 0.42 (STATISTICAL adds another 24%)
> - r²_total = 0.62 (DERIVED adds another 20%)
> - derived_share = 32%

Read as: **"AAPL: 18% sure-explained, 24% half-explained, 20%
mirror-suspect, 38% idiosyncratic."**

vs. the standard "R²=0.62" which says nothing about the composition.

## The four assessment patterns

After running on a universe of assets, you'll see these patterns:

### Pattern 1 — Honest high-R² (robust)
- Both r²_direct and r²_total are high
- Low derived_share (< 20%)
- Example assets: index ETFs (SPY, VTI), large-cap diversified (BLK)
- Interpretation: model genuinely captures these. Trust the betas.

### Pattern 2 — Mirror artifact (suspicious)
- r²_total is high (0.7+) but r²_direct is low (< 0.2)
- High derived_share (> 50%)
- Example assets: energy stocks (XOM/COP) against XLE; utilities (DUK)
  against XLU
- Interpretation: most of the R² comes from a sector ETF that contains
  the asset. The "explanation" is partially self-mirror.

### Pattern 3 — Genuinely hard to model
- All three R² values low (< 0.3)
- High idiosyncratic share (> 70%)
- Example assets: small-cap pharma (MRNA), niche consumer (DLTR)
- Interpretation: macro/style/sector factors don't capture this asset's
  variance. Would need fundamental-data factors.

### Pattern 4 — Real sector exposure
- r²_total > r²_+statistical (good DERIVED contribution)
- Moderate derived_share (20-40%)
- Asset is NOT in the relevant sector ETF
- Example: a bank holding company that's not in XLF
- Interpretation: legitimate factor explanation. Trust.

## The reclassification table

We translate the three R² values into a new **asset-quality tier** that
penalizes mirror-suspect assets:

```python
def derive_tier(r2_direct, r2_statistical, r2_total):
    derived_share = (r2_total - r2_statistical) / max(r2_total, 0.01)

    if r2_direct >= 0.35:
        return "HIGH"  # Solid foundation in hard factors

    if r2_statistical >= 0.45 and derived_share < 0.30:
        return "MED"   # Mostly statistical, low DERIVED reliance

    if r2_total >= 0.55 and derived_share < 0.50:
        return "MED_DERIVED_HEAVY"  # High R² but DERIVED-dominated

    return "LOW"
```

The `MED_DERIVED_HEAVY` tier is the new addition — it flags assets that
LOOK high-quality under standard metrics but are mirror-dependent.

## What we found empirically

On a 60-asset MVP universe (S&P 500 + mid-caps):

- **32 of 60 assets (53%) got a tier downgrade** under trust-stratified
  vs. monolithic R²
- 6 assets dropped from HIGH to LOW — specifically energy and utility
  stocks
- The downgraded set was predictable in retrospect: stocks that ARE in
  their own sector ETFs

When we then ran the same analysis after fixing the model (V3.5 added
Brent as DIRECT energy factor, moving energy_oil out of DERIVED):

- Mean r²_direct: **0.351 → 0.432 (+23%)**
- Mean derived_share: **25.3% → 20.3%** (less mirror)
- HIGH-to-LOW downgrades: **6 → 3** (-50%)

This demonstrates that the methodology not just diagnoses problems —
acting on its findings produces measurable improvements in model honesty.

## Implementation

See [`honest_factor_research/analysis/trust_stratified.py`](../honest_factor_research/analysis/trust_stratified.py).

## Limitations

- The classification of a factor as DIRECT/STATISTICAL/DERIVED is itself
  a judgment call. We use the catalog in
  [`honest_factor_research/config/factors.yaml`](../honest_factor_research/config/factors.yaml)
  but reasonable people could disagree on edge cases (is `growth` really
  STATISTICAL or partially DERIVED given how IWF concentration shifts
  over time?).
- The three regressions don't account for residualization order between
  classes (Ridge with all DIRECT factors might overfit if there's
  collinearity). Empirically this seems fine for 5-10 DIRECT factors,
  but watch out for it if you add many more.
- `r²_direct` is itself an in-sample fit — not a out-of-sample
  generalization metric. Use cross-validation if you want generalization
  guarantees.
