import streamlit as st
from googleapiclient.discovery import build
import yt_dlp
import re

# Configuración estética de la página
st.set_page_config(
    page_title="Extractor Pro RRSS", 
    page_icon="📊", 
    layout="centered"
)

st.title("📊 Extractor de Datos: YouTube & TikTok")
st.markdown("Introduce un enlace para obtener estadísticas en tiempo real.")

# --- FUNCIÓN PARA YOUTUBE ---
def get_yt_data(url, api_key):
    try:
        # Extraer el ID del video usando expresiones regulares
        video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if not video_id_match:
            return "Error: URL de YouTube no válida."
        
        video_id = video_id_match.group(1)
        youtube = build("youtube", "v3", developerKey=api_key)
        
        # Pedir datos a la API
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()
        
        if not response['items']:
            return "Error: No se encontró el video."
            
        item = response['items'][0]
        return {
            "Plataforma": "YouTube",
            "Título": item['snippet']['title'],
            "Canal": item['snippet']['channelTitle'],
            "Vistas": f"{int(item['statistics']['viewCount']):,}",
            "Likes": f"{int(item['statistics'].get('like_count', 0)):,}" if 'likeCount' in item['statistics'] else "Ocultos",
            "Comentarios": item['statistics'].get('commentCount', 'N/A')
        }
    except Exception as e:
        return f"Error técnico en YouTube: {str(e)}"

# --- FUNCIÓN PARA TIKTOK ---
def get_tt_data(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                "Plataforma": "TikTok",
                "Usuario": info.get('uploader', 'Desconocido'),
                "Descripción": (info.get('title')[:60] + '...') if info.get('title') else "Sin descripción",
                "Vistas": f"{info.get('view_count', 0):,}",
                "Likes": f"{info.get('like_count', 0):,}",
                "Comentarios": info.get('comment_count', 'N/A')
            }
        except Exception as e:
            return f"Error técnico en TikTok: {str(e)}"

# --- INTERFAZ DE USUARIO (SIDEBAR Y CUERPO) ---
with st.sidebar:
    st.header("Configuración")
    option = st.radio("Selecciona Red Social:", ["YouTube", "TikTok"])
    
    if option == "YouTube":
        api_key = st.text_input("YouTube API Key:", type="password", help="Pega aquí la clave que generaste en Google Cloud Console")

# Entrada de URL
url_input = st.text_input(f"Pega el link de {option} aquí:", placeholder="https://...")

if st.button(f"🔍 Extraer datos de {option}"):
    if not url_input:
        st.warning("Por favor, introduce un enlace.")
    else:
        with st.spinner('Buscando datos...'):
            if option == "YouTube":
                if not api_key:
                    st.error("Necesitas una API Key para YouTube.")
                else:
                    res = get_yt_data(url_input, api_key)
                    if isinstance(res, dict):
                        st.success("¡Datos extraídos!")
                        st.table(res.items())
                    else:
                        st.error(res)
            
            elif option == "TikTok":
                res = get_tt_data(url_input)
                if isinstance(res, dict):
                    st.success("¡Datos extraídos!")
                    st.table(res.items())
                else:
                    st.error(res)

st.info("Nota: Para YouTube necesitas tu propia API Key. Para TikTok no es necesaria.")
