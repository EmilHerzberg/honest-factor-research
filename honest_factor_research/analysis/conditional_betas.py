"""Analysis 10 — Conditional-Beta Analysis (regime-stratified).

For each (asset, factor) pair, computes OLS beta in three regime-binary
stratifications:
  - VIX:        VIX > 25 (high) vs VIX < 15 (low)
  - Rates:      rising (IEF-return < p5) vs falling (IEF-return > p95)
  - Bull-Bear:  60d-rolling-SPY-return > +2% vs < -2%

Compares the two regime-specific betas via t-test on their difference.
Pairs with |t_diff| ≥ 2.5 are regime-dependent — their unconditional beta
is a mean across regimes and is wrong in at least one.

Real-world finding: 18.3% of asset-factor pairs in our universe had
regime-dependent beta. Worst case: GE × value flipped +2.94 (high-VIX) to
-0.15 (low-VIX), a sign reversal. This finding drove the V3.5
regime-switching architecture (see ``honest_factor_research/exposure/regime.py``).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from honest_factor_research.analysis._common import (
    report_output_dir,
    resolve_factor_snapshot,
    setup_logging,
)
from honest_factor_research.data.snapshot import (
    iter_symbol_batches,
    list_symbols,
    load_returns_for_symbols,
    load_snapshot,
    long_to_wide_close,
)
from honest_factor_research.returns.load import load_factor_returns

logger = setup_logging("analysis.10_conditional_betas")

MIN_OBS_PER_REGIME = 60
T_DIFF_THRESHOLD = 2.5


def build_regime_masks(factor_returns: pd.DataFrame, snap_path: Path) -> dict[str, dict[str, pd.Series]]:
    """Return regime-name → {"high": mask, "low": mask}."""
    out: dict[str, dict[str, pd.Series]] = {}
    wide = long_to_wide_close(load_snapshot(snap_path))

    if "^VIX" in wide.columns:
        vix = wide["^VIX"].dropna()
        out["VIX"] = {"high": vix > 25, "low": vix < 15}
        logger.info("VIX regime: high=%d low=%d", int((vix > 25).sum()), int((vix < 15).sum()))

    if "rates" in factor_returns.columns:
        rates = factor_returns["rates"].dropna()
        p5, p95 = rates.quantile(0.05), rates.quantile(0.95)
        out["Rates"] = {"high": rates < p5, "low": rates > p95}

    if "SPY" in wide.columns:
        spy = wide["SPY"].dropna()
        spy_log = np.log(spy / spy.shift(1)).dropna()
        roll60 = spy_log.rolling(60).sum()
        out["Bull-Bear"] = {"high": roll60 > 0.02, "low": roll60 < -0.02}

    return out


def beta_in_subset(asset_ret: pd.Series, factor_ret: pd.Series, mask: pd.Series) -> tuple[float, float, int]:
    idx = asset_ret.index.intersection(factor_ret.index).intersection(mask.index)
    if len(idx) == 0:
        return float("nan"), float("nan"), 0
    sub_mask = mask.reindex(idx).fillna(False).astype(bool)
    if int(sub_mask.sum()) < MIN_OBS_PER_REGIME:
        return float("nan"), float("nan"), int(sub_mask.sum())
    sub_idx = idx[sub_mask.to_numpy()]
    y = asset_ret.reindex(sub_idx).dropna()
    x = factor_ret.reindex(y.index).dropna()
    y = y.reindex(x.index)
    if len(y) < MIN_OBS_PER_REGIME:
        return float("nan"), float("nan"), len(y)
    X = np.column_stack([np.ones(len(x)), x.to_numpy()])
    try:
        beta, *_ = np.linalg.lstsq(X, y.to_numpy(), rcond=None)
        res = y.to_numpy() - X @ beta
        df = len(y) - 2
        sigma2 = np.sum(res ** 2) / df
        XTX_inv = np.linalg.inv(X.T @ X)
        se = float(np.sqrt(sigma2 * XTX_inv[1, 1]))
        return float(beta[1]), se, len(y)
    except Exception:
        return float("nan"), float("nan"), len(y)


def write_report(sw_df: pd.DataFrame, out_dir: Path) -> None:
    md_path = out_dir / "10_conditional_betas.md"
    csv_path = out_dir / "10_conditional_betas.csv"
    sw_df.to_csv(csv_path, float_format="%.4f", index=False)

    lines = []
    lines.append("# Analysis 10 — Conditional-Beta Analysis (regime-stratified)\n")
    lines.append(f"**Date:** {pd.Timestamp.now().date().isoformat()}  ")
    lines.append(f"**Switch comparisons:** {len(sw_df)}\n")
    if sw_df.empty:
        md_path.write_text("\n".join(lines), encoding="utf-8")
        return

    abs_t = sw_df["t_diff"].abs()
    lines.append("## Global regime-switch t-stat\n")
    lines.append(f"- Mean |t_diff|: {abs_t.mean():.3f}")
    lines.append(f"- Median: {abs_t.median():.3f}")
    lines.append(f"- p95: {abs_t.quantile(0.95):.3f}")
    lines.append(f"- Pairs with |t_diff| ≥ 2.5: {int((abs_t >= 2.5).sum())} ({(abs_t >= 2.5).mean()*100:.1f}%)")
    lines.append(f"- Pairs with |t_diff| ≥ 4: {int((abs_t >= 4).sum())} ({(abs_t >= 4).mean()*100:.1f}%)\n")

    for regime in sw_df["regime"].unique():
        sub = sw_df[sw_df["regime"] == regime]
        flagged = sub[sub["t_diff"].abs() >= T_DIFF_THRESHOLD].sort_values(
            "t_diff", key=lambda s: -s.abs(),
        ).head(15)
        if flagged.empty:
            continue
        lines.append(f"## Top-15 regime-switches: {regime}\n")
        lines.append("| Asset | Factor | β_high | β_low | Δβ | t_diff |")
        lines.append("|---|---|---|---|---|---|")
        for _, r in flagged.iterrows():
            lines.append(
                f"| `{r['symbol']}` | `{r['factor']}` | {r['beta_high']:+.3f} | "
                f"{r['beta_low']:+.3f} | {r['diff']:+.3f} | {r['t_diff']:+.2f} |"
            )
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote: %s", md_path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--catalog", default=None)
    parser.add_argument("--asset-snapshot", default=None)
    parser.add_argument("--symbols", nargs="+", default=None)
    parser.add_argument("--batch-size", type=int, default=400,
                        help="Process assets in batches of this many symbols "
                             "to bound peak memory (broad universe).")
    parser.add_argument("--output-suffix", default="conditional-betas")
    args = parser.parse_args(argv)

    factor_snap = Path(args.snapshot) if args.snapshot else resolve_factor_snapshot()
    out_dir = report_output_dir(args.output_suffix)
    factor_returns = load_factor_returns(factor_snap, args.catalog)
    asset_snap = Path(args.asset_snapshot) if args.asset_snapshot else factor_snap
    symbols = args.symbols or list_symbols(asset_snap)
    logger.info("Symbols: %d (batch size %d)", len(symbols), args.batch_size)

    regimes = build_regime_masks(factor_returns, factor_snap)
    rows = []
    for bi, batch in enumerate(iter_symbol_batches(symbols, args.batch_size), 1):
        asset_returns = load_returns_for_symbols(asset_snap, batch)
        for sym in batch:
            if sym not in asset_returns.columns:
                continue
            ar = asset_returns[sym]
            for fid in factor_returns.columns:
                fr = factor_returns[fid]
                for regime, masks in regimes.items():
                    bh, sh, nh = beta_in_subset(ar, fr, masks["high"])
                    bl, sl, nl = beta_in_subset(ar, fr, masks["low"])
                    if nh < MIN_OBS_PER_REGIME or nl < MIN_OBS_PER_REGIME:
                        continue
                    diff = bh - bl
                    diff_se = np.sqrt(sh ** 2 + sl ** 2)
                    t = diff / diff_se if diff_se > 0 else float("nan")
                    rows.append({
                        "symbol": sym, "factor": fid, "regime": regime,
                        "beta_high": bh, "beta_low": bl, "diff": diff, "t_diff": t,
                        "n_high": nh, "n_low": nl,
                    })
        del asset_returns
        logger.info("batch %d done (%d symbols), %d rows so far",
                    bi, len(batch), len(rows))

    sw_df = pd.DataFrame(rows)
    write_report(sw_df, out_dir)
    print(f"OK: {out_dir}/10_conditional_betas.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
