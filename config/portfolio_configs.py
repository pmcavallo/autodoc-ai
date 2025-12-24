"""
Portfolio Configuration Registry for AutoDoc AI.

Defines configurations for each insurance portfolio including:
- Required and optional sections
- Quality thresholds and iteration limits
- Compliance checkpoints and common pitfalls
- Corpus document references

Usage:
    from config.portfolio_configs import PortfolioRegistry

    registry = PortfolioRegistry()
    config = registry.get_config("personal_auto")
    print(config.required_sections)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class PortfolioConfig:
    """Configuration for a specific insurance portfolio."""

    # Identity
    portfolio_id: str
    display_name: str
    description: str = ""

    # Section Configuration
    required_sections: List[str] = field(default_factory=list)
    optional_sections: List[str] = field(default_factory=list)
    portfolio_specific_sections: List[str] = field(default_factory=list)

    # Quality Thresholds
    min_quality_score: float = 7.0
    max_iterations: int = 3
    compliance_strictness: str = "standard"  # standard, elevated, strict

    # Agent Instructions
    research_focus_areas: List[str] = field(default_factory=list)
    compliance_checkpoints: List[str] = field(default_factory=list)
    common_pitfalls: List[str] = field(default_factory=list)

    # Corpus References
    anchor_document: str = ""
    regulation_document: str = ""
    audit_findings_document: str = ""
    model_doc_patterns: List[str] = field(default_factory=list)

    # Metadata
    exposure_basis: str = ""
    typical_distribution: str = ""
    regulatory_framework: str = ""


# Define all 4 portfolio configurations
PERSONAL_AUTO_CONFIG = PortfolioConfig(
    portfolio_id="personal_auto",
    display_name="Personal Auto Insurance",
    description="Private passenger auto frequency and severity models",

    required_sections=[
        "Executive Summary",
        "Methodology",
        "Data Sources",
        "Variable Selection",
        "Model Results",
        "Validation"
    ],
    optional_sections=["Business Context", "Model Development"],
    portfolio_specific_sections=[],

    min_quality_score=7.0,
    max_iterations=3,
    compliance_strictness="standard",

    research_focus_areas=[
        "driver characteristics and age rating",
        "vehicle type and symbol rating",
        "territory factors",
        "prior claims history",
        "credit score usage in rating"
    ],

    compliance_checkpoints=[
        "ASOP 12 compliance for risk classification",
        "ASOP 23 for data quality",
        "State-specific rate filing requirements",
        "Unfair discrimination testing documentation"
    ],

    common_pitfalls=[
        "Missing holdout validation methodology",
        "Incomplete variable selection rationale",
        "Lack of adverse selection discussion"
    ],

    anchor_document="data/anchor_document/personal_auto_methodology_guide.md",
    regulation_document="data/regulations/personal_auto_regulations.md",
    audit_findings_document="data/audit_findings/personal_auto_audit_findings.md",
    model_doc_patterns=[
        "data/synthetic_docs/2022_frequency_model_doc.md",
        "data/synthetic_docs/2022_severity_model_doc.md"
    ],

    exposure_basis="policy-years",
    typical_distribution="Poisson (frequency), Gamma (severity)",
    regulatory_framework="State DOI rate filings"
)


HOMEOWNERS_CONFIG = PortfolioConfig(
    portfolio_id="homeowners",
    display_name="Homeowners Insurance",
    description="Property insurance including CAT perils",

    required_sections=[
        "Executive Summary",
        "Methodology",
        "Data Sources",
        "Variable Selection",
        "Model Results",
        "Validation",
        "CAT Model Integration"
    ],
    optional_sections=["Business Context"],
    portfolio_specific_sections=[
        "CAT Model Integration",
        "Demand Surge Analysis",
        "Geographic Risk Assessment"
    ],

    min_quality_score=7.5,
    max_iterations=3,
    compliance_strictness="elevated",

    research_focus_areas=[
        "CAT model validation (AIR, RMS, CoreLogic)",
        "protection class rating",
        "construction type factors",
        "roof age and condition",
        "coastal zone definitions",
        "demand surge methodology"
    ],

    compliance_checkpoints=[
        "Third-party CAT model validation documentation",
        "ASOP 38 for catastrophe modeling",
        "Demand surge assumption justification",
        "Geographic concentration risk disclosure",
        "Reinsurance alignment verification"
    ],

    common_pitfalls=[
        "CAT model validation inadequate for third-party models",
        "Demand surge factors not documented",
        "Missing coastal zone boundary definitions",
        "Protection class source not cited"
    ],

    anchor_document="data/anchor_document/homeowners_methodology_guide.md",
    regulation_document="data/regulations/homeowners_regulations.md",
    audit_findings_document="data/audit_findings/homeowners_audit_findings.md",
    model_doc_patterns=[
        "data/synthetic_docs/2023_homeowners_fire_frequency.md",
        "data/synthetic_docs/2023_homeowners_wind_hail_severity.md"
    ],

    exposure_basis="policy-years",
    typical_distribution="Poisson (frequency), Gamma (severity)",
    regulatory_framework="State DOI + CAT model filing requirements"
)


WORKERS_COMP_CONFIG = PortfolioConfig(
    portfolio_id="workers_comp",
    display_name="Workers' Compensation Insurance",
    description="Workplace injury frequency and medical/indemnity severity",

    required_sections=[
        "Executive Summary",
        "Methodology",
        "Data Sources",
        "Variable Selection",
        "Model Results",
        "Validation",
        "Loss Development Analysis",
        "Medical Cost Trends"
    ],
    optional_sections=["Business Context"],
    portfolio_specific_sections=[
        "Loss Development Analysis",
        "Medical Cost Trends",
        "NCCI Classification Mapping",
        "State Fee Schedule Impact"
    ],

    min_quality_score=7.5,
    max_iterations=4,
    compliance_strictness="strict",

    research_focus_areas=[
        "NCCI classification codes",
        "medical vs indemnity cost split",
        "loss development tail factors",
        "state fee schedule impacts",
        "experience modification factors",
        "injury severity coding"
    ],

    compliance_checkpoints=[
        "NCCI classification accuracy verification",
        "Medical inflation assumption documentation",
        "Tail development factor justification (20+ year tail)",
        "State-specific fee schedule incorporation",
        "Experience rating methodology compliance",
        "Monopolistic state handling (OH, WA, WY, ND)"
    ],

    common_pitfalls=[
        "Tail development factors inadequate for long-tail claims",
        "Medical fee schedule updates not incorporated",
        "NCCI class code mapping incomplete",
        "Indemnity duration assumptions not justified",
        "Missing state-specific regulatory requirements"
    ],

    anchor_document="data/anchor_document/workers_comp_methodology_guide.md",
    regulation_document="data/regulations/workers_comp_regulations.md",
    audit_findings_document="data/audit_findings/workers_comp_audit_findings.md",
    model_doc_patterns=[
        "data/synthetic_docs/2023_workers_comp_injury_frequency.md",
        "data/synthetic_docs/2023_workers_comp_medical_severity.md"
    ],

    exposure_basis="payroll ($100s)",
    typical_distribution="Poisson (frequency), Lognormal (severity)",
    regulatory_framework="NCCI + State WC Bureaus"
)


COMMERCIAL_AUTO_CONFIG = PortfolioConfig(
    portfolio_id="commercial_auto",
    display_name="Commercial Auto Insurance",
    description="Fleet and commercial vehicle liability models",

    required_sections=[
        "Executive Summary",
        "Methodology",
        "Data Sources",
        "Variable Selection",
        "Model Results",
        "Validation",
        "Fleet Risk Analysis",
        "Social Inflation Trends"
    ],
    optional_sections=["Business Context"],
    portfolio_specific_sections=[
        "Fleet Risk Analysis",
        "Social Inflation Trends",
        "Jurisdiction Tier Analysis",
        "Large Loss Treatment"
    ],

    min_quality_score=7.5,
    max_iterations=3,
    compliance_strictness="elevated",

    research_focus_areas=[
        "fleet size tier rating",
        "vehicle class (light/medium/heavy truck)",
        "radius of operation",
        "driver turnover impact",
        "social inflation trends",
        "nuclear verdict exposure",
        "jurisdiction tier mapping"
    ],

    compliance_checkpoints=[
        "Fleet classification methodology documentation",
        "Social inflation assumption justification (cite 8% trend)",
        "Large loss cap and excess load documentation",
        "Jurisdiction tier definitions and data sources",
        "Driver MVR data quality verification",
        "Vehicle-year exposure calculation methodology"
    ],

    common_pitfalls=[
        "Social inflation trend not explicitly documented",
        "Jurisdiction tier mapping missing or incomplete",
        "Large loss treatment threshold not justified",
        "Fleet size tier boundaries arbitrary",
        "Driver turnover impact understated"
    ],

    anchor_document="data/anchor_document/commercial_auto_methodology_guide.md",
    regulation_document="data/regulations/commercial_auto_regulations.md",
    audit_findings_document="data/audit_findings/commercial_auto_audit_findings.md",
    model_doc_patterns=[
        "data/synthetic_docs/2023_commercial_auto_fleet_frequency.md",
        "data/synthetic_docs/2023_commercial_auto_liability_severity.md"
    ],

    exposure_basis="vehicle-years",
    typical_distribution="Negative Binomial (frequency), Lognormal (severity)",
    regulatory_framework="State DOI + ISO commercial lines"
)


class PortfolioRegistry:
    """Registry of all portfolio configurations."""

    def __init__(self):
        self.configs: Dict[str, PortfolioConfig] = {
            "personal_auto": PERSONAL_AUTO_CONFIG,
            "homeowners": HOMEOWNERS_CONFIG,
            "workers_comp": WORKERS_COMP_CONFIG,
            "commercial_auto": COMMERCIAL_AUTO_CONFIG
        }

    def get_config(self, portfolio_id: str) -> Optional[PortfolioConfig]:
        """Get configuration for a portfolio."""
        return self.configs.get(portfolio_id)

    def get_all_portfolios(self) -> List[str]:
        """Get list of all portfolio IDs."""
        return list(self.configs.keys())

    def get_default_config(self) -> PortfolioConfig:
        """Get default configuration (personal auto)."""
        return self.configs["personal_auto"]

    def __repr__(self) -> str:
        return f"PortfolioRegistry(portfolios={self.get_all_portfolios()})"
