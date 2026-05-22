# ============================================================
# app.py - File utama Flask
# Berisi semua route (URL) dan logika perhitungan backend
# ============================================================

from flask import Flask, render_template, request, jsonify
import math

# Membuat aplikasi Flask
app = Flask(__name__)

# ============================================================
# KURS MATA UANG (statis/ilustratif, bukan real-time)
# Semua dikonversi dari IDR
# ============================================================
KURS = {
    "IDR": 1,
    "USD": 1 / 16350,
    "EUR": 1 / 17800,
    "SGD": 1 / 12100,
    "JPY": 1 / 107,
    "MYR": 1 / 3700,
    "GBP": 1 / 20700,
    "AUD": 1 / 10400,
}

# ============================================================
# ROUTE UTAMA - Menampilkan halaman index.html
# ============================================================
@app.route("/")
def index():
    return render_template("index.html")

# ============================================================
# ROUTE ARITMATIKA
# Menerima: operator, nilai a, nilai b
# Mengembalikan: result, formula, steps (langkah-langkah)
# ============================================================
@app.route("/api/aritmatika", methods=["POST"])
def aritmatika():
    data = request.get_json()
    op = data.get("operator")

    # Ambil nilai a dan b dari request
    try:
        a = float(data.get("a", 0))
        b = float(data.get("b", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Input tidak valid"}), 400

    result, formula, steps = None, "", []

    try:
        if op == "tambah":
            result = a + b
            formula = f"{a} + {b} = {result}"
            steps = [f"Tambahkan {a} dan {b}", f"Hasil: {result}"]

        elif op == "kurang":
            result = a - b
            formula = f"{a} - {b} = {result}"
            steps = [f"Kurangkan {b} dari {a}", f"Hasil: {result}"]

        elif op == "kali":
            result = a * b
            formula = f"{a} x {b} = {result}"
            steps = [f"Kalikan {a} dengan {b}", f"Hasil: {result}"]

        elif op == "bagi":
            # Cegah pembagian dengan nol
            if b == 0:
                return jsonify({"error": "Tidak bisa membagi dengan nol"}), 400
            result = a / b
            formula = f"{a} / {b} = {result}"
            steps = [f"Bagi {a} dengan {b}", f"Hasil: {result}"]

        elif op == "pangkat":
            result = a ** b
            formula = f"{a} ^ {b} = {result}"
            steps = [f"Kalikan {a} sebanyak {int(b)} kali", f"Hasil: {result}"]

        elif op == "akar":
            # b = eksponen akar (default 2 = akar kuadrat)
            b = float(data.get("b", 2))
            if a < 0:
                return jsonify({"error": "Tidak bisa akar bilangan negatif"}), 400
            result = a ** (1 / b)
            formula = f"akar ke-{int(b)} dari {a} = {round(result, 6)}"
            steps = [f"Hitung {a} ^ (1/{int(b)})", f"Hasil: {round(result, 6)}"]

        elif op == "modulus":
            if b == 0:
                return jsonify({"error": "Modulus dengan nol tidak valid"}), 400
            result = a % b
            q = int(a // b)
            formula = f"{a} mod {b} = {result}"
            steps = [
                f"Bagi {a} dengan {b}, hasil bagi = {q}",
                f"Sisa = {a} - ({q} x {b}) = {result}"
            ]

        elif op == "floor":
            if b == 0:
                return jsonify({"error": "Floor division dengan nol tidak valid"}), 400
            result = int(a // b)
            formula = f"{a} // {b} = {result}"
            steps = [
                f"Bagi {a} dengan {b} = {a/b:.4f}",
                f"Bulatkan ke bawah = {result}"
            ]

        else:
            return jsonify({"error": "Operator tidak dikenal"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Bulatkan hasil float supaya tidak terlalu panjang
    if isinstance(result, float):
        result = round(result, 10)

    return jsonify({"result": result, "formula": formula, "steps": steps})


# ============================================================
# ROUTE LOGIKA
# Menerima: operator, nilai a (0/1), nilai b (0/1)
# ============================================================
@app.route("/api/logika", methods=["POST"])
def logika():
    data = request.get_json()
    op = data.get("operator")

    try:
        a = bool(int(data.get("a", 0)))
        # NOT hanya butuh 1 nilai, jadi b opsional
        b = bool(int(data.get("b", 0))) if op != "not" else None
    except (ValueError, TypeError):
        return jsonify({"error": "Input tidak valid"}), 400

    # Hitung hasil berdasarkan operator
    if op == "and":
        result = a and b
    elif op == "or":
        result = a or b
    elif op == "not":
        result = not a
    elif op == "xor":
        result = a ^ b
    elif op == "nand":
        result = not (a and b)
    elif op == "nor":
        result = not (a or b)
    else:
        return jsonify({"error": "Operator tidak dikenal"}), 400

    # Buat penjelasan langkah
    b_str = f", B={int(b)}" if b is not None else ""
    formula = f"A={int(a)}{b_str} → {op.upper()} = {int(result)}"
    steps = [
        f"Operator: {op.upper()}",
        f"Nilai A = {int(a)} ({'TRUE' if a else 'FALSE'})" + (f", B = {int(b)} ({'TRUE' if b else 'FALSE'})" if b is not None else ""),
        f"Hasil = {int(result)} ({'TRUE' if result else 'FALSE'})"
    ]

    return jsonify({
        "result": int(result),
        "label": "TRUE" if result else "FALSE",
        "formula": formula,
        "steps": steps
    })


# ============================================================
# ROUTE KONVERSI BASIS BILANGAN
# Mendukung: decimal, binary, octal, hexadecimal
# ============================================================
@app.route("/api/konversi-basis", methods=["POST"])
def konversi_basis():
    data = request.get_json()
    nilai = data.get("nilai", "").strip()
    frm = data.get("dari", "decimal")
    to = data.get("ke", "binary")

    try:
        # Mapping nama ke angka basis
        bases = {"decimal": 10, "binary": 2, "octal": 8, "hexadecimal": 16}

        # Konversi input ke desimal dulu
        decimal_val = int(nilai, bases[frm])

        # Lalu konversi dari desimal ke target
        if to == "decimal":
            result = str(decimal_val)
        elif to == "binary":
            result = bin(decimal_val)[2:]   # [2:] untuk buang prefix '0b'
        elif to == "octal":
            result = oct(decimal_val)[2:]   # [2:] untuk buang prefix '0o'
        elif to == "hexadecimal":
            result = hex(decimal_val)[2:].upper()  # upper() = huruf kapital
        else:
            return jsonify({"error": "Basis tujuan tidak valid"}), 400

        formula = f"({nilai}){bases[frm]} = ({result}){bases[to]}"
        steps = [
            f"Input: {nilai} (basis {bases[frm]})",
            f"Nilai desimal: {decimal_val}",
            f"Konversi ke basis {bases[to]}: {result}"
        ]
        return jsonify({"result": result, "formula": formula, "steps": steps})

    except Exception as e:
        return jsonify({"error": f"Input tidak valid: {str(e)}"}), 400


# ============================================================
# ROUTE KONVERSI SUHU
# Mendukung: celsius, fahrenheit, kelvin, reamur
# ============================================================
@app.route("/api/konversi-suhu", methods=["POST"])
def konversi_suhu():
    data = request.get_json()
    try:
        nilai = float(data.get("nilai", 0))
    except:
        return jsonify({"error": "Input tidak valid"}), 400

    frm = data.get("dari", "celsius")
    to = data.get("ke", "fahrenheit")

    # Langkah 1: Konversi semua ke Celsius dulu
    if frm == "celsius":      c = nilai
    elif frm == "fahrenheit": c = (nilai - 32) * 5 / 9
    elif frm == "kelvin":     c = nilai - 273.15
    elif frm == "reamur":     c = nilai * 5 / 4
    else: return jsonify({"error": "Satuan asal tidak valid"}), 400

    # Langkah 2: Konversi dari Celsius ke target
    if to == "celsius":       result = c
    elif to == "fahrenheit":  result = c * 9 / 5 + 32
    elif to == "kelvin":      result = c + 273.15
    elif to == "reamur":      result = c * 4 / 5
    else: return jsonify({"error": "Satuan tujuan tidak valid"}), 400

    result = round(result, 4)
    formula = f"{nilai}° {frm.capitalize()} = {result}° {to.capitalize()}"
    steps = [
        f"Input: {nilai}° {frm.capitalize()}",
        f"Konversi ke Celsius: {round(c, 4)}°C",
        f"Konversi ke {to.capitalize()}: {result}"
    ]
    return jsonify({"result": result, "formula": formula, "steps": steps})


# ============================================================
# ROUTE KONVERSI MATA UANG
# Rate bersifat statis (bukan real-time)
# ============================================================
@app.route("/api/konversi-mata-uang", methods=["POST"])
def konversi_mata_uang():
    data = request.get_json()
    try:
        nilai = float(data.get("nilai", 0))
    except:
        return jsonify({"error": "Input tidak valid"}), 400

    frm = data.get("dari", "IDR").upper()
    to = data.get("ke", "USD").upper()

    if frm not in KURS or to not in KURS:
        return jsonify({"error": "Mata uang tidak tersedia"}), 400

    # Konversi ke IDR dulu, lalu ke target
    idr = nilai / KURS[frm]
    result = round(idr * KURS[to], 4)

    formula = f"1 {frm} = {round(KURS[to]/KURS[frm], 6)} {to}"
    steps = [
        f"Input: {nilai} {frm}",
        f"Konversi ke IDR: {round(idr, 2)}",
        f"Konversi ke {to}: {result}",
        "⚠ Rate bersifat statis/ilustratif"
    ]
    return jsonify({"result": result, "formula": formula, "steps": steps})


# ============================================================
# ROUTE FAKTORIAL (BONUS)
# n! = n x (n-1) x ... x 1
# Maksimal n = 20 supaya tidak overflow
# ============================================================
@app.route("/api/faktorial", methods=["POST"])
def faktorial():
    data = request.get_json()
    try:
        n = int(data.get("n", 0))
    except:
        return jsonify({"error": "Input tidak valid"}), 400

    if n < 0:
        return jsonify({"error": "Hanya untuk bilangan non-negatif"}), 400
    if n > 20:
        return jsonify({"error": "Maksimal n = 20"}), 400

    result = math.factorial(n)

    # Buat string langkah: 5! = 1 x 2 x 3 x 4 x 5
    urutan = " x ".join(str(i) for i in range(1, n+1)) if n > 0 else "1"
    formula = f"{n}! = {result}"
    steps = [
        f"Rumus: n! = n x (n-1) x ... x 1",
        f"{n}! = {urutan}",
        f"Hasil: {result}"
    ]
    return jsonify({"result": result, "formula": formula, "steps": steps})


# ============================================================
# ROUTE FIBONACCI (BONUS)
# F(n) = F(n-1) + F(n-2), dimulai dari 0, 1
# Maksimal 50 suku
# ============================================================
@app.route("/api/fibonacci", methods=["POST"])
def fibonacci():
    data = request.get_json()
    try:
        n = int(data.get("n", 10))
    except:
        return jsonify({"error": "Input tidak valid"}), 400

    if n < 1:
        return jsonify({"error": "n harus minimal 1"}), 400
    if n > 50:
        return jsonify({"error": "Maksimal 50 suku"}), 400

    # Generate deret fibonacci
    fib = [0, 1]
    for _ in range(2, n):
        fib.append(fib[-1] + fib[-2])
    fib = fib[:n]

    formula = "F(n) = F(n-1) + F(n-2)"
    steps = [
        f"Mulai dengan F(0)=0, F(1)=1",
        f"Setiap suku = jumlah dua suku sebelumnya",
        f"Deret: {', '.join(map(str, fib))}",
        f"Suku ke-{n}: {fib[-1]}"
    ]
    return jsonify({"result": fib, "last": fib[-1], "formula": formula, "steps": steps})


# ============================================================
# Jalankan aplikasi
# debug=True = otomatis reload saat kode diubah
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)