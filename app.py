"""
InterviewIQ — MVP Streamlit
A2: Clasificador STAR + G2: Gemini feedback
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
#  CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; }
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: #F7F5FF !important;
    color: #111827 !important;
}
.stApp { background: #F7F5FF !important; }
.block-container {
    max-width: 820px !important;
    padding: 0 1.2rem 2rem !important;
}
#MainMenu, footer, header { visibility: hidden; }

/* ══════════════ NAV ══════════════ */
.iq-nav {
    background: #fff;
    border-radius: 0 0 20px 20px;
    padding: 1rem 1.5rem;
    display: flex; align-items: center; justify-content: space-between;
    margin: 0 -1.2rem 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.iq-nav-logo { font-size: 1.3rem; font-weight: 800; color: #111827; letter-spacing: -0.02em; }
.iq-nav-logo span { color: #7C3AED; }
.iq-nav-pills { display: flex; gap: 0.5rem; }
.iq-pill { font-size: 0.7rem; font-weight: 700; padding: 0.28rem 0.75rem; border-radius: 20px; }
.iq-pill.p  { background: #EDE9FE; color: #7C3AED; }
.iq-pill.g  { background: #DCFCE7; color: #15803D; }
.iq-pill.y  { background: #FEF9C3; color: #A16207; }

/* ══════════════ LANDING ══════════════ */

/* Hero band */
.iq-hero-band {
    background: linear-gradient(135deg, #6D28D9 0%, #8B5CF6 55%, #A78BFA 100%);
    border-radius: 24px;
    padding: 2rem 2rem 1.5rem;
    margin-bottom: 1rem;
    position: relative; overflow: hidden;
}
.iq-hero-band::before {
    content:''; position:absolute; top:-60px; right:-60px;
    width:220px; height:220px; border-radius:50%;
    background:rgba(255,255,255,0.08);
}
.iq-hero-band::after {
    content:''; position:absolute; bottom:-40px; left:30%;
    width:150px; height:150px; border-radius:50%;
    background:rgba(255,255,255,0.05);
}
.iq-hero-top { display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; z-index:1; position:relative; }
.iq-hero-h1 { font-size:2.2rem; font-weight:800; color:#fff; letter-spacing:-0.04em; line-height:1.1; margin-bottom:0.5rem; }
.iq-hero-h1 em { font-style:normal; color:#FDE68A; }
.iq-hero-sub { font-size:0.9rem; color:rgba(255,255,255,0.82); line-height:1.6; max-width:360px; margin-bottom:1.2rem; }
.iq-hero-mascot { font-size:5rem; filter:drop-shadow(0 8px 20px rgba(0,0,0,0.25)); flex-shrink:0; animation:bob 3s ease-in-out infinite; }
@keyframes bob { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }

/* Stats chips inside hero */
.iq-hero-stats { display:flex; gap:0.75rem; flex-wrap:wrap; }
.iq-hstat {
    background:rgba(255,255,255,0.18); backdrop-filter:blur(8px);
    border:1px solid rgba(255,255,255,0.28);
    border-radius:14px; padding:0.6rem 1rem; text-align:center; min-width:90px;
}
.iq-hstat-n { font-size:1.4rem; font-weight:800; color:#fff; line-height:1; }
.iq-hstat-l { font-size:0.65rem; color:rgba(255,255,255,0.72); font-weight:600; margin-top:0.15rem; }

/* STAR explain row */
.iq-star-row { display:grid; grid-template-columns:repeat(4,1fr); gap:0.75rem; margin-bottom:1rem; }
.iq-se {
    border-radius:18px; padding:1.1rem 0.8rem; text-align:center;
    border:2px solid; cursor:default;
    transition:transform .2s, box-shadow .2s;
}
.iq-se:hover { transform:translateY(-4px); box-shadow:0 8px 24px rgba(0,0,0,0.1); }
.iq-se.s { background:#EDE9FE; border-color:#C4B5FD; }
.iq-se.t { background:#DBEAFE; border-color:#93C5FD; }
.iq-se.a { background:#FEF3C7; border-color:#FCD34D; }
.iq-se.r { background:#DCFCE7; border-color:#86EFAC; }
.iq-se-letter { font-size:1.8rem; font-weight:800; line-height:1; margin-bottom:0.3rem; }
.iq-se.s .iq-se-letter { color:#7C3AED; }
.iq-se.t .iq-se-letter { color:#2563EB; }
.iq-se.a .iq-se-letter { color:#D97706; }
.iq-se.r .iq-se-letter { color:#059669; }
.iq-se-name { font-size:0.72rem; font-weight:700; color:#374151; margin-bottom:0.3rem; }
.iq-se-desc { font-size:0.68rem; color:#6B7280; line-height:1.45; }

/* Two-col info */
.iq-info-row { display:grid; grid-template-columns:1fr 1fr; gap:0.75rem; margin-bottom:1rem; }
.iq-info-card {
    background:#fff; border-radius:18px; padding:1.2rem;
    border:1.5px solid #E9D5FF;
    box-shadow:0 2px 8px rgba(109,40,217,0.07);
}
.iq-info-card-title {
    font-size:0.75rem; font-weight:700; color:#7C3AED;
    text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.9rem;
    display:flex; align-items:center; gap:0.4rem;
}
.iq-step-mini { display:flex; align-items:flex-start; gap:0.7rem; margin-bottom:0.75rem; }
.iq-step-mini:last-child { margin-bottom:0; }
.iq-snum {
    width:26px; height:26px; border-radius:8px; flex-shrink:0;
    background:linear-gradient(135deg,#7C3AED,#A855F7); color:#fff;
    font-size:0.72rem; font-weight:800;
    display:flex; align-items:center; justify-content:center;
    box-shadow:0 3px 8px rgba(124,58,237,0.35);
}
.iq-step-mini strong { font-size:0.82rem; color:#111827; display:block; margin-bottom:0.05rem; }
.iq-step-mini span { font-size:0.72rem; color:#6B7280; line-height:1.45; }
.iq-tip-row { display:flex; align-items:flex-start; gap:0.6rem; margin-bottom:0.6rem; }
.iq-tip-row:last-child { margin-bottom:0; }
.iq-tip-icon { font-size:1rem; flex-shrink:0; margin-top:0.05rem; }
.iq-tip-row strong { font-size:0.8rem; color:#111827; display:block; margin-bottom:0.05rem; }
.iq-tip-row span { font-size:0.72rem; color:#6B7280; line-height:1.45; }

/* Notice strip */
.iq-notice-strip {
    background:#fff; border:1.5px solid #E9D5FF; border-radius:14px;
    padding:0.8rem 1rem; font-size:0.78rem; color:#6B7280; line-height:1.5;
    margin-bottom:1rem; display:flex; gap:0.7rem; align-items:center;
}
.iq-notice-strip b { color:#374151; }

/* CTA button wrapper */
.iq-cta-wrap { text-align:center; margin-bottom:0.5rem; }

/* ══════════════ ANÁLISIS ══════════════ */

/* Progress bar de pasos */
.iq-progress {
    display:flex; align-items:center; gap:0; margin-bottom:1.5rem;
    background:#fff; border-radius:16px; padding:1rem 1.2rem;
    border:1.5px solid #E9D5FF;
    box-shadow:0 2px 8px rgba(109,40,217,0.06);
}
.iq-prog-step { display:flex; align-items:center; gap:0.5rem; flex:1; }
.iq-prog-dot {
    width:32px; height:32px; border-radius:10px; flex-shrink:0;
    display:flex; align-items:center; justify-content:center;
    font-size:0.8rem; font-weight:800;
}
.iq-prog-dot.active { background:linear-gradient(135deg,#7C3AED,#A855F7); color:#fff; box-shadow:0 4px 10px rgba(124,58,237,0.4); }
.iq-prog-dot.done   { background:#DCFCE7; color:#15803D; }
.iq-prog-dot.idle   { background:#F3F4F6; color:#9CA3AF; }
.iq-prog-label { font-size:0.75rem; font-weight:700; }
.iq-prog-label.active { color:#7C3AED; }
.iq-prog-label.done   { color:#15803D; }
.iq-prog-label.idle   { color:#9CA3AF; }
.iq-prog-line { flex:1; height:2px; background:#E9D5FF; margin:0 0.3rem; border-radius:2px; }
.iq-prog-line.done { background:#A855F7; }

/* Panel contenedor blanco */
.iq-panel {
    background:#fff; border-radius:20px; padding:1.4rem;
    border:1.5px solid #E9D5FF;
    box-shadow:0 2px 12px rgba(109,40,217,0.07);
    margin-bottom:0.9rem;
}
.iq-panel-head {
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:1rem;
}
.iq-panel-title { font-size:1rem; font-weight:800; color:#111827; }
.iq-panel-badge {
    font-size:0.68rem; font-weight:700; padding:0.25rem 0.7rem; border-radius:20px;
    background:#EDE9FE; color:#7C3AED;
}

.iq-q-preview {
    background:#F5F3FF; border-left:4px solid #7C3AED;
    border-radius:0 12px 12px 0; padding:0.85rem 1rem;
    font-size:0.88rem; color:#4C1D95; font-style:italic; line-height:1.55;
    margin-top:0.6rem;
}

/* Word count */
.iq-wc { display:flex; justify-content:space-between; font-size:0.74rem; margin-top:0.6rem; color:#9CA3AF; }
.iq-wc-track { height:5px; background:#F3F4F6; border-radius:10px; overflow:hidden; margin-top:0.3rem; }
.iq-wc-fill { height:100%; border-radius:10px; }

/* Result hero */
.iq-result-hero {
    background:linear-gradient(135deg,#6D28D9 0%,#8B5CF6 60%,#A78BFA 100%);
    border-radius:20px; padding:1.6rem;
    display:flex; align-items:center; gap:1.5rem;
    margin-bottom:0.9rem;
    box-shadow:0 12px 36px rgba(109,40,217,0.35);
    position:relative; overflow:hidden;
}
.iq-result-hero::after {
    content:''; position:absolute; top:-30px; right:-30px;
    width:130px; height:130px; border-radius:50%; background:rgba(255,255,255,0.07);
}
.iq-rv { font-size:1.4rem; font-weight:800; color:#fff; line-height:1.1; margin-bottom:0.4rem; }
.iq-rd { font-size:0.85rem; color:rgba(255,255,255,0.82); line-height:1.5; }
.iq-rcomps { display:flex; gap:0.4rem; margin-top:0.7rem; flex-wrap:wrap; }
.iq-rtag {
    background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.3);
    border-radius:20px; padding:0.2rem 0.7rem;
    font-size:0.73rem; font-weight:700; color:#fff;
}

/* STAR cards resultado */
.iq-star-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:0.75rem; margin-bottom:0.9rem; }
.iq-sc { border-radius:16px; padding:1rem 0.75rem; text-align:center; border:2px solid; }
.iq-sc.present { background:linear-gradient(180deg,#F0FDF4,#fff); border-color:#86EFAC; }
.iq-sc.absent  { background:linear-gradient(180deg,#FFF1F2,#fff); border-color:#FECDD3; }
.iq-sc:hover { transform:translateY(-3px); transition:transform .2s; }
.iq-sc-emoji { font-size:1.3rem; margin-bottom:0.3rem; }
.iq-sc-letter { font-size:1.5rem; font-weight:800; line-height:1; }
.present .iq-sc-letter { color:#16A34A; }
.absent  .iq-sc-letter { color:#DC2626; }
.iq-sc-name { font-size:0.68rem; color:#9CA3AF; font-weight:600; margin:0.2rem 0 0.5rem; }
.iq-sc-badge { display:inline-block; font-size:0.62rem; font-weight:700; padding:0.18rem 0.55rem; border-radius:20px; }
.present .iq-sc-badge { background:#DCFCE7; color:#15803D; }
.absent  .iq-sc-badge { background:#FFE4E6; color:#BE123C; }
.iq-sc-prob { font-size:0.58rem; color:#CBD5E1; margin-top:0.35rem; font-family:monospace; }

/* Feedback */
.iq-fb {
    background:#fff; border:1.5px solid #E9D5FF;
    border-radius:18px; padding:1.3rem;
    margin-bottom:0.9rem;
}
.iq-fb-top {
    display:flex; justify-content:space-between; align-items:center;
    margin-bottom:0.9rem; padding-bottom:0.8rem; border-bottom:1.5px solid #F3F4F6;
}
.iq-fb-title { font-size:0.95rem; font-weight:800; color:#111827; }
.iq-mode { font-size:0.68rem; font-weight:700; padding:0.2rem 0.65rem; border-radius:20px; }
.iq-mode.ia    { background:#EDE9FE; color:#7C3AED; }
.iq-mode.rules { background:#F3F4F6; color:#6B7280; }
.iq-fb-body { font-size:0.88rem; color:#374151; line-height:1.8; }
.iq-fb-body strong { color:#111827; }

/* Plantilla */
.iq-tpl { display:grid; grid-template-columns:1fr 1fr; gap:0.6rem; margin-top:0.6rem; }
.iq-ti { background:#FAFAFA; border:1.5px solid #E5E7EB; border-radius:12px; padding:0.85rem; }
.iq-ti-l { font-size:1rem; font-weight:800; margin-bottom:0.15rem; }
.iq-ti:nth-child(1) .iq-ti-l { color:#7C3AED; }
.iq-ti:nth-child(2) .iq-ti-l { color:#2563EB; }
.iq-ti:nth-child(3) .iq-ti-l { color:#D97706; }
.iq-ti:nth-child(4) .iq-ti-l { color:#059669; }
.iq-ti-role { font-size:0.62rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; color:#9CA3AF; margin-bottom:0.35rem; }
.iq-ti-txt { font-size:0.76rem; color:#6B7280; line-height:1.5; font-style:italic; }

/* Footer */
.iq-footer { text-align:center; font-size:0.72rem; color:#D1D5DB; padding:1.5rem 0 0.5rem; border-top:1.5px solid #EDE9FE; margin-top:1.5rem; }
.iq-footer a { color:#A78BFA; text-decoration:none; }

/* ══ BUTTONS ══ */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6D28D9, #8B5CF6) !important;
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.8rem 2.2rem !important;
    box-shadow: 0 6px 22px rgba(109,40,217,0.4) !important;
    letter-spacing: -0.01em !important;
    transition: all .2s !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(109,40,217,0.5) !important;
}
.stButton > button[kind="primary"]:disabled {
    background: #E5E7EB !important; color: #9CA3AF !important; box-shadow: none !important;
}
.stButton > button:not([kind="primary"]) {
    background: #fff !important; border: 1.5px solid #DDD6FE !important;
    border-radius: 12px !important; color: #7C3AED !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 0.85rem !important;
    transition: all .2s !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: #EDE9FE !important;
}

/* ══ INPUTS ══ */
div[data-testid="stSelectbox"] > div > div {
    background:#fff !important; border:1.5px solid #DDD6FE !important;
    border-radius:12px !important; color:#111827 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important; font-size:0.9rem !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within { border-color:#8B5CF6 !important; box-shadow:0 0 0 3px rgba(139,92,246,.15) !important; }
div[data-testid="stTextArea"] textarea {
    background:#fff !important; border:1.5px solid #DDD6FE !important;
    border-radius:12px !important; color:#111827 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:0.9rem !important; line-height:1.65 !important; padding:0.9rem 1rem !important;
}
div[data-testid="stTextArea"] textarea:focus { border-color:#8B5CF6 !important; box-shadow:0 0 0 3px rgba(139,92,246,.15) !important; }
div[data-testid="stTextInput"] input {
    background:#fff !important; border:1.5px solid #DDD6FE !important;
    border-radius:12px !important; color:#111827 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
}
div[data-testid="stWidgetLabel"] label p {
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:0.8rem !important; font-weight:700 !important; color:#374151 !important;
}
.stExpander { border:1.5px solid #DDD6FE !important; border-radius:14px !important; background:#fff !important; }
div[data-testid="stExpander"] summary { font-family:'Plus Jakarta Sans',sans-serif !important; font-size:0.85rem !important; font-weight:700 !important; color:#374151 !important; }
.stSpinner > div { border-top-color:#8B5CF6 !important; }
div[data-testid="stAlert"] { border-radius:12px !important; font-family:'Plus Jakarta Sans',sans-serif !important; font-size:0.83rem !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  LÓGICA
# ══════════════════════════════════════════════════════════════════════════════
ETIQUETAS    = ['situacion','tarea','accion','resultado']
NOMBRES_STAR = {
    'situacion':('S','Situación','🌍'),
    'tarea':    ('T','Tarea',    '📋'),
    'accion':   ('A','Acción',   '⚡'),
    'resultado':('R','Resultado','🏆'),
}
MODELS_DIR = Path(__file__).parent / "models"

@st.cache_resource
def cargar_modelos():
    cfg = MODELS_DIR / "config_clasificador.json"
    if not cfg.exists(): return None, None
    with open(cfg) as f: c = json.load(f)
    u = c.get("umbrales",{"situacion":0.30,"tarea":0.30,"accion":0.75,"resultado":0.70})
    m = {}
    for et in ETIQUETAS:
        p = MODELS_DIR / f"clasificador_star_{et}.pkl"
        if not p.exists(): return None, None
        m[et] = joblib.load(p)
    return m, u

def limpiar(t):
    t = str(t).lower()
    t = re.sub(r'[^\w\s]',' ',t)
    return re.sub(r'\s+',' ',t).strip()

def predecir(resp, mods, u):
    t = limpiar(resp)
    preds, probs = {}, {}
    for et in ETIQUETAS:
        p = mods[et].predict_proba([t])[0][1]
        preds[et]=int(p>=u[et]); probs[et]=round(float(p),3)
    comps=[NOMBRES_STAR[e][0] for e,v in preds.items() if v==1]
    return {"predicciones":preds,"probabilidades":probs,
            "resumen":"-".join(comps) if comps else "Ninguno"}

SP = """Eres InterviewIQ, coach de entrevistas para universitarios peruanos. Feedback en español, cálido, máximo 170 palabras.
Situación: contexto. Tarea: tu rol. Acción: pasos en 1ª persona. Resultado: qué cambió con datos.
REGLAS: No contradigas análisis STAR. No inventes datos.
FORMATO:
**Lo que hiciste bien:** 1–2 frases.
**Lo que falta:** un punto por componente AUSENTE.
**Cómo mejorarla:** sugerencia concreta."""

def _key():
    try: return st.secrets.get("GEMINI_API_KEY","") or os.environ.get("GEMINI_API_KEY","")
    except: return os.environ.get("GEMINI_API_KEY","")
def _llm():
    try: return st.secrets.get("GEMINI_MODEL","") or "gemini-2.5-flash"
    except: return "gemini-2.5-flash"

def gen_feedback(preg, resp, res, hip=False):
    k=_key()
    if not k: return _rules(res),"rules"
    pr=res["predicciones"]
    pres=[NOMBRES_STAR[e][1] for e,v in pr.items() if v==1]
    aus =[NOMBRES_STAR[e][1] for e,v in pr.items() if v==0]
    msg=f'Pregunta:"{preg}"\nRespuesta:\n"""{resp}"""\nPRESENTES:{",".join(pres) or "ninguno"}\nAUSENTES:{",".join(aus) or "ninguno"}'
    if hip: msg+="\nALERTA:hipotética."
    try:
        import requests
        r=requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{_llm()}:generateContent",
            params={"key":k},
            json={"system_instruction":{"parts":[{"text":SP}]},
                  "contents":[{"role":"user","parts":[{"text":msg}]}],
                  "generationConfig":{"temperature":0.4,"maxOutputTokens":800}},
            timeout=25)
        r.raise_for_status()
        t=r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        if not t: raise ValueError
        return t,"ia"
    except: return _rules(res),"rules"

def _rules(res):
    pr=res["predicciones"]
    aus =[NOMBRES_STAR[e][1] for e,v in pr.items() if v==0]
    pres=[NOMBRES_STAR[e][1] for e,v in pr.items() if v==1]
    if len(pres)==4: return "🌟 **¡Respuesta STAR completa!** Los 4 componentes presentes. Cuantifica resultados con % o plazos.","rules"
    if len(pres)==0: return "**Reorganiza tu respuesta:**\n\n**S:** ¿Cuál era el contexto?\n**T:** ¿Cuál era tu rol?\n**A:** ¿Qué hiciste tú?\n**R:** ¿Qué lograste?","rules"
    sug={"Situación":"Empieza con el contexto: empresa, equipo, momento.","Tarea":"Explica tu responsabilidad específica.","Acción":"Detalla los pasos que TÚ tomaste en 1ª persona.","Resultado":"Cierra con el impacto y un dato concreto."}
    return f"**Detectamos:** {', '.join(pres)}.\n\n"+"".join(f"→ **{a}:** {sug.get(a,'')}\n\n" for a in aus),"rules"

PHIP=re.compile(r"\b(si (yo )?(tuviera|estuviera|fuera)|(yo )?(har[ií]a|intentar[ií]a|buscar[ií]a|hablar[ií]a|tratar[ií]a|propondr[ií]a)|lo que har[ií]a|deber[ií]a)\b",re.I)
def es_hip(t): return len(PHIP.findall(t))>=2

def gauge_svg(total):
    pct=total/4; r=46; circ=2*3.14159*r
    arc=circ*0.75; dash=pct*arc
    col={0:"#F87171",1:"#F87171",2:"#FCD34D",3:"#FCD34D",4:"#4ADE80"}[total]
    return f"""<svg width="100" height="100" viewBox="0 0 110 110">
  <circle cx="55" cy="55" r="{r}" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="8"
      stroke-dasharray="{arc:.1f} {circ:.1f}" stroke-linecap="round" transform="rotate(135 55 55)"/>
  <circle cx="55" cy="55" r="{r}" fill="none" stroke="{col}" stroke-width="8"
      stroke-dasharray="{dash:.1f} {circ:.1f}" stroke-linecap="round" transform="rotate(135 55 55)"
      style="filter:drop-shadow(0 0 5px {col});"/>
  <text x="55" y="51" text-anchor="middle" font-family="Plus Jakarta Sans,sans-serif" font-size="26" font-weight="800" fill="white">{total}</text>
  <text x="55" y="66" text-anchor="middle" font-family="Plus Jakarta Sans,sans-serif" font-size="10" fill="rgba(255,255,255,0.65)" font-weight="600">de 4</text>
