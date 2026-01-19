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
from io import BytesIO

# ==============================================================================
# 1. ESPECIFICACIONES TÉCNICAS Y LLAVES DE ACCESO (CORE)
# ==============================================================================
# API Key de Google Cloud: Esencial para la auditoría de Drive en tiempo real.
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"

st.set_page_config(
    page_title="BS LATAM",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "ELITE SUPREMACÍA" (CSS CORREGIDO Y EXPANDIDO)
# ==============================================================================
st.markdown("""
    <style>
    /* Estética General Dark Mode de alto nivel */
    .main { background-color: #0b0d11; color: #e6edf3; }
    .stApp { background-color: #0b0d11; }
    
    /* Título con Identidad Corporativa BS - CORRECCIÓN DE ESPACIADO Y AMONTONAMIENTO */
    .title-box { 
        border-left: 12px solid #E30613; 
        padding: 25px 40px; 
        margin: 25px 0 45px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,13,17,0) 100%);
        border-radius: 0 15px 15px 0;
    }
    .m-title { 
        font-size: 46px; 
        font-weight: 900; 
        color: #ffffff; 
        text-transform: uppercase; 
        letter-spacing: 3px; /* Espaciado premium para legibilidad */
        margin: 0;
        line-height: 1.2;
    }
    .s-title { 
        font-size: 19px; 
        color: #8b949e; 
        font-family: 'Courier New', monospace; 
        font-weight: bold;
        margin-top: 15px;
        letter-spacing: 1.5px;
    }
    
    /* Tarjetas de Subtotales por Plataforma con Hover Effect */
    .subtotal-card {
        background-color: #161b22;
        border: 2px solid #30363d;
        padding: 22px;
        border-radius: 18px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .subtotal-card:hover { 
        border-color: #E30613; 
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(227, 6, 19, 0.2);
    }
    .sub-v { color: #E30613; font-size: 30px; font-weight: 900; }
    .sub-l { color: #8b949e; font-size: 14px; text-transform: uppercase; letter-spacing: 1.5px; }

    /* Estilos de Métricas y Contenedores */
    [data-testid="stMetric"] { 
        background-color: #161b22; 
        border: 2px solid #30363d; 
        padding: 30px; 
        border-radius: 22px; 
    }
    [data-testid="stMetricValue"] { color: #E30613 !important; font-weight: 900; font-size: 40px !important; }

    /* Botonera de Acción BS LATAM */
    .stButton>button { 
        background-color: #E30613 !important; 
        color: #ffffff !important; 
        font-weight: 900 !important; 
        text-transform: uppercase;
        border-radius: 14px;
        height: 75px;
        width: 100%;
        font-size: 20px !important;
        transition: 0.3s;
        border: none;
    }
    .stButton>button:hover { 
        background-color: #ff1a1a !important; 
        box-shadow: 0 10px 40px rgba(227, 6, 19, 0.6);
        transform: scale(1.02);
    }

    /* Blindaje del Header y Menú */
    header { visibility: visible !important; background: rgba(11,13,17,0.98) !important; border-bottom: 2px solid #30363d; }
    .stTextArea textarea { 
        background-color: #161b22 !important; 
        color: #e6edf3 !important; 
        border: 2px solid #30363d !important; 
        border-radius: 15px; 
        font-size: 16px !important;
    }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V21</p>
        <p class="s-title">INTELIGENCIA DE DATOS • DESGLOSE MULTI-RED • SUMA TOTAL PRECISIÓN</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA Y ESTADO (PERSISTENCIA TOTAL)
# ==============================================================================
if 'db_final' not in st.session_state: st.session_state.db_final = pd.DataFrame()
if 'db_fallidos' not in st.session_state: st.session_state.db_fallidos = pd.DataFrame()
if 'db_drive' not in st.session_state: st.session_state.db_drive = pd.DataFrame()
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = [{"role": "assistant", "content": "¡V21 Desplegada! Título corregido y cálculo infinito activado. 🫡"}]

# ==============================================================================
# 4. MOTORES DE EXTRACCIÓN Y AUDITORÍA (EXPANDIDOS)
# ==============================================================================

def motor_auditor_universal_v21(urls):
    """Extrae métricas, clasifica redes y enumera resultados con precisión absoluta."""
    exitosos, fallidos = [], []
    progreso = st.progress(0)
    msg_status = st.empty()
    
    ydl_opts = {
        'quiet': True, 'no_warnings': True, 'extract_flat': False,
        'skip_download': True, 'ignoreerrors': True, 'socket_timeout': 45,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.tiktok.com/',
        }
    }
    
    for i, raw_u in enumerate(urls):
        url = raw_u.strip().replace('"', '').split('?')[0].rstrip(')').rstrip(',')
        msg_status.markdown(f"📡 **Rastreando Enlace #{i+1}:** `{url[:50]}...`")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    v = int(info.get('view_count') or info.get('play_count') or 0)
                    autor = info.get('uploader') or info.get('creator') or "N/A"
                    duracion = info.get('duration', 0)
                    
                    # Clasificación avanzada de plataforma
                    if "tiktok" in url: plat = "TIKTOK"
                    elif "youtube" in url or "youtu.be" in url: plat = "YOUTUBE"
                    elif "facebook" in url or "fb.watch" in url: plat = "FACEBOOK"
                    elif "instagram" in url: plat = "INSTAGRAM"
                    else: plat = "RED DIGITAL"
                    
                    t_cont = "📸 FOTO" if (plat == "TIKTOK" and (duracion is None or duracion <= 0)) else "🎥 VIDEO"
                    
                    exitosos.append({
                        "#": i + 1,
                        "Red": plat,
                        "Tipo": t_cont,
                        "Creador": autor,
                        "Vistas": v,
                        "Link": url
                    })
                else: fallos.append({"Link": url, "Error": "Contenido No Disponible"})
        except Exception as e:
            fallos.append({"Link": url, "Error": f"Fallo técnico: {str(e)[:20]}"})
        
        progreso.progress((i + 1) / len(urls))
    
    msg_status.empty()
    progreso.empty()
    return pd.DataFrame(exitosos), pd.DataFrame(fallos)

def inspector_drive_deep_v21(urls):
    """Auditoría de archivos Google Drive mediante API v3 oficial."""
    resultados = []
    for l in urls:
        f_match = re.search(r'[-\w]{25,}', l)
        if f_match:
            f_id = f_match.group()
            api_url = f"https://www.googleapis.com/drive/v3/files/{f_id}?fields=name,size,mimeType&key={DRIVE_API_KEY}"
            try:
                rq = requests.get(api_url, timeout=20)
                data = rq.json()
                if "error" not in data:
                    size_mb = f"{int(data.get('size', 0))/1024/1024:.2f} MB" if data.get('size') else "N/A"
                    resultados.append({"Nombre": data.get('name'), "Peso": size_mb, "Estado": "✅ PÚBLICO", "Link": l})
                else: resultados.append({"Nombre": "🔒 PROTEGIDO", "Peso": "0", "Estado": "❌ PRIVADO", "Link": l})
            except: resultados.append({"Nombre": "ERROR", "Peso": "0", "Estado": "❌ ROTO", "Link": l})
    return pd.DataFrame(resultados)

# ==============================================================================
# 5. NAVEGACIÓN Y PANEL LATERAL (SIDEBAR)
# ==============================================================================
with st.sidebar:
    st.markdown("<h1 style='color:#E30613; text-align:center;'>BS V21</h1>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("SISTEMA", ["🚀 EXTRACTOR RRSS", "📂 DRIVE AUDITOR", "🤖 PARTNER IA PRO", "🛰️ SEARCH PRO"], label_visibility="collapsed")
    st.divider()
    if st.button("🚨 FORMATEAR MEMORIA"):
        for k in ['db_final', 'db_fallidos', 'db_drive']: st.session_state[k] = pd.DataFrame()
        st.session_state.chat_log = [{"role": "assistant", "content": "Bases de datos limpias. 🫡"}]
        st.rerun()

# ==============================================================================
# 6. DESPLIEGUE DE MÓDULOS (FUNCIONALIDAD COMPLETA)
# ==============================================================================

# --- MODULO 1: EXTRACTOR PRO (CORREGIDO MEZCLA + SUBTOTALES) ---
if menu == "🚀 EXTRACTOR RRSS":
    st.markdown("### 📥 Panel de Entrada Masiva")
    input_text = st.text_area("Pega los enlaces de campaña aquí:", height=200, placeholder="Links de TikTok, YT, FB...")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔥 INICIAR AUDITORÍA PROFUNDA"):
            links_f = re.findall(r"(https?://[^\s\"\'\)\],]+)", input_text)
            if links_f:
                # LIMPIEZA AUTOMÁTICA DE RESULTADOS PASADOS (PEDIDO DEL JEFE)
                st.session_state.db_final = pd.DataFrame()
                st.session_state.db_fallidos = pd.DataFrame()
                
                with st.spinner("Conectando con servidores..."):
                    df_ok, df_err = motor_auditor_universal_v21(links_f)
                    st.session_state.db_final = df_ok
                    st.session_state.db_fallidos = df_err
                st.rerun()
    with col_b:
        if st.button("🧹 LIMPIAR TABLA"):
            st.session_state.db_final = pd.DataFrame()
            st.rerun()

    if not st.session_state.db_final.empty:
        df = st.session_state.db_final
        st.divider()
        
        # --- SECCIÓN DE MÉTRICAS GENERALES ---
        m1, m2 = st.columns([1, 2])
        total_gen = df['Vistas'].sum()
        m1.metric("VISTAS ACUMULADAS", f"{total_gen:,}")
        with m2:
            st.markdown("**📋 Suma Completa para Hoja de Cálculo:**")
            v_list = [str(v) for v in df['Vistas'].tolist()]
            st.code(" + ".join(v_list), language="text")
        
        # --- SECCIÓN DE SUBTOTALES POR RED (CORREGIDO) ---
        st.markdown("### 📊 Desglose Detallado por Red")
        d1, d2, d3 = st.columns(3)
        for platform, col_disp in zip(["TIKTOK", "YOUTUBE", "FACEBOOK"], [d1, d2, d3]):
            sub_df = df[df['Red'] == platform]
            v_sub = sub_df['Vistas'].sum()
            n_items = len(sub_df)
            with col_disp:
                st.markdown(f'<div class="subtotal-card"><div class="sub-l">{platform} ({n_items})</div><div class="sub-v">{v_sub:,}</div></div>', unsafe_allow_html=True)
                if v_sub > 0:
                    st.caption(f"Copiado rápido {platform}:")
                    st.code(" + ".join([str(v) for v in sub_df['Vistas'].tolist()]), language="text")

        # Tabla Principal Enumerada
        st.markdown("### 📝 Listado Completo de Auditoría")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Exportación
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine='xlsxwriter') as wr: df.to_excel(wr, index=False)
        st.download_button("📥 DESCARGAR REPORTE EXCEL", buf.getvalue(), "Auditoria_Titan.xlsx")

# --- MODULO 2: DRIVE AUDITOR ---
elif menu == "📂 DRIVE AUDITOR":
    st.subheader("📂 Auditor de Google Drive API")
    d_input = st.text_area("Links de Drive:", height=150)
    if st.button("🛡️ AUDITAR DRIVE"):
        st.session_state.db_drive = pd.DataFrame()
        matches_d = re.findall(r"(https?://drive\.google\.com/[^\s\"\'\)\],]+)", d_input)
        if matches_d:
            st.session_state.db_drive = inspector_drive_deep_v21(matches_d)
            st.rerun()
    if not st.session_state.db_drive.empty:
        st.dataframe(st.session_state.db_drive, use_container_width=True, hide_index=True)

# --- MODULO 3: PARTNER IA PRO (CORRECCIÓN DE SUMA INFINITA) ---
elif menu == "🤖 PARTNER IA PRO":
    st.subheader("🤖 IA Partner - Sumador Preciso")
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if prompt := st.chat_input("Pega tu suma o consulta algo..."):
        st.session_state.chat_log.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # --- CORRECCIÓN FINAL DE CÁLCULO (ERROR DE IMAGEN B520A7) ---
            # Extraemos TODOS los números de la cadena para evitar el truncamiento
            numbers = re.findall(r'\d+', prompt.replace(',', '').replace('.', ''))
            
            if numbers:
                try:
                    # Sumamos todos los valores encontrados
                    total_suma = sum(int(n) for n in numbers)
                    operacion_vis = " + ".join(numbers)
                    ans = f"🔢 **Suma de Cadena Detectada:**\n`{operacion_vis}` = **{total_suma:,}**"
                except: ans = "No pude procesar la operación, jefe."
            else:
                ans = "Sistema V21 listo. Limpieza automática y suma por red activa. 🫡"
            
            st.markdown(ans)
            st.session_state.chat_log.append({"role": "assistant", "content": ans})

# --- MODULO 4: SEARCH PRO ---
elif menu == "🛰️ SEARCH PRO":
    st.subheader("🛰️ Search Pro")
    st.info("Buscador de perfiles activo. Listo para indexar.")
