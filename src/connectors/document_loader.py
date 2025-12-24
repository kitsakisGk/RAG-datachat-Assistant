"""
Document loading and processing utilities
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import PyPDF2
from docx import Document
from src.utils.logger import get_logger
from src.utils.validators import FileValidator

logger = get_logger(__name__)


class DocumentChunker:
    """Chunk documents into smaller pieces for embedding"""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize document chunker

        Args:
            chunk_size: Maximum characters per chunk
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> List[str]:
        """
        Chunk text into overlapping pieces

        Args:
            text: Input text

        Returns:
            List of text chunks
        """
        if not text:
            return []

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size

            # Try to break at sentence boundary
            if end < text_length:
                # Look for period, question mark, or exclamation point
                sentence_end = max(
                    text.rfind('. ', start, end),
                    text.rfind('? ', start, end),
                    text.rfind('! ', start, end)
                )
                if sentence_end != -1:
                    end = sentence_end + 1

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            # Move start with overlap
            start = end - self.chunk_overlap if end < text_length else text_length

        logger.info(f"Created {len(chunks)} chunks from text (length: {text_length})")

        return chunks


class DocumentLoader:
    """Load and process various document formats"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize document loader

        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.chunker = DocumentChunker(chunk_size, chunk_overlap)
        self.validator = FileValidator()

    def load_text_file(self, file_path: str) -> str:
        """
        Load plain text file

        Args:
            file_path: Path to text file

        Returns:
            File contents as string
        """
        logger.info(f"Loading text file: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"Loaded {len(content)} characters from {file_path}")
            return content
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
            logger.info(f"Loaded {len(content)} characters from {file_path} (latin-1 encoding)")
            return content

    def load_pdf(self, file_path: str) -> str:
        """
        Load PDF file

        Args:
            file_path: Path to PDF file

        Returns:
            Extracted text
        """
        logger.info(f"Loading PDF file: {file_path}")

        try:
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                num_pages = len(pdf_reader.pages)

                text_parts = []
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    text_parts.append(text)

                content = "\n\n".join(text_parts)
                logger.info(f"Extracted {len(content)} characters from {num_pages} pages")
                return content

        except Exception as e:
            logger.error(f"Error loading PDF: {e}")
            raise

    def load_docx(self, file_path: str) -> str:
        """
        Load DOCX file

        Args:
            file_path: Path to DOCX file

        Returns:
            Extracted text
        """
        logger.info(f"Loading DOCX file: {file_path}")

        try:
            doc = Document(file_path)
            paragraphs = [para.text for para in doc.paragraphs]
            content = "\n\n".join(paragraphs)
            logger.info(f"Extracted {len(content)} characters from DOCX")
            return content

        except Exception as e:
            logger.error(f"Error loading DOCX: {e}")
            raise

    def load_document(self, file_path: str) -> Dict[str, Any]:
        """
        Load document and create chunks with metadata

        Args:
            file_path: Path to document

        Returns:
            Dictionary with chunks and metadata
        """
        # Validate file
        if not self.validator.validate_file_size(file_path):
            raise ValueError(f"File too large: {file_path}")

        file_extension = self.validator.get_file_extension(file_path)
        file_name = Path(file_path).name

        logger.info(f"Loading document: {file_name}")

        # Load based on file type
        if file_extension == '.pdf':
            content = self.load_pdf(file_path)
        elif file_extension == '.docx':
            content = self.load_docx(file_path)
        elif file_extension in ['.txt', '.md']:
            content = self.load_text_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        # Chunk the document
        chunks = self.chunker.chunk_text(content)

        # Create metadata for each chunk
        metadatas = [
            {
                "source": file_name,
                "file_type": file_extension,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            for i in range(len(chunks))
        ]

        return {
            "chunks": chunks,
            "metadatas": metadatas,
            "file_name": file_name,
            "file_type": file_extension,
            "total_chunks": len(chunks)
        }

    def load_multiple_documents(
        self,
        file_paths: List[str]
    ) -> Dict[str, Any]:
        """
        Load multiple documents

        Args:
            file_paths: List of file paths

        Returns:
            Dictionary with all chunks and metadata
        """
        all_chunks = []
        all_metadatas = []

        for file_path in file_paths:
            try:
                doc_data = self.load_document(file_path)
                all_chunks.extend(doc_data["chunks"])
                all_metadatas.extend(doc_data["metadatas"])
            except Exception as e:
                logger.error(f"Failed to load {file_path}: {e}")
                continue

        logger.info(f"Loaded {len(all_chunks)} chunks from {len(file_paths)} documents")

        return {
            "chunks": all_chunks,
            "metadatas": all_metadatas,
            "num_documents": len(file_paths),
            "total_chunks": len(all_chunks)
        }


__all__ = ["DocumentLoader", "DocumentChunker"]
