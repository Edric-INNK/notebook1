import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets using the correct relative paths
day_data = pd.read_csv('./data/day.csv')  # Correct path to data folder
hour_data = pd.read_csv('./data/hour.csv')  # Correct path to data folder

# Sidebar options - Only the data selection (Daily or Hourly) remains
data_option = st.sidebar.selectbox('Pilih Dataset:', ['Data Harian', 'Data Per Jam'])

# Load appropriate dataset based on user selection
if data_option == 'Data Harian':
    data = day_data
    st.title('Data Penyewaan Sepeda Harian')
else:
    data = hour_data
    st.title('Data Penyewaan Sepeda Per Jam')

st.write("""
*Welcome to dashboard perusahaan sepeda sewa ahaha*
Dashboard ini dibuat dalam rangka mempermudah perusahaan untuk memahami data harian dan bulanan mengenai sewa sepeda.

Di dashboard ini kita akan membahas dua hal utama:
1. Apakah perbedaan musim mempengaruhi jumlah penyewaan sepeda? jika iya, maka bagaimanakah terdampaknya? 
2. Apakah kondisi cuaca mempengaruhi jumlah penyewaan sepeda? jika iya, maka bagaimana juga dampaknya?
3. Kita juga akan membahas aksi berikutnya yang perusahaan harus ambil untuk memiliki daya saing yang lebih kuat

Berikut akan ditunjukkan beberapa grafik serta penjelasan dan bagaimana grafik tersebut dapat memberi dampak pada
jumlah penyewaan sepeda.
""")

# *Univariate Analysis*
st.write("### Analisis Univariat")
st.write("Distribusi Total Penyewaan Sepeda")
fig, ax = plt.subplots()
sns.histplot(day_data['cnt'], kde=True, bins=30, ax=ax)
ax.set_title("Distribusi Total Penyewaan Sepeda")
ax.set_xlabel("Total Penyewaan")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)

st.write("Distribusi Suhu Harian")
fig, ax = plt.subplots()
sns.histplot(day_data['temp'], kde=True, bins=30, color='red', ax=ax)
ax.set_title("Distribusi Suhu Harian")
ax.set_xlabel("Suhu (Normalized)")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)

st.write("""
*Penjelasan Grafik*
- Grafik pertama menunjukkan berapa banyak sepeda yang disewa per bulan (Jumlah/Bln) pada sumbu X, dengan sumbu Y menunjukkan seberapa sering jumlah tersebut terjadi.
- Grafik kedua menunjukkan suhu rata-rata harian, memberikan wawasan tentang pola suhu di daerah tersebut.
""")

# *Categorical Analysis*
st.write("### Analisis Kategorikal")
st.write("Frekuensi Penyewaan Berdasarkan Musim")
fig, ax = plt.subplots()
sns.countplot(x='season', data=day_data, palette='pastel', ax=ax)
ax.set_title("Frekuensi Penyewaan Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Frekuensi")
ax.set_xticks(range(4))
ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'], rotation=45)
st.pyplot(fig)

