"""
Upload Page for AutoDoc AI

Allows users to:
- Upload PowerPoint presentations
- Validate file format and content
- Configure generation settings
- Start documentation generation
"""

import streamlit as st
from pathlib import Path
import sys
import io

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.components.disclaimer import show_disclaimer, show_footer, show_success_box, show_error_box
from app.components.ppt_validator import validate_and_display, show_template_info
from document_processing.pptx_parser import PPTXParser, PPTContent, SlideContent


def init_session_state():
    """Initialize session state for upload page."""
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None

    if 'file_validated' not in st.session_state:
        st.session_state.file_validated = False

    if 'validation_result' not in st.session_state:
        st.session_state.validation_result = None

    if 'ppt_content' not in st.session_state:
        st.session_state.ppt_content = None

    if 'generation_config' not in st.session_state:
        st.session_state.generation_config = {
            'model_type': 'frequency',
            'document_type': 'model_doc',
            'year': 2024,
            'max_iterations': 3
        }
    
    # Check API key configuration
    if 'api_key_configured' not in st.session_state:
        import os
        st.session_state.api_key_configured = bool(os.getenv('ANTHROPIC_API_KEY'))


def show_upload_section():
    """Display file upload section."""
    st.header("📤 Upload Model Presentation")

    st.markdown("""
    Upload your insurance model PowerPoint presentation to generate comprehensive documentation.

    **Supported formats:** `.pptx`, `.ppt`

    **Recommended structure:** 15-20 slides covering methodology, results, validation, and implementation.
    """)

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a PowerPoint file",
        type=['pptx', 'ppt'],
        help="Upload your model presentation (10-30 slides recommended)",
        key='file_uploader'
    )

    return uploaded_file


def show_configuration_section():
    """Display configuration options for documentation generation."""
    st.header("⚙️ Generation Configuration")

    col1, col2 = st.columns(2)

    with col1:
        model_type = st.selectbox(
            "Model Type",
            options=['frequency', 'severity', 'territory', 'comprehensive', 'other'],
            index=0,
            help="Type of insurance model being documented"
        )

        document_type = st.selectbox(
            "Document Type",
            options=['model_doc', 'methodology_update', 'validation_report'],
            index=0,
            help="Type of documentation to generate"
        )

    with col2:
        year = st.number_input(
            "Model Year",
            min_value=2020,
            max_value=2030,
            value=2024,
            step=1,
            help="Year of model development/implementation"
        )

        max_iterations = st.slider(
            "Max Quality Iterations",
            min_value=1,
            max_value=5,
            value=3,
            help="Maximum number of revision cycles for quality improvement"
        )

    # Update session state
    st.session_state.generation_config = {
        'model_type': model_type,
        'document_type': document_type,
        'year': year,
        'max_iterations': max_iterations
    }

    # Advanced options
    with st.expander("🔧 Advanced Options"):
        include_charts = st.checkbox(
            "Extract and reference charts",
            value=True,
            help="Extract charts from PPT and reference in documentation"
        )

        include_tables = st.checkbox(
            "Extract and format tables",
            value=True,
            help="Extract tables from PPT and format for documentation"
        )

        detailed_validation = st.checkbox(
            "Include detailed validation section",
            value=True,
            help="Generate comprehensive validation documentation"
        )

        st.session_state.generation_config.update({
            'include_charts': include_charts,
            'include_tables': include_tables,
            'detailed_validation': detailed_validation
        })


def extract_ppt_content(file_bytes: bytes, filename: str):
    """
    Extract structured content from PowerPoint file.

    Args:
        file_bytes: File bytes
        filename: Original filename

    Returns:
        Extracted content dictionary
    """
    try:
        file_stream = io.BytesIO(file_bytes)
        parser = PPTXParser()
        content = parser.extract_from_stream(file_stream)
        return content
    except Exception as e:
        st.error(f"Error extracting PowerPoint content: {str(e)}")
        return None


def show_ppt_preview(content: PPTContent):
    """Display preview of extracted PowerPoint content."""
    st.subheader("📄 Presentation Preview")

    # Summary stats
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Slides", content.total_slides)

    with col2:
        st.metric("Text Blocks", content.total_text_blocks)

    with col3:
        st.metric("Tables", content.total_tables)

    # Slide details
    with st.expander("📋 View All Slides"):
        slides = content.slides

        for i, slide in enumerate(slides, 1):
            st.markdown(f"**Slide {i}: {slide.title or 'Untitled'}**")

            # Show text content
            if slide.text_content:
                for text_block in slide.text_content[:3]:  # Show first 3 blocks
                    st.text(f"• {text_block[:100]}...")

            # Show table info
            if slide.tables:
                st.info(f"Contains {len(slide.tables)} table(s)")

            st.markdown("---")


