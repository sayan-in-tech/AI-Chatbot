import traceback
from typing import Dict, List
from backend.models.schema import Message

class MemoryStore:
    """In-memory storage for chat sessions"""
    
    def __init__(self):
        try:
            self._sessions: Dict[str, List[Message]] = {}
            print("✅ [services/memory/memory.py:__init__] MemoryStore initialized")
        except Exception as e:
            print(f"❌ [services/memory/memory.py:__init__] Error initializing MemoryStore: {str(e)}")
            traceback.print_exc()
            raise
    
    def get_history(self, session_id: str) -> List[Message]:
        """Get chat history for a session"""
        try:
            history = self._sessions.get(session_id, [])
            return history
        except KeyError as e:
            print(f"❌ [services/memory/memory.py:get_history] KeyError getting history for session {session_id}: {str(e)}")
            traceback.print_exc()
            return []
        except Exception as e:
            print(f"❌ [services/memory/memory.py:get_history] Error getting history for session {session_id}: {str(e)}")
            traceback.print_exc()
            return []
    
    def add_message(self, session_id: str, message: Message):
        """Add a message to the chat history"""
        try:
            if session_id not in self._sessions:
                self._sessions[session_id] = []
            self._sessions[session_id].append(message)
        except Exception as e:
            print(f"❌ [services/memory/memory.py:add_message] Error adding message to session {session_id}: {str(e)}")
            traceback.print_exc()
            raise
    
    def add_messages(self, session_id: str, messages: List[Message]):
        """Add multiple messages to the chat history"""
        try:
            if session_id not in self._sessions:
                self._sessions[session_id] = []
            self._sessions[session_id].extend(messages)
        except Exception as e:
            print(f"❌ [services/memory/memory.py:add_messages] Error adding messages to session {session_id}: {str(e)}")
            traceback.print_exc()
            raise
    
    def clear_session(self, session_id: str):
        """Clear history for a session"""
        try:
            if session_id in self._sessions:
                del self._sessions[session_id]
                print(f"✅ [services/memory/memory.py:clear_session] Cleared session {session_id}")
            else:
                print(f"⚠️  [services/memory/memory.py:clear_session] Session {session_id} not found")
        except KeyError as e:
            print(f"❌ [services/memory/memory.py:clear_session] KeyError clearing session {session_id}: {str(e)}")
            traceback.print_exc()
        except Exception as e:
            print(f"❌ [services/memory/memory.py:clear_session] Error clearing session {session_id}: {str(e)}")
            traceback.print_exc()
            raise
    
    def get_conversation_history(self, session_id: str) -> List[dict]:
        """Get conversation history as list of dicts for Gemini API"""
        try:
            messages = self.get_history(session_id)
            history = [
                {
                    "role": msg["role"],
                    "parts": [{"text": msg["content"]}]
                }
                for msg in messages
            ]
            return history
        except KeyError as e:
            print(f"❌ [services/memory/memory.py:get_conversation_history] KeyError getting conversation for session {session_id}: {str(e)}")
            traceback.print_exc()
            return []
        except Exception as e:
            print(f"❌ [services/memory/memory.py:get_conversation_history] Error getting conversation for session {session_id}: {str(e)}")
            traceback.print_exc()
            return []

    def get_all_histories(self) -> Dict[str, List[Message]]:
        """Return a shallow copy of all session histories"""
        try:
            return {sid: list(messages) for sid, messages in self._sessions.items()}
        except Exception as e:
            print(f"❌ [services/memory/memory.py:get_all_histories] Error getting all histories: {str(e)}")
            traceback.print_exc()
            return {}

# Global memory store instance
memory_store = MemoryStore()
