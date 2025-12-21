import streamlit as st
from googleapiclient.discovery import build
import yt_dlp
import re
import pandas as pd
import isodate

# Configuración de página
st.set_page_config(page_title="Data Master RRSS", page_icon="🚀", layout="wide")

st.title("🚀 Extractor Inteligente de RRSS")
st.markdown("Analiza múltiples enlaces, separa Shorts de Videos Largos y obtén totales.")

# --- LÓGICA DE EXTRACCIÓN YOUTUBE ---
def get_yt_data(url, api_key):
    try:
        video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if not video_id_match: return None
        video_id = video_id_match.group(1)
        
        # Detección por URL
        es_short_url = "/shorts/" in url.lower()
        
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.videos().list(part="snippet,statistics,contentDetails", id=video_id)
        response = request.execute()
        item = response['items'][0]
        
        # Detección por Duración
        duracion_iso = item['contentDetails']['duration']
        segundos = isodate.parse_duration(duracion_iso).total_seconds()
        
        # Clasificación
        tipo = "Short" if (es_short_url or segundos <= 60) else "Video Largo"
        
        return {
            "Plataforma": "YouTube",
            "Tipo": tipo,
            "Título": item['snippet']['title'],
            "Vistas": int(item['statistics']['viewCount']),
            "Likes": int(item['statistics'].get('likeCount', 0)),
            "Segundos": int(segundos),
            "Link": url
        }
    except: return None

# --- LÓGICA DE EXTRACCIÓN TIKTOK ---
def get_tt_data(url):
    ydl_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                "Plataforma": "TikTok",
                "Tipo": "TikTok",
                "Título": info.get('uploader', 'TikTok Video'),
                "Vistas": int(info.get('view_count', 0)),
                "Likes": int(info.get('like_count', 0)),
                "Segundos": int(info.get('duration', 0)),
                "Link": url
            }
        except: return None

# --- INTERFAZ DE USUARIO ---
with st.sidebar:
    st.header("⚙️ Configuración")
    plataforma = st.selectbox("Elegir plataforma:", ["YouTube", "TikTok"])
    api_key = ""
    if plataforma == "YouTube":
        api_key = st.text_input("YouTube API Key:", type="password")
        st.info("Obtén tu clave en Google Cloud Console.")

# Entrada masiva
st.subheader(f"1. Pega tus links de {plataforma}")
urls_raw = st.text_area("Un enlace por línea:", height=150, placeholder="https://www.youtube.com/watch?v=...\nhttps://www.youtube.com/shorts/...")

if st.button("📊 Procesar y Calcular Totales"):
    lista_urls = [line.strip() for line in urls_raw.split('\n') if line.strip()]
    
    if not lista_urls:
        st.warning("Escribe al menos un enlace.")
    elif plataforma == "YouTube" and not api_key:
        st.error("Debes poner tu API Key de YouTube en la izquierda.")
    else:
        resultados = []
        barra = st.progress(0)
        
        for i, url in enumerate(lista_urls):
            if plataforma == "YouTube":
                data = get_yt_data(url, api_key)
            else:
                data = get_tt_data(url)
            
            if data: resultados.append(data)
            barra.progress((i + 1) / len(lista_urls))

        if resultados:
            df = pd.DataFrame(resultados)
            
            # Mostrar Tabla
            st.subheader("2. Detalle de Videos")
            st.dataframe(df, use_container_width=True)
            
            # Cálculos de Totales
            st.divider()
            st.subheader("3. Resumen y Totales")
            
            # Agrupar por tipo (Short vs Largo)
            resumen = df.groupby("Tipo").agg({
                "Vistas": "sum",
                "Likes": "sum",
                "Link": "count"
            }).rename(columns={"Link": "Cantidad"})

            # Mostrar Métricas en columnas
            filas_resumen = resumen.index.tolist()
            cols = st.columns(len(filas_resumen))

            for idx, tipo in enumerate(filas_resumen):
                vistas = resumen.loc[tipo, 'Vistas']
                cantidad = resumen.loc[tipo, 'Cantidad']
                with cols[idx]:
                    st.metric(label=f"Total Vistas {tipo}", value=f"{vistas:,}")
                    st.write(f"📁 Basado en **{cantidad}** contenidos")

            # Botón de Descarga
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar Tabla en CSV (Excel)", csv, "reporte_datos.csv", "text/csv")
        else:
            st.error("No se pudieron extraer datos. Revisa los enlaces.")
