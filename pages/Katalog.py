import streamlit as st
import sqlite3
from pathlib import Path


# Streamlit sayfa yapılandırması
st.set_page_config(
    page_title=" KATALOG",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- DOSYA YOLLARI ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"


st.header('Katalog')

conn = sqlite3.connect("pizzadb.sqlite3")
c = conn.cursor()

c.execute("SELECT * FROM  pizzalar")
pizzalar = c.fetchall()


for  pizza in pizzalar:
    col1,col2,col3 = st.columns(3)
    with col1:
        st.image(pizza[5])
    with col2:
        st.subheader(pizza[0])
        st.write(pizza[4])
    with col3:
        st.write("Small",pizza[1],"₺")
        st.write("Medium",pizza[2],"₺")
        st.write("Large",pizza[3],"₺")