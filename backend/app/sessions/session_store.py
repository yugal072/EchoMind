from datetime import datetime
from pydantic import BaseModel
import json
from typing import List, Optional
from pathlib import Path

from langchain_core.messages import messages_to_dict, messages_from_dict 
from langchain_community.chat_message_histories import ChatMessageHistory

from app.core.config import SESSION_STORE_DIR


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None


class SessionData(BaseModel):
    session_id: str  
    messages: List[dict]
    created_at: datetime
    last_updated: datetime


class PersistentSessionStore:
    """Handles persistent chat history using JSON files."""

    def __init__(self):
        self.storage_dir: Path = SESSION_STORE_DIR
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, session_id: str) -> Path:
        return self.storage_dir / f"session_{session_id}.json"

    def get_session_history(self, session_id: str):
        file_path = self._get_file_path(session_id)
        if not file_path.exists():
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            raw_messages = data["messages"] if isinstance(data, dict) and "messages" in data else data

            # raw_messages must be in LangChain's native {"type": ..., "data": {...}} shape
            return messages_from_dict(raw_messages)

            return messages_from_dict(raw_messages)

        except Exception as e:
            print(f"Error loading session {session_id}: {e}")
            return []

    def store_session_history(self, session_id: str, messages: List) -> None:
        print(f"DEBUG: Attempting to save session {session_id} with {len(messages)} messages")

        if not messages:
            return

        file_path = self._get_file_path(session_id)

        try:
            # Preserve LangChain's native dict shape — don't flatten to role/content
            message_dicts = messages_to_dict(messages)

            # Preserve original created_at if the file already exists
            created_at = datetime.now()
            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        existing = json.load(f)
                    created_at = datetime.fromisoformat(existing["created_at"])
                except Exception:
                    pass

            session_data = SessionData(
                session_id=session_id,
                messages=message_dicts,
                created_at=created_at,
                last_updated=datetime.now()
            )

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(session_data.model_dump(), f, indent=4, default=str)

            print(f"✅ Successfully saved session {session_id}")
        except Exception as e:
            print(f"❌ Failed to save session {session_id}: {e}")

# ==================== CUSTOM HISTORY CLASS ====================

class PersistentChatMessageHistory(ChatMessageHistory):
    """Custom history that automatically loads and saves."""
    session_id:str
    session_store: PersistentSessionStore = None        # declare so pydantic allows it
    
    class Config:
        arbitrary_types_allowed = True  # PersistentSessionStore isn't a Pydantic model

    def __init__(self, session_id: str, **kwargs):
        super().__init__(session_id=session_id, **kwargs)
        self.session_id = session_id
        self.session_store = PersistentSessionStore()
        
        # Load existing messages
        loaded = self.session_store.get_session_history(session_id)
        self.messages = loaded

    def add_message(self, message):
        """Automatically save after adding a message"""
        print(f"DEBUG: add_message called for session {self.session_id}")
        
        super().add_message(message)                    # Let parent handle it
        self.session_store.store_session_history(self.session_id, self.messages)
        print(f"DEBUG: Auto-saved session {self.session_id}")