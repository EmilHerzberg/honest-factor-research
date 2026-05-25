"""Tests for the stationary block-bootstrap."""

from __future__ import annotations

import numpy as np

from honest_factor_research.exposure.bootstrap import (
    block_bootstrap_resamples,
    bootstrap_with_r2_ci,
    stationary_block_indices,
)


def test_stationary_block_indices_size():
    rng = np.random.default_rng(42)
    n = 200
    idx = stationary_block_indices(n, p=0.1, rng=rng)
    assert idx.shape == (n,)
    assert idx.dtype == np.int64
    assert idx.min() >= 0
    assert idx.max() < n


def test_stationary_block_indices_preserves_autocorrelation():
    """With mean block length ~10, consecutive indices should mostly be +1."""
    rng = np.random.default_rng(42)
    n = 10000
    idx = stationary_block_indices(n, p=0.1, rng=rng)  # mean block = 10
    diffs = np.diff(idx)
    # Most positions should extend the current block (diff = +1 mod n)
    is_continuation = (diffs == 1) | (diffs == -(n - 1))
    fraction_continuation = is_continuation.mean()
    # With p=0.1, ~90% should be continuations
    assert fraction_continuation > 0.85, (
        f"Expected ~90% block-continuations, got {fraction_continuation:.2%}"
    )


def test_bootstrap_with_r2_ci_basic():
    """Bootstrap on a perfectly fitted regression should give tight CI."""
    rng = np.random.default_rng(42)
    n, k = 252, 5
    # Perfect linear relationship: y = X @ true_beta + tiny_noise
    X = rng.normal(size=(n, k))
    true_beta = np.array([0.5, -0.3, 0.2, 0.1, -0.4])
    y = X @ true_beta + rng.normal(scale=0.01, size=n)
    stderr, r2_p05, r2_p95 = bootstrap_with_r2_ci(
        X, y, alpha=0.01, n_resamples=100, random_seed=42,
    )
    assert stderr.shape == (k,)
    # All stderrs should be small for this clean signal
    assert (stderr < 0.05).all()
    # R² should be near 1.0 with very tight CI
    assert r2_p05 > 0.99
    assert r2_p95 > 0.99


def test_bootstrap_with_r2_ci_noisy_gives_wide_ci():
    """Bootstrap on a noisy regression should give wider CI than clean one."""
    rng = np.random.default_rng(42)
    n, k = 252, 3
    X = rng.normal(size=(n, k))
    true_beta = np.array([0.5, -0.3, 0.2])
    # Noisy: signal-to-noise ratio ~1
    y = X @ true_beta + rng.normal(scale=1.0, size=n)
    _, r2_p05, r2_p95 = bootstrap_with_r2_ci(
        X, y, alpha=0.01, n_resamples=100, random_seed=42,
    )
    # CI should be wider than 0.05
    assert r2_p95 - r2_p05 > 0.05, f"CI too tight: [{r2_p05:.3f}, {r2_p95:.3f}]"


def test_bootstrap_deterministic_with_seed():
    """Same seed → same stderr and CI."""
    rng = np.random.default_rng(42)
    n, k = 100, 3
    X = rng.normal(size=(n, k))
    y = rng.normal(size=n)
    r1 = bootstrap_with_r2_ci(X, y, alpha=0.05, n_resamples=50, random_seed=123)
    r2 = bootstrap_with_r2_ci(X, y, alpha=0.05, n_resamples=50, random_seed=123)
    assert np.allclose(r1[0], r2[0])
    assert r1[1] == r2[1]
    assert r1[2] == r2[2]
