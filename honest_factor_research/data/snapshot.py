"""Long-format parquet I/O for frozen OHLCV datasets.

We use the same format as ``honest_factor_research.data.fetch``:
columns ``[Date, Open, High, Low, Close, Volume, symbol, interval]``,
tz-naive Date column.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def load_snapshot(path: Path | str) -> pd.DataFrame:
    """Load a long-format OHLCV parquet snapshot."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Snapshot missing at {path}. "
            "Run `python -m honest_factor_research.data.fetch` first."
        )
    df = pd.read_parquet(path)
    if "interval" in df.columns:
        df = df.loc[df["interval"] == "1d"].copy()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        if hasattr(df["Date"].dt, "tz") and df["Date"].dt.tz is not None:
            df["Date"] = df["Date"].dt.tz_localize(None)
    return df


def long_to_wide_close(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot a long-format snapshot to wide Close prices indexed by Date."""
    wide = (
        df.pivot_table(index="Date", columns="symbol", values="Close", aggfunc="last")
        .sort_index()
    )
    if hasattr(wide.index, "tz") and wide.index.tz is not None:
        wide.index = wide.index.tz_localize(None)
    return wide


def to_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Daily log returns. Drops the leading NaN row."""
    return np.log(prices / prices.shift(1)).iloc[1:]


def load_returns(path: Path | str) -> pd.DataFrame:
    """One-shot convenience: snapshot → wide log-returns DataFrame."""
    return to_log_returns(long_to_wide_close(load_snapshot(path)))


def load_vix_levels(path: Path | str, vix_symbol: str = "^VIX") -> pd.Series | None:
    """Load raw ^VIX-Spot closing levels (NOT log-returns).

    Used by the regime-switching pipeline to classify each day in the
    rolling window as low-vol (VIX<15) or high-vol (VIX>25).

    Returns ``None`` if ^VIX is missing from the snapshot.
    """
    df = load_snapshot(path)
    vix_rows = df.loc[df["symbol"] == vix_symbol]
    if vix_rows.empty:
        return None
    vix = vix_rows.set_index("Date")["Close"].sort_index()
    if hasattr(vix.index, "tz") and vix.index.tz is not None:
        vix.index = vix.index.tz_localize(None)
    return vix
