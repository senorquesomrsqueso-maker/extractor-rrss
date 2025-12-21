import streamlit as st
from googleapiclient.discovery import build
import yt_dlp
import re
import pandas as pd

st.set_page_config(page_title="Extractor Masivo RRSS", page_icon="📈", layout="wide")

st.title("📈 Extractor Masivo de Datos")
st.markdown("Pega varios enlaces (uno por línea) para obtener una tabla comparativa.")

# --- FUNCIONES DE EXTRACCIÓN ---
def get_yt_data(url, api_key):
    try:
        video_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url).group(1)
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.videos().list(part="snippet,statistics", id=video_id)
        response = request.execute()
        item = response['items'][0]
        return {
            "Plataforma": "YouTube",
            "Título/User": item['snippet']['title'],
            "Vistas": int(item['statistics']['viewCount']),
            "Likes": int(item['statistics'].get('likeCount', 0)),
            "Link": url
        }
    except: return None

def get_tt_data(url):
    ydl_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                "Plataforma": "TikTok",
                "Título/User": info.get('uploader'),
                "Vistas": info.get('view_count', 0),
                "Likes": info.get('like_count', 0),
                "Link": url
            }
        except: return None

# --- INTERFAZ ---
with st.sidebar:
    opcion = st.radio("Plataforma:", ["YouTube", "TikTok"])
    api_key = ""
    if opcion == "YouTube":
        api_key = st.text_input("API Key de YouTube:", type="password")

# Área de texto para múltiples links
urls_input = st.text_area(f"Pega tus enlaces de {opcion} aquí (uno por línea):", height=200)

if st.button("🚀 Procesar todos los enlaces"):
    lista_urls = [line.strip() for line in urls_input.split('\n') if line.strip()]
    
    if not lista_urls:
        st.warning("Escribe al menos un enlace.")
    else:
        resultados = []
        progreso = st.progress(0)
        
        for i, url in enumerate(lista_urls):
            if opcion == "YouTube":
                if api_key:
                    dato = get_yt_data(url, api_key)
                else:
                    st.error("Falta la API Key")
                    break
            else:
                dato = get_tt_data(url)
            
            if dato:
                resultados.append(dato)
            
            # Actualizar barra de progreso
            progreso.progress((i + 1) / len(lista_urls))

        if resultados:
            df = pd.DataFrame(resultados)
            st.success(f"Se procesaron {len(resultados)} enlaces con éxito.")
            
            # Mostrar tabla interactiva
            st.dataframe(df, use_container_width=True)
            
            # Opción para descargar en Excel/CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar datos (CSV)", csv, "datos_redes.csv", "text/csv")
