# 🤖 End-to-End AI Chatbot

> A modern, production-ready chatbot application built with **LangGraph**, **FastAPI**, **Streamlit**, and **OpenRouter**

## ✨ Features

- 🧠 **LangGraph** - Advanced conversation flow and state management
- ⚡ **FastAPI** - High-performance REST API backend
- 💬 **Streamlit** - Clean and intuitive chat interface
- 🌐 **OpenRouter** - Access to multiple LLM providers through one API
- 🔄 **Persistent Memory** - Maintains conversation context across messages
- 🎯 **Modular Architecture** - Clean separation of concerns
- 🚀 **Production Ready** - Includes logging, error handling, and CORS support

## � Visual Architecture

Want to understand how everything works together? Check out the **[complete workflow diagrams](WORKFLOW.md)** with:
- System Architecture
- Request Flow Sequence
- State Machine Visualization
- Component Dependencies
- Data Flow Maps

## �📁 Project Structure

```
end_to_end_chatbot/
│
├── backend/
│   ├── main.py              # FastAPI server with REST endpoints
│   ├── chatbot_graph.py     # LangGraph conversation logic
│   └── __init__.py          # Package initialization
│
├── frontend/
│   └── app.py               # Streamlit chat interface
│
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .env                    # Your actual environment variables (git-ignored)
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── WORKFLOW.md             # Visual architecture diagrams
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai/keys))
  - **Why OpenRouter?** Access multiple AI models (OpenAI, Anthropic, Google, Meta, etc.) through a single API
  - Cost-effective with competitive pricing
  - No need for separate API keys for each provider

### Step 1: Clone or Download

Navigate to your project directory:
```bash
cd "c:\Users\Lokesh\OneDrive\Desktop\chatbot using langraph"
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_actual_api_key_here
   OPENROUTER_SITE_URL=http://localhost:8501
   OPENROUTER_SITE_NAME=LangGraph Chatbot
   ```

   **OR** set it directly in PowerShell:
   ```powershell
   $env:OPENROUTER_API_KEY="your_actual_api_key_here"
   ```

## 🚀 Running the Application

You need to run **two separate terminals** - one for the backend and one for the frontend.

### Terminal 1: Start the Backend (FastAPI)

```bash
cd backend
uvicorn main:api --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Backend API Endpoints:**
- `GET /` - Health check
- `POST /chat` - Send message and get response
- `DELETE /session/{session_id}` - Clear conversation history
- `GET /sessions` - List active sessions

### Terminal 2: Start the Frontend (Streamlit)

Open a **new terminal** and run:

```bash
cd frontend
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501`

## 💡 Usage

1. **Open the Streamlit interface** in your browser
2. **Type your message** in the chat input at the bottom
3. **Press Enter** to send
4. **View the AI response** with full conversation context
5. **Continue chatting** - the bot remembers your conversation!

### Sidebar Features:
- 📊 **Session Info** - View current session ID and message count
- 🗑️ **Clear Chat** - Reset conversation history
- 🔌 **Backend Status** - Check API connection status
- 📖 **Instructions** - Quick how-to guide

## 🔧 Configuration

### Changing the AI Model

OpenRouter supports 100+ models! Edit your `.env` file:

```env
OPENROUTER_MODEL=openai/gpt-4o          # OpenAI GPT-4o
# OPENROUTER_MODEL=openai/gpt-4o-mini   # OpenAI GPT-4o-mini (faster, cheaper)
# OPENROUTER_MODEL=anthropic/claude-3.5-sonnet  # Anthropic Claude
# OPENROUTER_MODEL=google/gemini-pro-1.5        # Google Gemini
# OPENROUTER_MODEL=meta-llama/llama-3.1-70b     # Meta Llama
```

**Popular Models:**
- `openai/gpt-4o` - Most capable OpenAI model
- `openai/gpt-4o-mini` - Fast and cost-effective (default)
- `anthropic/claude-3.5-sonnet` - Excellent for reasoning
- `google/gemini-pro-1.5` - Google's latest
- `meta-llama/llama-3.1-70b` - Open source alternative

