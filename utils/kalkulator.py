import math
from datetime import datetime


class Kalkulator:
    """Kalkulator sederhana dengan berbagai fitur perhitungan."""

    def __init__(self):
        self.riwayat = []

    def tambah(self, a, b):
        hasil = a + b
        rumus = f"{a} + {b}"
        penjelasan = f"{a} ditambah {b} hasilnya {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def kurang(self, a, b):
        hasil = a - b
        rumus = f"{a} - {b}"
        penjelasan = f"{a} dikurangi {b} hasilnya {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def kali(self, a, b):
        hasil = a * b
        rumus = f"{a} × {b}"
        penjelasan = f"{a} dikali {b} hasilnya {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def bagi(self, a, b):
        if b == 0:
            return {"error": "Tidak bisa dibagi dengan 0.", "rumus": f"{a} ÷ {b}"}

        hasil = a / b
        rumus = f"{a} ÷ {b}"
        penjelasan = f"{a} dibagi {b} hasilnya {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def pangkat(self, a, b):
        hasil = a ** b
        rumus = f"{a}^{b}"
        penjelasan = f"{a} dipangkatkan {b} hasilnya {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def akar_kuadrat(self, a):
        if a < 0:
            return {"error": "Akar kuadrat tidak bisa dari bilangan negatif.", "rumus": f"√{a}"}

        hasil = math.sqrt(a)
        rumus = f"√{a}"
        penjelasan = f"Akar kuadrat dari {a} adalah {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def modulus(self, a, b):
        if b == 0:
            return {"error": "Tidak bisa modulus dengan 0.", "rumus": f"{a} mod {b}"}

        hasil = a % b
        rumus = f"{a} mod {b}"
        penjelasan = f"Sisa pembagian {a} oleh {b} adalah {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def pembagian_bulat(self, a, b):
        if b == 0:
            return {"error": "Tidak bisa dibagi dengan 0.", "rumus": f"{a} // {b}"}

        hasil = a // b
        rumus = f"{a} // {b}"
        penjelasan = f"Hasil pembagian bulat {a} oleh {b} adalah {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def dan_logika(self, a, b):
        hasil = 1 if (a and b) else 0
        rumus = f"{a} AND {b}"
        penjelasan = f"Operasi AND dari {a} dan {b} menghasilkan {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def atau_logika(self, a, b):
        hasil = 1 if (a or b) else 0
        rumus = f"{a} OR {b}"
        penjelasan = f"Operasi OR dari {a} dan {b} menghasilkan {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def tidak_logika(self, a):
        hasil = 1 if not a else 0
        rumus = f"NOT {a}"
        penjelasan = f"Operasi NOT dari {a} menghasilkan {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def xor_logika(self, a, b):
        hasil = 1 if a != b else 0
        rumus = f"{a} XOR {b}"
        penjelasan = f"Operasi XOR dari {a} dan {b} menghasilkan {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def nand_logika(self, a, b):
        hasil = 1 if not (a and b) else 0
        rumus = f"{a} NAND {b}"
        penjelasan = f"Operasi NAND dari {a} dan {b} menghasilkan {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def nor_logika(self, a, b):
        hasil = 1 if not (a or b) else 0
        rumus = f"{a} NOR {b}"
        penjelasan = f"Operasi NOR dari {a} dan {b} menghasilkan {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def desimal_ke_biner(self, n):
        hasil = bin(int(n))[2:]
        rumus = f"{n} (desimal)"
        penjelasan = f"Bilangan {n} dalam biner adalah {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def desimal_ke_oktal(self, n):
        hasil = oct(int(n))[2:]
        rumus = f"{n} (desimal)"
        penjelasan = f"Bilangan {n} dalam oktal adalah {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def desimal_ke_heksa(self, n):
        hasil = hex(int(n))[2:].upper()
        rumus = f"{n} (desimal)"
        penjelasan = f"Bilangan {n} dalam heksadesimal adalah {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def biner_ke_desimal(self, n):
        try:
            hasil = int(str(n), 2)
            rumus = f"{n} (biner)"
            penjelasan = f"Bilangan {n} dalam desimal adalah {hasil}"
            self._simpan_riwayat(rumus, hasil, penjelasan)
            return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}
        except:
            return {"error": "Input biner tidak valid. Gunakan hanya 0 dan 1."}

    def oktal_ke_desimal(self, n):
        try:
            hasil = int(str(n), 8)
            rumus = f"{n} (oktal)"
            penjelasan = f"Bilangan {n} dalam desimal adalah {hasil}"
            self._simpan_riwayat(rumus, hasil, penjelasan)
            return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}
        except:
            return {"error": "Input oktal tidak valid. Gunakan angka 0 sampai 7."}

    def heksa_ke_desimal(self, n):
        try:
            hasil = int(str(n), 16)
            rumus = f"{n} (heksadesimal)"
            penjelasan = f"Bilangan {n} dalam desimal adalah {hasil}"
            self._simpan_riwayat(rumus, hasil, penjelasan)
            return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}
        except:
            return {"error": "Input heksadesimal tidak valid. Gunakan 0-9 dan A-F."}

    def celsius_ke_fahrenheit(self, c):
        hasil = (c * 9 / 5) + 32
        rumus = f"{c}°C"
        penjelasan = f"{c}°C sama dengan {hasil:.2f}°F"
        self._simpan_riwayat(rumus, round(hasil, 2), penjelasan)
        return {"hasil": round(hasil, 2), "rumus": rumus, "penjelasan": penjelasan}

    def celsius_ke_kelvin(self, c):
        hasil = c + 273.15
        rumus = f"{c}°C"
        penjelasan = f"{c}°C sama dengan {hasil:.2f} K"
        self._simpan_riwayat(rumus, round(hasil, 2), penjelasan)
        return {"hasil": round(hasil, 2), "rumus": rumus, "penjelasan": penjelasan}

    def celsius_ke_reamur(self, c):
        hasil = c * 4 / 5
        rumus = f"{c}°C"
        penjelasan = f"{c}°C sama dengan {hasil:.2f}°R"
        self._simpan_riwayat(rumus, round(hasil, 2), penjelasan)
        return {"hasil": round(hasil, 2), "rumus": rumus, "penjelasan": penjelasan}

    def fahrenheit_ke_celsius(self, f):
        hasil = (f - 32) * 5 / 9
        rumus = f"{f}°F"
        penjelasan = f"{f}°F sama dengan {hasil:.2f}°C"
        self._simpan_riwayat(rumus, round(hasil, 2), penjelasan)
        return {"hasil": round(hasil, 2), "rumus": rumus, "penjelasan": penjelasan}

    def kelvin_ke_celsius(self, k):
        hasil = k - 273.15
        rumus = f"{k} K"
        penjelasan = f"{k} K sama dengan {hasil:.2f}°C"
        self._simpan_riwayat(rumus, round(hasil, 2), penjelasan)
        return {"hasil": round(hasil, 2), "rumus": rumus, "penjelasan": penjelasan}

    def reamur_ke_celsius(self, r):
        hasil = r * 5 / 4
        rumus = f"{r}°R"
        penjelasan = f"{r}°R sama dengan {hasil:.2f}°C"
        self._simpan_riwayat(rumus, round(hasil, 2), penjelasan)
        return {"hasil": round(hasil, 2), "rumus": rumus, "penjelasan": penjelasan}

    def konversi_mata_uang(self, jumlah, dari_mata_uang, ke_mata_uang):
        kurs = {
            "IDR": 1,
            "USD": 0.000062,
            "EUR": 0.000057,
            "SGD": 0.000084
        }

        if dari_mata_uang not in kurs or ke_mata_uang not in kurs:
            return {"error": "Mata uang tidak didukung."}

        jumlah_dalam_idr = jumlah / kurs[dari_mata_uang]
        hasil = jumlah_dalam_idr * kurs[ke_mata_uang]

        rumus = f"{jumlah} {dari_mata_uang}"
        penjelasan = f"{jumlah} {dari_mata_uang} sama dengan {hasil:.2f} {ke_mata_uang}"
        self._simpan_riwayat(rumus, round(hasil, 2), penjelasan)
        return {"hasil": round(hasil, 2), "rumus": rumus, "penjelasan": penjelasan}

    def faktorial(self, n):
        if n < 0:
            return {"error": "Faktorial hanya untuk bilangan positif."}

        hasil = math.factorial(int(n))
        rumus = f"{n}!"
        penjelasan = f"Faktorial dari {n} adalah {hasil}"
        self._simpan_riwayat(rumus, hasil, penjelasan)
        return {"hasil": hasil, "rumus": rumus, "penjelasan": penjelasan}

    def fibonacci(self, n):
        if n <= 0:
            return {"error": "Jumlah suku harus lebih dari 0."}

        deret = []
        a, b = 0, 1
        for _ in range(int(n)):
            deret.append(a)
            a, b = b, a + b

        rumus = f"Fibonacci({n})"
        penjelasan = f"Deret Fibonacci sebanyak {n} suku pertama adalah {deret}"
        self._simpan_riwayat(rumus, deret, penjelasan)
        return {"hasil": deret, "rumus": rumus, "penjelasan": penjelasan}

    def _simpan_riwayat(self, rumus, hasil, penjelasan):
        self.riwayat.append({
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rumus": rumus,
            "hasil": hasil,
            "penjelasan": penjelasan
        })

    def lihat_riwayat(self):
        return self.riwayat

    def hapus_riwayat(self):
        self.riwayat = []
        return {"pesan": "Riwayat berhasil dihapus."}