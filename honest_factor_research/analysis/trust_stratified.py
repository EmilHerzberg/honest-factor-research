"""Analysis 6 — Trust-Stratified R² Decomposition.

**The headline methodology** of this repo (see ``METHODOLOGY.md``).

For each (asset, snapshot), runs THREE separate Ridge regressions:

  1. DIRECT-only      → r²_direct
  2. + STATISTICAL    → r²_+statistical
  3. + DERIVED        → r²_total

Then ``derived_share = (r²_total − r²_+statistical) / r²_total`` — the
fraction of total R² that comes from heterogeneous sector baskets. High
derived_share is a warning sign that the asset may be mirror-fitting its
own sector ETF.

Reports include:
  - Global summary statistics per tier
  - Top-15 / Bottom-15 assets by r²_direct
  - Top-15 assets by derived_share (mirror-suspect)
  - Quality-tier reclassification (OLD r²_total-based vs NEW trust-stratified)
  - Optional spotlight on a specific asset (e.g. JPM)
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV  # type: ignore[import-untyped]

from honest_factor_research.analysis._common import (
    report_output_dir,
    resolve_factor_snapshot,
    setup_logging,
)
from honest_factor_research.data.snapshot import load_returns
from honest_factor_research.returns.load import load_factor_catalog, load_factor_returns

logger = setup_logging("analysis.06_trust_stratified")

WINDOW_DAYS = 252
RIDGE_ALPHAS = (0.01, 0.05, 0.1)


def fit_r2(X: np.ndarray, y: np.ndarray) -> float:
    """RidgeCV-fit, return only R². Consistent with main pipeline."""
    if X.shape[1] == 0 or X.shape[0] < X.shape[1] + 5:
        return float("nan")
    try:
        ridge = RidgeCV(alphas=list(RIDGE_ALPHAS))
        ridge.fit(X, y)
        return float(ridge.score(X, y))
    except Exception:
        return float("nan")


def compute_trust_decomposition(
    asset_returns: pd.Series,
    factor_returns: pd.DataFrame,
    direct_cols: list[str],
    statistical_cols: list[str],
    derived_cols: list[str],
) -> tuple[float, float, float]:
    """Three R² values from three RidgeCV-fits on the same joined window."""
    joined = pd.concat([asset_returns, factor_returns], axis=1).dropna()
    if len(joined) < WINDOW_DAYS:
        return float("nan"), float("nan"), float("nan")
    y = joined.iloc[:, 0].to_numpy()
    available = list(joined.columns[1:])

    direct_avail = [c for c in direct_cols if c in available]
    plus_stat = direct_avail + [c for c in statistical_cols if c in available]
    all_avail = plus_stat + [c for c in derived_cols if c in available]

    r2_direct = fit_r2(joined[direct_avail].to_numpy(), y) if direct_avail else float("nan")
    r2_stat = fit_r2(joined[plus_stat].to_numpy(), y) if plus_stat else float("nan")
    r2_total = fit_r2(joined[all_avail].to_numpy(), y) if all_avail else float("nan")
    return r2_direct, r2_stat, r2_total


def old_tier(r2_total: float) -> str:
    if r2_total >= 0.6:
        return "HIGH"
    if r2_total >= 0.3:
        return "MED"
    return "LOW"


def new_tier_trust_stratified(r2_direct: float, r2_stat: float, r2_total: float) -> str:
    """Trust-stratified asset-quality tier (see METHODOLOGY.md §3)."""
    if not np.isfinite(r2_total) or r2_total <= 0:
        return "LOW"
    derived_share = (r2_total - r2_stat) / r2_total
    if r2_direct >= 0.35:
        return "HIGH"
    if r2_stat >= 0.45 and derived_share < 0.30:
        return "MED"
    if r2_total >= 0.55 and derived_share < 0.50:
        return "MED_DERIVED_HEAVY"
    return "LOW"


def aggregate_per_asset(records: list[dict]) -> pd.DataFrame:
    """Mean-aggregate the per-snapshot records to per-asset summary."""
    by_asset = defaultdict(list)
    for r in records:
        by_asset[r["symbol"]].append(r)
    rows = []
    for sym, lst in by_asset.items():
        r2d = np.nanmean([r["r2_direct"] for r in lst])
        r2s = np.nanmean([r["r2_statistical"] for r in lst])
        r2t = np.nanmean([r["r2_total"] for r in lst])
        if r2t > 0.01:
            ds = (r2t - r2s) / r2t
        else:
            ds = 0.0
        rows.append({
            "symbol": sym,
            "n_snapshots": len(lst),
            "r2_direct": r2d,
            "r2_+statistical": r2s,
            "r2_total": r2t,
            "marginal_statistical": r2s - r2d,
            "marginal_derived": r2t - r2s,
            "derived_share": ds,
        })
    df = pd.DataFrame(rows).sort_values("r2_direct", ascending=False)
    return df


def write_report(per_asset: pd.DataFrame, spotlight: dict | None,
                 direct_cols, stat_cols, derived_cols, out_dir: Path) -> None:
    csv_path = out_dir / "06_trust_stratified_r2.csv"
    md_path = out_dir / "06_trust_stratified_r2.md"
    per_asset.to_csv(csv_path, float_format="%.4f", index=False)

    lines = []
    lines.append("# Analysis 6 — Trust-Stratified R² Decomposition\n")
    lines.append(f"**Date:** {pd.Timestamp.now().date().isoformat()}  ")
    lines.append("**Method:** three separate RidgeCV regressions per asset×snapshot  ")
    lines.append(f"**Window:** {WINDOW_DAYS} trading-days  ")
    lines.append(f"**Factors:** {len(direct_cols)} DIRECT, {len(stat_cols)} STATISTICAL, "
                 f"{len(derived_cols)} DERIVED_THEME\n")

    lines.append("## Classification\n")
    lines.append(f"- **DIRECT** ({len(direct_cols)}): "
                 + ", ".join(f"`{f}`" for f in direct_cols))
    lines.append(f"- **STATISTICAL** ({len(stat_cols)}): "
                 + ", ".join(f"`{f}`" for f in stat_cols))
    lines.append(f"- **DERIVED_THEME** ({len(derived_cols)}): "
                 + ", ".join(f"`{f}`" for f in derived_cols))
    lines.append("")

    lines.append("## Summary\n")
    lines.append(f"- **{len(per_asset)} assets** analyzed")
    lines.append(f"- Mean r²_direct: **{per_asset['r2_direct'].mean():.3f}**")
    lines.append(f"- Mean r²_+statistical: {per_asset['r2_+statistical'].mean():.3f}")
    lines.append(f"- Mean r²_total: {per_asset['r2_total'].mean():.3f}")
    lines.append(f"- Mean derived_share: **{per_asset['derived_share'].mean():.1%}**\n")

    # Tier reclassification
    per_asset = per_asset.copy()
    per_asset["old_tier"] = per_asset["r2_total"].apply(old_tier)
    per_asset["new_tier"] = per_asset.apply(
        lambda r: new_tier_trust_stratified(
            r["r2_direct"], r["r2_+statistical"], r["r2_total"]
        ), axis=1,
    )
    per_asset["tier_change"] = per_asset["old_tier"] + " → " + per_asset["new_tier"]

    lines.append("## Tier Reclassification (OLD r²_total based → NEW trust-stratified)\n")
    transitions = per_asset["tier_change"].value_counts().sort_index()
    lines.append("| Tier change | Count |")
    lines.append("|---|---|")
    for change, n in transitions.items():
        marker = "  ⚠️  Downgrade" if ("→ LOW" in change or "DERIVED_HEAVY" in change) else ""
        lines.append(f"| {change} | {n}{marker} |")
    lines.append("")

    lines.append("## Top-15 by r²_direct (highest DIRECT-trust)\n")
    lines.append("| Symbol | r²_direct | r²_+stat | r²_total | derived_share | NEW Tier |")
    lines.append("|---|---|---|---|---|---|")
    for _, r in per_asset.head(15).iterrows():
        lines.append(
            f"| `{r['symbol']}` | {r['r2_direct']:.3f} | {r['r2_+statistical']:.3f} | "
            f"{r['r2_total']:.3f} | {r['derived_share']:.1%} | {r['new_tier']} |"
        )
    lines.append("")

    lines.append("## Bottom-15 by r²_direct\n")
    lines.append("| Symbol | r²_direct | r²_+stat | r²_total | derived_share | NEW Tier |")
    lines.append("|---|---|---|---|---|---|")
    for _, r in per_asset.tail(15).iterrows():
        lines.append(
            f"| `{r['symbol']}` | {r['r2_direct']:.3f} | {r['r2_+statistical']:.3f} | "
            f"{r['r2_total']:.3f} | {r['derived_share']:.1%} | {r['new_tier']} |"
        )
    lines.append("")

    lines.append("## Top-15 by derived_share (highest DERIVED-dependency, mirror-suspect)\n")
    lines.append("| Symbol | derived_share | r²_total | r²_+stat | marginal_derived | OLD → NEW |")
    lines.append("|---|---|---|---|---|---|")
    for _, r in per_asset.sort_values("derived_share", ascending=False).head(15).iterrows():
        lines.append(
            f"| `{r['symbol']}` | {r['derived_share']:.1%} | {r['r2_total']:.3f} | "
            f"{r['r2_+statistical']:.3f} | +{r['marginal_derived']:.3f} | {r['tier_change']} |"
        )
    lines.append("")

    if spotlight:
        lines.append(f"## Spotlight: {spotlight['symbol']}\n")
        for k, v in spotlight.items():
            if k == "symbol":
                continue
            lines.append(f"- **{k}:** {v}")
        lines.append("")

    lines.append("## Interpretation\n")
    lines.append("- **r²_direct** = explanation from DIRECT-physical factors only (rates, "
                 "inflation, VIX-spot, etc.)")
    lines.append("- **r²_+statistical** = + academic style factors (value, momentum, quality)")
    lines.append("- **r²_total** = + heterogeneous sector baskets (XLF, XLV, etc.)")
    lines.append("- **derived_share** = fraction of R² that COULD be mirror artifact")
    lines.append("")
    lines.append("Honest statement per asset: r²_direct% sure-explained, marginal_statistical% "
                 "half-explained, marginal_derived% mirror-suspect, (1−r²_total)% idiosyncratic.\n")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote: %s", md_path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--catalog", default=None)
    parser.add_argument("--asset-snapshot", default=None,
                        help="Optional separate OHLCV parquet for assets (defaults to factor snapshot)")
    parser.add_argument("--symbols", nargs="+", default=None,
                        help="Restrict to these tickers (default: all in asset snapshot)")
    parser.add_argument("--output-suffix", default="trust-stratified")
    parser.add_argument("--spotlight", default=None,
                        help="Print a focused spotlight for this ticker (e.g. JPM)")
    parser.add_argument("--start-snapshot", default="2020-12-31",
                        help="First monthly snapshot date (default 2020-12-31)")
    parser.add_argument("--end-snapshot", default="2024-12-31",
                        help="Last monthly snapshot date (default 2024-12-31)")
    args = parser.parse_args(argv)

    factor_snap = Path(args.snapshot) if args.snapshot else resolve_factor_snapshot()
    out_dir = report_output_dir(args.output_suffix)

    catalog = load_factor_catalog(args.catalog)
    factor_returns = load_factor_returns(factor_snap, args.catalog)

    # Classify factors by trust tier
    direct_cols = [s.factor_id for s in catalog if s.klass == "DIRECT"]
    stat_cols = [s.factor_id for s in catalog if s.klass == "STATISTICAL"]
    derived_cols = [s.factor_id for s in catalog if s.klass == "DERIVED"]
    # market_beta is technically the foundational direct: include it in DIRECT
    if "market_beta" not in direct_cols and "market_beta" in stat_cols:
        # We classified market_beta as STATISTICAL in catalog conceptually,
        # but treat it as DIRECT for the trust-decomposition (SPY is unambiguous).
        stat_cols.remove("market_beta")
        direct_cols.insert(0, "market_beta")

    asset_snap = Path(args.asset_snapshot) if args.asset_snapshot else factor_snap
    asset_returns = load_returns(asset_snap)
    symbols = args.symbols or sorted(asset_returns.columns)
    logger.info("Symbols: %d", len(symbols))

    # Monthly snapshot grid
    month_ends = pd.date_range(start=args.start_snapshot, end=args.end_snapshot, freq="ME")
    factor_dates = pd.DatetimeIndex(factor_returns.index).normalize()
    snapshot_dates = []
    for me in month_ends:
        cand = factor_dates[factor_dates <= pd.Timestamp(me)]
        if len(cand) > 0:
            d = cand[-1].date()
            if not snapshot_dates or snapshot_dates[-1] != d:
                snapshot_dates.append(d)
    logger.info("Snapshots: %d", len(snapshot_dates))

    records = []
    spotlight_rows = []
    for sym in symbols:
        if sym not in asset_returns.columns:
            continue
        ar = asset_returns[sym]
        for snap in snapshot_dates:
            ts = pd.Timestamp(snap)
            ar_win = ar.loc[ar.index <= ts].tail(WINDOW_DAYS)
            fr_win = factor_returns.loc[factor_returns.index <= ts].tail(WINDOW_DAYS)
            r2d, r2s, r2t = compute_trust_decomposition(
                ar_win, fr_win, direct_cols, stat_cols, derived_cols,
            )
            if not np.isfinite(r2t):
                continue
            rec = {"symbol": sym, "snapshot": snap,
                   "r2_direct": r2d, "r2_statistical": r2s, "r2_total": r2t}
            records.append(rec)
            if args.spotlight and sym == args.spotlight:
                spotlight_rows.append(rec)

    per_asset = aggregate_per_asset(records)
    logger.info("Per-asset rows: %d", len(per_asset))

    spotlight = None
    if args.spotlight and spotlight_rows:
        r2d_arr = [r["r2_direct"] for r in spotlight_rows]
        r2s_arr = [r["r2_statistical"] for r in spotlight_rows]
        r2t_arr = [r["r2_total"] for r in spotlight_rows]
        spotlight = {
            "symbol": args.spotlight,
            "n_snapshots": len(spotlight_rows),
            "r²_direct mean": f"{np.nanmean(r2d_arr):.3f} (range {np.nanmin(r2d_arr):.3f} - {np.nanmax(r2d_arr):.3f})",
            "r²_+statistical mean": f"{np.nanmean(r2s_arr):.3f}",
            "r²_total mean": f"{np.nanmean(r2t_arr):.3f} (max {np.nanmax(r2t_arr):.3f})",
            "derived_share mean": f"{np.nanmean([(t-s)/max(t,0.01) for t,s in zip(r2t_arr, r2s_arr)]):.1%}",
        }

    write_report(per_asset, spotlight, direct_cols, stat_cols, derived_cols, out_dir)
    print(f"OK: {out_dir}/06_trust_stratified_r2.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
