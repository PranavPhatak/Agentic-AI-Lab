from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import streamlit as st

model = ChatGroq(model="openai/gpt-oss-120b")

st.title("AskBuddy - Your AI Assistant")

st.markdown("Welcome to AskBuddy! This is your personal AI assistant. You can ask me anything, and I'll do my best to help you.")
query = st.chat_input("Ask anything you want to know!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = message['role']
    content = message['content']
    st.chat_message(role).markdown(content)

if query:
    st.session_state.messages.append({"role":"user", "content":query})
    st.chat_message("User").markdown(query)
    response = model.invoke(query)
    st.session_state.messages.append({"role":"AskBuddy", "content":response.content})
    st.chat_message("AskBuddy").markdown(response.content)