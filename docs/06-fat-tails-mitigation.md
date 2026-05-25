# Fat-Tails Mitigation — Block-Bootstrap CI for R²

> **Problem:** Ridge minimizes squared errors — implicitly assumes Gauß
> residuals. Daily-return residuals have kurtosis 3-10 (vs Gauß = 3).
> R² gets pulled toward "normal" days; crisis days are underweighted as
> noise. **Solution (Option D):** stationary block-bootstrap gives a 90%
> CI for R² without distributional assumptions.

## The problem in one example

WMT 2021-02-26 snapshot. Ridge fits the 252-day window ending on that
date, reports R²=0.64.

That 252-day window includes the COVID-crash period (March 2020). On
2020-03-16 the SPY return was -13% — an 8σ event under the Gauß
assumption (probability ~10⁻¹⁶ — effectively impossible). Ridge sees that
day and treats it as noise that should be dampened.

Run the same regression with the COVID-crash days excluded: R²=0.82.
Run it on only the post-COVID-crash subset: R²=0.55.

The "point R²" 0.64 hides the fact that **the R² estimate is extremely
sensitive to which crisis days are in the window**.

## The four mitigation options we considered

1. **Winsorization** — cap returns at ±4σ before regression.
   *Pro:* trivial. *Con:* makes the problem WORSE (further smooths
   extreme days, which we're trying to give appropriate weight to).

2. **Huber-Regression** — L1/L2-hybrid loss, robust to outliers.
   *Pro:* methodologically clean. *Con:* no RidgeCV equivalent in
   sklearn, ~4h implementation, changes coefficient interpretation.

3. **GARCH-vol-scaling** — model conditional volatility, divide returns
   by σ_t, then regress.
   *Pro:* most-rigorous answer. *Con:* commits to a specific
   volatility-model spec, requires recalibration of downstream
   thresholds, ~1-2 weeks of work.

4. **Block-bootstrap CI for R²** — non-parametric, additive, doesn't
   change the point estimate.
   *Pro:* honest, no distributional assumptions, builds on existing
   bootstrap infrastructure. *Con:* gives a range, not a fix; doesn't
   solve coefficient bias.

We picked **Option 4** as the right starting point because it is
diagnostic: it tells us *whether* the fat-tails problem is quantitatively
serious for our specific data. If R²-CIs come out narrow, none of the
heavier mitigations are necessary.

## Stationary Block-Bootstrap (Politis-Romano 1994)

The standard row-bootstrap (sample rows i.i.d.) breaks time-series
autocorrelation. **Stationary block-bootstrap** resamples *contiguous
blocks of random length* — preserving autocorrelation up to block-length.

Algorithm per resample:
1. Start at a random index in the window
2. Each step, EITHER advance to the next index (with probability 1-p)
   OR jump to a new random start (with probability p)
3. Wrap around at the window boundary
4. Stop when you have n indices

Mean block length = 1/p. We use p=0.1 (mean ~10 trading-days =
~2 calendar-weeks of consecutive data per block) — typical macro-news
effect horizon.

Reference: Politis, D. N., & Romano, J. P. (1994). The Stationary
Bootstrap. *Journal of the American Statistical Association*, 89(428),
1303-1313.

## Implementation

See [`honest_factor_research/exposure/bootstrap.py`](../honest_factor_research/exposure/bootstrap.py):

```python
def bootstrap_with_r2_ci(X, y, alpha, n_resamples=200):
    """Returns (stderr_per_factor, r2_p05, r2_p95)."""
    coefs = np.empty((n_resamples, X.shape[1]))
    r2s = np.empty(n_resamples)
    rng = np.random.default_rng(seed)
    for i in range(n_resamples):
        idx = stationary_block_indices(n, p=0.1, rng=rng)
        model = Ridge(alpha=alpha)
        model.fit(X[idx], y[idx])
        coefs[i] = model.coef_
        r2s[i] = model.score(X[idx], y[idx])
    stderr = np.nanstd(coefs, axis=0, ddof=1)
    return stderr, np.nanpercentile(r2s, 5), np.nanpercentile(r2s, 95)
```

200 resamples per snapshot is the default — adds ~3x to the unconditional
fit time but tightens the CI considerably. Bump to 500 if you have time.

## What the empirical results look like

After running on 60 assets × 60 monthly snapshots:

- **Mean R² point estimate:** 0.59
- **Mean CI-width (p95 − p05):** 0.15 (±0.075 around point)
- **Max CI-width:** 0.43 (for WMT 2021-02-26 — that's the COVID-crash-in-window case)
- **Min CI-width:** 0.014 (for assets where the window is in a clean period)

In other words: for most assets in most periods, the point R² is
reasonably reliable. For Crisis-period windows, the CI is several times
wider than you'd intuit from the point value alone.

## How to use this in downstream code

The Asset-Quality-Tier function can use `r²_p05` as a **strict mode**:

```python
def quality_tier_strict(r2_p05):
    """Use the LOWER 90% CI bound — penalize wide-CI assets."""
    if r2_p05 >= 0.5:
        return "HIGH"
    if r2_p05 >= 0.25:
        return "MED"
    return "LOW"
```

This is more conservative than using the point R² — assets get HIGH
only if we're 95%-confident that their true R² is at least 0.5.

## Diagnostic: does our universe need GARCH (Option 3)?

The threshold question: **is the R²-CI typically wide enough that we
can't trust point estimates?**

In our empirical run: median CI-width was 0.13. For most assets and
periods, the point R² is within ±0.07 of what you'd see in any
reasonable resample. That's not large enough to warrant the 1-2 weeks
of GARCH implementation.

If you re-run this analysis on a more turbulent period (e.g. only
2008-2009 or 2020 windows) and CI-widths shoot up to 0.3+, that would
be the trigger to invest in GARCH.

## Limitations

- **In-sample R²** — the CI is for the in-sample fit quality, not for
  out-of-sample generalization. Both are uncertain; we only address one.
- **Block-length parameter (p=0.1)** — set to a reasonable default but
  not estimated from the data. More sophisticated methods would adapt
  block length to estimated autocorrelation structure.
- **Computing cost** — 200 bootstrap fits per snapshot adds compute.
  For very large universes (>10k assets) might be a problem; for the
  ~2,000-stock scale here it's fine.
- **Doesn't fix the coefficient bias** — if fat-tailed days are
  systematically pulling betas in a wrong direction, the bootstrap
  reports stderr correctly but the point coefficient itself is still
  biased. For that you need Huber (Option 2) or GARCH (Option 3).
