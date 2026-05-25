"""VIX-stratified regime-switching beta computation.

The conditional-beta analysis (see ``analysis/conditional_betas.py``) showed
that 18.3% of (asset, factor) pairs have regime-dependent beta with
|t_diff| ≥ 2.5 between high-VIX (>25) and low-VIX (<15) regimes. The static
beta from a full-window Ridge fit is a mean across regimes — in any specific
regime it may be substantially wrong.

This module re-runs Ridge on the VIX-stratified subsets of the window with
the SAME α the unconditional regression chose (CV-tuning per-subset would
make the regimes incomparable).

Skipped when the regime subset has < ``min_obs`` days (default 60) — the
caller falls back to the unconditional ``exposure_value`` in that case.
"""

from __future__ import annotations

import pandas as pd
from sklearn.linear_model import Ridge  # type: ignore[import-untyped]

# VIX-spot thresholds. Days with 15 ≤ VIX ≤ 25 are "neutral" and remain in
# the unconditional regression but are NOT counted toward either subset.
VIX_LOW_THRESHOLD = 15.0
VIX_HIGH_THRESHOLD = 25.0
REGIME_MIN_OBS = 60


def compute_regime_betas(
    joined: pd.DataFrame,
    factor_cols: list[str],
    alpha: float,
    vix_levels: pd.Series | None,
    min_obs: int = REGIME_MIN_OBS,
) -> dict[str, dict[str, tuple[float, float, int]]]:
    """Refit Ridge on VIX-stratified subsets of the window.

    Args:
        joined: design DataFrame with first column ``"__y__"`` (asset returns)
            and remaining columns the residualized factor returns. Index =
            trading days.
        factor_cols: ordered list of factor-id column names (excluding ``__y__``).
        alpha: Ridge α from the unconditional CV fit (held fixed here).
        vix_levels: pd.Series of VIX-spot levels indexed by Date. If None,
            returns an empty dict (no regime computation).
        min_obs: skip regime if subset has fewer than this many days.

    Returns:
        ``{"low_vix": {factor_id: (beta, r_squared, n_obs)}, "high_vix": {…}}``
        with one entry per regime that has ≥ ``min_obs`` qualifying days.
        Empty dict if VIX data unavailable.
    """
    if vix_levels is None:
        return {}

    vix_aligned = vix_levels.reindex(joined.index).dropna()
    valid_idx = joined.index.intersection(vix_aligned.index)
    if len(valid_idx) < min_obs * 2:
        return {}

    masks = {
        "low_vix": vix_aligned.loc[valid_idx] < VIX_LOW_THRESHOLD,
        "high_vix": vix_aligned.loc[valid_idx] > VIX_HIGH_THRESHOLD,
    }
    out: dict[str, dict[str, tuple[float, float, int]]] = {}
    for regime, mask in masks.items():
        n_obs = int(mask.sum())
        if n_obs < min_obs:
            continue
        sub = joined.loc[valid_idx[mask.to_numpy()]]
        if len(sub) < min_obs:
            continue
        y_sub = sub["__y__"].to_numpy()
        X_sub = sub[factor_cols].to_numpy()
        # Need more rows than predictors (+5 safety margin)
        if X_sub.shape[0] <= X_sub.shape[1] + 5:
            continue
        try:
            model = Ridge(alpha=alpha)
            model.fit(X_sub, y_sub)
            r2 = float(model.score(X_sub, y_sub))
            betas = model.coef_
        except Exception:  # noqa: BLE001
            continue
        out[regime] = {
            col: (float(betas[i]), r2, n_obs)
            for i, col in enumerate(factor_cols)
        }
    return out
