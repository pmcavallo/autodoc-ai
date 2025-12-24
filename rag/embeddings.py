"""
Embedding Generation for AutoDoc AI RAG System

This module provides embedding functionality using sentence-transformers
for converting text chunks into dense vector representations suitable for
semantic search in ChromaDB.

Key Features:
- Uses sentence-transformers for high-quality embeddings
- Default model: all-MiniLM-L6-v2 (lightweight, fast, good quality)
- Batch processing for efficient embedding generation
- Caching support to avoid re-embedding unchanged documents
- GPU acceleration when available

Usage:
    from rag.embeddings import EmbeddingGenerator

    generator = EmbeddingGenerator()
    embeddings = generator.embed_texts(["text1", "text2"])
"""

from sentence_transformers import SentenceTransformer
from typing import List, Optional, Union
import numpy as np
import torch
import logging
from pathlib import Path
import hashlib
import pickle

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
CACHE_DIR = PROJECT_ROOT / ".embedding_cache"


class EmbeddingGenerator:
    """
    Manages text embedding generation using sentence-transformers.

    This class provides a high-level interface for:
    - Loading pre-trained embedding models
    - Generating embeddings for single texts or batches
    - Caching embeddings to avoid redundant computation
    - Utilizing GPU when available for faster processing
    """

    # Default model: all-MiniLM-L6-v2
    # - 384 dimensions
    # - 22M parameters
    # - Fast inference (~3000 sentences/sec on CPU)
    # - Good quality for semantic search
    DEFAULT_MODEL = "all-MiniLM-L6-v2"

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        device: Optional[str] = None,
        use_cache: bool = True,
        batch_size: int = 32
    ):
        """
        Initialize the embedding generator.

        Args:
            model_name: Name of sentence-transformers model to use
            device: Device to use ('cuda', 'cpu', or None for auto-detect)
            use_cache: Whether to cache embeddings to disk
            batch_size: Batch size for embedding generation
        """
        self.model_name = model_name
        self.batch_size = batch_size
        self.use_cache = use_cache

        # Determine device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        # Load model
        logger.info(f"Loading embedding model: {model_name}")
        logger.info(f"Using device: {self.device}")

        try:
            self.model = SentenceTransformer(model_name, device=self.device)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            logger.info(f"Model loaded successfully. Embedding dimension: {self.embedding_dim}")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            raise

        # Setup cache directory
        if self.use_cache:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"Embedding cache enabled at: {CACHE_DIR}")

    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.

        Args:
            text: Input text string

        Returns:
            Numpy array of shape (embedding_dim,)
        """
        return self.embed_texts([text])[0]

    def embed_texts(
        self,
        texts: List[str],
        show_progress: bool = False,
        normalize: bool = True
    ) -> np.ndarray:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of input text strings
            show_progress: Whether to show progress bar
            normalize: Whether to normalize embeddings to unit length (recommended for cosine similarity)

        Returns:
            Numpy array of shape (len(texts), embedding_dim)
        """
        if not texts:
            logger.warning("Empty text list provided for embedding")
            return np.array([])

        logger.info(f"Generating embeddings for {len(texts)} texts")

        try:
            # Generate embeddings
            embeddings = self.model.encode(
                texts,
                batch_size=self.batch_size,
                show_progress_bar=show_progress,
                convert_to_numpy=True,
                normalize_embeddings=normalize
            )

            logger.info(f"Generated embeddings: shape {embeddings.shape}")
            return embeddings

        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    def embed_with_cache(
        self,
        text: str,
        cache_key: Optional[str] = None
    ) -> np.ndarray:
        """
        Generate embedding with caching support.

        Args:
            text: Input text string
            cache_key: Optional cache key (defaults to hash of text)

        Returns:
            Numpy array of shape (embedding_dim,)
        """
        if not self.use_cache:
            return self.embed_text(text)

        # Generate cache key from text hash if not provided
        if cache_key is None:
            cache_key = hashlib.md5(text.encode()).hexdigest()

        cache_file = CACHE_DIR / f"{self.model_name}_{cache_key}.pkl"

        # Check cache
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    embedding = pickle.load(f)
                logger.debug(f"Loaded embedding from cache: {cache_key}")
                return embedding
            except Exception as e:
                logger.warning(f"Failed to load cached embedding: {e}")

        # Generate and cache embedding
        embedding = self.embed_text(text)

        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(embedding, f)
            logger.debug(f"Cached embedding: {cache_key}")
        except Exception as e:
            logger.warning(f"Failed to cache embedding: {e}")

        return embedding

    def get_similarity(
        self,
        text1: str,
        text2: str,
        metric: str = "cosine"
    ) -> float:
        """
        Calculate similarity between two texts.

        Args:
            text1: First text
            text2: Second text
            metric: Similarity metric ('cosine' or 'dot')

        Returns:
            Similarity score (0-1 for cosine, unbounded for dot product)
        """
        emb1 = self.embed_text(text1)
        emb2 = self.embed_text(text2)

        if metric == "cosine":
            # Cosine similarity (assumes normalized embeddings)
            similarity = np.dot(emb1, emb2)
        elif metric == "dot":
            # Dot product similarity
            similarity = np.dot(emb1, emb2)
        else:
            raise ValueError(f"Unknown metric: {metric}")

        return float(similarity)

    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.

        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "embedding_dim": self.embedding_dim,
            "device": self.device,
            "max_seq_length": self.model.max_seq_length,
            "batch_size": self.batch_size,
            "cache_enabled": self.use_cache,
        }


