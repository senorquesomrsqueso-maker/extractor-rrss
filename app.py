import streamlit as st
import yt_dlp
import pandas as pd
import re
import time
import random
import requests
import math
from io import BytesIO

# --- 1. CONFIGURACIÓN DE SEGURIDAD Y LLAVES ---
# Tu llave oficial de Google Cloud para acceso profundo
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"

# --- 2. CONFIGURACIÓN DE PÁGINA E INTERFAZ ÉLITE ---
st.set_page_config(
    page_title="AUDIT-ELITE PRO V12",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para mantener el look profesional y oscuro
st.markdown("""
    <style>
    /* Fondo General Dark Mode */
    .main { background-color: #0b0d11; color: #e6edf3; }
    .stApp { background-color: #0b0d11; }
    header { visibility: hidden; }
    
    /* Contenedor del Título Principal con Barra Lateral Roja */
    .title-box { 
        border-left: 6px solid #E30613; 
        padding-left: 25px; 
        margin: 20px 0 35px 0; 
    }
    .main-header { font-size: 36px; font-weight: 900; color: #ffffff; margin: 0; text-transform: uppercase; letter-spacing: -1px; }
    .sub-header { font-size: 15px; color: #8b949e; margin: 0; font-weight: 400; }
    
    /* Métricas y Tablas de Datos */
    .stDataFrame td, .stDataFrame th { font-size: 11px !important; padding: 4px !important; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 18px; border-radius: 12px; }
    [data-testid="stMetricValue"] { font-size: 28px !important; color: #E30613 !important; font-weight: 800; }
    
    /* Áreas de Texto e Inputs Estilizados */
    .stTextArea textarea { font-size: 13px !important; background-color: #161b22 !important; color: #e6edf3 !important; border: 1px solid #30363d !important; border-radius: 8px; }
    .stChatInput input { background-color: #161b22 !important; color: #ffffff !important; border: 1px solid #30363d !important; }
    
    /* Botones de Acción Audit-Elite */
    .stButton>button { 
        background-color: #E30613 !important; 
        color: white !important; 
        font-weight: bold !important; 
        border-radius: 6px; 
        border: none;
        width: 100%;
        height: 50px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover { background-color: #ff1a1a !important; transform: scale(1.02); box-shadow: 0px 5px 15px rgba(227, 6, 19, 0.4); }
    
    /* Contenedores de Errores y Alertas */
    .error-container { 
        background-color: #2a1215; 
        border: 1px solid #662225; 
        padding: 20px; 
        border-radius: 10px; 
        color: #ff8888; 
        font-size: 13px;
    }
    .success-tag { color: #238636; font-weight: bold; }
    </style>
    
    <div class="title-box">
        <p class="main-header">AUDITORÍA DE EMBAJADORES V12</p>
        <p class="sub-header">Módulo de Inteligencia de Datos • RRSS • Google Cloud Drive Deep Engine</p>
    </div>
    """, unsafe_allow_html=True)

# --- 3. SISTEMA DE MEMORIA Y PERSISTENCIA (SESSION STATE) ---
if 'db_final' not in st.session_state: st.session_state.db_final = pd.DataFrame()
if 'db_fallidos' not in st.session_state: st.session_state.db_fallidos = pd.DataFrame()
if 'db_drive' not in st.session_state: st.session_state.db_drive = pd.DataFrame()
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = [
        {"role": "assistant", "content": "¡Saludos jefe! Sistema Audit-Elite V12 operando con API Key de Google. Estoy listo para procesar redes y archivos profundos. ¿Qué tenemos para hoy? 🫡"}
    ]

# --- 4. MOTOR DE EXTRACCIÓN RRSS (YOUTUBE, FACEBOOK, TIKTOK FOTO/VIDEO) ---
def motor_auditor_rrss(urls):
    exitosos, fallidos = [], []
    p_bar = st.progress(0)
    status_msg = st.empty()
    
    ydl_opts = {
        'quiet': True, 'no_warnings': True, 'extract_flat': False,
        'skip_download': True, 'ignoreerrors': True, 'socket_timeout': 30,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Referer': 'https://www.tiktok.com/',
        }
    }
    
    for i, url in enumerate(urls):
        u_clean = url.strip().replace('"', '').split('?')[0].rstrip(')').rstrip(',')
        status_msg.markdown(f"🛰️ **Analizando Redes:** `{u_clean[:50]}...`")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(u_clean, download=False)
                if info:
                    # Captura de vistas dual (Video o Foto)
                    vistas = int(info.get('view_count') or info.get('play_count') or 0)
                    autor = info.get('uploader') or info.get('creator') or "Desconocido"
                    duracion = info.get('duration', 0)
                    
                    if "tiktok" in u_clean:
                        tipo = "📸 TIKTOK FOTO" if (duracion is None or duracion <= 0) else "🎥 TIKTOK VIDEO"
                        plataforma = "TIKTOK"
                    elif "youtube" in u_clean or "youtu.be" in u_clean:
                        tipo = "🎥 YT VIDEO"
                        plataforma = "YOUTUBE"
                    else:
                        tipo = "🔗 LINK RRSS"
                        plataforma = "OTRA"

                    exitosos.append({
                        "Plataforma": plataforma,
                        "Tipo": tipo,
                        "Creador": autor,
                        "Vistas": vistas,
                        "Link": u_clean
                    })
                else:
                    fallidos.append({"Link": u_clean, "Motivo": "Sin datos públicos / Enlace Privado"})
        except Exception:
            fallos.append({"Link": u_clean, "Motivo": "Fallo de conexión técnica"})
        
        p_bar.progress((i + 1) / len(urls))
    
    p_bar.empty()
    status_msg.empty()
    return pd.DataFrame(exitosos), pd.DataFrame(fallidos)

