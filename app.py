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
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk" # Referencial
GEMINI_API_KEY = "AIzaSyA8HsM0vSCopd1s05nOryhbNIGU26dvxG4"

# Configuración de página de Streamlit - Interfaz Pro
st.set_page_config(
    page_title="BS LATAM - AUDIT ELITE SUPREMACÍA V32.2",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialización de Inteligencia Artificial Gemini 1.5
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
    
    # Instrucción del sistema "Todoterreno"
    system_instruction_core = (
        f"Eres el Consultor Senior y Partner Estratégico de BS LATAM. "
        f"HOY ES: {fecha_actual}. "
        "Tu misión es asistir al usuario en TODO: auditoría, programación, redacción, "
        "matemáticas complejas, análisis de negocios o charla casual. "
        "Eres una IA GENERAL, no limitada solo al tool. "
        "Si te piden la fecha, dásela. Si te piden calcular, hazlo con precisión extrema. "
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
# 2. CAPA DE DISEÑO VISUAL "ELITE SUPREMACÍA"
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
    
    /* BLOQUES DE CÓDIGO (Para copiar) */
    .stCodeBlock {
        border: 1px solid #E30613;
        border-radius: 10px;
    }

    /* ESTILO PARA FALLIDOS */
    .error-container {
        background-color: #2d0000;
        border: 1px solid #ff4b4b;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V32.2</p>
        <p class="s-title">SISTEMA INTEGRAL BS LATAM • DETECCIÓN DE FORMATO & VISION AI</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA Y LOGS
# ==============================================================================
if 'db_final' not in st.session_state: st.session_state.db_final = pd.DataFrame()
if 'db_fallidos' not in st.session_state: st.session_state.db_fallidos = pd.DataFrame()
if 'db_drive_vision' not in st.session_state: st.session_state.db_drive_vision = pd.DataFrame()
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = [{"role": "assistant", "content": f"Sistema V32 Online. Fecha: {datetime.datetime.now().strftime('%d/%m/%Y')}. A la orden."}]

# ==============================================================================
# 4. FUNCIONES CORE
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
            "Identifica el número TOTAL de VISTAS (Views, Visualizaciones, Reproducciones). "
            "Devuelve SOLO EL NÚMERO entero crudo (sin texto, sin comas, ejemplo: 45000). "
            "Si hay múltiples videos, devuelve la suma total o el número más prominente de visualizaciones."
        )
        response = model_ia.generate_content([prompt_vision, img])
        texto_limpio = re.sub(r'[^0-9]', '', response.text)
        return int(texto_limpio) if texto_limpio else 0
    except Exception:
        return 0

def motor_auditor_universal_v31(urls):
    """Core de scraping optimizado con detección de formato Shorts vs Videos"""
    resultados = []
    fallidos = []
    p_bar = st.progress(0)
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    ]

    for i, raw_url in enumerate(urls):
        url = raw_url.strip().replace('"', '').replace("'", "").split('?si=')[0]
        
        ydl_opts = {
            'quiet': True, 'ignoreerrors': True, 'skip_download': True,
            'http_headers': {'User-Agent': random.choice(user_agents)}
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    v_views = int(info.get('view_count') or 0)
                    v_platform = "TIKTOK" if "tiktok" in url else "YOUTUBE"
                    
                    # Lógica de detección: Shorts vs Largo
                    v_tipo = "N/A"
                    if v_platform == "YOUTUBE":
                        # Se asume Short si la duración < 65s o si la URL contiene 'shorts'
                        duration = info.get('duration') or 0
                        if "/shorts/" in url or duration <= 65:
                            v_tipo = "YouTube Shorts"
                        else:
                            v_tipo = "YouTube Video"
                    else:
                        v_tipo = "TikTok"

                    resultados.append({
                        "Fecha": info.get('upload_date', 'N/A'),
                        "Plataforma": v_platform,
                        "Tipo": v_tipo,
                        "Creador": info.get('uploader', 'N/A'),
                        "Título": info.get('title', 'N/A')[:60],
                        "Vistas": v_views,
                        "Likes": int(info.get('like_count') or 0),
                        "Comments": int(info.get('comment_count') or 0),
                        "Link": url
                    })
                else:
                    fallidos.append({"Link": url, "Error": "Acceso denegado / No encontrado"})
        except Exception as e:
            fallidos.append({"Link": url, "Error": str(e)[:40]})
        
        p_bar.progress((i + 1) / len(urls))
    
    p_bar.empty()
    return pd.DataFrame(resultados), pd.DataFrame(fallidos)

# ==============================================================================
# 5. SIDEBAR Y NAVEGACIÓN
# ==============================================================================
with st.sidebar:
    st.markdown('<p class="bs-latam-sidebar">BS LATAM</p>', unsafe_allow_html=True)
    modulo = st.radio("MÓDULOS OPERATIVOS", ["🚀 EXTRACTOR", "📂 DRIVE AUDITOR (VISION IA)", "🤖 PARTNER IA", "🛰️ SEARCH PRO"])
    
    st.divider()
    if st.button("🚨 REINICIO FORZADO"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    st.caption("BS LATAM Elite v32.2.0")

# ==============================================================================
# 6. MÓDULO 1: EXTRACTOR (MODIFICADO)
# ==============================================================================
if modulo == "🚀 EXTRACTOR":
    st.markdown('<div class="module-header">📥 Extractor de Métricas Masivas</div>', unsafe_allow_html=True)
    texto_entrada = st.text_area("Pega los enlaces (uno por línea):", height=200, placeholder="Pega aquí todos tus links...")
    
    if st.button("🔥 EJECUTAR AUDITORÍA"):
        # Regex mejorada para capturar links sin importar el formato
        urls = re.findall(r"(https?://[^\s\"\'\)\],]+)", texto_entrada)
        if urls:
            res, fail = motor_auditor_universal_v31(urls)
            st.session_state.db_final = res
            st.session_state.db_fallidos = fail
        else:
            st.warning("No detecté enlaces válidos.")

    # MOSTRAR ENLACES FALLIDOS PRIMERO (Si existen)
    if not st.session_state.db_fallidos.empty:
        st.markdown('<div class="sub-header">⚠️ ENLACES FALLIDOS / NO PROCESADOS</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.db_fallidos, use_container_width=True, hide_index=True)

    # MOSTRAR RESULTADOS EXITOSOS
    if not st.session_state.db_final.empty:
        df = st.session_state.db_final
        st.divider()
        st.markdown('<div class="sub-header">📊 RESULTADOS TABULADOS & TIPO DE VIDEO</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown('<div class="module-header">📋 CENTRO DE EXPORTACIÓN Y COPIADO</div>', unsafe_allow_html=True)
        st.info("Utiliza los botones de la esquina derecha de cada bloque para copiar las métricas segregadas.")

        # COLUMNAS DE RESULTADOS EXTENDIDAS
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown("**1. TOTAL GENERAL (SUMA)**")
            total_vistas = df['Vistas'].sum()
            st.code(f"{total_vistas}", language="text")
            st.caption("Cifra total limpia de todos los links.")

        with c2:
            st.markdown("**2. FÓRMULA LARGOS (X+Y+Z)**")
            # Filtro solo videos largos de YouTube
            df_largos = df[df['Tipo'] == 'YouTube Video']
            txt_vistas_largos = "+".join(df_largos['Vistas'].astype(str).tolist())
            st.code(txt_vistas_largos if txt_vistas_largos else "0", language="text")
            st.caption(f"Suma YouTube Largos: {df_largos['Vistas'].sum():,}")

        with c3:
            st.markdown("**3. VISTAS POR CATEGORÍA**")
            # Agrupación por el nuevo campo "Tipo"
            resumen = df.groupby('Tipo')['Vistas'].sum().reset_index()
            txt_resumen = ""
            for _, row in resumen.iterrows():
                txt_resumen += f"{row['Tipo']}: {row['Vistas']}\n"
            st.code(txt_resumen, language="yaml")
            st.caption("Desglose táctico por formato.")

        with c4:
            st.markdown("**4. TOTAL DE REGISTROS**")
            st.code(f"Procesados: {len(df)}\nFallidos: {len(st.session_state.db_fallidos)}", language="text")
            st.caption("Conteo de flujo de datos.")

        # SECCIÓN DE SUMATORIA COMPLETA (GENERAL)
        st.markdown("**FÓRMULA GENERAL DE TODOS LOS VIDEOS (X+Y+Z)**")
        txt_vistas_all = "+".join(df['Vistas'].astype(str).tolist())
        st.code(txt_vistas_all, language="text")

# ==============================================================================
# 7. MÓDULO 2: DRIVE AUDITOR (VISION IA)
# ==============================================================================
elif modulo == "📂 DRIVE AUDITOR (VISION IA)":
    st.markdown('<div class="module-header">👁️ Auditor Visual de Métricas (Gemini Vision)</div>', unsafe_allow_html=True)
    st.info("SISTEMA IA ACTIVADO: Sube las capturas de pantalla de analíticas. La IA detectará las vistas automáticamente.")
    
    uploaded_files = st.file_uploader("Sube tus capturas de métricas:", type=['png', 'jpg', 'jpeg', 'webp'], accept_multiple_files=True)

    if st.button("🧠 PROCESAR EVIDENCIA VISUAL"):
        resultados_vision = []
        if uploaded_files:
            bar_vision = st.progress(0)
            for idx, uploaded_file in enumerate(uploaded_files):
                st.toast(f"Escaneando: {uploaded_file.name}")
                vistas_detectadas = analizar_imagen_con_ia(uploaded_file)
                resultados_vision.append({
                    "Archivo": uploaded_file.name,
                    "Vistas Detectadas": vistas_detectadas,
                    "Estado": "✅ Leído" if vistas_detectadas > 0 else "⚠️ Revisión Manual"
                })
                bar_vision.progress((idx + 1) / len(uploaded_files))
            bar_vision.empty()
            st.session_state.db_drive_vision = pd.DataFrame(resultados_vision)
            st.success("Análisis Neural Completado.")

    if not st.session_state.db_drive_vision.empty:
        df_v = st.session_state.db_drive_vision
        st.dataframe(df_v, use_container_width=True, hide_index=True)
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.markdown("**Fórmula de Suma (X+Y+Z)**")
            lista_vistas = df_v[df_v['Vistas Detectadas'] > 0]['Vistas Detectadas'].tolist()
            st.code("+".join(map(str, lista_vistas)) if lista_vistas else "0", language="text")
        with col_v2:
            st.metric(label="Total Extraído", value=f"{df_v['Vistas Detectadas'].sum():,}")

# ==============================================================================
# 8. MÓDULO 3: PARTNER IA
# ==============================================================================
elif modulo == "🤖 PARTNER IA":
    st.markdown('<div class="module-header">🤖 Partner IA - Asistente General</div>', unsafe_allow_html=True)
    
    for mensaje in st.session_state.chat_log:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])
    
    if prompt_user := st.chat_input("Escribe tu instrucción..."):
        st.session_state.chat_log.append({"role": "user", "content": prompt_user})
        with st.chat_message("user"):
            st.markdown(prompt_user)
            
        with st.chat_message("assistant"):
            try:
                contexto_hist = []
                for m in st.session_state.chat_log[:-1]:
                    r_ia = "model" if m["role"] == "assistant" else "user"
                    contexto_hist.append({"role": r_ia, "parts": [m["content"]]})
                
                chat = model_ia.start_chat(history=contexto_hist)
                response = chat.send_message(prompt_user)
                st.markdown(response.text)
                st.session_state.chat_log.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error de conexión neural: {e}")

# ==============================================================================
# 9. MÓDULO 4: SEARCH PRO
# ==============================================================================
elif modulo == "🛰️ SEARCH PRO":
    st.markdown('<div class="module-header">🚀 Buscador Inteligente (Radar V32)</div>', unsafe_allow_html=True)
    area_canales = st.text_area("Pega los links de canales o usuarios:", height=200)
    
    col_p1, col_p2 = st.columns([2, 1])
    with col_p1:
        st.markdown('<div class="sub-header">📅 Rango de tiempo</div>', unsafe_allow_html=True)
        c_f1, c_f2 = st.columns(2)
        f_desde = c_f1.date_input("Desde:", value=datetime.date(2026, 2, 2))
        f_hasta = c_f2.date_input("Hasta:", value=datetime.date(2026, 2, 9))
    with col_p2:
        v_minimas = st.number_input("Vistas mínimas:", value=60000, step=5000)

    if st.button("🚀 LANZAR ESCANEO MASIVO"):
        canales_finales = [c.strip() for c in area_canales.split('\n') if c.strip()]
        if canales_finales:
            lista_acumulada_links = []
            with st.status("🛠️ Iniciando Rastreo Profundo...", expanded=True) as status_ui:
                for canal in canales_finales:
                    url_canal = canal.split('?')[0].rstrip('/')
                    if not url_canal.startswith('http'):
                        url_canal = f"https://www.tiktok.com/@{url_canal.replace('@', '')}"
                    
                    status_ui.write(f"🔍 Analizando: `{url_canal}`")
                    try:
                        opts_search = {'extract_flat': 'in_playlist', 'quiet': True, 'ignoreerrors': True, 'playlist_items': '1-20'}
                        with yt_dlp.YoutubeDL(opts_search) as ydl_s:
                            data_canal = ydl_s.extract_info(url_canal, download=False)
                            if data_canal and 'entries' in data_canal:
                                t_inicio = time.mktime(f_desde.timetuple())
                                t_fin = time.mktime((f_hasta + datetime.timedelta(days=1)).timetuple())
                                for video in data_canal['entries']:
                                    if not video: continue
                                    v_fecha = video.get('upload_date')
                                    if v_fecha:
                                        v_ts = time.mktime(datetime.datetime.strptime(v_fecha, "%Y%m%d").timetuple())
                                        if t_inicio <= v_ts <= t_fin:
                                            v_url = video.get('url') or f"https://www.tiktok.com/video/{video.get('id')}"
                                            lista_acumulada_links.append(v_url)
                    except:
                        status_ui.write(f"⚠️ Error en perfil `{url_canal}`.")
                
                if lista_acumulada_links:
                    st.session_state.db_final, _ = motor_auditor_universal_v31(list(set(lista_acumulada_links)))
                    st.rerun()
                else:
                    st.error("No se hallaron videos en ese rango.")

    if not st.session_state.db_final.empty:
        df_elite = st.session_state.db_final[st.session_state.db_final['Vistas'] >= v_minimas].sort_values(by="Vistas", ascending=False)
        st.markdown(f"### 🏆 Resultados Filtrados (+{v_minimas:,} vistas)")
        st.dataframe(df_elite, use_container_width=True, hide_index=True)

# ==============================================================================
# PIE DE PÁGINA
# ==============================================================================
st.markdown("---")
st.caption(f"BS LATAM SYSTEM V32.2 • {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} • ENCRYPTED")
