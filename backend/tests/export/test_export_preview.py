import pytest
from app.export.preview_builder import ExportPreviewBuilder
from app.export.models import ExportFormat, ExportMetadata, ExportDocument  # <-- tambahkan ExportDocument
from app.export.preview import ExportPreview

class TestExportPreview:
    def test_build_preview_pdf(self, sample_questions, sample_metadata):
        builder = ExportPreviewBuilder()
        from app.export.models import ExportDocument
        doc = ExportDocument(
            title="Test",
            questions=sample_questions,
            metadata=sample_metadata,
        )
        preview = builder.build(doc, ExportFormat.PDF)
        assert isinstance(preview, ExportPreview)
        assert preview.format == ExportFormat.PDF
        assert preview.question_count == 2
        assert preview.estimated_pages > 0
        assert preview.filename.endswith(".pdf")

    def test_build_preview_empty_questions(self):
        builder = ExportPreviewBuilder()
        doc = ExportDocument(            # Sekarang ExportDocument sudah dikenal
            title="Empty",
            questions=[],
            metadata=ExportMetadata()
        )
        preview = builder.build(doc, ExportFormat.PDF)
        assert preview.question_count == 0
        assert preview.estimated_pages == 1

    def test_warnings_for_large_document(self, sample_questions, sample_metadata):
        builder = ExportPreviewBuilder()
        # 2 pertanyaan × 120 = 240 pertanyaan → 120 halaman (asumsi 2 per halaman)
        many_questions = sample_questions * 120
        doc = ExportDocument(
            title="Large",
            questions=many_questions,
            metadata=sample_metadata,
        )
        preview = builder.build(doc, ExportFormat.PDF)
        assert any("Large document" in w for w in preview.warnings)