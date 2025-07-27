import requests

base_url = "http://127.0.0.1:8000/api/"

def get_aturan():
    response = requests.get(base_url + "aturan")
    if response.status_code == 200:
        data = response.json()       
        return data

    else:
        print("Gagal mendapatkan data")
aturan_s = get_aturan()

def a_predicate_suhu(x,a=35,b=41,normal=38):

    # jika x lebih besar dari nilai a dan lebih kecil dari nilai normal(tengah)
    if a <= x <= normal:
        low = (normal - x) / (normal - a)# linear turun
        standard = (x - a) / (normal - a)# linear normal(tengah) naik
        high = 0# linear naik
    elif normal < x <= b: # jika nilai x lebih besar dari normal namun masih lebih kecil dari nilai b
        low = 0
        standard = (b - x) / (b - normal)# linear normal(tengah) turun
        high = (x - normal) / (b - normal)# linear naik
    else:
        low = standard = high = 0
    return {"rendah": low, "normal": standard, "tinggi": high}

def a_predicate_batuk(x,a=1,b=10,normal=5):
    if a <= x <= normal:
        low = (normal - x) / (normal - a)
        standard = (x - a) / (normal - a)
        high = 0
    elif normal < x <= b:
        low = 0
        standard = (b - x) / (b - normal)
        high = (x - normal) / (b - normal)
    else:
        low = standard = high = 0
    return {"ringan": low, "sedang": standard, "parah": high}


def all_rules(*all):
    return list(all)

def rule(rule_suhu,rule_batuk,x_suhu,x_batuk):
    a_suhu = a_predicate_suhu(x_suhu)# ambil nilai alpha predikat income 
    a_batuk = a_predicate_batuk(x_batuk)# ambil nilai alpha predikat permintaan
    
    a = min(a_suhu[rule_suhu], a_batuk[rule_batuk])# bandingkan kedua nilai alpha predikat yang terkecil
    
    # Konsekuen: z untuk "layak" atau "tidak layak"
    # Misal: jika 'low' → z kecil, jika 'high' → z besar
    if rule_suhu == "tinggi" and rule_batuk == "parah":
        z = 2 * x_suhu + 3 * x_batuk + 10
        # print(f"nilai z rule 1 adalah {z}")
    elif rule_suhu == "normal" and rule_batuk == "sedang":
        z = x_suhu + x_batuk + 5
        # print(f"nilai z rule 2 adalah {z}")
    elif rule_suhu == "rendah" and rule_batuk == "ringan":
        z = 0.5 * x_suhu + 0.5 * x_batuk + 2
        # print(f"nilai z rule 3 adalah {z}")
    elif rule_suhu == "tinggi" and rule_batuk == "ringan":
        z = 2 * x_suhu + x_batuk + 4
        # print(f"nilai z rule 4 adalah {z}")
    elif rule_suhu == "normal" and rule_batuk == "parah":
        z = x_suhu + 3 * x_batuk + 7
        # print(f"nilai z rule 5 adalah {z}")
    else:
        z = 0  # fallback

    return {"alpha": a, "z": z}

def defuzzifikasi_sugeno(rules_result):# hitung nilai total z
    pembilang = sum(r["alpha"] * r["z"] for r in rules_result)# jumlahkan setiap nilai alpha predikat yang dikali dengan nilai z
    penyebut = sum(r["alpha"] for r in rules_result)# jumlahkan nilai alpha predikat
    return pembilang / penyebut if penyebut != 0 else 0 # bagikan pembilang dan penyebut

# Input data
suhu_input = 38.8
batuk_input = 9
rules = []

for aturan in aturan_s:
    rule_thing = rule(aturan["suhu"],aturan["batuk"],suhu_input,batuk_input)
    rules.append(rule_thing)

# Cetak setiap rule
for i, r in enumerate(rules, 1): # i = nilai index, r = nilai dari dictionary
    print(f"Rule {i}: a = {r['alpha']:.2f}, z = {r['z']:.2f}")

# Hitung defuzzifikasi
z_akhir = defuzzifikasi_sugeno(rules)
print(f"\nNilai akhir (defuzzifikasi sugeno): {z_akhir:.2f}")
