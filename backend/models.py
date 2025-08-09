from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ExtractedField(BaseModel):
    field_name: str
    value: str
    confidence: float = Field(ge=0.0, le=1.0)
    bounding_box: Optional[List[float]] = None
    page_number: int

class PageData(BaseModel):
    page_number: int
    extracted_fields: List[ExtractedField]
    page_image_url: Optional[str] = None
    text_content: Optional[str] = None
    processing_time: Optional[float] = None

class DocumentResponse(BaseModel):
    doc_id: str
    filename: str
    total_pages: int
    key_fields: List[str]
    pages: List[PageData]
    processing_status: str = "completed"
    created_at: datetime = Field(default_factory=datetime.now)
    total_processing_time: Optional[float] = None

class UploadRequest(BaseModel):
    key_fields: List[str] = Field(..., min_items=1, description="List of fields to extract")

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = "1.0.0"
