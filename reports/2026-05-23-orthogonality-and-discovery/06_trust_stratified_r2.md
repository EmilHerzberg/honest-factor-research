# Analysis 6 — Trust-Stratifiziertes R² Decomposition

**Datum:** 2026-05-23  
**Methode:** drei separate RidgeCV-Regressions pro Asset×Snapshot  
**Window:** 252 Trading Days (gleiche Konfiguration wie Production)  
**Faktor-Definitionen:** v1.0 (18 Faktoren, davon 5 DIRECT, 4 STATISTICAL, 9 DERIVED_THEME)

## Klassen-Zuordnung

- **DIRECT** (5): `market_beta`, `rates`, `inflation`, `usd_strength`, `volatility`
- **STATISTICAL** (4): `value`, `growth`, `momentum`, `quality`
- **DERIVED_THEME** (9): `semiconductors`, `energy_oil`, `xl_financials`, `xl_healthcare`, `xl_industrials`, `xl_consumer_defensive`, `xl_utilities`, `xl_real_estate`, `china_exposure`

## Zusammenfassung

- **60 Assets** ausgewertet
- **2940 Asset×Snapshot Datenpunkte**
- **Mean r²_direct über alle Assets:** 0.351
- **Mean r²_+statistical:** 0.418
- **Mean r²_total:** 0.548
- **Mean derived_share:** 25.3%

## Tier-Reklassifikation (OLD = r²_total-basiert → NEW = trust-stratifiziert)

| OLD → NEW Tier | Anzahl Assets |
|---|---|
| HIGH → HIGH | 15 |
| HIGH → LOW | 6  ⚠️  Downgrade |
| HIGH → MED_DERIVED_HEAVY | 3  ⚠️  Downgrade |
| LOW → LOW | 4  ⚠️  Downgrade |
| MED → HIGH | 9 |
| MED → LOW | 21  ⚠️  Downgrade |
| MED → MED_DERIVED_HEAVY | 2  ⚠️  Downgrade |

## Top-15 Assets nach r²_direct (höchstes DIRECT-Vertrauen)

| Symbol | r²_direct | r²_+stat | r²_total | derived_share | NEW Tier |
|---|---|---|---|---|---|
| `SPY` | 0.908 | 0.911 | 0.910 | -0.1% | HIGH |
| `IWB` | 0.904 | 0.908 | 0.909 | 0.1% | HIGH |
| `VTI` | 0.898 | 0.903 | 0.905 | 0.3% | HIGH |
| `QQQ` | 0.782 | 0.879 | 0.907 | 3.1% | HIGH |
| `DIA` | 0.769 | 0.806 | 0.828 | 2.8% | HIGH |
| `IWM` | 0.651 | 0.710 | 0.745 | 5.1% | HIGH |
| `BLK` | 0.554 | 0.578 | 0.619 | 7.1% | HIGH |
| `MSFT` | 0.551 | 0.658 | 0.679 | 3.5% | HIGH |
| `AAPL` | 0.526 | 0.602 | 0.620 | 3.5% | HIGH |
| `AVGO` | 0.498 | 0.573 | 0.716 | 20.6% | HIGH |
| `GOOGL` | 0.482 | 0.546 | 0.590 | 8.4% | HIGH |
| `NVDA` | 0.439 | 0.599 | 0.724 | 17.7% | HIGH |
| `AMZN` | 0.426 | 0.544 | 0.591 | 8.2% | HIGH |
| `ADBE` | 0.420 | 0.532 | 0.558 | 5.2% | HIGH |
| `HD` | 0.413 | 0.435 | 0.496 | 13.7% | HIGH |

## Bottom-15 Assets nach r²_direct

| Symbol | r²_direct | r²_+stat | r²_total | derived_share | NEW Tier |
|---|---|---|---|---|---|
| `UNH` | 0.201 | 0.252 | 0.425 | 47.2% | LOW |
| `SO` | 0.199 | 0.295 | 0.713 | 59.4% | LOW |
| `SLB` | 0.198 | 0.322 | 0.613 | 49.4% | MED_DERIVED_HEAVY |
| `PG` | 0.193 | 0.236 | 0.591 | 62.7% | LOW |
| `TTWO` | 0.192 | 0.258 | 0.288 | 11.0% | LOW |
| `COP` | 0.186 | 0.311 | 0.732 | 59.1% | LOW |
| `XOM` | 0.185 | 0.331 | 0.753 | 57.4% | LOW |
| `DUK` | 0.174 | 0.282 | 0.735 | 62.5% | LOW |
| `VLO` | 0.173 | 0.288 | 0.551 | 50.0% | MED_DERIVED_HEAVY |
| `JNJ` | 0.158 | 0.245 | 0.471 | 50.1% | LOW |
| `WMT` | 0.140 | 0.156 | 0.331 | 55.8% | LOW |
| `PFE` | 0.132 | 0.168 | 0.312 | 49.4% | LOW |
| `DLTR` | 0.132 | 0.148 | 0.201 | 28.5% | LOW |
| `LLY` | 0.127 | 0.175 | 0.335 | 50.4% | LOW |
| `MRNA` | 0.109 | 0.162 | 0.226 | 31.1% | LOW |

