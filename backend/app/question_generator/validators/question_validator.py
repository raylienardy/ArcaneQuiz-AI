"""
QuestionValidator – memvalidasi QuestionResponse yang sudah diparse.
"""

import logging
from typing import List
from ..models import QuestionResponse, Question, Choice, QuestionType
from ..exceptions import QuestionValidationError

logger = logging.getLogger(__name__)


class QuestionValidator:
    """Melakukan validasi struktural dan logika pada QuestionResponse."""

    def validate(self, response: QuestionResponse) -> QuestionResponse:
        """
        Memvalidasi response. Jika valid, kembalikan response.
        Jika tidak valid, raise QuestionValidationError dengan pesan detail.
        """
        logger.info("Validation started.")

        # 1. Response-level checks
        if not response:
            raise QuestionValidationError("QuestionResponse is None.")
        if not response.questions:
            raise QuestionValidationError("QuestionResponse has no questions.")

        # 2. Periksa tiap pertanyaan
        seen_ids = set()
        seen_texts = set()
        for i, question in enumerate(response.questions):
            self._validate_question(question, i, seen_ids, seen_texts)

        logger.info(f"Validation passed for {len(response.questions)} questions.")
        return response

    def _validate_question(self, q: Question, index: int, seen_ids: set, seen_texts: set):
        prefix = f"Question {q.id if q.id else index+1}"

        # ID
        if q.id is not None:
            if q.id in seen_ids:
                raise QuestionValidationError(f"{prefix}: duplicate ID {q.id}.")
            seen_ids.add(q.id)

        # Teks pertanyaan
        if not q.question or not q.question.strip():
            raise QuestionValidationError(f"{prefix}: question text is empty.")

        # Cek duplikasi teks pertanyaan
        if q.question.strip().lower() in seen_texts:
            raise QuestionValidationError(f"{prefix}: duplicate question text.")
        seen_texts.add(q.question.strip().lower())

        # Tipe pertanyaan
        if not isinstance(q.type, QuestionType):
            raise QuestionValidationError(f"{prefix}: invalid question type.")

        # Validasi berdasarkan tipe
        if q.type == QuestionType.MULTIPLE_CHOICE:
            self._validate_multiple_choice(q, prefix)
        elif q.type == QuestionType.ESSAY:
            self._validate_essay(q, prefix)
        elif q.type == QuestionType.TRUE_FALSE:
            self._validate_true_false(q, prefix)

        # Jawaban tidak boleh kosong
        if not q.answer or not q.answer.strip():
            raise QuestionValidationError(f"{prefix}: answer is missing or empty.")

    def _validate_multiple_choice(self, q: Question, prefix: str):
        if not q.choices or len(q.choices) == 0:
            raise QuestionValidationError(f"{prefix}: multiple choice must have choices.")
        if len(q.choices) != 4:
            raise QuestionValidationError(
                f"{prefix}: multiple choice expects exactly 4 choices, got {len(q.choices)}."
            )

        # Pilihan tidak boleh kosong
        for choice in q.choices:
            if not choice.text or not choice.text.strip():
                raise QuestionValidationError(f"{prefix}: a choice text is empty.")

        # Tidak ada duplikasi teks pilihan
        choice_texts = [c.text.strip().lower() for c in q.choices]
        if len(set(choice_texts)) != len(choice_texts):
            raise QuestionValidationError(f"{prefix}: duplicate choice texts detected.")
          
        if not q.answer or not q.answer.strip():
            raise QuestionValidationError(f"{prefix}: answer is missing or empty.")

        # Jawaban harus merujuk ke salah satu label (jika label digunakan)
        if q.choices and q.choices[0].label:  # asumsikan ada label
            valid_labels = {c.label.strip().upper() for c in q.choices}
            if q.answer.strip().upper() not in valid_labels:
                raise QuestionValidationError(
                    f"{prefix}: answer '{q.answer}' does not match any choice label {valid_labels}."
                )

    def _validate_essay(self, q: Question, prefix: str):
        if q.choices and len(q.choices) > 0:
            raise QuestionValidationError(f"{prefix}: essay question should not have choices.")
        # Penjelasan opsional, jadi tidak dicek

    def _validate_true_false(self, q: Question, prefix: str):
        if not q.choices or len(q.choices) != 2:
            raise QuestionValidationError(
                f"{prefix}: true/false must have exactly 2 choices (True/False)."
            )
        choice_labels = [c.label.strip().upper() for c in q.choices]
        if set(choice_labels) != {"TRUE", "FALSE"}:
            raise QuestionValidationError(
                f"{prefix}: true/false choices must be 'True' and 'False'."
            )
        if q.answer.strip().upper() not in {"TRUE", "FALSE"}:
            raise QuestionValidationError(
                f"{prefix}: true/false answer must be 'True' or 'False'."
            )