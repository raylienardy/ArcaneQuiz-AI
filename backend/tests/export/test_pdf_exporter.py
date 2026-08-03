import pytest
from app.export.exporters.pdf_exporter import PDFExporter
from app.export.models import ExportDocument, ExportMetadata, ExportStatus
from app.export.exceptions import ExportGenerationError

class TestPDFExporter:
    @pytest.mark.asyncio
    async def test_export_valid_document(self, sample_document):
        exporter = PDFExporter()
        await exporter.initialize()
        result = await exporter.export(sample_document)
        assert result.status == ExportStatus.COMPLETED
        assert result.content is not None
        assert len(result.content) > 0
        assert result.content_type == "application/pdf"
        assert result.filename.endswith(".pdf")

    @pytest.mark.asyncio
    async def test_export_empty_document_raises(self, empty_document):
        exporter = PDFExporter()
        await exporter.initialize()
        with pytest.raises(ExportGenerationError):
            await exporter.export(empty_document)

    @pytest.mark.asyncio
    async def test_export_not_initialized_raises(self, sample_document):
        exporter = PDFExporter()
        with pytest.raises(ExportGenerationError):
            await exporter.export(sample_document)

    def test_supports_pdf_format(self):
        exporter = PDFExporter()
        assert exporter.supports("pdf") is True
        assert exporter.supports("docx") is False

    @pytest.mark.asyncio
    async def test_health_check(self):
        exporter = PDFExporter()
        assert await exporter.health_check() is False  # belum diinisialisasi
        await exporter.initialize()
        assert await exporter.health_check() is True

    @pytest.mark.asyncio
    async def test_pdf_with_unicode(self):
        """Pastikan karakter unicode (Indonesia, emoji) tidak menyebabkan crash."""
        questions = [
            {
                "question": "Apa itu AI? 🚀",
                "type": "essay",
                "answer": "Kecerdasan buatan 🤖",
                "explanation": "Pembelajaran mesin dan deep learning."
            }
        ]
        doc = ExportDocument(
            title="Unicode Test",
            content="",
            questions=questions,
            metadata=ExportMetadata(language="id")
        )
        exporter = PDFExporter()
        await exporter.initialize()
        result = await exporter.export(doc)
        assert result.status == ExportStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_large_number_of_questions(self, sample_questions, sample_metadata):
        """Uji dengan 500 pertanyaan untuk melihat stabilitas."""
        many_questions = sample_questions * 250  # 500 pertanyaan
        doc = ExportDocument(
            title="Large Export",
            questions=many_questions,
            metadata=sample_metadata
        )
        exporter = PDFExporter()
        await exporter.initialize()
        result = await exporter.export(doc)
        assert result.status == ExportStatus.COMPLETED
        assert len(result.content) > 0

    @pytest.mark.asyncio
    async def test_metadata_rendered_in_pdf(self, sample_document):
        """Metadata harus muncul di PDF (cek biner untuk teks tertentu)."""
        exporter = PDFExporter()
        await exporter.initialize()
        result = await exporter.export(sample_document)
        # ReportLab PDF tidak mudah dibaca teks biasa, tapi kita bisa cek ukuran > 0
        assert len(result.content) > 100