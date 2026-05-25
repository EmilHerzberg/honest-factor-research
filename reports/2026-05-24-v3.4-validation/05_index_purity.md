# Analysis 5 — Index-Purity-Test (Risk #5 Phase 2)

**Datum:** 2026-05-24  
**Methode:** Korrelations-Test current Faktor-ETF vs. alternative ETFs 
die dasselbe Konzept abbilden sollten (z.B. value: IWD/Russell vs VLUE/MSCI 
vs IUSV/S&P vs RPV/Pure-Value).

## Bewertungs-Schema

- 🟢 **robust** (min ρ ≥ 0.95): Methodologie-übergreifend konsistent, 
  unser Proxy misst das was wir behaupten
- 🟡 **mostly_same** (0.90 ≤ ρ < 0.95): leichte Methodologie-Differenz, 
  aber gleicher Faktor
- 🟠 **different_proxy** (0.80 ≤ ρ < 0.90): unsere ETF-Wahl ist methodisch 
  ein eigener Faktor mit Bias
- 🔴 **fundamentally_different** (ρ < 0.80): unser Proxy misst etwas 
  Substanziell anderes als die Alternativen

## Zusammenfassung

- **7** robust 🟢
- **6** mostly_same 🟡
- **2** different_proxy 🟠
- **3** fundamentally_different 🔴
- 0 no_alternatives_available

## Pro-Faktor Detail (sortiert nach min ρ aufsteigend)

### 🔴 `inflation` — fundamentally_different

**Klasse:** DIRECT  
**Aktueller Proxy:** `TIP-IEF spread`  
**Methodologie:** iShares TIPS minus 7-10Y nominal  
**Was wir messen wollen:** Inflation breakeven / TIPS-bond expectations

**Min ρ:** +0.7286  
**Min ρ unter Alt-Proxies:** +0.7456  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `VTIP_minus_IEF` | +0.7286 | 🔴 substanziell anders |
| `SCHP_minus_IEF` | +0.9727 | 🟢 essentiell identisch |

> ⚠️ **Architektur-Implikation:** Unser Proxy für diesen Faktor ist 
> methodisch nicht stabil. Eine Migration zu einem alternativen ETF 
> würde das gemessene Faktor-Konstrukt substanziell verändern.

### 🔴 `xl_healthcare` — fundamentally_different

**Klasse:** DERIVED  
**Aktueller Proxy:** `XLV`  
**Methodologie:** Healthcare Select Sector (UNH 10%, LLY, JNJ, MRK, PFE)  
**Was wir messen wollen:** Healthcare sector exposure

**Min ρ:** +0.7560  
**Min ρ unter Alt-Proxies:** +0.7305  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `IBB` | +0.7560 | 🔴 substanziell anders |
| `IHI` | +0.8741 | 🟠 methodisch unterschiedlich |
| `VHT` | +0.9866 | 🟢 essentiell identisch |

> ⚠️ **Architektur-Implikation:** Unser Proxy für diesen Faktor ist 
> methodisch nicht stabil. Eine Migration zu einem alternativen ETF 
> würde das gemessene Faktor-Konstrukt substanziell verändern.

### 🔴 `china_exposure` — fundamentally_different

**Klasse:** DERIVED  
**Aktueller Proxy:** `FXI`  
**Methodologie:** FTSE China 50 (HK-listed Tech 30% + Banken 20%)  
**Was wir messen wollen:** China economy exposure

**Min ρ:** +0.7918  
**Min ρ unter Alt-Proxies:** +0.6707  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `ASHR` | +0.7918 | 🔴 substanziell anders |
| `KWEB` | +0.9142 | 🟡 leichte Differenz |
| `MCHI` | +0.9803 | 🟢 essentiell identisch |

> ⚠️ **Architektur-Implikation:** Unser Proxy für diesen Faktor ist 
> methodisch nicht stabil. Eine Migration zu einem alternativen ETF 
> würde das gemessene Faktor-Konstrukt substanziell verändern.

### 🟠 `usd_strength` — different_proxy

**Klasse:** DIRECT  
**Aktueller Proxy:** `UUP`  
**Methodologie:** Bullish USD vs DXY-basket (EUR/JPY/GBP/CAD/SEK/CHF, 58% EUR)  
**Was wir messen wollen:** USD strength vs major currencies

**Min ρ:** +0.8127  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `USDU` | +0.8127 | 🟠 methodisch unterschiedlich |

> 🟠 **Hinweis:** Methodologie-Wahl ist ein Bias. Bei zukünftigen 
> Faktor-Erweiterungen Alternative-ETFs explizit gegen aktuelles testen.

### 🟠 `xl_industrials` — different_proxy