class ChromaDBEmbeddingFunction:
    """
    Custom embedding function for ChromaDB integration.

    ChromaDB expects an embedding function with a specific interface.
    This class wraps our EmbeddingGenerator to work seamlessly with ChromaDB.
    """

    def __init__(
        self,
        model_name: str = EmbeddingGenerator.DEFAULT_MODEL,
        device: Optional[str] = None
    ):
        """
        Initialize ChromaDB-compatible embedding function.

        Args:
            model_name: Name of sentence-transformers model
            device: Device to use ('cuda', 'cpu', or None)
        """
        self._model_name = model_name
        self.generator = EmbeddingGenerator(
            model_name=model_name,
            device=device,
            use_cache=False  # ChromaDB handles its own caching
        )

    def name(self) -> str:
        """Return the name of this embedding function (required by ChromaDB)."""
        return f"sentence-transformers-{self._model_name}"

    def __call__(self, input: List[str]) -> List[List[float]]:
        """
        Generate embeddings for ChromaDB (for adding documents).

        Args:
            input: List of texts to embed (ChromaDB v1.1+ uses 'input' parameter)

        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        embeddings = self.generator.embed_texts(input, normalize=True)
        # Convert to list of lists for ChromaDB
        return embeddings.tolist()

    def embed_query(self, input: List[str]) -> List[List[float]]:
        """
        Generate embeddings for ChromaDB (for queries).

        Args:
            input: List of query texts to embed

        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        # Same implementation as __call__
        return self.__call__(input)


def create_embedding_function(
    model_name: str = EmbeddingGenerator.DEFAULT_MODEL,
    device: Optional[str] = None
) -> ChromaDBEmbeddingFunction:
    """
    Convenience function to create ChromaDB-compatible embedding function.

    Args:
        model_name: Name of sentence-transformers model
        device: Device to use ('cuda', 'cpu', or None)

    Returns:
        ChromaDBEmbeddingFunction instance
    """
    return ChromaDBEmbeddingFunction(model_name=model_name, device=device)


def main():
    """
    Test function for embedding generation.
    """
    print("=" * 60)
    print("AutoDoc AI - Embedding Generation Test")
    print("=" * 60)
    print()

    # Initialize generator
    print("1. Initializing EmbeddingGenerator...")
    generator = EmbeddingGenerator()

    model_info = generator.get_model_info()
    print(f"   ✓ Model: {model_info['model_name']}")
    print(f"   ✓ Embedding dimension: {model_info['embedding_dim']}")
    print(f"   ✓ Device: {model_info['device']}")
    print(f"   ✓ Max sequence length: {model_info['max_seq_length']}")
    print()

    # Test single text embedding
    print("2. Testing single text embedding...")
    sample_text = "The frequency model uses Poisson regression with a log link function to predict claim frequency."
    embedding = generator.embed_text(sample_text)
    print(f"   ✓ Input text: '{sample_text[:60]}...'")
    print(f"   ✓ Embedding shape: {embedding.shape}")
    print(f"   ✓ Embedding norm: {np.linalg.norm(embedding):.4f}")
    print(f"   ✓ Sample values: [{embedding[0]:.4f}, {embedding[1]:.4f}, {embedding[2]:.4f}, ...]")
    print()

    # Test batch embedding
    print("3. Testing batch embedding...")
    sample_texts = [
        "The severity model uses Gamma regression to predict claim costs.",
        "Territory rating factors are based on geographic clustering analysis.",
        "The XGBoost model includes SHAP values for explainability.",
        "Validation follows a three-tier framework with holdout testing.",
        "Model governance ensures compliance with NAIC Model Audit Rule."
    ]
    embeddings = generator.embed_texts(sample_texts)
    print(f"   ✓ Generated embeddings for {len(sample_texts)} texts")
    print(f"   ✓ Embeddings shape: {embeddings.shape}")
    print()

    # Test similarity calculation
    print("4. Testing similarity calculation...")
    text1 = "GLM frequency model with Poisson distribution"
    text2 = "Poisson regression for modeling claim frequency"
    text3 = "Territory clustering using K-means algorithm"

    sim_12 = generator.get_similarity(text1, text2)
    sim_13 = generator.get_similarity(text1, text3)

    print(f"   Text 1: '{text1}'")
    print(f"   Text 2: '{text2}'")
    print(f"   Text 3: '{text3}'")
    print(f"   ✓ Similarity(1,2): {sim_12:.4f} (related texts)")
    print(f"   ✓ Similarity(1,3): {sim_13:.4f} (unrelated texts)")
    print()

    # Test ChromaDB embedding function
    print("5. Testing ChromaDB embedding function...")
    chroma_fn = create_embedding_function()
    chroma_embeddings = chroma_fn(sample_texts[:2])
    print(f"   ✓ ChromaDB function created")
    print(f"   ✓ Generated embeddings: {len(chroma_embeddings)} texts")
    print(f"   ✓ Embedding dimension: {len(chroma_embeddings[0])}")
    print()

    # Performance test
    print("6. Performance test...")
    import time
    test_texts = sample_texts * 20  # 100 texts
    start_time = time.time()
    batch_embeddings = generator.embed_texts(test_texts)
    elapsed = time.time() - start_time
    print(f"   ✓ Embedded {len(test_texts)} texts in {elapsed:.2f} seconds")
    print(f"   ✓ Speed: {len(test_texts) / elapsed:.1f} texts/second")
    print()

    print("=" * 60)
    print("✓ Embedding Generation Implementation Complete!")
    print("=" * 60)
    print()
    print("Next Steps:")
    print("  1. Implement ingestion.py to combine chunking + embeddings")
    print("  2. Load all documents into ChromaDB vector store")
    print("  3. Test end-to-end RAG retrieval pipeline")
    print()


if __name__ == "__main__":
    main()
