import asyncio
from fastapi import UploadFile
from ..extractors.factory import ExtractorFactory
from ..extractors.models import ExtractionResult
from ..text_processing.pipeline import clean_text

EXTRACTION_TIMEOUT = 30  # detik

class ExtractionService:
    async def extract(self, file: UploadFile) -> ExtractionResult:
        if not file.filename:
            raise ValueError("File has no name, cannot determine type")

        # Dapatkan extractor dari factory
        extractor = ExtractorFactory.get_extractor(file.filename)

        try:
            # Jalankan ekstraksi dengan timeout
            result = await asyncio.wait_for(
                extractor.extract(file),
                timeout=EXTRACTION_TIMEOUT
            )
        except asyncio.TimeoutError:
            # Kembalikan hasil kosong dengan peringatan
            return ExtractionResult(
                file_type="unknown",
                warnings=["Text extraction timed out. The document may be too large or complex."]
            )
        except Exception as e:
            # Error tidak terduga dari extractor
            return ExtractionResult(
                file_type="unknown",
                warnings=[f"Extraction failed: {str(e)}"]
            )

        # Bersihkan teks
        if result.text:
            result.text = clean_text(result.text)

        # Perkaya dengan statistik
        if result.text:
            result.character_count = len(result.text)
            result.word_count = len(result.text.split())
        return result