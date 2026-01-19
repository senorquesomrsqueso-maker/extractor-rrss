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
from io import BytesIO

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL Y LLAVES DE ACCESO (CORE)
# ==============================================================================
# Llave Maestra para Auditoría de Google Drive API v3
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"

st.set_page_config(
    page_title="AUDIT-ELITE PRO V24 - OMNI TITAN MAX",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "ELITE SUPREMACÍA" (CSS REFORZADO - ANTI-ENCIMADO)
# ==============================================================================
st.markdown("""
    <style>
    /* Fondo Global Industrial Dark */
    .main { background-color: #0b0d11; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
    .stApp { background-color: #0b0d11; }
    
    /* BLOQUE DE TÍTULO: Corregido para evitar amontonamiento de letras */
    .title-box { 
        border-left: 15px solid #E30613; 
        padding: 35px 50px; 
        margin: 30px 0 50px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,13,17,0) 100%);
        border-radius: 0 25px 25px 0;
        box-shadow: 10px 0 30px rgba(0,0,0,0.5);
    }
    .m-title { 
        font-size: 48px; 
        font-weight: 900; 
        color: #ffffff; 
        text-transform: uppercase; 
        letter-spacing: 6px; /* Espaciado máximo para legibilidad total */
        margin: 0;
        line-height: 1.1;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }
    .s-title { 
        font-size: 20px; 
        color: #8b949e; 
        font-family: 'Courier New', monospace; 
        font-weight: bold;
        margin-top: 15px;
        letter-spacing: 2.5px;
    }
    
    /* Tarjetas de Métricas por Plataforma con Animación */
    .subtotal-card {
        background-color: #161b22;
        border: 2px solid #30363d;
        padding: 28px;
        border-radius: 22px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 20px;
    }
    .subtotal-card:hover { 
        border-color: #E30613; 
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 20px 45px rgba(227, 6, 19, 0.25);
    }
    .sub-v { color: #E30613; font-size: 34px; font-weight: 950; text-shadow: 0 0 10px rgba(227,6,19,0.3); }
    .sub-l { color: #8b949e; font-size: 15px; text-transform: uppercase; letter-spacing: 2px; font-weight: bold; }

    /* Estilos de Métricas Streamlit y Botones BS */
    [data-testid="stMetric"] { background-color: #161b22; border: 2px solid #30363d; padding: 35px; border-radius: 25px; }
    [data-testid="stMetricValue"] { color: #E30613 !important; font-weight: 900; font-size: 44px !important; }

    .stButton>button { 
        background: linear-gradient(135deg, #E30613 0%, #9e040d 100%) !important;
        color: #ffffff !important; 
        font-weight: 900 !important; 
        text-transform: uppercase;
        border-radius: 18px;
        height: 85px;
        width: 100%;
        font-size: 24px !important;
        border: none;
        letter-spacing: 1px;
    }
    .stButton>button:hover { 
        filter: brightness(1.2);
        box-shadow: 0 15px 50px rgba(227, 6, 19, 0.6);
        transform: scale(1.01);
    }

    /* Blindaje de UI: Sidebar, Textarea y Header */
    header { visibility: visible !important; background: rgba(11,13,17,0.99) !important; border-bottom: 3px solid #30363d; }
    .stTextArea textarea { 
        background-color: #161b22 !important; 
        color: #e6edf3 !important; 
        border: 2px solid #30363d !important; 
        border-radius: 20px;
        padding: 20px;
        font-size: 17px !important;
    }
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 2px solid #30363d; }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V24</p>
        <p class="s-title">INTELIGENCIA DE DATOS • DESGLOSE RRSS • SUMA TOTAL PRECISIÓN</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA Y ESTADO DEL SISTEMA (PERSISTENCIA)
# ==============================================================================
# Inicialización de bases de datos internas para evitar vacíos accidentales
if 'db_final' not in st.session_state: st.session_state.db_final = pd.DataFrame()
if 'db_fallidos' not in st.session_state: st.session_state.db_fallidos = pd.DataFrame()
if 'db_drive' not in st.session_state: st.session_state.db_drive = pd.DataFrame()
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = [{"role": "assistant", "content": "¡V24 Desplegada! Título corregido y motor de suma infinita activo. 🫡"}]

# ==============================================================================
# 4. MOTORES DE AUDITORÍA Y EXTRACCIÓN (REFORZADOS)
# ==============================================================================

def motor_auditor_universal_v24(urls):
    """Extrae métricas, clasifica y enumera links con blindaje de errores."""
    exitos, fallos = [], []
    p_bar = st.progress(0)
    msg_status = st.empty()
    
    # Opciones de extracción de alta compatibilidad
    ydl_opts = {
        'quiet': True, 'no_warnings': True, 'extract_flat': False,
        'skip_download': True, 'ignoreerrors': True, 'socket_timeout': 40,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.google.com/',
        }
    }
    
    for i, raw_u in enumerate(urls):
        # Limpieza profunda del link
        url = raw_u.strip().replace('"', '').split('?')[0].rstrip(')').rstrip(',')
        msg_status.markdown(f"📡 **Analizando Enlace #{i+1}:** `{url[:55]}...`")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    vistas = int(info.get('view_count') or info.get('play_count') or 0)
                    autor = info.get('uploader') or info.get('creator') or "N/A"
                    duracion = info.get('duration', 0)
                    
                    # Motor de clasificación por dominio
                    if "tiktok" in url: plat = "TIKTOK"
                    elif "youtube" in url or "youtu.be" in url: plat = "YOUTUBE"
                    elif "facebook" in url or "fb.watch" in url: plat = "FACEBOOK"
                    elif "instagram" in url: plat = "INSTAGRAM"
                    else: plat = "OTRA RED"
                    
                    tipo_c = "📸 FOTO/CARROUSEL" if (plat == "TIKTOK" and (duracion is None or duracion <= 0)) else "🎥 VIDEO"
                    
                    exitos.append({
                        "#": i + 1,
                        "Red": plat,
                        "Formato": tipo_c,
                        "Creador": autor,
                        "Vistas": vistas,
                        "Link Original": url
                    })
                else:
                    fallos.append({"Link": url, "Motivo": "Privado o Eliminado"})
        except Exception as e:
            fallos.append({"Link": url, "Motivo": f"Error de red: {str(e)[:15]}"})
        
        p_bar.progress((i + 1) / len(urls))
    
    msg_status.empty()
    p_bar.empty()
    return pd.DataFrame(exitos), pd.DataFrame(fallos)

def auditor_drive_api_v24(urls):
    """Auditoría de integridad de Drive vía Google API v3."""
    resultados_d = []
    for link in urls:
        f_id_match = re.search(r'[-\w]{25,}', link)
        if f_id_match:
            f_id = f_id_match.group()
            endpoint = f"https://www.googleapis.com/drive/v3/files/{f_id}?fields=name,size,mimeType&key={DRIVE_API_KEY}"
            try:
                resp = requests.get(endpoint, timeout=25)
                meta = resp.json()
                if "error" not in meta:
                    peso_mb = f"{int(meta.get('size', 0))/1024/1024:.2f} MB" if meta.get('size') else "N/A"
                    resultados_d.append({
                        "Archivo": meta.get('name'), 
                        "Peso": peso_mb, 
                        "Estado": "✅ DISPONIBLE", 
                        "Acceso": "PÚBLICO",
                        "Link": link
                    })
                else:
                    resultados_d.append({"Archivo": "🔒 PROTEGIDO", "Peso": "0", "Estado": "❌ BLOQUEADO", "Acceso": "PRIVADO", "Link": link})
            except:
                resultados_d.append({"Archivo": "ERROR", "Peso": "0", "Estado": "❌ ROTO", "Acceso": "S/N", "Link": link})
    return pd.DataFrame(resultados_d)

# ==============================================================================
# 5. PANEL DE NAVEGACIÓN (SIDEBAR ESTRATÉGICO)
# ==============================================================================
with st.sidebar:
    st.markdown("<h1 style='color:#E30613; text-align:center;'>SISTEMA BS TITAN</h1>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("SELECCIÓN DE MÓDULO", 
                    ["🚀 EXTRACTOR DE VISTAS", "📂 DRIVE AUDITOR", "🤖 PARTNER IA PRO", "🛰️ SEARCH PRO"], 
                    label_visibility="collapsed")
    st.divider()
    if st.button("🚨 REINICIAR TODO EL SISTEMA"):
        for k in ['db_final', 'db_fallidos', 'db_drive']: st.session_state[k] = pd.DataFrame()
        st.session_state.chat_log = [{"role": "assistant", "content": "Memoria formateada. Listo para nueva carga. 🫡"}]
        st.rerun()
    st.info(f"V24 Omni-Titan\nBuild: {datetime.date.today().year}.01.19")

# ==============================================================================
# 6. DESPLIEGUE DE MÓDULOS OPERATIVOS
# ==============================================================================

# --- MODULO 1: EXTRACTOR PRO (CORRECCIÓN DE SUMA + ENUMERACIÓN) ---
if menu == "🚀 EXTRACTOR DE VISTAS":
    st.markdown("### 📥 Entrada de Enlaces de Campaña")
    raw_input = st.text_area("Pega aquí todos los links (TikTok, YT, FB, IG):", height=220, 
                             placeholder="Pega la lista de enlaces de los embajadores...")
    
    col_run, col_clear = st.columns(2)
    with col_run:
        if st.button("🔥 EJECUTAR AUDITORÍA"):
            links_f = re.findall(r"(https?://[^\s\"\'\)\],]+)", raw_input)
            if links_f:
                # Limpieza obligatoria para evitar mezcla de datos
                st.session_state.db_final = pd.DataFrame()
                st.session_state.db_fallidos = pd.DataFrame()
                
                with st.spinner("Procesando metadatos de redes sociales..."):
                    try:
                        df_ok, df_err = motor_auditor_universal_v24(links_f)
                        st.session_state.db_final = df_ok
                        st.session_state.db_fallidos = df_err
                    except Exception:
                        st.error("Error crítico en el motor de extracción.")
                        st.code(traceback.format_exc())
                st.rerun()
    with col_clear:
        if st.button("🧹 LIMPIAR TABLA ACTUAL"):
            st.session_state.db_final = pd.DataFrame()
            st.rerun()

    if not st.session_state.db_final.empty:
        df = st.session_state.db_final
        st.divider()
        
        # SECCIÓN DE MÉTRICAS GLOBALES
        m_col1, m_col2 = st.columns([1, 2])
        vistas_globales = df['Vistas'].sum()
        m_col1.metric("VISTAS ACUMULADAS", f"{vistas_globales:,}")
        with m_col2:
            st.markdown("**📋 Suma para Hoja de Cálculo (General):**")
            v_list_full = [str(v) for v in df['Vistas'].tolist()]
            st.code(" + ".join(v_list_full), language="text")
        
        # SECCIÓN DE SUBTOTALES POR RED (PEDIDO DEL JEFE)
        st.markdown("### 📊 Desglose por Plataforma")
        d1, d2, d3 = st.columns(3)
        for platform, col_disp in zip(["TIKTOK", "YOUTUBE", "FACEBOOK"], [d1, d2, d3]):
            sub_df = df[df['Red'] == platform]
            v_sub = sub_df['Vistas'].sum()
            n_sub = len(sub_df)
            with col_disp:
                st.markdown(f"""
                <div class="subtotal-card">
                    <div class="sub-l">{platform} ({n_sub} ÍTEMS)</div>
                    <div class="sub-v">{v_sub:,}</div>
                </div>
                """, unsafe_allow_html=True)
                if v_sub > 0:
                    st.caption(f"Copiado rápido {platform}:")
                    st.code(" + ".join([str(v) for v in sub_df['Vistas'].tolist()]), language="text")

        # TABLA DE RESULTADOS ENUMERADA
        st.markdown("### 📝 Listado Completo de Auditoría")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # EXPORTACIÓN
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine='xlsxwriter') as wr: df.to_excel(wr, index=False)
        st.download_button("📥 DESCARGAR REPORTE EXCEL (XLSX)", buf.getvalue(), "Auditoria_Titan_V24.xlsx")

# --- MODULO 2: DRIVE AUDITOR ---
elif menu == "📂 DRIVE AUDITOR":
    st.subheader("📂 Auditor de Integridad de Google Drive")
    st.write("Verifica permisos y peso de archivos compartidos.")
    d_input = st.text_area("Links de Drive:", height=180)
    if st.button("🛡️ AUDITAR DRIVE"):
        st.session_state.db_drive = pd.DataFrame()
        matches_d = re.findall(r"(https?://drive\.google\.com/[^\s\"\'\)\],]+)", d_input)
        if matches_d:
            st.session_state.db_drive = auditor_drive_api_v24(matches_d)
            st.rerun()
    if not st.session_state.db_drive.empty:
        st.dataframe(st.session_state.db_drive, use_container_width=True, hide_index=True)

# --- MODULO 3: PARTNER IA PRO (CORRECCIÓN DE SUMA INFINITA - ERROR B520A7) ---
elif menu == "🤖 PARTNER IA PRO":
    st.subheader("🤖 IA Partner - Sumador de Cadena de Precisión")
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if prompt := st.chat_input("Pega aquí toda tu cadena de números (ej: 3013+4691+1287...)..."):
        st.session_state.chat_log.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # Lógica de extracción masiva de números (Soluciona el truncamiento de la V21)
            # Buscamos todos los grupos de dígitos ignorando comas y puntos decorativos
            num_strings = re.findall(r'\d+', prompt.replace(',', '').replace('.', ''))
            
            if num_strings:
                try:
                    # Convertimos a entero y sumamos la lista COMPLETA
                    values = [int(n) for n in num_strings]
                    total_suma = sum(values)
                    operacion_vis = " + ".join([f"{v:,}" for v in values])
                    
                    respuesta = f"🔢 **Suma Total de la Cadena:**\n`{operacion_vis}` = **{total_suma:,}**"
                except Exception:
                    respuesta = "Hubo un error procesando los números. Asegúrate de que sean solo dígitos."
            else:
                respuesta = "No detecté una cadena numérica para sumar. ¿Cómo puedo ayudarte, jefe?"
            
            st.markdown(respuesta)
            st.session_state.chat_log.append({"role": "assistant", "content": respuesta})

# --- MODULO 4: SEARCH PRO ---
elif menu == "🛰️ SEARCH PRO":
    st.subheader("🛰️ Search Pro - Indexación de Perfiles")
    st.info("Módulo de rastreo y búsqueda activa de perfiles estratégicos.")
