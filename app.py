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
    page_title="AUDIT-ELITE PRO V29 - OMNI TITAN EXPANDED",
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
    """
    Motor de extracción profunda. Mantiene la lógica de limpieza de parámetros
    y conteo de vistas original.
    """
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
        # Limpieza de URL para evitar errores por comas o paréntesis
        url = raw_u.strip().replace('"', '').split('?')[0].rstrip(')').rstrip(',')
        msg_status.markdown(f"📡 **Rastreando Objetivo:** `{url[:50]}...`")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    vistas = int(info.get('view_count') or info.get('play_count') or 0)
                    autor = info.get('uploader') or info.get('creator') or info.get('uploader_id') or "N/A"
                    
                    # Clasificación por Red
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
    """Auditor de archivos Google Drive mediante API v3."""
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
# 6. DESPLIEGUE DE MÓDULOS (LÓGICA EXPANDIDA)
# ==============================================================================

# --- MÓDULO 1: EXTRACTOR PRO (LÓGICA ORIGINAL SIN RECORTES) ---
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
        
        # Métrica Principal
        st.metric("📊 VISTAS ACUMULADAS TOTALES", f"{df['Vistas'].sum():,}")
        
        # Bloque de Suma para Copiado Rápido
        st.markdown("**📋 Suma para Excel / Reportes (Copiado Masivo):**")
        st.code(" + ".join([str(v) for v in df['Vistas'].tolist()]))
        
        # Desglose por Redes con Tarjetas CSS
        st.markdown("### 📊 Desglose por Plataforma")
        d_col1, d_col2, d_col3 = st.columns(3)
        platforms = [("TIKTOK", d_col1), ("YOUTUBE", d_col2), ("FACEBOOK", d_col3)]
        
        for p_name, p_col in platforms:
            sub_data = df[df['Red'] == p_name]
            v_total = sub_data['Vistas'].sum()
            with p_col:
                st.markdown(f"""
                <div class="subtotal-card">
                    <div class="sub-l">{p_name}</div>
                    <div class="sub-v">{v_total:,}</div>
                </div>
                """, unsafe_allow_html=True)
                if v_total > 0:
                    st.code(" + ".join([str(v) for v in sub_data['Vistas'].tolist()]))

        st.markdown("### 📝 Detalle Individual de Enlaces")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Sección de Errores/Fallidos
        if not st.session_state.db_fallidos.empty:
            st.markdown("---")
            st.warning("⚠️ ENLACES CON ERRORES (REVISAR MANUALMENTE):")
            st.dataframe(st.session_state.db_fallidos, use_container_width=True)

# --- MÓDULO 2: TIKTOK RADAR (LO NUEVO - EXPANDIDO) ---
elif menu == "🎯 TIKTOK RADAR":
    st.markdown("### 🎯 TikTok Radar - Inteligencia de Búsqueda")
    st.info("Configura filtros de búsqueda para contenido popular y forzado en español.")
    
    col_radar1, col_radar2 = st.columns(2)
    with col_radar1:
        query_text = st.text_input("🔍 Término de Búsqueda (Nicho/Marca):", placeholder="Ej: Gaming, Tech Review...")
    with col_radar2:
        hashtag_text = st.text_input("#️⃣ Filtrar por Hashtag:", placeholder="Ej: #mexico, #unboxing...")
    
    r_c1, r_c2, r_c3 = st.columns(3)
    with r_c1:
        filtro_fecha = st.selectbox("📅 Fecha del Video:", ["Hoy", "Esta Semana", "Este Mes", "Siempre"])
    with r_c2:
        filtro_orden = st.selectbox("📊 Priorizar por:", ["Más Relevante", "Más Populares (Likes)"])
    with r_c3:
        forzar_esp = st.toggle("Forzar Contenido Español 🇪🇸", value=True)

    if st.button("🚀 ACTIVAR RADAR Y BUSCAR"):
        if query_text or hashtag_text:
            # Lógica de construcción de búsqueda avanzada
            final_query = query_text
            if hashtag_text:
                tag = hashtag_text if hashtag_text.startswith('#') else f"#{hashtag_text}"
                final_query += f" {tag}"
            
            # Padding de idioma español (Truco de SEO para TikTok)
            if forzar_esp:
                final_query += " (de OR el OR en OR la)"
            
            encoded_search = urllib.parse.quote(final_query)
            tiktok_search_url = f"https://www.tiktok.com/search/video?q={encoded_search}"
            
            st.success(f"🎯 Radar apuntado a: {query_text} {hashtag_text if hashtag_text else ''}")
            st.link_button("🔥 ABRIR TIKTOK CON FILTROS APLICADOS", tiktok_search_url)
            
            st.markdown("""
                ---
                **PROTOCOLO SUGERIDO:**
                1. Navega por los resultados y selecciona los videos con más engagement.
                2. Copia los enlaces de los videos.
                3. Regresa al módulo **🚀 EXTRACTOR** para procesar los datos finales.
            """)
        else:
            st.error("Jefe, escribe algo en el buscador o el hashtag.")

# --- MÓDULO 3: DRIVE AUDITOR (IDÉNTICO A ORIGINAL) ---
elif menu == "📂 DRIVE AUDITOR":
    st.markdown("### 📂 Auditoría de Enlaces Google Drive")
    drive_input = st.text_area("Pega los enlaces de carpetas o archivos de Drive:", height=200)
    
    if st.button("🛡️ VERIFICAR ACCESO"):
        links_d = re.findall(r"(https?://drive\.google\.com/[^\s]+)", drive_input)
        if links_d:
            st.session_state.db_drive = auditor_drive_api_v24(links_d)
            st.rerun()
            
    if not st.session_state.db_drive.empty:
        st.markdown("### Resultados del Escaneo")
        st.dataframe(st.session_state.db_drive, use_container_width=True, hide_index=True)

# --- MÓDULO 4: PARTNER IA (IDÉNTICO A ORIGINAL) ---
elif menu == "🤖 PARTNER IA":
    st.markdown("### 🤖 IA Partner - Asistente de Cálculos")
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if chat_input := st.chat_input("Pega una lista de números o pide un cálculo..."):
        st.session_state.chat_log.append({"role": "user", "content": chat_input})
        with st.chat_message("user"): st.markdown(chat_input)
        
        with st.chat_message("assistant"):
            # Lógica de suma de cadena numérica
            numeros = re.findall(r'\d+', chat_input.replace(',', '').replace('.', ''))
            if numeros:
                valores = [int(n) for n in numeros]
                total_suma = sum(valores)
                respuesta = f"🔢 La suma de la cadena es: **{total_suma: ,}**"
                st.markdown(respuesta)
                st.session_state.chat_log.append({"role": "assistant", "content": respuesta})
            else:
                resp_error = "No encontré números para sumar en tu mensaje, jefe."
                st.markdown(resp_error)
                st.session_state.chat_log.append({"role": "assistant", "content": resp_error})

# --- MÓDULO 5: SEARCH PRO (MANTENIDO) ---
elif menu == "🛰️ SEARCH PRO":
    st.markdown("### 🛰️ Search Pro - Rastreador de Perfiles")
    st.info("Localiza perfiles específicos usando Dorks de Google.")
    target_name = st.text_input("Nombre de Creador, Usuario o Marca:")
    if st.button("🛰️ LANZAR RASTREO"):
        if target_name:
            dork_url = f"https://www.google.com/search?q=site:tiktok.com+%22{target_name}%22"
            st.link_button(f"Abrir búsqueda para {target_name}", dork_url)
