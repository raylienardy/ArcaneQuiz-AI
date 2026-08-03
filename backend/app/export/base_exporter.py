from abc import ABC, abstractmethod
from typing import Any
from .models import ExportDocument, ExportResult

class BaseExporter(ABC):
    """Antarmuka abstrak untuk semua pengekspor dokumen."""

    @abstractmethod
    async def initialize(self) -> None:
        """Siapkan resource yang diperlukan (misal, font, template)."""
        ...

    @abstractmethod
    async def export(self, document: ExportDocument) -> ExportResult:
        """Ekspor dokumen ke format target."""
        ...

    @abstractmethod
    def supports(self, format: str) -> bool:
        """Periksa apakah format didukung oleh pengekspor ini."""
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Periksa apakah pengekspor siap digunakan."""
        ...

    @abstractmethod
    async def close(self) -> None:
        """Bersihkan resource."""
        ...