# Analysis 10 — Conditional-Beta-Analyse (Regime-stratifiziert)

**Datum:** 2026-05-25  
**Universe:** 60 assets × 28 factors  
**Regimes:** 3 (VIX, Rates, Bull-Bear)  
**Switch-Comparisons:** 5040

## Regime-Definitionen

| Regime | High-Level | Low-Level |
|---|---|---|
| **VIX** | VIX-Level > 25 | VIX-Level < 15 |
| **Rates** | Rising (IEF-Return < p5) | Falling (IEF-Return > p95) |
| **Bull-Bear** | 60d-SPY-Return > +2% | < -2% |

## Globaler Regime-Switch t-Stat

- Mean |t_diff|: 1.521
- Median: 1.170
- p95: 4.142
- Pairs mit |t_diff| ≥ 2.5: 920 (18.3%)
- Pairs mit |t_diff| ≥ 4: 284 (5.6%)

## Top-15 Regime-Switches: VIX

| Asset | Factor | β_high | β_low | Δβ | t_diff |
|---|---|---|---|---|---|
| `SPY` | `market_beta` | +1.000 | +1.000 | -0.000 | -14.86 |
| `GE` | `value` | +2.944 | -0.154 | +3.097 | +8.49 |
| `JPM` | `value` | +2.924 | +0.769 | +2.155 | +7.82 |
| `AVGO` | `momentum` | +0.288 | +3.014 | -2.726 | -7.51 |
| `VLO` | `value` | +3.950 | +0.889 | +3.061 | +7.32 |
| `CVX` | `value` | +3.166 | +1.004 | +2.162 | +7.01 |
| `DIA` | `market_beta` | +1.005 | +0.710 | +0.295 | +7.00 |
| `O` | `credit_hy_spread` | +1.195 | -1.030 | +2.225 | +6.99 |
| `SO` | `xl_utilities` | +1.444 | +0.887 | +0.557 | +6.99 |
| `GE` | `momentum` | -1.159 | +1.001 | -2.160 | -6.97 |
| `AVGO` | `semiconductors` | +0.145 | +1.371 | -1.226 | -6.95 |
| `CVX` | `market_beta` | +1.160 | +0.187 | +0.973 | +6.91 |
| `AMT` | `credit_hy_spread` | +0.773 | -1.412 | +2.185 | +6.80 |
| `COF` | `value` | +3.685 | +1.050 | +2.635 | +6.79 |
| `COP` | `market_beta` | +1.306 | +0.207 | +1.098 | +6.66 |

## Top-15 Regime-Switches: Rates

| Asset | Factor | β_high | β_low | Δβ | t_diff |
|---|---|---|---|---|---|
| `SPY` | `market_beta` | +1.000 | +1.000 | -0.000 | -7.55 |
| `O` | `rates_30y` | +1.430 | -1.326 | +2.755 | +4.59 |
| `MCD` | `xl_utilities` | +0.007 | +1.041 | -1.034 | -4.50 |
| `BA` | `rates_30y` | +2.275 | -0.601 | +2.876 | +4.20 |
| `DUK` | `quality` | -3.850 | +1.613 | -5.462 | -4.14 |
| `COF` | `xl_real_estate` | -0.635 | +1.568 | -2.203 | -4.10 |
| `BAC` | `xl_real_estate` | -0.193 | +1.345 | -1.538 | -4.04 |
| `DAL` | `rates_30y` | +2.753 | +0.450 | +2.304 | +3.98 |
| `IWM` | `xl_real_estate` | -0.175 | +1.040 | -1.215 | -3.94 |
| `KO` | `quality` | -2.121 | +1.337 | -3.458 | -3.85 |
| `TSLA` | `xl_real_estate` | -1.275 | +1.077 | -2.352 | -3.84 |
| `CVX` | `rates_30y` | +1.440 | -0.600 | +2.040 | +3.82 |
| `LSCC` | `xl_real_estate` | -0.943 | +0.913 | -1.856 | -3.81 |
| `DAL` | `energy_oil` | +0.806 | -0.036 | +0.841 | +3.81 |
| `HD` | `inflation` | -2.285 | +1.892 | -4.178 | -3.75 |

## Top-15 Regime-Switches: Bull-Bear

