"""
Model untuk pratinjau ekspor.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from .models import ExportFormat, ExportMetadata

class ExportPreview(BaseModel):
    """Informasi pratinjau sebelum ekspor."""
    filename: str = Field(..., description="Nama file yang akan dihasilkan")
    format: ExportFormat = Field(..., description="Format ekspor")
    estimated_size: Optional[int] = Field(None, description="Estimasi ukuran dalam byte")
    estimated_size_human: Optional[str] = Field(None, description="Ukuran yang dapat dibaca manusia")
    estimated_pages: Optional[int] = Field(None, description="Estimasi jumlah halaman")
    question_count: int = Field(..., description="Jumlah pertanyaan")
    metadata: ExportMetadata = Field(default_factory=ExportMetadata, description="Metadata ekspor")
    warnings: List[str] = Field(default_factory=list, description="Peringatan")
    capabilities: Dict[str, Any] = Field(default_factory=dict, description="Kemampuan ekspor")
    download_endpoint: Optional[str] = Field(None, description="Endpoint untuk mengunduh file")
    session_id: Optional[str] = Field(None, description="ID sesi ekspor terkait")   # <--- BARU
    preview_timestamp: str = Field(..., description="Timestamp pratinjau")