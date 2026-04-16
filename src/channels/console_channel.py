"""
CS305 - Console Channel
Author: Bismark Mankata
Date: January 2026

Terminal/console-based communication channel for the chatbot.
"""

import sys
import os
from typing import Optional, Dict, Any, Callable

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from .base_channel import BaseChannel
from config import settings


class ConsoleChannel(BaseChannel):
    """
    Console-based channel for terminal interaction.
    
    This channel reads from stdin and writes to stdout,
    providing a simple command-line interface for the chatbot.
    """
    
    def __init__(self, bot_name: str = None, shop_name: str = None):
        """
        Initialize the console channel.
        
        Args:
            bot_name: Name of the bot (defaults to settings.BOT_NAME)
            shop_name: Name of the shop (defaults to settings.SHOP_NAME)
        """
        super().__init__(name="console_channel")
        
        self.bot_name = bot_name or settings.BOT_NAME
        self.shop_name = shop_name or settings.SHOP_NAME
        self.message_handler: Optional[Callable] = None
        self.running = False
        
        # Console colors (if supported)
        self.use_colors = self._supports_color()
        
        # Color codes
        self.COLORS = {
            'reset': '\033[0m',
            'bot': '\033[94m',      # Blue
            'user': '\033[92m',     # Green
            'error': '\033[91m',    # Red
            'info': '\033[93m',     # Yellow
            'header': '\033[95m'    # Magenta
        }
    
    def _supports_color(self) -> bool:
        """Check if terminal supports color output."""
        try:
            import colorama
            colorama.init()
            return True
        except ImportError:
            # Check if running in a terminal that supports ANSI
            return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    
    def _colorize(self, text: str, color: str) -> str:
        """Add color to text if supported."""
        if self.use_colors and color in self.COLORS:
            return f"{self.COLORS[color]}{text}{self.COLORS['reset']}"
        return text
    
    def start(self):
        """Start the console channel."""
        self.is_active = True
        self.running = True
        self._print_header()
        self._print_welcome()
    
    def stop(self):
        """Stop the console channel."""
        self.running = False
        self.is_active = False
        self._print_goodbye()
    
    def _print_header(self):
        """Print the channel header."""
        width = 60
        print()
        print("=" * width)
        title = f"  {self.bot_name} - {self.shop_name}  "
        print(self._colorize(title.center(width), 'header'))
        print("=" * width)
    
    def _print_welcome(self):
        """Print welcome message."""
        print()
        print(self._colorize(f"Hello! I'm {self.bot_name}, your shopping assistant.", 'bot'))
        print()
        print("I can help you with:")
        print("  • Checking order status")
        print("  • Product information")
        print("  • Return policy questions")
        print("  • Shipping details")
        print("  • Payment methods")
        print()
        print("Type " + self._colorize("'help'", 'info') + " for more options.")
        print("Type " + self._colorize("'quit'", 'info') + " to exit.")
        print("-" * 40)
        print()
    
    def _print_goodbye(self):
        """Print goodbye message."""
        print()
        print(self._colorize(f"Thank you for visiting {self.shop_name}!", 'bot'))
        print(self._colorize("Goodbye!", 'bot'))
        print()
    
    def send_message(self, message: str, context: Optional[Dict[str, Any]] = None):
        """
        Send a message to the console.
        
        Args:
            message: The message to display
            context: Optional context (unused in console)
        """
        formatted = self.format_message(message, sender="bot")
        print(self._colorize(formatted, 'bot'))
    
    def receive_message(self) -> Optional[str]:
        """
        Receive a message from console input.
        
        Returns:
            User input string, or None if error
        """
        try:
            prompt = self._colorize("You: ", 'user')
            user_input = input(prompt).strip()
            return user_input if user_input else None
        except (KeyboardInterrupt, EOFError):
            return None
    
    def send_error(self, message: str):
        """Send an error message."""
        print(self._colorize(f"Error: {message}", 'error'))
    
    def send_info(self, message: str):
        """Send an info message."""
        print(self._colorize(message, 'info'))
    
    def send_debug(self, message: str):
        """Send a debug message (only if debug mode is on)."""
        if settings.DEBUG_MODE:
            print(self._colorize(f"[DEBUG] {message}", 'info'))
    
    def format_message(self, message: str, sender: str = "bot") -> str:
        """
        Format a message for console display.
        
        Args:
            message: Raw message content
            sender: "bot" or "user"
            
        Returns:
            Formatted string
        """
        if sender == "bot":
            return f"{self.bot_name}: {message}"
        elif sender == "user":
            return f"You: {message}"
        return message
    
    def run_loop(self, process_func: Callable[[str], str]):
        """
        Run the main interaction loop.
        
        Args:
            process_func: Function that takes user input and returns bot response
        """
        self.start()
        
        while self.running:
            user_input = self.receive_message()
            
            if user_input is None:
                continue
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                self.stop()
                break
            
            # Check for help command
            if user_input.lower() == 'help':
                self._print_help()
                continue
            
            # Process the message
            try:
                response = process_func(user_input)
                self.send_message(response)
                print()  # Empty line for readability
            except Exception as e:
                self.send_error(f"Something went wrong: {str(e)}")
                if settings.DEBUG_MODE:
                    import traceback
                    traceback.print_exc()
    
    def _print_help(self):
        """Print help information."""
        print()
        print(self._colorize("Available Commands:", 'info'))
        print("-" * 30)
        print("  hello, hi          - Greeting")
        print("  order status       - Check order (provide ORD-12345)")
        print("  return policy      - Return and refund info")
        print("  shipping           - Shipping options and costs")
        print("  payment            - Payment methods")
        print("  products           - Browse products")
        print("  contact            - Support contact info")
        print("  help               - Show this help")
        print("  quit, exit, bye    - Exit chatbot")
        print()
        print(self._colorize("Examples:", 'info'))
        print("  • where is my order ORD-12345")
        print("  • what is your return policy")
        print("  • how much is shipping")
        print("  • my name is Bismark")
        print()


# Simple test when run directly
if __name__ == "__main__":
    channel = ConsoleChannel()
    
    def echo_process(msg: str) -> str:
        return f"You said: {msg}"
    
    channel.run_loop(echo_process)