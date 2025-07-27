# implementasi logika fuzzy dengan library scikit-fuzzy

import numpy as np #pip install numpy (untuk range data numerik)
import skfuzzy as fuzz #pip install scikit-fuzzy (library fuzzy)
from skfuzzy import control as ctrl #pip install scipy & pip install netwokx (modul khusus untuk membuat rule fuzzy)


# Input
#                     nilai minimum - nilai maksimum - interval
suhu = ctrl.Antecedent(np.arange(35, 41, 0.1), 'suhu')
batuk = ctrl.Antecedent(np.arange(0, 11, 1), 'batuk')

# Output
#                     nilai minimum - nilai maksimum - interval
penyakit = ctrl.Consequent(np.arange(0, 101, 1), 'penyakit')

# Membership function suhu, .trimf() membuat fungsi keanggotaan segitiga
suhu['normal'] = fuzz.trimf(suhu.universe, [35, 36.5, 37.2]) #fuzz.trimf(universe, [a=titik awal mulai naik dari 0, b=puncak segitiga 1, c=titik akhir turun ke 0])
suhu['tinggi'] = fuzz.trimf(suhu.universe, [37, 38, 39])
suhu['sangat_tinggi'] = fuzz.trimf(suhu.universe, [38.5, 39.5, 40.5])

# Membership function batuk
batuk['ringan'] = fuzz.trimf(batuk.universe, [0, 1.5, 3])
batuk['sedang'] = fuzz.trimf(batuk.universe, [3, 5, 6])
batuk['parah'] = fuzz.trimf(batuk.universe, [6, 8, 10])

# Membership function penyakit (output)
penyakit['demam_biasa'] = fuzz.trimf(penyakit.universe, [0, 20, 40])
penyakit['flu'] = fuzz.trimf(penyakit.universe, [30, 50, 70])
penyakit['covid'] = fuzz.trimf(penyakit.universe, [60, 80, 100])

# Rule Base (if....then....)
rule1 = ctrl.Rule(suhu['tinggi'] & batuk['sedang'], penyakit['flu'])
rule2 = ctrl.Rule(suhu['sangat_tinggi'] & batuk['parah'], penyakit['covid'])
rule3 = ctrl.Rule(suhu['normal'] & batuk['ringan'], penyakit['demam_biasa'])

# Control System
diagnosa_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])#menggabungkan semua rule menjadi satu system
diagnosa = ctrl.ControlSystemSimulation(diagnosa_ctrl)#menjalakan simulasi fuzzy

# Input data pasien (seluruh input harus berhubungan dengan rule)
diagnosa.input['suhu'] = 38.8
diagnosa.input['batuk'] = 9

# Proses inferensi
diagnosa.compute() #melakukan fuzifikasi - inferensi - defuzifikasi

# Output hasil
print(f'Skor kemungkinan penyakit: {diagnosa.output["penyakit"]:.2f}')
