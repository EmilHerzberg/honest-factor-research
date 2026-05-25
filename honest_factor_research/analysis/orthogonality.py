"""Analysis 1 — Factor Orthogonality after Gram-Schmidt Residualization.

Validates that the sequential Gram-Schmidt residualization makes our N
factors approximately orthogonal. Outputs a Pearson correlation matrix,
heatmap PNG, and flagged pairs above the redundancy threshold.

Real-world finding from this methodology: V3.2 of the original system had
``growth × value`` ρ=-0.925 (near-perfect anti-correlation, basically
double-counting style information). Moving ``growth`` from tier 3 to tier 4
with ``value`` as additional regressor reduced this to ρ=+0.000. This
analysis is exactly the diagnostic that catches such errors.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from honest_factor_research.analysis._common import (
    report_output_dir,
    resolve_factor_snapshot,
    setup_logging,
)
from honest_factor_research.returns.load import load_factor_catalog, load_factor_returns

logger = setup_logging("analysis.01_orthogonality")

REDUNDANCY_THRESHOLD = 0.30


def flag_redundancies(corr: pd.DataFrame, threshold: float = REDUNDANCY_THRESHOLD):
    """Return pairs (f1, f2, ρ) with |ρ| >= threshold, sorted by |ρ| descending."""
    pairs = []
    cols = list(corr.columns)
    for i, f1 in enumerate(cols):
        for f2 in cols[i + 1:]:
            rho = float(corr.loc[f1, f2])
            if abs(rho) >= threshold:
                pairs.append((f1, f2, rho))
    return sorted(pairs, key=lambda x: -abs(x[2]))


def plot_heatmap(corr: pd.DataFrame, out_path: Path) -> None:
    """Annotated correlation heatmap PNG."""
    n = len(corr)
    fig, ax = plt.subplots(figsize=(max(8, n * 0.4), max(6, n * 0.35)))
    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(corr.index, fontsize=8)
    for i in range(n):
        for j in range(n):
            val = corr.values[i, j]
            color = "white" if abs(val) > 0.5 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=6)
    plt.colorbar(im, ax=ax, label="Pearson ρ")
    ax.set_title(
        "Residualized Factor-Returns Correlation Matrix\n"
        f"(Diagonal=1.0; |ρ|>{REDUNDANCY_THRESHOLD} = redundancy candidate)"
    )
    plt.tight_layout()
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def write_report(corr: pd.DataFrame, flagged, specs, out_dir: Path) -> None:
    """Write markdown report + CSV + PNG."""
    csv_path = out_dir / "01_factor_orthogonality_corr.csv"
    png_path = out_dir / "01_factor_orthogonality_heatmap.png"
    md_path = out_dir / "01_factor_orthogonality.md"

    corr.to_csv(csv_path, float_format="%.4f")
    plot_heatmap(corr, png_path)

    off_diag = corr.values[~np.eye(corr.shape[0], dtype=bool)]
    abs_off = np.abs(off_diag)
    lines = []
    lines.append("# Analysis 1 — Factor Orthogonality\n")
    lines.append(f"**Date:** {pd.Timestamp.now().date().isoformat()}  ")
    lines.append(f"**Factors:** {len(corr)} (after Gram-Schmidt residualization)  ")
    lines.append(f"**Redundancy threshold:** |ρ| ≥ {REDUNDANCY_THRESHOLD}\n")

    lines.append("## Summary")
    lines.append(f"- Off-diagonal pairs: {len(off_diag) // 2}")
    lines.append(f"- Mean |ρ|: **{abs_off.mean():.3f}**")
    lines.append(f"- Max |ρ|: **{abs_off.max():.3f}**")
    lines.append(f"- Flagged pairs (|ρ| ≥ {REDUNDANCY_THRESHOLD}): **{len(flagged)}**\n")

    if flagged:
        lines.append("## Flagged Redundancy Candidates\n")
        lines.append("| Factor 1 | Factor 2 | ρ | Assessment |")
        lines.append("|---|---|---|---|")
        for f1, f2, rho in flagged:
            if abs(rho) >= 0.7:
                assess = "🔴 **strongly redundant** — residualization gap"
            elif abs(rho) >= 0.5:
                assess = "🟠 moderately redundant — possibly mergeable"
            else:
                assess = "🟡 weak residual correlation — acceptable"
            lines.append(f"| `{f1}` | `{f2}` | {rho:+.3f} | {assess} |")
        lines.append("")
    else:
        lines.append("## ✅ No Redundancy Candidates\n")
        lines.append(f"All off-diagonal correlations |ρ| < {REDUNDANCY_THRESHOLD}.\n")

    lines.append("## Residualization Order (Catalog)\n")
    lines.append("| Tier | Factor | Residualized against | Class |")
    lines.append("|---|---|---|---|")
    for s in specs:
        against = ", ".join(s.residualized_against) if s.residualized_against else "—"
        lines.append(f"| {s.tier} | `{s.factor_id}` | {against} | {s.klass} |")
    lines.append("")

    lines.append(f"## Heatmap\n\n![Correlation Heatmap]({png_path.name})\n")
    lines.append(f"Full matrix: `{csv_path.name}`\n")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote: %s", md_path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--snapshot", default=None,
                        help="Override factor-ETFs snapshot path")
    parser.add_argument("--catalog", default=None,
                        help="Override factor catalog YAML path")
    parser.add_argument("--output-suffix", default="orthogonality",
                        help="Subdirectory suffix under reports/")
    args = parser.parse_args(argv)

    snap = Path(args.snapshot) if args.snapshot else resolve_factor_snapshot()
    out_dir = report_output_dir(args.output_suffix)
    logger.info("Snapshot: %s", snap)
    logger.info("Output:   %s", out_dir)

    specs = load_factor_catalog(args.catalog)
    factor_returns = load_factor_returns(snap, args.catalog)
    logger.info("Loaded %d residualized factor returns over %d trading-days",
                len(factor_returns.columns), len(factor_returns))

    corr = factor_returns.corr(method="pearson")
    flagged = flag_redundancies(corr)
    for f1, f2, rho in flagged:
        logger.info("  %s ↔ %s: %+.3f", f1, f2, rho)
    write_report(corr, flagged, specs, out_dir)
    print(f"OK: {out_dir}/01_factor_orthogonality.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
