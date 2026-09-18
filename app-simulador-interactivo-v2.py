import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

st.set_page_config(page_title="Simulador de Compensación de Exposición", layout="wide")

# Definición de escalas EV y datos de referencia
f_stops = ['f/16', 'f/11', 'f/8', 'f/5.6', 'f/4', 'f/2.8', 'f/2', 'f/1.4', 'f/1.2']
f_ev = {'f/16': -3.0, 'f/11': -2.0, 'f/8': -1.0, 'f/5.6': 0.0, 'f/4': +1.0, 'f/2.8': +2.0, 'f/2': +3.0, 'f/1.4': +4.0, 'f/1.2': +4.5}

t_stops = ['1/4000s', '1/2000s', '1/1000s', '1/500s', '1/250s', '1/125s', '1/60s', '1/30s', '0.3"', '1"', '30"']
t_ev = {'1/4000s': -5.0, '1/2000s': -4.0, '1/1000s': -3.0, '1/500s': -2.0, '1/250s': -1.0, '1/125s': 0.0, '1/60s': +1.0, '1/30s': +2.0, '0.3"': +5.0, '1"': +7.0, '30"': +12.0}

iso_stops = ['100', '200', '400', '800', '1600', '3200', '6400']
iso_ev = {'100': -2.0, '200': -1.0, '400': 0.0, '800': +1.0, '1600': +2.0, '3200': +3.0, '6400': +4.0}

def draw_exposimeter(ev_total):
    fig, ax = plt.subplots(figsize=(10, 2.5), dpi=150)
    fig.patch.set_facecolor('#1e1e24')
    ax.set_facecolor('#1e1e24')
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    ax.text(0, 3.8, f"EXPOSÍMETRO: {ev_total:+.1f} EV", color='white', fontsize=13, fontweight='bold', ha='center')

    ax.plot([-3, 3], [2.2, 2.2], color='white', lw=2)
    for ev_mark in range(-3, 4):
        color = '#00ffcc' if ev_mark == 0 else 'white'
        ax.plot([ev_mark, ev_mark], [1.9, 2.5], color=color, lw=2 if ev_mark == 0 else 1)
        ax.text(ev_mark, 2.8, f"{ev_mark:+d}" if ev_mark != 0 else "0", color=color, fontsize=10, fontweight='bold', ha='center')

    ev_clamped = max(-3.5, min(3.5, ev_total))
    pointer = patches.Polygon([[ev_clamped, 1.8], [ev_clamped-0.2, 1.2], [ev_clamped+0.2, 1.2]], color='#00ffcc' if abs(ev_total) < 0.1 else '#ff4444')
    ax.add_patch(pointer)

    brightness_val = max(0.0, min(1.0, 0.5 + (ev_clamped / 6.0)))
    ax.add_patch(patches.Rectangle((-3, 0.2), 6, 0.7, facecolor=str(brightness_val), edgecolor='white', lw=1))
    ax.text(0, 0.55, "Luminancia Tonal Resultante", color='black' if brightness_val > 0.5 else 'white', fontsize=9, ha='center')

    return fig

# Header
st.title("📷 Simulador Interactivo de Exposición y Generador de Retos")
st.markdown("Herramienta didáctica para comprender la **compensación por pasos de luz (EV)** y resolver situaciones reales de toma.")

tab1, tab2 = st.tabs(["🎛️ Simulador Libre", "🎯 Generador de Retos Prácticos"])

