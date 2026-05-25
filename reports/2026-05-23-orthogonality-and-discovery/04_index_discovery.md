# Analysis 4 — Additional-Index Discovery

**Datum:** 2026-05-23  
**Asset-Universum:** 54 Aktien
**Index-Universum:** 50 ETFs (~46)  
**MVP-Faktor-ETFs:** ['FXI', 'IEF', 'IWD', 'IWF', 'MTUM', 'QUAL', 'SOXX', 'SPY', 'TIP_minus_IEF', 'UUP', 'VXX', 'XLE', 'XLF', 'XLI', 'XLP', 'XLRE', 'XLU', 'XLV']

## Methodik

Pro (Asset, Index)-Paar: univariate OLS-Regression `asset = α + β·index + ε`.
R² zeigt wie viel der Asset-Varianz dieser einzelne Index erklärt.
MVP-Faktor-ETFs sind mit `[MVP]` markiert. Top-3 NICHT-MVP-Kandidaten 
pro Asset sind die spannenden Findings: Indizes die wir aktuell nicht 
nutzen, die aber stark mit der Aktie korrelieren.

## Top-5 Indizes pro Asset (sortiert nach R²)

### `AAPL` — Technology

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLK` (Technology Sector) | sector | 0.735 | +0.969 |  |
| `QQQ` (NASDAQ-100) | broad | 0.711 | +1.037 |  |
| `IWF` (Russell 1000 Growth) | style | 0.705 | +1.081 |  ✅ MVP |
| `SPY` (S&P 500) | broad | 0.628 | +1.190 |  ✅ MVP |
| `IWB` (Russell 1000) | broad | 0.621 | +1.157 |  |

### `ADBE` — Technology

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `QQQ` (NASDAQ-100) | broad | 0.594 | +1.173 |  |
| `XLK` (Technology Sector) | sector | 0.581 | +1.066 |  |
| `IWF` (Russell 1000 Growth) | style | 0.581 | +1.214 |  ✅ MVP |
| `IWB` (Russell 1000) | broad | 0.477 | +1.255 |  |
| `QUAL` (MSCI USA Quality) | style | 0.477 | +1.248 |  ✅ MVP |

### `AMD` — Technology

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `SOXX` (PHLX Semiconductor) | industry | 0.631 | +1.119 |  ✅ MVP |
| `SMH` (VanEck Semiconductors) | industry | 0.629 | +1.136 |  |
| `QQQ` (NASDAQ-100) | broad | 0.544 | +1.502 |  |
| `XLK` (Technology Sector) | sector | 0.532 | +1.364 |  |
| `IWF` (Russell 1000 Growth) | style | 0.505 | +1.513 |  ✅ MVP |

### `AMT` — Real Estate

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLRE` (Real Estate Sector) | sector | 0.692 | +1.008 |  ✅ MVP |
| `USMV` (MSCI USA Min Volatility) | style | 0.458 | +1.165 |  |
| `XLU` (Utilities Sector) | sector | 0.457 | +0.887 |  ✅ MVP |
| `XLV` (Healthcare Sector) | sector | 0.393 | +1.044 |  ✅ MVP |
| `XLP` (Consumer Staples Sector) | sector | 0.371 | +1.099 |  ✅ MVP |

### `AMZN` — Consumer Cyclical

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `QQQ` (NASDAQ-100) | broad | 0.591 | +1.075 |  |
| `XLY` (Consumer Disc Sector) | sector | 0.559 | +1.027 |  |
| `IWF` (Russell 1000 Growth) | style | 0.559 | +1.093 |  ✅ MVP |
| `XLC` (Comm Services Sector) | sector | 0.492 | +1.035 |  |
| `XLK` (Technology Sector) | sector | 0.476 | +0.885 |  |

