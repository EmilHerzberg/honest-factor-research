# Reports — Research Evidence

This directory contains the actual markdown + CSV outputs from running
the analysis pipeline. These are real research deliverables produced
during the V3.3 → V3.5 evolution of the methodology — kept here as
evidence of what the code actually produces and as reproducible artifacts.

## Layout

```
reports/
├── 2026-05-23-orthogonality-and-discovery/   # Initial 60-asset MVP analyses
│   ├── 01_factor_orthogonality.md           # Validates Gram-Schmidt
│   ├── 02_beta_signs.md                     # Sector-prior sanity check
│   ├── 03_residual_analysis.md              # Per-asset residual stats
│   ├── 04_index_discovery.md                # Univariate factor search
│   └── 06_trust_stratified_r2.md            # THE headline (V3.3)
│
├── 2026-05-24-v3.4-validation/               # V3.4 + Broad-Universe scale-up
│   ├── 05_index_purity.md                   # Alternative-proxy correlations
│   ├── 07_direct_factor_replacement.md      # V1→V2→V3 + Tier-1-3 candidates
│   ├── 08_broad_universe_replay.md          # 2,241 stocks; r²_direct collapse
│   ├── 08_per_sector_factor_relevance.csv   # Per-sector factor essentialness
│   ├── replacement_proxies.parquet          # Cached yfinance fetch (~3 MB)
│   └── 05_alt_proxies.parquet               # Cached alt proxies
│
└── 2026-05-25-v3.5-regime-and-ci/            # V3.5 regime + bootstrap features
    ├── 06_trust_stratified_r2.md            # Re-run after V3.4 — shows +23% r²_direct
    ├── 09_lead_lag.md                       # Asset[t+1] vs Factor[t] tests
    └── 10_conditional_betas.md              # 18.3% of pairs are regime-dependent
```

## How to use these reports

**As reference:** when implementing your own analysis, look at the
markdown reports to see what shape of output to expect.

**As evidence:** the headline findings in [`../README.md`](../README.md)
all link back to specific sections in these reports.

**As reproducibility check:** re-run the corresponding analysis
(e.g. `python -m honest_factor_research.analysis.trust_stratified`) and
diff the output. Today's data + today's yfinance state will give slightly
different numbers but the patterns should hold.

## Caveats

- Numbers in the reports are from runs against the bundled
  `data/factor_etfs_2026-05-21.parquet` snapshot. Re-running with fresh
  data will give slightly different numbers as the rolling-window
  contents shift.
- The 2024-12-31 endpoint is the latest snapshot covered. Analysis past
  that date requires extending the snapshot via
  `python -m honest_factor_research.data.fetch`.
- Reports that ran against the broad-universe (Analysis 8) require the
  `broad_universe_ohlcv_*.parquet` file, which is gitignored due to size.
  Run `python -m honest_factor_research.data.fetch` to recreate (~10 min,
  ~50 MB).
