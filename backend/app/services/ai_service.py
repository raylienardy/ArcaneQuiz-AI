import logging
from ..ai.models import AIRequest, AIResponse
from ..ai.providers import get_provider_registry
from ..config import get_settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        settings = get_settings()
        self.provider_name = settings.ai_provider
        self.client = get_provider_registry().get_client(self.provider_name)
        logger.info(f"Selected AI provider: {self.provider_name}")

    async def initialize(self) -> None:
        await self.client.initialize()
        logger.info(f"AI provider '{self.provider_name}' initialized and ready.")

    async def generate(self, request: AIRequest) -> AIResponse:
        if not self.client._initialized:  # <-- gunakan flag
            await self.initialize()
        return await self.client.generate(request)