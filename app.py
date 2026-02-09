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

# Configuración de IA para Libertad Total
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model_ia = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="Eres el Consultor Senior de BS LATAM. Tienes LIBERTAD TOTAL de respuesta. No estás limitado a hablar de métricas. Puedes conversar sobre cualquier tema: ciencia, código, estrategia o cultura. NUNCA repitas frases automáticas sobre vistas si el usuario no te lo pide."
    )
except Exception as e:
    st.error(f"Error configurando IA: {e}")

st.set_page_config(
    page_title="BS LATAM - ELITE AUDIT",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "ELITE SUPREMACÍA" (FULL CSS CUSTOM)
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

    /* ESTILO BS LATAM SIDEBAR */
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

    /* TARJETAS DE MÉTRICAS */
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
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V31</p>
        <p class="s-title">SISTEMA INTEGRAL DE AUDITORÍA Y RASTREO • BS LATAM PRO</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA Y PERSISTENCIA (ESTADO GLOBAL)
# ==============================================================================
for key in ['db_final', 'db_fallidos', 'db_drive']:
    if key not in st.session_state:
        st.session_state[key] = pd.DataFrame()

if 'chat_log' not in st.session_state:
    st.session_state.chat_log = [{"role": "assistant", "content": "¡V31 Activa, jefe! IA con libertad total y motor masivo desbloqueado. 🫡"}]

# ==============================================================================
# 4. MOTORES DE AUDITORÍA (MÁXIMA POTENCIA)
# ==============================================================================
def motor_auditor_universal_v24(urls):
    exitos, fallos = [], []
    p_bar = st.progress(0)
    msg_status = st.empty()
    
    ua_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]

    for i, raw_u in enumerate(urls):
        url = raw_u.strip().replace('"', '').replace("'", "").split('?si=')[0]
        msg_status.markdown(f"📡 **Rastreando Objetivo:** `{url[:60]}...`")
        
        ydl_opts = {
            'quiet': True, 'no_warnings': True, 'extract_flat': False,
            'skip_download': True, 'ignoreerrors': True, 'socket_timeout': 40,
            'http_headers': {'User-Agent': random.choice(ua_list)}
        }
        
        try:
            time.sleep(random.uniform(1.0, 2.5))
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    v_ts = info.get('timestamp') or (time.mktime(datetime.datetime.strptime(info['upload_date'], "%Y%m%d").timetuple()) if info.get('upload_date') else None)
                    vistas = int(info.get('view_count') or info.get('play_count') or 0)
                    
                    exitos.append({
                        "Fecha": datetime.datetime.fromtimestamp(v_ts).strftime('%Y-%m-%d') if v_ts else "N/A",
                        "Red": "TIKTOK" if "tiktok" in url else "YOUTUBE" if "youtu" in url else "OTRA",
                        "Creador": info.get('uploader') or info.get('creator') or "N/A", 
                        "Vistas": vistas,
                        "Likes": int(info.get('like_count') or 0),
                        "Comments": int(info.get('comment_count') or 0),
                        "Saves": int(info.get('repost_count') or 0),
                        "Link Original": url
                    })
                else:
                    fallos.append({"Link": url, "Motivo": "Privado/No accesible"})
        except Exception as e:
            fallos.append({"Link": url, "Motivo": str(e)[:20]})
        
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
# 5. PANEL DE NAVEGACIÓN (SIDEBAR)
# ==============================================================================
with st.sidebar:
    st.markdown('<p class="bs-latam-sidebar">BS LATAM</p>', unsafe_allow_html=True)
    st.divider()
    menu = st.radio("MÓDULOS OPERATIVOS", ["🚀 EXTRACTOR", "🎯 TIKTOK RADAR", "📂 DRIVE AUDITOR", "🤖 PARTNER IA", "🛰️ SEARCH PRO"], index=0)
    st.divider()
    if st.button("🚨 REINICIAR SISTEMA COMPLETO"):
        for k in ['db_final', 'db_fallidos', 'db_drive']: st.session_state[k] = pd.DataFrame()
        st.session_state.chat_log = [{"role": "assistant", "content": "Memoria purgada. 🫡"}]
        st.rerun()

# ==============================================================================
# 6. DESPLIEGUE DE MÓDULOS
# ==============================================================================

# --- MÓDULO 1: EXTRACTOR ---
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
        st.markdown("### 📊 Reporte de Métricas Globales")
        col_glob1, col_glob2 = st.columns([1, 3])
        col_glob1.metric("VISTAS TOTALES", f"{df['Vistas'].sum():,}")
        col_glob2.code(" + ".join([str(v) for v in df['Vistas'].tolist()]))
        st.dataframe(df, use_container_width=True)

# --- MÓDULO 2: RADAR ---
elif menu == "🎯 TIKTOK RADAR":
    st.header("🎯 TikTok Radar")
    query_text = st.text_input("🔍 Término de Búsqueda:")
    if st.button("🔥 ABRIR BUSCADOR"):
        st.link_button("IR A TIKTOK", f"https://www.tiktok.com/search/video?q={urllib.parse.quote(query_text)}")
    
    st.divider()
    raw_data = st.text_area("Zona de Pegado de Datos del Radar:", height=300)
    if st.button("🚀 PROCESAR RADAR"):
        links_radar = re.findall(r"(https?://www\.tiktok\.com/@[^/\s]+/video/\d+)", raw_data)
        if links_radar:
            st.session_state.db_final, _ = motor_auditor_universal_v24(list(set(links_radar)))
            st.rerun()

