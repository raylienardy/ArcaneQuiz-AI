"""
File validation utilities using centralized settings.
"""
from pathlib import Path
from ..config import get_settings


def validate_uploaded_file(file) -> str | None:
    """
    Validate the uploaded file against allowed extensions, size, and emptiness.

    Args:
        file: FastAPI UploadFile object.

    Returns:
        str | None: Error message if invalid, otherwise None.
    """
    settings = get_settings()

    # 1. Missing file
    if not file or not file.filename:
        return "No file uploaded."

    # 2. Unsupported extension
    ext = Path(file.filename).suffix.lower()
    if ext not in settings.allowed_extensions:
        allowed = ", ".join(settings.allowed_extensions)
        return f"Unsupported file type '{ext}'. Allowed types: {allowed}."

    # 3. Empty file (check size if available, otherwise assume content will be read later)
    # FastAPI's UploadFile has .size attribute; if None, we cannot determine yet.
    if file.size is not None and file.size == 0:
        return "Uploaded file is empty."

    # 4. File size exceeds maximum
    if file.size is not None and file.size > settings.max_upload_size:
        max_mb = settings.max_upload_size / (1024 * 1024)
        return f"File exceeds the maximum upload size ({max_mb:.0f} MB)."

    return None