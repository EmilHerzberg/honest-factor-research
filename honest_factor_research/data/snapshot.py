"""Long-format parquet I/O for frozen OHLCV datasets.

We use the same format as ``honest_factor_research.data.fetch``:
columns ``[Date, Open, High, Low, Close, Volume, symbol, interval]``,
tz-naive Date column.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator, Sequence
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def _normalize_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce the Date column to tz-naive datetime (in place-ish)."""
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        if hasattr(df["Date"].dt, "tz") and df["Date"].dt.tz is not None:
            df["Date"] = df["Date"].dt.tz_localize(None)
    return df


def _read_long(
    path: Path | str,
    *,
    columns: Sequence[str] | None = None,
    symbols: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Read a long-format snapshot with optional column/symbol push-down.

    ``columns`` projects which parquet columns to read (memory saver — the
    analyses only need ``Close``). ``symbols`` applies a PyArrow predicate
    push-down on the ``symbol`` column so only those rows are materialised.
    Together these let broad-universe (15M-row) snapshots be processed in
    bounded memory regardless of universe size.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Snapshot missing at {path}. "
            "Run `python -m honest_factor_research.data.fetch` first."
        )
    read_kwargs: dict = {}
    if columns is not None:
        # 'interval' is needed for the 1d filter; keep it if it exists on disk.
        import pyarrow.parquet as pq

        on_disk = set(pq.ParquetFile(path).schema_arrow.names)
        want = list(dict.fromkeys(columns))  # de-dup, preserve order
        if "interval" in on_disk and "interval" not in want:
            want.append("interval")
        read_kwargs["columns"] = [c for c in want if c in on_disk]
    if symbols is not None:
        read_kwargs["filters"] = [("symbol", "in", list(symbols))]
    df = pd.read_parquet(path, **read_kwargs)
    if "interval" in df.columns:
        df = df.loc[df["interval"] == "1d"].copy()
    return _normalize_dates(df)


def load_snapshot(path: Path | str) -> pd.DataFrame:
    """Load a long-format OHLCV parquet snapshot (full — all columns/symbols)."""
    return _read_long(path)


def list_symbols(path: Path | str) -> list[str]:
    """Distinct ticker symbols in a long-format snapshot, read cheaply.

    Reads only the ``symbol`` column via PyArrow and computes uniques without
    pivoting or materialising the full multi-million-row frame in pandas.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Snapshot missing at {path}. "
            "Run `python -m honest_factor_research.data.fetch` first."
        )
    import pyarrow.compute as pc
    import pyarrow.parquet as pq

    table = pq.read_table(path, columns=["symbol"])
    return sorted(pc.unique(table.column("symbol")).to_pylist())


def iter_symbol_batches(
    symbols: Sequence[str], batch_size: int
) -> Iterator[list[str]]:
    """Yield ``symbols`` in chunks of at most ``batch_size``."""
    if batch_size <= 0:
        raise ValueError(f"batch_size must be positive, got {batch_size}")
    symbols = list(symbols)
    for i in range(0, len(symbols), batch_size):
        yield symbols[i : i + batch_size]


def load_returns_for_symbols(
    path: Path | str,
    symbols: Sequence[str],
    *,
    dtype: str | None = None,
) -> pd.DataFrame:
    """Wide log-returns for a *subset* of symbols, reading only ``Close``.

    Uses PyArrow column projection (Close only) and ``symbol`` predicate
    push-down, so peak memory scales with the size of ``symbols`` rather than
    the full universe. Numerically identical to slicing the columns out of
    :func:`load_returns` — batching does not change any per-symbol result.

    ``dtype`` optionally down-casts the price matrix (e.g. ``"float32"``) for
    an extra ~2x memory saving; leave ``None`` to keep full float64 precision.
    """
    df = _read_long(path, columns=["Date", "Close", "symbol"], symbols=symbols)
    wide = long_to_wide_close(df)
    if dtype is not None:
        wide = wide.astype(dtype)
    return to_log_returns(wide)


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