### `APD` — Basic Materials

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLB` (Materials Sector) | sector | 0.537 | +0.930 |  |
| `IWD` (Russell 1000 Value) | style | 0.436 | +0.957 |  ✅ MVP |
| `USMV` (MSCI USA Min Volatility) | style | 0.427 | +1.120 |  |
| `DIA` (Dow Jones) | broad | 0.408 | +0.937 |  |
| `XLI` (Industrials Sector) | sector | 0.394 | +0.822 |  ✅ MVP |

### `AVGO` — Technology

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `SOXX` (PHLX Semiconductor) | industry | 0.690 | +0.932 |  ✅ MVP |
| `SMH` (VanEck Semiconductors) | industry | 0.680 | +0.940 |  |
| `XLK` (Technology Sector) | sector | 0.601 | +1.154 |  |
| `QQQ` (NASDAQ-100) | broad | 0.571 | +1.225 |  |
| `IWF` (Russell 1000 Growth) | style | 0.556 | +1.264 |  ✅ MVP |

### `BA` — Industrials

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `ITA` (Aerospace & Defense) | industry | 0.682 | +1.540 |  |
| `XLI` (Industrials Sector) | sector | 0.508 | +1.568 |  ✅ MVP |
| `DIA` (Dow Jones) | broad | 0.465 | +1.682 |  |
| `IWN` (Russell 2000 Value) | style | 0.456 | +1.207 |  |
| `MDY` (S&P MidCap 400) | broad | 0.453 | +1.343 |  |

### `BAC` — Financial Services

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLF` (Financials Sector) | sector | 0.843 | +1.238 |  ✅ MVP |
| `KBE` (Big Banks) | industry | 0.789 | +0.871 |  |
| `KRE` (Regional Banks) | industry | 0.755 | +0.795 |  |
| `IWD` (Russell 1000 Value) | style | 0.701 | +1.419 |  ✅ MVP |
| `VLUE` (MSCI USA Value) | style | 0.679 | +1.258 |  |

### `BLK` — Financial Services

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `VTI` (Total Market) | broad | 0.660 | +1.178 |  |
| `IWB` (Russell 1000) | broad | 0.659 | +1.185 |  |
| `QUAL` (MSCI USA Quality) | style | 0.658 | +1.177 |  ✅ MVP |
| `SPY` (S&P 500) | broad | 0.657 | +1.209 |  ✅ MVP |
| `IWD` (Russell 1000 Value) | style | 0.647 | +1.203 |  ✅ MVP |

### `CAT` — Industrials

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLI` (Industrials Sector) | sector | 0.585 | +1.070 |  ✅ MVP |
| `XLB` (Materials Sector) | sector | 0.528 | +0.985 |  |
| `VLUE` (MSCI USA Value) | style | 0.522 | +1.007 |  |
| `IWD` (Russell 1000 Value) | style | 0.515 | +1.110 |  ✅ MVP |
| `IWN` (Russell 2000 Value) | style | 0.505 | +0.807 |  |

### `COF` — Financial Services

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLF` (Financials Sector) | sector | 0.717 | +1.437 |  ✅ MVP |
| `KBE` (Big Banks) | industry | 0.691 | +1.026 |  |
| `KRE` (Regional Banks) | industry | 0.650 | +0.929 |  |
| `IWN` (Russell 2000 Value) | style | 0.634 | +1.247 |  |
| `VLUE` (MSCI USA Value) | style | 0.630 | +1.525 |  |

### `COP` — Energy

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLE` (Energy Sector) | sector | 0.873 | +1.129 |  ✅ MVP |
| `IWD` (Russell 1000 Value) | style | 0.428 | +1.378 |  ✅ MVP |
| `XLF` (Financials Sector) | sector | 0.406 | +1.068 |  ✅ MVP |
| `VLUE` (MSCI USA Value) | style | 0.397 | +1.196 |  |
| `IWN` (Russell 2000 Value) | style | 0.392 | +0.969 |  |

### `COST` — Consumer Defensive

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLP` (Consumer Staples Sector) | sector | 0.457 | +0.964 |  ✅ MVP |
| `QQQ` (NASDAQ-100) | broad | 0.436 | +0.621 |  |
| `IWF` (Russell 1000 Growth) | style | 0.434 | +0.648 |  ✅ MVP |
| `QUAL` (MSCI USA Quality) | style | 0.422 | +0.724 |  ✅ MVP |
| `SPY` (S&P 500) | broad | 0.407 | +0.731 |  ✅ MVP |