| Asset | Factor | β_high | β_low | Δβ | t_diff |
|---|---|---|---|---|---|
| `SPY` | `market_beta` | +1.000 | +1.000 | +0.000 | +10.27 |
| `DIA` | `volatility` | -0.045 | +0.102 | -0.148 | -7.84 |
| `SPY` | `volatility` | -0.053 | +0.113 | -0.166 | -7.73 |
| `IWB` | `volatility` | -0.055 | +0.113 | -0.168 | -7.71 |
| `VTI` | `volatility` | -0.057 | +0.114 | -0.170 | -7.68 |
| `IWM` | `volatility` | -0.080 | +0.119 | -0.199 | -7.13 |
| `AAPL` | `volatility` | -0.052 | +0.160 | -0.212 | -6.91 |
| `QQQ` | `volatility` | -0.062 | +0.126 | -0.189 | -6.85 |
| `GOOGL` | `volatility` | -0.064 | +0.166 | -0.230 | -6.62 |
| `HD` | `volatility` | -0.047 | +0.131 | -0.178 | -6.43 |
| `BLK` | `volatility` | -0.072 | +0.144 | -0.216 | -6.43 |
| `AVGO` | `volatility` | -0.110 | +0.117 | -0.227 | -6.35 |
| `COP` | `energy_oil` | +0.626 | +0.279 | +0.347 | +6.15 |
| `VLO` | `energy_oil` | +0.547 | +0.120 | +0.427 | +6.14 |
| `MSFT` | `volatility` | -0.052 | +0.139 | -0.191 | -6.13 |

## Per-Faktor — Anzahl Assets mit Regime-Switch (|t_diff| ≥ 2.5)

| Factor | Bull-Bear | Rates | VIX | Total |
|---|---|---|---|---|
| `volatility` | 57 | 3 | 23 | 83 | **83** |
| `credit_hy_spread` | 24 | 1 | 42 | 67 | **67** |
| `rates_30y` | 4 | 16 | 31 | 51 | **51** |
| `xl_real_estate` | 1 | 25 | 24 | 50 | **50** |
| `semiconductors` | 3 | 0 | 47 | 50 | **50** |
| `inflation` | 3 | 17 | 29 | 49 | **49** |
| `xl_utilities` | 7 | 11 | 30 | 48 | **48** |
| `market_beta` | 11 | 2 | 32 | 45 | **45** |
| `usd_strength` | 7 | 2 | 34 | 43 | **43** |
| `value` | 5 | 0 | 34 | 39 | **39** |
| `quality` | 13 | 10 | 13 | 36 | **36** |
| `defense` | 12 | 3 | 20 | 35 | **35** |
| `biotech` | 3 | 4 | 27 | 34 | **34** |
| `rates` | 2 | 3 | 29 | 34 | **34** |
| `xl_healthcare` | 1 | 3 | 29 | 33 | **33** |
| `xl_consumer_defensive` | 2 | 1 | 29 | 32 | **32** |
| `xl_industrials` | 14 | 2 | 15 | 31 | **31** |
| `growth` | 14 | 1 | 16 | 31 | **31** |
| `xl_financials` | 8 | 1 | 19 | 28 | **28** |
| `energy_oil` | 16 | 2 | 8 | 26 | **26** |

## Interpretation

- **Erwartet:** Full-Sample-Beta sollte ≈ gewichtetes Mittel von Regime-Betas sein.
- **Wenn |t_diff| ≥ 2.5:** Beta ist regime-dependent. Full-Sample-Beta ist eine 
  Mittelung, die in keinem konkreten Regime gut prädiktiv ist.
- **Typische Pattern:**
  - VIX-Regime-Switches bei Defensiv-Sektoren (XLU, XLP) — in Krisen wird ihre 
    'Defensive' Property verstärkt (Beta zu market sinkt)
  - Rates-Regime-Switches bei Banken (rising rates → höhere Beta zu rates_30y)
  - Bull-Bear-Switches bei High-Beta-Stocks (TSLA, NVDA) — Beta steigt in Bull,
    sinkt in Bear (Reflexivität)
- **Konsequenz für Gate-Engine:** für Assets mit regime-dependent Beta sollten 
  wir die CURRENT-Regime-Beta nutzen statt Full-Sample-Beta. Implementierung-
  Vorschlag: separate Regime-Beta-Spalten in asset_factor_exposures, Propagator 
  wählt basierend auf aktuellem VIX-Level.

CSV: `10_conditional_betas.csv`
