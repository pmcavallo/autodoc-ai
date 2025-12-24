"""
Document Ingestion Pipeline for AutoDoc AI RAG System

This module orchestrates the complete document ingestion process:
1. Load documents from data directories
2. Chunk documents using intelligent chunking strategy
3. Generate embeddings using sentence-transformers
4. Store chunks and embeddings in ChromaDB vector store

Usage:
    # Ingest all synthetic documents
    python rag/ingestion.py

    # Or use programmatically
    from rag.ingestion import DocumentIngestionPipeline

    pipeline = DocumentIngestionPipeline()
    pipeline.ingest_all_documents()
"""

from pathlib import Path
from typing import List, Dict, Optional
import logging
from tqdm import tqdm

# Import our RAG components
from rag.vector_store import VectorStore
from rag.chunks.chunking_strategy import DocumentChunker, DocumentChunk
from rag.embeddings import create_embedding_function

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_ROOT = PROJECT_ROOT / "data"
SYNTHETIC_DOCS_DIR = DATA_ROOT / "synthetic_docs"
ANCHOR_DOC_DIR = DATA_ROOT / "anchor_document"
REGULATIONS_DIR = DATA_ROOT / "regulations"


class DocumentIngestionPipeline:
    """
    Complete pipeline for ingesting documents into ChromaDB.

    This pipeline:
    1. Discovers documents in configured directories
    2. Chunks documents respecting semantic boundaries
    3. Generates embeddings for each chunk
    4. Stores chunks with metadata in vector store
    5. Provides statistics and error handling
    """

    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        chunker: Optional[DocumentChunker] = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        embedding_model: str = "all-MiniLM-L6-v2",
        collection_name: str = "autodoc_knowledge_base"
    ):
        """
        Initialize the ingestion pipeline.

        Args:
            vector_store: VectorStore instance (creates new if None)
            chunker: DocumentChunker instance (creates new if None)
            chunk_size: Target chunk size in tokens
            chunk_overlap: Overlap between chunks in tokens
            embedding_model: Name of sentence-transformers model
            collection_name: ChromaDB collection name
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model
        self.collection_name = collection_name

        # Initialize vector store
        if vector_store is None:
            logger.info("Initializing new VectorStore")
            self.vector_store = VectorStore()
            self.vector_store.initialize_client()
        else:
            self.vector_store = vector_store

        # Initialize chunker
        if chunker is None:
            logger.info(f"Initializing DocumentChunker (size={chunk_size}, overlap={chunk_overlap})")
            self.chunker = DocumentChunker(
                chunk_size=chunk_size,
                overlap=chunk_overlap
            )
        else:
            self.chunker = chunker

        # Create or get collection with custom embedding function
        logger.info(f"Setting up collection: {collection_name}")
        self._setup_collection()

        # Statistics
        self.stats = {
            "documents_processed": 0,
            "chunks_created": 0,
            "chunks_stored": 0,
            "errors": []
        }

    def _setup_collection(self):
        """
        Setup ChromaDB collection with custom embedding function.
        """
        try:
            # Create embedding function
            embedding_fn = create_embedding_function(model_name=self.embedding_model)

            # Try to get existing collection
            try:
                self.collection = self.vector_store.client.get_collection(
                    name=self.collection_name,
                    embedding_function=embedding_fn
                )
                logger.info(f"Retrieved existing collection '{self.collection_name}' with {self.collection.count()} documents")
            except:
                # Create new collection
                self.collection = self.vector_store.client.create_collection(
                    name=self.collection_name,
                    embedding_function=embedding_fn,
                    metadata={
                        "description": "AutoDoc AI synthetic insurance model documentation",
                        "embedding_model": self.embedding_model,
                        "chunk_size": self.chunk_size,
                        "chunk_overlap": self.chunk_overlap,
                        "hnsw:space": "cosine",
                        "hnsw:construction_ef": 200,
                        "hnsw:search_ef": 100,
                    }
                )
                logger.info(f"Created new collection '{self.collection_name}'")

        except Exception as e:
            logger.error(f"Error setting up collection: {e}")
            raise

    def ingest_document(self, file_path: Path) -> int:
        """
        Ingest a single document into the vector store.

        Args:
            file_path: Path to markdown document

        Returns:
            Number of chunks created and stored
        """
        logger.info(f"Ingesting document: {file_path.name}")

        try:
            # Chunk the document
            chunks = self.chunker.chunk_document(file_path)
            self.stats["chunks_created"] += len(chunks)

            if not chunks:
                logger.warning(f"No chunks created from {file_path.name}")
                return 0

            # Prepare data for ChromaDB
            documents = [chunk.text for chunk in chunks]
            metadatas = [chunk.metadata for chunk in chunks]
            ids = [chunk.chunk_id for chunk in chunks]

            # Store in ChromaDB (embeddings generated automatically)
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

            self.stats["chunks_stored"] += len(chunks)
            self.stats["documents_processed"] += 1

            logger.info(f"[OK] Stored {len(chunks)} chunks from {file_path.name}")
            return len(chunks)

        except Exception as e:
            error_msg = f"Error ingesting {file_path.name}: {e}"
            logger.error(error_msg)
            self.stats["errors"].append(error_msg)
            return 0

    def ingest_directory(
        self,
        directory: Path,
        pattern: str = "*.md",
        show_progress: bool = True
    ) -> Dict[str, int]:
        """
        Ingest all documents from a directory.

        Args:
            directory: Path to directory containing documents
            pattern: Glob pattern for files to ingest
            show_progress: Whether to show progress bar

        Returns:
            Dictionary with ingestion statistics
        """
        logger.info(f"Ingesting directory: {directory}")

        if not directory.exists():
            logger.warning(f"Directory does not exist: {directory}")
            return {"files_processed": 0, "chunks_stored": 0}

        # Find all matching files
        files = list(directory.glob(pattern))

        if not files:
            logger.warning(f"No files found matching '{pattern}' in {directory}")
            return {"files_processed": 0, "chunks_stored": 0}

        logger.info(f"Found {len(files)} files to process")

        # Process each file
        files_processed = 0
        chunks_stored = 0

        iterator = tqdm(files, desc=f"Processing {directory.name}") if show_progress else files

        for file_path in iterator:
            chunk_count = self.ingest_document(file_path)
            if chunk_count > 0:
                files_processed += 1
                chunks_stored += chunk_count

        return {
            "files_processed": files_processed,
            "chunks_stored": chunks_stored
        }

    def ingest_all_documents(self, show_progress: bool = True) -> Dict:
        """
        Ingest all documents from all configured directories.

        Args:
            show_progress: Whether to show progress bars

        Returns:
            Dictionary with complete ingestion statistics
        """
        logger.info("=" * 60)
        logger.info("Starting full document ingestion")
        logger.info("=" * 60)

        # Reset statistics
        self.stats = {
            "documents_processed": 0,
            "chunks_created": 0,
            "chunks_stored": 0,
            "errors": []
        }

        directories = {
            "synthetic_docs": SYNTHETIC_DOCS_DIR,
            "anchor_document": ANCHOR_DOC_DIR,
            "regulations": REGULATIONS_DIR,
        }

        results = {}

        for dir_name, dir_path in directories.items():
            logger.info(f"\nProcessing {dir_name}...")
            result = self.ingest_directory(dir_path, show_progress=show_progress)
            results[dir_name] = result

        # Final statistics
        logger.info("\n" + "=" * 60)
        logger.info("Ingestion Complete!")
        logger.info("=" * 60)
        logger.info(f"Total documents processed: {self.stats['documents_processed']}")
        logger.info(f"Total chunks created: {self.stats['chunks_created']}")
        logger.info(f"Total chunks stored: {self.stats['chunks_stored']}")

        if self.stats["errors"]:
            logger.warning(f"Errors encountered: {len(self.stats['errors'])}")
            for error in self.stats["errors"]:
                logger.warning(f"  - {error}")

        return {
            "summary": self.stats,
            "by_directory": results
        }

    def get_collection_info(self) -> Dict:
        """
        Get information about the current collection.

        Returns:
            Dictionary with collection statistics
        """
        return {
            "name": self.collection.name,
            "count": self.collection.count(),
            "metadata": self.collection.metadata,
        }

    def clear_collection(self):
        """
        Clear all documents from the collection (WARNING: destructive).
        """
        logger.warning(f"Clearing collection '{self.collection_name}'")
        try:
            self.vector_store.client.delete_collection(name=self.collection_name)
            logger.info(f"Deleted collection '{self.collection_name}'")
            self._setup_collection()
            logger.info(f"Recreated empty collection '{self.collection_name}'")
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")
            raise

    def query_sample(self, query_text: str, n_results: int = 3) -> Dict:
        """
        Run a sample query to test the ingested data.

        Args:
            query_text: Query string
            n_results: Number of results to return

        Returns:
            Query results dictionary
        """
        logger.info(f"Running sample query: '{query_text}'")

        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

        logger.info(f"Query returned {len(results['ids'][0])} results")
        return results


def main():
    """
    Main function to run complete ingestion pipeline.
    """
    print("=" * 60)
    print("AutoDoc AI - Document Ingestion Pipeline")
    print("=" * 60)
    print()

    # Initialize pipeline
    print("1. Initializing ingestion pipeline...")
    pipeline = DocumentIngestionPipeline(
        chunk_size=500,
        chunk_overlap=50,
        embedding_model="all-MiniLM-L6-v2"
    )
    print("   [OK] Pipeline initialized")
    print()

    # Check initial collection state
    print("2. Checking collection state...")
    initial_info = pipeline.get_collection_info()
    print(f"   - Collection: {initial_info['name']}")
    print(f"   - Current document count: {initial_info['count']}")
    print()

    # Ask user if they want to clear existing data
    if initial_info['count'] > 0:
        print(f"   WARNING: Collection already contains {initial_info['count']} documents")
        response = input("   Clear existing data? (yes/no): ").strip().lower()
        if response == 'yes':
            pipeline.clear_collection()
            print("   [OK] Collection cleared")
        else:
            print("   [OK] Keeping existing data (may create duplicates)")
        print()

    # Ingest all documents
    print("3. Ingesting all documents...")
    print()
    results = pipeline.ingest_all_documents(show_progress=True)
    print()

    # Display results
    print("4. Ingestion Results:")
    print(f"   Total documents: {results['summary']['documents_processed']}")
    print(f"   Total chunks: {results['summary']['chunks_stored']}")
    print()

    print("   By directory:")
    for dir_name, dir_stats in results['by_directory'].items():
        print(f"   - {dir_name}: {dir_stats['files_processed']} files, {dir_stats['chunks_stored']} chunks")
    print()

    # Final collection info
    print("5. Final Collection Statistics:")
    final_info = pipeline.get_collection_info()
    print(f"   - Collection: {final_info['name']}")
    print(f"   - Total documents: {final_info['count']}")
    print(f"   - Metadata: {final_info['metadata']}")
    print()

    # Run sample queries
    print("6. Testing retrieval with sample queries...")
    print()

    sample_queries = [
        "frequency model poisson regression",
        "XGBoost model SHAP explainability",
        "NAIC Model Audit Rule requirements"
    ]

    for query in sample_queries:
        print(f"   Query: '{query}'")
        results = pipeline.query_sample(query, n_results=2)

        for i, doc_id in enumerate(results['ids'][0]):
            distance = results['distances'][0][i]
            metadata = results['metadatas'][0][i]
            text_preview = results['documents'][0][i][:100]

            print(f"     Result {i+1}:")
            print(f"     - Distance: {distance:.4f}")
            print(f"     - Source: {metadata.get('filename', 'N/A')}")
            print(f"     - Section: {metadata.get('section', 'N/A')}")
            print(f"     - Text: {text_preview}...")
            print()

    print("=" * 60)
    print("[OK] Document Ingestion Complete!")
    print("=" * 60)
    print()
    print("Next Steps:")
    print("  1. Test retrieval pipeline: python rag/retrieval.py")
    print("  2. Build specialized agents: see agents/ directory")
    print("  3. Create agent orchestration system")
    print()


if __name__ == "__main__":
    main()
