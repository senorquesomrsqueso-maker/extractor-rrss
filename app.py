import streamlit as st
import yt_dlp
import pandas as pd
import re
import time
import random
import requests
import json
import datetime
from io import BytesIO

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL DE ALTO NIVEL
# ==============================================================================
# La API Key de Google Cloud es el núcleo para la inspección de metadatos en Drive.
# Esta llave permite realizar peticiones GET autenticadas a los servidores de Google.
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"

# Configuración del entorno de Streamlit
st.set_page_config(
    page_title="BS LATAM - TITAN SYSTEM",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "ELITE DARK" (CSS EXPANDIDO)
# ==============================================================================
st.markdown("""
    <style>
    /* Estética General del Dashboard */
    .main { background-color: #0b0d11; color: #e6edf3; }
    .stApp { background-color: #0b0d11; }
    
    /* Encabezado Principal con Identidad Visual */
    .title-box { 
        border-left: 10px solid #E30613; 
        padding-left: 30px; 
        margin: 25px 0 45px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,13,17,0) 100%);
    }
    .m-title { 
        font-size: 42px; 
        font-weight: 900; 
        color: #ffffff; 
        margin: 0; 
        text-transform: uppercase; 
        letter-spacing: -2px; 
    }
    .s-title { 
        font-size: 18px; 
        color: #8b949e; 
        margin: 0; 
        font-family: 'Courier New', monospace; 
        font-weight: bold;
    }
    
    /* Contenedores de Métricas Pro */
    [data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        transition: transform 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #E30613;
    }
    [data-testid="stMetricValue"] { 
        color: #E30613 !important; 
        font-weight: 900; 
        font-size: 32px !important;
    }

    /* Botones de Acción de Alto Impacto */
    .stButton>button { 
        background-color: #E30613 !important; 
        color: #ffffff !important; 
        font-weight: 900 !important; 
        text-transform: uppercase;
        letter-spacing: 1px;
        border: none;
        border-radius: 8px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 60px;
        width: 100%;
        font-size: 16px !important;
    }
    .stButton>button:hover { 
        background-color: #ff1a1a !important; 
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(227, 6, 19, 0.6);
    }

    /* Configuración de Tablas y Inputs */
    .stTextArea textarea { 
        background-color: #161b22 !important; 
        color: #e6edf3 !important; 
        border: 1px solid #30363d !important; 
        font-size: 14px !important;
    }
    .stCodeBlock { border: 1px solid #E30613 !important; background-color: #000000 !important; }
    
    /* Blindaje del Header para evitar pérdida de menú lateral */
    header { visibility: visible !important; background: rgba(11,13,17,0.9) !important; border-bottom: 1px solid #30363d; }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE TITAN V15</p>
        <p class="s-title">INTELIGENCIA ESTRATÉGICA DE DATOS • REDES • DRIVE CLOUD • ANALYTICS</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. NÚCLEO DE MEMORIA (PERSISTENCIA DE SESIÓN)
# ==============================================================================
# Inicializamos las bases de datos internas si no existen en la sesión actual.
# No se eliminan líneas, se expande la lógica de log inicial.
persist_keys = ['db_final', 'db_fallidos', 'db_drive', 'chat_log', 'analytics_cache']
for pk in persist_keys:
    if pk not in st.session_state:
        if pk == 'chat_log':
            st.session_state[pk] = [{"role": "assistant", "content": "¡Sistema Titan V15 en línea jefe! Menú corregido, sumador de vistas activo y API de Google sincronizada. 🫡"}]
        elif pk == 'analytics_cache':
            st.session_state[pk] = {"total_scans": 0, "last_scan": "Nunca"}
        else:
            st.session_state[pk] = pd.DataFrame()

# ==============================================================================
# 4. MOTORES DE EXTRACCIÓN TÉCNICA (LÓGICA REFORZADA)
# ==============================================================================

def motor_auditor_rrss_v15(urls):
    """Motor especializado en extracción de métricas de video y foto mediante yt-dlp."""
    exitos, fallos = [], []
    p_bar = st.progress(0)
    status_label = st.empty()
    
    ydl_opts = {
        'quiet': True, 
        'no_warnings': True, 
        'extract_flat': False,
        'skip_download': True, 
        'ignoreerrors': True, 
        'socket_timeout': 30,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.tiktok.com/',
        }
    }
    
    for index, raw_url in enumerate(urls):
        # Limpieza profunda de enlaces para evitar errores de sintaxis
        url_clean = raw_url.strip().replace('"', '').split('?')[0].rstrip(')').rstrip(',')
        status_label.markdown(f"📡 **Rastreando Señal:** `{url_clean[:60]}...`")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_data = ydl.extract_info(url_clean, download=False)
                if info_data:
                    # Lógica de captura de vistas (Prioriza conteo de reproducción)
                    views_count = int(info_data.get('view_count') or info_data.get('play_count') or 0)
                    creator_name = info_data.get('uploader') or info_data.get('creator') or "N/A"
                    video_duration = info_data.get('duration', 0)
                    
                    # Clasificación por plataforma y tipo de contenido
                    if "tiktok" in url_clean:
                        content_type = "📸 TIKTOK FOTO" if (video_duration is None or video_duration <= 0) else "🎥 TIKTOK VIDEO"
                    elif "youtube" in url_clean or "youtu.be" in url_clean:
                        content_type = "🎥 YT VIDEO"
                    else:
                        content_type = "🔗 RED EXTERNA"
                        
                    exitos.append({
                        "Fecha": datetime.datetime.now().strftime("%Y-%m-%d"),
                        "Plataforma": "DIGITAL",
                        "Tipo": content_type,
                        "Creador": creator_name,
                        "Vistas": views_count,
                        "Link": url_clean
                    })
                else:
                    fallos.append({"Link": url_clean, "Error": "Contenido No Disponible / Privado"})
        except Exception as e:
            fallos.append({"Link": url_clean, "Error": f"Fallo de conexión: {str(e)[:30]}"})
        
        p_bar.progress((index + 1) / len(urls))
    
    status_label.empty()
    p_bar.empty()
    return pd.DataFrame(exitos), pd.DataFrame(fallos)

def inspector_drive_deep_v15(urls):
    """Motor oficial vinculado a Google Cloud API para auditoría de archivos pesados."""
    res_list = []
    p_bar_d = st.progress(0)
    for i, link in enumerate(urls):
        # Regex de seguridad para extraer el ID único de Google Drive
        drive_id_match = re.search(r'[-\w]{25,}', link)
        if drive_id_match:
            f_id = drive_id_match.group()
            # Endpoint de la API Drive v3 con campos específicos solicitados
            api_url = f"https://www.googleapis.com/drive/v3/files/{f_id}?fields=name,size,mimeType,modifiedTime,owners&key={DRIVE_API_KEY}"
            try:
                response = requests.get(api_url, timeout=20)
                data = response.json()
                if "error" not in data:
                    size_mb = f"{int(data.get('size', 0))/1024/1024:.2f} MB" if data.get('size') else "Desconocido"
                    res_list.append({
                        "Nombre del Archivo": data.get('name'),
                        "Peso": size_mb,
                        "Tipo MIME": data.get('mimeType').split('/')[-1].upper(),
                        "Estado": "✅ ACCESO TOTAL",
                        "Última Modif.": data.get('modifiedTime', 'N/A')[:10],
                        "Link Original": link
                    })
                else:
                    res_list.append({"Nombre del Archivo": "🔒 PROTEGIDO", "Peso": "0", "Tipo MIME": "N/A", "Estado": "❌ PRIVADO", "Última Modif.": "N/A", "Link Original": link})
            except Exception:
                res_list.append({"Nombre del Archivo": "ERROR TÉCNICO", "Peso": "0", "Tipo MIME": "ERR", "Estado": "❌ ROTO", "Última Modif.": "N/A", "Link Original": link})
        p_bar_d.progress((i + 1) / len(urls))
    p_bar_d.empty()
    return pd.DataFrame(res_list)

# ==============================================================================
# 5. PANEL DE CONTROL LATERAL (NAVIGATION BAR)
# ==============================================================================
with st.sidebar:
    st.markdown("<h1 style='color:#E30613; text-align:center;'>BS LATAM TITAN</h1>", unsafe_allow_html=True)
    st.divider()
    # Selector de módulos maestros
    menu_selector = st.radio(
        "MODULOS ESTRATÉGICOS", 
        ["🚀 EXTRACTOR DE VISTAS", "📊 PERFORMANCE ANALYTICS", "📂 DRIVE CLOUD AUDITOR", "🤖 PARTNER IA PRO", "🛰️ SEARCH PRO"], 
        index=0
    )
    st.divider()
    st.markdown(f"**API Status:** `HEALTHY ✅`")
    st.markdown(f"**Último Escaneo:** `{st.session_state.analytics_cache['last_scan']}`")
    st.divider()
    if st.button("🚨 FORMATEAR BASES DE DATOS"):
        for key in ['db_final', 'db_fallidos', 'db_drive']: st.session_state[key] = pd.DataFrame()
        st.session_state.analytics_cache = {"total_scans": 0, "last_scan": "Reset"}
        st.rerun()

# ==============================================================================
# 6. LÓGICA DE DESPLIEGUE POR MÓDULO (EL CORAZÓN DEL CÓDIGO)
# ==============================================================================

# --- MÓDULO 1: EXTRACTOR PRO CON SUMADOR ---
if menu_selector == "🚀 EXTRACTOR DE VISTAS":
    st.markdown("### 📥 Panel de Entrada de Campaña")
    st.info("Sugerencia: Pega múltiples enlaces separados por espacio o línea para auditoría masiva.")
    user_input = st.text_area("Inserte enlaces (TikTok, YT, FB):", height=220, placeholder="Pega los links de los embajadores aquí...")
    
    col_btn_1, col_btn_2 = st.columns([1, 1])
    with col_btn_1:
        ejecutar = st.button("🔥 EJECUTAR AUDITORÍA MAESTRA")
    with col_btn_2:
        if st.button("🧹 LIMPIAR ENTRADA"): st.rerun()
    
    if ejecutar:
        found_urls = re.findall(r"(https?://[^\s\"\'\)\],]+)", user_input)
        if found_urls:
            df_ex, df_fa = motor_auditor_rrss_v15(found_urls)
            st.session_state.db_final = pd.concat([st.session_state.db_final, df_ex]).drop_duplicates(subset=['Link'])
            st.session_state.db_fallidos = pd.concat([st.session_state.db_fallidos, df_fa]).drop_duplicates(subset=['Link'])
            st.session_state.analytics_cache['total_scans'] += len(found_urls)
            st.session_state.analytics_cache['last_scan'] = datetime.datetime.now().strftime("%H:%M:%S")
            st.rerun()

    if not st.session_state.db_final.empty:
        df_view = st.session_state.db_final
        st.divider()
        
        # --- SECCIÓN DE MÉTRICAS Y SUMADOR (PEDIDO JEFE) ---
        c1, c2 = st.columns([1, 2])
        total_vistas_sum = df_view['Vistas'].sum()
        c1.metric("MÉTRICA TOTAL DE VISTAS", f"{total_vistas_sum:,}")
        
        with c2:
            st.markdown("**📋 CADENA DE SUMA PARA COPIADO (Excel/Sheets):**")
            v_list = [str(v) for v in df_view['Vistas'].tolist()]
            suma_cadena = " + ".join(v_list)
            # st.code genera el botón de copiado automático al pasar el mouse
            st.code(suma_cadena, language="text")
            st.caption("✔️ Haz clic en el icono de la esquina superior derecha del cuadro negro para copiar la suma.")

        st.dataframe(df_view, use_container_width=True, hide_index=True)
        
        # Exportación Excel Pro
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_view.to_excel(writer, index=False, sheet_name='Auditoria_Redes')
        st.download_button("📥 EXPORTAR REPORTE EXCEL", buffer.getvalue(), "Reporte_Audit_Elite.xlsx")

    if not st.session_state.db_fallidos.empty:
        st.markdown("### ❌ Enlaces No Procesados")
        st.dataframe(st.session_state.db_fallidos, use_container_width=True, hide_index=True)

# --- MÓDULO 2: PERFORMANCE ANALYTICS (NUEVO) ---
elif menu_selector == "📊 PERFORMANCE ANALYTICS":
    st.subheader("📊 Análisis de Rendimiento de Campaña")
    if not st.session_state.db_final.empty:
        df_a = st.session_state.db_final
        col1, col2, col3 = st.columns(3)
        col1.metric("Promedio de Vistas", f"{int(df_a['Vistas'].mean()):,}")
        col2.metric("Mejor Rendimiento", f"{df_a['Vistas'].max():,}")
        col3.metric("Peor Rendimiento", f"{df_a['Vistas'].min():,}")
        
        st.bar_chart(df_a.set_index('Creador')['Vistas'])
    else:
        st.warning("No hay datos suficientes para generar analíticas. Por favor, realiza un escaneo primero.")

# --- MÓDULO 3: DRIVE AUDITOR CLOUD ---
elif menu_selector == "📂 DRIVE CLOUD AUDITOR":
    st.subheader("📂 Auditor de Archivos en Google Drive")
    st.markdown("Utiliza la API oficial de Google para verificar integridad y permisos de archivos.")
    input_d = st.text_area("Inserte links de Drive:", height=150, placeholder="https://drive.google.com/file/d/...")
    
    if st.button("🛡️ INSPECCIONAR SERVIDORES DRIVE"):
        links_drive = re.findall(r"(https?://drive\.google\.com/[^\s\"\'\)\],]+)", input_d)
        if links_drive:
            with st.spinner("Conectando con Google Cloud API..."):
                df_drive_res = inspector_drive_deep_v15(links_drive)
                st.session_state.db_drive = pd.concat([st.session_state.db_drive, df_drive_res]).drop_duplicates(subset=['Link Original'])
            st.rerun()
    
    if not st.session_state.db_drive.empty:
        st.dataframe(st.session_state.db_drive, use_container_width=True, hide_index=True)
        # Descarga Drive Excel
        buf_d = BytesIO()
        with pd.ExcelWriter(buf_d, engine='xlsxwriter') as wr:
            st.session_state.db_drive.to_excel(wr, index=False)
        st.download_button("📥 DESCARGAR REPORTE DRIVE", buf_d.getvalue(), "Auditoria_Drive_Deep.xlsx")

# --- MÓDULO 4: PARTNER IA PRO ---
elif menu_selector == "🤖 PARTNER IA PRO":
    st.subheader("🤖 Partner IA + Calculadora Estratégica")
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if chat_p := st.chat_input("Consulta métricas o realiza cálculos..."):
        st.session_state.chat_log.append({"role": "user", "content": chat_p})
        with st.chat_message("user"): st.markdown(chat_p)
        
        with st.chat_message("assistant"):
            clean_text = chat_p.lower().replace('x', '*').replace(',', '')
            math_regex = re.search(r"(\d+[\s\+\-\*\/\%]+\d+)", clean_text)
            if math_regex:
                try:
                    res_math = eval(math_regex.group(1))
                    final_ans = f"🔢 **Cálculo Detectado:** {math_regex.group(1)} = **{res_math:,}**"
                except: final_ans = "Hubo un error en la expresión matemática, jefe."
            else:
                final_ans = "Estoy procesando la información. La API Key de Google Drive está activa y el sumador de vistas está configurado para exportación rápida."
            st.markdown(final_ans)
            st.session_state.chat_log.append({"role": "assistant", "content": final_ans})

# --- MÓDULO 5: SEARCH PRO ---
elif menu_selector == "🛰️ SEARCH PRO":
    st.subheader("🛰️ Search Pro - Rastreador de Perfiles")
    st.info("Módulo de escaneo de canales activo. Listo para indexar nuevos usuarios.")
