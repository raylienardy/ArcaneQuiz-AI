"""
PromptBuilder mengonversi QuestionRequest menjadi string prompt siap pakai.
Tidak ada interaksi AI di sini.
"""

from .models import QuestionRequest
from . import prompt_templates as tpl

class PromptBuilder:
    """Membangun prompt provider-agnostic dari QuestionRequest."""

    def build(self, request: QuestionRequest) -> str:
        lang = request.language or "en"
        qtype = request.question_type.value  # e.g., "multiple_choice"

        sections = []

        # 1. System / Role
        sections.append(tpl.system_prompt(lang))

        # 2. Task description
        sections.append(tpl.task_instruction(qtype, lang))

        # 3. Number of questions
        if lang == "id":
            sections.append(f"Buatlah {request.number_of_questions} soal.")
        else:
            sections.append(f"Create {request.number_of_questions} questions.")

        # 4. Difficulty
        if request.difficulty:
            diff_instruction = tpl.difficulty_instruction(request.difficulty.value, lang)
            if diff_instruction:
                sections.append(diff_instruction)

        # 5. Language constraint
        sections.append(tpl.language_instruction(lang))

        # 6. Source material
        if lang == "id":
            sections.append(f"Teks sumber:\n\n{request.text}")
        else:
            sections.append(f"Source text:\n\n{request.text}")

        # 7. Additional instructions
        if request.additional_instruction:
            sections.append(request.additional_instruction)

        # 8. Format requirements
        sections.append(tpl.format_requirements(qtype, lang))

        # 9. Output instruction
        sections.append(tpl.output_format_instruction(lang))

        return "\n\n".join(sections)