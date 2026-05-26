# Analysis 6 — Trust-Stratified R² Decomposition

**Date:** 2026-05-26  
**Method:** three separate RidgeCV regressions per asset×snapshot  
**Window:** 252 trading-days  
**Factors:** 11 DIRECT, 4 STATISTICAL, 13 DERIVED_THEME

## Classification

- **DIRECT** (11): `market_beta`, `copper`, `credit_hy_spread`, `energy_oil`, `gold`, `inflation`, `natural_gas`, `rates`, `rates_30y`, `usd_strength`, `volatility`
- **STATISTICAL** (4): `momentum`, `quality`, `value`, `growth`
- **DERIVED_THEME** (13): `biotech`, `defense`, `lithium`, `semiconductors`, `uranium`, `xl_consumer_defensive`, `xl_financials`, `xl_healthcare`, `xl_industrials`, `xl_real_estate`, `xl_utilities`, `china_a_shares`, `china_exposure`

## Summary

- **2758 assets** analyzed
- Mean r²_direct: **0.253**
- Mean r²_+statistical: 0.282
- Mean r²_total: 0.352
- Mean derived_share: **21.0%**

## Tier Reclassification (OLD r²_total based → NEW trust-stratified)

| Tier change | Count |
|---|---|
| HIGH → HIGH | 106 |
| HIGH → LOW | 11  ⚠️  Downgrade |
| HIGH → MED_DERIVED_HEAVY | 14  ⚠️  Downgrade |
| LOW → LOW | 973  ⚠️  Downgrade |
| MED → HIGH | 441 |
| MED → LOW | 1189  ⚠️  Downgrade |
| MED → MED_DERIVED_HEAVY | 24  ⚠️  Downgrade |

## Top-15 by r²_direct (highest DIRECT-trust)

| Symbol | r²_direct | r²_+stat | r²_total | derived_share | NEW Tier |
|---|---|---|---|---|---|
| `GDV` | 0.685 | 0.697 | 0.719 | 3.0% | HIGH |
| `TY` | 0.681 | 0.685 | 0.705 | 2.8% | HIGH |
| `CII` | 0.668 | 0.672 | 0.692 | 2.9% | HIGH |
| `CSQ` | 0.661 | 0.668 | 0.693 | 3.6% | HIGH |
| `ECAT` | 0.645 | 0.651 | 0.671 | 2.9% | HIGH |
| `MSFT` | 0.637 | 0.699 | 0.717 | 2.5% | HIGH |
| `NIE` | 0.627 | 0.642 | 0.669 | 4.0% | HIGH |
| `GAM` | 0.625 | 0.630 | 0.652 | 3.4% | HIGH |
| `RVT` | 0.614 | 0.638 | 0.691 | 7.7% | HIGH |
| `APH` | 0.599 | 0.613 | 0.662 | 7.4% | HIGH |
| `BLK` | 0.589 | 0.603 | 0.654 | 7.7% | HIGH |
| `AMP` | 0.587 | 0.621 | 0.685 | 9.4% | HIGH |
| `BTX` | 0.581 | 0.634 | 0.697 | 9.1% | HIGH |
| `RMT` | 0.577 | 0.607 | 0.679 | 10.6% | HIGH |
| `BDJ` | 0.575 | 0.591 | 0.617 | 4.2% | HIGH |

## Bottom-15 by r²_direct

| Symbol | r²_direct | r²_+stat | r²_total | derived_share | NEW Tier |
|---|---|---|---|---|---|
| `BULL` | 0.014 | 0.014 | 0.036 | 59.8% | LOW |
| `PSIX` | 0.013 | 0.016 | 0.029 | 45.8% | LOW |
| `CCNEP` | 0.013 | 0.014 | 0.027 | 47.8% | LOW |
| `OCCIN` | 0.013 | 0.013 | 0.032 | 58.1% | LOW |
| `AIRJ` | 0.013 | 0.013 | 0.030 | 55.4% | LOW |
| `SAJ` | 0.011 | 0.014 | 0.026 | 46.8% | LOW |
| `GEGGL` | 0.011 | 0.014 | 0.056 | 75.2% | LOW |
| `NVCT` | 0.011 | 0.012 | 0.042 | 70.5% | LOW |
| `SAY` | 0.009 | 0.010 | 0.029 | 64.7% | LOW |
| `WHFCL` | 0.008 | 0.009 | 0.021 | 58.5% | LOW |
| `TRON` | 0.007 | 0.008 | 0.019 | 55.6% | LOW |
| `OFSSH` | 0.007 | 0.008 | 0.022 | 65.3% | LOW |
| `USAR` | 0.006 | 0.009 | 0.035 | 73.5% | LOW |
| `SWKHL` | 0.006 | 0.006 | 0.022 | 70.5% | LOW |
| `NEWTI` | 0.005 | 0.006 | 0.035 | 82.4% | LOW |

## Top-15 by derived_share (highest DERIVED-dependency, mirror-suspect)

| Symbol | derived_share | r²_total | r²_+stat | marginal_derived | OLD → NEW |
|---|---|---|---|---|---|
| `NEWTI` | 82.4% | 0.035 | 0.006 | +0.029 | LOW → LOW |
| `GEGGL` | 75.2% | 0.056 | 0.014 | +0.042 | LOW → LOW |
| `USAR` | 73.5% | 0.035 | 0.009 | +0.026 | LOW → LOW |
| `SWKHL` | 70.5% | 0.022 | 0.006 | +0.015 | LOW → LOW |
| `NVCT` | 70.5% | 0.042 | 0.012 | +0.029 | LOW → LOW |
| `AMPX` | 69.8% | 0.107 | 0.032 | +0.075 | LOW → LOW |
| `OXSQG` | 67.5% | 0.085 | 0.028 | +0.058 | LOW → LOW |
| `OFSSH` | 65.3% | 0.022 | 0.008 | +0.015 | LOW → LOW |
| `NUAI` | 65.1% | 0.059 | 0.021 | +0.038 | LOW → LOW |
| `SAY` | 64.7% | 0.029 | 0.010 | +0.018 | LOW → LOW |
| `OKLO` | 63.6% | 0.056 | 0.020 | +0.035 | LOW → LOW |
| `CLYM` | 61.6% | 0.059 | 0.023 | +0.037 | LOW → LOW |
| `BGS` | 61.3% | 0.170 | 0.066 | +0.104 | LOW → LOW |
| `BULL` | 59.8% | 0.036 | 0.014 | +0.022 | LOW → LOW |
| `WHFCL` | 58.5% | 0.021 | 0.009 | +0.012 | LOW → LOW |

## Interpretation

- **r²_direct** = explanation from DIRECT-physical factors only (rates, inflation, VIX-spot, etc.)
- **r²_+statistical** = + academic style factors (value, momentum, quality)
- **r²_total** = + heterogeneous sector baskets (XLF, XLV, etc.)
- **derived_share** = fraction of R² that COULD be mirror artifact

Honest statement per asset: r²_direct% sure-explained, marginal_statistical% half-explained, marginal_derived% mirror-suspect, (1−r²_total)% idiosyncratic.
