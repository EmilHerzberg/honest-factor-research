"""Single-stock explainer CLI.

Takes one US-listed ticker and runs the trust-stratified decomposition
for the latest snapshot in the bundled data. Output is designed to be
readable for non-quants:

  - Standard R² (the "looks-good" number)
  - Honest direct R² (real-world-priced factors only)
  - Statistical-style contribution (academic style factors)
  - Derived / sector-mirror contribution (where mirror artifacts hide)
  - Unexplained / idiosyncratic share
  - A short, plain-English interpretation tailored to the values

Usage:
    python examples/03_explain_single_stock.py --ticker AAPL
    python examples/03_explain_single_stock.py --ticker XOM --window-end 2024-06-28

If the requested ticker isn't in the bundled sample data, the script
falls back to listing what IS available — so you can re-run with a valid
symbol.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date

import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV

from honest_factor_research.analysis._common import resolve_factor_snapshot
from honest_factor_research.data.snapshot import load_returns
from honest_factor_research.returns.load import load_factor_catalog, load_factor_returns


def fit_r2(X: np.ndarray, y: np.ndarray) -> float:
    if X.shape[1] == 0 or X.shape[0] < X.shape[1] + 5:
        return float("nan")
    try:
        model = RidgeCV(alphas=[0.01, 0.05, 0.1])
        model.fit(X, y)
        return float(model.score(X, y))
    except Exception:
        return float("nan")


def interpret(r2_direct: float, r2_stat: float, r2_total: float) -> str:
    """Return a one-paragraph plain-English interpretation."""
    idio = 1 - r2_total
    derived_share = (r2_total - r2_stat) / max(r2_total, 0.01)

    parts = []
    if r2_direct >= 0.35:
        parts.append(
            "This stock is **genuinely well-explained** by direct real-world "
            "factors (rates, oil, VIX, credit spreads). The model can be "
            "trusted with reasonable confidence."
        )
    elif r2_direct >= 0.20:
        parts.append(
            "Direct macro factors explain a moderate share. The model has "
            "real grip on this stock but isn't telling the full story."
        )
    else:
        parts.append(
            "Direct macro factors explain very little. Most of the apparent "
            "R² comes from style or sector factors — be cautious about "
            "treating the model output as 'high confidence'."
        )

    if derived_share >= 0.40:
        parts.append(
            f"**About {derived_share:.0%} of the explained variance comes "
            "from sector-basket factors.** That's a mirror-artifact warning: "
            "if this stock is itself a major constituent of one of those "
            "baskets, the model is partly explaining the stock with itself."
        )
    elif derived_share >= 0.20:
        parts.append(
            f"Sector baskets contribute about {derived_share:.0%} of the "
            "explanation — moderate, not alarming."
        )
    else:
        parts.append(
            "Sector baskets contribute little additional explanation — "
            "the model isn't mirror-driven for this stock."
        )

    if idio >= 0.60:
        parts.append(
            f"About {idio:.0%} of this stock's variance is idiosyncratic — "
            "stock-specific noise that the factor model doesn't capture. "
            "That's typical for less-correlated mid/small caps."
        )

    return " ".join(parts)


def explain(ticker: str, window_end: date, snapshot_path) -> int:
    logging.basicConfig(level=logging.WARNING, format="%(message)s")
    logger = logging.getLogger(__name__)

    catalog = load_factor_catalog()
    factor_returns = load_factor_returns(snapshot_path)
    asset_returns = load_returns(snapshot_path)

    if ticker not in asset_returns.columns:
        print(f"\nTicker {ticker!r} is not in the bundled sample data.\n")
        print("Available tickers (first 30):")
        available = sorted(asset_returns.columns)
        for chunk_start in range(0, min(30, len(available)), 10):
            print("  " + ", ".join(available[chunk_start:chunk_start + 10]))
        print(f"\nTotal available: {len(available)}. To use a different "
              "ticker, fetch fresh data:")
        print("  python -m honest_factor_research.data.fetch")
        return 1

    ts = pd.Timestamp(window_end)
    ar = asset_returns[ticker].loc[asset_returns.index <= ts].tail(252)
    fr = factor_returns.loc[factor_returns.index <= ts].tail(252)
    joined = pd.concat([ar, fr], axis=1).dropna()
    if len(joined) < 240:
        print(f"\nInsufficient history for {ticker} at {window_end}: only "
              f"{len(joined)} aligned days (need ~252).\n")
        return 1
    y = joined.iloc[:, 0].to_numpy()

    direct_cols = [s.factor_id for s in catalog if s.klass == "DIRECT"]
    stat_cols = [s.factor_id for s in catalog if s.klass == "STATISTICAL"]
    derived_cols = [s.factor_id for s in catalog if s.klass == "DERIVED"]
    # Promote market_beta to DIRECT for the trust analysis (SPY is unambiguous)
    if "market_beta" in stat_cols:
        stat_cols.remove("market_beta")
        direct_cols.insert(0, "market_beta")

    def r2_for(cols):
        present = [c for c in cols if c in joined.columns]
        if not present:
            return 0.0
        return fit_r2(joined[present].to_numpy(), y)

    r2_direct = r2_for(direct_cols)
    r2_stat = r2_for(direct_cols + stat_cols)
    r2_total = r2_for(direct_cols + stat_cols + derived_cols)
    derived_share = (r2_total - r2_stat) / max(r2_total, 0.01)
    idio = 1 - r2_total

    print()
    print(f"{'=' * 60}")
    print(f"Honest Factor Research — Single-Stock Explainer")
    print(f"{'=' * 60}")
    print(f"Symbol     : {ticker}")
    print(f"Window-end : {window_end}  (252-day rolling window)")
    print(f"Aligned obs: {len(joined)}")
    print()
    print(f"Standard R² (point estimate)         : {r2_total:.3f}")
    print(f"Honest / Direct R²                   : {r2_direct:.3f}   <- trust this")
    print(f"Statistical-style component          : +{(r2_stat - r2_direct):.3f}  (value/growth/momentum/quality)")
    print(f"Derived / Sector-mirror component    : +{(r2_total - r2_stat):.3f}  (XL* sector baskets, themes)")
    print(f"Unexplained / idiosyncratic          : {idio:.1%}")
    print(f"Derived-share of total R²            : {derived_share:.1%}")
    print()
    print("Interpretation")
    print("-" * 60)
    text = interpret(r2_direct, r2_stat, r2_total)
    # Wrap to 60 chars
    import textwrap
    print("\n".join(textwrap.wrap(text, width=60)))
    print()
    print(f"Source factors used:")
    print(f"  DIRECT      ({len(direct_cols)}): {', '.join(direct_cols)}")
    print(f"  STATISTICAL ({len(stat_cols)}): {', '.join(stat_cols)}")
    print(f"  DERIVED     ({len(derived_cols)}): {', '.join(derived_cols[:6])}, ...")
    print()
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Single-stock honest-factor-research explainer.",
    )
    parser.add_argument(
        "--ticker", "-t", required=True,
        help="US-listed ticker symbol (e.g. AAPL, XOM, JPM)",
    )
    parser.add_argument(
        "--window-end", "-e", default="2024-06-28",
        help="Window-end date YYYY-MM-DD (default 2024-06-28)",
    )
    parser.add_argument(
        "--snapshot", default=None,
        help="Override factor-ETFs snapshot path",
    )
    args = parser.parse_args(argv)

    snap = resolve_factor_snapshot() if args.snapshot is None else args.snapshot
    try:
        window_end = date.fromisoformat(args.window_end)
    except ValueError:
        print(f"Invalid date: {args.window_end!r}. Use YYYY-MM-DD.")
        return 2

    return explain(args.ticker.upper(), window_end, snap)


if __name__ == "__main__":
    sys.exit(main())
