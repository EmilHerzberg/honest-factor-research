"""Factor catalog loader + residualized-returns assembly.

Top-level API:

* :func:`load_factor_catalog` — parse the YAML catalog into a list of
  :class:`FactorSpec`, sorted by ``(tier, factor_id)``.
* :func:`load_factor_returns` — full pipeline: snapshot → wide log-returns →
  build spread columns → residualize per spec → return wide
  ``DataFrame[Date, factor_id]``.
* :func:`raw_factor_returns` — same but without residualization, for
  diagnostics / lead-lag tests.

The residualization order in the YAML is the single source of truth — change
the YAML, the pipeline picks it up automatically. No order is hardcoded in
Python.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from honest_factor_research.data.snapshot import load_snapshot, long_to_wide_close
from honest_factor_research.returns.residualization import build_residualized

logger = logging.getLogger(__name__)


_SPREAD_INFIX = "_minus_"


@dataclass(frozen=True)
class FactorSpec:
    """One factor's full specification — what to load, how, residualized against what.

    For spread factors (``proxy_method == "spread"``), ``proxy_etf_symbol`` is
    parsed as ``LONG_minus_SHORT`` (e.g. ``"TIP_minus_IEF"``) and the two
    component symbols are stored in ``spread_long`` / ``spread_short``.

    ``klass`` is the trust-stratification tier (DIRECT / STATISTICAL /
    DERIVED) — kept as ``klass`` since ``class`` is a Python keyword.

    ``applicable_sectors`` is the Mitigation-2G sector-conditional list —
    if non-empty, the factor only applies to assets whose GICS sector is in
    the list. If empty, the factor is universal.
    """

    factor_id: str
    name: str
    category: str
    tier: int
    proxy_etf_symbol: str
    proxy_method: str  # "returns_regression" | "spread" | "level_change"
    klass: str          # "DIRECT" | "STATISTICAL" | "DERIVED"
    residualized_against: tuple[str, ...]
    applicable_sectors: tuple[str, ...] = ()
    description: str = ""
    spread_long: str | None = None
    spread_short: str | None = None


def load_factor_catalog(yaml_path: Path | str | None = None) -> list[FactorSpec]:
    """Load the YAML factor catalog and return tier-sorted FactorSpecs.

    If ``yaml_path`` is None, uses the default catalog shipped with the
    package (``honest_factor_research/config/factors.yaml``).
    """
    if yaml_path is None:
        yaml_path = Path(__file__).resolve().parents[1] / "config" / "factors.yaml"
    yaml_path = Path(yaml_path)
    with yaml_path.open(encoding="utf-8") as fh:
        catalog = yaml.safe_load(fh)

    # Build residualization order from the YAML's natural ordering: earlier
    # tiers first, alphabetically within a tier. Each factor's
    # ``residualized_against`` defaults to "all earlier-tier factors" if not
    # explicitly set — but we let the YAML override that for sub-tier nuance
    # (e.g. growth residualizes against value to break the -0.925 anti-corr).
    entries = catalog["factors"]

    # Group by tier to compute the default residualized-against
    by_tier: dict[int, list[dict]] = {}
    for e in entries:
        by_tier.setdefault(int(e["tier"]), []).append(e)

    # Default residualized-against = all factor_ids of strictly lower tiers
    earlier_factors_by_tier: dict[int, list[str]] = {}
    earlier = []
    for tier in sorted(by_tier):
        earlier_factors_by_tier[tier] = list(earlier)
        earlier.extend(sorted(e["id"] for e in by_tier[tier]))

    specs: list[FactorSpec] = []
    for e in entries:
        tier = int(e["tier"])
        explicit = e.get("residualized_against")
        if explicit is None:
            residualized = tuple(earlier_factors_by_tier[tier])
        else:
            residualized = tuple(explicit)

        proxy = e["proxy_etf_symbol"]
        method = e.get("proxy_method", "returns_regression")
        long_sym = short_sym = None
        if method == "spread":
            if _SPREAD_INFIX not in proxy:
                raise ValueError(
                    f"Factor {e['id']!r}: proxy_method=spread requires "
                    f"proxy_etf_symbol in 'LONG{_SPREAD_INFIX}SHORT' form, "
                    f"got {proxy!r}"
                )
            long_sym, short_sym = proxy.split(_SPREAD_INFIX, 1)

        specs.append(FactorSpec(
            factor_id=e["id"],
            name=e["name"],
            category=e["category"],
            tier=tier,
            proxy_etf_symbol=proxy,
            proxy_method=method,
            klass=e.get("class", "DERIVED"),
            residualized_against=residualized,
            applicable_sectors=tuple(e.get("applicable_sectors") or ()),
            description=e.get("description", ""),
            spread_long=long_sym,
            spread_short=short_sym,
        ))

    # Stable sort by (tier, factor_id) — deterministic residualization order
    specs.sort(key=lambda s: (s.tier, s.factor_id))
    return specs


def raw_factor_series(spec: FactorSpec, etf_returns: pd.DataFrame) -> pd.Series:
    """Build one factor's *raw* (pre-residualized) return series.

    Three proxy_method types supported:

    * ``returns_regression`` (default): just the column from ``etf_returns``
    * ``spread``: ``etf_returns[long] - etf_returns[short]`` (parsed from
      the ``LONG_minus_SHORT`` token)
    * ``level_change``: same as returns_regression — but the caller is
      expected to have converted the underlying level series (^VIX) to
      log-changes upstream, since log-returns of a level index are still
      a meaningful regime signal.
    """
    if spec.proxy_method == "spread":
        if spec.spread_long is None or spec.spread_short is None:
            raise ValueError(f"Spread factor {spec.factor_id} missing components")
        missing = [s for s in (spec.spread_long, spec.spread_short)
                   if s not in etf_returns.columns]
        if missing:
            raise ValueError(
                f"Spread factor {spec.factor_id!r} needs ETFs {missing} in returns. "
                f"Available: {sorted(etf_returns.columns)[:20]}..."
            )
        return (
            etf_returns[spec.spread_long] - etf_returns[spec.spread_short]
        ).rename(spec.factor_id)
    if spec.proxy_etf_symbol not in etf_returns.columns:
        raise ValueError(
            f"Factor {spec.factor_id} needs ETF {spec.proxy_etf_symbol!r} in returns. "
            f"Available: {sorted(etf_returns.columns)[:20]}..."
        )
    return etf_returns[spec.proxy_etf_symbol].rename(spec.factor_id)


def _snapshot_to_returns(snapshot_path: Path | str) -> pd.DataFrame:
    """Long parquet → wide log-returns matrix."""
    df = load_snapshot(snapshot_path)
    wide = long_to_wide_close(df)
    return np.log(wide / wide.shift(1)).iloc[1:]


def raw_factor_returns(
    snapshot_path: Path | str,
    catalog_path: Path | str | None = None,
) -> pd.DataFrame:
    """Pre-residualization factor returns (one column per factor_id).

    Useful for diagnostics (lead-lag tests, correlation analyses on the
    "natural" factor returns before orthogonalization).
    """
    specs = load_factor_catalog(catalog_path)
    etf_returns = _snapshot_to_returns(snapshot_path)
    cols = {}
    for spec in specs:
        cols[spec.factor_id] = raw_factor_series(spec, etf_returns)
    return pd.DataFrame(cols)


def load_factor_returns(
    snapshot_path: Path | str,
    catalog_path: Path | str | None = None,
) -> pd.DataFrame:
    """Top-level loader: snapshot → residualized factor returns.

    Returns a wide DataFrame indexed by trading-day with one column per
    ``factor_id``. Tier-1 columns are raw returns; tier-N columns are
    residuals of OLS(factor ~ earlier-tier residuals).

    Use this as the main input to :func:`exposure.pipeline.FactorExposurePipeline`.
    """
    specs = load_factor_catalog(catalog_path)
    etf_returns = _snapshot_to_returns(snapshot_path)
    return build_residualized(specs, etf_returns)
