"""
Research Agent for AutoDoc AI

This agent is responsible for gathering relevant information from the
knowledge base to support documentation generation tasks.

Key Responsibilities:
- Query the vector store for relevant context
- Synthesize information from multiple sources
- Generate proper citations and source tracking
- Provide structured research summaries

Usage:
    from agents.research_agent import ResearchAgent

    agent = ResearchAgent()
    research = agent.research_topic("frequency model validation procedures")
"""

from pathlib import Path
from typing import List, Dict, Optional
import logging
from dataclasses import dataclass, field

from rag.retrieval import DocumentRetriever, RetrievalResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ResearchFindings:
    """
    Structured research findings from the knowledge base.
    """
    query: str
    findings: List[RetrievalResult]
    context: str
    sources: List[str]
    summary: Optional[str] = None
    confidence: float = 0.0

    def __post_init__(self):
        """Calculate confidence score based on result similarities."""
        if self.findings:
            avg_similarity = sum(r.similarity for r in self.findings) / len(self.findings)
            self.confidence = avg_similarity

    def format_summary(self) -> str:
        """Format research findings as a readable summary."""
        lines = [
            f"Research Query: {self.query}",
            f"Confidence: {self.confidence:.2%}",
            f"Sources: {len(self.sources)} documents",
            "",
            "Key Findings:",
        ]

        for i, result in enumerate(self.findings[:3], 1):
            lines.append(f"\n{i}. {result.format_citation()} (relevance: {result.similarity:.2%})")
            lines.append(f"   {result.text[:200]}...")

        if self.summary:
            lines.append("\n\nSummary:")
            lines.append(self.summary)

        return "\n".join(lines)