def load_example_file(example_num: int):
    """
    Load an example PowerPoint file.

    Args:
        example_num: Which example to load (1, 2, or 3)
    """
    example_files = {
        1: "data/examples/bodily_injury_frequency_model.pptx",
        2: "data/examples/collision_severity_model.pptx",
        3: "data/examples/comprehensive_coverage_model.pptx"
    }

    filepath = Path(example_files[example_num])

    if not filepath.exists():
        st.error(f"Example file not found: {filepath}")
        return

    # Read file
    with open(filepath, 'rb') as f:
        file_bytes = f.read()

    # Store in session state (same as uploaded file)
    st.session_state.uploaded_file = {
        'name': filepath.name,
        'bytes': file_bytes,
        'size': len(file_bytes)
    }

    st.session_state.example_loaded = example_num
    st.success(f"✅ Loaded example: {filepath.name}")
    st.rerun()


def start_generation():
    """Start the documentation generation process."""
    if not st.session_state.file_validated:
        st.error("Please upload and validate a file first")
        return

    if not st.session_state.api_key_configured:
        st.error("API key not configured. Please set ANTHROPIC_API_KEY in environment variables.")
        return

    # Update session state
    st.session_state.processing_started = True
    st.session_state.processing_complete = False

    # Show success message and redirect
    show_success_box("Documentation generation started! Navigate to the Agent Dashboard to monitor progress.")

    # Create a button to navigate to dashboard
    st.info("👉 Go to the **🤖 Agent Dashboard** page to see real-time agent activity")


def main():
    """Main upload page."""
    st.set_page_config(
        page_title="Upload - AutoDoc AI",
        page_icon="📤",
        layout="wide"
    )

    init_session_state()

    st.title("📤 Upload Model Presentation")
    show_disclaimer()

    st.markdown("---")

    # Show template info
    with st.expander("📋 View Recommended Presentation Structure"):
        show_template_info()

    st.markdown("---")

    # Upload section
    uploaded_file = show_upload_section()

    if uploaded_file is not None:
        # Store file in session state
        file_bytes = uploaded_file.read()
        st.session_state.uploaded_file = {
            'name': uploaded_file.name,
            'bytes': file_bytes,
            'size': len(file_bytes)
        }

    # Process file if one is loaded (either uploaded or from example)
    if st.session_state.uploaded_file is not None:
        file_bytes = st.session_state.uploaded_file['bytes']
        file_name = st.session_state.uploaded_file['name']

        st.markdown("---")

        # Validate file
        st.header("✅ File Validation")

        with st.spinner("Validating PowerPoint file..."):
            is_valid, result = validate_and_display(file_bytes, file_name)

        st.session_state.file_validated = is_valid
        st.session_state.validation_result = result

        # If valid, extract content
        if is_valid:
            st.markdown("---")

            with st.spinner("Extracting PowerPoint content..."):
                ppt_content = extract_ppt_content(file_bytes, file_name)

            if ppt_content:
                st.session_state.ppt_content = ppt_content
                show_ppt_preview(ppt_content)

            st.markdown("---")

            # Configuration section
            show_configuration_section()

            st.markdown("---")

            # Start generation button
            st.header("🚀 Generate Documentation")

            col1, col2 = st.columns([1, 3])

            with col1:
                if st.button(
                    "▶️ Start Generation",
                    type="primary",
                    use_container_width=True,
                    disabled=not st.session_state.api_key_configured
                ):
                    start_generation()

            with col2:
                if not st.session_state.api_key_configured:
                    st.warning("⚠️ API key not configured. Set ANTHROPIC_API_KEY to enable generation.")
                else:
                    st.info("Click 'Start Generation' to begin. Monitor progress in the Agent Dashboard.")

    else:
        # Show examples section
        st.markdown("---")
        st.header("📚 Example Presentations")

        st.info("""
        Don't have a presentation ready? Try one of our example presentations:

        **Note:** Example presentations are included for demonstration purposes.
        In a production deployment, you would be able to download and use them.
        """)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            **Frequency Model**
            - GLM Poisson regression
            - 12 predictor variables
            - AUC 0.72, Gini 0.44
            """)
            if st.button("📂 Load Example 1", key="example_1", use_container_width=True):
                load_example_file(1)

        with col2:
            st.markdown("""
            **Severity Model**
            - GLM Gamma regression
            - 14 predictor variables
            - R² 0.52, MAPE 24.3%
            """)
            if st.button("📂 Load Example 2", key="example_2", use_container_width=True):
                load_example_file(2)

        with col3:
            st.markdown("""
            **Comprehensive Model**
            - XGBoost + SHAP
            - 42 predictor variables
            - R² 0.58 (freq), 0.44 (sev)
            """)
            if st.button("📂 Load Example 3", key="example_3", use_container_width=True):
                load_example_file(3)

    st.markdown("---")
    show_footer()


if __name__ == "__main__":
    main()
