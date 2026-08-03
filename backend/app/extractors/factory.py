from pathlib import Path
from .base import BaseExtractor
from .pdf import PDFExtractor
from .docx import DOCXExtractor
from .txt import TXTExtractor

class ExtractorFactory:
    """Memilih extractor berdasarkan ekstensi file."""
    
    _extractors = {
        ".pdf": PDFExtractor,
        ".docx": DOCXExtractor,
        ".txt": TXTExtractor,
    }
    
    @classmethod
    def get_extractor(cls, filename: str) -> BaseExtractor:
        ext = Path(filename).suffix.lower()
        extractor_class = cls._extractors.get(ext)
        if not extractor_class:
            raise ValueError(f"No extractor for extension '{ext}'")
        return extractor_class()
    
    @classmethod
    def register_extractor(cls, extension: str, extractor_class: type):
        """Metode untuk menambah extractor baru tanpa memodifikasi kode yang sudah ada."""
        cls._extractors[extension.lower()] = extractor_class