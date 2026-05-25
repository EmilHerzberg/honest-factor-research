# Analysis 8 — Broad-Universe Replay

**Datum:** 2026-05-24  
**Assets ausgewertet:** 2241  
**Window:** 252 Trading Days  
**Replay von:** Script 07 V1-V3 + 12 Tier-Tests + 3 kumulative

## Globaler Vergleich vs Script 07 (60-Asset-Sample)

| Variante | 60-Asset Mean r² (Script 07) | Broad-Universe Mean r² | Δ |
|---|---|---|---|
| V1_current | 0.386 | 0.250 | -0.136 |
| V2_vol_fix | 0.385 | 0.248 | -0.137 |
| V3_oil_fix | 0.407 | 0.259 | -0.148 |

## Marginal-Effekt je Kandidat (sortiert nach Mean Δr²)

| Kandidat | Beschreibung | 60-A Δr² | Broad Δr² | Median | p75 | n Assets Δ≥0.05 | Max Δ (Asset) |
|---|---|---|---|---|---|---|---|
| 🟡 **T3_Lithium** | Lithium | +0.0136 | +0.0101 | +0.0061 | +0.0120 | 34 | +0.203 (ALB) |
| 🟡 **T3_Uranium** | Uranium | +0.0071 | +0.0085 | +0.0055 | +0.0102 | 14 | +0.272 (EU) |
| 🟡 **T1_30Y** | 30Y Treasury | +0.0073 | +0.0077 | +0.0054 | +0.0100 | 0 | +0.050 (GBAB) |
| 🟡 **T1_HYCredit** | HY-Credit-Spread | +0.0052 | +0.0059 | +0.0050 | +0.0084 | 0 | +0.023 (MOV) |
| ⚪ **T1_Gold** | Gold | +0.0049 | +0.0047 | +0.0032 | +0.0059 | 6 | +0.320 (ASA) |
| ⚪ **T1_Copper** | Copper | +0.0066 | +0.0042 ⚠️ **Aufnehmen → Skip?** | +0.0029 | +0.0048 | 8 | +0.204 (FCX) |
| ⚪ **T2_NatGas** | Natural Gas | +0.0026 | +0.0036 | +0.0026 | +0.0040 | 6 | +0.205 (EQT) |
| ⚪ **T3_Agri** | Agriculture | +0.0030 | +0.0030 | +0.0023 | +0.0038 | 0 | +0.035 (CF) |
| ⚪ **T3_EMCurr** | EM-Currencies | +0.0029 | +0.0030 | +0.0023 | +0.0039 | 0 | +0.040 (AEF) |
| ⚪ **T2_USDJPY** | USD/JPY | +0.0019 | +0.0020 | +0.0016 | +0.0027 | 0 | +0.028 (ASA) |
| ⚪ **T2_EURUSD** | EUR/USD | +0.0014 | +0.0012 | +0.0009 | +0.0015 | 0 | +0.016 (ASA) |
| ⚪ **T1_2Y** | 2Y Treasury | +0.0002 | +0.0002 | +0.0001 | +0.0002 | 0 | +0.003 (VLYPO) |

## Per-Sektor Faktor-Relevanz (mean Δr² je Sektor)

| Sektor | n | T1_Gold | T1_Copper | T1_HYCredit | T1_2Y | T1_30Y | T2_NatGas | T2_EURUSD | T2_USDJPY | T3_Agri | T3_Lithium | T3_Uranium | T3_EMCurr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Basic Materials | 28 | **+0.027** | **+0.025** | +0.004 | +0.000 | +0.006 | +0.004 | +0.004 | +0.002 | +0.006 | +0.013 | **+0.027** | +0.006 |
| Consumer Discretionary | 453 | +0.004 | +0.004 | +0.006 | +0.000 | +0.006 | +0.003 | +0.001 | +0.002 | +0.003 | +0.008 | +0.007 | +0.003 |
| Consumer Staples | 57 | +0.003 | +0.003 | +0.003 | +0.000 | +0.003 | +0.003 | +0.001 | +0.002 | +0.003 | +0.014 | +0.006 | +0.002 |
| Energy | 83 | +0.005 | +0.008 | +0.006 | +0.000 | +0.005 | +0.019 | +0.001 | +0.002 | +0.006 | +0.011 | **+0.029** | +0.004 |
| Finance | 500 | +0.005 | +0.003 | +0.009 | +0.000 | +0.015 | +0.003 | +0.001 | +0.003 | +0.002 | +0.006 | +0.006 | +0.003 |
| Health Care | 289 | +0.003 | +0.002 | +0.003 | +0.000 | +0.003 | +0.003 | +0.001 | +0.001 | +0.003 | +0.011 | +0.009 | +0.002 |
| Industrials | 293 | +0.006 | +0.008 | +0.006 | +0.000 | +0.007 | +0.003 | +0.001 | +0.002 | +0.004 | +0.011 | +0.010 | +0.003 |
| Miscellaneous | 14 | +0.002 | +0.004 | +0.004 | +0.000 | +0.004 | +0.004 | +0.001 | +0.002 | +0.003 | +0.017 | +0.010 | +0.004 |
| Real Estate | 152 | +0.005 | +0.002 | +0.007 | +0.000 | +0.007 | +0.003 | +0.001 | +0.002 | +0.003 | +0.006 | +0.004 | +0.003 |
| Technology | 236 | +0.003 | +0.003 | +0.004 | +0.000 | +0.005 | +0.002 | +0.001 | +0.001 | +0.002 | +0.019 | +0.009 | +0.002 |
| Telecommunications | 37 | +0.003 | +0.003 | +0.003 | +0.000 | +0.004 | +0.003 | +0.001 | +0.002 | +0.003 | +0.009 | +0.005 | +0.002 |
| Utilities | 95 | +0.005 | +0.003 | +0.005 | +0.000 | +0.008 | +0.005 | +0.001 | +0.002 | +0.003 | +0.016 | +0.010 | +0.002 |