### `CRM` — Technology

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `IWF` (Russell 1000 Growth) | style | 0.500 | +1.150 |  ✅ MVP |
| `QQQ` (NASDAQ-100) | broad | 0.490 | +1.088 |  |
| `XLK` (Technology Sector) | sector | 0.484 | +0.993 |  |
| `IWB` (Russell 1000) | broad | 0.436 | +1.225 |  |
| `VTI` (Total Market) | broad | 0.430 | +1.208 |  |

### `CVX` — Energy

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLE` (Energy Sector) | sector | 0.860 | +0.906 |  ✅ MVP |
| `IWD` (Russell 1000 Value) | style | 0.517 | +1.226 |  ✅ MVP |
| `XLF` (Financials Sector) | sector | 0.475 | +0.935 |  ✅ MVP |
| `DIA` (Dow Jones) | broad | 0.464 | +1.176 |  |
| `VLUE` (MSCI USA Value) | style | 0.463 | +1.045 |  |

### `DAL` — Industrials

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `IWN` (Russell 2000 Value) | style | 0.467 | +1.176 |  |
| `ITA` (Aerospace & Defense) | industry | 0.464 | +1.223 |  |
| `XLI` (Industrials Sector) | sector | 0.464 | +1.442 |  ✅ MVP |
| `IJR` (S&P SmallCap 600) | broad | 0.454 | +1.211 |  |
| `MDY` (S&P MidCap 400) | broad | 0.449 | +1.288 |  |

### `DLTR` — Consumer Defensive

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLY` (Consumer Disc Sector) | sector | 0.168 | +0.627 |  |
| `MDY` (S&P MidCap 400) | broad | 0.168 | +0.640 |  |
| `XLP` (Consumer Staples Sector) | sector | 0.167 | +0.966 |  ✅ MVP |
| `IWD` (Russell 1000 Value) | style | 0.164 | +0.773 |  ✅ MVP |
| `DIA` (Dow Jones) | broad | 0.162 | +0.778 |  |

### `DUK` — Utilities

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLU` (Utilities Sector) | sector | 0.838 | +0.968 |  ✅ MVP |
| `USMV` (MSCI USA Min Volatility) | style | 0.535 | +1.014 |  |
| `XLP` (Consumer Staples Sector) | sector | 0.513 | +1.041 |  ✅ MVP |
| `XLRE` (Real Estate Sector) | sector | 0.508 | +0.696 |  ✅ MVP |
| `IWD` (Russell 1000 Value) | style | 0.428 | +0.767 |  ✅ MVP |

### `ESTC` — Technology

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `ARKK` (ARK Innovation) | theme | 0.455 | +0.838 |  |
| `IWO` (Russell 2000 Growth) | style | 0.327 | +1.205 |  |
| `IWF` (Russell 1000 Growth) | style | 0.326 | +1.384 |  ✅ MVP |
| `QQQ` (NASDAQ-100) | broad | 0.317 | +1.306 |  |
| `XLY` (Consumer Disc Sector) | sector | 0.292 | +1.232 |  |

### `FCX` — Basic Materials

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLB` (Materials Sector) | sector | 0.594 | +1.638 |  |
| `EEM` (Emerging Markets) | geo | 0.478 | +1.567 |  |
| `MDY` (S&P MidCap 400) | broad | 0.471 | +1.365 |  |
| `IWD` (Russell 1000 Value) | style | 0.452 | +1.632 |  ✅ MVP |
| `VLUE` (MSCI USA Value) | style | 0.451 | +1.467 |  |

