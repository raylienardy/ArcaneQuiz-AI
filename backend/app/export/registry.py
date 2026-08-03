import logging
from typing import Dict, List
from .base_exporter import BaseExporter
from .formatters.base_formatter import BaseFormatter

logger = logging.getLogger(__name__)

class ExportRegistry:
    """Registry pusat untuk semua pengekspor. Mengikuti pola AIProviderRegistry."""

    def __init__(self):
        self._exporters: Dict[str, BaseExporter] = {}

    def register(self, format: str, exporter: BaseExporter) -> None:
        """
        Daftarkan pengekspor untuk format tertentu.
        Lempar DuplicateExporterRegistration jika format sudah terdaftar.
        """
        fmt = format.lower()
        if fmt in self._exporters:
            from .exceptions import DuplicateExporterRegistration
            raise DuplicateExporterRegistration(
                f"Exporter for format '{fmt}' is already registered."
            )
        self._exporters[fmt] = exporter
        logger.info(f"Exporter '{exporter.__class__.__name__}' registered for format '{fmt}'.")

    def unregister(self, format: str) -> None:
        """Hapus pendaftaran pengekspor untuk format tertentu."""
        fmt = format.lower()
        if fmt in self._exporters:
            del self._exporters[fmt]
            logger.info(f"Exporter for format '{fmt}' unregistered.")

    def get_exporter(self, format: str) -> BaseExporter:
        """
        Dapatkan pengekspor berdasarkan format.
        Lempar ExporterNotFound jika tidak ada.
        """
        fmt = format.lower()
        if fmt not in self._exporters:
            from .exceptions import ExporterNotFound
            raise ExporterNotFound(f"No exporter registered for format '{fmt}'.")
        exporter = self._exporters[fmt]
        logger.info(f"Exporter '{exporter.__class__.__name__}' selected for format '{fmt}'.")
        return exporter

    def list_exporters(self) -> List[str]:
        """Kembalikan daftar format yang didukung."""
        return list(self._exporters.keys())

    def supports(self, format: str) -> bool:
        """Periksa apakah format didukung."""
        return format.lower() in self._exporters

    def available_formats(self) -> List[str]:
        """Alias untuk list_exporters()."""
        return self.list_exporters()

    # Alias untuk kompatibilitas dengan kode yang sudah ada
    def get(self, format: str) -> BaseExporter:
        """Alias untuk get_exporter()."""
        return self.get_exporter(format)


class FormatterRegistry:
    """Registry untuk formatter."""

    def __init__(self):
        self._formatters: Dict[str, BaseFormatter] = {}

    def register(self, name: str, formatter: BaseFormatter) -> None:
        self._formatters[name.lower()] = formatter

    def get(self, name: str) -> BaseFormatter:
        fmt = name.lower()
        if fmt not in self._formatters:
            raise KeyError(f"No formatter registered for '{fmt}'")
        return self._formatters[fmt]

    def list_formatters(self) -> List[str]:
        return list(self._formatters.keys())

    def supports(self, name: str) -> bool:
        return name.lower() in self._formatters


# Singleton instances
_export_registry = None
def get_export_registry() -> ExportRegistry:
    global _export_registry
    if _export_registry is None:
        _export_registry = ExportRegistry()
    return _export_registry

_formatter_registry = None
def get_formatter_registry() -> FormatterRegistry:
    global _formatter_registry
    if _formatter_registry is None:
        _formatter_registry = FormatterRegistry()
    return _formatter_registry