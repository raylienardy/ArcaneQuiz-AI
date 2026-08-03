"""
Membangun ExportPreview dari ExportDocument.
"""

import math
from datetime import datetime, timezone
from .models import ExportDocument, ExportFormat
from .preview import ExportPreview

# Rata-rata byte per halaman untuk estimasi (asumsi A4, font 11, margin standar)
AVERAGE_BYTES_PER_PAGE = 3500
AVERAGE_QUESTIONS_PER_PAGE = 2  # Estimasi kasar: 2 pertanyaan per halaman

class ExportPreviewBuilder:
    """Membangun pratinjau ekspor tanpa menghasilkan file final."""

    def build(self, document: ExportDocument, fmt: ExportFormat) -> ExportPreview:
        """
        Bangun ExportPreview dari ExportDocument.
        """
        # Estimasi jumlah halaman
        question_count = len(document.questions) if document.questions else 0
        if question_count > 0:
            estimated_pages = max(1, math.ceil(question_count / AVERAGE_QUESTIONS_PER_PAGE))
        else:
            # Jika tidak ada pertanyaan (misal rich document tanpa questions), estimasi dari konten
            content_length = len(document.content) if document.content else 0
            estimated_pages = max(1, math.ceil(content_length / AVERAGE_BYTES_PER_PAGE))

        # Estimasi ukuran file (rough)
        estimated_size = estimated_pages * AVERAGE_BYTES_PER_PAGE

        # Format ukuran manusia
        if estimated_size < 1024:
            size_human = f"{estimated_size} B"
        elif estimated_size < 1024 * 1024:
            size_human = f"{estimated_size / 1024:.0f} KB"
        else:
            size_human = f"{estimated_size / (1024 * 1024):.1f} MB"

        # Nama file default
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        base_name = f"OpenQuizAI_Questions"
        if document.metadata.language:
            base_name += f"_{document.metadata.language.upper()}"
        if document.metadata.difficulty:
            base_name += f"_{document.metadata.difficulty.capitalize()}"
        filename = f"{base_name}_{timestamp}.{fmt.value}"

        # Warnings
        warnings = []
        if estimated_pages > 100:
            warnings.append(f"Large document: estimated {estimated_pages} pages.")
        if estimated_size > 10 * 1024 * 1024:  # > 10 MB
            warnings.append(f"Large file: estimated {size_human}.")
        if not document.metadata.provider:
            warnings.append("Provider metadata unavailable.")

        # Capabilities (informasi untuk frontend tentang apa yang didukung ekspor ini)
        capabilities = {
            "has_footer": True,
            "has_metadata": True,
            "supports_unicode": True,
        }

        return ExportPreview(
            filename=filename,
            format=fmt,
            estimated_size=estimated_size,
            estimated_size_human=size_human,
            estimated_pages=estimated_pages,
            question_count=question_count,
            metadata=document.metadata,
            warnings=warnings,
            capabilities=capabilities,
            download_endpoint="/api/export/download",  # Placeholder, bisa disesuaikan
            preview_timestamp=datetime.now(timezone.utc).isoformat(),
        )