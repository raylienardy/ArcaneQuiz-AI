from typing import List, Dict, Any
from ..models import ExportDocument, ExportMetadata
from .base_formatter import BaseFormatter

class PlainFormatter(BaseFormatter):
    """Formatter untuk teks biasa."""

    async def format(self, questions: List[Dict[str, Any]], metadata: ExportMetadata,
                     title: str = "Generated Questions") -> ExportDocument:
        lines = [title, "=" * len(title), ""]
        for idx, q in enumerate(questions, start=1):
            lines.append(f"Question {idx}")
            lines.append(q.get("question", ""))
            # Pilihan
            choices = q.get("choices")
            if choices:
                for choice in choices:
                    lines.append(f"{choice.get('label', '')}. {choice.get('text', '')}")
            # Jawaban
            answer = q.get("answer")
            if answer:
                lines.append(f"Answer: {answer}")
            # Penjelasan
            explanation = q.get("explanation")
            if explanation:
                lines.append(f"Explanation: {explanation}")
            lines.append("")  # baris kosong pemisah

        content = "\n".join(lines)
        metadata.formatter_name = "plain"
        metadata.formatter_version = "1.0"
        return ExportDocument(
            title=title,
            content=content,
            questions=questions,
            metadata=metadata,
        )

    def supports(self, format_name: str) -> bool:
        return format_name == "plain"

    def description(self) -> str:
        return "Plain text formatter"