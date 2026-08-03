class QuestionGenerationError(Exception):
    """Kesalahan umum saat generasi pertanyaan."""
    pass

class QuestionValidationError(QuestionGenerationError):
    """Respons tidak lolos validasi."""
    pass

class QuestionParserError(QuestionGenerationError):
    """Gagal mengurai respons AI."""
    pass

class QuestionFormatError(QuestionGenerationError):
    """Format respons tidak sesuai yang diharapkan."""
    pass

class QuestionConfigurationError(QuestionGenerationError):
    """Konfigurasi generasi pertanyaan tidak valid."""
    pass