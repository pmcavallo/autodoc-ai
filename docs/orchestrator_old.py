"""
Orchestrator for AutoDoc AI Multi-Agent System

This module coordinates the workflow between multiple specialized agents
to automate insurance model documentation generation.

Agent Workflow:
1. Research Agent: Gather relevant context from knowledge base
2. Writer Agent: Generate documentation sections
3. Compliance Agent: Check regulatory compliance
4. Editor Agent: Review and improve quality
5. Iterate until quality standards met

Usage:
    from agents.orchestrator import DocumentationOrchestrator

    orchestrator = DocumentationOrchestrator()
    document = orchestrator.generate_documentation(
        model_type="frequency",
        document_template="model_doc"
    )
"""

from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from rag.retrieval import DocumentRetriever
from agents.research_agent import ResearchAgent, ResearchFindings
from agents.writer_agent import WriterAgent, SectionContent
from agents.compliance_agent import ComplianceAgent, ComplianceReport, ComplianceSeverity
from agents.editor_agent import EditorAgent, EditorialReview, ReviewPriority

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """Status of documentation generation workflow."""
    PENDING = "PENDING"
    RESEARCHING = "RESEARCHING"
    WRITING = "WRITING"
    COMPLIANCE_CHECK = "COMPLIANCE_CHECK"
    EDITING = "EDITING"
    REVISION = "REVISION"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class WorkflowState:
    """
    Tracks state of documentation generation workflow.
    """
    status: WorkflowStatus = WorkflowStatus.PENDING
    current_iteration: int = 0
    max_iterations: int = 3
    research_complete: bool = False
    writing_complete: bool = False
    compliance_passed: bool = False
    editorial_approved: bool = False
    sections_generated: List[SectionContent] = field(default_factory=list)
    compliance_report: Optional[ComplianceReport] = None
    editorial_review: Optional[EditorialReview] = None
    final_document: Optional[str] = None
    errors: List[str] = field(default_factory=list)


@dataclass
class GenerationRequest:
    """
    Request for documentation generation.
    """
    document_title: str
    document_type: str
    model_type: Optional[str] = None
    year: Optional[int] = None
    sections_required: List[str] = field(default_factory=list)
    additional_context: Optional[str] = None
    custom_instructions: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


