"""
Model untuk sesi ekspor.
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from .models import ExportFormat, ExportMetadata

class SessionStatus(str, Enum):
    CREATED = "created"
    PREVIEW_READY = "preview_ready"
    DOWNLOAD_STARTED = "download_started"
    DOWNLOAD_COMPLETED = "download_completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    CLOSED = "closed"

class ExportSession(BaseModel):
    """Mewakili satu siklus hidup ekspor."""
    session_id: str = Field(..., description="ID unik sesi")
    correlation_id: Optional[str] = Field(None, description="ID korelasi dengan request")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: Optional[str] = None
    closed_at: Optional[str] = None
    status: SessionStatus = SessionStatus.CREATED
    export_format: ExportFormat = ExportFormat.PDF
    provider: Optional[str] = None
    model: Optional[str] = None
    question_count: Optional[int] = None
    language: Optional[str] = None
    difficulty: Optional[str] = None
    generated_filename: Optional[str] = None
    estimated_size: Optional[int] = None
    estimated_pages: Optional[int] = None
    download_started_at: Optional[str] = None
    download_completed_at: Optional[str] = None
    generation_time: Optional[float] = None
    export_duration: Optional[float] = None
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    metadata: ExportMetadata = Field(default_factory=ExportMetadata)
    preview_available: bool = False
    download_available: bool = False