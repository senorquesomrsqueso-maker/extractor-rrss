import streamlit as st
import yt_dlp
import pandas as pd
import time
import os
import re
import random
from googleapiclient.discovery import build
import isodate

st.set_page_config(page_title="Extractor RRSS Pro", page_icon="📈", layout="wide")

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
            "Plataforma": "YouTube", "Tipo": tipo, "Título/Autor": item['snippet']['title'],
            "Vistas": int(item['statistics']['viewCount']), "Likes": int(item['statistics'].get('likeCount', 0)), "Link": url
        }
    except: return None

# --- FUNCIONES DE TIKTOK Y FACEBOOK (REFORZADA) ---
def get_social_data(url, plataforma):
    # Limpieza de URL para Facebook Reels
    if "facebook.com/reel/" in url:
        url = url.split('?')[0] # Elimina parámetros de rastreo que a veces bloquean la lectura

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False, # Cambiado a False para que intente profundizar en los datos de FB
        'force_generic_extractor': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Espera aleatoria más larga para Facebook
            time.sleep(random.uniform(6, 10)) 
            info = ydl.extract_info(url, download=False)
            if not info: return None
            
            # Facebook suele guardar las vistas en 'view_count' o 'play_count'
            vistas = info.get('view_count') or info.get('play_count') or 0
            likes = info.get('like_count') or 0

            return {
                "Plataforma": plataforma,
                "Tipo": "Video/Reel",
                "Título/Autor": info.get('uploader') or info.get('title', f'Contenido {plataforma}'),
                "Vistas": int(vistas),
                "Likes": int(likes),
                "Link": url
            }
        except Exception as e:
            return None

# --- INTERFAZ ---
st.title("📈 Extractor Multi-Plataforma")

with st.sidebar:
    st.header("⚙️ Configuración")
    plataforma = st.selectbox("Plataforma:", ["YouTube", "TikTok", "Facebook"])
    api_key = st.text_input("YouTube API Key:", type="password") if plataforma == "YouTube" else ""
    st.divider()
    if os.path.exists('cookies.txt'):
        st.success("✅ 'cookies.txt' detectado.")
    else:
        st.error("❌ Facebook REQUIERE cookies.txt para dar datos.")

urls_input = st.text_area(f"Pega tus enlaces de {plataforma} aquí:", height=200)

if st.button("🚀 Procesar Todo"):
    lista_urls = [line.strip() for line in urls_input.split('\n') if line.strip()]
    
    if lista_urls:
        resultados, fallidos = [], []
        barra = st.progress(0)
        status = st.empty()
        
        for i, url in enumerate(lista_urls):
            status.text(f"⏳ Procesando {i+1} de {len(lista_urls)}...")
            if plataforma == "YouTube":
                data = get_yt_data(url, api_key)
            else:
                data = get_social_data(url, plataforma)
            
            # Solo agregamos si las vistas son mayores a 0 para evitar falsos positivos
            if data and data["Vistas"] > 0:
                resultados.append(data)
            else:
                fallidos.append(url)
            barra.progress((i + 1) / len(lista_urls))
        
        status.empty()

        if resultados:
            df = pd.DataFrame(resultados)
            st.subheader("📊 Tabla de Resultados")
            st.dataframe(df, use_container_width=True)
            
            # COPIADO RÁPIDO
            st.write("📋 **Cadenas de vistas para sumar:**")
            vistas_lista = [str(v) for v in df['Vistas'].tolist()]
            st.code("+".join(vistas_lista), language="text")
            
            st.divider()
            c1, c2 = st.columns(2)
            c1.metric("🔥 SUMA TOTAL VISTAS", f"{df['Vistas'].sum():,}")
            c2.metric("👍 SUMA TOTAL LIKES", f"{df['Likes'].sum():,}")
        
        if fallidos:
            st.divider()
            st.subheader("❌ Enlaces con Datos Protegidos (0 vistas)")
            with st.expander("Ver enlaces que Facebook bloqueó"):
                for f in fallidos: st.write(f"- {f}")
                st.info("💡 Consejo: Facebook bloquea las métricas si detecta muchas peticiones. Prueba procesar de 3 en 3.")
