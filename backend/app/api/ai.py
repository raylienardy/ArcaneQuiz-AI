from fastapi import APIRouter, HTTPException
from ..services.ai_service import AIService
from ..ai.models import AIRequest
from ..ai.exceptions import (
    AIAuthenticationError,
    AIConnectionError,
    AIRateLimitError,
    AIResponseError,
    AITimeoutError,
    ProviderNotSupportedError,
)

router = APIRouter(prefix="/ai", tags=["AI Testing"])

@router.get("/test")
async def test_gemini_connection():
    ai_service = AIService()  # menggunakan AI_PROVIDER dari settings

    try:
        await ai_service.initialize()
    except AIAuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except AIConnectionError as e:
        raise HTTPException(status_code=500, detail=str(e))

    test_request = AIRequest(
        prompt="Reply only with the word: CONNECTED",
        temperature=0.0,
        max_tokens=10,
    )

    try:
        response = await ai_service.generate(test_request)
    except AIAuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except AIRateLimitError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except AITimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))
    except (AIConnectionError, AIResponseError) as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ProviderNotSupportedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    return {
        "success": True,
        "provider": response.provider,
        "model": response.metadata.get("model", "unknown"),
        "response": response.response_text,
    }