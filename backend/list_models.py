"""Script sederhana untuk menampilkan model Gemini yang tersedia."""
import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Harap set GEMINI_API_KEY di environment atau .env")
    exit(1)

client = genai.Client(api_key=api_key)
print("Model yang tersedia untuk akun ini:")
for model in client.models.list():
    if "gemini" in model.name:
        print(f" - {model.name}")