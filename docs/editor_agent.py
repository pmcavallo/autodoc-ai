"""
Editor Agent for AutoDoc AI

This agent is responsible for reviewing and improving documentation quality.

Key Responsibilities:
- Review documentation for clarity and consistency
- Check grammar, style, and professional tone
- Verify citations and cross-references
- Ensure logical flow and organization
- Provide specific improvement suggestions

Usage:
    from agents.editor_agent import EditorAgent

    agent = EditorAgent()
    review = agent.review_document(document_content)
"""

from pathlib import Path
from typing import List, Dict, Optional, Set
import logging
from dataclasses import dataclass, field
from enum import Enum
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReviewCategory(Enum):
    """Categories for editorial review findings."""
    CLARITY = "Clarity"
    CONSISTENCY = "Consistency"
    GRAMMAR = "Grammar"
    STYLE = "Style"
    STRUCTURE = "Structure"
    CITATIONS = "Citations"
    TERMINOLOGY = "Terminology"


class ReviewPriority(Enum):
    """Priority levels for editorial suggestions."""
    CRITICAL = "CRITICAL"  # Errors that must be fixed
    HIGH = "HIGH"          # Strong recommendations
    MEDIUM = "MEDIUM"      # Suggestions for improvement
    LOW = "LOW"            # Optional enhancements


@dataclass
class EditorialFinding:
    """
    Represents a single editorial finding.
    """
    priority: ReviewPriority
    category: ReviewCategory
    description: str
    location: Optional[str] = None  # Section or paragraph reference
    suggestion: Optional[str] = None
    example: Optional[str] = None

    def __repr__(self):
        return f"EditorialFinding({self.priority.value}, {self.category.value}: {self.description[:40]}...)"


@dataclass
class EditorialReview:
    """
    Complete editorial review report.
    """
    document_title: str
    findings: List[EditorialFinding] = field(default_factory=list)
    word_count: int = 0
    readability_score: Optional[float] = None
    consistency_issues: int = 0
    overall_quality: str = "PENDING"

    def __post_init__(self):
        """Calculate overall quality score."""
        if not self.findings:
            self.overall_quality = "EXCELLENT"
        else:
            critical = len([f for f in self.findings if f.priority == ReviewPriority.CRITICAL])
            high = len([f for f in self.findings if f.priority == ReviewPriority.HIGH])

            if critical > 0:
                self.overall_quality = "NEEDS REVISION"
            elif high > 3:
                self.overall_quality = "FAIR"
            elif high > 0:
                self.overall_quality = "GOOD"
            else:
                self.overall_quality = "VERY GOOD"

    def get_findings_by_category(self, category: ReviewCategory) -> List[EditorialFinding]:
        """Get all findings in a specific category."""
        return [f for f in self.findings if f.category == category]

    def get_findings_by_priority(self, priority: ReviewPriority) -> List[EditorialFinding]:
        """Get all findings of a specific priority."""
        return [f for f in self.findings if f.priority == priority]

    def format_summary(self) -> str:
        """Format review as readable summary."""
        lines = [
            "=" * 60,
            "EDITORIAL REVIEW",
            "=" * 60,
            f"Document: {self.document_title}",
            f"Word Count: {self.word_count}",
            f"Overall Quality: {self.overall_quality}",
            "",
            f"Total Findings: {len(self.findings)}",
        ]

        # Count by priority
        for priority in ReviewPriority:
            count = len(self.get_findings_by_priority(priority))
            if count > 0:
                lines.append(f"  - {priority.value}: {count}")

        if self.readability_score:
            lines.append(f"\nReadability Score: {self.readability_score:.1f}/10")

        if self.findings:
            lines.append("\nFindings by Category:")
            lines.append("")

            for category in ReviewCategory:
                findings = self.get_findings_by_category(category)
                if findings:
                    lines.append(f"{category.value} ({len(findings)}):")
                    for finding in findings[:3]:  # Show top 3 per category
                        lines.append(f"  - [{finding.priority.value}] {finding.description}")
                        if finding.suggestion:
                            lines.append(f"    → {finding.suggestion}")
                    if len(findings) > 3:
                        lines.append(f"  ... and {len(findings)-3} more")
                    lines.append("")

        return "\n".join(lines)


