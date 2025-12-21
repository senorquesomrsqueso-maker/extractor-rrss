import streamlit as st
import yt_dlp
import pandas as pd
import time
import os
import re
from googleapiclient.discovery import build
import isodate

st.set_page_config(page_title="Extractor Pro RRSS", page_icon="📊", layout="wide")

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
        'extract_flat': False, # Cambiado a False para forzar la lectura del video real
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Esta línea resuelve el link vm.tiktok.com al link real
            info = ydl.extract_info(url, download=False)
            if not info: return None
            
            return {
                "Plataforma": "TikTok",
                "Tipo": "TikTok",
                "Título/Autor": info.get('uploader') or info.get('title', 'Video'),
                "Vistas": int(info.get('view_count') or 0),
                "Likes": int(info.get('like_count') or 0),
                "Link": url
            }
        except Exception:
            return None

# --- INTERFAZ ---
st.title("📊 Extractor de Datos: YouTube & TikTok")

with st.sidebar:
    st.header("Configuración")
    plataforma = st.selectbox("Selecciona plataforma:", ["YouTube", "TikTok"])
    api_key = ""
    if plataforma == "YouTube":
        api_key = st.text_input("YouTube API Key:", type="password")

urls_raw = st.text_area(f"Pega tus enlaces de {plataforma} (uno por línea):", height=200)

if st.button("🚀 Extraer Datos"):
    urls = [u.strip() for u in urls_raw.split('\n') if u.strip()]
    
    if urls:
        resultados = []
        barra = st.progress(0)
        
        for i, url in enumerate(urls):
            if plataforma == "YouTube":
                data = get_yt_data(url, api_key)
            else:
                # Pausa necesaria para que TikTok no bloquee la IP
                time.sleep(2) 
                data = get_tt_data(url)
            
            if data: resultados.append(data)
            barra.progress((i + 1) / len(urls))

        if resultados:
            df = pd.DataFrame(resultados)
            st.success(f"✅ Éxito: {len(resultados)} resultados obtenidos.")
            st.dataframe(df, use_container_width=True)
            
            # Resumen Totales
            st.divider()
            col1, col2 = st.columns(2)
            col1.metric("Suma Total Vistas", f"{df['Vistas'].sum():,}")
            col2.metric("Suma Total Likes", f"{df['Likes'].sum():,}")
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar Excel (CSV)", csv, "reporte.csv", "text/csv")
        else:
            st.error("No se pudo obtener información. Asegúrate de que el archivo cookies.txt esté actualizado.")