# ==========================================
# TAB 1: SIMULADOR LIBRE
# ==========================================
with tab1:
    st.subheader("Configuración Manual de Parámetros")
    col1, col2, col3 = st.columns(3)

    with col1:
        f_sel = st.select_slider("Apertura (f/)", options=f_stops, value='f/5.6', key="free_f")
        st.caption("Controla entrada de luz y Profundidad de Campo")

    with col2:
        t_sel = st.select_slider("Tiempo de Exposición ('')", options=t_stops, value='1/125s', key="free_t")
        st.caption("Controla el Tiempo y el Movimiento")

    with col3:
        iso_sel = st.select_slider("Sensibilidad ISO", options=iso_stops, value='400', key="free_iso")
        st.caption("Controla Amplificación y Ruido")

    ev_total = f_ev[f_sel] + t_ev[t_sel] + iso_ev[iso_sel]

    st.pyplot(draw_exposimeter(ev_total))

    if abs(ev_total) < 0.1:
        st.success("✅ **Exposición Equilibrada (0 EV)** — Tono neutro ideal (Gris Neutro 18%).")
    elif ev_total < 0:
        st.warning(f"🌙 **Subexpuesto por {abs(ev_total):.1f} paso(s)** — Falta luz en el sensor (Sombras oscuras).")
    else:
        st.error(f"☀️ **Sobreexpuesto por {ev_total:.1f} paso(s)** — Exceso de luz en el sensor (Riesgo de luces quemadas).")

    st.markdown("---")
    st.subheader("💡 Diagnóstico Estético y Técnico")
    c_a, c_b, c_c = st.columns(3)

    with c_a:
        st.markdown("**📷 Profundidad de Campo**")
        if f_sel in ['f/1.2', 'f/1.4', 'f/2', 'f/2.8']:
            st.info("Poca profundidad de campo (Foco selectivo / Fondo desenfocado). Excelente para retratos.")
        elif f_sel in ['f/8', 'f/11']:
            st.success("Punto dulce del objetivo (Máxima nitidez óptica).")
        else:
            st.info("Gran profundidad de campo (Todo enfocado de frente a fondo). Ideal para paisajes.")

    with c_b:
        st.markdown("**🏃 Movimiento & Estabilidad**")
        if t_sel in ['1/4000s', '1/2000s', '1/1000s']:
            st.info("Tiempo congelado (Congela movimiento rápido/deportes).")
        elif t_sel == '1/60s':
            st.warning("1/60s: Límite recomendado a mano alzada.")
        elif t_sel in ['1/30s', '0.3"', '1"', '30"']:
            st.error("⚠️ Riesgo de foto movida / trepidada. Requiere trípode.")
        else:
            st.success("Velocidad estándar segura.")

    with c_c:
        st.markdown("**✨ Calidad / Ruido Digital**")
        if iso_sel in ['100', '200']:
            st.success("Máxima nitidez y pureza sin ruido digital.")
        elif iso_sel == '400':
            st.info("Sensibilidad nativa equilibrada.")
        else:
            st.warning("Presencia de ruido digital en sombras.")


