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
# 1. CONFIGURACIÓN ESTRUCTURAL Y LLAVES DE ACCESO (PROTECCIÓN DE NÚCLEO)
# ==============================================================================
# Esta sección mantiene la integridad de la conexión con las APIs externas.
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"

st.set_page_config(
    page_title="BS LATAM",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL "ELITE SUPREMACÍA" (LÍNEAS DE ESTILO ORIGINALES)
# ==============================================================================
# Se mantienen todas las líneas de CSS para asegurar la estética BS LATAM.
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
# 3. GESTIÓN DE MEMORIA Y PERSISTENCIA (SISTEMA DE DATOS EXTENDIDO)
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
# 4. MOTORES DE AUDITORÍA (MANTENIMIENTO DE LÓGICA V24)
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
    # Retornamos los datos ordenados de mayor a menor por defecto
    df_result = pd.DataFrame(exitos)
    if not df_result.empty:
        df_result = df_result.sort_values(by="Vistas", ascending=False)
    return df_result, pd.DataFrame(fallos)

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
# 5. PANEL DE NAVEGACIÓN Y CONTROL (SIDEBAR MÁXIMA EXTENSIÓN)
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
    
    st.divider()
    st.markdown(f"**ESTADO:** ÓPTIMO")
    st.markdown(f"**VERSIÓN:** 29.0.9 Omni-Titan")
    st.markdown(f"📅 {datetime.date.today()}")

# ==============================================================================
# 6. DESPLIEGUE DE MÓDULOS (LÓGICA AUTOMATIZADA SIN RECORTES)
# ==============================================================================

# --- MÓDULO 1: EXTRACTOR PRO ---
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
                st.markdown(f"""
                <div class="subtotal-card">
                    <div class="sub-l">{p_name}</div>
                    <div class="sub-v">{v_total:,}</div>
                </div>
                """, unsafe_allow_html=True)
                if v_total > 0:
                    st.code(" + ".join([str(v) for v in sub_data['Vistas'].tolist()]))

        st.markdown("### 📝 Detalle Individual (Ordenado por Vistas)")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        if not st.session_state.db_fallidos.empty:
            st.markdown("---")
            st.warning("⚠️ ENLACES CON ERRORES (REVISAR MANUALMENTE):")
            st.dataframe(st.session_state.db_fallidos, use_container_width=True)

# --- MÓDULO 2: TIKTOK RADAR (REPARADO: SIN SLIDER Y ORDENADO) ---
elif menu == "🎯 TIKTOK RADAR":
    st.markdown("### 🎯 TikTok Radar - Rastreador Total de Populares")
    st.info("Búsqueda automatizada de todo el contenido relevante. El sistema extraerá los videos populares y los ordenará de mayor a menor engagement automáticamente.")
    
    # Hemos eliminado el slider de cantidad para cumplir con el requerimiento de "buscar todos"
    query_text = st.text_input("🔍 Término de Búsqueda (Nicho/Marca):", placeholder="Ej: Blood Strike")
    forzar_esp = st.toggle("Forzar Contenido Español 🇪🇸", value=True)

    if st.button("🚀 ACTIVAR RASTREO TOTAL"):
        if query_text:
            with st.status("🛸 Iniciando Protocolo de Extracción Masiva...", expanded=True) as status:
                st.write("🔍 Escaneando el índice global de TikTok para 'Populares'...")
                final_q = query_text + (" (de OR el OR en OR la)" if forzar_esp else "")
                
                # Configuración de búsqueda sin límites de usuario
                search_opts = {
                    'quiet': True, 
                    'extract_flat': True, 
                    'force_generic_extractor': True,
                    'playlistend': 100  # Aumentamos el rango para capturar todo lo "popular" visible
                }
                
                try:
                    with yt_dlp.YoutubeDL(search_opts) as ydl:
                        search_url = f"https://www.tiktok.com/search/video?q={urllib.parse.quote(final_q)}"
                        info = ydl.extract_info(f"ytsearch100:{search_url}", download=False)
                        
                        links_encontrados = []
                        if 'entries' in info:
                            for entry in info['entries']:
                                if entry and 'url' in entry:
                                    links_encontrados.append(entry['url'])
                        
                        if not links_encontrados:
                            st.warning("⚠️ Acceso directo restringido por TikTok. Generando puente manual...")
                            st.link_button("🔥 ABRIR BÚSQUEDA MANUAL", search_url)
                        else:
                            st.write(f"✅ Se localizaron {len(links_encontrados)} videos. Procesando jerarquía de vistas...")
                            # La función motor_auditor_universal_v24 ya ordena de mayor a menor
                            df_res, df_err = motor_auditor_universal_v24(links_encontrados)
                            
                            st.session_state.db_final = df_res
                            st.session_state.db_fallidos = df_err
                            status.update(label="✅ Misión Cumplida. Resultados cargados y ordenados.", state="complete")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                except Exception as e:
                    st.error(f"Fallo en el sistema de rastreo: {str(e)}")
        else:
            st.error("Jefe, ingresa un objetivo de búsqueda.")

# --- MÓDULO 3: DRIVE AUDITOR (LÍNEAS INTEGRADAS) ---
elif menu == "📂 DRIVE AUDITOR":
    st.markdown("### 📂 Auditoría de Enlaces Google Drive")
    drive_input = st.text_area("Pega los enlaces de carpetas o archivos de Drive:", height=200)
    if st.button("🛡️ VERIFICAR ACCESO"):
        links_d = re.findall(r"(https?://drive\.google\.com/[^\s]+)", drive_input)
        if links_d:
            st.session_state.db_drive = auditor_drive_api_v24(links_d)
            st.rerun()
    if not st.session_state.db_drive.empty:
        st.markdown("### 📋 Resultados de Escaneo Drive")
        st.dataframe(st.session_state.db_drive, use_container_width=True, hide_index=True)

# --- MÓDULO 4: PARTNER IA (MANTENIMIENTO DE CÁLCULOS) ---
elif menu == "🤖 PARTNER IA":
    st.markdown("### 🤖 IA Partner - Asistente de Cálculos y Auditoría")
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if chat_input := st.chat_input("Pega una lista de números o haz una consulta..."):
        st.session_state.chat_log.append({"role": "user", "content": chat_input})
        with st.chat_message("user"): st.markdown(chat_input)
        with st.chat_message("assistant"):
            # Lógica de extracción de números para sumas rápidas
            numeros = re.findall(r'\d+', chat_input.replace(',', '').replace('.', ''))
            if numeros:
                suma = sum([int(n) for n in numeros])
                respuesta = f"🔢 He detectado una serie numérica. La suma total es: **{suma: ,}**"
            else:
                respuesta = "Estoy listo para procesar tus datos. Pega una lista de vistas y las sumaré por ti."
            st.markdown(respuesta)
            st.session_state.chat_log.append({"role": "assistant", "content": respuesta})

# --- MÓDULO 5: SEARCH PRO ---
elif menu == "🛰️ SEARCH PRO":
    st.markdown("### 🛰️ Search Pro - Rastreador de Perfiles Externos")
    target_name = st.text_input("Nombre de Creador o Marca:")
    if st.button("🛰️ LANZAR RASTREO"):
        if target_name:
            st.link_button(f"Abrir búsqueda para {target_name}", f"https://www.google.com/search?q=site:tiktok.com+%22{target_name}%22")
