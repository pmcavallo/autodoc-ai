"""
Execution Trace Component for AutoDoc AI Streamlit App

This component displays LangGraph state history for audit purposes.
Shows execution path, decision points, and full state transitions.

Usage in Streamlit:
    from app.components.execution_trace import display_execution_trace
    
    if st.session_state.get('audit_log'):
        display_execution_trace(st.session_state.audit_log)
"""

import streamlit as st
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import json


def display_execution_trace(
    audit_log: Any,
    show_full_history: bool = False,
    expanded: bool = True
) -> None:
    """
    Display execution trace in Streamlit for audit review.
    
    Args:
        audit_log: ExecutionAuditLog object from LangGraphOrchestrator
        show_full_history: Whether to show all state transitions
        expanded: Whether expanders start expanded
    """
    if audit_log is None:
        st.info("No execution history available. Generate a document first.")
        return
    
    # Header with key metrics
    st.subheader("🔍 Execution Audit Trail")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_emoji = "✅" if audit_log.generation_successful else "❌"
        st.metric(
            "Status",
            f"{status_emoji} {'Success' if audit_log.generation_successful else 'Failed'}"
        )
    
    with col2:
        st.metric(
            "Portfolio",
            audit_log.detected_portfolio.replace("_", " ").title()
        )
    
    with col3:
        st.metric(
            "Quality Score",
            f"{audit_log.final_quality_score:.1f}/10"
        )
    
    with col4:
        st.metric(
            "Iterations",
            str(audit_log.total_iterations)
        )
    
    st.markdown("---")
    
    # Execution path visualization
    st.markdown("**Execution Path:**")
    path_str = audit_log.get_path_summary()
    st.code(path_str, language=None)
    
    # Decision points (key for auditors)
    with st.expander("🎯 Decision Points (Routing Decisions)", expanded=expanded):
        decisions = audit_log.get_decision_points()
        
        if decisions:
            for decision in decisions:
                passed = decision.get("passed")
                node = decision.get("node", "unknown")
                routed_to = decision.get("routed_to", "unknown")
                iteration = decision.get("iteration", "-")
                quality = decision.get("quality_score")
                
                if passed is True:
                    st.success(f"**{node.title()}** (Iteration {iteration}) -> ✅ PASSED -> {routed_to}")
                elif passed is False:
                    st.warning(f"**{node.title()}** (Iteration {iteration}) -> ❌ FAILED -> {routed_to}")
                else:
                    st.info(f"**{node.title()}** (Iteration {iteration}) -> routed to {routed_to}")
                
                if quality:
                    st.caption(f"Quality score at decision: {quality:.1f}/10")
        else:
            st.info("No decision points recorded.")
    
    # Full state history (detailed audit)
    if show_full_history:
        with st.expander("📋 Full State History", expanded=False):
            display_state_history_table(audit_log.state_history)
    
    # Copyable audit summary for reports
    with st.expander("📄 Audit Summary (Copyable)", expanded=False):
        summary = generate_audit_summary(audit_log)
        st.text_area(
            "Copy this summary for audit documentation:",
            value=summary,
            height=300,
            key="audit_summary_text"
        )
        
        # JSON export option
        if st.button("📥 Export as JSON"):
            json_data = audit_log.to_dict()
            st.download_button(
                label="Download JSON",
                data=json.dumps(json_data, indent=2, default=str),
                file_name=f"audit_log_{audit_log.thread_id}.json",
                mime="application/json"
            )


def display_state_history_table(state_history: List[Any]) -> None:
    """
    Display state history as a table.
    
    Args:
        state_history: List of StateHistoryEntry objects
    """
    if not state_history:
        st.info("No state history available.")
        return
    
    # Convert to display format
    data = []
    for entry in state_history:
        row = {
            "Step": entry.step,
            "Node": entry.node,
            "Portfolio": entry.portfolio or "-",
            "Iteration": entry.iteration if entry.iteration is not None else "-",
            "Phase": entry.phase or "-",
            "Quality": f"{entry.quality_score:.1f}" if entry.quality_score else "-",
            "Compliance": "✅" if entry.compliance_passed else ("❌" if entry.compliance_passed is False else "-"),
            "Editorial": "✅" if entry.editorial_passed else ("❌" if entry.editorial_passed is False else "-"),
        }
        data.append(row)
    
    # Display as dataframe
    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


