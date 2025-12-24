"""
LangGraph-based orchestrator for AutoDoc AI.

This module assembles the documentation generation workflow
as a LangGraph StateGraph with explicit state transitions
and conditional routing.

Usage:
    from agents.langgraph_orchestrator import create_workflow, run_workflow

    app = create_workflow()
    result = run_workflow(app, document_title="...", source_content="...")
"""

import logging
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
from dataclasses import dataclass, asdict

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from agents.graph_state import DocumentState, create_initial_state
from agents.graph_nodes import (
    detect_portfolio,
    configure_for_portfolio,
    research_phase,
    writing_phase,
    compliance_phase,
    editorial_phase,
    revision_phase,
    complete_workflow,
    handle_failure,
    route_after_compliance,
    route_after_editorial,
    route_after_revision
)

logger = logging.getLogger(__name__)


@dataclass
class StateHistoryEntry:
    """
    A single entry in the execution history.
    
    Captures the state at each node transition for audit purposes.
    """
    step: int
    node: str
    timestamp: str
    portfolio: Optional[str]
    iteration: Optional[int]
    compliance_passed: Optional[bool]
    editorial_passed: Optional[bool]
    quality_score: Optional[float]
    phase: Optional[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass 
class ExecutionAuditLog:
    """
    Complete audit log for a document generation run.
    
    Provides full traceability for regulatory compliance.
    """
    thread_id: str
    document_title: str
    start_time: str
    end_time: Optional[str]
    detected_portfolio: str
    final_quality_score: float
    total_iterations: int
    generation_successful: bool
    execution_path: List[str]  # Ordered list of nodes visited
    state_history: List[StateHistoryEntry]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "thread_id": self.thread_id,
            "document_title": self.document_title,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "detected_portfolio": self.detected_portfolio,
            "final_quality_score": self.final_quality_score,
            "total_iterations": self.total_iterations,
            "generation_successful": self.generation_successful,
            "execution_path": self.execution_path,
            "state_history": [entry.to_dict() for entry in self.state_history]
        }
    
    def get_path_summary(self) -> str:
        """Get human-readable execution path summary."""
        return " → ".join(self.execution_path)
    
    def get_decision_points(self) -> List[Dict[str, Any]]:
        """Extract key decision points for audit review."""
        decisions = []
        for i, entry in enumerate(self.state_history):
            if entry.node in ["compliance", "editorial"]:
                passed = entry.compliance_passed if entry.node == "compliance" else entry.editorial_passed
                next_node = self.execution_path[i + 1] if i + 1 < len(self.execution_path) else "END"
                decisions.append({
                    "step": entry.step,
                    "node": entry.node,
                    "passed": passed,
                    "routed_to": next_node,
                    "iteration": entry.iteration,
                    "quality_score": entry.quality_score
                })
        return decisions


