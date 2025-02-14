import streamlit as st
from vector_store import FlowerShopVectorStore
from chatbot import app
from langchain_core.messages import AIMessage, HumanMessage
from tools import customers_database, data_protection_checks

st.set_page_config(page_title="CoachRunner", page_icon="🏃", layout="wide")

if "message_history" not in st.session_state:
    st.session_state.message_history = [AIMessage(content="Hi, I'm CoachRunner! How can I help you today?")]
    
left_col, main_col, right_col = st.columns([1, 2, 1])

with left_col:
    if st.button("Clear chat"):
        st.session_state.message_history = [AIMessage(content="Hi, I'm CoachRunner! How can I help you today?")]


with main_col:
    user_input = st.chat_input("Type here...")
    
    if user_input:
        st.session_state.message_history.append(HumanMessage(content=user_input))
        
        response = app.invoke({
            'messages': st.session_state.message_history
        })
        
        st.session_state.message_history = response['messages']
        
    for message in reversed(st.session_state.message_history):
        if isinstance(message, AIMessage):
            message_box = st.chat_message('assistant')
        else:
            message_box = st.chat_message('user')
            
        message_box.markdown(message.content)
        
with right_col:
    st.title('customers database')
    st.write(customers_database)
    st.title('data protection checks')
    st.write(data_protection_checks)