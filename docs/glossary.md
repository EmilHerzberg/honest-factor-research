# Glossary

> Terms used throughout this project, with plain-language explanations
> and (where useful) financial examples.

---

**Asset**
A single financial instrument that's traded — most commonly a stock
(e.g. Apple = AAPL). In this project, "asset" usually means one US-listed
stock whose returns we're trying to model.

**Factor**
A common driver that affects many stocks at once. Examples: interest
rates (affects bond-sensitive stocks), oil price (affects energy
stocks), the broad market (affects everything). A factor is typically
represented in code by the returns of an index or ETF that proxies that
underlying driver.

**Factor Model**
A statistical model that explains a stock's daily return as
(weighted sum of factor exposures) + (idiosyncratic noise). If the
factors are well-chosen, most of the stock's day-to-day movement can be
attributed to them; the leftover is "stock-specific" noise.

**R² (R-squared)**
The fraction of a stock's return variance that the factor model
explains. Ranges from 0 (no explanation) to 1 (perfect explanation).
A model with R²=0.6 explains 60% of the stock's variance; the other 40%
is idiosyncratic. *In this project, we argue that this single number
hides a lot of important detail — see "Honest R²" below.*

**Honest R² / Trust-Stratified R²**
The same R² split into three parts based on which kinds of factors
contributed:
- `r²_direct` (from real-world-priced factors like rates, VIX, Brent)
- `r²_+statistical` (the above + academic style factors like value, momentum)
- `r²_total` (the above + sector basket factors that might be self-mirroring)

A high `r²_total` with most of the gap concentrated in the `DERIVED`
tier is a yellow flag — see "Mirror artifact" below.

**Beta**
The model's estimated weight on one specific factor for one specific
stock. If XOM has rates_beta = -0.5, the model believes XOM tends to
fall by 0.5% when rates rise by 1% (oversimplified). Beta is the unit
of "factor sensitivity."

**Regime**
A market period with statistically similar properties — e.g. "high-VIX"
periods (Mar 2020, late 2022) vs "low-VIX" periods (most of 2017, 2019,
mid-2024). Different regimes can have very different beta structures.

**VIX**
The Cboe Volatility Index — a real-time measure of expected S&P 500
volatility for the next 30 days. Below 15 = calm markets; above 25 =
stressed; above 40 = crisis. We use VIX levels to define market regimes.

**Beta Flip**
The extreme case where a stock's beta to a factor *reverses sign*
between regimes. Example from this project: GE × value beta is +2.94 in
high-VIX days, -0.15 in low-VIX days. A single average across both is
fundamentally misleading.

**Ridge Regression**
A regularized linear regression that shrinks coefficients toward zero
to handle multicollinearity (when multiple factors are correlated with
each other). This project uses `RidgeCV` — Ridge with cross-validated
selection of the regularization strength.

**Cross-Validation (CV)**
A way to pick model hyperparameters (like Ridge's regularization
strength) by splitting the data into multiple train/test folds and
checking which choice generalizes best. Reduces overfitting risk.

**Residualization**
The process of removing one factor's contribution from another factor
before regression. Example: if the broad market goes up, almost every
factor ETF also goes up — so we *first* explain each factor by the
market, then keep only what's left over (the "residual"). This produces
near-orthogonal factors.

**Bootstrap**
A statistical method that estimates uncertainty by resampling the
existing data (with replacement) many times and refitting the model on
each resample. The spread of the resampled results gives a confidence
interval. The "Stationary Block-Bootstrap" used here samples contiguous
blocks of consecutive days, which preserves time-series autocorrelation
that plain row-bootstrap would destroy.

**Confidence Interval (CI)**
A range that likely contains the true value, given uncertainty. A 90%
CI means "if we re-ran this analysis many times, 90% of the resulting
intervals would contain the true value." Wider CI = more uncertainty.

**Sector ETF**
An exchange-traded fund that holds a basket of stocks from one sector.
Example: XLF (Financial Sector ETF) holds banks, insurers, asset
managers, etc. We use sector ETFs as factor proxies — but with caveats
(see "Sector Mirror" and "Mirror artifact" below).

