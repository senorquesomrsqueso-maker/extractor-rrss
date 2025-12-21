import streamlit as st
import yt_dlp
import pandas as pd
import time
import random

st.set_page_config(page_title="Extractor Express", page_icon="🚀")

def get_tt_no_cookies(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        # Simulamos un iPhone para que TikTok sea menos estricto
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
        'extract_flat': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Espera aleatoria para evitar el bloqueo por IP
            time.sleep(random.uniform(4, 7)) 
            info = ydl.extract_info(url, download=False)
            if not info: return None
            
            return {
                "Plataforma": "TikTok",
                "Título/Autor": info.get('uploader') or "Video Encontrado",
                "Vistas": int(info.get('view_count', 0)),
                "Likes": int(info.get('like_count', 0)),
                "Link": url
            }
        except Exception:
            return None

st.title("🚀 Extractor de TikTok (Sin Cookies)")
urls_raw = st.text_area("Pega tus links (uno por línea):", height=200)

if st.button("Extraer Datos"):
    urls = [u.strip() for u in urls_raw.split('\n') if u.strip()]
    if urls:
        resultados = []
        barra = st.progress(0)
        for i, url in enumerate(urls):
            data = get_tt_no_cookies(url)
            if data: resultados.append(data)
            barra.progress((i + 1) / len(urls))
        
        if resultados:
            st.table(resultados)
        else:
            st.error("TikTok sigue bloqueando la conexión. Por favor, intenta el método de las cookies.")
