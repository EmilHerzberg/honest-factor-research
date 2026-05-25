"""Analysis 4 — Univariate Index Discovery.

For each (asset, candidate-index) pair, runs a SINGLE-FACTOR OLS regression
on a common 252-day window and reports R². Ranks the candidates per asset
to identify which not-yet-in-catalog indices best explain that asset's
returns. Drives factor-catalog expansion decisions.

Real-world finding from this methodology: this analysis showed that
XLF (Financial Sector ETF) explains 85% of JPM variance univariately —
strong evidence to add XLF as a sector factor. Same for XLU/DUK,
XLRE/AMT, etc. The V3.3 sector-factor expansion was driven by this report.
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

logger = setup_logging("analysis.04_index_discovery")


def univariate_r2(y: pd.Series, x: pd.Series) -> tuple[float, float]:
    """OLS y ~ x (with intercept), return (R², beta)."""
    joined = pd.concat([y, x], axis=1).dropna()
    if len(joined) < 252:
        return float("nan"), float("nan")
    Y = joined.iloc[:, 0].to_numpy()
    X = joined.iloc[:, 1].to_numpy()
    X_design = np.column_stack([np.ones(len(X)), X])
    try:
        beta, *_ = np.linalg.lstsq(X_design, Y, rcond=None)
        fitted = X_design @ beta
        ss_res = float(np.sum((Y - fitted) ** 2))
        ss_tot = float(np.sum((Y - Y.mean()) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
        return r2, float(beta[1])
    except Exception:
        return float("nan"), float("nan")


def write_report(r2_matrix: pd.DataFrame, beta_matrix: pd.DataFrame, out_dir: Path) -> None:
    md_path = out_dir / "04_index_discovery.md"
    r2_csv = out_dir / "04_index_discovery_r_squared.csv"
    beta_csv = out_dir / "04_index_discovery_betas.csv"
    r2_matrix.to_csv(r2_csv, float_format="%.4f")
    beta_matrix.to_csv(beta_csv, float_format="%.4f")

    lines = []
    lines.append("# Analysis 4 — Univariate Index Discovery\n")
    lines.append(f"**Date:** {pd.Timestamp.now().date().isoformat()}  ")
    lines.append(f"**Assets:** {len(r2_matrix)}, **Candidate indices:** {len(r2_matrix.columns)}\n")

    lines.append("## Per-asset top-3 candidate factors (univariate R²)\n")
    lines.append("| Symbol | Top-1 | R² | Top-2 | R² | Top-3 | R² |")
    lines.append("|---|---|---|---|---|---|---|")
    for sym in r2_matrix.index:
        row = r2_matrix.loc[sym].sort_values(ascending=False).head(3)
        cells = [sym]
        for cand, r2 in row.items():
            cells.append(cand)
            cells.append(f"{r2:.3f}")
        while len(cells) < 7:
            cells.append("—")
        lines.append("| " + " | ".join(str(c) for c in cells) + " |")
    lines.append("")

    lines.append("## How to read this\n")
    lines.append("If a non-MVP candidate (e.g. `XLF`, `XLU`, `XLRE`, `ITA`) shows R²>0.4 for ")
    lines.append("multiple assets in a sector, that's strong evidence the catalog is missing ")
    lines.append("that sector factor. This analysis drove the V3.3 sector-factor expansion ")
    lines.append("(adding XLF/XLV/XLI/XLP/XLU/XLRE).\n")
    lines.append(f"Full R²-matrix: `{r2_csv.name}`; betas: `{beta_csv.name}`\n")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote: %s", md_path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--asset-snapshot", default=None)
    parser.add_argument("--candidates", nargs="+", default=None,
                        help="Candidate-index symbols (default: all non-asset columns in snapshot)")
    parser.add_argument("--symbols", nargs="+", default=None)
    parser.add_argument("--output-suffix", default="index-discovery")
    args = parser.parse_args(argv)

    snap = Path(args.snapshot) if args.snapshot else resolve_factor_snapshot()
    out_dir = report_output_dir(args.output_suffix)
    all_returns = load_returns(snap)
    if args.asset_snapshot and args.asset_snapshot != str(snap):
        asset_returns = load_returns(Path(args.asset_snapshot))
    else:
        asset_returns = all_returns
    symbols = args.symbols or sorted(asset_returns.columns)
    candidates = args.candidates or sorted(all_returns.columns)
    logger.info("Symbols: %d, Candidates: %d", len(symbols), len(candidates))

    r2_data = {}
    beta_data = {}
    for sym in symbols:
        if sym not in asset_returns.columns:
            continue
        y = asset_returns[sym]
        r2_row = {}
        beta_row = {}
        for cand in candidates:
            if cand == sym or cand not in all_returns.columns:
                continue
            r2, b = univariate_r2(y, all_returns[cand])
            r2_row[cand] = r2
            beta_row[cand] = b
        r2_data[sym] = r2_row
        beta_data[sym] = beta_row

    r2_matrix = pd.DataFrame(r2_data).T
    beta_matrix = pd.DataFrame(beta_data).T
    write_report(r2_matrix, beta_matrix, out_dir)
    print(f"OK: {out_dir}/04_index_discovery.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
