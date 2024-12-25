# Panduan Penggunaan SteganoFlaskver

## Persiapan

1. **Install Dependencies**

bash
pip install -r requirements.txt

2. **Jalankan Server**

bash
python api.py

## Cara Penggunaan

### 1. Menggunakan Web Interface (Recommended)

1. Buka file `test.html` di browser
2. Untuk Menyembunyikan Pesan:
   - Pilih gambar
   - Masukkan pesan
   - Masukkan key (password)
   - Klik "Encode"
   - Download hasil
3. Untuk Mengekstrak Pesan:
   - Pilih gambar hasil encode
   - Masukkan key yang sama
   - Klik "Decode"

### 2. Menggunakan Python Script

python:GUIDE.md
import requests
import base64
Encode
with open("gambar.jpg", "rb") as image_file:
image_base64 = base64.b64encode(image_file.read()).decode()
response = requests.post("http://localhost:5000/encode",
json={
"image": image_base64,
"message": "Pesan rahasia"
})
Decode
response = requests.post("http://localhost:5000/decode",
json={
"image": response.json()['encoded_image']
})

### 3. Testing API

1. Test Sederhana:
```bash
python test_simple.py
```
bash:GUIDE.md
python test_simple.py
```

2. Test Lengkap:
```bash
python test_api.py

bash:GUIDE.md
python test_api.py
```

## Struktur Project

SteganoFlaskver/
├── api.py            # Server Flask dan endpoint API
├── imgstegno.py     # Implementasi steganografi
├── test.html        # Web interface
├── test_api.py      # Testing script (lengkap)
├── test_simple.py   # Testing script (sederhana)
└── requirements.txt # Dependencies
```

## Catatan Penting

1. Server harus berjalan (`python api.py`) sebelum menggunakan API
2. Gunakan format PNG untuk hasil terbaik
3. Ukuran pesan tidak boleh melebihi kapasitas gambar
4. Simpan key dengan aman - dibutuhkan untuk decode
5. Jangan kompres atau edit gambar hasil - bisa merusak pesan

## Troubleshooting

1. "Server tidak merespon"
   - Pastikan `python api.py` berjalan
   - Cek port 5000 tidak digunakan aplikasi lain

2. "Pesan tidak terbaca"
   - Pastikan menggunakan key yang sama
   - Pastikan gambar tidak dimodifikasi

3. "Error saat encode"
   - Cek ukuran pesan
   - Pastikan format gambar didukung