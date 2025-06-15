import streamlit as st
import io
import google.generativeai as genai
from PIL import Image
import requests
import datetime
import os
from pymongo import MongoClient
import requests





st.header('Agente Impressora 3d')
st.header(' ')




gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)
modelo_vision = genai.GenerativeModel("gemini-2.0-flash", generation_config={"temperature": 0.1})
modelo_texto = genai.GenerativeModel("gemini-1.5-flash")

# Conexão com MongoDB
client2 = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/auto_doc?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&tlsAllowInvalidCertificates=true")
db = client2['arquivos_planejamento']
collection = db['auto_doc']
banco = client2["arquivos_planejamento"]
db_clientes = banco["clientes"]  
db_briefings = banco["briefings_coca"]  


# Carrega diretrizes
with open('data.txt', 'r') as file:
    conteudo = file.read()

tab_chatbot = st.tabs([
    "💬 Chatbot Agente Coca Cola", 
])


with tab_chatbot:  
    st.header("Chat Impressora 3d")
    
    # Inicializa o histórico de chat na session_state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Exibe o histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Como posso ajudar?"):
        # Adiciona a mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Prepara o contexto com as diretrizes
        contexto = f"""
        Você é um assistente virtual especializado no uso da impressora 3d CREALITY Ender-3 V3 SE 3D Printer. Você está aqui
        para auxiliar os alunos da Cyrus a fazerem uso dela.
        ####CONTEXTO####
        {conteudo}
        ####END CONTEXTO####


        
        Regras importantes:
        - Seja preciso e técnico
        - Mantenha o tom profissional mas amigável
        - Se a pergunta for irrelevante, oriente educadamente
        - Forneça exemplos quando útil
        """
        
        # Gera a resposta do modelo
        with st.chat_message("assistant"):
            with st.spinner('Pensando...'):
                try:
                    # Usa o histórico completo para contexto
                    historico_formatado = "\n".join(
                        [f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages]
                    )
                    
                    resposta = modelo_texto.generate_content(
                        f"{contexto}\n\nHistórico da conversa:\n{historico_formatado}\n\nResposta:"
                    )
                    
                    # Exibe a resposta
                    st.markdown(resposta.text)
                    
                    # Adiciona ao histórico
                    st.session_state.messages.append({"role": "assistant", "content": resposta.text})
                    
                except Exception as e:
                    st.error(f"Erro ao gerar resposta: {str(e)}")



