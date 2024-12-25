import requests
import base64
import sys

def test_connection():
    """Test koneksi ke API"""
    try:
        response = requests.get('http://localhost:5000/')
        if response.status_code == 200:
            print("API berjalan dengan baik!")
            return True
        else:
            print(f"API error dengan status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Tidak dapat terhubung ke API. Pastikan server sedang berjalan.")
        return False

def test_steganography():
    # Test koneksi terlebih dahulu
    if not test_connection():
        sys.exit(1)
        
    # URL API
    base_url = "http://localhost:5000"
    
    try:
        # Baca gambar dan konversi ke base64
        with open("upi.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        # Data untuk encode
        encode_data = {
            "image": encoded_string,
            "message": "Pesan rahasia"
        }
        
        # Kirim request untuk encode
        print("Mengirim pesan untuk dienkripsi...")
        response = requests.post(f"{base_url}/encode", json=encode_data)
        
        if response.status_code == 200:
            result = response.json()
            print("Pesan berhasil disembunyikan!")
            
            # Simpan gambar hasil encode
            img_data = base64.b64decode(result['encoded_image'])
            with open("encoded_image.png", "wb") as f:
                f.write(img_data)
            
            # Data untuk decode
            decode_data = {
                "image": result['encoded_image']
            }
            
            # Kirim request untuk decode
            print("\nMencoba mengekstrak pesan...")
            response = requests.post(f"{base_url}/decode", json=decode_data)
            
            if response.status_code == 200:
                result = response.json()
                print("Pesan berhasil diekstrak!")
                print(f"Pesan: {result['message']}")
            else:
                print(f"Error saat decode: {response.json()['error']}")
        else:
            print(f"Error saat encode: {response.json()['error']}")
    except Exception as e:
        print(f"Terjadi error: {str(e)}")

if __name__ == "__main__":
    test_steganography() 