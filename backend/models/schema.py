from typing_extensions import TypedDict
from typing import List, Dict, Any

class State(TypedDict):
    """State for chat flow"""
    chat_response: List[Dict[str, Any]]
    role: str
    message: str
    history: List[Dict[str, Any]]

class Message(TypedDict):
    role: str
    content: str

class History(TypedDict):
    """Chat history"""
    messages: List[Message]

class ChatResponse(TypedDict):
    """Chat response"""
    messages: List[Message]