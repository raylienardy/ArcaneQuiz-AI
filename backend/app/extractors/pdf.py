"""
PDF Extractor using pypdf library.
Extracts text from text-based PDFs, handles various error conditions gracefully.
"""

from fastapi import UploadFile
from .base import BaseExtractor
from .models import ExtractionResult
import io

try:
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError, DependencyError
except ImportError:
    PdfReader = None

class PDFExtractor(BaseExtractor):
    """Extract text from PDF files using pypdf."""

    async def extract(self, file: UploadFile) -> ExtractionResult:
        file_type = "pdf"
        warnings = []
        metadata = {}
        text = ""

        # Baca konten file
        try:
            content = await file.read()
        except Exception as e:
            return ExtractionResult(
                file_type=file_type,
                warnings=[f"Failed to read file: {str(e)}"]
            )

        if not content:
            return ExtractionResult(
                file_type=file_type,
                warnings=["File is empty."]
            )

        # Buka PDF dari stream memori
        try:
            pdf_file = io.BytesIO(content)
            reader = PdfReader(pdf_file)
        except PdfReadError as e:
            # Terkadang file terenkripsi atau rusak
            return ExtractionResult(
                file_type=file_type,
                warnings=[f"Cannot read PDF: {str(e)}. It may be encrypted or corrupted."]
            )
        except Exception as e:
            return ExtractionResult(
                file_type=file_type,
                warnings=[f"Unexpected error opening PDF: {str(e)}"]
            )

        # Cek apakah PDF terenkripsi (terproteksi kata sandi)
        if reader.is_encrypted:
            return ExtractionResult(
                file_type=file_type,
                warnings=["PDF is encrypted. Unable to extract text."]
            )

        # Ambil metadata halaman jika tersedia
        try:
            num_pages = len(reader.pages)
            metadata["page_count"] = num_pages
        except Exception:
            num_pages = 0
            warnings.append("Could not determine page count.")

        if num_pages == 0:
            return ExtractionResult(
                file_type=file_type,
                warnings=["PDF contains no pages."],
                metadata=metadata
            )

        # Ekstraksi teks halaman demi halaman
        extracted_pages = []
        empty_pages = 0
        for i, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    extracted_pages.append(page_text.strip())
                else:
                    empty_pages += 1
            except Exception as e:
                warnings.append(f"Failed to extract text from page {i}: {str(e)}")
                continue

        if empty_pages > 0:
            warnings.append(f"{empty_pages} page(s) were empty or contained no extractable text.")

        # Gabungkan halaman dengan pemisah newline ganda
        text = "\n\n".join(extracted_pages)

        # Jika tidak ada teks sama sekali, mungkin PDF berbasis gambar
        if not text.strip():
            warnings.append("No text could be extracted. The PDF may be image-based or contain only scanned images.")

        return ExtractionResult(
            text=text,
            file_type=file_type,
            warnings=warnings,
            metadata=metadata
        )