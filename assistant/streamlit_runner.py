import streamlit as st
from chatbot import MFAPIChain
from config import Config
from langchain_openai import OpenAI
import time
history_token_length = 2000
grade_level = 4
if 'llm' not in st.session_state:
    st.session_state['llm'] = OpenAI( openai_api_key="REMOVED")
if 'chatbot' not in st.session_state:
    st.session_state['chatbot'] = MFAPIChain("REMOVED", st.session_state['llm'], grade_level, history_token_length, Config())
st.title("Babylon Micro Farms Chatbot + API Tool")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
with st.sidebar:
    category = st.radio(
        "Mode you want the chatbot to be in",
        ["API", "General"]
    )
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = st.session_state['chatbot'].invoke({'content' : prompt, "category" : category})
    st.session_state.messages.append({"role": "assistant", "content":  response['output']})
    st.chat_message("assistant").write(response['output'])