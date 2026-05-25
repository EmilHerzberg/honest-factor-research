# Plain-English Guide: Why Honest Factor Models Matter

> This guide is for people who care about how investment models work,
> but don't necessarily speak fluent statistics. No PhD required.

---

## The problem in one paragraph

Imagine someone tells you they've built a great model that explains how
a stock moves. The model says "R² of 0.85" — sounds impressive, right?
85% explained. But there are at least four hidden ways that number can
be misleading: the model might be using a sector ETF that *already
contains* the stock, the same beta might fail completely when markets
get stressed, the proxy might measure something different from what its
name suggests, and the single "R² = 0.85" might secretly span anything
from 0.55 to 0.92 depending on which days you sample.

This project builds tools to detect each of those issues automatically.

---

## Example 1: The sector mirror problem

A model wants to explain ExxonMobil (XOM). It uses the energy sector ETF
XLE as one of its factors. The fit looks great: R² = 0.75.

But here's the catch: **XOM is itself 22% of XLE.** So when you run a
regression of XOM against XLE, you're partly running a regression of XOM
against (0.22 × XOM + 0.78 × other-energy-stocks). The fit "looks good"
because the right-hand side literally contains the left-hand side.

It's not exactly wrong — the model isn't lying about correlation. But
the 0.75 is much less informative than it appears.

This project measures, per stock, **how much of the R² comes from this
kind of self-mirroring** vs. genuinely external factors like Brent oil
prices, interest rates, and credit spreads.

---

## Example 2: Why one beta is not enough

Factor models typically report one beta per (stock, factor) pair —
calculated across the last ~12 months of data.

But the same stock-factor relationship often works very differently in
calm markets than in stress markets:

- In calm markets, General Electric's "value beta" (sensitivity to the
  value factor) is roughly **-0.15** — basically neutral, slightly anti.
- In high-volatility periods (VIX > 25), the same beta jumps to **+2.94**.

That's not noise. That's a structural regime shift. A model that reports
"GE value beta = 1.2" (the average across both regimes) is wrong in
*both* — too high in calm markets, way too low in crisis markets.

This project computes betas separately for high-VIX and low-VIX regimes
and flags pairs with large divergence.

---

## Example 3: Why uncertainty matters

A standard report says: "WMT 2021-02-26 snapshot: R² = 0.64."

Sounds reasonable. But this window includes the COVID-March-2020 crash.
On 2020-03-16, the S&P 500 fell 13% in one day — under a normal-distribution
assumption, this is essentially impossible (probability < 10⁻¹⁶).

The block-bootstrap CI for this same window is **[0.39, 0.82]** — a
spread of 0.43. That means: "Given the data and the fat-tailed days
in this window, the R² could reasonably be anywhere between 0.39 and
0.82."

A single number 0.64 hides this. Reporting both the point and the
interval is more honest.

---

## What "honest" means here

Honest, in this project, means:

- **Don't celebrate every high R².** Decompose it into trustworthy
  components.
- **Mark sector mirrors explicitly.** If the explanation is mostly the
  asset explaining itself via its own sector ETF, say so.
- **Detect unstable factor relationships.** If the beta flips between
  regimes, surface it.
- **Make uncertainty visible.** Report confidence intervals, not just
  point estimates.
- **Prefer robust explanation to pretty-looking precision.** A lower
  number that's actually defensible beats a higher number that hides
  its own fragility.

The core principle: **prefer a lower honest R² over a higher mirror-driven R².**

---

## What this project is NOT

- **Not investment advice.** No buy / sell recommendations. No predictions.
- **Not a trading bot.** No automated execution. No alpha-generation claims.
- **Not a market oracle.** Past correlations don't guarantee future ones.
- **Not a finished product.** It's a research framework / evaluation tool.

If you're looking for "how to make money in stocks", this isn't it.
There are no shortcuts to that here.

---

## What it IS

- **A research framework** — runnable analyses that take real market
  data and produce reports.
- **A model-audit toolkit** — diagnostic tests for sector mirrors,
  regime breaks, proxy contamination, and uncertainty.
- **A reproducibility demonstrator** — everything is built from
  publicly available data; anyone can re-run it.
- **A communication exercise** — showing that complex ML evaluation
  can be explained at multiple depths.

---

## How to use this guide

If you want to:

- **Understand the philosophy** → keep reading; you're done with this guide.
- **See specific terms defined** → [`glossary.md`](glossary.md).
- **Understand the technical methodology** → [`../METHODOLOGY.md`](../METHODOLOGY.md).
- **Run the analysis yourself** → [`../README.md`](../README.md) Quickstart section.
- **Read the actual research outputs** → [`../reports/`](../reports/).

---

## A final thought

The financial-data community has been good at building factor models for
50+ years. The community has been less good at consistently asking
"how would we know if this model was wrong?"

This project is one small contribution to that question. It doesn't
solve the problem — there are entire research fields dedicated to robust
statistics, regime-switching models, leakage detection, etc. But it
takes the existing tooling, packages it for an applied research context,
and shows that even small empirical audits can change conclusions you
would otherwise have published with confidence.

The same lesson applies to ML systems far outside finance. Any model
that produces a single confidence score risks producing it
overconfidently. Building the habit of asking "how much of this can we
actually defend?" is the broader takeaway.
