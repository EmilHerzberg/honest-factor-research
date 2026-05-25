"""yfinance + NASDAQ-screener data fetching.

Two main entry points:

* :func:`fetch_ohlcv` — bulk-download OHLCV for a list of tickers via yfinance
* :func:`fetch_broad_universe_constituents` — Top-N US stocks by market cap
  from the public NASDAQ-screener JSON API

Both return long-format ``pd.DataFrame`` with columns
``[Date, Open, High, Low, Close, Volume, symbol, interval]`` (OHLCV) or
``[symbol, name, sector, industry, market_cap_usd]`` (constituents).
"""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Iterable

import pandas as pd
import requests

logger = logging.getLogger(__name__)


# ─── OHLCV via yfinance ─────────────────────────────────────────────


def fetch_one_ticker(
    symbol: str, start: datetime, end: datetime,
) -> pd.DataFrame:
    """Fetch daily OHLCV for one ticker via yfinance.

    Returns a long-format DataFrame with columns
    ``[Date, Open, High, Low, Close, Volume, symbol, interval]``.
    Empty DataFrame if yfinance returns no data (delisted, bad ticker, etc.).
    """
    import yfinance as yf  # type: ignore[import-untyped]

    logger.info("Fetching %s [%s .. %s]", symbol, start.date(), end.date())
    ticker = yf.Ticker(symbol)
    df = ticker.history(
        interval="1d",
        start=start.strftime("%Y-%m-%d"),
        end=end.strftime("%Y-%m-%d"),
    )
    if df is None or df.empty:
        logger.warning("No data returned for %s — skipping", symbol)
        return pd.DataFrame()

    # Drop tz so parquet stays portable
    if hasattr(df.index, "tz") and df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    df.index.name = "Date"
    df = df.reset_index()
    keep = ["Date", "Open", "High", "Low", "Close", "Volume"]
    df = df[[c for c in keep if c in df.columns]].copy()
    df["symbol"] = symbol
    df["interval"] = "1d"
    return df


def fetch_ohlcv(
    symbols: Iterable[str],
    start: datetime,
    end: datetime,
    batch_size: int = 100,
    rate_limit_sleep: float = 0.5,
) -> pd.DataFrame:
    """Bulk-fetch OHLCV for multiple tickers in batches.

    Uses ``yf.download`` in batches of ``batch_size`` (default 100) with a
    short pause between batches to be polite to yfinance rate limits.

    Symbols that yfinance can't fetch are silently skipped (delisted,
    rate-limited, etc.) — see logs for which ones failed.
    """
    import yfinance as yf  # type: ignore[import-untyped]

    symbols = list(symbols)
    n_batches = (len(symbols) + batch_size - 1) // batch_size
    all_frames = []
    failed: list[str] = []
    t0 = time.time()

    for i in range(0, len(symbols), batch_size):
        batch_idx = i // batch_size + 1
        batch = symbols[i : i + batch_size]
        elapsed = time.time() - t0
        rate = i / max(elapsed, 1)
        eta = (len(symbols) - i) / max(rate, 0.1)
        logger.info(
            "Batch %d/%d (%d symbols)... elapsed=%.0fs eta=%.0fs",
            batch_idx, n_batches, len(batch), elapsed, eta,
        )
        try:
            df = yf.download(
                tickers=batch,
                start=start.strftime("%Y-%m-%d"),
                end=end.strftime("%Y-%m-%d"),
                interval="1d",
                group_by="ticker",
                auto_adjust=False,
                progress=False,
                threads=True,
            )
            if df.empty:
                failed.extend(batch)
                continue

            # Unpack MultiIndex (Ticker, OHLCV) into long format
            if isinstance(df.columns, pd.MultiIndex):
                symbols_in_df = df.columns.get_level_values(0).unique()
                for sym in symbols_in_df:
                    sub = df[sym].copy()
                    if sub.dropna(how="all").empty:
                        continue
                    sub = sub.reset_index()
                    sub["symbol"] = sym
                    sub["interval"] = "1d"
                    all_frames.append(sub)
                got_symbols = set(df.columns.get_level_values(0).unique())
                missing = set(batch) - got_symbols
                failed.extend(missing)
            else:
                if batch:
                    sub = df.reset_index()
                    sub["symbol"] = batch[0]
                    sub["interval"] = "1d"
                    all_frames.append(sub)
        except Exception as exc:  # noqa: BLE001
            logger.error("Batch %d failed: %s", batch_idx, exc)
            failed.extend(batch)
        time.sleep(rate_limit_sleep)

    if not all_frames:
        return pd.DataFrame()

    combined = pd.concat(all_frames, ignore_index=True)
    keep = ["Date", "Open", "High", "Low", "Close", "Volume", "symbol", "interval"]
    combined = combined[[c for c in keep if c in combined.columns]].copy()
    if "Date" in combined.columns:
        combined["Date"] = pd.to_datetime(combined["Date"]).dt.tz_localize(None)
    combined = combined.sort_values(["symbol", "Date"]).reset_index(drop=True)

    n_symbols = combined["symbol"].nunique()
    logger.info(
        "Bulk fetch done: %d rows × %d symbols (failed: %d)",
        len(combined), n_symbols, len(failed),
    )
    if failed:
        logger.warning("First 30 failed: %s", sorted(failed)[:30])
    return combined


