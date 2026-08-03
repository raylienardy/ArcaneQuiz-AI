"""
Kumpulan aturan pembersihan teks individual.
Setiap fungsi menerima string dan mengembalikan string yang telah dibersihkan.
"""

import re
import unicodedata

def normalize_newlines(text: str) -> str:
    """Ubah semua gaya baris baru (CRLF, CR) menjadi LF (\n)."""
    return text.replace('\r\n', '\n').replace('\r', '\n')

def remove_tabs(text: str) -> str:
    """Ganti tab dengan spasi tunggal."""
    return text.replace('\t', ' ')

def collapse_spaces(text: str) -> str:
    """Hancurkan spasi berurutan menjadi satu spasi."""
    return re.sub(r' {2,}', ' ', text)

def collapse_blank_lines(text: str) -> str:
    """Sisakan maksimal satu baris kosong berturut-turut."""
    return re.sub(r'\n{3,}', '\n\n', text)

def remove_control_characters(text: str) -> str:
    """
    Hapus karakter kontrol yang tidak terlihat (kecuali newline \n dan tab yang sudah ditangani).
    Karakter kontrol ASCII 0-31 kecuali 10 (\n) dan 9 (\t) dihilangkan.
    Juga hapus karakter Unicode kategori 'Cc' kecuali \n, \r, \t.
    """
    # Hapus karakter kontrol ASCII selain \n, \r, \t (tapi \r sudah dinormalisasi)
    # Kita gunakan regex untuk mencocokkan karakter kontrol selain \n
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

def normalize_unicode(text: str) -> str:
    """
    Normalisasi Unicode ke bentuk NFC, sehingga karakter yang tampilannya sama 
    memiliki representasi yang konsisten. Tidak merusak huruf beraksen.
    """
    return unicodedata.normalize('NFC', text)

def trim_text(text: str) -> str:
    """Hapus spasi dan baris kosong di awal dan akhir teks."""
    return text.strip()