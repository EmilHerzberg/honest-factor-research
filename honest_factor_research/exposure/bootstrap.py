"""Stationary block-bootstrap (Politis-Romano 1994) for time-series regression.

Why block-bootstrap instead of plain row-bootstrap:
  Daily-return regression residuals are autocorrelated (vol-clusters,
  serial dependence). Plain row-bootstrap (sample rows i.i.d.) breaks that
  structure and produces over-confident stderr.

  Stationary block-bootstrap resamples *contiguous blocks* with random
  lengths (geometric-distributed, mean L). Preserves autocorrelation
  structure up to block-length. Politis & Romano (1994):
  https://www.jstor.org/stable/2291363

Two main entry points:
  * :func:`block_bootstrap_resamples` — low-level, returns (coefs, r2s) arrays
  * :func:`bootstrap_with_r2_ci` — high-level, returns (stderr, r2_p05, r2_p95)
"""

from __future__ import annotations

import numpy as np
from sklearn.linear_model import Ridge  # type: ignore[import-untyped]


def stationary_block_indices(
    n: int, p: float, rng: np.random.Generator,
) -> np.ndarray:
    """Generate one stationary-block-bootstrap resample of size n.

    At each position, either start a new block (probability ``p``) at a
    random offset, or extend the current block by one (probability ``1-p``,
    with wraparound). Result is a length-``n`` index array preserving
    autocorrelation through contiguous-block resampling.

    Args:
        n: number of observations in original window
        p: per-position restart probability (= 1 / mean_block_length).
            Typical values: ~0.1 for daily-returns (mean block ~10 days).
        rng: numpy random generator (for determinism in tests)

    Returns:
        np.ndarray of length n with int64 indices into [0, n).
    """
    idx = np.empty(n, dtype=np.int64)
    current = int(rng.integers(0, n))
    restart = rng.random(n) < p
    restart[0] = True
    for t in range(n):
        if restart[t]:
            current = int(rng.integers(0, n))
        idx[t] = current
        current = (current + 1) % n
    return idx


def block_bootstrap_resamples(
    X: np.ndarray,
    y: np.ndarray,
    alpha: float,
    n_resamples: int = 200,
    mean_block_length: float = 10.0,
    random_seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Run stationary block-bootstrap; return per-resample (coefs, R²).

    Args:
        X: design matrix (n_obs × n_factors), already residualized
        y: target vector (n_obs,), asset log-returns
        alpha: Ridge regularization α (held fixed across resamples — we
            don't re-tune via CV per-resample, that would be circular)
        n_resamples: number of bootstrap samples (default 200; bump to 500
            for tighter CI)
        mean_block_length: mean length of contiguous blocks (default 10
            trading-days = ~2 calendar weeks)
        random_seed: for deterministic reproducibility

    Returns:
        coefs: (n_resamples, n_factors) array of refitted Ridge coefficients
        r2s:   (n_resamples,) array of in-sample R² per resample
    """
    n, k = X.shape
    rng = np.random.default_rng(random_seed)
    coefs = np.empty((n_resamples, k), dtype=float)
    r2s = np.empty(n_resamples, dtype=float)
    p = 1.0 / mean_block_length
    for i in range(n_resamples):
        idx = stationary_block_indices(n, p, rng)
        try:
            model = Ridge(alpha=alpha)
            model.fit(X[idx], y[idx])
            coefs[i] = model.coef_
            r2s[i] = model.score(X[idx], y[idx])
        except Exception:  # noqa: BLE001
            coefs[i] = np.nan
            r2s[i] = np.nan
    return coefs, r2s


def bootstrap_with_r2_ci(
    X: np.ndarray,
    y: np.ndarray,
    alpha: float,
    n_resamples: int = 200,
    mean_block_length: float = 10.0,
    random_seed: int = 42,
) -> tuple[np.ndarray, float, float]:
    """Combined block-bootstrap: per-factor stderr + R²-CI from same resamples.

    Returns:
        stderr_per_factor: (n_factors,) std-dev of bootstrap coefs
        r2_p05: 5th percentile of R² across resamples
        r2_p95: 95th percentile of R² across resamples

    The R²-CI is the non-parametric answer to fat-tailed daily-return
    distributions making point R² too smooth. Wide gap = high uncertainty.
    """
    coefs, r2s = block_bootstrap_resamples(
        X, y, alpha,
        n_resamples=n_resamples,
        mean_block_length=mean_block_length,
        random_seed=random_seed,
    )
    with np.errstate(invalid="ignore"):
        stderr = np.nanstd(coefs, axis=0, ddof=1)
        r2_p05 = float(np.nanpercentile(r2s, 5))
        r2_p95 = float(np.nanpercentile(r2s, 95))
    # Guard against zero stderr (perfect bootstrap-collinearity)
    stderr = np.where(stderr <= 0, np.finfo(float).eps, stderr)
    return stderr, r2_p05, r2_p95
