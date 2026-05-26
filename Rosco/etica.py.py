import streamlit as st

# 1. Configuración de la base de preguntas con OPCIONES MÚLTIPLES
ROSCO_DATA = [
    {
        "letra": "B",
        "definicion": "Fin social o beneficio particular que cada profesión debe aportar a la comunidad (ej. curar en la medicina).",
        "opciones": ["Bien interno", "Bien externo", "Beneficio económico", "Burocracia profesional"],
        "respuesta": "Bien interno"
    },
    {
        "letra": "C",
        "definicion": "Fenómeno que ocurre cuando un profesional antepone el dinero, poder o estatus por encima de su verdadera función social.",
        "opciones": ["Competitividad", "Corrupción", "Cooperación", "Corporativismo"],
        "respuesta": "Corrupción"
    },
    {
        "letra": "E",
        "definicion": "Estándar que debe buscar un buen profesional, caracterizado por competir consigo mismo para dar el mejor servicio.",
        "opciones": ["Egoísmo", "Eficiencia pura", "Excelencia", "Estatus"],
        "respuesta": "Excelencia"
    },
    {
        "letra": "M",
        "definicion": "Actitud criticada por Adela Cortina que daña el tejido social y defrauda la confianza al hacer las cosas a medias.",
        "opciones": ["Mediocridad", "Meritocracia", "Motivación", "Modernización"],
        "respuesta": "Mediocridad"
    },
    {
        "letra": "O",
        "definicion": "Estructura o entidad colectiva (empresa, hospital) que necesita construir un 'clima ético' interno.",
        "opciones": ["Oposición", "Organización", "Oligarquía", "Opinión pública"],
        "respuesta": "Organización"
    },
    {
        "letra": "P",
        "definicion": "Actividad social cooperativa que busca brindar un bien específico a la comunidad además del sustento económico.",
        "opciones": ["Pasatiempo", "Productividad", "Profesión", "Privatización"],
        "respuesta": "Profesión"
    },
    {
        "letra": "R",
        "definicion": "Cualidad de prestigio y crédito que ganan las empresas que actúan éticamente a largo plazo.",
        "opciones": ["Rentabilidad financiera", "Reputación", "Regulación estatal", "Rivalidad"],
        "respuesta": "Reputación"
    },
    {
        "letra": "V",
        "definicion": "Principios morales (como la justicia o la honestidad) que son pilares indispensables para la ética profesional.",
        "opciones": ["Variables de mercado", "Valores", "Vicios", "Vanguardias"],
        "respuesta": "Valores"
    }
]

# 2. Inicialización del Estado de la Sesión (Session State)
if "nombre_jugador" not in st.session_state:
    st.session_state.nombre_jugador = ""
if "juego_iniciado" not in st.session_state:
    st.session_state.juego_iniciado = False
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "historial" not in st.session_state:
    st.session_state.historial = []

# Interfaz de Usuario (UI)
st.title("🎓 El Rosco de la Ética Profesional")
st.caption("Basado en las tesis de la filósofa Adela Cortina")
st.write("---")

# PANTALLA 1: Registro de Nombre
if not st.session_state.juego_iniciado:
    st.write("### 👤 Registro del participante")
    nombre = st.text_input("Introduce tu nombre o el de tu equipo:", placeholder="Ej. Equipo Alfa / Juan Pérez")
    
    if st.button("Comenzar Juego 🚀"):
        if nombre.strip():
            st.session_state.nombre_jugador = nombre.strip()
            st.session_state.juego_iniciado = True
            st.rerun()
        else:
            st.warning("Por favor, escribe un nombre para poder empezar.")

# PANTALLA 2: El Juego en marcha
elif not st.session_state.game_over:
    # Verificar si ya llegamos al final de las preguntas
    if st.session_state.current_index >= len(ROSCO_DATA):
        st.session_state.game_over = True
        st.rerun()
        
    pregunta_actual = ROSCO_DATA[st.session_state.current_index]
    
    # Mostrar datos del jugador actual
    st.sidebar.markdown(f"### 🎮 Jugando: **{st.session_state.nombre_jugador}**")
    st.sidebar.metric(label="Aciertos actuales", value=f"{st.session_state.score}")
    
    # Progreso visual
    progreso = " | ".join([f"**{p['letra']}**" for p in ROSCO_DATA])
    st.markdown(f"**Letras del juego:** {progreso}")
    
    st.info(f"### Con la letra **{pregunta_actual['letra']}**")
    st.markdown(f"**Definición:** {pregunta_actual['definicion']}")
    
    # Formulario con Opciones Múltiples (Radio Buttons)
    with st.form(key="formulario_opciones", clear_on_submit=True):
        # Seleccionar opción
        seleccion = st.radio("Selecciona la respuesta correcta:", pregunta_actual["opciones"], index=0)
        
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button(label="Comprobar Respuesta 🔘")
        with col2:
            pasapalabra_button = st.form_submit_button(label="Pasapalabra ⏭️")
            
    if submit_button:
        if seleccion == pregunta_actual["respuesta"]:
            st.session_state.score += 1
            st.session_state.historial.append(f"🟢 Letra {pregunta_actual['letra']}: ¡Correcto! ({seleccion})")
        else:
            st.session_state.historial.append(f"🔴 Letra {pregunta_actual['letra']}: Incorrecto (Elegiste: {seleccion} | Era: {pregunta_actual['respuesta']})")
            
        st.session_state.current_index += 1
        st.rerun()
        
    if pasapalabra_button:
        st.session_state.historial.append(f"🟡 Letra {pregunta_actual['letra']}: Pasapalabra")
        st.session_state.current_index += 1
        st.rerun()

# PANTALLA 3: Resultados finales
else:
    st.balloons()
    st.success(f"### 🎉 ¡Fin del juego para {st.session_state.nombre_jugador}!")
    st.metric(label="Puntuación Final", value=f"{st.session_state.score} / {len(ROSCO_DATA)}")
    
    st.write("#### Resumen de la partida:")
    for h in st.session_state.historial:
        st.write(h)
        
    # Botón para reiniciar por completo (Permite cambiar de jugador)
    if st.button("Registrar nuevo jugador / Reiniciar 🔄"):
        st.session_state.juego_iniciado = False
        st.session_state.nombre_jugador = ""
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.historial = []
        st.rerun()