# --- 5. MOTOR DE DRIVE PROFUNDO (GOOGLE CLOUD API ENGINE) ---
def inspector_drive_deep_api(urls):
    resultados = []
    p_bar_d = st.progress(0)
    status_d = st.empty()
    
    for i, url in enumerate(urls):
        status_d.markdown(f"📂 **Consultando API Google:** `{url[:45]}...`")
        # Extraer el ID del archivo de la URL
        file_id_match = re.search(r'[-\w]{25,}', url)
        
        if file_id_match:
            file_id = file_id_match.group()
            # Llamada oficial a Google Drive API v3
            api_endpoint = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=name,size,mimeType,description,modifiedTime&key={DRIVE_API_KEY}"
            
            try:
                r = requests.get(api_endpoint, timeout=15)
                data = r.json()
                
                if "error" not in data:
                    nombre = data.get('name', 'Archivo detectado')
                    peso_bytes = int(data.get('size', 0))
                    peso_final = f"{peso_bytes/1024/1024:.2f} MB" if peso_bytes > 0 else "N/A"
                    tipo_mime = data.get('mimeType', '')
                    
                    # Clasificación inteligente
                    if "folder" in tipo_mime: tipo_label = "📁 CARPETA"
                    elif "video" in tipo_mime: tipo_label = "🎬 VIDEO"
                    elif "image" in tipo_mime: tipo_label = "🖼️ IMAGEN"
                    else: tipo_label = "📄 DOCUMENTO"
                    
                    resultados.append({
                        "Nombre del Archivo": nombre,
                        "Tipo": tipo_label,
                        "Tamaño/Peso": peso_final,
                        "Estado": "✅ ACCESO LIBRE (API)",
                        "Última Modif.": data.get('modifiedTime', 'N/A')[:10],
                        "Link": url
                    })
                else:
                    resultados.append({"Nombre del Archivo": "🔒 Protegido", "Tipo": "???", "Tamaño/Peso": "0", "Estado": "❌ PRIVADO / BLOQUEADO", "Última Modif.": "N/A", "Link": url})
            except:
                resultados.append({"Nombre del Archivo": "ERROR", "Tipo": "ERROR", "Tamaño/Peso": "0", "Estado": "❌ ERROR API", "Última Modif.": "N/A", "Link": url})
        
        p_bar_d.progress((i + 1) / len(urls))
    
    p_bar_d.empty()
    status_d.empty()
    return pd.DataFrame(resultados)

# --- 6. NAVEGACIÓN LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='color:#E30613; text-align:center;'>BS LATAM V12</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("MÓDULOS DE SISTEMA", ["🚀 Extractor Multi-Redes", "🤖 Partner IA + Calc", "🛰️ Search Pro", "📂 Drive Auditor API"], label_visibility="collapsed")
    st.divider()
    st.info("Estado del API: **ACTIVO ✅**")
    if st.button("🗑️ REINICIO MAESTRO"):
        for k in ['db_final', 'db_fallidos', 'db_drive']: st.session_state[k] = pd.DataFrame()
        st.session_state.chat_log = [{"role": "assistant", "content": "Sistema reiniciado jefe. Memoria limpia. 🫡"}]
        st.rerun()

# --- 7. LÓGICA DE MÓDULOS ---

