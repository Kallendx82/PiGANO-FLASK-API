from PIL import Image
import base64
import io

def encode_image_api(image_data, message, output_filename):
    """
    Fungsi untuk menyembunyikan pesan dalam gambar
    
    Args:
        image_data: String base64 dari gambar input
        message: Pesan yang akan disembunyikan
        output_filename: Nama file output (tidak digunakan dalam versi API)
    
    Returns:
        String base64 dari gambar yang sudah berisi pesan
    """
    # Konversi string base64 menjadi gambar
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    
    # Tambahkan marker '$$' di akhir pesan untuk menandai akhir pesan
    message = message + "$$"
    
    # Buat salinan gambar untuk dimodifikasi
    encoded_image = image.copy()
    pixels = encoded_image.load()
    width, height = image.size
    
    # Konversi setiap karakter pesan menjadi 8-bit binary
    # Contoh: 'A' (65 dalam ASCII) -> '01000001'
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_length = len(binary_message)
    
    # Cek apakah pesan terlalu panjang
    if binary_length > width * height * 3:
        raise ValueError("Pesan terlalu panjang untuk gambar ini")
    
    # Proses penyembunyian pesan
    idx = 0
    for y in range(height):
        for x in range(width):
            if idx < binary_length:
                r, g, b = pixels[x, y]
                # Modifikasi bit terakhir (LSB) dari setiap komponen RGB
                if idx < binary_length:
                    # Contoh: jika r=200 (11001000) dan bit pesan=1
                    # r & ~1 = 11001000 & 11111110 = 11001000 (hapus bit terakhir)
                    # | int(bit) = 11001000 | 00000001 = 11001001
                    r = (r & ~1) | int(binary_message[idx])
                    idx += 1
                if idx < binary_length:
                    g = (g & ~1) | int(binary_message[idx])
                    idx += 1
                if idx < binary_length:
                    b = (b & ~1) | int(binary_message[idx])
                    idx += 1
                pixels[x, y] = (r, g, b)
            else:
                break
    
    # Konversi gambar hasil ke base64
    buffered = io.BytesIO()
    encoded_image.save(buffered, format="PNG")
    encoded_image_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return encoded_image_base64

def decode_image_api(image_data):
    """
    Fungsi untuk mengekstrak pesan tersembunyi dari gambar
    
    Args:
        image_data: String base64 dari gambar yang berisi pesan
    
    Returns:
        String pesan yang berhasil diekstrak atau pesan error
    """
    # Konversi string base64 menjadi gambar
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    
    pixels = image.load()
    width, height = image.size
    
    # Ekstrak bit terakhir (LSB) dari setiap komponen RGB
    binary_data = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            # Ambil bit terakhir dari setiap komponen RGB
            # Contoh: 201 (11001001) & 1 = 00000001 = 1
            binary_data += str(r & 1)  # Ambil LSB dari Red
            binary_data += str(g & 1)  # Ambil LSB dari Green
            binary_data += str(b & 1)  # Ambil LSB dari Blue
    
    # Konversi binary ke teks
    decoded_data = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) == 8:
            try:
                # Konversi 8 bit ke karakter
                # Contoh: '01000001' -> 65 -> 'A'
                char = chr(int(byte, 2))
                decoded_data += char
                # Cek apakah sudah mencapai marker '$$'
                if decoded_data[-2:] == "$$":
                    return decoded_data[:-2]  # Hapus marker
            except:
                break
    
    return "Tidak ada pesan tersembunyi atau format tidak sesuai"
