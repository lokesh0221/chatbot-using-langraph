"""
LangGraph Chatbot Logic
Manages conversation flow and memory using LangGraph state machine.
Uses OpenRouter for LLM access.
"""

from langgraph.graph import StateGraph, END
from openai import OpenAI
from typing import TypedDict, List, Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenRouter client once (reused across requests)
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


class ChatState(TypedDict):
    """State structure for the chatbot conversation."""
    user_input: str
    messages: List[Dict[str, str]]
    reply: str


def chat_node(state: ChatState) -> ChatState:
    """
    Main chat node that processes user input and generates AI response using OpenRouter.
    
    Args:
        state: Current conversation state with user input and message history
        
    Returns:
        Updated state with AI response
    """
    # Get current messages and user input
    messages = state.get("messages", [])
    user_input = state["user_input"]
    
    # Add user message to history
    messages.append({"role": "user", "content": user_input})
    
    # Get model and temperature from environment or use defaults
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")
    temperature = float(os.getenv("OPENROUTER_TEMPERATURE", "0.7"))
    
    # Generate AI response using OpenRouter
    completion = openrouter_client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost:8501"),
            "X-Title": os.getenv("OPENROUTER_SITE_NAME", "LangGraph Chatbot"),
        },
        model=model,
        messages=messages,
        temperature=temperature,
    )
    
    # Extract response content
    response_content = completion.choices[0].message.content
    
    # Add assistant response to history
    messages.append({"role": "assistant", "content": response_content})
    
    # Update state
    state["messages"] = messages
    state["reply"] = response_content
    
    return state


# Build the LangGraph workflow
def create_chat_graph():
    """
    Creates and compiles the LangGraph chatbot workflow.
    
    Returns:
        Compiled LangGraph application
    """
    graph = StateGraph(ChatState)
    
    # Add the chat node
    graph.add_node("chat", chat_node)
    
    # Set entry point
    graph.set_entry_point("chat")
    
    # Add edge to END
    graph.add_edge("chat", END)
    
    # Compile the graph
    return graph.compile()


# Create the chatbot app instance
app = create_chat_graph()