# MÓDULO 1: RRSS
if menu == "🚀 Extractor Multi-Redes":
    st.markdown("<p style='font-weight:bold; color:#8b949e;'>📥 INGRESO DE ENLACES RRSS:</p>", unsafe_allow_html=True)
    txt_input = st.text_area("", height=180, placeholder="Pega links de TikTok, YouTube o Facebook...")
    
    if st.button("🔍 EJECUTAR AUDITORÍA"):
        urls_found = re.findall(r"(https?://[^\s\"\'\)\],]+)", txt_input)
        if urls_found:
            with st.spinner("Conectando con servidores..."):
                df_ok, df_err = motor_auditor_rrss(urls_found)
                st.session_state.db_final = pd.concat([st.session_state.db_final, df_ok]).drop_duplicates(subset=['Link'])
                st.session_state.db_fallidos = pd.concat([st.session_state.db_fallidos, df_err]).drop_duplicates(subset=['Link'])
            st.rerun()

    if not st.session_state.db_final.empty:
        df = st.session_state.db_final
        st.markdown("### ✅ DATOS CONFIRMADOS")
        c1, c2, c3 = st.columns(3)
        c1.metric("Contenido", len(df))
        c2.metric("Vistas Totales", f"{df['Vistas'].sum():,}")
        c3.metric("Fuentes", df['Plataforma'].nunique())
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Descarga Excel
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine='xlsxwriter') as w: df.to_excel(w, index=False)
        st.download_button("📥 DESCARGAR REPORTE EXCEL", buf.getvalue(), f"Auditoria_RRSS_{int(time.time())}.xlsx")

    if not st.session_state.db_fallidos.empty:
        st.divider()
        st.markdown("### ⚠️ ENLACES NO DETECTADOS")
        st.dataframe(st.session_state.db_fallidos, use_container_width=True, hide_index=True)

# MÓDULO 2: IA Y CALCULADORA
elif menu == "🤖 Partner IA + Calc":
    st.markdown("<p style='font-weight:bold; color:#E30613; font-size:18px;'>🤖 PARTNER IA + CALCULADORA</p>", unsafe_allow_html=True)
    for m in st.session_state.chat_log:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Dime algo jefe, o pídeme un cálculo..."):
        st.session_state.chat_log.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            clean_p = prompt.lower().replace('x', '*').replace(',', '')
            math_match = re.search(r"(\d+[\s\+\-\*\/\%]+\d+)", clean_p)
            if math_match:
                try:
                    res = eval(math_match.group(1))
                    ans = f"🔢 **Resultado del Cálculo:** {math_match.group(1)} = **{res:,}**"
                except: ans = "Error matemático jefe."
            elif any(w in clean_p for w in ["hola", "como estas"]):
                ans = random.choice(["¡Al 100% jefe! ¿Qué auditamos?", "¡Excelente! API de Drive lista."])
            else: ans = "Entendido jefe. Estoy monitoreando la base de datos."
            st.markdown(ans)
            st.session_state.chat_log.append({"role": "assistant", "content": ans})

# MÓDULO 3: SEARCH (ESTÁTICO SEGÚN PETICIÓN)
elif menu == "🛰️ Search Pro":
    st.subheader("🛰️ Search Pro")
    st.info("Módulo de rastreo de canales activo. Esperando integración de API.")

# MÓDULO 4: DRIVE API (EL NUEVO "GIGANTE")
elif menu == "📂 Drive Auditor API":
    st.subheader("📂 Google Drive Deep Inspector (Official API)")
    st.write("Verificación de archivos, peso y permisos mediante Google Cloud.")
    txt_drive = st.text_area("Pega links de Drive aquí:", height=150, placeholder="https://drive.google.com/...")
    
    if st.button("⚡ INICIAR INSPECCIÓN PROFUNDA"):
        links_d = re.findall(r"(https?://drive\.google\.com/[^\s\"\'\)\],]+)", txt_drive)
        if links_d:
            with st.spinner("Accediendo a la red de Google..."):
                df_drive_new = inspector_drive_deep_api(links_d)
                st.session_state.db_drive = pd.concat([st.session_state.db_drive, df_drive_new]).drop_duplicates(subset=['Link'])
            st.rerun()
    
    if not st.session_state.db_drive.empty:
        st.markdown("### 📊 ARCHIVOS DETECTADOS EN DRIVE")
        st.dataframe(st.session_state.db_drive, use_container_width=True, hide_index=True)
        # Descarga Excel Drive
        buf_d = BytesIO()
        with pd.ExcelWriter(buf_d, engine='xlsxwriter') as w: st.session_state.db_drive.to_excel(w, index=False)
        st.download_button("📥 DESCARGAR REPORTE DRIVE", buf_d.getvalue(), "Auditoria_Drive_Deep.xlsx")
