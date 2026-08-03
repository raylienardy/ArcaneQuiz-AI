def estimate_tokens(text: str) -> int:
    """Estimasi kasar: 1 token ≈ 0.75 kata (atau 1.3 kata per token)."""
    words = text.split()
    return int(len(words) * 1.3)

def truncate_text(text: str, max_tokens: int = 5000) -> tuple:
    """Potong teks jika estimasi token melebihi max_tokens. Return (text, was_truncated)."""
    if estimate_tokens(text) <= max_tokens:
        return text, False
    max_words = int(max_tokens / 1.3)
    words = text.split()[:max_words]
    return ' '.join(words), True