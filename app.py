from query.create_response import CreatResponse
from database.db_connection import DatabaseConnection
import streamlit as st
from streamlit import session_state as ss
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
import time

# # Import your necessary classes (DatabaseConnection, CreatResponse, etc.)
load_dotenv()

# Load configuration for the page
st.set_page_config(page_title="AskDB - SQL Chatbot (●'◡'●)", page_icon=":robot_face:", layout="wide")

# Custom CSS to make human messages appear on the right
st.markdown("""
<style>
    .chat-message-human {
        background-color: #F3F4F6;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        color: #000000;
        margin-left: auto;
    }
    .chat-message-ai {
        background-color: #F3F4F6; 
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 10px;
        font-family: 'Cairo', sans-serif;
        color: #000000;
    }
    .bady {
        font-family: 'Cairo', sans-serif;
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)
# Header and App Title
st.title("🤖 AskDB")
st.markdown("Ask me anything about your database! I will help you craft SQL queries and provide natural language responses.")
with st.sidebar:
    st.subheader("🔌 Connect to Database")
    st.write("Please fill in the necessary details to connect to your database.")

    db_type = st.selectbox("Database Type", ["postgresql", "mysql", "sqlite"], index=0)
    db_host = st.text_input("Host", value="localhost")
    db_port = st.number_input("Port", value=5432)
    db_user = st.text_input("User", value="postgres")
    db_password = st.text_input("Password", type="password", value="2002")
    db_name = st.text_input("Database", value="ecommerce")

    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            try:
                conn = DatabaseConnection(
                    db_user,
                    db_name,
                    db_password,
                    db_host,
                    db_port,
                    db_type,
                )
                conn.create_engine_connection()
                ss.db = conn  # ✅ Store the connection
                ss.db_connected = True  # ✅ Flag for successful connection
                st.success(f"Connected to `{db_name}` database successfully!")
            except Exception as e:
                ss.db_connected = False
                st.error(f"Failed to connect: {e}")


if "chat_history" not in ss:
    ss.chat_history = [
        AIMessage(content="Hello! I'm AskDB. Ask me anything about your database."),
    ]
if "db_connected" not in ss:
    ss.db_connected = False

st.markdown("### 💬 Chat")
for message in ss.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI", avatar="pics/download.png"):
            st.markdown(f'<div class="chat-message-ai">{message.content}</div>', unsafe_allow_html=True)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human", avatar="pics/user_avatar.png"):
            st.markdown(f'<div class="chat-message-human">{message.content}</div>', unsafe_allow_html=True)

# Chat input
user_query = st.chat_input("Type a message...")


if user_query:
    if not ss.db_connected:
        st.warning("Please connect to the database first using the sidebar.")
    else:
        ss.chat_history.append(HumanMessage(content=user_query))
        with st.chat_message("Human", avatar="pics/user_avatar.png"):
            st.markdown(f'<div class="chat-message-human">{user_query}</div>', unsafe_allow_html=True)

        with st.chat_message("AI", avatar="pics/download.png"):
            with st.spinner("Thinking...", show_time=True):
                accss = CreatResponse(ss.db)
                response = accss.get_response(user_query, ss.chat_history)

            response_container = st.empty()
            partial_response = ""
            for char in response:
                partial_response += char
                response_container.markdown(
                    f'<div class="chat-message-ai">{partial_response}</div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.005)

        ss.chat_history.append(AIMessage(content=response))
    

    



