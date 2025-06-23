import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from pulp import LpMaximize, LpProblem, LpVariable


# ========== MENU 4: MODEL LAINNYA ==========

    st.title("Model Proyeksi Permintaan Motor")

    # Deskripsi singkat model
    st.write("Memprediksi permintaan motor di masa depan menggunakan regresi linear sederhana.")

    # Formulir input data historis penjualan
    st.markdown("Masukkan data historis penjualan:")
    # Masukan Harga 1 Unit Motor
    st.number_input("Masukan Harga 1 Unit Motor :", value=0)
    # Input tahun-tahun historis, dipisahkan koma
    years = st.text_input("Tahun-tahun (pisahkan dengan koma)", "2019,2020,2021,2022,2023")

    # Input data penjualan per tahun yang sesuai
    sales = st.text_input("Jumlah terjual per tahun (unit)", "2000,2200,2500,2700,3000")

    try:
        # Mengubah string input tahun menjadi array integer
        X = np.array([int(x) for x in years.split(",")])

        # Mengubah string input penjualan menjadi array integer
        Y = np.array([int(y) for y in sales.split(",")])

        # Mengecek apakah panjang data tahun dan penjualan cocok
        if len(X) != len(Y):
            st.error("Jumlah tahun dan data penjualan harus sama.")
        else:
            # ==========================
            # Proses Regresi Linear
            # ==========================

            # Menggunakan numpy.polyfit untuk mencari garis regresi linear: y = b*x + a
            coef = np.polyfit(X, Y, 1)  # coef[0] = b (slope), coef[1] = a (intercept)
            a, b = coef[1], coef[0]     # assign agar lebih mudah dibaca

            # Input tahun yang ingin diprediksi
            tahun_pred = st.number_input("Prediksi permintaan untuk tahun:", value=2025)

            # Menghitung hasil prediksi menggunakan rumus regresi: y = a + b*x
            prediksi = a + b * tahun_pred
            #Menghitung Harga Jual
            final_cost = cost * prediksi
            # Menampilkan hasil prediksi ke user
            st.success(f"Prediksi permintaan untuk tahun {tahun_pred}: {prediksi:.0f} unit")
            
            st.success(f"Total Biaya Untuk Tahun {tahun_pred} : Rp. {final_cost}")

            # ==========================
            # Visualisasi Garis Regresi
            # ==========================

            # Membuat array tahun untuk digambar di grafik (lebih rapat agar garis halus)
            x_plot = np.linspace(min(X)-1, max(X)+2, 100)

            # Menghitung nilai y (penjualan) berdasarkan garis regresi
            y_plot = a + b * x_plot

            # Membuat grafik
            fig, ax = plt.subplots()

            # Menampilkan titik data aktual (tahun vs penjualan)
            ax.plot(X, Y, 'o-', label='Data Aktual')

            # Menampilkan garis regresi (garis prediksi)
            ax.plot(x_plot, y_plot, 'r--', label='Regresi Linear')

            # Menandai tahun prediksi dengan garis vertikal
            ax.axvline(tahun_pred, color='gray', linestyle='--', label='Tahun Prediksi')

            # Menandai hasil prediksi dengan garis horizontal
            ax.axhline(prediksi, color='green', linestyle=':', label='Prediksi')

            # Memberi label sumbu dan legend
            ax.set_xlabel("Tahun")
            ax.set_ylabel("Jumlah Terjual (unit)")
            ax.legend()

            # Menampilkan grafik di Streamlit
            st.pyplot(fig)

    except:
        # Menangani kesalahan input jika user salah format angka/koma
        st.error("Pastikan input berupa angka dan dipisahkan dengan koma.")
