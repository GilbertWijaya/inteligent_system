import pandas as pd
import math

# Baca file CSV
data = pd.read_csv("data_rumah.csv")

# Cek isi data
print(data)

# Ambil kolom
X = data["LuasBangunan"]
Y = data["HargaRumah"]

# Tampilkan data mentahnya
# print("Luas Bangunan (X):", x.to_list())
# print("Harga Rumah (Y):", y.to_list())

DATA_TOTAL = len(data)
X_TOTAL = X.sum()
X_SQUARE = (X**2).sum()
X_AVERAGE = X.mean()
Y_TOTAL = Y.sum()
Y_AVERAGE = Y.mean()
XY = (X * Y).sum()


b = (((DATA_TOTAL*XY ) - (X_TOTAL * Y_TOTAL)) / ((DATA_TOTAL * X_SQUARE) - (X_TOTAL**2))).round(3)
a = (Y_AVERAGE - (b * X_AVERAGE)).round(3)
Y_AKSEN = (a + (b * X)).round(3)
Y_AASQUARE = ((Y - Y_AKSEN)**2).round(3)
Y_AASQUARE_TOTAL = Y_AASQUARE.sum().round(3)
TAKSIR_STANDAR = math.sqrt((Y_AASQUARE_TOTAL / (DATA_TOTAL - 2)))

PREDICTION = 160

# print("Prediksi Harga Rumah dengan Luas Bangunan {} m2: {:.3f}".format(PREDICTION, (a + (b * PREDICTION)).round(3)))
# print("Batas Atas Harga Rumah dengan Luas Bangunan : {:.3f}".format(((a + (b * PREDICTION)).round(3)) + TAKSIR_STANDAR))
# print("Batas Bawah Harga Rumah dengan Luas Bangunan : {:.3f}".format(((a + (b * PREDICTION)).round(3)) - TAKSIR_STANDAR))

print(f"Prediksi Harga Rumah dengan Luas Bangunan {X} m2: {(a + (b * X))}")


# print("Persamaan Regresi Linear: Y = {:.3f} + {:.3f}X".format(a, b))