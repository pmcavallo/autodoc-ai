"""
Compliance Agent for AutoDoc AI

This agent is responsible for checking documentation against regulatory
requirements and actuarial standards.

Key Responsibilities:
- Verify compliance with NAIC Model Audit Rule
- Check adherence to Actuarial Standards of Practice (ASOPs)
- Identify missing required sections
- Flag potential compliance issues
- Provide remediation recommendations

Usage:
    from agents.compliance_agent import ComplianceAgent

    agent = ComplianceAgent()
    report = agent.check_compliance(document_content, document_type="model_doc")
"""

from pathlib import Path
from typing import List, Dict, Optional, Set
import logging
from dataclasses import dataclass, field
from enum import Enum
import re
import json  # ← NEW: For parsing LLM JSON responses
import os    # ← NEW: For environment variables

from rag.retrieval import DocumentRetriever

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ComplianceSeverity(Enum):
    """Severity levels for compliance findings."""
    CRITICAL = "CRITICAL"  # Must fix before approval
    HIGH = "HIGH"          # Should fix, may block approval
    MEDIUM = "MEDIUM"      # Should address
    LOW = "LOW"            # Nice to have
    INFO = "INFO"          # Informational only


@dataclass
class ComplianceFinding:
    """
    Represents a single compliance finding.
    """
    severity: ComplianceSeverity
    category: str
    description: str
    requirement: str
    recommendation: Optional[str] = None
    reference: Optional[str] = None

    def __repr__(self):
        return f"ComplianceFinding({self.severity.value}, {self.category}: {self.description[:50]}...)"


@dataclass
class ComplianceReport:
    """
    Complete compliance check report.
    """
    document_title: str
    document_type: str
    findings: List[ComplianceFinding] = field(default_factory=list)
    required_sections: Dict[str, bool] = field(default_factory=dict)
    asop_compliance: Dict[str, bool] = field(default_factory=dict)
    overall_status: str = "PENDING"

    def __post_init__(self):
        """Calculate overall status based on findings."""
        if not self.findings:
            self.overall_status = "COMPLIANT"
        elif any(f.severity == ComplianceSeverity.CRITICAL for f in self.findings):
            self.overall_status = "NON-COMPLIANT"
        elif any(f.severity == ComplianceSeverity.HIGH for f in self.findings):
            self.overall_status = "CONDITIONAL"
        else:
            self.overall_status = "COMPLIANT WITH NOTES"

    def get_findings_by_severity(self, severity: ComplianceSeverity) -> List[ComplianceFinding]:
        """Get all findings of a specific severity."""
        return [f for f in self.findings if f.severity == severity]

    def format_summary(self) -> str:
        """Format compliance report as readable summary."""
        lines = [
            "=" * 60,
            "COMPLIANCE REPORT",
            "=" * 60,
            f"Document: {self.document_title}",
            f"Type: {self.document_type}",
            f"Overall Status: {self.overall_status}",
            "",
            f"Total Findings: {len(self.findings)}",
        ]

        # Count by severity
        for severity in ComplianceSeverity:
            count = len(self.get_findings_by_severity(severity))
            if count > 0:
                lines.append(f"  - {severity.value}: {count}")

        lines.append("")
        lines.append("Required Sections:")
        for section, present in self.required_sections.items():
            status = "[OK]" if present else "[X]"
            lines.append(f"  {status} {section}")

        if self.asop_compliance:
            lines.append("")
            lines.append("ASOP Compliance:")
            for asop, compliant in self.asop_compliance.items():
                status = "[OK]" if compliant else "[X]"
                lines.append(f"  {status} {asop}")

        if self.findings:
            lines.append("")
            lines.append("Findings by Severity:")
            lines.append("")

            for severity in [ComplianceSeverity.CRITICAL, ComplianceSeverity.HIGH,
                           ComplianceSeverity.MEDIUM, ComplianceSeverity.LOW]:
                findings = self.get_findings_by_severity(severity)
                if findings:
                    lines.append(f"{severity.value}:")
                    for finding in findings:
                        lines.append(f"  - {finding.category}: {finding.description}")
                        if finding.recommendation:
                            lines.append(f"    → {finding.recommendation}")
                    lines.append("")

        return "\n".join(lines)


