import streamlit as st
import sqlite3
from pathlib import Path


# Streamlit sayfa yapılandırması
st.set_page_config(
    page_title=" Sipariş Oluştur",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- DOSYA YOLLARI ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
conn = sqlite3.connect("pizzadb.sqlite3")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS siparisler(isim_soyisim TEXT, Adress TEXT, pizza TEXT, boy TEXT, icecek TEXT, fiyat REAL)")
conn.commit()

c.execute("SELECT isim FROM pizzalar")
isimler = c.fetchall()

isimlerlist = []

for i in isimler:
    isimlerlist.append(i[0])

st.header('Sipariş')

with st.form("Sipariş", clear_on_submit=True):
    isim_soyisim = st.text_input("İsim Soyisim")
    Adress = st.text_area("Adres")
    pizza = st.selectbox("Pizza Sec", isimlerlist)
    boy = st.selectbox("Boy", ["Small", "Medium", "Large"])
    icecek = st.selectbox("icecek", ["Ayran", "Soda", "Cola", " Ice Tea", "Su"])
    siparisver = st.form_submit_button("Sipariş Ver")
    
    if siparisver:
        if boy == "Small":
            c.execute("SELECT smfiyat FROM pizzalar WHERE isim = ?", (pizza,))
        elif boy == "Medium":
            c.execute("SELECT mdfiyat FROM pizzalar WHERE isim = ?", (pizza,))
        elif boy == "Large":
            c.execute("SELECT lgfiyat FROM pizzalar WHERE isim = ?", (pizza,))
        
        fiyat = c.fetchone()[0]  # Fiyatı alır
        
        icecek_fiyatları = {
            "Ayran": 15,
            "Cola": 40,
            "Soda": 30,
            "Su": 5,
            "Ice Tea": 30
        }
        
        icecek_fiyati = icecek_fiyatları[icecek]  # Seçilen içeceğin fiyatını alır
        
        toplam_fiyat = fiyat + icecek_fiyati  # Toplam fiyatı hesaplar
        
        c.execute("INSERT INTO siparisler VALUES(?,?,?,?,?,?)", (isim_soyisim, Adress, pizza, boy, icecek, toplam_fiyat))
        conn.commit()
        
        st.success(f"Sipariş Başarılı Bir Şekilde Gerçekleştirildi. Toplam Ücret: {toplam_fiyat} ₺")

conn.close()