class ResearchAgent:
    """
    Agent for researching topics in the AutoDoc AI knowledge base.

    This agent:
    1. Accepts research queries
    2. Retrieves relevant information from vector store
    3. Synthesizes findings from multiple sources
    4. Tracks citations and sources
    5. Provides structured research outputs
    """

    def __init__(
        self,
        retriever: Optional[DocumentRetriever] = None,
        default_n_results: int = 5,
        min_similarity: float = 0.3
    ):
        """
        Initialize the research agent.

        Args:
            retriever: DocumentRetriever instance (creates new if None)
            default_n_results: Default number of results to retrieve
            min_similarity: Minimum similarity threshold for results
        """
        self.default_n_results = default_n_results
        self.min_similarity = min_similarity

        # Initialize retriever
        if retriever is None:
            logger.info("ResearchAgent: Initializing DocumentRetriever")
            self.retriever = DocumentRetriever()
        else:
            self.retriever = retriever

        logger.info("ResearchAgent initialized")

    def research_topic(
        self,
        topic: str,
        n_results: Optional[int] = None,
        filters: Optional[Dict] = None,
        include_summary: bool = False
    ) -> ResearchFindings:
        """
        Research a specific topic in the knowledge base.

        Args:
            topic: Topic or question to research
            n_results: Number of results to retrieve
            filters: Metadata filters for targeted search
            include_summary: Whether to generate a summary (requires LLM)

        Returns:
            ResearchFindings object with structured results
        """
        logger.info(f"Researching topic: '{topic}'")

        if n_results is None:
            n_results = self.default_n_results

        # Retrieve relevant documents
        results = self.retriever.retrieve(
            query=topic,
            n_results=n_results,
            filters=filters,
            min_similarity=self.min_similarity
        )

        if not results:
            logger.warning(f"No results found for topic: '{topic}'")

        # Build context
        context = self.retriever.build_context(
            results=results,
            max_tokens=4000,
            include_citations=True
        )

        # Get sources
        sources = self.retriever.get_relevant_sources(results)

        # Create research findings
        findings = ResearchFindings(
            query=topic,
            findings=results,
            context=context,
            sources=sources
        )

        # Generate summary if requested (placeholder - would use LLM in production)
        if include_summary:
            findings.summary = self._generate_summary(findings)

        logger.info(f"Research complete: {len(results)} findings, confidence {findings.confidence:.2%}")
        return findings

    def research_multi_topic(
        self,
        topics: List[str],
        n_results_per_topic: int = 3
    ) -> List[ResearchFindings]:
        """
        Research multiple related topics.

        Args:
            topics: List of topics to research
            n_results_per_topic: Number of results per topic

        Returns:
            List of ResearchFindings, one per topic
        """
        logger.info(f"Researching {len(topics)} topics")

        all_findings = []
        for topic in topics:
            findings = self.research_topic(topic, n_results=n_results_per_topic)
            all_findings.append(findings)

        return all_findings

    def research_by_document_type(
        self,
        topic: str,
        document_type: str,
        n_results: Optional[int] = None
    ) -> ResearchFindings:
        """
        Research a topic within specific document types.

        Args:
            topic: Topic to research
            document_type: Document type filter (e.g., "model_doc", "methodology")
            n_results: Number of results to retrieve

        Returns:
            ResearchFindings object
        """
        logger.info(f"Researching '{topic}' in document type: {document_type}")

        return self.research_topic(
            topic=topic,
            n_results=n_results,
            filters={"document_type": document_type}
        )

    def research_model_documentation(
        self,
        topic: str,
        model_type: Optional[str] = None,
        year: Optional[int] = None,
        n_results: Optional[int] = None
    ) -> ResearchFindings:
        """
        Research topic in model documentation with optional filters.

        Args:
            topic: Topic to research
            model_type: Model type filter (e.g., "frequency", "severity")
            year: Year filter
            n_results: Number of results to retrieve

        Returns:
            ResearchFindings object
        """
        filters = {"document_type": "model_doc"}

        if model_type:
            filters["model_type"] = model_type
        if year:
            filters["year"] = year

        logger.info(f"Researching model documentation: '{topic}' with filters {filters}")

        return self.research_topic(
            topic=topic,
            n_results=n_results,
            filters=filters
        )

    def research_regulatory_requirements(
        self,
        topic: str,
        n_results: Optional[int] = None
    ) -> ResearchFindings:
        """
        Research regulatory requirements and compliance topics.

        Args:
            topic: Regulatory topic to research
            n_results: Number of results to retrieve

        Returns:
            ResearchFindings object
        """
        logger.info(f"Researching regulatory requirements: '{topic}'")

        return self.research_topic(
            topic=topic,
            n_results=n_results,
            filters={"document_type": "regulation"}
        )

    def compare_models(
        self,
        model_type: str,
        years: List[int],
        aspect: str
    ) -> Dict[int, ResearchFindings]:
        """
        Compare specific aspects across model versions.

        Args:
            model_type: Type of model (e.g., "frequency", "severity")
            years: List of years to compare
            aspect: Aspect to compare (e.g., "validation", "performance")

        Returns:
            Dictionary mapping year to ResearchFindings
        """
        logger.info(f"Comparing {model_type} models across years {years} for aspect: {aspect}")

        comparison = {}
        for year in years:
            query = f"{model_type} model {aspect}"
            findings = self.research_model_documentation(
                topic=query,
                model_type=model_type,
                year=year,
                n_results=3
            )
            comparison[year] = findings

        return comparison

    def find_similar_sections(
        self,
        reference_text: str,
        n_results: int = 5,
        filters: Optional[Dict] = None
    ) -> List[RetrievalResult]:
        """
        Find sections similar to a reference text.

        Useful for finding precedents or similar documentation.

        Args:
            reference_text: Text to find similar sections for
            n_results: Number of similar sections to find
            filters: Optional metadata filters

        Returns:
            List of RetrievalResult objects
        """
        logger.info(f"Finding similar sections to reference text ({len(reference_text)} chars)")

        results = self.retriever.retrieve(
            query=reference_text,
            n_results=n_results,
            filters=filters,
            min_similarity=self.min_similarity
        )

        return results

    def _generate_summary(self, findings: ResearchFindings) -> str:
        """
        Generate a summary of research findings.

        In production, this would use an LLM to synthesize findings.
        For now, returns a structured placeholder.

        Args:
            findings: ResearchFindings object

        Returns:
            Summary string
        """
        # Placeholder implementation
        summary_parts = [
            f"Research on '{findings.query}' yielded {len(findings.findings)} relevant sources.",
            f"Confidence level: {findings.confidence:.2%}",
            f"Key sources: {', '.join(findings.sources[:3])}"
        ]

        if findings.findings:
            top_result = findings.findings[0]
            summary_parts.append(f"\nMost relevant finding ({top_result.similarity:.2%} match):")
            summary_parts.append(f"{top_result.text[:300]}...")

        return "\n".join(summary_parts)

    def get_context_for_writing(
        self,
        section_topic: str,
        max_tokens: int = 3000,
        document_types: Optional[List[str]] = None
    ) -> str:
        """
        Get formatted context for a writing task.

        Args:
            section_topic: Topic for the section to be written
            max_tokens: Maximum context tokens
            document_types: List of document types to search

        Returns:
            Formatted context string with citations
        """
        logger.info(f"Getting context for writing: '{section_topic}'")

        # If document types specified, search each and merge
        if document_types:
            all_results = []
            for doc_type in document_types:
                results = self.retriever.retrieve(
                    query=section_topic,
                    n_results=3,
                    filters={"document_type": doc_type}
                )
                all_results.extend(results)

            # Sort by similarity
            all_results.sort(key=lambda r: r.similarity, reverse=True)
            results = all_results
        else:
            results = self.retriever.retrieve(
                query=section_topic,
                n_results=5
            )

        # Build context
        context = self.retriever.build_context(
            results=results,
            max_tokens=max_tokens,
            include_citations=True
        )

        return context


