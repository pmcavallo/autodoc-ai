"""
Vector Store Setup for AutoDoc AI - ChromaDB Implementation

This module initializes and manages the ChromaDB vector store for storing
and retrieving embedded document chunks from synthetic insurance model documentation.

Usage:
    python rag/vector_store.py  # Test initialization
"""

import chromadb
from chromadb.config import Settings
from pathlib import Path
from typing import Optional, Dict, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
CHROMA_DB_PATH = PROJECT_ROOT / "chroma_db"
DATA_PATH = PROJECT_ROOT / "data"


class VectorStore:
    """
    ChromaDB vector store manager for AutoDoc AI knowledge base.

    This class handles initialization, configuration, and basic operations
    for the persistent ChromaDB instance storing embedded documentation chunks.
    """

    def __init__(self, persist_directory: Optional[Path] = None):
        """
        Initialize ChromaDB client with persistent storage.

        Args:
            persist_directory: Path to ChromaDB storage directory.
                              Defaults to PROJECT_ROOT/chroma_db
        """
        self.persist_directory = persist_directory or CHROMA_DB_PATH
        self.client = None
        self.collection = None

        logger.info(f"Initializing VectorStore with directory: {self.persist_directory}")

    def initialize_client(self) -> chromadb.Client:
        """
        Create and configure ChromaDB persistent client.

        Returns:
            Configured ChromaDB client instance
        """
        # Create directory if it doesn't exist
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        # Initialize persistent client with optimized settings
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(
                anonymized_telemetry=False,  # Disable telemetry for privacy
                allow_reset=True,            # Allow database reset if needed
            )
        )

        logger.info(f"ChromaDB client initialized at {self.persist_directory}")
        return self.client

    def create_collection(
        self,
        name: str = "autodoc_knowledge_base",
        metadata: Optional[Dict] = None
    ) -> chromadb.Collection:
        """
        Create or retrieve the main document collection.

        Args:
            name: Collection name (default: "autodoc_knowledge_base")
            metadata: Optional collection metadata

        Returns:
            ChromaDB collection instance
        """
        if self.client is None:
            self.initialize_client()

        # Default metadata if not provided
        if metadata is None:
            metadata = {
                "description": "Synthetic insurance model documentation for RAG system",
                "project": "AutoDoc AI",
                "data_type": "synthetic",
                "hnsw:space": "cosine",  # Use cosine similarity for semantic search
                "hnsw:construction_ef": 200,  # Higher = better recall, slower indexing
                "hnsw:search_ef": 100,  # Higher = better recall, slower search
            }

        # Get or create collection
        try:
            self.collection = self.client.get_or_create_collection(
                name=name,
                metadata=metadata
            )
            logger.info(f"Collection '{name}' initialized with {self.collection.count()} documents")
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise

        return self.collection

    def get_collection(self, name: str = "autodoc_knowledge_base") -> chromadb.Collection:
        """
        Retrieve existing collection by name.

        Args:
            name: Collection name to retrieve

        Returns:
            ChromaDB collection instance

        Raises:
            ValueError: If collection does not exist
        """
        if self.client is None:
            self.initialize_client()

        try:
            self.collection = self.client.get_collection(name=name)
            logger.info(f"Retrieved collection '{name}' with {self.collection.count()} documents")
            return self.collection
        except Exception as e:
            logger.error(f"Collection '{name}' not found: {e}")
            raise ValueError(f"Collection '{name}' does not exist. Create it first.")

    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict],
        ids: List[str]
    ) -> None:
        """
        Add document chunks to the collection.

        Args:
            documents: List of text chunks to embed and store
            metadatas: List of metadata dicts (one per document)
            ids: List of unique IDs (one per document)

        Note:
            ChromaDB will automatically generate embeddings using default
            sentence-transformers model (all-MiniLM-L6-v2).
        """
        if self.collection is None:
            raise ValueError("Collection not initialized. Call create_collection() first.")

        if not (len(documents) == len(metadatas) == len(ids)):
            raise ValueError("documents, metadatas, and ids must have same length")

        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(documents)} documents to collection")
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise

    def query(
        self,
        query_texts: List[str],
        n_results: int = 5,
        where: Optional[Dict] = None,
        where_document: Optional[Dict] = None
    ) -> Dict:
        """
        Query the collection for similar documents.

        Args:
            query_texts: List of query strings to search for
            n_results: Number of results to return per query
            where: Optional metadata filter (e.g., {"model_type": "frequency"})
            where_document: Optional document content filter

        Returns:
            Dictionary containing:
                - ids: List of document IDs
                - distances: List of cosine distances
                - documents: List of document texts
                - metadatas: List of metadata dicts
        """
        if self.collection is None:
            raise ValueError("Collection not initialized. Call get_collection() first.")

        try:
            results = self.collection.query(
                query_texts=query_texts,
                n_results=n_results,
                where=where,
                where_document=where_document
            )
            logger.info(f"Query returned {len(results['ids'][0])} results")
            return results
        except Exception as e:
            logger.error(f"Error querying collection: {e}")
            raise

    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the current collection.

        Returns:
            Dictionary with collection statistics
        """
        if self.collection is None:
            raise ValueError("Collection not initialized.")

        stats = {
            "name": self.collection.name,
            "count": self.collection.count(),
            "metadata": self.collection.metadata,
        }

        # Try to get sample documents for more detailed stats
        try:
            sample = self.collection.peek(limit=10)
            if sample and sample.get('metadatas'):
                # Extract unique document types
                doc_types = set()
                for meta in sample['metadatas']:
                    if 'document_type' in meta:
                        doc_types.add(meta['document_type'])
                stats['document_types_sample'] = list(doc_types)
        except Exception as e:
            logger.warning(f"Could not retrieve sample documents: {e}")

        return stats

    def reset_collection(self, name: str = "autodoc_knowledge_base") -> None:
        """
        Delete and recreate collection (WARNING: deletes all data).

        Args:
            name: Collection name to reset
        """
        if self.client is None:
            self.initialize_client()

        try:
            self.client.delete_collection(name=name)
            logger.warning(f"Deleted collection '{name}'")
            self.create_collection(name=name)
            logger.info(f"Recreated collection '{name}'")
        except Exception as e:
            logger.error(f"Error resetting collection: {e}")
            raise


def initialize_vector_store() -> VectorStore:
    """
    Convenience function to initialize vector store with default settings.

    Returns:
        Configured VectorStore instance with collection initialized
    """
    store = VectorStore()
    store.initialize_client()
    store.create_collection()
    return store


def get_vector_store() -> VectorStore:
    """
    Get existing vector store instance (does not create collection).

    Returns:
        VectorStore instance with client initialized
    """
    store = VectorStore()
    store.initialize_client()
    try:
        store.get_collection()
    except ValueError:
        logger.warning("Collection does not exist. Call initialize_vector_store() first.")
    return store


def main():
    """
    Test function for vector store initialization and basic operations.
    """
    print("="*60)
    print("AutoDoc AI - Vector Store Initialization Test")
    print("="*60)
    print()

    # Initialize vector store
    print("1. Initializing ChromaDB client...")
    store = initialize_vector_store()
    print(f"   ✓ Client initialized at: {store.persist_directory}")
    print(f"   ✓ Collection: {store.collection.name}")
    print()

    # Get collection stats
    print("2. Collection Statistics:")
    stats = store.get_collection_stats()
    for key, value in stats.items():
        print(f"   - {key}: {value}")
    print()

    # Test adding sample documents (if collection is empty)
    if store.collection.count() == 0:
        print("3. Adding sample documents for testing...")
        sample_docs = [
            "This is a sample frequency model documentation for testing purposes.",
            "This is a sample severity model documentation for testing purposes.",
            "This is a sample territory rating model documentation for testing purposes."
        ]
        sample_metadata = [
            {"document_type": "model_doc", "model_type": "frequency", "year": 2022},
            {"document_type": "model_doc", "model_type": "severity", "year": 2022},
            {"document_type": "model_doc", "model_type": "territory", "year": 2023}
        ]
        sample_ids = ["test_doc_1", "test_doc_2", "test_doc_3"]

        store.add_documents(
            documents=sample_docs,
            metadatas=sample_metadata,
            ids=sample_ids
        )
        print(f"   ✓ Added {len(sample_docs)} sample documents")
        print()

    # Test querying
    print("4. Testing query functionality...")
    query_result = store.query(
        query_texts=["frequency model documentation"],
        n_results=2
    )
    print(f"   ✓ Query returned {len(query_result['ids'][0])} results")
    print()

    # Display sample results
    if query_result['ids'][0]:
        print("5. Sample Query Results:")
        for i, doc_id in enumerate(query_result['ids'][0]):
            print(f"   Result {i+1}:")
            print(f"   - ID: {doc_id}")
            print(f"   - Distance: {query_result['distances'][0][i]:.4f}")
            print(f"   - Metadata: {query_result['metadatas'][0][i]}")
            print(f"   - Text preview: {query_result['documents'][0][i][:100]}...")
            print()

    # Final stats
    print("6. Final Collection Statistics:")
    final_stats = store.get_collection_stats()
    print(f"   - Total documents: {final_stats['count']}")
    print(f"   - Collection name: {final_stats['name']}")
    print()

    print("="*60)
    print("✓ Vector Store Setup Complete!")
    print("="*60)
    print()
    print("Next Steps:")
    print("  1. Run document ingestion: python rag/ingestion.py")
    print("  2. Test RAG retrieval: python rag/retrieval.py")
    print("  3. Start building agents: see agents/ directory")
    print()


if __name__ == "__main__":
    main()
