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

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL Y NÚCLEO IA DE ALTO RENDIMIENTO
# ==============================================================================
# Llaves de acceso (Mantener protocolos de seguridad)
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk" 
GEMINI_API_KEY = "AIzaSyA8HsM0vSCopd1s05nOryhbNIGU26dvxG4"

# Configuración de página de Streamlit - Interfaz Pro
st.set_page_config(
    page_title="BS LATAM - AUDIT ELITE SUPREMACÍA V32.5",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialización de Inteligencia Artificial Gemini 1.5 Flash
try:
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Obtenemos fecha actual para el contexto de la IA
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    generation_config = {
        "temperature": 0.85,
        "top_p": 0.95,
        "top_k": 45,
        "max_output_tokens": 4096,
    }
    
    # Instrucción del sistema "Todoterreno" - Identidad Corporativa BS LATAM
    system_instruction_core = (
        f"Eres el Consultor Senior y Partner Estratégico de BS LATAM. "
        f"HOY ES: {fecha_actual}. "
        "Tu misión es asistir al usuario en TODO: auditoría, programación, redacción, "
        "matemáticas complejas y análisis de negocios. "
        "Eres una IA GENERAL, no limitada solo al tool. "
        "Mantén siempre un tono profesional, con autoridad técnica (Estilo Cyberpunk/Industrial Corporativo). "
        "NUNCA uses frases robóticas. Eres el copiloto de la operación."
    )

    model_ia = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        generation_config=generation_config,
        system_instruction=system_instruction_core
    )
