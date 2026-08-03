def test_pdf_extraction(client):
    from pypdf import PdfWriter
    from io import BytesIO
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    pdf_bytes = BytesIO()
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)
    files = {"file": ("test.pdf", pdf_bytes.read(), "application/pdf")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    # Karena halaman kosong tanpa teks, harus ada peringatan
    assert len(data["data"]["warnings"]) > 0 or data["data"]["text"] == ""

def test_docx_extraction(client):
    # Uji dengan DOCX minimal menggunakan python-docx
    from docx import Document
    from io import BytesIO
    doc = Document()
    doc.add_paragraph("Hello DOCX")
    docx_bytes = BytesIO()
    doc.save(docx_bytes)
    docx_bytes.seek(0)
    files = {"file": ("test.docx", docx_bytes.read(), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Hello DOCX" in data["data"]["text"]