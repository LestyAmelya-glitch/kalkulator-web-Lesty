from flask import Flask, render_template, request, jsonify
from utils.kalkulator import Kalkulator

# Inisialisasi Flask app
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Agar JSON support Bahasa Indonesia

# Inisialisasi Kalkulator
kalkulator = Kalkulator()

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Route utama - menampilkan halaman kalkulator"""
    return render_template('index.html')

# ==================== OPERASI ARITMATIKA ====================

@app.route('/api/tambah', methods=['POST'])
def tambah():
    """API untuk penjumlahan"""
    data = request.json
    a = float(data.get('a'))
    b = float(data.get('b'))
    hasil = kalkulator.tambah(a, b)
    return jsonify(hasil)

@app.route('/api/kurang', methods=['POST'])
def kurang():
    """API untuk pengurangan"""
    data = request.json
    a = float(data.get('a'))
    b = float(data.get('b'))
    hasil = kalkulator.kurang(a, b)
    return jsonify(hasil)

@app.route('/api/kali', methods=['POST'])
def kali():
    """API untuk perkalian"""
    data = request.json
    a = float(data.get('a'))
    b = float(data.get('b'))
    hasil = kalkulator.kali(a, b)
    return jsonify(hasil)

@app.route('/api/bagi', methods=['POST'])
def bagi():
    """API untuk pembagian"""
    data = request.json
    a = float(data.get('a'))
    b = float(data.get('b'))
    hasil = kalkulator.bagi(a, b)
    return jsonify(hasil)

@app.route('/api/pangkat', methods=['POST'])
def pangkat():
    """API untuk pangkat"""
    data = request.json
    a = float(data.get('a'))
    b = float(data.get('b'))
    hasil = kalkulator.pangkat(a, b)
    return jsonify(hasil)

@app.route('/api/akar-kuadrat', methods=['POST'])
def akar_kuadrat():
    """API untuk akar kuadrat"""
    data = request.json
    a = float(data.get('a'))
    hasil = kalkulator.akar_kuadrat(a)
    return jsonify(hasil)

@app.route('/api/modulus', methods=['POST'])
def modulus():
    """API untuk modulus (sisa bagi)"""
    data = request.json
    a = float(data.get('a'))
    b = float(data.get('b'))
    hasil = kalkulator.modulus(a, b)
    return jsonify(hasil)

@app.route('/api/pembagian-bulat', methods=['POST'])
def pembagian_bulat():
    """API untuk pembagian bulat"""
    data = request.json
    a = float(data.get('a'))
    b = float(data.get('b'))
    hasil = kalkulator.pembagian_bulat(a, b)
    return jsonify(hasil)

# ==================== OPERASI LOGIKA ====================

@app.route('/api/dan-logika', methods=['POST'])
def dan_logika():
    """API untuk operasi AND"""
    data = request.json
    a = int(data.get('a'))
    b = int(data.get('b'))
    hasil = kalkulator.dan_logika(a, b)
    return jsonify(hasil)

@app.route('/api/atau-logika', methods=['POST'])
def atau_logika():
    """API untuk operasi OR"""
    data = request.json
    a = int(data.get('a'))
    b = int(data.get('b'))
    hasil = kalkulator.atau_logika(a, b)
    return jsonify(hasil)

@app.route('/api/tidak-logika', methods=['POST'])
def tidak_logika():
    """API untuk operasi NOT"""
    data = request.json
    a = int(data.get('a'))
    hasil = kalkulator.tidak_logika(a)
    return jsonify(hasil)

@app.route('/api/xor-logika', methods=['POST'])
def xor_logika():
    """API untuk operasi XOR"""
    data = request.json
    a = int(data.get('a'))
    b = int(data.get('b'))
    hasil = kalkulator.xor_logika(a, b)
    return jsonify(hasil)

@app.route('/api/nand-logika', methods=['POST'])
def nand_logika():
    """API untuk operasi NAND"""
    data = request.json
    a = int(data.get('a'))
    b = int(data.get('b'))
    hasil = kalkulator.nand_logika(a, b)
    return jsonify(hasil)

@app.route('/api/nor-logika', methods=['POST'])
def nor_logika():
    """API untuk operasi NOR"""
    data = request.json
    a = int(data.get('a'))
    b = int(data.get('b'))
    hasil = kalkulator.nor_logika(a, b)
    return jsonify(hasil)

# ==================== KONVERSI BASIS ====================

@app.route('/api/desimal-ke-biner', methods=['POST'])
def desimal_ke_biner():
    """API konversi Desimal ke Biner"""
    data = request.json
    n = data.get('n')
    hasil = kalkulator.desimal_ke_biner(n)
    return jsonify(hasil)

@app.route('/api/desimal-ke-oktal', methods=['POST'])
def desimal_ke_oktal():
    """API konversi Desimal ke Oktal"""
    data = request.json
    n = data.get('n')
    hasil = kalkulator.desimal_ke_oktal(n)
    return jsonify(hasil)

@app.route('/api/desimal-ke-heksa', methods=['POST'])
def desimal_ke_heksa():
    """API konversi Desimal ke Heksadesimal"""
    data = request.json
    n = data.get('n')
    hasil = kalkulator.desimal_ke_heksa(n)
    return jsonify(hasil)

@app.route('/api/biner-ke-desimal', methods=['POST'])
def biner_ke_desimal():
    """API konversi Biner ke Desimal"""
    data = request.json
    n = data.get('n')
    hasil = kalkulator.biner_ke_desimal(n)
    return jsonify(hasil)

@app.route('/api/oktal-ke-desimal', methods=['POST'])
def oktal_ke_desimal():
    """API konversi Oktal ke Desimal"""
    data = request.json
    n = data.get('n')
    hasil = kalkulator.oktal_ke_desimal(n)
    return jsonify(hasil)

@app.route('/api/heksa-ke-desimal', methods=['POST'])
def heksa_ke_desimal():
    """API konversi Heksadesimal ke Desimal"""
    data = request.json
    n = data.get('n')
    hasil = kalkulator.heksa_ke_desimal(n)
    return jsonify(hasil)

# ==================== KONVERSI SUHU ====================

@app.route('/api/celsius-ke-fahrenheit', methods=['POST'])
def celsius_ke_fahrenheit():
    """API konversi Celsius ke Fahrenheit"""
    data = request.json
    c = float(data.get('c'))
    hasil = kalkulator.celsius_ke_fahrenheit(c)
    return jsonify(hasil)

@app.route('/api/celsius-ke-kelvin', methods=['POST'])
def celsius_ke_kelvin():
    """API konversi Celsius ke Kelvin"""
    data = request.json
    c = float(data.get('c'))
    hasil = kalkulator.celsius_ke_kelvin(c)
    return jsonify(hasil)

@app.route('/api/celsius-ke-reamur', methods=['POST'])
def celsius_ke_reamur():
    """API konversi Celsius ke Reamur"""
    data = request.json
    c = float(data.get('c'))
    hasil = kalkulator.celsius_ke_reamur(c)
    return jsonify(hasil)

@app.route('/api/fahrenheit-ke-celsius', methods=['POST'])
def fahrenheit_ke_celsius():
    """API konversi Fahrenheit ke Celsius"""
    data = request.json
    f = float(data.get('f'))
    hasil = kalkulator.fahrenheit_ke_celsius(f)
    return jsonify(hasil)

@app.route('/api/kelvin-ke-celsius', methods=['POST'])
def kelvin_ke_celsius():
    """API konversi Kelvin ke Celsius"""
    data = request.json
    k = float(data.get('k'))
    hasil = kalkulator.kelvin_ke_celsius(k)
    return jsonify(hasil)

@app.route('/api/reamur-ke-celsius', methods=['POST'])
def reamur_ke_celsius():
    """API konversi Reamur ke Celsius"""
    data = request.json
    r = float(data.get('r'))
    hasil = kalkulator.reamur_ke_celsius(r)
    return jsonify(hasil)

# ==================== KONVERSI MATA UANG ====================

@app.route('/api/konversi-mata-uang', methods=['POST'])
def konversi_mata_uang():
    """API konversi mata uang"""
    data = request.json
    jumlah = float(data.get('jumlah'))
    dari = data.get('dari_mata_uang')
    ke = data.get('ke_mata_uang')
    hasil = kalkulator.konversi_mata_uang(jumlah, dari, ke)
    return jsonify(hasil)

# ==================== BONUS: FAKTORIAL & FIBONACCI ====================

@app.route('/api/faktorial', methods=['POST'])
def faktorial():
    """API untuk faktorial"""
    data = request.json
    n = int(data.get('n'))
    hasil = kalkulator.faktorial(n)
    return jsonify(hasil)

@app.route('/api/fibonacci', methods=['POST'])
def fibonacci():
    """API untuk deret Fibonacci"""
    data = request.json
    n = int(data.get('n'))
    hasil = kalkulator.fibonacci(n)
    return jsonify(hasil)

# ==================== HISTORY ====================

@app.route('/api/riwayat', methods=['GET'])
def get_riwayat():
    """API untuk mendapatkan riwayat perhitungan"""
    riwayat = kalkulator.lihat_riwayat()
    return jsonify({"riwayat": riwayat})

@app.route('/api/hapus-riwayat', methods=['POST'])
def hapus_riwayat():
    """API untuk menghapus riwayat"""
    hasil = kalkulator.hapus_riwayat()
    return jsonify(hasil)

# ==================== ERROR HANDLER ====================

@app.errorhandler(404)
def not_found(error):
    """Handler untuk route yang tidak ditemukan"""
    return jsonify({"error": "Route tidak ditemukan"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handler untuk error internal server"""
    return jsonify({"error": "Error internal server"}), 500

# ==================== RUN APP ====================

if __name__ == '__main__':
    # debug=True untuk development, nanti diubah ke False untuk production
    app.run(debug=True, host='localhost', port=5000)