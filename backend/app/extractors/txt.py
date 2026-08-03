from fastapi import UploadFile
from .base import BaseExtractor
from .models import ExtractionResult

class TXTExtractor(BaseExtractor):
    ENCODINGS = ["utf-8", "utf-8-sig", "latin-1"]

    async def extract(self, file: UploadFile) -> ExtractionResult:
        warnings = []
        file_type = "txt"

        # Baca byte
        try:
            raw_bytes = await file.read()
        except Exception as e:
            return ExtractionResult(
                file_type=file_type,
                warnings=[f"Failed to read file: {str(e)}"]
            )

        if not raw_bytes:
            return ExtractionResult(
                file_type=file_type,
                warnings=["File is empty."]
            )

        # Decode dengan fallback encoding
        decoded = None
        used_encoding = None
        for enc in self.ENCODINGS:
            try:
                decoded = raw_bytes.decode(enc)
                used_encoding = enc
                break
            except (UnicodeDecodeError, LookupError):
                continue

        if decoded is None:
            return ExtractionResult(
                file_type=file_type,
                warnings=["Unable to decode file with supported encodings."]
            )

        if used_encoding != "utf-8":
            warnings.append(f"File decoded using {used_encoding} instead of UTF-8.")

        # Hanya mengembalikan teks mentah dan peringatan
        return ExtractionResult(
            text=decoded,
            file_type=file_type,
            warnings=warnings
        )