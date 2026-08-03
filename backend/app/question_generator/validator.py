from abc import ABC, abstractmethod
from .models import QuestionResponse

class BaseValidator(ABC):
    """Validator untuk QuestionResponse."""

    @abstractmethod
    def validate(self, response: QuestionResponse) -> bool:
        """
        Memeriksa apakah respons valid (jumlah pertanyaan, pilihan, dll.).
        Return True jika lolos validasi.
        """
        pass