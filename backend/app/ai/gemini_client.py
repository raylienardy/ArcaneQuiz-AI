import logging
from typing import Optional
from google import genai
from google.genai.types import GenerateContentConfig

from .base_client import BaseAIClient
from .models import AIRequest, AIResponse
from .exceptions import (
    AIAuthenticationError,
    AIConnectionError,
    AIRateLimitError,
    AIResponseError,
    AITimeoutError,
)
from ..config import get_settings

logger = logging.getLogger(__name__)

class GeminiClient(BaseAIClient):
    def __init__(self):
        self._client: Optional[genai.Client] = None
        self._model_name: Optional[str] = None
        self._initialized = False   # <-- tambahan

    async def initialize(self) -> None:
        if self._client:
            return
        if self._initialized:
            return

        settings = get_settings()
        api_key = settings.gemini_api_key.strip()
        self._model_name = settings.gemini_model.strip()

        if not api_key:
            raise AIAuthenticationError("Gemini API key is missing. Set GEMINI_API_KEY in .env.")
        if not self._model_name:
            raise AIConnectionError("Gemini model is not configured. Set GEMINI_MODEL in .env.")

        try:
            self._client = genai.Client(api_key=api_key)
            self._initialized = True
            logger.info(f"Gemini client initialized for model '{self._model_name}'.")
        except Exception as e:
            raise AIConnectionError(f"Failed to initialize Gemini client: {str(e)}") from e

    async def generate(self, request: AIRequest) -> AIResponse:
        if not self._client:
            raise AIConnectionError("Gemini client not initialized.")

        try:
            config = GenerateContentConfig(
                temperature=request.temperature,
                max_output_tokens=request.max_tokens,
                candidate_count=1,
            )
            response = self._client.models.generate_content(
                model=self._model_name,
                contents=request.prompt,
                config=config,
            )

            response_text = ""
            if response.candidates:
                candidate = response.candidates[0]
                if candidate.content and candidate.content.parts:
                    response_text = "".join(part.text for part in candidate.content.parts if hasattr(part, 'text'))

            return AIResponse(
                response_text=response_text,
                provider="gemini",
                metadata={
                    "model": self._model_name,
                    "finish_reason": str(candidate.finish_reason) if response.candidates else None,
                },
            )
        except genai.errors.APIError as e:
            # Klasifikasi error berdasarkan pesan/kode
            error_str = str(e).lower()
            if "authentication" in error_str or "api key" in error_str:
                raise AIAuthenticationError(str(e)) from e
            elif "rate" in error_str and "limit" in error_str:
                raise AIRateLimitError(str(e)) from e
            elif "timeout" in error_str:
                raise AITimeoutError(str(e)) from e
            else:
                raise AIResponseError(str(e)) from e
        except Exception as e:
            raise AIConnectionError(f"Unexpected error: {str(e)}") from e

    async def health_check(self) -> bool:
        if not self._client:
            return False
        try:
            req = AIRequest(prompt="Ping", max_tokens=5)
            resp = await self.generate(req)
            return bool(resp.response_text)
        except Exception:
            return False

    async def close(self) -> None:
        self._client = None