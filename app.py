import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mi superchat de IA", page_icon="🤖", layout="centered")
st.title("Primeros pasos en mi aplicación con Streamlit")

nombre = st.text_input("¿Cómo te llamás?")
if st.button("Saludar"):
    st.write(f"Hola, {nombre}! Bienvenido a mi primer aplicación de IA.")

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configuracion_pagina():
    st.title("Mi Chatbot de IA")
    st.sidebar.title("Configuración de la IA")
    MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b']
    elegirModelo = st.sidebar.selectbox("Elegí un modelo de IA para generar tus respuestas", options=MODELOS, index=0)
    return elegirModelo

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def obtener_respuesta(cliente, modelo, mensajeDeEntrada):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True
    )
    texto = ""
    for chunk in respuesta:
        if chunk.choices[0].delta.content:
            texto += chunk.choices[0].delta.content
    return texto

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

clienteUsuario = crear_usuario_groq()
inicializar_estado()
modelo = configuracion_pagina()

mostrar_historial()  

mensaje = st.chat_input("Escribí tu prompt:")

if mensaje:
    actualizar_historial("usuario", mensaje, avatar="👤")

    respuesta_texto = obtener_respuesta(clienteUsuario, modelo, mensaje)

    with st.chat_message("Bot", avatar="🤖"):
        st.markdown(respuesta_texto)

    actualizar_historial("Bot", respuesta_texto, avatar="🤖")
