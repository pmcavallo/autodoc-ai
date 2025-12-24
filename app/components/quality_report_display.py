"""
Component for displaying LLM-as-Judge Quality Reports in Streamlit

Shows:
- Overall quality score
- 6 dimension scores (Source Fidelity, Technical Accuracy, etc.)
- Critical issues
- Recommended improvements
- Iteration history
"""

import streamlit as st
from typing import Optional


def display_quality_report(quality_report, show_details=True):
    """
    Display LLM-as-judge quality evaluation report.
    
    Args:
        quality_report: QualityReport object from editor_agent
        show_details: Whether to show detailed feedback
    """
    if not quality_report:
        return
    
    # Overall score with color coding
    st.subheader("📊 LLM-as-Judge Quality Evaluation")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Overall score
        score = quality_report.overall_score
        if score >= 8.0:
            st.success(f"**{score:.1f}/10.0**")
            st.success("✓ EXCELLENT")
        elif score >= 7.0:
            st.success(f"**{score:.1f}/10.0**")
            st.success("✓ READY")
        elif score >= 5.0:
            st.warning(f"**{score:.1f}/10.0**")
            st.warning("⚠ NEEDS WORK")
        else:
            st.error(f"**{score:.1f}/10.0**")
            st.error("✗ POOR QUALITY")
    
    with col2:
        if quality_report.ready_for_submission:
            st.success("**✓ Ready for Submission**")
            st.caption("Document meets quality standards (score ≥ 7.0)")
        else:
            st.error("**✗ Not Ready for Submission**")
            st.caption(f"Document needs revision (score < 7.0)")
    
    st.markdown("---")
    
    # Dimension scores
    st.subheader("📈 Dimension Scores")
    
    dimensions = quality_report.dimension_scores
    
    # Source Fidelity (most important) - Show first and highlighted
    if 'source_fidelity' in dimensions:
        fidelity_score = dimensions['source_fidelity']
        
        st.markdown("### 🎯 Source Fidelity (Accuracy Check)")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if fidelity_score >= 9.0:
                st.success(f"**{fidelity_score:.1f}/10**")
            elif fidelity_score >= 7.0:
                st.warning(f"**{fidelity_score:.1f}/10**")
            else:
                st.error(f"**{fidelity_score:.1f}/10**")
        
        with col2:
            if fidelity_score >= 9.0:
                st.success("✓ All metrics match source PowerPoint")
                st.caption("Numbers, dates, sample sizes, and performance metrics verified")
            elif fidelity_score >= 7.0:
                st.warning("⚠ Minor discrepancies detected")
                st.caption("Most metrics match, but some differences found")
            else:
                st.error("✗ Significant mismatches")
                st.caption("Metrics don't match source - review required")
        
        st.markdown("---")
    
    # Other dimensions in 2 columns
    st.markdown("### 📊 Other Quality Dimensions")
    
    col1, col2 = st.columns(2)
    
    dimension_order = [
        ('technical_accuracy', 'Technical Accuracy', '🔬'),
        ('completeness', 'Completeness', '📋'),
        ('clarity', 'Clarity & Readability', '📖'),
        ('compliance', 'Regulatory Compliance', '⚖️'),
        ('professional_tone', 'Professional Tone', '💼')
    ]
    
    for i, (key, label, icon) in enumerate(dimension_order):
        if key not in dimensions:
            continue
            
        score = dimensions[key]
        
        # Alternate between columns
        target_col = col1 if i % 2 == 0 else col2
        
        with target_col:
            st.markdown(f"**{icon} {label}**")
            
            # Progress bar with color
            if score >= 7.0:
                st.progress(score / 10.0)
                st.caption(f"✓ {score:.1f}/10")
            else:
                st.progress(score / 10.0)
                st.caption(f"✗ {score:.1f}/10 - Needs improvement")
    
    if show_details:
        st.markdown("---")
        
        # Critical Issues
        if quality_report.critical_issues:
            st.subheader("🚨 Critical Issues (MUST FIX)")
            for issue in quality_report.critical_issues:
                st.error(f"✗ {issue}")
        
        # Recommended Improvements
        if quality_report.recommended_improvements:
            st.subheader("💡 Recommended Improvements")
            for improvement in quality_report.recommended_improvements[:5]:  # Show top 5
                st.info(f"→ {improvement}")
        
        # Sections to revise
        if quality_report.sections_to_revise:
            st.subheader("📝 Sections Needing Revision")
            st.write(", ".join(quality_report.sections_to_revise))


def display_iteration_history(workflow_state):
    """
    Display quality score progression across iterations.
    
    Args:
        workflow_state: WorkflowState with iteration_history
    """
    if not workflow_state or not workflow_state.iteration_history:
        return
    
    st.subheader("🔄 Iteration History")
    st.caption("Quality scores improving across revisions")
    
    # Create table
    history_data = []
    
    for iter_data in workflow_state.iteration_history:
        row = {
            'Iteration': iter_data['iteration'],
            'Overall Score': f"{iter_data.get('overall_score', 0):.1f}/10" if 'overall_score' in iter_data else "N/A",
            'Status': '✓ Ready' if iter_data.get('ready', False) else '✗ Needs Work',
        }
        
        # Add Source Fidelity if available
        if 'dimension_scores' in iter_data and 'source_fidelity' in iter_data['dimension_scores']:
            row['Source Fidelity'] = f"{iter_data['dimension_scores']['source_fidelity']:.1f}/10"
        
        history_data.append(row)
    
    # Display as dataframe
    import pandas as pd
    df = pd.DataFrame(history_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Show improvement
    if len(workflow_state.iteration_history) > 1:
        first_score = workflow_state.iteration_history[0].get('overall_score', 0)
        last_score = workflow_state.iteration_history[-1].get('overall_score', 0)
        
        if last_score > first_score:
            improvement = last_score - first_score
            st.success(f"📈 Quality improved by {improvement:.1f} points across iterations")
        elif last_score == first_score:
            st.info("📊 Quality remained consistent across iterations")


def display_quality_summary_card(quality_report):
    """
    Display a compact quality summary card (for dashboard view).
    
    Args:
        quality_report: QualityReport object
    """
    if not quality_report:
        return
    
    score = quality_report.overall_score
    
    # Color-coded card
    if score >= 7.0:
        st.success(f"""
        **Quality Score: {score:.1f}/10.0** ✓
        
        Ready for submission
        """)
    else:
        st.warning(f"""
        **Quality Score: {score:.1f}/10.0** ⚠
        
        Needs revision
        """)
    
    # Show Source Fidelity specifically
    if 'source_fidelity' in quality_report.dimension_scores:
        fidelity = quality_report.dimension_scores['source_fidelity']
        if fidelity >= 9.0:
            st.success(f"✓ Source Fidelity: {fidelity:.1f}/10 - All metrics verified")
        elif fidelity >= 7.0:
            st.warning(f"⚠ Source Fidelity: {fidelity:.1f}/10 - Minor discrepancies")
        else:
            st.error(f"✗ Source Fidelity: {fidelity:.1f}/10 - Significant mismatches")
