# Regime-Switching Betas

> **Problem:** Ridge-fit on a 252-day window produces ONE beta per
> (asset, factor) — an average across all market regimes in the window.
> **18.3% of asset-factor pairs have regime-dependent beta** with |t_diff|
> ≥ 2.5 between high-VIX and low-VIX days. Static beta is wrong in BOTH
> regimes when the asset has regime-dependence.

## The empirical finding

Analysis 10 ([`conditional_betas.py`](../honest_factor_research/analysis/conditional_betas.py))
runs OLS beta separately on VIX-stratified subsets of the same 252-day
window. Three regime stratifications:

| Regime | High level | Low level |
|---|---|---|
| **VIX** | VIX > 25 | VIX < 15 |
| **Rates** | Rising (IEF-return < p5) | Falling (IEF-return > p95) |
| **Bull-Bear** | 60d-SPY-return > +2% | < -2% |

**Worst cases found:**

| Asset × Factor | Regime | β-high | β-low | Δβ |
|---|---|---|---|---|
| GE × value | VIX | **+2.94** | **-0.15** | +3.09 sign reversal |
| JPM × value | VIX | +2.92 | +0.77 | +2.15 |
| AVGO × momentum | VIX | +0.29 | +3.01 | -2.73 magnitude flip |
| O × credit_hy_spread | VIX | +1.20 | -1.03 | +2.23 sign reversal |
| O × rates_30y | Rates | +1.43 | -1.33 | +2.76 sign reversal |
| DUK × quality | Rates | -3.85 | +1.61 | -5.46 sign reversal |

Most extreme pattern: **Index ETFs and Mega-Cap-Tech show volatility-beta
sign-flips** between bull and bear markets (classic equity leverage
effect). All of SPY, IWB, VTI, QQQ, AAPL, MSFT, GOOGL exhibit this.

## What this means for static-beta models

Suppose your model has AAPL × volatility beta = -0.05 (from the full
252-day fit). At decision time, an event reduces VIX-spot by 0.5:
- Model predicts AAPL return contribution: -0.05 × -0.5 = +0.025
- But: in current Bull regime, true β is -0.052 → contribution +0.026 ✓
- And: in Bear regime, true β might be +0.143 → contribution -0.072 ✗

The static beta works in one regime and inverts in the other. The Bull
beta is what AAPL "looks like" most of the time, so the model averages
toward it. But when you actually need accuracy (in a Bear regime,
because that's when volatility events matter most), the model is
fundamentally wrong.

## The mitigation

Re-fit Ridge with the **SAME α** the unconditional regression chose, but
on the VIX-stratified subset of the window:

```python
# Unconditional fit (existing) — uses CV-selected α
ridge_cv = RidgeCV(alphas=ALPHAS)
ridge_cv.fit(X, y)
alpha = ridge_cv.alpha_
unconditional_betas = ridge_cv.coef_

# Regime-stratified fit — REUSE the α (CV-tuning per regime would be circular)
for regime, mask in [("low_vix", vix < 15), ("high_vix", vix > 25)]:
    sub = joined.loc[mask]
    if len(sub) < 60:
        continue  # too few days in this regime — fall back to unconditional
    model = Ridge(alpha=alpha)  # fixed α
    model.fit(sub[factor_cols], sub["__y__"])
    regime_betas[regime] = model.coef_
```

Output: in addition to the unconditional `exposure_value`, the
:class:`ExposureRow` carries `exposure_value_low_vix` and
`exposure_value_high_vix`. The Propagator at decision time can read
current VIX-spot and pick the appropriate column.

## Implementation

See [`honest_factor_research/exposure/regime.py`](../honest_factor_research/exposure/regime.py)
for the core logic and [`pipeline.py`](../honest_factor_research/exposure/pipeline.py)
for the integration.

## Skipping rules

- **min_obs = 60 days** in the regime subset. Below that, the regime
  beta is too noisy — store NULL and let the Propagator fall back to
  unconditional.
- **No CV per regime.** Reusing the unconditional α keeps the regime
  betas on the same regularization scale and prevents data-snooping bias
  from per-subset CV.
- **Same factor set.** Don't add or remove factors between unconditional
  and regime regressions — keeping the design matrix identical means
  the regime beta is interpretable as "what would the unconditional
  beta have been if we only had these days?".

## Limitations

- **Three binary regimes** are a crude discretization. A real
  regime-switching model would use Markov chains or HMMs. We use binary
  thresholds because they're interpretable and the data quality at our
  scale doesn't support more sophisticated models.
- **The regime-mask is OFFLINE.** Built from the full historical VIX
  series. A production system would need a current-regime classifier at
  decision time — straightforward (just read today's VIX) but not
  implemented in this research code.
- **Combining regimes is ambiguous.** What if today is high-VIX AND
  rising-rates AND bear-market? The Propagator needs a tie-breaker rule.
  Out of scope here.
- **Regime stationarity assumed.** The 252-day window for the regression
  spans potentially multiple regime episodes. If those episodes
  themselves have shifting beta structures, the regime-mean is still a
  mean.
