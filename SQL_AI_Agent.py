from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
import streamlit as st
from dotenv import load_dotenv
load_dotenv()


db = SQLDatabase.from_uri("sqlite:///my_tasks.db")
db.run("""
    CREATE TABLE IF NOT EXISTS tasks (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        Description TEXT,
        Status TEXT Check (Status IN ("pending", "in_progress", "completed")) DEFAULT "pending",
        Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

""")

model = ChatGroq(model="openai/gpt-oss-20b")
toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()

system_prompt = """
system_prompt = #""
You are a task management assistant that interacts with a SQL database containing a 'task' table

TASK RULES:
1. Limit SELECT queries to 10 results max with ORDER BY created_at DESC
2. After CREATE/UPDATE/DELETE, confirm with SELECT query
3. If the user requests a list of tasks, present the output in a structured table format to ensure a clean and organized display in the browser.
4. NEVER show SQL queries to the user.
5. NEVER explain the SQL query you executed.
6. Only provide the final answer in natural language.
7. For database operations, execute the required SQL using the available tools, but keep all SQL and tool execution details hidden from the user.

CRUD OPERATIONS:
CREATE: INSERT INTO tasks(title, description, status)
READ: SELECT * FROM tasks WHERE ... LIMIT 10
UPDATE: UPDATE tasks SET status =? WHERE id =? OR title =?
DELETE: DELETE FROM tasks WHERE id =? OR title =?

Table schema: id, title, description, status(pending/progress/completed), created_at.
"""
st.title("TaskBot - Manage your todos")
st.markdown("SQL bot is the AI agent that manages you tasks")

@st.cache_resource # this will prevent the function get refreshed everytime when the streamlit refreshs
def get_agent():
    agent = create_agent(
        model=model,
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt=system_prompt
    )
    return agent

agent = get_agent()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)


query = st.chat_input("Ask me anything about task")

if query:
    st.session_state.chat_history.append({"role":"user", "content":query})
    st.chat_message("user").markdown(query)

    with st.chat_message("ai"):
        with st.spinner("Processing your query..."):
            response = agent.invoke({
                "messages" : [
                    {
                        "role":"user",
                        "content":query
                    }
                ]
            },
            {"configurable": {"thread_id": "sql_agent"}}
            )
        message = response["messages"][-1].content
        st.markdown(message)
        st.session_state.chat_history.append({"role":"ai", "content":message})
            

