from app.text_processing.pipeline import clean_text

def test_clean_text_basic():
    raw = "Hello    World\r\n\r\n\r\nNext line\t\twith tab\x00"
    cleaned = clean_text(raw)
    assert "  " not in cleaned
    assert "\r" not in cleaned
    assert "\t" not in cleaned
    assert "\x00" not in cleaned
    assert "Hello World" in cleaned
    # Harusnya kolaps baris kosong
    assert "\n\n\n" not in cleaned