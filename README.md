# SteganoFlaskver
Stegano for Kejarkom 


# Image Steganography with LSB Method

Aplikasi steganografi gambar yang menggunakan metode LSB (Least Significant Bit) untuk menyembunyikan pesan dalam gambar digital. Proyek ini menyediakan baik API (menggunakan Flask) maupun antarmuka web sederhana.

## Fitur

- Menyembunyikan pesan teks dalam gambar menggunakan metode LSB
- Mengekstrak pesan tersembunyi dari gambar
- Mendukung format gambar PNG
- Tersedia dalam bentuk API REST dan antarmuka web
- Implementasi marker sistem untuk deteksi akhir pesan
- Validasi ukuran pesan terhadap kapasitas gambar

## Teknologi yang Digunakan

- Python 3.x
- Flask (Web Framework)
- Pillow (Image Processing)
- HTML5 Canvas (Web Interface)
- Base64 Encoding/Decoding

## Cara Kerja

### Metode LSB (Least Significant Bit)

Aplikasi ini menggunakan teknik LSB, dimana pesan disembunyikan dengan memodifikasi bit terakhir dari setiap komponen warna (RGB) dalam pixel gambar. Karena perubahan terjadi pada bit yang paling tidak signifikan, perubahan pada gambar hampir tidak terlihat oleh mata manusia.

### Proses Encoding

1. Konversi pesan ke bentuk binary (8-bit per karakter)
2. Tambahkan marker '$$' di akhir pesan
3. Modifikasi LSB dari setiap komponen RGB pixel
4. Simpan hasil sebagai gambar PNG

### Proses Decoding

1. Ekstrak LSB dari setiap komponen RGB pixel
2. Konversi sequence bit menjadi karakter
3. Deteksi marker '$$' untuk menentukan akhir pesan

## Instalasi

bash
Clone repository
git clone https://github.com/username/image-steganography.git
cd image-steganography
Install dependencies
pip install -r requirements.txt


## Penggunaan

### Menggunakan API

1. Jalankan server Flask:


bash
python api.py


2. Gunakan endpoint API:
- `GET /` - Cek status API
- `GET /docs` - Lihat dokumentasi API
- `POST /encode` - Sembunyikan pesan dalam gambar
- `POST /decode` - Ekstrak pesan dari gambar

### Menggunakan Web Interface

1. Buka file `test.html` di browser
2. Upload gambar
3. Masukkan pesan
4. Klik tombol Encode/Decode

### Menggunakan Python Script


python
import requests
import base64
Baca gambar
with open("gambar.jpg", "rb") as image_file:
image_base64 = base64.b64encode(image_file.read()).decode()
Encode pesan
response = requests.post("http://localhost:5000/encode",
json={
"image": image_base64,
"message": "Pesan rahasia"
})  

## Struktur Proyek

image-steganography/
├── api.py # Server Flask dan endpoint API
├── imgstegno.py # Implementasi fungsi steganografi
├── test_simple.py # Script testing API
├── test.html # Antarmuka web
└── requirements.txt # Dependencies

## Batasan

- Ukuran pesan yang dapat disembunyikan tergantung pada resolusi gambar
- Hanya mendukung gambar format PNG untuk output
- Perubahan pada gambar hasil (seperti kompresi) dapat merusak pesan tersembunyi

## Kontribusi

Kontribusi selalu diterima. Untuk perubahan besar, silakan buka issue terlebih dahulu untuk mendiskusikan perubahan yang diinginkan.

## Lisensi

[MIT License](LICENSE)
