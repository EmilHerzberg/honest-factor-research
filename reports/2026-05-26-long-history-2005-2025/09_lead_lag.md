# Analysis 9 — Lead-Lag-Test (Asset[t+1] vs Factor[t])

**Date:** 2026-05-26  
**Pairs analyzed:** 77224

## Global lead-t-stat distribution

- Mean |t_lead|: 1.270
- Median: 0.977
- p95: 3.383
- Pairs with |t_lead| ≥ 3: 5685 (7.4%)

## Top-20 Lead-Lag suspicious pairs (|t_lead| ≥ 3)

| Asset | Factor | Lead β | Lead t | Contemp β | Contemp t |
|---|---|---|---|---|---|
| `PRK` | `market_beta` | -0.3966 | -15.01 | +1.2198 | +57.78 |
| `LKFN` | `market_beta` | -0.3665 | -14.99 | +0.9738 | +46.23 |
| `THFF` | `market_beta` | -0.3712 | -14.77 | +1.1321 | +55.56 |
| `DGICA` | `market_beta` | -0.3309 | -14.43 | +0.8206 | +40.06 |
| `WTBA` | `market_beta` | -0.4678 | -14.40 | +1.2859 | +45.93 |
| `AROW` | `market_beta` | -0.3286 | -14.16 | +0.9660 | +49.42 |
| `CTBI` | `market_beta` | -0.3131 | -13.88 | +1.0249 | +56.57 |
| `CCBG` | `market_beta` | -0.3975 | -13.83 | +1.0947 | +43.67 |
| `BUSE` | `market_beta` | -0.3742 | -13.79 | +1.1627 | +51.66 |
| `WASH` | `market_beta` | -0.3442 | -13.41 | +1.1277 | +53.74 |
| `SYBT` | `market_beta` | -0.3236 | -13.12 | +1.0978 | +54.89 |
| `ADC` | `market_beta` | -0.3245 | -13.10 | +0.9555 | +44.53 |
| `CZNC` | `market_beta` | -0.3656 | -13.05 | +0.9492 | +37.54 |
| `TMP` | `market_beta` | -0.3097 | -12.92 | +0.9780 | +48.25 |
| `SRCE` | `market_beta` | -0.3639 | -12.90 | +1.2389 | +53.80 |
| `WEYS` | `market_beta` | -0.3674 | -12.74 | +1.0158 | +39.49 |
| `PEBO` | `market_beta` | -0.3677 | -12.45 | +1.2814 | +52.91 |
| `SFNC` | `market_beta` | -0.3242 | -12.43 | +1.1635 | +55.29 |
| `O` | `market_beta` | -0.2738 | -12.42 | +0.9636 | +53.49 |
| `FFIN` | `market_beta` | -0.2794 | -12.36 | +1.0396 | +58.09 |

## Top-15 Reverse-Lead (Asset leads Factor, |t_lag| ≥ 3)

These are price-discovery leaders — the asset is large enough in the index 
that its moves anticipate the index.

| Asset | Factor | Lag β | Lag t |
|---|---|---|---|
| `MGR` | `usd_strength` | -0.8561 | -11.76 |
| `BTZ` | `inflation` | +0.7690 | +11.74 |
| `BGR` | `inflation` | +1.0455 | +11.25 |
| `MS` | `inflation` | +1.5704 | +11.12 |
| `OIS` | `inflation` | +1.8774 | +10.72 |
| `NOV` | `inflation` | +1.5467 | +10.43 |
| `ARCC` | `inflation` | +1.0639 | +10.41 |
| `RS` | `inflation` | +1.2717 | +10.38 |
| `COP` | `inflation` | +1.1176 | +10.28 |
| `EPD` | `inflation` | +0.8277 | +10.28 |
| `RES` | `inflation` | +1.7629 | +10.23 |
| `HST` | `inflation` | +1.3476 | +10.13 |
| `APA` | `inflation` | +1.5919 | +10.13 |
| `RZB` | `usd_strength` | -0.5148 | -10.07 |
| `PTEN` | `inflation` | +1.7737 | +10.07 |
