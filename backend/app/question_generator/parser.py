from abc import ABC, abstractmethod
from typing import Any
from .models import QuestionResponse

class BaseParser(ABC):
    """Parser untuk mengubah respons mentah AI menjadi QuestionResponse."""

    @abstractmethod
    def parse(self, raw: Any) -> QuestionResponse:
        pass