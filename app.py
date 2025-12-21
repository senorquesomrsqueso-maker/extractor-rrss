import streamlit as st
import yt_dlp
import pandas as pd
import time
import os
import re
import random
from googleapiclient.discovery import build
import isodate

# Configuración de la página
st.set_page_config(page_title="Extractor Data RRSS", page_icon="📈", layout="wide")

# --- FUNCIONES DE YOUTUBE ---
def get_yt_data(url, api_key):
    try:
        video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if not video_id_match: return None
        video_id = video_id_match.group(1)
        
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.videos().list(part="snippet,statistics,contentDetails", id=video_id)
        response = request.execute()
        item = response['items'][0]
        
        duracion_iso = item['contentDetails']['duration']
        segundos = isodate.parse_duration(duracion_iso).total_seconds()
        
        tipo = "Short" if ("/shorts/" in url.lower() or segundos <= 61) else "Video Largo"
        
        return {
            "Plataforma": "YouTube",
            "Tipo": tipo,
            "Título/Autor": item['snippet']['title'],
            "Vistas": int(item['statistics']['viewCount']),
            "Likes": int(item['statistics'].get('likeCount', 0)),
            "Link": url
        }
    except: return None

# --- FUNCIONES DE TIKTOK ---
def get_tt_data(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True, 
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Pausa moderada para no ser bloqueado
            time.sleep(random.uniform(2, 4)) 
            info = ydl.extract_info(url, download=False)
            if not info: return None
            
            return {
                "Plataforma": "TikTok",
                "Tipo": "TikTok",
                "Título/Autor": info.get('uploader') or info.get('title', 'Video TikTok'),
                "Vistas": int(info.get('view_count', 0)),
                "Likes": int(info.get('like_count', 0)),
                "Link": url
            }
        except: return None

# --- INTERFAZ ---
st.title("📈 Extractor Masivo: YouTube & TikTok")

with st.sidebar:
    st.header("⚙️ Configuración")
    plataforma = st.selectbox("Elige plataforma:", ["YouTube", "TikTok"])
    api_key = ""
    if plataforma == "YouTube":
        api_key = st.text_input("YouTube API Key:", type="password")
    
    st.divider()
    if os.path.exists('cookies.txt'):
        st.success("✅ Cookies detectadas")
    else:
        st.warning("⚠️ Sin 'cookies.txt'")

urls_input = st.text_area(f"Pega tus enlaces de {plataforma} aquí:", height=200)

if st.button("🚀 Procesar Todo"):
    lista_urls = [line.strip() for line in urls_input.split('\n') if line.strip()]
    
    if lista_urls:
        resultados = []
        fallidos = []
        barra = st.progress(0)
        
        for i, url in enumerate(lista_urls):
            data = get_yt_data(url, api_key) if plataforma == "YouTube" else get_tt_data(url)
            
            if data and data.get("Vistas", 0) > 0:
                resultados.append(data)
            else:
                fallidos.append(url)
            
            barra.progress((i + 1) / len(lista_urls))
        
        if resultados:
            df = pd.DataFrame(resultados)
            st.subheader("📊 Tabla de Resultados")
            st.dataframe(df, use_container_width=True)
            
            # --- TOTALES ---
            st.divider()
            col1, col2 = st.columns(2)
            col1.metric("🔥 SUMA TOTAL VISTAS", f"{df['Vistas'].sum():,}")
            col2.metric("👍 SUMA TOTAL LIKES", f"{df['Likes'].sum():,}")
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar CSV", csv, "reporte.csv", "text/csv")
            
        if fallidos:
            st.divider()
            with st.expander("❌ Ver enlaces que fallaron"):
                for f in fallidos:
                    st.write(f"- {f}")