# ─── Broad-universe constituents via NASDAQ-screener ────────────────


def fetch_broad_universe_constituents(top_n: int = 3000) -> pd.DataFrame:
    """Fetch Top-N US stocks by market cap from NASDAQ-screener public API.

    Returns a DataFrame with columns
    ``[symbol, name, sector, industry, market_cap_usd]``. Filters to
    ``country=="United States"`` and ``market_cap > 0``, then takes Top-N.

    Used in this repo as a Russell-3000 approximation. Trade-off: it's
    today's snapshot — delisted stocks (Lehman, SVB, etc.) are missing.
    See ``docs/future-investigations.md`` for the survivorship-bias caveat.
    """
    ua = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0) Chrome/120.0",
        "Accept": "application/json",
    }
    url = (
        "https://api.nasdaq.com/api/screener/stocks"
        "?tableonly=true&limit=10000&offset=0&download=true"
    )
    logger.info("Fetching constituent universe from NASDAQ-screener...")
    r = requests.get(url, headers=ua, timeout=60)
    r.raise_for_status()
    j = r.json()
    df = pd.DataFrame(j["data"]["rows"])
    logger.info("Total US-listed stocks: %d", len(df))

    us = df[df["country"] == "United States"].copy()

    def to_float(x):
        if pd.isna(x) or x == "" or x is None:
            return 0.0
        try:
            return float(str(x).replace(",", "").replace("$", ""))
        except Exception:
            return 0.0

    us["marketCap_num"] = us["marketCap"].apply(to_float)
    us = us[us["marketCap_num"] > 0]
    logger.info("US-domiciled with market cap: %d", len(us))

    top = us.nlargest(top_n, "marketCap_num").copy()
    top = top[["symbol", "name", "sector", "industry", "marketCap_num"]].rename(
        columns={"marketCap_num": "market_cap_usd"},
    )
    logger.info(
        "Selected Top %d, MC range: $%.0fM - $%.0fM",
        len(top),
        top["market_cap_usd"].min() / 1e6,
        top["market_cap_usd"].max() / 1e6,
    )
    return top


def normalize_for_yfinance(symbol: str) -> str:
    """BRK.B → BRK-B, BF.B → BF-B etc. for yfinance compatibility."""
    return symbol.replace(".", "-")


# ─── CLI entry-point ────────────────────────────────────────────────


def main() -> int:
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="Fetch OHLCV + constituents for honest-factor-research."
    )
    parser.add_argument(
        "--factors-only", action="store_true",
        help="Fetch only the ~30 factor ETFs (small, ~2 min). Otherwise full broad universe.",
    )
    parser.add_argument(
        "--start", default="2019-06-01", help="OHLCV start date YYYY-MM-DD",
    )
    parser.add_argument(
        "--end", default="2024-12-31", help="OHLCV end date YYYY-MM-DD",
    )
    parser.add_argument(
        "--output-dir", default="data", help="Output directory for parquet files",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    start = datetime.strptime(args.start, "%Y-%m-%d")
    end = datetime.strptime(args.end, "%Y-%m-%d")

    if args.factors_only:
        # All factor-ETF proxies used in the V3.5 catalog (see config/factors.yaml)
        factor_etfs = [
            "SPY", "IEF", "TIP", "UUP", "^VIX", "BZ=F", "TLT", "HYG",
            "IWD", "IWF", "MTUM", "QUAL",
            "SOXX", "XLF", "XLV", "XLI", "XLP", "XLU", "XLRE", "FXI",
            "GLD", "CPER", "UNG", "IBB", "ITA", "ASHR",
            "LIT", "URA",
        ]
        df = fetch_ohlcv(factor_etfs, start, end, batch_size=30)
        out = out_dir / f"factor_etfs_{end.strftime('%Y-%m-%d')}.parquet"
        df.to_parquet(out, index=False, compression="snappy")
        print(f"OK: {out} ({len(df)} rows × {df['symbol'].nunique()} symbols)")
        return 0

    # Full broad universe
    consts = fetch_broad_universe_constituents(top_n=3000)
    consts_path = out_dir / f"broad_universe_constituents_{end.strftime('%Y-%m-%d')}.csv"
    consts.to_csv(consts_path, index=False)
    print(f"OK constituents: {consts_path}")

    symbols_yf = sorted({normalize_for_yfinance(s) for s in consts["symbol"].tolist()})
    df = fetch_ohlcv(symbols_yf, start, end, batch_size=100)
    out = out_dir / f"broad_universe_ohlcv_{end.strftime('%Y-%m-%d')}.parquet"
    df.to_parquet(out, index=False, compression="snappy")
    print(f"OK OHLCV: {out} ({len(df)} rows × {df['symbol'].nunique()} symbols)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