See all models at: https://openrouter.ai/models

### Adjusting Temperature

Lower temperature (0.0-0.5) = More focused and deterministic
Higher temperature (0.5-1.0) = More creative and varied

Edit your `.env` file:
```env
OPENROUTER_TEMPERATURE=0.9
```

### Custom Backend URL

If running on a different host/port, edit `frontend/app.py`:

```python
API_URL = "http://your-backend-url:8000/chat"
```

## 🧪 Testing the Backend API

You can test the backend directly using curl or any API client:

### Send a chat message:
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Hello, who are you?", "session_id": "test123"}'
```

### Check health:
```bash
curl http://127.0.0.1:8000/
```

### List active sessions:
```bash
curl http://127.0.0.1:8000/sessions
```

## 📊 Architecture Overview

```
User Input (Streamlit UI)
    ↓
FastAPI REST API (/chat endpoint)
    ↓
LangGraph State Machine
    ↓
OpenRouter API → Multiple LLM Providers
    ↓
Response with Context
    ↓
Streamlit Display
```

### How It Works:

1. **User enters message** in Streamlit chat input
2. **Frontend sends POST request** to FastAPI backend
3. **Backend retrieves session state** (conversation history)
4. **LangGraph processes** the message through its state machine
5. **OpenRouter routes to selected LLM** (OpenAI, Anthropic, Google, etc.)
6. **LLM generates response** based on full conversation context
7. **Backend updates session** with new messages
8. **Response sent back** to frontend
9. **Streamlit displays** the reply in chat interface

## 🎯 Key Components

### `backend/chatbot_graph.py`
- Defines the LangGraph state structure
- Implements the chat node logic
- Manages message history and AI responses

### `backend/main.py`
- FastAPI server with CORS support
- Session management (in-memory store)
- REST API endpoints
- Error handling and logging

### `frontend/app.py`
- Streamlit chat interface
- Session state management
- Real-time updates
- Backend health monitoring

## 🔐 Security Notes

- **Never commit your `.env` file** to version control
- In production, use proper session storage (Redis, PostgreSQL, etc.)
- Replace `allow_origins=["*"]` with specific frontend URLs
- Implement authentication for production use
- Use HTTPS in production environments

## 🚀 Production Deployment

For production deployment, consider:

1. **Use a proper database** for session storage (Redis, MongoDB, PostgreSQL)
2. **Add authentication** (OAuth2, JWT tokens)
3. **Deploy backend** using Docker + Kubernetes or cloud services
4. **Deploy frontend** using Streamlit Cloud, Docker, or cloud platforms
5. **Use environment variables** for all configuration
6. **Implement rate limiting** to prevent abuse
7. **Add monitoring** and logging (ELK stack, CloudWatch, etc.)
8. **Use HTTPS** for all connections

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify OPENROUTER_API_KEY is set
- Install all dependencies from requirements.txt

### Frontend can't connect to backend
- Ensure backend is running on http://127.0.0.1:8000
- Check backend status in sidebar
- Verify no firewall blocking localhost connections

### API Key errors
- Verify your OpenRouter API key is valid at https://openrouter.ai/keys
- Check if you have credits available in your OpenRouter account
- Ensure OPENROUTER_API_KEY environment variable is properly set
- Note: OpenRouter requires prepaid credits (very affordable pricing)

### Import errors
- Run `pip install -r requirements.txt` again
- Use a virtual environment to avoid conflicts

## 📝 License

This project is open source and available for educational and commercial use.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📧 Support

For questions or issues, please create an issue in the repository.

---

**Built with ❤️ using LangGraph, FastAPI, Streamlit, and OpenRouter**

### 🌟 Why OpenRouter?

- **Access 100+ AI models** through a single API
- **No vendor lock-in** - switch models easily
- **Cost-effective** - competitive pricing across all providers
- **Unified interface** - same code works with OpenAI, Anthropic, Google, Meta, etc.
- **Transparent pricing** - see costs per request
- **Free models available** - test without spending money