**Klasse:** DERIVED  
**Aktueller Proxy:** `XLI`  
**Methodologie:** Industrials Select Sector (GE, RTX, BA, HON, MMM, Rails ~15%)  
**Was wir messen wollen:** Industrials sector exposure

**Min ρ:** +0.8993  
**Min ρ unter Alt-Proxies:** +0.8646  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `ITA` | +0.8993 | 🟠 methodisch unterschiedlich |
| `IYJ` | +0.9749 | 🟢 essentiell identisch |
| `VIS` | +0.9938 | 🟢 essentiell identisch |

> 🟠 **Hinweis:** Methodologie-Wahl ist ein Bias. Bei zukünftigen 
> Faktor-Erweiterungen Alternative-ETFs explizit gegen aktuelles testen.

### 🟡 `xl_financials` — mostly_same

**Klasse:** DERIVED  
**Aktueller Proxy:** `XLF`  
**Methodologie:** Financial Select Sector (BRK.B 13%, JPM 10%, BAC, WFC, BLK, MMC)  
**Was wir messen wollen:** Financials sector exposure

**Min ρ:** +0.9043  
**Min ρ unter Alt-Proxies:** +0.9022  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `KBE` | +0.9043 | 🟡 leichte Differenz |
| `IYF` | +0.9856 | 🟢 essentiell identisch |
| `VFH` | +0.9951 | 🟢 essentiell identisch |

### 🟡 `xl_consumer_defensive` — mostly_same

**Klasse:** DERIVED  
**Aktueller Proxy:** `XLP`  
**Methodologie:** Consumer Staples Select (WMT+COST ~25%, PG, KO, PEP, Tobacco)  
**Was wir messen wollen:** Consumer staples sector

**Min ρ:** +0.9046  
**Min ρ unter Alt-Proxies:** +0.9131  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `IYK` | +0.9046 | 🟡 leichte Differenz |
| `VDC` | +0.9930 | 🟢 essentiell identisch |

### 🟡 `energy_oil` — mostly_same

**Klasse:** DERIVED  
**Aktueller Proxy:** `XLE`  
**Methodologie:** Energy Select Sector (US Energy stocks, XOM 22% + CVX 17%)  
**Was wir messen wollen:** Energy/oil sector exposure (NICHT Öl-Preis direkt — siehe Brent)

**Min ρ:** +0.9145  
**Min ρ unter Alt-Proxies:** +0.9234  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `XOP` | +0.9145 | 🟡 leichte Differenz |
| `VDE` | +0.9971 | 🟢 essentiell identisch |
| `IYE` | +0.9976 | 🟢 essentiell identisch |

### 🟡 `momentum` — mostly_same

**Klasse:** STATISTICAL  
**Aktueller Proxy:** `MTUM`  
**Methodologie:** MSCI USA Momentum (6/12-mo risk-adjusted, halbjährliches Rebal)  
**Was wir messen wollen:** Momentum-factor premium

**Min ρ:** +0.9296  
**Min ρ unter Alt-Proxies:** +0.9024  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `PDP` | +0.9296 | 🟡 leichte Differenz |
| `SPMO` | +0.9344 | 🟡 leichte Differenz |

### 🟡 `growth` — mostly_same

**Klasse:** STATISTICAL  
**Aktueller Proxy:** `IWF`  
**Methodologie:** Russell 1000 Growth (high P/B + high sales-growth)  
**Was wir messen wollen:** Growth-style premium

**Min ρ:** +0.9338  
**Min ρ unter Alt-Proxies:** +0.9303  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `RPG` | +0.9338 | 🟡 leichte Differenz |
| `SCHG` | +0.9961 | 🟢 essentiell identisch |
| `VONG` | +0.9985 | 🟢 essentiell identisch |

### 🟡 `value` — mostly_same

**Klasse:** STATISTICAL  
**Aktueller Proxy:** `IWD`  
**Methodologie:** Russell 1000 Value (low P/B + low sales-growth)  
**Was wir messen wollen:** Value-style premium

**Min ρ:** +0.9465  
**Min ρ unter Alt-Proxies:** +0.9469  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `RPV` | +0.9465 | 🟡 leichte Differenz |
| `VLUE` | +0.9706 | 🟢 essentiell identisch |
| `IUSV` | +0.9918 | 🟢 essentiell identisch |

### 🟢 `rates` — robust

**Klasse:** DIRECT  
**Aktueller Proxy:** `IEF`  
**Methodologie:** iShares 7-10Y Treasury  
**Was wir messen wollen:** Mid-tenor US Treasury exposure / duration

**Min ρ:** +0.9604  
**Min ρ unter Alt-Proxies:** +0.9368  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `GOVT` | +0.9604 | 🟢 essentiell identisch |
| `VGIT` | +0.9785 | 🟢 essentiell identisch |

