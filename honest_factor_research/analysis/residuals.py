"""Analysis 3 — Per-Asset Residual Statistics.

For each asset, fits Ridge against the full factor set and computes
residual statistics: std-dev, kurtosis, max-σ-outlier-day, count of ≥3σ
days. Assets with high residual kurtosis or many extreme days are
fundamentally hard to model with macro/style factors alone.

Real-world finding from this methodology: TSLA had residual std=3.49%
daily — the highest in the 60-asset MVP universe — indicating
fundamentally weak factor-explainability. This was diagnostic that drove
later research into asset-specific factors (Mitigation 2G).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kurtosis  # type: ignore[import-untyped]
from sklearn.linear_model import RidgeCV  # type: ignore[import-untyped]

from honest_factor_research.analysis._common import (
    report_output_dir,
    resolve_factor_snapshot,
    setup_logging,
)
from honest_factor_research.data.snapshot import load_returns
from honest_factor_research.returns.load import load_factor_returns

logger = setup_logging("analysis.03_residuals")


def per_asset_stats(
    asset_returns: pd.Series, factor_returns: pd.DataFrame,
) -> dict | None:
    """Fit Ridge → compute residual statistics."""
    joined = pd.concat([asset_returns, factor_returns], axis=1).dropna()
    if len(joined) < 252:
        return None
    y = joined.iloc[:, 0].to_numpy()
    X = joined.iloc[:, 1:].to_numpy()
    try:
        ridge = RidgeCV(alphas=[0.01, 0.05, 0.1])
        ridge.fit(X, y)
        fitted = ridge.predict(X)
        residuals = y - fitted
    except Exception:
        return None
    sigma = float(np.std(residuals, ddof=1))
    if sigma <= 0:
        return None
    return {
        "n_obs": len(residuals),
        "residual_std_daily": sigma,
        "residual_std_annualized": sigma * np.sqrt(252),
        "residual_kurtosis": float(kurtosis(residuals, fisher=False)),
        "max_abs_sigma": float(np.max(np.abs(residuals)) / sigma),
        "n_3sigma_days": int((np.abs(residuals) >= 3 * sigma).sum()),
        "n_4sigma_days": int((np.abs(residuals) >= 4 * sigma).sum()),
        "r_squared": float(ridge.score(X, y)),
    }


def write_report(df: pd.DataFrame, out_dir: Path) -> None:
    md_path = out_dir / "03_residual_analysis.md"
    csv_path = out_dir / "03_residual_analysis.csv"
    df.to_csv(csv_path, float_format="%.4f", index=False)

    lines = []
    lines.append("# Analysis 3 — Per-Asset Residual Statistics\n")
    lines.append(f"**Date:** {pd.Timestamp.now().date().isoformat()}  ")
    lines.append(f"**Assets:** {len(df)}\n")

    if df.empty:
        md_path.write_text("\n".join(lines), encoding="utf-8")
        return

    lines.append("## Highest residual volatility (hardest to model)\n")
    lines.append("| Symbol | residual σ (daily) | residual σ (ann.) | kurtosis | max |σ| | #≥3σ days |")
    lines.append("|---|---|---|---|---|---|")
    for _, r in df.sort_values("residual_std_daily", ascending=False).head(15).iterrows():
        lines.append(
            f"| `{r['symbol']}` | {r['residual_std_daily']*100:.2f}% | "
            f"{r['residual_std_annualized']*100:.1f}% | {r['residual_kurtosis']:.1f} | "
            f"{r['max_abs_sigma']:.1f} | {int(r['n_3sigma_days'])} |"
        )
    lines.append("")

    lines.append("## Most leptokurtic residuals (heaviest tails)\n")
    lines.append("| Symbol | kurtosis | residual σ (daily) | max |σ| | #≥4σ days |")
    lines.append("|---|---|---|---|---|")
    for _, r in df.sort_values("residual_kurtosis", ascending=False).head(15).iterrows():
        lines.append(
            f"| `{r['symbol']}` | {r['residual_kurtosis']:.1f} | "
            f"{r['residual_std_daily']*100:.2f}% | {r['max_abs_sigma']:.1f} | "
            f"{int(r['n_4sigma_days'])} |"
        )
    lines.append("")

    lines.append("## Interpretation\n")
    lines.append("- **Residual std-daily** > 2% suggests the asset is fundamentally noisy")
    lines.append("- **Kurtosis** > 5 = noticeably fat-tailed (Gauß = 3)")
    lines.append("- **#≥3σ days** > 10 in 1000 days = significantly more tail-events than Gauß predicts")
    lines.append("- These assets are candidates for ASSET-SPECIFIC factor additions (Mitigation 2G)")
    lines.append("  or for stricter Gate-Engine confidence thresholds.\n")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote: %s", md_path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--catalog", default=None)
    parser.add_argument("--asset-snapshot", default=None)
    parser.add_argument("--symbols", nargs="+", default=None)
    parser.add_argument("--output-suffix", default="residuals")
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
        stats = per_asset_stats(asset_returns[sym], factor_returns)
        if stats is None:
            continue
        rows.append({"symbol": sym, **stats})

    df = pd.DataFrame(rows)
    write_report(df, out_dir)
    print(f"OK: {out_dir}/03_residual_analysis.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
