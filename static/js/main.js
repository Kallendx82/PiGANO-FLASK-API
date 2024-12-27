// Fungsi untuk upload file
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        if (response.ok) {
            console.log('File berhasil diunggah:', data.filename);
            return data.filename;
        } else {
            throw new Error(data.error || 'Gagal mengunggah file');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Gagal mengunggah file: ' + error.message);
        return null;
    }
}

// Event handler untuk form encode
document.getElementById('encodeForm').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const file = formData.get('file');
    
    // Upload file terlebih dahulu
    const uploadedFilename = await uploadFile(file);
    if (!uploadedFilename) {
        return; // Berhenti jika upload gagal
    }
    
    try {
        const response = await fetch('/encode', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const contentType = response.headers.get('content-type');
            
            if (contentType && contentType.includes('image/png')) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                
                const previewDiv = document.getElementById('previewImage');
                const previewImg = document.getElementById('encodedImage');
                previewImg.src = url;
                previewDiv.style.display = 'block';
                
                const a = document.createElement('a');
                a.href = url;
                a.download = 'encoded_image.png';
                document.body.appendChild(a);
                a.click();
                a.remove();
                
                document.getElementById('showCipherBtn').style.display = 'inline-block';
            } else {
                const errorText = await response.text();
                alert('Error: ' + errorText);
            }
        } else {
            const errorText = await response.text();
            alert('Error: ' + errorText);
        }
    } catch (error) {
        alert('Error: ' + error);
    }
};

// Event handler untuk tombol Show Cipher
document.getElementById('showCipherBtn').onclick = async () => {
    const formData = new FormData(document.getElementById('encodeForm'));
    
    try {
        const response = await fetch('/get-cipher', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            const cipherResult = document.getElementById('cipherResult');
            const cipherText = document.getElementById('cipherText');
            cipherText.textContent = data.cipher_text;
            cipherResult.style.display = 'block';
        } else {
            const errorText = await response.text();
            alert('Error: ' + errorText);
        }
    } catch (error) {
        alert('Error: ' + error);
    }
};

// Event handler untuk form decode
document.getElementById('decodeForm').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const resultDiv = document.getElementById('result');
    
    try {
        const response = await fetch('/decode', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <h3>Hasil Dekripsi:</h3>
                <p><strong>Cipher text:</strong> ${data.cipher_text}</p>
                <p><strong>Plain text:</strong> ${data.plain_text}</p> 
            `;
        } else {
            alert('Error: ' + await response.text());
        }
    } catch (error) {
        alert('Error: ' + error);
    }
};

// Fungsi untuk mengecek status folder
async function checkFolders() {
    try {
        const response = await fetch('/check-folders');
        const data = await response.json();
        console.log('Status folder:', data);
    } catch (error) {
        console.error('Error checking folders:', error);
    }
}

// Event listener saat DOM loaded
document.addEventListener('DOMContentLoaded', checkFolders);
