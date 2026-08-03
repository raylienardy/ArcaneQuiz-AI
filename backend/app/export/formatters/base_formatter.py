from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..models import ExportDocument, ExportMetadata

class BaseFormatter(ABC):
    """Antarmuka abstrak untuk semua formatter dokumen."""

    @abstractmethod
    async def format(self, questions: List[Dict[str, Any]], metadata: ExportMetadata,
                     title: str = "Generated Questions") -> ExportDocument:
        """Ubah pertanyaan dan metadata menjadi ExportDocument."""
        ...

    @abstractmethod
    def supports(self, format_name: str) -> bool:
        """Periksa apakah formatter mendukung format tertentu (plain, markdown, rich)."""
        ...

    @abstractmethod
    def description(self) -> str:
        """Deskripsi singkat formatter."""
        ...