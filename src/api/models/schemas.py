"""
Pydantic models for API request/response validation
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str = Field(..., min_length=1, max_length=1000, description="User question")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What was the total revenue in Q4 2025?",
                "session_id": "user-123"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str = Field(..., description="Generated answer")
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="Source documents used")
    num_sources: int = Field(..., description="Number of source documents")
    session_id: Optional[str] = Field(None, description="Session ID")

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "The total revenue in Q4 2025 was $2.5 million.",
                "sources": [
                    {
                        "content": "Q4 2025 Sales Report...",
                        "metadata": {"source": "sample_sales_data.txt"}
                    }
                ],
                "num_sources": 1,
                "session_id": "user-123"
            }
        }


class DocumentUploadResponse(BaseModel):
    """Response model for document upload"""
    message: str = Field(..., description="Upload status message")
    filename: str = Field(..., description="Uploaded filename")
    num_chunks: int = Field(..., description="Number of chunks created")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Document uploaded successfully",
                "filename": "sales_report.pdf",
                "num_chunks": 15
            }
        }


class DocumentInfo(BaseModel):
    """Document information model"""
    id: str = Field(..., description="Document ID")
    filename: str = Field(..., description="Document filename")
    num_chunks: int = Field(..., description="Number of chunks")
    uploaded_at: str = Field(..., description="Upload timestamp")


class DocumentListResponse(BaseModel):
    """Response model for document list"""
    documents: List[DocumentInfo] = Field(default_factory=list, description="List of documents")
    total: int = Field(..., description="Total number of documents")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    ollama_available: bool = Field(..., description="Ollama service status")


class MetricsResponse(BaseModel):
    """Metrics response"""
    total_documents: int = Field(..., description="Total documents in database")
    total_queries: int = Field(0, description="Total queries processed")
    avg_response_time: float = Field(0.0, description="Average response time (seconds)")
    uptime: float = Field(..., description="Service uptime (seconds)")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Document upload failed",
                "detail": "Unsupported file type: .exe"
            }
        }
