import streamlit as st
import yt_dlp
import pandas as pd
import re
import time
import requests
import json
import datetime
import math
import os
import traceback
import urllib.parse
import random
import google.generativeai as genai
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL Y NÚCLEO IA DE ALTO RENDIMIENTO
# ==============================================================================

# Credenciales de Acceso - Protocolo BS LATAM
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk" 
GEMINI_API_KEY = "AIzaSyA8HsM0vSCopd1s05nOryhbNIGU26dvxG4"

# Configuración Inicial del Dashboard
st.set_page_config(
    page_title="BS LATAM - AUDIT ELITE SUPREMACÍA V32.9",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialización de Inteligencia Artificial Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Marcador de tiempo para el registro de auditoría
    fecha_actual_global = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    generation_config = {
        "temperature": 0.85,
        "top_p": 0.95,
        "top_k": 45,
        "max_output_tokens": 4096,
    }
    
    # Instrucción Maestra del Sistema - Identidad Corporativa
    system_instruction_core = (
        f"Eres el Consultor Senior y Partner Estratégico de BS LATAM. "
        f"HOY ES: {fecha_actual_global}. "
        "Tu misión es asistir al usuario en TODO: auditoría de métricas, programación, "
        "redacción de reportes, matemáticas complejas y análisis de mercado. "
        "Eres una IA de PROPÓSITO GENERAL. "
        "Mantén siempre un tono profesional, con autoridad técnica. "
        "Estilo visual: Cyberpunk Industrial / Corporativo de Élite. "
        "NUNCA uses frases robóticas ni disculpas innecesarias."
    )

    # SE CORRIGE A 'gemini-1.5-flash' PARA ESTABILIDAD Y EVITAR ERROR 404
    model_ia = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        generation_config=generation_config,
        system_instruction=system_instruction_core
    )

except Exception as e_ia_init:
    st.error(f"FALLA CRÍTICA EN NÚCLEO NEURAL: {e_ia_init}")

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "ELITE SUPREMACÍA" (CSS EXTENDIDO)
# ==============================================================================