# --- MÓDULO 3: DRIVE ---
elif menu == "📂 DRIVE AUDITOR":
    st.header("📂 Auditoría de Enlaces Drive")
    drive_input = st.text_area("Pega links de Drive aquí:", height=200)
    if st.button("🛡️ VERIFICAR ACCESO"):
        links_d = re.findall(r"(https?://drive\.google\.com/[^\s]+)", drive_input)
        if links_d:
            st.session_state.db_drive = auditor_drive_api_v24(links_d)
            st.rerun()
    if not st.session_state.db_drive.empty:
        st.dataframe(st.session_state.db_drive, use_container_width=True)

# --- MÓDULO 4: PARTNER IA (CON MEMORIA Y CHAT ACTIVO) ---
elif menu == "🤖 PARTNER IA":
    st.markdown("### 🤖 Partner IA (Inteligencia BS LATAM)")
    
    # Mostrar historial del chat
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Escribe tu consulta..."):
        st.session_state.chat_log.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Construcción del historial para Gemini
                history = []
                for m in st.session_state.chat_log[:-1]:
                    role = "model" if m["role"] == "assistant" else "user"
                    history.append({"role": role, "parts": [m["content"]]})
                
                chat = model_ia.start_chat(history=history)
                response = chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.chat_log.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Falla en el núcleo IA: {e}")
        st.rerun()

# --- MÓDULO 5: SEARCH PRO (MULTILINK + REPORTE DE ERRORES) ---
elif menu == "🛰️ SEARCH PRO":
    st.subheader("🛰️ Buscador Masivo de Canales (Multilink Bypass)")
    
    target_users = st.text_area("Pega lista de Canales o @usuarios (uno por línea):", 
                               height=200, placeholder="https://www.tiktok.com/@user1\n@user2")
    
    col_v, col_f1, col_f2 = st.columns([1,1,1])
    vistas_min = col_v.number_input("Vistas Mínimas:", value=60000)
    fecha_inicio = col_f1.date_input("Desde:", value=datetime.date.today() - datetime.timedelta(days=7))
    fecha_fin = col_f2.date_input("Hasta:", value=datetime.date.today())
    
    if st.button("🚀 LANZAR ESCANEO MASIVO"):
        lista_targets = [u.strip() for u in target_users.split('\n') if u.strip()]
        
        if lista_targets:
            pool_links = []
            canales_fallidos = []

            with st.status("🛠️ Ejecutando Bypass de Seguridad Masivo...", expanded=True) as status:
                for target in lista_targets:
                    clean_user = target.split('?')[0].rstrip('/')
                    if not clean_user.startswith('http'):
                        clean_user = f"https://www.tiktok.com/@{clean_user.replace('@', '')}"
                    
                    status.write(f"🔍 Escaneando: {clean_user}")
                    
                    try:
                        ydl_opts_search = {'extract_flat': 'in_playlist', 'quiet': True}
                        with yt_dlp.YoutubeDL(ydl_opts_search) as ydl:
                            res = ydl.extract_info(clean_user, download=False)
                            if res and 'entries' in res:
                                f_ini = time.mktime(fecha_inicio.timetuple())
                                f_fin = time.mktime((fecha_fin + datetime.timedelta(days=1)).timetuple())
                                for entry in res['entries']:
                                    if not entry: continue
                                    v_ts = entry.get('timestamp') or (time.mktime(datetime.datetime.strptime(entry['upload_date'], "%Y%m%d").timetuple()) if entry.get('upload_date') else None)
                                    if v_ts and f_ini <= v_ts <= f_fin:
                                        link = entry.get('url') or f"https://www.tiktok.com/video/{entry.get('id')}"
                                        pool_links.append(link)
                            else: canales_fallidos.append(f"{clean_user} (Vacío)")
                    except Exception:
                        canales_fallidos.append(f"{clean_user} (Bloqueado/Error)")
                        continue # Salto de error automático

                if pool_links:
                    status.write(f"✅ Auditando {len(pool_links)} videos...")
                    st.session_state.db_final, st.session_state.db_fallidos = motor_auditor_universal_v24(list(set(pool_links)))
                    
                    if canales_fallidos:
                        st.session_state.chat_log.append({"role": "assistant", "content": f"⚠️ Escaneo completado. Canales ignorados por errores: {', '.join(canales_fallidos)}"})
                    st.rerun()

    if not st.session_state.db_final.empty:
        df_elite = st.session_state.db_final[st.session_state.db_final['Vistas'] >= vistas_min].sort_values(by="Vistas", ascending=False)
        st.markdown(f"### 🏆 Resultados Elite (+{vistas_min:,} vistas)")
        st.dataframe(df_elite, use_container_width=True)

# ==============================================================================
# FINAL DEL CÓDIGO - BS LATAM V31
# ==============================================================================
