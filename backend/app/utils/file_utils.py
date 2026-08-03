"""
File validation utilities.
"""

from pathlib import Path

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


def validate_file(file) -> None:
    """
    Validate the uploaded file against allowed extensions and maximum size.

    Args:
        file: FastAPI UploadFile object.

    Raises:
        ValueError: If the file fails validation (missing name, unsupported type, too large).
    """
    if not file.filename:
        raise ValueError("No file selected.")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{ext}'. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    if file.size is not None and file.size > MAX_FILE_SIZE:
        raise ValueError(
            f"File size ({file.size} bytes) exceeds the maximum limit of 20 MB."
        )