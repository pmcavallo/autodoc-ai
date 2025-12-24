"""
Agent Dashboard Page for AutoDoc AI

Real-time monitoring of multi-agent documentation generation:
- Agent activity and status
- Workflow progress
- Compliance and quality checks
- Token usage and costs

FIXED VERSION: Now extracts and passes PPT content to orchestrator
"""

import streamlit as st
from pathlib import Path
import sys
import time
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.components.disclaimer import show_disclaimer, show_footer, show_agent_info_box
from app.components.cost_tracker import display_cost_dashboard
from agents.orchestrator import DocumentationOrchestrator, GenerationRequest, WorkflowStatus


def init_session_state():
    """Initialize session state for dashboard page."""
    if 'processing_started' not in st.session_state:
        st.session_state.processing_started = False

    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False

    if 'workflow_state' not in st.session_state:
        st.session_state.workflow_state = None

    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = None

    if 'workflow_logs' not in st.session_state:
        st.session_state.workflow_logs = []

    if 'cost_tracker' not in st.session_state:
        from app.components.cost_tracker import CostTracker
        st.session_state.cost_tracker = CostTracker()


def show_workflow_status():
    """Display current workflow status and progress."""
    st.header("📊 Workflow Status")

    if not st.session_state.processing_started:
        st.info("""
        ⏳ **No active workflow**

        Upload a PowerPoint presentation on the Upload page to start documentation generation.
        """)
        return

    # Progress bar
    if st.session_state.workflow_state:
        state = st.session_state.workflow_state
        progress = (state.current_iteration / state.max_iterations) * 100
        st.progress(progress / 100)
        st.caption(f"Iteration {state.current_iteration} of {state.max_iterations}")
    else:
        st.progress(0)

    st.markdown("---")

    # Workflow phases
    st.subheader("🔄 Workflow Phases")

    phases = [
        ("Research", "Gathering context from knowledge base"),
        ("Writing", "Generating documentation sections"),
        ("Compliance", "Checking regulatory requirements"),
        ("Editorial", "Reviewing quality and style"),
        ("Revision", "Improving based on feedback")
    ]

    # Determine current phase
    current_status = None
    if st.session_state.workflow_state:
        current_status = st.session_state.workflow_state.status

    for phase_name, phase_desc in phases:
        # Determine status for this phase
        if current_status:
            if phase_name.upper() in current_status.name:
                status = "working"
            elif st.session_state.workflow_state.research_complete and phase_name == "Research":
                status = "complete"
            elif st.session_state.workflow_state.writing_complete and phase_name == "Writing":
                status = "complete"
            elif st.session_state.workflow_state.compliance_passed and phase_name == "Compliance":
                status = "complete"
            elif st.session_state.workflow_state.editorial_approved and phase_name == "Editorial":
                status = "complete"
            else:
                status = "idle"
        else:
            status = "idle"

        show_agent_info_box(phase_name, phase_desc, status)


def show_agent_activity():
    """Display detailed agent activity."""
    st.header("🤖 Agent Activity")

    if not st.session_state.processing_started:
        st.info("No active agents. Start a documentation generation to see agent activity.")
        return

    # Create tabs for each agent
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Research Agent",
        "✍️ Writer Agent",
        "✅ Compliance Agent",
        "📝 Editor Agent"
    ])

    with tab1:
        st.subheader("Research Agent Activity")
        st.markdown("""
        **Role:** Query knowledge base for relevant context

        **Capabilities:**
        - RAG retrieval from past model docs
        - Regulatory requirements lookup
        - Audit findings research
        - Best practices extraction
        """)

        if st.session_state.workflow_state and st.session_state.workflow_state.research_complete:
            st.success("✅ Research phase complete")

            # Show sample research findings (mock data for demo)
            with st.expander("📚 Research Findings Summary"):
                st.markdown("""
                **Context Gathered:**
                - 15 relevant chunks from past documentations
                - 8 regulatory requirement sections
                - 3 audit finding examples
                - 5 best practice guidelines

                **Confidence:** High (0.82 average similarity score)
                """)
        else:
            st.info("⏳ Research not started or in progress")

    with tab2:
        st.subheader("Writer Agent Activity")
        st.markdown("""
        **Role:** Generate documentation sections

        **Capabilities:**
        - Template-based generation
        - Context-aware writing
        - Citation management
        - Section assembly
        """)

        if st.session_state.workflow_state and st.session_state.workflow_state.writing_complete:
            st.success("✅ Writing phase complete")

            sections = st.session_state.workflow_state.sections_generated
            if sections:
                with st.expander(f"📄 Generated Sections ({len(sections)})"):
                    for i, section in enumerate(sections, 1):
                        st.markdown(f"**{i}. {section.title}**")
                        st.caption(f"Words: {section.word_count}, Citations: {len(section.sources_cited)}")
        else:
            st.info("⏳ Writing not started or in progress")

    with tab3:
        st.subheader("Compliance Agent Activity")
        st.markdown("""
        **Role:** Validate regulatory compliance

        **Capabilities:**
        - NAIC Model Audit Rule checking
        - ASOP compliance (12, 23, 41, 56)
        - Required section validation
        - Citation quality checks
        """)

        if st.session_state.workflow_state and st.session_state.workflow_state.compliance_report:
            report = st.session_state.workflow_state.compliance_report

            if st.session_state.workflow_state.compliance_passed:
                st.success("✅ Compliance checks passed")
            else:
                st.warning("⚠️ Compliance issues found")

            with st.expander("📋 Compliance Report"):
                st.markdown(f"""
                **Overall Status:** {report.overall_status}

                **Findings:**
                - Critical: {sum(1 for f in report.findings if f.severity.name == 'CRITICAL')}
                - High: {sum(1 for f in report.findings if f.severity.name == 'HIGH')}
                - Medium: {sum(1 for f in report.findings if f.severity.name == 'MEDIUM')}
                - Low: {sum(1 for f in report.findings if f.severity.name == 'LOW')}
                """)
        else:
            st.info("⏳ Compliance check not started or in progress")

    with tab4:
        st.subheader("Editor Agent Activity")
        st.markdown("""
        **Role:** Review and improve quality

        **Capabilities:**
        - Readability scoring
        - Style guide enforcement
        - Consistency checking
        - Improvement suggestions
        """)

        if st.session_state.workflow_state and st.session_state.workflow_state.editorial_review:
            review = st.session_state.workflow_state.editorial_review

            if st.session_state.workflow_state.editorial_approved:
                st.success("✅ Editorial review passed")
            else:
                st.warning("⚠️ Editorial improvements recommended")

            with st.expander("📝 Editorial Review"):
                st.markdown(f"""
                **Overall Quality:** {review.overall_quality}
                **Readability Score:** {review.readability_score:.1f}/10

                **Findings:**
                - Critical: {sum(1 for f in review.findings if f.priority.name == 'CRITICAL')}
                - High: {sum(1 for f in review.findings if f.priority.name == 'HIGH')}
                - Medium: {sum(1 for f in review.findings if f.priority.name == 'MEDIUM')}
                - Low: {sum(1 for f in review.findings if f.priority.name == 'LOW')}
                """)
        else:
            st.info("⏳ Editorial review not started or in progress")