## Top-Sektoren pro Faktor (welche Branche braucht welchen Faktor)

#### T1_Gold (Gold)
- **Basic Materials** (n=28): +0.0267
- **Industrials** (n=293): +0.0061
- **Finance** (n=500): +0.0055

#### T1_Copper (Copper)
- **Basic Materials** (n=28): +0.0245
- **Energy** (n=83): +0.0077
- **Industrials** (n=293): +0.0075

#### T1_HYCredit (HY-Credit-Spread)
- **Finance** (n=500): +0.0088
- **Real Estate** (n=152): +0.0068
- **Consumer Discretionary** (n=453): +0.0062

#### T1_30Y (30Y Treasury)
- **Finance** (n=500): +0.0149
- **Utilities** (n=95): +0.0075
- **Real Estate** (n=152): +0.0072

#### T2_NatGas (Natural Gas)
- **Energy** (n=83): +0.0187
- **Utilities** (n=95): +0.0047
- **Basic Materials** (n=28): +0.0035

#### T3_Agri (Agriculture)
- **Basic Materials** (n=28): +0.0063
- **Energy** (n=83): +0.0057
- **Industrials** (n=293): +0.0038

#### T3_Lithium (Lithium)
- **Technology** (n=236): +0.0189
- **Miscellaneous** (n=14): +0.0167
- **Utilities** (n=95): +0.0157

#### T3_Uranium (Uranium)
- **Energy** (n=83): +0.0289
- **Basic Materials** (n=28): +0.0270
- **Miscellaneous** (n=14): +0.0104

#### T3_EMCurr (EM-Currencies)
- **Basic Materials** (n=28): +0.0060
- **Miscellaneous** (n=14): +0.0036
- **Energy** (n=83): +0.0035

## V3.4-Empfehlung (basierend auf Broad-Universe)

**Aufnehmen (Broad-Universe Mean Δr² ≥ 0.005):**

- `T3_Lithium` (+0.0101, n_sig=34)
- `T3_Uranium` (+0.0085, n_sig=14)
- `T1_30Y` (+0.0077, n_sig=0)
- `T1_HYCredit` (+0.0059, n_sig=0)

**Skip (Mean Δr² < 0.005):**

- `T1_Gold` (+0.0047) — kein breiter Mehrwert
- `T1_Copper` (+0.0042) — kein breiter Mehrwert
- `T2_NatGas` (+0.0036) — kein breiter Mehrwert
- `T3_Agri` (+0.0030) — kein breiter Mehrwert
- `T3_EMCurr` (+0.0030) — kein breiter Mehrwert
- `T2_USDJPY` (+0.0020) — kein breiter Mehrwert
- `T2_EURUSD` (+0.0012) — kein breiter Mehrwert
- `T1_2Y` (+0.0002) — kein breiter Mehrwert

## Interpretation

- Marginal-Effekt = mean Δr² wenn ein einzelner Kandidat zu V3 hinzugefügt wird.
- **n Assets Δ≥0.05** zeigt Konzentration: ein Faktor mit kleinem mean aber vielen Δ≥0.05 
  ist wertvoll für eine spezifische Cluster-Gruppe.
- ⚠️ Verdict-Change vs. Script 07 sind die wichtigsten Erkenntnisse.
- Per-Sektor Tabellen zeigen welche Branche WIRKLICH welchen Faktor braucht — 
  das ist die Basis für eventuelle Asset-spezifische Faktor-Wahl (Risk #2 Mitigation 2G).

CSVs: `08_broad_universe_replay.csv` (per-Asset), `08_per_sector_factor_relevance.csv` (per-Sektor)
