from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ExtractionResult:
    """Standardized output from any document extractor."""
    text: str = ""
    file_type: str = ""
    character_count: int = 0
    word_count: int = 0
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)   # tambahan: menyimpan info seperti page_count