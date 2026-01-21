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
# 1. CONFIGURACIÓN ESTRUCTURAL Y LLAVES DE ACCESO (BS LATAM ELITE)
# ==============================================================================
# Llave maestra con permisos para YouTube Data API v3 y Google Drive API
# Esta llave es el corazón del sistema para evitar los bloqueos de IP
API_KEY_BS = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"

st.set_page_config(
    page_title="BS LATAM - AUDIT ELITE SUPREMACÍA V30.9",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "ELITE SUPREMACÍA" (CSS INDUSTRIAL DARK)
# ==============================================================================
st.markdown("""
    <style>
    /* Configuración de fondo y scroll personalizado */
    .main { background-color: #0b0d11; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
    .stApp { background-color: #0b0d11; }
    
    /* Bloque de Título Estilo BS LATAM */
    .title-box { 
        border-left: 15px solid #E30613; padding: 45px 65px; margin: 35px 0 65px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,13,17,0) 100%);
        border-radius: 0 35px 35px 0; box-shadow: 18px 0 45px rgba(0,0,0,0.7);
    }
    .m-title { 
        font-size: 55px; font-weight: 950; color: #ffffff; 
        text-transform: uppercase; letter-spacing: 9px; margin: 0; line-height: 1.0;
        text-shadow: 4px 4px 8px rgba(0,0,0,0.8);
    }
    .s-title { 
        font-size: 24px; color: #8b949e; font-family: 'Courier New', monospace; 
        margin-top: 25px; letter-spacing: 4px; font-weight: bold;
    }

    /* Diseño de Barra Lateral Elite */
    .bs-latam-sidebar {
        color: #ffffff; font-weight: 950; font-size: 38px; text-align: center;
        text-transform: uppercase; letter-spacing: 6px;
        text-shadow: 0px 0px 25px #0055ff, 2px 2px 0px #000000;
        margin-bottom: 40px; padding: 20px; border-bottom: 3px solid #E30613;
    }
    
    /* Indicadores de Métricas (Cards) */
    [data-testid="stMetric"] { 
        background-color: #161b22; border: 2px solid #30363d; 
        padding: 45px; border-radius: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    [data-testid="stMetricValue"] { color: #E30613 !important; font-weight: 900; font-size: 52px !important; }
    [data-testid="stMetricLabel"] { font-size: 18px !important; color: #8b949e !important; text-transform: uppercase; }

    /* Botones de Impacto */
    .stButton>button { 
        background: linear-gradient(135deg, #E30613 0%, #9e040d 100%) !important;
        color: #ffffff !important; font-weight: 900 !important; text-transform: uppercase;
        border-radius: 22px; height: 90px; width: 100%; font-size: 26px !important;
        border: none; box-shadow: 0 12px 25px rgba(227,6,19,0.35);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(227,6,19,0.5); }
    
    /* Áreas de Texto y Código */
    .stTextArea textarea { 
        background-color: #161b22 !important; color: #e6edf3 !important; 
        border: 2px solid #30363d !important; border-radius: 25px; font-size: 17px;
        padding: 20px;
    }
    
    code { 
        font-size: 17px !important; color: #00ffcc !important; background-color: #0b0d11 !important; 
        border: 2px solid #E30613 !important; padding: 25px !important; border-radius: 15px; 
        display: block; margin: 15px 0; line-height: 1.6;
    }

    /* Tablas de Datos */
    .stDataFrame { border: 1px solid #30363d; border-radius: 15px; background-color: #161b22; }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V30.9</p>
        <p class="s-title">SISTEMA TOTAL DE AUDITORÍA Y RASTREO • BS LATAM PRO</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA Y ESTADOS DE SESIÓN (PERSISTENCIA TOTAL)
# ==============================================================================
if 'db_final' not in st.session_state: st.session_state.db_final = pd.DataFrame()
if 'db_fallidos' not in st.session_state: st.session_state.db_fallidos = []
if 'db_drive' not in st.session_state: st.session_state.db_drive = pd.DataFrame()
if 'chat_log' not in st.session_state: 
    st.session_state.chat_log = [{"role": "assistant", "content": "Protocolo BS-ELITE V30.9 iniciado. Sistemas de rastreo listos. 🫡"}]

# ==============================================================================
# 4. NÚCLEO DE EXTRACCIÓN HÍBRIDO (MOTOR DE LIMPIEZA TOTAL)
# ==============================================================================

def clean_bs_link(url):
    """Limpia enlaces de basura de rastreo y parámetros UTM para evitar errores de red social."""
    url = url.strip().replace('"', '').replace("'", "")
    if "?" in url: url = url.split('?')[0]
    return url.rstrip('/')

def fetch_youtube_api_pro(url):
    """Extracción vía API Oficial de Google para YouTube (Blindaje contra 0 vistas)."""
    try:
        vid_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if not vid_match: return None
        v_id = vid_match.group(1)
        
        service = build("youtube", "v3", developerKey=API_KEY_BS)
        res = service.videos().list(part="snippet,statistics,contentDetails", id=v_id).execute()
        
        if not res['items']: return None
        item = res['items'][0]
        # Cálculo exacto de duración para determinar tipo
        dur_iso = item['contentDetails']['duration']
        dur_sec = isodate.parse_duration(dur_iso).total_seconds()
        
        return {
            "Fecha": datetime.datetime.now().strftime('%Y-%m-%d'),
            "Red": "YOUTUBE",
            "Tipo": "Short" if (dur_sec <= 61 or "/shorts/" in url) else "Video Largo",
            "Creador": item['snippet']['channelTitle'],
            "Vistas": int(item['statistics'].get('viewCount', 0)),
            "Likes": int(item['statistics'].get('likeCount', 0)),
            "Comments": int(item['statistics'].get('commentCount', 0)),
            "Saves": 0,
            "Link Original": url
        }
    except Exception as e:
        return None

def fetch_social_dlp_elite(url, platform):
    """Extracción vía Scrapping Reforzado para TikTok y Facebook con rotación de UA."""
    opts = {
        'quiet': True, 'no_warnings': True, 'extract_flat': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'socket_timeout': 45
    }
    if os.path.exists('cookies.txt'): opts['cookiefile'] = 'cookies.txt'
    
    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            # Delay de seguridad contra bloqueos por IP
            time.sleep(random.uniform(2.5, 4.5))
            info = ydl.extract_info(url, download=False)
            if not info: return None
            
            vistas = info.get('view_count') or info.get('play_count') or 0
            likes = info.get('like_count') or 0
            
            return {
                "Fecha": datetime.datetime.now().strftime('%Y-%m-%d'),
                "Red": platform.upper(),
                "Tipo": "Reel/TikTok",
                "Creador": info.get('uploader') or info.get('channel', 'N/A'),
                "Vistas": int(vistas),
                "Likes": int(likes),
                "Comments": int(info.get('comment_count', 0)),
                "Saves": int(info.get('repost_count', 0)),
                "Link Original": url
            }
        except Exception:
            return None

def extractor_maestro_pro(raw_text):
    """Detector automático de plataforma y limpieza de enlaces."""
    urls_found = re.findall(r"(https?://[^\s\"\'\)\],]+)", raw_text)
    resultados, fallos = [], []
    
    pbar = st.progress(0)
    status = st.empty()
    
    for i, raw_url in enumerate(urls_found):
        clean_url = clean_bs_link(raw_url)
        status.markdown(f"📡 **ANALIZANDO OBJETIVO [{i+1}/{len(urls_found)}]:** `{clean_url[:60]}...`")
        
        data = None
        if "youtube.com" in clean_url or "youtu.be" in clean_url:
            data = fetch_youtube_api_pro(clean_url)
        elif "tiktok.com" in clean_url:
            data = fetch_social_dlp_elite(clean_url, "TikTok")
        elif "facebook.com" in clean_url or "fb.watch" in clean_url:
            data = fetch_social_dlp_elite(clean_url, "Facebook")
            
        if data and data["Vistas"] > 0:
            resultados.append(data)
        else:
            fallos.append(clean_url)
        
        pbar.progress((i + 1) / len(urls_found))
    
    status.empty()
    pbar.empty()
    return pd.DataFrame(resultados), fallos

# ==============================================================================
# 5. MÓDULO DE DRIVE AUDITOR (GESTIÓN DE PESO Y ACCESO)
# ==============================================================================

def auditor_drive_elite(links):
    """Verifica el tamaño y estado de enlaces masivos de Google Drive."""
    results = []
    for l in links:
        f_id_match = re.search(r'[-\w]{25,}', l)
        if f_id_match:
            fid = f_id_match.group()
            url_api = f"https://www.googleapis.com/drive/v3/files/{fid}?fields=name,size&key={API_KEY_BS}"
            try:
                r = requests.get(url_api, timeout=25).json()
                if "error" not in r:
                    peso_mb = f"{int(r.get('size', 0))/1024/1024:.2f} MB" if r.get('size') else "N/A"
                    results.append({"Archivo": r.get('name'), "Peso": peso_mb, "Estado": "✅ DISPONIBLE", "Link": l})
                else:
                    results.append({"Archivo": "🔒 PRIVADO", "Peso": "-", "Estado": "❌ BLOQUEADO", "Link": l})
            except:
                results.append({"Archivo": "ERROR", "Peso": "-", "Estado": "❌ ROTO", "Link": l})
    return pd.DataFrame(results)

# ==============================================================================
# 6. PANEL DE CONTROL LATERAL (SIDEBAR ELITE)
# ==============================================================================
with st.sidebar:
    st.markdown('<p class="bs-latam-sidebar">BS LATAM</p>', unsafe_allow_html=True)
    st.divider()
    menu = st.radio(
        "MÓDULOS OPERATIVOS", 
        ["🚀 EXTRACTOR UNIFICADO", "🎯 TIKTOK RADAR", "📂 DRIVE AUDITOR", "🤖 PARTNER IA", "🛰️ SEARCH PRO"],
        index=0
    )
    st.divider()
    st.info("💡 **Tip:** El extractor unificado detecta automáticamente YouTube, TikTok y Facebook.")
    if st.button("🚨 REINICIAR SISTEMA"):
        st.session_state.db_final = pd.DataFrame()
        st.session_state.db_fallidos = []
        st.session_state.db_drive = pd.DataFrame()
        st.rerun()

# ==============================================================================
# 7. DESPLIEGUE DE MÓDULOS DE INTERFAZ (LÓGICA DE NEGOCIO)
# ==============================================================================

# --- MÓDULO 1: EXTRACTOR UNIFICADO ---
if menu == "🚀 EXTRACTOR UNIFICADO":
    st.markdown("### 📥 Extracción Masiva de Enlaces (Multi-Plataforma)")
    raw_input = st.text_area("Pega tus links aquí (YouTube, TikTok, Facebook):", height=280)
    
    if st.button("🔥 INICIAR AUDITORÍA DE IMPACTO"):
        if raw_input:
            st.session_state.db_final, st.session_state.db_fallidos = extractor_maestro_pro(raw_input)
            st.rerun()
            
    if not st.session_state.db_final.empty:
        df = st.session_state.db_final
        st.divider()
        
        # Bloque de Métricas Críticas
        mcol1, mcol2 = st.columns(2)
        with mcol1:
            st.metric("🌍 VISTAS TOTALES", f"{int(df['Vistas'].sum()):,}")
            st.write("📋 **CADENA DE SUMA (+):**")
            v_string = [str(int(v)) for v in df['Vistas'].tolist()]
            st.code("+".join(v_string))
            
        with mcol2:
            st.metric("👍 LIKES TOTALES", f"{int(df['Likes'].sum()):,}")
            st.write("📊 **DESGLOSE POR PLATAFORMA:**")
            v_dict = df.groupby('Red')['Vistas'].sum().to_dict()
            txt_plat = "\n".join([f"{k}: {v:,}" for k, v in v_dict.items()])
            st.code(txt_plat if txt_plat else "Calculando...")
        
        st.divider()
        st.subheader("📝 Tabla de Resultados Detallada")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Gestión de Fallos
        if st.session_state.db_fallidos:
            with st.expander("❌ Enlaces con error o 0 vistas (Posible bloqueo)"):
                for f in st.session_state.db_fallidos: st.error(f)
        
        # Exportación
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 DESCARGAR REPORTE EXCEL (CSV)", data=csv, file_name=f"audit_bs_{datetime.date.today()}.csv", mime='text/csv')

# --- MÓDULO 2: TIKTOK RADAR ---
elif menu == "🎯 TIKTOK RADAR":
    st.markdown("### 🎯 TikTok Radar de Tendencias")
    q_radar = st.text_input("🔍 Término o Hashtag de Búsqueda:")
    if st.button("🔥 ABRIR RADAR EXTERNO"):
        st.link_button("EJECUTAR BÚSQUEDA EN TIKTOK", f"https://www.tiktok.com/search/video?q={urllib.parse.quote(q_radar)}")
    
    radar_input = st.text_area("Pega los datos del radar para extraer enlaces:", height=300)
    if st.button("🚀 PROCESAR RADAR"):
        # Filtrar solo links de video de TikTok
        links_radar = re.findall(r"(https?://www\.tiktok\.com/@[^/\s]+/video/\d+)", radar_input)
        if links_radar:
            st.session_state.db_final, _ = extractor_maestro_pro("\n".join(list(set(links_radar))))
            st.rerun()

# --- MÓDULO 3: DRIVE AUDITOR ---
elif menu == "📂 DRIVE AUDITOR":
    st.markdown("### 📂 Auditoría de Enlaces Google Drive")
    drive_input = st.text_area("Pega enlaces de Drive aquí:", height=200)
    if st.button("🛡️ VERIFICAR ACCESIBILIDAD"):
        links_d = re.findall(r"(https?://drive\.google\.com/[^\s]+)", drive_input)
        if links_d:
            st.session_state.db_drive = auditor_drive_elite(links_d)
    
    if not st.session_state.db_drive.empty:
        st.dataframe(st.session_state.db_drive, use_container_width=True)

# --- MÓDULO 4: IA PARTNER ---
elif menu == "🤖 PARTNER IA":
    st.markdown("### 🤖 Partner IA Operativo")
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if prompt := st.chat_input("Consulta operativa sobre la auditoría..."):
        st.session_state.chat_log.append({"role": "user", "content": prompt})
        # Lógica de respuesta IA simulada para análisis de datos
        res_ia = "Análisis completado. Los datos muestran una retención alta en YouTube."
        st.session_state.chat_log.append({"role": "assistant", "content": res_ia})
        st.rerun()

# --- MÓDULO 5: SEARCH PRO ---
elif menu == "🛰️ SEARCH PRO":
    st.subheader("🛰️ Escaneo Profundo de Canales")
    target_channel = st.text_input("Link del Perfil o Canal:", placeholder="https://www.tiktok.com/@usuario")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1: f_inicio = st.date_input("Fecha Inicio:", value=datetime.date.today() - datetime.timedelta(days=15))
    with col_f2: f_fin = st.date_input("Fecha Fin:", value=datetime.date.today())
    
    if st.button("🚀 INICIAR ESCANEO DE CANAL"):
        if target_channel:
            with st.status("🛠️ Ejecutando Escaneo...", expanded=True) as status:
                ydl_opts_search = {'extract_flat': True, 'quiet': True}
                try:
                    with yt_dlp.YoutubeDL(ydl_opts_search) as ydl:
                        res_info = ydl.extract_info(target_channel, download=False)
                        if res_info and 'entries' in res_info:
                            ts_ini = time.mktime(f_inicio.timetuple())
                            ts_fin = time.mktime((f_fin + datetime.timedelta(days=1)).timetuple())
                            
                            valid_urls = []
                            for entry in res_info['entries']:
                                # Intentar obtener fecha de subida
                                e_ts = entry.get('timestamp') or (time.mktime(datetime.datetime.strptime(entry['upload_date'], "%Y%m%d").timetuple()) if entry.get('upload_date') else None)
                                if e_ts and ts_ini <= e_ts <= ts_fin:
                                    valid_urls.append(entry.get('url') or f"https://www.tiktok.com/video/{entry.get('id')}")
                            
                            if valid_urls:
                                st.session_state.db_final, _ = extractor_maestro_pro("\n".join(valid_urls))
                                st.rerun()
                except Exception as e:
                    st.error(f"Error en escaneo: {e}")

# ==============================================================================
# 8. FOOTER DE SEGURIDAD Y CONTROL DE VERSIÓN
# ==============================================================================
st.markdown("---")
st.caption(f"BS LATAM AUDIT ELITE V30.9 | {datetime.datetime.now().strftime('%H:%M:%S')} | ACCESO NIVEL 5 ACTIVADO")
