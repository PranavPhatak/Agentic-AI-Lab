from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
load_dotenv()
import streamlit as st

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "memory" not in st.session_state:
    st.session_state.memory = InMemorySaver()

memory = st.session_state.memory

model = ChatNVIDIA(model="nvidia/nemotron-3.5-lightning-30b-a3b")
search = TavilySearch(max_results=5)

agent = create_agent(
    model = model,
    tools = [search],
    checkpointer = memory,
    system_prompt = (
        """
You are a helpful AI search agent.

    When answering a question:
    1. Use the search tool when current or web-based information is needed.
    2. Carefully analyze the search results before answering.
    3. Answer the user's exact question directly.
    4. Do not add unrelated information.
    5. If multiple sources disagree, mention the disagreement.
    6. Do not claim information that is not supported by the search results.
    7. Give a concise and easy-to-understand answer.
    """
    )
)

st.title("🔎 Google Search Agent")
st.markdown("Ask questions and I will search the web to find the answer.")

query = st.chat_input("Ask me anything...")


for message in st.session_state.chat_history:
    role = message["role"]
    content = message['content']
    st.chat_message(role).markdown(content)

if query:
    st.session_state.chat_history.append({"role":"user", "content":query})
    st.chat_message("user").markdown(query)

    with st.chat_message("ai"):
        response = agent.invoke({
            "messages": [{
                "role":"user",
                "content":query
            }]},
            {"configurable": {"thread_id": "search_agent_thread"}}
        )
        answer = response["messages"][-1].content
        st.markdown(answer)

    st.session_state.chat_history.append({"role":"ai", "content": answer})