def create_workflow(checkpointer: Optional[MemorySaver] = None) -> StateGraph:
    """
    Create the documentation generation workflow graph.

    The graph structure:

    detect_portfolio -> configure -> research -> write -> compliance
                                                          |
                                             +------------+------------+
                                             |                        |
                                        (passed)                  (failed)
                                             |                        |
                                        editorial              revision <--+
                                             |                    |       |
                                   +---------+---------+         |       |
                                   |                   |         +-------+
                              (passed)             (failed)           ^
                                   |                   |              |
                              complete            revision -----------+

    Args:
        checkpointer: Optional MemorySaver for state persistence

    Returns:
        Compiled StateGraph application
    """
    logger.info("[LangGraph] Creating workflow graph")

    # Create the graph with DocumentState schema
    workflow = StateGraph(DocumentState)

    # ============================================================
    # ADD NODES
    # ============================================================
    workflow.add_node("detect_portfolio", detect_portfolio)
    workflow.add_node("configure", configure_for_portfolio)
    workflow.add_node("research", research_phase)
    workflow.add_node("write", writing_phase)
    workflow.add_node("compliance", compliance_phase)
    workflow.add_node("editorial", editorial_phase)
    workflow.add_node("revision", revision_phase)
    workflow.add_node("complete", complete_workflow)
    workflow.add_node("fail", handle_failure)

    logger.info("[LangGraph] Added 9 nodes")

    # ============================================================
    # ADD EDGES (unconditional transitions)
    # ============================================================
    workflow.add_edge("detect_portfolio", "configure")
    workflow.add_edge("configure", "research")
    workflow.add_edge("research", "write")
    workflow.add_edge("write", "compliance")

    logger.info("[LangGraph] Added linear edges")

    # ============================================================
    # ADD CONDITIONAL EDGES (routing based on state)
    # ============================================================

    # After compliance: route to editorial, revision, or complete
    workflow.add_conditional_edges(
        "compliance",
        route_after_compliance,
        {
            "editorial": "editorial",
            "revision": "revision",
            "complete": "complete"
        }
    )

    # After editorial: route to complete or revision
    workflow.add_conditional_edges(
        "editorial",
        route_after_editorial,
        {
            "complete": "complete",
            "revision": "revision"
        }
    )

    # After revision: always go back to compliance
    workflow.add_conditional_edges(
        "revision",
        route_after_revision,
        {
            "compliance": "compliance"
        }
    )

    logger.info("[LangGraph] Added conditional edges (cycles)")

    # ============================================================
    # SET ENTRY AND EXIT POINTS
    # ============================================================
    workflow.set_entry_point("detect_portfolio")
    workflow.add_edge("complete", END)
    workflow.add_edge("fail", END)

    logger.info("[LangGraph] Set entry point and end nodes")

    # ============================================================
    # COMPILE
    # ============================================================
    if checkpointer:
        app = workflow.compile(checkpointer=checkpointer)
        logger.info("[LangGraph] Compiled with checkpointer")
    else:
        app = workflow.compile()
        logger.info("[LangGraph] Compiled without checkpointer")

    return app


def run_workflow(
    app: StateGraph,
    document_title: str,
    document_type: str,
    source_content: str,
    model_type: Optional[str] = None,
    year: Optional[int] = None,
    user_id: str = "default",
    thread_id: Optional[str] = None
) -> Tuple[Optional[str], Dict[str, Any]]:
    """
    Execute the documentation generation workflow.

    Args:
        app: Compiled StateGraph
        document_title: Title for the document
        document_type: Type of document
        source_content: Source PPT content
        model_type: Optional model type hint
        year: Optional year
        user_id: User identifier
        thread_id: Optional thread ID for checkpointing

    Returns:
        Tuple of (final_document, final_state)
    """
    logger.info(f"[LangGraph] Starting workflow: {document_title}")

    # Create initial state
    initial_state = create_initial_state(
        document_title=document_title,
        document_type=document_type,
        source_content=source_content,
        model_type=model_type,
        year=year,
        user_id=user_id
    )

    # Configure execution
    config = {}
    if thread_id:
        config["configurable"] = {"thread_id": thread_id}

    # Execute the graph
    try:
        final_state = app.invoke(initial_state, config=config)

        logger.info(f"[LangGraph] Workflow complete")
        logger.info(f"[LangGraph] Portfolio: {final_state.get('detected_portfolio')}")
        logger.info(f"[LangGraph] Iterations: {final_state.get('current_iteration')}")
        logger.info(f"[LangGraph] Quality Score: {final_state.get('quality_score', 0):.1f}")
        logger.info(f"[LangGraph] Success: {final_state.get('generation_successful')}")

        return final_state.get("final_document"), final_state

    except Exception as e:
        logger.error(f"[LangGraph] Workflow failed: {e}")
        return None, {"error": str(e), "generation_successful": False}


