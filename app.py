import streamlit as st
import yt_dlp
import pandas as pd
import re
import time
import requests
import json
import datetime
import math
import threading
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
# 4. MOTORES DE AUDITORÍA (EXTRACTOR REFORZADO CON MÉTRICAS TOTALES)
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
        'socket_timeout': 60,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        }
    }
    
    for i, raw_u in enumerate(urls):
        url = raw_u.strip().replace('"', '').split('?')[0].rstrip(')').rstrip(',')
        msg_status.markdown(f"📡 **Rastreando Objetivo:** `{url[:50]}...`")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    v_ts = info.get('timestamp') or (time.mktime(datetime.datetime.strptime(info['upload_date'], "%Y%m%d").timetuple()) if info.get('upload_date') else None)
                    
                    # Lógica de extracción de vistas multicanal
                    vistas = int(info.get('view_count') or info.get('play_count') or 0)
                    
                    autor = info.get('uploader') or info.get('creator') or info.get('channel') or "N/A"
                    
                    # Detectar Red
                    red_tag = "OTRA"
                    if "tiktok.com" in url: red_tag = "TIKTOK"
                    elif "instagram.com" in url: red_tag = "INSTAGRAM"
                    elif "youtube.com" in url or "youtu.be" in url: red_tag = "YOUTUBE"
                    elif "facebook.com" in url or "fb.watch" in url: red_tag = "FACEBOOK"

                    exitos.append({
                        "Fecha": datetime.datetime.fromtimestamp(v_ts).strftime('%Y-%m-%d') if v_ts else "N/A",
                        "Red": red_tag,
                        "Creador": autor, 
                        "Vistas": vistas,
                        "Likes": int(info.get('like_count') or 0),
                        "Comments": int(info.get('comment_count') or 0),
                        "Saves": int(info.get('repost_count') or 0),
                        "Link Original": url
                    })
                else:
                    fallos.append({"Link": url, "Motivo": "Sin datos"})
        except Exception as e:
            fallos.append({"Link": url, "Motivo": f"Error: {str(e)[:20]}"})
        
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
                    resultados_d.append({"Archivo": resp.get('name'), "Peso": peso_mb, "Estado": "✅ DISPONIBLE", "Link": link})
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
    menu = st.radio("MÓDULOS OPERATIVOS", ["🚀 EXTRACTOR", "🎯 TIKTOK RADAR", "📂 DRIVE AUDITOR", "🤖 PARTNER IA", "🛰️ SEARCH PRO"], index=0)
    st.divider()
    if st.button("🚨 REINICIAR SISTEMA COMPLETO"):
        for k in ['db_final', 'db_fallidos', 'db_drive']: st.session_state[k] = pd.DataFrame()
        st.session_state.chat_log = [{"role": "assistant", "content": "Memoria purgada. Sistema listo. 🫡"}]
        st.rerun()

# ==============================================================================
# 6. DESPLIEGUE DE MÓDULOS
# ==============================================================================

if menu == "🚀 EXTRACTOR":
    st.markdown("### 📥 Entrada de Enlaces para Auditoría")
    raw_input = st.text_area("Pega tus links masivos aquí:", height=220)
    if st.button("🔥 INICIAR EXTRACCIÓN"):
        links_f = re.findall(r"(https?://[^\s\"\'\)\],]+)", raw_input)
        if links_f:
            st.session_state.db_final, st.session_state.db_fallidos = motor_auditor_universal_v24(links_f)
            st.rerun()
    
    if not st.session_state.db_final.empty:
        df = st.session_state.db_final
        
        st.divider()
        st.markdown("### 📊 Resumen de Impacto (Copiar)")
        
        c1, c2 = st.columns(2)
        with c1:
            total_vistas = int(df['Vistas'].sum())
            st.write("🌍 **VISTAS TOTALES:**")
            st.code(f"{total_vistas:,}")
            
            st.write("➕ **SUMA DETALLADA (+):**")
            # Mostramos todos, incluso ceros, para diagnosticar si el extractor falló
            vistas_list = [str(int(v)) for v in df['Vistas'].tolist()]
            st.code(" + ".join(vistas_list))

        with c2:
            st.write("📱 **POR PLATAFORMAS:**")
            resumen_redes = df.groupby('Red')['Vistas'].sum().reset_index()
            txt_redes = ""
            for _, row in resumen_redes.iterrows():
                txt_redes += f"{row['Red']}: {int(row['Vistas']):,}\n"
            st.code(txt_redes.strip())
        
        st.divider()
        st.dataframe(df, use_container_width=True, hide_index=True)

