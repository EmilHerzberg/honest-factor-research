# Analysis 7 — Direct-Faktor-Replacement & Expansion-Test

**Datum:** 2026-05-24  
**Assets:** 60  
**Window:** 252 Trading Days  
**Regression:** RidgeCV(alphas=0.01/0.05/0.1)

## Coverage neuer Proxies

| Symbol | Datenpunkte | Tier |
|---|---|---|
| `^VIX` | 1405 | Phase A |
| `BZ=F` | 1406 | Phase A |
| `GLD` | 1405 | Tier 1 |
| `CPER` | 1405 | Tier 1 |
| `HYG` | 1405 | Tier 1 |
| `SHY` | 1405 | Tier 1 |
| `TLT` | 1405 | Tier 1 |
| `UNG` | 1405 | Tier 2 |
| `FXE` | 1405 | Tier 2 |
| `FXY` | 1405 | Tier 2 |
| `DBA` | 1405 | Tier 3 |
| `LIT` | 1405 | Tier 3 |
| `URA` | 1405 | Tier 3 |
| `CEW` | 1405 | Tier 3 |

## Phase A — Replacement-Tests (V1 → V2 → V3)

Klare Migration-Frage: lohnt sich der Wechsel von VXX zu ^VIX, und von XLE zu Brent (energy_oil aus DERIVED in DIRECT)?

### Globale Mittelwerte

| Variante | Faktoren | Mean r² | Δ vs V1 |
|---|---|---|---|
| V1_current | 5 | 0.386 | +0.000 |
| V2_vol_fix | 5 | 0.385 | -0.001 |
| V3_oil_fix | 6 | 0.407 | +0.021 |

### Bewertung

- **V2 − V1 (VXX → ^VIX): -0.001** — ⚪ neutral — keine echte Wirkung
- **V3 − V2 (+ Brent): +0.021** — 🟡 leichte Verbesserung — abwägen
- **V3 − V1 (gesamt Phase A): +0.021** — 🟡 leichte Verbesserung — abwägen

### Top-10 Beneficiaries von Brent (V3 − V2)

| Symbol | V2 r² | V3 r² | Δ |
|---|---|---|---|
| `COP` | 0.229 | 0.447 | +0.218 |
| `XOM` | 0.232 | 0.450 | +0.218 |
| `SLB` | 0.228 | 0.405 | +0.176 |
| `CVX` | 0.265 | 0.438 | +0.173 |
| `VLO` | 0.204 | 0.331 | +0.127 |
| `FCX` | 0.361 | 0.401 | +0.040 |
| `CAT` | 0.331 | 0.369 | +0.038 |
| `MRNA` | 0.119 | 0.137 | +0.018 |
| `PG` | 0.232 | 0.246 | +0.014 |
| `NEE` | 0.283 | 0.297 | +0.014 |

## Phase B — Individual Tier 1-3 Erweiterungen (jeweils V3 + 1 Faktor)

Pro Kandidat: marginaler Mean Δr² wenn nur DIESER eine Faktor zu V3 hinzugefügt wird. Top-3 Beneficiaries je Faktor zeigen, ob die Verbesserung breit gestreut ist oder nur 1-2 spezifische Assets trifft.

### Marginal-Effekt je Kandidat (sortiert nach Größe)

| Kandidat | Beschreibung | Mean Δr² vs V3 | Max Δr² (einzelnes Asset) |
|---|---|---|---|
| 🟡 **T3_Lithium** | Lithium — EV-Supply-Chain | +0.0136 | +0.088 (TSLA) |
| 🟡 **T1_30Y** | 30Y Treasury — Term-Premium | +0.0073 | +0.040 (BAC) |
| 🟡 **T3_Uranium** | Uranium — Nuclear-Renaissance | +0.0071 | +0.073 (FCX) |
| 🟡 **T1_Copper** | Copper — globale Wirtschaftsaktivität | +0.0066 | +0.204 (FCX) |
| 🟡 **T1_HYCredit** | HY-Credit-Spread — Recession-Leading | +0.0052 | +0.021 (BAC) |
| ⚪ **T1_Gold** | Gold — Safe-haven, Inflations-Hedge | +0.0049 | +0.023 (FCX) |
| ⚪ **T3_Agri** | Agriculture — Food-Inflation | +0.0030 | +0.025 (FCX) |
| ⚪ **T3_EMCurr** | EM-Currencies — EM-Stress | +0.0029 | +0.020 (FCX) |
| ⚪ **T2_NatGas** | Natural Gas — Energie-Krise-Proxy | +0.0026 | +0.005 (LIN) |
| ⚪ **T2_USDJPY** | USD/JPY — Safe-haven-Carry | +0.0019 | +0.009 (BAC) |
| ⚪ **T2_EURUSD** | EUR/USD — direkter EU-Stress | +0.0014 | +0.010 (FCX) |
| ⚪ **T1_2Y** | 2Y Treasury — Fed-Policy-Front-End | +0.0002 | +0.001 (DUK) |

### Top-5 Beneficiaries pro signifikantem Kandidat (Δ > 0.005)

#### T3_Lithium — Lithium — EV-Supply-Chain

