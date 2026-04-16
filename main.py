"""
CS305 - E-Commerce Chatbot
Main Entry Point - Console Version
Author: Bismark Mankata
Date: January 2026
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
from src.channels import ConsoleChannel
from src.nlp import IntentClassifier, EntityExtractor
from src.personalization.user_context import UserContext
from src.handlers import (
    GreetingHandler,
    OrderHandler,
    FAQHandler,
    FallbackHandler
)


class ChatbotEngine:
    """Main chatbot engine that coordinates all components."""
    
    def __init__(self):
        """Initialize the chatbot engine."""
        # Initialize NLP components
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
        
        # Initialize handlers
        self.handlers = [
            GreetingHandler(),
            OrderHandler(),
            FAQHandler(),
            FallbackHandler()
        ]
        
        # Sort handlers by priority
        self.handlers.sort(key=lambda h: h.get_priority(), reverse=True)
        
        # User context storage
        self.user_context = UserContext("console_user")
    
    def process_message(self, user_input: str) -> str:
        """
        Process a user message and return a response.
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Bot response string
        """
        if not user_input or not user_input.strip():
            return "I didn't catch that. Could you say something?"
        
        # Classify intent
        intent, confidence = self.intent_classifier.classify(user_input)
        
        if settings.DEBUG_MODE:
            print(f"[DEBUG] Intent: {intent} (confidence: {confidence:.2f})")
        
        # Build context for handlers
        handler_context = {
            'user_name': self.user_context.get_name(),
            'session_id': self.user_context.session_id,
            'conversation_history': self.user_context.conversation_history
        }
        
        # Find and use appropriate handler
        response = None
        for handler in self.handlers:
            if handler.can_handle(intent):
                try:
                    response = handler.handle(user_input, intent, handler_context)
                    
                    # Update user name if captured
                    if 'user_name' in handler_context and handler_context['user_name']:
                        self.user_context.set_name(handler_context['user_name'])
                    
                    break
                except Exception as e:
                    if settings.DEBUG_MODE:
                        print(f"[ERROR] Handler {handler.get_name()} failed: {e}")
                    continue
        
        # Fallback if no handler responded
        if response is None:
            response = "I'm not sure how to respond to that. Type 'help' for options."
        
        # Add to history
        self.user_context.add_to_history(user_input, response, intent)
        
        return response


def main():
    """Main entry point."""
    
    # Show configuration if debug mode
    if settings.DEBUG_MODE:
        print(settings.get_config_summary())
        print()
    
    # Initialize engine
    engine = ChatbotEngine()
    
    # Create and run console channel
    channel = ConsoleChannel()
    
    def process_func(user_input: str) -> str:
        return engine.process_message(user_input)
    
    channel.run_loop(process_func)


if __name__ == "__main__":
    main()