"""Tests for the Gram-Schmidt residualization step."""

from __future__ import annotations

import numpy as np
import pandas as pd

from honest_factor_research.returns.residualization import residualize_one


def test_residualize_against_self_gives_zero():
    """Residualizing y against itself should give zero (within float-eps)."""
    rng = np.random.default_rng(42)
    n = 500
    idx = pd.date_range("2020-01-01", periods=n, freq="B")
    y = pd.Series(rng.normal(size=n), index=idx, name="y")
    X = pd.DataFrame({"x": y.values}, index=idx)
    resid = residualize_one(y, X)
    assert np.allclose(resid.dropna().values, 0, atol=1e-10)


def test_residualize_against_orthogonal_preserves_y():
    """Residualizing y against a series independent of y → resid ≈ y - mean(y)."""
    rng = np.random.default_rng(42)
    n = 1000
    idx = pd.date_range("2020-01-01", periods=n, freq="B")
    y = pd.Series(rng.normal(loc=0, scale=1, size=n), index=idx, name="y")
    x_indep = pd.Series(rng.normal(loc=0, scale=1, size=n), index=idx, name="x")
    X = pd.DataFrame({"x": x_indep})
    resid = residualize_one(y, X)
    # Residual should be highly correlated with the demeaned original y
    corr = np.corrcoef(resid.values, (y - y.mean()).values)[0, 1]
    assert corr > 0.95


def test_residualize_empty_X_returns_copy():
    rng = np.random.default_rng(42)
    n = 100
    y = pd.Series(rng.normal(size=n), name="y")
    X = pd.DataFrame(index=y.index)
    resid = residualize_one(y, X)
    assert (resid == y).all()


def test_residualize_handles_nans():
    """NaN rows should propagate to the output."""
    rng = np.random.default_rng(42)
    n = 100
    idx = pd.date_range("2020-01-01", periods=n, freq="B")
    y = pd.Series(rng.normal(size=n), index=idx, name="y")
    y.iloc[10:15] = np.nan
    X = pd.DataFrame({"x": rng.normal(size=n)}, index=idx)
    resid = residualize_one(y, X)
    assert resid.iloc[10:15].isna().all()
    assert resid.iloc[:10].notna().all()