# ==========================================
# TAB 2: GENERADOR DE RETOS PRÁCTICOS
# ==========================================
with tab2:
    st.subheader("🎯 Desafíos de Compensación de Exposición")
    st.markdown("Ponte a prueba resolviendo problemas reales de exposición. El objetivo es mantener o recuperar el equilibrio en **0 EV** cumpliendo los requisitos fotográficos.")

    # Base de datos de retos
    retos = [
        {
            "id": 1,
            "titulo": "Reto #1: Retrato con Foco Selectivo",
            "escenario": "Estás en la posición inicial balanceada (f/5.6, 1/125s, ISO 400 = 0 EV). Para aislar a un sujeto en un retrato, abres el diafragma a **f/2.8** (+2 EV).",
            "f_fijo": "f/2.8",
            "t_fijo": None,
            "iso_fijo": None,
            "pista": "Apertura f/2.8 te suma +2 EV de luz. Debes restar 2 EV ajustando el Tiempo o el ISO para volver a 0 EV."
        },
        {
            "id": 2,
            "titulo": "Reto #2: Congelar Acción en Deportes",
            "escenario": "Fotografías a un patinador. La velocidad estándar de 1/125s trepida la foto, por lo que aceleras a **1/1000s** (-3 EV de luz). Mantén el ISO en **400**.",
            "f_fijo": None,
            "t_fijo": "1/1000s",
            "iso_fijo": "400",
            "pista": "Subir el tiempo a 1/1000s te restó 3 pasos de luz (-3 EV). Al mantener ISO 400, debes compensar abriendo la Apertura 3 pasos."
        },
        {
            "id": 3,
            "titulo": "Reto #3: Paisaje Nítido en Trípode",
            "escenario": "Para fotografiar un paisaje con máxima nitidez, fijas la Apertura en **f/11** (-2 EV) y el ISO en **100** (-2 EV) para evitar ruido digital.",
            "f_fijo": "f/11",
            "t_fijo": None,
            "iso_fijo": "100",
            "pista": "f/11 (-2 EV) e ISO 100 (-2 EV) suman una pérdida total de -4 EV. Debes compensar ganando +4 EV con un tiempo de exposición más lento."
        },
        {
            "id": 4,
            "titulo": "Reto #4: Fotografía en Interiores con Poca Luz",
            "escenario": "En una sala oscura, no puedes usar flash. Abres el diafragma a **f/2.8** (+2 EV) y necesitas una velocidad segura a mano alzada de **1/125s** (0 EV).",
            "f_fijo": "f/2.8",
            "t_fijo": "1/125s",
            "iso_fijo": None,
            "pista": "f/2.8 te da +2 EV de luz. Para equilibrar el medidor exactamente en 0 EV con tiempo de 1/125s, selecciona el ISO equivalente."
        }
    ]

    # Inicializar estado de sesión
    if 'reto_index' not in st.session_state:
        st.session_state.reto_index = 0
    if 'puntos' not in st.session_state:
        st.session_state.puntos = 0

    col_btn1, col_btn2, col_score = st.columns([2, 2, 2])
    with col_btn1:
        if st.button("🎲 Cambiar Reto Aleatorio"):
            st.session_state.reto_index = random.randint(0, len(retos) - 1)
    with col_score:
        st.metric("Puntuación / Retos Logrados", f"{st.session_state.puntos} pts")

    reto_actual = retos[st.session_state.reto_index]

    st.info(f"### {reto_actual['titulo']}\n\n{reto_actual['escenario']}")
    st.caption(f"💡 **Pista:** {reto_actual['pista']}")

    st.markdown("#### Ajusta tus parámetros para resolver el reto:")
    col_r1, col_r2, col_r3 = st.columns(3)

    with col_r1:
        if reto_actual['f_fijo']:
            f_reto = st.text_input("Apertura (Fija)", value=reto_actual['f_fijo'], disabled=True)
        else:
            f_reto = st.selectbox("Apertura (f/)", options=f_stops, index=3)

    with col_r2:
        if reto_actual['t_fijo']:
            t_reto = st.text_input("Tiempo (Fijo)", value=reto_actual['t_fijo'], disabled=True)
        else:
            t_reto = st.selectbox("Tiempo (s)", options=t_stops, index=5)

    with col_r3:
        if reto_actual['iso_fijo']:
            iso_reto = st.text_input("ISO (Fijo)", value=reto_actual['iso_fijo'], disabled=True)
        else:
            iso_reto = st.selectbox("ISO", options=iso_stops, index=2)

    ev_reto_total = f_ev[f_reto] + t_ev[t_reto] + iso_ev[str(iso_reto)]

    st.pyplot(draw_exposimeter(ev_reto_total))

    if st.button("✔️ Verificar Solución"):
        if abs(ev_reto_total) < 0.1:
            st.balloons()
            st.success("🎉 ¡CORRECTO! Has logrado equilibrar perfectamente la exposición (0 EV) cumpliendo todas las condiciones del reto.")
            st.session_state.puntos += 10
        elif ev_reto_total < 0:
            st.error(f"❌ La imagen sigue subexpuesta por {abs(ev_reto_total):.1f} EV. Ajusta los parámetros para permitir mayor entrada de luz.")
        else:
            st.error(f"❌ La imagen quedó sobreexpuesta por {ev_reto_total:.1f} EV. Ajusta los parámetros para reducir la entrada de luz.")
