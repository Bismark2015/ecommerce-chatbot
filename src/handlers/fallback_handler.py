"""
CS305 - Fallback Handler
Author: Bismark Mankata
Date: January 2026
"""

import os
import sys
import random
from typing import Optional, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from .base_handler import BaseHandler
from config import settings
from src.utils import helpers


class FallbackHandler(BaseHandler):
    """Handles unknown intents with helpful error messages."""
    
    def __init__(self):
        super().__init__()
        self.name = "fallback_handler"
        self.priority = 0
        self.fallback_counts = {}
        
        self.suggestions = [
            "Try asking about 'order status', 'shipping', or 'returns'.",
            "You can type 'help' to see everything I can do.",
            "Need to track an order? Share your order number like 'ORD-12345'."
        ]
    
    def can_handle(self, intent: str) -> bool:
        return True
    
    def handle(self, user_input: str, intent: str, context: Optional[Dict[str, Any]] = None) -> str:
        session_id = context.get('session_id', 'default') if context else 'default'
        
        current_count = self.fallback_counts.get(session_id, 0) + 1
        self.fallback_counts[session_id] = current_count
        
        if current_count >= 3:
            return self._get_detailed_help()
        
        base_message = helpers.get_random_response(settings.FALLBACK_MESSAGES)
        tip = random.choice(self.suggestions)
        
        return f"{base_message}\n\nTip: {tip}"
    
    def _get_detailed_help(self) -> str:
        return """I can help you with:
• Order tracking - "Where is my order ORD-12345?"
• Returns - "What is your return policy?"
• Shipping - "How much is shipping?"
• Payment - "What payment methods do you accept?"
• Products - "What products do you have?"

What would you like to know?"""
    
    def reset_fallback_count(self, session_id: str):
        if session_id in self.fallback_counts:
            self.fallback_counts[session_id] = 0
    
    def get_fallback_count(self, session_id: str) -> int:
        return self.fallback_counts.get(session_id, 0)