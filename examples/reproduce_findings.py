"""Run ALL 10 analysis scripts end-to-end (reproduces the headline findings).

Wall-clock: ~1 hour on 8 cores. Most time is in Analysis 8 (broad-universe
replay across 2,241 assets with multiprocessing).

Prerequisites:
    pip install -e ".[notebooks]"
    python -m honest_factor_research.data.fetch                 # broad universe, ~10 min
    python -m honest_factor_research.data.fetch --factors-only  # if you only want factor ETFs

Run:
    python examples/reproduce_findings.py
"""

from __future__ import annotations

import logging

from honest_factor_research.analysis import (
    beta_signs,
    broad_universe,
    conditional_betas,
    index_discovery,
    index_purity,
    lead_lag,
    orthogonality,
    replacement_test,
    residuals,
    trust_stratified,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

print("=== Analysis 1: Factor Orthogonality ===")
orthogonality.main([])

print("\n=== Analysis 2: Beta Signs ===")
beta_signs.main([])

print("\n=== Analysis 3: Residual Statistics ===")
residuals.main([])

print("\n=== Analysis 4: Univariate Index Discovery ===")
index_discovery.main([])

print("\n=== Analysis 5: Index Purity ===")
index_purity.main([])

print("\n=== Analysis 6: Trust-Stratified R² ===")
trust_stratified.main([])

print("\n=== Analysis 7: Replacement Test ===")
replacement_test.main([])

print("\n=== Analysis 8: Broad-Universe Replay (slow!) ===")
broad_universe.main([])

print("\n=== Analysis 9: Lead-Lag Test ===")
lead_lag.main([])

print("\n=== Analysis 10: Conditional Betas ===")
conditional_betas.main([])

print("\nDone. Reports under reports/<today>-* subdirectories.")
