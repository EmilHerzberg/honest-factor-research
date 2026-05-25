"""Analysis 5 — Index-Purity Test.

Per factor in the catalog, fetches 1-3 ALTERNATIVE ETFs that should measure
the same concept (e.g. ``value: IWD-Russell`` vs ``VLUE-MSCI`` vs ``IUSV-S&P``
vs ``RPV-S&P-Pure-Value``). Tests their pairwise correlation. If the
alternatives don't agree (ρ < 0.90), our specific ETF choice is itself a
methodological factor — not just "value", but specifically "Russell-value
methodology".

Real-world finding: this analysis showed that XLV (Healthcare Select) has
ρ=0.76 with IBB (Biotech only) — they're measuring genuinely different
things, despite both being labeled "healthcare". XLV is 10% UnitedHealth
(a health insurer), so it's really "healthcare ex-pure-biotech".
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from honest_factor_research.analysis._common import (
    DEFAULT_DATA_DIR,
    report_output_dir,
    resolve_factor_snapshot,
    setup_logging,
)
from honest_factor_research.data.fetch import fetch_one_ticker
from honest_factor_research.data.snapshot import long_to_wide_close, load_snapshot, to_log_returns

logger = setup_logging("analysis.05_index_purity")


# Maps each factor_id → (current proxy ETF, list of alternative ETFs with description)
FACTOR_ALTERNATIVES: dict[str, dict] = {
    "market_beta": {
        "current": "SPY",
        "alternatives": [("VTI", "Vanguard Total US"), ("IWB", "Russell 1000"), ("ITOT", "iShares Total")],
    },
    "rates": {
        "current": "IEF",
        "alternatives": [("VGIT", "Vanguard Interm. Treasury"), ("GOVT", "iShares US Treasury Broad")],
    },
    "value": {
        "current": "IWD",
        "alternatives": [("VLUE", "MSCI USA Value"), ("IUSV", "Core S&P Value"), ("RPV", "S&P Pure Value")],
    },
    "growth": {
        "current": "IWF",
        "alternatives": [("SCHG", "Schwab Large-Cap Growth"), ("VONG", "Vanguard Russell 1000 Growth")],
    },
    "momentum": {
        "current": "MTUM",
        "alternatives": [("SPMO", "S&P 500 Momentum"), ("PDP", "Invesco DWA Momentum")],
    },
    "quality": {
        "current": "QUAL",
        "alternatives": [("SPHQ", "S&P 500 Quality"), ("FQAL", "Fidelity Quality")],
    },
    "semiconductors": {
        "current": "SOXX",
        "alternatives": [("SMH", "VanEck Semis"), ("PSI", "Invesco Dynamic Semis")],
    },
    "xl_financials": {
        "current": "XLF",
        "alternatives": [("VFH", "Vanguard Financials"), ("KBE", "SPDR Bank")],
    },
    "xl_healthcare": {
        "current": "XLV",
        "alternatives": [("VHT", "Vanguard Healthcare"), ("IBB", "iShares Biotech"), ("IHI", "iShares Medical Devices")],
    },
    "xl_industrials": {
        "current": "XLI",
        "alternatives": [("VIS", "Vanguard Industrials"), ("ITA", "iShares Defense")],
    },
    "xl_utilities": {
        "current": "XLU",
        "alternatives": [("VPU", "Vanguard Utilities"), ("IDU", "iShares Utilities")],
    },
    "xl_real_estate": {
        "current": "XLRE",
        "alternatives": [("VNQ", "Vanguard REIT"), ("IYR", "iShares Real Estate")],
    },
    "china_exposure": {
        "current": "FXI",
        "alternatives": [("MCHI", "MSCI China"), ("ASHR", "CSI 300 A-Shares"), ("KWEB", "China Internet")],
    },
}


def fetch_alternatives_cache(cache_path: Path, start: datetime, end: datetime) -> pd.DataFrame:
    """Fetch all alt-proxy ETFs via yfinance, cache as parquet."""
    all_syms = set()
    for cfg in FACTOR_ALTERNATIVES.values():
        for sym, _label in cfg["alternatives"]:
            all_syms.add(sym)

    existing = pd.read_parquet(cache_path) if cache_path.exists() else pd.DataFrame()
    have = set(existing["symbol"].unique()) if not existing.empty else set()
    missing = sorted(all_syms - have)
    if missing:
        logger.info("Fetching %d alt-proxies: %s", len(missing), missing[:10])
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


def compute_purity(factor_id: str, log_ret: pd.DataFrame) -> dict | None:
    """Compute correlations between current proxy and alternatives."""
    cfg = FACTOR_ALTERNATIVES.get(factor_id)
    if cfg is None:
        return None
    current = cfg["current"]
    if current not in log_ret.columns:
        return None
    cols = [current] + [sym for sym, _ in cfg["alternatives"] if sym in log_ret.columns]
    if len(cols) < 2:
        return None
    sub = log_ret[cols].dropna()
    if len(sub) < 200:
        return None
    corr = sub.corr(method="pearson")
    rhos = {alt: float(corr.loc[alt, current]) for alt in cols[1:]}
    min_rho = min(rhos.values())
    if min_rho >= 0.95:
        verdict = "🟢 robust"
    elif min_rho >= 0.90:
        verdict = "🟡 mostly_same"
    elif min_rho >= 0.80:
        verdict = "🟠 different_proxy"
    else:
        verdict = "🔴 fundamentally_different"
    return {
        "factor_id": factor_id,
        "current": current,
        "n_obs": len(sub),
        "rhos": rhos,
        "min_rho": min_rho,
        "verdict": verdict,
    }


def write_report(results: list[dict], out_dir: Path) -> None:
    md_path = out_dir / "05_index_purity.md"
    csv_path = out_dir / "05_index_purity.csv"
    rows = []
    for r in results:
        for alt, rho in r["rhos"].items():
            rows.append({"factor_id": r["factor_id"], "current": r["current"],
                         "alternative": alt, "rho": rho, "verdict": r["verdict"]})
    pd.DataFrame(rows).to_csv(csv_path, float_format="%.4f", index=False)

    lines = []
    lines.append("# Analysis 5 — Index-Purity Test\n")
    lines.append(f"**Date:** {pd.Timestamp.now().date().isoformat()}  ")
    lines.append(f"**Factors tested:** {len(results)}\n")

    lines.append("## Verdict counts\n")
    from collections import Counter
    counts = Counter(r["verdict"] for r in results)
    for v, n in sorted(counts.items()):
        lines.append(f"- {v}: **{n}**")
    lines.append("")

    lines.append("## Per-factor detail (sorted by lowest ρ)\n")
    for r in sorted(results, key=lambda r: r["min_rho"]):
        lines.append(f"### {r['verdict']} `{r['factor_id']}` (current: `{r['current']}`)\n")
        lines.append(f"**Min ρ across alternatives:** {r['min_rho']:+.4f} "
                     f"(N={r['n_obs']} trading-days)\n")
        lines.append("| Alternative | ρ to current |")
        lines.append("|---|---|")
        for alt, rho in sorted(r["rhos"].items(), key=lambda x: x[1]):
            lines.append(f"| `{alt}` | {rho:+.4f} |")
        lines.append("")

    lines.append("## How to interpret\n")
    lines.append("- 🟢 **robust** (ρ ≥ 0.95): methodologies agree; the factor concept is well-defined")
    lines.append("- 🟡 **mostly_same** (0.90-0.95): minor methodology bias, but same factor")
    lines.append("- 🟠 **different_proxy** (0.80-0.90): your ETF choice IS a methodological factor")
    lines.append("- 🔴 **fundamentally_different** (< 0.80): your proxy measures something the ")
    lines.append("  alternative doesn't — be very explicit about what you're modeling.\n")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote: %s", md_path)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--start", default="2020-01-01")
    parser.add_argument("--end", default="2024-12-31")
    parser.add_argument("--output-suffix", default="index-purity")
    args = parser.parse_args(argv)

    snap = Path(args.snapshot) if args.snapshot else resolve_factor_snapshot()
    out_dir = report_output_dir(args.output_suffix)
    base = load_snapshot(snap)
    base_wide = long_to_wide_close(base)

    start = datetime.strptime(args.start, "%Y-%m-%d")
    end = datetime.strptime(args.end, "%Y-%m-%d")
    cache_path = DEFAULT_DATA_DIR / "cache" / "alt_proxies.parquet"
    alt_df = fetch_alternatives_cache(cache_path, start, end)
    alt_wide = long_to_wide_close(alt_df)
    # Merge without duplicates
    new_uniq = alt_wide[[c for c in alt_wide.columns if c not in base_wide.columns]]
    combined = base_wide.join(new_uniq, how="outer").sort_index()
    log_ret = to_log_returns(combined)

    results = []
    for factor_id in FACTOR_ALTERNATIVES:
        r = compute_purity(factor_id, log_ret)
        if r is not None:
            logger.info("%s: %s min_rho=%.3f", factor_id, r["verdict"], r["min_rho"])
            results.append(r)

    write_report(results, out_dir)
    print(f"OK: {out_dir}/05_index_purity.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
