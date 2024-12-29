from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import logging
import subprocess
from imgstegno import encrypt_message, encode_image, decode_image, decrypt_message

app = Flask(__name__)

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Konfigurasi folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')

# Buat folder jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Set permission folder berdasarkan sistem operasi
if os.name == 'nt':  # Untuk Windows
    try:
        # Jalankan icacls untuk memberikan full permission
        subprocess.run(['icacls', UPLOAD_FOLDER, '/grant', 'Everyone:(OI)(CI)F'], check=True)
        subprocess.run(['icacls', OUTPUT_FOLDER, '/grant', 'Everyone:(OI)(CI)F'], check=True)
        logger.info("Permission folder berhasil diatur untuk Windows")
    except Exception as e:
        logger.error(f"Error saat mengatur permission folder: {str(e)}")
else:  # Untuk Unix/Linux
    try:
        os.chmod(UPLOAD_FOLDER, 0o777)
        os.chmod(OUTPUT_FOLDER, 0o777)
        logger.info("Permission folder berhasil diatur untuk Unix/Linux")
    except Exception as e:
        logger.error(f"Error saat mengatur permission folder: {str(e)}")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

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
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Proses enkripsi dan encoding
        encrypted_message = encrypt_message(message, key)
        output_filename = f'encoded_{filename.rsplit(".", 1)[0]}.png'
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        try:
            result = encode_image(input_path, encrypted_message, output_path)
            return send_file(
                output_path,
                mimetype='image/png',
                as_attachment=True,
                download_name=output_filename
            )
        except Exception as e:
            return str(e), 400
    
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
    
    return 'Format file tidak diizinkan', 400

@app.route('/get-cipher', methods=['POST'])
def get_cipher():
    if 'file' not in request.files:
        return 'Tidak ada file yang diunggah', 400
    
    file = request.files['file']
    message = request.form.get('message', '')
    key = int(request.form.get('key', 0))
    
    if file.filename == '':
        return 'Tidak ada file yang dipilih', 400
    
    if file and allowed_file(file.filename):
        # Hanya enkripsi pesan tanpa menyimpan gambar
        encrypted_message = encrypt_message(message, key)
        return jsonify({'cipher_text': encrypted_message})
    
    return 'Format file tidak diizinkan', 400

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return jsonify({
            'success': True,
            'message': 'File berhasil diunggah',
            'filename': filename
        }), 200
    
    return jsonify({'error': 'Format file tidak diizinkan'}), 400

@app.route('/check-folders')
def check_folders():
    upload_exists = os.path.exists(app.config['UPLOAD_FOLDER'])
    upload_writable = os.access(app.config['UPLOAD_FOLDER'], os.W_OK)
    
    return jsonify({
        'upload_folder_exists': upload_exists,
        'upload_folder_writable': upload_writable,
        'upload_folder_path': app.config['UPLOAD_FOLDER']
    })

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        image = request.files['image']
        
        if image.content_length > 10 * 1024 * 1024:  # 10MB
            return jsonify({'error': 'File size must not exceed 10MB'}), 400

        key = request.form.get('key')

        if not key:
            return jsonify({'error': 'Key is required'}), 400

        try:
            key = int(key)
        except ValueError:
            return jsonify({'error': 'Key must be an integer'}), 400

        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)

        encrypted_message = decode_image(image_path)
        if encrypted_message == "Tidak ada pesan tersembunyi atau format tidak sesuai":
            return jsonify({'error': encrypted_message}), 400

        decrypted_message = decrypt_message(encrypted_message, key)

        return jsonify({'message': 'Decryption successful', 'decrypted_message': decrypted_message}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 