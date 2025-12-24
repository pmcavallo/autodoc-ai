"""
LangGraph-Based Orchestrator for AutoDoc AI Multi-Agent System

This module uses LangGraph to coordinate the workflow between multiple specialized agents
to automate insurance model documentation generation.

Agent Workflow (LangGraph State Machine):
1. Research Agent: Gather relevant context from knowledge base
2. Writer Agent: Generate documentation sections
3. Compliance Agent: Check regulatory compliance
4. Editor Agent: Review and improve quality
5. Conditional routing: If quality fails → Revise → back to Compliance
6. Iterate until quality standards met or max iterations reached

Key LangGraph Features Used:
- StateGraph: Manages shared state across all nodes
- Conditional edges: Routes based on compliance/quality results
- State persistence: Maintains iteration count, sections, reports
- Visualization: Can generate workflow diagrams

Usage:
    from agents.orchestrator_langgraph import DocumentationOrchestrator
    
    orchestrator = DocumentationOrchestrator()
    result = orchestrator.generate_documentation(
        model_type="frequency",
        document_template="model_doc",
        source_content=ppt_text
    )
"""

from pathlib import Path
from typing import List, Dict, Optional, Tuple, TypedDict, Annotated
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import operator

# LangGraph imports
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

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
class GenerationRequest:
    """Request for documentation generation."""
    document_title: str
    model_type: Optional[str] = None
    document_type: str = "model_doc"
    sections_required: Optional[List[str]] = None
    year: Optional[int] = None
    custom_instructions: Optional[str] = None
    additional_context: Optional[str] = None  # Source PPT content
    metadata: Optional[Dict] = None  # Additional metadata for tracking


# LangGraph State Definition
class DocumentationState(TypedDict):
    """
    Shared state object that flows through all nodes in the LangGraph workflow.
    
    This is the key to LangGraph - all nodes read from and write to this shared state.
    Each node can update any field, and subsequent nodes see the updates.
    """
    # Input
    request: GenerationRequest
    
    # Research phase
    research_results: Dict[str, ResearchFindings]
    
    # Writing phase
    sections: List[SectionContent]
    current_document: str
    
    # Compliance phase
    compliance_report: Optional[ComplianceReport]
    
    # Editorial phase
    editorial_review: Optional[EditorialReview]
    
    # Iteration tracking
    current_iteration: Annotated[int, operator.add]  # Automatically increments
    max_iterations: int
    
    # Quality tracking
    quality_passed: bool
    
    # Status and errors
    status: WorkflowStatus
    errors: Annotated[List[str], operator.add]  # Automatically appends
    
    # Final output
    final_document: Optional[str]


# Backward compatibility: WorkflowState is an alias for DocumentationState
WorkflowState = DocumentationState


