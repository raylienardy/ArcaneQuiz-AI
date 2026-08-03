from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class AIRequest:
    """Generic AI request, reusable across providers."""
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 1000
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AIResponse:
    """Generic AI response."""
    response_text: str = ""
    provider: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None