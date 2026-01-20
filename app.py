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
from io import BytesIO

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL Y LLAVES DE ACCESO (PROTEGIDAS)
# ==============================================================================
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"

st.set_page_config(
    page_title="BS LATAM",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "ELITE SUPREMACÍA" (ESTILO BS LATAM COMPLETO)
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
    
    /* BLOQUE DE TÍTULO PRINCIPAL EXPANDIDO */
    .title-box { 
        border-left: 15px solid #E30613; 
        padding: 40px 60px; 
        margin: 30px 0 60px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,13,17,0) 100%);
        border-radius: 0 30px 30px 0;
        box-shadow: 15px 0 40px rgba(0,0,0,0.6);
    }
    .m-title { 
        font-size: 52px; 
        font-weight: 900; 
        color: #ffffff; 
        text-transform: uppercase; 
        letter-spacing: 8px; 
        margin: 0; 
        line-height: 1.0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.9);
    }
    .s-title { 
        font-size: 22px; 
        color: #8b949e; 
        font-family: 'Courier New', monospace; 
        margin-top: 20px; 
        letter-spacing: 3px;
        font-weight: bold;
    }

    /* ESTILO BS LATAM SIDEBAR - MÁXIMA VISIBILIDAD */
    .bs-latam-sidebar {
        color: #ffffff; 
        font-weight: 950; 
        font-size: 36px; 
        text-align: center;
        text-transform: uppercase; 
        letter-spacing: 5px;
        text-shadow: 0px 0px 20px #0055ff, 2px 2px 0px #000000;
        margin-bottom: 35px; 
        padding: 15px;
        border-bottom: 2px solid #30363d;
    }
    
    /* TARJETAS DE MÉTRICAS INDIVIDUALES */
    .subtotal-card {
        background-color: #161b22; 
        border: 2px solid #30363d; 
        padding: 30px;
        border-radius: 25px; 
        text-align: center; 
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    .subtotal-card:hover {
        transform: translateY(-5px);
        border-color: #E30613;
    }
    .sub-v { 
        color: #E30613; 
        font-size: 38px; 
        font-weight: 950; 
        text-shadow: 0 0 15px rgba(227,6,19,0.4);
    }
    .sub-l { 
        color: #8b949e; 
        font-size: 16px; 
        text-transform: uppercase; 
        font-weight: bold;
        letter-spacing: 2px;
    }

    /* ESTILOS DE COMPONENTES STREAMLIT */
    [data-testid="stMetric"] { 
        background-color: #161b22; 
        border: 2px solid #30363d; 
        padding: 40px; 
        border-radius: 28px; 
    }
    [data-testid="stMetricValue"] { 
        color: #E30613 !important; 
        font-weight: 900; 
        font-size: 48px !important; 
    }

    .stButton>button { 
        background: linear-gradient(135deg, #E30613 0%, #9e040d 100%) !important;
        color: #ffffff !important; 
        font-weight: 900 !important; 
        text-transform: uppercase;
        border-radius: 20px; 
        height: 85px; 
        width: 100%; 
        font-size: 24px !important;
        border: none;
        box-shadow: 0 10px 20px rgba(227,6,19,0.2);
    }
    
    .stTextArea textarea { 
        background-color: #161b22 !important; 
        color: #e6edf3 !important; 
        border: 2px solid #30363d !important; 
        border-radius: 20px;
        font-size: 16px;
    }
    
    /* BLOQUES DE CÓDIGO (COPIADO RÁPIDO Y MASIVO) */
    code { 
        font-size: 15px !important; 
        color: #ffffff !important; 
        background-color: #161b22 !important; 
        border: 1px solid #444c56 !important;
        padding: 18px !important; 
        border-radius: 12px; 
        display: block;
        margin: 10px 0;
    }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V29</p>
        <p class="s-title">SISTEMA INTEGRAL DE AUDITORÍA Y RASTREO • BS LATAM PRO</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA Y PERSISTENCIA (SISTEMA DE DATOS)
# ==============================================================================
if 'db_final' not in st.session_state:
    st.session_state.db_final = pd.DataFrame()
if 'db_fallidos' not in st.session_state:
    st.session_state.db_fallidos = pd.DataFrame()
if 'db_drive' not in st.session_state:
    st.session_state.db_drive = pd.DataFrame()
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = [{"role": "assistant", "content": "¡V29 Activa, jefe! Radar de TikTok desplegado y Extractor listo. 🫡"}]

# ==============================================================================
# 4. MOTORES DE AUDITORÍA (EXTRACTOR ORIGINAL V24 REFORZADO)
# ==============================================================================
def motor_auditor_universal_v24(urls):
    exitos, fallos = [], []
    p_bar = st.progress(0)
    msg_status = st.empty()
    
    ydl_opts = {
        'quiet': True, 
        'no_warnings': True, 
        'extract_flat': False,
        'skip_download': True, 
        'ignoreerrors': True, 
        'socket_timeout': 40,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
    }
    
    for i, raw_u in enumerate(urls):
        url = raw_u.strip().replace('"', '').split('?')[0].rstrip(')').rstrip(',')
        msg_status.markdown(f"📡 **Rastreando Objetivo:** `{url[:50]}...`")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    vistas = int(info.get('view_count') or info.get('play_count') or 0)
                    autor = info.get('uploader') or info.get('creator') or info.get('uploader_id') or "N/A"
                    
                    if "tiktok" in url: plat = "TIKTOK"
                    elif "youtube" in url or "youtu.be" in url: plat = "YOUTUBE"
                    elif "facebook" in url or "fb.watch" in url: plat = "FACEBOOK"
                    elif "instagram" in url: plat = "INSTAGRAM"
                    else: plat = "OTRA RED"
                    
                    exitos.append({
                        "#": i + 1,
                        "Red": plat,
                        "Creador": autor, 
                        "Vistas": vistas,
                        "Link Original": url
                    })
                else:
                    fallos.append({"Link": url, "Motivo": "Privado/Eliminado o Inaccesible"})
        except Exception as e:
            fallos.append({"Link": url, "Motivo": f"Error Técnico: {str(e)[:30]}"})
        
        p_bar.progress((i + 1) / len(urls))
    
    msg_status.empty()
    p_bar.empty()
    return pd.DataFrame(exitos), pd.DataFrame(fallos)

def auditor_drive_api_v24(urls):
    resultados_d = []
    for link in urls:
        f_id_match = re.search(r'[-\w]{25,}', link)
        if f_id_match:
            f_id = f_id_match.group()
            endpoint = f"https://www.googleapis.com/drive/v3/files/{f_id}?fields=name,size&key={DRIVE_API_KEY}"
            try:
                resp = requests.get(endpoint, timeout=20).json()
                if "error" not in resp:
                    peso_mb = f"{int(resp.get('size', 0))/1024/1024:.2f} MB" if resp.get('size') else "N/A"
                    resultados_d.append({
                        "Archivo": resp.get('name'), 
                        "Peso": peso_mb, 
                        "Estado": "✅ DISPONIBLE", 
                        "Link": link
                    })
                else:
                    resultados_d.append({"Archivo": "🔒 PROTEGIDO", "Peso": "0", "Estado": "❌ BLOQUEADO", "Link": link})
            except:
                resultados_d.append({"Archivo": "ERROR", "Peso": "0", "Estado": "❌ ROTO", "Link": link})
    return pd.DataFrame(resultados_d)

# ==============================================================================
# 5. PANEL DE NAVEGACIÓN Y CONTROL (SIDEBAR)
# ==============================================================================
with st.sidebar:
    st.markdown('<p class="bs-latam-sidebar">BS LATAM</p>', unsafe_allow_html=True)
    st.divider()
    
    menu = st.radio(
        "MÓDULOS OPERATIVOS", 
        ["🚀 EXTRACTOR", "🎯 TIKTOK RADAR", "📂 DRIVE AUDITOR", "🤖 PARTNER IA", "🛰️ SEARCH PRO"],
        index=0
    )
    
    st.divider()
    st.markdown("### ⚙️ Centro de Control")
    if st.button("🚨 REINICIAR SISTEMA COMPLETO"):
        for k in ['db_final', 'db_fallidos', 'db_drive']:
            st.session_state[k] = pd.DataFrame()
        st.session_state.chat_log = [{"role": "assistant", "content": "Memoria purgada. Sistema listo para nueva misión. 🫡"}]
        st.rerun()

# ==============================================================================
# 6. DESPLIEGUE DE MÓDULOS (LÓGICA AMPLIADA)
# ==============================================================================

if menu == "🚀 EXTRACTOR":
    st.markdown("### 📥 Entrada de Enlaces para Auditoría")
    raw_input = st.text_area("Pega tus links masivos aquí (TikTok, YT, IG, FB):", height=220)
    
    col_acc1, col_acc2 = st.columns(2)
    with col_acc1:
        if st.button("🔥 INICIAR EXTRACCIÓN DE VISTAS"):
            links_f = re.findall(r"(https?://[^\s\"\'\)\],]+)", raw_input)
            if links_f:
                st.session_state.db_final, st.session_state.db_fallidos = motor_auditor_universal_v24(links_f)
                st.rerun()
    with col_acc2:
        if st.button("🧹 LIMPIAR RESULTADOS"):
            st.session_state.db_final = pd.DataFrame()
            st.session_state.db_fallidos = pd.DataFrame()
            st.rerun()

    if not st.session_state.db_final.empty:
        df = st.session_state.db_final
        st.divider()
        st.metric("📊 VISTAS ACUMULADAS TOTALES", f"{df['Vistas'].sum():,}")
        st.markdown("**📋 Suma para Excel / Reportes (Copiado Masivo):**")
        st.code(" + ".join([str(v) for v in df['Vistas'].tolist()]))
        
        st.markdown("### 📊 Desglose por Plataforma")
        d_col1, d_col2, d_col3 = st.columns(3)
        platforms = [("TIKTOK", d_col1), ("YOUTUBE", d_col2), ("FACEBOOK", d_col3)]
        for p_name, p_col in platforms:
            sub_data = df[df['Red'] == p_name]
            v_total = sub_data['Vistas'].sum()
            with p_col:
                st.markdown(f'<div class="subtotal-card"><div class="sub-l">{p_name}</div><div class="sub-v">{v_total:,}</div></div>', unsafe_allow_html=True)
                if v_total > 0: st.code(" + ".join([str(v) for v in sub_data['Vistas'].tolist()]))

        st.markdown("### 📝 Detalle Individual de Enlaces")
        st.dataframe(df, use_container_width=True, hide_index=True)
        if not st.session_state.db_fallidos.empty:
            st.warning("⚠️ ENLACES CON ERRORES:")
            st.dataframe(st.session_state.db_fallidos, use_container_width=True)

elif menu == "🎯 TIKTOK RADAR":
    st.markdown("### 🎯 TikTok Radar - Protocolo de Rastreo")
    st.info("Para evitar el bloqueo de TikTok, sigue estos pasos: 1. Abre el buscador. 2. Copia todo (Ctrl+A y Ctrl+C). 3. Pega abajo.")
    
    col_radar1, col_radar2 = st.columns(2)
    with col_radar1:
        query_text = st.text_input("🔍 Término de Búsqueda:", placeholder="Ej: Blood Strike")
    with col_radar2:
        forzar_esp = st.toggle("Forzar Contenido Español es", value=True)

    if st.button("🔥 ABRIR BUSCADOR"):
        if query_text:
            final_q = query_text + (" (de OR el OR en OR la)" if forzar_esp else "")
            st.link_button("IR A TIKTOK", f"https://www.tiktok.com/search/video?q={urllib.parse.quote(final_q)}")

    st.divider()
    raw_data = st.text_area("Zona de Pegado de Datos (Ctrl+V):", height=450, placeholder="Pega aquí todo lo copiado de la página de TikTok...")
    
    if st.button("🚀 FILTRAR Y PROCESAR RADAR"):
        links_radar = re.findall(r"(https?://www\.tiktok\.com/@[^/\s]+/video/\d+)", raw_data)
        if links_radar:
            st.session_state.db_final, _ = motor_auditor_universal_v24(list(set(links_radar)))
            st.success(f"Se detectaron {len(links_radar)} videos únicos.")
            st.rerun()

elif menu == "📂 DRIVE AUDITOR":
    st.markdown("### 📂 Auditoría de Enlaces Google Drive")
    drive_input = st.text_area("Pega los enlaces de carpetas o archivos de Drive:", height=200)
    if st.button("🛡️ VERIFICAR ACCESO"):
        links_d = re.findall(r"(https?://drive\.google\.com/[^\s]+)", drive_input)
        if links_d:
            st.session_state.db_drive = auditor_drive_api_v24(links_d)
            st.rerun()
    if not st.session_state.db_drive.empty:
        st.dataframe(st.session_state.db_drive, use_container_width=True, hide_index=True)

elif menu == "🤖 PARTNER IA":
    st.markdown("### 🤖 IA Partner - Asistente de Cálculos")
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if chat_input := st.chat_input("Pega una lista de números..."):
        st.session_state.chat_log.append({"role": "user", "content": chat_input})
        with st.chat_message("user"): st.markdown(chat_input)
        with st.chat_message("assistant"):
            numeros = re.findall(r'\d+', chat_input.replace(',', '').replace('.', ''))
            total = sum([int(n) for n in numeros]) if numeros else 0
            res = f"🔢 Suma: **{total: ,}**" if numeros else "No hay números, jefe."
            st.markdown(res)
            st.session_state.chat_log.append({"role": "assistant", "content": res})

elif menu == "🛰️ SEARCH PRO":
    st.markdown("### 🛰️ Rastreador de Virales por Perfil (Elite +60k)")
    st.info("Localiza videos virales de un creador específico usando dorks temporales.")
    
    target_user = st.text_input("👤 Usuario o Perfil del Creador (Ej: @nombre):", placeholder="@usuario")
    vistas_min = st.number_input("🔥 Umbral de Vistas (Elite):", value=60000, step=10000)
    
    st.divider()
    st.markdown("#### 📅 Configuración de Rango de Fechas")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fecha_inicio = st.date_input("Desde:", value=datetime.date.today() - datetime.timedelta(days=30))
    with col_f2:
        fecha_fin = st.date_input("Hasta:", value=datetime.date.today())

    if st.button("🔍 GENERAR BÚSQUEDA PERSONALIZADA"):
        if target_user:
            clean_user = target_user.replace("@", "")
            # Formato de fecha para Google (YYYY-MM-DD)
            f_start = fecha_inicio.strftime("%Y-%m-%d")
            f_end = fecha_fin.strftime("%Y-%m-%d")
            
            # Construcción del Dork con rango de fechas
            dork = f"site:tiktok.com/@{clean_user} after:{f_start} before:{f_end}"
            url_google = f"https://www.google.com/search?q={urllib.parse.quote(dork)}"
            
            st.success(f"Búsqueda lista para {target_user} entre {f_start} y {f_end}")
            st.link_button("🚀 EJECUTAR BÚSQUEDA EN GOOGLE", url_google)
        else:
            st.error("Por favor, ingresa un usuario primero.")

    st.divider()
    
    # Segmentación automática de virales +60k (del extractor actual)
    if not st.session_state.db_final.empty:
        # Filtramos solo lo que cumple el umbral
        df_elite = st.session_state.db_final[st.session_state.db_final['Vistas'] >= vistas_min]
        
        if not df_elite.empty:
            st.markdown(f"### 🏆 Rendimiento Elite (+{vistas_min//1000}k)")
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown(f"""
                <div class="subtotal-card">
                    <div class="sub-l">SUMA VISTAS ELITE</div>
                    <div class="sub-v">{df_elite['Vistas'].sum():,}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_m2:
                st.markdown(f"""
                <div class="subtotal-card">
                    <div class="sub-l">VIDEOS DETECTADOS</div>
                    <div class="sub-v">{len(df_elite)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("**📋 Cadena de suma para Excel (Solo Elite):**")
            st.code(" + ".join([str(v) for v in df_elite['Vistas'].tolist()]))
            st.dataframe(df_elite, use_container_width=True, hide_index=True)
        else:
            st.warning(f"No se detectaron videos con más de {vistas_min:,} vistas para este creador.")
    else:
        st.warning("Primero procesa los enlaces en el Extractor para ver el análisis de virales aquí.")