class DocumentationOrchestrator:
    """
    LangGraph-based orchestrator for multi-agent documentation generation.
    
    This version uses LangGraph's StateGraph to manage workflow, replacing
    the manual method-call orchestration with a proper state machine.
    
    Benefits over manual orchestration:
    1. Declarative workflow definition (easier to understand)
    2. Automatic state management (no manual passing of dictionaries)
    3. Conditional routing (quality checks determine path)
    4. Visualization capabilities (can generate workflow diagrams)
    5. Better debugging (inspect state at each node)
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
        Initialize the orchestrator and build the LangGraph workflow.
        
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
        
        # Initialize agents (these don't change - still use the same agent classes)
        logger.info("Orchestrator: Initializing agents")
        self.research_agent = ResearchAgent(retriever=self.retriever)
        self.writer_agent = WriterAgent()
        self.compliance_agent = ComplianceAgent(retriever=self.retriever)
        self.editor_agent = EditorAgent()
        
        # Build the LangGraph workflow
        self.workflow = self._build_workflow()
        
        logger.info("LangGraph DocumentationOrchestrator initialized")
    
    def _build_workflow(self) -> CompiledStateGraph:
        """
        Build the LangGraph state machine for document generation workflow.
        
        This is where the magic happens - we define:
        1. All the nodes (functions that process state)
        2. Edges between nodes (workflow connections)
        3. Conditional edges (routing based on state)
        
        Returns:
            Compiled LangGraph workflow ready for execution
        """
        # Create the graph
        workflow = StateGraph(DocumentationState)
        
        # Add nodes (each is a function that takes state and returns updates)
        workflow.add_node("research", self._research_node)
        workflow.add_node("write", self._write_node)
        workflow.add_node("compliance", self._compliance_node)
        workflow.add_node("editorial", self._editorial_node)
        workflow.add_node("revise", self._revise_node)
        workflow.add_node("finalize", self._finalize_node)
        
        # Set entry point
        workflow.set_entry_point("research")
        
        # Add edges (unconditional transitions)
        workflow.add_edge("research", "write")
        workflow.add_edge("write", "compliance")
        workflow.add_edge("compliance", "editorial")
        workflow.add_edge("revise", "compliance")  # After revision, check compliance again
        
        # Add conditional edges (this is the key LangGraph feature!)
        # After editorial review, decide: revise, finalize, or end
        workflow.add_conditional_edges(
            "editorial",
            self._should_revise,  # Function that returns next node name
            {
                "revise": "revise",      # Quality failed, not max iterations → revise
                "finalize": "finalize",  # Quality passed → finalize
                "end": END               # Max iterations → accept and end
            }
        )
        
        # Finalize always ends
        workflow.add_edge("finalize", END)
        
        # Compile the graph
        return workflow.compile()
    
    def generate_documentation(
        self,
        request: GenerationRequest
    ) -> Tuple[str, DocumentationState]:
        """
        Generate complete documentation using LangGraph workflow.
        
        This is much simpler than the manual version - we just:
        1. Create initial state
        2. Invoke the compiled workflow
        3. Extract final results
        
        Args:
            request: GenerationRequest specifying what to generate
        
        Returns:
            Tuple of (final_document_text, final_state)
        """
        logger.info(f"Starting LangGraph documentation generation: {request.document_title}")
        
        # Initialize state
        initial_state: DocumentationState = {
            "request": request,
            "research_results": {},
            "sections": [],
            "current_document": "",
            "compliance_report": None,
            "editorial_review": None,
            "current_iteration": 0,
            "max_iterations": self.max_iterations,
            "quality_passed": False,
            "status": WorkflowStatus.PENDING,
            "errors": [],
            "final_document": None
        }
        
        try:
            # Execute the workflow (LangGraph handles all the routing!)
            final_state = self.workflow.invoke(initial_state)
            
            # Add backward compatibility attributes for test files
            final_state["sections_generated"] = final_state["sections"]
            final_state["research_complete"] = len(final_state["research_results"]) > 0
            final_state["writing_complete"] = len(final_state["sections"]) > 0
            final_state["compliance_passed"] = final_state["quality_passed"]
            final_state["editorial_approved"] = final_state["quality_passed"]
            
            logger.info(f"[OK] LangGraph workflow complete: {request.document_title}")
            return final_state["final_document"], final_state
            
        except Exception as e:
            logger.error(f"Error in LangGraph workflow: {e}")
            initial_state["status"] = WorkflowStatus.FAILED
            initial_state["errors"].append(str(e))
            return None, initial_state
    
    def generate_status_report(self, state: DocumentationState) -> str:
        """
        Generate a human-readable status report from workflow state.
        
        This is for backward compatibility with existing test files.
        
        Args:
            state: Final state from workflow execution
        
        Returns:
            Formatted status report string
        """
        lines = []
        lines.append("Workflow Status Report")
        lines.append("=" * 50)
        lines.append(f"Status: {state['status'].value}")
        lines.append(f"Iterations: {state['current_iteration']}/{state['max_iterations']}")
        lines.append(f"Quality Passed: {state['quality_passed']}")
        lines.append("")
        
        # Research phase
        research_count = len(state.get('research_results', {}))
        lines.append(f"Research Complete: {research_count} sections researched")
        
        # Writing phase
        sections_count = len(state.get('sections', []))
        lines.append(f"Writing Complete: {sections_count} sections generated")
        
        # Compliance phase
        if state.get('compliance_report'):
            report = state['compliance_report']
            lines.append(f"Compliance Check: {len(report.issues)} issues found")
        else:
            lines.append("Compliance Check: Not performed")
        
        # Editorial phase
        if state.get('editorial_review'):
            review = state['editorial_review']
            lines.append(f"Editorial Review: {review.overall_quality} quality")
        else:
            lines.append("Editorial Review: Not performed")
        
        # Errors
        if state.get('errors'):
            lines.append("")
            lines.append("Errors:")
            for error in state['errors']:
                lines.append(f"  - {error}")
        
        return "\n".join(lines)
    
    # ============================================================================
    # NODE FUNCTIONS
    # Each node is a function that receives state and returns state updates
    # ============================================================================
    
    def _research_node(self, state: DocumentationState) -> Dict:
        """
        Research node: Gather relevant context for each section.
        
        This is the same logic as before, just formatted as a LangGraph node.
        """
        logger.info("Node: Research")
        state["status"] = WorkflowStatus.RESEARCHING
        
        request = state["request"]
        sections = request.sections_required or self.STANDARD_MODEL_SECTIONS
        research_results = {}
        
        for section in sections:
            logger.info(f"  Researching: {section}")
            
            query = f"{section} {request.model_type or ''} model {request.document_type or ''}"
            
            filters = {}
            if request.model_type:
                filters["model_type"] = request.model_type
            if request.year:
                filters["year"] = request.year
            
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
                research_results[section] = ResearchFindings(
                    query=query,
                    findings=[],
                    context="",
                    sources=[]
                )
        
        return {"research_results": research_results}
    
    def _write_node(self, state: DocumentationState) -> Dict:
        """
        Write node: Generate documentation sections using research context.
        
        CRITICAL: Now passes source_content from request to writer agent.
        """
        logger.info("Node: Write")
        state["status"] = WorkflowStatus.WRITING
        
        request = state["request"]
        research_results = state["research_results"]
        sections = request.sections_required or self.STANDARD_MODEL_SECTIONS
        
        # Get source content from request (THE FIX for 0% → 100% accuracy)
        source_content = request.additional_context or ""
        
        generated_sections = []
        
        for section_name in sections:
            logger.info(f"  Writing: {section_name}")
            
            findings = research_results.get(section_name)
            context = findings.context if findings else ""
            
            try:
                # THE CRITICAL FIX: Pass source_content to writer
                section = self.writer_agent.write_section(
                    section_title=section_name,
                    context=context,
                    source_content=source_content,  # THIS IS THE KEY
                    template=request.document_type,
                    custom_instructions=request.custom_instructions
                )
                generated_sections.append(section)
                logger.info(f"    [OK] Generated {len(section.content.split())} words")
            except Exception as e:
                logger.error(f"    [X] Writing failed for {section_name}: {e}")
                # Create placeholder
                generated_sections.append(
                    SectionContent(
                        title=section_name,
                        content=f"[Error generating {section_name}: {e}]",
                        metadata={}
                    )
                )
        
        # Combine into document
        document_parts = [f"# {request.document_title}\n"]
        for section in generated_sections:
            document_parts.append(f"\n## {section.title}\n")
            document_parts.append(section.content)
        
        current_document = "\n".join(document_parts)
        
        return {
            "sections": generated_sections,
            "current_document": current_document
        }
    
    def _compliance_node(self, state: DocumentationState) -> Dict:
        """
        Compliance node: Check regulatory requirements.
        """
        logger.info("Node: Compliance Check")
        state["status"] = WorkflowStatus.COMPLIANCE_CHECK
        
        # Increment iteration counter (happens automatically with Annotated[int, operator.add])
        # But we need to do it explicitly here since we're returning updates
        current_iteration = state.get("current_iteration", 0) + 1
        
        request = state["request"]
        document = state["current_document"]
        
        try:
            report = self.compliance_agent.check_compliance(
                document_text=document,
                document_type=request.document_type,
                model_type=request.model_type
            )
            logger.info(f"    [OK] Compliance check complete")
            logger.info(f"        Critical: {len([i for i in report.issues if i.severity == ComplianceSeverity.CRITICAL])}")
            logger.info(f"        High: {len([i for i in report.issues if i.severity == ComplianceSeverity.HIGH])}")
            
            return {
                "compliance_report": report,
                "current_iteration": current_iteration
            }
        except Exception as e:
            logger.error(f"    [X] Compliance check failed: {e}")
            return {
                "compliance_report": None,
                "current_iteration": current_iteration,
                "errors": [f"Compliance check failed: {e}"]
            }
    
    def _editorial_node(self, state: DocumentationState) -> Dict:
        """
        Editorial node: Review quality and consistency.
        """
        logger.info("Node: Editorial Review")
        state["status"] = WorkflowStatus.EDITING
        
        request = state["request"]
        document = state["current_document"]
        
        try:
            review = self.editor_agent.review_document(
                document_text=document,
                document_type=request.document_type,
                model_type=request.model_type
            )
            logger.info(f"    [OK] Editorial review complete")
            logger.info(f"        Overall quality: {review.overall_quality}")
            logger.info(f"        Critical issues: {len([i for i in review.issues if i.priority == ReviewPriority.CRITICAL])}")
            
            return {"editorial_review": review}
        except Exception as e:
            logger.error(f"    [X] Editorial review failed: {e}")
            return {
                "editorial_review": None,
                "errors": [f"Editorial review failed: {e}"]
            }
    
    def _revise_node(self, state: DocumentationState) -> Dict:
        """
        Revise node: Apply fixes based on compliance and editorial feedback.
        """
        logger.info("Node: Revise")
        state["status"] = WorkflowStatus.REVISION
        
        request = state["request"]
        sections = state["sections"]
        research_results = state["research_results"]
        compliance_report = state["compliance_report"]
        editorial_review = state["editorial_review"]
        
        # Get source content
        source_content = request.additional_context or ""
        
        # Build revision instructions from feedback
        revision_instructions = self._build_revision_instructions(
            compliance_report,
            editorial_review
        )
        
        logger.info(f"  Revising sections with feedback:")
        for instruction in revision_instructions[:3]:  # Show first 3
            logger.info(f"    - {instruction}")
        
        revised_sections = []
        for section in sections:
            findings = research_results.get(section.title)
            context = findings.context if findings else ""
            
            try:
                revised = self.writer_agent.write_section(
                    section_title=section.title,
                    context=context,
                    source_content=source_content,
                    template=request.document_type,
                    custom_instructions="\n".join(revision_instructions)
                )
                revised_sections.append(revised)
            except Exception as e:
                logger.warning(f"    [X] Revision failed for {section.title}: {e}")
                revised_sections.append(section)  # Keep original
        
        # Rebuild document
        document_parts = [f"# {request.document_title}\n"]
        for section in revised_sections:
            document_parts.append(f"\n## {section.title}\n")
            document_parts.append(section.content)
        
        current_document = "\n".join(document_parts)
        
        return {
            "sections": revised_sections,
            "current_document": current_document
        }
    
    def _finalize_node(self, state: DocumentationState) -> Dict:
        """
        Finalize node: Mark document as complete and ready.
        """
        logger.info("Node: Finalize")
        state["status"] = WorkflowStatus.COMPLETED
        
        return {
            "final_document": state["current_document"],
            "quality_passed": True
        }
    
    # ============================================================================
    # CONDITIONAL ROUTING LOGIC
    # This function determines which path to take after editorial review
    # ============================================================================
    
    def _should_revise(self, state: DocumentationState) -> str:
        """
        Conditional edge function: Decide whether to revise, finalize, or end.
        
        This is THE key LangGraph feature - conditional routing based on state.
        
        Decision logic:
        1. If quality passed → "finalize"
        2. If max iterations reached → "end" (accept current version)
        3. Otherwise → "revise" (try again)
        
        Returns:
            One of: "revise", "finalize", "end"
        """
        compliance_report = state["compliance_report"]
        editorial_review = state["editorial_review"]
        current_iteration = state["current_iteration"]
        max_iterations = state["max_iterations"]
        
        # Check quality
        quality_passed = self._check_quality(compliance_report, editorial_review)
        
        if quality_passed:
            logger.info(f"[OK] Quality passed on iteration {current_iteration}")
            return "finalize"
        elif current_iteration >= max_iterations:
            logger.warning(f"[!] Max iterations ({max_iterations}) reached. Accepting current version.")
            return "end"
        else:
            logger.info(f"[!] Quality not met. Routing to revision ({current_iteration}/{max_iterations})")
            return "revise"
    
    # ============================================================================
    # HELPER METHODS (same as before)
    # ============================================================================
    
    def _check_quality(
        self,
        compliance_report: Optional[ComplianceReport],
        editorial_review: Optional[EditorialReview]
    ) -> bool:
        """Check if quality standards are met."""
        if not compliance_report or not editorial_review:
            return False
        
        # Check compliance
        critical_issues = [
            i for i in compliance_report.issues
            if i.severity == ComplianceSeverity.CRITICAL
        ]
        if critical_issues:
            return False
        
        high_priority_issues = [
            i for i in compliance_report.issues
            if i.severity == ComplianceSeverity.HIGH
        ]
        if len(high_priority_issues) > 2:
            return False
        
        # Check editorial
        critical_editorial = [
            i for i in editorial_review.issues
            if i.priority == ReviewPriority.CRITICAL
        ]
        if len(critical_editorial) > 3:
            return False
        
        return True
    
    def _build_revision_instructions(
        self,
        compliance_report: Optional[ComplianceReport],
        editorial_review: Optional[EditorialReview]
    ) -> List[str]:
        """Build revision instructions from feedback."""
        instructions = []
        
        if compliance_report:
            for issue in compliance_report.issues:
                if issue.severity in [ComplianceSeverity.CRITICAL, ComplianceSeverity.HIGH]:
                    instructions.append(f"COMPLIANCE: {issue.description} - {issue.recommendation}")
        
        if editorial_review:
            for issue in editorial_review.issues:
                if issue.priority in [ReviewPriority.CRITICAL, ReviewPriority.HIGH]:
                    instructions.append(f"EDITORIAL: {issue.description} - {issue.suggestion}")
        
        return instructions


# For visualization (optional but cool!)
def visualize_workflow():
    """
    Generate a visual diagram of the LangGraph workflow.
    
    This is one of the benefits of using LangGraph - you can
    automatically generate workflow diagrams.
    """
    orchestrator = DocumentationOrchestrator()
    
    # Get the Mermaid diagram
    mermaid_diagram = orchestrator.workflow.get_graph().draw_mermaid()
    
    print("LangGraph Workflow Diagram (Mermaid):")
    print(mermaid_diagram)
    
    return mermaid_diagram


if __name__ == "__main__":
    # Quick test
    print("Testing LangGraph orchestrator...")
    
    # Visualize the workflow
    visualize_workflow()
    
    print("\nLangGraph orchestrator ready!")
