"""Data classes for factor-exposure output rows."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class ExposureRow:
    """In-memory representation of one (asset, factor, window_end) exposure.

    The pipeline emits a list of these per (asset, window_end). Callers
    persist them however they want (parquet, SQLite, Postgres, in-memory…).

    Fields:
        symbol: asset ticker, e.g. ``"AAPL"``
        factor_id: factor slug, e.g. ``"rates"``
        window_start / window_end: regression window boundary trading-days
        n_obs: number of joint asset-factor observations in the window
               (after dropping NaN rows)

        # ─── Core regression output ─────────────────────────────────
        exposure_value: unconditional Ridge beta on the 252-day window
        exposure_stderr: bootstrap stderr of beta (None if bootstrap failed)
        r_squared: in-sample R² of the unconditional regression
        ridge_lambda: CV-selected α from RidgeCV

        # ─── V3.5 R²-CI from stationary block-bootstrap ─────────────
        r_squared_p05: 5th percentile of R² across bootstrap resamples
        r_squared_p95: 95th percentile of R² across bootstrap resamples

        # ─── V3.5 regime-switching betas (VIX-stratified) ───────────
        exposure_value_low_vix / exposure_value_high_vix: beta refit on the
            subset of window days with VIX < 15 / > 25 respectively. None
            when the regime subset has < 60 days (caller falls back to
            unconditional).
        r_squared_low_vix / r_squared_high_vix: R² of the regime fits.
        n_obs_low_vix / n_obs_high_vix: subset sizes.
    """

    symbol: str
    factor_id: str
    window_start: date
    window_end: date
    n_obs: int

    exposure_value: float
    exposure_stderr: float | None
    r_squared: float | None
    ridge_lambda: float | None

    r_squared_p05: float | None = None
    r_squared_p95: float | None = None

    exposure_value_low_vix: float | None = None
    r_squared_low_vix: float | None = None
    n_obs_low_vix: int | None = None
    exposure_value_high_vix: float | None = None
    r_squared_high_vix: float | None = None
    n_obs_high_vix: int | None = None