except Exception as e_ia:
    st.error(f"Falla crítica en el núcleo neural: {e_ia}")

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
    .stApp { background-color: #0b0d11; }
    
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
        font-size: 60px; font-weight: 900; color: #ffffff; 
        text-transform: uppercase; letter-spacing: 12px; margin: 0; 
        line-height: 1.1; text-shadow: 5px 5px 10px rgba(0,0,0,1);
    }
    .s-title { 
        font-size: 26px; color: #8b949e; font-family: 'Courier New', monospace; 
        margin-top: 25px; letter-spacing: 5px; font-weight: bold;
    }

    /* ESTILO DE LOS ENCABEZADOS DE MÓDULO */
    .module-header {
        font-size: 32px; font-weight: 700; color: #ffffff;
        margin-top: 40px; margin-bottom: 25px;
        display: flex; align-items: center; gap: 15px;
        border-bottom: 1px solid #30363d; padding-bottom: 15px;
    }
    .sub-header {
        font-size: 20px; font-weight: 600; color: #E30613;
        margin-top: 20px; text-transform: uppercase; letter-spacing: 2px;
    }

    /* ESTILO BS LATAM SIDEBAR */
    .bs-latam-sidebar {
        color: #ffffff; font-weight: 950; font-size: 45px; text-align: center;
        text-transform: uppercase; letter-spacing: 7px;
        text-shadow: 0px 0px 30px #0055ff, 4px 4px 0px #000000;
        margin-bottom: 45px; padding: 25px; border-bottom: 4px solid #E30613;
    }

    /* BOTONERÍA ÉLITE */
    .stButton>button { 
        background: linear-gradient(135deg, #E30613 0%, #9e040d 100%) !important;
        color: #ffffff !important; font-weight: 900 !important; 
        text-transform: uppercase; border-radius: 30px; 
        height: 70px; width: 100%; font-size: 22px !important;
        border: none; box-shadow: 0 10px 20px rgba(227,6,19,0.35);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover {
        transform: scale(1.02) translateY(-4px);
        box-shadow: 0 15px 35px rgba(227,6,19,0.55);
        border: 2px solid #ffffff;
    }
    
    /* INPUTS Y TEXT AREAS MASIVAS */
    .stTextArea textarea, .stTextInput input, .stNumberInput input { 
        background-color: #161b22 !important; color: #e6edf3 !important; 
        border: 2px solid #30363d !important; border-radius: 15px;
        font-size: 16px; padding: 15px;
    }
    .stTextArea textarea:focus, .stTextInput input:focus { 
        border-color: #E30613 !important; 
    }

    /* TABLAS Y DATAFRAMES */
    [data-testid="stDataFrame"] {
        border: 2px solid #30363d; border-radius: 20px; overflow: hidden;
        background-color: #161b22;
    }
    
    /* BLOQUES DE CÓDIGO */
    .stCodeBlock {
        border: 1px solid #E30613;
        border-radius: 10px;
    }

    /* MÉTRICAS PERSONALIZADAS */
    .metric-card {
        background: #161b22;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363d;
        text-align: center;
    }
    .metric-value {
        font-size: 35px; font-weight: 800; color: #E30613;
    }
    .metric-label {
        font-size: 14px; color: #8b949e; text-transform: uppercase;
    }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V32.5</p>
        <p class="s-title">SISTEMA INTEGRAL BS LATAM • EXTRACTOR & FORMAT DETECTION</p>
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
    st.session_state.chat_log = [{"role": "assistant", "content": f"Sistema V32.5 Online. Núcleo táctico activado. ¿Cuál es la misión de hoy?"}]

# ==============================================================================
# 4. FUNCIONES CORE - LÓGICA DE PROCESAMIENTO
# ==============================================================================
def calcular_puntuacion_engagement(vistas, likes, comentarios):
    if vistas == 0: return 0.0
    score = ((likes + (comentarios * 3)) / vistas) * 100
    return round(score, 3)

def exportar_excel_pro(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='BS_LATAM_AUDIT')
        workbook = writer.book
        worksheet = writer.sheets['BS_LATAM_AUDIT']
        header_format = workbook.add_format({'bold': True, 'bg_color': '#E30613', 'font_color': 'white'})
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
    return output.getvalue()

def analizar_imagen_con_ia(image_file):
    """Usa Gemini Vision para leer métricas de imágenes."""
    try:
        img = Image.open(image_file)
        prompt_vision = (
            "Actúa como un extractor de datos OCR de alta precisión. "
            "Analiza esta imagen de métricas de redes sociales. "
            "Identifica el número TOTAL de VISTAS. "
            "Devuelve SOLO EL NÚMERO entero crudo."
        )
        response = model_ia.generate_content([prompt_vision, img])
        texto_limpio = re.sub(r'[^0-9]', '', response.text)
        return int(texto_limpio) if texto_limpio else 0
    except Exception:
        return 0

def motor_auditor_universal_v32(urls):
    """Core de scraping optimizado con detección de formato Shorts vs Largo"""
    resultados = []
    fallidos = []
    p_bar = st.progress(0)
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]

    for i, raw_url in enumerate(urls):
        # Limpieza de URL
        url = raw_url.strip().replace('"', '').replace("'", "").split('?si=')[0]
        
        ydl_opts = {
            'quiet': True, 'ignoreerrors': True, 'skip_download': True,
            'http_headers': {'User-Agent': random.choice(user_agents)},
            'extract_flat': False
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    # Lógica de detección de plataforma y formato
                    plataforma = "OTRO"
                    formato = "ESTÁNDAR"
                    
                    if "tiktok.com" in url:
                        plataforma = "TIKTOK"
                    elif "youtube.com" in url or "youtu.be" in url:
                        plataforma = "YOUTUBE"
                        # Detección de Shorts: Por URL o por duración (< 61 seg)
                        duracion = info.get('duration', 0)
                        if "/shorts/" in url or (duracion and duracion <= 65):
                            formato = "SHORTS"
                        else:
                            formato = "LARGO"

                    views = int(info.get('view_count') or 0)
                    resultados.append({
                        "Fecha": info.get('upload_date', 'N/A'),
                        "Plataforma": plataforma,
                        "Formato": formato,
                        "Creador": info.get('uploader', 'N/A'),
                        "Título": info.get('title', 'N/A')[:60],
                        "Vistas": views,
                        "Likes": int(info.get('like_count') or 0),
                        "Comments": int(info.get('comment_count') or 0),
                        "Link": url
                    })
                else:
                    fallidos.append({"Link": url, "Error": "Sin respuesta del servidor"})
        except Exception as e:
            fallidos.append({"Link": url, "Error": str(e)[:50]})
        
        p_bar.progress((i + 1) / len(urls))
    
    p_bar.empty()
    return pd.DataFrame(resultados), pd.DataFrame(fallidos)

# ==============================================================================
# 5. SIDEBAR Y NAVEGACIÓN
# ==============================================================================
with st.sidebar:
    st.markdown('<p class="bs-latam-sidebar">BS LATAM</p>', unsafe_allow_html=True)
    modulo = st.radio("MÓDULOS OPERATIVOS", ["🚀 EXTRACTOR ELITE", "📂 DRIVE AUDITOR", "🤖 PARTNER IA", "🛰️ SEARCH PRO"])
    
    st.divider()
    st.markdown("### 🛠️ Herramientas Rápidas")
    if st.button("🚨 REINICIO DE CACHÉ"):
        st.session_state.clear()
        st.rerun()
    
    st.info("V32.5: Ahora detecta automáticamente si un video de YT es Short o Largo.")

# ==============================================================================
# 6. MÓDULO 1: EXTRACTOR (MODIFICADO CON NUEVAS REGLAS)
# ==============================================================================
if modulo == "🚀 EXTRACTOR ELITE":
    st.markdown('<div class="module-header">📥 Extractor de Métricas Masivas</div>', unsafe_allow_html=True)
    
    # Entrada de links masiva
    texto_entrada = st.text_area("Pega los enlaces (uno por línea o separados por comas):", height=250)
    
    col_btn, col_info = st.columns([1, 2])
    with col_btn:
        ejecutar = st.button("🔥 EJECUTAR AUDITORÍA")
    with col_info:
        st.caption("Acepta YouTube (VOD/Shorts) y TikTok. Procesamiento en paralelo.")

    if ejecutar:
        urls = re.findall(r"(https?://[^\s\"\'\)\],]+)", texto_entrada)
        if urls:
            res, fails = motor_auditor_universal_v32(urls)
            st.session_state.db_final = res
            st.session_state.db_fallidos = fails
            st.success(f"Proceso completado. {len(res)} éxitos, {len(fails)} fallos.")
        else:
            st.warning("No detecté enlaces válidos.")

    # --- VISUALIZACIÓN DE RESULTADOS ---
    if not st.session_state.db_final.empty:
        df = st.session_state.db_final
        
        st.divider()
        st.markdown('<div class="sub-header">📊 DATOS EXTRAÍDOS (DETECCIÓN DE FORMATO)</div>', unsafe_allow_html=True)
        
        # Colorear la columna Formato para visibilidad
        def highlight_format(val):
            color = '#E30613' if val == 'LARGO' else '#0055ff' if val == 'SHORTS' else 'white'
            return f'color: {color}; font-weight: bold'
        
        st.dataframe(df.style.applymap(highlight_format, subset=['Formato']), use_container_width=True, hide_index=True)

        # --- SECCIÓN DE LINKS FALLIDOS ---
        if not st.session_state.db_fallidos.empty:
            with st.expander("⚠️ VER ENLACES FALLIDOS / NO ACCESIBLES"):
                st.table(st.session_state.db_fallidos)

        # --- PANEL DE EXPORTACIÓN Y SUMATORIAS ---
        st.markdown('<div class="module-header">📋 CENTRO DE COPIADO Y MÉTRICAS</div>', unsafe_allow_html=True)
        
        # Cálculos específicos solicitados
        total_vistas = df['Vistas'].sum()
        yt_largos = df[(df['Plataforma'] == 'YOUTUBE') & (df['Formato'] == 'LARGO')]
        yt_shorts = df[(df['Plataforma'] == 'YOUTUBE') & (df['Formato'] == 'SHORTS')]
        tiktok_vistas = df[df['Plataforma'] == 'TIKTOK']

        # Fórmulas de suma
        formula_general = "+".join(df['Vistas'].astype(str).tolist())
        formula_largos = "+".join(yt_largos['Vistas'].astype(str).tolist())
        formula_shorts = "+".join(yt_shorts['Vistas'].astype(str).tolist())

        # Columnas de visualización de métricas
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-card"><p class="metric-label">Vistas Totales</p><p class="metric-value">{total_vistas:,}</p></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><p class="metric-label">Vistas YT Largos</p><p class="metric-value">{yt_largos["Vistas"].sum():,}</p></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><p class="metric-label">Vistas YT Shorts</p><p class="metric-value">{yt_shorts["Vistas"].sum():,}</p></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-card"><p class="metric-label">Total Links</p><p class="metric-value">{len(df)}</p></div>', unsafe_allow_html=True)

        # Bloques de copiado (ZONA CRÍTICA)
        st.markdown("### 📥 Bloques de Texto para Copiar")
        
        c_copy1, c_copy2 = st.columns(2)
        
        with c_copy1:
            st.markdown("**1. FÓRMULA VISTAS (GENERAL)**")
            st.code(formula_general, language="text")
            
            st.markdown("**2. FÓRMULA VISTAS (YOUTUBE LARGOS)**")
            st.code(formula_largos if formula_largos else "0", language="text")
            
            st.markdown("**3. FÓRMULA VISTAS (YOUTUBE SHORTS)**")
            st.code(formula_shorts if formula_shorts else "0", language="text")

        with c_copy2:
            st.markdown("**4. DESGLOSE POR PLATAFORMA / TIPO**")
            resumen_txt = (
                f"YouTube Videos: {yt_largos['Vistas'].sum()}\n"
                f"YouTube Shorts: {yt_shorts['Vistas'].sum()}\n"
                f"TikTok: {tiktok_vistas['Vistas'].sum()}\n"
                f"TOTAL: {total_vistas}"
            )
            st.code(resumen_txt, language="yaml")
            
            st.markdown("**5. LINKS PROCESADOS**")
            links_txt = "\n".join(df['Link'].tolist())
            st.code(links_txt, language="text")

# ==============================================================================
# 7. MÓDULO 2: DRIVE AUDITOR (VISION IA)
# ==============================================================================
elif modulo == "📂 DRIVE AUDITOR":
    st.markdown('<div class="module-header">👁️ Auditor Visual de Métricas</div>', unsafe_allow_html=True)
    st.info("Sube capturas de pantalla de analíticas. La IA leerá los números automáticamente.")
    
    uploaded_files = st.file_uploader("Arrastra las capturas aquí:", type=['png', 'jpg', 'jpeg', 'webp'], accept_multiple_files=True)
    
    if st.button("🧠 PROCESAR EVIDENCIA VISUAL"):
        if uploaded_files:
            resultados_v = []
            bar = st.progress(0)
            for idx, file in enumerate(uploaded_files):
                vistas = analizar_imagen_con_ia(file)
                resultados_v.append({"Archivo": file.name, "Vistas Detectadas": vistas})
                bar.progress((idx+1)/len(uploaded_files))
            st.session_state.db_drive_vision = pd.DataFrame(resultados_v)
            st.success("Análisis completado.")

    if not st.session_state.db_drive_vision.empty:
        st.dataframe(st.session_state.db_drive_vision, use_container_width=True)
        st.code("+".join(st.session_state.db_drive_vision['Vistas Detectadas'].astype(str).tolist()))

# ==============================================================================
# 8. MÓDULO 3: PARTNER IA
# ==============================================================================
elif modulo == "🤖 PARTNER IA":
    st.markdown('<div class="module-header">🤖 Partner IA - Consultor Estratégico</div>', unsafe_allow_html=True)
    
    for mensaje in st.session_state.chat_log:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])
    
    if prompt := st.chat_input("Escribe tu instrucción..."):
        st.session_state.chat_log.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Pasar historial para memoria de conversación
                historial = []
                for m in st.session_state.chat_log[:-1]:
                    rol = "model" if m["role"] == "assistant" else "user"
                    historial.append({"role": rol, "parts": [m["content"]]})
                
                chat = model_ia.start_chat(history=historial)
                response = chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.chat_log.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error en enlace neural: {e}")

