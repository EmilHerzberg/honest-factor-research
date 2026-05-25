"""Shared helpers for analysis scripts (output dir, logger, snapshot paths)."""

from __future__ import annotations

import datetime as dt
import logging
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend for CLI use


# Project-relative defaults — adjust if you move the package
PACKAGE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = PACKAGE_ROOT / "data"
DEFAULT_REPORTS_DIR = PACKAGE_ROOT / "reports"


def resolve_factor_snapshot(date_suffix: str = "2026-05-21") -> Path:
    """Locate the default factor-ETFs snapshot parquet."""
    candidate = DEFAULT_DATA_DIR / f"factor_etfs_{date_suffix}.parquet"
    if candidate.exists():
        return candidate
    # Fallback: look in any *.parquet matching the pattern
    matches = sorted(DEFAULT_DATA_DIR.glob("factor_etfs_*.parquet"))
    if matches:
        return matches[-1]
    raise FileNotFoundError(
        f"No factor_etfs_*.parquet in {DEFAULT_DATA_DIR}. "
        f"Run: python -m honest_factor_research.data.fetch --factors-only"
    )


def resolve_broad_universe(date_suffix: str | None = None) -> tuple[Path, Path]:
    """Locate the broad-universe constituents CSV + OHLCV parquet.

    OHLCV parquet is gitignored due to size — must be re-fetched via
    ``python -m honest_factor_research.data.fetch``.
    """
    consts_pattern = "broad_universe_constituents_*.csv"
    ohlcv_pattern = "broad_universe_ohlcv_*.parquet"
    consts_matches = sorted(DEFAULT_DATA_DIR.glob(consts_pattern))
    ohlcv_matches = sorted(DEFAULT_DATA_DIR.glob(ohlcv_pattern))
    if not consts_matches:
        raise FileNotFoundError(
            f"No {consts_pattern} in {DEFAULT_DATA_DIR}. "
            f"Run: python -m honest_factor_research.data.fetch"
        )
    if not ohlcv_matches:
        raise FileNotFoundError(
            f"No {ohlcv_pattern} in {DEFAULT_DATA_DIR}. "
            f"Run: python -m honest_factor_research.data.fetch  (takes ~3 min for 3000 stocks)"
        )
    return consts_matches[-1], ohlcv_matches[-1]


def report_output_dir(suffix: str | None = None) -> Path:
    """Today's report directory under ``reports/`` (creates if missing).

    Pass an optional ``suffix`` to namespace different analyses on the
    same day, e.g. ``report_output_dir("v3.5-verification")``.
    """
    today = dt.date.today().isoformat()
    name = f"{today}-{suffix}" if suffix else today
    out = DEFAULT_REPORTS_DIR / name
    out.mkdir(parents=True, exist_ok=True)
    return out


def setup_logging(name: str, level: int = logging.INFO) -> logging.Logger:
    """Bootstrap a sensibly-formatted logger for analysis scripts."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    return logging.getLogger(name)