def show_workflow_logs():
    """Display workflow event logs."""
    st.header("📋 Workflow Logs")

    if not st.session_state.workflow_logs:
        st.info("No workflow events logged yet.")
        return

    for log_entry in reversed(st.session_state.workflow_logs[-10:]):  # Show last 10
        timestamp = log_entry.get('timestamp', 'N/A')
        event = log_entry.get('event', 'Event')
        message = log_entry.get('message', '')
        level = log_entry.get('level', 'info')

        if level == 'error':
            st.error(f"[{timestamp}] {event}: {message}")
        elif level == 'warning':
            st.warning(f"[{timestamp}] {event}: {message}")
        elif level == 'success':
            st.success(f"[{timestamp}] {event}: {message}")
        else:
            st.info(f"[{timestamp}] {event}: {message}")


def start_documentation_generation():
    """
    Start real documentation generation using the orchestrator.

    This function integrates with the backend orchestrator to:
    - Parse uploaded PowerPoint content
    - Create a generation request
    - Run the multi-agent workflow
    - Stream results to the UI
    
    FIXED: Now extracts full PPT content and passes to orchestrator
    """
    import os
    import datetime
    from rag.retrieval import DocumentRetriever

    # Check API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        st.error("""
        ⚠️ **API Key Not Configured**

        Please set the ANTHROPIC_API_KEY environment variable to use the documentation generation feature.

        You can still explore the demo mode to see how the system works.
        """)
        if st.button("🎬 Run Demo Mode Instead", type="secondary"):
            simulate_demo_workflow()
        return

    # Check if file uploaded
    if not st.session_state.get('ppt_content'):
        st.warning("Please upload a PowerPoint file on the Upload page first.")
        return

    # Get configuration
    config = st.session_state.get('generation_config', {})
    ppt_content = st.session_state.ppt_content

    # Show configuration
    st.info(f"""
    **Ready to Generate Documentation**

    - **File:** {ppt_content.filename}
    - **Slides:** {ppt_content.total_slides}
    - **Model Type:** {config.get('model_type', 'frequency')}
    - **Document Type:** {config.get('document_type', 'model_doc')}
    - **Max Iterations:** {config.get('max_iterations', 3)}
    """)

    if st.button("🚀 Start Generation", type="primary"):
        st.session_state.processing_started = True

        now = datetime.datetime.now().strftime("%H:%M:%S")

        with st.spinner("Initializing orchestrator..."):
            try:
                # Initialize orchestrator
                orchestrator = DocumentationOrchestrator(
                    max_iterations=config.get('max_iterations', 3)
                )

                # ============================================================
                # CRITICAL FIX: Extract full text content from PPT
                # ============================================================
                st.info("📄 Extracting content from PowerPoint...")
                ppt_text_content = []
                
                for slide in ppt_content.slides:
                    # Build slide text with title and content
                    slide_text = f"Slide {slide.slide_number}: {slide.title or 'Untitled'}\n"
                    
                    # Add all text content
                    if slide.text_content:
                        slide_text += "\n".join(slide.text_content)
                    
                    # Note tables (actual table parsing would go here)
                    if slide.tables:
                        slide_text += f"\n[Contains {len(slide.tables)} table(s)]"
                        # In production, you'd extract table data here
                    
                    ppt_text_content.append(slide_text)
                
                # Join all slide content into one string
                full_ppt_content = "\n\n".join(ppt_text_content)
                
                st.success(f"✅ Extracted {len(full_ppt_content)} characters from {ppt_content.total_slides} slides")
                # ============================================================

                # Create generation request WITH SOURCE CONTENT
                request = GenerationRequest(
                    document_title=f"{config.get('model_type', 'Model')} Documentation",
                    document_type=config.get('document_type', 'model_doc'),
                    model_type=config.get('model_type'),
                    year=config.get('year', 2024),
                    sections_required=DocumentationOrchestrator.STANDARD_MODEL_SECTIONS,
                    additional_context=full_ppt_content,  # ← CRITICAL FIX: Pass PPT content
                    metadata={
                        'source_file': ppt_content.filename,
                        'total_slides': ppt_content.total_slides,
                        'total_tables': ppt_content.total_tables
                    }
                )

                # Log start
                st.session_state.workflow_logs.append({
                    "timestamp": now,
                    "event": "Generation Started",
                    "message": f"Starting {request.document_title}",
                    "level": "info"
                })

                # Run generation (this will take time)
                with st.spinner("Generating documentation... This may take several minutes."):
                    final_document, workflow_state = orchestrator.generate_documentation(request)

                    # Store results
                    st.session_state.workflow_state = workflow_state
                    st.session_state.generated_document = final_document
                    st.session_state.processing_complete = True

                    # Record costs from generated sections
                    if 'cost_tracker' not in st.session_state:
                        from app.components.cost_tracker import CostTracker
                        st.session_state.cost_tracker = CostTracker()

                    # Extract token usage from sections and record in cost tracker
                    if workflow_state.sections_generated:
                        for section in workflow_state.sections_generated:
                            if 'input_tokens' in section.metadata and 'output_tokens' in section.metadata:
                                st.session_state.cost_tracker.record_usage(
                                    agent="Writer Agent",
                                    operation=f"Generate {section.title}",
                                    input_tokens=section.metadata['input_tokens'],
                                    output_tokens=section.metadata['output_tokens']
                                )

                    # Log completion
                    st.session_state.workflow_logs.append({
                        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                        "event": "Generation Complete",
                        "message": f"Generated {len(final_document)} characters",
                        "level": "success"
                    })

                    # Rerun to show completion message at top of page
                    st.rerun()

            except Exception as e:
                st.error(f"Error during generation: {str(e)}")
                st.session_state.workflow_logs.append({
                    "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                    "event": "Generation Failed",
                    "message": str(e),
                    "level": "error"
                })


def simulate_demo_workflow():
    """
    Simulate workflow for demo purposes when API key is not available.
    """
    import datetime

    now = datetime.datetime.now().strftime("%H:%M:%S")

    sample_logs = [
        {"timestamp": now, "event": "Research Started", "message": "Querying knowledge base", "level": "info"},
        {"timestamp": now, "event": "Research Complete", "message": "Found 15 relevant chunks", "level": "success"},
        {"timestamp": now, "event": "Writing Started", "message": "Generating Executive Summary", "level": "info"},
        {"timestamp": now, "event": "Writing Complete", "message": "8 sections generated", "level": "success"},
    ]

    st.session_state.workflow_logs.extend(sample_logs)
    st.session_state.processing_started = True
    st.info("Demo workflow simulated. In production mode with an API key, real documentation would be generated.")
    st.rerun()


def main():
    """Main agent dashboard page."""
    st.set_page_config(
        page_title="Agent Dashboard - AutoDoc AI",
        page_icon="🤖",
        layout="wide"
    )

    init_session_state()

    st.title("🤖 Agent Dashboard")
    show_disclaimer()

    st.markdown("---")

    # Show completion message if processing just finished
    if st.session_state.get('processing_complete', False) and st.session_state.get('generated_document'):
        st.success("✅ Documentation generation complete!")
        st.info("👉 **Go to the Results page** (in the sidebar) to view and download your document.")

        # Show quick stats
        doc_length = len(st.session_state.generated_document)
        word_count = len(st.session_state.generated_document.split())
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Document Size", f"{doc_length:,} characters")
        with col2:
            st.metric("Word Count", f"{word_count:,} words")

        st.markdown("---")

    # Show workflow status
    show_workflow_status()

    st.markdown("---")

    # Show agent activity
    show_agent_activity()

    st.markdown("---")

    # Cost tracking
    if 'cost_tracker' in st.session_state:
        display_cost_dashboard(st.session_state.cost_tracker)

        st.markdown("---")

    # Workflow logs
    show_workflow_logs()

    st.markdown("---")

    # Documentation generation
    st.header("🚀 Generate Documentation")
    start_documentation_generation()

    st.markdown("---")
    show_footer()


if __name__ == "__main__":
    main()
