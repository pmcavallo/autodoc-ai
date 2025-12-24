"""
Document Chunking Strategy for AutoDoc AI RAG System

This module implements intelligent chunking of insurance model documentation
into semantically meaningful chunks suitable for vector embedding and retrieval.

Key Features:
- Respects markdown section boundaries (headers)
- Target chunk size: 500 tokens with 50-token overlap
- Preserves metadata from YAML frontmatter
- Maintains document context in chunk metadata

Usage:
    from rag.chunks.chunking_strategy import DocumentChunker

    chunker = DocumentChunker(chunk_size=500, overlap=50)
    chunks = chunker.chunk_document(file_path)
"""

import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import yaml
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Approximate tokens per character (rough estimate: 1 token ≈ 4 characters)
CHARS_PER_TOKEN = 4


class DocumentChunk:
    """
    Represents a single chunk of a document with metadata.
    """

    def __init__(
        self,
        text: str,
        metadata: Dict,
        chunk_id: str,
        start_char: int,
        end_char: int
    ):
        """
        Initialize a document chunk.

        Args:
            text: The chunk text content
            metadata: Metadata dict containing document info
            chunk_id: Unique identifier for this chunk
            start_char: Starting character position in original document
            end_char: Ending character position in original document
        """
        self.text = text
        self.metadata = metadata
        self.chunk_id = chunk_id
        self.start_char = start_char
        self.end_char = end_char

    def __repr__(self):
        return f"DocumentChunk(id={self.chunk_id}, tokens≈{len(self.text)//CHARS_PER_TOKEN}, section={self.metadata.get('section', 'N/A')})"


