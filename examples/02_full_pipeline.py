"""Run the full :class:`FactorExposurePipeline` end-to-end for a handful of
assets with all V3.5 features (sector-conditional, regime-switching,
block-bootstrap CI).

Prerequisites:
    pip install -e ".[notebooks]"
    python -m honest_factor_research.data.fetch --factors-only

Run:
    python examples/02_full_pipeline.py
"""

from __future__ import annotations

import logging
from datetime import date

import pandas as pd

from honest_factor_research.analysis._common import resolve_factor_snapshot
from honest_factor_research.data.snapshot import load_returns
from honest_factor_research.exposure import FactorExposurePipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

snap_path = resolve_factor_snapshot()
asset_returns = load_returns(snap_path)

# Sample sector map for Mitigation 2G — only relevant for these tickers
sector_lookup = {
    "AAPL": "Technology",
    "MSFT": "Technology",
    "JPM": "Financial Services",
    "XOM": "Energy",
    "DUK": "Utilities",
}

symbols = [s for s in sector_lookup if s in asset_returns.columns]
print(f"Computing exposures for: {symbols}")

pipeline = FactorExposurePipeline.from_snapshot(
    factor_etfs_snapshot=snap_path,
    asset_returns=asset_returns,
    sector_lookup=sector_lookup,
)

# Single snapshot — full V3.5 output for one date
window_end = date(2024, 6, 28)
for sym in symbols:
    rows = pipeline.fit_one(sym, window_end)
    if not rows:
        print(f"{sym}: no data on {window_end}")
        continue
    print(f"\n=== {sym} — {window_end} ({len(rows)} factors applicable) ===")
    print(f"{'factor_id':<25s} {'beta':>10s} {'r²':>7s} {'r² CI':>20s} "
          f"{'β low-vix':>10s} {'β high-vix':>10s}")
    for r in rows[:8]:
        ci = (f"[{r.r_squared_p05:.3f},{r.r_squared_p95:.3f}]"
              if r.r_squared_p05 is not None else "—")
        low = f"{r.exposure_value_low_vix:+.3f}" if r.exposure_value_low_vix is not None else "—"
        high = f"{r.exposure_value_high_vix:+.3f}" if r.exposure_value_high_vix is not None else "—"
        print(f"{r.factor_id:<25s} {r.exposure_value:>+10.4f} "
              f"{r.r_squared:>7.3f} {ci:>20s} {low:>10s} {high:>10s}")
    if len(rows) > 8:
        print(f"  ... and {len(rows) - 8} more factors (run with full output for all)")

# Monthly snapshots (multi-month) — produces a DataFrame ready for analysis
print("\n=== Monthly snapshots (2024) ===")
df = pipeline.fit_monthly_snapshots(symbols, start_date=date(2024, 1, 1), end_date=date(2024, 12, 31))
print(f"Generated {len(df)} (symbol, factor, window_end) rows")
print(df[["symbol", "factor_id", "window_end", "exposure_value", "r_squared",
          "r_squared_p05", "r_squared_p95"]].head(10))
