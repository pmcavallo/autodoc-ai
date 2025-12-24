"""
Retrieval Module for AutoDoc AI RAG System

This module provides advanced retrieval capabilities for querying the
ChromaDB vector store with metadata filtering, result ranking, and
context management for LLM prompts.

Key Features:
- Semantic search with cosine similarity
- Metadata filtering (document type, year, model type)
- Result re-ranking and deduplication
- Context window management for LLM prompts
- Citation generation with source tracking

Usage:
    from rag.retrieval import DocumentRetriever

    retriever = DocumentRetriever()
    results = retriever.retrieve(
        query="frequency model validation procedures",
        n_results=5,
        filters={"document_type": "model_doc"}
    )
"""

from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging
from dataclasses import dataclass

from rag.vector_store import VectorStore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class RetrievalResult:
    """
    Represents a single retrieval result with metadata and relevance score.
    """
    chunk_id: str
    text: str
    metadata: Dict
    distance: float
    rank: int

    @property
    def similarity(self) -> float:
        """Convert distance to similarity score (for cosine: similarity = 1 - distance)."""
        return 1.0 - self.distance

    @property
    def source_file(self) -> str:
        """Get the source filename."""
        return self.metadata.get('filename', 'Unknown')

    @property
    def section(self) -> str:
        """Get the section title."""
        return self.metadata.get('section', 'Unknown')

    def format_citation(self) -> str:
        """Format as a citation string."""
        return f"[{self.source_file}:{self.section}]"

    def __repr__(self):
        return f"RetrievalResult(id={self.chunk_id}, sim={self.similarity:.3f}, source={self.source_file})"


