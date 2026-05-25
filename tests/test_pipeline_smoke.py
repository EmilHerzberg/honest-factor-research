"""Smoke test for the FactorExposurePipeline — requires bundled sample data."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from honest_factor_research.analysis._common import DEFAULT_DATA_DIR
from honest_factor_research.data.snapshot import load_returns
from honest_factor_research.exposure import FactorExposurePipeline


SAMPLE_SNAPSHOT = DEFAULT_DATA_DIR / "factor_etfs_2026-05-21.parquet"


@pytest.mark.skipif(not SAMPLE_SNAPSHOT.exists(),
                    reason="Sample snapshot missing — run data.fetch first")
def test_pipeline_basic_fit():
    """Construct + fit one snapshot end-to-end."""
    asset_returns = load_returns(SAMPLE_SNAPSHOT)
    assert len(asset_returns) > 200
    pipeline = FactorExposurePipeline.from_snapshot(
        factor_etfs_snapshot=SAMPLE_SNAPSHOT,
        asset_returns=asset_returns,
        bootstrap_samples=20,  # tiny for speed
    )
    # Pick any symbol present in the snapshot
    symbol = asset_returns.columns[0]
    rows = pipeline.fit_one(symbol, date(2024, 6, 28))
    assert len(rows) > 0
    r = rows[0]
    assert isinstance(r.exposure_value, float)
    assert r.symbol == symbol
    assert r.r_squared is None or 0 <= r.r_squared <= 1


@pytest.mark.skipif(not SAMPLE_SNAPSHOT.exists(),
                    reason="Sample snapshot missing — run data.fetch first")
def test_pipeline_emits_r2_ci():
    """R²-CI columns should be populated alongside the point R²."""
    asset_returns = load_returns(SAMPLE_SNAPSHOT)
    pipeline = FactorExposurePipeline.from_snapshot(
        factor_etfs_snapshot=SAMPLE_SNAPSHOT,
        asset_returns=asset_returns,
        bootstrap_samples=30,
    )
    symbol = asset_returns.columns[0]
    rows = pipeline.fit_one(symbol, date(2024, 6, 28))
    if not rows:
        pytest.skip(f"No data for {symbol}")
    r = rows[0]
    # If R² passed the threshold, CI should be present
    if r.r_squared is not None and r.r_squared >= 0.2:
        assert r.r_squared_p05 is not None
        assert r.r_squared_p95 is not None
        assert r.r_squared_p05 <= r.r_squared_p95
