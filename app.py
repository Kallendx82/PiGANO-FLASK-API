from flask import Flask, render_template, request, jsonify, send_file, make_response, send_from_directory
from flask_cors import CORS
from imgstegno import encrypt_message, decrypt_message, encode_image, decode_image
import os

app = Flask(__name__)
CORS(app)  # Allow CORS from all sources

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "service": "PiGANO API",
        "status": "API is running",
        "version": "1.0",
        "connection": {
            "type": "Flask Web Server",
            "port": 5000,
            "host": "localhost",
            "framework": "Flask (Python)",
            "database": "No Database Required",
            "service_type": "Image Steganography Service"
        }
    }), 200

@app.route('/encode', methods=['POST'])
def encrypt():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        image = request.files['image']
        message = request.form.get('message')
        key = request.form.get('key')

        if not message or not key:
            return jsonify({'error': 'Message and key are required'}), 400

        try:
            key = int(key)
        except ValueError:
            return jsonify({'error': 'Key must be an integer'}), 400

        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)

        encrypted_message = encrypt_message(message, key)

        output_image_name = f"encoded_{image.filename.rsplit('.', 1)[0]}.png"
        output_image_path = os.path.join(RESULT_FOLDER, output_image_name)
        mse, psnr = encode_image(image_path, encrypted_message, output_image_path)

        response = {
            'ciphertext': encrypted_message,
            'filename': output_image_name,
            'mse': mse,
            'psnr': psnr
        }
        # Return JSON response
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/decode', methods=['POST'])
def decrypt():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        image = request.files['file']
        
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

        encoded_message = decode_image(image_path)
        if encoded_message == "Tidak ada pesan tersembunyi atau format tidak sesuai":
            return jsonify({'error': encoded_message}), 400

        decrypted_message = decrypt_message(encoded_message, key)

        return {'cipher_text': encoded_message, 'plain_text': decrypted_message}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        filename = data.get('filename') if data else None
        if not filename:
            return jsonify({'error': 'Filename is required'}), 400
        
        file_path = os.path.join(RESULT_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

for rule in app.url_map.iter_rules():
    print(f"Endpoint: {rule.endpoint}, URL: {rule}")

if __name__ == '__main__':
    app.run(debug=True)
