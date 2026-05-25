"""Sequential Gram-Schmidt residualization for factor returns.

The N factor ETFs we use are heavily multicollinear (SOXX-QQQ ρ≈0.85,
IWF-SPY ρ≈0.70). Running Ridge directly on the raw matrix gives unstable
betas with mixed signs. The Barra-Axioma convention is to *sequentially
residualize* each factor against the already-residualized earlier-tier
factors, producing a near-orthogonal basis.

Order matters: it encodes economic priority. Tier 1 (market) is residualized
against nothing; Tier 2 (macro: rates, inflation, vol, fx) is residualized
against market; Tier 3 (style: value/momentum/quality) against market+rates;
Tier 4 (sector) against market+rates+relevant-style; Tier 5 (geo) against
market+rates+style.

The exact ``residualized_against`` per factor comes from
:func:`load_factor_catalog`. The pipeline is *pure pandas + numpy* — sklearn
not needed for this step.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def residualize_one(y: pd.Series, X: pd.DataFrame) -> pd.Series:
    """OLS-regress ``y`` on ``X`` (with intercept) and return residuals.

    Drops NaN rows from the joint design matrix before fitting. Rows with at
    least one NaN in ``X`` or ``y`` are also NaN in the output. Uses a
    closed-form lstsq solve so this stays pure numpy.

    Returns a Series indexed identically to ``y`` with name preserved.
    """
    if X.shape[1] == 0:
        return y.copy()
    joint = pd.concat([y, X], axis=1).dropna()
    if len(joint) < X.shape[1] + 2:
        logger.warning(
            "Residualization for %s skipped: only %d overlapping rows for %d cols",
            y.name, len(joint), X.shape[1],
        )
        return y.copy()
    Y_arr = joint.iloc[:, 0].to_numpy()
    X_arr = joint.iloc[:, 1:].to_numpy()
    X_design = np.column_stack([np.ones(len(X_arr)), X_arr])
    beta, *_ = np.linalg.lstsq(X_design, Y_arr, rcond=None)
    resid = Y_arr - X_design @ beta
    out = pd.Series(np.nan, index=y.index, name=y.name)
    out.loc[joint.index] = resid
    return out


def build_residualized(
    specs: list,  # list of FactorSpec — typed in load.py
    etf_returns: pd.DataFrame,
) -> pd.DataFrame:
    """Walk specs in tier order; residualize each against its earlier-tier ancestors.

    Args:
        specs: list of :class:`FactorSpec` (from :func:`load_factor_catalog`),
            already sorted by ``(tier, factor_id)``.
        etf_returns: wide log-returns DataFrame with one column per source ETF
            (plus any constructed spread columns).

    Returns:
        DataFrame indexed by Date with one column per ``factor_id``. Tier-1
        columns are the raw returns; tier-N columns are the residuals of
        OLS(factor_return ~ already-residualized [residualized_against]).
    """
    from honest_factor_research.returns.load import raw_factor_series  # noqa: PLC0415

    out = pd.DataFrame(index=etf_returns.index)
    for spec in specs:
        raw = raw_factor_series(spec, etf_returns)
        if not spec.residualized_against:
            out[spec.factor_id] = raw
            continue
        regressors = [r for r in spec.residualized_against if r in out.columns]
        missing = set(spec.residualized_against) - set(regressors)
        if missing:
            raise ValueError(
                f"Factor {spec.factor_id} residualized against {missing} "
                "which are not yet built — check tier order in the catalog."
            )
        X = out[list(regressors)]
        out[spec.factor_id] = residualize_one(raw, X)
    return out