**Proxy Contamination**
When the ETF we're using as a factor proxy doesn't actually measure
what its name suggests. Example: XLV is labeled "Healthcare" but
includes UnitedHealth (a health insurer) at 10% — so it's more like
"healthcare + health insurance" than pure pharma/biotech.

**Mirror Artifact / Sector Mirror**
When a stock is itself a significant constituent of the factor ETF used
to "explain" it. Example: XOM is 22% of XLE, so regressing XOM against
XLE is partly XOM regressed against itself. The resulting R² will be
inflated relative to genuine independent explanation.

**Fat Tails**
The empirical fact that daily-return distributions have more
extreme values than a normal (Gauß) distribution predicts. The
2020-03-16 SPY decline of -13% has probability essentially zero under
Gauß; in reality, days like that happen every few years. Models that
assume Gauß errors (like vanilla Ridge) underestimate uncertainty.

**Rolling Window**
A fixed-length time window (e.g. 252 trading days = ~1 year) that
"rolls" forward through history. At each window-end date, we re-fit the
model on the most recent 252 days. Standard practice in time-series
analysis to allow the model to adapt to changing market conditions.

**Sequential Gram-Schmidt**
The mathematical procedure used here for residualization. Process
factors in tier order; each factor is residualized against all
earlier-tier factors before being added to the model. This produces a
near-orthogonal factor basis where each factor's beta has a clear
interpretation.

**Trust Tier (DIRECT / STATISTICAL / DERIVED)**
The three-class taxonomy this project uses for factors:
- **DIRECT_PHYSICAL** — corresponds to a real-world price or measurable
  macro quantity (rates, inflation, VIX, oil, gold). Event-to-factor
  mechanism is clear.
- **STATISTICAL_FACTOR** — academically-validated factor with long
  history (market_beta, value, momentum, quality).
- **DERIVED_THEME** — heterogeneous sector basket whose contents are
  semantically unclear (XLF, XLV, china_exposure). High risk of mirror
  artifacts.

**Idiosyncratic / Residual Variance**
The portion of a stock's variance that the factor model does NOT
explain — i.e. (1 − R²). Genuinely stock-specific noise: company news,
earnings surprises, individual rumors. A higher idiosyncratic share is
NOT a bug; it just means macro/factor models don't capture this stock
well.

**Survivorship Bias**
The systematic distortion that comes from studying only stocks that
still exist *today*. Delisted stocks (Lehman, Bed Bath & Beyond, SVB)
are missing from the analysis, which makes historical results look
better than they would with the full surviving + delisted population.

**OHLCV**
"Open, High, Low, Close, Volume" — the standard daily data fields for
a traded stock. This project uses Close prices to compute log-returns.

**Log-Return**
The natural-logarithm of the price ratio: `log(P_t / P_{t-1})`.
Mathematically nicer than percent returns because log-returns are
additive over time (you can sum daily log-returns to get a multi-day
log-return).

**Multicollinearity**
When two or more factors are highly correlated with each other (e.g.
SOXX vs QQQ; growth vs market). Causes unstable beta estimates in
regression. This project addresses it via residualization + Ridge
regularization.

**Sequential Block-Bootstrap (Politis-Romano 1994)**
A specific block-bootstrap variant where block lengths are randomly
drawn from a geometric distribution (rather than fixed). Preserves
the stationarity of the underlying time series in the resampled
output. Reference: Politis & Romano (1994), *Journal of the
American Statistical Association*, 89(428), 1303-1313.

**Stationary**
A statistical property where the distribution of values doesn't change
over time. Daily-return *means* are roughly stationary; daily-return
*variances* clearly are not (vol-clustering). Many statistical methods
assume stationarity even when it's not strictly true.

**Autocorrelation**
The correlation of a time series with a lagged version of itself.
Daily returns have low (~0.0-0.05) autocorrelation; daily squared
returns have substantial autocorrelation (vol clustering). Plain
row-bootstrap ignores this; block-bootstrap respects it.
