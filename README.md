# PiGANO

## Deskripsi
PiGANO adalah aplikasi web untuk menyembunyikan pesan rahasia ke dalam gambar menggunakan teknik steganografi. Aplikasi ini memungkinkan pengguna untuk mengenkripsi pesan ke dalam gambar dan mendekripsi pesan dari gambar yang telah dienkripsi.

---

## Fitur Utama

### 1. **Encode Pesan**
- Upload gambar (format: `.png`, `.jpg`, atau `.jpeg`)
- Masukkan pesan yang akan disembunyikan
- Masukkan kunci numerik untuk enkripsi
- Preview gambar hasil encode
- Download gambar hasil encode
- Lihat cipher text hasil enkripsi
- Batasan ukuran file: maksimal 10MB

### 2. **Decode Pesan**
- Upload gambar yang berisi pesan tersembunyi (format: `.png`)
- Masukkan kunci numerik untuk dekripsi
- Tampilkan hasil dekripsi (cipher text dan plain text)
- Batasan ukuran file: maksimal 10MB

---

## Endpoint API

### 1. **Encode Image (`/encode`)**
- **Metode:** POST
- **Request Body (multipart/form-data):**
  - `file`: File gambar
  - `message`: Pesan yang akan disembunyikan
  - `key`: Kunci numerik
- **Response:**
  - File gambar hasil encode (format PNG)

### 2. **Decode Image (`/decode`)**
- **Metode:** POST
- **Request Body (multipart/form-data):**
  - `file`: File gambar
  - `key`: Kunci numerik
- **Response:**
  ```json
  {
    "cipher_text": "Pesan terenkripsi",
    "plain_text": "Pesan asli"
  }
  ```

### 3. **Get Cipher Text (`/get-cipher`)**
- **Metode:** POST
- **Request Body (multipart/form-data):**
  - `file`: File gambar
  - `message`: Pesan
  - `key`: Kunci numerik
- **Response:**
  ```json
  {
    "cipher_text": "Pesan terenkripsi"
  }
  ```

---

## Batasan dan Keamanan
- Ukuran file maksimal: 10MB
- Format file yang didukung:
  - Input: PNG, JPG, JPEG
  - Output: Selalu PNG untuk menjaga kualitas
- Validasi input untuk mencegah file berbahaya
- Pengecekan integritas file sebelum pemrosesan

---

## Teknologi yang Digunakan
- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Image Processing: PIL (Python Imaging Library)
- File Handling: Werkzeug

---

## Catatan Penggunaan
1. Pastikan menggunakan kunci sama saat encode dan decode
2. Simpan kunci dengan aman karena diperlukan untuk mendekripsi pesan, dan kunci tidak dapat dikembalikan.
3. Gambar hasil encode akan selalu dalam format PNG
4. Jika terjadi error saat decode, pastikan:
   - File yang diupload adalah file hasil encode
   - Menggunakan kunci yang benar
   - Format file adalah PNG
   - Ukuran file tidak melebihi 10megabyte
5. Jika ingin menggunakan kunci yang berbeda, maka kunci yang digunakan saat encode dan decode harus berbeda.
6. Berikan clue kepada target, agar target mengetahui kunci yang digunakan.
7. Bersihkan cache browser, agar tidak ada data yang tersimpan di browser.

---

## Keamanan
- Pesan dienkripsi sebelum disembunyikan dalam gambar
- Kunci numerik diperlukan untuk enkripsi dan dekripsi
- Tidak ada penyimpanan pesan atau kunci di server
- Validasi file untuk mencegah serangan berbasis file
- Lindungi kunci dengan baik, agar informasi rahasia tidak dapat dibuka oleh orang lain yang tidak berhak.
- Samarkan nama file yang diupload, agar tidak mencurigakan, dan menjadi sasaran serangan.

## Kontak:
- Email: [rajihnibras@gmail.com]/[iel.auriel25@upi.edu]
- Instagram: [@rajih.nm]/[_auriel_03]
- Github: [Kallendx82]/[AurielILearnHowToCode]

## Struktur File

### 1. `app.py`
File utama aplikasi Flask yang menangani:
- Routing dan endpoint API
- Penanganan request dari client
- Manajemen file upload/download
- Integrasi dengan fungsi steganografi
- Konfigurasi server dan CORS

### 2. `imgstegno.py`
File yang berisi implementasi steganografi:
- Fungsi enkripsi dan dekripsi pesan
- Fungsi encode pesan ke dalam gambar
- Fungsi decode pesan dari gambar
- Implementasi algoritma substitusi dan Caesar cipher
- Penanganan manipulasi pixel gambar

### 3. `templates/index.html`
File template utama yang menampilkan:
- Interface pengguna (UI)
- Form untuk encode dan decode
- Preview gambar hasil
- Tampilan hasil enkripsi/dekripsi
- Styling CSS untuk tampilan aplikasi

### 4. `static/js/main.js`
File JavaScript yang menangani:
- Interaksi client-side
- AJAX requests ke server
- Validasi input pengguna
- Penanganan file upload
- Preview dan download hasil
- Manajemen tampilan dinamis

### 5. `requirements.txt`
File yang berisi daftar dependensi Python:
- Flask: Web framework
- Pillow: Library pengolahan gambar
- Flask-CORS: Penanganan Cross-Origin Resource Sharing
- Werkzeug: Utilitas WSGI
- Dependensi lain yang diperlukan

### 6. Folder `uploads/`
Folder yang digunakan untuk:
- Menyimpan file gambar sementara yang diupload pengguna
- Menampung file sebelum diproses encode/decode
- File dalam folder ini akan dihapus secara otomatis
- Memastikan penanganan file yang aman

### 7. Folder `outputs/`
Folder yang digunakan untuk:
- Menyimpan hasil gambar yang telah di-encode
- Tempat penyimpanan sementara sebelum file didownload
- File akan dihapus setelah didownload
- Memastikan hasil encode dapat diakses pengguna

Setiap file memiliki peran penting dalam menjalankan aplikasi PiGANO secara keseluruhan, mulai dari backend processing hingga frontend interface.