### `GE` — Industrials

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLI` (Industrials Sector) | sector | 0.555 | +1.263 |  ✅ MVP |
| `ITA` (Aerospace & Defense) | industry | 0.521 | +1.037 |  |
| `VLUE` (MSCI USA Value) | style | 0.486 | +1.177 |  |
| `IWD` (Russell 1000 Value) | style | 0.485 | +1.306 |  ✅ MVP |
| `XLF` (Financials Sector) | sector | 0.477 | +1.031 |  ✅ MVP |

### `GOOGL` — Communication Services

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLC` (Comm Services Sector) | sector | 0.713 | +1.126 |  |
| `QQQ` (NASDAQ-100) | broad | 0.638 | +1.010 |  |
| `IWF` (Russell 1000 Growth) | style | 0.627 | +1.047 |  ✅ MVP |
| `XLK` (Technology Sector) | sector | 0.569 | +0.876 |  |
| `SPY` (S&P 500) | broad | 0.557 | +1.151 |  ✅ MVP |

### `GS` — Financial Services

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLF` (Financials Sector) | sector | 0.760 | +1.090 |  ✅ MVP |
| `IWD` (Russell 1000 Value) | style | 0.666 | +1.282 |  ✅ MVP |
| `VLUE` (MSCI USA Value) | style | 0.655 | +1.145 |  |
| `DIA` (Dow Jones) | broad | 0.655 | +1.288 |  |
| `KBE` (Big Banks) | industry | 0.645 | +0.731 |  |

### `HD` — Consumer Cyclical

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `DIA` (Dow Jones) | broad | 0.568 | +1.060 |  |
| `IWB` (Russell 1000) | broad | 0.554 | +1.008 |  |
| `USMV` (MSCI USA Min Volatility) | style | 0.551 | +1.219 |  |
| `VTI` (Total Market) | broad | 0.549 | +0.997 |  |
| `SPY` (S&P 500) | broad | 0.546 | +1.024 |  ✅ MVP |

### `JNJ` — Healthcare

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLV` (Healthcare Sector) | sector | 0.545 | +0.788 |  ✅ MVP |
| `XLP` (Consumer Staples Sector) | sector | 0.452 | +0.778 |  ✅ MVP |
| `USMV` (MSCI USA Min Volatility) | style | 0.428 | +0.722 |  |
| `DIA` (Dow Jones) | broad | 0.358 | +0.565 |  |
| `XLU` (Utilities Sector) | sector | 0.349 | +0.497 |  ✅ MVP |

### `JPM` — Financial Services

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLF` (Financials Sector) | sector | 0.847 | +1.130 |  ✅ MVP |
| `KBE` (Big Banks) | industry | 0.693 | +0.743 |  |
| `IWD` (Russell 1000 Value) | style | 0.683 | +1.274 |  ✅ MVP |
| `KRE` (Regional Banks) | industry | 0.647 | +0.670 |  |
| `VLUE` (MSCI USA Value) | style | 0.639 | +1.111 |  |

### `KO` — Consumer Defensive

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLP` (Consumer Staples Sector) | sector | 0.683 | +1.019 |  ✅ MVP |
| `USMV` (MSCI USA Min Volatility) | style | 0.579 | +0.895 |  |
| `IWD` (Russell 1000 Value) | style | 0.499 | +0.702 |  ✅ MVP |
| `DIA` (Dow Jones) | broad | 0.490 | +0.704 |  |
| `XLU` (Utilities Sector) | sector | 0.488 | +0.626 |  ✅ MVP |

### `LIN` — Basic Materials

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLB` (Materials Sector) | sector | 0.694 | +0.899 |  |
| `IWD` (Russell 1000 Value) | style | 0.579 | +0.938 |  ✅ MVP |
| `DIA` (Dow Jones) | broad | 0.574 | +0.946 |  |
| `SPY` (S&P 500) | broad | 0.568 | +0.927 |  ✅ MVP |
| `USMV` (MSCI USA Min Volatility) | style | 0.564 | +1.096 |  |

### `LLY` — Healthcare

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLV` (Healthcare Sector) | sector | 0.360 | +1.050 |  ✅ MVP |
| `USMV` (MSCI USA Min Volatility) | style | 0.229 | +0.865 |  |
| `QUAL` (MSCI USA Quality) | style | 0.198 | +0.660 |  ✅ MVP |
| `MTUM` (MSCI USA Momentum) | style | 0.197 | +0.591 |  ✅ MVP |
| `XLP` (Consumer Staples Sector) | sector | 0.187 | +0.820 |  ✅ MVP |

