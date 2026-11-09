"""
InterviewIQ — MVP Streamlit
Componente A2: Clasificador STAR + Componente G2: Feedback RAG
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
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .star-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }
    .star-present {
        border-left-color: #28a745;
        background: #f0fff4;
    }
    .star-absent {
        border-left-color: #dc3545;
        background: #fff5f5;
    }
    .feedback-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .metric-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    .pill-green { background: #d4edda; color: #155724; }
    .pill-red   { background: #f8d7da; color: #721c24; }
    .pill-blue  { background: #d1ecf1; color: #0c5460; }
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

# Ruta a los modelos — funciona local y en Streamlit Cloud
MODELS_DIR = Path(__file__).parent / "models"

# ─── Carga de modelos (con caché) ────────────────────────────────────────────
@st.cache_resource
def cargar_modelos():
    """Carga los 4 modelos .pkl y el config JSON desde la carpeta models/."""
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


# ─── Funciones de predicción ─────────────────────────────────────────────────
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

    componentes = [
        NOMBRES_STAR[e][0]
        for e, v in predicciones.items() if v == 1
    ]
    resumen = "-".join(componentes) if componentes else "Ninguno"

    return {
        "predicciones": predicciones,
        "probabilidades": probabilidades,
        "resumen": resumen,
        "componentes_presentes": componentes,
    }


# ─── Feedback con OpenAI (G2) — opcional ─────────────────────────────────────
def generar_feedback_rag(respuesta: str, resultado_star: dict, api_key: str) -> str:
    """
    Genera feedback personalizado usando GPT-4o-mini.
    Si no hay API key, retorna feedback basado en reglas.
    """
    if not api_key:
        return _feedback_por_reglas(resultado_star)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        componentes = resultado_star["predicciones"]
        ausentes = [
            NOMBRES_STAR[e][1]
            for e, v in componentes.items() if v == 0
        ]
        presentes = [
            NOMBRES_STAR[e][1]
            for e, v in componentes.items() if v == 1
        ]

        prompt_sistema = """Eres un coach experto en entrevistas de trabajo para estudiantes universitarios.
Tu rol es dar feedback constructivo, específico y motivador sobre respuestas a preguntas de entrevista.
Siempre usas el método STAR (Situación, Tarea, Acción, Resultado) como marco de referencia.
Sé conciso (máximo 200 palabras), directo y da ejemplos concretos de cómo mejorar."""

        prompt_usuario = f"""El estudiante respondió esta pregunta de entrevista:

"{respuesta}"

Análisis automático STAR:
- Componentes PRESENTES: {', '.join(presentes) if presentes else 'Ninguno'}
- Componentes AUSENTES: {', '.join(ausentes) if ausentes else 'Ninguno (¡respuesta completa!)'}

Por favor:
1. Reconoce brevemente lo que hizo bien
2. Explica qué componentes STAR faltan y POR QUÉ son importantes
3. Da una sugerencia CONCRETA de cómo mejorar la respuesta
4. Termina con una frase motivadora"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario},
            ],
            max_tokens=400,
            temperature=0.7,
        )
        return response.choices[0].message.content

    except Exception as e:
        return _feedback_por_reglas(resultado_star) + f"\n\n*(Nota: feedback IA no disponible: {str(e)[:60]})*"


def _feedback_por_reglas(resultado_star: dict) -> str:
    """Feedback basado en reglas cuando no hay API key."""
    predicciones = resultado_star["predicciones"]
    ausentes = [NOMBRES_STAR[e][1] for e, v in predicciones.items() if v == 0]
    presentes = [NOMBRES_STAR[e][1] for e, v in predicciones.items() if v == 1]
    total = len(presentes)

    if total == 4:
        return (
            "🌟 **¡Excelente respuesta!** Tu respuesta incluye los 4 componentes STAR. "
            "Tienes una estructura clara y completa. Para seguir mejorando, "
            "asegúrate de cuantificar tus resultados (números, porcentajes, plazos)."
        )
    elif total == 0:
        return (
            "💡 **Tu respuesta necesita más estructura.** Intenta organizar tu respuesta así:\n\n"
            "1. **Situación**: ¿Cuál era el contexto? (empresa, equipo, momento)\n"
            "2. **Tarea**: ¿Cuál era tu responsabilidad específica?\n"
            "3. **Acción**: ¿Qué hiciste tú concretamente?\n"
            "4. **Resultado**: ¿Qué logró tu acción? (con datos si puedes)"
        )
    else:
        fb = f"✅ **Bien encaminado.** Detectamos: {', '.join(presentes)}.\n\n"
        fb += f"📌 **Por trabajar**: {', '.join(ausentes)}.\n\n"
        sugerencias = {
            "Situación": "Empieza describiendo el contexto: en qué empresa/equipo/momento ocurrió.",
            "Tarea": "Explica cuál era TU responsabilidad específica en esa situación.",
            "Acción": "Detalla los pasos concretos que TÚ tomaste (usa verbos de acción).",
            "Resultado": "Cierra con el impacto de tus acciones, idealmente con números o métricas.",
        }
        for a in ausentes:
            fb += f"- **{a}**: {sugerencias.get(a, '')}\n"
        return fb


