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
import os
from io import BytesIO

# ==============================================================================
# 1. ESPECIFICACIONES TÉCNICAS Y LLAVES DE ACCESO (CORE)
# ==============================================================================
# API Key de Google Cloud: Esencial para la auditoría de Drive en tiempo real.
# Esta llave permite la comunicación con el endpoint v3 de Google Drive.
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"

# Configuración de la Interfaz de Usuario (UI)
st.set_page_config(
    page_title="BS LATAM ",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "ELITE SUPREMACÍA" (CSS EXPANDIDO)
# ==============================================================================
st.markdown("""
    <style>
    /* Estética General Dark Mode */
    .main { background-color: #0b0d11; color: #e6edf3; }
    .stApp { background-color: #0b0d11; }
    
    /* Título con Identidad Corporativa BS */
    .title-box { 
        border-left: 12px solid #E30613; 
        padding-left: 35px; 
        margin: 30px 0 50px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,13,17,0) 100%);
        border-radius: 0 12px 12px 0;
    }
    .m-title { 
        font-size: 48px; 
        font-weight: 900; 
        color: #ffffff; 
        text-transform: uppercase; 
        letter-spacing: -3px; 
        margin: 0;
    }
    .s-title { 
        font-size: 20px; 
        color: #8b949e; 
        font-family: 'Courier New', monospace; 
        font-weight: bold;
        margin-top: 5px;
    }
    
    /* Tarjetas de Subtotales por Plataforma */
    .subtotal-card {
        background-color: #161b22;
        border: 2px solid #30363d;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .subtotal-card:hover { border-color: #E30613; transform: translateY(-5px); }
    .sub-v { color: #E30613; font-size: 28px; font-weight: 900; }
    .sub-l { color: #8b949e; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }

    /* Estilos de Métricas y Botones */
    [data-testid="stMetric"] { background-color: #161b22; border: 2px solid #30363d; padding: 25px; border-radius: 20px; }
    [data-testid="stMetricValue"] { color: #E30613 !important; font-weight: 900; font-size: 38px !important; }

    .stButton>button { 
        background-color: #E30613 !important; 
        color: #ffffff !important; 
        font-weight: 900 !important; 
        text-transform: uppercase;
        border-radius: 12px;
        height: 70px;
        width: 100%;
        font-size: 20px !important;
        transition: 0.4s;
    }
    .stButton>button:hover { background-color: #ff1a1a !important; box-shadow: 0 10px 35px rgba(227, 6, 19, 0.6); }

    /* Blindaje del Header para evitar pérdida de menú lateral */
    header { visibility: visible !important; background: rgba(11,13,17,0.98) !important; border-bottom: 2px solid #30363d; }
    .stTextArea textarea { background-color: #161b22 !important; color: #e6edf3 !important; border: 2px solid #30363d !important; border-radius: 12px; }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V19</p>
        <p class="s-title">INTELIGENCIA DE DATOS • DESGLOSE MULTI-RED • SUMA INFINITA</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA Y ESTADO (PERSISTENCIA MÁXIMA)
# ==============================================================================
# Inicialización de bases de datos internas para evitar errores de carga.
if 'db_final' not in st.session_state: st.session_state.db_final = pd.DataFrame()
if 'db_fallidos' not in st.session_state: st.session_state.db_fallidos = pd.DataFrame()
if 'db_drive' not in st.session_state: st.session_state.db_drive = pd.DataFrame()
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = [{"role": "assistant", "content": "¡V19 Omni-Titan Desplegada! Todo está bajo control, jefe. 🫡"}]

# ==============================================================================
# 4. MOTORES DE EXTRACCIÓN Y AUDITORÍA (REFORZADOS)
# ==============================================================================

def motor_auditor_universal_v19(urls):
    """Extrae métricas, clasifica redes y enumera resultados con precisión quirúrgica."""
    exitos, fallos = [], []
    p_bar = st.progress(0)
    msg_status = st.empty()
    
    # Opciones de extracción de alto rendimiento
    ydl_opts = {
        'quiet': True, 'no_warnings': True, 'extract_flat': False,
        'skip_download': True, 'ignoreerrors': True, 'socket_timeout': 40,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.tiktok.com/',
        }
    }
    
    for i, raw_u in enumerate(urls):
        url = raw_u.strip().replace('"', '').split('?')[0].rstrip(')').rstrip(',')
        msg_status.markdown(f"📡 **Rastreando Enlace #{i+1}:** `{url[:55]}...`")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                data = ydl.extract_info(url, download=False)
                if data:
                    vistas = int(data.get('view_count') or data.get('play_count') or 0)
                    autor = data.get('uploader') or data.get('creator') or "N/A"
                    duracion = data.get('duration', 0)
                    
                    # Clasificación Lógica de Red Social
                    if "tiktok" in url: plat = "TIKTOK"
                    elif "youtube" in url or "youtu.be" in url: plat = "YOUTUBE"
                    elif "facebook" in url or "fb.watch" in url: plat = "FACEBOOK"
                    elif "instagram" in url: plat = "INSTAGRAM"
                    else: plat = "OTRO"
                    
                    # Tipo de contenido
                    t_cont = "📸 FOTO" if (plat == "TIKTOK" and (duracion is None or duracion <= 0)) else "🎥 VIDEO"
                    
                    exitos.append({
                        "#": i + 1,
                        "Red": plat,
                        "Tipo": t_cont,
                        "Creador": autor,
                        "Vistas": vistas,
                        "Enlace": url
                    })
                else:
                    fallos.append({"Link": url, "Error": "Contenido Privado/No Disponible"})
        except Exception as e:
            fallos.append({"Link": url, "Error": f"Fallo de Red: {str(e)[:20]}"})
        
        p_bar.progress((i + 1) / len(urls))
    
    msg_status.empty()
    p_bar.empty()
    return pd.DataFrame(exitos), pd.DataFrame(fallos)

def inspector_drive_deep_v19(urls):
    """Valida integridad de archivos en Google Drive mediante API Key."""
    resultados_d = []
    for l in urls:
        f_id_match = re.search(r'[-\w]{25,}', l)
        if f_id_match:
            f_id = f_id_match.group()
            endpoint = f"https://www.googleapis.com/drive/v3/files/{f_id}?fields=name,size,mimeType&key={DRIVE_API_KEY}"
            try:
                resp = requests.get(endpoint, timeout=25)
                meta = resp.json()
                if "error" not in meta:
                    peso_mb = f"{int(meta.get('size', 0))/1024/1024:.2f} MB" if meta.get('size') else "N/A"
                    resultados_d.append({"Archivo": meta.get('name'), "Peso": peso_mb, "Estado": "✅ PÚBLICO", "Link": l})
                else:
                    resultados_d.append({"Archivo": "🔒 PRIVADO", "Peso": "0", "Estado": "❌ BLOQUEADO", "Link": l})
            except:
                resultados_d.append({"Archivo": "ERROR", "Peso": "0", "Estado": "❌ ROTO", "Link": l})
    return pd.DataFrame(resultados_d)

# ==============================================================================
# 5. NAVEGACIÓN Y PANEL LATERAL
# ==============================================================================
with st.sidebar:
    st.markdown("<h1 style='color:#E30613; text-align:center;'>BS TITAN V19</h1>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("MÓDULOS DEL SISTEMA", ["🚀 EXTRACTOR DE VISTAS", "📂 DRIVE AUDITOR", "🤖 PARTNER IA PRO", "🛰️ SEARCH PRO"], label_visibility="collapsed")
    st.divider()
    if st.button("🚨 REINICIAR BASES DE DATOS"):
        for k in ['db_final', 'db_fallidos', 'db_drive']: st.session_state[k] = pd.DataFrame()
        st.session_state.chat_log = [{"role": "assistant", "content": "Sistema reiniciado. 🫡"}]
        st.rerun()

# ==============================================================================
# 6. DESPLIEGUE DE MÓDULOS (FUNCIONALIDAD COMPLETA)
# ==============================================================================

# --- MODULO 1: EXTRACTOR PRO (ENUMERACIÓN + SUB-TOTALES) ---
if menu == "🚀 EXTRACTOR DE VISTAS":
    st.markdown("### 📥 Panel de Entrada Estratégica")
    raw_input = st.text_area("Pega los enlaces de los embajadores aquí:", height=200, placeholder="TikTok, YT, FB, IG...")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔥 EJECUTAR AUDITORÍA"):
            links_f = re.findall(r"(https?://[^\s\"\'\)\],]+)", raw_input)
            if links_f:
                # LIMPIEZA AUTOMÁTICA DE RESULTADOS PASADOS
                st.session_state.db_final = pd.DataFrame()
                st.session_state.db_fallidos = pd.DataFrame()
                
                with st.spinner("Conectando con servidores..."):
                    df_ok, df_err = motor_auditor_universal_v19(links_f)
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
            st.markdown("**📋 Suma para Hoja de Cálculo (General):**")
            v_list = [str(v) for v in df['Vistas'].tolist()]
            st.code(" + ".join(v_list), language="text")
        
        # --- SECCIÓN DE DESGLOSE POR RED (PEDIDO DEL JEFE) ---
        st.markdown("### 📊 Desglose Detallado por Red Social")
        d1, d2, d3 = st.columns(3)
        
        for platform, col_disp in zip(["TIKTOK", "YOUTUBE", "FACEBOOK"], [d1, d2, d3]):
            sub_df = df[df['Red'] == platform]
            sub_vistas = sub_df['Vistas'].sum()
            sub_cantidad = len(sub_df)
            
            with col_disp:
                st.markdown(f"""
                <div class="subtotal-card">
                    <div class="sub-l">{platform} ({sub_cantidad} ITEMS)</div>
                    <div class="sub-v">{sub_vistas:,}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if sub_vistas > 0:
                    st.caption(f"Copiado rápido {platform}:")
                    sub_v_list = [str(v) for v in sub_df['Vistas'].tolist()]
                    st.code(" + ".join(sub_v_list), language="text")

        # Tabla Principal Enumerada
        st.markdown("### 📝 Listado Completo de Auditoría")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Excel
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
            df_d_res = inspector_drive_deep_v19(matches_d)
            st.session_state.db_drive = df_d_res
            st.rerun()
    if not st.session_state.db_drive.empty:
        st.dataframe(st.session_state.db_drive, use_container_width=True, hide_index=True)

# --- MODULO 3: PARTNER IA PRO (SUMA INFINITA) ---
elif menu == "🤖 PARTNER IA PRO":
    st.subheader("🤖 Partner IA + Calculadora de Cadena")
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if chat_p := st.chat_input("Pega tu suma o consulta algo..."):
        st.session_state.chat_log.append({"role": "user", "content": chat_p})
        with st.chat_message("user"): st.markdown(chat_p)
        
        with st.chat_message("assistant"):
            clean_txt = chat_p.replace(' ', '').replace(',', '')
            # Regex para capturar toda la tira matemática
            math_match = re.search(r"([\d\+\-\*\/\.]+)", clean_txt)
            if math_match:
                try:
                    operacion = math_match.group(1)
                    resultado = eval(operacion)
                    final_ans = f"🔢 **Total Calculado:** {resultado:,}\n`Detalle: {operacion}`"
                except: final_ans = "Error en operación."
            else:
                final_ans = "Sistema V19 operando al 100%. Limpieza y sumador de red activos."
            
            st.markdown(final_ans)
            st.session_state.chat_log.append({"role": "assistant", "content": final_ans})

# --- MODULO 4: SEARCH PRO ---
elif menu == "🛰️ SEARCH PRO":
    st.subheader("🛰️ Search Pro")
    st.info("Módulo de rastreo de perfiles activo. Listo para indexación.")