class EditorAgent:
    """
    Agent for reviewing and improving documentation quality.

    This agent:
    1. Reviews documentation for clarity and consistency
    2. Checks professional tone and style
    3. Verifies proper citations
    4. Identifies structural issues
    5. Provides specific improvement recommendations
    """

    # Standard actuarial terminology
    STANDARD_TERMINOLOGY = {
        "freq": "frequency",
        "sev": "severity",
        "GLM": "generalized linear model",
        "pred": "prediction",
        "var": "variable",
        "perf": "performance",
    }

    # Required professional phrases
    PROFESSIONAL_PHRASES = [
        "based on",
        "consistent with",
        "in accordance with",
        "demonstrates",
        "indicates",
        "suggests"
    ]

    # Words to avoid in professional writing
    AVOID_WORDS = [
        "very",
        "really",
        "quite",
        "just",
        "basically",
        "actually",
        "literally"
    ]

    def __init__(
        self,
        enforce_style_guide: bool = True,
        check_citations: bool = True
    ):
        """
        Initialize the editor agent.

        Args:
            enforce_style_guide: Whether to enforce professional style guide
            check_citations: Whether to validate citations
        """
        self.enforce_style_guide = enforce_style_guide
        self.check_citations = check_citations

        logger.info("EditorAgent initialized")

    def review_document(
        self,
        document_content: str,
        document_title: str,
        document_type: str = "model_doc"
    ) -> EditorialReview:
        """
        Perform complete editorial review of a document.

        Args:
            document_content: Full document text
            document_title: Document title
            document_type: Type of document

        Returns:
            EditorialReview with findings and suggestions
        """
        logger.info(f"Reviewing document: {document_title}")

        review = EditorialReview(
            document_title=document_title,
            word_count=len(document_content.split())
        )

        # Run various checks
        review.findings.extend(self._check_structure(document_content))
        review.findings.extend(self._check_clarity(document_content))
        review.findings.extend(self._check_consistency(document_content))
        review.findings.extend(self._check_style(document_content))

        if self.check_citations:
            review.findings.extend(self._check_citations(document_content))

        review.findings.extend(self._check_terminology(document_content))
        review.findings.extend(self._check_formatting(document_content))

        # Calculate metrics
        review.consistency_issues = len(review.get_findings_by_category(ReviewCategory.CONSISTENCY))
        review.readability_score = self._calculate_readability(document_content)

        # Update overall quality
        review.__post_init__()

        logger.info(f"Review complete: {len(review.findings)} findings, quality: {review.overall_quality}")
        return review

    def _check_structure(self, content: str) -> List[EditorialFinding]:
        """Check document structure and organization."""
        findings = []

        # Check for proper heading hierarchy
        headings = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)

        if not headings:
            findings.append(EditorialFinding(
                priority=ReviewPriority.CRITICAL,
                category=ReviewCategory.STRUCTURE,
                description="No section headings found",
                suggestion="Add clear section headings using markdown format"
            ))
            return findings

        # Check heading levels
        prev_level = 0
        for i, (hashes, title) in enumerate(headings):
            level = len(hashes)

            # Check for skipped levels (e.g., # to ###)
            if level - prev_level > 1:
                findings.append(EditorialFinding(
                    priority=ReviewPriority.MEDIUM,
                    category=ReviewCategory.STRUCTURE,
                    description=f"Heading level skip detected at '{title}'",
                    location=f"Section: {title}",
                    suggestion="Use consistent heading hierarchy (don't skip levels)"
                ))

            prev_level = level

        # Check for very short sections
        sections = content.split('\n##')
        for section in sections:
            if len(section.split()) < 20 and len(section.strip()) > 0:
                section_title = section.split('\n')[0].strip('# ')
                findings.append(EditorialFinding(
                    priority=ReviewPriority.LOW,
                    category=ReviewCategory.STRUCTURE,
                    description=f"Very short section: '{section_title}'",
                    location=section_title,
                    suggestion="Consider expanding this section or merging with related content"
                ))

        return findings

    def _check_clarity(self, content: str) -> List[EditorialFinding]:
        """Check for clarity issues."""
        findings = []

        # Check for very long sentences (> 40 words)
        sentences = re.split(r'[.!?]+', content)
        for sentence in sentences:
            words = sentence.split()
            if len(words) > 40:
                findings.append(EditorialFinding(
                    priority=ReviewPriority.MEDIUM,
                    category=ReviewCategory.CLARITY,
                    description=f"Very long sentence ({len(words)} words)",
                    suggestion="Consider breaking into multiple sentences",
                    example=sentence[:100] + "..."
                ))

        # Check for passive voice indicators
        passive_indicators = ['was', 'were', 'been', 'being']
        passive_count = sum(content.lower().count(f' {word} ') for word in passive_indicators)

        if passive_count > len(content.split()) * 0.1:  # More than 10% passive
            findings.append(EditorialFinding(
                priority=ReviewPriority.LOW,
                category=ReviewCategory.CLARITY,
                description="Frequent use of passive voice detected",
                suggestion="Consider using active voice for clearer communication"
            ))

        # Check for undefined acronyms (3+ capital letters not first use)
        acronyms = re.findall(r'\b[A-Z]{3,}\b', content)
        unique_acronyms = list(set(acronyms))

        for acronym in unique_acronyms[:5]:  # Check first 5
            first_occurrence = content.find(acronym)
            # Check if defined (has parentheses nearby)
            context = content[max(0, first_occurrence-50):first_occurrence+50]
            if '(' not in context and acronym not in ['GLM', 'AUC', 'ASOP', 'NAIC']:
                findings.append(EditorialFinding(
                    priority=ReviewPriority.MEDIUM,
                    category=ReviewCategory.CLARITY,
                    description=f"Acronym '{acronym}' may not be defined on first use",
                    suggestion=f"Define acronym on first use: '{acronym} (Full Name)'"
                ))

        return findings

    def _check_consistency(self, content: str) -> List[EditorialFinding]:
        """Check for consistency issues."""
        findings = []

        # Check for inconsistent terminology
        inconsistencies = {
            ('modeling', 'modelling'): 'modeling',
            ('data set', 'dataset'): 'dataset',
            ('cross validation', 'cross-validation'): 'cross-validation',
        }

        for (term1, term2), preferred in inconsistencies.items():
            count1 = content.lower().count(term1.lower())
            count2 = content.lower().count(term2.lower())

            if count1 > 0 and count2 > 0:
                findings.append(EditorialFinding(
                    priority=ReviewPriority.MEDIUM,
                    category=ReviewCategory.CONSISTENCY,
                    description=f"Inconsistent usage: '{term1}' and '{term2}'",
                    suggestion=f"Use '{preferred}' consistently throughout"
                ))

        # Check for inconsistent date formats
        date_formats = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', content)
        if date_formats and len(set(date_formats)) > 3:
            findings.append(EditorialFinding(
                priority=ReviewPriority.LOW,
                category=ReviewCategory.CONSISTENCY,
                description="Multiple date formats detected",
                suggestion="Use consistent date format (e.g., YYYY-MM-DD)"
            ))

        return findings

    def _check_style(self, content: str) -> List[EditorialFinding]:
        """Check professional style."""
        findings = []

        if not self.enforce_style_guide:
            return findings

        # Check for words to avoid
        for word in self.AVOID_WORDS:
            count = len(re.findall(rf'\b{word}\b', content, re.IGNORECASE))
            if count > 0:
                findings.append(EditorialFinding(
                    priority=ReviewPriority.LOW,
                    category=ReviewCategory.STYLE,
                    description=f"Consider avoiding informal word '{word}' ({count} occurrences)",
                    suggestion=f"Remove or replace '{word}' with more precise language"
                ))

        # Check for first-person pronouns (rare in professional docs)
        first_person = ['I ', 'we ', 'our ', 'my ']
        first_person_count = sum(content.count(pronoun) for pronoun in first_person)

        if first_person_count > 5:
            findings.append(EditorialFinding(
                priority=ReviewPriority.LOW,
                category=ReviewCategory.STYLE,
                description="Frequent first-person pronouns",
                suggestion="Consider using third-person or passive constructions in formal documentation"
            ))

        return findings

    def _check_citations(self, content: str) -> List[EditorialFinding]:
        """Check citation quality and consistency."""
        findings = []

        # Find citations in format [filename:section]
        citations = re.findall(r'\[([^\]]+\.md):([^\]]+)\]', content)

        if not citations:
            findings.append(EditorialFinding(
                priority=ReviewPriority.MEDIUM,
                category=ReviewCategory.CITATIONS,
                description="No citations found",
                suggestion="Add citations to support methodology and claims"
            ))
            return findings

        # Check for broken citation format
        potential_citations = re.findall(r'\[[^\]]+\](?!\()', content)
        for citation in potential_citations:
            if ':' not in citation and '.md' in citation:
                findings.append(EditorialFinding(
                    priority=ReviewPriority.HIGH,
                    category=ReviewCategory.CITATIONS,
                    description=f"Malformed citation: {citation}",
                    suggestion="Use format [filename.md:section]",
                    example=citation
                ))

        # Check for citation diversity
        unique_sources = set(source for source, _ in citations)
        if len(unique_sources) < 2 and len(citations) > 3:
            findings.append(EditorialFinding(
                priority=ReviewPriority.LOW,
                category=ReviewCategory.CITATIONS,
                description="Limited source diversity in citations",
                suggestion="Consider citing multiple authoritative sources"
            ))

        return findings

    def _check_terminology(self, content: str) -> List[EditorialFinding]:
        """Check for proper terminology usage."""
        findings = []

        # Check for non-standard abbreviations
        for abbrev, full_term in self.STANDARD_TERMINOLOGY.items():
            if abbrev.lower() in content.lower() and full_term not in content.lower():
                findings.append(EditorialFinding(
                    priority=ReviewPriority.MEDIUM,
                    category=ReviewCategory.TERMINOLOGY,
                    description=f"Non-standard abbreviation '{abbrev}' used",
                    suggestion=f"Use full term '{full_term}' or spell out on first use"
                ))

        return findings

    def _check_formatting(self, content: str) -> List[EditorialFinding]:
        """Check markdown formatting."""
        findings = []

        # Check for proper list formatting
        list_items = re.findall(r'^\s*[-*+]\s*.+$', content, re.MULTILINE)
        if list_items:
            for item in list_items[:3]:
                if not item.strip().startswith(('-', '*', '+')):
                    findings.append(EditorialFinding(
                        priority=ReviewPriority.LOW,
                        category=ReviewCategory.STRUCTURE,
                        description="Inconsistent list formatting",
                        suggestion="Use consistent bullet character (-, *, or +)"
                    ))
                    break

        # Check for proper code block formatting
        inline_code = re.findall(r'`[^`]+`', content)
        if len(inline_code) > 10:
            findings.append(EditorialFinding(
                priority=ReviewPriority.LOW,
                category=ReviewCategory.STRUCTURE,
                description="Many inline code elements",
                suggestion="Consider using code blocks for longer code snippets"
            ))

        return findings

    def _calculate_readability(self, content: str) -> float:
        """
        Calculate readability score (0-10, higher is more readable).

        Simplified metric based on:
        - Average sentence length
        - Average word length
        - Use of technical jargon
        """
        sentences = [s.strip() for s in re.split(r'[.!?]+', content) if s.strip()]
        words = content.split()

        if not sentences or not words:
            return 0.0

        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)

        # Simplified scoring (professional docs typically score 5-7)
        score = 10.0
        score -= (avg_sentence_length - 15) * 0.1  # Penalty for long sentences
        score -= (avg_word_length - 5) * 0.5      # Penalty for long words
        score = max(0.0, min(10.0, score))

        return score

    def suggest_improvements(
        self,
        review: EditorialReview,
        max_suggestions: int = 10
    ) -> List[str]:
        """
        Generate prioritized list of improvement suggestions.

        Args:
            review: EditorialReview object
            max_suggestions: Maximum number of suggestions to return

        Returns:
            List of improvement suggestions
        """
        suggestions = []

        # Prioritize by priority level
        for priority in [ReviewPriority.CRITICAL, ReviewPriority.HIGH,
                        ReviewPriority.MEDIUM, ReviewPriority.LOW]:
            findings = review.get_findings_by_priority(priority)

            for finding in findings:
                if finding.suggestion and len(suggestions) < max_suggestions:
                    suggestions.append(f"[{priority.value}] {finding.suggestion}")

        return suggestions