st.write("Frekuensi Penyewaan Berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots()
sns.countplot(x='weathersit', data=day_data, palette='cool', ax=ax)
ax.set_title("Frekuensi Penyewaan Berdasarkan Kondisi Cuaca")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Frekuensi")
ax.set_xticks(range(4))
ax.set_xticklabels([
    'Cerah / Sedikit Berawan', 
    'Berkabut / Berawan', 
    'Hujan Ringan / Salju', 
    'Hujan Deras / Badai Salju'
], rotation=45)
st.pyplot(fig)

st.write("""
*Penjelasan Grafik*
- Grafik pertama menunjukkan jumlah penyewaan sepeda berdasarkan musim. Grafik ini memberikan wawasan tentang pola penyewaan yang berbeda pada setiap musim.
- Grafik kedua menunjukkan jumlah penyewaan sepeda berdasarkan kondisi cuaca. Grafik ini memberikan wawasan tentang bagaimana cuaca dapat memengaruhi keputusan untuk menyewa sepeda.
""")

# *Multivariate Analysis: Hubungan Suhu dengan Penyewaan*
st.write("### Analisis Multivariat")
st.write("### Hubungan Suhu dengan Penyewaan Sepeda")
fig, ax = plt.subplots()
sns.scatterplot(
    x='temp', y='cnt', hue='season', data=data, palette='viridis', ax=ax
)
ax.set_title("Hubungan Suhu dengan Penyewaan Sepeda Berdasarkan Musim")
ax.set_xlabel("Suhu Normalized")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

# *Analisis Multivariat: Hubungan Kelembapan dengan Penyewaan*
st.write("### Hubungan Kelembapan dengan Penyewaan Sepeda")
fig, ax = plt.subplots()
sns.scatterplot(
    x='hum', y='cnt', hue='season', data=data, palette='coolwarm', ax=ax
)
ax.set_title("Hubungan Kelembapan dengan Penyewaan Sepeda Berdasarkan Musim")
ax.set_xlabel("Kelembapan")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

# *Heatmap Korelasi antar Fitur Numerik*
st.write("### Heatmap Korelasi Antar Fitur")
corr = data[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
ax.set_title("Korelasi Antar Fitur")
st.pyplot(fig)

# *Penjelasan Grafik*
st.write("""
*Penjelasan Grafik*
- Grafik pertama menunjukkan scatterplot yang mendetailkan jumlah total penyewaan di sumbu Y berdasarkan suhu normal yang ada di sekitar area (sumbu X). Warna pada tiap titik menunjukkan musim penyewaan.
- Grafik kedua menunjukkan scatterplot yang mendetailkan jumlah penyewaan sepeda di sumbu Y berdasarkan kelembapan di sumbu X, dengan warna titik-titik scatterplot berdasarkan musim.
- Grafik ketiga menunjukkan korelasi antara fitur-fitur yang ada dalam file CSV seperti temp, atemp, hum, windspeed, dan cnt.
""")

# **Pertanyaan Bisnis 1:** Apakah perbedaan musim mempengaruhi pola penggunaan / penyewaan sepeda?
st.write("### Total Penyewaan Sepeda Berdasarkan Musim")
seasonal_rentals = data.groupby('season')['cnt'].sum()
fig, ax = plt.subplots()
seasonal_rentals.plot(kind='bar', ax=ax, color='orange')
ax.set_title('Total Penyewaan Sepeda Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Total Penyewaan')
ax.set_xticks(range(len(seasonal_rentals.index)))
ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'], rotation=45)
st.pyplot(fig)

st.write("""
- Dari sini kita dapat melihat bahwa iya, musim mempengaruhi berapa banyak sepeda yang digunakan / disewakan.
- Lebih tepatnya, di musim-musim menjelang musim dingin (Fall / musim gugur memiliki hawa yang nyaman untuk bersepeda (harusnya))
""")

# **Pertanyaan Bisnis 2:** Apakah cuaca memiliki dampak terhadap penyewaan sepeda?
st.write("### Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
weather_rentals = data.groupby('weathersit')['cnt'].mean()
fig, ax = plt.subplots()
weather_rentals.plot(kind='bar', ax=ax, color='green')
ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Rata-rata Penyewaan')

# Dynamically set xticks and labels based on the data available
ax.set_xticks(range(len(weather_rentals.index)))
weather_labels = [
    'Cerah / Sedikit Berawan', 
    'Berkabut / Berawan', 
    'Hujan Ringan / Salju', 
    'Hujan Deras / Badai Salju'
][:len(weather_rentals.index)]  # Slice labels to match the number of categories
ax.set_xticklabels(weather_labels, rotation=45)

st.pyplot(fig)

st.write("""
**Insight:**
- Pertanyaan bisnis pertama telah terjawab, bahwa iya, musim memiliki dampak terhadap penyewaan sepeda.
- Pertanyaan bisnis kedua juga sudah terjawab, bahwa cuaca (tidak terikat dengan perbedaan musim) pun juga memiliki dampak terhadap penyewaan sepeda.
""")

# **Menampilkan Statistik Dasar untuk Data yang Disaring**
st.write("### Statistik Dasar untuk Data yang Disaring")
st.write(data.describe())

# **Kesimpulan untuk Pertanyaan Bisnis 1 dan 2**
st.write("""
## Kesimpulan:
### Kesimpulan Pertanyaan 1:
Iya, musim memberikan dampak terhadap jumlah penyewaan sepeda. Pada musim gugur dan musim dingin, penyewa akan lebih cenderung menyewa sepeda karena suhu yang lebih sejuk dan udara yang nyaman. Di musim panas, orang juga cenderung lebih tertarik untuk bersepeda karena banyaknya aktivitas luar ruangan di musim panas. Ini menjelaskan mengapa penyewaan lebih tinggi pada musim-musim tersebut.
    
### Kesimpulan Pertanyaan 2:
Cuaca juga memberikan efek yang signifikan terhadap jumlah penyewaan sepeda. Penyewa akan lebih cenderung untuk menyewa sepeda ketika langit cerah dan tidak ada hujan. Penyewa juga menyewa sepeda saat cuaca berkabut atau mendung karena udara lebih sejuk. Namun, ketika terjadi hujan ringan atau badai salju, jumlah penyewaan sepeda turun drastis, karena orang lebih memilih untuk tidak bersepeda saat cuaca buruk.

### Aksi Berikutnya untuk Perusahaan:
- Melakukan marketing yang sesuai dengan musim, dengan fokus pada aktivitas luar ruangan pada musim panas dan musim semi, serta mempromosikan suasana sejuk untuk bersepeda di musim dingin dan gugur.
- Memantau ramalan cuaca untuk memperkirakan hujan atau cuaca buruk agar perusahaan dapat merencanakan operasional dan anggaran dengan lebih baik pada hari-hari ketika penyewaan sepeda berkurang.
""")
        