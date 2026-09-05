from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

model = ChatGroq(model="openai/gpt-oss-120b")

st.title("AskBuddy - Your Personal AI Assistant")
st.markdown("AskBuddy is a chatbot that can answer your questions and help you with your tasks. It is powered by the Groq AI model.")

query = st.chat_input("Ask me anything!")

if "messages_history" not in st.session_state:
    st.session_state.messages_history = []

for message in st.session_state.messages_history:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

if query:
    st.session_state.messages_history.append({"role":"user", "content":query})
    st.chat_message("user").markdown(query)

    with st.chat_message("ai"):
        response = st.write_stream(
            chunk.content for chunk in model.stream(st.session_state.messages_history)
        )

    st.session_state.messages_history.append({"role":"ai", "content":response})
    