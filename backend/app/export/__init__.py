from .base_exporter import BaseExporter
from .models import (
    ExportRequest, ExportResponse, ExportDocument, ExportFormat, ExportStatus, ExportResult, ExportMetadata,
)
from .exceptions import (
    ExportError, ExportInitializationError, ExportValidationError, ExportGenerationError,
    ExportFormatError, ExportPermissionError, ExportConfigurationError, ExportTimeoutError,
    ExporterNotFound, UnsupportedExportFormat, DuplicateExporterRegistration, InvalidExporter,
)
from .registry import ExportRegistry, FormatterRegistry, get_export_registry, get_formatter_registry
from .formatter import QuestionToDocumentFormatter
from .formatters import PlainFormatter, MarkdownFormatter, RichFormatter
from .exporters.pdf_exporter import PDFExporter
from .registry import get_formatter_registry

# Daftarkan PDFExporter saat modul diimpor pertama kali
_registry = get_export_registry()
if not _registry.supports("pdf"):
    _registry.register("pdf", PDFExporter())
    

_formatter_reg = get_formatter_registry()
if "plain" not in _formatter_reg.list_formatters():
    _formatter_reg.register("plain", PlainFormatter())
if "markdown" not in _formatter_reg.list_formatters():
    _formatter_reg.register("markdown", MarkdownFormatter())
if "rich" not in _formatter_reg.list_formatters():
    _formatter_reg.register("rich", RichFormatter())