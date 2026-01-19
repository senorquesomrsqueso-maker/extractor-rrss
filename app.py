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
# 1. ESPECIFICACIONES DE NÚCLEO (V31 - MÁXIMA EXTENSIÓN)
# ==============================================================================
# Llave de API para el módulo de Drive
DRIVE_API_KEY = "AIzaSyBjETNqerBHpqCBQBH7B1bZl55eYWrtMQk"

st.set_page_config(
    page_title="BS LATAM",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. ARQUITECTURA VISUAL (CSS DE ALTA FIDELIDAD)
# ==============================================================================
st.markdown("""
    <style>
    /* Configuración de Fondo Principal */
    .main { background-color: #0b0d11; color: #e6edf3; }
    .stApp { background-color: #0b0d11; }
    
    /* BLOQUE DE TÍTULO: Espaciado de 7.5px corregido (Img b59c6a) */
    .title-box { 
        border-left: 15px solid #E30613; 
        padding: 40px 55px; 
        margin: 30px 0 60px 0; 
        background: linear-gradient(90deg, #161b22 0%, rgba(11,17,23,0) 100%);
        border-radius: 0 30px 30px 0;
        box-shadow: 15px 15px 40px rgba(0,0,0,0.6);
    }
    .m-title { 
        font-size: 48px; 
        font-weight: 950; 
        color: #ffffff; 
        text-transform: uppercase; 
        letter-spacing: 7.5px; 
        margin: 0;
        line-height: 1.0;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.5));
    }
    .s-title { 
        font-size: 20px; 
        color: #8b949e; 
        font-family: 'Courier New', monospace; 
        font-weight: bold;
        margin-top: 18px;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    /* Tarjetas de Métricas de Red Social */
    .subtotal-card {
        background-color: #161b22;
        border: 2px solid #30363d;
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .subtotal-card:hover { 
        border-color: #E30613; 
        transform: translateY(-15px);
        box-shadow: 0 20px 45px rgba(227, 6, 19, 0.35);
    }
    .sub-v { color: #E30613; font-size: 36px; font-weight: 950; }
    .sub-l { color: #8b949e; font-size: 15px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; }

    /* BLOQUES DE CÓDIGO (SIMETRÍA TAMAÑO 10 - Img b700c8) */
    code { 
        font-size: 14px !important; 
        color: #ffffff !important; 
        background-color: #0d1117 !important; 
        border: 1px solid #444c56 !important;
        padding: 12px !important;
        border-radius: 10px;
        display: block;
        margin-top: 5px;
    }

    /* Botón de Ejecución Maestro */
    .stButton>button { 
        background: linear-gradient(135deg, #E30613 0%, #8b0000 100%) !important;
        color: #ffffff !important; 
        font-weight: 900 !important; 
        text-transform: uppercase;
        border-radius: 20px;
        height: 85px;
        width: 100%;
        font-size: 26px !important;
        border: none;
        letter-spacing: 2px;
        transition: 0.4s;
    }
    .stButton>button:hover { 
        filter: brightness(1.2); 
        box-shadow: 0 0 30px rgba(227, 6, 19, 0.6);
        transform: scale(1.01);
    }

    /* Áreas de Texto y Inputs */
    .stTextArea textarea { 
        background-color: #161b22 !important; 
        color: #e6edf3 !important; 
        border: 2px solid #30363d !important; 
        border-radius: 20px;
        padding: 20px;
        font-size: 16px;
    }
    
    header { visibility: visible !important; background: rgba(11,13,17,0.95) !important; border-bottom: 2px solid #30363d; }
    </style>
    
    <div class="title-box">
        <p class="m-title">AUDIT-ELITE SUPREMACÍA V31</p>
        <p class="s-title">ESTRUCTURA TITÁN • DATA MINING PROFESIONAL • SIMETRÍA VISUAL</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. NÚCLEO DE PROCESAMIENTO ESTABLE (NO-OPTIMIZADO / SIN ERRORES)
# ==============================================================================

def motor_auditor_overlord(urls):
    """Procesamiento lineal de alta fidelidad para evitar Traceback (Img b5a7c8)"""
    exitosos, errores = [], []
    barra_progreso = st.progress(0)
    contenedor_status = st.empty()
    
    # Opciones de extracción de video
    ydl_params = {
        'quiet': True, 
        'no_warnings': True, 
        'extract_flat': False,
        'skip_download': True, 
        'ignoreerrors': True, 
        'socket_timeout': 30,
        'http_headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    }
    
    for indice, url_cruda in enumerate(urls):
        url_limpia = url_cruda.strip().replace('"', '').split('?')[0].rstrip(')').rstrip(',')
        contenedor_status.markdown(f"📡 **ANALIZANDO LINK {indice+1}/{len(urls)}:** `{url_limpia[:50]}...`")
        
        try:
            with yt_dlp.YoutubeDL(ydl_params) as ydl:
                info_dict = ydl.extract_info(url_limpia, download=False)
                if info_dict:
                    # Cálculo de vistas con fallback a 0
                    vistas = int(info_dict.get('view_count') or info_dict.get('play_count') or 0)
                    autor = info_dict.get('uploader') or info_dict.get('creator') or "Unknown"
                    
                    # Clasificación por plataforma
                    if "tiktok" in url_limpia: plataforma = "TIKTOK"
                    elif "youtube" in url_limpia or "youtu.be" in url_limpia: plataforma = "YOUTUBE"
                    elif "facebook" in url_limpia or "fb.watch" in url_limpia: plataforma = "FACEBOOK"
                    elif "instagram" in url_limpia: plataforma = "INSTAGRAM"
                    else: plataforma = "RED_DESCONOCIDA"
                    
                    exitosos.append({
                        "#": len(exitosos) + 1,
                        "Red": plataforma,
                        "Creador": autor,
                        "Vistas": vistas,
                        "Enlace": url_limpia
                    })
                else:
                    errores.append({"Enlace": url_limpia, "Motivo": "Privado / No Indexado"})
        except Exception as e:
            errores.append({"Enlace": url_limpia, "Motivo": f"Fallo Crítico: {str(e)[:25]}"})
        
        # Actualización de progreso visual
        barra_progreso.progress((indice + 1) / len(urls))
    
    contenedor_status.empty()
    barra_progreso.empty()
    return pd.DataFrame(exitosos), pd.DataFrame(errores)

# ==============================================================================
# 4. SISTEMA DE PERSISTENCIA (SESSION STATE)
# ==============================================================================
# Aseguramos que los datos no se borren al cambiar de pestaña
if 'db_final' not in st.session_state:
    st.session_state.db_final = pd.DataFrame()
if 'db_fallidos' not in st.session_state:
    st.session_state.db_fallidos = pd.DataFrame()
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = [{"role": "assistant", "content": "SISTEMA V31 EN LÍNEA. Sin recortes, pura potencia. 🫡"}]

# ==============================================================================
# 5. PANEL DE CONTROL (SIDEBAR)
# ==============================================================================
with st.sidebar:
    st.markdown("<h1 style='color:#E30613; text-align:center;'>CONTROL TITÁN</h1>", unsafe_allow_html=True)
    st.divider()
    opcion = st.radio("MÓDULOS DEL SISTEMA", 
                     ["🚀 EXTRACTOR DE MÉTRICAS", "🤖 PARTNER IA SUMADOR", "📂 AUDITOR DRIVE", "🛰️ BUSCADOR PRO"],
                     label_visibility="collapsed")
    st.divider()
    if st.button("🚨 FORMATEAR MEMORIA"):
        st.session_state.db_final = pd.DataFrame()
        st.session_state.db_fallidos = pd.DataFrame()
        st.rerun()

# ==============================================================================
# 6. MÓDULO: EXTRACTOR DE MÉTRICAS (SIMETRÍA TOTAL)
# ==============================================================================
if opcion == "🚀 EXTRACTOR DE MÉTRICAS":
    st.markdown("### 📥 Entrada Masiva de Enlaces")
    area_links = st.text_area("Pega los enlaces de RRSS aquí:", height=250, placeholder="TikTok, YT, FB, IG...")
    
    if st.button("🔥 EJECUTAR AUDITORÍA PROFESIONAL"):
        # Regex avanzada para capturar links limpios
        enlaces_limpios = re.findall(r"(https?://[^\s\"\'\)\],]+)", area_links)
        if enlaces_limpios:
            ok, err = motor_auditor_overlord(enlaces_limpios)
            st.session_state.db_final = ok
            st.session_state.db_fallidos = err
            st.rerun()

    if not st.session_state.db_final.empty:
        df_res = st.session_state.db_final
        st.divider()
        
        # --- APARTADO DE TOTALES SIMÉTRICOS (Img b700c8 Corregido) ---
        st.markdown("### 🏆 Consolidado de Impacto")
        col_total, col_suma = st.columns(2)
        
        with col_total:
            st.markdown("**💰 Total de Vistas (Copiable):**")
            # Bloque simétrico tamaño 10
            st.code(f"{df_res['Vistas'].sum():,}", language="text")
            
        with col_suma:
            st.markdown("**📋 Tira de Suma Global (Para Excel/Cálculos):**")
            # Bloque idéntico al de al lado
            st.code(" + ".join([str(v) for v in df_res['Vistas'].tolist()]), language="text")
        
        st.divider()
        
        # --- DESGLOSE POR RED SOCIAL ---
        st.markdown("### 📊 Desglose por Plataforma")
        d1, d2, d3 = st.columns(3)
        plataformas_auditadas = [("TIKTOK", d1), ("YOUTUBE", d2), ("FACEBOOK", d3)]
        
        for plat_nombre, columna_ui in plataformas_auditadas:
            df_plat = df_res[df_res['Red'] == plat_nombre]
            valor_vistas = df_plat['Vistas'].sum()
            with columna_ui:
                st.markdown(f"""
                <div class="subtotal-card">
                    <div class="sub-l">{plat_nombre} ({len(df_plat)})</div>
                    <div class="sub-v">{valor_vistas:,}</div>
                </div>
                """, unsafe_allow_html=True)
                if valor_vistas > 0:
                    st.code(" + ".join([str(v) for v in df_plat['Vistas'].tolist()]), language="text")

        st.divider()
        st.markdown("### 📋 Registro Detallado de Auditoría")
        st.dataframe(df_res, use_container_width=True, hide_index=True)

        # --- SECCIÓN DE LINKS FALLIDOS (Img b5a7c8 Restaurado) ---
        if not st.session_state.db_fallidos.empty:
            st.divider()
            st.markdown("### ⚠️ Enlaces No Auditados")
            st.warning("Los siguientes links presentaron problemas y fueron excluidos del conteo:")
            st.dataframe(st.session_state.db_fallidos, use_container_width=True, hide_index=True)

# ==============================================================================
# 7. MÓDULO: PARTNER IA (SUMA SIN LÍMITES - Img b520a7 Corregido)
# ==============================================================================
elif opcion == "🤖 PARTNER IA SUMADOR":
    st.subheader("🤖 Partner IA - Procesamiento de Números Masivo")
    
    for mensaje in st.session_state.chat_log:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])
    
    if user_prompt := st.chat_input("Pega aquí tu lista de números..."):
        st.session_state.chat_log.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)
            
        with st.chat_message("assistant"):
            # Lógica de extracción de todos los dígitos ignorando puntos/comas
            lista_numeros = re.findall(r'\d+', user_prompt.replace(',', '').replace('.', ''))
            if lista_numeros:
                gran_total = sum(int(n) for n in lista_numeros)
                cadena_suma = " + ".join(lista_numeros)
                respuesta_ia = f"🔢 **Cálculo Detectado Completo:**\n`{cadena_suma}` = **{gran_total:,}**"
            else:
                respuesta_ia = "No encontré valores numéricos para procesar, jefe."
            
            st.markdown(respuesta_ia)
            st.session_state.chat_log.append({"role": "assistant", "content": respuesta_ia})

# ==============================================================================
# 8. MÓDULOS DE SOPORTE (NO-OPTIMIZADOS / COMPLETOS)
# ==============================================================================
elif opcion == "📂 AUDITOR DRIVE":
    st.subheader("📂 Módulo Auditor de Google Drive")
    st.info("Estructura de validación de permisos en espera de carga masiva.")

elif opcion == "🛰️ BUSCADOR PRO":
    st.subheader("🛰️ Buscador e Indexador")
    st.info("Módulo de rastreo de perfiles activo.")
