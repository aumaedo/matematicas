import streamlit as st
import random
import time

def generar_operacion(tipo):
    if tipo == 'suma':
        a, b = random.randint(1, 50), random.randint(1, 50)
        return f"{a} + {b}", a + b
    elif tipo == 'resta':
        a, b = random.randint(1, 50), random.randint(1, 50)
        a, b = max(a, b), min(a, b)
        return f"{a} - {b}", a - b
    elif tipo == 'multiplicación':
        a, b = random.randint(1, 10), random.randint(1, 10)
        return f"{a} × {b}", a * b
    elif tipo == 'división':
        b = random.randint(1, 10)
        res = random.randint(1, 10)
        a = b * res
        return f"{a} ÷ {b}", res
    else:
        return None, None

st.set_page_config(page_title="Cálculo Mental para Niños", layout="centered")
st.title("🧠 Cálculo Mental para Niños")

st.sidebar.header("⚙️ Configuración")
tiempo_max = st.sidebar.slider("⏱ Tiempo máximo por operación (segundos)", 2, 30, 10)

tipos_operaciones = ['suma', 'resta', 'multiplicación', 'división']
operaciones_config = {}
total_preguntas = 0

for tipo in tipos_operaciones:
    cantidad = st.sidebar.number_input(f"¿Cuántas de {tipo}?", min_value=0, max_value=20, value=2)
    operaciones_config[tipo] = cantidad
    total_preguntas += cantidad

if "estado" not in st.session_state:
    st.session_state.estado = "inicio"
    st.session_state.preguntas = []
    st.session_state.indice = 0
    st.session_state.resultados = []
    st.session_state.tiempo_inicio = 0

if st.session_state.estado == "inicio":
    if st.button("🎮 ¡Comenzar!"):
        preguntas = []
        for tipo, cantidad in operaciones_config.items():
            for _ in range(cantidad):
                op, res = generar_operacion(tipo)
                preguntas.append((op, res))
        random.shuffle(preguntas)
        st.session_state.preguntas = preguntas
        st.session_state.indice = 0
        st.session_state.resultados = []
        st.session_state.estado = "jugando"
        st.rerun()

elif st.session_state.estado == "jugando":
    indice = st.session_state.indice
    if indice < len(st.session_state.preguntas):
        pregunta, resultado_correcto = st.session_state.preguntas[indice]

        if "respuesta_usuario" not in st.session_state:
            st.session_state.respuesta_usuario = ""

        st.subheader(f"Pregunta {indice + 1} de {len(st.session_state.preguntas)}")
        st.markdown(f"⏳ Tienes **{tiempo_max} segundos** para responder.")

        if "tiempo_inicio" not in st.session_state or st.session_state.tiempo_inicio == 0:
            st.session_state.tiempo_inicio = time.time()

        respuesta = st.text_input(f"✏️ ¿Cuánto es {pregunta}?", key=f"pregunta_{indice}")
        tiempo_transcurrido = time.time() - st.session_state.tiempo_inicio

        if st.button("Enviar"):
            try:
                correcta = (int(respuesta) == resultado_correcto) and (tiempo_transcurrido <= tiempo_max)
            except:
                correcta = False

            st.session_state.resultados.append({
                'pregunta': pregunta,
                'respuesta_usuario': respuesta,
                'respuesta_correcta': resultado_correcto,
                'tiempo': round(tiempo_transcurrido, 2),
                'correcta': correcta
            })

            st.session_state.indice += 1
            st.session_state.tiempo_inicio = 0
            st.rerun()
    else:
        st.session_state.estado = "fin"
        st.experimental_rerun()

elif st.session_state.estado == "fin":
    st.success("✅ ¡Has terminado la serie!")
    aciertos = sum(1 for r in st.session_state.resultados if r['correcta'])
    total = len(st.session_state.resultados)
    st.metric("Aciertos", f"{aciertos} de {total}")

    with st.expander("📋 Ver detalle"):
        for r in st.session_state.resultados:
            st.write(f"🔹 {r['pregunta']} = {r['respuesta_correcta']} | "
                     f"Tú: {r['respuesta_usuario']} | "
                     f"⏱ {r['tiempo']}s | "
                     f"{'✅' if r['correcta'] else '❌'}")

    if st.button("🔁 Volver a empezar"):
        st.session_state.estado = "inicio"
        st.session_state.preguntas = []
        st.session_state.resultados = []
        st.session_state.indice = 0
        st.session_state.tiempo_inicio = 0
        st.experimental_rerun()
