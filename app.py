import streamlit as st
import yt_dlp
import pandas as pd
import re
import requests
import traceback
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL
# ==============================================================================
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"

st.set_page_config(
    page_title="BS LATAM",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL (SIN CAMBIOS, SOLO OPTIMIZACIÓN DE CARGA)
# ==============================================================================
st.markdown("""
    <style>
    .main { background-color: #0b0d11; color: #e6edf3; }
    .stApp { background-color: #0b0d11; }
    
    .title-box { 
        border-left: 15px solid #E30613; 
        padding: 35px 50px; 
        margin: 30px 0 50px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,13,17,0) 100%);
        border-radius: 0 25px 25px 0;
    }
    .m-title { 
        font-size: 46px; 
        font-weight: 900; 
        color: #ffffff; 
        text-transform: uppercase; 
        letter-spacing: 7px; 
        margin: 0;
        line-height: 1.1;
    }
    .s-title { 
        font-size: 19px; 
        color: #8b949e; 
        font-family: 'Courier New', monospace; 
        font-weight: bold;
        margin-top: 15px;
        letter-spacing: 2px;
    }
    
    .subtotal-card {
        background-color: #161b22;
        border: 2px solid #30363d;
        padding: 25px;
        border-radius: 22px;
        text-align: center;
        transition: 0.3s ease-in-out;
    }
    .subtotal-card:hover { 
        border-color: #E30613; 
        transform: translateY(-10px);
    }
    .sub-v { color: #E30613; font-size: 34px; font-weight: 950; }
    .sub-l { color: #8b949e; font-size: 14px; text-transform: uppercase; letter-spacing: 1.5px; }

    code { font-size: 14px !important; color: #e6edf3 !important; background-color: #0d1117 !important; }

    [data-testid="stMetricValue"] { color: #E30613 !important; font-weight: 900; font-size: 44px !important; }

    .stButton>button { 
        background: linear-gradient(135deg, #E30613 0%, #a3050e 100%) !important;
        color: #ffffff !important; 
        font-weight: 900 !important; 
        text-transform: uppercase;
        border-radius: 18px;
        height: 80px;
        width: 100%;
        font-size: 24px !important;
        border: none;
    }
    header { visibility: visible !important; background: rgba(11,13,17,0.98) !important; border-bottom: 2px solid #30363d; }
    .stTextArea textarea { background-color: #161b22 !important; color: #e6edf3 !important; border: 2px solid #30363d !important; border-radius: 20px; }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V28</p>
        <p class="s-title">INTELIGENCIA DE DATOS • DESGLOSE RRSS • OPTIMIZACIÓN TITÁN</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GESTIÓN DE MEMORIA
# ==============================================================================
for key in ['db_final', 'db_fallidos', 'db_drive']:
    if key not in st.session_state: st.session_state[key] = pd.DataFrame()
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = [{"role": "assistant", "content": "¡V28 Optimizada! Todo el poder, misma interfaz. 🫡"}]

# ==============================================================================
# 4. MOTOR OPTIMIZADO (MULTI-THREADING PARA VELOCIDAD)
# ==============================================================================

def extraer_dato_unico(url_raw):
    """Función optimizada para procesamiento paralelo."""
    url = url_raw.strip().replace('"', '').split('?')[0].rstrip(')').rstrip(',')
    ydl_opts = {'quiet': True, 'no_warnings': True, 'skip_download': True, 'ignoreerrors': True, 'socket_timeout': 15}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                v = int(info.get('view_count') or info.get('play_count') or 0)
                if "tiktok" in url: plat = "TIKTOK"
                elif "youtube" in url or "youtu.be" in url: plat = "YOUTUBE"
                elif "facebook" in url: plat = "FACEBOOK"
                else: plat = "OTRA RED"
                return {"success": True, "Red": plat, "Creador": info.get('uploader', 'N/A'), "Vistas": v, "Enlace": url}
    except: pass
    return {"success": False, "Enlace": url, "Error": "No accesible"}

def motor_auditor_v28(urls):
    exitos, fallos = [], []
    p_bar = st.progress(0)
    
    # Optimización: Procesamos hasta 5 links al mismo tiempo para no tardar una eternidad
    with ThreadPoolExecutor(max_workers=5) as executor:
        resultados = list(executor.map(extraer_dato_unico, urls))
        
    for i, res in enumerate(resultados):
        if res["success"]:
            res["#"] = len(exitos) + 1
            del res["success"]
            exitos.append(res)
        else:
            fallos.append({"Enlace": res["Enlace"], "Error": res["Error"]})
        p_bar.progress((i + 1) / len(urls))
    
    p_bar.empty()
    return pd.DataFrame(exitos), pd.DataFrame(fallos)

# ==============================================================================
# 5. INTERFAZ Y MÓDULOS (SIN CAMBIOS VISUALES)
# ==============================================================================
with st.sidebar:
    st.markdown("<h1 style='color:#E30613; text-align:center;'>BS TITAN V28</h1>", unsafe_allow_html=True)
    menu = st.radio("SELECCIÓN", ["🚀 EXTRACTOR RRSS", "🤖 PARTNER IA PRO", "📂 DRIVE AUDITOR", "🛰️ SEARCH PRO"], label_visibility="collapsed")
    if st.button("🚨 REINICIAR"):
        st.session_state.db_final = pd.DataFrame()
        st.session_state.db_fallidos = pd.DataFrame()
        st.rerun()

if menu == "🚀 EXTRACTOR RRSS":
    txt_in = st.text_area("Pega tus links aquí:", height=200)
    if st.button("🔥 INICIAR AUDITORÍA"):
        links = re.findall(r"(https?://[^\s\"\'\)\],]+)", txt_in)
        if links:
            st.session_state.db_final = pd.DataFrame()
            ok, err = motor_auditor_v28(links)
            st.session_state.db_final, st.session_state.db_fallidos = ok, err
            st.rerun()

    if not st.session_state.db_final.empty:
        df = st.session_state.db_final
        st.divider()
        
        # TOTALES Y COPIABLES
        c1, c2 = st.columns([1, 2])
        c1.metric("VISTAS ACUMULADAS", f"{df['Vistas'].sum():,}")
        with c2:
            st.markdown("**📋 Copiar Suma Global:**")
            st.code(" + ".join([str(v) for v in df['Vistas'].tolist()]), language="text")
        
        st.markdown("### 📊 Desglose por Red")
        d1, d2, d3 = st.columns(3)
        for platform, col in zip(["TIKTOK", "YOUTUBE", "FACEBOOK"], [d1, d2, d3]):
            sub = df[df['Red'] == platform]
            v_sub = sub['Vistas'].sum()
            with col:
                st.markdown(f'<div class="subtotal-card"><div class="sub-l">{platform} ({len(sub)})</div><div class="sub-v">{v_sub:,}</div></div>', unsafe_allow_html=True)
                if v_sub > 0: st.code(" + ".join([str(v) for v in sub['Vistas'].tolist()]), language="text")

        st.dataframe(df, use_container_width=True, hide_index=True)

        if not st.session_state.db_fallidos.empty:
            st.divider()
            st.markdown("### ⚠️ Links Fallidos")
            st.error("Enlaces no procesados:")
            st.dataframe(st.session_state.db_fallidos, use_container_width=True, hide_index=True)

elif menu == "🤖 PARTNER IA PRO":
    st.subheader("🤖 IA Partner - Sumador Preciso")
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if prompt := st.chat_input("Pega tus números..."):
        st.session_state.chat_log.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            nums = re.findall(r'\d+', prompt.replace(',', '').replace('.', ''))
            if nums:
                total = sum(int(n) for n in nums)
                res = f"🔢 **Suma Total:**\n`{' + '.join(nums)}` = **{total:,}**"
            else: res = "No hay números, jefe."
            st.markdown(res)
            st.session_state.chat_log.append({"role": "assistant", "content": res})

elif menu == "📂 DRIVE AUDITOR":
    st.subheader("📂 Drive")
    st.info("Módulo activo.")

elif menu == "🛰️ SEARCH PRO":
    st.subheader("🛰️ Search")
    st.info("Buscador activo.")
