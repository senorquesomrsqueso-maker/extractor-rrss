import streamlit as st
import yt_dlp
import pandas as pd
import re
import time
import random
import requests
import json
import datetime
import math
from io import BytesIO

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL DE ALTO NIVEL (CORE)
# ==============================================================================
# La API Key de Google Cloud es vital para el acceso profundo a archivos de Drive.
# Permite obtener metadata real como peso, nombre y fecha de modificación.
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"

# Configuración de entorno Streamlit (Layout ancho para máxima visibilidad)
st.set_page_config(
    page_title="BS LATAM - TITAN DATA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. DISEÑO VISUAL "ELITE DARK" (CSS REFORZADO Y EXPANDIDO)
# ==============================================================================
st.markdown("""
    <style>
    /* Estética Dark Mode de Alto Nivel */
    .main { background-color: #0b0d11; color: #e6edf3; }
    .stApp { background-color: #0b0d11; }
    
    /* Encabezado Principal Estilo Branding BS */
    .title-box { 
        border-left: 12px solid #E30613; 
        padding-left: 35px; 
        margin: 30px 0 50px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,13,17,0) 100%);
        border-radius: 0 10px 10px 0;
    }
    .m-title { 
        font-size: 45px; 
        font-weight: 900; 
        color: #ffffff; 
        margin: 0; 
        text-transform: uppercase; 
        letter-spacing: -2.5px; 
    }
    .s-title { 
        font-size: 19px; 
        color: #8b949e; 
        margin: 5px 0 0 0; 
        font-family: 'Courier New', monospace; 
        font-weight: bold;
    }
    
    /* Contenedores de Métricas Pro */
    [data-testid="stMetric"] {
        background-color: #161b22;
        border: 2px solid #30363d;
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 12px 24px rgba(0,0,0,0.6);
        transition: all 0.4s ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: #E30613;
        transform: scale(1.02);
    }
    [data-testid="stMetricValue"] { 
        color: #E30613 !important; 
        font-weight: 900; 
        font-size: 36px !important;
    }

    /* Botones de Acción de BS LATAM */
    .stButton>button { 
        background-color: #E30613 !important; 
        color: #ffffff !important; 
        font-weight: 900 !important; 
        text-transform: uppercase;
        letter-spacing: 1.5px;
        border: none;
        border-radius: 10px;
        transition: all 0.3s cubic-bezier(0.19, 1, 0.22, 1);
        height: 65px;
        width: 100%;
        font-size: 18px !important;
    }
    .stButton>button:hover { 
        background-color: #ff1a1a !important; 
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(227, 6, 19, 0.5);
    }

    /* Campos de Entrada de Datos */
    .stTextArea textarea { 
        background-color: #161b22 !important; 
        color: #e6edf3 !important; 
        border: 2px solid #30363d !important; 
        font-size: 15px !important;
        border-radius: 12px;
    }
    .stCodeBlock { border: 2px solid #30363d !important; background-color: #000000 !important; border-radius: 10px; }
    
    /* Mantenimiento del Header (Solución error menú) */
    header { visibility: visible !important; background: rgba(11,13,17,0.95) !important; border-bottom: 2px solid #30363d; }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V17</p>
        <p class="s-title">ESTRATEGIA DIGITAL • GOOGLE CLOUD ENGINE • MULTI-SUMA PRECISIÓN</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA Y ESTADO (PERSISTENCIA TOTAL)
# ==============================================================================
# Definición de llaves de sesión para evitar pérdida de datos al navegar.
keys_to_init = ['db_final', 'db_fallidos', 'db_drive', 'chat_log', 'session_meta']
for key in keys_to_init:
    if key not in st.session_state:
        if key == 'chat_log':
            st.session_state[key] = [{"role": "assistant", "content": "¡Sistema V17 Supremacía en línea! Corregido: Limpieza automática de tablas y suma infinita activada. 🫡"}]
        elif key == 'session_meta':
            st.session_state[key] = {"init_time": time.time(), "total_actions": 0}
        else:
            st.session_state[key] = pd.DataFrame()

# ==============================================================================
# 4. MOTORES DE ANÁLISIS DE DATOS (REFORZADOS)
# ==============================================================================

def motor_auditor_rrss_v17(urls):
    """Extrae métricas de vistas de videos y fotos de TikTok/YT/FB/IG."""
    exitosos, fallidos = [], []
    progreso = st.progress(0)
    msg_status = st.empty()
    
    ydl_opts = {
        'quiet': True, 'no_warnings': True, 'extract_flat': False,
        'skip_download': True, 'ignoreerrors': True, 'socket_timeout': 30,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.tiktok.com/',
        }
    }
    
    for i, u_raw in enumerate(urls):
        url = u_raw.strip().replace('"', '').split('?')[0].rstrip(')').rstrip(',')
        msg_status.markdown(f"📡 **Analizando:** `{url[:55]}...`")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    vistas = int(info.get('view_count') or info.get('play_count') or 0)
                    autor = info.get('uploader') or info.get('creator') or "Anónimo"
                    duracion = info.get('duration', 0)
                    
                    if "tiktok" in url:
                        tipo_c = "📸 TIKTOK FOTO" if (duracion is None or duracion <= 0) else "🎥 TIKTOK VIDEO"
                    elif "youtube" in url or "youtu.be" in url:
                        tipo_c = "🎥 YT VIDEO"
                    else:
                        tipo_c = "🔗 ENLACE RED"
                        
                    exitosos.append({
                        "Registro": datetime.datetime.now().strftime("%H:%M:%S"),
                        "Plataforma": "DIGITAL",
                        "Tipo": tipo_c,
                        "Creador": autor,
                        "Vistas": vistas,
                        "Link": url
                    })
                else:
                    fallidos.append({"Link": url, "Error": "Contenido Privado/No Encontrado"})
        except Exception as e:
            fallos.append({"Link": url, "Error": f"Fallo técnico: {str(e)[:25]}"})
        
        progreso.progress((i + 1) / len(urls))
    
    msg_status.empty()
    progreso.empty()
    return pd.DataFrame(exitosos), pd.DataFrame(fallidos)

def inspector_drive_deep_v17(urls):
    """Auditoría profunda de Google Drive mediante API Key oficial."""
    res = []
    bar_d = st.progress(0)
    for i, l in enumerate(urls):
        f_match = re.search(r'[-\w]{25,}', l)
        if f_match:
            f_id = f_match.group()
            # Endpoint de Google Drive API v3
            api_endpoint = f"https://www.googleapis.com/drive/v3/files/{f_id}?fields=name,size,mimeType,modifiedTime&key={DRIVE_API_KEY}"
            try:
                rq = requests.get(api_endpoint, timeout=20)
                data = rq.json()
                if "error" not in data:
                    size_mb = f"{int(data.get('size', 0))/1024/1024:.2f} MB" if data.get('size') else "N/A"
                    res.append({
                        "Archivo": data.get('name'),
                        "Peso": size_mb,
                        "Formato": data.get('mimeType').split('/')[-1].upper(),
                        "Estado": "✅ PÚBLICO",
                        "Link": l
                    })
                else:
                    res.append({"Archivo": "🔒 PRIVADO", "Peso": "0", "Formato": "N/A", "Estado": "❌ BLOQUEADO", "Link": l})
            except:
                res.append({"Archivo": "ERROR", "Peso": "0", "Formato": "ERR", "Estado": "❌ ROTO", "Link": l})
        bar_d.progress((i + 1) / len(urls))
    bar_d.empty()
    return pd.DataFrame(res)

# ==============================================================================
# 5. NAVEGACIÓN Y PANEL LATERAL (SIDEBAR)
# ==============================================================================
with st.sidebar:
    st.markdown("<h1 style='color:#E30613; text-align:center;'>BS V17</h1>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("SECCIONES MAESTRAS", ["🚀 EXTRACTOR RRSS", "📂 DRIVE AUDITOR", "🤖 PARTNER IA PRO", "🛰️ SEARCH PRO"], label_visibility="collapsed")
    st.divider()
    st.write(f"Acciones en sesión: `{st.session_state.session_meta['total_actions']}`")
    if st.button("🚨 REINICIAR SISTEMA"):
        for k in ['db_final', 'db_fallidos', 'db_drive']: st.session_state[k] = pd.DataFrame()
        st.session_state.chat_log = [{"role": "assistant", "content": "Memoria formateada. 🫡"}]
        st.rerun()

# ==============================================================================
# 6. LÓGICA DE MÓDULOS (EXPANSIÓN Y CORRECCIÓN DE ERRORES)
# ==============================================================================

# --- MODULO 1: EXTRACTOR PRO (CORREGIDO MEZCLA DE DATOS) ---
if menu == "🚀 EXTRACTOR RRSS":
    st.markdown("### 📥 Panel de Entrada Masiva")
    input_urls = st.text_area("Pega los enlaces de campaña aquí:", height=200, placeholder="TikTok, YouTube, Facebook...")
    
    col1, col2 = st.columns(2)
    with col1:
        btn_go = st.button("🔥 INICIAR AUDITORÍA PROFUNDA")
    with col2:
        if st.button("🧹 LIMPIAR TABLA ACTUAL"):
            st.session_state.db_final = pd.DataFrame()
            st.rerun()
    
    if btn_go:
        matches = re.findall(r"(https?://[^\s\"\'\)\],]+)", input_urls)
        if matches:
            # --- CORRECCIÓN ERROR 1: LIMPIEZA ANTES DE NUEVOS DATOS ---
            st.session_state.db_final = pd.DataFrame() 
            st.session_state.db_fallidos = pd.DataFrame()
            
            with st.spinner("Procesando enlaces..."):
                ok, err = motor_auditor_rrss_v17(matches)
                st.session_state.db_final = ok
                st.session_state.db_fallidos = err
                st.session_state.session_meta['total_actions'] += 1
            st.rerun()

    if not st.session_state.db_final.empty:
        df = st.session_state.db_final
        st.divider()
        
        # --- SECCIÓN DE COPIADO RÁPIDO Y SUMA ---
        m1, m2 = st.columns([1, 2])
        total_v = df['Vistas'].sum()
        m1.metric("VISTAS TOTALES", f"{total_v:,}")
        
        with m2:
            st.markdown("**📋 Suma para Hoja de Cálculo (Excel/Sheets):**")
            v_list = [str(v) for v in df['Vistas'].tolist()]
            cadena_suma = " + ".join(v_list)
            # st.code incluye botón de copiado nativo
            st.code(cadena_suma, language="text")
            st.caption("Pasa el mouse sobre el cuadro negro para copiar la cadena.")

        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Exportación
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine='xlsxwriter') as wr: df.to_excel(wr, index=False)
        st.download_button("📥 DESCARGAR REPORTE EXCEL", buf.getvalue(), "Auditoria_RRSS.xlsx")

# --- MODULO 2: DRIVE AUDITOR ---
elif menu == "📂 DRIVE AUDITOR":
    st.subheader("📂 Google Drive Deep Auditor (API Mode)")
    input_dr = st.text_area("Links de Drive:", height=150)
    if st.button("🛡️ AUDITAR GOOGLE DRIVE"):
        # Limpieza automática para Drive también
        st.session_state.db_drive = pd.DataFrame()
        matches_d = re.findall(r"(https?://drive\.google\.com/[^\s\"\'\)\],]+)", input_dr)
        if matches_d:
            df_dr = inspector_drive_deep_v17(matches_d)
            st.session_state.db_drive = df_dr
            st.rerun()
    if not st.session_state.db_drive.empty:
        st.dataframe(st.session_state.db_drive, use_container_width=True, hide_index=True)

# --- MODULO 3: PARTNER IA PRO (CORREGIDO MULTI-SUMA) ---
elif menu == "🤖 PARTNER IA PRO":
    st.subheader("🤖 Partner IA + Calculadora Infinita")
    for m in st.session_state.chat_log:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if prompt := st.chat_input("Dime algo jefe o pega tu suma..."):
        st.session_state.chat_log.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # --- CORRECCIÓN ERROR 2: SUMA DE CADENA INFINITA ---
            # Limpiamos el texto de espacios y caracteres basura
            clean_p = prompt.replace(' ', '').replace(',', '')
            # Regex que captura TODA la cadena matemática (números y operadores)
            math_match = re.search(r"([\d\+\-\*\/\.]+)", clean_p)
            
            if math_match:
                try:
                    # eval() ejecuta la cadena completa (ej: 100+200+300+400)
                    op_completa = math_match.group(1)
                    res_math = eval(op_completa)
                    resp = f"🔢 **Cálculo de Cadena Detectado:**\n`{op_completa}` = **{res_math:,}**"
                except:
                    resp = "Error en la expresión matemática, jefe."
            else:
                resp = "Estoy listo jefe. Módulos de limpieza y suma infinita activos. 🫡"
            
            st.markdown(resp)
            st.session_state.chat_log.append({"role": "assistant", "content": resp})

# --- MODULO 4: SEARCH PRO ---
elif menu == "🛰️ SEARCH PRO":
    st.subheader("🛰️ Search Pro - Rastreador de Canales")
    st.info("Buscador de perfiles activo. Ingrese nombres para indexar datos de embajadores.")
