import streamlit as st
import yt_dlp
import pandas as pd
import time
import os
import re
import random
from googleapiclient.discovery import build
import isodate

st.set_page_config(page_title="Extractor Pro v3", page_icon="📸", layout="wide")

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
            "Plataforma": "YouTube", "Tipo": tipo, "Título/Autor": item['snippet']['title'],
            "Vistas": int(item['statistics']['viewCount']), "Likes": int(item['statistics'].get('likeCount', 0)), "Link": url
        }
    except: return None

# --- LÓGICA DE TIKTOK REFORZADA PARA FOTOS ---
def get_tt_data(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        # Usamos un User-Agent de móvil más moderno para evitar el bloqueo en fotos
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
        'referer': 'https://www.tiktok.com/',
    }
    
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Pausa humana más larga para carruseles de fotos
            time.sleep(random.uniform(4, 6))
            info = ydl.extract_info(url, download=False)
            
            if not info: return None
            
            # Detectar si es carrusel o video
            es_foto = info.get('playlist_count') is not None or "/photo/" in info.get('webpage_url', '')
            tipo_contenido = "TikTok (Foto)" if es_foto else "TikTok (Video)"
            
            return {
                "Plataforma": "TikTok",
                "Tipo": tipo_contenido,
                "Título/Autor": info.get('uploader') or info.get('creator') or "Contenido TikTok",
                "Vistas": int(info.get('view_count') or 0),
                "Likes": int(info.get('like_count') or 0),
                "Link": url
            }
        except: return None

# --- INTERFAZ ---
st.title("📈 Extractor Pro: YouTube & TikTok (Fotos y Videos)")

with st.sidebar:
    st.header("⚙️ Panel")
    plataforma = st.selectbox("Plataforma:", ["YouTube", "TikTok"])
    api_key = st.text_input("YouTube API Key:", type="password") if plataforma == "YouTube" else ""
    st.divider()
    if os.path.exists('cookies.txt'):
        st.success("✅ Cookies cargadas")
    else:
        st.error("❌ No hay 'cookies.txt'. Las fotos saldrán en 0.")

urls_raw = st.text_area(f"Pega tus enlaces de {plataforma} aquí:", height=200)

if st.button("🚀 Iniciar Extracción Masiva"):
    urls = [u.strip() for u in urls_raw.split('\n') if u.strip()]
    
    if urls:
        resultados = []
        fallidos = []
        barra = st.progress(0)
        
        for i, url in enumerate(urls):
            data = get_yt_data(url, api_key) if plataforma == "YouTube" else get_tt_data(url)
            if data and data.get("Vistas", 0) > 0:
                resultados.append(data)
            else:
                fallidos.append(url)
            barra.progress((i + 1) / len(urls))
        
        if resultados:
            df = pd.DataFrame(resultados)
            st.subheader("📊 Tabla de Resultados")
            st.dataframe(df, use_container_width=True)
            
            st.divider()
            c1, c2 = st.columns(2)
            c1.metric("🔥 SUMA TOTAL VISTAS", f"{df['Vistas'].sum():,}")
            c2.metric("👍 SUMA TOTAL LIKES", f"{df['Likes'].sum():,}")
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar CSV", csv, "reporte.csv", "text/csv")

        if fallidos:
            st.divider()
            with st.expander("❌ Enlaces con error o bloqueados (Vistas en 0)"):
                st.warning("TikTok bloqueó estos enlaces. Intenta renovar el archivo cookies.txt.")
                for f in fallidos: st.write(f"- {f}")