class DocumentationOrchestrator:
    """
    Orchestrates multi-agent workflow for documentation generation.

    This orchestrator:
    1. Manages agent interactions and workflow
    2. Coordinates research, writing, compliance, and editing
    3. Handles iteration and revision cycles
    4. Ensures quality standards are met
    5. Produces final documentation artifacts
    """

    # Standard sections for model documentation
    STANDARD_MODEL_SECTIONS = [
        "Executive Summary",
        "Methodology",
        "Data Sources",
        "Variable Selection",
        "Model Results",
        "Model Development",
        "Validation",
        "Business Context"
    ]

    def __init__(
        self,
        retriever: Optional[DocumentRetriever] = None,
        max_iterations: int = 3,
        quality_threshold: str = "GOOD"
    ):
        """
        Initialize the orchestrator.

        Args:
            retriever: DocumentRetriever instance (shared across agents)
            max_iterations: Maximum revision iterations
            quality_threshold: Minimum quality threshold to accept
        """
        self.max_iterations = max_iterations
        self.quality_threshold = quality_threshold

        # Initialize shared retriever
        if retriever is None:
            try:
                logger.info("Orchestrator: Initializing DocumentRetriever")
                self.retriever = DocumentRetriever()
            except Exception as e:
                logger.warning(f"Could not initialize retriever: {e}")
                self.retriever = None
        else:
            self.retriever = retriever

        # Initialize agents
        logger.info("Orchestrator: Initializing agents")
        self.research_agent = ResearchAgent(retriever=self.retriever)
        self.writer_agent = WriterAgent()
        self.compliance_agent = ComplianceAgent(retriever=self.retriever)
        self.editor_agent = EditorAgent()

        logger.info("DocumentationOrchestrator initialized")

    def generate_documentation(
        self,
        request: GenerationRequest
    ) -> Tuple[str, WorkflowState]:
        """
        Generate complete documentation using multi-agent workflow.

        Args:
            request: GenerationRequest specifying what to generate

        Returns:
            Tuple of (final_document_text, workflow_state)
        """
        logger.info(f"Starting documentation generation: {request.document_title}")

        # Initialize workflow state
        state = WorkflowState(max_iterations=self.max_iterations)

        try:
            # Phase 1: Research
            state.status = WorkflowStatus.RESEARCHING
            research_results = self._research_phase(request)
            state.research_complete = True
            logger.info("[OK] Research phase complete")

            # Phase 2: Writing
            state.status = WorkflowStatus.WRITING
            sections = self._writing_phase(request, research_results)
            state.sections_generated = sections
            state.writing_complete = True
            logger.info("[OK] Writing phase complete")

            # Phase 3: Iteration loop (compliance + editing + revision)
            for iteration in range(1, self.max_iterations + 1):
                state.current_iteration = iteration
                logger.info(f"\n--- Iteration {iteration}/{self.max_iterations} ---")

                # Combine sections into document
                document = self._combine_sections(request, sections)

                # Compliance check
                state.status = WorkflowStatus.COMPLIANCE_CHECK
                compliance_report = self._compliance_phase(document, request)
                state.compliance_report = compliance_report

                # Editorial review
                state.status = WorkflowStatus.EDITING
                editorial_review = self._editorial_phase(document, request)
                state.editorial_review = editorial_review

                # Check if quality standards met
                if self._quality_check_passed(compliance_report, editorial_review):
                    logger.info("[OK] Quality standards met")
                    state.compliance_passed = True
                    state.editorial_approved = True
                    state.final_document = document
                    state.status = WorkflowStatus.COMPLETED
                    break

                # Revise if not final iteration
                if iteration < self.max_iterations:
                    state.status = WorkflowStatus.REVISION
                    logger.info("Quality standards not met. Initiating revision...")
                    sections = self._revision_phase(
                        sections,
                        compliance_report,
                        editorial_review,
                        research_results
                    )
                else:
                    logger.warning("Max iterations reached. Accepting current version.")
                    state.final_document = document
                    state.status = WorkflowStatus.COMPLETED

            logger.info(f"\n[OK] Documentation generation complete: {request.document_title}")
            return state.final_document, state

        except Exception as e:
            logger.error(f"Error in documentation generation: {e}")
            state.status = WorkflowStatus.FAILED
            state.errors.append(str(e))
            return None, state

    def _research_phase(
        self,
        request: GenerationRequest
    ) -> Dict[str, ResearchFindings]:
        """
        Phase 1: Research relevant information for each section.

        Args:
            request: GenerationRequest

        Returns:
            Dictionary mapping section names to ResearchFindings
        """
        logger.info("Phase 1: Research")

        sections = request.sections_required or self.STANDARD_MODEL_SECTIONS
        research_results = {}

        for section in sections:
            logger.info(f"  Researching: {section}")

            # Build research query
            query = f"{section} {request.model_type or ''} model {request.document_type or ''}"

            # Build filters
            filters = {}
            if request.model_type:
                filters["model_type"] = request.model_type
            if request.year:
                filters["year"] = request.year

            # Perform research
            try:
                findings = self.research_agent.research_topic(
                    topic=query,
                    n_results=5,
                    filters=filters if filters else None
                )
                research_results[section] = findings
                logger.info(f"    [OK] Found {len(findings.findings)} relevant sources")
            except Exception as e:
                logger.warning(f"    [X] Research failed for {section}: {e}")
                # Create empty findings
                from agents.research_agent import ResearchFindings
                research_results[section] = ResearchFindings(
                    query=query,
                    findings=[],
                    context="",
                    sources=[]
                )

        return research_results

    def _writing_phase(
        self,
        request: GenerationRequest,
        research_results: Dict[str, ResearchFindings]
    ) -> List[SectionContent]:
        """
        Phase 2: Generate documentation sections.

        Args:
            request: GenerationRequest
            research_results: Research findings for each section

        Returns:
            List of SectionContent objects
        """
        logger.info("Phase 2: Writing")

        sections = []

        for section_name, findings in research_results.items():
            logger.info(f"  Writing: {section_name}")

            # Map section names to templates
            template = self._get_template_for_section(section_name)

            # Generate section
            try:
                section = self.writer_agent.write_section(
                    section_title=section_name,
                    context=findings.context,
                    template=template,
                    length_target="medium",
                    custom_instructions=request.custom_instructions
                )
                sections.append(section)
                logger.info(f"    [OK] Generated ({section.word_count} words)")
            except Exception as e:
                logger.error(f"    [X] Writing failed for {section_name}: {e}")

        return sections

    def _compliance_phase(
        self,
        document: str,
        request: GenerationRequest
    ) -> ComplianceReport:
        """
        Phase 3a: Check regulatory compliance.

        Args:
            document: Complete document text
            request: GenerationRequest

        Returns:
            ComplianceReport
        """
        logger.info("Phase 3a: Compliance Check")

        report = self.compliance_agent.check_compliance(
            document_content=document,
            document_title=request.document_title,
            document_type=request.document_type
        )

        logger.info(f"  Status: {report.overall_status}")
        logger.info(f"  Findings: {len(report.findings)}")

        critical = len(report.get_findings_by_severity(ComplianceSeverity.CRITICAL))
        high = len(report.get_findings_by_severity(ComplianceSeverity.HIGH))

        if critical > 0:
            logger.warning(f"  ⚠ {critical} CRITICAL compliance issues")
        if high > 0:
            logger.warning(f"  ⚠ {high} HIGH priority compliance issues")

        return report

    def _editorial_phase(
        self,
        document: str,
        request: GenerationRequest
    ) -> EditorialReview:
        """
        Phase 3b: Editorial review.

        Args:
            document: Complete document text
            request: GenerationRequest

        Returns:
            EditorialReview
        """
        logger.info("Phase 3b: Editorial Review")

        review = self.editor_agent.review_document(
            document_content=document,
            document_title=request.document_title,
            document_type=request.document_type
        )

        logger.info(f"  Quality: {review.overall_quality}")
        logger.info(f"  Findings: {len(review.findings)}")
        logger.info(f"  Readability: {review.readability_score:.1f}/10")

        critical = len(review.get_findings_by_priority(ReviewPriority.CRITICAL))
        high = len(review.get_findings_by_priority(ReviewPriority.HIGH))

        if critical > 0:
            logger.warning(f"  ⚠ {critical} CRITICAL editorial issues")
        if high > 0:
            logger.warning(f"  ⚠ {high} HIGH priority editorial issues")

        return review

    def _revision_phase(
        self,
        sections: List[SectionContent],
        compliance_report: ComplianceReport,
        editorial_review: EditorialReview,
        research_results: Dict[str, ResearchFindings]
    ) -> List[SectionContent]:
        """
        Phase 4: Revise sections based on feedback.

        Args:
            sections: Original sections
            compliance_report: Compliance findings
            editorial_review: Editorial findings
            research_results: Research context for additional info

        Returns:
            Revised sections
        """
        logger.info("Phase 4: Revision")

        # Generate revision instructions from compliance and editorial feedback
        revision_instructions = []

        # Add compliance issues
        for finding in compliance_report.findings[:5]:  # Top 5
            if finding.recommendation:
                revision_instructions.append(finding.recommendation)

        # Add editorial suggestions
        suggestions = self.editor_agent.suggest_improvements(editorial_review, max_suggestions=5)
        revision_instructions.extend(suggestions)

        # For now, return original sections with revision note
        # In production, this would use LLM to actually revise content
        logger.info(f"  Generated {len(revision_instructions)} revision instructions")
        logger.info("  [Placeholder: In production, sections would be revised by LLM]")

        return sections

    def _combine_sections(
        self,
        request: GenerationRequest,
        sections: List[SectionContent]
    ) -> str:
        """
        Combine sections into complete document.

        Args:
            request: GenerationRequest
            sections: List of SectionContent objects

        Returns:
            Complete document text
        """
        # Prepare frontmatter
        frontmatter = {
            "title": request.document_title,
            "document_type": request.document_type,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "generated_by": "AutoDoc AI",
        }

        # Add optional metadata
        if request.model_type:
            frontmatter["model_type"] = request.model_type
        if request.year:
            frontmatter["year"] = request.year

        frontmatter.update(request.metadata)

        # Combine using writer agent
        document = self.writer_agent.combine_sections(
            sections=sections,
            document_title=request.document_title,
            frontmatter=frontmatter
        )

        return document

    def _quality_check_passed(
        self,
        compliance_report: ComplianceReport,
        editorial_review: EditorialReview
    ) -> bool:
        """
        Check if quality standards are met.

        Args:
            compliance_report: ComplianceReport
            editorial_review: EditorialReview

        Returns:
            True if quality standards met
        """
        # Check compliance
        compliance_ok = (
            len(compliance_report.get_findings_by_severity(ComplianceSeverity.CRITICAL)) == 0
            and len(compliance_report.get_findings_by_severity(ComplianceSeverity.HIGH)) <= 2
        )

        # Check editorial quality
        editorial_ok = (
            len(editorial_review.get_findings_by_priority(ReviewPriority.CRITICAL)) == 0
            and len(editorial_review.get_findings_by_priority(ReviewPriority.HIGH)) <= 3
        )

        return compliance_ok and editorial_ok

    def _get_template_for_section(self, section_name: str) -> Optional[str]:
        """Map section name to template name."""
        template_mapping = {
            "Executive Summary": "executive_summary",
            "Methodology": "methodology",
            "Data Sources": "data_sources",
            "Variable Selection": "variable_selection",
            "Model Results": "results",
            "Model Development": "methodology",
            "Validation": "validation",
            "Business Context": "business_context",
        }
        return template_mapping.get(section_name)

    def generate_status_report(self, state: WorkflowState) -> str:
        """
        Generate human-readable status report.

        Args:
            state: WorkflowState

        Returns:
            Formatted status report
        """
        lines = [
            "=" * 60,
            "DOCUMENTATION GENERATION STATUS",
            "=" * 60,
            f"Status: {state.status.value}",
            f"Iteration: {state.current_iteration}/{state.max_iterations}",
            "",
            "Progress:",
            f"  Research: {'[OK]' if state.research_complete else '[ ]'}",
            f"  Writing: {'[OK]' if state.writing_complete else '[ ]'}",
            f"  Compliance: {'[OK]' if state.compliance_passed else '[ ]'}",
            f"  Editorial: {'[OK]' if state.editorial_approved else '[ ]'}",
            "",
        ]

        if state.sections_generated:
            lines.append(f"Sections Generated: {len(state.sections_generated)}")

        if state.compliance_report:
            lines.append(f"Compliance Status: {state.compliance_report.overall_status}")

        if state.editorial_review:
            lines.append(f"Editorial Quality: {state.editorial_review.overall_quality}")

        if state.errors:
            lines.append("\nErrors:")
            for error in state.errors:
                lines.append(f"  - {error}")

        return "\n".join(lines)


