"""
CS305 - Base Handler Abstract Class
Author: Bismark Mankata
Date: January 2026

Defines the interface that all intent handlers must implement.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseHandler(ABC):
    """
    Abstract base class for all intent handlers.
    
    Each handler is responsible for processing specific types of user intents
    and generating appropriate responses.
    """
    
    def __init__(self):
        """Initialize the handler."""
        self.name = "base_handler"
        self.priority = 0  # Higher priority handlers are checked first
    
    @abstractmethod
    def can_handle(self, intent: str) -> bool:
        """
        Check if this handler can process the given intent.
        
        Args:
            intent: The classified intent tag (e.g., 'greeting', 'order_status')
            
        Returns:
            True if this handler can process the intent, False otherwise
        """
        pass
    
    @abstractmethod
    def handle(self, user_input: str, intent: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process the user input and return a response.
        
        Args:
            user_input: The raw user message
            intent: The classified intent tag
            context: Optional dictionary containing session context (user name, history, etc.)
            
        Returns:
            A string response to send back to the user
        """
        pass
    
    def get_confidence(self, user_input: str) -> float:
        """
        Return confidence score for this handler on the given input.
        
        This can be overridden by subclasses to provide more sophisticated
        confidence scoring beyond simple intent matching.
        
        Args:
            user_input: The raw user message
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        return 0.0
    
    def get_name(self) -> str:
        """Return the name of this handler."""
        return self.name
    
    def get_priority(self) -> int:
        """Return the priority of this handler."""
        return self.priority
    
    def __str__(self) -> str:
        return f"{self.name} (priority: {self.priority})"