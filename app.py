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
import random
import traceback
import urllib.parse
from io import BytesIO
from googleapiclient.discovery import build
import isodate

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL DE ALTO NIVEL
# ==============================================================================
# Llave maestra para Drive y YouTube (Asegurar que tenga permisos Data API v3)
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"
YT_API_KEY = DRIVE_API_KEY 

st.set_page_config(
    page_title="BS LATAM - AUDIT ELITE SUPREMACÍA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "ELITE SUPREMACÍA" (CSS INDUSTRIAL DARK)
# ==============================================================================
st.markdown("""
    <style>
    /* Fondo y tipografía base */
    .main { 
        background-color: #0b0d11; 
        color: #e6edf3; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    }
    .stApp { background-color: #0b0d11; }
    
    /* Bloque de Título Principal Estilo Militar */
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

    /* Sidebar Customization */
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
    
    /* Metricas y Tablas */
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

    /* Botones de Acción Crítica */
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
    
    /* Campos de Texto */
    .stTextArea textarea { 
        background-color: #161b22 !important; 
        color: #e6edf3 !important; 
        border: 2px solid #30363d !important; 
        border-radius: 20px;
        font-size: 16px;
    }
    
    /* Bloques de Código de Resultados */
    code { 
        font-size: 16px !important; 
        color: #ffffff !important; 
        background-color: #161b22 !important; 
        border: 1px solid #E30613 !important;
        padding: 20px !important; 
        border-radius: 12px; 
        display: block;
        margin: 10px 0;
    }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V29.9</p>
        <p class="s-title">SISTEMA INTEGRAL DE AUDITORÍA Y RASTREO • BS LATAM PRO</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. PERSISTENCIA DE DATOS Y ESTADOS DE SESIÓN
# ==============================================================================
if 'db_final' not in st.session_state:
    st.session_state.db_final = pd.DataFrame()
if 'db_fallidos' not in st.session_state:
    st.session_state.db_fallidos = []
if 'db_drive' not in st.session_state:
    st.session_state.db_drive = pd.DataFrame()
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = [{"role": "assistant", "content": "Sistema V29.9 en línea. Esperando directrices del comando. 🫡"}]

# ==============================================================================
# 4. MOTOR DE EXTRACCIÓN HÍBRIDO (API GOOGLE + SCRAPING AVANZADO)
# ==============================================================================

def get_yt_data_api_v3(url, api_key):
    """Extracción vía API Oficial para evitar bloqueos de IP y errores de 0 vistas."""
    try:
        video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if not video_id_match:
            return None
        video_id = video_id_match.group(1)
        
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=video_id
        )
        response = request.execute()
        
        if not response['items']:
            return None
            
        item = response['items'][0]
        # Cálculo de tipo de video por duración
        dur_iso = item['contentDetails']['duration']
        segundos = isodate.parse_duration(dur_iso).total_seconds()
        tipo_video = "Short" if ("/shorts/" in url.lower() or segundos <= 61) else "Video Largo"
        
        return {
            "Fecha": datetime.datetime.now().strftime('%Y-%m-%d'),
            "Red": "YOUTUBE",
            "Tipo": tipo_video,
            "Creador": item['snippet']['channelTitle'],
            "Vistas": int(item['statistics'].get('viewCount', 0)),
            "Likes": int(item['statistics'].get('likeCount', 0)),
            "Comments": int(item['statistics'].get('commentCount', 0)),
            "Saves": 0,
            "Link Original": url
        }
    except Exception as e:
        return None

def get_social_data_scrapper(url, plataforma_id):
    """Extracción vía Scrapping Reforzado para TikTok, Facebook e Instagram."""
    # Limpieza de URL específica para evitar parámetros de rastreo
    if "facebook.com" in url or "fb.watch" in url:
        url = url.split('?')[0]
        
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'skip_download': True,
        'ignoreerrors': True,
        'socket_timeout': 30,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    
    # Carga de cookies si existen para Facebook/Instagram
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Delay aleatorio para evitar detección de bots
            time.sleep(random.uniform(2.0, 4.5))
            info = ydl.extract_info(url, download=False)
            
            if not info:
                return None
                
            vistas = info.get('view_count') or info.get('play_count') or 0
            likes = info.get('like_count') or 0
            
            return {
                "Fecha": datetime.datetime.now().strftime('%Y-%m-%d'),
                "Red": plataforma_id.upper(),
                "Tipo": "Video/Reel",
                "Creador": info.get('uploader') or info.get('title', 'N/A'),
                "Vistas": int(vistas),
                "Likes": int(likes),
                "Comments": int(info.get('comment_count') or 0),
                "Saves": int(info.get('repost_count') or 0),
                "Link Original": url
            }
        except Exception:
            return None

def motor_auditor_completo(urls, red_default):
    """Orquestador que decide qué motor usar para cada link."""
    exitos = []
    fallos = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for index, url in enumerate(urls):
        url = url.strip().replace('"', '').split('?')[0].rstrip(')').rstrip(',')
        status_text.markdown(f"📡 **AUDITANDO OBJETIVO [{index+1}/{len(urls)}]:** `{url[:50]}...`")
        
        data = None
        # Priorizar API para YouTube para evitar el error de 0 vistas
        if "youtube.com" in url or "youtu.be" in url:
            data = get_yt_data_api_v3(url, YT_API_KEY)
        else:
            data = get_social_data_scrapper(url, red_default)
            
        if data and data["Vistas"] >= 0:
            exitos.append(data)
        else:
            fallos.append(url)
            
        progress_bar.progress((index + 1) / len(urls))
        
    status_text.empty()
    progress_bar.empty()
    return pd.DataFrame(exitos), fallos

# ==============================================================================
# 5. GESTIÓN DE GOOGLE DRIVE (AUDITORÍA DE ACCESOS)
# ==============================================================================
def auditor_drive_api_v24(urls):
    resultados_d = []
    for link in urls:
        f_id_match = re.search(r'[-\w]{25,}', link)
        if f_id_match:
            f_id = f_id_match.group()
            endpoint = f"https://www.googleapis.com/drive/v3/files/{f_id}?fields=name,size,mimeType&key={DRIVE_API_KEY}"
            try:
                resp = requests.get(endpoint, timeout=20).json()
                if "error" not in resp:
                    size = int(resp.get('size', 0))
                    peso_mb = f"{size/1024/1024:.2f} MB" if size > 0 else "N/A"
                    resultados_d.append({
                        "Archivo": resp.get('name'), 
                        "Peso": peso_mb, 
                        "Estado": "✅ DISPONIBLE", 
                        "Link": link
                    })
                else:
                    resultados_d.append({"Archivo": "🔒 PROTEGIDO", "Peso": "0", "Estado": "❌ BLOQUEADO", "Link": link})
            except Exception:
                resultados_d.append({"Archivo": "ERROR", "Peso": "0", "Estado": "❌ ROTO", "Link": link})
    return pd.DataFrame(resultados_d)

# ==============================================================================
# 6. SIDEBAR Y NAVEGACIÓN
# ==============================================================================
with st.sidebar:
    st.markdown('<p class="bs-latam-sidebar">BS LATAM</p>', unsafe_allow_html=True)
    st.divider()
    menu_op = st.radio(
        "MÓDULOS DE OPERACIÓN", 
        ["🚀 EXTRACTOR", "🎯 TIKTOK RADAR", "📂 DRIVE AUDITOR", "🤖 PARTNER IA", "🛰️ SEARCH PRO"],
        index=0
    )
    st.divider()
    red_global = st.selectbox("Forzar Plataforma (No-YT):", ["TikTok", "Facebook", "Instagram"])
    
    if st.button("🚨 REINICIAR SISTEMA"):
        st.session_state.db_final = pd.DataFrame()
        st.session_state.db_fallidos = []
        st.session_state.db_drive = pd.DataFrame()
        st.rerun()

# ==============================================================================
# 7. MÓDULOS DE INTERFAZ (LOGICA DE NEGOCIO)
# ==============================================================================

# --- MÓDULO 1: EXTRACTOR ---
if menu_op == "🚀 EXTRACTOR":
    st.markdown("### 📥 Entrada de Enlaces para Auditoría Masiva")
    input_text = st.text_area("Pega tus links (uno por línea o bloque de texto):", height=250)
    
    col_btn1, col_btn2 = st.columns([2,1])
    with col_btn1:
        if st.button("🔥 INICIAR EXTRACCIÓN DE ALTO IMPACTO"):
            links_limpios = re.findall(r"(https?://[^\s\"\'\)\],]+)", input_text)
            if links_limpios:
                st.session_state.db_final, st.session_state.db_fallidos = motor_auditor_completo(links_limpios, red_global)
                st.rerun()
    
    if not st.session_state.db_final.empty:
        df_res = st.session_state.db_final
        
        st.divider()
        st.subheader("📊 Panel de Métricas Acumuladas")
        
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric("🌍 VISTAS TOTALES", f"{int(df_res['Vistas'].sum()):,}")
            st.write("📋 **CADENA DE SUMA PARA COPIADO (+):**")
            cadena_vistas = [str(int(v)) for v in df_res['Vistas'].tolist()]
            st.code("+".join(cadena_vistas), language="text")
            
        with m_col2:
            st.metric("👍 LIKES TOTALES", f"{int(df_res['Likes'].sum()):,}")
            st.write("📱 **DESGLOSE POR RED:**")
            por_red = df_res.groupby('Red')['Vistas'].sum().reset_index()
            txt_desglose = "\n".join([f"{r['Red']}: {int(r['Vistas']):,}" for _, r in por_red.iterrows()])
            st.code(txt_desglose if txt_desglose else "Calculando...")
            
        st.divider()
        st.dataframe(df_res, use_container_width=True, hide_index=True)
        
        # Botón de Descarga
        csv_data = df_res.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DESCARGAR REPORTE EXCEL (CSV)",
            data=csv_data,
            file_name=f"BS_LATAM_AUDIT_{datetime.date.today()}.csv",
            mime='text/csv',
        )

# --- MÓDULO 2: TIKTOK RADAR ---
elif menu_op == "🎯 TIKTOK RADAR":
    st.markdown("### 🎯 TikTok Radar de Tendencias")
    q_search = st.text_input("🔍 Término o Hashtag de Búsqueda:")
    if st.button("🔥 ABRIR RADAR"):
        st.link_button("EJECUTAR BÚSQUEDA EN TIKTOK", f"https://www.tiktok.com/search/video?q={urllib.parse.quote(q_search)}")
    
    radar_input = st.text_area("Pega los datos del radar aquí:", height=300)
    if st.button("🚀 PROCESAR RADAR"):
        links_radar = re.findall(r"(https?://www\.tiktok\.com/@[^/\s]+/video/\d+)", radar_input)
        if links_radar:
            st.session_state.db_final, _ = motor_auditor_completo(list(set(links_radar)), "TikTok")
            st.rerun()

# --- MÓDULO 3: DRIVE AUDITOR ---
elif menu_op == "📂 DRIVE AUDITOR":
    st.markdown("### 📂 Auditoría de Seguridad Google Drive")
    drive_links = st.text_area("Pega enlaces de Drive:", height=200)
    if st.button("🛡️ VERIFICAR ACCESIBILIDAD"):
        links_d = re.findall(r"(https?://drive\.google\.com/[^\s]+)", drive_links)
        if links_d:
            st.session_state.db_drive = auditor_drive_api_v24(links_d)
            st.rerun()
    if not st.session_state.db_drive.empty:
        st.dataframe(st.session_state.db_drive, use_container_width=True)

# --- MÓDULO 4: IA PARTNER ---
elif menu_op == "🤖 PARTNER IA":
    st.markdown("### 🤖 Partner IA Operativo")
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if chat_in := st.chat_input("Escribe tu consulta sobre los datos..."):
        st.session_state.chat_log.append({"role": "user", "content": chat_in})
        # Lógica de respuesta simulada (puedes conectar un LLM aquí)
        st.session_state.chat_log.append({"role": "assistant", "content": "Entendido. Procesando análisis de métricas..."})
        st.rerun()

# --- MÓDULO 5: SEARCH PRO ---
elif menu_op == "🛰️ SEARCH PRO":
    st.subheader("🛰️ Escáner de Canales y Perfiles")
    target = st.text_input("Link del Canal/Usuario:", placeholder="https://www.tiktok.com/@usuario")
    v_min_filter = st.number_input("Filtrar por vistas mínimas:", value=50000)
    
    c_f1, c_f2 = st.columns(2)
    with c_f1: f_ini = st.date_input("Fecha Inicio:", value=datetime.date.today() - datetime.timedelta(days=15))
    with c_f2: f_fin = st.date_input("Fecha Fin:", value=datetime.date.today())
    
    if st.button("🚀 ESCANEAR PERFIL COMPLETO"):
        if target:
            with st.status("🛠️ Ejecutando Escaneo Profundo...", expanded=True) as status:
                ydl_search_opts = {'extract_flat': True, 'quiet': True}
                try:
                    with yt_dlp.YoutubeDL(ydl_search_opts) as ydl:
                        res_info = ydl.extract_info(target, download=False)
                        if res_info and 'entries' in res_info:
                            ts_start = time.mktime(f_ini.timetuple())
                            ts_end = time.mktime((f_fin + datetime.timedelta(days=1)).timetuple())
                            
                            valid_urls = []
                            for entry in res_info['entries']:
                                entry_ts = entry.get('timestamp') or (time.mktime(datetime.datetime.strptime(entry['upload_date'], "%Y%m%d").timetuple()) if entry.get('upload_date') else None)
                                if entry_ts and ts_start <= entry_ts <= ts_end:
                                    valid_urls.append(entry.get('url') or f"https://www.tiktok.com/video/{entry.get('id')}")
                            
                            if valid_urls:
                                st.session_state.db_final, _ = motor_auditor_completo(valid_urls, "TikTok")
                                st.rerun()
                except Exception as e:
                    st.error(f"Error en escaneo: {e}")

# ==============================================================================
# 8. FOOTER DE SEGURIDAD Y CONTROL
# ==============================================================================
st.markdown("---")
st.caption(f"BS LATAM AUDIT ELITE V29.9 | {datetime.datetime.now().strftime('%H:%M:%S')} | ACCESO NIVEL 5")
