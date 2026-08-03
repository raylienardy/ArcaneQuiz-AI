from typing import List, Dict, Any
from ..models import ExportDocument, ExportMetadata
from .base_formatter import BaseFormatter

class MarkdownFormatter(BaseFormatter):
    """Formatter untuk Markdown."""

    def _escape_markdown(self, text: str) -> str:
        """Escape karakter khusus Markdown sederhana."""
        return text.replace("_", "\\_").replace("*", "\\*")

    async def format(self, questions: List[Dict[str, Any]], metadata: ExportMetadata,
                     title: str = "Generated Questions") -> ExportDocument:
        lines = [f"# {title}", ""]
        for idx, q in enumerate(questions, start=1):
            lines.append(f"## Question {idx}")
            lines.append(q.get("question", ""))
            lines.append("")
            # Pilihan
            choices = q.get("choices")
            if choices:
                for choice in choices:
                    prefix = f"- {choice.get('label', '')}."
                    text = self._escape_markdown(choice.get('text', ''))
                    # Jika ini jawaban, tebalkan
                    if choice.get('label', '') == q.get('answer', ''):
                        text = f"**{text}**"
                    lines.append(f"{prefix} {text}")
                lines.append("")
            # Jawaban
            answer = q.get("answer")
            if answer and not choices:  # untuk esai/true-false tanpa pilihan
                lines.append(f"**Answer:** {answer}")
                lines.append("")
            elif answer and choices:
                lines.append(f"**Answer:** {answer}")
                lines.append("")
            # Penjelasan
            explanation = q.get("explanation")
            if explanation:
                lines.append(f"**Explanation:** {explanation}")
                lines.append("")
            lines.append("---")
            lines.append("")

        content = "\n".join(lines)
        metadata.formatter_name = "markdown"
        metadata.formatter_version = "1.0"
        return ExportDocument(
            title=title,
            content=content,
            questions=questions,
            metadata=metadata,
        )

    def supports(self, format_name: str) -> bool:
        return format_name == "markdown"

    def description(self) -> str:
        return "Markdown formatter"