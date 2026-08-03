# OpenQuiz AI — Panduan Lengkap untuk Pemula

Selamat datang di OpenQuiz AI! Proyek ini adalah aplikasi web sederhana yang bisa membuat soal ujian dari file PDF, Word, atau teks biasa dengan bantuan AI.  
Kamu tidak perlu jago coding untuk menjalankannya—cukup ikuti langkah‑langkah di bawah ini secara berurutan.

---

## 1. Apa yang Kamu Butuhkan?

Sebelum mulai, pastikan komputer kamu sudah memiliki:

- **Python** (versi 3.10 atau lebih baru) → [Download Python](https://www.python.org/downloads/)  
  _Saat instalasi, centang “Add Python to PATH” agar mudah dipanggil dari terminal._
- **Node.js** (versi 18 atau lebih baru) → [Download Node.js](https://nodejs.org/en/download)  
  _Pilih versi LTS (rekomendasi)._
- **Git** (opsional, tapi berguna) → [Download Git](https://git-scm.com/downloads)  
  _Tidak wajib, karena kamu sudah menerima file zip proyek ini._

---

## 2. Ekstrak File Zip

Setelah menerima file `OpenQuiz-AI.zip`, klik kanan → **Extract All…** (Windows) atau gunakan aplikasi dekompresi favorit kamu.  
Letakkan folder hasil ekstrak di tempat yang mudah dijangkau, misalnya `C:\Users\NamaKamu\Documents\OpenQuiz-AI`.

Di dalam folder tersebut ada dua folder utama:

```
openquiz-ai/
  ├── backend/     ← Tempat kode server (Python)
  └── frontend/    ← Tempat kode tampilan (React)
```

---

## 3. Menjalankan Server Backend (Python)

### 3.1. Buka Terminal di Folder Backend

1. Buka folder `backend` di **File Explorer**.
2. Klik di bilah alamat (address bar) dan ketik `cmd` lalu **Enter**.  
   Akan muncul jendela Command Prompt (CMD) yang langsung berada di dalam folder `backend`.

### 3.2. Buat Virtual Environment (Opsional tapi Disarankan)

Ini membuat lingkungan Python terpisah agar tidak bentrok dengan proyek lain.

```bash
python -m venv .venv
```

Tunggu beberapa detik sampai selesai (tidak ada output khusus).

### 3.3. Aktifkan Virtual Environment

- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  source .venv/bin/activate
  ```

Setelah aktif, kamu akan melihat `(.venv)` di baris perintah.

### 3.4. Instal Paket yang Dibutuhkan

```bash
pip install -r requirements.txt
```

Proses ini akan mengunduh dan memasang semua library yang diperlukan (FastAPI, PyPDF, Groq SDK, dll). Tunggu sampai selesai.

### 3.5. Atur File Konfigurasi `.env`

1. Di dalam folder `backend`, ada file bernama `.env.example`.  
   **Salin** file tersebut dan ubah namanya menjadi `.env` (tanpa `.example`).

   Cara mudah di Windows:
   - Klik kanan `.env.example` → Copy
   - Klik kanan di area kosong → Paste
   - Klik kanan file hasil copy → Rename, hapus `.example` sehingga namanya menjadi `.env` (mungkin muncul peringatan, klik Yes).

2. Buka file `.env` dengan Notepad atau editor teks.

3. Isi dengan konfigurasi AI yang ingin kamu pakai. Pilih **salah satu** dari tiga pilihan di bawah ini:

   **A. Mock AI (gratis, tanpa internet, untuk uji coba cepat)**

   ```
   AI_PROVIDER=mock
   ```

   **B. Groq AI (gratis, butuh internet, lebih pintar)**

   ```
   AI_PROVIDER=groq
   GROQ_API_KEY=gsk_api_key_kamu_disini
   GROQ_MODEL=llama-3.1-8b-instant
   ```

   _Dapatkan API key gratis di [console.groq.com](https://console.groq.com) (daftar pakai Google/email)._

   **C. Gemini AI (Google, gratis terbatas)**

   ```
   AI_PROVIDER=gemini
   GEMINI_API_KEY=api_key_kamu_disini
   GEMINI_MODEL=models/gemini-2.0-flash
   ```

   _Dapatkan API key di [Google AI Studio](https://aistudio.google.com/apikey)._

4. Simpan file `.env` dan tutup editor.

### 3.6. Jalankan Server

Di CMD yang masih terbuka, ketik:

```bash
source .venv/Scripts/activate
python -m uvicorn app.main:app --reload
```

Biarkan jendela ini tetap terbuka. Jika berhasil, kamu akan melihat tulisan seperti:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Artinya server backend sudah berjalan. **Jangan tutup jendela ini.**

---

## 4. Menjalankan Frontend (Tampilan Web)

### 4.1. Buka Terminal Baru di Folder Frontend

1. Kembali ke folder utama proyek, buka folder `frontend`.
2. Klik di bilah alamat dan ketik `cmd` lalu Enter (seperti tadi).

### 4.2. Instal Paket Node.js

```bash
npm install
```

Tunggu hingga semua paket terunduh (biasanya agak lama untuk pertama kali).

### 4.3. Jalankan Server Frontend

```bash
npm run dev
```

Jika berhasil, akan muncul:

```
  VITE v6.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

Biarkan jendela ini tetap terbuka.

---

## 5. Buka Aplikasi di Browser

1. Buka browser (Chrome/Firefox/Edge) dan arahkan ke **http://localhost:5173**.
2. Kamu akan melihat halaman **OpenQuiz AI**.  
   Klik tautan **Upload** (atau langsung ke **http://localhost:5173/upload**).

---

## 6. Cara Menggunakan Aplikasi

1. **Upload File**
   - Seret file .pdf, .docx, atau .txt ke area yang tersedia, atau klik “Browse Files”.
   - File maksimal 20 MB.

2. **Generate Soal**
   - Setelah berhasil upload, teks hasil ekstraksi akan muncul.
   - Klik tombol **Generate Questions**.
   - Tunggu beberapa detik, soal buatan AI akan muncul.

3. **Review Soal**
   - Gunakan kotak pencarian, filter, dan pengurutan untuk melihat soal.
   - Klik kartu soal untuk melihat detail lengkap (jawaban, penjelasan).
   - Statistik jumlah soal, tipe, dan metadata AI juga ditampilkan.

4. **Export PDF**
   - Klik tombol **📄 Export PDF** di bagian bawah.
   - Akan muncul jendela pratinjau ekspor.
   - Klik **Download** untuk mengunduh file PDF berisi semua soal.

---

## 7. Menghentikan Aplikasi

- **Backend**: Buka jendela CMD yang menjalankan server, tekan **Ctrl+C**.
- **Frontend**: Buka jendela CMD yang menjalankan Vite, tekan **Ctrl+C**.

Setiap kali ingin menjalankan lagi, kamu hanya perlu mengulangi langkah **3.6** dan **4.3** (virtual environment sudah terinstal, tidak perlu `pip install` lagi).

---

## 8. Troubleshooting (Masalah Umum)

### “python: command not found”

- Pastikan Python sudah diinstal dan dicentang “Add to PATH”.
- Coba `python3` atau `py -3` jika `python` tidak dikenali.

### “npm: command not found”

- Pastikan Node.js sudah terinstal. Restart CMD setelah instalasi.

### Error 429 (Too Many Requests) saat generate soal

- Kamu mungkin kehabisan kuota gratis Groq/Gemini.
- Ganti ke Mock provider dengan mengedit `.env` → `AI_PROVIDER=mock`, lalu restart backend.

### Halaman putih atau error di browser

- Buka **Developer Tools** (F12) dan lihat tab Console.
- Catat pesan error dan tanyakan ke yang lebih paham coding.

---

## 9. Bantuan Lebih Lanjut

Jika ada kendala, silakan hubungi pembuat proyek atau buka issue di [GitHub repository](https://github.com/username/openquiz-ai) (jika tersedia).

Selamat mencoba! 🚀