def get_workflow_visualization(app: StateGraph = None) -> str:
    """
    Get a text representation of the workflow graph.

    Args:
        app: Compiled StateGraph (optional)

    Returns:
        ASCII representation of the graph
    """
    return """
    AutoDoc AI - LangGraph Workflow
    ================================

    +------------------+
    | detect_portfolio |
    +--------+---------+
             |
             v
    +------------------+
    |    configure     |
    +--------+---------+
             |
             v
    +------------------+
    |    research      |
    +--------+---------+
             |
             v
    +------------------+
    |     write        |
    +--------+---------+
             |
             v
    +------------------+
    |   compliance     |<--------------+
    +--------+---------+               |
             |                         |
        +----+----+                    |
        v         v                    |
    (passed)  (failed)                 |
        |         |                    |
        v         v                    |
    +------------------+               |
    |   editorial      |               |
    +--------+---------+               |
             |                         |
        +----+----+                    |
        v         v                    |
    (passed)  (failed)                 |
        |         |                    |
        v         v                    |
    +------------------+   +------------------+
    |    complete      |   |    revision      |
    +--------+---------+   +--------+---------+
             |                      |
             v                      +-----------+
           [END]

    Legend:
    - Solid arrows: Unconditional transitions
    - (passed)/(failed): Conditional routing based on state
    - Revision creates a cycle back to compliance
    """


