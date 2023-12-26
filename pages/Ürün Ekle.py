import streamlit as st
import sqlite3
from pathlib import Path


# Streamlit sayfa yapılandırması
st.set_page_config(
    page_title=" Ürün Ekle",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- DOSYA YOLLARI ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

# Veritabanı bağlantısı oluşturma veya var olanı kullanma
conn = sqlite3.connect("pizzadb.sqlite3")
c = conn.cursor()

# Eğer yoksa "pizzalar" adında bir tablo oluşturalım
c.execute("CREATE TABLE IF NOT EXISTS pizzalar(isim TEXT, smfiyat REAL, mdfiyat REAL, lgfiyat REAL, Icindekiler TEXT, resim TEXT)")
conn.commit()

# Streamlit arayüzü oluşturma
st.header('Pizza Ekle')

with st.form('Pizza Ekle', clear_on_submit=True):
    isim = st.text_input('Pizza İsmi')
    smfiyat = st.number_input('Small Fiyat')
    mdfiyat = st.number_input('Medium Fiyat')
    lgfiyat = st.number_input('Large Fiyat')
    Icindekiler = st.multiselect('İçindekiler', ["Mantar", "Janbon", "Sucuk", "Zeytin", "Tavuk", "Ton Balığı", "Fesleğen", "Salam", "Mısır", "Biber", "Ekstra Peynir"])
    resim = st.file_uploader("Resim Yükle")
    ekle = st.form_submit_button("Ekle")

    if ekle:
        if not isim or smfiyat <= 0 or mdfiyat <= 0 or lgfiyat <= 0 or not Icindekiler or not resim:
            st.warning("Lütfen tüm alanları doldurun.")
        else:
            try:
                Icindekiler = str(Icindekiler).replace("[", "").replace("]", "").replace("'", "")
                resimurl = "img/" + resim.name
                open(resimurl, "wb").write(resim.read())
                c.execute("INSERT INTO pizzalar VALUES (?, ?, ?, ?, ?, ?)", (isim, smfiyat, mdfiyat, lgfiyat, Icindekiler, resimurl))
                conn.commit()
                st.success("Pizza Başarıyla eklendi.")
            except sqlite3.Error as e:
                st.error(f"Veritabanı Hatası: {e}")

# # Veritabanındaki pizzaları gösterme
# st.header('Mevcut Pizzalar')
# c.execute("SELECT * FROM pizzalar")
# pizzalar = c.fetchall() #veri tabanını ekrana yansıtır.

# for pizza in pizzalar:
#     st.write(f"**Pizza İsmi:** {pizza[0]}")
#     st.write(f"**Fiyatlar:** Small: {pizza[1]}, Medium: {pizza[2]}, Large: {pizza[3]}")
#     st.write(f"**İçindekiler:** {pizza[4]}")
#     st.image(pizza[5], caption='Pizza', width=150)
#     st.write('---')
    
# Veritabanındaki pizzaları gösterme
st.header('Menüye Eklenen Son Pizza')
c.execute("SELECT * FROM pizzalar ORDER BY ROWID DESC LIMIT 1")
son_eklenen_pizza = c.fetchone()

if son_eklenen_pizza:
    st.write(f"**Pizza İsmi:** {son_eklenen_pizza[0]}")
    st.write(f"**Fiyatlar:** Small: {son_eklenen_pizza[1]}, Medium: {son_eklenen_pizza[2]}, Large: {son_eklenen_pizza[3]}")
    st.write(f"**İçindekiler:** {son_eklenen_pizza[4]}")
    st.image(son_eklenen_pizza[5], caption='Pizza', width=150)
else:
    st.write("Henüz pizza eklenmemiş.")

# Veritabanı bağlantısını kapatma
conn.close()
