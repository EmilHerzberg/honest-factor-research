"""Factor-return loading + sequential Gram-Schmidt residualization."""

from honest_factor_research.returns.load import (
    FactorSpec,
    load_factor_catalog,
    load_factor_returns,
    raw_factor_returns,
)
from honest_factor_research.returns.residualization import residualize_one, build_residualized

__all__ = [
    "FactorSpec",
    "load_factor_catalog",
    "load_factor_returns",
    "raw_factor_returns",
    "residualize_one",
    "build_residualized",
]
