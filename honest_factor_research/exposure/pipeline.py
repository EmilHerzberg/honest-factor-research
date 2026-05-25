"""Rolling Ridge factor-exposure pipeline (standalone, no-DB).

Top-level API:

* :class:`FactorExposurePipeline` — construct once with the factor catalog +
  asset returns, then call :meth:`fit_one` per (symbol, window_end).
* :meth:`fit_monthly_snapshots` — convenience iterator over month-end snapshots
  for a list of symbols.

For each (asset, window_end):

  1. Filter factors by ``applicable_sectors`` matching ``asset.sector``
     (Mitigation 2G — see ``METHODOLOGY.md``).
  2. Slice the 252-day window of asset+factor returns. Sector-heuristic
     fallback if window is too short.
  3. ``RidgeCV(alphas)`` fits the unconditional regression. R²-fallback if
     fit is too weak (default R² < 0.20).
  4. Stationary block-bootstrap (200 resamples by default) for per-factor
     stderr AND R²-CI (p05, p95).
  5. Re-fit Ridge with the CV-selected α on VIX-stratified subsets (low/high)
     of the window. Skipped if subset < 60 days.
  6. Emit one :class:`ExposureRow` per applicable factor.

Output is a list of :class:`ExposureRow` — caller persists however they like
(in-memory DataFrame, parquet, SQLite, etc.).
"""

from __future__ import annotations

import logging
import math
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge, RidgeCV  # type: ignore[import-untyped]

from honest_factor_research.exposure.bootstrap import bootstrap_with_r2_ci
from honest_factor_research.exposure.models import ExposureRow
from honest_factor_research.exposure.regime import compute_regime_betas
from honest_factor_research.returns.load import FactorSpec, load_factor_catalog, load_factor_returns

logger = logging.getLogger(__name__)


DEFAULT_WINDOW_DAYS = 252
DEFAULT_RIDGE_ALPHAS: tuple[float, ...] = (0.01, 0.05, 0.1)
DEFAULT_BOOTSTRAP_SAMPLES = 200
R2_FALLBACK_THRESHOLD = 0.20


