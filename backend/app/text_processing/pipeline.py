"""
Pipeline pembersihan teks: menjalankan aturan-aturan dalam urutan tertentu.
"""

from . import rules

def clean_text(raw_text: str) -> str:
    """
    Membersihkan teks mentah hasil ekstraksi.
    Urutan langkah sengaja diatur untuk hasil terbaik.
    """
    if not raw_text:
        return raw_text

    # 1. Normalisasi Unicode agar karakter seragam (NFC)
    text = rules.normalize_unicode(raw_text)

    # 2. Normalisasi baris baru ke \n
    text = rules.normalize_newlines(text)

    # 3. Hapus tab
    text = rules.remove_tabs(text)

    # 4. Hapus karakter kontrol tak terlihat
    text = rules.remove_control_characters(text)

    # 5. Hancurkan spasi berlebihan
    text = rules.collapse_spaces(text)

    # 6. Hancurkan baris kosong berlebihan
    text = rules.collapse_blank_lines(text)

    # 7. Potong spasi/baris di ujung
    text = rules.trim_text(text)

    return text