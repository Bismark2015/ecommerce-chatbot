"""
CS305 - E-Commerce Chatbot Web API
Author: Bismark Mankata
Date: January 2026

This file creates a web server that handles chat requests using
the complete handler architecture for Requirement #1, #2, and #3.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import random
from datetime import datetime

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
from src.utils import helpers
from src.nlp.intent_classifier import IntentClassifier
from src.personalization.user_context import UserContext

# Import all handlers
from src.handlers import (
    GreetingHandler,
    OrderHandler,
    FAQHandler,
    FallbackHandler
)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow requests from GitHub Pages

# Initialize chatbot components
intent_classifier = IntentClassifier()

# Initialize handlers
greeting_handler = GreetingHandler()
order_handler = OrderHandler()
faq_handler = FAQHandler()
fallback_handler = FallbackHandler()

# Store user sessions
user_sessions = {}

# Handler mapping - order matters (higher priority first)
handlers = [
    greeting_handler,   # Priority 10
    order_handler,      # Priority 8
    faq_handler,        # Priority 5
    fallback_handler    # Priority 0 (always matches)
]

# Sort handlers by priority
handlers.sort(key=lambda h: h.get_priority(), reverse=True)

# Load data
intents_data = helpers.load_json_file(settings.INTENTS_FILE)
orders_data = helpers.load_json_file(settings.ORDERS_FILE)
products_data = helpers.load_json_file(settings.PRODUCTS_FILE)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple endpoint to check if API is running."""
    return jsonify({
        'status': 'online',
        'bot_name': settings.BOT_NAME,
        'shop_name': settings.SHOP_NAME,
        'version': settings.VERSION,
        'handlers_loaded': len(handlers),
        'active_sessions': len(user_sessions),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint.
    Receives user message, processes through handlers, returns bot response.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'response': 'Invalid request. Please send JSON data.',
                'error': True
            }), 400
        
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({
                'response': 'Please send a message.',
                'error': True
            }), 400
        
        # Get or create user session
        if session_id not in user_sessions:
            user_sessions[session_id] = {
                'context': UserContext(session_id),
                'created_at': datetime.now(),
                'message_count': 0
            }
        
        session_data = user_sessions[session_id]
        user_context = session_data['context']
        session_data['message_count'] += 1
        
        # Check for exit commands
        if is_exit_command(user_message):
            response = get_goodbye_response(user_context)
            
            # Clean up session if needed
            # user_sessions.pop(session_id, None)
            
            return jsonify({
                'response': response,
                'user_name': user_context.get_name(),
                'session_id': session_id,
                'intent': 'goodbye'
            })
        
        # Classify intent
        intent, confidence = intent_classifier.classify(user_message)
        
        if settings.DEBUG_MODE:
            print(f"[DEBUG] Session: {session_id}")
            print(f"[DEBUG] Message: {user_message}")
            print(f"[DEBUG] Intent: {intent} (confidence: {confidence:.2f})")
        
        # Process through handlers
        response = process_with_handlers(user_message, intent, user_context)
        
        # Add to conversation history
        user_context.add_to_history(user_message, response, intent)
        
        # Reset fallback count if this was a successful response
        if intent != 'unknown':
            fallback_handler.reset_fallback_count(session_id)
        
        # Check if we need to capture user's name
        name_captured = check_name_capture(user_message, user_context)
        
        return jsonify({
            'response': response,
            'user_name': user_context.get_name(),
            'session_id': session_id,
            'intent': intent,
            'confidence': confidence,
            'name_captured': name_captured,
            'message_count': session_data['message_count']
        })
        
    except Exception as e:
        print(f"[ERROR] Chat processing error: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'response': helpers.get_random_response(settings.FALLBACK_MESSAGES),
            'error': True
        }), 500


def process_with_handlers(user_message: str, intent: str, context: UserContext) -> str:
    """
    Process user message through the handler chain.
    
    Args:
        user_message: The raw user input
        intent: Classified intent tag
        context: User session context
        
    Returns:
        Bot response string
    """
    # Build context dictionary for handlers
    handler_context = {
        'user_name': context.get_name(),
        'session_id': context.session_id,
        'conversation_history': context.conversation_history,
        'fallback_count': fallback_handler.get_fallback_count(context.session_id)
    }
    
    # Find the first handler that can process this intent
    for handler in handlers:
        if handler.can_handle(intent):
            if settings.DEBUG_MODE:
                print(f"[DEBUG] Using handler: {handler.get_name()}")
            
            try:
                response = handler.handle(user_message, intent, handler_context)
                
                # Update context with any changes from handler
                if 'user_name' in handler_context and handler_context['user_name']:
                    context.set_name(handler_context['user_name'])
                
                return response
                
            except Exception as e:
                print(f"[ERROR] Handler {handler.get_name()} failed: {e}")
                continue
    
    # Ultimate fallback
    return helpers.get_random_response(settings.FALLBACK_MESSAGES)


