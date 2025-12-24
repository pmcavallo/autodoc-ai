"""
Node functions for AutoDoc AI LangGraph workflow.

Each node is a function that:
1. Receives the current state
2. Performs some operation
3. Returns updated state (partial update)

LangGraph merges the returned dict into the existing state.
"""

import logging
from typing import Dict, Any

from config.portfolio_configs import PortfolioRegistry

logger = logging.getLogger(__name__)

# Initialize shared components (lazy loading)
_retriever = None
_registry = None


def get_retriever():
    """Lazily initialize the document retriever."""
    global _retriever
    if _retriever is None:
        from rag.retrieval import DocumentRetriever
        _retriever = DocumentRetriever()
    return _retriever


def get_registry():
    """Lazily initialize the portfolio registry."""
    global _registry
    if _registry is None:
        _registry = PortfolioRegistry()
    return _registry


# ============================================================
# NODE: detect_portfolio
# ============================================================
def detect_portfolio(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detect the insurance portfolio from source content.

    Analyzes keywords in source_content to determine which
    portfolio (personal_auto, homeowners, workers_comp, commercial_auto)
    the document belongs to.
    """
    logger.info("[Node: detect_portfolio] Starting portfolio detection")

    source_content = state.get("source_content", "").lower()

    # Keyword sets for each portfolio
    PORTFOLIO_KEYWORDS = {
        "personal_auto": [
            "driver age", "vehicle type", "collision", "bodily injury", "territory",
            "prior claims", "comprehensive", "liability", "pip", "uninsured motorist",
            "deductible", "annual mileage", "good driver", "multi-car",
            "credit score", "garaging", "symbol", "model year", "vehicle age"
        ],
        "homeowners": [
            "dwelling", "protection class", "cat ", "hurricane", "hail", "roof",
            "construction type", "fire", "coverage a", "coverage b", "coverage c",
            "acv", "replacement cost", "wind", "tornado", "wildfire", "flood zone",
            "coastal", "air ", "rms", "corelogic", "demand surge", "building age"
        ],
        "workers_comp": [
            "injury", "ncci", "payroll", "medical cost", "indemnity", "classification code",
            "class code", "experience mod", "body part", "nature of injury", "cause of injury",
            "temporary disability", "permanent disability", "medical only", "lost time",
            "fee schedule", "monopolistic state", "tail development", "claim duration"
        ],
        "commercial_auto": [
            "fleet", "vehicle class", "radius", "gvw", "for-hire", "driver turnover",
            "commercial vehicle", "trucking", "light truck", "medium truck", "heavy truck",
            "tractor", "trailer", "hired auto", "non-owned auto", "mcs-90",
            "social inflation", "nuclear verdict", "jurisdiction"
        ]
    }

    # Count matches for each portfolio
    match_counts = {}
    matched_keywords = {}

    for portfolio, keywords in PORTFOLIO_KEYWORDS.items():
        matches = [kw for kw in keywords if kw in source_content]
        match_counts[portfolio] = len(matches)
        matched_keywords[portfolio] = matches

    # Find best match
    best_portfolio = max(match_counts, key=match_counts.get)
    best_count = match_counts[best_portfolio]

    # Require minimum 3 matches for confidence
    if best_count < 3:
        best_portfolio = "personal_auto"  # Default
        confidence = 0.3
    else:
        # Calculate confidence based on match count
        confidence = min(1.0, best_count / 10.0)

    # Detect model type (frequency vs severity)
    FREQUENCY_KEYWORDS = ["frequency", "count", "number of claims", "claim count",
                          "poisson", "negative binomial", "occurrence", "how many"]
    SEVERITY_KEYWORDS = ["severity", "claim amount", "loss amount", "average claim",
                         "gamma", "lognormal", "cost per claim", "claim size"]

    freq_matches = sum(1 for kw in FREQUENCY_KEYWORDS if kw in source_content)
    sev_matches = sum(1 for kw in SEVERITY_KEYWORDS if kw in source_content)

    if freq_matches > sev_matches:
        model_type = "frequency"
    elif sev_matches > freq_matches:
        model_type = "severity"
    else:
        model_type = state.get("model_type", "frequency")  # Use hint or default

    logger.info(f"[Node: detect_portfolio] Detected: {best_portfolio} (confidence: {confidence:.2f})")
    logger.info(f"[Node: detect_portfolio] Model type: {model_type}")
    logger.info(f"[Node: detect_portfolio] Keywords matched: {matched_keywords[best_portfolio][:5]}")

    return {
        "detected_portfolio": best_portfolio,
        "detected_model_type": model_type,
        "portfolio_confidence": confidence,
        "detection_keywords": matched_keywords[best_portfolio][:10],
        "phase": "detecting",
        "next_action": "configure"
    }


# ============================================================
# NODE: configure_for_portfolio
# ============================================================
def configure_for_portfolio(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Load and apply portfolio-specific configuration.

    Sets quality thresholds, required sections, compliance rules,
    and custom instructions based on detected portfolio.
    """
    logger.info("[Node: configure_for_portfolio] Configuring for portfolio")

    portfolio = state.get("detected_portfolio", "personal_auto")
    registry = get_registry()

    config = registry.get_config(portfolio)
    if not config:
        logger.warning(f"No config for {portfolio}, using default")
        config = registry.get_default_config()

    # Build custom instructions from config
    instructions = []
    instructions.append(f"PORTFOLIO: {config.display_name}")
    instructions.append(f"EXPOSURE BASIS: {config.exposure_basis}")
    instructions.append(f"TYPICAL DISTRIBUTION: {config.typical_distribution}")
    instructions.append("")

    instructions.append("FOCUS AREAS (prioritize these topics):")
    for area in config.research_focus_areas[:5]:
        instructions.append(f"  - {area}")
    instructions.append("")

    instructions.append("COMMON PITFALLS TO AVOID:")
    for pitfall in config.common_pitfalls:
        instructions.append(f"  - {pitfall}")
    instructions.append("")

    instructions.append("COMPLIANCE CHECKPOINTS (must address):")
    for checkpoint in config.compliance_checkpoints[:5]:
        instructions.append(f"  - {checkpoint}")

    custom_instructions = "\n".join(instructions)

    # Merge required + portfolio-specific sections
    all_sections = list(config.required_sections)
    for section in config.portfolio_specific_sections:
        if section not in all_sections:
            all_sections.append(section)

    logger.info(f"[Node: configure_for_portfolio] Config: {config.display_name}")
    logger.info(f"[Node: configure_for_portfolio] Sections: {len(all_sections)}")
    logger.info(f"[Node: configure_for_portfolio] Quality threshold: {config.min_quality_score}")

    # Serialize config for state
    config_dict = {
        "portfolio_id": config.portfolio_id,
        "display_name": config.display_name,
        "exposure_basis": config.exposure_basis,
        "typical_distribution": config.typical_distribution,
        "anchor_document": config.anchor_document,
        "regulation_document": config.regulation_document,
        "audit_findings_document": config.audit_findings_document,
        "model_doc_patterns": config.model_doc_patterns
    }

    return {
        "portfolio_config": config_dict,
        "required_sections": all_sections,
        "quality_threshold": config.min_quality_score,
        "max_iterations": config.max_iterations,
        "compliance_strictness": config.compliance_strictness,
        "custom_instructions": custom_instructions,
        "phase": "configuring",
        "next_action": "research"
    }


# ============================================================
# NODE: research_phase
# ============================================================
def research_phase(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Research relevant information for each required section.

    Uses RAG to find relevant context from the corpus.
    """
    logger.info("[Node: research_phase] Starting research")

    sections = state.get("required_sections", [])
    model_type = state.get("detected_model_type", "frequency")

    from agents.research_agent import ResearchAgent
    retriever = get_retriever()
    research_agent = ResearchAgent(retriever=retriever)

    research_results = {}
    research_contexts = {}
    research_queries = {}

    for section in sections:
        logger.info(f"[Node: research_phase] Researching: {section}")

        query = f"{section} {model_type} model documentation"

        try:
            findings = research_agent.research_topic(
                topic=query,
                n_results=5
            )

            # Serialize findings
            research_results[section] = {
                "query": findings.query,
                "context": findings.context,
                "sources": findings.sources,
                "finding_count": len(findings.findings)
            }
            research_contexts[section] = findings.context
            research_queries[section] = query

            logger.info(f"[Node: research_phase] Found {len(findings.findings)} sources for {section}")

        except Exception as e:
            logger.warning(f"[Node: research_phase] Research failed for {section}: {e}")
            research_results[section] = {"query": query, "context": "", "sources": [], "finding_count": 0}
            research_contexts[section] = ""
            research_queries[section] = query

    logger.info(f"[Node: research_phase] Research complete for {len(sections)} sections")

    return {
        "research_results": research_results,
        "research_contexts": research_contexts,
        "research_queries": research_queries,
        "phase": "researching",
        "next_action": "write"
    }


# ============================================================
# NODE: writing_phase
# ============================================================
def writing_phase(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate documentation sections using the Writer Agent.
    """
    logger.info("[Node: writing_phase] Starting writing")

    sections = state.get("required_sections", [])
    research_contexts = state.get("research_contexts", {})
    source_content = state.get("source_content", "")
    custom_instructions = state.get("custom_instructions", "")
    document_title = state.get("document_title", "Model Documentation")

    from agents.writer_agent import WriterAgent
    writer_agent = WriterAgent()

    sections_written = []
    sections_content = {}

    for section_name in sections:
        logger.info(f"[Node: writing_phase] Writing: {section_name}")

        context = research_contexts.get(section_name, "")

        try:
            section = writer_agent.write_section(
                section_title=section_name,
                context=context,
                source_content=source_content,
                template=None,
                length_target="medium",
                custom_instructions=custom_instructions
            )

            sections_written.append({
                "title": section.title,
                "content": section.content,
                "word_count": section.word_count,
                "metadata": section.metadata
            })
            sections_content[section_name] = section.content

            logger.info(f"[Node: writing_phase] Wrote {section.word_count} words for {section_name}")

        except Exception as e:
            logger.error(f"[Node: writing_phase] Failed to write {section_name}: {e}")
            sections_written.append({
                "title": section_name,
                "content": f"[Error generating {section_name}]",
                "word_count": 0,
                "metadata": {"error": str(e)}
            })
            sections_content[section_name] = ""

    # Combine into document
    document_parts = [f"# {document_title}\n"]
    for section in sections_written:
        document_parts.append(f"\n## {section['title']}\n\n{section['content']}")

    current_document = "\n".join(document_parts)

    logger.info(f"[Node: writing_phase] Writing complete. Document: {len(current_document)} chars")

    return {
        "sections_written": sections_written,
        "sections_content": sections_content,
        "current_document": current_document,
        "current_iteration": state.get("current_iteration", 0) + 1,
        "phase": "writing",
        "next_action": "compliance"
    }


# ============================================================
# NODE: compliance_phase
# ============================================================
def compliance_phase(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check document for regulatory compliance.
    """
    logger.info("[Node: compliance_phase] Checking compliance")

    document = state.get("current_document", "")
    document_title = state.get("document_title", "")
    document_type = state.get("document_type", "model_doc")

    from agents.compliance_agent import ComplianceAgent, ComplianceSeverity
    retriever = get_retriever()
    compliance_agent = ComplianceAgent(retriever=retriever)

    try:
        report = compliance_agent.check_compliance(
            document_content=document,
            document_title=document_title,
            document_type=document_type
        )

        # Count issues by severity
        critical_count = len(report.get_findings_by_severity(ComplianceSeverity.CRITICAL))
        high_count = len(report.get_findings_by_severity(ComplianceSeverity.HIGH))

        # Serialize findings
        compliance_issues = []
        for finding in report.findings:
            compliance_issues.append({
                "description": finding.description if hasattr(finding, 'description') else str(finding),
                "severity": finding.severity.value if hasattr(finding, 'severity') else "MEDIUM",
                "section": finding.section if hasattr(finding, 'section') else "Document",
                "recommendation": finding.recommendation if hasattr(finding, 'recommendation') else ""
            })

        # Determine if passed
        compliance_passed = (critical_count == 0 and high_count <= 2)

        logger.info(f"[Node: compliance_phase] Status: {report.overall_status}")
        logger.info(f"[Node: compliance_phase] Critical: {critical_count}, High: {high_count}")
        logger.info(f"[Node: compliance_phase] Passed: {compliance_passed}")

        return {
            "compliance_report": {"status": report.overall_status, "finding_count": len(report.findings)},
            "compliance_passed": compliance_passed,
            "compliance_issues": compliance_issues,
            "critical_compliance_count": critical_count,
            "high_compliance_count": high_count,
            "phase": "compliance",
            "next_action": "editorial" if compliance_passed else "check_iteration"
        }

    except Exception as e:
        logger.error(f"[Node: compliance_phase] Error: {e}")
        return {
            "compliance_report": {"status": "ERROR", "error": str(e)},
            "compliance_passed": False,
            "compliance_issues": [{"description": str(e), "severity": "CRITICAL"}],
            "critical_compliance_count": 1,
            "high_compliance_count": 0,
            "phase": "compliance",
            "next_action": "check_iteration",
            "errors": state.get("errors", []) + [f"Compliance error: {e}"]
        }


# ============================================================
# NODE: editorial_phase
# ============================================================
def editorial_phase(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform editorial review with LLM-as-judge quality scoring.
    """
    logger.info("[Node: editorial_phase] Starting editorial review")

    document = state.get("current_document", "")
    document_title = state.get("document_title", "")
    document_type = state.get("document_type", "model_doc")
    source_content = state.get("source_content", "")
    quality_threshold = state.get("quality_threshold", 7.0)

    from agents.editor_agent import EditorAgent
    retriever = get_retriever()
    editor_agent = EditorAgent(retriever=retriever, enable_llm_judge=True)

    try:
        review = editor_agent.review_document(
            document_content=document,
            document_title=document_title,
            document_type=document_type,
            source_content=source_content,
            use_llm_judge=True
        )

        # Extract quality score
        quality_score = 0.0
        source_fidelity = 0.0

        if review.quality_report:
            quality_score = review.quality_report.overall_score
            if 'source_fidelity' in review.quality_report.dimension_scores:
                source_fidelity = review.quality_report.dimension_scores['source_fidelity']

        # Serialize issues
        editorial_issues = []
        for finding in review.findings:
            editorial_issues.append({
                "description": str(finding),
                "priority": finding.priority.value if hasattr(finding, 'priority') else "MEDIUM"
            })

        # Determine if passed
        editorial_passed = quality_score >= quality_threshold

        logger.info(f"[Node: editorial_phase] Quality Score: {quality_score:.1f}/{quality_threshold}")
        logger.info(f"[Node: editorial_phase] Source Fidelity: {source_fidelity:.1f}")
        logger.info(f"[Node: editorial_phase] Passed: {editorial_passed}")

        # Determine next action
        if editorial_passed:
            next_action = "complete"
        else:
            next_action = "check_iteration"

        return {
            "editorial_review": {
                "quality": review.overall_quality,
                "readability": review.readability_score,
                "finding_count": len(review.findings)
            },
            "quality_score": quality_score,
            "editorial_passed": editorial_passed,
            "editorial_issues": editorial_issues,
            "source_fidelity_score": source_fidelity,
            "phase": "editorial",
            "next_action": next_action
        }

    except Exception as e:
        logger.error(f"[Node: editorial_phase] Error: {e}")
        return {
            "editorial_review": {"error": str(e)},
            "quality_score": 0.0,
            "editorial_passed": False,
            "editorial_issues": [{"description": str(e), "priority": "CRITICAL"}],
            "source_fidelity_score": 0.0,
            "phase": "editorial",
            "next_action": "check_iteration",
            "errors": state.get("errors", []) + [f"Editorial error: {e}"]
        }


# ============================================================
# NODE: revision_phase
# ============================================================
def revision_phase(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Revise sections based on compliance and editorial feedback.
    """
    logger.info("[Node: revision_phase] Starting revision")

    sections_written = state.get("sections_written", [])
    compliance_issues = state.get("compliance_issues", [])
    editorial_issues = state.get("editorial_issues", [])
    source_content = state.get("source_content", "")
    research_contexts = state.get("research_contexts", {})
    document_title = state.get("document_title", "Model Documentation")

    from agents.writer_agent import WriterAgent, SectionContent
    writer_agent = WriterAgent()

    # Build revision instructions from issues
    revision_instructions = []

    for issue in compliance_issues[:5]:
        if issue.get("severity") in ["CRITICAL", "HIGH"]:
            revision_instructions.append(f"COMPLIANCE: {issue.get('description', '')}")

    for issue in editorial_issues[:5]:
        if issue.get("priority") in ["CRITICAL", "HIGH"]:
            revision_instructions.append(f"EDITORIAL: {issue.get('description', '')}")

    combined_instructions = "\n".join(revision_instructions)

    logger.info(f"[Node: revision_phase] Addressing {len(revision_instructions)} issues")

    # Revise each section
    revised_sections = []
    sections_content = {}

    for section in sections_written[:6]:  # Limit to 6 sections
        section_name = section.get("title", "")
        original_content = section.get("content", "")

        if revision_instructions:
            try:
                # Create SectionContent-like object for revision
                original = SectionContent(
                    title=section_name,
                    content=original_content,
                    word_count=section.get("word_count", 0),
                    metadata=section.get("metadata", {})
                )

                context = research_contexts.get(section_name, "")

                revised = writer_agent.revise_section(
                    original_content=original,
                    revision_instructions=combined_instructions,
                    additional_context=context,
                    source_content=source_content
                )

                revised_sections.append({
                    "title": revised.title,
                    "content": revised.content,
                    "word_count": revised.word_count,
                    "metadata": {**revised.metadata, "revised": True}
                })
                sections_content[section_name] = revised.content

                logger.info(f"[Node: revision_phase] Revised: {section_name}")

            except Exception as e:
                logger.warning(f"[Node: revision_phase] Failed to revise {section_name}: {e}")
                revised_sections.append(section)
                sections_content[section_name] = original_content
        else:
            revised_sections.append(section)
            sections_content[section_name] = original_content

    # Add any remaining sections unchanged
    for section in sections_written[6:]:
        revised_sections.append(section)
        sections_content[section.get("title", "")] = section.get("content", "")

    # Rebuild document
    document_parts = [f"# {document_title}\n"]
    for section in revised_sections:
        document_parts.append(f"\n## {section['title']}\n\n{section['content']}")

    current_document = "\n".join(document_parts)

    # Record revision
    revision_entry = {
        "iteration": state.get("current_iteration", 0),
        "issues_addressed": len(revision_instructions),
        "sections_revised": len([s for s in revised_sections if s.get("metadata", {}).get("revised")])
    }

    logger.info(f"[Node: revision_phase] Revision complete. Revised {revision_entry['sections_revised']} sections")

    return {
        "sections_written": revised_sections,
        "sections_content": sections_content,
        "current_document": current_document,
        "current_iteration": state.get("current_iteration", 0) + 1,  # Increment to prevent infinite loop
        "revision_history": state.get("revision_history", []) + [revision_entry],
        "issues_addressed": [i.get("description", "") for i in compliance_issues[:3]],
        "phase": "revision",
        "next_action": "compliance"  # Loop back to check again
    }


# ============================================================
# NODE: complete_workflow
# ============================================================
def complete_workflow(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Finalize the workflow and prepare output.
    """
    logger.info("[Node: complete_workflow] Completing workflow")

    from datetime import datetime

    return {
        "final_document": state.get("current_document", ""),
        "generation_successful": True,
        "phase": "completed",
        "should_continue": False,
        "end_time": datetime.now().isoformat()
    }


# ============================================================
# NODE: handle_failure
# ============================================================
def handle_failure(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle workflow failure gracefully.
    """
    logger.error("[Node: handle_failure] Workflow failed")

    from datetime import datetime

    return {
        "final_document": state.get("current_document", ""),  # Return partial if available
        "generation_successful": False,
        "phase": "failed",
        "should_continue": False,
        "end_time": datetime.now().isoformat()
    }


# ============================================================
# ROUTER FUNCTIONS (for conditional edges)
# ============================================================

def route_after_compliance(state: Dict[str, Any]) -> str:
    """
    Decide next step after compliance check.

    Returns:
        "editorial" if compliance passed
        "revision" if failed but iterations remain
        "complete" if max iterations exceeded
    """
    compliance_passed = state.get("compliance_passed", False)
    current_iteration = state.get("current_iteration", 0)
    max_iterations = state.get("max_iterations", 3)

    if compliance_passed:
        return "editorial"
    elif current_iteration < max_iterations:
        return "revision"
    else:
        logger.warning(f"Max iterations ({max_iterations}) reached at compliance")
        return "complete"  # Accept what we have


def route_after_editorial(state: Dict[str, Any]) -> str:
    """
    Decide next step after editorial review.

    Returns:
        "complete" if quality passed
        "revision" if failed but iterations remain
        "complete" if max iterations exceeded (accept anyway)
    """
    editorial_passed = state.get("editorial_passed", False)
    current_iteration = state.get("current_iteration", 0)
    max_iterations = state.get("max_iterations", 3)

    if editorial_passed:
        return "complete"
    elif current_iteration < max_iterations:
        return "revision"
    else:
        logger.warning(f"Max iterations ({max_iterations}) reached at editorial")
        return "complete"  # Accept what we have


def route_after_revision(state: Dict[str, Any]) -> str:
    """
    After revision, always go back to compliance to re-check.
    """
    return "compliance"
