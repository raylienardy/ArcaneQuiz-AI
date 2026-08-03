from abc import ABC, abstractmethod
from .models import QuestionRequest, QuestionResponse

class BaseQuestionGenerator(ABC):
    """Interface untuk semua generator pertanyaan."""

    @abstractmethod
    async def generate(self, request: QuestionRequest) -> QuestionResponse:
        """Menghasilkan pertanyaan berdasarkan request."""
        pass

    @abstractmethod
    def build_request(self, request: QuestionRequest) -> any:
        """Membangun payload untuk provider AI. Mengembalikan objek sesuai provider."""
        pass

    @abstractmethod
    def parse_response(self, raw_response: any) -> QuestionResponse:
        """Mengurai respons mentah AI menjadi QuestionResponse."""
        pass

    @abstractmethod
    def validate_response(self, response: QuestionResponse) -> bool:
        """Memvalidasi hasil akhir. Return True jika valid."""
        pass