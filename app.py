from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# kurs statis buat konversi mata uang
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


# halaman welcome
@app.route("/")
def welcome():
    return render_template("welcome.html")


# halaman kalkulator utama
@app.route("/kalkulator")
def index():
    return render_template("index.html")


@app.route("/api/aritmatika", methods=["POST"])
def aritmatika():
    data = request.get_json()
    op = data.get("operator")

    try:
        a = float(data.get("a", 0))
        b = float(data.get("b", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Input tidak valid"}), 400

    result, formula, steps = None, "", []

    try:
        if op == "tambah":
            result  = a + b
            formula = f"{a} + {b} = {result}"
            steps   = [
                f"Operasi: Penjumlahan",
                f"Rumus: A + B",
                f"Masukkan nilai: {a} + {b}",
                f"Hitung: {a} + {b} = {result}",
                f"Hasil: {result}",
            ]

        elif op == "kurang":
            result  = a - b
            formula = f"{a} - {b} = {result}"
            steps   = [
                f"Operasi: Pengurangan",
                f"Rumus: A - B",
                f"Masukkan nilai: {a} - {b}",
                f"Hitung: {a} - {b} = {result}",
                f"Hasil: {result}",
            ]

        elif op == "kali":
            result  = a * b
            formula = f"{a} × {b} = {result}"
            steps   = [
                f"Operasi: Perkalian",
                f"Rumus: A × B",
                f"Masukkan nilai: {a} × {b}",
                f"Hitung: {a} × {b} = {result}",
                f"Hasil: {result}",
            ]

        elif op == "bagi":
            if b == 0:
                return jsonify({"error": "Tidak bisa membagi dengan nol"}), 400
            result  = a / b
            formula = f"{a} ÷ {b} = {round(result, 10)}"
            steps   = [
                f"Operasi: Pembagian",
                f"Rumus: A ÷ B",
                f"Masukkan nilai: {a} ÷ {b}",
                f"Hitung: {a} ÷ {b} = {round(result, 10)}",
                f"Hasil: {round(result, 10)}",
            ]

        elif op == "pangkat":
            result  = a ** b
            formula = f"{a}^{b} = {result}"
            steps   = [
                f"Operasi: Perpangkatan",
                f"Rumus: A^B (A dikalikan sebanyak B kali)",
                f"Masukkan nilai: {a}^{int(b)}",
                f"Artinya: {' × '.join([str(a)] * int(b)) if int(b) <= 6 else str(a) + ' × ... (sebanyak ' + str(int(b)) + ' kali)'}",
                f"Hitung: {a}^{int(b)} = {result}",
                f"Hasil: {result}",
            ]

        elif op == "akar":
            b = float(data.get("b", 2))
            if a < 0:
                return jsonify({"error": "Tidak bisa akar bilangan negatif"}), 400
            result  = a ** (1 / b)
            formula = f"⁽¹/{int(b)}⁾√{a} = {round(result, 6)}"
            steps   = [
                f"Operasi: Penarikan Akar ke-{int(b)}",
                f"Rumus: A^(1/B) — akar ke-B dari A",
                f"Masukkan nilai: {a}^(1/{int(b)})",
                f"Artinya: cari angka yang kalau dipangkatkan {int(b)} hasilnya {a}",
                f"Hitung: {a}^(1/{int(b)}) = {round(result, 6)}",
                f"Hasil: {round(result, 6)}",
            ]

        elif op == "modulus":
            if b == 0:
                return jsonify({"error": "Modulus dengan nol tidak valid"}), 400
            result  = a % b
            q       = int(a // b)
            formula = f"{a} mod {b} = {result}"
            steps   = [
                f"Operasi: Modulus (sisa bagi)",
                f"Rumus: A mod B = A - (A ÷ B dibulatkan bawah) × B",
                f"Masukkan nilai: {a} mod {b}",
                f"Langkah 1 — Bagi: {a} ÷ {b} = {a/b:.4f}",
                f"Langkah 2 — Bulatkan ke bawah: floor({a/b:.4f}) = {q}",
                f"Langkah 3 — Hitung sisa: {a} - ({q} × {b}) = {a} - {q*b} = {result}",
                f"Hasil: {result}",
            ]

        elif op == "floor":
            if b == 0:
                return jsonify({"error": "Floor division dengan nol tidak valid"}), 400
            result  = int(a // b)
            formula = f"{a} // {b} = {result}"
            steps   = [
                f"Operasi: Floor Division (bagi bulat bawah)",
                f"Rumus: A // B = floor(A ÷ B)",
                f"Masukkan nilai: {a} // {b}",
                f"Langkah 1 — Bagi biasa: {a} ÷ {b} = {a/b:.6f}",
                f"Langkah 2 — Bulatkan ke bawah: floor({a/b:.6f}) = {result}",
                f"Hasil: {result}",
            ]

        else:
            return jsonify({"error": "Operator tidak dikenal"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    if isinstance(result, float):
        result = round(result, 10)

    return jsonify({"result": result, "formula": formula, "steps": steps})


@app.route("/api/logika", methods=["POST"])
def logika():
    data = request.get_json()
    op   = data.get("operator")

    try:
        a = bool(int(data.get("a", 0)))
        b = bool(int(data.get("b", 0))) if op != "not" else None
    except (ValueError, TypeError):
        return jsonify({"error": "Input tidak valid"}), 400

    if   op == "and":   result = a and b
    elif op == "or":    result = a or b
    elif op == "not":   result = not a
    elif op == "xor":   result = a ^ b
    elif op == "nand":  result = not (a and b)
    elif op == "nor":   result = not (a or b)
    else:
        return jsonify({"error": "Operator tidak dikenal"}), 400

    label_a = "TRUE" if a else "FALSE"
    label_b = "TRUE" if b else "FALSE" if b is not None else None
    label_r = "TRUE" if result else "FALSE"

    b_str   = f", B={int(b)} ({label_b})" if b is not None else ""
    formula = f"A={int(a)} ({label_a}){b_str} → {op.upper()} = {int(result)} ({label_r})"

    # langkah sesuai operator
    if op == "and":
        steps = [
            f"Operasi: AND (DAN) — hasil TRUE hanya jika SEMUA input TRUE",
            f"Tabel kebenaran: T AND T = T | T AND F = F | F AND T = F | F AND F = F",
            f"Nilai A = {int(a)} ({label_a})",
            f"Nilai B = {int(b)} ({label_b})",
            f"Cek: {label_a} AND {label_b} = ?",
            f"Karena {'keduanya TRUE' if a and b else 'salah satu atau keduanya FALSE'} → hasil = {label_r}",
            f"Hasil: {int(result)} ({label_r})",
        ]
    elif op == "or":
        steps = [
            f"Operasi: OR (ATAU) — hasil TRUE jika SALAH SATU atau lebih input TRUE",
            f"Tabel kebenaran: T OR T = T | T OR F = T | F OR T = T | F OR F = F",
            f"Nilai A = {int(a)} ({label_a})",
            f"Nilai B = {int(b)} ({label_b})",
            f"Cek: {label_a} OR {label_b} = ?",
            f"Karena {'minimal satu TRUE' if a or b else 'keduanya FALSE'} → hasil = {label_r}",
            f"Hasil: {int(result)} ({label_r})",
        ]
    elif op == "not":
        steps = [
            f"Operasi: NOT (NEGASI) — membalik nilai input",
            f"Tabel kebenaran: NOT TRUE = FALSE | NOT FALSE = TRUE",
            f"Nilai A = {int(a)} ({label_a})",
            f"Cek: NOT {label_a} = ?",
            f"Balik nilai: {label_a} → {label_r}",
            f"Hasil: {int(result)} ({label_r})",
        ]
    elif op == "xor":
        steps = [
            f"Operasi: XOR (EXCLUSIVE OR) — hasil TRUE jika input BERBEDA",
            f"Tabel kebenaran: T XOR T = F | T XOR F = T | F XOR T = T | F XOR F = F",
            f"Nilai A = {int(a)} ({label_a})",
            f"Nilai B = {int(b)} ({label_b})",
            f"Cek: {label_a} XOR {label_b} = ?",
            f"Karena {'nilainya berbeda' if a ^ b else 'nilainya sama'} → hasil = {label_r}",
            f"Hasil: {int(result)} ({label_r})",
        ]
    elif op == "nand":
        and_result = a and b
        steps = [
            f"Operasi: NAND (NOT AND) — kebalikan dari AND",
            f"Tabel kebenaran: T NAND T = F | T NAND F = T | F NAND T = T | F NAND F = T",
            f"Nilai A = {int(a)} ({label_a})",
            f"Nilai B = {int(b)} ({label_b})",
            f"Langkah 1 — Hitung AND dulu: {label_a} AND {label_b} = {'TRUE' if and_result else 'FALSE'}",
            f"Langkah 2 — Balik hasilnya (NOT): NOT {'TRUE' if and_result else 'FALSE'} = {label_r}",
            f"Hasil: {int(result)} ({label_r})",
        ]
    elif op == "nor":
        or_result = a or b
        steps = [
            f"Operasi: NOR (NOT OR) — kebalikan dari OR",
            f"Tabel kebenaran: T NOR T = F | T NOR F = F | F NOR T = F | F NOR F = T",
            f"Nilai A = {int(a)} ({label_a})",
            f"Nilai B = {int(b)} ({label_b})",
            f"Langkah 1 — Hitung OR dulu: {label_a} OR {label_b} = {'TRUE' if or_result else 'FALSE'}",
            f"Langkah 2 — Balik hasilnya (NOT): NOT {'TRUE' if or_result else 'FALSE'} = {label_r}",
            f"Hasil: {int(result)} ({label_r})",
        ]

    return jsonify({"result": int(result), "label": label_r, "formula": formula, "steps": steps})


@app.route("/api/konversi-basis", methods=["POST"])
def konversi_basis():
    data  = request.get_json()
    nilai = data.get("nilai", "").strip()
    frm   = data.get("dari", "decimal")
    to    = data.get("ke", "binary")

    try:
        bases       = {"decimal": 10, "binary": 2, "octal": 8, "hexadecimal": 16}
        nama_basis  = {"decimal": "Desimal", "binary": "Biner", "octal": "Oktal", "hexadecimal": "Heksadesimal"}
        decimal_val = int(nilai, bases[frm])

        if   to == "decimal":     result = str(decimal_val)
        elif to == "binary":      result = bin(decimal_val)[2:]
        elif to == "octal":       result = oct(decimal_val)[2:]
        elif to == "hexadecimal": result = hex(decimal_val)[2:].upper()
        else:
            return jsonify({"error": "Basis tujuan tidak valid"}), 400

        formula = f"({nilai}){bases[frm]} = ({result}){bases[to]}"

        # langkah konversi ke desimal dulu
        if frm == "decimal":
            steps_to_dec = [f"Input sudah desimal: {decimal_val}"]
        elif frm == "binary":
            bits  = nilai[::-1]
            parts = [f"{b}×2^{i}={int(b)*(2**i)}" for i, b in enumerate(bits)]
            steps_to_dec = [
                f"Konversi {nama_basis[frm]} → Desimal:",
                f"Tiap digit dikali 2^posisi (dari kanan mulai 0)",
                f"= {' + '.join(parts[::-1])} = {decimal_val}",
            ]
        elif frm == "octal":
            digits = nilai[::-1]
            parts  = [f"{d}×8^{i}={int(d)*(8**i)}" for i, d in enumerate(digits)]
            steps_to_dec = [
                f"Konversi {nama_basis[frm]} → Desimal:",
                f"Tiap digit dikali 8^posisi (dari kanan mulai 0)",
                f"= {' + '.join(parts[::-1])} = {decimal_val}",
            ]
        elif frm == "hexadecimal":
            hex_map = {str(i): i for i in range(10)}
            hex_map.update({"A":10,"B":11,"C":12,"D":13,"E":14,"F":15})
            digits  = nilai.upper()[::-1]
            parts   = [f"{d}×16^{i}={hex_map.get(d,0)*(16**i)}" for i, d in enumerate(digits)]
            steps_to_dec = [
                f"Konversi {nama_basis[frm]} → Desimal:",
                f"Tiap digit dikali 16^posisi (A=10, B=11, ..., F=15)",
                f"= {' + '.join(parts[::-1])} = {decimal_val}",
            ]

        # langkah dari desimal ke target
        if to == "decimal":
            steps_from_dec = [f"Target sudah desimal: {result}"]
        elif to == "binary":
            n, divs = decimal_val, []
            tmp = decimal_val
            while tmp > 0:
                divs.append(f"{tmp} ÷ 2 = {tmp//2} sisa {tmp%2}")
                tmp //= 2
            steps_from_dec = [
                f"Konversi Desimal → {nama_basis[to]}:",
                f"Bagi terus dengan 2, catat sisa:",
                *divs,
                f"Baca sisa dari bawah ke atas → {result}",
            ]
        elif to == "octal":
            tmp, divs = decimal_val, []
            while tmp > 0:
                divs.append(f"{tmp} ÷ 8 = {tmp//8} sisa {tmp%8}")
                tmp //= 8
            steps_from_dec = [
                f"Konversi Desimal → {nama_basis[to]}:",
                f"Bagi terus dengan 8, catat sisa:",
                *divs,
                f"Baca sisa dari bawah ke atas → {result}",
            ]
        elif to == "hexadecimal":
            tmp, divs = decimal_val, []
            hex_chars = "0123456789ABCDEF"
            while tmp > 0:
                sisa = tmp % 16
                divs.append(f"{tmp} ÷ 16 = {tmp//16} sisa {sisa} ({hex_chars[sisa]})")
                tmp //= 16
            steps_from_dec = [
                f"Konversi Desimal → {nama_basis[to]}:",
                f"Bagi terus dengan 16, catat sisa (10=A, 11=B, ..., 15=F):",
                *divs,
                f"Baca sisa dari bawah ke atas → {result}",
            ]

        steps = [
            f"Input: {nilai} ({nama_basis[frm]}, basis {bases[frm]})",
            *steps_to_dec,
            *steps_from_dec,
            f"Hasil: {result} ({nama_basis[to]}, basis {bases[to]})",
        ]

        return jsonify({"result": result, "formula": formula, "steps": steps})

    except Exception as e:
        return jsonify({"error": f"Input tidak valid: {str(e)}"}), 400


@app.route("/api/konversi-suhu", methods=["POST"])
def konversi_suhu():
    data = request.get_json()
    try:
        nilai = float(data.get("nilai", 0))
    except Exception:
        return jsonify({"error": "Input tidak valid"}), 400

    frm = data.get("dari", "celsius")
    to  = data.get("ke", "fahrenheit")

    # ke celsius dulu
    if   frm == "celsius":    c = nilai
    elif frm == "fahrenheit": c = (nilai - 32) * 5 / 9
    elif frm == "kelvin":     c = nilai - 273.15
    elif frm == "reamur":     c = nilai * 5 / 4
    else:
        return jsonify({"error": "Satuan asal tidak valid"}), 400

    # dari celsius ke target
    if   to == "celsius":    result = c
    elif to == "fahrenheit": result = c * 9 / 5 + 32
    elif to == "kelvin":     result = c + 273.15
    elif to == "reamur":     result = c * 4 / 5
    else:
        return jsonify({"error": "Satuan tujuan tidak valid"}), 400

    result  = round(result, 4)
    c       = round(c, 4)
    formula = f"{nilai}° {frm.capitalize()} = {result}° {to.capitalize()}"

    # rumus konversi ke celsius
    rumus_ke_c = {
        "celsius":    f"C = {nilai} (sudah Celsius)",
        "fahrenheit": f"C = ({nilai} - 32) × 5/9 = {c}°C",
        "kelvin":     f"C = {nilai} - 273.15 = {c}°C",
        "reamur":     f"C = {nilai} × 5/4 = {c}°C",
    }

    # rumus konversi dari celsius ke target
    rumus_dari_c = {
        "celsius":    f"{to.capitalize()} = {c} (sudah Celsius)",
        "fahrenheit": f"{to.capitalize()} = {c} × 9/5 + 32 = {result}°F",
        "kelvin":     f"{to.capitalize()} = {c} + 273.15 = {result}K",
        "reamur":     f"{to.capitalize()} = {c} × 4/5 = {result}°Ré",
    }

    if frm == to:
        steps = [
            f"Input: {nilai}° {frm.capitalize()}",
            f"Satuan asal dan tujuan sama, tidak perlu konversi.",
            f"Hasil: {result}° {to.capitalize()}",
        ]
    else:
        steps = [
            f"Input: {nilai}° {frm.capitalize()}",
            f"Strategi: konversi ke Celsius dulu, lalu ke {to.capitalize()}",
            f"Langkah 1 — ke Celsius: {rumus_ke_c[frm]}",
            f"Langkah 2 — ke {to.capitalize()}: {rumus_dari_c[to]}",
            f"Hasil: {result}° {to.capitalize()}",
        ]

    return jsonify({"result": result, "formula": formula, "steps": steps})


@app.route("/api/konversi-mata-uang", methods=["POST"])
def konversi_mata_uang():
    data = request.get_json()
    try:
        nilai = float(data.get("nilai", 0))
    except Exception:
        return jsonify({"error": "Input tidak valid"}), 400

    frm = data.get("dari", "IDR").upper()
    to  = data.get("ke", "USD").upper()

    if frm not in KURS or to not in KURS:
        return jsonify({"error": "Mata uang tidak tersedia"}), 400

    idr    = nilai / KURS[frm]
    result = round(idr * KURS[to], 4)
    rate   = round(KURS[to] / KURS[frm], 6)

    formula = f"1 {frm} = {rate} {to}"
    steps   = [
        f"Input: {nilai} {frm}",
        f"Catatan: kurs bersifat statis/ilustratif",
        f"Langkah 1 — ke IDR dulu: {nilai} {frm} ÷ {KURS[frm]} = {round(idr, 2)} IDR",
        f"Langkah 2 — ke {to}: {round(idr, 2)} IDR × {KURS[to]} = {result} {to}",
        f"Atau langsung: {nilai} × {rate} = {result} {to}",
        f"Hasil: {result} {to}",
    ]

    return jsonify({"result": result, "formula": formula, "steps": steps})


@app.route("/api/faktorial", methods=["POST"])
def faktorial():
    data = request.get_json()
    try:
        n = int(data.get("n", 0))
    except Exception:
        return jsonify({"error": "Input tidak valid"}), 400

    if n < 0:  return jsonify({"error": "Hanya untuk bilangan non-negatif"}), 400
    if n > 20: return jsonify({"error": "Maksimal n = 20"}), 400

    result = math.factorial(n)
    urutan = " × ".join(str(i) for i in range(n, 0, -1)) if n > 0 else "1"

    # langkah akumulatif
    acc_steps = []
    acc = 1
    for i in range(1, n + 1):
        acc *= i
        acc_steps.append(f"  × {i} = {acc}")

    formula = f"{n}! = {result}"
    steps   = [
        f"Operasi: Faktorial",
        f"Rumus: n! = n × (n-1) × (n-2) × ... × 2 × 1",
        f"Kasus khusus: 0! = 1 (by definition)",
        f"Masukkan n = {n}",
        f"{n}! = {urutan}",
        f"Proses perkalian bertahap:",
        *acc_steps,
        f"Hasil: {n}! = {result}",
    ]

    return jsonify({"result": result, "formula": formula, "steps": steps})


@app.route("/api/fibonacci", methods=["POST"])
def fibonacci():
    data = request.get_json()
    try:
        n = int(data.get("n", 10))
    except Exception:
        return jsonify({"error": "Input tidak valid"}), 400

    if n < 1:  return jsonify({"error": "n harus minimal 1"}), 400
    if n > 50: return jsonify({"error": "Maksimal 50 suku"}), 400

    fib = [0, 1]
    for _ in range(2, n):
        fib.append(fib[-1] + fib[-2])
    fib = fib[:n]

    # tampilkan max 8 langkah penjumlahan biar tidak terlalu panjang
    fib_steps = []
    for i in range(2, min(n, 10)):
        fib_steps.append(f"  F({i}) = F({i-1}) + F({i-2}) = {fib[i-1]} + {fib[i-2]} = {fib[i]}")
    if n > 10:
        fib_steps.append(f"  ... (dilanjutkan sampai suku ke-{n})")

    formula = "F(n) = F(n-1) + F(n-2)"
    steps   = [
        f"Operasi: Deret Fibonacci",
        f"Rumus: setiap suku = jumlah dua suku sebelumnya",
        f"Nilai awal: F(0) = 0, F(1) = 1",
        f"Proses pembentukan deret:",
        *fib_steps,
        f"Deret lengkap ({n} suku): {', '.join(map(str, fib))}",
        f"Suku ke-{n}: {fib[-1]}",
    ]

    return jsonify({"result": fib, "last": fib[-1], "formula": formula, "steps": steps})


if __name__ == "__main__":
    app.run(debug=True)