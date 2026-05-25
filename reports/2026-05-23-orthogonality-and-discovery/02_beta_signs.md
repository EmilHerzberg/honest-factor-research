# Analysis 2 — Beta-Sign Sanity Check

**Datum:** 2026-05-23

## Zusammenfassung

- **120 (Asset, Faktor)-Paare** insgesamt
- **35 Paare** mit ökonomischem Prior
- **✓ 19 matches** (Vorzeichen wie erwartet)
- **~ 8 borderline** (eines neutral)
- **✗ 8 MISMATCHES** ⚠️

## ⚠️ Beta-Sign Mismatches (Anomalien)

| Severity | Symbol | Sector | Faktor | Expected | Actual β | R² | Hypothese |
|---|---|---|---|---|---|---|---|
| 🔴 | `AVGO` | Technology | `rates` | - | +0.060 | 0.70 | Maybe asset profits from rate hikes (less common — check specifics) |
| 🔴 | `NVDA` | Technology | `rates` | - | +0.103 | 0.70 | Maybe asset profits from rate hikes (less common — check specifics) |
| 🔴 | `MSFT` | Technology | `rates` | - | +0.059 | 0.69 | Maybe asset profits from rate hikes (less common — check specifics) |
| 🔴 | `MSFT` | Technology | `semiconductors` | + | -0.095 | 0.69 | Beta klein — Signal ggf. nicht robust |
| 🔴 | `AAPL` | Technology | `rates` | - | +0.059 | 0.62 | Maybe asset profits from rate hikes (less common — check specifics) |
| 🔴 | `AAPL` | Technology | `semiconductors` | + | -0.087 | 0.62 | Beta klein — Signal ggf. nicht robust |
| 🔴 | `GOOGL` | Communication Services | `rates` | - | +0.071 | 0.58 | Maybe asset profits from rate hikes (less common — check specifics) |
| 🔴 | `JPM` | Financial Services | `rates` | + | -0.185 | 0.52 | Standard duration-sensitivity (high-mult or bond-proxy asset) |

## Match-Rate pro Sektor

| Sektor | N geprüft | Matches | Mismatches | Match-Rate |
|---|---|---|---|---|
| Communication Services | 4 | 2 | 2 | 50% |
| Consumer Cyclical | 4 | 2 | 2 | 50% |
| Energy | 4 | 3 | 1 | 75% |
| Financial Services | 3 | 2 | 1 | 67% |
| Technology | 20 | 10 | 10 | 50% |

## Methodik

- Expected-Sign aus ökonomischen Priors (siehe `SECTOR_FACTOR_PRIORS` in `02_beta_signs.py`)
- Actual-Sign aus mean exposure_value über alle rolling_ridge_252d Snapshots
- Threshold: |actual| > 0.05 für Sign-Eindeutigkeit, sonst 'neutral' (0)
- Severity:
  - 🔴 R² ≥ 0.5 (Mismatch ist starkes Signal)
  - 🟠 0.3 ≤ R² < 0.5 (mittleres Vertrauen)
  - 🟡 R² < 0.3 (low confidence — Mismatch könnte Rauschen sein)

Detaillierte Daten in `02_beta_signs.csv`.
