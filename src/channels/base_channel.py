"""
CS305 - Base Channel Abstract Class
Author: Bismark Mankata
Date: January 2026

Abstract base class defining the interface for all communication channels.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseChannel(ABC):
    """
    Abstract base class for all communication channels.
    
    A channel handles input/output for a specific medium:
    - Console (terminal)
    - Web (HTTP/REST)
    - WhatsApp (future)
    - Telegram (future)
    """
    
    def __init__(self, name: str = "base_channel"):
        """
        Initialize the channel.
        
        Args:
            name: Identifier for this channel
        """
        self.name = name
        self.is_active = False
    
    @abstractmethod
    def start(self):
        """
        Start the channel and begin listening for messages.
        
        This method should initialize the channel and begin
        the main interaction loop or server.
        """
        pass
    
    @abstractmethod
    def stop(self):
        """
        Stop the channel and clean up resources.
        """
        pass
    
    @abstractmethod
    def send_message(self, message: str, context: Optional[Dict[str, Any]] = None):
        """
        Send a message to the user through this channel.
        
        Args:
            message: The message to send
            context: Optional context information (user ID, session, etc.)
        """
        pass
    
    @abstractmethod
    def receive_message(self) -> Optional[str]:
        """
        Receive a message from the user.
        
        Returns:
            The user's message, or None if no message available
        """
        pass
    
    def get_name(self) -> str:
        """Return the name of this channel."""
        return self.name
    
    def is_running(self) -> bool:
        """Check if the channel is currently active."""
        return self.is_active
    
    def format_message(self, message: str, sender: str = "bot") -> str:
        """
        Format a message for display in this channel.
        
        Args:
            message: Raw message content
            sender: Who sent the message ("bot" or "user")
            
        Returns:
            Formatted message string
        """
        if sender == "bot":
            return f"Bot: {message}"
        elif sender == "user":
            return f"You: {message}"
        return message
    
    def __str__(self) -> str:
        return f"{self.name} (active: {self.is_active})"