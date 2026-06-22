# Invoice Renamer OCR

Aplikasi Python untuk:

* Membaca PDF invoice
* Mendeteksi PDF text atau scan
* OCR otomatis menggunakan PaddleOCR
* Mengambil nama perusahaan pengirim invoice
* Mengambil nomor invoice
* Membuat folder berdasarkan nama perusahaan
* Rename PDF menjadi:

PT_VENDOR_NAMA_NOINVOICE.pdf

Contoh:

PT_ALUR_BIRU_MARITIM_C123-00026.pdf

---

## Struktur Folder

invoice-renamer/

├── input/

├── output/

├── failed/

├── logs/

├── app/

│   ├── config.py

│   ├── pdf_detector.py

│   ├── text_extractor.py

│   ├── invoice_parser.py

│   ├── renamer.py

│   └── logger.py

├── .env

├── main.py

└── requirements.txt

---

## Install

Buat virtual environment:

Windows

python -m venv venv

Aktifkan:

venv\Scripts\activate

Install dependency:

pip install -r requirements.txt

---

## Konfigurasi

Buat file .env

INPUT_FOLDER=./input
OUTPUT_FOLDER=./output
FAILED_FOLDER=./failed

MIN_TEXT_LENGTH=50

OCR_LANGUAGE=en

---

## Menjalankan

python main.py

---

## Alur Kerja

1. Ambil semua PDF dari folder input

2. Deteksi PDF text atau scan

3. Jika text:

   * Extract text langsung

4. Jika scan:

   * OCR menggunakan PaddleOCR

5. Cari:

   * Nama perusahaan pengirim
   * Nomor invoice

6. Rename file:

   COMPANY_INVOICE.pdf

7. Simpan ke:

output/COMPANY/

Contoh:

output/PT_ALUR_BIRU_MARITIM/PT_ALUR_BIRU_MARITIM_C123-00026.pdf

---

## Folder Failed

Jika gagal diproses:

failed/

File tetap disimpan untuk dianalisis ulang.

---

## Log

Semua proses disimpan ke:

logs/process.log

Contoh:

SUCCESS:
PT_ALUR_BIRU_MARITIM_C123-00026.pdf

FAILED:
UNKNOWN_COMPANY_NO_INVOICE.pdf

---

## Vendor Yang Sudah Diuji

* PT Alur Biru Maritim
* PT Yuan Wira Perdana
* PT Satra Prima Niaga

---

## Pengembangan Berikutnya

* Export hasil ke Excel
* Dashboard monitoring
* Training model OCR khusus invoice Indonesia
* Database vendor whitelist
* Auto koreksi OCR PT ↔ PI
* Auto koreksi nama vendor menggunakan RapidFuzz
* REST API dengan FastAPI
* Batch processing multi-thread
* Docker deployment
