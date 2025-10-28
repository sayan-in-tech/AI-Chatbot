# AI Chatbot - FastAPI Backend

A sophisticated chatbot backend with streaming responses, conversation memory, and Google Search grounding.

## Features

- **Streaming Responses**: Real-time token-by-token streaming via Server-Sent Events (SSE)
- **Conversation Memory**: Maintains chat history per session
- **Google Search Grounding**: Uses Google Search tool for accurate information
- **Multiple Roles**: Support for general, doctor, and programmer personas
- **REST API**: FastAPI with automatic OpenAPI documentation

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your-google-api-key-here
MODEL=gemini-2.5-flash
```

Get a Google API key from: https://makersuite.google.com/app/apikey

### 3. Run the Server

```bash
python -m backend.run
```

The API will be available at: `http://127.0.0.1:8000`

## API Endpoints

- **Documentation**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

### Available Endpoints

1. `POST /api/v1/chat` - Non-streaming chat
2. `POST /api/v1/chat/stream` - Streaming chat (SSE)
3. `GET /api/v1/history/{session_id}` - Get chat history
4. `POST /api/v1/history/clear` - Clear chat history

## Usage Example

### Streaming Chat

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/api/v1/chat/stream",
    json={
        "message": "Hello!",
        "session_id": "my-session",
        "role": "general"
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

### Get Chat History

```python
import requests

response = requests.get("http://127.0.0.1:8000/api/v1/history/my-session")
print(response.json())
```

## Project Structure

```
backend/
├── app.py                      # FastAPI app entry point
├── routes/routes.py           # API endpoints
├── services/
│   ├── chat/chat.py           # Chat logic with streaming
│   ├── llm_connector/         # Gemini client
│   └── memory/memory.py       # Conversation memory
├── models/schema.py           # Pydantic models
└── prompts/prompts.py         # System prompts
```

## Testing

Run the test script:

```bash
python test_api.py
```

## Requirements

- Python 3.9+
- Google API key
- See `requirements.txt` for all dependencies
