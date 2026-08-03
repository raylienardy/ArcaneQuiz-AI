from typing import Optional
from .models import ExportDocument, ExportMetadata

class QuestionToDocumentFormatter:
    """
    Mengonversi QuestionResponse (atau representasi internalnya) menjadi ExportDocument.
    Kelas ini dapat diperluas dengan berbagai strategi pemformatan (Markdown, HTML, dll.)
    """

    async def format(self, questions: list, metadata: Optional[ExportMetadata] = None,
                     title: str = "Generated Questions") -> ExportDocument:
        """
        Ubah daftar pertanyaan (dict) menjadi ExportDocument.
        Untuk saat ini, placeholder: hanya menggabungkan pertanyaan sebagai teks biasa.
        """
        content = ""
        for idx, q in enumerate(questions, start=1):
            content += f"{idx}. {q.get('question', '')}\n"
            if 'choices' in q:
                for choice in q['choices']:
                    content += f"   {choice['label']}. {choice['text']}\n"
            if 'answer' in q:
                content += f"   Answer: {q['answer']}\n"
            content += "\n"

        return ExportDocument(
            title=title,
            content=content,
            questions=questions,
            metadata=metadata or ExportMetadata(),
        )