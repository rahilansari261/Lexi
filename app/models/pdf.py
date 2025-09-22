"""
PDF-related models
"""
from typing import Optional
from pydantic import BaseModel, Field

class PDFUploadRequest(BaseModel):
    """PDF upload request model"""
    case_number: str = Field(description="Case number")
    base64_data: str = Field(description="Base64 encoded PDF data")
    filename: Optional[str] = Field(default=None, description="Custom filename (optional)")

class PDFUploadResponse(BaseModel):
    """PDF upload response model"""
    success: bool = Field(description="Upload success status")
    case_number: str = Field(description="Case number")
    document_link: str = Field(description="Download URL for the PDF")
    filename: str = Field(description="Stored filename")
    message: str = Field(description="Response message")
