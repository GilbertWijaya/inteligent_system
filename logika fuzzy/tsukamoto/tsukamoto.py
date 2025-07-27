# hitung nilai alpha predikat income
def a_predicate_income(x,a=1,b=10,normal=5):

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
    return {"low": low, "standard": standard, "high": high}

# hitung nilai alpha predikat permintaan
def a_predicate_request(x,a=5,b=100,normal=50):
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
    return {"low": low, "standard": standard, "high": high}


# gabungkan semua dictionary rule dalam satu list
def all_rules(*all):
    return list(all)

# cocokan rule dan cari nilai z dari alpha predikat yang diketahui
def rule(rule_income,rule_request,x_income,x_request):
    a_income = a_predicate_income(x_income)# ambil nilai alpha predikat income 
    a_request = a_predicate_request(x_request)# ambil nilai alpha predikat permintaan
    
    a = min(a_income[rule_income], a_request[rule_request])# bandingkan kedua nilai alpha predikat yang terkecil
    
    # Konsekuen: z untuk "layak" atau "tidak layak"
    # Misal: jika 'low' → z kecil, jika 'high' → z besar
    if rule_income == "low" and rule_request == "high":
        z = 50 - a * (50 - 5) # turun
    elif rule_income == "high" and rule_request == "low":
        z = a * (100 - 50) + 50  # naik
    elif rule_income == "high" and rule_request == "high":
        z = a * (50 - 5) + 5   # normal naik
    elif rule_income == "low" and rule_request == "low":
        z = a * (100 - 50) + 100 # turun
    else:
        z = 0  # fallback

    return {"alpha": a, "z": z}

# Defuzzifikasi metode Tsukamoto
def defuzzifikasi_tsukamoto(rules_result):# hitung nilai total z
    pembilang = sum(r["alpha"] * r["z"] for r in rules_result)# jumlahkan setiap nilai alpha predikat yang dikali dengan nilai z
    penyebut = sum(r["alpha"] for r in rules_result)# jumlahkan nilai alpha predikat
    return pembilang / penyebut if penyebut != 0 else 0 # bagikan pembilang dan penyebut

# Input data
x_income = 4
x_request = 80

# Buat rules
rule_1 = rule("low", "high", x_income, x_request)
rule_2 = rule("high", "low", x_income, x_request)
rule_3 = rule("high", "high", x_income, x_request)
rule_4 = rule("low", "low", x_income, x_request)

rules = all_rules(rule_1,rule_2,rule_3,rule_4)


# Cetak setiap rule
for i, r in enumerate(rules, 1): # i = nilai index, r = nilai dari dictionary
    print(f"Rule {i}: a = {r['alpha']:.2f}, z = {r['z']:.2f}")

# Hitung defuzzifikasi
z_akhir = defuzzifikasi_tsukamoto(rules)
print(f"\nNilai akhir (defuzzifikasi Tsukamoto): {z_akhir:.2f}")




