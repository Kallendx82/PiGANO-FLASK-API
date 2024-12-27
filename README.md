# Dokumentasi Endpoint API

## Deskripsi
API ini menyediakan layanan untuk melakukan enkripsi dan dekripsi pesan pada file gambar menggunakan teknik steganografi. Ini adalah dokumentasi untuk endpoint yang tersedia, pengaturan CORS, dan fitur lainnya.

---

## Endpoint API

### 1. **Encrypt Message**
- **Endpoint:** `/encrypt`
- **Metode:** POST
- **Deskripsi:** Meng-enkripsi pesan ke dalam file gambar.
- **Request:**
  - **Headers:**
    - `Content-Type: multipart/form-data`
  - **Body:**
    - `file`: File gambar (format: `.png`, `.jpg`, atau `.jpeg`).
    - `message`: Pesan teks yang akan dienkripsi.
- **Response:**
  - **200 OK**:
    ```json
    {
      "status": "success",
      "message": "Encryption successful",
      "encrypted_file": "<nama_file_terenkripsi>"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "status": "error",
      "message": "Invalid file or parameters"
    }
    ```

### 2. **Decrypt Message**
- **Endpoint:** `/decrypt`
- **Metode:** POST
- **Deskripsi:** Mendekripsi pesan dari file gambar.
- **Request:**
  - **Headers:**
    - `Content-Type: multipart/form-data`
  - **Body:**
    - `file`: File gambar yang berisi pesan terenkripsi.
- **Response:**
  - **200 OK**:
    ```json
    {
      "status": "success",
      "message": "<pesan_terenkripsi>"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "status": "error",
      "message": "Invalid file"
    }
    ```

---

## Pengaturan CORS
Untuk mengatur agar API ini dapat diakses dari semua sumber URL, gunakan pustaka `flask-cors`. Tambahkan konfigurasi berikut di file utama:

```python
from flask_cors import CORS

# Mengaktifkan CORS
CORS(app, resources={r"/*": {"origins": "*"}})
```

---

## Kustomisasi Nama File
Agar API mendukung semua nama file gambar, logika berikut digunakan:

1. Ketika file diunggah:
   - API secara otomatis menyimpan file dengan nama yang diunggah.
   - Format file dicek untuk memastikan kompatibilitas (.png, .jpg, .jpeg).

2. Contoh implementasi:
   ```python
   from werkzeug.utils import secure_filename

   @app.route('/encrypt', methods=['POST'])
   def encrypt():
       file = request.files['file']
       filename = secure_filename(file.filename)
       file.save(os.path.join('uploads', filename))
       # Proses enkripsi di sini
       return jsonify({"status": "success", "encrypted_file": filename})
   ```

---

## Catatan Keamanan
Untuk memastikan keamanan tambahan:
- Jangan tampilkan detail kunci atau metode enkripsi dalam pesan respon API.
- Kembalikan hanya hasil akhir (contohnya nama file terenkripsi atau pesan dekripsi).

Contoh response hasil akhir:
```json
{
  "status": "success",
  "message": "Decryption successful",
  "result": "<pesan_terenkripsi>"
}
