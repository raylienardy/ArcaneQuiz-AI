import pytest
from app.export.registry import ExportRegistry
from app.export.exceptions import DuplicateExporterRegistration, ExporterNotFound
from app.export.base_exporter import BaseExporter
from unittest.mock import MagicMock

class DummyExporter(BaseExporter):
    async def initialize(self): pass
    async def export(self, doc): pass
    def supports(self, fmt): return fmt == "dummy"
    async def health_check(self): return True
    async def close(self): pass

class TestExportRegistry:
    def test_register_new_exporter(self):
        registry = ExportRegistry()
        exporter = DummyExporter()
        registry.register("dummy", exporter)
        assert registry.supports("dummy")
        assert "dummy" in registry.list_exporters()

    def test_register_duplicate_raises(self):
        registry = ExportRegistry()
        registry.register("dummy", DummyExporter())
        with pytest.raises(DuplicateExporterRegistration):
            registry.register("dummy", DummyExporter())

    def test_get_exporter_success(self):
        registry = ExportRegistry()
        exporter = DummyExporter()
        registry.register("dummy", exporter)
        assert registry.get_exporter("dummy") is exporter

    def test_get_exporter_not_found_raises(self):
        registry = ExportRegistry()
        with pytest.raises(ExporterNotFound):
            registry.get_exporter("nonexistent")

    def test_unregister_exporter(self):
        registry = ExportRegistry()
        registry.register("dummy", DummyExporter())
        registry.unregister("dummy")
        assert not registry.supports("dummy")

    def test_list_exporters_initially_empty(self):
        registry = ExportRegistry()
        assert registry.list_exporters() == []

    def test_available_formats(self):
        registry = ExportRegistry()
        registry.register("pdf", DummyExporter())
        registry.register("csv", DummyExporter())
        assert set(registry.available_formats()) == {"pdf", "csv"}