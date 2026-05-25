"""Rolling Ridge factor-exposure pipeline + bootstrap + regime-switching."""

from honest_factor_research.exposure.bootstrap import (
    block_bootstrap_resamples,
    bootstrap_with_r2_ci,
    stationary_block_indices,
)
from honest_factor_research.exposure.models import ExposureRow
from honest_factor_research.exposure.pipeline import FactorExposurePipeline
from honest_factor_research.exposure.regime import compute_regime_betas

__all__ = [
    "ExposureRow",
    "FactorExposurePipeline",
    "block_bootstrap_resamples",
    "bootstrap_with_r2_ci",
    "compute_regime_betas",
    "stationary_block_indices",
]
