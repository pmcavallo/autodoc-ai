"""
State definition for AutoDoc AI LangGraph workflow.

The state is a TypedDict that carries all information needed
across nodes in the documentation generation graph.
"""

from typing import TypedDict, List, Dict, Optional, Any
from enum import Enum


class WorkflowPhase(str, Enum):
    """Current phase of the workflow."""
    INIT = "init"
    DETECTING = "detecting"
    CONFIGURING = "configuring"
    RESEARCHING = "researching"
    WRITING = "writing"
    COMPLIANCE = "compliance"
    EDITORIAL = "editorial"
    REVISION = "revision"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentState(TypedDict, total=False):
    """
    State that flows through the documentation generation graph.

    All nodes read from and write to this shared state.
    Using total=False makes all fields optional for flexibility.
    """

    # === Input Fields (set at start) ===
    document_title: str
    document_type: str
    model_type: Optional[str]
    source_content: str  # PPT content
    year: Optional[int]
    user_id: str

    # === Portfolio Detection ===
    detected_portfolio: str  # personal_auto, homeowners, workers_comp, commercial_auto
    detected_model_type: str  # frequency, severity
    portfolio_confidence: float  # 0.0 to 1.0
    detection_keywords: List[str]  # Keywords that triggered detection

    # === Configuration ===
    portfolio_config: Dict[str, Any]  # Serialized PortfolioConfig
    required_sections: List[str]
    quality_threshold: float
    max_iterations: int
    compliance_strictness: str
    custom_instructions: str  # Built from portfolio config

    # === Research Phase ===
    research_results: Dict[str, Any]  # Section -> ResearchFindings
    research_contexts: Dict[str, str]  # Section -> context string
    research_queries: Dict[str, str]  # Section -> query used

    # === Writing Phase ===
    sections_written: List[Dict[str, Any]]  # List of section dicts
    sections_content: Dict[str, str]  # Section name -> content
    current_document: str  # Combined document text

    # === Compliance Phase ===
    compliance_report: Dict[str, Any]  # Serialized ComplianceReport
    compliance_passed: bool
    compliance_issues: List[Dict[str, Any]]
    critical_compliance_count: int
    high_compliance_count: int

    # === Editorial Phase ===
    editorial_review: Dict[str, Any]  # Serialized EditorialReview
    quality_score: float  # 0.0 to 10.0
    editorial_passed: bool
    editorial_issues: List[Dict[str, Any]]
    source_fidelity_score: float

    # === Revision Tracking ===
    current_iteration: int
    revision_history: List[Dict[str, Any]]
    issues_addressed: List[str]

    # === Workflow Control ===
    phase: str  # Current WorkflowPhase value
    should_continue: bool
    next_action: str  # What to do next (for conditional routing)

    # === Output ===
    final_document: Optional[str]
    generation_successful: bool
    errors: List[str]

    # === Memory Integration ===
    session_id: str
    memory_insights: Dict[str, Any]
    cross_session_patterns: List[str]

    # === Metrics ===
    start_time: str
    end_time: str
    total_tokens_used: int
    api_cost: float


def create_initial_state(
    document_title: str,
    document_type: str,
    source_content: str,
    model_type: Optional[str] = None,
    year: Optional[int] = None,
    user_id: str = "default"
) -> DocumentState:
    """
    Create initial state for a new documentation generation run.

    Args:
        document_title: Title for the document
        document_type: Type of document (e.g., "model_doc")
        source_content: PPT content to process
        model_type: Optional model type hint
        year: Optional year
        user_id: User identifier for memory

    Returns:
        Initialized DocumentState
    """
    from datetime import datetime

    return DocumentState(
        # Input
        document_title=document_title,
        document_type=document_type,
        model_type=model_type,
        source_content=source_content,
        year=year,
        user_id=user_id,

        # Portfolio Detection (to be filled)
        detected_portfolio="unknown",
        detected_model_type="unknown",
        portfolio_confidence=0.0,
        detection_keywords=[],

        # Configuration (to be filled)
        portfolio_config={},
        required_sections=[],
        quality_threshold=7.0,
        max_iterations=3,
        compliance_strictness="standard",
        custom_instructions="",

        # Research (to be filled)
        research_results={},
        research_contexts={},
        research_queries={},

        # Writing (to be filled)
        sections_written=[],
        sections_content={},
        current_document="",

        # Compliance (to be filled)
        compliance_report={},
        compliance_passed=False,
        compliance_issues=[],
        critical_compliance_count=0,
        high_compliance_count=0,

        # Editorial (to be filled)
        editorial_review={},
        quality_score=0.0,
        editorial_passed=False,
        editorial_issues=[],
        source_fidelity_score=0.0,

        # Revision
        current_iteration=0,
        revision_history=[],
        issues_addressed=[],

        # Workflow
        phase=WorkflowPhase.INIT.value,
        should_continue=True,
        next_action="detect",

        # Output
        final_document=None,
        generation_successful=False,
        errors=[],

        # Memory
        session_id="",
        memory_insights={},
        cross_session_patterns=[],

        # Metrics
        start_time=datetime.now().isoformat(),
        end_time="",
        total_tokens_used=0,
        api_cost=0.0
    )