### `LSCC` — Technology

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `SOXX` (PHLX Semiconductor) | industry | 0.644 | +1.154 |  ✅ MVP |
| `SMH` (VanEck Semiconductors) | industry | 0.612 | +1.143 |  |
| `XLK` (Technology Sector) | sector | 0.499 | +1.347 |  |
| `QQQ` (NASDAQ-100) | broad | 0.493 | +1.459 |  |
| `IWF` (Russell 1000 Growth) | style | 0.469 | +1.489 |  ✅ MVP |

### `MCD` — Consumer Cyclical

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `DIA` (Dow Jones) | broad | 0.531 | +0.822 |  |
| `USMV` (MSCI USA Min Volatility) | style | 0.519 | +0.949 |  |
| `IWD` (Russell 1000 Value) | style | 0.476 | +0.768 |  ✅ MVP |
| `XLI` (Industrials Sector) | sector | 0.443 | +0.669 |  ✅ MVP |
| `SPY` (S&P 500) | broad | 0.436 | +0.733 |  ✅ MVP |

### `META` — Communication Services

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLC` (Comm Services Sector) | sector | 0.690 | +1.547 |  |
| `QQQ` (NASDAQ-100) | broad | 0.495 | +1.242 |  |
| `IWF` (Russell 1000 Growth) | style | 0.469 | +1.264 |  ✅ MVP |
| `XLK` (Technology Sector) | sector | 0.415 | +1.044 |  |
| `QUAL` (MSCI USA Quality) | style | 0.405 | +1.333 |  ✅ MVP |

### `MRNA` — Healthcare

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `IBB` (Biotech Industry) | industry | 0.219 | +1.403 |  |
| `ARKK` (ARK Innovation) | theme | 0.092 | +0.467 |  |
| `QQQ` (NASDAQ-100) | broad | 0.059 | +0.697 |  |
| `IWO` (Russell 2000 Growth) | style | 0.056 | +0.616 |  |
| `MTUM` (MSCI USA Momentum) | style | 0.051 | +0.694 |  ✅ MVP |

### `MSFT` — Technology

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLK` (Technology Sector) | sector | 0.800 | +0.974 |  |
| `QQQ` (NASDAQ-100) | broad | 0.777 | +1.046 |  |
| `IWF` (Russell 1000 Growth) | style | 0.777 | +1.094 |  ✅ MVP |
| `SPY` (S&P 500) | broad | 0.673 | +1.188 |  ✅ MVP |
| `IWB` (Russell 1000) | broad | 0.667 | +1.156 |  |

### `NEE` — Utilities

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLU` (Utilities Sector) | sector | 0.700 | +1.094 |  ✅ MVP |
| `USMV` (MSCI USA Min Volatility) | style | 0.443 | +1.142 |  |
| `XLRE` (Real Estate Sector) | sector | 0.405 | +0.769 |  ✅ MVP |
| `XLP` (Consumer Staples Sector) | sector | 0.371 | +1.095 |  ✅ MVP |
| `IWD` (Russell 1000 Value) | style | 0.340 | +0.845 |  ✅ MVP |

### `NFLX` — Communication Services

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLC` (Comm Services Sector) | sector | 0.354 | +1.144 |  |
| `QQQ` (NASDAQ-100) | broad | 0.337 | +1.058 |  |
| `IWF` (Russell 1000 Growth) | style | 0.307 | +1.056 |  ✅ MVP |
| `ARKK` (ARK Innovation) | theme | 0.288 | +0.524 |  |
| `XLK` (Technology Sector) | sector | 0.266 | +0.863 |  |

