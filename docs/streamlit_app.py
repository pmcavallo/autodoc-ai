"""
AutoDoc AI - Main Streamlit Application

Multi-agent RAG system for automated insurance model documentation.

Entry point for the Streamlit application with:
- Home/welcome page
- Navigation to upload, dashboard, and results pages
- Session state management
- Configuration and initialization
"""

import streamlit as st
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.components.disclaimer import show_disclaimer, show_footer
from app.components.cost_tracker import CostTracker, display_cost_dashboard


def init_session_state():
    """Initialize Streamlit session state variables."""
    # File upload state
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None

    if 'file_validated' not in st.session_state:
        st.session_state.file_validated = False

    # Processing state
    if 'processing_started' not in st.session_state:
        st.session_state.processing_started = False

    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False

    # Generated document
    if 'generated_document' not in st.session_state:
        st.session_state.generated_document = None

    if 'document_metadata' not in st.session_state:
        st.session_state.document_metadata = {}

    # Agent workflow state
    if 'workflow_state' not in st.session_state:
        st.session_state.workflow_state = None

    # Cost tracking
    if 'cost_tracker' not in st.session_state:
        st.session_state.cost_tracker = CostTracker()

    # Rate limiting (NEW)
    if 'rate_limiter' not in st.session_state:
        from rate_limiter import RateLimiter
        st.session_state.rate_limiter = RateLimiter(
            data_dir="data",
            max_per_user=3,
            max_daily_total=100
        )

    # Configuration
    if 'show_agent_progress' not in st.session_state:
        st.session_state.show_agent_progress = True

    if 'api_key_configured' not in st.session_state:
        # Check if API key is set in environment
        st.session_state.api_key_configured = bool(os.getenv('ANTHROPIC_API_KEY'))


