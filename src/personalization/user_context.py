"""
CS305 - User Context for Personalization
Author: Bismark Mankata
"""

from datetime import datetime
from typing import Optional, List


class UserContext:
    """Stores user session information for personalization."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self._name: Optional[str] = None
        self.conversation_history: List[dict] = []
        self.session_start = datetime.now()
        self.fallback_count = 0
        self.last_intent: Optional[str] = None
    
    def set_name(self, name: str):
        """Store user's name."""
        self._name = name.strip()
    
    def get_name(self) -> Optional[str]:
        """Get user's name if known."""
        return self._name
    
    def add_to_history(self, user_message: str, bot_response: str, intent: str):
        """Record conversation exchange."""
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user': user_message,
            'bot': bot_response,
            'intent': intent
        })
        self.last_intent = intent
    
    def get_session_duration(self) -> str:
        """Get formatted session duration."""
        duration = datetime.now() - self.session_start
        minutes = int(duration.total_seconds() // 60)
        seconds = int(duration.total_seconds() % 60)
        return f"{minutes}m {seconds}s"
    
    def increment_fallback(self):
        """Track how many times bot didn't understand."""
        self.fallback_count += 1
    
    def should_suggest_help(self) -> bool:
        """Check if user seems lost."""
        return self.fallback_count >= 3