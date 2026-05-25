# Honest Factor Research

> Empirical research on the limits of factor models for US equities — and a
> methodology for distinguishing real explanation from mirror artifacts.

A standalone Python package + reports + notebooks documenting a multi-week
factor-research project on US equities (S&P 500 + broad universe of 2,241
top-market-cap US stocks). Built with pandas + scikit-learn + yfinance —
fully reproducible, no paid data feeds.

## TL;DR — Four Findings That Changed The Model

Backed by empirical results on 2,241 US stocks (2020-2024 daily data, ~5M
OHLCV rows):

### 1. 53% of asset quality tiers were overstated in a "standard" factor model

When you decompose R² into three trust tiers
(`r²_direct` / `r²_+statistical` / `r²_total`), most assets fall in tier
significantly. Energy stocks scoring R²=0.75 in a standard
multi-factor regression turn out to be **55% mirror artifacts** of their
own sector ETF (XOM is 22% of XLE). See
[`docs/03-trust-stratified-r2.md`](docs/03-trust-stratified-r2.md).

### 2. 18.3% of asset-factor pairs have regime-dependent beta

Static beta is a mean across regimes — in any specific regime it can be
substantially wrong. Worst case found: **GE × value flips from +2.94
(high-VIX) to -0.15 (low-VIX)**, a sign reversal. See
[`docs/05-regime-switching.md`](docs/05-regime-switching.md).

### 3. Lithium > Gold as a universal factor (counterintuitive)

Broad-universe replay of 12 commodity/macro factor candidates showed:
- Lithium (LIT ETF): mean Δr²=+0.010, 34 assets with Δr²≥0.05
- Gold (GLD ETF): mean Δr²=+0.005, 6 assets
- Theory said Gold was essential. Empirics disagree. See
  [`reports/2026-05-24/07_direct_factor_replacement.md`](reports/2026-05-24/07_direct_factor_replacement.md).

### 4. Block-bootstrap CIs reveal which R² values you should actually trust

Replacing point R² with a Politis-Romano stationary-block-bootstrap 90% CI:
- WMT 2021-02-26: R²=0.64 with CI **[0.39, 0.82]** → 0.43 spread = unreliable
  (window contains the COVID-crash period)
- AAPL 2023-06: R²=0.62 with CI **[0.59, 0.65]** → 0.06 spread = trustworthy

The CI width quantifies fat-tail-driven uncertainty without distributional
assumptions. See [`docs/06-fat-tails-mitigation.md`](docs/06-fat-tails-mitigation.md).

## What's Novel

**Trust-stratified R² decomposition.** Instead of reporting a single R² per
asset, decompose into three classes of factors:

```
r²_direct         = real-world-priced factors only
                    (market_beta, rates, inflation, VIX-spot, Brent, gold-spot...)
r²_+statistical   = + academic style factors
                    (value, growth, momentum, quality)
r²_total          = + sector basket factors
                    (XLF, XLV, semiconductors, ...)
1 − r²_total      = honest idiosyncratic variance
```

The gap `r²_total − r²_+statistical` is the **DERIVED-share** — explanation
that comes from sector baskets, which (for stocks that ARE in those baskets)
may largely be the asset modeling itself. The model-honesty principle:
prefer a lower honest `r²_direct` over a higher `r²_total` that's mostly
mirror.

## Quick Start

```bash
git clone https://github.com/EmilHerzberg/honest-factor-research
cd honest-factor-research
pip install -e ".[dev,notebooks]"

# Fetch sample factor-ETF data (4 MB, takes ~2 min)
python -m honest_factor_research.data.fetch --factors-only

# Run the headline analysis
python examples/02_trust_stratified.py

# Or interactive walkthrough
jupyter notebook notebooks/01_quickstart.ipynb
```

## What's Inside

### The 10 Research Scripts