### `NKE` — Consumer Cyclical

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `QUAL` (MSCI USA Quality) | style | 0.427 | +1.057 |  ✅ MVP |
| `XLY` (Consumer Disc Sector) | sector | 0.412 | +0.859 |  |
| `VTI` (Total Market) | broad | 0.400 | +1.022 |  |
| `IWB` (Russell 1000) | broad | 0.399 | +1.026 |  |
| `SPY` (S&P 500) | broad | 0.396 | +1.046 |  ✅ MVP |

### `NVDA` — Technology

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `SMH` (VanEck Semiconductors) | industry | 0.750 | +1.267 |  |
| `SOXX` (PHLX Semiconductor) | industry | 0.699 | +1.204 |  ✅ MVP |
| `XLK` (Technology Sector) | sector | 0.668 | +1.561 |  |
| `QQQ` (NASDAQ-100) | broad | 0.658 | +1.688 |  |
| `IWF` (Russell 1000 Growth) | style | 0.634 | +1.733 |  ✅ MVP |

### `O` — Real Estate

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLRE` (Real Estate Sector) | sector | 0.613 | +1.000 |  ✅ MVP |
| `IWD` (Russell 1000 Value) | style | 0.466 | +1.046 |  ✅ MVP |
| `MDY` (S&P MidCap 400) | broad | 0.450 | +0.842 |  |
| `USMV` (MSCI USA Min Volatility) | style | 0.441 | +1.205 |  |
| `DIA` (Dow Jones) | broad | 0.433 | +1.021 |  |

### `ORCL` — Technology

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLK` (Technology Sector) | sector | 0.380 | +0.716 |  |
| `SPY` (S&P 500) | broad | 0.378 | +0.949 |  ✅ MVP |
| `IWB` (Russell 1000) | broad | 0.374 | +0.923 |  |
| `QUAL` (MSCI USA Quality) | style | 0.374 | +0.918 |  ✅ MVP |
| `VTI` (Total Market) | broad | 0.364 | +0.905 |  |

### `PFE` — Healthcare

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLV` (Healthcare Sector) | sector | 0.355 | +0.890 |  ✅ MVP |
| `USMV` (MSCI USA Min Volatility) | style | 0.251 | +0.772 |  |
| `XLP` (Consumer Staples Sector) | sector | 0.223 | +0.764 |  ✅ MVP |
| `IWD` (Russell 1000 Value) | style | 0.212 | +0.600 |  ✅ MVP |
| `DIA` (Dow Jones) | broad | 0.207 | +0.601 |  |

### `PG` — Consumer Defensive

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLP` (Consumer Staples Sector) | sector | 0.732 | +1.056 |  ✅ MVP |
| `USMV` (MSCI USA Min Volatility) | style | 0.466 | +0.804 |  |
| `XLU` (Utilities Sector) | sector | 0.429 | +0.587 |  ✅ MVP |
| `XLV` (Healthcare Sector) | sector | 0.422 | +0.740 |  ✅ MVP |
| `DIA` (Dow Jones) | broad | 0.345 | +0.592 |  |

### `PLD` — Real Estate

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLRE` (Real Estate Sector) | sector | 0.760 | +1.095 |  ✅ MVP |
| `USMV` (MSCI USA Min Volatility) | style | 0.551 | +1.324 |  |
| `IWB` (Russell 1000) | broad | 0.505 | +1.045 |  |
| `IWD` (Russell 1000 Value) | style | 0.501 | +1.067 |  ✅ MVP |
| `VTI` (Total Market) | broad | 0.498 | +1.031 |  |

### `SLB` — Energy

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLE` (Energy Sector) | sector | 0.786 | +1.196 |  ✅ MVP |
| `IWN` (Russell 2000 Value) | style | 0.424 | +1.124 |  |
| `IWD` (Russell 1000 Value) | style | 0.407 | +1.501 |  ✅ MVP |
| `XLF` (Financials Sector) | sector | 0.406 | +1.193 |  ✅ MVP |
| `VLUE` (MSCI USA Value) | style | 0.403 | +1.345 |  |

