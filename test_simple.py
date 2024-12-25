import requests
import base64

def test_api():
    # URL API
    base_url = "http://localhost:5000"
    
    # 1. Test endpoint root
    response = requests.get(base_url)
    print("Root endpoint:", response.json())
    
    # 2. Test encode
    # Baca gambar
    with open("upi.jpg", "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode()
    
    # Data untuk encode
    encode_data = {
        "image": image_base64,
        "message": "Pesan rahasia"
    }
    
    # Kirim request encode
    print("\nMencoba encode...")
    response = requests.post(f"{base_url}/encode", json=encode_data)
    
    if response.status_code == 200:
        result = response.json()
        print("Encode berhasil!")
        
        # Simpan gambar hasil
        img_data = base64.b64decode(result['encoded_image'])
        with open("hasil_encode.png", "wb") as f:
            f.write(img_data)
        print("Gambar tersimpan sebagai hasil_encode.png")
        
        # 3. Test decode
        decode_data = {
            "image": result['encoded_image']
        }
        
        print("\nMencoba decode...")
        response = requests.post(f"{base_url}/decode", json=decode_data)
        
        if response.status_code == 200:
            result = response.json()
            print("Decode berhasil!")
            print("Pesan:", result['message'])
        else:
            print("Error decode:", response.json().get('error'))
    else:
        print("Error encode:", response.json().get('error'))

if __name__ == "__main__":
    test_api() 