# Analysis 6 — Trust-Stratifiziertes R² Decomposition

**Datum:** 2026-05-25  
**Methode:** drei separate RidgeCV-Regressions pro Asset×Snapshot  
**Window:** 252 Trading Days (gleiche Konfiguration wie Production)  
**Faktor-Definitionen:** v1.0 (18 Faktoren, davon 11 DIRECT, 4 STATISTICAL, 13 DERIVED_THEME)

## Klassen-Zuordnung

- **DIRECT** (11): `market_beta`, `rates`, `inflation`, `usd_strength`, `volatility`, `rates_30y`, `credit_hy_spread`, `energy_oil`, `gold`, `copper`, `natural_gas`
- **STATISTICAL** (4): `value`, `growth`, `momentum`, `quality`
- **DERIVED_THEME** (13): `semiconductors`, `xl_financials`, `xl_healthcare`, `xl_industrials`, `xl_consumer_defensive`, `xl_utilities`, `xl_real_estate`, `china_exposure`, `lithium`, `uranium`, `biotech`, `defense`, `china_a_shares`

## Zusammenfassung

- **60 Assets** ausgewertet
- **2220 Asset×Snapshot Datenpunkte**
- **Mean r²_direct über alle Assets:** 0.432
- **Mean r²_+statistical:** 0.487
- **Mean r²_total:** 0.598
- **Mean derived_share:** 20.3%

## Tier-Reklassifikation (OLD = r²_total-basiert → NEW = trust-stratifiziert)

| OLD → NEW Tier | Anzahl Assets |
|---|---|
| HIGH → HIGH | 25 |
| HIGH → LOW | 3  ⚠️  Downgrade |
| HIGH → MED_DERIVED_HEAVY | 3  ⚠️  Downgrade |
| LOW → LOW | 1  ⚠️  Downgrade |
| MED → HIGH | 15 |
| MED → LOW | 13  ⚠️  Downgrade |

## Top-15 Assets nach r²_direct (höchstes DIRECT-Vertrauen)

| Symbol | r²_direct | r²_+stat | r²_total | derived_share | NEW Tier |
|---|---|---|---|---|---|
| `SPY` | 0.931 | 0.933 | 0.932 | -0.1% | HIGH |
| `IWB` | 0.927 | 0.931 | 0.931 | 0.0% | HIGH |
| `VTI` | 0.921 | 0.926 | 0.928 | 0.3% | HIGH |
| `DIA` | 0.828 | 0.856 | 0.875 | 2.2% | HIGH |
| `QQQ` | 0.819 | 0.904 | 0.924 | 2.3% | HIGH |
| `IWM` | 0.705 | 0.751 | 0.818 | 8.6% | HIGH |
| `MSFT` | 0.634 | 0.719 | 0.736 | 2.4% | HIGH |
| `AAPL` | 0.609 | 0.675 | 0.692 | 2.7% | HIGH |
| `FCX` | 0.605 | 0.625 | 0.686 | 9.0% | HIGH |
| `BLK` | 0.604 | 0.618 | 0.657 | 6.2% | HIGH |
| `AVGO` | 0.562 | 0.616 | 0.748 | 18.0% | HIGH |
| `GOOGL` | 0.561 | 0.617 | 0.659 | 6.9% | HIGH |
| `NVDA` | 0.515 | 0.638 | 0.757 | 15.9% | HIGH |
| `LIN` | 0.508 | 0.523 | 0.559 | 7.0% | HIGH |
| `ADBE` | 0.492 | 0.601 | 0.632 | 5.2% | HIGH |

## Bottom-15 Assets nach r²_direct

| Symbol | r²_direct | r²_+stat | r²_total | derived_share | NEW Tier |
|---|---|---|---|---|---|
| `TSLA` | 0.299 | 0.430 | 0.501 | 14.7% | LOW |
| `TMUS` | 0.293 | 0.312 | 0.356 | 12.9% | LOW |
| `UNH` | 0.276 | 0.329 | 0.518 | 38.7% | LOW |
| `NFLX` | 0.268 | 0.341 | 0.400 | 15.3% | LOW |
| `PG` | 0.266 | 0.317 | 0.649 | 52.2% | LOW |
| `SO` | 0.264 | 0.347 | 0.734 | 53.5% | LOW |
| `SMCI` | 0.250 | 0.262 | 0.338 | 23.9% | LOW |
| `DUK` | 0.231 | 0.320 | 0.753 | 58.7% | LOW |
| `TTWO` | 0.225 | 0.292 | 0.338 | 14.6% | LOW |
| `JNJ` | 0.220 | 0.301 | 0.525 | 43.9% | LOW |
| `WMT` | 0.191 | 0.207 | 0.388 | 48.5% | LOW |
| `DLTR` | 0.169 | 0.180 | 0.236 | 26.0% | LOW |
| `PFE` | 0.169 | 0.203 | 0.375 | 48.7% | LOW |
| `LLY` | 0.166 | 0.206 | 0.369 | 46.6% | LOW |
| `MRNA` | 0.148 | 0.205 | 0.434 | 55.8% | LOW |