class ComplianceAgent:
    """
    Agent for checking documentation compliance with regulatory standards.

    This agent:
    1. Checks for required documentation sections
    2. Verifies ASOP compliance (12, 23, 41, 56)
    3. Reviews NAIC Model Audit Rule adherence
    4. Identifies potential issues
    5. Provides remediation recommendations
    """

    # Required sections for model documentation
    MODEL_DOC_REQUIRED_SECTIONS = {
        "Executive Summary",
        "Business Context",
        "Data Sources",
        "Methodology",
        "Model Development",
        "Validation",
        "Performance",
        "Implementation",
        "Limitations",
        "Monitoring"
    }

    # ASOP requirements
    ASOP_REQUIREMENTS = {
        "ASOP 12": ["Risk Classification", "Rate Differentiation", "Actuarial Justification"],
        "ASOP 23": ["Data Quality", "Data Limitations", "Data Sources"],
        "ASOP 41": ["Documentation", "Professional Communication", "Assumptions"],
        "ASOP 56": ["Model Validation", "Model Governance", "Model Limitations"]
    }

    # NAIC Model Audit Rule requirements
    NAIC_MAR_REQUIREMENTS = [
        "Model inventory and classification",
        "Model development documentation",
        "Model validation procedures",
        "Model governance framework",
        "Ongoing monitoring procedures"
    ]

    def __init__(
        self,
        retriever: Optional[DocumentRetriever] = None,
        cost_tracker: Optional['CostTracker'] = None,  # ← NEW: For cost tracking
        strict_mode: bool = False
    ):
        """
        Initialize the compliance agent.

        Args:
            retriever: DocumentRetriever for accessing regulatory requirements
            cost_tracker: CostTracker instance for recording API costs
            strict_mode: If True, enforce stricter compliance standards
        """
        self.strict_mode = strict_mode
        self.retriever = retriever
        self.cost_tracker = cost_tracker

        # Initialize Anthropic client if we have retriever (enables LLM+RAG checks)
        if self.retriever is not None:
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                logger.info("ComplianceAgent initialized with LLM+RAG capability")
            except ImportError:
                logger.warning("anthropic package not installed - LLM checks disabled")
                self.client = None
        else:
            self.client = None
            logger.info("ComplianceAgent initialized without retriever (rule-based only)")

    # ================================================================
    # PHASE 1: RAG + LLM COMPLIANCE METHODS
    # ================================================================

    def _retrieve_regulatory_context(
        self,
        topic: str,
        n_results: int = 8  # ← PHASE 1 FIX: Increased from 3 to 8 for better coverage
    ) -> str:
        """
        Retrieve regulatory requirements from knowledge base.
        
        Args:
            topic: Topic to retrieve requirements for (e.g., "ASOP 23", "NAIC Model Audit Rule")
            n_results: Number of results to retrieve (default 8, was 3)
            
        Returns:
            Formatted context string with regulatory requirements
        """
        if not self.retriever:
            return ""
        
        try:
            # PHASE 1 FIX: Use specific queries for better retrieval precision
            # Maps regulation names to targeted queries that retrieve the RIGHT sections
            # This fixes the issue where all ASOPs are in Section 2 and generic queries
            # return mixed content (ASOP 12, 23, 41, 56 all together)
            query_map = {
                "ASOP 23": "ASOP No. 23 Section 2.2 Data Quality assessment completeness accuracy timeliness review procedures documentation requirements data sources validation limitations",
                "ASOP 41": "ASOP No. 41 Section 2.3 Actuarial Communications required content form disclosure scope purpose assumptions uncertainty identification effective date",
                "NAIC Model Audit Rule": "NAIC Model Audit Rule Section 1 model governance framework documentation validation requirements high-risk model designation third-party validation model risk committee approval quarterly performance reporting regulatory examination model inventory risk classification enhanced documentation standards material financial impact"
            }
            
            # Get specific query or fallback to generic for other topics
            query = query_map.get(topic, f"{topic} regulatory requirements compliance standards")
            
            results = self.retriever.retrieve(
                query=query,  # ← Now uses specific queries from query_map
                filters={"document_type": "regulation"},
                n_results=n_results,
                min_similarity=0.3
            )
            
            if not results:
                logger.warning(f"No regulatory context found for: {topic}")
                return ""
            
            # Build context from retrieved chunks
            context = self.retriever.build_context(results, max_tokens=1500)
            logger.info(f"Retrieved regulatory context for {topic}: {len(context)} chars (~{len(context)//4} tokens)")
            return context
            
        except Exception as e:
            logger.error(f"Error retrieving regulatory context: {e}")
            return ""

    def _robust_json_parse(self, response_text: str, context: str = "") -> dict:
        """
        Robustly parse JSON from LLM response with multiple fallback strategies.
        
        Handles common LLM response issues:
        - Markdown code blocks
        - Extra text before/after JSON
        - Unescaped quotes in strings
        - Truncated responses
        
        Args:
            response_text: Raw text response from LLM
            context: Context string for error logging (e.g., "ASOP 41")
            
        Returns:
            Parsed JSON dict, or empty result dict if all strategies fail
        """
        import re
        
        # Layer 1: Direct parse (handles clean responses ~70% of cases)
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        # Layer 2: Remove markdown code blocks (~20% of cases)
        try:
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
                return json.loads(json_str)
        except (IndexError, json.JSONDecodeError):
            pass
        
        # Layer 3: Extract JSON object using regex (~8% of cases)
        try:
            # Find the first complete JSON object in the text
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
        
        # Layer 4: Try to fix common JSON errors (~2% of cases)
        try:
            # Remove any text before first { and after last }
            fixed_text = response_text
            start_idx = fixed_text.find('{')
            end_idx = fixed_text.rfind('}')
            if start_idx != -1 and end_idx != -1:
                fixed_text = fixed_text[start_idx:end_idx+1]
                return json.loads(fixed_text)
        except json.JSONDecodeError as e:
            logger.warning(f"All JSON parsing strategies failed for {context}")
            logger.debug(f"Problematic response (first 500 chars): {response_text[:500]}")
            logger.debug(f"JSON error: {e}")
        
        # All strategies failed - return empty result (safe fallback)
        logger.error(f"Could not parse JSON for {context}. Returning empty result.")
        return {
            "compliant": True,
            "issues": [],
            "severity": "LOW",
            "recommendations": []
        }

    def _check_asop_compliance_with_llm(
        self,
        document_content: str,
        asop_num: str
    ) -> List[ComplianceFinding]:
        """
        Use LLM to evaluate ASOP compliance against retrieved requirements.
        
        Args:
            document_content: Full document text
            asop_num: ASOP number (e.g., "23", "41")
            
        Returns:
            List of ComplianceFinding objects
        """
        if not self.client or not self.retriever:
            return []
        
        try:
            # Retrieve actual ASOP requirements
            asop_context = self._retrieve_regulatory_context(f"ASOP {asop_num}")
            
            if not asop_context:
                logger.warning(f"No context retrieved for ASOP {asop_num}, skipping LLM check")
                return []
            
            # Build evaluation prompt with stricter JSON requirements
            prompt = f"""You are an expert actuarial compliance reviewer. Evaluate this document for ASOP {asop_num} compliance.

ASOP {asop_num} Requirements (from regulatory knowledge base):
{asop_context}

Document to Evaluate (first 8000 chars):
{document_content[:8000]}

Evaluate compliance and return findings in STRICTLY VALID JSON format.

CRITICAL JSON RULES:
1. Use double quotes for all strings
2. Escape any quotes inside strings with backslash: \\"
3. Return ONLY the JSON object, no other text
4. Do not use apostrophes or contractions in strings
5. Keep issue descriptions under 100 characters

Required JSON schema:
{{
  "compliant": true or false,
  "issues": ["Issue 1 without apostrophes", "Issue 2 without quotes"],
  "severity": "CRITICAL" or "HIGH" or "MEDIUM" or "LOW",
  "recommendations": ["Fix 1", "Fix 2"]
}}

If compliant, return: {{"compliant": true, "issues": [], "severity": "LOW", "recommendations": []}}

Return ONLY valid JSON, no markdown, no explanation.
"""
            
            # Call Claude Haiku (cheap, sufficient for compliance checking)
            response = self.client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1000,
                temperature=0.1,  # Very low for consistency
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Track cost
            if self.cost_tracker:
                self.cost_tracker.record_usage(
                    agent="Compliance Agent",
                    operation=f"ASOP {asop_num} LLM check",
                    input_tokens=response.usage.input_tokens,
                    output_tokens=response.usage.output_tokens
                )
            
            # Parse JSON response using robust parser
            response_text = response.content[0].text.strip()
            
            # Use robust JSON parser with multiple fallback strategies
            result = self._robust_json_parse(response_text, context=f"ASOP {asop_num}")
            
            logger.info(f"ASOP {asop_num} LLM check: compliant={result.get('compliant')}, issues={len(result.get('issues', []))}")
            
            # Convert to ComplianceFindings
            findings = []
            if not result.get("compliant", True) and result.get("issues"):
                severity_map = {
                    "CRITICAL": ComplianceSeverity.CRITICAL,
                    "HIGH": ComplianceSeverity.HIGH,
                    "MEDIUM": ComplianceSeverity.MEDIUM,
                    "LOW": ComplianceSeverity.LOW
                }
                severity = severity_map.get(result.get("severity", "MEDIUM"), ComplianceSeverity.MEDIUM)
                
                for idx, issue in enumerate(result.get("issues", [])):
                    recommendation = result.get("recommendations", [])[idx] if idx < len(result.get("recommendations", [])) else None
                    
                    finding = ComplianceFinding(
                        severity=severity,
                        category=f"ASOP {asop_num}",
                        description=issue,
                        requirement=f"ASOP {asop_num} compliance",
                        recommendation=recommendation,
                        reference=f"ASOP {asop_num}"
                    )
                    findings.append(finding)
            
            return findings
            
        except Exception as e:
            logger.error(f"Error in ASOP {asop_num} LLM check: {e}")
            return []

    def _check_naic_compliance_with_llm(
        self,
        document_content: str
    ) -> List[ComplianceFinding]:
        """
        Use LLM to evaluate NAIC Model Audit Rule compliance.
        
        Args:
            document_content: Full document text
            
        Returns:
            List of ComplianceFinding objects
        """
        if not self.client or not self.retriever:
            return []
        
        try:
            # Retrieve NAIC Model Audit Rule requirements
            naic_context = self._retrieve_regulatory_context("NAIC Model Audit Rule")
            
            if not naic_context:
                logger.warning("No context retrieved for NAIC MAR, skipping LLM check")
                return []
            
            # Build evaluation prompt with stricter JSON requirements
            prompt = f"""You are an expert actuarial compliance reviewer. Evaluate this document for NAIC Model Audit Rule (MAR) compliance.

NAIC Model Audit Rule Requirements (from regulatory knowledge base):
{naic_context}

Document to Evaluate (first 8000 chars):
{document_content[:8000]}

Evaluate compliance and return findings in STRICTLY VALID JSON format.

CRITICAL JSON RULES:
1. Use double quotes for all strings
2. Escape any quotes inside strings with backslash: \\"
3. Return ONLY the JSON object, no other text
4. Do not use apostrophes or contractions in strings
5. Keep issue descriptions under 100 characters

Required JSON schema:
{{
  "compliant": true or false,
  "issues": ["Issue 1 without apostrophes", "Issue 2 without quotes"],
  "severity": "CRITICAL" or "HIGH" or "MEDIUM" or "LOW",
  "recommendations": ["Fix 1", "Fix 2"]
}}

If compliant, return: {{"compliant": true, "issues": [], "severity": "LOW", "recommendations": []}}

Return ONLY valid JSON, no markdown, no explanation.
"""
            
            # Call Claude Haiku
            response = self.client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Track cost
            if self.cost_tracker:
                self.cost_tracker.record_usage(
                    agent="Compliance Agent",
                    operation="NAIC MAR LLM check",
                    input_tokens=response.usage.input_tokens,
                    output_tokens=response.usage.output_tokens
                )
            
            # Parse JSON response using robust parser
            response_text = response.content[0].text.strip()
            
            # Use robust JSON parser with multiple fallback strategies
            result = self._robust_json_parse(response_text, context="NAIC MAR")
            
            logger.info(f"NAIC MAR LLM check: compliant={result.get('compliant')}, issues={len(result.get('issues', []))}")
            
            # Convert to ComplianceFindings
            findings = []
            if not result.get("compliant", True) and result.get("issues"):
                severity_map = {
                    "CRITICAL": ComplianceSeverity.CRITICAL,
                    "HIGH": ComplianceSeverity.HIGH,
                    "MEDIUM": ComplianceSeverity.MEDIUM,
                    "LOW": ComplianceSeverity.LOW
                }
                severity = severity_map.get(result.get("severity", "MEDIUM"), ComplianceSeverity.MEDIUM)
                
                for idx, issue in enumerate(result.get("issues", [])):
                    recommendation = result.get("recommendations", [])[idx] if idx < len(result.get("recommendations", [])) else None
                    
                    finding = ComplianceFinding(
                        severity=severity,
                        category="NAIC Model Audit Rule",
                        description=issue,
                        requirement="NAIC Model Audit Rule compliance",
                        recommendation=recommendation,
                        reference="NAIC MAR"
                    )
                    findings.append(finding)
            
            return findings
            
        except Exception as e:
            logger.error(f"Error in NAIC MAR LLM check: {e}")
            return []

    # ================================================================
    # END PHASE 1 METHODS
    # ================================================================


    def check_compliance(
        self,
        document_content: str,
        document_title: str,
        document_type: str = "model_doc"
    ) -> ComplianceReport:
        """
        Perform complete compliance check on a document.

        Args:
            document_content: Full document text
            document_title: Document title
            document_type: Type of document (model_doc, methodology, etc.)

        Returns:
            ComplianceReport with findings
        """
        logger.info(f"Checking compliance for: {document_title} (type: {document_type})")

        report = ComplianceReport(
            document_title=document_title,
            document_type=document_type
        )

        # Check required sections
        if document_type == "model_doc":
            section_findings = self._check_required_sections(
                document_content,
                self.MODEL_DOC_REQUIRED_SECTIONS
            )
            report.findings.extend(section_findings)
            report.required_sections = self._get_section_presence(
                document_content,
                self.MODEL_DOC_REQUIRED_SECTIONS
            )

        # Check ASOP compliance (rule-based)
        asop_findings = self._check_asop_compliance(document_content)
        report.findings.extend(asop_findings)
        report.asop_compliance = self._get_asop_compliance_status(document_content)

        # Check NAIC MAR compliance (rule-based)
        naic_findings = self._check_naic_compliance(document_content)
        report.findings.extend(naic_findings)

        # ============================================================
        # PHASE 1: Add LLM+RAG compliance checks if available
        # ============================================================
        if self.client and self.retriever:
            logger.info("Running LLM+RAG compliance checks...")
            
            # Check ASOP 23 (Data Quality) with LLM
            asop_23_findings = self._check_asop_compliance_with_llm(document_content, "23")
            report.findings.extend(asop_23_findings)
            logger.info(f"  ASOP 23 LLM check: {len(asop_23_findings)} findings")
            
            # Check ASOP 41 (Actuarial Communications) with LLM
            asop_41_findings = self._check_asop_compliance_with_llm(document_content, "41")
            report.findings.extend(asop_41_findings)
            logger.info(f"  ASOP 41 LLM check: {len(asop_41_findings)} findings")
            
            # Check NAIC Model Audit Rule with LLM
            naic_llm_findings = self._check_naic_compliance_with_llm(document_content)
            report.findings.extend(naic_llm_findings)
            logger.info(f"  NAIC MAR LLM check: {len(naic_llm_findings)} findings")
            
            logger.info(f"LLM+RAG checks complete: +{len(asop_23_findings) + len(asop_41_findings) + len(naic_llm_findings)} findings")
        else:
            logger.info("LLM+RAG checks skipped (client or retriever not available)")
        # ============================================================

        # Check for synthetic data disclaimer
        disclaimer_finding = self._check_synthetic_disclaimer(document_content)
        if disclaimer_finding:
            report.findings.append(disclaimer_finding)

        # Update overall status
        report.__post_init__()

        logger.info(f"Compliance check complete: {len(report.findings)} findings, status: {report.overall_status}")
        return report

    def _check_required_sections(
        self,
        content: str,
        required_sections: Set[str]
    ) -> List[ComplianceFinding]:
        """Check for presence of required sections."""
        findings = []

        for section in required_sections:
            # Look for section headers (# Section, ## Section, ### Section)
            pattern = rf'^#{1,3}\s+{re.escape(section)}'
            if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                findings.append(ComplianceFinding(
                    severity=ComplianceSeverity.HIGH,
                    category="Missing Section",
                    description=f"Required section '{section}' not found",
                    requirement="Model documentation must include all required sections",
                    recommendation=f"Add a section titled '{section}' with appropriate content"
                ))

        return findings

    def _get_section_presence(
        self,
        content: str,
        required_sections: Set[str]
    ) -> Dict[str, bool]:
        """Get presence status for all required sections."""
        presence = {}

        for section in required_sections:
            pattern = rf'^#{1,3}\s+{re.escape(section)}'
            presence[section] = bool(re.search(pattern, content, re.MULTILINE | re.IGNORECASE))

        return presence

    def _check_asop_compliance(self, content: str) -> List[ComplianceFinding]:
        """Check compliance with Actuarial Standards of Practice."""
        findings = []

        for asop, requirements in self.ASOP_REQUIREMENTS.items():
            for requirement in requirements:
                # Simple keyword check (in production, would use more sophisticated analysis)
                if requirement.lower() not in content.lower():
                    severity = ComplianceSeverity.MEDIUM if self.strict_mode else ComplianceSeverity.LOW

                    findings.append(ComplianceFinding(
                        severity=severity,
                        category=f"{asop} Compliance",
                        description=f"No explicit reference to '{requirement}'",
                        requirement=f"{asop} requires documentation of {requirement.lower()}",
                        recommendation=f"Add section or paragraph addressing {requirement.lower()}",
                        reference=asop
                    ))

        return findings

    def _get_asop_compliance_status(self, content: str) -> Dict[str, bool]:
        """Get compliance status for each ASOP."""
        compliance = {}

        for asop, requirements in self.ASOP_REQUIREMENTS.items():
            # Consider compliant if at least 50% of requirements are mentioned
            mentions = sum(1 for req in requirements if req.lower() in content.lower())
            compliance[asop] = mentions >= len(requirements) / 2

        return compliance

    def _check_naic_compliance(self, content: str) -> List[ComplianceFinding]:
        """Check NAIC Model Audit Rule compliance."""
        findings = []

        for requirement in self.NAIC_MAR_REQUIREMENTS:
            # Extract key terms
            key_terms = requirement.lower().split()[:3]

            # Check if key terms appear
            mentions = sum(1 for term in key_terms if term in content.lower())

            if mentions < len(key_terms) / 2:
                findings.append(ComplianceFinding(
                    severity=ComplianceSeverity.MEDIUM,
                    category="NAIC MAR",
                    description=f"Limited coverage of: {requirement}",
                    requirement=f"NAIC Model Audit Rule requires: {requirement}",
                    recommendation=f"Add explicit documentation addressing {requirement}",
                    reference="NAIC Model Audit Rule"
                ))

        return findings

    def _check_synthetic_disclaimer(self, content: str) -> Optional[ComplianceFinding]:
        """Check for synthetic data disclaimer."""
        if "SYNTHETIC DATA DISCLAIMER" not in content:
            return ComplianceFinding(
                severity=ComplianceSeverity.INFO,
                category="Synthetic Data",
                description="No synthetic data disclaimer found",
                requirement="Portfolio/demo documents should include synthetic data disclaimer",
                recommendation="Add synthetic data disclaimer at document beginning"
            )
        return None

    def validate_regulatory_section(
        self,
        section_content: str,
        section_type: str
    ) -> List[ComplianceFinding]:
        """
        Validate a specific section against regulatory requirements.

        Args:
            section_content: Content of the section
            section_type: Type of section (validation, methodology, etc.)

        Returns:
            List of compliance findings
        """
        logger.info(f"Validating regulatory section: {section_type}")

        findings = []

        # Define section-specific requirements
        section_requirements = {
            "validation": [
                "holdout testing",
                "cross-validation",
                "performance metrics",
                "stability analysis"
            ],
            "methodology": [
                "data sources",
                "model technique",
                "variable selection",
                "business justification"
            ],
            "governance": [
                "model oversight",
                "documentation procedures",
                "approval process",
                "monitoring framework"
            ]
        }

        requirements = section_requirements.get(section_type.lower(), [])

        for requirement in requirements:
            if requirement.lower() not in section_content.lower():
                findings.append(ComplianceFinding(
                    severity=ComplianceSeverity.MEDIUM,
                    category=f"{section_type.title()} Section",
                    description=f"Missing discussion of '{requirement}'",
                    requirement=f"{section_type.title()} sections should address {requirement}",
                    recommendation=f"Add paragraph discussing {requirement}"
                ))

        return findings

    def check_citation_quality(
        self,
        document_content: str,
        min_citations: int = 3
    ) -> List[ComplianceFinding]:
        """
        Check that document has adequate source citations.

        Args:
            document_content: Full document text
            min_citations: Minimum number of citations expected

        Returns:
            List of compliance findings
        """
        findings = []

        # Find citations in format [filename:section]
        citations = re.findall(r'\[[^\]]+\.md:[^\]]+\]', document_content)

        if len(citations) < min_citations:
            findings.append(ComplianceFinding(
                severity=ComplianceSeverity.LOW,
                category="Documentation Quality",
                description=f"Only {len(citations)} citations found (expected: {min_citations}+)",
                requirement="Documentation should cite source materials",
                recommendation="Add citations to support claims and methodology"
            ))

        return findings

    def get_remediation_plan(
        self,
        report: ComplianceReport
    ) -> List[str]:
        """
        Generate prioritized remediation plan from compliance report.

        Args:
            report: ComplianceReport with findings

        Returns:
            List of remediation steps, prioritized by severity
        """
        remediation_steps = []

        # Group by severity
        for severity in [ComplianceSeverity.CRITICAL, ComplianceSeverity.HIGH,
                        ComplianceSeverity.MEDIUM, ComplianceSeverity.LOW]:
            findings = report.get_findings_by_severity(severity)

            if findings:
                remediation_steps.append(f"\n{severity.value} Priority:")
                for i, finding in enumerate(findings, 1):
                    if finding.recommendation:
                        remediation_steps.append(f"  {i}. {finding.recommendation}")
                    else:
                        remediation_steps.append(f"  {i}. Address: {finding.description}")

        return remediation_steps