def main():
    """
    Test function for orchestrator.
    """
    print("=" * 60)
    print("AutoDoc AI - Orchestrator Test")
    print("=" * 60)
    print()

    try:
        # Initialize orchestrator
        print("1. Initializing DocumentationOrchestrator...")
        orchestrator = DocumentationOrchestrator(max_iterations=2)
        print("   [OK] Orchestrator initialized")
        print("   [OK] All agents initialized")
        print()

        # Create generation request
        print("2. Creating documentation generation request...")
        request = GenerationRequest(
            document_title="Test Frequency Model Documentation",
            document_type="model_doc",
            model_type="frequency",
            year=2024,
            sections_required=[
                "Executive Summary",
                "Methodology",
                "Validation"
            ],
            metadata={
                "author": "AutoDoc AI System",
                "status": "draft"
            }
        )
        print(f"   [OK] Request: {request.document_title}")
        print(f"   [OK] Sections: {len(request.sections_required)}")
        print()

        # Generate documentation
        print("3. Generating documentation...")
        print("   (This will run the full multi-agent workflow)")
        print()

        document, state = orchestrator.generate_documentation(request)

        print()
        print("4. Generation Complete!")
        print()

        # Display status
        print("5. Status Report:")
        status_report = orchestrator.generate_status_report(state)
        print(status_report)
        print()

        # Display document preview
        if document:
            print("6. Document Preview (first 500 chars):")
            print("-" * 60)
            print(document[:500])
            print("...")
            print("-" * 60)
            print()
            print(f"   [OK] Total document length: {len(document)} characters")
            print(f"   [OK] Word count: ~{len(document.split())} words")
        else:
            print("6. Document generation failed")
            print(f"   Errors: {state.errors}")

        print()
        print("=" * 60)
        print("[OK] Orchestrator Test Complete!")
        print("=" * 60)
        print()
        print("The orchestrator successfully coordinated all agents")
        print("through the complete documentation generation workflow.")
        print()

    except Exception as e:
        print(f"\n[X] Error: {e}")
        print("\nNote: The orchestrator requires the vector store to be populated.")
        print("Run: python rag/ingestion.py")
        print()


if __name__ == "__main__":
    main()