# ─── Preguntas de ejemplo ─────────────────────────────────────────────────────
PREGUNTAS_EJEMPLO = [
    "Cuéntame de una vez que tuviste que trabajar bajo presión y cómo lo manejaste.",
    "Describe una situación en la que tuviste que resolver un conflicto en tu equipo.",
    "Cuéntame de un logro del que te sientas orgulloso/a en tu vida académica o laboral.",
    "¿Hubo alguna vez que cometiste un error importante? ¿Qué hiciste al respecto?",
    "Describe una situación en la que tuviste que convencer a alguien de tu idea.",
]

# ─── UI Principal ─────────────────────────────────────────────────────────────
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 InterviewIQ</h1>
        <p style="font-size:1.1rem; opacity:0.9;">
            Entrena tus respuestas de entrevista con el método STAR
        </p>
        <small>AD5018 IA para Negocios · UTEC 2026-2</small>
    </div>
    """, unsafe_allow_html=True)

    # Cargar modelos
    modelos, umbrales = cargar_modelos()

    if modelos is None:
        st.error(
            "⚠️ **Modelos no encontrados.** "
            "Asegúrate de que la carpeta `models/` contiene los archivos `.pkl` y `config_clasificador.json`."
        )
        st.info(
            "📂 Estructura esperada:\n"
            "```\n"
            "models/\n"
            "  clasificador_star_situacion.pkl\n"
            "  clasificador_star_tarea.pkl\n"
            "  clasificador_star_accion.pkl\n"
            "  clasificador_star_resultado.pkl\n"
            "  config_clasificador.json\n"
            "```"
        )
        st.stop()

    # ── Paso 1: Selección de pregunta ─────────────────────────────────────────
    st.subheader("📝 Paso 1 — Elige una pregunta de entrevista")

    col1, col2 = st.columns([3, 1])
    with col1:
        pregunta_sel = st.selectbox(
            "Pregunta:",
            options=[""] + PREGUNTAS_EJEMPLO + ["✏️ Escribir mi propia pregunta..."],
            index=0,
            label_visibility="collapsed",
        )

    pregunta_custom = ""
    if pregunta_sel == "✏️ Escribir mi propia pregunta...":
        pregunta_custom = st.text_input("Tu pregunta:", placeholder="Escribe aquí tu pregunta de entrevista...")
        pregunta_final = pregunta_custom
    else:
        pregunta_final = pregunta_sel

    if pregunta_final:
        st.info(f"**{pregunta_final}**")

    st.divider()

    # ── Paso 2: Respuesta del usuario ─────────────────────────────────────────
    st.subheader("💬 Paso 2 — Escribe tu respuesta")

    respuesta = st.text_area(
        "Tu respuesta:",
        placeholder=(
            "Escribe tu respuesta aquí...\n\n"
            "Consejo: intenta incluir una Situación, Tarea, Acción y Resultado."
        ),
        height=180,
        label_visibility="collapsed",
    )

    palabras = len(respuesta.split()) if respuesta.strip() else 0
    if respuesta.strip():
        color = "🟢" if palabras >= 50 else "🟡" if palabras >= 20 else "🔴"
        st.caption(f"{color} {palabras} palabras {'(longitud recomendada ≥50)' if palabras < 50 else '✓'}")

    # ── Configuración API (opcional) ──────────────────────────────────────────
    with st.expander("⚙️ Configuración — Feedback con IA (opcional)"):
        st.markdown(
            "Para recibir feedback personalizado con GPT-4o-mini, ingresa tu OpenAI API Key. "
            "Sin API Key, el sistema usa feedback basado en reglas."
        )
        api_key = st.text_input(
            "OpenAI API Key:",
            type="password",
            placeholder="sk-...",
            help="Tu clave no se guarda ni se envía a ningún servidor externo salvo OpenAI.",
        )

    st.divider()

    # ── Botón de análisis ─────────────────────────────────────────────────────
    analizar = st.button(
        "🔍 Analizar mi respuesta",
        type="primary",
        use_container_width=True,
        disabled=(not respuesta.strip()),
    )

    # ── Resultados ────────────────────────────────────────────────────────────
    if analizar and respuesta.strip():
        with st.spinner("Analizando tu respuesta..."):
            resultado = predecir_star(respuesta, modelos, umbrales)

        st.subheader("📊 Paso 3 — Análisis STAR")

        # Score visual
        total_presentes = sum(resultado["predicciones"].values())
        score_pct = total_presentes * 25

        col_score, col_resumen = st.columns([1, 2])
        with col_score:
            st.metric(
                label="Componentes STAR",
                value=f"{total_presentes}/4",
                delta=f"{score_pct}% completo",
            )
        with col_resumen:
            st.markdown(f"**Detectados:** `{resultado['resumen']}`")
            if total_presentes == 4:
                st.success("🌟 ¡Respuesta STAR completa!")
            elif total_presentes >= 2:
                st.warning("⚡ Buen inicio, puedes mejorarla")
            else:
                st.error("💡 Necesita más estructura STAR")

        # Cards por componente
        st.markdown("**Detalle por componente:**")
        cols = st.columns(4)
        for i, etiqueta in enumerate(ETIQUETAS):
            letra, nombre, emoji = NOMBRES_STAR[etiqueta]
            presente = resultado["predicciones"][etiqueta] == 1
            prob = resultado["probabilidades"][etiqueta]
            umbral = umbrales[etiqueta]

            with cols[i]:
                estado = "✅" if presente else "❌"
                color = "#28a745" if presente else "#dc3545"
                st.markdown(
                    f"""
                    <div style="
                        border: 2px solid {color};
                        border-radius: 10px;
                        padding: 0.75rem;
                        text-align: center;
                        background: {'#f0fff4' if presente else '#fff5f5'};
                    ">
                        <div style="font-size:1.5rem">{emoji}</div>
                        <div style="font-weight:700; color:{color}">{letra} — {nombre}</div>
                        <div style="font-size:1.2rem">{estado}</div>
                        <div style="font-size:0.75rem; color:#666;">
                            prob: {prob:.2f} | umbral: {umbral}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.divider()

        # ── Feedback ─────────────────────────────────────────────────────────
        st.subheader("💡 Paso 4 — Feedback personalizado")

        with st.spinner("Generando feedback..."):
            feedback = generar_feedback_rag(respuesta, resultado, api_key if api_key else "")

        st.markdown(
            f'<div class="feedback-box">{feedback}</div>',
            unsafe_allow_html=True,
        )

        # ── Recomendación de siguiente paso ───────────────────────────────────
        st.divider()
        ausentes = [
            etiqueta for etiqueta, v in resultado["predicciones"].items() if v == 0
        ]
        if ausentes:
            st.subheader("🚀 Siguiente paso")
            with st.expander("Ver cómo estructurar una respuesta STAR completa"):
                st.markdown("""
**Plantilla STAR:**

> **S — Situación** *(contexto)*
> "En mi práctica en [empresa/equipo], durante [momento específico]..."

> **T — Tarea** *(tu rol)*
> "Mi responsabilidad era [qué se esperaba de ti]..."

> **A — Acción** *(qué hiciste tú)*
> "Lo que hice fue [pasos concretos que tomaste]..."

> **R — Resultado** *(impacto medible)*
> "Como resultado, [logro + datos si puedes]..."
                """)

        # Botón para reiniciar
        if st.button("🔄 Analizar otra respuesta", use_container_width=True):
            st.rerun()

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#999; font-size:0.8rem;'>"
        "InterviewIQ · AD5018 IA para Negocios · UTEC 2026-2 · "
        "<a href='https://github.com/itslueli/InterviewIQ' style='color:#667eea'>GitHub</a>"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