@dataclass
class FactorExposurePipeline:
    """Standalone rolling-Ridge factor-exposure pipeline.

    Construct once per analysis run with the factor catalog + snapshot path;
    re-use the cached factor_returns and asset_returns across many fit
    calls. The pipeline does NOT touch a database — all output is returned
    as :class:`ExposureRow` instances for the caller to persist.

    Args:
        factor_returns: wide residualized factor-return DataFrame
            (output of :func:`load_factor_returns`). One column per factor_id.
        asset_returns: wide asset-return DataFrame, one column per ticker.
        factor_catalog: list of :class:`FactorSpec` (output of
            :func:`load_factor_catalog`). Used for ``applicable_sectors``
            filtering.
        vix_levels: optional VIX-spot Series (NOT log-returns) — used for
            regime-stratified beta refits. If None, regime computation is
            skipped.
        window_days: rolling-window length (default 252 trading-days).
        ridge_alphas: candidate α for RidgeCV.
        bootstrap_samples: number of stationary-block-bootstrap resamples
            for stderr + R²-CI (default 200; bump to 500 for tighter CI).
        random_seed: for deterministic bootstrap reproducibility.
        sector_lookup: optional dict ``{symbol: GICS-sector-string}`` for
            sector-conditional filtering. If empty, all factors are loaded
            for all assets (no Mitigation 2G).
    """

    factor_returns: pd.DataFrame
    asset_returns: pd.DataFrame
    factor_catalog: list[FactorSpec]
    vix_levels: pd.Series | None = None
    window_days: int = DEFAULT_WINDOW_DAYS
    ridge_alphas: tuple[float, ...] = DEFAULT_RIDGE_ALPHAS
    bootstrap_samples: int = DEFAULT_BOOTSTRAP_SAMPLES
    random_seed: int = 42
    sector_lookup: dict[str, str | None] = field(default_factory=dict)

    @classmethod
    def from_snapshot(
        cls,
        factor_etfs_snapshot: Path | str,
        asset_returns: pd.DataFrame,
        sector_lookup: dict[str, str | None] | None = None,
        catalog_path: Path | str | None = None,
        vix_symbol: str = "^VIX",
        **kwargs,
    ) -> FactorExposurePipeline:
        """Convenience constructor: load everything from disk in one call.

        Args:
            factor_etfs_snapshot: path to the long-format OHLCV parquet
                containing all factor ETFs.
            asset_returns: wide log-returns DataFrame for the assets you
                want to compute exposures for.
            sector_lookup: ``{symbol: sector}`` for Mitigation 2G. Empty
                ⇒ all factors applied to all assets.
            catalog_path: optional override of the bundled factors.yaml.
            vix_symbol: symbol to use for regime stratification (default ``^VIX``).
            **kwargs: forwarded to :class:`FactorExposurePipeline` constructor.
        """
        from honest_factor_research.data.snapshot import load_vix_levels

        catalog = load_factor_catalog(catalog_path)
        factor_returns = load_factor_returns(factor_etfs_snapshot, catalog_path)
        vix_levels = load_vix_levels(factor_etfs_snapshot, vix_symbol)
        return cls(
            factor_returns=factor_returns,
            asset_returns=asset_returns,
            factor_catalog=catalog,
            vix_levels=vix_levels,
            sector_lookup=sector_lookup or {},
            **kwargs,
        )

    # ── filtering ──────────────────────────────────────────────────

    def _applicable_factors_for(self, symbol: str) -> list[FactorSpec]:
        """Return factor specs that apply to ``symbol`` (Mitigation 2G)."""
        asset_sector = self.sector_lookup.get(symbol)
        kept = []
        for spec in self.factor_catalog:
            if not spec.applicable_sectors:
                kept.append(spec)  # universal
                continue
            if asset_sector and asset_sector in spec.applicable_sectors:
                kept.append(spec)
        return kept

    # ── core fit ───────────────────────────────────────────────────

    def fit_one(self, symbol: str, window_end: date) -> list[ExposureRow]:
        """Compute factor exposures for one asset at one window_end.

        Returns a list of :class:`ExposureRow` — one per applicable factor.
        Empty list if the asset is missing from ``asset_returns`` or has
        insufficient history.
        """
        if symbol not in self.asset_returns.columns:
            logger.info("Asset %s missing from asset_returns — skipping", symbol)
            return []

        # Filter to applicable factors
        applicable = self._applicable_factors_for(symbol)
        applicable_ids = [s.factor_id for s in applicable]
        if not applicable_ids:
            logger.warning("No applicable factors for %s — skipping", symbol)
            return []

        # Slice the regression window
        window_ts = pd.Timestamp(window_end)
        fr_window_full = self.factor_returns.loc[self.factor_returns.index <= window_ts].tail(self.window_days)
        fr_window = fr_window_full[[c for c in applicable_ids if c in fr_window_full.columns]]
        if fr_window.shape[1] == 0:
            return []
        ar_window = self.asset_returns.loc[self.asset_returns.index <= window_ts, symbol].dropna().tail(self.window_days)

        # Inner-join on the window dates (some ETFs miss days the equity has).
        # Allow ~5% missing-row tolerance — US trading-day calendars and
        # individual ETF holidays don't always align perfectly with the asset.
        joined = pd.concat([ar_window, fr_window], axis=1, sort=True).dropna()
        joined.columns = ["__y__", *fr_window.columns]
        min_aligned = int(self.window_days * 0.95)
        if len(joined) < min_aligned:
            logger.info(
                "%s has %d aligned rows ending %s (<%d minimum) — skipping",
                symbol, len(joined), window_end, min_aligned,
            )
            return []

        # Fit unconditional RidgeCV
        y = joined["__y__"].to_numpy()
        factor_cols = list(fr_window.columns)
        X = joined[factor_cols].to_numpy()
        try:
            ridge_cv = RidgeCV(alphas=list(self.ridge_alphas))
            ridge_cv.fit(X, y)
        except Exception as exc:  # noqa: BLE001
            logger.warning("RidgeCV failed for %s @ %s: %s", symbol, window_end, exc)
            return []
        r_squared = float(ridge_cv.score(X, y))
        lambda_used = float(ridge_cv.alpha_)

        if r_squared < R2_FALLBACK_THRESHOLD:
            logger.info(
                "%s R²=%.3f < %.2f at %s — skipping",
                symbol, r_squared, R2_FALLBACK_THRESHOLD, window_end,
            )
            return []

        # Block-bootstrap: per-factor stderr + R²-CI
        stderr_per_factor, r2_p05, r2_p95 = bootstrap_with_r2_ci(
            X, y, lambda_used,
            n_resamples=self.bootstrap_samples,
            random_seed=self.random_seed,
        )

        # V3.5 regime-switching: refit on VIX-stratified subsets
        regime_results = compute_regime_betas(
            joined, factor_cols, lambda_used, self.vix_levels,
        )

        window_start = joined.index[0].date()
        betas = ridge_cv.coef_.tolist()
        rows: list[ExposureRow] = []
        for col, beta, se in zip(factor_cols, betas, stderr_per_factor):
            se_val: float | None = float(se) if math.isfinite(float(se)) else None
            low_data = regime_results.get("low_vix", {}).get(col)
            high_data = regime_results.get("high_vix", {}).get(col)
            rows.append(ExposureRow(
                symbol=symbol,
                factor_id=col,
                window_start=window_start,
                window_end=window_end,
                n_obs=len(joined),
                exposure_value=float(beta),
                exposure_stderr=se_val,
                r_squared=r_squared,
                ridge_lambda=lambda_used,
                r_squared_p05=r2_p05 if math.isfinite(r2_p05) else None,
                r_squared_p95=r2_p95 if math.isfinite(r2_p95) else None,
                exposure_value_low_vix=low_data[0] if low_data else None,
                r_squared_low_vix=low_data[1] if low_data else None,
                n_obs_low_vix=low_data[2] if low_data else None,
                exposure_value_high_vix=high_data[0] if high_data else None,
                r_squared_high_vix=high_data[1] if high_data else None,
                n_obs_high_vix=high_data[2] if high_data else None,
            ))
        return rows

    # ── batch driver ───────────────────────────────────────────────

    def fit_monthly_snapshots(
        self,
        symbols: Iterable[str],
        start_date: date,
        end_date: date,
    ) -> pd.DataFrame:
        """Run the pipeline over a grid of (symbol, monthly-end) pairs.

        Returns a flat DataFrame with one row per (symbol, factor_id,
        window_end). Use this as the convenient one-shot driver — for
        custom snapshot grids call :meth:`fit_one` directly.
        """
        # Generate month-end snapshot dates from factor_returns index
        factor_dates = pd.DatetimeIndex(self.factor_returns.index).normalize()
        month_ends = pd.date_range(start=start_date, end=end_date, freq="ME")
        snapshot_dates: list[date] = []
        for me in month_ends:
            candidates = factor_dates[factor_dates <= pd.Timestamp(me)]
            if len(candidates) == 0:
                continue
            cand = candidates[-1].date()
            if not snapshot_dates or snapshot_dates[-1] != cand:
                snapshot_dates.append(cand)
        logger.info("Snapshots: %d", len(snapshot_dates))

        all_rows: list[ExposureRow] = []
        symbols = list(symbols)
        for i, symbol in enumerate(symbols, 1):
            for snap in snapshot_dates:
                rows = self.fit_one(symbol, snap)
                all_rows.extend(rows)
            if i % 10 == 0:
                logger.info("%d/%d symbols processed (%d rows so far)",
                            i, len(symbols), len(all_rows))

        # Flatten ExposureRow dataclass to DataFrame
        data = [
            {
                "symbol": r.symbol,
                "factor_id": r.factor_id,
                "window_start": r.window_start,
                "window_end": r.window_end,
                "n_obs": r.n_obs,
                "exposure_value": r.exposure_value,
                "exposure_stderr": r.exposure_stderr,
                "r_squared": r.r_squared,
                "ridge_lambda": r.ridge_lambda,
                "r_squared_p05": r.r_squared_p05,
                "r_squared_p95": r.r_squared_p95,
                "exposure_value_low_vix": r.exposure_value_low_vix,
                "r_squared_low_vix": r.r_squared_low_vix,
                "n_obs_low_vix": r.n_obs_low_vix,
                "exposure_value_high_vix": r.exposure_value_high_vix,
                "r_squared_high_vix": r.r_squared_high_vix,
                "n_obs_high_vix": r.n_obs_high_vix,
            }
            for r in all_rows
        ]
        return pd.DataFrame(data)
