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

# ══════════════════════════════════════════════════════════════════════════════
#  CSS GLOBAL
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: #ffffff !important;
    color: #111827 !important;
}
.stApp { background: #ffffff !important; }
.block-container { max-width: 780px !important; padding: 0 1.5rem 3rem !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── NAV ── */
.iq-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.4rem 0 1.2rem;
    border-bottom: 1.5px solid #F3F4F6;
    margin-bottom: 2.5rem;
}
.iq-nav-logo { font-size: 1.25rem; font-weight: 800; color: #111827; letter-spacing: -0.02em; }
.iq-nav-logo span { color: #7C3AED; }
.iq-nav-pill {
    background: #F5F3FF; color: #7C3AED;
    font-size: 0.7rem; font-weight: 700;
    padding: 0.25rem 0.75rem; border-radius: 20px;
    margin-left: 0.5rem;
}
.iq-nav-pill.g { background: #ECFDF5; color: #059669; }

/* ─────────────────────────────────────────────────────
   LANDING PAGE
───────────────────────────────────────────────────── */

/* Hero central */
.iq-hero-center {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
.iq-hero-icon {
    display: inline-flex; align-items: center; justify-content: center;
    width: 80px; height: 80px; border-radius: 24px;
    background: linear-gradient(135deg, #7C3AED, #A855F7);
    font-size: 2.2rem;
    box-shadow: 0 12px 35px rgba(124,58,237,0.35);
    margin-bottom: 1.5rem;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
}
.iq-hero-h1 {
    font-size: 2.8rem; font-weight: 800; color: #111827;
    letter-spacing: -0.04em; line-height: 1.1;
    margin-bottom: 0.6rem;
}
.iq-hero-h1 span { color: #7C3AED; }
.iq-hero-sub {
    font-size: 1.05rem; color: #6B7280; line-height: 1.65;
    max-width: 480px; margin: 0 auto 2rem;
}

/* Stats row */
.iq-stats {
    display: flex; justify-content: center; gap: 2rem;
    margin-bottom: 2.5rem; flex-wrap: wrap;
}
.iq-stat {
    text-align: center;
}
.iq-stat-num {
    font-size: 1.8rem; font-weight: 800; color: #7C3AED;
    letter-spacing: -0.03em; line-height: 1;
}
.iq-stat-lbl { font-size: 0.75rem; color: #9CA3AF; font-weight: 600; margin-top: 0.2rem; }

/* STAR cards explicativas */
.iq-star-explain {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem;
    margin: 0 auto 2.5rem; max-width: 680px;
}
.iq-se-card {
    border-radius: 16px; padding: 1.1rem 0.75rem; text-align: center;
    border: 2px solid;
    transition: transform .2s;
}
.iq-se-card:hover { transform: translateY(-4px); }
.iq-se-card:nth-child(1) { background: #F5F3FF; border-color: #DDD6FE; }
.iq-se-card:nth-child(2) { background: #EFF6FF; border-color: #BFDBFE; }
.iq-se-card:nth-child(3) { background: #FFFBEB; border-color: #FDE68A; }
.iq-se-card:nth-child(4) { background: #ECFDF5; border-color: #A7F3D0; }
.iq-se-letter {
    font-size: 1.8rem; font-weight: 800; line-height: 1; margin-bottom: 0.3rem;
}
.iq-se-card:nth-child(1) .iq-se-letter { color: #7C3AED; }
.iq-se-card:nth-child(2) .iq-se-letter { color: #2563EB; }
.iq-se-card:nth-child(3) .iq-se-letter { color: #D97706; }
.iq-se-card:nth-child(4) .iq-se-letter { color: #059669; }
.iq-se-name { font-size: 0.75rem; font-weight: 700; color: #374151; margin-bottom: 0.3rem; }
.iq-se-desc { font-size: 0.72rem; color: #6B7280; line-height: 1.45; }

/* Cómo funciona */
.iq-steps {
    background: #FAFAFA; border: 1.5px solid #F3F4F6;
    border-radius: 20px; padding: 1.8rem 2rem;
    margin-bottom: 2.5rem; text-align: left;
}
.iq-steps-title {
    font-size: 0.72rem; font-weight: 700; color: #9CA3AF;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1.2rem;
    text-align: center;
}
.iq-step-row {
    display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 1rem;
}
.iq-step-row:last-child { margin-bottom: 0; }
.iq-step-num {
    width: 32px; height: 32px; border-radius: 10px; flex-shrink: 0;
    background: linear-gradient(135deg, #7C3AED, #A855F7);
    color: #fff; font-size: 0.8rem; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 10px rgba(124,58,237,0.3);
}
.iq-step-info strong { font-size: 0.9rem; color: #111827; display: block; margin-bottom: 0.1rem; }
.iq-step-info span { font-size: 0.8rem; color: #6B7280; line-height: 1.5; }

/* Notice landing */
.iq-notice-sm {
    background: #fff; border: 1.5px solid #F3F4F6;
    border-radius: 12px; padding: 0.8rem 1rem;
    font-size: 0.78rem; color: #9CA3AF; line-height: 1.5;
    margin-bottom: 1rem; text-align: center;
}
.iq-notice-sm b { color: #6B7280; }

/* ─────────────────────────────────────────────────────
   ANÁLISIS PAGE
───────────────────────────────────────────────────── */
.iq-sep { border: none; border-top: 1.5px solid #F3F4F6; margin: 2rem 0; }
.iq-label {
    font-size: 0.72rem; font-weight: 700; color: #9CA3AF;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;
}
.iq-q-preview {
    background: #F5F3FF; border-left: 4px solid #7C3AED;
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.1rem; font-size: 0.9rem; color: #4C1D95;
    font-style: italic; line-height: 1.55; margin-top: 0.5rem;
}
.iq-wc { display: flex; justify-content: space-between; font-size: 0.75rem; margin-top: 0.5rem; color: #9CA3AF; }
.iq-wc-track { height: 4px; background: #F3F4F6; border-radius: 10px; overflow: hidden; margin-top: 0.3rem; }
.iq-wc-fill { height: 100%; border-radius: 10px; transition: width 0.4s; }

/* Result header */
.iq-result-header {
    background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
    border-radius: 20px; padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    display: flex; align-items: center; gap: 1.5rem;
    box-shadow: 0 12px 40px rgba(124,58,237,0.3);
    position: relative; overflow: hidden;
}
.iq-result-header::after {
    content:''; position:absolute; top:-40px; right:-40px;
    width:150px; height:150px;
    background:rgba(255,255,255,0.07); border-radius:50%;
}
.iq-result-verdict { font-size:1.5rem; font-weight:800; color:#fff; line-height:1.1; margin-bottom:0.4rem; }
.iq-result-desc { font-size:0.88rem; color:rgba(255,255,255,0.8); line-height:1.55; }
.iq-result-comps { display:flex; gap:0.5rem; margin-top:0.8rem; flex-wrap:wrap; }
.iq-comp-tag {
    background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.3);
    border-radius:20px; padding:0.2rem 0.75rem;
    font-size:0.75rem; font-weight:700; color:#fff;
}

/* STAR result grid */
.iq-star-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:0.75rem; margin-bottom:1.5rem; }
.iq-star-card { border-radius:16px; padding:1.1rem 0.8rem; text-align:center; border:2px solid; }
.iq-star-card.present { background:#F0FDF4; border-color:#86EFAC; }
.iq-star-card.absent  { background:#FFF1F2; border-color:#FECDD3; }
.iq-sc-emoji { font-size:1.4rem; margin-bottom:0.4rem; }
.iq-sc-letter { font-size:1.5rem; font-weight:800; line-height:1; }
.present .iq-sc-letter { color:#16A34A; }
.absent  .iq-sc-letter { color:#DC2626; }
.iq-sc-name { font-size:0.7rem; color:#9CA3AF; font-weight:600; margin:0.2rem 0 0.5rem; }
.iq-sc-badge { display:inline-block; font-size:0.65rem; font-weight:700; padding:0.2rem 0.6rem; border-radius:20px; }
.present .iq-sc-badge { background:#DCFCE7; color:#15803D; }
.absent  .iq-sc-badge { background:#FFE4E6; color:#BE123C; }
.iq-sc-prob { font-size:0.6rem; color:#CBD5E1; margin-top:0.4rem; font-family:monospace; }

/* Feedback */
.iq-feedback {
    background:#FAFAFA; border:1.5px solid #E5E7EB;
    border-radius:16px; padding:1.5rem; margin-bottom:1rem;
}
.iq-feedback-top {
    display:flex; justify-content:space-between; align-items:center;
    margin-bottom:1rem; padding-bottom:0.9rem; border-bottom:1.5px solid #F3F4F6;
}
.iq-feedback-title { font-size:0.95rem; font-weight:700; color:#111827; }
.iq-mode-pill { font-size:0.68rem; font-weight:700; padding:0.2rem 0.65rem; border-radius:20px; }
.iq-mode-pill.ia    { background:#EDE9FE; color:#7C3AED; }
.iq-mode-pill.rules { background:#F3F4F6; color:#6B7280; }
.iq-feedback-body { font-size:0.9rem; color:#374151; line-height:1.8; }
.iq-feedback-body strong { color:#111827; }

/* Template */
.iq-tpl { display:grid; grid-template-columns:1fr 1fr; gap:0.6rem; margin-top:0.5rem; }
.iq-tpl-item { background:#fff; border:1.5px solid #E5E7EB; border-radius:12px; padding:0.9rem; }
.iq-tpl-l { font-size:1.1rem; font-weight:800; margin-bottom:0.15rem; }
.iq-tpl-item:nth-child(1) .iq-tpl-l { color:#7C3AED; }
.iq-tpl-item:nth-child(2) .iq-tpl-l { color:#0EA5E9; }
.iq-tpl-item:nth-child(3) .iq-tpl-l { color:#F59E0B; }
.iq-tpl-item:nth-child(4) .iq-tpl-l { color:#10B981; }
.iq-tpl-role { font-size:0.65rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; color:#9CA3AF; margin-bottom:0.4rem; }
.iq-tpl-txt { font-size:0.78rem; color:#6B7280; line-height:1.55; font-style:italic; }

/* Footer */
.iq-footer { text-align:center; font-size:0.75rem; color:#D1D5DB; padding:2rem 0 1rem; border-top:1.5px solid #F3F4F6; margin-top:2.5rem; }
.iq-footer a { color:#A78BFA; text-decoration:none; }

/* ── BUTTONS OVERRIDE ── */
.stButton > button[kind="primary"] {
    background: #7C3AED !important;
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    box-shadow: 0 4px 18px rgba(124,58,237,0.35) !important;
    transition: opacity .2s, transform .2s !important;
    letter-spacing: -0.01em !important;
}
.stButton > button[kind="primary"]:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }
.stButton > button[kind="primary"]:disabled { background: #E5E7EB !important; color: #9CA3AF !important; box-shadow: none !important; }
.stButton > button:not([kind="primary"]) {
    background: #fff !important; border: 1.5px solid #E5E7EB !important;
    border-radius: 12px !important; color: #374151 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
}
.stButton > button:not([kind="primary"]):hover { border-color: #A78BFA !important; color: #7C3AED !important; }

/* ── INPUTS ── */
div[data-testid="stSelectbox"] > div > div {
    background:#fff !important; border:1.5px solid #E5E7EB !important;
    border-radius:12px !important; color:#111827 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important; font-size:0.92rem !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within { border-color:#A78BFA !important; box-shadow:0 0 0 3px rgba(167,139,250,.15) !important; }
div[data-testid="stTextArea"] textarea {
    background:#fff !important; border:1.5px solid #E5E7EB !important;
    border-radius:12px !important; color:#111827 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:0.92rem !important; line-height:1.65 !important; padding:0.9rem 1rem !important;
}
div[data-testid="stTextArea"] textarea:focus { border-color:#A78BFA !important; box-shadow:0 0 0 3px rgba(167,139,250,.15) !important; }
div[data-testid="stTextInput"] input {
    background:#fff !important; border:1.5px solid #E5E7EB !important;
    border-radius:12px !important; color:#111827 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
}
div[data-testid="stWidgetLabel"] label p {
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:0.82rem !important; font-weight:600 !important; color:#374151 !important;
}
.stExpander { border:1.5px solid #E5E7EB !important; border-radius:14px !important; background:#fff !important; }
div[data-testid="stExpander"] summary { font-family:'Plus Jakarta Sans',sans-serif !important; font-size:0.88rem !important; font-weight:600 !important; color:#374151 !important; }
.stSpinner > div { border-top-color:#7C3AED !important; }
div[data-testid="stAlert"] { border-radius:12px !important; font-family:'Plus Jakarta Sans',sans-serif !important; font-size:0.85rem !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTES / MODELOS
# ══════════════════════════════════════════════════════════════════════════════
ETIQUETAS    = ['situacion', 'tarea', 'accion', 'resultado']
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
    if not cfg.exists(): return None, None
    with open(cfg) as f: config = json.load(f)
    umbrales = config.get("umbrales", {"situacion":0.30,"tarea":0.30,"accion":0.75,"resultado":0.70})
    mods = {}
    for et in ETIQUETAS:
        p = MODELS_DIR / f"clasificador_star_{et}.pkl"
        if not p.exists(): return None, None
        mods[et] = joblib.load(p)
    return mods, umbrales

def limpiar(t):
    t = str(t).lower()
    t = re.sub(r'[^\w\s]',' ',t)
    return re.sub(r'\s+',' ',t).strip()

def predecir(resp, mods, umbrales):
    t = limpiar(resp)
    preds, probs = {}, {}
    for et in ETIQUETAS:
        prob = mods[et].predict_proba([t])[0][1]
        preds[et] = int(prob >= umbrales[et])
        probs[et]  = round(float(prob), 3)
    comps = [NOMBRES_STAR[e][0] for e,v in preds.items() if v==1]
    return {"predicciones":preds,"probabilidades":probs,
            "resumen":"-".join(comps) if comps else "Ninguno",
            "componentes_presentes":comps}

GUIA_STAR = "Situación: contexto. Tarea: tu rol. Acción: pasos en 1ª persona. Resultado: qué cambió con datos."
SYSTEM_PROMPT = f"""Eres InterviewIQ, coach de entrevistas para universitarios peruanos. Feedback en español, cálido, máximo 170 palabras.
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

def feedback_fn(preg, resp, res, hip=False):
    key = _apikey()
    if not key: return _reglas(res), "rules"
    pr = res["predicciones"]
    pres=[NOMBRES_STAR[e][1] for e,v in pr.items() if v==1]
    aus =[NOMBRES_STAR[e][1] for e,v in pr.items() if v==0]
    msg=f'Pregunta:"{preg or "libre"}"\nRespuesta:\n"""{resp}"""\nPRESENTES:{",".join(pres) or "ninguno"}\nAUSENTES:{",".join(aus) or "ninguno"}'
    if hip: msg+="\nALERTA:hipotética."
    try:
        import requests
        r=requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{_llm()}:generateContent",
            params={"key":key},
            json={"system_instruction":{"parts":[{"text":SYSTEM_PROMPT}]},
                  "contents":[{"role":"user","parts":[{"text":msg}]}],
                  "generationConfig":{"temperature":0.4,"maxOutputTokens":800}},
            timeout=25)
        r.raise_for_status()
        txt=r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        if not txt: raise ValueError
        return txt,"ia"
    except: return _reglas(res),"rules"

def _reglas(res):
    pr=res["predicciones"]
    aus =[NOMBRES_STAR[e][1] for e,v in pr.items() if v==0]
    pres=[NOMBRES_STAR[e][1] for e,v in pr.items() if v==1]
    if len(pres)==4: return "🌟 **¡Respuesta STAR completa!** Tu respuesta incluye los 4 componentes. Cuantifica tus resultados con números o porcentajes para potenciarla."
    if len(pres)==0: return "**Reorganiza tu respuesta:**\n\n**S:** ¿Cuál era el contexto?\n**T:** ¿Cuál era tu rol?\n**A:** ¿Qué hiciste tú?\n**R:** ¿Qué lograste?"
    sug={"Situación":"Empieza con el contexto: empresa, equipo, momento.","Tarea":"Explica tu responsabilidad específica.","Acción":"Detalla los pasos que TÚ tomaste en primera persona.","Resultado":"Cierra con el impacto, con datos si puedes."}
    return f"**Detectamos:** {', '.join(pres)}.\n\n"+"".join(f"→ **{a}:** {sug.get(a,'')}\n\n" for a in aus)

PATRON_HIP=re.compile(r"\b(si (yo )?(tuviera|estuviera|fuera)|(yo )?(har[ií]a|intentar[ií]a|buscar[ií]a|hablar[ií]a|tratar[ií]a|propondr[ií]a)|lo que har[ií]a|deber[ií]a)\b",re.I)
def es_hip(t): return len(PATRON_HIP.findall(t))>=2

PREGUNTAS=[
    "Cuéntame de una vez que tuviste que trabajar bajo presión y cómo lo manejaste.",
    "Describe una situación en la que tuviste que resolver un conflicto en tu equipo.",
    "Cuéntame de un logro del que te sientas orgulloso/a en tu vida académica o laboral.",
    "¿Hubo alguna vez que cometiste un error importante? ¿Qué hiciste al respecto?",
    "Describe una situación en la que tuviste que convencer a alguien de tu idea.",
]

def gauge_svg(total):
    pct=total/4; r=48; circ=2*3.14159*r
    arc=circ*0.75; dash=pct*arc
    col={0:"#F87171",1:"#F87171",2:"#FCD34D",3:"#FCD34D",4:"#4ADE80"}[total]
    return f"""<svg width="110" height="110" viewBox="0 0 120 120">
  <circle cx="60" cy="60" r="{r}" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="9"
      stroke-dasharray="{arc:.1f} {circ:.1f}" stroke-linecap="round" transform="rotate(135 60 60)"/>
  <circle cx="60" cy="60" r="{r}" fill="none" stroke="{col}" stroke-width="9"
      stroke-dasharray="{dash:.1f} {circ:.1f}" stroke-linecap="round" transform="rotate(135 60 60)"
      style="filter:drop-shadow(0 0 6px {col});"/>
  <text x="60" y="55" text-anchor="middle" font-family="Plus Jakarta Sans,sans-serif"
      font-size="28" font-weight="800" fill="white">{total}</text>
  <text x="60" y="72" text-anchor="middle" font-family="Plus Jakarta Sans,sans-serif"
      font-size="11" fill="rgba(255,255,255,0.65)" font-weight="600">de 4</text>
</svg>"""

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "pagina" not in st.session_state:
    st.session_state.pagina = "landing"

# ══════════════════════════════════════════════════════════════════════════════
#  NAV — siempre visible
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="iq-nav">
  <div class="iq-nav-logo">Interview<span>IQ</span></div>
  <div>
    <span class="iq-nav-pill">UTEC · AD5018</span>
    <span class="iq-nav-pill g">F1 = 0.830 ✓</span>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA: LANDING
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.pagina == "landing":

    st.markdown("""
    <div class="iq-hero-center">
      <div class="iq-hero-icon">🎙️</div>
      <div class="iq-hero-h1">Practica tus<br>respuestas <span>STAR</span></div>
      <div class="iq-hero-sub">
        Escribe tu respuesta a una pregunta de entrevista por competencias
        y recibe análisis automático + feedback personalizado con IA.
      </div>
    </div>""", unsafe_allow_html=True)

    # Stats
    st.markdown("""
    <div class="iq-stats">
      <div class="iq-stat">
        <div class="iq-stat-num">0.830</div>
        <div class="iq-stat-lbl">F1 Macro del modelo</div>
      </div>
      <div class="iq-stat">
        <div class="iq-stat-num">4</div>
        <div class="iq-stat-lbl">Componentes STAR</div>
      </div>
      <div class="iq-stat">
        <div class="iq-stat-num">200</div>
        <div class="iq-stat-lbl">Respuestas de entrenamiento</div>
      </div>
      <div class="iq-stat">
        <div class="iq-stat-num">~5s</div>
        <div class="iq-stat-lbl">Feedback al instante</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Cards STAR explicativas
    st.markdown("""
    <div class="iq-star-explain">
      <div class="iq-se-card">
        <div class="iq-se-letter">S</div>
        <div class="iq-se-name">Situación</div>
        <div class="iq-se-desc">El contexto en el que ocurrió la experiencia</div>
      </div>
      <div class="iq-se-card">
        <div class="iq-se-letter">T</div>
        <div class="iq-se-name">Tarea</div>
        <div class="iq-se-desc">Tu rol y responsabilidad específica en ese momento</div>
      </div>
      <div class="iq-se-card">
        <div class="iq-se-letter">A</div>
        <div class="iq-se-name">Acción</div>
        <div class="iq-se-desc">Los pasos concretos que tomaste en primera persona</div>
      </div>
      <div class="iq-se-card">
        <div class="iq-se-letter">R</div>
        <div class="iq-se-name">Resultado</div>
        <div class="iq-se-desc">El impacto de tus acciones, idealmente con datos</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Cómo funciona
    st.markdown("""
    <div class="iq-steps">
      <div class="iq-steps-title">Cómo funciona</div>
      <div class="iq-step-row">
        <div class="iq-step-num">1</div>
        <div class="iq-step-info">
          <strong>Elige una pregunta de entrevista</strong>
          <span>Selecciona del banco de preguntas conductuales o escribe la tuya propia.</span>
        </div>
      </div>
      <div class="iq-step-row">
        <div class="iq-step-num">2</div>
        <div class="iq-step-info">
          <strong>Escribe tu respuesta real</strong>
          <span>Cuenta una experiencia que hayas vivido — no hipotética. Mínimo 20 palabras.</span>
        </div>
      </div>
      <div class="iq-step-row">
        <div class="iq-step-num">3</div>
        <div class="iq-step-info">
          <strong>Análisis STAR automático</strong>
          <span>Un modelo de ML detecta qué componentes STAR están presentes o ausentes.</span>
        </div>
      </div>
      <div class="iq-step-row">
        <div class="iq-step-num">4</div>
        <div class="iq-step-info">
          <strong>Feedback personalizado con IA</strong>
          <span>Gemini genera recomendaciones concretas basadas en el análisis de tu respuesta.</span>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Notice + botón
    st.markdown("""
    <div class="iq-notice-sm">
      🤖 Herramienta de práctica — puede equivocarse y no predice resultados reales. &nbsp;·&nbsp;
      🔒 <b>Privacidad (Ley N.° 29733):</b> tu respuesta se usa solo en esta sesión.
    </div>""", unsafe_allow_html=True)

    _, c, _ = st.columns([1, 2, 1])
    with c:
        if st.button("Comenzar práctica →", type="primary", use_container_width=True):
            st.session_state.pagina = "analisis"
            st.rerun()

    st.markdown("""
    <div class="iq-footer">
      InterviewIQ · AD5018 IA para Negocios · UTEC 2026-2 ·
      <a href="https://github.com/itslueli/InterviewIQ">GitHub</a>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA: ANÁLISIS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.pagina == "analisis":

    mods, umbrales = cargar_modelos()
    if mods is None:
        st.error("⚠️ Modelos no encontrados. Verifica que `models/` contiene los archivos `.pkl` y `config_clasificador.json`.")
        st.stop()

    # Back link
    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("← Volver"):
            st.session_state.pagina = "landing"
            st.rerun()

    # Título
    st.markdown("""
    <div style="margin-bottom:1.8rem;">
      <div style="font-size:1.6rem;font-weight:800;color:#111827;letter-spacing:-0.03em;margin-bottom:0.3rem;">
        Analiza tu respuesta
      </div>
      <div style="font-size:0.9rem;color:#6B7280;line-height:1.55;">
        Elige una pregunta, escribe tu respuesta real y presiona analizar.
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Paso 1 ────────────────────────────────────────────────────────────────
    st.markdown('<div class="iq-label">Paso 1 · Pregunta de entrevista</div>', unsafe_allow_html=True)
    pregunta_sel = st.selectbox(
        "Elige una pregunta del banco o escribe la tuya:",
        options=[""] + PREGUNTAS + ["✏️ Escribe tu propia pregunta..."],
        index=0,
    )
    pregunta_custom = ""
    if pregunta_sel == "✏️ Escribe tu propia pregunta...":
        pregunta_custom = st.text_input("Tu pregunta:", placeholder="Escribe aquí tu pregunta de entrevista...")
        pregunta_final = pregunta_custom
    else:
        pregunta_final = pregunta_sel

    if pregunta_final:
        st.markdown(f'<div class="iq-q-preview">💬 &nbsp;"{pregunta_final}"</div>', unsafe_allow_html=True)

    st.markdown('<hr class="iq-sep">', unsafe_allow_html=True)

    # ── Paso 2 ────────────────────────────────────────────────────────────────
    st.markdown('<div class="iq-label">Paso 2 · Tu respuesta</div>', unsafe_allow_html=True)
    respuesta = st.text_area(
        "Escribe una experiencia real (Situación → Tarea → Acción → Resultado):",
        placeholder="Ejemplo: En mi práctica en [empresa], tuve que [tarea específica]. Lo que hice fue [acciones concretas]. Como resultado, [logro + datos].",
        height=175,
    )

    palabras = len(respuesta.split()) if respuesta.strip() else 0
    if respuesta.strip():
        pct_w = min(palabras / 150, 1.0)
        if palabras >= 50:
            fc, lc, lbl = "#4ADE80", "#16A34A", f"{palabras} palabras ✓"
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

    # ── Botón analizar ────────────────────────────────────────────────────────
    analizar = st.button(
        "Analizar mi respuesta →",
        type="primary",
        use_container_width=True,
        disabled=not respuesta.strip(),
    )

    # ── Resultados ────────────────────────────────────────────────────────────
    if analizar and respuesta.strip():
        if palabras < 20:
            st.warning("Tu respuesta tiene menos de 20 palabras — el análisis puede ser impreciso.")
        if es_hip(respuesta):
            st.warning('Tu respuesta parece hipotética ("yo haría..."). Te pedimos un caso real que hayas vivido.')

        with st.spinner("Analizando componentes STAR..."):
            res = predecir(respuesta, mods, umbrales)

        total_p = sum(res["predicciones"].values())
        verdicts = {
            4: ("🌟 Respuesta STAR Completa", "Excelente — los 4 componentes presentes. ¡Listo!"),
            3: ("⚡ Casi perfecto", "Muy buena estructura, falta un componente."),
            2: ("📈 Buen inicio", "Tienes la mitad — agrega los que faltan."),
            1: ("💡 Falta desarrollar", "Solo 1 componente — expande tu respuesta."),
            0: ("🔧 Sin estructura STAR", "Reorganiza usando la plantilla de abajo."),
        }
        v_title, v_desc = verdicts[total_p]
        tags_html = "".join(
            f'<span class="iq-comp-tag">{NOMBRES_STAR[e][0]} — {NOMBRES_STAR[e][1]}</span>'
            for e,v in res["predicciones"].items() if v==1
        ) or '<span class="iq-comp-tag" style="background:rgba(248,113,113,.25)">Sin componentes</span>'

        st.markdown(f"""
        <div class="iq-result-header">
          <div style="flex-shrink:0;">{gauge_svg(total_p)}</div>
          <div>
            <div class="iq-result-verdict">{v_title}</div>
            <div class="iq-result-desc">{v_desc}</div>
            <div class="iq-result-comps">{tags_html}</div>
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
            icon = "✅" if pres else "❌"
            pill = "Presente" if pres else "Ausente"
            cards += f"""
            <div class="iq-star-card {cls}">
              <div class="iq-sc-emoji">{emoji}</div>
              <div class="iq-sc-letter">{letra}</div>
              <div class="iq-sc-name">{nombre}</div>
              <div style="font-size:1.1rem;margin-bottom:.4rem">{icon}</div>
              <span class="iq-sc-badge">{pill}</span>
              <div class="iq-sc-prob">p={prob:.2f} · u={u}</div>
            </div>"""
        st.markdown(f'<div class="iq-star-grid">{cards}</div>', unsafe_allow_html=True)

        st.markdown('<hr class="iq-sep">', unsafe_allow_html=True)
        st.markdown('<div class="iq-label">Feedback personalizado</div>', unsafe_allow_html=True)

        with st.spinner("Generando feedback..."):
            fb_txt, modo = feedback_fn(pregunta_final, respuesta, res, es_hip(respuesta))

        modo_html = (
            '<span class="iq-mode-pill ia">🤖 Gemini</span>' if modo=="ia"
            else '<span class="iq-mode-pill rules">📋 Reglas</span>'
        )
        st.markdown(f"""
        <div class="iq-feedback">
          <div class="iq-feedback-top">
            <div class="iq-feedback-title">Análisis de tu respuesta</div>
            {modo_html}
          </div>
          <div class="iq-feedback-body">{fb_txt.replace(chr(10),'<br>')}</div>
        </div>""", unsafe_allow_html=True)

        # Plantilla
        aus_et = [et for et,v in res["predicciones"].items() if v==0]
        if aus_et:
            with st.expander("Ver plantilla STAR"):
                st.markdown("""
                <div class="iq-tpl">
                  <div class="iq-tpl-item"><div class="iq-tpl-l">S</div><div class="iq-tpl-role">Situación</div><div class="iq-tpl-txt">"En [empresa/equipo], durante [momento]..."</div></div>
                  <div class="iq-tpl-item"><div class="iq-tpl-l">T</div><div class="iq-tpl-role">Tarea</div><div class="iq-tpl-txt">"Mi responsabilidad era [objetivo específico]..."</div></div>
                  <div class="iq-tpl-item"><div class="iq-tpl-l">A</div><div class="iq-tpl-role">Acción</div><div class="iq-tpl-txt">"Lo que hice fue [pasos en primera persona]..."</div></div>
                  <div class="iq-tpl-item"><div class="iq-tpl-l">R</div><div class="iq-tpl-role">Resultado</div><div class="iq-tpl-txt">"Como resultado, [logro + dato: %, tiempo]..."</div></div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<hr class="iq-sep">', unsafe_allow_html=True)
        if st.button("← Analizar otra respuesta", use_container_width=True):
            st.rerun()

    st.markdown("""
    <div class="iq-footer">
      InterviewIQ · AD5018 IA para Negocios · UTEC 2026-2 ·
      <a href="https://github.com/itslueli/InterviewIQ">GitHub</a>
    </div>""", unsafe_allow_html=True)


if __name__ == "__main__":
    pass
