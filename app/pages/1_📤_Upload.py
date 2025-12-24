"""
Upload Page for AutoDoc AI

Allows users to:
- Upload PowerPoint presentations
- AUTO-DETECT model type and year (NEW!)
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

# ================================================================
# NEW: Import PPT analyzer for auto-detection
# ================================================================
try:
    from utils.ppt_analyzer import analyze_ppt, format_confidence
    PPT_ANALYZER_AVAILABLE = True
except ImportError:
    PPT_ANALYZER_AVAILABLE = False
    import logging
    logging.warning("PPT analyzer not available - auto-detection disabled")
# ================================================================


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
    
    # ================================================================
    # NEW: Auto-detection session state
    # ================================================================
    if 'detected_model_type' not in st.session_state:
        st.session_state.detected_model_type = None
    
    if 'detected_year' not in st.session_state:
        st.session_state.detected_year = None
    
    if 'model_confidence' not in st.session_state:
        st.session_state.model_confidence = 0.0
    
    if 'year_confidence' not in st.session_state:
        st.session_state.year_confidence = 0.0
    
    if 'last_uploaded_file' not in st.session_state:
        st.session_state.last_uploaded_file = None
    
    if 'ppt_analyzed' not in st.session_state:
        st.session_state.ppt_analyzed = False
    # ================================================================


def show_upload_section():
    """Display file upload section."""
    st.header("📤 Upload Model Presentation")

    st.markdown("""
    Upload your insurance model PowerPoint presentation to generate comprehensive documentation.

    **Supported formats:** `.pptx`, `.ppt`

    **Recommended structure:** 15-20 slides covering methodology, results, validation, and implementation.
    
    **🎯 NEW:** System will automatically detect model type and year from your PPT!
    """)

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a PowerPoint file",
        type=['pptx', 'ppt'],
        help="Upload your model presentation - we'll auto-detect the model type!",
        key='file_uploader'
    )

    return uploaded_file


# ================================================================
# NEW: Auto-detection function
# ================================================================
def analyze_uploaded_ppt(file_bytes: bytes, filename: str):
    """
    Analyze uploaded PPT to auto-detect model type and year.
    
    Args:
        file_bytes: PPT file bytes
        filename: Original filename
    """
    if not PPT_ANALYZER_AVAILABLE:
        st.warning("⚠️ Auto-detection not available. Please select model type manually.")
        return
    
    # Save to temp file for analysis
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pptx') as tmp_file:
        tmp_file.write(file_bytes)
        tmp_path = tmp_file.name
    
    try:
        with st.spinner("🔍 Analyzing your PPT to detect model type and year..."):
            result = analyze_ppt(tmp_path)
        
        # Store results in session state
        st.session_state.detected_model_type = result.model_type
        st.session_state.detected_year = result.year
        st.session_state.model_confidence = result.model_type_confidence
        st.session_state.year_confidence = result.year_confidence
        st.session_state.ppt_analyzed = True
        
        # Show success message
        col1, col2 = st.columns(2)
        
        with col1:
            confidence_label = format_confidence(result.model_type_confidence)
            if result.model_type != "unknown":
                st.success(f"✅ Detected Model Type: **{result.model_type}** ({confidence_label} confidence)")
            else:
                st.warning("⚠️ Could not auto-detect model type. Please select manually.")
        
        with col2:
            if result.year:
                confidence_label = format_confidence(result.year_confidence)
                st.success(f"✅ Detected Year: **{result.year}** ({confidence_label} confidence)")
            else:
                st.info("ℹ️ Could not detect year. Using default (2024).")
        
        # Show keyword matches if available
        if result.detected_keywords:
            with st.expander("🔍 Detection Details"):
                st.markdown("**Keyword Matches Found:**")
                keyword_counts = [(k, v) for k, v in result.detected_keywords.items() if v > 0]
                keyword_counts.sort(key=lambda x: x[1], reverse=True)
                
                for model_type, count in keyword_counts[:5]:
                    st.write(f"- **{model_type}**: {count} matches")
        
    except Exception as e:
        st.error(f"Error analyzing PPT: {e}")
        st.info("Please select model type manually below.")
    
    finally:
        # Clean up temp file
        import os
        try:
            os.unlink(tmp_path)
        except:
            pass
# ================================================================


def show_configuration_section():
    """Display configuration options for documentation generation (WITH AUTO-DETECTION)."""
    st.header("⚙️ Generation Configuration")
    
    # ================================================================
    # NEW: Show auto-detection results or manual selection
    # ================================================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Model Type")
        
        # Check if we have auto-detected value
        if st.session_state.detected_model_type and st.session_state.detected_model_type != "unknown":
            # Show detected value with confidence
            confidence_badge = format_confidence(st.session_state.model_confidence)
            st.info(f"🎯 **Auto-Detected:** {st.session_state.detected_model_type.upper()}")
            st.caption(f"Confidence: {confidence_badge} ({st.session_state.model_confidence:.0%})")
            
            # Allow override
            manual_override = st.checkbox(
                "Change model type manually?",
                key="override_model",
                help="Check this to select a different model type"
            )
            
            if manual_override:
                model_type = st.selectbox(
                    "Select different model type:",
                    options=['frequency', 'severity', 'pure_premium', 'loss_ratio', 'retention', 'territory', 'comprehensive', 'other'],
                    index=['frequency', 'severity', 'pure_premium', 'loss_ratio', 'retention', 'territory', 'comprehensive', 'other'].index(st.session_state.detected_model_type) if st.session_state.detected_model_type in ['frequency', 'severity', 'pure_premium', 'loss_ratio', 'retention', 'territory', 'comprehensive', 'other'] else 0,
                    help="Override the auto-detected model type"
                )
                st.warning("⚠️ You've overridden the auto-detected value. Make sure this matches your PPT!")
            else:
                model_type = st.session_state.detected_model_type
        else:
            # Fallback to manual selection
            if PPT_ANALYZER_AVAILABLE and st.session_state.ppt_analyzed:
                st.warning("⚠️ Auto-detection unsuccessful")
            
            model_type = st.selectbox(
                "Model Type",
                options=['frequency', 'severity', 'pure_premium', 'loss_ratio', 'retention', 'territory', 'comprehensive', 'other'],
                index=0,
                help="Type of insurance model being documented"
            )
        
        # Document type (keep manual)
        document_type = st.selectbox(
            "Document Type",
            options=['model_doc', 'methodology_update', 'validation_report'],
            index=0,
            help="Type of documentation to generate"
        )
    
    with col2:
        st.markdown("### Model Year")
        
        # Check if we have auto-detected year
        if st.session_state.detected_year:
            # Show detected value with confidence
            confidence_badge = format_confidence(st.session_state.year_confidence)
            st.info(f"🎯 **Auto-Detected:** {st.session_state.detected_year}")
            st.caption(f"Confidence: {confidence_badge} ({st.session_state.year_confidence:.0%})")
            
            # Allow override
            manual_override_year = st.checkbox(
                "Change year manually?",
                key="override_year",
                help="Check this to select a different year"
            )
            
            if manual_override_year:
                year = st.number_input(
                    "Select different year:",
                    min_value=2015,
                    max_value=2030,
                    value=st.session_state.detected_year,
                    step=1,
                    help="Override the auto-detected year"
                )
                st.warning("⚠️ You've overridden the auto-detected value.")
            else:
                year = st.session_state.detected_year
        else:
            # Fallback to manual selection
            if PPT_ANALYZER_AVAILABLE and st.session_state.ppt_analyzed:
                st.info("ℹ️ Year not detected, using default")
            
            year = st.number_input(
                "Model Year",
                min_value=2015,
                max_value=2030,
                value=2024,
                step=1,
                help="Year of model development/implementation"
            )
        
        # Max iterations (keep manual)
        max_iterations = st.slider(
            "Max Quality Iterations",
            min_value=1,
            max_value=5,
            value=3,
            help="Maximum number of revision cycles for quality improvement"
        )
    # ================================================================

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

    # Reset detection state (will re-analyze)
    st.session_state.ppt_analyzed = False
    st.session_state.detected_model_type = None
    st.session_state.detected_year = None

    st.session_state.example_loaded = example_num
    st.success(f"✅ Loaded example: {filepath.name}")
    st.rerun()


def prepare_for_generation():
    """Prepare file for generation - does NOT start generation."""
    if not st.session_state.file_validated:
        st.error("Please upload and validate a file first")
        return

    if not st.session_state.api_key_configured:
        st.error("API key not configured. Please set ANTHROPIC_API_KEY in environment variables.")
        return

    # Show success message and redirect
    # NOTE: We do NOT set processing_started here - that happens in Agent Dashboard
    show_success_box("✅ File validated and ready! Go to the Agent Dashboard to start generation.")

    # Create a button to navigate to dashboard
    st.info("👉 Click **🤖 Agent Dashboard** in the sidebar to generate documentation")


def main():
    """Main upload page."""
    st.set_page_config(
        page_title="Upload - AutoDoc AI",
        page_icon="📤",
        layout="wide"
    )

    init_session_state()

    st.title("📤 Upload Model Presentation")
    
    # ================================================================
    # NEW: Show auto-detection status banner
    # ================================================================
    if PPT_ANALYZER_AVAILABLE:
        st.success("🎯 **Auto-Detection Enabled** - System will automatically identify your model type and year!")
    else:
        st.info("ℹ️ Auto-detection not available. Manual selection will be used. To enable: `pip install python-pptx`")
    # ================================================================
    
    show_disclaimer()

    st.markdown("---")

    # Show template info
    with st.expander("📋 View Recommended Presentation Structure"):
        show_template_info()

    st.markdown("---")

    # Upload section
    uploaded_file = show_upload_section()

    # ================================================================
    # NEW: Reset detection when new file uploaded
    # ================================================================
    if uploaded_file is not None:
        current_file_name = uploaded_file.name
        if st.session_state.last_uploaded_file != current_file_name:
            # New file uploaded - reset detection
            st.session_state.last_uploaded_file = current_file_name
            st.session_state.ppt_analyzed = False
            st.session_state.detected_model_type = None
            st.session_state.detected_year = None
    # ================================================================

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

        # ================================================================
        # NEW: Run auto-detection if not already done
        # ================================================================
        if not st.session_state.ppt_analyzed and PPT_ANALYZER_AVAILABLE:
            st.markdown("---")
            analyze_uploaded_ppt(file_bytes, file_name)
            st.markdown("---")
        # ================================================================

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

            # Configuration section (now with auto-detection!)
            show_configuration_section()

            st.markdown("---")

            # Preparation button
            st.header("🚀 Ready to Generate Documentation")

            col1, col2 = st.columns([1, 3])

            with col1:
                if st.button(
                    "✅ File Ready - Go to Dashboard",
                    type="primary",
                    use_container_width=True,
                    disabled=not st.session_state.api_key_configured
                ):
                    prepare_for_generation()

            with col2:
                if not st.session_state.api_key_configured:
                    st.warning("⚠️ API key not configured. Set ANTHROPIC_API_KEY to enable generation.")
                else:
                    st.info("File is validated and ready. Click the button to confirm, then go to Agent Dashboard to start generation.")

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
