"""
InterviewIQ — MVP Streamlit
Componente A2: Clasificador STAR + G2: feedback con Gemini
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
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #F0F2FF !important;
    color: #1A1A2E;
}
.stApp { background: #F0F2FF !important; }

/* ── Ocultar chrome de Streamlit ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 1.5rem 2rem !important; max-width: 1200px !important; }

/* ══ HEADER HERO ══ */
.iq-hero {
    background: linear-gradient(135deg, #6C2BD9 0%, #9B59F5 50%, #C47AF5 100%);
    border-radius: 24px;
    padding: 2rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(108, 43, 217, 0.35);
}
.iq-hero::before {
    content: '';
    position: absolute; top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}
.iq-hero::after {
    content: '';
    position: absolute; bottom: -60px; right: 120px;
    width: 150px; height: 150px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.iq-hero-left { z-index: 1; }
.iq-hero-greeting {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: rgba(255,255,255,0.75);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.iq-hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #fff;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}
.iq-hero-title span { color: #FFD93D; }
.iq-hero-sub {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.8);
    max-width: 420px;
    line-height: 1.5;
}
.iq-hero-badges { display: flex; gap: 0.6rem; margin-top: 1rem; flex-wrap: wrap; }
.iq-hero-badge {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.75rem;
    font-weight: 600;
    color: #fff;
}
.iq-hero-emoji {
    font-size: 5rem;
    z-index: 1;
    filter: drop-shadow(0 10px 20px rgba(0,0,0,0.2));
}

/* ══ NOTICE ══ */
.iq-notice-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.iq-notice-card {
    background: #fff;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    display: flex;
    gap: 0.9rem;
    align-items: flex-start;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid rgba(108,43,217,0.08);
}
.iq-notice-icon {
    width: 38px; height: 38px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; flex-shrink: 0;
}
.iq-notice-icon.purple { background: #EDE9FE; }
.iq-notice-icon.green  { background: #DCFCE7; }
.iq-notice-text { font-size: 0.82rem; color: #64748B; line-height: 1.5; }
.iq-notice-text strong { color: #1A1A2E; display: block; margin-bottom: 0.15rem; font-size: 0.87rem; }

/* ══ SECTION LABEL ══ */
.iq-section-label {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #9CA3AF;
    margin-bottom: 0.6rem;
}

/* ══ PREGUNTA CARD ══ */
.iq-panel {
    background: #fff;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06);
    border: 1px solid rgba(108,43,217,0.08);
    margin-bottom: 1rem;
}
.iq-panel-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #1A1A2E;
    display: flex; align-items: center; gap: 0.5rem;
    margin-bottom: 1rem;
}
.iq-panel-title .pill {
    background: #EDE9FE; color: #6C2BD9;
    font-size: 0.7rem; font-weight: 700;
    padding: 0.2rem 0.6rem; border-radius: 20px;
    letter-spacing: 0.04em;
}
.iq-q-preview {
    background: linear-gradient(135deg, #EDE9FE, #F3E8FF);
    border: 1px solid rgba(108,43,217,0.15);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    font-size: 0.9rem;
    color: #4C1D95;
    font-style: italic;
    line-height: 1.5;
    margin-top: 0.8rem;
}

/* ══ WORD COUNT BAR ══ */
.iq-wc-bar-wrap {
    margin-top: 0.8rem;
}
.iq-wc-label {
    display: flex; justify-content: space-between;
    font-size: 0.75rem; color: #94A3B8; margin-bottom: 0.3rem;
}
.iq-wc-label span { font-weight: 600; }
.iq-wc-track {
    height: 6px; background: #F1F5F9; border-radius: 10px; overflow: hidden;
}
.iq-wc-fill {
    height: 100%; border-radius: 10px;
    transition: width 0.4s ease;
}

/* ══ ANALYZE BUTTON (via CSS targeting) ══ */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6C2BD9, #9B59F5) !important;
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.8rem 2rem !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 8px 25px rgba(108,43,217,0.35) !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button[kind="primary"]:disabled {
    background: #E2E8F0 !important; color: #94A3B8 !important;
    box-shadow: none !important;
}
.stButton > button:not([kind="primary"]) {
    background: #fff !important; color: #6C2BD9 !important;
    border: 1.5px solid #DDD6FE !important;
    border-radius: 12px !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
}

/* ══ INPUTS ══ */
.stSelectbox > div > div {
    background: #fff !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 12px !important;
    color: #1A1A2E !important;
    font-size: 0.92rem !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #9B59F5 !important;
    box-shadow: 0 0 0 3px rgba(155,89,245,0.12) !important;
}
.stTextArea > div > div > textarea {
    background: #fff !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 12px !important;
    color: #1A1A2E !important;
    font-size: 0.92rem !important;
    line-height: 1.65 !important;
    padding: 1rem !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: #9B59F5 !important;
    box-shadow: 0 0 0 3px rgba(155,89,245,0.12) !important;
}
.stTextInput > div > div > input {
    background: #fff !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 12px !important;
    color: #1A1A2E !important;
}

/* ══ RESULTADO — GAUGE ══ */
.iq-results-hero {
    background: linear-gradient(135deg, #6C2BD9 0%, #9B59F5 100%);
    border-radius: 24px;
    padding: 2rem;
    display: flex;
    align-items: center;
    gap: 2rem;
    box-shadow: 0 20px 50px rgba(108,43,217,0.3);
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.iq-results-hero::before {
    content: '';
    position: absolute; top: -30px; right: -30px;
    width: 160px; height: 160px;
    background: rgba(255,255,255,0.07); border-radius: 50%;
}
.iq-gauge-svg { flex-shrink: 0; }
.iq-results-info { flex: 1; }
.iq-results-score-label {
    font-size: 0.8rem; font-weight: 600;
    color: rgba(255,255,255,0.7);
    text-transform: uppercase; letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
}
.iq-results-verdict {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.8rem; font-weight: 800;
    color: #fff; line-height: 1.1; margin-bottom: 0.4rem;
}
.iq-results-desc { font-size: 0.88rem; color: rgba(255,255,255,0.78); line-height: 1.5; }
.iq-results-tags { display: flex; gap: 0.5rem; margin-top: 0.8rem; flex-wrap: wrap; }
.iq-results-tag {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px; padding: 0.25rem 0.8rem;
    font-size: 0.75rem; font-weight: 600; color: #fff;
}

/* ══ STAR CARDS ══ */
.iq-star-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.iq-star-card {
    background: #fff;
    border-radius: 20px;
    padding: 1.4rem 1rem;
    text-align: center;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    border: 2px solid transparent;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
}
.iq-star-card:hover { transform: translateY(-3px); }
.iq-star-card.present {
    border-color: #10B981;
    background: linear-gradient(180deg, #ECFDF5 0%, #fff 60%);
}
.iq-star-card.absent {
    border-color: #F87171;
    background: linear-gradient(180deg, #FFF1F2 0%, #fff 60%);
}
.iq-star-card-top {
    width: 52px; height: 52px; border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem;
    margin: 0 auto 0.8rem;
}
.present .iq-star-card-top { background: #DCFCE7; }
.absent  .iq-star-card-top { background: #FFE4E6; }
.iq-star-letter {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.6rem; font-weight: 800; line-height: 1;
    margin-bottom: 0.15rem;
}
.present .iq-star-letter { color: #059669; }
.absent  .iq-star-letter { color: #DC2626; }
.iq-star-name { font-size: 0.75rem; color: #94A3B8; font-weight: 500; margin-bottom: 0.6rem; }
.iq-star-status { font-size: 1.3rem; margin-bottom: 0.4rem; }
.iq-star-pill {
    display: inline-block;
    font-size: 0.65rem; font-weight: 700;
    padding: 0.2rem 0.65rem; border-radius: 20px;
    letter-spacing: 0.04em;
}
.present .iq-star-pill { background: #DCFCE7; color: #059669; }
.absent  .iq-star-pill { background: #FFE4E6; color: #DC2626; }
.iq-star-prob { font-size: 0.65rem; color: #CBD5E1; margin-top: 0.4rem; font-family: monospace; }

/* ══ FEEDBACK PANEL ══ */
.iq-feedback-wrap {
    background: #fff;
    border-radius: 20px;
    padding: 1.8rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    border: 1px solid rgba(108,43,217,0.1);
    margin-bottom: 1rem;
}
.iq-feedback-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1.2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #F1F5F9;
}
.iq-feedback-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1rem; font-weight: 700; color: #1A1A2E;
    display: flex; align-items: center; gap: 0.5rem;
}
.iq-feedback-mode-badge {
    font-size: 0.7rem; font-weight: 600;
    padding: 0.25rem 0.7rem; border-radius: 20px;
}
.iq-feedback-mode-badge.ia { background: #EDE9FE; color: #6C2BD9; }
.iq-feedback-mode-badge.rules { background: #F1F5F9; color: #64748B; }
.iq-feedback-body {
    font-size: 0.9rem; color: #374151; line-height: 1.75;
}
.iq-feedback-body strong { color: #1A1A2E; }

/* ══ TEMPLATE ══ */
.iq-template-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem; margin-top: 0.5rem;
}
.iq-template-item {
    background: #FAFAFA;
    border: 1px solid #E2E8F0;
    border-radius: 12px; padding: 1rem;
}
.iq-template-letter {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.1rem; font-weight: 800;
    margin-bottom: 0.3rem;
}
.iq-template-item:nth-child(1) .iq-template-letter { color: #6C2BD9; }
.iq-template-item:nth-child(2) .iq-template-letter { color: #0EA5E9; }
.iq-template-item:nth-child(3) .iq-template-letter { color: #F59E0B; }
.iq-template-item:nth-child(4) .iq-template-letter { color: #10B981; }
.iq-template-role { font-size: 0.72rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.4rem; }
.iq-template-text { font-size: 0.8rem; color: #64748B; line-height: 1.5; }

/* ══ SPINNER ══ */
.stSpinner > div { border-top-color: #6C2BD9 !important; }

/* ══ EXPANDER ══ */
.stExpander {
    background: #fff !important;
    border: 1px solid rgba(108,43,217,0.1) !important;
    border-radius: 16px !important;
}

/* ══ ALERT ══ */
.stAlert { border-radius: 12px !important; }

/* ══ WARNING ══ */
[data-baseweb="notification"] {
    background: #FFFBEB !important;
    border: 1px solid #FDE68A !important;
    border-radius: 12px !important;
    color: #92400E !important;
}

/* ══ FOOTER ══ */
.iq-footer {
    text-align: center; color: #CBD5E1; font-size: 0.75rem;
    padding: 1.5rem 0 0.5rem;
    border-top: 1px solid #E2E8F0;
    margin-top: 2rem;
}

/* scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #F1F5F9; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTES
# ══════════════════════════════════════════════════════════════════════════════
ETIQUETAS = ['situacion', 'tarea', 'accion', 'resultado']
NOMBRES_STAR = {
    'situacion': ('S', 'Situación', '🌍'),
    'tarea':     ('T', 'Tarea',     '📋'),
    'accion':    ('A', 'Acción',    '⚡'),
    'resultado': ('R', 'Resultado', '🏆'),
}
MODELS_DIR = Path(__file__).parent / "models"


# ══════════════════════════════════════════════════════════════════════════════
#  MODELOS
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def cargar_modelos():
    config_path = MODELS_DIR / "config_clasificador.json"
    if not config_path.exists():
        return None, None
    with open(config_path) as f:
        config = json.load(f)
    umbrales = config.get("umbrales", {
        "situacion": 0.30, "tarea": 0.30, "accion": 0.75, "resultado": 0.70
    })
    modelos = {}
    for et in ETIQUETAS:
        p = MODELS_DIR / f"clasificador_star_{et}.pkl"
        if not p.exists():
            return None, None
        modelos[et] = joblib.load(p)
    return modelos, umbrales


def limpiar(texto: str) -> str:
    texto = str(texto).lower()
    texto = re.sub(r'[^\w\s]', ' ', texto)
    return re.sub(r'\s+', ' ', texto).strip()


def predecir_star(respuesta: str, modelos: dict, umbrales: dict) -> dict:
    t = limpiar(respuesta)
    preds, probs = {}, {}
    for et in ETIQUETAS:
        prob = modelos[et].predict_proba([t])[0][1]
        preds[et] = int(prob >= umbrales[et])
        probs[et]  = round(float(prob), 3)
    comps = [NOMBRES_STAR[e][0] for e, v in preds.items() if v == 1]
    return {
        "predicciones": preds, "probabilidades": probs,
        "resumen": "-".join(comps) if comps else "Ninguno",
        "componentes_presentes": comps,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  FEEDBACK
# ══════════════════════════════════════════════════════════════════════════════
GUIA_STAR = """GUÍA STAR DE INTERVIEWIQ (contexto fijo)
- Situación: contexto concreto — dónde, cuándo, con quién.
- Tarea: responsabilidad específica del candidato.
- Acción: pasos que tomó personalmente (verbos en 1ª persona).
- Resultado: qué cambió, idealmente con dato verificable.
- Duración ideal: 100–250 palabras.
- Errores comunes: hablar en "nosotros"; olvidar el resultado; respuestas hipotéticas."""

SYSTEM_PROMPT = f"""Eres InterviewIQ, un coach de entrevistas por competencias para estudiantes universitarios peruanos.
Das feedback en español, cálido y directo, máximo 170 palabras.