def main():
    """
    Test function for research agent.
    """
    print("=" * 60)
    print("AutoDoc AI - Research Agent Test")
    print("=" * 60)
    print()

    try:
        # Initialize agent
        print("1. Initializing ResearchAgent...")
        agent = ResearchAgent()
        print("   [OK] Agent initialized")
        print()

        # Test basic research
        print("2. Testing basic research...")
        topic = "model validation procedures"
        findings = agent.research_topic(topic, n_results=3)

        print(f"   Topic: '{topic}'")
        print(f"   [OK] Findings: {len(findings.findings)}")
        print(f"   [OK] Confidence: {findings.confidence:.2%}")
        print(f"   [OK] Sources: {findings.sources}")
        print()

        # Display findings
        print("3. Research Findings:")
        for result in findings.findings[:2]:
            print(f"   - {result.format_citation()} (relevance: {result.similarity:.2%})")
            print(f"     {result.text[:100]}...")
            print()

        # Test filtered research
        print("4. Testing filtered research (model documentation only)...")
        model_findings = agent.research_model_documentation(
            topic="XGBoost SHAP values",
            n_results=2
        )
        print(f"   [OK] Found {len(model_findings.findings)} model doc results")
        print(f"   [OK] Confidence: {model_findings.confidence:.2%}")
        print()

        # Test regulatory research
        print("5. Testing regulatory research...")
        reg_findings = agent.research_regulatory_requirements(
            topic="NAIC Model Audit Rule",
            n_results=2
        )
        print(f"   [OK] Found {len(reg_findings.findings)} regulatory results")
        print()

        # Test context generation
        print("6. Testing context generation for writing...")
        context = agent.get_context_for_writing(
            section_topic="frequency model validation framework",
            max_tokens=1000
        )
        print(f"   [OK] Generated context: {len(context)} chars (~{len(context)//4} tokens)")
        print(f"   [OK] Context preview:")
        print(f"   {context[:200]}...")
        print()

        # Test formatted summary
        print("7. Testing formatted summary...")
        summary = findings.format_summary()
        print(f"   [OK] Summary length: {len(summary)} chars")
        print()
        print(summary[:400])
        print()

        print("=" * 60)
        print("[OK] Research Agent Test Complete!")
        print("=" * 60)

    except Exception as e:
        print(f"\n[X] Error: {e}")
        print("\nPlease ensure the vector store is populated:")
        print("   python rag/ingestion.py")
        print()


if __name__ == "__main__":
    main()
