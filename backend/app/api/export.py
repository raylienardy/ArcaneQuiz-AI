from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from ..services.export_service import ExportService
from ..export.models import ExportFormat, ExportMetadata
from ..export.preview_builder import ExportPreviewBuilder
from ..export.preview import ExportPreview
from ..export.session_manager import get_session_manager
from ..export.registry import get_export_registry
from ..export.exceptions import ExporterNotFound

router = APIRouter(prefix="/export", tags=["Export"])

@router.post("/preview")
async def export_preview(request: dict):
    questions = request.get("questions", [])
    if not questions:
        raise HTTPException(status_code=400, detail="No questions provided.")

    fmt_str = request.get("format", "pdf").upper()
    if fmt_str not in ExportFormat.__members__:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {fmt_str}")
    fmt = ExportFormat[fmt_str]
    metadata_dict = request.get("metadata", {})
    metadata = ExportMetadata(**metadata_dict)

    service = ExportService()
    formatter_name = "rich" if fmt == ExportFormat.PDF else "markdown"
    document = await service.formatter_registry.get(formatter_name).format(
        questions, metadata, title="Generated Questions"
    )

    from ..export.preview_builder import ExportPreviewBuilder
    builder = ExportPreviewBuilder()
    preview = builder.build(document, fmt)

    return preview.model_dump()
  
@router.post("/download")
async def download_export(request: dict):
    questions = request.get("questions", [])
    if not questions:
        raise HTTPException(status_code=400, detail="No questions provided")

    fmt_str = request.get("format", "pdf").upper()
    if fmt_str not in ExportFormat.__members__:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {fmt_str}")
    fmt = ExportFormat[fmt_str]

    metadata_dict = request.get("metadata", {})
    metadata = ExportMetadata(**metadata_dict)

    service = ExportService()
    formatter_name = "rich" if fmt == ExportFormat.PDF else "markdown"
    document = await service.formatter_registry.get(formatter_name).format(
        questions, metadata, title="Generated Questions"
    )

    try:
        exporter = service.export_registry.get_exporter(fmt.value)
        await exporter.initialize()                    # ← TAMBAHKAN BARIS INI
        result = await exporter.export(document)
    except ExporterNotFound:
        raise HTTPException(status_code=400, detail="Exporter not available")
    finally:
        # Tutup exporter setelah selesai (jika ada resource)
        if 'exporter' in locals():
            await exporter.close()

    return Response(
        content=result.content,
        media_type=result.content_type or "application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{result.filename}"'}
    )