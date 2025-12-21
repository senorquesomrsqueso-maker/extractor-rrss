import streamlit as st
import yt_dlp
import pandas as pd
import time
import os
import re
import random
from googleapiclient.discovery import build
import isodate

# Configuración visual de la página
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
        
        # Calcular duración para separar Shorts
        duracion_iso = item['contentDetails']['duration']
        segundos = isodate.parse_duration(duracion_iso).total_seconds()
        
        # Clasificación: Short si tiene /shorts/ en el link o dura menos de 61 seg
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
        'extract_flat': False, 
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    # Verificación automática de cookies
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            time.sleep(random.uniform(2, 4)) # Pausa para evitar bloqueos
            info = ydl.extract_info(url, download=False)
            if not info: return None
            
            return {
                "Plataforma": "TikTok",
                "Tipo": "TikTok (Vertical)",
                "Título/Autor": info.get('uploader') or info.get('title', 'Video TikTok'),
                "Vistas": int(info.get('view_count', 0)),
                "Likes": int(info.get('like_count', 0)),
                "Link": url
            }
        except: return None

# --- INTERFAZ DE USUARIO ---
st.title("📈 Extractor Masivo: YouTube & TikTok")
st.markdown("Analiza tus enlaces, separa categorías y obtén la suma total de métricas.")

with st.sidebar:
    st.header("⚙️ Configuración")
    plataforma = st.selectbox("Elige la plataforma:", ["YouTube", "TikTok"])
    
    api_key = ""
    if plataforma == "YouTube":
        api_key = st.text_input("YouTube API Key:", type="password")
    
    st.divider()
    # Indicador de estado de cookies
    if os.path.exists('cookies.txt'):
        st.success("✅ Archivo 'cookies.txt' detectado.")
    else:
        st.warning("⚠️ Sin 'cookies.txt'. TikTok podría dar 0 vistas.")

# Entrada de enlaces
urls_input = st.text_area(f"Pega tus enlaces de {plataforma} aquí (uno por línea):", height=200)

if st.button("🚀 Procesar y Calcular Totales"):
    lista_urls = [line.strip() for line in urls_input.split('\n') if line.strip()]
    
    if not lista_urls:
        st.warning("Por favor, introduce al menos un enlace.")
    else:
        resultados = []
        barra = st.progress(0)
        status = st.empty()
        
        for i, url in enumerate(lista_urls):
            status.text(f"⏳ Procesando {i+1} de {len(lista_urls)}...")
            
            if plataforma == "YouTube":
                data = get_yt_data(url, api_key)
            else:
                data = get_tt_data(url)
            
            if data:
                resultados.append(data)
            
            barra.progress((i + 1) / len(lista_urls))
        
        status.empty()

        if resultados:
            df = pd.DataFrame(resultados)
            
            # 1. Tabla de resultados
            st.subheader("📊 Resultados Detallados")
            st.dataframe(df, use_container_width=True)
            
            # 2. Sección de Totales (Como estaba antes)
            st.divider()
            st.subheader("🎯 Resumen General")
            
            # Agrupar por tipo para mostrar totales específicos
            resumen_vistas = df.groupby("Tipo")["Vistas"].sum()
            resumen_cantidad = df.groupby("Tipo")["Link"].count()
            
            columnas = st.columns(len(resumen_vistas))
            
            for idx, (tipo, total_vistas) in enumerate(resumen_vistas.items()):
                with columnas[idx]:
                    st.metric(label=f"Vistas Totales {tipo}", value=f"{total_vistas:,}")
                    st.caption(f"Basado en {resumen_cantidad[tipo]} videos")
            
            # Gran total acumulado de toda la tabla
            st.divider()
            gran_total = df["Vistas"].sum()
            st.metric(label="🔥 TOTAL ACUMULADO (TODOS)", value=f"{gran_total:,}")
            
            # Botón de descarga
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar reporte CSV", csv, "reporte_rrss.csv", "text/csv")
        else:
            st.error("No se pudo obtener información. Revisa tus enlaces o el estado de las cookies.")