def generate_audit_summary(audit_log: Any) -> str:
    """
    Generate a text summary suitable for audit documentation.
    
    Args:
        audit_log: ExecutionAuditLog object
        
    Returns:
        Formatted text summary
    """
    summary_lines = [
        "=" * 60,
        "AUTODOC AI - EXECUTION AUDIT SUMMARY",
        "=" * 60,
        "",
        f"Thread ID:        {audit_log.thread_id}",
        f"Document Title:   {audit_log.document_title}",
        f"Detected Portfolio: {audit_log.detected_portfolio}",
        "",
        f"Start Time:       {audit_log.start_time}",
        f"End Time:         {audit_log.end_time}",
        "",
        f"Generation Status: {'SUCCESS' if audit_log.generation_successful else 'FAILED'}",
        f"Final Quality:    {audit_log.final_quality_score:.1f}/10",
        f"Total Iterations: {audit_log.total_iterations}",
        "",
        "-" * 60,
        "EXECUTION PATH",
        "-" * 60,
        audit_log.get_path_summary(),
        "",
        "-" * 60,
        "DECISION POINTS",
        "-" * 60,
    ]
    
    decisions = audit_log.get_decision_points()
    for decision in decisions:
        passed_str = "PASSED" if decision["passed"] else "FAILED"
        summary_lines.append(
            f"Step {decision['step']}: {decision['node']} -> {passed_str} -> {decision['routed_to']}"
        )
    
    summary_lines.extend([
        "",
        "-" * 60,
        "NARRATIVE SUMMARY",
        "-" * 60,
    ])
    
    # Generate narrative
    narrative = generate_narrative(audit_log)
    summary_lines.append(narrative)
    
    summary_lines.extend([
        "",
        "=" * 60,
        "This audit trail was automatically generated by LangGraph.",
        "=" * 60,
    ])
    
    return "\n".join(summary_lines)


def generate_narrative(audit_log: Any) -> str:
    """
    Generate a human-readable narrative of the execution.
    
    Args:
        audit_log: ExecutionAuditLog object
        
    Returns:
        Narrative string
    """
    portfolio = audit_log.detected_portfolio.replace("_", " ").title()
    iterations = audit_log.total_iterations
    quality = audit_log.final_quality_score
    success = audit_log.generation_successful
    
    decisions = audit_log.get_decision_points()
    
    # Count failures
    compliance_failures = sum(1 for d in decisions if d["node"] == "compliance" and not d["passed"])
    editorial_failures = sum(1 for d in decisions if d["node"] == "editorial" and not d["passed"])
    
    # Build narrative
    parts = []
    parts.append(f"Document was detected as {portfolio}.")
    
    if compliance_failures > 0:
        parts.append(f"Failed compliance {compliance_failures} time(s), requiring revision.")
    else:
        parts.append("Passed compliance on first attempt.")
    
    if editorial_failures > 0:
        parts.append(f"Failed editorial review {editorial_failures} time(s).")
    else:
        parts.append("Passed editorial review.")
    
    if success:
        parts.append(f"Completed successfully after {iterations} iteration(s) with final quality score of {quality:.1f}/10.")
    else:
        parts.append(f"Generation failed after {iterations} iteration(s).")
    
    return " ".join(parts)


def display_execution_summary_sidebar(execution_summary: Dict[str, Any]) -> None:
    """
    Display a compact execution summary in the sidebar.
    
    Args:
        execution_summary: Dictionary from get_execution_summary()
    """
    if not execution_summary or "error" in execution_summary:
        return
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Last Execution")
    
    # Status
    success = execution_summary.get("generation_successful", False)
    status_emoji = "✅" if success else "❌"
    st.sidebar.markdown(f"**Status:** {status_emoji} {'Success' if success else 'Failed'}")
    
    # Portfolio
    portfolio = execution_summary.get("portfolio_detected", "unknown")
    st.sidebar.markdown(f"**Portfolio:** {portfolio.replace('_', ' ').title()}")
    
    # Quality
    quality = execution_summary.get("final_quality_score", "N/A")
    st.sidebar.markdown(f"**Quality:** {quality}")
    
    # Iterations
    iterations = execution_summary.get("total_iterations", 0)
    st.sidebar.markdown(f"**Iterations:** {iterations}")
    
    # Path
    path = execution_summary.get("execution_path", "")
    if path:
        with st.sidebar.expander("Execution Path"):
            st.code(path, language=None)


# =============================================================================
# MERMAID DIAGRAM GENERATION (for enhanced visualization)
# =============================================================================

def generate_execution_mermaid(audit_log: Any) -> str:
    """
    Generate a Mermaid diagram showing the actual execution path.
    
    Args:
        audit_log: ExecutionAuditLog object
        
    Returns:
        Mermaid diagram code
    """
    lines = ["```mermaid", "graph TD"]
    
    # Track which transitions happened
    path = audit_log.execution_path
    
    for i, node in enumerate(path[:-1]):
        next_node = path[i + 1]
        
        # Style based on node type
        if node in ["compliance", "editorial"]:
            # Check if this was a pass or fail
            decisions = audit_log.get_decision_points()
            decision = next((d for d in decisions if d["step"] == i), None)
            
            if decision:
                if decision["passed"]:
                    lines.append(f"    {node}([{node}]) -->|PASSED| {next_node}([{next_node}])")
                else:
                    lines.append(f"    {node}([{node}]) -->|FAILED| {next_node}([{next_node}])")
            else:
                lines.append(f"    {node}([{node}]) --> {next_node}([{next_node}])")
        else:
            lines.append(f"    {node}([{node}]) --> {next_node}([{next_node}])")
    
    # Add styling
    lines.append("    ")
    lines.append("    style complete fill:#90EE90")
    lines.append("    style fail fill:#FFB6C1")
    
    lines.append("```")
    
    return "\n".join(lines)


def display_execution_mermaid(audit_log: Any) -> None:
    """
    Display execution path as a Mermaid diagram.
    
    Args:
        audit_log: ExecutionAuditLog object
    """
    mermaid_code = generate_execution_mermaid(audit_log)
    st.markdown(mermaid_code)