</svg>"""

PREGUNTAS=[
    "Cuéntame de una vez que tuviste que trabajar bajo presión y cómo lo manejaste.",
    "Describe una situación en la que tuviste que resolver un conflicto en tu equipo.",
    "Cuéntame de un logro del que te sientas orgulloso/a en tu vida académica o laboral.",
    "¿Hubo alguna vez que cometiste un error importante? ¿Qué hiciste al respecto?",
    "Describe una situación en la que tuviste que convencer a alguien de tu idea.",
]

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "pagina" not in st.session_state:
    st.session_state.pagina = "landing"

# ══════════════════════════════════════════════════════════════════════════════
#  NAV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="iq-nav">
  <div class="iq-nav-logo">Interview<span>IQ</span></div>
  <div class="iq-nav-pills">
    <span class="iq-pill p">AD5018 · UTEC</span>
    <span class="iq-pill g">F1 = 0.830 ✓</span>
    <span class="iq-pill y">⚡ IA + STAR</span>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  LANDING
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.pagina == "landing":

    # Hero band
    st.markdown("""
    <div class="iq-hero-band">
      <div class="iq-hero-top">
        <div>
          <div class="iq-hero-h1">Practica tus<br>respuestas <em>STAR</em> 🎯</div>
          <div class="iq-hero-sub">
            Escribe tu respuesta a una pregunta de entrevista por competencias
            y recibe análisis automático con IA en segundos.
          </div>
          <div class="iq-hero-stats">
            <div class="iq-hstat"><div class="iq-hstat-n">0.830</div><div class="iq-hstat-l">F1 Macro</div></div>
            <div class="iq-hstat"><div class="iq-hstat-n">4</div><div class="iq-hstat-l">Componentes</div></div>
            <div class="iq-hstat"><div class="iq-hstat-n">200</div><div class="iq-hstat-l">Respuestas</div></div>
            <div class="iq-hstat"><div class="iq-hstat-n">~5s</div><div class="iq-hstat-l">Feedback</div></div>
          </div>
        </div>
        <div class="iq-hero-mascot">🤖</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Cards STAR
    st.markdown("""
    <div class="iq-star-row">
      <div class="iq-se s">
        <div class="iq-se-letter">S</div>
        <div class="iq-se-name">Situación</div>
        <div class="iq-se-desc">El contexto en que ocurrió la experiencia</div>
      </div>
      <div class="iq-se t">
        <div class="iq-se-letter">T</div>
        <div class="iq-se-name">Tarea</div>
        <div class="iq-se-desc">Tu rol y responsabilidad en ese momento</div>
      </div>
      <div class="iq-se a">
        <div class="iq-se-letter">A</div>
        <div class="iq-se-name">Acción</div>
        <div class="iq-se-desc">Pasos concretos que tomaste en 1ª persona</div>
      </div>
      <div class="iq-se r">
        <div class="iq-se-letter">R</div>
        <div class="iq-se-name">Resultado</div>
        <div class="iq-se-desc">El impacto de tus acciones, con datos</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Info row: Cómo funciona + Tips
    st.markdown("""
    <div class="iq-info-row">
      <div class="iq-info-card">
        <div class="iq-info-card-title">📋 Cómo funciona</div>
        <div class="iq-step-mini">
          <div class="iq-snum">1</div>
          <div><strong>Elige una pregunta</strong><span>Del banco de preguntas conductuales o escribe la tuya.</span></div>
        </div>
        <div class="iq-step-mini">
          <div class="iq-snum">2</div>
          <div><strong>Escribe tu respuesta</strong><span>Un caso real que hayas vivido — no hipotético.</span></div>
        </div>
        <div class="iq-step-mini">
          <div class="iq-snum">3</div>
          <div><strong>Análisis STAR con ML</strong><span>El modelo detecta qué componentes están presentes.</span></div>
        </div>
        <div class="iq-step-mini">
          <div class="iq-snum">4</div>
          <div><strong>Feedback con Gemini</strong><span>Recomiendaciones concretas basadas en tu respuesta.</span></div>
        </div>
      </div>
      <div class="iq-info-card">
        <div class="iq-info-card-title">💡 Tips para una buena respuesta</div>
        <div class="iq-tip-row">
          <span class="iq-tip-icon">✅</span>
          <div><strong>Usa verbos en 1ª persona</strong><span>"Yo organicé", "Yo propuse" — no "nosotros hicimos".</span></div>
        </div>
        <div class="iq-tip-row">
          <span class="iq-tip-icon">📏</span>
          <div><strong>50 a 150 palabras</strong><span>Respuestas muy cortas no dan contexto suficiente.</span></div>
        </div>
        <div class="iq-tip-row">
          <span class="iq-tip-icon">📊</span>
          <div><strong>Incluye datos</strong><span>"Mejoré un 30%", "en 2 semanas" — el resultado se mide.</span></div>
        </div>
        <div class="iq-tip-row">
          <span class="iq-tip-icon">🚫</span>
          <div><strong>No respondas hipotético</strong><span>Te piden un caso real, no "yo haría...".</span></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Notice
    st.markdown("""
    <div class="iq-notice-strip">
      <span>🤖</span>
      <span>Herramienta de práctica con IA — puede equivocarse y no predice resultados en entrevistas reales.&nbsp;
      <b>Privacidad (Ley N.° 29733):</b> tu respuesta se usa solo en esta sesión; evita datos personales.</span>
    </div>""", unsafe_allow_html=True)

    # CTA
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Comenzar práctica →", type="primary", use_container_width=True):
            st.session_state.pagina = "analisis"
            st.rerun()

    st.markdown("""<div class="iq-footer">
      InterviewIQ · AD5018 IA para Negocios · UTEC 2026-2 ·
      <a href="https://github.com/itslueli/InterviewIQ">GitHub</a>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ANÁLISIS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.pagina == "analisis":

    mods, umbrales = cargar_modelos()
    if mods is None:
        st.error("⚠️ Modelos no encontrados. Verifica que `models/` contiene los archivos `.pkl` y `config_clasificador.json`.")
        st.stop()

    # Progress bar
    paso_actual = st.session_state.get("paso", 1)

    def prog_dot(n, actual):
        if n < actual:   return "done",   "✓"
        if n == actual:  return "active",  str(n)
        return "idle", str(n)

    p1c, p1l = prog_dot(1, paso_actual)
    p2c, p2l = prog_dot(2, paso_actual)
    p3c, p3l = prog_dot(3, paso_actual)
    l1 = "done" if paso_actual > 1 else ""
    l2 = "done" if paso_actual > 2 else ""

    st.markdown(f"""
    <div class="iq-progress">
      <div class="iq-prog-step">
        <div class="iq-prog-dot {p1c}">{p1l}</div>
        <span class="iq-prog-label {p1c}">Pregunta</span>
      </div>
      <div class="iq-prog-line {l1}"></div>
      <div class="iq-prog-step">
        <div class="iq-prog-dot {p2c}">{p2l}</div>
        <span class="iq-prog-label {p2c}">Respuesta</span>
      </div>
      <div class="iq-prog-line {l2}"></div>
      <div class="iq-prog-step">
        <div class="iq-prog-dot {p3c}">{p3l}</div>
        <span class="iq-prog-label {p3c}">Análisis</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # Panel pregunta
    st.markdown('<div class="iq-panel"><div class="iq-panel-head"><div class="iq-panel-title">1 · Pregunta de entrevista</div><span class="iq-panel-badge">BANCO</span></div>', unsafe_allow_html=True)
    pregunta_sel = st.selectbox(
        "Elige una pregunta:",
        options=[""] + PREGUNTAS + ["✏️ Escribe tu propia pregunta..."],
        index=0, label_visibility="collapsed",
    )
    pregunta_custom = ""
    if pregunta_sel == "✏️ Escribe tu propia pregunta...":
        pregunta_custom = st.text_input("Tu pregunta:", placeholder="Escribe tu pregunta de entrevista...", label_visibility="collapsed")
        pregunta_final = pregunta_custom
    else:
        pregunta_final = pregunta_sel
    if pregunta_final:
        st.markdown(f'<div class="iq-q-preview">💬 &nbsp;"{pregunta_final}"</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # close panel — solo cierra el div visual, no wrappea widgets

    # Panel respuesta
    st.markdown('<div class="iq-panel"><div class="iq-panel-head"><div class="iq-panel-title">2 · Tu respuesta</div><span class="iq-panel-badge">STAR</span></div>', unsafe_allow_html=True)
    respuesta = st.text_area(
        "Escribe una experiencia real:",
        placeholder="Ejemplo: En mi práctica en [empresa], tuve que [tarea]. Lo que hice fue [acciones concretas]. Como resultado, [logro + datos].",
        height=160, label_visibility="collapsed",
    )
    palabras = len(respuesta.split()) if respuesta.strip() else 0
    if respuesta.strip():
        pct_w = min(palabras/150, 1.0)
        if palabras >= 50:   fc,lc,lbl = "#4ADE80","#16A34A",f"{palabras} palabras ✓"
        elif palabras >= 20: fc,lc,lbl = "#FCD34D","#D97706",f"{palabras} palabras — intenta llegar a 50"
        else:                fc,lc,lbl = "#F87171","#DC2626",f"{palabras} palabras — muy corta"
        st.markdown(f"""
        <div class="iq-wc"><span>Longitud</span><span style="color:{lc};font-weight:700;">{lbl}</span></div>
        <div class="iq-wc-track"><div class="iq-wc-fill" style="width:{int(pct_w*100)}%;background:{fc};"></div></div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Botón
    col_b1, col_b2 = st.columns([3, 1])
    with col_b1:
        analizar = st.button("Analizar respuesta →", type="primary", use_container_width=True, disabled=not respuesta.strip())
    with col_b2:
        if st.button("← Volver", use_container_width=True):
            st.session_state.pagina = "landing"
            st.session_state.pop("paso", None)
            st.rerun()

    # Resultados
    if analizar and respuesta.strip():
        st.session_state.paso = 3
        if palabras < 20:
            st.warning("Tu respuesta tiene menos de 20 palabras — el análisis puede ser impreciso.")
        if es_hip(respuesta):
            st.warning('Tu respuesta parece hipotética ("yo haría..."). Cuenta un caso real.')

        with st.spinner("Analizando componentes STAR..."):
            res = predecir(respuesta, mods, umbrales)

        total_p = sum(res["predicciones"].values())
        verdicts = {
            4:("🌟 Respuesta STAR Completa","Los 4 componentes presentes — ¡listo para la entrevista!"),
            3:("⚡ Casi perfecto","Muy buena estructura, falta un componente."),
            2:("📈 Buen inicio","Tienes la mitad — agrega los que faltan."),
            1:("💡 Falta desarrollar","Solo 1 componente — expande tu respuesta."),
            0:("🔧 Sin estructura STAR","Reorganiza usando la plantilla de abajo."),
        }
        v_title, v_desc = verdicts[total_p]
        tags = "".join(
            f'<span class="iq-rtag">{NOMBRES_STAR[e][0]} — {NOMBRES_STAR[e][1]}</span>'
            for e,v in res["predicciones"].items() if v==1
        ) or '<span class="iq-rtag" style="background:rgba(248,113,113,.25)">Sin componentes</span>'

        st.markdown(f"""
        <div class="iq-result-hero">
          <div style="flex-shrink:0">{gauge_svg(total_p)}</div>
          <div>
            <div class="iq-rv">{v_title}</div>
            <div class="iq-rd">{v_desc}</div>
            <div class="iq-rcomps">{tags}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Star cards
        cards = ""
        for et in ETIQUETAS:
            letra,nombre,emoji = NOMBRES_STAR[et]
            pres = res["predicciones"][et]==1
            prob = res["probabilidades"][et]
            u    = umbrales[et]
            cls  = "present" if pres else "absent"
            icon = "✅" if pres else "❌"
            pill = "Presente" if pres else "Ausente"
            cards += f"""<div class="iq-sc {cls}">
              <div class="iq-sc-emoji">{emoji}</div>
              <div class="iq-sc-letter">{letra}</div>
              <div class="iq-sc-name">{nombre}</div>
              <div style="font-size:1rem;margin-bottom:.35rem">{icon}</div>
              <span class="iq-sc-badge">{pill}</span>
              <div class="iq-sc-prob">p={prob:.2f} · u={u}</div>
            </div>"""
        st.markdown(f'<div class="iq-star-grid">{cards}</div>', unsafe_allow_html=True)

        # Feedback
        with st.spinner("Generando feedback personalizado..."):
            fb_txt, modo = gen_feedback(pregunta_final, respuesta, res, es_hip(respuesta))

        modo_html = (
            '<span class="iq-mode ia">🤖 Google Gemini</span>' if modo=="ia"
            else '<span class="iq-mode rules">📋 Reglas</span>'
        )
        st.markdown(f"""
        <div class="iq-fb">
          <div class="iq-fb-top">
            <div class="iq-fb-title">💬 Feedback personalizado</div>
            {modo_html}
          </div>
          <div class="iq-fb-body">{fb_txt.replace(chr(10),'<br>')}</div>
        </div>""", unsafe_allow_html=True)

        aus_et = [et for et,v in res["predicciones"].items() if v==0]
        if aus_et:
            with st.expander("Ver plantilla STAR para mejorar tu respuesta"):
                st.markdown("""
                <div class="iq-tpl">
                  <div class="iq-ti"><div class="iq-ti-l">S</div><div class="iq-ti-role">Situación</div><div class="iq-ti-txt">"En [empresa/equipo], durante [momento]..."</div></div>
                  <div class="iq-ti"><div class="iq-ti-l">T</div><div class="iq-ti-role">Tarea</div><div class="iq-ti-txt">"Mi responsabilidad era [objetivo específico]..."</div></div>
                  <div class="iq-ti"><div class="iq-ti-l">A</div><div class="iq-ti-role">Acción</div><div class="iq-ti-txt">"Lo que hice fue [pasos en primera persona]..."</div></div>
                  <div class="iq-ti"><div class="iq-ti-l">R</div><div class="iq-ti-role">Resultado</div><div class="iq-ti-txt">"Como resultado, [logro + % o dato]..."</div></div>
                </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 Analizar otra respuesta", use_container_width=True):
                st.session_state.paso = 1
                st.rerun()
        with c2:
            if st.button("🏠 Volver al inicio", use_container_width=True):
                st.session_state.pagina = "landing"
                st.session_state.pop("paso", None)
                st.rerun()

    st.markdown("""<div class="iq-footer">
      InterviewIQ · AD5018 IA para Negocios · UTEC 2026-2 ·
      <a href="https://github.com/itslueli/InterviewIQ">GitHub</a>
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    pass