def main():
    """
    Test function for editor agent.
    """
    print("=" * 60)
    print("AutoDoc AI - Editor Agent Test")
    print("=" * 60)
    print()

    # Initialize agent
    print("1. Initializing EditorAgent...")
    agent = EditorAgent()
    print("   [OK] Agent initialized")
    print()

    # Create sample document with various issues
    print("2. Creating sample document for testing...")
    sample_doc = """
# Model Documentation

## Executive Summary

This document describes a freq model. The model was really good and performs very well.
We used GLM and got great results basically showing that the model is quite effective.

## Methodology

The modeling approach utilizes machine learning. Data set was prepared carefully.
Cross validation was used for testing. Model performance was evaluated using various metrics.

This is a very long sentence that goes on and on without any breaks or pauses and contains multiple clauses that could easily be split into separate sentences for better readability and clarity which would make it much easier for readers to understand the content being presented here.

## Results

The model achieves an AUC of 0.72. The freq predictions are accurate.
Results were validated using cross-validation techniques.

### Performance Metrics

Performance was excellent. Results show improvement.

## Implementation

The model will be deployed to production systems.
Monitoring procedures have been established.
"""

    print("   [OK] Sample document created")
    print()

    # Run editorial review
    print("3. Running editorial review...")
    review = agent.review_document(
        document_content=sample_doc,
        document_title="Model Documentation Test",
        document_type="model_doc"
    )
    print(f"   [OK] Review complete")
    print(f"   [OK] Overall Quality: {review.overall_quality}")
    print(f"   [OK] Total findings: {len(review.findings)}")
    print()

    # Display review summary
    print("4. Editorial Review:")
    print(review.format_summary())
    print()

    # Get improvement suggestions
    print("5. Top Improvement Suggestions:")
    suggestions = agent.suggest_improvements(review, max_suggestions=5)
    for i, suggestion in enumerate(suggestions, 1):
        print(f"   {i}. {suggestion}")
    print()

    # Show findings by category
    print("6. Findings Summary by Category:")
    for category in ReviewCategory:
        findings = review.get_findings_by_category(category)
        if findings:
            print(f"   {category.value}: {len(findings)} issues")
    print()

    print("=" * 60)
    print("[OK] Editor Agent Test Complete!")
    print("=" * 60)
    print()
    print("The agent successfully identified clarity, consistency,")
    print("style, and citation issues in the sample document.")
    print()


if __name__ == "__main__":
    main()
