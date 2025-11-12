"""
FastAPI Backend Server
Provides REST API endpoints for the LangGraph chatbot.
"""

from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import logging

from chatbot_graph import app as chat_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
api = FastAPI(
    title="LangGraph Chatbot API",
    description="AI Chatbot backend powered by LangGraph and OpenAI",
    version="1.0.0"
)

# Add CORS middleware for frontend communication
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory conversation state store (use Redis/DB for production)
conversation_state: Dict[str, Dict] = {}


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    user_input: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    reply: str
    session_id: str


@api.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "message": "LangGraph Chatbot API is running",
        "version": "1.0.0"
    }


@api.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint that processes user messages.
    
    Args:
        request: Chat request containing user input and session ID
        
    Returns:
        ChatResponse with AI reply and session ID
    """
    try:
        session_id = request.session_id
        user_input = request.user_input
        
        # Initialize session if it doesn't exist
        if session_id not in conversation_state:
            conversation_state[session_id] = {"messages": []}
            logger.info(f"New session created: {session_id}")
        
        # Invoke the LangGraph chatbot
        result = chat_app.invoke({
            "user_input": user_input,
            "messages": conversation_state[session_id]["messages"]
        })
        
        # Update session memory with conversation history
        conversation_state[session_id]["messages"] = result["messages"]
        
        logger.info(f"Session {session_id}: User: {user_input[:50]}... | Bot: {result['reply'][:50]}...")
        
        return ChatResponse(
            reply=result["reply"],
            session_id=session_id
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@api.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """
    Clear conversation history for a specific session.
    
    Args:
        session_id: Session identifier to clear
        
    Returns:
        Status message
    """
    if session_id in conversation_state:
        del conversation_state[session_id]
        logger.info(f"Session cleared: {session_id}")
        return {"status": "success", "message": f"Session {session_id} cleared"}
    else:
        return {"status": "not_found", "message": f"Session {session_id} not found"}


@api.get("/sessions")
async def list_sessions():
    """
    List all active sessions.
    
    Returns:
        List of active session IDs and message counts
    """
    sessions = {
        sid: {"message_count": len(state["messages"])}
        for sid, state in conversation_state.items()
    }
    return {"active_sessions": sessions}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000, reload=True)
