import io
import zipfile

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Dasbor
st.set_page_config(page_title="Tiby - Dasbor Pengujian Sistem", layout="wide")

st.title("Dasbor Hasil Pengujian Sistem dan Evaluasi Keselamatan Tiby")
st.caption("Laporan Penjaminan Kualitas Internal • Lomba Pengembangan Web UINIC 8.0")

# 2. Pembacaan Data Langsung dari Berkas CSV
DATA_DIR = "data"

try:
    df_suara = pd.read_csv(f"{DATA_DIR}/sampel_suara.csv")
    df_tot = pd.read_csv(f"{DATA_DIR}/time_on_task.csv")
    df_ueqs = pd.read_csv(f"{DATA_DIR}/ueq_s.csv")
    df_ringkasan = pd.read_csv(f"{DATA_DIR}/ringkasan.csv")
except Exception as e:
    st.error(f"Gagal membaca berkas data di folder {DATA_DIR}/. Pastikan folder data berada di folder yang sama. Detail: {e}")
    st.stop()

# 3. Kartu Ringkasan Metrik
k1, k2, k3, k4 = st.columns(4)
k1.metric("Keberhasilan Tugas", "100%", "Target: ≥80%")
k2.metric("Sensitivitas Tanda Bahaya", "98,0%", "49 dari 50 Kasus")
k3.metric("Kepatuhan Penanganan Aman", "100%", "Sesuai Standar")
k4.metric("Rata-rata Skor UEQ-S", "+1,84", "Predikat: Sangat Baik")

st.divider()

# 4. Tombol Unduh Data Dummy (ZIP berisi 4 CSV)
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
    for nama in ["sampel_suara.csv", "time_on_task.csv", "ueq_s.csv", "ringkasan.csv"]:
        zf.write(f"{DATA_DIR}/{nama}", arcname=nama)
st.download_button(
    label="📥 Unduh Dokumen Lengkap Pengujian (.ZIP)",
    data=buf.getvalue(),
    file_name="data-dummy-pengujian-tiby.zip",
    mime="application/zip",
    help="Klik untuk mengunduh berkas data dummy (4 CSV: 50 sampel suara, time on task, UEQ-S, ringkasan).",
)

# 5. Tab Navigasi Data dan Visualisasi
tab_grafik, tab_suara, tab_waktu, tab_kuesioner = st.tabs([
    "📊 Dasbor Visual & Grafik",
    "🎙️ 50 Sampel Suara & Aturan Keselamatan",
    "⏱️ Waktu Pengerjaan Tugas (Time on Task)",
    "📋 Kuesioner UEQ-S"
])

with tab_grafik:
    kolom_kiri, kolom_kanan = st.columns(2)

    with kolom_kiri:
        st.subheader("Matriks Klasifikasi Deteksi Bahaya")
        data_matriks = [[49, 1], [0, 50]]
        grafik_matriks = px.imshow(
            data_matriks,
            x=['Terdeteksi Bahaya', 'Lolos'],
            y=['Kondisi Nyata Bahaya', 'Kondisi Nyata Aman'],
            color_continuous_scale='Teal',
            text_auto=True,
        )
        grafik_matriks.update_layout(xaxis_title='', yaxis_title='')
        st.plotly_chart(grafik_matriks, use_container_width=True)

    with kolom_kanan:
        st.subheader("Rata-rata Durasi Pengerjaan Tugas (Detik)")
        data_grafik_durasi = pd.DataFrame({
            "Alur Tugas": [
                "T1: Masuk Akun",
                "T2: Lapor Suara",
                "T3: Tombol Cadangan",
                "T4: Bot WhatsApp",
                "T5: Input Data Faskes"
            ],
            "Durasi (Detik)": [28.0, 39.0, 19.0, 24.0, 52.0]
        })
        grafik_batang = px.bar(
            data_grafik_durasi,
            x="Alur Tugas",
            y="Durasi (Detik)",
            color="Durasi (Detik)",
            color_continuous_scale="Teal"
        )
        st.plotly_chart(grafik_batang, use_container_width=True)

with tab_suara:
    st.subheader("Data Pengujian 50 Sampel Suara dan Aturan Keselamatan")
    st.caption("Menampilkan data pengujian masukan suara sehari-hari, kondisi suara tak jelas, dan deteksi kegawatdaruratan.")
    st.dataframe(df_suara, use_container_width=True, height=500)

with tab_waktu:
    st.subheader("Pengukuran Efisiensi dan Durasi Pengerjaan Tugas (Time on Task)")
    st.caption("Pencatatan waktu pengerjaan 5 tugas utama oleh 6 partisipan uji.")
    st.dataframe(df_tot, use_container_width=True)

with tab_kuesioner:
    st.subheader("Data Mentah Pengukuran Kuesioner Pengalaman Pengguna (UEQ-S)")
    st.caption("Hasil evaluasi 8 pasangan skala kata sifat untuk mengukur Kualitas Pragmatis dan Kualitas Hedonis.")
    st.dataframe(df_ueqs, use_container_width=True)
