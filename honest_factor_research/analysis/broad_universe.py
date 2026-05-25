"""Analysis 8 — Broad-Universe Replay (multiprocessing).

Scale-up of the replacement-test (Analysis 7) from a 60-asset MVP universe
to the full broad-universe (Russell-3000 approximation, ~2,241 US stocks
with sufficient history). Uses ``ProcessPoolExecutor`` with 8 workers —
~18 minutes total wall-clock on a typical laptop.

Real-world finding from this methodology: global r²_direct collapsed from
0.386 (60-asset sample, large-cap-biased) to **0.250** (broad universe).
This is the moment we realized our small-sample R² statistics were
systematically over-optimistic — 75% of mid/small-cap variance is
idiosyncratic, not factor-explained.

Per-sector slice reports identify which factors are essential for which
GICS sectors → directly informs the Mitigation-2G sector-conditional
factor architecture.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from collections.abc import Iterable
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV  # type: ignore[import-untyped]

from honest_factor_research.analysis._common import (
    DEFAULT_DATA_DIR,
    report_output_dir,
    resolve_broad_universe,
    resolve_factor_snapshot,
    setup_logging,
)
from honest_factor_research.analysis.replacement_test import (
    TIER_INDIVIDUAL,
    V1_CURRENT,
    V2_VOL_FIX,
    V3_OIL_FIX,
    fetch_replacement_proxies,
)
from honest_factor_research.data.snapshot import long_to_wide_close, load_snapshot, to_log_returns

logger = setup_logging("analysis.08_broad_universe")

WINDOW_DAYS = 252
MIN_HISTORY_DAYS = 252 + 49 * 21  # ~3.5 years
RIDGE_ALPHAS = (0.01, 0.05, 0.1)


def fit_r2(X: np.ndarray, y: np.ndarray) -> float:
    if X.shape[1] == 0 or X.shape[0] < X.shape[1] + 5:
        return float("nan")
    try:
        m = RidgeCV(alphas=list(RIDGE_ALPHAS))
        m.fit(X, y)
        return float(m.score(X, y))
    except Exception:
        return float("nan")


# Worker-init globals — set by Pool initializer
_G_FACTOR_RETURNS: pd.DataFrame | None = None
_G_SNAPSHOTS: list = []
_G_VARIANTS: dict[str, list[str]] = {}


def _init_worker(factor_returns, snapshots, variants):
    global _G_FACTOR_RETURNS, _G_SNAPSHOTS, _G_VARIANTS
    _G_FACTOR_RETURNS = factor_returns
    _G_SNAPSHOTS = snapshots
    _G_VARIANTS = variants


def fit_one_asset(args) -> tuple[str, dict[str, float]]:
    """Compute mean r² per variant for one asset across all snapshots."""
    sym, asset_series = args
    out: dict[str, float] = {}
    for vname, cols in _G_VARIANTS.items():
        available = [c for c in cols if c in _G_FACTOR_RETURNS.columns]
        vdf = _G_FACTOR_RETURNS[available]
        r2s = []
        for ts in _G_SNAPSHOTS:
            ar_win = asset_series.loc[asset_series.index <= ts].tail(WINDOW_DAYS)
            fr_win = vdf.loc[vdf.index <= ts].tail(WINDOW_DAYS)
            joined = pd.concat([ar_win, fr_win], axis=1, sort=False).dropna()
            if len(joined) < WINDOW_DAYS:
                continue
            y = joined.iloc[:, 0].to_numpy()
            X = joined.iloc[:, 1:].to_numpy()
            r2 = fit_r2(X, y)
            if np.isfinite(r2):
                r2s.append(r2)
        out[vname] = float(np.nanmean(r2s)) if r2s else float("nan")
    return sym, out


def make_variants():
    """V1-V3 + 12 Tier individual + 3 cumulative sets."""
    variants = {"V1_current": V1_CURRENT, "V2_vol_fix": V2_VOL_FIX, "V3_oil_fix": V3_OIL_FIX}
    for name, (col, _) in TIER_INDIVIDUAL.items():
        variants[name] = V3_OIL_FIX + [col]
    return variants


def build_factor_returns_combined(snap_path: Path, new_df: pd.DataFrame) -> pd.DataFrame:
    base = long_to_wide_close(load_snapshot(snap_path))
    new_wide = long_to_wide_close(new_df)
    new_uniq = new_wide[[c for c in new_wide.columns if c not in base.columns]]
    combined = base.join(new_uniq, how="outer").sort_index()
    log_ret = to_log_returns(combined)
    if {"TIP", "IEF"}.issubset(log_ret.columns):
        log_ret["TIP_minus_IEF"] = log_ret["TIP"] - log_ret["IEF"]
    if {"HYG", "IEF"}.issubset(log_ret.columns):
        log_ret["HYG_minus_IEF"] = log_ret["HYG"] - log_ret["IEF"]
    return log_ret


def filter_eligible(log_ret_assets: pd.DataFrame, min_days: int) -> list[str]:
    counts = log_ret_assets.count()
    return sorted(counts[counts >= min_days].index.tolist())


def write_report(df_per_asset: pd.DataFrame, constituents: pd.DataFrame, out_dir: Path) -> None:
    df = df_per_asset.merge(
        constituents[["symbol", "sector", "industry", "market_cap_usd"]],
        on="symbol", how="left",
    )
    for vname, (col, _) in TIER_INDIVIDUAL.items():
        if vname in df.columns:
            df[f"delta_{vname}"] = df[vname] - df["V3_oil_fix"]
    df["delta_V3_minus_V1"] = df["V3_oil_fix"] - df["V1_current"]

    csv_path = out_dir / "08_broad_universe.csv"
    df.to_csv(csv_path, float_format="%.4f", index=False)

    md_path = out_dir / "08_broad_universe.md"
    lines = []
    lines.append("# Analysis 8 — Broad-Universe Replay\n")
    lines.append(f"**Date:** {pd.Timestamp.now().date().isoformat()}  ")
    lines.append(f"**Assets analyzed:** {len(df)}\n")

    lines.append("## Marginal-effect per tier candidate (sorted by Mean Δr²)\n")
    lines.append("| Candidate | Mean Δr² | n assets w/ Δ≥0.05 | Max Δ (asset) |")
    lines.append("|---|---|---|---|")
    rows = []
    for vname in TIER_INDIVIDUAL:
        dcol = f"delta_{vname}"
        if dcol not in df.columns:
            continue
        d = df[dcol].dropna()
        if d.empty:
            continue
        rows.append((vname, d.mean(), int((d >= 0.05).sum()), d.max(), df.loc[d.idxmax(), "symbol"]))
    rows.sort(key=lambda r: -r[1])
    for vname, m, n_sig, max_d, argmax in rows:
        marker = "🟢" if m >= 0.02 else "🟡" if m >= 0.005 else "⚪"
        lines.append(f"| {marker} `{vname}` | {m:+.4f} | {n_sig} | {max_d:+.3f} ({argmax}) |")
    lines.append("")

    lines.append("## Per-sector factor relevance (mean Δr² per GICS sector)\n")
    delta_cols = [f"delta_{n}" for n in TIER_INDIVIDUAL if f"delta_{n}" in df.columns]
    sector_agg = df.groupby("sector")[delta_cols].mean()
    lines.append("| Sector | " + " | ".join(c.replace("delta_", "") for c in delta_cols) + " |")
    lines.append("|" + "---|" * (len(delta_cols) + 1))
    for sec, row in sector_agg.iterrows():
        if pd.isna(sec) or len(df[df["sector"] == sec]) < 5:
            continue
        cells = [sec]
        for c in delta_cols:
            v = row[c]
            cells.append(f"**{v:+.3f}**" if v >= 0.02 else f"{v:+.3f}")
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")

    lines.append(f"Full per-asset table: `{csv_path.name}`\n")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote: %s", md_path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--snapshot", default=None,
                        help="Factor-ETFs snapshot (defaults to bundled)")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--sample", type=int, default=None,
                        help="Test mode: only process N assets")
    parser.add_argument("--start", default="2019-06-01")
    parser.add_argument("--end", default="2024-12-31")
    parser.add_argument("--start-snapshot", default="2020-12-31",
                        help="First monthly snapshot date (default 2020-12-31)")
    parser.add_argument("--output-suffix", default="broad-universe")
    args = parser.parse_args(argv)

    factor_snap = Path(args.snapshot) if args.snapshot else resolve_factor_snapshot()
    consts_path, ohlcv_path = resolve_broad_universe()
    out_dir = report_output_dir(args.output_suffix)
    logger.info("Factor snapshot: %s", factor_snap)
    logger.info("Broad universe constituents: %s", consts_path)
    logger.info("Broad universe OHLCV: %s", ohlcv_path)

    from datetime import datetime
    cache_path = DEFAULT_DATA_DIR / "cache" / "replacement_proxies.parquet"
    new_df = fetch_replacement_proxies(
        cache_path,
        datetime.strptime(args.start, "%Y-%m-%d"),
        datetime.strptime(args.end, "%Y-%m-%d"),
    )
    factor_returns = build_factor_returns_combined(factor_snap, new_df)
    asset_log_ret = to_log_returns(long_to_wide_close(load_snapshot(ohlcv_path)))
    constituents = pd.read_csv(consts_path)

    eligible = filter_eligible(asset_log_ret, MIN_HISTORY_DAYS)
    if args.sample:
        eligible = eligible[: args.sample]
    logger.info("Eligible assets: %d", len(eligible))

    month_ends = pd.date_range(start=args.start_snapshot, end=args.end, freq="ME")
    factor_dates = pd.DatetimeIndex(factor_returns.index).normalize()
    snapshot_dates = []
    for me in month_ends:
        cand = factor_dates[factor_dates <= pd.Timestamp(me)]
        if len(cand) > 0:
            d = cand[-1]
            if not snapshot_dates or snapshot_dates[-1] != d:
                snapshot_dates.append(d)
    logger.info("Snapshots: %d", len(snapshot_dates))

    variants = make_variants()
    work_items = [(sym, asset_log_ret[sym]) for sym in eligible]

    results = []
    t0 = time.time()
    with ProcessPoolExecutor(
        max_workers=args.workers,
        initializer=_init_worker,
        initargs=(factor_returns, snapshot_dates, variants),
    ) as ex:
        futures = {ex.submit(fit_one_asset, item): item[0] for item in work_items}
        done = 0
        for fut in as_completed(futures):
            sym = futures[fut]
            try:
                _, r2_dict = fut.result()
                results.append({"symbol": sym, **r2_dict})
            except Exception as exc:
                logger.error("%s failed: %s", sym, exc)
            done += 1
            if done % 100 == 0 or done == len(work_items):
                elapsed = time.time() - t0
                eta = (len(work_items) - done) * elapsed / max(done, 1)
                logger.info("%d/%d done (elapsed=%.0fs, eta=%.0fs)",
                            done, len(work_items), elapsed, eta)

    df_per_asset = pd.DataFrame(results)
    write_report(df_per_asset, constituents, out_dir)
    print(f"OK: {out_dir}/08_broad_universe.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
