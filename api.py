from flask import Flask, jsonify, request
from flask_cors import CORS
from imgstegno import encode_image_api, decode_image_api

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# API Documentation - Dokumentasi struktur dan endpoint API
API_DOCS = {
    "info": {
        "title": "Steganography API",
        "version": "1.0.0",
        "description": "API untuk menyembunyikan dan mengekstrak pesan dari gambar"
    },
    "endpoints": {
        "/": {
            "get": {
                "description": "Endpoint untuk mengecek status API",
                "responses": {
                    "200": {
                        "description": "API berjalan dengan baik",
                        "example": {
                            "status": "success",
                            "message": "Steganography API is running"
                        }
                    }
                }
            }
        },
        "/docs": {
            "get": {
                "description": "Menampilkan dokumentasi API",
                "responses": {
                    "200": {
                        "description": "Dokumentasi API berhasil ditampilkan"
                    }
                }
            }
        },
        "/encode": {
            "post": {
                "description": "Menyembunyikan pesan dalam gambar",
                "request_body": {
                    "required": True,
                    "content": {
                        "image": "string (base64 encoded image)",
                        "message": "string (pesan yang akan disembunyikan)"
                    }
                },
                "responses": {
                    "200": {
                        "description": "Pesan berhasil disembunyikan",
                        "example": {
                            "status": "success",
                            "encoded_image": "string (base64 encoded image)"
                        }
                    },
                    "400": {
                        "description": "Data tidak lengkap atau invalid"
                    }
                }
            }
        },
        "/decode": {
            "post": {
                "description": "Mengekstrak pesan dari gambar",
                "request_body": {
                    "required": True,
                    "content": {
                        "image": "string (base64 encoded image)"
                    }
                },
                "responses": {
                    "200": {
                        "description": "Pesan berhasil diekstrak",
                        "example": {
                            "status": "success",
                            "message": "string (pesan yang diekstrak)"
                        }
                    },
                    "400": {
                        "description": "Data tidak lengkap atau invalid"
                    }
                }
            }
        }
    }
}

@app.route('/', methods=['GET'])
def home():
    """Endpoint untuk mengecek apakah API berjalan"""
    return jsonify({"status": "success"})

@app.route('/docs', methods=['GET'])
def get_docs():
    """Endpoint untuk menampilkan dokumentasi API"""
    return jsonify(API_DOCS)

@app.route('/encode', methods=['POST'])
def encode():
    """
    Endpoint untuk menyembunyikan pesan dalam gambar
    Menerima: 
    - image: base64 string dari gambar
    - message: pesan yang akan disembunyikan
    """
    # Terima request dari client
    data = request.get_json()
    
    # Panggil fungsi dari imgstegno.py
    encoded_image = encode_image_api(data['image'], data['message'], 'output.png')
    
    # Kirim hasil ke client
    return jsonify({
        'status': 'success',
        'encoded_image': encoded_image
    })

@app.route('/decode', methods=['POST'])
def decode():
    """
    Endpoint untuk mengekstrak pesan dari gambar
    Menerima:
    - image: base64 string dari gambar yang berisi pesan
    """
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'Data tidak lengkap'}), 400
        
        # Decode gambar
        message = decode_image_api(data['image'])
        if message == "Tidak ada pesan tersembunyi atau format tidak sesuai":
            return jsonify({'error': message}), 400
        
        return jsonify({
            'status': 'success',
            'message': message
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)