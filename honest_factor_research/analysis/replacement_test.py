"""Analysis 7 — Direct-Factor Replacement + Tier Expansion Test.

Two-phase analysis:

**Phase A — Replacements:** V1 (baseline current factors) → V2 (vol-fix:
VXX → ^VIX) → V3 (oil-fix: XLE → Brent BZ=F). Marginal mean Δr² per step.

**Phase B — Individual Tier 1-3 Expansions:** for each candidate factor
(Gold, Copper, HY-Credit, 2Y/30Y Treasury, NatGas, EUR/USD, USD/JPY,
Agriculture, Lithium, Uranium, EM-Currencies), runs ``V3 + that ONE factor``
and reports marginal Δr² vs V3.

The pattern is what matters: **measure marginal contribution against a
reference set, not aggregate R²**. A factor with global mean Δr²=+0.003
might still be essential for a specific sector cluster.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV  # type: ignore[import-untyped]

from honest_factor_research.analysis._common import (
    DEFAULT_DATA_DIR,
    report_output_dir,
    resolve_factor_snapshot,
    setup_logging,
)
from honest_factor_research.data.fetch import fetch_one_ticker
from honest_factor_research.data.snapshot import long_to_wide_close, load_snapshot, to_log_returns

logger = setup_logging("analysis.07_replacement_test")

WINDOW_DAYS = 252
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


# Sequential variant definitions (V1 → V2 → V3)
V1_CURRENT = ["SPY", "IEF", "TIP_minus_IEF", "UUP", "VXX"]
V2_VOL_FIX = ["SPY", "IEF", "TIP_minus_IEF", "UUP", "^VIX"]
V3_OIL_FIX = ["SPY", "IEF", "TIP_minus_IEF", "UUP", "^VIX", "BZ=F"]

# Tier 1-3 individual candidates to test as V3 + 1 extra
TIER_INDIVIDUAL = {
    "T1_Gold":     ("GLD", "Gold spot"),
    "T1_Copper":   ("CPER", "Copper spot"),
    "T1_HYCredit": ("HYG_minus_IEF", "HY-Credit spread"),
    "T1_2Y":       ("SHY", "2Y Treasury"),
    "T1_30Y":      ("TLT", "30Y Treasury"),
    "T2_NatGas":   ("UNG", "Natural Gas"),
    "T2_EURUSD":   ("FXE", "EUR/USD"),
    "T2_USDJPY":   ("FXY", "USD/JPY"),
    "T3_Agri":     ("DBA", "Agriculture"),
    "T3_Lithium":  ("LIT", "Lithium / battery"),
    "T3_Uranium":  ("URA", "Uranium / nuclear"),
    "T3_EMCurr":   ("CEW", "EM-Currencies basket"),
}


def fetch_replacement_proxies(cache_path: Path, start: datetime, end: datetime) -> pd.DataFrame:
    """Cache + fetch the 14 ETFs needed for the replacement test."""
    needed = ["^VIX", "BZ=F", "GLD", "CPER", "HYG", "SHY", "TLT",
              "UNG", "FXE", "FXY", "DBA", "LIT", "URA", "CEW"]
    existing = pd.read_parquet(cache_path) if cache_path.exists() else pd.DataFrame()
    have = set(existing["symbol"].unique()) if not existing.empty else set()
    missing = [s for s in needed if s not in have]
    if missing:
        logger.info("Fetching %d replacement proxies", len(missing))
        frames = [existing] if not existing.empty else []
        for sym in missing:
            df = fetch_one_ticker(sym, start, end)
            if not df.empty:
                frames.append(df)
            time.sleep(0.1)
        combined = pd.concat(frames, ignore_index=True)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        combined.to_parquet(cache_path, index=False)
        return combined
    return existing


def build_returns(snap_path: Path, new_df: pd.DataFrame) -> pd.DataFrame:
    base = load_snapshot(snap_path)
    base_wide = long_to_wide_close(base)
    new_wide = long_to_wide_close(new_df)
    new_uniq = new_wide[[c for c in new_wide.columns if c not in base_wide.columns]]
    combined = base_wide.join(new_uniq, how="outer").sort_index()
    log_ret = to_log_returns(combined)
    # Construct spread columns
    if {"TIP", "IEF"}.issubset(log_ret.columns):
        log_ret["TIP_minus_IEF"] = log_ret["TIP"] - log_ret["IEF"]
    if {"HYG", "IEF"}.issubset(log_ret.columns):
        log_ret["HYG_minus_IEF"] = log_ret["HYG"] - log_ret["IEF"]
    return log_ret


def mean_r2(log_ret: pd.DataFrame, cols: list[str], asset_ret: pd.DataFrame,
            symbols: list[str], snapshot_dates: list) -> dict[str, float]:
    """Mean r² across snapshots per asset for a given factor-column-list."""
    available = [c for c in cols if c in log_ret.columns]
    vdf = log_ret[available]
    out: dict[str, float] = {}
    for sym in symbols:
        if sym not in asset_ret.columns:
            continue
        ar = asset_ret[sym]
        r2s = []
        for snap in snapshot_dates:
            ts = pd.Timestamp(snap)
            ar_win = ar.loc[ar.index <= ts].tail(WINDOW_DAYS)
            fr_win = vdf.loc[vdf.index <= ts].tail(WINDOW_DAYS)
            joined = pd.concat([ar_win, fr_win], axis=1, sort=False).dropna()
            if len(joined) < WINDOW_DAYS:
                continue
            y = joined.iloc[:, 0].to_numpy()
            X = joined.iloc[:, 1:].to_numpy()
            r2 = fit_r2(X, y)
            if np.isfinite(r2):
                r2s.append(r2)
        out[sym] = float(np.nanmean(r2s)) if r2s else float("nan")
    return out


def write_report(df_seq: pd.DataFrame, df_indiv: pd.DataFrame, out_dir: Path) -> None:
    md_path = out_dir / "07_replacement_test.md"
    csv_path = out_dir / "07_replacement_test.csv"
    merged = df_seq.merge(df_indiv, on="symbol", how="left")
    merged.to_csv(csv_path, float_format="%.4f", index=False)

    lines = []
    lines.append("# Analysis 7 — Direct-Factor Replacement + Tier Expansion Test\n")
    lines.append(f"**Date:** {pd.Timestamp.now().date().isoformat()}  ")
    lines.append(f"**Assets:** {len(df_seq)}\n")

    lines.append("## Phase A — Sequential Replacements (mean r² across assets)\n")
    lines.append("| Variant | n factors | Mean r² | Δ vs V1 |")
    lines.append("|---|---|---|---|")
    v1_mean = df_seq["V1_current"].mean()
    for vname, cols in (("V1_current", V1_CURRENT), ("V2_vol_fix", V2_VOL_FIX), ("V3_oil_fix", V3_OIL_FIX)):
        m = df_seq[vname].mean()
        lines.append(f"| {vname} | {len(cols)} | {m:.3f} | {m-v1_mean:+.3f} |")
    lines.append("")

    lines.append("## Phase B — Individual Tier 1-3 Candidates (Δr² vs V3)\n")
    lines.append("| Candidate | Description | Mean Δr² | Max Δr² (asset) |")
    lines.append("|---|---|---|---|")
    v3_per_asset = df_seq.set_index("symbol")["V3_oil_fix"]
    rows = []
    for vname, (col, desc) in TIER_INDIVIDUAL.items():
        if vname not in df_indiv.columns:
            continue
        per_asset = df_indiv.set_index("symbol")[vname]
        delta = (per_asset - v3_per_asset).dropna()
        if delta.empty:
            continue
        rows.append((vname, desc, delta.mean(), delta.max(), delta.idxmax()))
    rows.sort(key=lambda r: -r[2])
    for vname, desc, mean_d, max_d, argmax in rows:
        marker = "🟢" if mean_d >= 0.02 else "🟡" if mean_d >= 0.005 else "⚪"
        lines.append(f"| {marker} **{vname}** | {desc} | {mean_d:+.4f} | "
                     f"{max_d:+.3f} ({argmax}) |")
    lines.append("")

    lines.append("## How to interpret\n")
    lines.append("- 🟢 Mean Δr² ≥ 0.02 → add to universal catalog")
    lines.append("- 🟡 Mean Δr² 0.005-0.02 → consider sector-conditional addition")
    lines.append("- ⚪ Mean Δr² < 0.005 → likely no universal value, but check top-asset Δ for niche use")
    lines.append("- A factor with low mean Δr² but huge max-Δ (e.g. Copper +0.20 for FCX) is ")
    lines.append("  sector-conditional value — see Mitigation 2G in METHODOLOGY.md.\n")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote: %s", md_path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--asset-snapshot", default=None)
    parser.add_argument("--symbols", nargs="+", default=None)
    parser.add_argument("--start", default="2019-06-01")
    parser.add_argument("--end", default="2024-12-31")
    parser.add_argument("--output-suffix", default="replacement-test")
    args = parser.parse_args(argv)

    snap = Path(args.snapshot) if args.snapshot else resolve_factor_snapshot()
    out_dir = report_output_dir(args.output_suffix)
    cache_path = DEFAULT_DATA_DIR / "cache" / "replacement_proxies.parquet"
    new_df = fetch_replacement_proxies(
        cache_path,
        datetime.strptime(args.start, "%Y-%m-%d"),
        datetime.strptime(args.end, "%Y-%m-%d"),
    )
    log_ret = build_returns(snap, new_df)
    asset_snap = Path(args.asset_snapshot) if args.asset_snapshot else snap
    asset_ret = to_log_returns(long_to_wide_close(load_snapshot(asset_snap)))
    symbols = args.symbols or sorted(asset_ret.columns)

    month_ends = pd.date_range(start="2020-12-31", end=args.end, freq="ME")
    log_ret_dates = pd.DatetimeIndex(log_ret.index).normalize()
    snapshot_dates = []
    for me in month_ends:
        cand = log_ret_dates[log_ret_dates <= pd.Timestamp(me)]
        if len(cand) > 0:
            d = cand[-1].date()
            if not snapshot_dates or snapshot_dates[-1] != d:
                snapshot_dates.append(d)
    logger.info("Snapshots: %d", len(snapshot_dates))

    # Phase A: sequential
    seq_data = {"symbol": symbols}
    for vname, cols in (("V1_current", V1_CURRENT), ("V2_vol_fix", V2_VOL_FIX), ("V3_oil_fix", V3_OIL_FIX)):
        per_asset = mean_r2(log_ret, cols, asset_ret, symbols, snapshot_dates)
        seq_data[vname] = [per_asset.get(s, float("nan")) for s in symbols]
    df_seq = pd.DataFrame(seq_data)

    # Phase B: individual additions to V3
    indiv_data = {"symbol": symbols}
    for vname, (col, _desc) in TIER_INDIVIDUAL.items():
        cols = V3_OIL_FIX + [col]
        per_asset = mean_r2(log_ret, cols, asset_ret, symbols, snapshot_dates)
        indiv_data[vname] = [per_asset.get(s, float("nan")) for s in symbols]
    df_indiv = pd.DataFrame(indiv_data)

    write_report(df_seq, df_indiv, out_dir)
    print(f"OK: {out_dir}/07_replacement_test.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
