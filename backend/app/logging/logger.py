import logging
import time
from typing import Optional, Dict, Any
from .context import GenerationContext
from . import events

logger = logging.getLogger("openquiz.generation")
# Konfigurasi handler jika belum ada; bisa juga diatur di main.py.
# Untuk sekarang kita asumsikan handler sudah terpasang.

def _base_event(event: str, ctx: GenerationContext, extra: Optional[Dict[str, Any]] = None) -> dict:
    """Buat base payload untuk event log."""
    payload = {
        "event": event,
        "request_id": ctx.request_id,
        "session_id": ctx.session_id,
        "provider": ctx.provider,
        "model": ctx.model,
        "prompt_version": ctx.prompt_version,
        "schema_version": ctx.schema_version,
        "status": "success",
    }
    if extra:
        payload.update(extra)
    return payload

def log_generation_started(ctx: GenerationContext) -> None:
    payload = _base_event(events.GENERATION_STARTED, ctx, {"status": "started"})
    logger.info(payload)

def log_prompt_built(ctx: GenerationContext) -> None:
    logger.info(_base_event(events.PROMPT_BUILT, ctx))

def log_provider_selected(ctx: GenerationContext) -> None:
    logger.info(_base_event(events.PROVIDER_SELECTED, ctx))

def log_request_sent(ctx: GenerationContext) -> float:
    """Mulai mengukur waktu request, return waktu mulai dalam detik."""
    start = time.time()
    logger.info(_base_event(events.REQUEST_SENT, ctx, {"timestamp_start": start}))
    return start

def log_response_received(ctx: GenerationContext, start_time: float) -> float:
    """Catat respons diterima, hitung elapsed, dan return elapsed detik."""
    elapsed = time.time() - start_time
    logger.info(_base_event(events.RESPONSE_RECEIVED, ctx, {
        "elapsed_seconds": round(elapsed, 3)
    }))
    return elapsed

def log_json_parsed(ctx: GenerationContext) -> None:
    logger.info(_base_event(events.JSON_PARSED, ctx))

def log_validation_started(ctx: GenerationContext) -> None:
    logger.info(_base_event(events.VALIDATION_STARTED, ctx, {"status": "started"}))

def log_validation_completed(ctx: GenerationContext, success: bool, errors: Optional[list] = None) -> None:
    payload = _base_event(events.VALIDATION_COMPLETED, ctx, {
        "status": "passed" if success else "failed",
    })
    if errors:
        payload["errors"] = errors
    logger.info(payload)

def log_generation_completed(ctx: GenerationContext, question_count: int, total_elapsed: float) -> None:
    logger.info(_base_event(events.GENERATION_COMPLETED, ctx, {
        "generated_questions": question_count,
        "elapsed_seconds": round(total_elapsed, 3),
        "status": "completed"
    }))

def log_generation_failed(ctx: GenerationContext, error: str, error_type: Optional[str] = None) -> None:
    logger.error(_base_event(events.GENERATION_FAILED, ctx, {
        "status": "failure",
        "error": error,
        "error_type": error_type or "Unknown",
    }))