import streamlit as st
import yt_dlp
import pandas as pd
import time
import os

st.set_page_config(page_title="Extractor De Enlaces", page_icon="🛡️", layout="wide")

st.title("🛡️ Extractor de Datos (Modo Local Seguro)")

# --- CONFIGURACIÓN DE SEGURIDAD ---
def get_data_ultra_safe(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        # Simulamos un navegador real
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'extract_flat': True,
        'ignoreerrors': True, # Si uno falla, no mata el programa
    }

    # Intentar usar cookies si el archivo existe
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Reintento pequeño si falla
            info = ydl.extract_info(url, download=False)
            if not info:
                return None
            
            # Clasificación inteligente
            vistas = info.get('view_count', 0)
            likes = info.get('like_count', 0)
            
            return {
                "Plataforma": "TikTok" if "tiktok.com" in url else "YouTube",
                "Título/Autor": info.get('uploader') or info.get('title', 'Sin nombre'),
                "Vistas": int(vistas) if vistas else 0,
                "Likes": int(likes) if likes else 0,
                "Link": url
            }
        except Exception:
            return None

# --- INTERFAZ ---
urls_raw = st.text_area("Pega tus links aquí (uno por línea):", height=200)

if st.button("🚀 Iniciar Extracción Segura"):
    urls = [u.strip() for u in urls_raw.split('\n') if u.strip()]
    
    if urls:
        resultados = []
        barra = st.progress(0)
        status = st.empty()
        
        for i, url in enumerate(urls):
            status.text(f"Analizando: {url}...")
            # Pausa aleatoria para engañar al sistema (entre 2 y 4 segundos)
            time.sleep(2.5) 
            
            data = get_data_ultra_safe(url)
            if data:
                resultados.append(data)
            
            barra.progress((i + 1) / len(urls))
        
        status.empty()

        if resultados:
            df = pd.DataFrame(resultados)
            st.success(f"✅ Se obtuvieron {len(resultados)} resultados de {len(urls)} links.")
            st.dataframe(df, use_container_width=True)
            
            # Suma Total
            st.metric("Suma Total de Vistas", f"{df['Vistas'].sum():,}")
            
            # Exportar a Excel (Requiere: pip install openpyxl)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar reporte CSV", csv, "datos.csv", "text/csv")
        else:
            st.error("❌ No se pudo extraer nada. Prueba renovando el archivo 'cookies.txt'.")
