import streamlit as st

st.set_page_config(page_title="CoachRunner", page_icon="🏃", layout="wide")

if "message_history" not in st.session_state:
    st.session_state.message_history = [{"content": "Hi, I'm CoachRunner! How can I help you today?", "type": "assistant"}]
    
left_col, main_col, right_col = st.columns([1, 2, 1])

with left_col:
    if st.button("Clear chat"):
        st.session_state.message_history = [{"content": "Hi, I'm CoachRunner! How can I help you today?", "type": "assistant"}]


with main_col:
    user_input = st.chat_input("Type here...")
    
    if user_input:
        st.session_state.message_history.append({"content": user_input, "type": "user"})
        
    for message in reversed(st.session_state.message_history):
        message_box = st.chat_message(message["type"])
        message_box.markdown(message["content"])

        
with right_col:
    st.text(st.session_state.message_history)