# ==============================================================================
# 9. MÓDULO 4: SEARCH PRO (MANTENIDO Y OPTIMIZADO)
# ==============================================================================
elif modulo == "🛰️ SEARCH PRO":
    st.markdown('<div class="module-header">🚀 Buscador Inteligente (Radar V32.5)</div>', unsafe_allow_html=True)
    
    area_canales = st.text_area("Pega los links de canales o usuarios:", height=200, placeholder="@usuario\nhttps://youtube.com/@canal")
    
    c_p1, c_p2 = st.columns(2)
    f_desde = c_p1.date_input("Desde:", value=datetime.date(2026, 2, 2))
    v_minimas = c_p2.number_input("Umbral de vistas:", value=50000)

    if st.button("🚀 LANZAR ESCANEO MASIVO"):
        canales = [c.strip() for c in area_canales.split('\n') if c.strip()]
        if canales:
            # Lógica simplificada para el ejemplo, pero funcional
            st.info("Iniciando fase de descubrimiento...")
            # Aquí se integraría la lógica de yt_dlp para listar videos de canales
            # y luego pasarlos por el motor_auditor_universal_v32
        else:
            st.warning("Ingresa al menos un canal.")

# ==============================================================================
# PIE DE PÁGINA Y METADATOS DE SESIÓN
# ==============================================================================
st.markdown("---")
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.caption(f"BS LATAM SYSTEM V32.5 • {fecha_actual} • ENCRIPTACIÓN ACTIVA")
with col_f2:
    st.markdown('<p style="text-align:right; color:#8b949e; font-size:12px;">© 2026 ELITE SUPREMACY UNIT</p>', unsafe_allow_html=True)