### `SMCI` — Technology

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `SMH` (VanEck Semiconductors) | industry | 0.224 | +0.982 |  |
| `SOXX` (PHLX Semiconductor) | industry | 0.221 | +0.960 |  ✅ MVP |
| `XLK` (Technology Sector) | sector | 0.180 | +1.148 |  |
| `QUAL` (MSCI USA Quality) | style | 0.172 | +1.454 |  ✅ MVP |
| `IWF` (Russell 1000 Growth) | style | 0.170 | +1.271 |  ✅ MVP |

### `SO` — Utilities

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLU` (Utilities Sector) | sector | 0.839 | +1.038 |  ✅ MVP |
| `USMV` (MSCI USA Min Volatility) | style | 0.529 | +1.082 |  |
| `XLP` (Consumer Staples Sector) | sector | 0.495 | +1.097 |  ✅ MVP |
| `XLRE` (Real Estate Sector) | sector | 0.478 | +0.724 |  ✅ MVP |
| `IWD` (Russell 1000 Value) | style | 0.426 | +0.820 |  ✅ MVP |

### `TMUS` — Communication Services

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `USMV` (MSCI USA Min Volatility) | style | 0.364 | +0.929 |  |
| `SPY` (S&P 500) | broad | 0.330 | +0.746 |  ✅ MVP |
| `IWB` (Russell 1000) | broad | 0.327 | +0.726 |  |
| `VTI` (Total Market) | broad | 0.324 | +0.718 |  |
| `DIA` (Dow Jones) | broad | 0.323 | +0.749 |  |

### `TSLA` — Consumer Cyclical

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLY` (Consumer Disc Sector) | sector | 0.465 | +1.744 |  |
| `ARKK` (ARK Innovation) | theme | 0.449 | +0.934 |  |
| `QQQ` (NASDAQ-100) | broad | 0.362 | +1.567 |  |
| `IWF` (Russell 1000 Growth) | style | 0.337 | +1.581 |  ✅ MVP |
| `MTUM` (MSCI USA Momentum) | style | 0.291 | +1.497 |  ✅ MVP |

### `TTWO` — Technology

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `QQQ` (NASDAQ-100) | broad | 0.277 | +0.709 |  |
| `XLC` (Comm Services Sector) | sector | 0.274 | +0.743 |  |
| `IWF` (Russell 1000 Growth) | style | 0.263 | +0.722 |  ✅ MVP |
| `XLK` (Technology Sector) | sector | 0.242 | +0.608 |  |
| `ARKK` (ARK Innovation) | theme | 0.233 | +0.348 |  |

### `UNH` — Healthcare

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLV` (Healthcare Sector) | sector | 0.561 | +1.223 |  ✅ MVP |
| `DIA` (Dow Jones) | broad | 0.458 | +0.977 |  |
| `USMV` (MSCI USA Min Volatility) | style | 0.434 | +1.112 |  |
| `IWD` (Russell 1000 Value) | style | 0.373 | +0.871 |  ✅ MVP |
| `SPY` (S&P 500) | broad | 0.337 | +0.826 |  ✅ MVP |

### `VLO` — Energy

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLE` (Energy Sector) | sector | 0.669 | +1.074 |  ✅ MVP |
| `IWN` (Russell 2000 Value) | style | 0.390 | +1.050 |  |
| `IWD` (Russell 1000 Value) | style | 0.389 | +1.428 |  ✅ MVP |
| `VLUE` (MSCI USA Value) | style | 0.384 | +1.279 |  |
| `XLF` (Financials Sector) | sector | 0.383 | +1.128 |  ✅ MVP |

