"""Analysis 9 — Lead-Lag-Test (Asset[t+1] vs Factor[t]).

For each (asset, factor) pair, computes three OLS regressions:

  1. Contemporaneous: asset[t] ~ factor[t]
  2. LEAD:            asset[t+1] ~ factor[t]  (asset response to yesterday's factor move)
  3. LAG:             asset[t] ~ factor[t+1]  (asset leads factor)

In an efficient liquid market, lead-beta should be ≈ 0. Significant
|t_lead| > 3 indicates:
  - ETF settlement-timing differences (asia-Asia factors lead US-listed
    assets due to time-zone)
  - Stocks with low liquidity reacting with delay
  - Genuine economic lead-lag relationship (rare for liquid US large-caps)

Significant LAG-beta indicates the asset itself is a *price discovery
leader* — e.g. NVDA leading SOXX since NVDA is ~30% of SOXX.
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
from honest_factor_research.data.snapshot import load_returns
from honest_factor_research.returns.load import load_factor_returns

logger = setup_logging("analysis.09_lead_lag")

MIN_OBS = 500


def ols_with_se(y: np.ndarray, x: np.ndarray) -> tuple[float, float, float]:
    """OLS y ~ x (with intercept). Returns (beta, SE, t-stat)."""
    if len(y) < 30:
        return float("nan"), float("nan"), float("nan")
    X = np.column_stack([np.ones(len(x)), x])
    try:
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        fitted = X @ beta
        residuals = y - fitted
        n, k = X.shape
        df = n - k
        sigma2 = np.sum(residuals ** 2) / df
        XTX_inv = np.linalg.inv(X.T @ X)
        se = float(np.sqrt(sigma2 * XTX_inv[1, 1]))
        b = float(beta[1])
        t = b / se if se > 0 else float("nan")
        return b, se, t
    except Exception:
        return float("nan"), float("nan"), float("nan")


def lead_lag_for_pair(asset_ret: pd.Series, factor_ret: pd.Series) -> dict:
    df = pd.concat([asset_ret, factor_ret], axis=1, sort=True).dropna()
    df.columns = ["asset", "factor"]
    if len(df) < MIN_OBS:
        return {"n_obs": len(df)}
    b_c, se_c, t_c = ols_with_se(df["asset"].to_numpy(), df["factor"].to_numpy())

    df_lead = pd.concat(
        [df["asset"].shift(-1).rename("asset_next"), df["factor"]],
        axis=1,
    ).dropna()
    b_l, se_l, t_l = ols_with_se(df_lead["asset_next"].to_numpy(), df_lead["factor"].to_numpy())

    df_lag = pd.concat(
        [df["asset"], df["factor"].shift(-1).rename("factor_next")],
        axis=1,
    ).dropna()
    b_g, se_g, t_g = ols_with_se(df_lag["asset"].to_numpy(), df_lag["factor_next"].to_numpy())
    return {
        "n_obs": len(df),
        "contemp_beta": b_c, "contemp_t": t_c,
        "lead_beta": b_l, "lead_t": t_l,
        "lag_beta": b_g, "lag_t": t_g,
    }


def write_report(df: pd.DataFrame, out_dir: Path) -> None:
    md_path = out_dir / "09_lead_lag.md"
    csv_path = out_dir / "09_lead_lag.csv"
    df.to_csv(csv_path, float_format="%.4f", index=False)

    lines = []
    lines.append("# Analysis 9 — Lead-Lag-Test (Asset[t+1] vs Factor[t])\n")
    lines.append(f"**Date:** {pd.Timestamp.now().date().isoformat()}  ")
    lines.append(f"**Pairs analyzed:** {len(df)}\n")
    if df.empty:
        md_path.write_text("\n".join(lines), encoding="utf-8")
        return

    abs_t = df["lead_t"].abs()
    lines.append("## Global lead-t-stat distribution\n")
    lines.append(f"- Mean |t_lead|: {abs_t.mean():.3f}")
    lines.append(f"- Median: {abs_t.median():.3f}")
    lines.append(f"- p95: {abs_t.quantile(0.95):.3f}")
    lines.append(f"- Pairs with |t_lead| ≥ 3: {int((abs_t >= 3).sum())} ({(abs_t >= 3).mean()*100:.1f}%)\n")

    susp = df[df["lead_t"].abs() >= 3].sort_values(
        "lead_t", key=lambda s: -s.abs(),
    ).head(20)
    if not susp.empty:
        lines.append("## Top-20 Lead-Lag suspicious pairs (|t_lead| ≥ 3)\n")
        lines.append("| Asset | Factor | Lead β | Lead t | Contemp β | Contemp t |")
        lines.append("|---|---|---|---|---|---|")
        for _, r in susp.iterrows():
            lines.append(
                f"| `{r['symbol']}` | `{r['factor']}` | {r['lead_beta']:+.4f} | "
                f"{r['lead_t']:+.2f} | {r['contemp_beta']:+.4f} | {r['contemp_t']:+.2f} |"
            )
        lines.append("")

    lag_susp = df[df["lag_t"].abs() >= 3].sort_values(
        "lag_t", key=lambda s: -s.abs(),
    ).head(15)
    if not lag_susp.empty:
        lines.append("## Top-15 Reverse-Lead (Asset leads Factor, |t_lag| ≥ 3)\n")
        lines.append("These are price-discovery leaders — the asset is large enough in the index ")
        lines.append("that its moves anticipate the index.\n")
        lines.append("| Asset | Factor | Lag β | Lag t |")
        lines.append("|---|---|---|---|")
        for _, r in lag_susp.iterrows():
            lines.append(f"| `{r['symbol']}` | `{r['factor']}` | {r['lag_beta']:+.4f} | {r['lag_t']:+.2f} |")
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote: %s", md_path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--catalog", default=None)
    parser.add_argument("--asset-snapshot", default=None)
    parser.add_argument("--symbols", nargs="+", default=None)
    parser.add_argument("--output-suffix", default="lead-lag")
    args = parser.parse_args(argv)

    factor_snap = Path(args.snapshot) if args.snapshot else resolve_factor_snapshot()
    out_dir = report_output_dir(args.output_suffix)
    factor_returns = load_factor_returns(factor_snap, args.catalog)
    asset_snap = Path(args.asset_snapshot) if args.asset_snapshot else factor_snap
    asset_returns = load_returns(asset_snap)
    symbols = args.symbols or sorted(asset_returns.columns)

    rows = []
    for sym in symbols:
        if sym not in asset_returns.columns:
            continue
        ar = asset_returns[sym]
        for fid in factor_returns.columns:
            r = lead_lag_for_pair(ar, factor_returns[fid])
            if r.get("n_obs", 0) < MIN_OBS:
                continue
            rows.append({"symbol": sym, "factor": fid, **r})

    df = pd.DataFrame(rows)
    write_report(df, out_dir)
    print(f"OK: {out_dir}/09_lead_lag.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
