"""
Template prompt modular. Setiap bagian adalah fungsi yang mengembalikan string,
sehingga mudah disesuaikan atau ditambahkan di masa depan.
"""

def system_prompt(language: str) -> str:
    return {
        "id": "Anda adalah asisten AI yang ahli dalam membuat soal pendidikan.",
        "en": "You are an AI assistant specialized in creating educational questions.",
    }.get(language, "You are an AI assistant specialized in creating educational questions.")

def task_instruction(question_type: str, language: str) -> str:
    templates = {
        "id": {
            "multiple_choice": "Buatlah soal pilihan ganda.",
            "essay": "Buatlah soal esai.",
            "true_false": "Buatlah soal benar/salah.",
        },
        "en": {
            "multiple_choice": "Create multiple-choice questions.",
            "essay": "Create essay questions.",
            "true_false": "Create true/false questions.",
        }
    }
    return templates.get(language, templates["en"]).get(question_type, "")

def format_requirements(question_type: str, language: str) -> str:
    base = {
        "id": {
            "multiple_choice": "Setiap soal harus memiliki tepat 4 pilihan (A, B, C, D) dan satu jawaban benar. Sertakan penjelasan.",
            "essay": "Setiap soal harus memiliki jawaban berupa esai singkat dan penjelasan.",
            "true_false": "Setiap soal harus memiliki jawaban True atau False dan penjelasan.",
        },
        "en": {
            "multiple_choice": "Each question must have exactly 4 choices (A, B, C, D) and one correct answer. Include an explanation.",
            "essay": "Each question must have a short essay answer and an explanation.",
            "true_false": "Each question must have a True or False answer and an explanation.",
        }
    }
    return base.get(language, base["en"]).get(question_type, "")

def difficulty_instruction(difficulty: str, language: str) -> str:
    mapping = {
        "id": {
            "easy": "Gunakan konsep sederhana dan pertanyaan yang mudah dipahami.",
            "medium": "Gunakan tingkat pemahaman menengah.",
            "hard": "Gunakan analisis dan penalaran yang lebih dalam.",
        },
        "en": {
            "easy": "Use simple concepts and easy-to-understand questions.",
            "medium": "Use intermediate understanding level.",
            "hard": "Use deeper analysis and reasoning.",
        }
    }
    return mapping.get(language, mapping["en"]).get(difficulty, "")

def output_format_instruction(language: str) -> str:
    return {
        "id": (
            "HANYA kembalikan JSON. Jangan sertakan markdown, penjelasan di luar JSON, atau blok kode. "
            "Format JSON harus persis seperti:\n"
            '{"questions": [{"question": "...", "choices": [{"label": "A", "text": "..."}, ...], "answer": "A", "explanation": "..."}]}'
        ),
        "en": (
            "ONLY return JSON. Do not include markdown, explanations outside JSON, or code fences. "
            "The JSON format must be exactly:\n"
            '{"questions": [{"question": "...", "choices": [{"label": "A", "text": "..."}, ...], "answer": "A", "explanation": "..."}]}'
        )
    }.get(language, "")

def language_instruction(target_language: str) -> str:
    return {
        "id": "Semua soal dan penjelasan harus dalam Bahasa Indonesia.",
        "en": "All questions and explanations must be in English.",
    }.get(target_language, "All questions and explanations must be in English.")