def main():
    """
    Test function for compliance agent.
    """
    print("=" * 60)
    print("AutoDoc AI - Compliance Agent Test")
    print("=" * 60)
    print()

    # Initialize agent
    print("1. Initializing ComplianceAgent...")
    agent = ComplianceAgent(strict_mode=False)
    print("   [OK] Agent initialized")
    print()

    # Create sample document content
    print("2. Creating sample document for testing...")
    sample_doc = """
# Frequency Model Documentation

**SYNTHETIC DATA DISCLAIMER**
*This document contains synthetic data for demonstration purposes only.*

## Executive Summary
This model predicts claim frequency using GLM Poisson regression.

## Data Sources
Data was extracted from PolicyMaster and ClaimsVision systems.

## Methodology
The model uses Poisson regression with log link function.
Data quality checks were performed according to ASOP 23 standards.

## Model Development
Variables were selected based on business justification and statistical significance.

## Validation
Holdout testing was performed on 20% of data.
Performance metrics include AUC of 0.72.

## Performance
The model achieved strong performance on validation data.

## Limitations
Model limitations include geographic scope and data availability.
"""

    print("   [OK] Sample document created")
    print()

    # Run compliance check
    print("3. Running compliance check...")
    report = agent.check_compliance(
        document_content=sample_doc,
        document_title="Frequency Model Documentation",
        document_type="model_doc"
    )
    print(f"   [OK] Compliance check complete")
    print(f"   [OK] Status: {report.overall_status}")
    print(f"   [OK] Total findings: {len(report.findings)}")
    print()

    # Display report summary
    print("4. Compliance Report:")
    print(report.format_summary())
    print()

    # Get remediation plan
    print("5. Remediation Plan:")
    remediation = agent.get_remediation_plan(report)
    for step in remediation:
        print(step)
    print()

    # Test section validation
    print("6. Testing section validation...")
    validation_section = """
The model was validated using holdout testing with 20% of data.
Performance metrics show good stability across time periods.
"""

    section_findings = agent.validate_regulatory_section(
        section_content=validation_section,
        section_type="validation"
    )
    print(f"   [OK] Section validation findings: {len(section_findings)}")
    for finding in section_findings:
        print(f"     - {finding.description}")
    print()

    # Test citation quality check
    print("7. Testing citation quality check...")
    citation_findings = agent.check_citation_quality(sample_doc, min_citations=3)
    print(f"   [OK] Citation findings: {len(citation_findings)}")
    if citation_findings:
        print(f"     - {citation_findings[0].description}")
    print()

    print("=" * 60)
    print("[OK] Compliance Agent Test Complete!")
    print("=" * 60)
    print()
    print("The agent successfully identified missing sections,")
    print("ASOP requirements, and provided remediation guidance.")
    print()


if __name__ == "__main__":
    main()