### 🟢 `quality` — robust

**Klasse:** STATISTICAL  
**Aktueller Proxy:** `QUAL`  
**Methodologie:** MSCI USA Quality (high ROE + low leverage + stable EPS)  
**Was wir messen wollen:** Quality-factor premium

**Min ρ:** +0.9743  
**Min ρ unter Alt-Proxies:** +0.9739  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `SPHQ` | +0.9743 | 🟢 essentiell identisch |
| `FQAL` | +0.9819 | 🟢 essentiell identisch |

### 🟢 `semiconductors` — robust

**Klasse:** DERIVED  
**Aktueller Proxy:** `SOXX`  
**Methodologie:** ICE Semiconductor (30 chip stocks, modified-cap-weighted)  
**Was wir messen wollen:** Semiconductor industry exposure

**Min ρ:** +0.9794  
**Min ρ unter Alt-Proxies:** +0.9702  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `PSI` | +0.9794 | 🟢 essentiell identisch |
| `SMH` | +0.9915 | 🟢 essentiell identisch |

### 🟢 `volatility` — robust

**Klasse:** DIRECT  
**Aktueller Proxy:** `VXX`  
**Methodologie:** 30-day rolling VIX-futures ETN (contango-decay)  
**Was wir messen wollen:** Market vol-regime / fear-gauge

**Min ρ:** +0.9801  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `VIXY` | +0.9801 | 🟢 essentiell identisch |

### 🟢 `xl_real_estate` — robust

**Klasse:** DERIVED  
**Aktueller Proxy:** `XLRE`  
**Methodologie:** Real Estate Select (Industrial/Tower/Datacenter/Retail/Resi REITs)  
**Was wir messen wollen:** REIT sector exposure

**Min ρ:** +0.9876  
**Min ρ unter Alt-Proxies:** +0.9972  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `VNQ` | +0.9876 | 🟢 essentiell identisch |
| `IYR` | +0.9893 | 🟢 essentiell identisch |

### 🟢 `xl_utilities` — robust

**Klasse:** DERIVED  
**Aktueller Proxy:** `XLU`  
**Methodologie:** Utilities Select Sector (Electric 60%, Gas, Water, Multi)  
**Was wir messen wollen:** Utilities sector (bond-proxy)

**Min ρ:** +0.9957  
**Min ρ unter Alt-Proxies:** +0.9964  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `IDU` | +0.9957 | 🟢 essentiell identisch |
| `VPU` | +0.9974 | 🟢 essentiell identisch |

### 🟢 `market_beta` — robust

**Klasse:** STATISTICAL  
**Aktueller Proxy:** `SPY`  
**Methodologie:** S&P 500  
**Was wir messen wollen:** Broad US equity market exposure

**Min ρ:** +0.9959  
**Min ρ unter Alt-Proxies:** +0.9976  
**N Trading-Days verglichen:** 1255

| Alt-Proxy | ρ zu aktuell | Verdikt |
|---|---|---|
| `VTI` | +0.9959 | 🟢 essentiell identisch |
| `ITOT` | +0.9959 | 🟢 essentiell identisch |
| `IWB` | +0.9979 | 🟢 essentiell identisch |

## Architektur-Implikationen

**5 Faktoren** mit nicht-trivialer Methodologie-Variabilität:

- `inflation` (DIRECT): fundamentally_different mit min ρ=+0.729
- `xl_healthcare` (DERIVED): fundamentally_different mit min ρ=+0.756
- `china_exposure` (DERIVED): fundamentally_different mit min ρ=+0.792
- `usd_strength` (DIRECT): different_proxy mit min ρ=+0.813
- `xl_industrials` (DERIVED): different_proxy mit min ρ=+0.899

**Empfehlung:** für jeden flagged Faktor in V3.4 dokumentieren 
welches spezifische Konstrukt wir messen (Russell vs. MSCI vs. S&P-
Methodologie), und welches Sub-Verhalten dadurch eingebaut ist.

## Was NICHT getestet wurde

- **Top-N-Holdings-Konzentration** — yfinance fund_holdings unzuverlässig; 
  bräuchte SEC NPORT-P-Filings oder kommerzielle ETF-Daten
- **PCA-Decomposition** der Konstituenten — gleiches Datenproblem
- **Cross-Asset-Class-Korrelationen** (z.B. ist value-vs-growth wirklich 
  unkorreliert? siehe Risk #3 separat)
- **Asymmetrische Stress-Korrelationen** — was passiert in Krisen-Perioden?

Vollständige Korrelations-Daten siehe `05_index_purity.csv`.
