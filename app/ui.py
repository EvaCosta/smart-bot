import streamlit as st
from chatbot import Chatbot

def run_ui():
    st.title("ChatLearn - Chatbot Adaptativo")
    st.write("Interaja com o chatbot e veja como ele aprende ao longo do tempo.")

    chatbot = Chatbot()

    user_input = st.text_input("Digite sua mensagem:")
    if st.button("Enviar"):
        response = chatbot.respond(user_input)
        st.write("Chatbot:", response)

if __name__ == "__main__":
    run_ui()
