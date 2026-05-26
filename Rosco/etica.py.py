import streamlit as st

# 1. Configuración de la base de preguntas (El Rosco)
# Puedes cambiar o añadir más letras según tu tarea.
ROSCO_DATA = [
    {
        "letra": "B",
        "definicion": "Fin social o beneficio particular que cada profesión debe aportar a la comunidad (ej. curar en la medicina).",
        "respuesta": "bien interno"
    },
    {
        "letra": "C",
        "definicion": "Fenómeno que ocurre cuando un profesional antepone el dinero, poder o estatus por encima de su verdadera función social.",
        "respuesta": "corrupcion"
    },
    {
        "letra": "E",
        "definicion": "Estándar que debe buscar un buen profesional, caracterizado por competir consigo mismo para dar el mejor servicio.",
        "respuesta": "excelencia"
    },
    {
        "letra": "M",
        "definicion": "Actitud criticada por Adela Cortina que daña el tejido social y defrauda la confianza al hacer las cosas a medias.",
        "respuesta": "mediocridad"
    },
    {
        "letra": "O",
        "definicion": "Estructura o entidad colectiva (empresa, hospital) que necesita construir un 'clima ético' interno.",
        "respuesta": "organizacion"
    },
    {
        "letra": "P",
        "definicion": "Actividad social cooperativa que busca brindar un bien específico a la comunidad además del sustento económico.",
        "respuesta": "profesion"
    },
    {
        "letra": "R",
        "definicion": "Cualidad de prestigio y crédito que ganan las empresas que actúan éticamente a largo plazo.",
        "respuesta": "reputacion"
    },
    {
        "letra": "V",
        "definicion": "Principios morales (como la justicia o la honestidad) que son pilares indispensables para la ética profesional.",
        "respuesta": "valores"
    }
]

# 2. Inicialización del Estado de la Sesión (Session State)
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "historial" not in st.session_state:
    st.session_state.historial = [] # Para guardar si acertó o falló cada letra

# 3. Interfaz de Usuario (UI)
st.title("🎓 El Rosco de la Ética Profesional")
st.caption("Basado en las tesis de la filósofa Adela Cortina")
st.write("---")

# Función para normalizar texto (eliminar acentos y mayúsculas para evitar errores tipográficos)
def normalizar(texto):
    import unicodedata
    texto = texto.lower().strip()
    # Elimina acentos de forma simple
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

# Verificar si el juego terminó
if st.session_state.current_index >= len(ROSCO_DATA):
    st.session_state.game_over = True

if not st.session_state.game_over:
    # Obtener la pregunta actual
    pregunta_actual = ROSCO_DATA[st.session_state.current_index]
    
    # Mostrar el progreso del juego de forma visual
    progreso = " | ".join([f"**{p['letra']}**" for p in ROSCO_DATA])
    st.markdown(f"**Letras del juego:** {progreso}")
    
    st.info(f"### Con la letra **{pregunta_actual['letra']}**")
    st.write(pregunta_actual['definicion'])
    
    # Formulario para capturar la respuesta y controlar el flujo con Enter o botón
    with st.form(key="formulario_respuesta", clear_on_submit=True):
        user_input = st.text_input("Tu respuesta:", placeholder="Escribe aquí tu respuesta...")
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button(label="Comprobar")
        with col2:
            pasapalabra_button = st.form_submit_button(label="Pasapalabra / Saltar")
            
    if submit_button:
        if user_input:
            resp_usuario = normalizar(user_input)
            resp_correcta = normalizar(pregunta_actual['respuesta'])
            
            if resp_usuario == resp_correcta:
                st.session_state.score += 1
                st.session_state.historial.append(f"🟢 Letra {pregunta_actual['letra']}: ¡Correcto!")
                st.success("¡Excelente! Respuesta correcta.")
            else:
                st.session_state.historial.append(f"🔴 Letra {pregunta_actual['letra']}: Incorrecto (Era: {pregunta_actual['respuesta']})")
                st.error(f"¡Oops! La respuesta correcta era: **{pregunta_actual['respuesta']}**")
                
            # Avanzar a la siguiente letra
            st.session_state.current_index += 1
            st.rerun()
        else:
            st.warning("Por favor, escribe algo antes de comprobar.")
            
    if pasapalabra_button:
        # En esta versión básica lo salta al final, puedes acumularlo si quieres complicarlo
        st.session_state.historial.append(f"🟡 Letra {pregunta_actual['letra']}: Pasapalabra")
        st.session_state.current_index += 1
        st.rerun()

else:
    # Pantalla Final de Resultados
    st.balloons()
    st.success("### 🎉 ¡Has terminado el Rosco Ético!")
    st.metric(label="Puntuación Final", value=f"{st.session_state.score} / {len(ROSCO_DATA)}")
    
    st.write("#### Resumen de tu partida:")
    for h in st.session_state.historial:
        st.write(h)
        
    # Botón para reiniciar el juego
    if st.button("Jugar de nuevo"):
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.historial = []
        st.rerun()