| Symbol | V3 r² | V3+Cand r² | Δ |
|---|---|---|---|
| `TSLA` | 0.275 | 0.363 | +0.088 |
| `FCX` | 0.401 | 0.470 | +0.069 |
| `DUK` | 0.200 | 0.246 | +0.046 |
| `LSCC` | 0.478 | 0.522 | +0.043 |
| `ESTC` | 0.308 | 0.350 | +0.041 |

#### T1_30Y — 30Y Treasury — Term-Premium

| Symbol | V3 r² | V3+Cand r² | Δ |
|---|---|---|---|
| `BAC` | 0.439 | 0.479 | +0.040 |
| `JPM` | 0.426 | 0.458 | +0.032 |
| `CAT` | 0.369 | 0.392 | +0.023 |
| `COF` | 0.412 | 0.434 | +0.022 |
| `GE` | 0.347 | 0.365 | +0.018 |

#### T3_Uranium — Uranium — Nuclear-Renaissance

| Symbol | V3 r² | V3+Cand r² | Δ |
|---|---|---|---|
| `FCX` | 0.401 | 0.474 | +0.073 |
| `SLB` | 0.405 | 0.433 | +0.028 |
| `COP` | 0.447 | 0.472 | +0.025 |
| `XOM` | 0.450 | 0.472 | +0.022 |
| `IWM` | 0.699 | 0.721 | +0.022 |

#### T1_Copper — Copper — globale Wirtschaftsaktivität

| Symbol | V3 r² | V3+Cand r² | Δ |
|---|---|---|---|
| `FCX` | 0.401 | 0.605 | +0.204 |
| `CAT` | 0.369 | 0.396 | +0.027 |
| `APD` | 0.349 | 0.361 | +0.012 |
| `CVX` | 0.438 | 0.447 | +0.009 |
| `VLO` | 0.331 | 0.340 | +0.008 |

#### T1_HYCredit — HY-Credit-Spread — Recession-Leading

| Symbol | V3 r² | V3+Cand r² | Δ |
|---|---|---|---|
| `BAC` | 0.439 | 0.460 | +0.021 |
| `JPM` | 0.426 | 0.446 | +0.020 |
| `DAL` | 0.334 | 0.352 | +0.017 |
| `COF` | 0.412 | 0.429 | +0.017 |
| `CAT` | 0.369 | 0.382 | +0.013 |

## Kumulative Tier-Sets (V4-V6)

Was passiert wenn ALLE Tier-Faktoren gemeinsam zugefügt werden? Marginal-Effekt kann höher oder niedriger als Summe der Einzel-Effekte sein (je nach Korrelation der Erweiterungen).

| Variante | Faktoren-Anzahl | Mean r² | Δ vs V3 |
|---|---|---|---|
| V4_plus_Tier1 | 11 | 0.428 | +0.021 |
| V5_plus_Tier2 | 14 | 0.432 | +0.026 |
| V6_plus_Tier3 | 18 | 0.451 | +0.045 |

## Empfehlung (auf Basis der Daten)

### Phase A — Replacements

- **V3-Migration empfohlen** — Brent als DIRECT-Faktor liefert signifikanten Gewinn (insb. Energy-Stocks).
- V2 (VXX → ^VIX) ist **statistisch neutral** — Migration nur aus konzeptionellen Gründen (DIRECT_MECHANICAL-Klassifikation, sauberer Event-Mapping mit VIX-Level).

### Phase B — Erweiterungen (welche Faktoren in V3.4 aufnehmen)

**Aufnehmen (mean Δr² ≥ 0.005):**

- `T3_Lithium` (+0.0136)
- `T1_30Y` (+0.0073)
- `T3_Uranium` (+0.0071)
- `T1_Copper` (+0.0066)
- `T1_HYCredit` (+0.0052)

**Nicht aufnehmen (Δr² < 0.005):**

- `T1_Gold` (+0.0049) — kein messbarer Mehrwert
- `T3_Agri` (+0.0030) — kein messbarer Mehrwert
- `T3_EMCurr` (+0.0029) — kein messbarer Mehrwert
- `T2_NatGas` (+0.0026) — kein messbarer Mehrwert
- `T2_USDJPY` (+0.0019) — kein messbarer Mehrwert
- `T2_EURUSD` (+0.0014) — kein messbarer Mehrwert
- `T1_2Y` (+0.0002) — kein messbarer Mehrwert

## Interpretation

- r² hier ist immer **DIRECT-only-R²** — nur die getesteten Faktoren, keine STATISTICAL oder DERIVED-Beigaben.
- **Marginal-Test** zeigt was JEDER Faktor allein zu V3 beiträgt. Globaler Mean kann klein sein wenn der Faktor nur für 5-10 Assets wirkt.
- **Kumulative Sets** zeigen Sättigungs-Effekt — wenn Faktoren stark korreliert sind, ist V6-V3 < Summe der Einzel-Marginals.
- Asset-spezifische Top-Beneficiaries-Tabellen sind oft wichtiger als globaler Mean: ein Faktor mit Δr²=0.003 global aber +0.25 für FCX ist trotzdem wertvoll für FCX-Modellierung.

Vollständige Tabelle siehe `07_direct_factor_replacement.csv`.
