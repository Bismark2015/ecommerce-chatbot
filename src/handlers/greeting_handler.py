"""
CS305 - Greeting Handler
Author: Bismark Mankata
Date: January 2026

Handles greeting intents and user name capture for personalization.
"""

import random
import re
from typing import Optional, Dict, Any

from .base_handler import BaseHandler


class GreetingHandler(BaseHandler):
    """Handles greeting intents like hello, hi, good morning."""
    
    def __init__(self):
        super().__init__()
        self.name = "greeting_handler"
        self.priority = 10
        self.intents = ['greeting']
        
        self.greetings = [
            "Hello! Welcome to Bismark's Store. How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! Thanks for stopping by. What are you looking for?",
            "Good to see you! How may I assist you with your shopping?",
            "Welcome! I'm here to help with any questions about our products or orders."
        ]
        
        self.personalized_greetings = [
            "Welcome back, {name}! How can I help you today?",
            "Hello again, {name}! What can I do for you?",
            "Hi {name}! Great to see you again. How can I assist?",
            "Hey {name}! Ready to do some shopping?",
            "Welcome back, {name}! What brings you to Bismark's Store today?"
        ]
        
        self.name_indicators = ['my name is', 'i am', "i'm", 'call me', 'this is']
    
    def can_handle(self, intent: str) -> bool:
        return intent in self.intents
    
    def handle(self, user_input: str, intent: str, context: Optional[Dict[str, Any]] = None) -> str:
        if context and context.get('user_name'):
            name = context['user_name']
            template = random.choice(self.personalized_greetings)
            return template.format(name=name)
        
        if self._is_name_introduction(user_input):
            name = self._extract_name(user_input)
            if name:
                if context is not None:
                    context['user_name'] = name
                    context['name_captured'] = True
                return f"Nice to meet you, {name}! How can I help you with Bismark's Store today?"
        
        return random.choice(self.greetings)
    
    def _is_name_introduction(self, text: str) -> bool:
        text_lower = text.lower().strip()
        for indicator in self.name_indicators:
            if indicator in text_lower:
                parts = text_lower.split(indicator)
                if len(parts) > 1 and len(parts[1].strip()) > 0:
                    return True
        return False
    
    def _extract_name(self, text: str) -> str:
        text_lower = text.lower().strip()
        for indicator in self.name_indicators:
            if indicator in text_lower:
                parts = text_lower.split(indicator)
                if len(parts) > 1:
                    name_part = parts[1].strip()
                    name_part = re.sub(r'[^\w\s]', '', name_part)
                    words = name_part.split()
                    if words:
                        return words[0].capitalize()
        return ""
    
    def get_confidence(self, user_input: str) -> float:
        greeting_keywords = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'howdy']
        user_lower = user_input.lower()
        for keyword in greeting_keywords:
            if keyword in user_lower:
                return 0.9
        if self._is_name_introduction(user_input):
            return 0.7
        return 0.0