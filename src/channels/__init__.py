"""
CS305 - Channels Module
Author: Bismark Mankata
Date: January 2026

Communication channels for the chatbot.
Supports console, web API, and extensible for future channels.
"""

from .base_channel import BaseChannel
from .console_channel import ConsoleChannel

__all__ = [
    'BaseChannel',
    'ConsoleChannel'
]