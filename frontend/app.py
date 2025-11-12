"""
Streamlit Chat Interface
Simple and clean UI for the LangGraph chatbot.
"""

import streamlit as st
import requests
from typing import List, Tuple
import time

# Page configuration
st.set_page_config(
    page_title="LangGraph AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)

# Constants
API_URL = "http://127.0.0.1:8000/chat"
SESSION_ID = "demo"

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🤖 LangGraph AI Chatbot")
st.markdown("*Powered by LangGraph, FastAPI, and OpenAI*")
st.divider()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "session_id" not in st.session_state:
    st.session_state["session_id"] = SESSION_ID


def send_message(user_input: str, session_id: str) -> str:
    """
    Send message to the backend API and get response.
    
    Args:
        user_input: User's message
        session_id: Session identifier
        
    Returns:
        Bot's reply
    """
    try:
        response = requests.post(
            API_URL,
            json={"user_input": user_input, "session_id": session_id},
            timeout=30
        )
        response.raise_for_status()
        return response.json()["reply"]
    except requests.exceptions.ConnectionError:
        return "❌ Error: Cannot connect to backend server. Please make sure the FastAPI server is running on http://127.0.0.1:8000"
    except requests.exceptions.Timeout:
        return "❌ Error: Request timed out. Please try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def clear_chat():
    """Clear the chat history."""
    st.session_state["chat_history"] = []
    st.rerun()


# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Session info
    st.subheader("Session Info")
    st.text(f"Session ID: {st.session_state['session_id']}")
    st.text(f"Messages: {len(st.session_state['chat_history'])}")
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        clear_chat()
    
    st.divider()
    
    # Instructions
    st.subheader("📖 How to Use")
    st.markdown("""
    1. Type your message in the input box
    2. Press Enter or click Send
    3. The bot will respond with context
    4. Continue the conversation!
    """)
    
    st.divider()
    
    # Status check
    st.subheader("🔌 Backend Status")
    try:
        health_check = requests.get("http://127.0.0.1:8000/", timeout=2)
        if health_check.status_code == 200:
            st.success("✅ Connected")
        else:
            st.error("❌ Backend Error")
    except:
        st.error("❌ Not Connected")


# Display chat history
chat_container = st.container()
with chat_container:
    for i, (speaker, text) in enumerate(st.session_state["chat_history"]):
        if speaker == "You":
            with st.chat_message("user", avatar="👤"):
                st.markdown(text)
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(text)

# Chat input
user_input = st.chat_input("Type your message here...", key="chat_input")

if user_input:
    # Add user message to history and display
    st.session_state["chat_history"].append(("You", user_input))
    
    with chat_container:
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
    
    # Get bot response
    with st.spinner("🤔 Thinking..."):
        reply = send_message(user_input, st.session_state["session_id"])
    
    # Add bot response to history and display
    st.session_state["chat_history"].append(("Bot", reply))
    
    with chat_container:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(reply)
    
    # Rerun to update the UI
    st.rerun()

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8rem;'>"
    "Built with ❤️ using LangGraph, FastAPI, and Streamlit"
    "</div>",
    unsafe_allow_html=True
)
