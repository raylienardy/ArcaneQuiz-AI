"""
Parser untuk mengubah respons teks AI menjadi QuestionResponse.
Menangani pembersihan markdown, ekstraksi JSON, dan konversi ke model Pydantic.
"""

import json
import re
import logging
from typing import List, Union, Dict, Any
from .models import QuestionResponse, Question, Choice, QuestionType
from .exceptions import QuestionParserError, QuestionFormatError
from .parser import BaseParser

logger = logging.getLogger(__name__)

class JSONResponseParser(BaseParser):
    """
    Mengurai respons AI yang berisi JSON (mungkin dibungkus markdown atau teks tambahan).
    """

    def parse(self, raw: str) -> QuestionResponse:
        """
        Langkah:
        1. Bersihkan teks (hapus markdown, ekstrak JSON).
        2. Deserialisasi ke dictionary.
        3. Konversi dictionary ke QuestionResponse (Pydantic).
        """
        if not raw or not raw.strip():
            raise QuestionParserError("Empty response from AI provider.")

        cleaned = self._extract_json(raw)
        logger.info("JSON extracted successfully.")

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise QuestionFormatError(f"Invalid JSON from AI: {str(e)}")

        return self._dict_to_question_response(data)

    def _extract_json(self, text: str) -> str:
        """
        Mencoba mengekstrak bagian JSON dari teks.
        1. Jika teks diapit ```json ... ```, ambil dalamnya.
        2. Jika tidak, cari objek JSON pertama yang valid.
        """
        # Coba hapus markdown code fences
        text = text.strip()
        # Pola: ```json ... ``` atau ``` ... ```
        code_fence = re.search(r'```(?:json)?\s*\n(.*?)\n```', text, re.DOTALL)
        if code_fence:
            text = code_fence.group(1).strip()
        else:
            # Cari kurung kurawal pertama dan terakhir
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1 and end > start:
                text = text[start:end+1]
            # Jika tidak ditemukan objek, mungkin array? Tapi kita harap objek.
        return text.strip()

    def _dict_to_question_response(self, data: dict) -> QuestionResponse:
        if "questions" not in data:
            raise QuestionFormatError("'questions' key is missing in AI response.")
        questions_raw = data.get("questions", [])
        if not isinstance(questions_raw, list):
            raise QuestionFormatError("'questions' field must be a list.")
        """Konversi dictionary mentah ke QuestionResponse dengan validasi Pydantic."""
        try:
            questions_raw = data.get("questions", [])
            if not isinstance(questions_raw, list):
                raise QuestionFormatError("'questions' field must be a list.")

            questions = []
            for idx, q_dict in enumerate(questions_raw):
                question = self._parse_single_question(q_dict, idx)
                questions.append(question)

            return QuestionResponse(questions=questions)
        except QuestionFormatError:
            raise
        except Exception as e:
            raise QuestionFormatError(f"Failed to convert AI response to QuestionResponse: {str(e)}")

    def _parse_single_question(self, q_dict: dict, index: int) -> Question:
        """Parsing satu soal dari dictionary."""
        question_text = q_dict.get("question", "")
        if not question_text:
            raise QuestionFormatError(f"Question {index+1}: 'question' field is missing or empty.")

        q_type_str = q_dict.get("type", "multiple_choice").lower()
        # Konversi ke enum QuestionType
        try:
            q_type = QuestionType(q_type_str)
        except ValueError:
            # Default ke multiple_choice jika tidak dikenali
            q_type = QuestionType.MULTIPLE_CHOICE

        choices = None
        if q_type == QuestionType.MULTIPLE_CHOICE:
            choices = self._parse_choices(q_dict.get("choices", []), index)

        answer = q_dict.get("answer", None)
        explanation = q_dict.get("explanation", None)

        return Question(
            id=index + 1,  # id sementara sesuai urutan
            question=question_text,
            type=q_type,
            choices=choices,
            answer=answer,
            explanation=explanation,
            difficulty=None,
            metadata={}
        )

    def _parse_choices(self, choices_data: list, q_index: int) -> List[Choice]:
        """Parsing daftar pilihan ganda. Mendukung array string sederhana atau array objek."""
        parsed = []
        if not choices_data or not isinstance(choices_data, list):
            raise QuestionFormatError(f"Question {q_index+1}: choices must be a non-empty list.")

        for i, item in enumerate(choices_data):
            if isinstance(item, str):
                # Format sederhana: string, label = A, B, C, D...
                label = chr(ord('A') + i) if i < 26 else str(i)
                parsed.append(Choice(label=label, text=item))
            elif isinstance(item, dict):
                label = item.get("label", chr(ord('A') + i))
                text = item.get("text", "")
                is_correct = item.get("is_correct", None)
                if not text:
                    raise QuestionFormatError(f"Question {q_index+1}: choice text cannot be empty.")
                parsed.append(Choice(label=label, text=text, is_correct=is_correct))
            else:
                raise QuestionFormatError(f"Question {q_index+1}: invalid choice format.")
        return parsed