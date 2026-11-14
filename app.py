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
    background: #F3F0FF !important;
    color: #111827 !important;
}
.stApp { background: #F3F0FF !important; }
.block-container {
    max-width: 800px !important;
    padding: 0 1.2rem 2rem !important;
}
#MainMenu, footer, header { visibility: hidden; }

/* NAV */
.iq-nav {
    background: #fff;
    border-radius: 0 0 20px 20px;
    padding: 1rem 1.5rem;
    display: flex; align-items: center; justify-content: space-between;
    margin: 0 -1.2rem 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
}
.iq-nav-logo { font-size: 1.3rem; font-weight: 800; color: #111827; letter-spacing: -0.02em; }
.iq-nav-logo span { color: #7C3AED; }
.iq-nav-pills { display: flex; gap: 0.5rem; }
.iq-pill { font-size: 0.7rem; font-weight: 700; padding: 0.28rem 0.75rem; border-radius: 20px; }
.iq-pill.p  { background: #EDE9FE; color: #6D28D9; }
.iq-pill.g  { background: #DCFCE7; color: #15803D; }
.iq-pill.y  { background: #FEF9C3; color: #A16207; }

/* ══════════════ LANDING ══════════════ */
.iq-hero {
    background: linear-gradient(135deg, #5B21B6 0%, #7C3AED 55%, #9C6CFE 100%);
    border-radius: 24px;
    padding: 2.2rem 2rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative; overflow: hidden;
}
.iq-hero::before {
    content:''; position:absolute; top:-70px; right:-70px;
    width:230px; height:230px; border-radius:50%;
    background:rgba(255,255,255,0.08);
}
.iq-hero-inner { display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; position:relative; z-index:1; }
.iq-h1 { font-size:2.4rem; font-weight:800; color:#fff; letter-spacing:-0.04em; line-height:1.1; margin-bottom:0.6rem; }
.iq-h1 em { font-style:normal; color:#FDE68A; }
.iq-hsub { font-size:0.92rem; color:rgba(255,255,255,0.85); line-height:1.65; max-width:360px; margin-bottom:1.4rem; }
.iq-mascot { font-size:5.5rem; flex-shrink:0; animation:bob 3s ease-in-out infinite; filter:drop-shadow(0 8px 24px rgba(0,0,0,0.3)); }
@keyframes bob { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
.iq-stats { display:flex; gap:0.8rem; flex-wrap:wrap; }
.iq-stat {
    background:rgba(255,255,255,0.18); backdrop-filter:blur(8px);
    border:1px solid rgba(255,255,255,0.3); border-radius:14px;
    padding:0.65rem 1rem; text-align:center; min-width:88px;
}
.iq-stat-n { font-size:1.5rem; font-weight:800; color:#fff; line-height:1; }
.iq-stat-l { font-size:0.63rem; color:rgba(255,255,255,0.75); font-weight:600; margin-top:0.1rem; }

/* STAR cards */
.iq-star-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:0.75rem; margin-bottom:1.2rem; }
.iq-sc {
    border-radius:18px; padding:1.1rem 0.8rem; text-align:center;
    border:2px solid; cursor:default; transition:transform .2s, box-shadow .2s;
}
.iq-sc:hover { transform:translateY(-4px); box-shadow:0 8px 24px rgba(0,0,0,0.12); }
.iq-sc.s { background:#EDE9FE; border-color:#C4B5FD; }
.iq-sc.t { background:#DBEAFE; border-color:#93C5FD; }
.iq-sc.a { background:#FEF3C7; border-color:#FCD34D; }
.iq-sc.r { background:#DCFCE7; border-color:#86EFAC; }
.iq-sc-letter { font-size:1.9rem; font-weight:800; line-height:1; margin-bottom:0.3rem; }
.iq-sc.s .iq-sc-letter { color:#6D28D9; }
.iq-sc.t .iq-sc-letter { color:#1D4ED8; }
.iq-sc.a .iq-sc-letter { color:#B45309; }
.iq-sc.r .iq-sc-letter { color:#047857; }
.iq-sc-name { font-size:0.73rem; font-weight:700; color:#1F2937; margin-bottom:0.3rem; }
.iq-sc-desc { font-size:0.68rem; color:#4B5563; line-height:1.45; }

/* Info two-col */
.iq-2col { display:grid; grid-template-columns:1fr 1fr; gap:0.75rem; margin-bottom:1.2rem; }
.iq-card {
    background:#fff; border-radius:18px; padding:1.3rem;
    border:2px solid #E9D5FF; box-shadow:0 2px 10px rgba(109,40,217,0.08);
}
.iq-card-ttl {
    font-size:0.75rem; font-weight:700; color:#6D28D9;
    text-transform:uppercase; letter-spacing:0.08em;
    margin-bottom:1rem; display:flex; align-items:center; gap:0.4rem;
}
.iq-row { display:flex; align-items:flex-start; gap:0.7rem; margin-bottom:0.75rem; }
.iq-row:last-child { margin-bottom:0; }
.iq-num {
    width:28px; height:28px; border-radius:8px; flex-shrink:0;
    background:linear-gradient(135deg,#6D28D9,#9C6CFE); color:#fff;
    font-size:0.73rem; font-weight:800;
    display:flex; align-items:center; justify-content:center;
    box-shadow:0 3px 8px rgba(109,40,217,0.35);
}
.iq-row-ttl { font-size:0.83rem; font-weight:700; color:#111827; display:block; margin-bottom:0.08rem; }
.iq-row-sub { font-size:0.72rem; color:#4B5563; line-height:1.45; }
.iq-tip-icon { font-size:1.1rem; flex-shrink:0; margin-top:0.05rem; }

/* Notice */
.iq-notice {
    background:#fff; border:2px solid #E9D5FF; border-radius:14px;
    padding:0.85rem 1rem; font-size:0.78rem; color:#4B5563;
    line-height:1.55; margin-bottom:1.2rem;
    display:flex; gap:0.7rem; align-items:center;
}
.iq-notice b { color:#1F2937; }

/* ══════════════ ANÁLISIS ══════════════ */
.iq-progress {
    display:flex; align-items:center;
    background:#fff; border-radius:16px; padding:1rem 1.4rem;
    border:2px solid #E9D5FF; box-shadow:0 2px 8px rgba(109,40,217,0.07);
    margin-bottom:1.2rem;
}
.iq-ps { display:flex; align-items:center; gap:0.5rem; flex:1; }
.iq-pd {
    width:34px; height:34px; border-radius:10px; flex-shrink:0;
    display:flex; align-items:center; justify-content:center;
    font-size:0.82rem; font-weight:800;
}
.iq-pd.active { background:linear-gradient(135deg,#6D28D9,#9C6CFE); color:#fff; box-shadow:0 4px 12px rgba(109,40,217,0.4); }
.iq-pd.done   { background:#DCFCE7; color:#15803D; }
.iq-pd.idle   { background:#F3F4F6; color:#9CA3AF; }
.iq-pl { font-size:0.76rem; font-weight:700; }
.iq-pl.active { color:#6D28D9; }
.iq-pl.done   { color:#15803D; }
.iq-pl.idle   { color:#9CA3AF; }
.iq-pline { flex:1; height:2px; background:#DDD6FE; margin:0 0.4rem; border-radius:2px; }
.iq-pline.done { background:#8B5CF6; }

/* Containers nativos como paneles */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background:#fff !important;
    border:2px solid #DDD6FE !important;
    border-radius:18px !important;
    padding:1.2rem 1.3rem !important;
    box-shadow:0 2px 12px rgba(109,40,217,0.08) !important;
    margin-bottom:1rem !important;
}

div[data-testid="stSelectbox"] > div > div {
    background:#fff !important; border:2px solid #DDD6FE !important;
    border-radius:12px !important; color:#111827 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:0.92rem !important; font-weight:500 !important;
    min-height:48px !important;
}

.iq-qpreview {
    background:#EDE9FE; border-left:4px solid #7C3AED;
    border-radius:0 12px 12px 0; padding:0.9rem 1rem;
    font-size:0.9rem; color:#3B0764; font-style:italic; line-height:1.6;
    margin-top:0.6rem; margin-bottom:0.4rem;
}

/* Word counter */
.iq-wc { display:flex; justify-content:space-between; font-size:0.75rem; margin-top:0.6rem; }
.iq-wc-label { color:#6B7280; font-weight:600; }
.iq-wc-track { height:6px; background:#F3F4F6; border-radius:10px; overflow:hidden; margin-top:0.35rem; }
.iq-wc-fill  { height:100%; border-radius:10px; transition:width .3s; }

/* Resultado hero */
.iq-rhero {
    background:linear-gradient(135deg,#5B21B6 0%,#7C3AED 60%,#9C6CFE 100%);
    border-radius:20px; padding:1.7rem;
    display:flex; align-items:center; gap:1.5rem;
    margin-bottom:1rem; box-shadow:0 12px 36px rgba(109,40,217,0.35);
    position:relative; overflow:hidden;
}
.iq-rhero::after {
    content:''; position:absolute; top:-30px; right:-30px;
    width:140px; height:140px; border-radius:50%; background:rgba(255,255,255,0.07);
}
.iq-rv { font-size:1.45rem; font-weight:800; color:#fff; line-height:1.1; margin-bottom:0.4rem; }
.iq-rd { font-size:0.87rem; color:rgba(255,255,255,0.85); line-height:1.5; }
.iq-rtags { display:flex; gap:0.4rem; margin-top:0.75rem; flex-wrap:wrap; }
.iq-rtag {
    background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.35);
    border-radius:20px; padding:0.22rem 0.75rem;
    font-size:0.74rem; font-weight:700; color:#fff;
}

/* STAR resultado cards */
.iq-rstar { display:grid; grid-template-columns:repeat(4,1fr); gap:0.75rem; margin-bottom:1rem; }
.iq-rsc { border-radius:16px; padding:1rem 0.75rem; text-align:center; border:2px solid; }
.iq-rsc.present { background:linear-gradient(180deg,#F0FDF4,#fff); border-color:#86EFAC; }
.iq-rsc.absent  { background:linear-gradient(180deg,#FFF1F2,#fff); border-color:#FECDD3; }
.iq-rsc:hover { transform:translateY(-3px); transition:transform .2s; box-shadow:0 6px 18px rgba(0,0,0,0.1); }
.iq-rsc-emoji { font-size:1.3rem; margin-bottom:0.3rem; }
.iq-rsc-letter { font-size:1.6rem; font-weight:800; line-height:1; }
.present .iq-rsc-letter { color:#15803D; }
.absent  .iq-rsc-letter { color:#DC2626; }
.iq-rsc-name { font-size:0.68rem; color:#6B7280; font-weight:600; margin:0.2rem 0 0.5rem; text-transform:uppercase; letter-spacing:0.05em; }
.iq-rsc-pill { display:inline-block; font-size:0.63rem; font-weight:700; padding:0.2rem 0.6rem; border-radius:20px; }
.present .iq-rsc-pill { background:#DCFCE7; color:#15803D; }
.absent  .iq-rsc-pill { background:#FFE4E6; color:#BE123C; }
.iq-rsc-prob { font-size:0.6rem; color:#9CA3AF; margin-top:0.4rem; font-family:monospace; }

/* Feedback */
.iq-fb {
    background:#fff; border:2px solid #E9D5FF;
    border-radius:18px; padding:1.4rem; margin-bottom:1rem;
}
.iq-fb-hd {
    display:flex; justify-content:space-between; align-items:center;
    margin-bottom:1rem; padding-bottom:0.9rem; border-bottom:1.5px solid #F3F4F6;
}
.iq-fb-ttl { font-size:1rem; font-weight:800; color:#111827; }
.iq-mode-ia    { font-size:0.68rem; font-weight:700; padding:0.22rem 0.65rem; border-radius:20px; background:#EDE9FE; color:#6D28D9; }
.iq-mode-rules { font-size:0.68rem; font-weight:700; padding:0.22rem 0.65rem; border-radius:20px; background:#F3F4F6; color:#4B5563; }
.iq-fb-body { font-size:0.9rem; color:#1F2937; line-height:1.85; }
.iq-fb-body strong { color:#111827; font-weight:700; }
.iq-fb-body b { color:#111827; font-weight:700; }

/* Template */
.iq-tpl { display:grid; grid-template-columns:1fr 1fr; gap:0.75rem; margin-top:0.75rem; }
.iq-tpl-item { background:#FAFAFA; border:1.5px solid #E5E7EB; border-radius:12px; padding:0.9rem; }
.iq-tpl-l { font-size:1.05rem; font-weight:800; margin-bottom:0.15rem; }
.iq-tpl-item:nth-child(1) .iq-tpl-l { color:#6D28D9; }
.iq-tpl-item:nth-child(2) .iq-tpl-l { color:#1D4ED8; }
.iq-tpl-item:nth-child(3) .iq-tpl-l { color:#B45309; }
.iq-tpl-item:nth-child(4) .iq-tpl-l { color:#047857; }
.iq-tpl-role { font-size:0.62rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; color:#9CA3AF; margin-bottom:0.4rem; }
.iq-tpl-txt  { font-size:0.78rem; color:#4B5563; line-height:1.55; font-style:italic; }

/* Footer */
.iq-footer { text-align:center; font-size:0.72rem; color:#9CA3AF; padding:1.5rem 0 0.5rem; border-top:1.5px solid #EDE9FE; margin-top:1.5rem; }
.iq-footer a { color:#8B5CF6; text-decoration:none; }

/* BOTONES */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #5B21B6, #8B5CF6) !important;
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 2rem !important;
    box-shadow: 0 6px 24px rgba(91,33,182,0.45) !important;
    letter-spacing: -0.01em !important;
    transition: all .2s !important;
    width: 100% !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(91,33,182,0.55) !important;
}
.stButton > button[kind="primary"]:disabled {
    background: #E5E7EB !important; color: #9CA3AF !important;
    box-shadow: none !important; cursor: not-allowed !important;
}
.stButton > button:not([kind="primary"]) {
    background: #fff !important; border: 2px solid #DDD6FE !important;
    border-radius: 12px !important; color: #6D28D9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 0.88rem !important;
    transition: all .2s !important; width: 100% !important;
}
.stButton > button:not([kind="primary"]):hover { background: #F5F3FF !important; }

/* INPUTS */
div[data-testid="stTextArea"] textarea {
    background:#fff !important; border:2px solid #DDD6FE !important;
    border-radius:12px !important; color:#111827 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:0.92rem !important; line-height:1.7 !important;
    padding:1rem !important;
}
div[data-testid="stTextArea"] textarea::placeholder {
    color:#9CA3AF !important; font-style:italic !important; opacity:1 !important;
}
div[data-testid="stTextArea"] textarea:focus,
div[data-testid="stSelectbox"] > div > div:focus-within {
    border-color:#8B5CF6 !important;
    box-shadow:0 0 0 3px rgba(139,92,246,.18) !important;
}
div[data-testid="stTextInput"] input {
    background:#fff !important; border:2px solid #DDD6FE !important;
    border-radius:12px !important; color:#111827 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:0.92rem !important;
}
div[data-testid="stWidgetLabel"] label p {
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:0.82rem !important; font-weight:700 !important; color:#374151 !important;
}
.stExpander { border:2px solid #DDD6FE !important; border-radius:14px !important; background:#fff !important; }
div[data-testid="stExpander"] summary {
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:0.87rem !important; font-weight:700 !important; color:#374151 !important;
}
.stSpinner > div { border-top-color:#8B5CF6 !important; }
div[data-testid="stAlert"] {
    border-radius:12px !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:0.84rem !important;
}
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

@st.cache_resource(ttl=300)
def cargar_modelos():
    cfg = MODELS_DIR / "config_clasificador.json"
    if not cfg.exists(): return None, None
    with open(cfg) as f: c = json.load(f)
    u = c.get("umbrales", {"situacion":0.30,"tarea":0.30,"accion":0.75,"resultado":0.50})
    m = {}
    for et in ETIQUETAS:
        p = MODELS_DIR / f"clasificador_star_{et}.pkl"
        if not p.exists(): return None, None
        m[et] = joblib.load(p)
    return m, u

def limpiar(t):
    t = str(t).lower()
    t = re.sub(r'[^\w\s]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

def predecir(resp, mods, u):
    t = limpiar(resp)
    preds, probs = {}, {}
    for et in ETIQUETAS:
        p = mods[et].predict_proba([t])[0][1]
        preds[et] = int(p >= u[et])
        probs[et]  = round(float(p), 3)
    comps = [NOMBRES_STAR[e][0] for e, v in preds.items() if v == 1]
    return {
        "predicciones":  preds,
        "probabilidades": probs,
        "resumen": "-".join(comps) if comps else "Ninguno"
    }

SP = """Eres InterviewIQ, coach de entrevistas para universitarios peruanos.
Da feedback en español, cálido y directo, máximo 170 palabras.
Situación: contexto. Tarea: tu rol. Acción: pasos en 1ª persona. Resultado: qué cambió con datos.
REGLAS: No contradigas el análisis STAR. No inventes datos.
FORMATO:
**Lo que hiciste bien:** 1–2 frases concretas.
**Lo que falta:** un punto claro por cada componente AUSENTE.
**Cómo mejorarla:** sugerencia práctica de una sola oración."""

def _key():
    try:
        return st.secrets.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
    except:
        return os.environ.get("GEMINI_API_KEY", "")

def _llm():
    try:
        return st.secrets.get("GEMINI_MODEL", "") or "gemini-2.5-flash"
    except:
        return "gemini-2.5-flash"

def _rules(res):
    """Fallback basado en reglas. Siempre retorna un string."""
    pr   = res["predicciones"]
    pres = [NOMBRES_STAR[e][1] for e, v in pr.items() if v == 1]
    aus  = [NOMBRES_STAR[e][1] for e, v in pr.items() if v == 0]
    if len(pres) == 4:
        return "🌟 **¡Respuesta STAR completa!** Los 4 componentes están presentes. Para destacarte aún más, cuantifica tu resultado con porcentajes o plazos concretos."
    if len(pres) == 0:
        return (
            "**Reorganiza tu respuesta** usando la plantilla STAR:\n\n"
            "→ **Situación:** ¿Cuál era el contexto o problema?\n"
            "→ **Tarea:** ¿Cuál era tu responsabilidad específica?\n"
            "→ **Acción:** ¿Qué hiciste *tú* paso a paso?\n"
            "→ **Resultado:** ¿Qué lograste? ¿Qué impacto tuvo?"
        )
    sug = {
        "Situación": "Empieza describiendo el contexto: empresa, equipo, momento y cuál era el desafío.",
        "Tarea": "Explica cuál era tu responsabilidad específica en esa situación.",
        "Acción": "Detalla los pasos que *tú* tomaste en primera persona (evita 'nosotros').",
        "Resultado": "Cierra con el impacto concreto y, si puedes, un dato o porcentaje."
    }
    bien = f"**Lo que hiciste bien:** Incluiste {', '.join(pres)}.\n\n"
    falta = "**Lo que falta:**\n" + "".join(f"→ **{a}:** {sug.get(a, '')}\n\n" for a in aus)
    return bien + falta

def gen_feedback(preg, resp, res, hip=False):
    """Retorna (texto_str, modo_str). Nunca retorna None."""
    k = _key()
    if not k:
        return _rules(res), "rules"

    pr   = res["predicciones"]
    pres = [NOMBRES_STAR[e][1] for e, v in pr.items() if v == 1]
    aus  = [NOMBRES_STAR[e][1] for e, v in pr.items() if v == 0]
    msg  = (
        f'Pregunta: "{preg}"\n'
        f'Respuesta:\n"""{resp}"""\n'
        f'PRESENTES: {", ".join(pres) or "ninguno"}\n'
        f'AUSENTES: {", ".join(aus) or "ninguno"}'
    )
    if hip:
        msg += "\nALERTA: la respuesta parece hipotética."

    try:
        import requests
        r = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{_llm()}:generateContent",
            params={"key": k},
            json={
                "system_instruction": {"parts": [{"text": SP}]},
                "contents":           [{"role": "user", "parts": [{"text": msg}]}],
                "generationConfig":   {"temperature": 0.4, "maxOutputTokens": 800}
            },
            timeout=25
        )
        r.raise_for_status()
        texto = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        if not texto:
            raise ValueError("Respuesta vacía de Gemini")
        return texto, "ia"
    except Exception:
        return _rules(res), "rules"

PHIP = re.compile(
    r"\b(si (yo )?(tuviera|estuviera|fuera)|(yo )?(har[ií]a|intentar[ií]a|buscar[ií]a|hablar[ií]a|tratar[ií]a|propondr[ií]a)|lo que har[ií]a|deber[ií]a)\b",
    re.I
)
def es_hip(t): return len(PHIP.findall(t)) >= 2

def gauge_svg(total):
    pct  = total / 4
    r    = 46
    circ = 2 * 3.14159 * r
    arc  = circ * 0.75
    dash = pct * arc
    col  = {0:"#F87171", 1:"#F87171", 2:"#FCD34D", 3:"#FCD34D", 4:"#4ADE80"}[total]
    return f"""<svg width="100" height="100" viewBox="0 0 110 110">
  <circle cx="55" cy="55" r="{r}" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="9"
      stroke-dasharray="{arc:.1f} {circ:.1f}" stroke-linecap="round" transform="rotate(135 55 55)"/>
  <circle cx="55" cy="55" r="{r}" fill="none" stroke="{col}" stroke-width="9"
      stroke-dasharray="{dash:.1f} {circ:.1f}" stroke-linecap="round" transform="rotate(135 55 55)"
      style="filter:drop-shadow(0 0 6px {col});"/>
  <text x="55" y="51" text-anchor="middle" font-family="Plus Jakarta Sans,sans-serif"
        font-size="26" font-weight="800" fill="white">{total}</text>
  <text x="55" y="66" text-anchor="middle" font-family="Plus Jakarta Sans,sans-serif"
        font-size="10" fill="rgba(255,255,255,0.7)" font-weight="600">de 4</text>
</svg>"""

def render_feedback_text(texto):
    """Convierte el texto de feedback a HTML seguro."""
    if not texto:
        return "<em>No se pudo generar feedback.</em>"
    # Markdown bold → HTML
    html = str(texto)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*',    r'<em>\1</em>', html)
    html = html.replace('\n', '<br>')
    return html

PREGUNTAS = [
    "Cuéntame de una vez que tuviste que trabajar bajo presión y cómo lo manejaste.",
    "Describe una situación en la que tuviste que resolver un conflicto en tu equipo.",
    "Cuéntame de un logro del que te sientas orgulloso/a en tu vida académica o laboral.",
    "¿Hubo alguna vez que cometiste un error importante? ¿Qué hiciste al respecto?",
    "Describe una situación en la que tuviste que convencer a alguien de tu idea.",
]

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
for k, v in [("pagina","landing"), ("paso",1), ("resultado",None), ("feedback",None), ("feedback_modo",None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
#  NAV
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="iq-nav">
  <div class="iq-nav-logo">Interview<span>IQ</span></div>
  <div class="iq-nav-pills">
    <span class="iq-pill p">AD5018 · UTEC</span>
    <span class="iq-pill g">F1 = 0.808 ✓</span>
    <span class="iq-pill y">⚡ IA + STAR</span>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  LANDING
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.pagina == "landing":

    st.markdown("""
    <div class="iq-hero">
      <div class="iq-hero-inner">
        <div>
          <div class="iq-h1">Practica tus<br>respuestas <em>STAR</em> 🎯</div>
          <div class="iq-hsub">
            Escribe tu respuesta a una pregunta de entrevista por competencias
            y recibe análisis con IA en segundos.
          </div>
          <div class="iq-stats">
            <div class="iq-stat"><div class="iq-stat-n">0.808</div><div class="iq-stat-l">F1 Macro</div></div>
            <div class="iq-stat"><div class="iq-stat-n">4</div><div class="iq-stat-l">Componentes</div></div>
            <div class="iq-stat"><div class="iq-stat-n">200</div><div class="iq-stat-l">Respuestas</div></div>
            <div class="iq-stat"><div class="iq-stat-n">~5s</div><div class="iq-stat-l">Feedback</div></div>
          </div>
        </div>
        <div class="iq-mascot">🤖</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="iq-star-grid">
      <div class="iq-sc s">
        <div class="iq-sc-letter">S</div>
        <div class="iq-sc-name">Situación</div>
        <div class="iq-sc-desc">El contexto en que ocurrió la experiencia</div>
      </div>
      <div class="iq-sc t">
        <div class="iq-sc-letter">T</div>
        <div class="iq-sc-name">Tarea</div>
        <div class="iq-sc-desc">Tu rol y responsabilidad específica</div>
      </div>
      <div class="iq-sc a">
        <div class="iq-sc-letter">A</div>
        <div class="iq-sc-name">Acción</div>
        <div class="iq-sc-desc">Los pasos que tomaste en 1ª persona</div>
      </div>
      <div class="iq-sc r">
        <div class="iq-sc-letter">R</div>
        <div class="iq-sc-name">Resultado</div>
        <div class="iq-sc-desc">El impacto de tus acciones, con datos</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="iq-2col">
      <div class="iq-card">
        <div class="iq-card-ttl">📋 Cómo funciona</div>
        <div class="iq-row">
          <div class="iq-num">1</div>
          <div><span class="iq-row-ttl">Elige una pregunta</span>
               <span class="iq-row-sub">Del banco de preguntas conductuales o escribe la tuya.</span></div>
        </div>
        <div class="iq-row">
          <div class="iq-num">2</div>
          <div><span class="iq-row-ttl">Escribe tu respuesta</span>
               <span class="iq-row-sub">Un caso real que hayas vivido — no hipotético.</span></div>
        </div>
        <div class="iq-row">
          <div class="iq-num">3</div>
          <div><span class="iq-row-ttl">Análisis STAR con ML</span>
               <span class="iq-row-sub">El modelo detecta qué componentes están presentes.</span></div>
        </div>
        <div class="iq-row">
          <div class="iq-num">4</div>
          <div><span class="iq-row-ttl">Feedback con reglas</span>
               <span class="iq-row-sub">Recomendaciones concretas basadas en tu respuesta.</span></div>
        </div>
      </div>
      <div class="iq-card">
        <div class="iq-card-ttl">💡 Tips para una buena respuesta</div>
        <div class="iq-row">
          <span class="iq-tip-icon">✅</span>
          <div><span class="iq-row-ttl">Usa verbos en 1ª persona</span>
               <span class="iq-row-sub">"Yo organicé", "Yo propuse" — no "nosotros hicimos".</span></div>
        </div>
        <div class="iq-row">
          <span class="iq-tip-icon">📏</span>
          <div><span class="iq-row-ttl">50 a 150 palabras</span>
               <span class="iq-row-sub">Respuestas muy cortas no dan contexto suficiente.</span></div>
        </div>
        <div class="iq-row">
          <span class="iq-tip-icon">📊</span>
          <div><span class="iq-row-ttl">Incluye datos</span>
               <span class="iq-row-sub">"Mejoré un 30%", "en 2 semanas" — el resultado se mide.</span></div>
        </div>
        <div class="iq-row">
          <span class="iq-tip-icon">🚫</span>
          <div><span class="iq-row-ttl">No respondas hipotético</span>
               <span class="iq-row-sub">Te piden un caso real que viviste, no "yo haría...".</span></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="iq-notice">
      <span>🛡️</span>
      <span>Herramienta de práctica — puede equivocarse y no predice resultados en entrevistas reales.
      <b>Privacidad (Ley N.° 29733):</b> tu respuesta se usa solo en esta sesión; evita datos personales.</span>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Comenzar práctica →", type="primary", use_container_width=True):
            st.session_state.pagina = "analisis"
            st.session_state.paso   = 1
            st.session_state.resultado   = None
            st.session_state.feedback    = None
            st.session_state.feedback_modo = None
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

    # ── Barra de progreso ──────────────────────────────────────────────────
    paso = st.session_state.paso

    def _dot(n):
        if n < paso:   return "done",   "✓"
        if n == paso:  return "active",  str(n)
        return "idle", str(n)

    p1c, p1l = _dot(1)
    p2c, p2l = _dot(2)
    p3c, p3l = _dot(3)
    l1 = "done" if paso > 1 else ""
    l2 = "done" if paso > 2 else ""

    st.markdown(f"""
    <div class="iq-progress">
      <div class="iq-ps">
        <div class="iq-pd {p1c}">{p1l}</div>
        <span class="iq-pl {p1c}">Pregunta</span>
      </div>
      <div class="iq-pline {l1}"></div>
      <div class="iq-ps">
        <div class="iq-pd {p2c}">{p2l}</div>
        <span class="iq-pl {p2c}">Respuesta</span>
      </div>
      <div class="iq-pline {l2}"></div>
      <div class="iq-ps">
        <div class="iq-pd {p3c}">{p3l}</div>
        <span class="iq-pl {p3c}">Análisis</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Panel: Pregunta ────────────────────────────────────────────────────
    with st.container(border=True):
        st.markdown("""
        <div style="display:flex;align-items:center;justify-content:space-between;
                    margin-bottom:0.9rem;padding-bottom:0.75rem;border-bottom:1.5px solid #F3F4F6;">
          <span style="font-size:1rem;font-weight:800;color:#111827;">1 · Pregunta de entrevista</span>
          <span style="font-size:0.68rem;font-weight:700;padding:0.25rem 0.75rem;
                       border-radius:20px;background:#EDE9FE;color:#6D28D9;">BANCO</span>
        </div>""", unsafe_allow_html=True)

        pregunta_sel = st.selectbox(
            "Pregunta:",
            options=["— Elige una pregunta del banco —"] + PREGUNTAS + ["✏️ Escribe tu propia pregunta..."],
            index=0,
            label_visibility="collapsed",
        )

        pregunta_custom = ""
        if pregunta_sel == "✏️ Escribe tu propia pregunta...":
            pregunta_custom = st.text_input(
                "Tu pregunta:",
                placeholder="Escribe tu pregunta de entrevista conductual...",
                label_visibility="collapsed",
            )
            pregunta_final = pregunta_custom
        elif pregunta_sel == "— Elige una pregunta del banco —":
            pregunta_final = ""
        else:
            pregunta_final = pregunta_sel

        if pregunta_final:
            st.markdown(f'<div class="iq-qpreview">💬 &nbsp;"{pregunta_final}"</div>', unsafe_allow_html=True)

    # ── Panel: Respuesta ───────────────────────────────────────────────────
    with st.container(border=True):
        st.markdown("""
        <div style="display:flex;align-items:center;justify-content:space-between;
                    margin-bottom:0.9rem;padding-bottom:0.75rem;border-bottom:1.5px solid #F3F4F6;">
          <span style="font-size:1rem;font-weight:800;color:#111827;">2 · Tu respuesta</span>
          <span style="font-size:0.68rem;font-weight:700;padding:0.25rem 0.75rem;
                       border-radius:20px;background:#EDE9FE;color:#6D28D9;">STAR</span>
        </div>""", unsafe_allow_html=True)

        respuesta = st.text_area(
            "Respuesta:",
            placeholder="Ejemplo: En mi práctica en [empresa], estábamos en [situación]. Mi responsabilidad era [tarea]. Lo que hice fue [acciones concretas]. Como resultado, [logro + datos].",
            height=175,
            label_visibility="collapsed",
        )

        palabras = len(respuesta.split()) if respuesta.strip() else 0
        if respuesta.strip():
            pct_w = min(palabras / 150, 1.0)
            if palabras >= 50:
                fc, lc, lbl = "#4ADE80", "#15803D", f"{palabras} palabras ✓"
            elif palabras >= 20:
                fc, lc, lbl = "#FCD34D", "#B45309", f"{palabras} palabras — intenta llegar a 50"
            else:
                fc, lc, lbl = "#F87171", "#DC2626", f"{palabras} palabras — muy corta"
            st.markdown(f"""
            <div class="iq-wc">
              <span class="iq-wc-label">Longitud</span>
              <span style="color:{lc};font-weight:700;font-size:0.75rem;">{lbl}</span>
            </div>
            <div class="iq-wc-track">
              <div class="iq-wc-fill" style="width:{int(pct_w*100)}%;background:{fc};"></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            palabras = 0

    # ── Botones ────────────────────────────────────────────────────────────
    st.write("")
    col_a, col_b = st.columns([3, 1])
    with col_a:
        analizar = st.button(
            "Analizar respuesta →",
            type="primary",
            use_container_width=True,
            disabled=not (respuesta.strip() and pregunta_final),
        )
    with col_b:
        if st.button("← Volver", use_container_width=True):
            st.session_state.pagina = "landing"
            st.session_state.paso   = 1
            st.rerun()

    # ── Resultados ─────────────────────────────────────────────────────────
    if analizar and respuesta.strip() and pregunta_final:
        st.session_state.paso = 3

        if palabras < 20:
            st.warning("Tu respuesta tiene menos de 20 palabras — el análisis puede ser impreciso.")
        if es_hip(respuesta):
            st.info('Tu respuesta parece hipotética ("yo haría..."). Intenta contar un caso real que hayas vivido.')

        with st.spinner("Analizando componentes STAR con el modelo..."):
            res = predecir(respuesta, mods, umbrales)
        st.session_state.resultado = res

        total_p = sum(res["predicciones"].values())
        verdicts = {
            4: ("🌟 Respuesta STAR Completa",  "Los 4 componentes están presentes — ¡estructura perfecta!"),
            3: ("⚡ Casi perfecto",             "Muy buena estructura, solo falta 1 componente."),
            2: ("📈 Buen inicio",               "Tienes la mitad de la estructura — agrega los que faltan."),
            1: ("💡 Falta desarrollar",          "Solo 1 componente detectado — expande tu respuesta."),
            0: ("🔧 Sin estructura STAR",        "Reorganiza tu respuesta usando la plantilla de abajo."),
        }
        v_title, v_desc = verdicts[total_p]
        tags = "".join(
            f'<span class="iq-rtag">{NOMBRES_STAR[e][0]} — {NOMBRES_STAR[e][1]}</span>'
            for e, v in res["predicciones"].items() if v == 1
        ) or '<span class="iq-rtag" style="background:rgba(248,113,113,.25)">Sin componentes detectados</span>'

        st.markdown(f"""
        <div class="iq-rhero">
          <div style="flex-shrink:0">{gauge_svg(total_p)}</div>
          <div style="position:relative;z-index:1;">
            <div class="iq-rv">{v_title}</div>
            <div class="iq-rd">{v_desc}</div>
            <div class="iq-rtags">{tags}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Tarjetas STAR
        cards_html = ""
        for et in ETIQUETAS:
            letra, nombre, emoji = NOMBRES_STAR[et]
            pres = res["predicciones"][et] == 1
            prob = res["probabilidades"][et]
            u_thr = umbrales[et]
            cls   = "present" if pres else "absent"
            icon  = "✅" if pres else "❌"
            pill  = "Presente" if pres else "Ausente"
            cards_html += f"""<div class="iq-rsc {cls}">
              <div class="iq-rsc-emoji">{emoji}</div>
              <div class="iq-rsc-letter">{letra}</div>
              <div class="iq-rsc-name">{nombre}</div>
              <div style="font-size:1.1rem;margin-bottom:.4rem">{icon}</div>
              <span class="iq-rsc-pill">{pill}</span>
              <div class="iq-rsc-prob">p={prob:.2f} · u={u_thr}</div>
            </div>"""
        st.markdown(f'<div class="iq-rstar">{cards_html}</div>', unsafe_allow_html=True)

        # Feedback
        with st.spinner("Generando feedback personalizado con Gemini..."):
            fb_txt, modo = gen_feedback(pregunta_final, respuesta, res, es_hip(respuesta))

        # Garantizamos que fb_txt sea string
        if not isinstance(fb_txt, str) or not fb_txt.strip():
            fb_txt = _rules(res)
            modo   = "rules"

        st.session_state.feedback      = fb_txt
        st.session_state.feedback_modo = modo

        modo_html = (
            '<span class="iq-mode-ia">🤖 Google Gemini</span>'
            if modo == "ia"
            else '<span class="iq-mode-rules">📋 Análisis por reglas</span>'
        )

        st.markdown(f"""
        <div class="iq-fb">
          <div class="iq-fb-hd">
            <div class="iq-fb-ttl">💬 Feedback personalizado</div>
            {modo_html}
          </div>
          <div class="iq-fb-body">{render_feedback_text(fb_txt)}</div>
        </div>""", unsafe_allow_html=True)

        # Plantilla si faltan componentes
        aus_et = [et for et, v in res["predicciones"].items() if v == 0]
        if aus_et:
            with st.expander("📝 Ver plantilla STAR para mejorar tu respuesta"):
                st.markdown("""
                <div class="iq-tpl">
                  <div class="iq-tpl-item">
                    <div class="iq-tpl-l">S</div>
                    <div class="iq-tpl-role">Situación</div>
                    <div class="iq-tpl-txt">"En [empresa/equipo], durante [momento], el desafío era [problema]..."</div>
                  </div>
                  <div class="iq-tpl-item">
                    <div class="iq-tpl-l">T</div>
                    <div class="iq-tpl-role">Tarea</div>
                    <div class="iq-tpl-txt">"Mi responsabilidad era [objetivo específico y medible]..."</div>
                  </div>
                  <div class="iq-tpl-item">
                    <div class="iq-tpl-l">A</div>
                    <div class="iq-tpl-role">Acción</div>
                    <div class="iq-tpl-txt">"Lo que hice fue [pasos concretos en primera persona]..."</div>
                  </div>
                  <div class="iq-tpl-item">
                    <div class="iq-tpl-l">R</div>
                    <div class="iq-tpl-role">Resultado</div>
                    <div class="iq-tpl-txt">"Como resultado, [logro + % o dato + timeframe]..."</div>
                  </div>
                </div>""", unsafe_allow_html=True)

        st.write("")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 Intentar de nuevo", use_container_width=True):
                st.session_state.paso = 1
                st.session_state.resultado = None
                st.rerun()
        with c2:
            if st.button("🏠 Volver al inicio", use_container_width=True):
                st.session_state.pagina = "landing"
                st.session_state.paso   = 1
                st.rerun()

    st.markdown("""<div class="iq-footer">
      InterviewIQ · AD5018 IA para Negocios · UTEC 2026-2 ·
      <a href="https://github.com/itslueli/InterviewIQ">GitHub</a>
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    pass