| Script | What it does |
|---|---|
| `01_orthogonality` | Validates Gram-Schmidt residualization with correlation matrix + heatmap |
| `02_beta_signs` | Sanity-check actual vs expected betas per sector |
| `03_residuals` | Per-asset residual statistics (kurtosis, outliers, max-σ) |
| `04_index_discovery` | Univariate OLS of N assets × M index candidates — finds missing factors |
| `05_index_purity` | **Original method:** test if your factor-ETF measures what its name claims |
| `06_trust_stratified` | **The headline:** R² decomposition into DIRECT/STATISTICAL/DERIVED |
| `07_replacement_test` | V1→V2→V3 + Tier 1-3 factor candidate marginal-Δr² tests |
| `08_broad_universe` | Scale-up to 2,241 stocks with multiprocessing |
| `09_lead_lag` | Asset[t+1] regressed on Factor[t] for price-discovery violations |
| `10_conditional_betas` | Regime-stratified beta (VIX / Rates / Bull-Bear) |

### The Pipeline (~600 lines)

`honest_factor_research/exposure/pipeline.py`:
- Rolling RidgeCV with 252-day windows
- Stationary block-bootstrap for both beta-stderr AND R²-CI
- VIX-stratified regime-switching beta computation
- Sector-conditional factor loading (Mitigation 2G from `docs/04-sector-conditional.md`)

### The Reports as Evidence

`reports/2026-05-{23,24,25}/` contains the actual markdown + CSV outputs
from running this pipeline. These are real research deliverables, not toy
results — feel free to reproduce or extend.

## Methodology in One Sentence

**Test every factor proposal empirically via marginal-Δr² against a broad
universe (>1,000 stocks) before adding it; classify it as DIRECT /
STATISTICAL / DERIVED; track regime-dependence; report R² as a confidence
interval, not a point — and prefer lower-but-honest explanation over
higher-but-mirror-driven.**

Full methodology in [`METHODOLOGY.md`](METHODOLOGY.md).

## Documentation

- [`METHODOLOGY.md`](METHODOLOGY.md) — the model-honesty principle in detail
- [`docs/02-factor-taxonomy.md`](docs/02-factor-taxonomy.md) — DIRECT/STATISTICAL/DERIVED classification of all factors used
- [`docs/03-trust-stratified-r2.md`](docs/03-trust-stratified-r2.md) — the headline finding methodology
- [`docs/04-sector-conditional.md`](docs/04-sector-conditional.md) — Mitigation 2G architecture
- [`docs/05-regime-switching.md`](docs/05-regime-switching.md) — VIX-stratified betas
- [`docs/06-fat-tails-mitigation.md`](docs/06-fat-tails-mitigation.md) — block-bootstrap CI for R²
- [`docs/risks-and-improvements.md`](docs/risks-and-improvements.md) — living risk register (7 documented risks)
- [`docs/future-investigations.md`](docs/future-investigations.md) — 10 open questions

## Reproducibility

Everything in this repo is reproducible with free data:
- **yfinance** for OHLCV (covered by their TOS for research use)
- **NASDAQ-Screener API** for broad-universe constituents (public endpoint)
- No paid data sources, no proprietary calibration

`examples/reproduce_findings.py` runs the full pipeline end-to-end (~1 hour
on 8 cores, mostly the broad-universe replay).

## Limitations

Be honest about the limitations:

- **Survivorship bias**: the broad-universe constituents are *today's*
  NASDAQ-screener output. Delisted stocks (Lehman, SVB, Bed Bath & Beyond)
  are missing. Mentioned in
  [`docs/future-investigations.md#i-007`](docs/future-investigations.md).
- **Period 2020-2024**: heavy COVID + post-COVID monetary-policy regime —
  may not generalize to 1990s-style cycles.
- **No trading-signal validation**: this is *exposure* research, not a
  strategy backtest. R² improvements don't directly translate to alpha.
- **yfinance data quality**: occasionally has bad ticks for small-caps;
  see `docs/future-investigations.md#i-010`.

## License

MIT (see [`LICENSE`](LICENSE)). The research findings, code, and methodology
are released for educational and research purposes — **not investment
advice**.

## Citation

If this research informs your work, citation would be appreciated:

```
Herzberg, E. (2026). Honest Factor Research: Trust-Stratified R²,
Regime-Switching Betas, and Block-Bootstrap CIs for US Equity Factor Models.
GitHub: EmilHerzberg/honest-factor-research
```

## Contributing

Open issues for:
- Reproducibility problems (please include OS / Python / package versions)
- Conceptual questions about the methodology
- Suggested improvements to the documentation

Substantial extensions (new factors, new regimes, alternative bootstrap
schemes) very welcome via PR — but please open an issue first to align on
scope.
