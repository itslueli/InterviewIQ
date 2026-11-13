"""
InterviewIQ — MVP Streamlit
Componente A2: Clasificador STAR + Capa de lenguaje G1: feedback con LLM (Gemini) y contexto fijo
AD5018 IA para Negocios — UTEC 2026-2
"""

import streamlit as st
import joblib
import json
import re
import os
from pathlib import Path

# ─── Configuración de página ────────────────────────────────────────────────
st.set_page_config(
    page_title="InterviewIQ",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Estilos CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #0D1B2A;
    color: #F8FAFC;
}

/* ── Header ── */
.iq-header {
    background: linear-gradient(135deg, #0D1B2A 0%, #0f2744 60%, #0D1B2A 100%);
    border-bottom: 1px solid rgba(0, 212, 255, 0.15);
    padding: 2.5rem 2rem 2rem;
    text-align: center;
    margin: -1rem -1rem 2rem -1rem;
    position: relative;
    overflow: hidden;
}
.iq-header::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%; transform: translateX(-50%);
    width: 400px; height: 200px;
    background: radial-gradient(ellipse, rgba(0,212,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.iq-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.iq-logo span {
    color: #00D4FF;
}
.iq-tagline {
    font-size: 0.95rem;
    color: #94A3B8;
    font-weight: 400;
    margin-bottom: 0.5rem;
}
.iq-badge {
    display: inline-block;
    background: rgba(0, 212, 255, 0.1);
    border: 1px solid rgba(0, 212, 255, 0.25);
    color: #00D4FF;
    font-size: 0.72rem;
    font-weight: 500;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    letter-spacing: 0.02em;
}

/* ── Notice banner ── */
.iq-notice {
    background: rgba(0, 212, 255, 0.05);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    font-size: 0.85rem;
    color: #CBD5E1;
    line-height: 1.5;
}
.iq-notice strong { color: #00D4FF; }

.iq-privacy {
    background: rgba(248, 250, 252, 0.03);
    border-left: 3px solid rgba(148, 163, 184, 0.3);
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 1rem;
    margin-bottom: 1.5rem;
    font-size: 0.78rem;
    color: #64748B;
    line-height: 1.5;
}

/* ── Step headers ── */
.iq-step {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.2rem;
    margin-top: 0.5rem;
}
.iq-step-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: rgba(0, 212, 255, 0.15);
    line-height: 1;
    min-width: 2.5rem;
}
.iq-step-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: #F1F5F9;
    line-height: 1.2;
}
.iq-step-sub {
    font-size: 0.8rem;
    color: #64748B;
    margin-top: 0.1rem;
}

/* ── Question card ── */
.iq-question-active {
    background: rgba(0, 212, 255, 0.06);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-top: 0.8rem;
    font-size: 0.95rem;
    color: #E2E8F0;
    font-style: italic;
    line-height: 1.5;
}

/* ── Divider ── */
.iq-divider {
    border: none;
    border-top: 1px solid rgba(248, 250, 252, 0.06);
    margin: 1.8rem 0;
}

/* ── Word count ── */
.iq-wordcount {
    font-size: 0.75rem;
    color: #475569;
    margin-top: 0.4rem;
}
.iq-wordcount.ok { color: #10B981; }
.iq-wordcount.warn { color: #F59E0B; }
.iq-wordcount.bad { color: #EF4444; }

/* ── STAR score gauge ── */
.iq-gauge-wrap {
    text-align: center;
    padding: 1.5rem 1rem;
}
.iq-gauge-ring {
    display: inline-block;
    position: relative;
    width: 120px;
    height: 120px;
    margin-bottom: 0.8rem;
}
.iq-gauge-ring svg {
    transform: rotate(-90deg);
}
.iq-gauge-label {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #F8FAFC;
    line-height: 1;
}
.iq-gauge-sub {
    font-size: 0.65rem;
    color: #64748B;
    margin-top: 0.1rem;
}

/* ── STAR component cards ── */
.iq-star-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 1.2rem 0;
}
.iq-star-card {
    background: #1E2D3D;
    border: 1px solid rgba(248, 250, 252, 0.07);
    border-radius: 12px;
    padding: 1rem 0.75rem;
    text-align: center;
    transition: transform 0.2s;
}
.iq-star-card.present {
    border-color: rgba(16, 185, 129, 0.4);
    background: rgba(16, 185, 129, 0.07);
}
.iq-star-card.absent {
    border-color: rgba(239, 68, 68, 0.3);
    background: rgba(239, 68, 68, 0.05);
}
.iq-star-emoji { font-size: 1.5rem; margin-bottom: 0.4rem; }
.iq-star-letter {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    line-height: 1;
}
.present .iq-star-letter { color: #10B981; }
.absent .iq-star-letter { color: #EF4444; }
.iq-star-name {
    font-size: 0.72rem;
    color: #94A3B8;
    margin: 0.2rem 0;
}
.iq-star-status { font-size: 1.1rem; margin: 0.3rem 0; }
.iq-star-prob {
    font-size: 0.65rem;
    color: #475569;
    font-family: 'Space Grotesk', monospace;
}

/* ── Result banner ── */
.iq-result-banner {
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.iq-result-banner.full {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34D399;
}
.iq-result-banner.partial {
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.25);
    color: #FCD34D;
}
.iq-result-banner.low {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.25);
    color: #FCA5A5;
}

/* ── Feedback panel ── */
.iq-feedback-panel {
    background: #111f2e;
    border: 1px solid rgba(0, 212, 255, 0.12);
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    margin-top: 0.5rem;
    line-height: 1.7;
    color: #CBD5E1;
    font-size: 0.92rem;
}
.iq-feedback-panel strong { color: #F1F5F9; }
.iq-feedback-mode {
    font-size: 0.72rem;
    color: #475569;
    margin-top: 0.8rem;
    padding-top: 0.8rem;
    border-top: 1px solid rgba(248,250,252,0.05);
}

/* ── STAR template expander ── */
.iq-template {
    background: #1E2D3D;
    border: 1px solid rgba(248, 250, 252, 0.07);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    font-size: 0.85rem;
    color: #94A3B8;
    line-height: 1.8;
}
.iq-template strong { color: #00D4FF; }

/* ── Footer ── */
.iq-footer {
    text-align: center;
    color: #334155;
    font-size: 0.75rem;
    padding: 1.5rem 0 0.5rem;
    border-top: 1px solid rgba(248, 250, 252, 0.04);
    margin-top: 2rem;
}
.iq-footer a { color: #475569; text-decoration: none; }
.iq-footer a:hover { color: #00D4FF; }

/* ── Streamlit overrides ── */
.stSelectbox > div > div {
    background-color: #1E2D3D !important;
    border: 1px solid rgba(248, 250, 252, 0.1) !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
}
.stTextArea > div > div > textarea {
    background-color: #1E2D3D !important;
    border: 1px solid rgba(248, 250, 252, 0.1) !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
    font-size: 0.92rem !important;
    line-height: 1.6 !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: rgba(0, 212, 255, 0.4) !important;
    box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.08) !important;
}
.stTextInput > div > div > input {
    background-color: #1E2D3D !important;
    border: 1px solid rgba(248, 250, 252, 0.1) !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00D4FF 0%, #0099CC 100%) !important;
    color: #0D1B2A !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.5rem !important;
    letter-spacing: 0.01em !important;
    transition: opacity 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    opacity: 0.88 !important;
}
.stButton > button[kind="primary"]:disabled {
    background: #1E2D3D !important;
    color: #334155 !important;
}
.stButton > button:not([kind="primary"]) {
    background: rgba(248, 250, 252, 0.04) !important;
    color: #94A3B8 !important;
    border: 1px solid rgba(248, 250, 252, 0.1) !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: rgba(248, 250, 252, 0.08) !important;
    color: #F1F5F9 !important;
}
.stExpander {
    background: #1A2A3A !important;
    border: 1px solid rgba(248, 250, 252, 0.07) !important;
    border-radius: 10px !important;
}
.stExpander summary {
    color: #94A3B8 !important;
    font-size: 0.88rem !important;
}
/* Spinner */
.stSpinner > div { border-top-color: #00D4FF !important; }

/* Metric */
[data-testid="stMetric"] {
    background: #1E2D3D;
    border: 1px solid rgba(248,250,252,0.07);
    border-radius: 10px;
    padding: 1rem;
}
[data-testid="stMetricLabel"] { color: #64748B !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #F8FAFC !important;
    font-size: 2rem !important;
}
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

/* Warning/error/info boxes */
.stAlert {
    background: rgba(245, 158, 11, 0.07) !important;
    border: 1px solid rgba(245, 158, 11, 0.2) !important;
    border-radius: 8px !important;
    color: #FCD34D !important;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Constantes ──────────────────────────────────────────────────────────────
ETIQUETAS = ['situacion', 'tarea', 'accion', 'resultado']
NOMBRES_STAR = {
    'situacion': ('S', 'Situación', '🌍'),
    'tarea':     ('T', 'Tarea',     '📋'),
    'accion':    ('A', 'Acción',    '⚡'),
    'resultado': ('R', 'Resultado', '🏆'),
}

MODELS_DIR = Path(__file__).parent / "models"

# ─── Carga de modelos ────────────────────────────────────────────────────────
@st.cache_resource
def cargar_modelos():
    modelos = {}
    config_path = MODELS_DIR / "config_clasificador.json"
    if not config_path.exists():
        return None, None
    with open(config_path, "r") as f:
        config = json.load(f)
    umbrales = config.get("umbrales", {
        "situacion": 0.30, "tarea": 0.30, "accion": 0.75, "resultado": 0.70
    })
    for etiqueta in ETIQUETAS:
        pkl_path = MODELS_DIR / f"clasificador_star_{etiqueta}.pkl"
        if pkl_path.exists():
            modelos[etiqueta] = joblib.load(pkl_path)
        else:
            return None, None
    return modelos, umbrales


# ─── Predicción ──────────────────────────────────────────────────────────────
def limpiar_texto(texto: str) -> str:
    texto = str(texto).lower()
    texto = re.sub(r'[^\w\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


def predecir_star(respuesta_texto: str, modelos: dict, umbrales: dict) -> dict:
    texto_limpio = limpiar_texto(respuesta_texto)
    predicciones = {}
    probabilidades = {}
    for etiqueta in ETIQUETAS:
        modelo = modelos[etiqueta]
        umbral = umbrales[etiqueta]
        prob = modelo.predict_proba([texto_limpio])[0][1]
        pred = int(prob >= umbral)
        predicciones[etiqueta] = pred
        probabilidades[etiqueta] = round(float(prob), 3)
    componentes = [NOMBRES_STAR[e][0] for e, v in predicciones.items() if v == 1]
    resumen = "-".join(componentes) if componentes else "Ninguno"
    return {
        "predicciones": predicciones,
        "probabilidades": probabilidades,
        "resumen": resumen,
        "componentes_presentes": componentes,
    }


# ─── Feedback ────────────────────────────────────────────────────────────────
GUIA_STAR = """GUÍA STAR DE INTERVIEWIQ (contexto fijo del equipo)
- Situación: contexto concreto — dónde, cuándo, con quién (curso, práctica, trabajo, equipo).
- Tarea: la responsabilidad o el objetivo específico del candidato en esa situación.
- Acción: los pasos que el candidato tomó personalmente (verbos en primera persona: "organicé", "propuse").
- Resultado: qué cambió gracias a la acción, idealmente con un dato verificable (nota, tiempo, %, reconocimiento) y qué aprendió.
- Una buena respuesta dura entre 1 y 2 minutos hablada (unas 100–250 palabras).
- Errores comunes: hablar en "nosotros" sin decir qué hizo uno; contar la situación y olvidar el resultado; respuestas hipotéticas ("yo haría...") en vez de un caso real."""

SYSTEM_PROMPT = f"""Eres InterviewIQ, un coach de entrevistas por competencias para estudiantes universitarios peruanos de últimos ciclos.
Das feedback en español, cálido y directo, de máximo 170 palabras.

{GUIA_STAR}

REGLAS QUE NO PUEDES ROMPER:
1. El análisis STAR que recibes viene de un modelo entrenado por el equipo. NO lo contradigas: nunca digas que un componente marcado AUSENTE está presente, ni al revés.
2. No inventes experiencias, datos ni logros del estudiante. Si sugieres un dato, dilo como ejemplo entre corchetes, p. ej. [porcentaje de mejora].
3. No afirmes probabilidades de ser contratado ni prometas resultados en entrevistas reales.
4. Si la respuesta no tiene relación con una entrevista o es demasiado corta, dilo con amabilidad y pide un ejemplo real.

FORMATO:
**Lo que hiciste bien:** 1–2 frases.
**Lo que falta:** un punto por cada componente AUSENTE, explicando por qué importa.
**Cómo mejorarla:** una sugerencia concreta (puede ser una frase modelo que el estudiante complete).
"""


def _obtener_api_key() -> str:
    try:
        return st.secrets.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
    except Exception:
        return os.environ.get("GEMINI_API_KEY", "")


def _obtener_modelo_llm() -> str:
    try:
        return st.secrets.get("GEMINI_MODEL", "") or "gemini-2.5-flash"
    except Exception:
        return "gemini-2.5-flash"


def generar_feedback(pregunta: str, respuesta: str, resultado_star: dict, hipotetica: bool = False) -> tuple[str, str]:
    api_key = _obtener_api_key()
    if not api_key:
        return _feedback_por_reglas(resultado_star), "reglas"
    predicciones = resultado_star["predicciones"]
    presentes = [NOMBRES_STAR[e][1] for e, v in predicciones.items() if v == 1]
    ausentes = [NOMBRES_STAR[e][1] for e, v in predicciones.items() if v == 0]
    mensaje = f"""Pregunta de entrevista: "{pregunta or 'Pregunta conductual libre'}"

Respuesta del estudiante:
\"\"\"{respuesta}\"\"\"

Análisis STAR del modelo (no lo contradigas):
- PRESENTES: {', '.join(presentes) if presentes else 'ninguno'}
- AUSENTES: {', '.join(ausentes) if ausentes else 'ninguno (respuesta completa)'}"""
    if hipotetica:
        mensaje += (
            "\n\nALERTA: la respuesta parece hipotética (habla de lo que el estudiante 'haría'), "
            "no de un caso real. Explícale primero que en una entrevista por competencias debe contar "
            "una experiencia que sí vivió, y pídele un ejemplo concreto."
        )
    try:
        import requests
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{_obtener_modelo_llm()}:generateContent"
        )
        payload = {
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [{"role": "user", "parts": [{"text": mensaje}]}],
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 800},
        }
        r = requests.post(url, params={"key": api_key}, json=payload, timeout=25)
        r.raise_for_status()
        texto = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        if not texto:
            raise ValueError("respuesta vacía")
        return texto, "ia"
    except Exception:
        return _feedback_por_reglas(resultado_star), "reglas"


def _feedback_por_reglas(resultado_star: dict) -> str:
    predicciones = resultado_star["predicciones"]
    ausentes = [NOMBRES_STAR[e][1] for e, v in predicciones.items() if v == 0]
    presentes = [NOMBRES_STAR[e][1] for e, v in predicciones.items() if v == 1]
    total = len(presentes)
    if total == 4:
        return (
            "🌟 **¡Respuesta STAR completa!** Tu respuesta incluye los 4 componentes. "
            "Tienes una estructura sólida. Para seguir mejorando, cuantifica tus resultados "
            "con números, porcentajes o plazos concretos."
        )
    elif total == 0:
        return (
            "**Tu respuesta necesita estructura STAR.** Organízala así:\n\n"
            "**Situación** — ¿Cuál era el contexto? (empresa, equipo, momento)\n\n"
            "**Tarea** — ¿Cuál era tu responsabilidad específica?\n\n"
            "**Acción** — ¿Qué hiciste tú concretamente?\n\n"
            "**Resultado** — ¿Qué logró tu acción? (con datos si puedes)"
        )
    else:
        fb = f"**Detectamos:** {', '.join(presentes)}.\n\n"
        fb += f"**Por trabajar:** {', '.join(ausentes)}.\n\n"
        sugerencias = {
            "Situación": "Empieza describiendo el contexto: en qué empresa, equipo o momento ocurrió.",
            "Tarea": "Explica cuál era TU responsabilidad específica en esa situación.",
            "Acción": "Detalla los pasos concretos que TÚ tomaste — usa verbos de acción en primera persona.",
            "Resultado": "Cierra con el impacto de tus acciones, idealmente con números o métricas.",
        }
        for a in ausentes:
            fb += f"→ **{a}:** {sugerencias.get(a, '')}\n\n"
        return fb


# ─── Detección de respuestas hipotéticas ─────────────────────────────────────
PATRON_HIPOTETICO = re.compile(
    r"\b(si (yo )?(tuviera|estuviera|fuera|me pasara|me tocara)|"
    r"(yo )?(har[ií]a|intentar[ií]a|buscar[ií]a|hablar[ií]a|tratar[ií]a|propondr[ií]a|escuchar[ií]a)|"
    r"lo que har[ií]a|deber[ií]a)\b",
    re.IGNORECASE,
)


def es_hipotetica(texto: str) -> bool:
    return len(PATRON_HIPOTETICO.findall(texto)) >= 2


# ─── Gauge SVG ───────────────────────────────────────────────────────────────
def render_gauge(total: int) -> str:
    pct = total / 4
    r = 48
    circ = 2 * 3.14159 * r
    dash = pct * circ
    colors = {0: "#EF4444", 1: "#EF4444", 2: "#F59E0B", 3: "#F59E0B", 4: "#10B981"}
    color = colors[total]
    return f"""
    <div class="iq-gauge-wrap">
        <div class="iq-gauge-ring">
            <svg width="120" height="120" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="{r}" fill="none" stroke="rgba(248,250,252,0.06)" stroke-width="8"/>
                <circle cx="60" cy="60" r="{r}" fill="none" stroke="{color}" stroke-width="8"
                    stroke-dasharray="{dash:.1f} {circ:.1f}"
                    stroke-linecap="round"
                    style="transition: stroke-dasharray 0.6s ease;"/>
            </svg>
            <div class="iq-gauge-label">{total}<span style="font-size:1rem;color:#64748B">/4</span></div>
        </div>
        <div style="font-family:'Space Grotesk',sans-serif; font-size:0.8rem; color:#64748B;">componentes STAR</div>
    </div>
    """


# ─── Preguntas ────────────────────────────────────────────────────────────────
PREGUNTAS_EJEMPLO = [
    "Cuéntame de una vez que tuviste que trabajar bajo presión y cómo lo manejaste.",
    "Describe una situación en la que tuviste que resolver un conflicto en tu equipo.",
    "Cuéntame de un logro del que te sientas orgulloso/a en tu vida académica o laboral.",
    "¿Hubo alguna vez que cometiste un error importante? ¿Qué hiciste al respecto?",
    "Describe una situación en la que tuviste que convencer a alguien de tu idea.",
]


# ─── UI ───────────────────────────────────────────────────────────────────────
def main():
    # Header
    st.markdown("""
    <div class="iq-header">
        <div class="iq-logo">Interview<span>IQ</span></div>
        <div class="iq-tagline">Entrena tus respuestas de entrevista con el método STAR</div>
        <span class="iq-badge">AD5018 IA para Negocios · UTEC 2026-2</span>
    </div>
    """, unsafe_allow_html=True)

    # Avisos
    st.markdown("""
    <div class="iq-notice">
        <strong>Estás usando una herramienta con Inteligencia Artificial.</strong>
        Un modelo entrenado por el equipo detecta los componentes STAR de tu respuesta
        y un modelo de lenguaje redacta el feedback. Es una herramienta de práctica:
        puede equivocarse y no es una evaluación oficial ni predice si te contratarán.
    </div>
    <div class="iq-privacy">
        🔒 <strong>Privacidad:</strong> tu respuesta solo se usa para darte feedback en esta sesión.
        No se guarda ni se asocia a tu identidad. Se envía a Google Gemini únicamente para generar el feedback.
        Evita escribir datos personales como tu DNI, teléfono o nombres de terceros (Ley N.° 29733).
    </div>
    """, unsafe_allow_html=True)

    # Cargar modelos
    modelos, umbrales = cargar_modelos()
    if modelos is None:
        st.error("⚠️ Modelos no encontrados. Verifica que la carpeta `models/` contiene los archivos `.pkl` y `config_clasificador.json`.")
        st.stop()

    # ── Paso 1 ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="iq-step">
        <div class="iq-step-num">01</div>
        <div>
            <div class="iq-step-title">Elige una pregunta de entrevista</div>
            <div class="iq-step-sub">Selecciona una del banco o escribe la tuya</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    pregunta_sel = st.selectbox(
        "Pregunta:",
        options=[""] + PREGUNTAS_EJEMPLO + ["✏️ Escribir mi propia pregunta..."],
        index=0,
        label_visibility="collapsed",
    )

    pregunta_custom = ""
    if pregunta_sel == "✏️ Escribir mi propia pregunta...":
        pregunta_custom = st.text_input("Tu pregunta:", placeholder="Escribe aquí tu pregunta de entrevista...", label_visibility="collapsed")
        pregunta_final = pregunta_custom
    else:
        pregunta_final = pregunta_sel

    if pregunta_final:
        st.markdown(f'<div class="iq-question-active">"{pregunta_final}"</div>', unsafe_allow_html=True)

    st.markdown('<hr class="iq-divider">', unsafe_allow_html=True)

    # ── Paso 2 ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="iq-step">
        <div class="iq-step-num">02</div>
        <div>
            <div class="iq-step-title">Escribe tu respuesta</div>
            <div class="iq-step-sub">Mínimo 20 palabras · Recomendado 50–150 palabras</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    respuesta = st.text_area(
        "Tu respuesta:",
        placeholder="Escribe tu respuesta aquí...\n\nConsejo: intenta incluir una Situación, Tarea, Acción y Resultado.",
        height=180,
        label_visibility="collapsed",
    )

    palabras = len(respuesta.split()) if respuesta.strip() else 0
    if respuesta.strip():
        if palabras >= 50:
            cls, label = "ok", f"{palabras} palabras ✓"
        elif palabras >= 20:
            cls, label = "warn", f"{palabras} palabras — intenta llegar a 50"
        else:
            cls, label = "bad", f"{palabras} palabras — muy corta"
        st.markdown(f'<div class="iq-wordcount {cls}">{label}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="iq-divider">', unsafe_allow_html=True)

    # ── Botón ─────────────────────────────────────────────────────────────────
    analizar = st.button(
        "Analizar mi respuesta →",
        type="primary",
        use_container_width=True,
        disabled=(not respuesta.strip()),
    )

    # ── Resultados ────────────────────────────────────────────────────────────
    if analizar and respuesta.strip():
        if palabras < 20:
            st.warning("Tu respuesta tiene menos de 20 palabras. El análisis puede no ser confiable — cuenta un caso real con más detalle.")

        hipotetica = es_hipotetica(respuesta)
        if hipotetica:
            st.warning('Tu respuesta parece hipotética ("yo haría..."). En una entrevista por competencias te piden un caso que sí viviste. El análisis de abajo puede ser menos preciso.')

        with st.spinner("Analizando..."):
            resultado = predecir_star(respuesta, modelos, umbrales)

        # ── Paso 3: Análisis ──────────────────────────────────────────────────
        st.markdown("""
        <div class="iq-step">
            <div class="iq-step-num">03</div>
            <div>
                <div class="iq-step-title">Análisis STAR</div>
                <div class="iq-step-sub">Componentes detectados en tu respuesta</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        total_presentes = sum(resultado["predicciones"].values())

        col_gauge, col_banner = st.columns([1, 2])
        with col_gauge:
            st.markdown(render_gauge(total_presentes), unsafe_allow_html=True)
        with col_banner:
            st.markdown(f"<div style='height:1.5rem'></div>", unsafe_allow_html=True)
            if total_presentes == 4:
                st.markdown('<div class="iq-result-banner full">🌟 Respuesta STAR completa</div>', unsafe_allow_html=True)
            elif total_presentes >= 2:
                st.markdown('<div class="iq-result-banner partial">⚡ Buen inicio — puedes mejorarla</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="iq-result-banner low">💡 Necesita más estructura STAR</div>', unsafe_allow_html=True)
            st.markdown(f"<div style='font-family:Space Grotesk,sans-serif; font-size:0.85rem; color:#475569; margin-top:0.5rem;'>Detectados: <strong style='color:#F1F5F9'>{resultado['resumen']}</strong></div>", unsafe_allow_html=True)

        # Cards STAR
        cards_html = '<div class="iq-star-grid">'
        for etiqueta in ETIQUETAS:
            letra, nombre, emoji = NOMBRES_STAR[etiqueta]
            presente = resultado["predicciones"][etiqueta] == 1
            prob = resultado["probabilidades"][etiqueta]
            umbral = umbrales[etiqueta]
            cls = "present" if presente else "absent"
            status = "✅" if presente else "❌"
            cards_html += f"""
            <div class="iq-star-card {cls}">
                <div class="iq-star-emoji">{emoji}</div>
                <div class="iq-star-letter">{letra}</div>
                <div class="iq-star-name">{nombre}</div>
                <div class="iq-star-status">{status}</div>
                <div class="iq-star-prob">p={prob:.2f} · u={umbral}</div>
            </div>"""
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

        st.markdown('<hr class="iq-divider">', unsafe_allow_html=True)

        # ── Paso 4: Feedback ──────────────────────────────────────────────────
        st.markdown("""
        <div class="iq-step">
            <div class="iq-step-num">04</div>
            <div>
                <div class="iq-step-title">Feedback personalizado</div>
                <div class="iq-step-sub">Basado en el análisis STAR de tu respuesta</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Generando feedback..."):
            feedback, modo = generar_feedback(pregunta_final, respuesta, resultado, hipotetica)

        st.markdown(f"""
        <div class="iq-feedback-panel">
            {feedback.replace(chr(10), '<br>')}
            <div class="iq-feedback-mode">
                {"🤖 Generado por IA (Google Gemini) · basado en el análisis STAR del modelo" if modo == "ia" else "ℹ️ Generado con reglas estructuradas · servicio de IA no disponible en este momento"}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Plantilla STAR
        ausentes = [etiqueta for etiqueta, v in resultado["predicciones"].items() if v == 0]
        if ausentes:
            st.markdown('<hr class="iq-divider">', unsafe_allow_html=True)
            with st.expander("Ver plantilla STAR para mejorar tu respuesta"):
                st.markdown("""
                <div class="iq-template">
                    <strong>S — Situación</strong> <em>(contexto)</em><br>
                    "En mi práctica en [empresa/equipo], durante [momento específico]..."<br><br>
                    <strong>T — Tarea</strong> <em>(tu rol)</em><br>
                    "Mi responsabilidad era [qué se esperaba de ti]..."<br><br>
                    <strong>A — Acción</strong> <em>(qué hiciste tú)</em><br>
                    "Lo que hice fue [pasos concretos que tomaste]..."<br><br>
                    <strong>R — Resultado</strong> <em>(impacto medible)</em><br>
                    "Como resultado, [logro + datos si puedes]..."
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<hr class="iq-divider">', unsafe_allow_html=True)
        if st.button("Analizar otra respuesta", use_container_width=True):
            st.rerun()

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="iq-footer">
        InterviewIQ · AD5018 IA para Negocios · UTEC 2026-2 ·
        <a href="https://github.com/itslueli/InterviewIQ">GitHub</a>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
