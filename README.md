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
