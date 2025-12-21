import streamlit as st
import yt_dlp
import pandas as pd
import time
import os
import re
import random
from googleapiclient.discovery import build
import isodate

st.set_page_config(page_title="Extractor Ilimitado RRSS", page_icon="🔥", layout="wide")

# Lista de identidades para evitar bloqueos
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
]

# --- LÓGICA DE YOUTUBE ---
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

# --- LÓGICA DE TIKTOK (VERSIÓN ILIMITADA) ---
def get_tt_data(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'user_agent': random.choice(USER_AGENTS),
        'ignoreerrors': True,
    }
    
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
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
        except: return None

# --- INTERFAZ ---
st.title("🔥 Extractor Masivo Ilimitado")

with st.sidebar:
    st.header("⚙️ Panel de Control")
    plataforma = st.selectbox("Selecciona plataforma:", ["YouTube", "TikTok"])
    api_key = ""
    if plataforma == "YouTube":
        api_key = st.text_input("YouTube API Key:", type="password")
    
    st.divider()
    st.info("💡 Consejo: Si usas TikTok, asegúrate de tener el archivo cookies.txt actualizado en la carpeta.")

urls_raw = st.text_area(f"Pega todos tus enlaces de {plataforma} aquí:", height=250, placeholder="Pega 10, 50 o 100 links...")

if st.button("🚀 Iniciar Extracción Total"):
    urls = [u.strip() for u in urls_raw.split('\n') if u.strip()]
    
    if urls:
        resultados = []
        fallidos = 0
        barra = st.progress(0)
        status = st.empty()
        
        for i, url in enumerate(urls):
            status.text(f"⏳ Procesando {i+1} de {len(urls)}...")
            
            if plataforma == "YouTube":
                data = get_yt_data(url, api_key)
            else:
                # Pausa aleatoria para evitar detección de bot
                time.sleep(random.uniform(1.5, 3.0)) 
                data = get_tt_data(url)
            
            if data:
                resultados.append(data)
            else:
                fallidos += 1
            
            barra.progress((i + 1) / len(urls))

        status.empty()

        if resultados:
            df = pd.DataFrame(resultados)
            st.success(f"✅ Finalizado: {len(resultados)} obtenidos con éxito. ❌ Fallidos: {fallidos}")
            
            # Mostrar Tabla Interactiva
            st.dataframe(df, use_container_width=True)
            
            # Resumen Totales
            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("Vistas Totales", f"{df['Vistas'].sum():,}")
            c2.metric("Likes Totales", f"{df['Likes'].sum():,}")
            c3.metric("Promedio Vistas", f"{int(df['Vistas'].mean()):,}")
            
            # Botón de Descarga
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar Excel (CSV)", csv, "reporte_ilimitado.csv", "text/csv")
        else:
            st.error("No se pudo extraer ningún dato. Verifica tus links o actualiza el archivo cookies.txt.")
