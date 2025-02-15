import streamlit as st
from vector_store import RunnerShopVectorStore
from chatbot import app
from langchain_core.messages import AIMessage, HumanMessage
from tools import customers_database, data_protection_checks

# Page configuration
st.set_page_config(
    page_title="CoachRunner",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Chat container */
    .stChatMessage {
        background-color: black;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* User message styling */
    .user-message {
        background-color: #007bff;
        color: white;
    }
    
    /* Bot message styling */
    .assistant-message {
        background-color: #f8f9fa;
    }
    
    /* Custom button styling */
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 25px;
        padding: 10px 25px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #0056b3;
        transform: translateY(-2px);
    }
    
    /* Chat input styling */
    .stTextInput>div>div>input {
        border-radius: 25px;
        border: 2px solid #007bff;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "message_history" not in st.session_state:
    st.session_state.message_history = [AIMessage(content="👋 Hi, I'm CoachRunner! How can I help you today?")]

# Sidebar with features
with st.sidebar:
    st.title("🏃 CoachRunner")
    st.markdown("---")
    
    # Add helpful features in sidebar
    st.subheader("Quick Actions")
    if st.button("🔄 Clear Chat"):
        st.session_state.message_history = [AIMessage(content="👋 Hi, I'm CoachRunner! How can I help you today?")]
    
    st.markdown("---")
    st.subheader("Tips")
    st.markdown("""
        - 💡 Ask about running techniques
        - 📊 Get training statistics
        - 🎯 Set personal goals
        - 📅 Schedule training sessions
    """)

# Main chat interface
main_container = st.container()
with main_container:
    # Chat input
    user_input = st.chat_input("💭 Ask me anything about running...", key="chat_input")
    
    if user_input:
        st.session_state.message_history.append(HumanMessage(content=user_input))
        
        with st.spinner('Thinking...'):
            response = app.invoke({
                'messages': st.session_state.message_history
            })
                
        st.session_state.message_history = response['messages']
        
    # Chat messages display
    for message in reversed(st.session_state.message_history):
        if isinstance(message, AIMessage):
            message_box = st.chat_message('assistant', avatar="🏃")
        else:
            message_box = st.chat_message('user', avatar="👤")
        
        message_box.markdown(message.content)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Made with ❤️ by CoachRunner Team | Need help? Contact support
    </div>
    """, 
    unsafe_allow_html=True
)