class LangGraphOrchestrator:
    """
    High-level interface for the LangGraph workflow.

    Provides a similar interface to the original DocumentationOrchestrator
    for backward compatibility.
    
    Features:
    - Automatic state history tracking for audit compliance
    - Execution path logging for regulatory review
    - Full traceability of all routing decisions
    """

    def __init__(
        self,
        user_id: str = "default",
        enable_checkpointing: bool = True  # Default ON for audit trail
    ):
        """
        Initialize the LangGraph orchestrator.

        Args:
            user_id: User identifier for memory
            enable_checkpointing: Whether to enable state checkpointing (default: True for audit)
        """
        self.user_id = user_id
        self.enable_checkpointing = enable_checkpointing
        
        # Create checkpointer (enabled by default for audit trail)
        self.checkpointer = MemorySaver() if enable_checkpointing else None

        # Create the workflow
        self.app = create_workflow(checkpointer=self.checkpointer)
        
        # Track current/last execution for history retrieval
        self._last_thread_id: Optional[str] = None
        self._last_config: Optional[Dict] = None
        self._audit_logs: Dict[str, ExecutionAuditLog] = {}

        logger.info(f"[LangGraphOrchestrator] Initialized for user: {user_id}")
        logger.info(f"[LangGraphOrchestrator] Checkpointing: {enable_checkpointing}")
        if enable_checkpointing:
            logger.info(f"[LangGraphOrchestrator] Audit trail enabled")

    def generate_documentation(
        self,
        document_title: str,
        document_type: str,
        source_content: str,
        model_type: Optional[str] = None,
        year: Optional[int] = None
    ) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Generate documentation using the LangGraph workflow.

        Args:
            document_title: Title for the document
            document_type: Type of document
            source_content: Source PPT content
            model_type: Optional model type hint
            year: Optional year

        Returns:
            Tuple of (final_document, workflow_state)
            
        Note:
            After calling this method, use get_execution_history() or
            get_audit_log() to retrieve the full execution trace.
        """
        import uuid
        thread_id = str(uuid.uuid4())
        start_time = datetime.now().isoformat()
        
        # Store for history retrieval
        self._last_thread_id = thread_id
        self._last_config = {"configurable": {"thread_id": thread_id}}

        document, final_state = run_workflow(
            app=self.app,
            document_title=document_title,
            document_type=document_type,
            source_content=source_content,
            model_type=model_type,
            year=year,
            user_id=self.user_id,
            thread_id=thread_id
        )
        
        # Build and store audit log if checkpointing is enabled
        if self.enable_checkpointing and self.checkpointer:
            audit_log = self._build_audit_log(
                thread_id=thread_id,
                document_title=document_title,
                start_time=start_time,
                final_state=final_state
            )
            self._audit_logs[thread_id] = audit_log
            
            # Add thread_id to state for reference
            final_state["thread_id"] = thread_id
            final_state["audit_log_available"] = True
        
        return document, final_state

    def get_visualization(self) -> str:
        """Get workflow visualization."""
        return get_workflow_visualization(self.app)
    
    def get_execution_history(self, thread_id: Optional[str] = None) -> List[StateHistoryEntry]:
        """
        Get the execution history for a document generation run.
        
        Args:
            thread_id: Thread ID to retrieve history for.
                      If None, uses the last execution.
        
        Returns:
            List of StateHistoryEntry objects showing each state transition.
            
        Raises:
            ValueError: If checkpointing is not enabled or no history available.
        """
        if not self.enable_checkpointing or not self.checkpointer:
            raise ValueError("Checkpointing must be enabled to retrieve execution history")
        
        thread_id = thread_id or self._last_thread_id
        if not thread_id:
            raise ValueError("No execution history available. Run generate_documentation first.")
        
        config = {"configurable": {"thread_id": thread_id}}
        
        history = []
        step = 0
        
        try:
            for state_snapshot in self.app.get_state_history(config):
                values = state_snapshot.values
                metadata = state_snapshot.metadata or {}
                
                entry = StateHistoryEntry(
                    step=step,
                    node=metadata.get("source", "unknown"),
                    timestamp=metadata.get("created_at", datetime.now().isoformat()),
                    portfolio=values.get("detected_portfolio"),
                    iteration=values.get("current_iteration"),
                    compliance_passed=values.get("compliance_passed"),
                    editorial_passed=values.get("editorial_passed"),
                    quality_score=values.get("quality_score"),
                    phase=values.get("phase")
                )
                history.append(entry)
                step += 1
        except Exception as e:
            logger.warning(f"[LangGraphOrchestrator] Error retrieving history: {e}")
        
        # Reverse to get chronological order (LangGraph returns newest first)
        return list(reversed(history))
    
    def get_audit_log(self, thread_id: Optional[str] = None) -> Optional[ExecutionAuditLog]:
        """
        Get the complete audit log for a document generation run.
        
        Args:
            thread_id: Thread ID to retrieve audit log for.
                      If None, uses the last execution.
        
        Returns:
            ExecutionAuditLog with full traceability information.
        """
        thread_id = thread_id or self._last_thread_id
        if not thread_id:
            return None
        return self._audit_logs.get(thread_id)
    
    def _build_audit_log(
        self,
        thread_id: str,
        document_title: str,
        start_time: str,
        final_state: Dict[str, Any]
    ) -> ExecutionAuditLog:
        """
        Build a complete audit log from execution history.
        
        Args:
            thread_id: Thread ID of the execution
            document_title: Title of the document
            start_time: ISO timestamp when execution started
            final_state: Final state after execution
            
        Returns:
            ExecutionAuditLog with complete execution trace
        """
        history = self.get_execution_history(thread_id)
        execution_path = [entry.node for entry in history if entry.node != "unknown"]
        
        return ExecutionAuditLog(
            thread_id=thread_id,
            document_title=document_title,
            start_time=start_time,
            end_time=final_state.get("end_time", datetime.now().isoformat()),
            detected_portfolio=final_state.get("detected_portfolio", "unknown"),
            final_quality_score=final_state.get("quality_score", 0.0),
            total_iterations=final_state.get("current_iteration", 0),
            generation_successful=final_state.get("generation_successful", False),
            execution_path=execution_path,
            state_history=history
        )
    
    def get_execution_summary(self, thread_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a human-readable summary of execution for display in UI.
        
        Args:
            thread_id: Thread ID to summarize. If None, uses last execution.
            
        Returns:
            Dictionary with formatted summary suitable for Streamlit display.
        """
        audit_log = self.get_audit_log(thread_id)
        if not audit_log:
            return {"error": "No execution history available"}
        
        decision_points = audit_log.get_decision_points()
        
        return {
            "thread_id": audit_log.thread_id,
            "document_title": audit_log.document_title,
            "portfolio_detected": audit_log.detected_portfolio,
            "execution_path": audit_log.get_path_summary(),
            "total_nodes_visited": len(audit_log.execution_path),
            "total_iterations": audit_log.total_iterations,
            "final_quality_score": f"{audit_log.final_quality_score:.1f}/10",
            "generation_successful": audit_log.generation_successful,
            "decision_points": decision_points,
            "start_time": audit_log.start_time,
            "end_time": audit_log.end_time,
            "state_transitions": [
                {
                    "step": entry.step,
                    "node": entry.node,
                    "iteration": entry.iteration,
                    "phase": entry.phase
                }
                for entry in audit_log.state_history
            ]
        }
    
    def print_execution_trace(self, thread_id: Optional[str] = None) -> None:
        """
        Print a formatted execution trace to console.
        
        Useful for debugging and demonstration.
        
        Args:
            thread_id: Thread ID to trace. If None, uses last execution.
        """
        audit_log = self.get_audit_log(thread_id)
        if not audit_log:
            print("No execution history available.")
            return
        
        print("\n" + "=" * 70)
        print("EXECUTION AUDIT LOG")
        print("=" * 70)
        print(f"Thread ID:    {audit_log.thread_id}")
        print(f"Document:     {audit_log.document_title}")
        print(f"Portfolio:    {audit_log.detected_portfolio}")
        print(f"Start Time:   {audit_log.start_time}")
        print(f"End Time:     {audit_log.end_time}")
        print(f"Success:      {audit_log.generation_successful}")
        print(f"Quality:      {audit_log.final_quality_score:.1f}/10")
        print(f"Iterations:   {audit_log.total_iterations}")
        print("\n" + "-" * 70)
        print("EXECUTION PATH")
        print("-" * 70)
        print(audit_log.get_path_summary())
        print("\n" + "-" * 70)
        print("STATE TRANSITIONS")
        print("-" * 70)
        print(f"{'Step':<6}{'Node':<20}{'Iteration':<12}{'Phase':<15}")
        print("-" * 70)
        for entry in audit_log.state_history:
            iteration_str = str(entry.iteration) if entry.iteration is not None else "-"
            phase_str = entry.phase if entry.phase else "-"
            print(f"{entry.step:<6}{entry.node:<20}{iteration_str:<12}{phase_str:<15}")
        print("\n" + "-" * 70)
        print("DECISION POINTS")
        print("-" * 70)
        for decision in audit_log.get_decision_points():
            passed_str = "PASSED" if decision["passed"] else "FAILED"
            print(f"Step {decision['step']}: {decision['node']} -> {passed_str} -> routed to {decision['routed_to']}")
        print("=" * 70 + "\n")


