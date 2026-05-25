# Future Investigations

> **Living document.** Open detail questions from the research phase that
> aren't blocking but should be tracked. Convention: append new items;
> on resolution add a status-update, don't delete.

---

## I-001 — Why does Lithium (LIT) help Tech-sector assets?

**Status:** 📥 open

**Background:** Broad-Universe analysis showed Lithium delivers mean Δr² =
+0.019 for Technology (236 stocks) — second only to xl_industrials.
Counterintuitive: I expected Lithium to be niche to battery/auto stocks.

**Hypotheses:**
1. EV/clean-tech cluster overlap (TSLA + chip suppliers like NVDA-Auto)
2. Lithium ETF (LIT) is 30% China — correlated with Asia-tech-exposed names
3. Lithium-related stocks in the Technology classification (battery
   software, EV-stack chip designers)
4. LIT is high-volatility correlation with growth/momentum styles

**Method:** per-sub-industry decomposition + cross-correlation with SOXX/QQQ.

**Effort:** ~1-2h

---

## I-002 — Survivorship Bias in Broad Universe

**Status:** 📥 known limitation, 📥 unmitigated

**Background:** Broad-universe constituents come from NASDAQ-screener's
TODAY snapshot. Delisted stocks (Lehman, SVB, Bed Bath & Beyond, etc.)
are missing. Performance statistics are systematically optimistic-biased.

**Mitigation options:**
1. Accept + document (current — this is research, not strategy backtest)
2. Buy CRSP survivorship-bias-free data (~$5-15k/year)
3. DIY reconstitution from Wikipedia + SEC EDGAR diffs (~1 week)

---

## I-003 — Asymmetric Stress Correlations

**Status:** 📥 open

**Background:** Factor correlation matrices (from Analysis 1) are full-period
means. In crisis periods (COVID-March-2020, SVB-March-2023, Russia-Feb-2022)
correlation structure changes dramatically ("everything correlates to 1.0
when liquidity disappears").

**Method:** VIX-quintile-stratified correlation matrices; DCC-GARCH for
top factor pairs.

**Effort:** ~1-2 days (real research)

---

## I-004 — Cross-Factor Interactions on Multi-Event Days

**Status:** 📥 open

**Background:** When FOMC + CPI release on the same day, the market move
isn't the sum of individual-event effects. Pipeline currently treats
events sequentially.

**Method:** identify historical multi-event days, compare actual factor
move to sum-of-individual-predictions, model interaction terms.

**Effort:** ~2-3 days (requires historical event database)

---

## I-005 — Sub-Factor Expansion for fundamentally_different Proxies

**Status:** 🚧 partially addressed

**Background:** Analysis 5 found 3 proxies as `fundamentally_different`:
inflation (TIP-IEF), xl_healthcare (XLV), china_exposure (FXI). The latter
two were mitigated by adding sector-conditional `biotech` (IBB) and
`china_a_shares` (ASHR). But `inflation` still has the TIP-IEF vs
VTIP-IEF gap.

**Open:** add `inflation_short` (VTIP-IEF) as a separate factor and let
analysts choose which inflation concept they need.

---

## I-006 — Index-Purity for the V3.4 New Factors

**Status:** 📥 open

**Background:** Analysis 5 was run on the V3.3 catalog (18 factors). The
6 new V3.4 factors (lithium, uranium, gold, copper, natural_gas, defense)
haven't been Index-Purity-tested yet.

**Method:** extend `FACTOR_ALTERNATIVES` in `analysis/index_purity.py`
with alternatives for each new factor (e.g. LIT vs BATT vs DRIV; URA vs
URNM; GLD vs IAU; CPER vs JJC; UNG vs FCG; ITA vs PPA).

**Effort:** ~1h script + 2 min run

---

## I-007 — Out-of-Sample R² Validation

**Status:** 📥 open

**Background:** All R² reported in this repo is **in-sample**. For
predictive use, we need out-of-sample R² — train on window-1, test on
following window.

**Method:** extend `exposure/pipeline.py` to compute OOS R² in addition
to IS R². Could use the next 21 trading days after the window as the
test set.

**Effort:** ~4-6h

---

## I-008 — Block-Length Adaptive Selection

**Status:** 📥 open, low priority

**Background:** Stationary block-bootstrap uses fixed mean block length =
10 days. Politis & Romano have a procedure to estimate optimal block
length from autocorrelation structure.

**Method:** implement Politis-White (2004) automatic-block-length
estimator. Compare CIs.

**Effort:** ~1-2 days

---

## I-009 — Pre-Compute Trust-Stratified R² as DB Columns

**Status:** 📥 open, design question

**Background:** Currently Analysis 6 re-runs all three regressions per
asset×snapshot. If the pipeline persisted `r_squared_direct` and
`r_squared_+statistical` as columns alongside `r_squared`, downstream
consumers (e.g. Asset-Quality-Tier) could just read them.

**Trade-off:** more storage per row, but cleaner downstream code.

---

## I-010 — Migrate to Alpha Vantage / Polygon (Beyond yfinance)

**Status:** 📥 open

**Background:** yfinance is great for research but has rate limits,
occasional bad data, and depends on Yahoo's tolerance. For more serious
work, a paid feed (Alpha Vantage, Polygon, IEX Cloud) would be more
reliable.

**Effort:** ~3-5 days depending on provider API quality

---

## Closed / Resolved

(none yet)