class DocumentRetriever:
    """
    Advanced retrieval interface for the AutoDoc AI knowledge base.

    This retriever provides:
    1. Semantic search using vector embeddings
    2. Metadata filtering for precise queries
    3. Result ranking and deduplication
    4. Context management for LLM prompts
    5. Source citation generation
    """

    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        collection_name: str = "autodoc_knowledge_base",
        default_n_results: int = 5
    ):
        """
        Initialize the document retriever.

        Args:
            vector_store: VectorStore instance (creates new if None)
            collection_name: ChromaDB collection name
            default_n_results: Default number of results to retrieve
        """
        self.collection_name = collection_name
        self.default_n_results = default_n_results

        # Initialize vector store
        if vector_store is None:
            logger.info("Initializing new VectorStore")
            self.vector_store = VectorStore()
            self.vector_store.initialize_client()
        else:
            self.vector_store = vector_store

        # Get collection
        try:
            self.collection = self.vector_store.get_collection(collection_name)
            logger.info(f"Retrieved collection '{collection_name}' with {self.collection.count()} documents")
        except ValueError:
            logger.error(f"Collection '{collection_name}' does not exist. Run ingestion first.")
            raise

    def _build_chroma_filter(self, filters: Optional[Dict]) -> Optional[Dict]:
        """
        Convert plain dictionary filters to ChromaDB operator format.

        ChromaDB v1.1+ requires filters to use operators like $eq, $and, etc.

        Args:
            filters: Plain dict like {"model_type": "frequency", "year": 2024}

        Returns:
            ChromaDB operator format like:
            {"$and": [{"model_type": {"$eq": "frequency"}}, {"year": {"$eq": 2024}}]}
            or None if filters is None/empty
        """
        if not filters:
            return None

        # Single filter
        if len(filters) == 1:
            key, value = list(filters.items())[0]
            return {key: {"$eq": value}}

        # Multiple filters - use $and
        filter_list = []
        for key, value in filters.items():
            filter_list.append({key: {"$eq": value}})

        return {"$and": filter_list}

    def retrieve(
        self,
        query: str,
        n_results: Optional[int] = None,
        filters: Optional[Dict] = None,
        min_similarity: float = 0.0
    ) -> List[RetrievalResult]:
        """
        Retrieve relevant documents for a query.
        
        FALLBACK LOGIC: If filters return 0 results:
        1. Try without 'year' filter (too restrictive)
        2. Try without any filters (last resort)

        Args:
            query: Query string
            n_results: Number of results to return (uses default if None)
            filters: Metadata filters (e.g., {"document_type": "model_doc", "year": 2023})
            min_similarity: Minimum similarity threshold (0-1)

        Returns:
            List of RetrievalResult objects, sorted by relevance
        """
        if n_results is None:
            n_results = self.default_n_results

        logger.info(f"Retrieving documents for query: '{query[:50]}...'")
        logger.info(f"Filters: {filters}, n_results: {n_results}, min_similarity: {min_similarity}")

        # Convert filters to ChromaDB operator format
        chroma_filters = self._build_chroma_filter(filters)
        if chroma_filters:
            logger.info(f"ChromaDB filters: {chroma_filters}")

        try:
            # Query ChromaDB with operator-formatted filters
            query_params = {
                "query_texts": [query],
                "n_results": n_results
            }

            # Only add where clause if filters exist
            if chroma_filters:
                query_params["where"] = chroma_filters

            raw_results = self.collection.query(**query_params)

            # Parse results
            results = []
            for i in range(len(raw_results['ids'][0])):
                result = RetrievalResult(
                    chunk_id=raw_results['ids'][0][i],
                    text=raw_results['documents'][0][i],
                    metadata=raw_results['metadatas'][0][i],
                    distance=raw_results['distances'][0][i],
                    rank=i + 1
                )

                # Apply similarity threshold
                if result.similarity >= min_similarity:
                    results.append(result)

            logger.info(f"Retrieved {len(results)} results (after filtering)")
            
            # FALLBACK LOGIC: If 0 results with filters, try without restrictive filters
            if len(results) == 0 and filters:
                logger.warning(f"No results with filters {filters}. Trying fallback...")
                
                # Try 1: Remove 'year' filter (most restrictive)
                if 'year' in filters and len(filters) > 1:
                    fallback_filters = {k: v for k, v in filters.items() if k != 'year'}
                    logger.info(f"Fallback 1: Trying without 'year' filter: {fallback_filters}")
                    return self.retrieve(
                        query=query,
                        n_results=n_results,
                        filters=fallback_filters,
                        min_similarity=min_similarity
                    )
                
                # Try 2: No filters at all (last resort)
                logger.warning(f"Fallback 2: Trying without any filters (last resort)")
                return self.retrieve(
                    query=query,
                    n_results=n_results,
                    filters=None,
                    min_similarity=min_similarity
                )
            
            return results

        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            raise

    def retrieve_by_document_type(
        self,
        query: str,
        document_type: str,
        n_results: Optional[int] = None
    ) -> List[RetrievalResult]:
        """
        Retrieve documents filtered by document type.

        Args:
            query: Query string
            document_type: Document type filter (e.g., "model_doc", "methodology", "regulation")
            n_results: Number of results to return

        Returns:
            List of RetrievalResult objects
        """
        return self.retrieve(
            query=query,
            n_results=n_results,
            filters={"document_type": document_type}
        )

    def retrieve_by_model_type(
        self,
        query: str,
        model_type: str,
        n_results: Optional[int] = None
    ) -> List[RetrievalResult]:
        """
        Retrieve model documentation filtered by model type.

        Args:
            query: Query string
            model_type: Model type filter (e.g., "frequency", "severity", "territory")
            n_results: Number of results to return

        Returns:
            List of RetrievalResult objects
        """
        return self.retrieve(
            query=query,
            n_results=n_results,
            filters={"model_type": model_type}
        )

    def retrieve_by_year(
        self,
        query: str,
        year: int,
        n_results: Optional[int] = None
    ) -> List[RetrievalResult]:
        """
        Retrieve documents filtered by year.

        Args:
            query: Query string
            year: Year filter (e.g., 2022, 2023, 2024)
            n_results: Number of results to return

        Returns:
            List of RetrievalResult objects
        """
        return self.retrieve(
            query=query,
            n_results=n_results,
            filters={"year": year}
        )

    def retrieve_multi_query(
        self,
        queries: List[str],
        n_results_per_query: int = 3,
        deduplicate: bool = True
    ) -> List[RetrievalResult]:
        """
        Retrieve documents for multiple queries and merge results.

        Useful for complex questions that require multiple perspectives.

        Args:
            queries: List of query strings
            n_results_per_query: Number of results per query
            deduplicate: Whether to remove duplicate chunks

        Returns:
            Merged list of RetrievalResult objects
        """
        logger.info(f"Multi-query retrieval with {len(queries)} queries")

        all_results = []
        seen_ids = set()

        for query in queries:
            results = self.retrieve(query=query, n_results=n_results_per_query)

            for result in results:
                if deduplicate:
                    if result.chunk_id not in seen_ids:
                        all_results.append(result)
                        seen_ids.add(result.chunk_id)
                else:
                    all_results.append(result)

        # Re-rank by similarity
        all_results.sort(key=lambda r: r.similarity, reverse=True)

        # Update ranks
        for i, result in enumerate(all_results):
            result.rank = i + 1

        logger.info(f"Multi-query retrieved {len(all_results)} unique results")
        return all_results

    def build_context(
        self,
        results: List[RetrievalResult],
        max_tokens: int = 4000,
        include_citations: bool = True,
        separator: str = "\n\n---\n\n"
    ) -> str:
        """
        Build context string for LLM prompt from retrieval results.

        Args:
            results: List of RetrievalResult objects
            max_tokens: Maximum context length in tokens (approximate)
            include_citations: Whether to include source citations
            separator: Separator between chunks

        Returns:
            Formatted context string
        """
        # Approximate: 1 token ≈ 4 characters
        max_chars = max_tokens * 4

        context_parts = []
        current_length = 0

        for result in results:
            # Format chunk with citation
            if include_citations:
                chunk_text = f"{result.format_citation()}\n{result.text}"
            else:
                chunk_text = result.text

            chunk_length = len(chunk_text) + len(separator)

            # Check if adding this chunk would exceed limit
            if current_length + chunk_length > max_chars:
                logger.info(f"Context limit reached. Including {len(context_parts)}/{len(results)} chunks")
                break

            context_parts.append(chunk_text)
            current_length += chunk_length

        context = separator.join(context_parts)
        logger.info(f"Built context: {len(context)} chars (~{len(context)//4} tokens) from {len(context_parts)} chunks")

        return context

    def get_relevant_sources(
        self,
        results: List[RetrievalResult],
        deduplicate: bool = True
    ) -> List[str]:
        """
        Extract list of source documents from results.

        Args:
            results: List of RetrievalResult objects
            deduplicate: Whether to remove duplicate sources

        Returns:
            List of source filenames
        """
        sources = [r.source_file for r in results]

        if deduplicate:
            # Preserve order while deduplicating
            seen = set()
            sources = [s for s in sources if not (s in seen or seen.add(s))]

        return sources

    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the collection.

        Returns:
            Dictionary with collection statistics
        """
        return {
            "name": self.collection.name,
            "count": self.collection.count(),
            "metadata": self.collection.metadata,
        }


def main():
    """
    Test function for retrieval module.
    """
    print("=" * 60)
    print("AutoDoc AI - Retrieval Module Test")
    print("=" * 60)
    print()

    try:
        # Initialize retriever
        print("1. Initializing DocumentRetriever...")
        retriever = DocumentRetriever()

        stats = retriever.get_collection_stats()
        print(f"   [OK] Collection: {stats['name']}")
        print(f"   [OK] Documents: {stats['count']}")
        print()

        if stats['count'] == 0:
            print("   [X] Collection is empty. Run ingestion first:")
            print("      python rag/ingestion.py")
            return

        # Test basic retrieval
        print("2. Testing basic retrieval...")
        query = "frequency model validation procedures"
        results = retriever.retrieve(query=query, n_results=3)

        print(f"   Query: '{query}'")
        print(f"   [OK] Retrieved {len(results)} results")
        print()

        for result in results[:2]:
            print(f"   Result {result.rank}:")
            print(f"   - Similarity: {result.similarity:.3f}")
            print(f"   - Source: {result.source_file}")
            print(f"   - Section: {result.section}")
            print(f"   - Citation: {result.format_citation()}")
            print(f"   - Text preview: {result.text[:100]}...")
            print()

        # Test filtered retrieval
        print("3. Testing filtered retrieval (model_doc only)...")
        results_filtered = retriever.retrieve_by_document_type(
            query="XGBoost model SHAP values",
            document_type="model_doc",
            n_results=3
        )
        print(f"   [OK] Retrieved {len(results_filtered)} model documents")
        sources = retriever.get_relevant_sources(results_filtered)
        print(f"   [OK] Sources: {sources}")
        print()

        # Test multi-query retrieval
        print("4. Testing multi-query retrieval...")
        queries = [
            "model validation framework",
            "three-tier validation",
            "holdout testing"
        ]
        multi_results = retriever.retrieve_multi_query(queries, n_results_per_query=2)
        print(f"   [OK] Retrieved {len(multi_results)} unique results from {len(queries)} queries")
        print()

        # Test context building
        print("5. Testing context building...")
        context = retriever.build_context(
            results=results,
            max_tokens=1000,
            include_citations=True
        )
        print(f"   [OK] Built context: {len(context)} characters (~{len(context)//4} tokens)")
        print(f"   [OK] Context preview:")
        print(f"   {context[:200]}...")
        print()

        print("=" * 60)
        print("[OK] Retrieval Module Test Complete!")
        print("=" * 60)

    except ValueError as e:
        print(f"\n[X] Error: {e}")
        print("\nPlease run the ingestion pipeline first:")
        print("   python rag/ingestion.py")
        print()


if __name__ == "__main__":
    main()
