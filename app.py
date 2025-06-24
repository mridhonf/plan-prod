import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from io import BytesIO

st.title("Model Proyeksi Permintaan Motor")
st.write("Memprediksi permintaan motor di masa depan menggunakan regresi linear sederhana.")

# Input data historis
st.markdown("Masukkan data historis penjualan:")
harga = st.number_input("Masukan Harga 1 Unit Motor : ", value=0)
years = st.text_input("Tahun-tahun (pisahkan dengan koma)", "2019,2020,2021,2022,2023")
sales = st.text_input("Jumlah terjual per tahun (unit)", "2000,2200,2500,2700,3000")

try:
    X = np.array([int(x) for x in years.split(",")])
    Y = np.array([int(y) for y in sales.split(",")])

    if len(X) != len(Y):
        st.error("Jumlah tahun dan data penjualan harus sama.")
    else:
        coef = np.polyfit(X, Y, 1)
        a, b = coef[1], coef[0]
        tahun_pred = st.number_input("Prediksi permintaan untuk tahun:", value=2025)
        prediksi = a + b * tahun_pred
        final_cost = harga * prediksi

        st.success(f"Prediksi permintaan untuk tahun {tahun_pred}: {prediksi:.0f} unit")
        st.success(f"Total Biaya Untuk Tahun {tahun_pred} : Rp. {final_cost:.0f}")

        # Visualisasi grafik
        x_plot = np.linspace(min(X)-1, max(X)+2, 100)
        y_plot = a + b * x_plot
        fig, ax = plt.subplots()
        ax.plot(X, Y, 'o-', label='Data Aktual')
        ax.plot(x_plot, y_plot, 'r--', label='Regresi Linear')
        ax.axvline(tahun_pred, color='gray', linestyle='--', label='Tahun Prediksi')
        ax.axhline(prediksi, color='green', linestyle=':', label='Prediksi')
        ax.set_xlabel("Tahun")
        ax.set_ylabel("Jumlah Terjual (unit)")
        ax.legend()
        st.pyplot(fig)

        # ========= EXPORT AREA =========
        # Data untuk disimpan
        data_export = pd.DataFrame({
            "Tahun": X.tolist() + [tahun_pred],
            "Jumlah Terjual": Y.tolist() + [round(prediksi)],
            "Keterangan": ["Data Historis"] * len(X) + ["Prediksi"]
        })

        # Export ke Excel
        buffer_excel = BytesIO()
        with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
            data_export.to_excel(writer, index=False, sheet_name='Hasil Prediksi')
            df_biaya = pd.DataFrame({
                "Tahun Prediksi": [tahun_pred],
                "Prediksi Permintaan": [round(prediksi)],
                "Harga per Unit": [harga],
                "Total Biaya": [round(final_cost)]
            })
            df_biaya.to_excel(writer, sheet_name='Biaya', index=False)
        st.download_button("📥 Export ke Excel (.xlsx)", data=buffer_excel.getvalue(), file_name="hasil_prediksi.xlsx")

        # Export ke PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Laporan Prediksi Permintaan Motor", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.ln(10)

        pdf.cell(0, 10, f"Tanggal Export: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", ln=True)
        pdf.cell(0, 10, f"Tahun Prediksi: {tahun_pred}", ln=True)
        pdf.cell(0, 10, f"Prediksi Permintaan: {round(prediksi)} unit", ln=True)
        pdf.cell(0, 10, f"Harga per Unit: Rp. {harga}", ln=True)
        pdf.cell(0, 10, f"Total Biaya: Rp. {round(final_cost)}", ln=True)

        pdf_output = BytesIO()
        pdf.output(pdf_output)
        st.download_button("📄 Export ke PDF", data=pdf_output.getvalue(), file_name="hasil_prediksi.pdf")

except Exception as e:
    st.error(f"Terjadi kesalahan input atau perhitungan: {str(e)}")
