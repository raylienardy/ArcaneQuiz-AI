class ExportError(Exception):
    """Kesalahan dasar untuk modul ekspor."""
    pass

class ExportInitializationError(ExportError):
    """Gagal menginisialisasi pengekspor."""
    pass

class ExportValidationError(ExportError):
    """Data yang akan diekspor tidak valid."""
    pass

class ExportGenerationError(ExportError):
    """Gagal menghasilkan file ekspor."""
    pass

class ExportFormatError(ExportError):
    """Format ekspor tidak didukung."""
    pass

class ExportPermissionError(ExportError):
    """Izin menulis file ditolak."""
    pass

class ExportConfigurationError(ExportError):
    """Konfigurasi ekspor salah."""
    pass

class ExportTimeoutError(ExportError):
    """Proses ekspor melebihi batas waktu."""
    pass

class ExporterNotFound(ExportError):
    """Pengekspor untuk format yang diminta tidak ditemukan."""
    pass

class UnsupportedExportFormat(ExportError):
    """Format ekspor tidak didukung oleh sistem."""
    pass

class DuplicateExporterRegistration(ExportError):
    """Pengekspor sudah terdaftar untuk format yang sama."""
    pass

class InvalidExporter(ExportError):
    """Pengekspor tidak valid (tidak mengimplementasikan BaseExporter)."""
    pass

class RegistryInitializationError(ExportError):
    """Kesalahan saat inisialisasi registry."""
    pass