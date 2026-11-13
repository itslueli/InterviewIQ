"""
InterviewIQ — MVP Streamlit
A2: Clasificador STAR + G2: feedback con Gemini
AD5018 IA para Negocios — UTEC 2026-2
"""

import streamlit as st
import joblib
import json
import re
import os
from pathlib import Path

st.set_page_config(
    page_title="InterviewIQ",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: #ffffff !important;
    color: #111827 !important;
}
.stApp { background: #ffffff !important; }
.block-container { max-width: 760px !important; padding: 0 1.5rem 3rem !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── TOP NAV ── */
.iq-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.4rem 0 1.2rem;
    border-bottom: 1.5px solid #F3F4F6;
    margin-bottom: 2.5rem;
}
.iq-nav-logo {
    font-size: 1.3rem; font-weight: 800; color: #111827; letter-spacing: -0.02em;
}
.iq-nav-logo span { color: #7C3AED; }
.iq-nav-right { display: flex; align-items: center; gap: 0.8rem; }
.iq-nav-pill {
    background: #F5F3FF; color: #7C3AED;
    font-size: 0.72rem; font-weight: 700;
    padding: 0.3rem 0.8rem; border-radius: 20px;
    letter-spacing: 0.03em;
}
.iq-nav-pill.green { background: #ECFDF5; color: #059669; }

/* ── PAGE TITLE ── */
.iq-page-title {
    font-size: 2rem; font-weight: 800; color: #111827;
    letter-spacing: -0.03em; line-height: 1.15;
    margin-bottom: 0.5rem;
}
.iq-page-sub {
    font-size: 0.95rem; color: #6B7280; line-height: 1.6;
    margin-bottom: 2rem;
}

/* ── SECTION ── */
.iq-section {
    margin-bottom: 2rem;
}
.iq-label {
    font-size: 0.72rem; font-weight: 700; color: #9CA3AF;
    text-transform: uppercase; letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}
.iq-h2 {
    font-size: 1.1rem; font-weight: 700; color: #111827;
    margin-bottom: 0.9rem;
}

/* ── NOTICE ── */
.iq-notice {
    background: #FAFAFA;
    border: 1.5px solid #F3F4F6;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    font-size: 0.83rem; color: #6B7280; line-height: 1.6;
    margin-bottom: 2rem;
    display: flex; gap: 0.9rem; align-items: flex-start;
}
.iq-notice-ico { font-size: 1.1rem; margin-top: 0.05rem; flex-shrink: 0; }
.iq-notice b { color: #374151; }

/* ── PREGUNTA PREVIEW ── */
.iq-q-preview {
    background: #F5F3FF;
    border-left: 4px solid #7C3AED;
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.1rem;
    font-size: 0.92rem; color: #4C1D95;
    font-style: italic; line-height: 1.55;
    margin-top: 0.5rem; margin-bottom: 0;
}

/* ── BARRA PALABRAS ── */
.iq-wc {
    display: flex; justify-content: space-between;
    font-size: 0.75rem; margin-top: 0.5rem;
    color: #9CA3AF;
}
.iq-wc-track {
    height: 4px; background: #F3F4F6; border-radius: 10px;
    overflow: hidden; margin-top: 0.3rem;
}
.iq-wc-fill { height: 100%; border-radius: 10px; transition: width 0.4s; }

/* ── SEPARADOR ── */
.iq-sep {
    border: none; border-top: 1.5px solid #F3F4F6;
    margin: 2rem 0;
}

/* ── RESULTADO HEADER ── */
.iq-result-header {
    background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    display: flex; align-items: center; gap: 1.5rem;
    position: relative; overflow: hidden;
    box-shadow: 0 12px 40px rgba(124,58,237,0.3);
}
.iq-result-header::after {
    content: '';
    position: absolute; top: -40px; right: -40px;
    width: 150px; height: 150px;
    background: rgba(255,255,255,0.07); border-radius: 50%;
}
.iq-gauge-wrap { flex-shrink: 0; }
.iq-gauge-score {
    font-size: 3.2rem; font-weight: 800; color: #fff;
    line-height: 1; text-align: center;
}
.iq-gauge-den { font-size: 1rem; color: rgba(255,255,255,0.6); font-weight: 500; }
.iq-gauge-arc { display: block; margin: 0 auto 0.3rem; }
.iq-result-text { z-index: 1; }
.iq-result-verdict {
    font-size: 1.5rem; font-weight: 800; color: #fff;
    letter-spacing: -0.02em; line-height: 1.1; margin-bottom: 0.4rem;
}
.iq-result-desc { font-size: 0.88rem; color: rgba(255,255,255,0.8); line-height: 1.55; }
.iq-result-comps { margin-top: 0.8rem; display: flex; gap: 0.5rem; flex-wrap: wrap; }
.iq-comp-tag {
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px; padding: 0.2rem 0.75rem;
    font-size: 0.75rem; font-weight: 700; color: #fff;
}

/* ── STAR GRID ── */
.iq-star-grid {
    display: grid; grid-template-columns: repeat(4,1fr); gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.iq-star-card {
    border-radius: 16px; padding: 1.1rem 0.8rem;
    text-align: center;
    border: 2px solid;
}
.iq-star-card.present {
    background: #F0FDF4; border-color: #86EFAC;
}
.iq-star-card.absent {
    background: #FFF1F2; border-color: #FECDD3;
}
.iq-sc-emoji { font-size: 1.4rem; margin-bottom: 0.4rem; }
.iq-sc-letter { font-size: 1.5rem; font-weight: 800; line-height: 1; }
.present .iq-sc-letter { color: #16A34A; }
.absent  .iq-sc-letter { color: #DC2626; }
.iq-sc-name { font-size: 0.7rem; color: #9CA3AF; font-weight: 600; margin: 0.2rem 0 0.5rem; }
.iq-sc-badge {
    display: inline-block; font-size: 0.65rem; font-weight: 700;
    padding: 0.2rem 0.6rem; border-radius: 20px;
}
.present .iq-sc-badge { background: #DCFCE7; color: #15803D; }
.absent  .iq-sc-badge { background: #FFE4E6; color: #BE123C; }
.iq-sc-prob { font-size: 0.6rem; color: #CBD5E1; margin-top: 0.4rem; font-family: monospace; }

/* ── FEEDBACK BOX ── */
.iq-feedback {
    background: #FAFAFA;
    border: 1.5px solid #E5E7EB;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.iq-feedback-top {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 1rem; padding-bottom: 0.9rem;
    border-bottom: 1.5px solid #F3F4F6;
}
.iq-feedback-title { font-size: 0.95rem; font-weight: 700; color: #111827; }
.iq-mode-pill {
    font-size: 0.68rem; font-weight: 700;
    padding: 0.2rem 0.65rem; border-radius: 20px;
}
.iq-mode-pill.ia    { background: #EDE9FE; color: #7C3AED; }
.iq-mode-pill.rules { background: #F3F4F6; color: #6B7280; }
.iq-feedback-body {
    font-size: 0.9rem; color: #374151; line-height: 1.8;
}
.iq-feedback-body strong { color: #111827; }

/* ── PLANTILLA ── */
.iq-tpl {
    display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem;
    margin-top: 0.5rem;
}
.iq-tpl-item {
    background: #fff; border: 1.5px solid #E5E7EB;
    border-radius: 12px; padding: 0.9rem;
}
.iq-tpl-l { font-size: 1.1rem; font-weight: 800; margin-bottom: 0.15rem; }
.iq-tpl-item:nth-child(1) .iq-tpl-l { color: #7C3AED; }
.iq-tpl-item:nth-child(2) .iq-tpl-l { color: #0EA5E9; }
.iq-tpl-item:nth-child(3) .iq-tpl-l { color: #F59E0B; }
.iq-tpl-item:nth-child(4) .iq-tpl-l { color: #10B981; }
.iq-tpl-role { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #9CA3AF; margin-bottom: 0.4rem; }
.iq-tpl-txt { font-size: 0.78rem; color: #6B7280; line-height: 1.55; font-style: italic; }

/* ── FOOTER ── */
.iq-footer {
    text-align: center; font-size: 0.75rem; color: #D1D5DB;
    padding: 2rem 0 1rem;
    border-top: 1.5px solid #F3F4F6; margin-top: 2.5rem;
}
.iq-footer a { color: #A78BFA; text-decoration: none; }

/* ── STREAMLIT NATIVE OVERRIDES ── */
div[data-testid="stSelectbox"] > div > div {
    background: #fff !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 12px !important;
    color: #111827 !important;
    font-size: 0.92rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #A78BFA !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.15) !important;
}
div[data-testid="stTextArea"] textarea {
    background: #fff !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 12px !important;
    color: #111827 !important;
    font-size: 0.92rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    line-height: 1.65 !important;
    padding: 0.9rem 1rem !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: #A78BFA !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.15) !important;
}
div[data-testid="stTextInput"] input {
    background: #fff !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 12px !important;
    color: #111827 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stButton > button[kind="primary"] {
    background: #7C3AED !important;
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 1.6rem !important;
    box-shadow: 0 4px 14px rgba(124,58,237,0.3) !important;
    transition: opacity .2s !important;
}
.stButton > button[kind="primary"]:hover { opacity: 0.85 !important; }
.stButton > button[kind="primary"]:disabled {
    background: #E5E7EB !important; color: #9CA3AF !important;
    box-shadow: none !important;
}
.stButton > button:not([kind="primary"]) {
    background: #fff !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 12px !important;
    color: #374151 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}
.stButton > button:not([kind="primary"]):hover {
    border-color: #A78BFA !important;
    color: #7C3AED !important;
}
.stExpander {
    border: 1.5px solid #E5E7EB !important;
    border-radius: 14px !important;
    background: #fff !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.88rem !important; font-weight: 600 !important;
    color: #374151 !important;
}
.stSpinner > div { border-top-color: #7C3AED !important; }
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.85rem !important;
}
/* label de st.text_area / selectbox */
div[data-testid="stWidgetLabel"] label p {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important; font-weight: 600 !important;
    color: #374151 !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
ETIQUETAS   = ['situacion', 'tarea', 'accion', 'resultado']
NOMBRES_STAR = {
    'situacion': ('S', 'Situación', '🌍'),
    'tarea':     ('T', 'Tarea',     '📋'),
    'accion':    ('A', 'Acción',    '⚡'),
    'resultado': ('R', 'Resultado', '🏆'),
}
MODELS_DIR = Path(__file__).parent / "models"

@st.cache_resource
def cargar_modelos():
    cfg = MODELS_DIR / "config_clasificador.json"
    if not cfg.exists():
        return None, None
    with open(cfg) as f:
        config = json.load(f)
    umbrales = config.get("umbrales", {
        "situacion": 0.30, "tarea": 0.30, "accion": 0.75, "resultado": 0.70
    })
    mods = {}
    for et in ETIQUETAS:
        p = MODELS_DIR / f"clasificador_star_{et}.pkl"
        if not p.exists():
            return None, None
        mods[et] = joblib.load(p)
    return mods, umbrales

def limpiar(t):
    t = str(t).lower()
    t = re.sub(r'[^\w\s]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

def predecir(resp, mods, umbrales):
    t = limpiar(resp)
    preds, probs = {}, {}
    for et in ETIQUETAS:
        prob = mods[et].predict_proba([t])[0][1]
        preds[et] = int(prob >= umbrales[et])
        probs[et]  = round(float(prob), 3)
    comps = [NOMBRES_STAR[e][0] for e, v in preds.items() if v == 1]
    return {"predicciones": preds, "probabilidades": probs,
            "resumen": "-".join(comps) if comps else "Ninguno",
            "componentes_presentes": comps}

GUIA_STAR = """GUÍA STAR (contexto fijo):
- Situación: contexto concreto — dónde, cuándo, con quién.
- Tarea: responsabilidad específica del candidato.
- Acción: pasos concretos en 1ª persona.
- Resultado: qué cambió, con dato si es posible.
- 100–250 palabras ideal. No respuestas hipotéticas."""

SYSTEM_PROMPT = f"""Eres InterviewIQ, coach de entrevistas por competencias para universitarios peruanos.
Feedback en español, cálido y directo, máximo 170 palabras.
{GUIA_STAR}
REGLAS: No contradigas el análisis STAR. No inventes datos. No prometas resultados.
FORMATO:
**Lo que hiciste bien:** 1–2 frases.
**Lo que falta:** un punto por componente AUSENTE.
**Cómo mejorarla:** sugerencia concreta."""

def _apikey():
    try: return st.secrets.get("GEMINI_API_KEY","") or os.environ.get("GEMINI_API_KEY","")
    except: return os.environ.get("GEMINI_API_KEY","")

def _llm():
    try: return st.secrets.get("GEMINI_MODEL","") or "gemini-2.5-flash"
    except: return "gemini-2.5-flash"

def feedback(preg, resp, res, hip=False):
    key = _apikey()
    if not key:
        return _reglas(res), "rules"
    pr = res["predicciones"]
    pres = [NOMBRES_STAR[e][1] for e,v in pr.items() if v==1]
    aus  = [NOMBRES_STAR[e][1] for e,v in pr.items() if v==0]
    msg = f'Pregunta: "{preg or "libre"}"\nRespuesta:\n"""{resp}"""\nAnálisis STAR:\n- PRESENTES: {", ".join(pres) or "ninguno"}\n- AUSENTES: {", ".join(aus) or "ninguno"}'
    if hip: msg += "\nALERTA: hipotética, pídele caso real."
    try:
        import requests
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{_llm()}:generateContent"
        body = {
            "system_instruction": {"parts":[{"text":SYSTEM_PROMPT}]},
            "contents":[{"role":"user","parts":[{"text":msg}]}],
            "generationConfig":{"temperature":0.4,"maxOutputTokens":800},
        }
        r = requests.post(url, params={"key":key}, json=body, timeout=25)
        r.raise_for_status()
        txt = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        if not txt: raise ValueError
        return txt, "ia"
    except:
        return _reglas(res), "rules"

def _reglas(res):
    pr = res["predicciones"]
    aus  = [NOMBRES_STAR[e][1] for e,v in pr.items() if v==0]
    pres = [NOMBRES_STAR[e][1] for e,v in pr.items() if v==1]
    if len(pres)==4: return "🌟 **¡Respuesta STAR completa!** Tu respuesta incluye los 4 componentes. Cuantifica tus resultados con números o porcentajes para potenciarla."
    if len(pres)==0: return "**Reorganiza tu respuesta con la estructura STAR:**\n\n**S — Situación:** ¿Cuál era el contexto?\n**T — Tarea:** ¿Cuál era tu rol?\n**A — Acción:** ¿Qué hiciste tú?\n**R — Resultado:** ¿Qué lograste?"
    sug = {"Situación":"Empieza con el contexto: empresa, equipo, momento.","Tarea":"Explica tu responsabilidad específica.","Acción":"Detalla los pasos que TÚ tomaste en primera persona.","Resultado":"Cierra con el impacto de tus acciones, con datos si puedes."}
    return f"**Detectamos:** {', '.join(pres)}.\n\n" + "".join(f"→ **{a}:** {sug.get(a,'')}\n\n" for a in aus)

PATRON_HIP = re.compile(r"\b(si (yo )?(tuviera|estuviera|fuera)|(yo )?(har[ií]a|intentar[ií]a|buscar[ií]a|hablar[ií]a|tratar[ií]a|propondr[ií]a)|lo que har[ií]a|deber[ií]a)\b", re.I)
def es_hip(t): return len(PATRON_HIP.findall(t)) >= 2

PREGUNTAS = [
    "Cuéntame de una vez que tuviste que trabajar bajo presión y cómo lo manejaste.",
    "Describe una situación en la que tuviste que resolver un conflicto en tu equipo.",
    "Cuéntame de un logro del que te sientas orgulloso/a en tu vida académica o laboral.",
    "¿Hubo alguna vez que cometiste un error importante? ¿Qué hiciste al respecto?",
    "Describe una situación en la que tuviste que convencer a alguien de tu idea.",
]

def gauge_svg(total):
    pct = total / 4
    r = 48; circ = 2*3.14159*r
    arc = circ * 0.75; dash = pct * arc
    col = {0:"#F87171",1:"#F87171",2:"#FCD34D",3:"#FCD34D",4:"#4ADE80"}[total]
    return f"""<svg width="120" height="120" viewBox="0 0 120 120" class="iq-gauge-arc">
  <circle cx="60" cy="60" r="{r}" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="9"
      stroke-dasharray="{arc:.1f} {circ:.1f}" stroke-linecap="round" transform="rotate(135 60 60)"/>
  <circle cx="60" cy="60" r="{r}" fill="none" stroke="{col}" stroke-width="9"
      stroke-dasharray="{dash:.1f} {circ:.1f}" stroke-linecap="round" transform="rotate(135 60 60)"
      style="filter:drop-shadow(0 0 6px {col});transition:stroke-dasharray .8s ease;"/>
  <text x="60" y="55" text-anchor="middle" font-family="Plus Jakarta Sans,sans-serif"
      font-size="28" font-weight="800" fill="white">{total}</text>
  <text x="60" y="72" text-anchor="middle" font-family="Plus Jakarta Sans,sans-serif"
      font-size="11" fill="rgba(255,255,255,0.6)" font-weight="600">de 4</text>
</svg>"""

# ══════════════════════════════════════════════════════════════════════════════
#  UI
# ══════════════════════════════════════════════════════════════════════════════
def main():
    mods, umbrales = cargar_modelos()

    # NAV
    st.markdown("""
    <div class="iq-nav">
      <div class="iq-nav-logo">Interview<span>IQ</span></div>
      <div class="iq-nav-right">
        <span class="iq-nav-pill">UTEC · AD5018</span>
        <span class="iq-nav-pill green">F1 = 0.830 ✓</span>
      </div>
    </div>""", unsafe_allow_html=True)

    if mods is None:
        st.error("⚠️ Modelos no encontrados. Verifica que `models/` contiene los archivos `.pkl` y `config_clasificador.json`.")
        st.stop()

    # TÍTULO
    st.markdown("""
    <div class="iq-page-title">Entrena tu respuesta de entrevista</div>
    <div class="iq-page-sub">
        Escribe una respuesta real, detectamos los componentes <strong>STAR</strong>
        y recibes feedback personalizado al instante.
    </div>""", unsafe_allow_html=True)

    # NOTICE
    st.markdown("""
    <div class="iq-notice">
      <span class="iq-notice-ico">🤖</span>
      <span>Esta herramienta usa IA para detectar componentes STAR y generar feedback. Es una práctica — puede equivocarse y no predice resultados en entrevistas reales. <b>Privacidad (Ley N.° 29733):</b> tu respuesta se usa solo en esta sesión; evita datos personales.</span>
    </div>""", unsafe_allow_html=True)

    # ── PASO 1 ────────────────────────────────────────────────────────────────
    st.markdown('<div class="iq-label">Paso 1 · Pregunta de entrevista</div>', unsafe_allow_html=True)

    pregunta_sel = st.selectbox(
        "Elige una pregunta del banco o escribe la tuya:",
        options=[""] + PREGUNTAS + ["✏️ Escribe tu propia pregunta..."],
        index=0,
    )
    pregunta_custom = ""
    if pregunta_sel == "✏️ Escribe tu propia pregunta...":
        pregunta_custom = st.text_input("Tu pregunta:", placeholder="Escribe aquí...")
        pregunta_final = pregunta_custom
    else:
        pregunta_final = pregunta_sel

    if pregunta_final:
        st.markdown(f'<div class="iq-q-preview">💬 &nbsp;"{pregunta_final}"</div>', unsafe_allow_html=True)

    st.markdown('<hr class="iq-sep">', unsafe_allow_html=True)

    # ── PASO 2 ────────────────────────────────────────────────────────────────
    st.markdown('<div class="iq-label">Paso 2 · Tu respuesta</div>', unsafe_allow_html=True)

    respuesta = st.text_area(
        "Escribe una experiencia real (recuerda: Situación → Tarea → Acción → Resultado):",
        placeholder="Ejemplo: En mi práctica en [empresa], tuve que [tarea]. Lo que hice fue [acciones]. Como resultado, [logro con datos].",
        height=175,
    )

    palabras = len(respuesta.split()) if respuesta.strip() else 0
    if respuesta.strip():
        pct_w = min(palabras / 150, 1.0)
        if palabras >= 50:
            fc, lc, lbl = "#4ADE80", "#16A34A", f"{palabras} palabras ✓ buena longitud"
        elif palabras >= 20:
            fc, lc, lbl = "#FCD34D", "#D97706", f"{palabras} palabras — intenta llegar a 50"
        else:
            fc, lc, lbl = "#F87171", "#DC2626", f"{palabras} palabras — muy corta"
        st.markdown(f"""
        <div class="iq-wc">
            <span>Longitud</span>
            <span style="color:{lc};font-weight:600;">{lbl}</span>
        </div>
        <div class="iq-wc-track">
            <div class="iq-wc-fill" style="width:{int(pct_w*100)}%;background:{fc};"></div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="iq-sep">', unsafe_allow_html=True)

    # ── BOTÓN ─────────────────────────────────────────────────────────────────
    analizar = st.button(
        "Analizar mi respuesta →",
        type="primary",
        use_container_width=True,
        disabled=not respuesta.strip(),
    )

    # ── RESULTADOS ────────────────────────────────────────────────────────────
    if analizar and respuesta.strip():
        if palabras < 20:
            st.warning("Tu respuesta tiene menos de 20 palabras — el análisis puede ser impreciso. Cuenta el caso con más detalle.")
        if es_hip(respuesta):
            st.warning('Tu respuesta parece hipotética ("yo haría..."). En competencias te piden un caso real que hayas vivido.')

        with st.spinner("Analizando componentes STAR..."):
            res = predecir(respuesta, mods, umbrales)

        total_p = sum(res["predicciones"].values())

        verdicts = {
            4: ("🌟 Respuesta STAR Completa", "Excelente — tienes los 4 componentes. ¡Listo para la entrevista!"),
            3: ("⚡ Casi perfecto — falta 1", "Muy buena estructura. Solo un componente por agregar."),
            2: ("📈 Buen inicio — faltan 2", "Tienes la mitad. Agrega los componentes que faltan para una respuesta sólida."),
            1: ("💡 Falta desarrollar más", "Solo 1 componente detectado. Expande tu respuesta con más detalle."),
            0: ("🔧 Sin estructura STAR", "No se detectaron componentes. Reorganiza usando la plantilla de abajo."),
        }
        v_title, v_desc = verdicts[total_p]
        tags_html = "".join(
            f'<span class="iq-comp-tag">{NOMBRES_STAR[e][0]} — {NOMBRES_STAR[e][1]}</span>'
            for e, v in res["predicciones"].items() if v == 1
        )

        # Resultado hero
        st.markdown(f"""
        <div class="iq-result-header">
          <div class="iq-gauge-wrap">{gauge_svg(total_p)}</div>
          <div class="iq-result-text">
            <div class="iq-result-verdict">{v_title}</div>
            <div class="iq-result-desc">{v_desc}</div>
            <div class="iq-result-comps">{tags_html if tags_html else '<span class="iq-comp-tag" style="background:rgba(248,113,113,0.25)">Sin componentes detectados</span>'}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Cards STAR
        cards = ""
        for et in ETIQUETAS:
            letra, nombre, emoji = NOMBRES_STAR[et]
            pres = res["predicciones"][et] == 1
            prob = res["probabilidades"][et]
            u = umbrales[et]
            cls = "present" if pres else "absent"
            pill = "Presente" if pres else "Ausente"
            icon = "✅" if pres else "❌"
            cards += f"""
            <div class="iq-star-card {cls}">
              <div class="iq-sc-emoji">{emoji}</div>
              <div class="iq-sc-letter">{letra}</div>
              <div class="iq-sc-name">{nombre}</div>
              <div style="font-size:1.1rem;margin-bottom:0.4rem;">{icon}</div>
              <span class="iq-sc-badge">{pill}</span>
              <div class="iq-sc-prob">p={prob:.2f} · u={u}</div>
            </div>"""
        st.markdown(f'<div class="iq-star-grid">{cards}</div>', unsafe_allow_html=True)

        st.markdown('<hr class="iq-sep">', unsafe_allow_html=True)
        st.markdown('<div class="iq-label">Feedback personalizado</div>', unsafe_allow_html=True)

        with st.spinner("Generando feedback..."):
            fb_txt, modo = feedback(pregunta_final, respuesta, res, es_hip(respuesta))

        modo_html = (
            '<span class="iq-mode-pill ia">🤖 Gemini</span>'
            if modo == "ia" else
            '<span class="iq-mode-pill rules">📋 Reglas</span>'
        )
        st.markdown(f"""
        <div class="iq-feedback">
          <div class="iq-feedback-top">
            <div class="iq-feedback-title">Análisis de tu respuesta</div>
            {modo_html}
          </div>
          <div class="iq-feedback-body">
            {fb_txt.replace(chr(10), '<br>')}
          </div>
        </div>""", unsafe_allow_html=True)

        # Plantilla
        aus_et = [et for et, v in res["predicciones"].items() if v == 0]
        if aus_et:
            with st.expander("Ver plantilla STAR"):
                st.markdown("""
                <div class="iq-tpl">
                  <div class="iq-tpl-item">
                    <div class="iq-tpl-l">S</div>
                    <div class="iq-tpl-role">Situación</div>
                    <div class="iq-tpl-txt">"En [empresa/equipo], durante [momento], nos enfrentamos a [contexto]..."</div>
                  </div>
                  <div class="iq-tpl-item">
                    <div class="iq-tpl-l">T</div>
                    <div class="iq-tpl-role">Tarea</div>
                    <div class="iq-tpl-txt">"Mi responsabilidad era [objetivo específico tuyo]..."</div>
                  </div>
                  <div class="iq-tpl-item">
                    <div class="iq-tpl-l">A</div>
                    <div class="iq-tpl-role">Acción</div>
                    <div class="iq-tpl-txt">"Lo que hice fue [pasos concretos en primera persona]..."</div>
                  </div>
                  <div class="iq-tpl-item">
                    <div class="iq-tpl-l">R</div>
                    <div class="iq-tpl-role">Resultado</div>
                    <div class="iq-tpl-txt">"Como resultado, [logro + dato: %, tiempo, reconocimiento]..."</div>
                  </div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<hr class="iq-sep">', unsafe_allow_html=True)
        if st.button("← Analizar otra respuesta", use_container_width=True):
            st.rerun()

    # FOOTER
    st.markdown("""
    <div class="iq-footer">
      InterviewIQ · AD5018 IA para Negocios · UTEC 2026-2 ·
      <a href="https://github.com/itslueli/InterviewIQ">GitHub</a>
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