# ============================================================
# TEST / DEMO
# ============================================================
def main():
    """Test the LangGraph orchestrator."""

    print("=" * 60)
    print("AutoDoc AI - LangGraph Orchestrator Test")
    print("=" * 60)
    print()

    # Display workflow structure
    orchestrator = LangGraphOrchestrator()
    print(orchestrator.get_visualization())
    print()

    # Test with sample content
    sample_content = """
    This workers' compensation frequency model uses NCCI classification codes
    to predict injury rates based on payroll exposure. The model incorporates
    medical cost trends and indemnity duration factors. Key variables include
    industry class code, experience modification, and state fee schedules.
    """

    print("Testing with Workers' Comp sample content...")
    print()

    # Just test portfolio detection (don't run full workflow without API)
    from agents.graph_state import create_initial_state
    from agents.graph_nodes import detect_portfolio, configure_for_portfolio

    state = create_initial_state(
        document_title="Test WC Model",
        document_type="model_doc",
        source_content=sample_content
    )

    # Test detect_portfolio
    state_after_detect = {**state, **detect_portfolio(state)}
    print(f"Detected Portfolio: {state_after_detect['detected_portfolio']}")
    print(f"Confidence: {state_after_detect['portfolio_confidence']:.2f}")
    print(f"Keywords: {state_after_detect['detection_keywords'][:5]}")
    print()

    # Test configure
    state_after_config = {**state_after_detect, **configure_for_portfolio(state_after_detect)}
    print(f"Configuration Applied:")
    print(f"  Quality Threshold: {state_after_config['quality_threshold']}")
    print(f"  Max Iterations: {state_after_config['max_iterations']}")
    print(f"  Compliance Strictness: {state_after_config['compliance_strictness']}")
    print(f"  Required Sections: {len(state_after_config['required_sections'])}")
    for section in state_after_config['required_sections']:
        print(f"    - {section}")
    print()

    print("=" * 60)
    print("[OK] LangGraph Orchestrator Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