st.markdown("""
    <style>
    /* Estética General Dark Industrial */
    .main { 
        background-color: #0b0d11; 
        color: #e6edf3; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    }

    .stApp { 
        background-color: #0b0d11; 
    }
    
    /* BLOQUE DE TÍTULO PRINCIPAL EXTENDIDO */
    .title-box { 
        border-left: 20px solid #E30613; 
        padding: 50px 70px; 
        margin: 40px 0 70px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,13,17,0) 100%);
        border-radius: 0 40px 40px 0;
        box-shadow: 20px 0 50px rgba(0,0,0,0.7);
    }

    .m-title { 
        font-size: 60px; 
        font-weight: 900; 
        color: #ffffff; 
        text-transform: uppercase; 
        letter-spacing: 12px; 
        margin: 0; 
        line-height: 1.1; 
        text-shadow: 5px 5px 10px rgba(0,0,0,1);
    }

    .s-title { 
        font-size: 26px; 
        color: #8b949e; 
        font-family: 'Courier New', monospace; 
        margin-top: 25px; 
        letter-spacing: 5px; 
        font-weight: bold;
    }

    /* ESTILO DE LOS ENCABEZADOS DE MÓDULO */
    .module-header {
        font-size: 32px; 
        font-weight: 700; 
        color: #ffffff;
        margin-top: 40px; 
        margin-bottom: 25px;
        display: flex; 
        align-items: center; 
        gap: 15px;
        border-bottom: 1px solid #30363d; 
        padding-bottom: 15px;
    }

    .sub-header {
        font-size: 20px; 
        font-weight: 600; 
        color: #E30613;
        margin-top: 20px; 
        text-transform: uppercase; 
        letter-spacing: 2px;
    }

    /* ESTILO BS LATAM SIDEBAR */
    .bs-latam-sidebar {
        color: #ffffff; 
        font-weight: 950; 
        font-size: 45px; 
        text-align: center;
        text-transform: uppercase; 
        letter-spacing: 7px;
        text-shadow: 0px 0px 30px #0055ff, 4px 4px 0px #000000;
        margin-bottom: 45px; 
        padding: 25px; 
        border-bottom: 4px solid #E30613;
    }

    /* BOTONERÍA ÉLITE */
    .stButton>button { 
        background: linear-gradient(135deg, #E30613 0%, #9e040d 100%) !important;
        color: #ffffff !important; 
        font-weight: 900 !important; 
        text-transform: uppercase; 
        border-radius: 30px; 
        height: 70px; 
        width: 100%; 
        font-size: 22px !important;
        border: none; 
        box-shadow: 0 10px 20px rgba(227,6,19,0.35);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .stButton>button:hover {
        transform: scale(1.02) translateY(-4px);
        box-shadow: 0 15px 35px rgba(227,6,19,0.55);
        border: 2px solid #ffffff;
    }
    
    /* INPUTS Y TEXT AREAS MASIVAS */
    .stTextArea textarea, .stTextInput input, .stNumberInput input { 
        background-color: #161b22 !important; 
        color: #e6edf3 !important; 
        border: 2px solid #30363d !important; 
        border-radius: 15px;
        font-size: 16px; 
        padding: 15px;
    }

    .stTextArea textarea:focus, .stTextInput input:focus { 
        border-color: #E30613 !important; 
    }

    /* TABLAS Y DATAFRAMES */
    [data-testid="stDataFrame"] {
        border: 2px solid #30363d; 
        border-radius: 20px; 
        overflow: hidden;
        background-color: #161b22;
    }
    
    /* BLOQUES DE CÓDIGO (Optimización para copiado) */
    .stCodeBlock {
        border: 1px solid #E30613;
        border-radius: 10px;
    }

    /* CONTENEDORES DE ERROR PERSONALIZADOS */
    .error-card {
        background-color: #2d0000;
        border: 1px solid #ff4b4b;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }

    /* MÉTRICAS FLOTANTES */
    .metric-value {
        color: #E30613; 
        font-size: 38px; 
        font-weight: 900;
    }

    /* ESTILO RESUMEN TÁCTICO V32.9 */
    .tactical-summary {
        background: linear-gradient(135deg, #161b22 0%, #0b0d11 100%);
        border: 1px solid #30363d;
        border-left: 5px solid #E30613;
        padding: 20px;
        border-radius: 10px;
        color: #e6edf3;
        font-family: 'Courier New', monospace;
    }

    .tactical-item { 
        margin-bottom: 8px; 
        display: flex; 
        justify-content: space-between; 
    }

    .tactical-label { 
        color: #8b949e; 
        text-transform: uppercase; 
        font-size: 14px; 
    }

    .tactical-value { 
        color: #ffffff; 
        font-weight: bold; 
        border-bottom: 1px solid #E30613; 
    }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V32.9</p>
        <p class="s-title">SISTEMA INTEGRAL BS LATAM • FB / YT / TK / VISION-IA</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA, VARIABLES DE ESTADO Y LOGS
# ==============================================================================

if 'db_final' not in st.session_state: 
    st.session_state.db_final = pd.DataFrame()

if 'db_fallidos' not in st.session_state: 
    st.session_state.db_fallidos = pd.DataFrame()

if 'db_drive_vision' not in st.session_state: 
    st.session_state.db_drive_vision = pd.DataFrame()

if 'chat_log' not in st.session_state:
    st.session_state.chat_log = [
        {"role": "assistant", "content": f"SISTEMA OPERATIVO V32.9 LISTO. Resumen Táctico optimizado."}
    ]

# ==============================================================================
# 4. FUNCIONES CORE - LÓGICA DE PROCESAMIENTO MULTI-PLATAFORMA
# ==============================================================================

def limpiar_url_táctica(url):
    """Limpia parámetros de rastreo para evitar errores de scraping."""
    url = url.strip().replace('"', '').replace("'", "")
    if '?si=' in url: 
        url = url.split('?si=')[0]
    if '&pp=' in url: 
        url = url.split('&pp=')[0]
    if 'fb.watch' in url: 
        return url 
    return url

def obtener_tipo_video(url, info_dict):
    """Determina la categoría exacta del contenido."""
    if "facebook.com" in url or "fb.watch" in url:
        return "Facebook Video"
    
    if "tiktok.com" in url:
        return "TikTok"
    
    if "youtube.com" in url or "youtu.be" in url:
        duration = info_dict.get('duration', 0)
        if "/shorts/" in url or (duration and duration <= 65):
            return "YouTube Shorts"
        return "YouTube Video"
    
    return "Contenido Externo"

def navegar_ia_en_enlace(url):
    """Permite que el sistema 'entre' en un enlace y extraiga texto para la IA."""
    try:
        header_request = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        r = requests.get(url, headers=header_request, timeout=12)
        if r.status_code == 200:
            s = BeautifulSoup(r.text, 'html.parser')
            for tag in s(["script", "style", "header", "footer", "nav"]):
                tag.decompose()
            return s.get_text(separator=' ')[:5000]
        return "Error: No se pudo acceder al sitio."
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def analizar_imagen_con_ia(image_file):
    """Usa Gemini Vision para leer métricas de imágenes."""
    try:
        img = Image.open(image_file)
        prompt_vision = (
            "Actúa como un extractor de datos OCR de alta precisión para BS LATAM. "
            "Analiza esta imagen de métricas de redes sociales. "
            "Identifica el número TOTAL de VISTAS (Views). "
            "Devuelve SOLO EL NÚMERO entero crudo sin puntos ni letras."
        )
        response = model_ia.generate_content([prompt_vision, img])
        texto_limpio = re.sub(r'[^0-9]', '', response.text)
        return int(texto_limpio) if texto_limpio else 0
    except Exception as e_vision:
        return 0

def motor_auditor_universal_v32(urls):
    """Core de scraping masivo con soporte para FACEBOOK, YT y TIKTOK."""
    resultados = []
    fallidos = []
    
    p_bar = st.progress(0)
    status_text = st.empty()
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
    ]

    for i, raw_url in enumerate(urls):
        url = limpiar_url_táctica(raw_url)
        status_text.markdown(f"🔍 **AUDITANDO:** `{url[:50]}...`")
        
        ydl_opts = {
            'quiet': True,
            'ignoreerrors': True,
            'skip_download': True,
            'no_warnings': True,
            'http_headers': {'User-Agent': random.choice(user_agents)},
            'extract_flat': False
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if info:
                    vistas = int(info.get('view_count') or 0)
                    tipo = obtener_tipo_video(url, info)
                    plataforma = tipo.split(' ')[0].upper()

                    resultados.append({
                        "Fecha": info.get('upload_date', 'N/A'),
                        "Plataforma": plataforma,
                        "Tipo": tipo,
                        "Creador": info.get('uploader', 'N/A'),
                        "Título": info.get('title', 'N/A')[:65],
                        "Vistas": vistas,
                        "Likes": int(info.get('like_count') or 0),
                        "Comments": int(info.get('comment_count') or 0),
                        "Link": url
                    })
                else:
                    fallidos.append({"Link": url, "Error": "Sin respuesta / Privado"})
        
        except Exception as e_scrap:
            fallidos.append({"Link": url, "Error": str(e_scrap)[:50]})
        
        p_bar.progress((i + 1) / len(urls))
    
    p_bar.empty()
    status_text.empty()
    return pd.DataFrame(resultados), pd.DataFrame(fallidos)

# ==============================================================================
# 5. SIDEBAR - CONTROL DE MISIONES
# ==============================================================================

with st.sidebar:
    st.markdown('<p class="bs-latam-sidebar">BS LATAM</p>', unsafe_allow_html=True)
    
    modulo = st.radio(
        "MÓDULOS OPERATIVOS", 
        ["🚀 EXTRACTOR ELITE", "📂 DRIVE AUDITOR (VISION)", "🤖 PARTNER IA", "🛰️ SEARCH PRO"],
        index=0
    )
    
    st.divider()
    
    if st.button("🚨 REINICIO DE CACHÉ"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    st.caption(f"VERSIÓN: 32.9.0-ELITE")
    st.caption(f"ÚLTIMO SYNC: {datetime.datetime.now().strftime('%H:%M:%S')}")

# ==============================================================================
# 6. MÓDULO 1: EXTRACTOR ELITE (MODO MULTI-PLATAFORMA)
# ==============================================================================

if modulo == "🚀 EXTRACTOR ELITE":
    st.markdown('<div class="module-header">📥 Extractor de Métricas Masivas</div>', unsafe_allow_html=True)
    
    texto_entrada = st.text_area(
        "Pega los enlaces (uno por línea o separados por comas):", 
        height=250, 
        placeholder="https://..."
    )
    
    c_btn1, c_btn2 = st.columns([1, 4])
    with c_btn1:
        ejecutar = st.button("🔥 EJECUTAR AUDITORÍA")
    
    if ejecutar:
        urls_detectadas = re.findall(r"(https?://[^\s\"\'\)\],]+)", texto_entrada)
        
        if urls_detectadas:
            res, fails = motor_auditor_universal_v32(urls_detectadas)
            st.session_state.db_final = res
            st.session_state.db_fallidos = fails
            
            if not res.empty:
                st.success(f"PROCESO FINALIZADO: {len(res)} registros extraídos con éxito.")
            if not fails.empty:
                st.warning(f"AVISO: {len(fails)} enlaces presentaron anomalías.")
        else:
            st.error("ERROR: No se detectaron URLs válidas en el campo de texto.")

    # --- ZONA DE VISUALIZACIÓN DE RESULTADOS ---
    
    if not st.session_state.db_fallidos.empty:
        with st.expander("⚠️ VER ENLACES NO PROCESADOS / ERRORES"):
            st.markdown('<div class="error-card">', unsafe_allow_html=True)
            st.dataframe(st.session_state.db_fallidos, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if not st.session_state.db_final.empty:
        df = st.session_state.db_final
        st.divider()
        st.markdown('<div class="sub-header">📊 DATOS EXTRAÍDOS (MULTI-PLATAFORMA)</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown('<div class="module-header">📋 CENTRO DE COPIADO Y FÓRMULAS</div>', unsafe_allow_html=True)
        
        # Grid de métricas rápidas
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            total_v = df['Vistas'].sum()
            st.markdown(f"**TOTAL VISTAS**\n## {total_v:,}")
        with m2:
            df_yt_v = df[df['Tipo'] == 'YouTube Video']
            st.markdown(f"**YT LARGOS**\n## {df_yt_v['Vistas'].sum():,}")
        with m3:
            df_fb = df[df['Plataforma'] == 'FACEBOOK']
            st.markdown(f"**FACEBOOK**\n## {df_fb['Vistas'].sum():,}")
        with m4:
            df_tk = df[df['Plataforma'] == 'TIKTOK']
            st.markdown(f"**TIKTOK**\n## {df_tk['Vistas'].sum():,}")

        # BLOQUES DE CÓDIGO PARA COPIADO DIRECTO
        st.divider()
        st.markdown("### 📥 Bloques de Texto para Copiar")
        
        col_copy1, col_copy2 = st.columns(2)
        
        with col_copy1:
            st.markdown("**1. FÓRMULA YT LARGOS (X+Y+Z)**")
            f_yt_largos = "+".join(df_yt_v['Vistas'].astype(str).tolist())
            st.code(f_yt_largos if f_yt_largos else "0", language="text")
            
            st.markdown("**2. FÓRMULA FACEBOOK (X+Y+Z)**")
            f_fb = "+".join(df_fb['Vistas'].astype(str).tolist())
            st.code(f_fb if f_fb else "0", language="text")
            
            st.markdown("**3. FÓRMULA YT SHORTS (X+Y+Z)**")
            df_shorts = df[df['Tipo'] == 'YouTube Shorts']
            f_shorts = "+".join(df_shorts['Vistas'].astype(str).tolist())
            st.code(f_shorts if f_shorts else "0", language="text")

            st.markdown("**4. VISTAS TOTALES DE TODO (SUMA GLOBAL)**")
            st.code(f"{total_v}", language="text")

        with col_copy2:
            st.markdown("**5. FÓRMULA TIKTOK (X+Y+Z)**")
            f_tk = "+".join(df_tk['Vistas'].astype(str).tolist())
            st.code(f_tk if f_tk else "0", language="text")

            st.markdown("**6. FÓRMULA TOTAL GENERAL**")
            st.code(f"{total_v}", language="text")
            
            st.markdown("**7. RESUMEN TÁCTICO DE OPERACIÓN**")
            st.markdown(f"""
                <div class="tactical-summary">
                    <div class="tactical-item"><span class="tactical-label">Protocolo:</span><span class="tactical-value">BS LATAM AUDIT ELITE</span></div>
                    <div class="tactical-item"><span class="tactical-label">Exitosos:</span><span class="tactical-value">{len(df)}</span></div>
                    <div class="tactical-item"><span class="tactical-label">YouTube:</span><span class="tactical-value">{df_yt_v['Vistas'].sum() + df_shorts['Vistas'].sum():,}</span></div>
                    <div class="tactical-item"><span class="tactical-label">Facebook:</span><span class="tactical-value">{df_fb['Vistas'].sum():,}</span></div>
                    <div class="tactical-item"><span class="tactical-label">TikTok:</span><span class="tactical-value">{df_tk['Vistas'].sum():,}</span></div>
                    <div style="border-top: 1px dashed #E30613; margin-top: 10px; padding-top: 10px;" class="tactical-item">
                        <span class="tactical-label" style="color:#E30613;">Acumulado Global:</span>
                        <span class="tactical-value" style="font-size: 18px;">{total_v:,}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# 7. MÓDULO 2: DRIVE AUDITOR (VISION IA + NAVEGACIÓN)
# ==============================================================================

elif modulo == "📂 DRIVE AUDITOR (VISION)":
    st.markdown('<div class="module-header">👁️ Auditor Visual y de Enlaces</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header">🔗 Auditoría por Navegación IA (Lectura de Link)</div>', unsafe_allow_html=True)
    entrada_enlaces_drive = st.text_area(
        "Pega aquí los enlaces (La IA 'entrará' a leer la data):", 
        height=150, 
        placeholder="Pega múltiples enlaces aquí..."
    )
    
    st.divider()
    
    st.markdown('<div class="sub-header">📸 Auditoría por Evidencia Visual (OCR)</div>', unsafe_allow_html=True)
    up_files = st.file_uploader("Arrastra las evidencias aquí:", type=['png', 'jpg', 'jpeg', 'webp'], accept_multiple_files=True)
    
    if st.button("🧠 INICIAR AUDITORÍA PROFUNDA"):
        v_results_final = []
        
        # Procesamiento de Enlaces mediante Navegación Textual IA
        urls_drive = re.findall(r"(https?://[^\s\"\'\)\],]+)", entrada_enlaces_drive)
        if urls_drive:
            for u in urls_drive:
                with st.spinner(f"IA Navegando en {u[:30]}..."):
                    texto_web = navegar_ia_en_enlace(u)
                    prompt_ia_link = f"Analiza este texto extraído de una web y busca el número de VISTAS o REPRODUCCIONES. Solo responde el número: {texto_web}"
                    res_ia_link = model_ia.generate_content(prompt_ia_link)
                    vistas_final = re.sub(r'[^0-9]', '', res_ia_link.text)
                    
                    v_results_final.append({
                        "Fecha": "Enlace IA", "Plataforma": "LINK", "Tipo": "Scraping IA", 
                        "Creador": "N/A", "Título": u[:50], 
                        "Vistas": int(vistas_final) if vistas_final else 0, "Link": u
                    })

        # Procesamiento de Imágenes Vision
        if up_files:
            v_bar = st.progress(0)
            for idx, f in enumerate(up_files):
                v_img = analizar_imagen_con_ia(f)
                v_results_final.append({
                    "Fecha": "OCR IA", "Plataforma": "VISION", "Tipo": "Captura", 
                    "Creador": "N/A", "Título": f.name, "Vistas": v_img, "Link": "Archivo Local"
                })
                v_bar.progress((idx + 1) / len(up_files))
        
        st.session_state.db_drive_vision = pd.DataFrame(v_results_final)
        st.success("Análisis Profundo Completado.")

    if not st.session_state.db_drive_vision.empty:
        st.markdown('<div class="sub-header">📊 DATA CONSOLIDADA DRIVE/VISION</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.db_drive_vision, use_container_width=True, hide_index=True)
        f_ia = "+".join(st.session_state.db_drive_vision['Vistas'].astype(str).tolist())
        st.markdown("**FÓRMULA DE SUMA DRIVE/VISION**")
        st.code(f_ia, language="text")

# ==============================================================================
# 8. MÓDULO 3: PARTNER IA (ARREGLADO)
# ==============================================================================

elif modulo == "🤖 PARTNER IA":
    st.markdown('<div class="module-header">🤖 Partner IA - Consultor Estratégico</div>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if p_user := st.chat_input("Instrucción técnica..."):
        st.session_state.chat_log.append({"role": "user", "content": p_user})
        with st.chat_message("user"): 
            st.markdown(p_user)
        
        with st.chat_message("assistant"):
            try:
                # SE USA EL MODELO ESTABLE PARA EVITAR 404
                response = model_ia.generate_content(p_user)
                if response and response.text:
                    texto_ia = response.text
                    st.markdown(texto_ia)
                    st.session_state.chat_log.append({"role": "assistant", "content": texto_ia})
            except Exception as e_chat:
                st.error(f"FALLO EN LA CONEXIÓN NEURAL: {str(e_chat)}")

# ==============================================================================
# 9. MÓDULO 4: SEARCH PRO (IMPLEMENTADO MULTI-PERFIL)
# ==============================================================================

elif modulo == "🛰️ SEARCH PRO":
    st.markdown('<div class="module-header">🚀 Buscador Inteligente (Radar V32.9)</div>', unsafe_allow_html=True)
    
    area_search = st.text_area("Canales o perfiles a rastrear (uno por línea):", height=150, placeholder="https://youtube.com/@Canal1\nhttps://tiktok.com/@User2")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    f_inicio = col_s1.date_input("Desde:", value=datetime.date(2026, 2, 1))
    f_fin = col_s2.date_input("Hasta:", value=datetime.date(2026, 2, 28))
    v_umbral = col_s3.number_input("Vistas Mínimas:", value=50000)

    if st.button("🚀 INICIAR ESCANEO RADAR"):
        perfiles = [p.strip() for p in area_search.split('\n') if p.strip()]
        
        if perfiles:
            with st.status("📡 Iniciando barrido masivo...", expanded=True) as status:
                st.write(f"🔍 Detectados {len(perfiles)} perfiles para auditoría...")
                res_search, _ = motor_auditor_universal_v32(perfiles)
                status.update(label="✅ Escaneo Completado", state="complete", expanded=False)
            
            st.markdown('<div class="sub-header">📊 RESULTADOS DEL RADAR</div>', unsafe_allow_html=True)
            st.dataframe(res_search, use_container_width=True, hide_index=True)
            
            # Cálculo de Reporte
            st.markdown('<div class="tactical-summary">', unsafe_allow_html=True)
            total_radar = res_search['Vistas'].sum()
            st.markdown(f"**VISTAS TOTALES DETECTADAS:** {total_radar:,}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("**FÓRMULA TOTAL COPIABLE:**")
            f_search_total = "+".join(res_search['Vistas'].astype(str).tolist())
            st.code(f_search_total if f_search_total else "0", language="text")
        else:
            st.error("Error: Debe ingresar al menos un perfil para el radar.")

# ==============================================================================
# PIE DE PÁGINA Y METADATOS
# ==============================================================================

st.markdown("---")
st.caption(f"BS LATAM SYSTEM V32.9 • {fecha_actual_global} • SECURE PROTOCOL")
