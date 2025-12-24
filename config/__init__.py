"""
Configuration module for AutoDoc AI.

Contains portfolio configurations and registry for multi-portfolio support.
"""

from .portfolio_configs import (
    PortfolioConfig,
    PortfolioRegistry,
    PERSONAL_AUTO_CONFIG,
    HOMEOWNERS_CONFIG,
    WORKERS_COMP_CONFIG,
    COMMERCIAL_AUTO_CONFIG
)

__all__ = [
    'PortfolioConfig',
    'PortfolioRegistry',
    'PERSONAL_AUTO_CONFIG',
    'HOMEOWNERS_CONFIG',
    'WORKERS_COMP_CONFIG',
    'COMMERCIAL_AUTO_CONFIG'
]
