import pytest
from unittest.mock import AsyncMock
from app.services.export_service import ExportService
from app.export.models import (
    ExportRequest, ExportFormat, ExportDocument, ExportMetadata, ExportResult, ExportStatus
)

class TestExportService:
    @pytest.mark.asyncio
    async def test_export_with_registered_exporter(self, sample_document, clean_export_registry):
        service = ExportService()
        dummy = AsyncMock()
        dummy.initialize.return_value = None
        dummy.export.return_value = ExportResult(
            status=ExportStatus.COMPLETED,
            format=ExportFormat.CSV,   # Harus sesuai dengan yang didaftarkan
            content=b"csv data",
            content_type="text/csv",
            filename="test.csv",
        )
        dummy.close.return_value = None
        service.export_registry.register("csv", dummy)

        request = ExportRequest(
            format=ExportFormat.CSV,
            document=sample_document,
        )
        response = await service.export(request)
        assert response.success is True
        assert response.result.format == ExportFormat.CSV

    @pytest.mark.asyncio
    async def test_export_unregistered_format(self, sample_document, clean_export_registry):
        service = ExportService()
        request = ExportRequest(
            format=ExportFormat.DOCX,
            document=sample_document,
        )
        response = await service.export(request)
        assert response.success is False
        assert "No exporter" in response.message

    @pytest.mark.asyncio
    async def test_format_and_export(self, sample_questions, sample_metadata, clean_export_registry):
        service = ExportService()
        from app.export.formatters import PlainFormatter
        service.formatter_registry.register("plain", PlainFormatter())

        dummy = AsyncMock()
        dummy.initialize.return_value = None
        dummy.export.return_value = ExportResult(
            status=ExportStatus.COMPLETED,
            format=ExportFormat.MARKDOWN,
            content=b"markdown",
            content_type="text/markdown",
            filename="test.md",
        )
        dummy.close.return_value = None
        service.export_registry.register("markdown", dummy)

        response = await service.format_and_export(
            questions=sample_questions,
            metadata=sample_metadata,
            format="markdown",
            formatter_name="plain",
            title="My Questions",
        )
        assert response.success is True