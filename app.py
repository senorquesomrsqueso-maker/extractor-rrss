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
from io import BytesIO

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL (V34 - MÁXIMA EXTENSIÓN)
# ==============================================================================
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"

st.set_page_config(
    page_title="BS LATAM",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CAPA DE DISEÑO VISUAL (BS LATAM RGB & ESPACIADO PROFESIONAL)
# ==============================================================================
st.markdown("""
    <style>
    /* Fondo Industrial Dark Principal */
    .main { background-color: #0b0d11; color: #e6edf3; }
    .stApp { background-color: #0b0d11; }
    
    /* BLOQUE DE TÍTULO: Espaciado masivo de 12px para evitar encimamiento (Img b59c6a) */
    .title-box { 
        border-left: 15px solid #E30613; 
        padding: 50px 70px; 
        margin: 30px 0 70px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,17,23,0) 100%);
        border-radius: 0 45px 45px 0;
        box-shadow: 25px 25px 60px rgba(0,0,0,0.9);
    }
    .m-title { 
        font-size: 54px; 
        font-weight: 950; 
        color: #ffffff; 
        text-transform: uppercase; 
        letter-spacing: 12px; 
        margin: 0;
        line-height: 1.2;
    }
    .s-title { 
        font-size: 22px; 
        color: #8b949e; 
        font-family: 'Courier New', monospace; 
        font-weight: bold;
        margin-top: 25px;
        letter-spacing: 6px;
        text-transform: uppercase;
    }

    /* BS LATAM - ESTILO RGB (Sombreado Negro y Resplandor Azul) */
    .bs-latam-sidebar {
        color: #ffffff;
        font-weight: 900;
        font-size: 36px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 4px;
        text-shadow: 4px 4px 0px #000000, 0px 0px 15px #0055ff, 0px 0px 30px #00aaff;
        margin-bottom: 30px;
        padding: 10px;
    }
    
    /* BLOQUES DE CÓDIGO (SIMETRÍA TAMAÑO 10 - Img b700c8) */
    code { 
        font-size: 14px !important; 
        color: #ffffff !important; 
        background-color: #161b22 !important; 
        border: 2px solid #30363d !important;
        padding: 20px !important;
        border-radius: 18px;
        display: block;
        margin-top: 10px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.7);
    }

    /* Tarjetas de Métricas de Red Social */
    .subtotal-card {
        background-color: #161b22;
        border: 2px solid #30363d;
        padding: 40px;
        border-radius: 35px;
        text-align: center;
        transition: 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .subtotal-card:hover { 
        border-color: #E30613; 
        transform: translateY(-12px);
        box-shadow: 0 15px 40px rgba(227, 6, 19, 0.2);
    }
    .sub-v { color: #E30613; font-size: 42px; font-weight: 950; }
    .sub-l { color: #8b949e; font-size: 17px; text-transform: uppercase; letter-spacing: 3px; }

    /* Botón Maestro BS LATAM */
    .stButton>button { 
        background: linear-gradient(135deg, #E30613 0%, #8b0000 100%) !important;
        color: #ffffff !important; 
        font-weight: 950 !important; 
        text-transform: uppercase;
        border-radius: 25px;
        height: 95px;
        font-size: 30px !important;
        border: none;
        letter-spacing: 5px;
        transition: 0.4s;
    }
    .stButton>button:hover { 
        filter: brightness(1.2); 
        box-shadow: 0 0 40px rgba(227, 6, 19, 0.5);
    }
    
    header { visibility: visible !important; background: rgba(11,13,17,0.98) !important; border-bottom: 2px solid #30363d; }
    .stTextArea textarea { background-color: #161b22 !important; color: #e6edf3 !important; border: 2px solid #30363d !important; border-radius: 25px; padding: 25px; }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V34</p>
        <p class="s-title">INTELIGENCIA BS LATAM • EXTRACCIÓN MASIVA • CERO ERRORES</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. MOTOR DE AUDITORÍA (ESTABILIDAD PROFESIONAL SIN FALLOS)
# ==============================================================================

def motor_auditor_bs_latam_pro(urls):
    """Procesamiento detallado para evitar Traceback (Img b5a7c8)"""
    exitosos, fallidos = [], []
    progreso_visual = st.progress(0)
    estado_texto = st.empty()
    
    ydl_opts = {
        'quiet': True, 
        'no_warnings': True, 
        'extract_flat': False,
        'skip_download': True, 
        'ignoreerrors': True, 
        'socket_timeout': 40,
        'http_headers': {'User-Agent': 'Mozilla/5.0'}
    }
    
    for i, u_raw in enumerate(urls):
        url = u_raw.strip().replace('"', '').split('?')[0].rstrip(')').rstrip(',')
        estado_texto.markdown(f"📡 **Auditoría BS LATAM en progreso:** `{url[:55]}...`")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    # Captura de vistas real
                    v_real = int(info.get('view_count') or info.get('play_count') or 0)
                    autor_real = info.get('uploader') or info.get('creator') or "N/A"
                    
                    # Clasificación por Red
                    if "tiktok" in url: plt = "TIKTOK"
                    elif "youtube" in url or "youtu.be" in url: plt = "YOUTUBE"
                    elif "facebook" in url: plt = "FACEBOOK"
                    else: plt = "OTRA RED"
                    
                    exitosos.append({
                        "#": len(exitosos) + 1,
                        "Red": plt,
                        "Creador": autor_real,
                        "Vistas": v_real,
                        "Enlace": url
                    })
                else:
                    fallidos.append({"Enlace": url, "Motivo": "Privado o Inaccesible"})
        except Exception as e:
            fallidos.append({"Enlace": url, "Motivo": f"Error: {str(e)[:25]}"})
        
        progreso_visual.progress((i + 1) / len(urls))
    
    estado_texto.empty()
    progreso_visual.empty()
    return pd.DataFrame(exitosos), pd.DataFrame(fallidos)

# ==============================================================================
# 4. GESTIÓN DE SESIÓN Y PERSISTENCIA
# ==============================================================================
if 'db_final' not in st.session_state: st.session_state.db_final = pd.DataFrame()
if 'db_fallidos' not in st.session_state: st.session_state.db_fallidos = pd.DataFrame()

# ==============================================================================
# 5. SIDEBAR: CONTROL MAESTRO BS LATAM
# ==============================================================================
with st.sidebar:
    st.markdown('<p class="bs-latam-sidebar">BS LATAM</p>', unsafe_allow_html=True)
    st.divider()
    modulo = st.radio("SELECCIÓN", ["🚀 EXTRACTOR RRSS", "🤖 PARTNER IA", "📂 AUDITOR DRIVE"], label_visibility="collapsed")
    st.divider()
    if st.button("🚨 FORMATEAR SISTEMA"):
        st.session_state.db_final = pd.DataFrame()
        st.session_state.db_fallidos = pd.DataFrame()
        st.rerun()

# ==============================================================================
# 6. MÓDULO EXTRACTOR (CORRECCIÓN DE SIMETRÍA Y DATOS REALES)
# ==============================================================================
if modulo == "🚀 EXTRACTOR RRSS":
    st.markdown("### 📥 Entrada de Auditoría")
    user_input = st.text_area("Pega los links aquí:", height=200, placeholder="Enlaces de TikTok, YT, FB...")
    
    if st.button("🔥 INICIAR AUDITORÍA BS LATAM"):
        links_detectados = re.findall(r"(https?://[^\s\"\'\)\],]+)", user_input)
        if links_detectados:
            st.session_state.db_final = pd.DataFrame()
            ok, err = motor_auditor_bs_latam_pro(links_detectados)
            st.session_state.db_final = ok
            st.session_state.db_fallidos = err
            st.rerun()

    if not st.session_state.db_final.empty:
        df_audit = st.session_state.db_final
        st.divider()
        
        # --- APARTADO DE TOTALES SIMÉTRICOS (Corrigiendo Img b700c8 y b75a87) ---
        st.markdown("### 🏆 Consolidado de Impacto")
        col_total, col_tira = st.columns(2)
        
        with col_total:
            st.markdown("**💰 Vistas Totales (Copiable):**")
            # Bloque simétrico tamaño 10
            st.code(f"{df_audit['Vistas'].sum():,}", language="text")
            
        with col_tira:
            st.markdown("**📋 Tira de Suma (Valores Reales):**")
            # CORRECCIÓN: Aquí aparecen los números reales, no ceros.
            st.code(" + ".join([str(v) for v in df_audit['Vistas'].tolist()]), language="text")
        
        st.divider()
        
        # --- SUBTOTALES POR PLATAFORMA ---
        st.markdown("### 📊 Desglose por Red Social")
        d1, d2, d3 = st.columns(3)
        plataformas = [("TIKTOK", d1), ("YOUTUBE", d2), ("FACEBOOK", d3)]
        
        for p_name, p_col in plataformas:
            df_sub = df_audit[df_audit['Red'] == p_name]
            v_sub = df_sub['Vistas'].sum()
            with p_col:
                st.markdown(f'<div class="subtotal-card"><div class="sub-l">{p_name} ({len(df_sub)})</div><div class="sub-v">{v_sub:,}</div></div>', unsafe_allow_html=True)
                if v_sub > 0:
                    st.code(" + ".join([str(v) for v in df_sub['Vistas'].tolist()]), language="text")

        st.divider()
        st.markdown("### 📝 Listado Detallado de Auditoría")
        st.dataframe(df_audit, use_container_width=True, hide_index=True)

        # --- SECCIÓN DE ENLACES FALLIDOS (Img b5a7c8 Restaurado) ---
        if not st.session_state.db_fallidos.empty:
            st.divider()
            st.markdown("### ⚠️ Enlaces Fallidos Detectados")
            st.warning("Los siguientes links presentaron problemas y fueron excluidos del conteo:")
            st.dataframe(st.session_state.db_fallidos, use_container_width=True, hide_index=True)

# --- MÓDULO IA ---
elif modulo == "🤖 PARTNER IA":
    st.subheader("🤖 Sumador IA de Precisión")
    p_chat = st.chat_input("Pega tus números aquí...")
    if p_chat:
        numeros = re.findall(r'\d+', p_chat.replace(',', '').replace('.', ''))
        if numeros:
            total_ia = sum(int(n) for n in numeros)
            st.code(f"{' + '.join(numeros)} = {total_ia:,}")