def is_exit_command(message: str) -> bool:
    """
    Check if user wants to exit the conversation.
    
    Args:
        message: User input
        
    Returns:
        True if exit command detected
    """
    exit_keywords = ['quit', 'exit', 'goodbye', 'bye', 'see you', 'take care']
    message_lower = message.lower().strip()
    
    for keyword in exit_keywords:
        if message_lower == keyword or message_lower.startswith(keyword):
            return True
    
    return False


def get_goodbye_response(context: UserContext) -> str:
    """
    Generate personalized goodbye message.
    
    Args:
        context: User session context
        
    Returns:
        Goodbye message
    """
    name = context.get_name()
    duration = context.get_session_duration()
    
    responses = [
        f"Thank you for visiting {settings.SHOP_NAME}! Have a great day!",
        f"Goodbye! Come back anytime to {settings.SHOP_NAME}.",
        f"Take care! We appreciate your business.",
        f"Thanks for chatting with {settings.BOT_NAME}! See you next time."
    ]
    
    response = random.choice(responses)
    
    if name:
        response = f"Goodbye, {name}! " + response.split('!', 1)[-1] if '!' in response else response
    
    if settings.DEBUG_MODE:
        response += f"\n\n(Session duration: {duration})"
    
    return response


def check_name_capture(user_message: str, context: UserContext) -> bool:
    """
    Check if user's name was captured in this message.
    
    Args:
        user_message: User input
        context: User session context
        
    Returns:
        True if name was just captured
    """
    if context.get_name():
        return False  # Already have name
    
    # Check for name introduction
    name_indicators = ['my name is', 'i am', "i'm", 'call me', 'this is']
    message_lower = user_message.lower()
    
    for indicator in name_indicators:
        if indicator in message_lower:
            parts = message_lower.split(indicator)
            if len(parts) > 1:
                name_part = parts[1].strip().split()[0]
                if name_part:
                    name = name_part.capitalize()
                    context.set_name(name)
                    return True
    
    return False


@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Get active session information (for debugging)."""
    if not settings.DEBUG_MODE:
        return jsonify({'error': 'Debug mode disabled'}), 403
    
    sessions_info = {}
    for session_id, data in user_sessions.items():
        context = data['context']
        sessions_info[session_id] = {
            'created_at': data['created_at'].isoformat(),
            'message_count': data['message_count'],
            'user_name': context.get_name(),
            'duration': context.get_session_duration(),
            'fallback_count': fallback_handler.get_fallback_count(session_id)
        }
    
    return jsonify({
        'total_sessions': len(user_sessions),
        'sessions': sessions_info
    })


@app.route('/api/reset', methods=['POST'])
def reset_session():
    """Reset a user session."""
    data = request.get_json()
    session_id = data.get('session_id', 'default')
    
    if session_id in user_sessions:
        user_sessions.pop(session_id)
        fallback_handler.reset_fallback_count(session_id)
        return jsonify({
            'message': f'Session {session_id} reset successfully',
            'session_id': session_id
        })
    
    return jsonify({
        'message': f'Session {session_id} not found',
        'session_id': session_id
    }), 404


@app.route('/api/orders/<order_number>', methods=['GET'])
def get_order(order_number):
    """Direct order lookup endpoint."""
    if not orders_data:
        return jsonify({'error': 'Order data not available'}), 500
    
    for order in orders_data.get('orders', []):
        if order.get('order_number', '').upper() == order_number.upper():
            return jsonify(order)
    
    return jsonify({'error': f'Order {order_number} not found'}), 404


@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products."""
    if not products_data:
        return jsonify({'error': 'Product data not available'}), 500
    
    return jsonify(products_data)


@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get specific product by ID."""
    if not products_data:
        return jsonify({'error': 'Product data not available'}), 500
    
    for product in products_data.get('products', []):
        if product.get('id') == product_id:
            return jsonify(product)
    
    return jsonify({'error': f'Product {product_id} not found'}), 404


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get chatbot statistics."""
    total_messages = sum(data['message_count'] for data in user_sessions.values())
    
    return jsonify({
        'bot_name': settings.BOT_NAME,
        'version': settings.VERSION,
        'total_sessions': len(user_sessions),
        'total_messages': total_messages,
        'handlers': [h.get_name() for h in handlers],
        'debug_mode': settings.DEBUG_MODE,
        'uptime': 'Active'
    })


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'Check /api/health for available endpoints'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'Please try again later'
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print(f"  {settings.BOT_NAME} - CS305 Chatbot Web API")
    print(f"  {settings.SHOP_NAME}")
    print("=" * 60)
    print()
    print(f"Version: {settings.VERSION}")
    print(f"Debug Mode: {settings.DEBUG_MODE}")
    print()
    print("Loaded Handlers:")
    for handler in handlers:
        print(f"  • {handler.get_name()} (Priority: {handler.get_priority()})")
    print()
    print(f"Server running at: http://localhost:5000")
    print(f"Health check: http://localhost:5000/api/health")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=settings.DEBUG_MODE)