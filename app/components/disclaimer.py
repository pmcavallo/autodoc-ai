"""
Disclaimer Component for AutoDoc AI Streamlit App

Displays synthetic data warning banner across all pages.
"""

import streamlit as st


def show_disclaimer():
    """
    Display prominent synthetic data disclaimer banner.

    This warning appears on all pages to remind users that this is
    a demonstration system using entirely fictional data.
    """
    st.warning(
        "⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**\n\n"
        "This application uses entirely synthetic data created for portfolio "
        "demonstration purposes. No real insurance data, customer information, "
        "proprietary methodologies, or confidential information from any insurance "
        "company or financial institution is used or simulated."
    )


def show_footer():
    """Display footer with project information."""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p><strong>AutoDoc AI</strong> - Automated Insurance Model Documentation</p>
            <p style='font-size: 0.9em;'>
                Multi-agent RAG system demonstrating AI-powered documentation automation
            </p>
            <p style='font-size: 0.8em;'>
                Tech Stack: Claude Sonnet 4 • ChromaDB • Streamlit • LangGraph
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_agent_info_box(agent_name: str, description: str, status: str = "idle"):
    """
    Display information box for an agent.

    Args:
        agent_name: Name of the agent
        description: Brief description of agent's role
        status: Current status (idle, working, complete, error)
    """
    status_colors = {
        "idle": "🔵",
        "working": "🟡",
        "complete": "🟢",
        "error": "🔴"
    }

    status_emoji = status_colors.get(status, "⚪")

    st.markdown(
        f"""
        <div style='padding: 10px; border-left: 4px solid #1f77b4; background-color: #f0f2f6; margin: 10px 0;'>
            <strong>{status_emoji} {agent_name}</strong><br/>
            <span style='font-size: 0.9em; color: #666;'>{description}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_warning_box(message: str):
    """Display a warning message box."""
    st.warning(f"⚠️ {message}")


def show_success_box(message: str):
    """Display a success message box."""
    st.success(f"✅ {message}")


def show_error_box(message: str):
    """Display an error message box."""
    st.error(f"❌ {message}")


def show_info_box(message: str):
    """Display an info message box."""
    st.info(f"ℹ️ {message}")


if __name__ == "__main__":
    # Test the disclaimer component
    st.set_page_config(page_title="Disclaimer Test", layout="wide")

    st.title("Disclaimer Component Test")

    show_disclaimer()

    st.header("Agent Info Boxes")
    show_agent_info_box("Research Agent", "Gathering context from knowledge base", "working")
    show_agent_info_box("Writer Agent", "Generating documentation sections", "complete")
    show_agent_info_box("Compliance Agent", "Checking regulatory requirements", "idle")
    show_agent_info_box("Editor Agent", "Reviewing document quality", "error")

    st.header("Message Boxes")
    show_success_box("Document generated successfully!")
    show_warning_box("API key not configured")
    show_error_box("Failed to parse PowerPoint file")
    show_info_box("Upload a PowerPoint file to get started")

    show_footer()
