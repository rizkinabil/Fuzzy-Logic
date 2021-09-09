import pandas as pd


df = pd.read_csv('restoran.csv')
makanan = list(df['makanan'])
pelayanan = list(df['pelayanan'])
id_restoran = list(df['id'])


#fuzzification
buruk = tidak_enak = cukup_p = cukup_m = bagus = enak = 0
# array_rating_resto = []

def skala_pelayanan(var_pelayanan):
  global buruk, cukup_p, bagus
  if var_pelayanan <= 30:
    buruk = 1
  elif var_pelayanan >= 30 and var_pelayanan < 40:
    buruk = (40-var_pelayanan)/(40-30)
    cukup_p = (var_pelayanan-30)/(40-30)
  elif var_pelayanan >= 40 and var_pelayanan < 60:
    cukup_p = 1
  elif var_pelayanan >= 60 and var_pelayanan < 70:
    cukup_p = (70-var_pelayanan)/(70-60)
    bagus = (var_pelayanan - 60)/(70-60)
  elif var_pelayanan >= 70 and var_pelayanan <= 100:
    bagus = 1


def skala_makanan(var_makanan):
  global tidak_enak, cukup_m, enak
  if var_makanan <= 3:
    tidak_enak = 1
  elif var_makanan >= 3 and var_makanan < 4:
    tidak_enak = (4-var_makanan)/4-3
    cukup_m = (var_makanan-3)/(4-3)
  elif var_makanan >= 4 and var_makanan < 6:
    cukup_m = 1
  elif var_makanan >= 6 and var_makanan < 7:
    cukup_m = (7-var_makanan)/(7-6)
    enak = (var_makanan-6)/(7-6)
  elif var_makanan >= 7 and var_makanan <=10:
    enak = 1




#fuzzy inference
rating = []
def ratingRendah(var_pelayanan, var_makanan):
  global rating
  if var_pelayanan != 0:
    if var_makanan != 0:
      hasil = min(var_pelayanan, var_makanan)
      rating.append([hasil,30])
  # print(rating)
def ratingSedang(var_pelayanan, var_makanan):
  global rating
  if var_pelayanan != 0:
    if var_makanan != 0:
      hasil = min(var_pelayanan, var_makanan)
      rating.append([hasil, 60])
def ratingTinggi(var_pelayanan, var_makanan):
  global rating
  if var_pelayanan != 0:
    if var_makanan != 0:
      hasil = min(var_pelayanan, var_makanan)
      rating.append([hasil, 100])




#hitung inferensi

def infrensi(kualitas_p, kualitas_m):
  skala_pelayanan(kualitas_p)
  skala_makanan(kualitas_m)
  ratingRendah(buruk, tidak_enak)
  ratingRendah(buruk, cukup_m)
  ratingRendah(buruk, enak)
  ratingRendah(cukup_p, tidak_enak)
  ratingSedang(cukup_p, cukup_m)
  ratingSedang(bagus, tidak_enak)
  ratingTinggi(cukup_p, enak)
  ratingTinggi(bagus, cukup_m)
  ratingTinggi(bagus, enak)



#defuzifikasi
def defuzifikasi():
  pengali = 0
  pembagi = 0
  for i in range(0,len(rating)):
    atas = rating[i][0]*rating[i][1]
    bawah = rating[i][0]
    pengali = pengali + atas
    pembagi = pembagi + bawah
  z = (atas / bawah)
  return z




# rating = []
# infrensi(100, 10)
# print(rating)
# nilai = defuzifikasi()
# print(nilai)

array_rating_resto = []
for i in range(0, len(id_restoran)):
  
  buruk = tidak_enak = cukup_p = cukup_m = bagus = enak = 0
  infrensi(pelayanan[i], makanan[i])
  nilai = defuzifikasi()
  array_rating_resto.append(nilai)
  # print(rating)
  rating = []

print(array_rating_resto)
hasil_akhir = sorted(array_rating_resto, reverse = True)
id_hasil = id_restoran[:10]
hasil_csv = {'rating' : hasil_akhir[:10], 'id_resto' : id_hasil} 

result_csv = pd.DataFrame(hasil_csv, columns= ['id_resto','rating'])
result_csv.to_csv('hasil.csv')
