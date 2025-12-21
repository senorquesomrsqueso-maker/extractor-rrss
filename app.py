import streamlit as st
from googleapiclient.discovery import build
import yt_dlp
import re
import pandas as pd
import isodate
import time

# Configuración de página
st.set_page_config(page_title="Data Master RRSS", page_icon="🚀", layout="wide")

st.title("🚀 Extractor de enlaces (Programa de Embajadores BS LATAM)")
st.markdown("Si un enlace falla, el programa continuará con el siguiente automáticamente.")

# --- LÓGICA DE YOUTUBE ---
def get_yt_data(url, api_key):
    try:
        video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if not video_id_match: return None
        video_id = video_id_match.group(1)
        
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.videos().list(part="snippet,statistics,contentDetails", id=video_id)
        response = request.execute()
        
        if not response['items']: return None
        item = response['items'][0]
        
        duracion_iso = item['contentDetails']['duration']
        segundos = isodate.parse_duration(duracion_iso).total_seconds()
        
        tipo = "Short" if ("/shorts/" in url.lower() or segundos <= 61) else "Video Largo"
        
        return {
            "Plataforma": "YouTube",
            "Tipo": tipo,
            "Título": item['snippet']['title'],
            "Vistas": int(item['statistics']['viewCount']),
            "Likes": int(item['statistics'].get('likeCount', 0)),
            "Link": url
        }
    except Exception:
        return None

# --- LÓGICA DE TIKTOK ---
def get_tt_data(url):
    ydl_opts = {
        'quiet': True, 
        'no_warnings': True,
        'extract_flat': True,
        'break_on_reject': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Añadimos un pequeño retraso para no saturar a TikTok
            time.sleep(1) 
            info = ydl.extract_info(url, download=False)
            if not info: return None
            return {
                "Plataforma": "TikTok",
                "Tipo": "TikTok",
                "Título": info.get('uploader', 'Video'),
                "Vistas": int(info.get('view_count', 0)),
                "Likes": int(info.get('like_count', 0)),
                "Link": url
            }
        except Exception:
            return None

# --- INTERFAZ ---
with st.sidebar:
    plataforma = st.selectbox("Elegir plataforma:", ["YouTube", "TikTok"])
    api_key = ""
    if plataforma == "YouTube":
        api_key = st.text_input("YouTube API Key:", type="password")

urls_raw = st.text_area("Pega tus links (uno por línea):", height=200)

if st.button("📊 Procesar Lista Completa"):
    lista_urls = [line.strip() for line in urls_raw.split('\n') if line.strip()]
    
    if not lista_urls:
        st.warning("Pega los enlaces primero.")
    elif plataforma == "YouTube" and not api_key:
        st.error("Pon tu API Key en la izquierda.")
    else:
        resultados = []
        errores = 0
        progreso = st.progress(0)
        status_text = st.empty()
        
        for i, url in enumerate(lista_urls):
            status_text.text(f"Procesando {i+1} de {len(lista_urls)}...")
            
            # Intentar extraer
            data = get_yt_data(url, api_key) if plataforma == "YouTube" else get_tt_data(url)
            
            if data:
                resultados.append(data)
            else:
                errores += 1
            
            progreso.progress((i + 1) / len(lista_urls))

        status_text.empty()

        if resultados:
            df = pd.DataFrame(resultados)
            st.success(f"✅ Éxito: {len(resultados)} | ❌ Fallidos: {errores}")
            st.dataframe(df, use_container_width=True)
            
            # Resumen Total
            st.divider()
            resumen = df.groupby("Tipo")["Vistas"].sum()
            cols = st.columns(len(resumen))
            for idx, (tipo, total) in enumerate(resumen.items()):
                cols[idx].metric(f"Total Vistas {tipo}", f"{total:,}")
        else:
            st.error("No se pudo extraer información de ningún enlace. Revisa que los links sean correctos.")
