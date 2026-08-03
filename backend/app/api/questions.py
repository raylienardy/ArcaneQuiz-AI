from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import JSONResponse
from ..question_generator.models import QuestionRequest
from ..services.question_service import QuestionService
import json
from ..question_generator.exceptions import (
    QuestionParserError,
    QuestionFormatError,
    QuestionGenerationError,
    QuestionValidationError,
)
from ..ai.exceptions import (
    AIAuthenticationError,
    AIConnectionError,
    AIRateLimitError,
    AIResponseError,
    AITimeoutError,
    ProviderNotSupportedError,
)

router = APIRouter(prefix="/questions", tags=["Question Generation"])

@router.post("/generate")
async def generate_questions(request: QuestionRequest, debug: bool = Query(False)):
    question_service = QuestionService()
    try:
        result = await question_service.generate_questions(request, debug=debug)
    except (QuestionParserError, QuestionFormatError, QuestionValidationError) as e:
        status_code = 422
        detail = str(e)
        return _build_response(False, detail, question_service.debug_info if debug else None, status_code)
    except QuestionGenerationError as e:
        status_code = 500
        detail = str(e)
        return _build_response(False, detail, question_service.debug_info if debug else None, status_code)
    except AIAuthenticationError as e:
        status_code = 401
        detail = str(e)
        return _build_response(False, detail, question_service.debug_info if debug else None, status_code)
    except AIRateLimitError as e:
        status_code = 429
        detail = str(e)
        return _build_response(False, detail, question_service.debug_info if debug else None, status_code)
    except AITimeoutError as e:
        status_code = 504
        detail = str(e)
        return _build_response(False, detail, question_service.debug_info if debug else None, status_code)
    except (AIConnectionError, AIResponseError) as e:
        status_code = 502
        detail = str(e)
        return _build_response(False, detail, question_service.debug_info if debug else None, status_code)
    except ProviderNotSupportedError as e:
        status_code = 400
        detail = str(e)
        return _build_response(False, detail, question_service.debug_info if debug else None, status_code)
    except Exception as e:
        status_code = 500
        detail = f"Internal error: {str(e)}"
        return _build_response(False, detail, question_service.debug_info if debug else None, status_code)

    response_data = {
        "success": True,
        "message": "Questions generated successfully.",
        "data": {
            "questions": result.questions,
        },
        "metadata": {
            "provider": result.provider,
            "model": result.model,
            "latency_seconds": result.generation_time,
            "prompt_version": result.metadata.get("prompt_version"),
            "schema_version": result.metadata.get("schema_version"),
            "generation_timestamp": result.metadata.get("generation_timestamp"),
            "token_usage": result.metadata.get("token_usage"),
            "finish_reason": result.metadata.get("finish_reason"),
        },
    }
    if debug:
        response_data["debug"] = question_service.debug_info
        # opsional: prompt juga ditambahkan jika diminta (tapi debug_info sudah ada prompt)
    if debug and question_service._last_prompt:
        response_data["prompt"] = question_service._last_prompt  # redundansi yang aman

    return response_data

def _build_response(success: bool, message: str, debug_data: dict = None, status_code: int = 200):
    body = {
        "success": success,
        "message": message,
    }
    if debug_data:
        # Konversi set ke list agar bisa di-serialize JSON
        body["debug"] = _make_json_safe(debug_data)
    return JSONResponse(content=body, status_code=status_code)

def _make_json_safe(obj):
    """Rekursif mengubah set menjadi list."""
    if isinstance(obj, dict):
        return {k: _make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_make_json_safe(v) for v in obj]
    elif isinstance(obj, set):
        return list(obj)
    else:
        return obj