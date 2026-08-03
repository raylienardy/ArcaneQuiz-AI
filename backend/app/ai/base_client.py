from abc import ABC, abstractmethod
from .models import AIRequest, AIResponse

class BaseAIClient(ABC):
    """Abstract interface for all AI providers."""

    @abstractmethod
    async def initialize(self) -> None:
        """Setup API keys, connections, etc."""
        pass

    @abstractmethod
    async def generate(self, request: AIRequest) -> AIResponse:
        """Generate content based on the request."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Return True if the provider is reachable."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Cleanup resources."""
        pass