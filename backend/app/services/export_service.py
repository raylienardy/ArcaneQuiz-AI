import logging
from typing import Optional, List, Dict, Any
from ..export.registry import get_export_registry, get_formatter_registry
from ..export.models import (
    ExportRequest,
    ExportResponse,
    ExportResult,
    ExportStatus,
    ExportDocument,
    ExportMetadata,
)
from ..export.exceptions import ExportError, ExporterNotFound

logger = logging.getLogger(__name__)

class ExportService:
    def __init__(self):
        self.export_registry = get_export_registry()
        self.formatter_registry = get_formatter_registry()

    async def export(self, request: ExportRequest) -> ExportResponse:
        """Ekspor dokumen menggunakan exporter yang sesuai."""
        try:
            exporter = self.export_registry.get_exporter(request.format.value)
        except ExporterNotFound as e:
            return ExportResponse(
                success=False,
                message=str(e),
            )

        try:
            await exporter.initialize()
        except Exception as e:
            return ExportResponse(
                success=False,
                message=f"Failed to initialize exporter: {str(e)}",
            )

        try:
            result = await exporter.export(request.document)
            return ExportResponse(
                success=True,
                message="Export completed successfully.",
                result=result,
            )
        except Exception as e:
            return ExportResponse(
                success=False,
                message=f"Export failed: {str(e)}",
            )
        finally:
            await exporter.close()

    async def format_and_export(
        self,
        questions: List[Dict[str, Any]],
        metadata: ExportMetadata,
        format: str,
        formatter_name: str = "plain",
        title: str = "Generated Questions",
        options: Optional[Dict[str, Any]] = None,
    ) -> ExportResponse:
        """Format pertanyaan lalu ekspor."""
        try:
            formatter = self.formatter_registry.get(formatter_name)
        except KeyError:
            return ExportResponse(
                success=False,
                message=f"No formatter registered for '{formatter_name}'",
            )

        document = await formatter.format(questions, metadata, title)

        export_request = ExportRequest(
            format=format,
            document=document,
            options=options or {},
        )

        return await self.export(export_request)