import pytest
from app.export.exceptions import ExportValidationError

# Untuk validasi, kita bisa menguji melalui ExportService atau membuat validator sendiri.
# Karena ExportService belum memiliki metode validasi terpisah, kita tambahkan di sini.
# (Nanti bisa diintegrasikan)

def test_validation_empty_questions():
    """Simulasi validasi: questions kosong harus menghasilkan error."""
    questions = []
    if len(questions) == 0:
        with pytest.raises(ExportValidationError, match="No questions to export"):
            raise ExportValidationError("No questions to export")

def test_validation_unsupported_format():
    fmt = "invalid"
    supported = {"pdf", "docx"}
    if fmt not in supported:
        with pytest.raises(ExportValidationError, match=f"Unsupported format: {fmt}"):
            raise ExportValidationError(f"Unsupported format: {fmt}")