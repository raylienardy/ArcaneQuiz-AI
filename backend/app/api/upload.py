from fastapi import APIRouter, File, UploadFile
from ..services.upload_service import handle_upload, UploadError
from ..services.extraction_service import ExtractionService
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 1. Validasi file dan dapatkan metadata
    try:
        file_info = handle_upload(file)
    except UploadError as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "message": e.message,
                "errors": {"detail": e.message},
            },
        )

    # 2. Ekstraksi teks
    extraction_service = ExtractionService()
    try:
        extraction_result = await extraction_service.extract(file)
    except Exception as e:
        # Jika ekstraksi gagal, tetap kembalikan metadata + peringatan
        return {
            "success": True,
            "message": "File uploaded, but text extraction failed.",
            "data": {
                **file_info,
                "text": "",
                "character_count": 0,
                "word_count": 0,
                "warnings": [f"Extraction error: {str(e)}"],
                "metadata": {}
            }
        }

    # 3. Gabungkan metadata file + hasil ekstraksi
    return {
        "success": True,
        "message": "File uploaded and processed successfully.",
        "data": {
            **file_info,
            "text": extraction_result.text,
            "character_count": extraction_result.character_count,
            "word_count": extraction_result.word_count,
            "warnings": extraction_result.warnings,
            "metadata": extraction_result.metadata,
        }
    }