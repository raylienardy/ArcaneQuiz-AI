import uuid
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class GenerationContext:
    """Menyimpan identitas untuk korelasi log."""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    prompt_version: Optional[str] = None
    schema_version: Optional[str] = None