def show_home_page():
    """Display the home/welcome page."""

    # Hero section
    st.title("🤖 AutoDoc AI")
    st.subheader("Automated Insurance Model Documentation Generator")

    show_disclaimer()

    st.markdown("---")

    # Value proposition
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ## Transform PowerPoint to Audit-Ready Documentation

        **AutoDoc AI** uses a multi-agent RAG system to automatically generate comprehensive
        model documentation from your PowerPoint presentations.

        ### How It Works

        1. **📤 Upload** - Upload your model presentation (PowerPoint)
        2. **🤖 Process** - Multi-agent system analyzes and generates documentation
        3. **📊 Review** - Preview generated documentation with quality scores
        4. **📥 Download** - Get audit-ready PDF White Paper

        ### Key Benefits

        - ⏱️ **60-75% Time Savings** - 40 hours → 10 hours per model
        - 💰 **$8K-15K Cost Savings** per model
        - ✅ **Built-in Compliance** - NAIC, ASOPs standards enforced
        - 📈 **Consistent Quality** - Standardized documentation across all models
        """)

    with col2:
        st.info("""
        **Tech Stack**

        🧠 **LLM**
        Claude Haiku 4.5

        🔎 **RAG**
        ChromaDB

        🤖 **Orchestration**
        Multi-Agent System

        📊 **UI**
        Streamlit

        🚀 **Deployment**
        Render / HF Spaces
        """)

    st.markdown("---")

    # Multi-agent system overview
    st.header("🔬 Multi-Agent Architecture")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        **1️⃣ Research Agent**

        Queries knowledge base:
        - Past model docs
        - Regulations (NAIC, ASOPs)
        - Audit findings
        - Best practices
        """)

    with col2:
        st.markdown("""
        **2️⃣ Writer Agent**

        Generates sections:
        - Executive Summary
        - Methodology
        - Validation
        - Implementation
        - And more...
        """)

    with col3:
        st.markdown("""
        **3️⃣ Compliance Agent**

        Validates against:
        - NAIC Model Audit Rule
        - ASOP 12, 23, 41, 56
        - Required sections
        - Citation quality
        """)

    with col4:
        st.markdown("""
        **4️⃣ Editor Agent**

        Reviews for:
        - Clarity & readability
        - Consistency
        - Professional style
        - Proper structure
        """)

    st.info("""
    💡 **Iterative Quality Loop**: If compliance or editorial checks fail, the system
    automatically revises the document until quality standards are met (max 3 iterations).
    """)

    st.markdown("---")

    # Getting started
    st.header("🚀 Get Started")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Option 1: Upload Your Presentation

        Have a model presentation ready?

        1. Go to the **📤 Upload** page
        2. Upload your PowerPoint file
        3. Start the documentation generation

        👉 Use the sidebar to navigate to **Upload**
        """)

    with col2:
        st.markdown("""
        ### Option 2: Use Example Presentations

        Don't have a presentation yet?

        Try one of our example presentations:
        - Frequency Model (GLM)
        - Severity Model (GLM)
        - Territory Rating (Clustering)

        👉 Examples available on the **Upload** page
        """)

    # API Key warning
    if not st.session_state.api_key_configured:
        st.warning("""
        ⚠️ **API Key Not Configured**

        To generate documentation, you need to configure your Anthropic API key.

        For local development:
        1. Create a `.env` file in the project root
        2. Add: `ANTHROPIC_API_KEY=your_api_key_here`

        For deployment (Render/HF Spaces):
        1. Go to Settings > Environment Variables/Secrets
        2. Add `ANTHROPIC_API_KEY` with your key
        """)

    st.markdown("---")

    # Performance metrics
    st.header("📊 Performance Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Time Savings",
            "60-75%",
            delta="30-40 hours saved"
        )

    with col2:
        st.metric(
            "Cost per Model",
            "~$0.02",
            delta="12x cheaper (Haiku vs Sonnet)",
            delta_color="inverse"
        )

    with col3:
        st.metric(
            "Quality Score",
            "8.7/10",
            delta="+2.3 vs manual"
        )

    with col4:
        st.metric(
            "ROI",
            "2,000%+",
            delta="At 10 models/quarter"
        )

    st.markdown("---")

    # Rate limiting info (NEW)
    st.header("🔒 Demo Rate Limits")
    
    st.info("""
    **Cost Protection During Demo:**
    - 📋 **Per User**: 3 documents per day
    - 🌐 **Global**: 100 documents per day ($2 daily budget)
    - ⏰ **Reset**: Every 24 hours
    
    These limits protect against unexpected costs during the demo period.
    """)

    st.markdown("---")

    show_footer()


def main():
    """Main application entry point."""

    # Page configuration
    st.set_page_config(
        page_title="AutoDoc AI - Automated Model Documentation",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    init_session_state()

    # Sidebar
    with st.sidebar:
        st.title("🤖 AutoDoc AI")
        st.markdown("---")

        # Navigation info
        st.markdown("""
        **Navigation**

        Use the pages above to:
        - 📤 Upload presentations
        - 🤖 Monitor agent progress
        - 📊 View results & download
        """)

        st.markdown("---")

        # Settings
        st.subheader("⚙️ Settings")

        show_progress = st.checkbox(
            "Show agent progress",
            value=st.session_state.show_agent_progress,
            help="Display real-time agent activity during processing"
        )
        st.session_state.show_agent_progress = show_progress

        st.markdown("---")

        # Status
        st.subheader("📋 Status")

        if st.session_state.uploaded_file:
            st.success("✅ File uploaded")
        else:
            st.info("⏳ No file uploaded")

        if st.session_state.processing_complete:
            st.success("✅ Processing complete")
        elif st.session_state.processing_started:
            st.warning("⚙️ Processing...")
        else:
            st.info("⏳ Not started")

        st.markdown("---")

        # API Key status
        if st.session_state.api_key_configured:
            st.success("🔑 API Key: Configured")
        else:
            st.error("🔑 API Key: Not configured")

        st.markdown("---")

        # Rate limit stats (NEW)
        st.subheader("📊 Rate Limit Stats")
        
        if 'rate_limiter' in st.session_state:
            limiter = st.session_state.rate_limiter
            stats = limiter.get_stats()
            
            st.metric("Daily Generations", f"{stats['total_generations_today']}/{stats['global_limit']}")
            st.metric("Budget Used", f"${stats['total_generations_today'] * 0.02:.2f} / $2.00")
            
            # Show remaining budget
            remaining_budget = (stats['global_remaining'] * 0.02)
            st.progress(1 - (stats['total_generations_today'] / stats['global_limit']))
            st.caption(f"${remaining_budget:.2f} remaining today")

    # Main content area - Home page
    show_home_page()


if __name__ == "__main__":
    main()
