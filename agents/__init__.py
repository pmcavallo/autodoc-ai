"""
AutoDoc AI Agent System

This package contains the multi-agent system for generating actuarial model documentation.
"""

from .orchestrator import DocumentationOrchestrator, WorkflowStatus, WorkflowState
from .research_agent import ResearchAgent, ResearchFindings
from .writer_agent import WriterAgent, SectionContent, DocumentTemplate
from .compliance_agent import ComplianceAgent, ComplianceReport, ComplianceSeverity
from .editor_agent import EditorAgent, EditorialReview, ReviewPriority

__all__ = [
    'DocumentationOrchestrator',
    'WorkflowStatus',
    'WorkflowState',
    'ResearchAgent',
    'ResearchFindings',
    'WriterAgent',
    'SectionContent',
    'DocumentTemplate',
    'ComplianceAgent',
    'ComplianceReport',
    'ComplianceSeverity',
    'EditorAgent',
    'EditorialReview',
    'ReviewPriority',
]
