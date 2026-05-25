# Methodology Index

This directory contains the architectural docs for the honest-factor-research
methodology. The main entry point is the top-level
[`METHODOLOGY.md`](../METHODOLOGY.md), which explains the model-honesty
principle.

The docs in this directory are deeper-dives on specific design decisions:

| Doc | Topic |
|---|---|
| [`02-factor-taxonomy.md`](02-factor-taxonomy.md) | DIRECT / STATISTICAL / DERIVED classification of all factors |
| [`03-trust-stratified-r2.md`](03-trust-stratified-r2.md) | The headline R² decomposition methodology |
| [`04-sector-conditional.md`](04-sector-conditional.md) | Mitigation 2G — per-sector factor catalogs |
| [`05-regime-switching.md`](05-regime-switching.md) | VIX-stratified beta computation |
| [`06-fat-tails-mitigation.md`](06-fat-tails-mitigation.md) | Block-bootstrap CI for R² |
| [`risks-and-improvements.md`](risks-and-improvements.md) | Living risk register (5 documented risks + mitigations) |
| [`future-investigations.md`](future-investigations.md) | 10 open research questions for follow-up |

## Reading order suggestion

If you're new to the methodology:

1. Start with [`METHODOLOGY.md`](../METHODOLOGY.md) for the high-level
   "model-honesty" principle.
2. Read [`02-factor-taxonomy.md`](02-factor-taxonomy.md) to understand
   the trust-tier classification.
3. Read [`03-trust-stratified-r2.md`](03-trust-stratified-r2.md) for the
   headline finding.
4. Skim the other docs based on what you want to use.

## Reading order if you want to implement

1. [`02-factor-taxonomy.md`](02-factor-taxonomy.md) — understand the
   factor classification before adding your own.
2. [`04-sector-conditional.md`](04-sector-conditional.md) — understand
   `applicable_sectors` if you want to use Mitigation 2G.
3. [`03-trust-stratified-r2.md`](03-trust-stratified-r2.md) — understand
   the decomposition so you interpret the output correctly.
4. Look at [`../examples/`](../examples/) for working code.

## Reading order if you want to extend

1. [`risks-and-improvements.md`](risks-and-improvements.md) — open issues
   in the current methodology.
2. [`future-investigations.md`](future-investigations.md) — concrete
   research projects worth doing.
3. [`05-regime-switching.md`](05-regime-switching.md) +
   [`06-fat-tails-mitigation.md`](06-fat-tails-mitigation.md) — recent
   additions show how to extend the pipeline with new capabilities.
