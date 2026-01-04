"""
Document management API endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
import tempfile
import os
from datetime import datetime

from src.api.models.schemas import (
    DocumentUploadResponse,
    DocumentListResponse,
    DocumentInfo,
    ErrorResponse
)
from src.core.rag_engine import RAGEngine
from src.connectors.document_loader import DocumentLoader
from src.utils.logger import get_logger
from src.api.routes.chat import get_rag_engine

logger = get_logger(__name__)
router = APIRouter(prefix="/api/documents", tags=["documents"])

# Allowed file extensions
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx"}


@router.post("/upload", response_model=DocumentUploadResponse, responses={400: {"model": ErrorResponse}})
async def upload_document(
    file: UploadFile = File(..., description="Document file to upload (PDF, DOCX, or TXT)"),
    rag_engine: RAGEngine = Depends(get_rag_engine)
):
    """
    Upload a document to the knowledge base

    - **file**: Document file (PDF, DOCX, or TXT format)

    The document will be chunked and added to the vector database.
    """
    try:
        # Validate file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        logger.info(f"Uploading document: {file.filename}")

        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            # Load and process document
            loader = DocumentLoader()
            chunks = loader.load_document(tmp_path, filename=file.filename)

            # Add to RAG engine
            metadatas = [{
                "source": file.filename,
                "uploaded_at": datetime.now().isoformat(),
                "chunk_index": i
            } for i in range(len(chunks))]

            rag_engine.add_documents(chunks, metadatas=metadatas)

            logger.info(f"Document uploaded: {file.filename} ({len(chunks)} chunks)")

            return DocumentUploadResponse(
                message="Document uploaded successfully",
                filename=file.filename,
                num_chunks=len(chunks)
            )

        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading document: {str(e)}"
        )


@router.get("", response_model=DocumentListResponse)
async def list_documents(rag_engine: RAGEngine = Depends(get_rag_engine)):
    """
    List all documents in the knowledge base

    Returns list of documents with metadata.
    """
    try:
        # Get document count from vector store
        total_docs = rag_engine.vector_store.count()

        # For now, return basic info
        # TODO: Implement proper document tracking in database
        response = DocumentListResponse(
            documents=[],
            total=total_docs
        )

        logger.info(f"Listed {total_docs} documents")
        return response

    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing documents: {str(e)}"
        )


@router.delete("/{document_id}")
async def delete_document(document_id: str, rag_engine: RAGEngine = Depends(get_rag_engine)):
    """
    Delete a document from the knowledge base

    - **document_id**: Document ID to delete

    NOTE: Full document deletion requires implementing document tracking.
    Currently resets entire database.
    """
    try:
        # TODO: Implement proper document deletion by ID
        # For now, we can only reset the entire database
        logger.warning(f"Document deletion requested for ID: {document_id}")
        raise HTTPException(
            status_code=501,
            detail="Document deletion by ID not yet implemented. Use database reset instead."
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting document: {str(e)}"
        )


@router.post("/reset")
async def reset_database(rag_engine: RAGEngine = Depends(get_rag_engine)):
    """
    Reset the entire document database

    **WARNING**: This will delete ALL documents from the knowledge base!
    """
    try:
        logger.warning("Database reset requested")
        rag_engine.vector_store.reset()
        rag_engine.clear_history()

        logger.info("Database reset complete")
        return {"message": "Database reset successfully", "total_documents": 0}

    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error resetting database: {str(e)}"
        )