## Top-15 Assets nach derived_share (höchste DERIVED-Abhängigkeit)

| Symbol | derived_share | r²_total | r²_+stat | marginal_derived | OLD → NEW |
|---|---|---|---|---|---|
| `DUK` | 58.7% | 0.753 | 0.320 | +0.432 | HIGH → LOW |
| `MRNA` | 55.8% | 0.434 | 0.205 | +0.230 | MED → LOW |
| `SO` | 53.5% | 0.734 | 0.347 | +0.387 | HIGH → LOW |
| `PG` | 52.2% | 0.649 | 0.317 | +0.332 | HIGH → LOW |
| `PFE` | 48.7% | 0.375 | 0.203 | +0.172 | MED → LOW |
| `WMT` | 48.5% | 0.388 | 0.207 | +0.182 | MED → LOW |
| `NEE` | 48.0% | 0.648 | 0.344 | +0.305 | HIGH → MED_DERIVED_HEAVY |
| `LLY` | 46.6% | 0.369 | 0.206 | +0.163 | MED → LOW |
| `AMT` | 44.0% | 0.665 | 0.381 | +0.284 | HIGH → HIGH |
| `JNJ` | 43.9% | 0.525 | 0.301 | +0.224 | MED → LOW |
| `O` | 39.5% | 0.624 | 0.383 | +0.241 | HIGH → MED_DERIVED_HEAVY |
| `UNH` | 38.7% | 0.518 | 0.329 | +0.189 | MED → LOW |
| `PLD` | 37.6% | 0.714 | 0.454 | +0.260 | HIGH → HIGH |
| `KO` | 35.0% | 0.649 | 0.425 | +0.224 | HIGH → MED_DERIVED_HEAVY |
| `BA` | 33.9% | 0.620 | 0.412 | +0.208 | HIGH → HIGH |

## ⚠️  JPM-Spezial-Analyse — ist der V3.3-Sektor-Gain echt?

Risk #4 Mitigation hat xl_financials hinzugefügt. JPM-R² stieg von 0.516 (Baseline) auf 0.588 (mean, post-V3.3). Frage: kommt diese Steigerung aus ECHTER Erklärungs-Kraft oder einem Spiegel-Artefakt (JPM ist ~10% des XLF-ETF, also passt sich xl_financials teilweise an JPM selbst an)?

**JPM-Decomposition (mean über 49 Snapshots):**

- `r²_direct`        = **0.472** (range 0.250 - 0.737)
- `r²_+statistical`  = **0.566**
- `r²_total`         = **0.687** (max 0.915)
- `marginal_derived` = **+0.121** (Beitrag von xl_*, semiconductors, china_exposure)
- `derived_share`    = **18.0%** (wieviel % von r²_total kommt von DERIVED?)

**Verdikt:** ✅ **GAIN IST ECHT.** DERIVED-Anteil ist klein — die echten Faktoren (market_beta, rates, value) erklären JPM gut, xl_financials nur als Marginal-Verbesserung.

## Vollständige Tabelle

Siehe `06_trust_stratified_r2.csv` für alle 60 Assets.

## Interpretation

- **r²_direct** = was wir mit klar-feststellbaren Faktoren erklären (market_beta, rates, inflation, usd_strength, volatility)
- **r²_+statistical** = + akademisch validierte Style-Faktoren (value, growth, momentum, quality)
- **r²_total** = + heterogene Sektor-Baskets (xl_*, semiconductors, energy_oil, china_exposure)
- **derived_share** = (r²_total - r²_+stat) / r²_total — wieviel % der Erklärung KÖNNTE Spiegel-Artefakt sein

**Ehrliche Aussage pro Asset:** r²_direct% sicher erklärt, marginal_statistical% halbwegs erklärt, marginal_derived% fraglich erklärt, (1-r²_total)% unerklärt.
