import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# Streamlit sayfa yapılandırması
st.set_page_config(
    page_title="Sipariş Uygulaması",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- DOSYA YOLLARI ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

# Streamlit başlık
st.markdown("""
    <div style='text-align:center'>
        <h1>HomePage</h1>
    </div>
""", unsafe_allow_html=True)

# SQLite veritabanı bağlantısı
conn = sqlite3.connect("pizzadb.sqlite3")
c = conn.cursor()

# Veritabanından veri çekme
c.execute("SELECT * FROM siparisler")
siparisler = c.fetchall()

# Verileri bir DataFrame'e dönüştürme ve sütun adlarını ayarlama
df = pd.DataFrame(siparisler)
df.columns = ["isim_soyisim", "Adress", "pizza", "boy", "icecek", "toplam_fiyat"]

# Adrese göre filtreleme için kullanıcı girişi
filter_address = st.text_input("Enter the address you want to filter")

# Adrese göre verileri filtreleme
filtered_df = df[df['Adress'].str.contains(filter_address, case=False)]

# # DataFrame'i Streamlit arayüzünde tablo olarak gösterme
# st.table(df)
# Filtrelenmiş verileri gösterme
st.table(filtered_df)
# Sipariş sayısını hesaplama
num_orders = len(df)

# Sipariş sayısını başarı mesajıyla kullanıcıya bildirme
st.success(f"Toplam {num_orders} adet siparişiniz vardır.", icon="✅")






