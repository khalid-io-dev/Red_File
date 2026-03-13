from typing import List, Dict, Any, Optional
from datetime import datetime
import json

class ConversationMemory:
    def __init__(self, max_messages: int = 20, max_tokens: int = 4000):
        self.messages: List[Dict[str, Any]] = []
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.metadata: Dict[str, Any] = {}
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.messages.append(message)
        self._trim_history()
    
    def get_messages(self, include_system: bool = True) -> List[Dict[str, str]]:
        messages = []
        for msg in self.messages:
            if not include_system and msg["role"] == "system":
                continue
            messages.append({"role": msg["role"], "content": msg["content"]})
        return messages
    
    def get_context_window(self) -> List[Dict[str, str]]:
        return self.get_messages()[-self.max_messages:]
    
    def _trim_history(self):
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def clear(self):
        self.messages = []
        self.metadata = {}
    
    def save(self, filepath: str):
        with open(filepath, 'w') as f:
            json.dump({
                "messages": self.messages,
                "metadata": self.metadata
            }, f, indent=2)
    
    def load(self, filepath: str):
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.messages = data.get("messages", [])
            self.metadata = data.get("metadata", {})