### `WMT` — Consumer Defensive

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLP` (Consumer Staples Sector) | sector | 0.421 | +0.864 |  ✅ MVP |
| `USMV` (MSCI USA Min Volatility) | style | 0.247 | +0.631 |  |
| `DIA` (Dow Jones) | broad | 0.195 | +0.480 |  |
| `XLV` (Healthcare Sector) | sector | 0.194 | +0.542 |  ✅ MVP |
| `SPY` (S&P 500) | broad | 0.191 | +0.468 |  ✅ MVP |

### `XOM` — Energy

| Index | Category | R² | β | MVP? |
|---|---|---|---|---|
| `XLE` (Energy Sector) | sector | 0.875 | +0.877 |  ✅ MVP |
| `IWD` (Russell 1000 Value) | style | 0.440 | +1.084 |  ✅ MVP |
| `VLUE` (MSCI USA Value) | style | 0.410 | +0.943 |  |
| `XLF` (Financials Sector) | sector | 0.400 | +0.822 |  ✅ MVP |
| `IWN` (Russell 2000 Value) | style | 0.399 | +0.758 |  |

## ⭐ Top NICHT-MVP Index-Empfehlungen (über alle Assets)

Welche Indizes haben das höchste R² bei den meisten Assets, die NICHT bereits Faktor sind?

| Rank | Index | Category | Mean R² über alle 60 Assets | Hypothese |
|---|---|---|---|---|
| 1 | `IWB` (Russell 1000) | broad | 0.373 | Add as candidate broad factor |
| 2 | `VTI` (Total Market) | broad | 0.372 | Add as candidate broad factor |
| 3 | `DIA` (Dow Jones) | broad | 0.366 | Add as candidate broad factor |
| 4 | `USMV` (MSCI USA Min Volatility) | style | 0.346 | Add as candidate style factor |
| 5 | `VLUE` (MSCI USA Value) | style | 0.342 | Alternative Value-Faktor |
| 6 | `MDY` (S&P MidCap 400) | broad | 0.335 | Add as candidate broad factor |
| 7 | `XLB` (Materials Sector) | sector | 0.315 | Add as candidate sector factor |
| 8 | `QQQ` (NASDAQ-100) | broad | 0.310 | Add as candidate broad factor |
| 9 | `XLK` (Technology Sector) | sector | 0.309 | Tech-Sector-Faktor (zusätzlich zu Style) |
| 10 | `IWM` (Russell 2000) | broad | 0.303 | Add as candidate broad factor |
| 11 | `XLY` (Consumer Disc Sector) | sector | 0.300 | Consumer-Disc-Sector-Faktor |
| 12 | `IJR` (S&P SmallCap 600) | broad | 0.294 | Add as candidate broad factor |
| 13 | `IWN` (Russell 2000 Value) | style | 0.290 | Add as candidate style factor |
| 14 | `IWO` (Russell 2000 Growth) | style | 0.289 | Add as candidate style factor |
| 15 | `XLC` (Comm Services Sector) | sector | 0.280 | Comm-Services-Sector |

## Asset-spezifische Empfehlungen (R² ≥ 0.3 bei nicht-MVP)

| Asset | Sector | Empfohlener neuer Index | R² | Verbesserung über bestes MVP |
|---|---|---|---|---|
| `APD` | Basic Materials | `XLB` (Materials Sector) | 0.537 | +0.100 |
| `BA` | Industrials | `ITA` (Aerospace & Defense) | 0.682 | +0.174 |
| `ESTC` | Technology | `ARKK` (ARK Innovation) | 0.455 | +0.130 |
| `FCX` | Basic Materials | `XLB` (Materials Sector) | 0.594 | +0.141 |
| `GOOGL` | Communication Services | `XLC` (Comm Services Sector) | 0.713 | +0.086 |
| `LIN` | Basic Materials | `XLB` (Materials Sector) | 0.694 | +0.115 |
| `MCD` | Consumer Cyclical | `DIA` (Dow Jones) | 0.531 | +0.055 |
| `META` | Communication Services | `XLC` (Comm Services Sector) | 0.690 | +0.221 |
| `NVDA` | Technology | `SMH` (VanEck Semiconductors) | 0.750 | +0.052 |
| `TSLA` | Consumer Cyclical | `XLY` (Consumer Disc Sector) | 0.465 | +0.128 |

## Detailed Data

- Vollständige Beta-Matrix: `04_index_discovery_betas.csv`
- Vollständige R²-Matrix: `04_index_discovery_r_squared.csv`
