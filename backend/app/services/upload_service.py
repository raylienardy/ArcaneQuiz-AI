"""
Service layer for handling file uploads.
"""

from fastapi import UploadFile
from ..utils.file_validator import validate_uploaded_file


class UploadError(Exception):
    """Custom exception to carry error message and status code."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def handle_upload(file: UploadFile) -> dict:
    """
    Validate the uploaded file and return metadata.

    Args:
        file: The uploaded file.

    Returns:
        dict: Metadata (filename, content_type, size) if valid.

    Raises:
        UploadError: If validation fails.
    """
    error_message = validate_uploaded_file(file)

    if error_message:
        # Tentukan status code
        if "No file" in error_message or "empty" in error_message:
            status_code = 400
        elif "Unsupported" in error_message:
            status_code = 415
        elif "exceeds" in error_message:
            status_code = 413
        else:
            status_code = 400
        raise UploadError(error_message, status_code)

    filename = file.filename
    content_type = file.content_type or "application/octet-stream"
    size = file.size if file.size is not None else 0

    return {
        "filename": filename,
        "content_type": content_type,
        "size": size,
    }