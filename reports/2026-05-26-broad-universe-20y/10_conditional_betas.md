# Analysis 10 — Conditional-Beta Analysis (regime-stratified)

**Date:** 2026-05-26  
**Switch comparisons:** 227836

## Global regime-switch t-stat

- Mean |t_diff|: 1.454
- Median: 1.065
- p95: 3.860
- Pairs with |t_diff| ≥ 2.5: 34016 (14.9%)
- Pairs with |t_diff| ≥ 4: 10352 (4.5%)

## Top-15 regime-switches: VIX

| Asset | Factor | β_high | β_low | Δβ | t_diff |
|---|---|---|---|---|---|
| `BTZ` | `market_beta` | +0.774 | +0.177 | +0.597 | +15.68 |
| `L` | `volatility` | +0.189 | -0.048 | +0.238 | +15.02 |
| `ITW` | `volatility` | +0.128 | -0.061 | +0.189 | +14.89 |
| `WOR` | `volatility` | +0.221 | -0.096 | +0.316 | +14.74 |
| `ROP` | `volatility` | +0.146 | -0.058 | +0.204 | +14.72 |
| `ETV` | `market_beta` | +0.952 | +0.477 | +0.475 | +14.48 |
| `TY` | `volatility` | +0.111 | -0.042 | +0.153 | +14.43 |
| `RPM` | `volatility` | +0.139 | -0.060 | +0.199 | +14.16 |
| `RVT` | `volatility` | +0.135 | -0.057 | +0.192 | +14.10 |
| `PPG` | `volatility` | +0.133 | -0.064 | +0.197 | +14.03 |
| `FAST` | `volatility` | +0.135 | -0.072 | +0.207 | +14.02 |
| `PCAR` | `volatility` | +0.152 | -0.070 | +0.222 | +13.96 |
| `TROW` | `volatility` | +0.184 | -0.070 | +0.254 | +13.94 |
| `MLI` | `volatility` | +0.183 | -0.082 | +0.265 | +13.94 |
| `EMR` | `volatility` | +0.142 | -0.064 | +0.205 | +13.91 |

## Top-15 regime-switches: Rates

| Asset | Factor | β_high | β_low | Δβ | t_diff |
|---|---|---|---|---|---|
| `CGBD` | `rates_30y` | +2.246 | -1.576 | +3.821 | +7.95 |
| `USAC` | `rates_30y` | +3.330 | -0.303 | +3.633 | +7.40 |
| `EPD` | `credit_hy_spread` | -0.143 | +1.755 | -1.898 | -7.39 |
| `SLRC` | `rates_30y` | +1.962 | -0.863 | +2.825 | +7.39 |
| `GSBD` | `rates_30y` | +1.721 | -1.190 | +2.911 | +7.37 |
| `TCPC` | `rates_30y` | +2.321 | -1.055 | +3.375 | +7.34 |
| `AGNCM` | `rates_30y` | +2.445 | -0.314 | +2.759 | +7.22 |
| `AGNCN` | `rates_30y` | +2.022 | -0.319 | +2.342 | +7.21 |
| `FHI` | `credit_hy_spread` | -1.213 | +1.399 | -2.613 | -7.08 |
| `PFLT` | `rates_30y` | +1.998 | -0.671 | +2.669 | +7.06 |
| `GCBC` | `market_beta` | +1.108 | -0.100 | +1.208 | +7.05 |
| `AGNCO` | `rates_30y` | +2.623 | -0.312 | +2.935 | +6.91 |
| `PSEC` | `credit_hy_spread` | -1.630 | +1.340 | -2.970 | -6.79 |
| `FDUS` | `rates_30y` | +2.105 | -0.999 | +3.104 | +6.79 |
| `CGBD` | `xl_utilities` | -0.644 | +1.981 | -2.625 | -6.76 |

## Top-15 regime-switches: Bull-Bear

| Asset | Factor | β_high | β_low | Δβ | t_diff |
|---|---|---|---|---|---|
| `GAM` | `volatility` | -0.043 | +0.149 | -0.192 | -18.64 |
| `L` | `volatility` | -0.043 | +0.222 | -0.265 | -18.57 |
| `AFG` | `volatility` | -0.050 | +0.249 | -0.299 | -18.09 |
| `GDV` | `volatility` | -0.048 | +0.176 | -0.224 | -18.02 |
| `RVT` | `volatility` | -0.062 | +0.167 | -0.229 | -18.00 |
| `RPM` | `volatility` | -0.055 | +0.176 | -0.231 | -17.92 |
| `TY` | `volatility` | -0.044 | +0.136 | -0.180 | -17.92 |
| `RTX` | `volatility` | -0.056 | +0.163 | -0.219 | -17.70 |
| `ETV` | `volatility` | -0.040 | +0.159 | -0.199 | -17.49 |
| `GAB` | `volatility` | -0.053 | +0.187 | -0.240 | -17.34 |
| `ROP` | `volatility` | -0.054 | +0.171 | -0.225 | -17.33 |
| `IVZ` | `volatility` | -0.085 | +0.276 | -0.362 | -17.28 |
| `TROW` | `volatility` | -0.070 | +0.227 | -0.297 | -17.21 |
| `AVY` | `volatility` | -0.057 | +0.172 | -0.229 | -17.19 |
| `CTAS` | `volatility` | -0.056 | +0.157 | -0.212 | -17.19 |
