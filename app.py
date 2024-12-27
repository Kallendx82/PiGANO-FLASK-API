from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
from imgstegno import encrypt_message, encode_image, decode_image, decrypt_message

app = Flask(__name__)

# Konfigurasi upload folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Buat folder jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"}), 200

@app.route('/encode', methods=['POST'])
def encode():
    if 'file' not in request.files:
        return 'Tidak ada file yang diunggah', 400
    
    file = request.files['file']
    message = request.form.get('message', '')
    key = int(request.form.get('key', 0))
    
    if file.filename == '':
        return 'Tidak ada file yang dipilih', 400
    
    if file and allowed_file(file.filename):
        # Simpan file yang diunggah
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Proses enkripsi dan encoding
        encrypted_message = encrypt_message(message, key)
        output_filename = f'encoded_{filename.rsplit(".", 1)[0]}.png'
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        try:
            result = encode_image(input_path, encrypted_message, output_path)
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return str(e), 400
        finally:
            # Bersihkan file temporary
            if os.path.exists(input_path):
                os.remove(input_path)
    
    return 'Format file tidak diizinkan', 400

@app.route('/decode', methods=['POST'])
def decode():
    if 'file' not in request.files:
        return 'Tidak ada file yang diunggah', 400
    
    file = request.files['file']
    key = int(request.form.get('key', 0))
    
    if file.filename == '':
        return 'Tidak ada file yang dipilih', 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        try:
            # Decode dan dekripsi pesan
            encoded_message = decode_image(input_path)
            if encoded_message == "Tidak ada pesan tersembunyi atau format tidak sesuai":
                return encoded_message
            
            decrypted_message = decrypt_message(encoded_message, key)
            return {'cipher_text': encoded_message, 'plain_text': decrypted_message}
        except Exception as e:
            return str(e), 400
        finally:
            # Bersihkan file temporary
            if os.path.exists(input_path):
                os.remove(input_path)
    
    return 'Format file tidak diizinkan', 400

if __name__ == '__main__':
    app.run(debug=True) 