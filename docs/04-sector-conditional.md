# Sector-Conditional Factor Architecture (Mitigation 2G)

> **Problem:** adding 12 new sector-specific factors universally would
> bloat the regression for every asset. **Solution:** factors can declare
> ``applicable_sectors: [...]`` and the pipeline only loads them for assets
> whose GICS sector matches.

## The motivation — broad-universe per-sector findings

Analysis 8 (`broad_universe.py`) on 2,241 US stocks measured the marginal
Δr² of each candidate factor — both globally and per GICS sector.

**Pattern that emerged:** several factors are valuable, but their value is
concentrated in specific sectors:

| Factor | Global Mean Δr² | Best sector | Sector Δr² |
|---|---|---|---|
| Gold (GLD) | +0.005 | Basic Materials | **+0.027** |
| Copper (CPER) | +0.004 | Basic Materials | **+0.025** |
| Natural Gas (UNG) | +0.004 | Energy | **+0.019** |
| Uranium (URA) | +0.009 | Energy | **+0.029** |
| Biotech (IBB) | varies | Health Care | substantial |
| Defense (ITA) | varies | Industrials | substantial |

A naive "if it's globally small, skip it" rule would discard these. But
**for the specific assets in those sectors, the factor is essential**.

## Two architectural options

**Option A — Universal:** add every useful factor to the universal catalog.
Every asset gets the full regression with all factors.
- Pro: simple, no per-asset filtering logic
- Con: bloats the regression for assets that don't need the factor;
  Ridge regularization compensates partially but information dilution

**Option B — Sector-Conditional (this repo's choice):** factors can
declare ``applicable_sectors`` and are only loaded for assets whose GICS
sector matches.
- Pro: honest — each asset gets the right factors
- Con: per-asset filtering adds pipeline complexity

## Implementation

In [`config/factors.yaml`](../honest_factor_research/config/factors.yaml):

```yaml
- id: gold
  name: "Gold Spot"
  category: theme
  proxy_etf_symbol: GLD
  proxy_method: returns_regression
  tier: 2
  class: DIRECT
  applicable_sectors:
    - "Basic Materials"
```

In [`honest_factor_research/exposure/pipeline.py`](../honest_factor_research/exposure/pipeline.py):

```python
def _applicable_factors_for(self, symbol: str) -> list[FactorSpec]:
    asset_sector = self.sector_lookup.get(symbol)
    kept = []
    for spec in self.factor_catalog:
        if not spec.applicable_sectors:
            kept.append(spec)  # universal — always include
            continue
        if asset_sector and asset_sector in spec.applicable_sectors:
            kept.append(spec)  # sector matches — include
    return kept
```

A factor with empty `applicable_sectors` (or unset) is **universal** —
applied to all assets. A factor with non-empty list is loaded only when
the asset's sector matches.

## The 6 sector-conditional factors in this repo

| Factor | Proxy | Sectors |
|---|---|---|
| `gold` | GLD | Basic Materials |
| `copper` | CPER | Basic Materials |
| `natural_gas` | UNG | Energy |
| `biotech` | IBB | Health Care |
| `defense` | ITA | Industrials |
| `china_a_shares` | ASHR | Basic Materials, Industrials, Energy |

## What we measured

After implementing Option B, we re-ran Analysis 6 (trust-stratified R²)
on the 60-asset MVP universe:

- Mean r²_direct: **0.351 → 0.432 (+23%)**
- Mean derived_share: **25.3% → 20.3%** (more honest, less mirror)
- HIGH→LOW tier downgrades: **6 → 3** (-50%)

Specific dramatic improvements:
- FCX (copper miner): newly Top-15 with r²_direct=0.605 (Copper + Uranium)
- LIN (industrial gases): newly Top-15 with r²_direct=0.508
- Energy stocks (XOM/COP/SLB/CVX): escaped the Bottom-15 entirely
  (Brent + Uranium working as DIRECT factors)

## When NOT to use this pattern

Don't add sector-conditional factors when:
- The factor improves r²_total but not r²_direct (= it's a mirror artifact)
- The factor's effect is tiny (< 0.01 Δr²) even within its target sector
- The "applicable sector" is so narrow that only 1-2 assets benefit
  (= sample size too small to be statistically meaningful)

## Caveats

- **GICS sector taxonomy is lossy.** Berkshire Hathaway is in "Financial
  Services" but is mostly an insurance + Apple-holdings company. The
  sector-conditional logic uses the sector label as a heuristic.
- **A stock can change sectors.** Real Estate was carved out of
  Financials in 2016. The sector_lookup needs maintenance.
- **Cross-sector themes are not modeled.** A company with significant
  China revenue but classified as Tech wouldn't get `china_a_shares`
  via this mechanism. Would need a separate "China revenue exposure"
  scoring system.