class DocumentChunker:
    """
    Intelligent document chunker that respects semantic boundaries.

    This chunker:
    1. Parses YAML frontmatter for document metadata
    2. Identifies markdown sections (headers)
    3. Creates chunks that respect section boundaries
    4. Maintains overlap between chunks for context continuity
    5. Enriches each chunk with metadata for filtering during retrieval
    """

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
        min_chunk_size: int = 100
    ):
        """
        Initialize the document chunker.

        Args:
            chunk_size: Target chunk size in tokens (default: 500)
            overlap: Number of overlapping tokens between chunks (default: 50)
            min_chunk_size: Minimum chunk size in tokens to avoid tiny chunks (default: 100)
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.min_chunk_size = min_chunk_size

        # Convert token sizes to character estimates
        self.chunk_size_chars = chunk_size * CHARS_PER_TOKEN
        self.overlap_chars = overlap * CHARS_PER_TOKEN
        self.min_chunk_size_chars = min_chunk_size * CHARS_PER_TOKEN

        logger.info(f"Initialized DocumentChunker: chunk_size={chunk_size} tokens, overlap={overlap} tokens")

    def parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """
        Extract YAML frontmatter from markdown document.

        Args:
            content: Full document content

        Returns:
            Tuple of (metadata_dict, content_without_frontmatter)
        """
        metadata = {}

        # Check for YAML frontmatter (--- at start, --- at end)
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(frontmatter_pattern, content, re.DOTALL)

        if match:
            try:
                yaml_content = match.group(1)
                metadata = yaml.safe_load(yaml_content)
                # Remove frontmatter from content
                content = content[match.end():]
                logger.debug(f"Parsed frontmatter: {metadata}")
            except yaml.YAMLError as e:
                logger.warning(f"Failed to parse YAML frontmatter: {e}")

        return metadata, content

    def extract_sections(self, content: str) -> List[Dict]:
        """
        Extract markdown sections based on headers.

        Args:
            content: Document content (without frontmatter)

        Returns:
            List of section dicts with 'title', 'level', 'text', 'start', 'end'
        """
        sections = []

        # Find all headers (# Header, ## Header, etc.)
        header_pattern = r'^(#{1,6})\s+(.+)$'

        lines = content.split('\n')
        current_section = None
        current_text = []
        char_position = 0

        for line in lines:
            line_length = len(line) + 1  # +1 for newline

            header_match = re.match(header_pattern, line)

            if header_match:
                # Save previous section if exists
                if current_section is not None:
                    current_section['text'] = '\n'.join(current_text)
                    current_section['end'] = char_position
                    sections.append(current_section)

                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2).strip()

                current_section = {
                    'title': title,
                    'level': level,
                    'start': char_position,
                    'text': '',
                    'end': 0
                }
                current_text = [line]
            else:
                # Add line to current section
                if current_section is not None:
                    current_text.append(line)
                else:
                    # Content before first header
                    if not sections:
                        current_section = {
                            'title': 'Introduction',
                            'level': 0,
                            'start': 0,
                            'text': '',
                            'end': 0
                        }
                        current_text = [line]

            char_position += line_length

        # Save final section
        if current_section is not None:
            current_section['text'] = '\n'.join(current_text)
            current_section['end'] = char_position
            sections.append(current_section)

        logger.debug(f"Extracted {len(sections)} sections")
        return sections

    def chunk_text(self, text: str, start_offset: int = 0) -> List[Tuple[str, int, int]]:
        """
        Split text into chunks with overlap.

        Args:
            text: Text to chunk
            start_offset: Character offset in original document

        Returns:
            List of tuples (chunk_text, start_char, end_char)
        """
        chunks = []
        text_length = len(text)

        if text_length <= self.chunk_size_chars:
            # Text fits in one chunk
            return [(text, start_offset, start_offset + text_length)]

        start = 0
        while start < text_length:
            end = start + self.chunk_size_chars

            # Try to break at sentence boundary if possible
            if end < text_length:
                # Look for sentence endings within last 20% of chunk
                search_start = int(end * 0.8)
                search_text = text[search_start:end]

                # Find last sentence ending (., !, ?, or newline)
                last_sentence = max(
                    search_text.rfind('. '),
                    search_text.rfind('.\n'),
                    search_text.rfind('! '),
                    search_text.rfind('? '),
                    search_text.rfind('\n\n')
                )

                if last_sentence != -1:
                    end = search_start + last_sentence + 1

            chunk_text = text[start:end].strip()

            # Skip very small chunks at the end
            if len(chunk_text) >= self.min_chunk_size_chars or start == 0:
                chunks.append((
                    chunk_text,
                    start_offset + start,
                    start_offset + end
                ))

            # Move start position with overlap
            start = end - self.overlap_chars

            # Prevent infinite loop
            if start <= chunks[-1][1] - start_offset:
                start = chunks[-1][2] - start_offset

        return chunks

    def chunk_document(self, file_path: Path) -> List[DocumentChunk]:
        """
        Chunk a complete document into semantically meaningful chunks.

        Args:
            file_path: Path to markdown document

        Returns:
            List of DocumentChunk objects
        """
        logger.info(f"Chunking document: {file_path}")

        # Read document
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse frontmatter
        doc_metadata, content = self.parse_frontmatter(content)

        # Add document-level metadata
        doc_metadata['source_file'] = str(file_path)
        doc_metadata['filename'] = file_path.name

        # Extract sections
        sections = self.extract_sections(content)

        # Create chunks
        all_chunks = []
        chunk_counter = 0

        for section in sections:
            section_text = section['text']

            # Skip empty sections
            if not section_text.strip():
                continue

            # Chunk the section text
            text_chunks = self.chunk_text(section_text, section['start'])

            for chunk_text, start_char, end_char in text_chunks:
                # Create chunk metadata
                chunk_metadata = doc_metadata.copy()
                chunk_metadata.update({
                    'section': section['title'],
                    'section_level': section['level'],
                    'chunk_index': chunk_counter,
                    'char_start': start_char,
                    'char_end': end_char,
                })

                # Create chunk ID
                doc_id = file_path.stem  # filename without extension
                chunk_id = f"{doc_id}_chunk_{chunk_counter:03d}"

                # Create DocumentChunk object
                chunk = DocumentChunk(
                    text=chunk_text,
                    metadata=chunk_metadata,
                    chunk_id=chunk_id,
                    start_char=start_char,
                    end_char=end_char
                )

                all_chunks.append(chunk)
                chunk_counter += 1

        logger.info(f"Created {len(all_chunks)} chunks from {file_path.name}")
        return all_chunks

    def chunk_directory(
        self,
        directory: Path,
        pattern: str = "*.md"
    ) -> List[DocumentChunk]:
        """
        Chunk all documents in a directory.

        Args:
            directory: Path to directory containing documents
            pattern: Glob pattern for files to chunk (default: "*.md")

        Returns:
            List of all DocumentChunk objects from all files
        """
        logger.info(f"Chunking directory: {directory} (pattern: {pattern})")

        all_chunks = []
        files = list(directory.glob(pattern))

        if not files:
            logger.warning(f"No files found matching pattern '{pattern}' in {directory}")
            return all_chunks

        for file_path in files:
            try:
                chunks = self.chunk_document(file_path)
                all_chunks.extend(chunks)
            except Exception as e:
                logger.error(f"Error chunking {file_path}: {e}")

        logger.info(f"Total chunks created: {len(all_chunks)} from {len(files)} documents")
        return all_chunks


def main():
    """
    Test function for document chunking.
    """
    print("=" * 60)
    print("AutoDoc AI - Document Chunking Test")
    print("=" * 60)
    print()

    # Setup paths
    project_root = Path(__file__).parent.parent.parent
    synthetic_docs = project_root / "data" / "synthetic_docs"

    # Initialize chunker
    print("1. Initializing DocumentChunker...")
    chunker = DocumentChunker(chunk_size=500, overlap=50)
    print(f"   ✓ Chunk size: {chunker.chunk_size} tokens (~{chunker.chunk_size_chars} chars)")
    print(f"   ✓ Overlap: {chunker.overlap} tokens (~{chunker.overlap_chars} chars)")
    print()

    # Test on a single document
    test_files = list(synthetic_docs.glob("*.md"))
    if not test_files:
        print("   ✗ No markdown files found in data/synthetic_docs/")
        return

    test_file = test_files[0]
    print(f"2. Testing on: {test_file.name}")

    chunks = chunker.chunk_document(test_file)
    print(f"   ✓ Created {len(chunks)} chunks")
    print()

    # Display sample chunks
    print("3. Sample Chunks:")
    for i, chunk in enumerate(chunks[:3]):
        print(f"   Chunk {i+1}:")
        print(f"   - ID: {chunk.chunk_id}")
        print(f"   - Section: {chunk.metadata.get('section', 'N/A')}")
        print(f"   - Size: ~{len(chunk.text) // CHARS_PER_TOKEN} tokens")
        print(f"   - Metadata keys: {list(chunk.metadata.keys())}")
        print(f"   - Text preview: {chunk.text[:150]}...")
        print()

    # Test directory chunking
    print("4. Testing directory chunking...")
    all_chunks = chunker.chunk_directory(synthetic_docs)
    print(f"   ✓ Total chunks from all documents: {len(all_chunks)}")
    print()

    # Statistics
    print("5. Chunking Statistics:")
    chunk_sizes = [len(c.text) // CHARS_PER_TOKEN for c in all_chunks]
    print(f"   - Total documents: {len(test_files)}")
    print(f"   - Total chunks: {len(all_chunks)}")
    print(f"   - Avg chunk size: ~{sum(chunk_sizes) // len(chunk_sizes)} tokens")
    print(f"   - Min chunk size: ~{min(chunk_sizes)} tokens")
    print(f"   - Max chunk size: ~{max(chunk_sizes)} tokens")
    print()

    print("=" * 60)
    print("✓ Chunking Strategy Implementation Complete!")
    print("=" * 60)
    print()
    print("Next Steps:")
    print("  1. Implement embeddings.py for sentence-transformers")
    print("  2. Implement ingestion.py to load chunks into ChromaDB")
    print()


if __name__ == "__main__":
    main()
