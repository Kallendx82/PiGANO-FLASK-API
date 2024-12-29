from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
from imgstegno import encrypt_message, encode_image, decode_image, decrypt_message
from cryptography import encrypt_text, decrypt_text
from functools import wraps
import sqlite3
from data import load_locations

app = Flask(__name__, static_folder='static')

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

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stegano')
def stegano_page():
    return render_template('stegano.html')

@app.route('/crypto')
def crypto_page():
    return render_template('crypto.html')

@app.route('/encrypt')
def encrypt_page():
    return render_template('encrypt.html')

@app.route('/decrypt')
def decrypt_page():
    return render_template('decrypt.html')

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
        return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
    
    file = request.files['file']
    key = int(request.form.get('key', 0))
    
    if file.filename == '':
        return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        try:
            # Decode dan dekripsi pesan
            encoded_message = decode_image(input_path)
            if encoded_message == "Tidak ada pesan tersembunyi atau format tidak sesuai":
                return jsonify({'error': encoded_message}), 400
            
            decrypted_message = decrypt_message(encoded_message, key)
            return jsonify({
                'cipher_text': encoded_message,
                'plain_text': decrypted_message
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        finally:
            # Bersihkan file temporary
            if os.path.exists(input_path):
                os.remove(input_path)
    
    return jsonify({'error': 'Format file tidak diizinkan'}), 400

@app.route('/encrypt_text', methods=['POST'])
def encrypt_text_route():
    data = request.json
    text = data.get('text', '')
    key = data.get('key', 0)
    
    try:
        encrypted_text = encrypt_text(text, key)
        return jsonify({'encrypted_text': encrypted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/decrypt_text', methods=['POST'])
def decrypt_text_route():
    data = request.json
    text = data.get('text', '')
    key = data.get('key', 0)
    
    try:
        decrypted_text = decrypt_text(text, key)
        return jsonify({'decrypted_text': decrypted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        user = c.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and user[3] == password:  # Dalam produksi, gunakan password hashing!
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('profile_page'))
        else:
            return render_template('login.html', error='Username atau password salah')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return render_template('register.html', error='Password tidak cocok')
        
        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                     (username, email, password))  # Dalam produksi, hash password!
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', error='Username atau email sudah digunakan')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html')

@app.route('/select_profile_picture', methods=['GET'])
def select_profile_picture():
    return render_template('select_profile_picture.html')

# Inisialisasi database saat aplikasi dimulai
with app.app_context():
    init_db()

# Tambahkan secret key untuk session
app.secret_key = 'your-secret-key-here'  # Ganti dengan secret key yang aman!

# Memuat lokasi dari file
locations = load_locations('lokasi.txt')

@app.route('/get_locations', methods=['GET'])
def get_locations():
    return jsonify(locations)

@app.route('/upload_profile_image', methods=['POST'])
def upload_profile_image():
    if 'profileImage' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['profileImage']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True) 