elif menu == "🎯 TIKTOK RADAR":
    st.markdown("### 🎯 TikTok Radar")
    query_text = st.text_input("🔍 Término de Búsqueda:")
    if st.button("🔥 ABRIR BUSCADOR"):
        st.link_button("IR A TIKTOK", f"https://www.tiktok.com/search/video?q={urllib.parse.quote(query_text)}")
    raw_data = st.text_area("Zona de Pegado de Datos:", height=400)
    if st.button("🚀 FILTRAR Y PROCESAR"):
        links_radar = re.findall(r"(https?://www\.tiktok\.com/@[^/\s]+/video/\d+)", raw_data)
        if links_radar:
            st.session_state.db_final, _ = motor_auditor_universal_v24(list(set(links_radar)))
            st.rerun()

elif menu == "📂 DRIVE AUDITOR":
    st.markdown("### 📂 Auditoría de Enlaces Google Drive")
    drive_input = st.text_area("Enlaces de Drive:", height=200)
    if st.button("🛡️ VERIFICAR ACCESO"):
        links_d = re.findall(r"(https?://drive\.google\.com/[^\s]+)", drive_input)
        if links_d:
            st.session_state.db_drive = auditor_drive_api_v24(links_d)
            st.rerun()
    st.dataframe(st.session_state.db_drive)

elif menu == "🤖 PARTNER IA":
    st.markdown("### 🤖 IA Partner")
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if chat_input := st.chat_input("Escribe..."):
        st.session_state.chat_log.append({"role": "user", "content": chat_input})
        st.rerun()

elif menu == "🛰️ SEARCH PRO":
    st.subheader("🛰️ Buscador Inteligente de Canales (Auditoría Cronológica)")
    
    col_u1, col_u2 = st.columns([2, 1])
    with col_u1:
        target_user = st.text_input("Pega el link del Canal o @usuario:", placeholder="https://www.tiktok.com/@usuario")
    with col_u2:
        vistas_min = st.number_input("Vistas mínimas", value=60000)
    
    st.divider()
    st.markdown("#### 📅 Rango de tiempo para Escaneo (Filtro Estricto)")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fecha_inicio = st.date_input("Desde:", value=datetime.date.today() - datetime.timedelta(days=7))
    with col_f2:
        fecha_fin = st.date_input("Hasta:", value=datetime.date.today())
    
    if st.button("🚀 Escanear Canal"):
        if target_user:
            clean_user = target_user.split('?')[0].rstrip('/')
            if not clean_user.startswith('http'):
                clean_user = f"https://www.tiktok.com/@{clean_user.replace('@', '')}"
            
            with st.status("🛠️ Iniciando Escaneo Cronológico Estricto...", expanded=True) as status:
                ydl_opts_search = {
                    'extract_flat': True, 'quiet': True,
                    'http_headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                }
                try:
                    with yt_dlp.YoutubeDL(ydl_opts_search) as ydl:
                        res = ydl.extract_info(clean_user, download=False)
                        if res and 'entries' in res:
                            f_inicio_ts = time.mktime(fecha_inicio.timetuple())
                            f_fin_ts = time.mktime((fecha_fin + datetime.timedelta(days=1)).timetuple())
                            
                            valid_links = []
                            for entry in res['entries']:
                                v_ts = entry.get('timestamp') or (time.mktime(datetime.datetime.strptime(entry['upload_date'], "%Y%m%d").timetuple()) if entry.get('upload_date') else None)
                                if v_ts and f_inicio_ts <= v_ts <= f_fin_ts:
                                    valid_links.append(entry.get('url') or f"https://www.tiktok.com/video/{entry.get('id')}")
                            
                            if valid_links:
                                st.session_state.db_final, _ = motor_auditor_universal_v24(valid_links)
                                status.update(label="✅ Escaneo Finalizado!", state="complete")
                                st.rerun()
                except Exception as e:
                    st.error(f"Error Técnico: {str(e)}")
        else:
            st.warning("Introduce un canal.")

    if not st.session_state.db_final.empty:
        df_elite = st.session_state.db_final[st.session_state.db_final['Vistas'] >= vistas_min].sort_values(by="Vistas", ascending=False)
        if not df_elite.empty:
            st.markdown(f"### 🏆 Resultados Elite (+{vistas_min:,} vistas)")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Vistas", f"{df_elite['Vistas'].sum():,}")
            m2.metric("Likes", f"{df_elite['Likes'].sum():,}")
            m3.metric("Comments", f"{df_elite['Comments'].sum():,}")
            m4.metric("Contenido", len(df_elite))
            
            st.code(" + ".join([str(int(v)) for v in df_elite['Vistas'].tolist()]))
            st.dataframe(df_elite[["Fecha", "Vistas", "Likes", "Comments", "Saves", "Link Original"]], use_container_width=True, hide_index=True)
