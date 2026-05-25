# Analysis 9 — Lead-Lag-Test: Asset[t+1] gegen Faktor[t]

**Datum:** 2026-05-25  
**Universe:** 60 assets × 28 factors  
**Pairs analysiert:** 1680

## Bewertungs-Schema

- |t_lead| < 2: keine signifikante Lead-Lag (effiziente Preisbildung)
- 2 ≤ |t_lead| < 3: marginal, akzeptabel
- 3 ≤ |t_lead| < 4: VERDÄCHTIG — investigation nötig
- |t_lead| ≥ 4: STARK — etweder ETF-Timing-Issue oder echte Inefficiency

## Globaler Lead-t-Stat (alle Pairs)

- Mean |t_lead|: 1.571
- Median |t_lead|: 1.304
- p95 |t_lead|: 3.926
- Pairs mit |t_lead| ≥ 3: 236 (14.0%)
- Pairs mit |t_lead| ≥ 4: 76 (4.5%)

## Top-20 Lead-Lag-Verdachtsfälle (|t_lead| ≥ 3)

| Asset | Factor | Lead β | Lead t | Contemp β | Contemp t |
|---|---|---|---|---|---|
| `MSFT` | `market_beta` | -0.3061 | -7.65 | +1.1876 | +50.78 |
| `HD` | `market_beta` | -0.2493 | -6.47 | +1.0238 | +38.85 |
| `TMUS` | `market_beta` | -0.2283 | -6.32 | +0.7460 | +24.85 |
| `AVGO` | `market_beta` | -0.3353 | -6.09 | +1.4143 | +36.22 |
| `ADBE` | `market_beta` | -0.3149 | -6.08 | +1.2776 | +33.52 |
| `QQQ` | `market_beta` | -0.2027 | -5.96 | +1.1358 | +90.18 |
| `DIA` | `market_beta` | -0.1635 | -5.96 | +0.9340 | +105.74 |
| `AMT` | `usd_strength` | -0.6674 | -5.74 | -0.1698 | -1.44 |
| `O` | `defense` | +0.3577 | +5.68 | +0.2265 | +3.57 |
| `IWB` | `market_beta` | -0.1618 | -5.67 | +1.0206 | +544.36 |
| `O` | `usd_strength` | -0.6879 | -5.61 | +0.0572 | +0.46 |
| `DUK` | `usd_strength` | -0.5255 | -5.60 | +0.0313 | +0.33 |
| `SPY` | `market_beta` | -0.1548 | -5.54 | +1.0000 | +159197986620818560.00 |
| `O` | `xl_consumer_defensive` | -0.4415 | -5.44 | +0.3282 | +4.03 |
| `VTI` | `market_beta` | -0.1553 | -5.40 | +1.0248 | +390.25 |
| `SO` | `usd_strength` | -0.5388 | -5.35 | +0.0237 | +0.23 |
| `MCD` | `defense` | +0.2448 | +5.34 | +0.0712 | +1.54 |
| `NVDA` | `market_beta` | -0.3770 | -5.32 | +1.7816 | +34.91 |
| `PG` | `market_beta` | -0.1454 | -5.24 | +0.5490 | +23.52 |
| `ORCL` | `market_beta` | -0.2254 | -5.22 | +0.9488 | +27.59 |

## Per-Faktor — Anzahl Assets mit Lead-Verdacht (|t_lead| ≥ 3)

| Factor | n Assets |
|---|---|
| `market_beta` | 44 |
| `usd_strength` | 29 |
| `xl_consumer_defensive` | 28 |
| `xl_healthcare` | 27 |
| `defense` | 26 |
| `xl_industrials` | 18 |
| `volatility` | 15 |
| `lithium` | 11 |
| `rates` | 9 |
| `rates_30y` | 9 |
| `semiconductors` | 6 |
| `xl_utilities` | 5 |
| `natural_gas` | 2 |
| `growth` | 1 |
| `biotech` | 1 |

## Top-15 Reverse-Lead (Asset[t] führt Factor[t+1], |t_lag| ≥ 3)

Hinweis: Wenn Asset signifikant gegen Factor[t+1] regressiert, ist es ein Preis-Entdecker (price-discovery leader). Z.B. NVDA in SOXX.

| Asset | Factor | Lag β | Lag t |
|---|---|---|---|
| `DIA` | `usd_strength` | -0.7916 | -10.30 |
| `BA` | `usd_strength` | -1.8904 | -9.95 |
| `VTI` | `usd_strength` | -0.7542 | -9.33 |
| `O` | `usd_strength` | -1.1171 | -9.30 |
| `IWB` | `usd_strength` | -0.7446 | -9.27 |
| `SPY` | `usd_strength` | -0.7234 | -9.20 |
| `JPM` | `usd_strength` | -1.0415 | -8.57 |
| `LIN` | `usd_strength` | -0.8208 | -8.45 |
| `MCD` | `usd_strength` | -0.7372 | -8.40 |
| `IWM` | `usd_strength` | -0.8651 | -8.38 |
| `DAL` | `usd_strength` | -1.5380 | -8.32 |
| `GS` | `usd_strength` | -1.0243 | -8.26 |
| `HD` | `usd_strength` | -0.8933 | -8.15 |
| `UNH` | `usd_strength` | -0.9063 | -8.04 |
| `COF` | `usd_strength` | -1.3546 | -8.03 |

## Interpretation

- **Effizienz-Annahme:** in liquiden US-Märkten sollte Asset[t+1] nicht durch 
  Factor[t] vorhersagbar sein (Markt verarbeitet Info am gleichen Tag).
- **Mögliche Ursachen für Lead-Verdachtsfälle:**
  - Faktor-ETF schließt nach Asset (selten in US-only)
  - China-ETF (FXI/ASHR) → Asia-Markt schließt vor US, Lead durch Time-Zone
  - Small-Cap-Assets mit niedrigem Volume → Verzögerte Reaktion
  - Idiosyncratic Information-Flow
- **Lag-Verdachtsfälle** (Asset leads Factor) zeigen Price-Discovery: das Asset ist 
  groß genug im Index dass seine Bewegung den Faktor verzögert beeinflusst.
- **Konsequenz für V3.4:** wenn ein Faktor systematisch Lead-Verdacht zeigt, ist seine 
  Beta-Schätzung unzuverlässig — die Faktor-Bewegung von gestern wird vom Asset heute 
  reproduziert. Solche Faktoren sollten als sektor-conditional skeptischer behandelt werden.

CSV: `09_lead_lag.csv`
