# LangGraph Chatbot - System Architecture & Workflow

## 🏗️ System Architecture Diagram

```mermaid
flowchart TB
    A[Streamlit UI Port 8501]
    A1[Chat Input]
    A2[Chat Display]
    A3[Session State]
    
    B[FastAPI Server Port 8000]
    B1[Chat Endpoint]
    B2[Session Manager]
    B3[CORS Middleware]
    
    C[LangGraph State Machine]
    C1[Chat Node]
    C2[State Management]
    
    D[OpenRouter Gateway]
    D1[OpenAI GPT-4]
    D2[Anthropic Claude]
    D3[Google Gemini]
    D4[Meta Llama]
    
    E[In-Memory Store]
    E1[Conversation History]
    E2[Session Data]
    
    A --> A1
    A --> A2
    A --> A3
    B --> B1
    B --> B2
    B --> B3
    C --> C1
    C --> C2
    D --> D1
    D --> D2
    D --> D3
    D --> D4
    E --> E1
    E --> E2
    
    A1 -->|User Message| B1
    B1 -->|Request| C1
    C1 -->|API Call| D
    D -->|LLM Response| C1
    C1 -->|Update State| C2
    C2 -->|Store| E1
    B2 <-->|Read/Write| E
    C2 -->|Response| B1
    B1 -->|JSON Reply| A2
```

## 📊 Request Flow Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant ST as Streamlit UI
    participant FA as FastAPI
    participant LG as LangGraph
    participant OR as OpenRouter
    participant AI as AI Model
    participant DB as Memory Store

    U->>ST: Type message
    ST->>FA: POST /chat {user_input, session_id}
    FA->>DB: Get session history
    DB-->>FA: Return messages[]
    FA->>LG: Invoke graph with state
    LG->>LG: Add user message to history
    LG->>OR: Send messages to OpenRouter
    OR->>AI: Route to selected model
    AI-->>OR: Generate response
    OR-->>LG: Return completion
    LG->>LG: Add AI response to history
    LG->>DB: Update session state
    LG-->>FA: Return updated state
    FA-->>ST: JSON {reply, session_id}
    ST-->>U: Display AI response
```

## 🔄 LangGraph State Machine

```mermaid
stateDiagram-v2
    [*] --> ChatNode
    ChatNode --> GetMessages: Load History
    GetMessages --> AddUserMessage: Append Input
    AddUserMessage --> CallLLM: Send to OpenRouter
    CallLLM --> ExtractResponse: Get Completion
    ExtractResponse --> AddAIMessage: Append Reply
    AddAIMessage --> UpdateState: Save to Memory
    UpdateState --> [*]: Return State
```

## 🗂️ File Structure & Dependencies

```mermaid
flowchart LR
    R[Project Root]
    
    B1[main.py]
    B2[chatbot_graph.py]
    B3[__init__.py]
    
    F1[app.py]
    
    C1[requirements.txt]
    C2[.env]
    C3[.env.example]
    C4[.gitignore]
    
    D1[README.md]
    D2[WORKFLOW.md]

    R --> B1
    R --> B2
    R --> B3
    R --> F1
    R --> C1
    R --> C2
    R --> C3
    R --> C4
    R --> D1
    R --> D2

    B1 -.->|imports| B2
    F1 -.->|HTTP| B1
```

## 🎯 Component Interaction Map

```mermaid
flowchart TD
    EXT1[FastAPI]
    EXT2[Streamlit]
    EXT3[LangGraph]
    EXT4[OpenAI SDK]
    EXT5[Pydantic]
    
    MAIN[main.py]
    GRAPH[chatbot_graph.py]
    APP[app.py]
    
    OR[OpenRouter API]
    end

    subgraph Services["External Services"]
        OR[OpenRouter API]
    end

    MAIN --> EXT1
    MAIN --> EXT5
    MAIN --> GRAPH

    GRAPH --> EXT3
    GRAPH --> EXT4
    GRAPH --> OR

    APP --> EXT2
    APP --> MAIN
```

## 📦 Data Flow

```mermaid
flowchart LR
    A[User Input] --> B{Session Exists?}
    B -->|No| C[Create New Session]
    B -->|Yes| D[Load Session Data]
    C --> E[Empty Message Array]
    D --> F[Existing Messages]
    E --> G[Append User Message]
    F --> G
    G --> H[Send to LangGraph]
    H --> I[OpenRouter API]
    I --> J[AI Model Processing]
    J --> K[Response Generated]
    K --> L[Append AI Message]
    L --> M[Update Session]
    M --> N[Return to User]
    N --> O[Display in UI]
```

## 🔐 Environment Variables Flow

```mermaid
flowchart TD
    ENV[.env File] --> A[OPENROUTER_API_KEY]
    ENV --> B[OPENROUTER_MODEL]
    ENV --> C[OPENROUTER_TEMPERATURE]
    ENV --> D[OPENROUTER_SITE_URL]
    ENV --> E[OPENROUTER_SITE_NAME]

    A --> F[OpenAI Client Init]
    B --> G[Model Selection]
    C --> G
    D --> H[Extra Headers]
    E --> H

    F --> I[OpenRouter Request]
    G --> I
    H --> I

    I --> J[AI Response]

```

## 🚀 Deployment Architecture (Future)

```mermaid
flowchart TB
    LB[Load Balancer]
    
    ST1[Streamlit 1]
    ST2[Streamlit 2]
    ST3[Streamlit N]
    
    FA1[FastAPI 1]
    FA2[FastAPI 2]
    FA3[FastAPI N]
    
    REDIS[Redis Cluster]
    PG[PostgreSQL]
    MONGO[MongoDB]
    OR[OpenRouter API]

    LB --> ST1
    LB --> ST2
    LB --> ST3
    
    ST1 --> FA1
    ST2 --> FA2
    ST3 --> FA3
    
    FA1 --> REDIS
    FA2 --> REDIS
    FA3 --> REDIS
    
    FA1 --> PG
    FA2 --> MONGO
    FA3 --> PG
    
    FA1 --> OR
    FA2 --> OR
    FA3 --> OR
```

## 📈 Session Management

```mermaid
stateDiagram-v2
    [*] --> Idle: No Session
    Idle --> Active: User Sends Message
    Active --> Processing: LangGraph Processing
    Processing --> Active: Response Received
    Active --> Active: Continue Chat
    Active --> Cleared: User Clears Chat
    Cleared --> Idle: Session Deleted
    Active --> Timeout: Inactivity
    Timeout --> Idle: Session Expired

    note right of Active
        Messages stored
        Context maintained
    end note

    note right of Processing
        API call in progress
        State locked
    end note
```

---

## 🎨 Visual Legend

- 🟦 **Blue**: User Interface / Frontend
- 🟨 **Yellow**: Backend / API Layer
- 🟪 **Purple**: Business Logic
- 🟩 **Green**: External Services / AI
- 🟥 **Red**: Data Storage / Memory

---

**Generated for**: End-to-End AI Chatbot using LangGraph, FastAPI, Streamlit & OpenRouter
**Last Updated**: November 12, 2025
