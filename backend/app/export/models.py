from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum

class ExportFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    MARKDOWN = "markdown"
    HTML = "html"
    CSV = "csv"
    MOODLE_XML = "moodle_xml"
    JSON = "json"
    ZIP = "zip"

class ExportStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class TokenUsage(BaseModel):
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

class ExportMetadata(BaseModel):
    generated_at: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    generation_time: Optional[float] = None
    prompt_version: Optional[str] = None
    schema_version: Optional[str] = None
    question_count: Optional[int] = None
    language: Optional[str] = None
    difficulty: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    export_format: Optional[str] = None
    formatter_name: Optional[str] = None
    formatter_version: Optional[str] = None
    application_version: Optional[str] = "1.0.0"
    generation_status: Optional[str] = None  # completed, failed, partial
    token_usage: Optional[TokenUsage] = None
    provider_latency: Optional[float] = None
    additional: Dict[str, Any] = Field(default_factory=dict)

class ExportDocument(BaseModel):
    """Dokumen standar yang akan diekspor oleh pengekspor."""
    title: str = ""
    content: str = ""                     # Konten utama (untuk plain/markdown)
    questions: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: ExportMetadata = Field(default_factory=ExportMetadata)
    raw_data: Optional[Dict[str, Any]] = None
    # Untuk rich formatter: daftar bagian (section) dan footer opsional
    sections: Optional[List[Dict[str, Any]]] = None
    footer: Optional[str] = None

class ExportRequest(BaseModel):
    format: ExportFormat
    document: ExportDocument
    options: Dict[str, Any] = Field(default_factory=dict)

class ExportResult(BaseModel):
    status: ExportStatus = ExportStatus.COMPLETED
    format: ExportFormat
    content: Optional[bytes] = None
    content_type: Optional[str] = None
    filename: Optional[str] = None
    errors: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ExportResponse(BaseModel):
    success: bool
    message: str
    result: Optional[ExportResult] = None