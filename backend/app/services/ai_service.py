import logging
from ..ai.models import AIRequest, AIResponse
from ..ai.providers import get_provider_registry
from ..ai.exceptions import (
    AIAuthenticationError,
    AIConnectionError,
    AIRateLimitError,
)

logger = logging.getLogger(__name__)


class AIService:
    """Service layer untuk generasi AI dengan fallback ke 5 API key Telkom LLM."""

    def __init__(self):
        self.provider_names = [f"telkom{i}" for i in range(1, 6)]

    async def initialize(self) -> None:
        """Dummy initialize untuk kompatibilitas dengan QuestionService."""
        pass

    async def generate(self, request: AIRequest) -> AIResponse:
        """Mencoba generate melalui semua provider secara berurutan."""
        last_error = None

        for provider_name in self.provider_names:
            try:
                client = get_provider_registry().get_client(provider_name)
                await client.initialize()
                response = await client.generate(request)
                logger.info(f"Successfully generated using {provider_name}.")
                return response
            except (AIRateLimitError, AIConnectionError, AIAuthenticationError) as e:
                logger.warning(f"Provider {provider_name} failed: {str(e)}. Trying next...")
                last_error = e
                continue
            except Exception as e:
                logger.error(f"Provider {provider_name} unexpected error: {str(e)}")
                raise

        raise AIRateLimitError(
            f"All Telkom LLM API keys have been exhausted. Last error: {str(last_error)}"
        )