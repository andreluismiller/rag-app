"""Pagina principal: interface de chat para interagir com o RAG."""

import uuid

import streamlit as st

from app.utils.db import save_feedback, save_interaction
from src.rag.pipeline import answer_question

st.set_page_config(page_title="RAG Chat", page_icon=":speech_balloon:", layout="wide")
st.title("Assistente RAG")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Digite sua pergunta...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Buscando resposta..."):
            result = answer_question(question)
            result["session_id"] = st.session_state.session_id
            interaction_id = save_interaction(result)

        st.markdown(result["answer"])

        with st.expander("Fontes utilizadas"):
            for chunk in result["retrieved_chunks"]:
                st.markdown(f"- (score {chunk['score']:.3f}) {chunk['text'][:200]}...")

        col1, col2 = st.columns(2)
        if col1.button("👍 Util", key=f"up-{interaction_id}"):
            save_feedback(interaction_id, rating=1)
            st.toast("Obrigado pelo feedback!")
        if col2.button("👎 Nao util", key=f"down-{interaction_id}"):
            save_feedback(interaction_id, rating=-1)
            st.toast("Obrigado pelo feedback!")

    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
