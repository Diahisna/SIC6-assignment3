import streamlit as st # untuk Streamlit
from pymongo import MongoClient # untuk MongoDB
import pandas as pd # untuk manipulasi data

# === Koneksi MongoDB ===
MONGO_API_KEY = st.secrets["MONGO_API_KEY"]  # ambil dari secrets
client = MongoClient(f"mongodb+srv://Diah:{MONGO_API_KEY}@cluster0.hco8p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["MyDatabase"]
collection = db["AudioCollection"]

# === Judul untuk ditampilkan pada streamlit ===
st.set_page_config(page_title="Audio Analysis Dashboard", layout="wide")
st.title("🎧 Audio Analysis Dashboard")

# Ambil data dari MongoDB
docs = list(collection.find().sort("timestamp", -1))  # urutkan dari terbaru

if not docs:
    st.warning("Belum ada data yang dianalisis.")
else:
    # Sidebar untuk pilih file
    filenames = [doc["filename"] for doc in docs]
    selected_filename = st.sidebar.selectbox("Pilih file audio", filenames)

    # Ambil dokumen yang dipilih
    selected_doc = next((doc for doc in docs if doc["filename"] == selected_filename), None)

    if selected_doc:
        st.subheader(f"📄 Informasi File: {selected_doc['filename']}")
        st.markdown(f"*🕒 Timestamp*: {selected_doc['timestamp']}")
        st.markdown(f"*🔗 Google Drive*: [Lihat File]({selected_doc['drive_url']})")

        # Optional: Embed audio (kalau public)
        st.audio(f"https://drive.google.com/uc?export=download&id={selected_doc['drive_url'].split('/d/')[1].split('/')[0]}", format="audio/wav")

        st.markdown("---")
        st.subheader("📝 Transkrip")
        st.write(selected_doc["transcript"])

        st.markdown("---")
        st.subheader("🧠 Ringkasan (dengan fact-check)")
        st.write(selected_doc["summary"])

        st.markdown("---")
        st.subheader("🔍 Hasil Fact Check")
        for item in selected_doc["fact_check"]:
            st.markdown(f"*Claim:* {item['claim']}")
            st.markdown(f"> 💡 {item['explanation']}")
            st.markdown("---")