// ==================== FUNGSI ARITMATIKA ====================

async function hitungAritmatika() {
    const operasi = document.querySelector('input[name="operasi-aritmatika"]:checked').value;
    const single = ['akar-kuadrat'];
    
    let data;
    if (single.includes(operasi)) {
        const a = parseFloat(document.getElementById('aritmatika-single').value);
        if (isNaN(a)) {
            alert('Masukkan bilangan yang bener kocak!');
            return;
        }
        data = { a };
    } else {
        const a = parseFloat(document.getElementById('aritmatika-a').value);
        const b = parseFloat(document.getElementById('aritmatika-b').value);
        if (isNaN(a) || isNaN(b)) {
            alert('Masukkan bilangan yang bener kocak!');
            return;
        }
        data = { a, b };
    }

    try {
        const response = await fetch(`/api/${operasi}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        tampilkanHasil(result);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ==================== FUNGSI LOGIKA ====================

async function hitungLogika() {
    const operasi = document.querySelector('input[name="operasi-logika"]:checked').value;
    const single = ['tidak-logika'];
    
    let data;
    if (single.includes(operasi)) {
        const a = parseInt(document.getElementById('logika-single').value);
        if (isNaN(a) || (a !== 0 && a !== 1)) {
            alert('Masukkan 0 atau 1!');
            return;
        }
        data = { a };
    } else {
        const a = parseInt(document.getElementById('logika-a').value);
        const b = parseInt(document.getElementById('logika-b').value);
        if (isNaN(a) || isNaN(b) || (a !== 0 && a !== 1) || (b !== 0 && b !== 1)) {
            alert('Masukkan 0 atau 1!');
            return;
        }
        data = { a, b };
    }

    try {
        const response = await fetch(`/api/${operasi}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        tampilkanHasil(result);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ==================== FUNGSI KONVERSI BASIS ====================

async function hitungKonversiBasis() {
    const dari = document.getElementById('basis-dari').value;
    const ke = document.getElementById('basis-ke').value;
    const nilai = document.getElementById('basis-nilai').value;

    if (!nilai) {
        alert('Masukkan bilangan!');
        return;
    }

    const operasiMap = {
        'desimal-biner': 'desimal-ke-biner',
        'desimal-oktal': 'desimal-ke-oktal',
        'desimal-heksa': 'desimal-ke-heksa',
        'biner-desimal': 'biner-ke-desimal',
        'oktal-desimal': 'oktal-ke-desimal',
        'heksa-desimal': 'heksa-ke-desimal'
    };

    const key = `${dari}-${ke}`;
    const operasi = operasiMap[key];

    if (!operasi) {
        alert('Konversi tidak didukung!');
        return;
    }

    try {
        const response = await fetch(`/api/${operasi}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ n: nilai })
        });
        const result = await response.json();
        tampilkanHasil(result);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ==================== FUNGSI KONVERSI SUHU ====================

async function hitungKonversiSuhu() {
    const dari = document.getElementById('suhu-dari').value;
    const ke = document.getElementById('suhu-ke').value;
    const nilai = parseFloat(document.getElementById('suhu-nilai').value);

    if (isNaN(nilai)) {
        alert('Masukkan nilai suhu yang valid!');
        return;
    }

    const operasiMap = {
        'celsius-fahrenheit': 'celsius-ke-fahrenheit',
        'celsius-kelvin': 'celsius-ke-kelvin',
        'celsius-reamur': 'celsius-ke-reamur',
        'fahrenheit-celsius': 'fahrenheit-ke-celsius',
        'kelvin-celsius': 'kelvin-ke-celsius',
        'reamur-celsius': 'reamur-ke-celsius'
    };

    const key = `${dari}-${ke}`;
    const operasi = operasiMap[key];

    if (!operasi) {
        alert('Konversi tidak didukung!');
        return;
    }

    const paramMap = {
        'celsius-fahrenheit': 'c',
        'celsius-kelvin': 'c',
        'celsius-reamur': 'c',
        'fahrenheit-celsius': 'f',
        'kelvin-celsius': 'k',
        'reamur-celsius': 'r'
    };

    const param = paramMap[key];
    const data = { [param]: nilai };

    try {
        const response = await fetch(`/api/${operasi}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        tampilkanHasil(result);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ==================== FUNGSI KONVERSI MATA UANG ====================

async function hitungKonversiMatauang() {
    const dari = document.getElementById('mata-uang-dari').value;
    const ke = document.getElementById('mata-uang-ke').value;
    const jumlah = parseFloat(document.getElementById('mata-uang-nilai').value);

    if (isNaN(jumlah)) {
        alert('Masukkan jumlah yang valid!');
        return;
    }

    try {
        const response = await fetch('/api/konversi-mata-uang', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                jumlah: jumlah,
                dari_mata_uang: dari,
                ke_mata_uang: ke
            })
        });
        const result = await response.json();
        tampilkanHasil(result);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ==================== FUNGSI BONUS ====================

async function hitungBonus() {
    const operasi = document.querySelector('input[name="bonus-operasi"]:checked').value;
    const nilai = parseInt(document.getElementById('bonus-nilai').value);

    if (isNaN(nilai) || nilai < 0) {
        alert('Masukkan bilangan positif!');
        return;
    }

    try {
        const response = await fetch(`/api/${operasi}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ n: nilai })
        });
        const result = await response.json();
        tampilkanHasil(result);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ==================== FUNGSI DISPLAY HASIL ====================

function tampilkanHasil(result) {
    const resultSection = document.getElementById('result-section');
    const noResult = document.getElementById('no-result');

    if (result.error) {
        alert('Error: ' + result.error);
        return;
    }

    document.getElementById('result-formula').textContent = result.rumus || result.formula || '-';
    document.getElementById('result-value').textContent = result.hasil || result.result || '-';
    document.getElementById('result-explanation').textContent = result.penjelasan || result.explanation || '-';

    resultSection.style.display = 'block';
    noResult.style.display = 'none';
}

// ==================== FUNGSI HISTORY ====================

async function loadRiwayat() {
    try {
        const response = await fetch('/api/riwayat');
        const data = await response.json();
        const riwayat = data.riwayat;

        const historyBody = document.getElementById('history-body');
        
        if (riwayat.length === 0) {
            historyBody.innerHTML = '<tr><td colspan="4" class="text-center text-muted"><i class="fas fa-inbox"></i> Belum ada riwayat</td></tr>';
            return;
        }

        historyBody.innerHTML = riwayat.map(item => `
            <tr>
                <td><small>${item.waktu}</small></td>
                <td><strong>${item.rumus}</strong></td>
                <td><strong class="text-success">${item.hasil}</strong></td>
                <td><small>${item.penjelasan.substring(0, 50)}...</small></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function simpkeRiwayat() {
    alert('Hasil sudah disimpan ke riwayat!');
    loadRiwayat();
}

async function hapusRiwayat() {
    if (!confirm('Yakin ingin menghapus semua riwayat?')) return;

    try {
        await fetch('/api/hapus-riwayat', { method: 'POST' });
        alert('Riwayat berhasil dihapus!');
        loadRiwayat();
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ==================== DARK MODE ====================

const darkModeToggle = document.getElementById('darkModeToggle');
const htmlElement = document.documentElement;

// Check saved preference
if (localStorage.getItem('darkMode') === 'enabled') {
    htmlElement.setAttribute('data-bs-theme', 'dark');
    darkModeToggle.innerHTML = '<i class="fas fa-sun"></i> Light Mode';
}

darkModeToggle.addEventListener('click', function() {
    const isDark = htmlElement.getAttribute('data-bs-theme') === 'dark';
    
    if (isDark) {
        htmlElement.removeAttribute('data-bs-theme');
        darkModeToggle.innerHTML = '<i class="fas fa-moon"></i> Dark Mode';
        localStorage.setItem('darkMode', 'disabled');
    } else {
        htmlElement.setAttribute('data-bs-theme', 'dark');
        darkModeToggle.innerHTML = '<i class="fas fa-sun"></i> Light Mode';
        localStorage.setItem('darkMode', 'enabled');
    }
});

// Load riwayat on page load
document.addEventListener('DOMContentLoaded', function() {
    loadRiwayat();
});