{GUIA_STAR}

REGLAS:
1. El análisis STAR viene de un modelo entrenado. NO lo contradigas.
2. No inventes experiencias ni datos del estudiante.
3. No afirmes probabilidades de ser contratado.
4. Si la respuesta es muy corta o hipotética, dilo con amabilidad.

FORMATO:
**Lo que hiciste bien:** 1–2 frases.
**Lo que falta:** un punto por cada componente AUSENTE.
**Cómo mejorarla:** una sugerencia concreta.
"""


def _api_key() -> str:
    try:
        return st.secrets.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
    except Exception:
        return os.environ.get("GEMINI_API_KEY", "")


def _modelo_llm() -> str:
    try:
        return st.secrets.get("GEMINI_MODEL", "") or "gemini-2.5-flash"
    except Exception:
        return "gemini-2.5-flash"


def generar_feedback(pregunta: str, respuesta: str, resultado: dict, hipotetica: bool = False) -> tuple[str, str]:
    api_key = _api_key()
    if not api_key:
        return _feedback_reglas(resultado), "rules"
    preds = resultado["predicciones"]
    presentes = [NOMBRES_STAR[e][1] for e, v in preds.items() if v == 1]
    ausentes   = [NOMBRES_STAR[e][1] for e, v in preds.items() if v == 0]
    msg = f'Pregunta: "{pregunta or "Pregunta conductual libre"}"\n\nRespuesta:\n"""{respuesta}"""\n\nAnálisis STAR:\n- PRESENTES: {", ".join(presentes) if presentes else "ninguno"}\n- AUSENTES: {", ".join(ausentes) if ausentes else "ninguno"}'
    if hipotetica:
        msg += "\n\nALERTA: respuesta hipotética. Pídele un caso real."
    try:
        import requests
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{_modelo_llm()}:generateContent"
        payload = {
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [{"role": "user", "parts": [{"text": msg}]}],
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 800},
        }
        r = requests.post(url, params={"key": api_key}, json=payload, timeout=25)
        r.raise_for_status()
        texto = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        if not texto:
            raise ValueError("vacío")
        return texto, "ia"
    except Exception:
        return _feedback_reglas(resultado), "rules"


def _feedback_reglas(resultado: dict) -> str:
    preds = resultado["predicciones"]
    ausentes  = [NOMBRES_STAR[e][1] for e, v in preds.items() if v == 0]
    presentes = [NOMBRES_STAR[e][1] for e, v in preds.items() if v == 1]
    total = len(presentes)
    if total == 4:
        return "🌟 **¡Respuesta STAR completa!** Tu respuesta incluye los 4 componentes. Para seguir mejorando, cuantifica tus resultados con números, porcentajes o plazos concretos."
    elif total == 0:
        return "**Tu respuesta necesita estructura STAR.**\n\n**S — Situación:** ¿Cuál era el contexto?\n\n**T — Tarea:** ¿Cuál era tu rol?\n\n**A — Acción:** ¿Qué hiciste tú?\n\n**R — Resultado:** ¿Qué lograste?"
    else:
        sugerencias = {
            "Situación": "Empieza describiendo el contexto: en qué empresa, equipo o momento ocurrió.",
            "Tarea": "Explica cuál era TU responsabilidad específica.",
            "Acción": "Detalla los pasos concretos que TÚ tomaste — usa verbos de acción en primera persona.",
            "Resultado": "Cierra con el impacto de tus acciones, idealmente con números o métricas.",
        }
        fb = f"**Detectamos:** {', '.join(presentes)}.\n\n"
        for a in ausentes:
            fb += f"→ **{a}:** {sugerencias.get(a, '')}\n\n"
        return fb


PATRON_HIP = re.compile(
    r"\b(si (yo )?(tuviera|estuviera|fuera)|"
    r"(yo )?(har[ií]a|intentar[ií]a|buscar[ií]a|hablar[ií]a|tratar[ií]a|propondr[ií]a)|"
    r"lo que har[ií]a|deber[ií]a)\b", re.IGNORECASE)

def es_hipotetica(texto: str) -> bool:
    return len(PATRON_HIP.findall(texto)) >= 2


# ══════════════════════════════════════════════════════════════════════════════
#  GAUGE SVG (estilo dashboard con arco coloreado)
# ══════════════════════════════════════════════════════════════════════════════
def render_gauge(total: int) -> str:
    pct = total / 4
    r = 54
    circ = 2 * 3.14159 * r
    # Usamos solo 270° del círculo (3/4)
    arc = circ * 0.75
    dash = pct * arc
    colors = {0: "#F87171", 1: "#F87171", 2: "#FCD34D", 3: "#FCD34D", 4: "#34D399"}
    color = colors[total]
    # Rotate so arc starts bottom-left → bottom-right
    return f"""
    <div style="display:flex;align-items:center;justify-content:center;position:relative;width:140px;height:140px;margin:0 auto;">
      <svg width="140" height="140" viewBox="0 0 140 140">
        <circle cx="70" cy="70" r="{r}" fill="none"
            stroke="rgba(255,255,255,0.15)" stroke-width="10"
            stroke-dasharray="{arc:.1f} {circ:.1f}"
            stroke-linecap="round"
            transform="rotate(135 70 70)"/>
        <circle cx="70" cy="70" r="{r}" fill="none"
            stroke="{color}" stroke-width="10"
            stroke-dasharray="{dash:.1f} {circ:.1f}"
            stroke-linecap="round"
            transform="rotate(135 70 70)"
            style="transition:stroke-dasharray 0.8s ease;filter:drop-shadow(0 0 8px {color}88);"/>
      </svg>
      <div style="position:absolute;text-align:center;">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:2.4rem;font-weight:800;color:#fff;line-height:1;">{total}</div>
        <div style="font-size:0.65rem;color:rgba(255,255,255,0.6);font-weight:600;letter-spacing:0.05em;">DE 4</div>
      </div>
    </div>
    """


# ══════════════════════════════════════════════════════════════════════════════
#  PREGUNTAS
# ══════════════════════════════════════════════════════════════════════════════
PREGUNTAS = [
    "Cuéntame de una vez que tuviste que trabajar bajo presión y cómo lo manejaste.",
    "Describe una situación en la que tuviste que resolver un conflicto en tu equipo.",
    "Cuéntame de un logro del que te sientas orgulloso/a en tu vida académica o laboral.",
    "¿Hubo alguna vez que cometiste un error importante? ¿Qué hiciste al respecto?",
    "Describe una situación en la que tuviste que convencer a alguien de tu idea.",
]


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    # ── HERO ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="iq-hero">
      <div class="iq-hero-left">
        <div class="iq-hero-greeting">AD5018 IA para Negocios · UTEC 2026-2</div>
        <div class="iq-hero-title">Interview<span>IQ</span></div>
        <div class="iq-hero-sub">Entrena tus respuestas de entrevista con el método STAR y recibe feedback personalizado al instante.</div>
        <div class="iq-hero-badges">
          <span class="iq-hero-badge">🤖 IA + Reglas STAR</span>
          <span class="iq-hero-badge">⚡ Feedback al instante</span>
          <span class="iq-hero-badge">🎯 F1 = 0.830</span>
        </div>
      </div>
      <div class="iq-hero-emoji">🎙️</div>
    </div>
    """, unsafe_allow_html=True)

    # ── NOTICES ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="iq-notice-row">
      <div class="iq-notice-card">
        <div class="iq-notice-icon purple">🤖</div>
        <div class="iq-notice-text">
          <strong>Herramienta con Inteligencia Artificial</strong>
          Un modelo entrenado por el equipo detecta componentes STAR y un LLM genera feedback. Es una herramienta de práctica — puede equivocarse.
        </div>
      </div>
      <div class="iq-notice-card">
        <div class="iq-notice-icon green">🔒</div>
        <div class="iq-notice-text">
          <strong>Privacidad (Ley N.° 29733)</strong>
          Tu respuesta se usa solo para darte feedback en esta sesión. No se guarda ni se asocia a tu identidad. Evita datos personales.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Cargar modelos
    modelos, umbrales = cargar_modelos()
    if modelos is None:
        st.error("⚠️ Modelos no encontrados. Verifica que `models/` contiene los archivos `.pkl` y `config_clasificador.json`.")
        st.stop()

    # ── LAYOUT DOS COLUMNAS ───────────────────────────────────────────────────
    col_izq, col_der = st.columns([1, 1], gap="large")

    with col_izq:
        # ── Paso 1 ────────────────────────────────────────────────────────────
        st.markdown('<div class="iq-section-label">Paso 1 — Pregunta</div>', unsafe_allow_html=True)
        st.markdown('<div class="iq-panel">', unsafe_allow_html=True)
        st.markdown('<div class="iq-panel-title">Elige tu pregunta de entrevista <span class="pill">BANCO</span></div>', unsafe_allow_html=True)

        pregunta_sel = st.selectbox(
            "Pregunta:",
            options=[""] + PREGUNTAS + ["✏️ Escribir mi propia pregunta..."],
            index=0,
            label_visibility="collapsed",
        )

        pregunta_custom = ""
        if pregunta_sel == "✏️ Escribir mi propia pregunta...":
            pregunta_custom = st.text_input("Tu pregunta:", placeholder="Escribe tu pregunta de entrevista...", label_visibility="collapsed")
            pregunta_final = pregunta_custom
        else:
            pregunta_final = pregunta_sel

        if pregunta_final:
            st.markdown(f'<div class="iq-q-preview">💬 &nbsp;"{pregunta_final}"</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        # ── Paso 2 ────────────────────────────────────────────────────────────
        st.markdown('<div class="iq-section-label">Paso 2 — Tu respuesta</div>', unsafe_allow_html=True)
        st.markdown('<div class="iq-panel">', unsafe_allow_html=True)
        st.markdown('<div class="iq-panel-title">Escribe tu respuesta <span class="pill">STAR</span></div>', unsafe_allow_html=True)

        respuesta = st.text_area(
            "Respuesta:",
            placeholder="Cuenta una experiencia real usando el método STAR:\n\nSituación → Tarea → Acción → Resultado",
            height=160,
            label_visibility="collapsed",
        )

        palabras = len(respuesta.split()) if respuesta.strip() else 0
        if respuesta.strip():
            pct = min(palabras / 150, 1)
            if palabras >= 50:
                fill_color, label_color, label = "#10B981", "#059669", f"{palabras} palabras ✓"
            elif palabras >= 20:
                fill_color, label_color, label = "#F59E0B", "#D97706", f"{palabras} palabras — intenta llegar a 50"
            else:
                fill_color, label_color, label = "#F87171", "#DC2626", f"{palabras} palabras — muy corta"
            pct_pct = int(pct * 100)
            st.markdown(f"""
            <div class="iq-wc-bar-wrap">
              <div class="iq-wc-label">
                <span>Longitud de respuesta</span>
                <span style="color:{label_color}">{label}</span>
              </div>
              <div class="iq-wc-track">
                <div class="iq-wc-fill" style="width:{pct_pct}%;background:{fill_color};"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Botón ─────────────────────────────────────────────────────────────────
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        analizar = st.button(
            "🎯  Analizar mi respuesta",
            type="primary",
            use_container_width=True,
            disabled=(not respuesta.strip()),
        )

    # ── RESULTADOS ────────────────────────────────────────────────────────────
    if analizar and respuesta.strip():
        if palabras < 20:
            st.warning("Tu respuesta tiene menos de 20 palabras. El análisis puede no ser confiable — cuenta un caso real con más detalle.")

        hipotetica = es_hipotetica(respuesta)
        if hipotetica:
            st.warning('Tu respuesta parece hipotética ("yo haría..."). En una entrevista por competencias te piden un caso que sí viviste.')

        with st.spinner("Analizando con IA..."):
            resultado = predecir_star(respuesta, modelos, umbrales)

        total_p = sum(resultado["predicciones"].values())
        verdicts = {
            4: ("🌟 Respuesta STAR Completa", "Excelente — tu respuesta incluye los 4 componentes STAR. ¡Estás listo para la entrevista!"),
            3: ("⚡ Casi perfecto", "Muy buena respuesta — falta un componente para llegar al 100%."),
            2: ("📈 Buen inicio", "Tienes 2 de 4 componentes. Agrega los que faltan para una respuesta sólida."),
            1: ("💡 Necesita más estructura", "Solo 1 componente detectado. La respuesta necesita más desarrollo."),
            0: ("🔧 Sin estructura STAR", "No se detectaron componentes STAR. Reorganiza tu respuesta con la plantilla."),
        }
        v_title, v_desc = verdicts[total_p]
        tags = [f"{NOMBRES_STAR[e][0]} ✓" for e, v in resultado["predicciones"].items() if v == 1]
        tags_html = "".join(f'<span class="iq-results-tag">{t}</span>' for t in tags) if tags else '<span class="iq-results-tag" style="background:rgba(248,113,113,0.2)">Sin componentes</span>'

        st.markdown(f"""
        <div class="iq-results-hero">
          {render_gauge(total_p)}
          <div class="iq-results-info">
            <div class="iq-results-score-label">Puntuación STAR</div>
            <div class="iq-results-verdict">{v_title}</div>
            <div class="iq-results-desc">{v_desc}</div>
            <div class="iq-results-tags">{tags_html}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Cards STAR
        cards_html = '<div class="iq-star-row">'
        for et in ETIQUETAS:
            letra, nombre, emoji = NOMBRES_STAR[et]
            presente = resultado["predicciones"][et] == 1
            prob = resultado["probabilidades"][et]
            u = umbrales[et]
            cls = "present" if presente else "absent"
            status = "✅" if presente else "❌"
            pill_txt = "Presente" if presente else "Ausente"
            cards_html += f"""
            <div class="iq-star-card {cls}">
              <div class="iq-star-card-top">{emoji}</div>
              <div class="iq-star-letter">{letra}</div>
              <div class="iq-star-name">{nombre}</div>
              <div class="iq-star-status">{status}</div>
              <span class="iq-star-pill">{pill_txt}</span>
              <div class="iq-star-prob">p={prob:.2f} · u={u}</div>
            </div>"""
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

        # Feedback
        with st.spinner("Generando feedback personalizado..."):
            feedback, modo = generar_feedback(pregunta_final, respuesta, resultado, hipotetica)

        modo_html = (
            '<span class="iq-feedback-mode-badge ia">🤖 Google Gemini</span>'
            if modo == "ia" else
            '<span class="iq-feedback-mode-badge rules">📋 Reglas estructuradas</span>'
        )
        st.markdown(f"""
        <div class="iq-feedback-wrap">
          <div class="iq-feedback-header">
            <div class="iq-feedback-title">💬 Feedback personalizado</div>
            {modo_html}
          </div>
          <div class="iq-feedback-body">
            {feedback.replace(chr(10), '<br>')}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Plantilla STAR
        ausentes_et = [et for et, v in resultado["predicciones"].items() if v == 0]
        if ausentes_et:
            with st.expander("📐 Ver plantilla STAR para mejorar tu respuesta"):
                st.markdown("""
                <div class="iq-template-grid">
                  <div class="iq-template-item">
                    <div class="iq-template-letter">S</div>
                    <div class="iq-template-role">Situación</div>
                    <div class="iq-template-text">"En [empresa/equipo/momento], nos enfrentamos a [contexto específico]..."</div>
                  </div>
                  <div class="iq-template-item">
                    <div class="iq-template-letter">T</div>
                    <div class="iq-template-role">Tarea</div>
                    <div class="iq-template-text">"Mi responsabilidad era [objetivo/rol específico tuyo]..."</div>
                  </div>
                  <div class="iq-template-item">
                    <div class="iq-template-letter">A</div>
                    <div class="iq-template-role">Acción</div>
                    <div class="iq-template-text">"Lo que hice fue [pasos concretos en primera persona]..."</div>
                  </div>
                  <div class="iq-template-item">
                    <div class="iq-template-letter">R</div>
                    <div class="iq-template-role">Resultado</div>
                    <div class="iq-template-text">"Como resultado, [logro + datos: %, tiempo, reconocimiento]..."</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        _, r_col, _ = st.columns([1, 2, 1])
        with r_col:
            if st.button("🔄  Analizar otra respuesta", use_container_width=True):
                st.rerun()

    # ── FOOTER ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="iq-footer">
        InterviewIQ · AD5018 IA para Negocios · UTEC 2026-2 ·
        <a href="https://github.com/itslueli/InterviewIQ" style="color:#9B59F5;text-decoration:none;">GitHub</a>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