## Top-15 Assets nach derived_share (höchste DERIVED-Abhängigkeit)

| Symbol | derived_share | r²_total | r²_+stat | marginal_derived | OLD → NEW |
|---|---|---|---|---|---|
| `PG` | 62.7% | 0.591 | 0.236 | +0.355 | MED → LOW |
| `DUK` | 62.5% | 0.735 | 0.282 | +0.453 | HIGH → LOW |
| `SO` | 59.4% | 0.713 | 0.295 | +0.418 | HIGH → LOW |
| `COP` | 59.1% | 0.732 | 0.311 | +0.421 | HIGH → LOW |
| `XOM` | 57.4% | 0.753 | 0.331 | +0.422 | HIGH → LOW |
| `NEE` | 56.3% | 0.620 | 0.278 | +0.342 | HIGH → LOW |
| `WMT` | 55.8% | 0.331 | 0.156 | +0.175 | MED → LOW |
| `CVX` | 53.5% | 0.717 | 0.346 | +0.372 | HIGH → LOW |
| `LLY` | 50.4% | 0.335 | 0.175 | +0.160 | MED → LOW |
| `JNJ` | 50.1% | 0.471 | 0.245 | +0.227 | MED → LOW |
| `VLO` | 50.0% | 0.551 | 0.288 | +0.264 | MED → MED_DERIVED_HEAVY |
| `PFE` | 49.4% | 0.312 | 0.168 | +0.144 | MED → LOW |
| `SLB` | 49.4% | 0.613 | 0.322 | +0.290 | HIGH → MED_DERIVED_HEAVY |
| `UNH` | 47.2% | 0.425 | 0.252 | +0.173 | MED → LOW |
| `AMT` | 46.2% | 0.631 | 0.347 | +0.284 | HIGH → MED_DERIVED_HEAVY |

## ⚠️  JPM-Spezial-Analyse — ist der V3.3-Sektor-Gain echt?

Risk #4 Mitigation hat xl_financials hinzugefügt. JPM-R² stieg von 0.516 (Baseline) auf 0.588 (mean, post-V3.3). Frage: kommt diese Steigerung aus ECHTER Erklärungs-Kraft oder einem Spiegel-Artefakt (JPM ist ~10% des XLF-ETF, also passt sich xl_financials teilweise an JPM selbst an)?

**JPM-Decomposition (mean über 49 Snapshots):**

- `r²_direct`        = **0.369** (range 0.141 - 0.686)
- `r²_+statistical`  = **0.482**
- `r²_total`         = **0.588** (max 0.910)
- `marginal_derived` = **+0.107** (Beitrag von xl_*, semiconductors, china_exposure)
- `derived_share`    = **18.1%** (wieviel % von r²_total kommt von DERIVED?)

**Verdikt:** ✅ **GAIN IST ECHT.** DERIVED-Anteil ist klein — die echten Faktoren (market_beta, rates, value) erklären JPM gut, xl_financials nur als Marginal-Verbesserung.

## Vollständige Tabelle

Siehe `06_trust_stratified_r2.csv` für alle 60 Assets.

## Interpretation

- **r²_direct** = was wir mit klar-feststellbaren Faktoren erklären (market_beta, rates, inflation, usd_strength, volatility)
- **r²_+statistical** = + akademisch validierte Style-Faktoren (value, growth, momentum, quality)
- **r²_total** = + heterogene Sektor-Baskets (xl_*, semiconductors, energy_oil, china_exposure)
- **derived_share** = (r²_total - r²_+stat) / r²_total — wieviel % der Erklärung KÖNNTE Spiegel-Artefakt sein

**Ehrliche Aussage pro Asset:** r²_direct% sicher erklärt, marginal_statistical% halbwegs erklärt, marginal_derived% fraglich erklärt, (1-r²_total)% unerklärt.
