def test_upload_valid_txt(client):
    files = {"file": ("test.txt", b"Hello world", "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert data["data"]["filename"] == "test.txt"
    assert data["data"]["text"] == "Hello world"

def test_upload_empty_txt(client):
    files = {"file": ("empty.txt", b"", "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert response.json()["success"] is False

def test_upload_unsupported_file(client):
    files = {"file": ("image.png", b"fakeimage", "image/png")}
    response = client.post("/upload", files=files)
    assert response.status_code == 415  # Unsupported Media Type