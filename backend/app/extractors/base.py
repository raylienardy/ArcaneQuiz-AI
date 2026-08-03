from abc import ABC, abstractmethod
from fastapi import UploadFile
from .models import ExtractionResult

class BaseExtractor(ABC):
    """Abstract base for all document extractors."""
    
    @abstractmethod
    async def extract(self, file: UploadFile) -> ExtractionResult:
        """Extract text from a file. Must be implemented by each extractor."""
        pass