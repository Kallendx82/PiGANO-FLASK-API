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

// Fungsi untuk menangani perubahan file input
function handleFileInputChange(inputElement, previewElement) {
    inputElement.addEventListener('change', function() {
        const file = this.files[0];
    });
}

// Modifikasi fungsi untuk menangani refresh
let touchStartY = 0;
let touchEndY = 0;

// Event listener untuk touch start
document.addEventListener('touchstart', function(e) {
    touchStartY = e.touches[0].clientY;
}, false);

// Event listener untuk touch move
document.addEventListener('touchmove', function(e) {
    touchEndY = e.touches[0].clientY;
}, false);

// Event listener untuk touch end
document.addEventListener('touchend', function() {
    const pullDistance = touchEndY - touchStartY;
    // Jika pull distance lebih dari 100px dan scroll sudah di paling atas
    if (pullDistance > 100 && window.scrollY <= 0) {
        handleRefresh();
    }
}, false);

// Fungsi untuk konfirmasi refresh
window.onbeforeunload = function(e) {
    const isProcessing = document.querySelector('#previewImage[style*="block"]') || 
                        document.querySelector('#result[style*="block"]');
    
    // Hanya tampilkan konfirmasi jika refresh dilakukan dengan cara lain
    // (misalnya melalui shortcut keyboard atau menu browser)
    if (isProcessing) {
        const message = 'Proses yang sedang berlangsung saat ini akan menghapus perubahan yang belum disimpan';
        e.returnValue = message;
        return message;
    }
};

// Event listener saat DOM loaded
document.addEventListener('DOMContentLoaded', function() {
    // Inisialisasi handler untuk file input
    const encodeFileInput = document.getElementById('encodeFile');
    const decodeFileInput = document.getElementById('decodeFile');
    const previewDiv = document.getElementById('previewImage');
    const resultDiv = document.getElementById('result');

    handleFileInputChange(encodeFileInput, previewDiv);
    handleFileInputChange(decodeFileInput, resultDiv);
    
    checkFolders();
});

// Event handler untuk form encode
document.getElementById('encodeForm').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const file = formData.get('file');
    
    const fileInput = document.getElementById('encodeFile');
    const maxSize = 10 * 1024 * 1024; // 10MB

    if (file.size > maxSize) {
        alert('Pilih file lain dengan ukuran kurang dari 10MB');
        return false;
    }
    
    const previewDiv = document.getElementById('previewImage');
    const downloadBtn = document.getElementById('downloadBtn');
    previewDiv.style.display = 'block';
    downloadBtn.style.display = 'none';
    previewDiv.innerHTML = '<p>Sedang memproses...</p>';
    
    // Upload file terlebih dahulu
    const uploadedFilename = await uploadFile(file);
    if (!uploadedFilename) {
        previewDiv.style.display = 'none';
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
                
                // Update preview dengan gambar hasil dan tombol download
                previewDiv.innerHTML = `
                    <h4>Gambar Hasil Encode:</h4>
                    <img id="encodedImage" style="max-width: 100%; height: auto;" src="${url}" />
                    <div style="margin-top: 10px;">
                        <button id="downloadBtn" class="btn-download" style="background-color: #28a745;">
                            Download Gambar
                        </button>
                    </div>
                `;

                // Tambahkan event listener untuk tombol download
                document.getElementById('downloadBtn').onclick = () => {
                    const a = document.createElement('a');
                    a.href = url;
                    // Dapatkan nama file asli dari input
                    const originalFileName = document.getElementById('encodeFile').files[0].name;
                    const baseName = originalFileName.split('.')[0]; // Ambil nama tanpa ekstensi
                    a.download = `encoded_${baseName}.png`;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                };
                
                document.getElementById('showCipherBtn').style.display = 'inline-block';
            } else {
                const errorText = await response.text();
                previewDiv.style.display = 'none';
                if (errorText.includes('image is truncated')) {
                    alert('Pilih file lain dengan ukuran kurang dari 10MB');
                } else {
                    alert('Error: ' + errorText);
                }
            }
        } else {
            const errorText = await response.text();
            previewDiv.style.display = 'none';
            if (errorText.includes('image is truncated')) {
                alert('Pilih file lain dengan ukuran kurang dari 10MB');
            } else {
                alert('Error: ' + errorText);
            }
        }
    } catch (error) {
        previewDiv.style.display = 'none';
        if (error.message.includes('image is truncated')) {
            alert('Pilih file lain dengan ukuran kurang dari 10MB');
        } else {
            alert('Error: ' + error);
        }
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
    const fileInput = document.getElementById('decodeFile');
    const file = fileInput.files[0];
    const maxSize = 10 * 1024 * 1024; // 10MB

    if (file.size > maxSize) {
        alert('Pilih file lain dengan ukuran kurang dari 10MB');
        return false;
    }

    const formData = new FormData(e.target);
    const resultDiv = document.getElementById('result');
    
    try {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = '<p>Sedang memproses...</p>';

        const response = await fetch('/decode', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            resultDiv.innerHTML = `
                <h3>Hasil Dekripsi:</h3>
                <p><strong>Cipher text:</strong> ${data.cipher_text}</p>
                <p><strong>Plain text:</strong> ${data.plain_text}</p> 
            `;
        } else {
            const errorText = await response.text();
            resultDiv.style.display = 'none';
            if (errorText.includes('image is truncated')) {
                alert('Pilih file lain dengan ukuran kurang dari 10MB');
            } else {
                alert('Error: ' + errorText);
            }
        }
    } catch (error) {
        resultDiv.style.display = 'none';
        if (error.message.includes('image is truncated')) {
            alert('Pilih file lain dengan ukuran kurang dari 10MB');
        } else {
            alert('Error: ' + error);
        }
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
