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
import random
import google.generativeai as genai
from io import BytesIO

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL Y LLAVES DE ACCESO (PROTEGIDAS)
# ==============================================================================
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"
GEMINI_API_KEY = "AIzaSyA8HsM0vSCopd1s05nOryhbNIGU26dvxG4"

# Configuración de IA Real
genai.configure(api_key=GEMINI_API_KEY)
model_gemini = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(
    page_title="BS LATAM",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "ELITE SUPREMACÍA"
# ==============================================================================
st.markdown("""
    <style>
    .main { background-color: #0b0d11; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
    .stApp { background-color: #0b0d11; }
    .title-box { 
        border-left: 15px solid #E30613; padding: 40px 60px; margin: 30px 0 60px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,13,17,0) 100%);
        border-radius: 0 30px 30px 0; box-shadow: 15px 0 40px rgba(0,0,0,0.6);
    }
    .m-title { font-size: 52px; font-weight: 900; color: #ffffff; text-transform: uppercase; letter-spacing: 8px; margin: 0; }
    .s-title { font-size: 22px; color: #8b949e; font-family: 'Courier New', monospace; margin-top: 20px; font-weight: bold; }
    .bs-latam-sidebar { color: #ffffff; font-weight: 950; font-size: 36px; text-align: center; text-transform: uppercase; text-shadow: 0px 0px 20px #0055ff; }
    [data-testid="stMetricValue"] { color: #E30613 !important; font-weight: 900; font-size: 35px !important; }
    .stButton>button { 
        background: linear-gradient(135deg, #E30613 0%, #9e040d 100%) !important;
        color: #ffffff !important; font-weight: 900 !important; border-radius: 20px; height: 85px; width: 100%; font-size: 24px !important;
    }
    .stTextArea textarea { background-color: #161b22 !important; color: #e6edf3 !important; border: 2px solid #30363d !important; border-radius: 20px; }
    code { font-size: 15px !important; color: #ffffff !important; background-color: #161b22 !important; border: 1px solid #444c56 !important; padding: 18px !important; border-radius: 12px; display: block; }
    </style>
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V31</p>
        <p class="s-title">SISTEMA INTEGRAL DE AUDITORÍA Y RASTREO • BS LATAM PRO</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA Y PERSISTENCIA
# ==============================================================================
if 'db_final' not in st.session_state: st.session_state.db_final = pd.DataFrame()
if 'db_fallidos' not in st.session_state: st.session_state.db_fallidos = pd.DataFrame()
if 'db_drive' not in st.session_state: st.session_state.db_drive = pd.DataFrame()
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = [{"role": "assistant", "content": "¡V31 Activa, jefe! Módulo IA con Gemini 1.5 listo. 🫡"}]

# ==============================================================================
# 4. MOTORES DE AUDITORÍA
# ==============================================================================
def motor_auditor_universal_v24(urls):
    exitos, fallos = [], []
    p_bar = st.progress(0)
    msg_status = st.empty()
    ua_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36']

    for i, raw_u in enumerate(urls):
        url = raw_u.strip().replace('"', '').replace("'", "").rstrip(')').rstrip(',')
        if "?si=" in url: url = url.split('?si=')[0]
        msg_status.markdown(f"📡 **Rastreando:** `{url[:50]}...`")
        
        ydl_opts = {
            'quiet': True, 'no_warnings': True, 'extract_flat': False,
            'skip_download': True, 'ignoreerrors': True, 'socket_timeout': 30,
            'http_headers': {'User-Agent': random.choice(ua_list)}
        }
        try:
            time.sleep(random.uniform(0.5, 1.0))
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    v_ts = info.get('timestamp') or (time.mktime(datetime.datetime.strptime(info['upload_date'], "%Y%m%d").timetuple()) if info.get('upload_date') else None)
                    red_social = "TIKTOK" if "tiktok" in url else "YOUTUBE" if "youtu" in url else "FACEBOOK" if "facebook" in url else "OTRA"
                    exitos.append({
                        "Fecha": datetime.datetime.fromtimestamp(v_ts).strftime('%Y-%m-%d') if v_ts else "N/A",
                        "Red": red_social, "Creador": info.get('uploader') or "N/A", 
                        "Vistas": int(info.get('view_count') or info.get('play_count') or 0),
                        "Likes": int(info.get('like_count') or 0), "Comments": int(info.get('comment_count') or 0),
                        "Saves": int(info.get('repost_count') or 0), "Link Original": url
                    })
                else: fallos.append({"Link": url, "Motivo": "Privado/Bloqueado"})
        except Exception as e: fallos.append({"Link": url, "Motivo": f"Error: {str(e)[:20]}"})
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
                else: resultados_d.append({"Archivo": "🔒 PROTEGIDO", "Peso": "0", "Estado": "❌ BLOQUEADO", "Link": link})
            except: resultados_d.append({"Archivo": "ERROR", "Peso": "0", "Estado": "❌ ROTO", "Link": link})
    return pd.DataFrame(resultados_d)

# ==============================================================================
# 5. PANEL DE NAVEGACIÓN
# ==============================================================================
with st.sidebar:
    st.markdown('<p class="bs-latam-sidebar">BS LATAM</p>', unsafe_allow_html=True)
    st.divider()
    menu = st.radio("MÓDULOS OPERATIVOS", ["🚀 EXTRACTOR", "🎯 TIKTOK RADAR", "📂 DRIVE AUDITOR", "🤖 PARTNER IA", "🛰️ SEARCH PRO"], index=0)
    st.divider()
    if st.button("🚨 REINICIAR SISTEMA"):
        for k in ['db_final', 'db_fallidos', 'db_drive']: st.session_state[k] = pd.DataFrame()
        st.session_state.chat_log = [{"role": "assistant", "content": "Memoria purgada. 🫡"}]
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
        col_glob1, col_glob2 = st.columns([1, 3])
        col_glob1.metric("VISTAS TOTALES (GLOBAL)", f"{df['Vistas'].sum():,}")
        col_glob2.code(" + ".join([str(v) for v in df['Vistas'].tolist()]))
        st.dataframe(df, use_container_width=True)
    if not st.session_state.db_fallidos.empty:
        with st.expander("❌ ENLACES FALLIDOS DETECTADOS"): st.table(st.session_state.db_fallidos)

elif menu == "🎯 TIKTOK RADAR":
    st.markdown("### 🎯 TikTok Radar")
    query_text = st.text_input("🔍 Término de Búsqueda:")
    if st.button("🔥 ABRIR BUSCADOR"): st.link_button("IR A TIKTOK", f"https://www.tiktok.com/search/video?q={urllib.parse.quote(query_text)}")
    raw_data = st.text_area("Zona de Pegado de Datos:", height=400)
    if st.button("🚀 FILTRAR Y PROCESAR"):
        links_radar = re.findall(r"(https?://www\.tiktok\.com/@[^/\s]+/video/\d+)", raw_data)
        if links_radar:
            st.session_state.db_final, _ = motor_auditor_universal_v24(list(set(links_radar)))
            st.rerun()

elif menu == "📂 DRIVE AUDITOR":
    st.markdown("### 📂 Auditoría Drive")
    drive_input = st.text_area("Enlaces:", height=200)
    if st.button("🛡️ VERIFICAR ACCESO"):
        links_d = re.findall(r"(https?://drive\.google\.com/[^\s]+)", drive_input)
        if links_d: st.session_state.db_drive = auditor_drive_api_v24(links_d); st.rerun()
    st.dataframe(st.session_state.db_drive)

elif menu == "🤖 PARTNER IA":
    st.markdown("### 🤖 Partner IA (Cerebro Gemini Active)")
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if prompt := st.chat_input("Escribe tu consulta sobre los datos..."):
        st.session_state.chat_log.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # Contexto de datos
            ctx = ""
            if not st.session_state.db_final.empty:
                vistas = st.session_state.db_final['Vistas'].sum()
                ctx = f"Datos actuales: {len(st.session_state.db_final)} videos procesados con {vistas:,} vistas totales."
            
            try:
                response = model_gemini.generate_content(f"Eres el asistente de BS LATAM. Contexto: {ctx}. Usuario pregunta: {prompt}")
                respuesta = response.text
                st.markdown(respuesta)
                st.session_state.chat_log.append({"role": "assistant", "content": respuesta})
            except Exception as e:
                st.error(f"Error IA: {e}")

elif menu == "🛰️ SEARCH PRO":
    st.subheader("🛰️ Buscador Inteligente Masivo (Bulk Mode)")
    target_input = st.text_area("Pega varios links de Canales o @usuarios (uno por línea):", height=150, placeholder="https://www.tiktok.com/@user1\n@user2")
    vistas_min = st.number_input("Vistas mínimas", value=60000)
    
    col_f1, col_f2 = st.columns(2)
    fecha_inicio = col_f1.date_input("Desde:", value=datetime.date.today() - datetime.timedelta(days=7))
    fecha_fin = col_f2.date_input("Hasta:", value=datetime.date.today())
    
    if st.button("🚀 Iniciar Escaneo Masivo"):
        canales = re.findall(r"(@[\w\.]+|https?://www\.tiktok\.com/@[^/\s\?]+)", target_input)
        if canales:
            all_valid_links = []
            canales_fallidos = []
            status_p = st.status("🕵️ Procesando lista de canales...", expanded=True)
            
            for canal in canales:
                clean_user = canal.split('?')[0].rstrip('/')
                if not clean_user.startswith('http'): clean_user = f"https://www.tiktok.com/@{clean_user.replace('@', '')}"
                
                status_p.write(f"🔍 Escaneando: {clean_user}")
                ydl_opts_search = {'extract_flat': 'in_playlist', 'quiet': True, 'http_headers': {'User-Agent': 'Mozilla/5.0'}}
                
                try:
                    with yt_dlp.YoutubeDL(ydl_opts_search) as ydl:
                        res = ydl.extract_info(clean_user, download=False)
                        if res and 'entries' in res:
                            f_ini, f_fin = time.mktime(fecha_inicio.timetuple()), time.mktime((fecha_fin + datetime.timedelta(days=1)).timetuple())
                            for entry in res['entries']:
                                if not entry: continue
                                v_ts = entry.get('timestamp') or (time.mktime(datetime.datetime.strptime(entry['upload_date'], "%Y%m%d").timetuple()) if entry.get('upload_date') else None)
                                if v_ts and f_ini <= v_ts <= f_fin:
                                    all_valid_links.append(entry.get('url') or f"https://www.tiktok.com/video/{entry.get('id')}")
                        else: canales_fallidos.append({"Canal": clean_user, "Motivo": "Sin acceso/Vacío"})
                except: canales_fallidos.append({"Canal": clean_user, "Motivo": "Error de Red"})
            
            if all_valid_links:
                status_p.write(f"✅ Auditando {len(all_valid_links)} videos detectados...")
                st.session_state.db_final, extra_fallos = motor_auditor_universal_v24(all_valid_links)
                if not extra_fallos.empty:
                    canales_fallidos.extend(extra_fallos.to_dict('records'))
                st.session_state.db_fallidos = pd.DataFrame(canales_fallidos)
                st.rerun()
            else: st.error("No se detectaron videos válidos en los canales ingresados.")
        else: st.warning("Ingresa al menos un canal.")

    if not st.session_state.db_final.empty:
        df_elite = st.session_state.db_final[st.session_state.db_final['Vistas'] >= vistas_min].sort_values(by="Vistas", ascending=False)
        if not df_elite.empty:
            st.markdown(f"### 🏆 Resultados Elite (+{vistas_min:,} vistas)")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Vistas", f"{df_elite['Vistas'].sum():,}"); m2.metric("Likes", f"{df_elite['Likes'].sum():,}")
            m3.metric("Comments", f"{df_elite['Comments'].sum():,}"); m4.metric("Contenido", len(df_elite))
            st.code(" + ".join([str(v) for v in df_elite['Vistas'].tolist()]))
            st.dataframe(df_elite, use_container_width=True, hide_index=True)
    if not st.session_state.db_fallidos.empty:
        with st.expander("❌ CANALES O VIDEOS FALLIDOS"): st.table(st.session_state.db_fallidos)
