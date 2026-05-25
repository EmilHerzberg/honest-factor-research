"""Analysis 2 — Beta-Signs Sanity Check.

For each (asset, factor) pair, computes the unconditional Ridge beta and
checks whether the SIGN matches naive sector-priors (e.g. Technology should
have NEGATIVE rates-beta, Energy should have POSITIVE energy_oil-beta).

Mismatches don't necessarily indicate a bug — but a high rate of mismatches
in a sector suggests either a bad proxy, a missing factor, or an unusual
sample period.
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

logger = setup_logging("analysis.02_beta_signs")


# Naive priors: (sector_substring, factor_id) → expected sign
SECTOR_FACTOR_PRIORS: dict[tuple[str, str], str] = {
    ("Technology", "rates"): "NEG",          # Long-duration → rate-sensitive
    ("Technology", "growth"): "POS",
    ("Technology", "semiconductors"): "POS",
    ("Financial", "rates"): "POS",            # Banks benefit from rising rates
    ("Financial", "value"): "POS",
    ("Financial", "xl_financials"): "POS",
    ("Energy", "energy_oil"): "POS",
    ("Energy", "value"): "POS",
    ("Utilities", "rates"): "NEG",
    ("Utilities", "xl_utilities"): "POS",
    ("Real Estate", "rates"): "NEG",
    ("Real Estate", "xl_real_estate"): "POS",
}


def sign(x: float) -> str:
    if not np.isfinite(x):
        return "NA"
    if x > 0.05:
        return "POS"
    if x < -0.05:
        return "NEG"
    return "~0"


def compute_unconditional_betas(
    asset_returns: pd.Series, factor_returns: pd.DataFrame,
) -> dict[str, float]:
    """Single Ridge fit on the whole common period. Returns {factor_id: beta}."""
    from sklearn.linear_model import RidgeCV  # type: ignore[import-untyped]

    joined = pd.concat([asset_returns, factor_returns], axis=1).dropna()
    if len(joined) < 252:
        return {}
    y = joined.iloc[:, 0].to_numpy()
    cols = list(joined.columns[1:])
    X = joined[cols].to_numpy()
    try:
        ridge = RidgeCV(alphas=[0.01, 0.05, 0.1])
        ridge.fit(X, y)
    except Exception:
        return {}
    return {col: float(b) for col, b in zip(cols, ridge.coef_)}


def write_report(records: list[dict], out_dir: Path) -> None:
    md_path = out_dir / "02_beta_signs.md"
    csv_path = out_dir / "02_beta_signs.csv"
    df = pd.DataFrame(records)
    df.to_csv(csv_path, float_format="%.4f", index=False)

    lines = []
    lines.append("# Analysis 2 — Beta-Signs Sanity Check\n")
    lines.append(f"**Date:** {pd.Timestamp.now().date().isoformat()}  ")
    lines.append(f"**Pairs checked:** {len(df)}\n")

    if df.empty:
        lines.append("(No data)\n")
        md_path.write_text("\n".join(lines), encoding="utf-8")
        return

    # Aggregate match rate
    matches = df["matches_prior"].sum()
    total = df["matches_prior"].notna().sum()
    lines.append("## Summary\n")
    lines.append(f"- **Match rate:** {matches}/{total} ({matches/max(total,1)*100:.1f}%)\n")

    lines.append("## Mismatches\n")
    mism = df[df["matches_prior"] == False].sort_values("beta", key=lambda s: -s.abs())
    if mism.empty:
        lines.append("✅ All checked pairs match the naive prior sign.\n")
    else:
        lines.append("| Symbol | Sector | Factor | β | Expected | Actual |")
        lines.append("|---|---|---|---|---|---|")
        for _, r in mism.head(30).iterrows():
            lines.append(
                f"| `{r['symbol']}` | {r['sector']} | `{r['factor_id']}` | "
                f"{r['beta']:+.3f} | {r['expected_sign']} | {r['actual_sign']} |"
            )
        lines.append("")

    lines.append("## Note on interpretation\n")
    lines.append("Sign mismatches don't necessarily indicate a bug — they can mean:")
    lines.append("- The sector-prior is wrong (Tech became less rate-sensitive in 2023-2024)")
    lines.append("- The sample period was unusual (COVID era distorts everything)")
    lines.append("- The proxy ETF doesn't measure what its name suggests (see Analysis 5)")
    lines.append("- The factor is being residualized against a heavily-correlated earlier factor\n")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote: %s", md_path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--catalog", default=None)
    parser.add_argument("--asset-snapshot", default=None)
    parser.add_argument("--sector-map", default=None,
                        help="CSV with columns symbol,sector — overrides naive heuristic")
    parser.add_argument("--symbols", nargs="+", default=None)
    parser.add_argument("--output-suffix", default="beta-signs")
    args = parser.parse_args(argv)

    factor_snap = Path(args.snapshot) if args.snapshot else resolve_factor_snapshot()
    out_dir = report_output_dir(args.output_suffix)
    factor_returns = load_factor_returns(factor_snap, args.catalog)
    asset_snap = Path(args.asset_snapshot) if args.asset_snapshot else factor_snap
    asset_returns = load_returns(asset_snap)
    symbols = args.symbols or sorted(asset_returns.columns)

    sector_map = {}
    if args.sector_map:
        sm_df = pd.read_csv(args.sector_map)
        sector_map = dict(zip(sm_df["symbol"], sm_df["sector"]))

    records = []
    for sym in symbols:
        if sym not in asset_returns.columns:
            continue
        sector = sector_map.get(sym, "")
        betas = compute_unconditional_betas(asset_returns[sym], factor_returns)
        for factor_id, beta in betas.items():
            expected = None
            for (sec_substr, fid), exp_sign in SECTOR_FACTOR_PRIORS.items():
                if fid == factor_id and sec_substr.lower() in sector.lower():
                    expected = exp_sign
                    break
            actual = sign(beta)
            matches = (expected == actual) if expected else None
            records.append({
                "symbol": sym, "sector": sector, "factor_id": factor_id,
                "beta": beta, "expected_sign": expected,
                "actual_sign": actual, "matches_prior": matches,
            })

    write_report(records, out_dir)
    print(f"OK: {out_dir}/02_beta_signs.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
