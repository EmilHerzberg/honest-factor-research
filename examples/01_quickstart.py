"""15-minute quickstart: load data, run the trust-stratified analysis on
one asset, plot the result.

Prerequisites:
    pip install -e ".[notebooks]"
    python -m honest_factor_research.data.fetch --factors-only

Run:
    python examples/01_quickstart.py
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV

from honest_factor_research.analysis._common import resolve_factor_snapshot
from honest_factor_research.data.snapshot import load_returns
from honest_factor_research.returns.load import load_factor_catalog, load_factor_returns

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# 1. Load data
snap_path = resolve_factor_snapshot()
print(f"Loading factor returns from: {snap_path}")
catalog = load_factor_catalog()
factor_returns = load_factor_returns(snap_path)
asset_returns = load_returns(snap_path)
print(f"  -> {len(factor_returns.columns)} residualized factors over "
      f"{len(factor_returns)} trading days")

# 2. Pick an asset and run trust-stratified decomposition for one snapshot
SYMBOL = "AAPL" if "AAPL" in asset_returns.columns else asset_returns.columns[0]
WINDOW_END = pd.Timestamp("2024-06-28")  # mid-2024 snapshot

ar = asset_returns[SYMBOL].loc[asset_returns.index <= WINDOW_END].tail(252)
fr = factor_returns.loc[factor_returns.index <= WINDOW_END].tail(252)
joined = pd.concat([ar, fr], axis=1).dropna()
y = joined.iloc[:, 0].to_numpy()

direct_cols = [s.factor_id for s in catalog if s.klass == "DIRECT"]
stat_cols = [s.factor_id for s in catalog if s.klass == "STATISTICAL"]
derived_cols = [s.factor_id for s in catalog if s.klass == "DERIVED"]
# Promote market_beta to DIRECT for the trust analysis (SPY is unambiguous) —
# matches Analysis 6 (trust_stratified.py) and the single-stock explainer.
if "market_beta" in stat_cols:
    stat_cols.remove("market_beta")
    direct_cols.insert(0, "market_beta")

# Three regressions on the same window
def r2_for(cols):
    cols_present = [c for c in cols if c in joined.columns]
    if not cols_present:
        return 0.0
    m = RidgeCV(alphas=[0.01, 0.05, 0.1])
    m.fit(joined[cols_present].to_numpy(), y)
    return float(m.score(joined[cols_present].to_numpy(), y))

r2_direct = r2_for(direct_cols)
r2_stat = r2_for(direct_cols + stat_cols)
r2_total = r2_for(direct_cols + stat_cols + derived_cols)

print(f"\n=== Trust-Stratified R² for {SYMBOL} on {WINDOW_END.date()} ===")
print(f"r²_direct        = {r2_direct:.3f}  (DIRECT factors only)")
print(f"r²_+statistical  = {r2_stat:.3f}    (+ STATISTICAL — marginal +{r2_stat - r2_direct:.3f})")
print(f"r²_total         = {r2_total:.3f}   (+ DERIVED — marginal +{r2_total - r2_stat:.3f})")
print(f"derived_share    = {(r2_total - r2_stat) / max(r2_total, 0.01):.1%}")
print(f"idiosyncratic    = {1 - r2_total:.1%}")

# 3. Plot the decomposition
fig, ax = plt.subplots(figsize=(8, 4))
bars = ["DIRECT", "+ STATISTICAL", "+ DERIVED", "idiosyncratic"]
values = [r2_direct, r2_stat - r2_direct, r2_total - r2_stat, 1 - r2_total]
colors = ["#2ecc71", "#3498db", "#e67e22", "#95a5a6"]
ax.barh(bars, values, color=colors, edgecolor="black")
ax.set_xlim(0, 1)
ax.set_xlabel("Fraction of asset return variance")
ax.set_title(f"Trust-Stratified R² Decomposition\n{SYMBOL} — window ending {WINDOW_END.date()}")
ax.invert_yaxis()
for i, v in enumerate(values):
    ax.text(v + 0.01, i, f"{v:.3f}", va="center", fontsize=10)
plt.tight_layout()
out = Path("examples/01_quickstart_decomposition.png")
plt.savefig(out, dpi=120, bbox_inches="tight")
print(f"\nPlot saved: {out}")
