FROM python:3.10-slim

WORKDIR /app

# Salin requirements dan install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode backend
COPY backend/ .

# Jalankan server
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]