"""
CS305 - Intent Classifier
Author: Bismark Mankata
Date: January 2026
"""

import os
import sys
from typing import Tuple, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import settings
from src.utils import helpers


class IntentClassifier:
    """Classifies user messages into intents."""
    
    def __init__(self):
        self.intents_data = None
        self.patterns = {}
        self.intent_keywords = {}
        self.load_intents()
        self._build_pattern_index()
    
    def load_intents(self):
        """Load intents from JSON file."""
        self.intents_data = helpers.load_json_file(settings.INTENTS_FILE)
        if not self.intents_data:
            print(f"Warning: Could not load intents from {settings.INTENTS_FILE}")
            self._load_fallback_intents()
    
    def _load_fallback_intents(self):
        """Load fallback intents if JSON missing."""
        self.intents_data = {
            "intents": [
                {
                    "tag": "greeting",
                    "patterns": ["hello", "hi", "hey", "good morning"],
                    "responses": ["Hello! How can I help you?"]
                },
                {
                    "tag": "goodbye",
                    "patterns": ["bye", "goodbye", "see you", "quit"],
                    "responses": ["Goodbye! Have a great day!"]
                },
                {
                    "tag": "order_status",
                    "patterns": ["where is my order", "track order", "order status"],
                    "responses": ["Please provide your order number (ORD-12345)."]
                },
                {
                    "tag": "help",
                    "patterns": ["help", "what can you do"],
                    "responses": ["I can help with orders, products, and returns."]
                }
            ],
            "fallback_responses": ["I'm not sure I understand. Could you rephrase that?"]
        }
    
    def _build_pattern_index(self):
        """Build keyword index for fast matching."""
        if not self.intents_data:
            return
        
        for intent in self.intents_data.get('intents', []):
            tag = intent.get('tag', '')
            patterns = intent.get('patterns', [])
            self.patterns[tag] = patterns
            
            keywords = set()
            for pattern in patterns:
                words = helpers.tokenize(pattern)
                keywords.update(words)
            self.intent_keywords[tag] = keywords
    
    def classify(self, message: str) -> Tuple[str, float]:
        """Classify message and return (intent, confidence)."""
        if not message or not message.strip():
            return ('unknown', 0.0)
        
        normalized = helpers.normalize_text(message)
        
        # Rule-based first
        rule_intent = self._rule_based_classify(normalized)
        if rule_intent:
            return (rule_intent, 0.95)
        
        # Keyword matching
        best_intent = 'unknown'
        best_score = 0.0
        
        message_words = set(helpers.tokenize(normalized))
        
        for intent, keywords in self.intent_keywords.items():
            if not keywords:
                continue
            overlap = message_words.intersection(keywords)
            if overlap:
                score = len(overlap) / len(keywords)
                if len(overlap) >= 2:
                    score = min(score * 1.5, 1.0)
                if score > best_score:
                    best_score = score
                    best_intent = intent
        
        if best_score >= settings.CONFIDENCE_THRESHOLD:
            return (best_intent, best_score)
        
        return ('unknown', best_score)
    
    def _rule_based_classify(self, message: str) -> Optional[str]:
        """High-precision rule-based classification."""
        
        # Order number pattern (highest priority)
        if helpers.extract_order_number(message):
            return 'order_number_provided'
        
        # Goodbye patterns - check before greeting
        goodbye_words = ['bye', 'goodbye', 'quit', 'exit', 'see you', 'see ya', 'take care', 'later']
        if any(word in message for word in goodbye_words):
            return 'goodbye'
        
        # Help pattern - check before greeting
        if message in ['help', 'what can you do', 'capabilities', 'menu', 'options']:
            return 'help'
        if message == 'help' or (len(message) < 10 and 'help' in message):
            return 'help'
        
        # Return policy patterns - check before greeting
        return_keywords = ['return', 'refund', 'money back', 'send back', 'exchange']
        if any(keyword in message for keyword in return_keywords):
            return 'return_policy'
        
        # Shipping patterns - check before greeting
        shipping_keywords = ['shipping', 'delivery', 'arrive', 'ship', 'how long']
        if any(keyword in message for keyword in shipping_keywords):
            return 'shipping_info'
        
        # Order status patterns - check before greeting
        order_keywords = ['order status', 'track', 'where is my', 'package', 'my order']
        if any(keyword in message for keyword in order_keywords):
            return 'order_status'
        
        # Payment patterns - check before greeting
        payment_keywords = ['payment', 'pay', 'momo', 'mobile money', 'card', 'transfer', 'how to pay', 'pay with']
        if any(keyword in message for keyword in payment_keywords):
            return 'payment_methods'
        
        # Contact support patterns - check before greeting
        contact_keywords = ['contact', 'support', 'customer service', 'phone', 'email', 'call you', 'speak to', 'human']
        if any(keyword in message for keyword in contact_keywords):
            return 'contact_support'
        
        # Product inquiry patterns - check before greeting
        product_keywords = ['product', 'products', 'catalog', 'what do you sell', 'what do you have', 'items', 'in stock']
        if any(keyword in message for keyword in product_keywords):
            return 'product_inquiry'
        
        # Thanks patterns - check before greeting
        thanks_keywords = ['thank', 'thanks', 'appreciate', 'grateful']
        if any(keyword in message for keyword in thanks_keywords):
            return 'thanks'
        
        # Greeting patterns - check LAST
        greeting_words = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'howdy', 'what\'s up']
        message_words = message.split()
        if len(message_words) <= 3:
            if any(word in message for word in greeting_words):
                return 'greeting'
        else:
            first_word = message_words[0].lower()
            if first_word in ['hello', 'hi', 'hey']:
                return 'greeting'
        
        return None
    
    def get_all_intents(self) -> list:
        """Get list of all available intent tags."""
        if not self.intents_data:
            return []
        
        intents = []
        for intent in self.intents_data.get('intents', []):
            tag = intent.get('tag', '')
            if tag:
                intents.append(tag)
        
        return intents
    
    def get_response(self, intent_tag: str) -> str:
        """Get random response for intent."""
        if not self.intents_data:
            return helpers.get_random_response(settings.FALLBACK_MESSAGES)
        
        for intent in self.intents_data.get('intents', []):
            if intent.get('tag') == intent_tag:
                responses = intent.get('responses', [])
                if responses:
                    return helpers.get_random_response(responses)
        
        return helpers.get_random_response(settings.FALLBACK_MESSAGES)
    
    """
CS305 - Intent Classifier
Author: Bismark Mankata
Date: January 2026
"""

import os
import sys
from typing import Tuple, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import settings
from src.utils import helpers


class IntentClassifier:
    """Classifies user messages into intents."""
    
    def __init__(self):
        self.intents_data = None
        self.patterns = {}
        self.intent_keywords = {}
        self.load_intents()
        self._build_pattern_index()
    
    def load_intents(self):
        """Load intents from JSON file."""
        self.intents_data = helpers.load_json_file(settings.INTENTS_FILE)
        if not self.intents_data:
            print(f"Warning: Could not load intents from {settings.INTENTS_FILE}")
            self._load_fallback_intents()
    
    def _load_fallback_intents(self):
        """Load fallback intents if JSON missing."""
        self.intents_data = {
            "intents": [
                {
                    "tag": "greeting",
                    "patterns": ["hello", "hi", "hey", "good morning"],
                    "responses": ["Hello! How can I help you?"]
                },
                {
                    "tag": "goodbye",
                    "patterns": ["bye", "goodbye", "see you", "quit"],
                    "responses": ["Goodbye! Have a great day!"]
                },
                {
                    "tag": "order_status",
                    "patterns": ["where is my order", "track order", "order status"],
                    "responses": ["Please provide your order number (ORD-12345)."]
                },
                {
                    "tag": "help",
                    "patterns": ["help", "what can you do"],
                    "responses": ["I can help with orders, products, and returns."]
                }
            ],
            "fallback_responses": ["I'm not sure I understand. Could you rephrase that?"]
        }
    
    def _build_pattern_index(self):
        """Build keyword index for fast matching."""
        if not self.intents_data:
            return
        
        for intent in self.intents_data.get('intents', []):
            tag = intent.get('tag', '')
            patterns = intent.get('patterns', [])
            self.patterns[tag] = patterns
            
            keywords = set()
            for pattern in patterns:
                words = helpers.tokenize(pattern)
                keywords.update(words)
            self.intent_keywords[tag] = keywords
    
    def classify(self, message: str) -> Tuple[str, float]:
        """Classify message and return (intent, confidence)."""
        if not message or not message.strip():
            return ('unknown', 0.0)
        
        normalized = helpers.normalize_text(message)
        
        # Rule-based first
        rule_intent = self._rule_based_classify(normalized)
        if rule_intent:
            return (rule_intent, 0.95)
        
        # Keyword matching
        best_intent = 'unknown'
        best_score = 0.0
        
        message_words = set(helpers.tokenize(normalized))
        
        for intent, keywords in self.intent_keywords.items():
            if not keywords:
                continue
            overlap = message_words.intersection(keywords)
            if overlap:
                score = len(overlap) / len(keywords)
                if len(overlap) >= 2:
                    score = min(score * 1.5, 1.0)
                if score > best_score:
                    best_score = score
                    best_intent = intent
        
        if best_score >= settings.CONFIDENCE_THRESHOLD:
            return (best_intent, best_score)
        
        return ('unknown', best_score)
    
    def _rule_based_classify(self, message: str) -> Optional[str]:
        """High-precision rule-based classification."""
        
        # Order number pattern (highest priority)
        if helpers.extract_order_number(message):
            return 'order_number_provided'
        
        # Goodbye patterns - check before greeting
        goodbye_words = ['bye', 'goodbye', 'quit', 'exit', 'see you', 'see ya', 'take care', 'later']
        if any(word in message for word in goodbye_words):
            return 'goodbye'
        
        # Help pattern - check before greeting
        if message in ['help', 'what can you do', 'capabilities', 'menu', 'options']:
            return 'help'
        if message == 'help' or (len(message) < 10 and 'help' in message):
            return 'help'
        
        # Return policy patterns - check before greeting
        return_keywords = ['return', 'refund', 'money back', 'send back', 'exchange']
        if any(keyword in message for keyword in return_keywords):
            return 'return_policy'
        
        # Shipping patterns - check before greeting
        shipping_keywords = ['shipping', 'delivery', 'arrive', 'ship', 'how long']
        if any(keyword in message for keyword in shipping_keywords):
            return 'shipping_info'
        
        # Order status patterns - check before greeting
        order_keywords = ['order status', 'track', 'where is my', 'package', 'my order']
        if any(keyword in message for keyword in order_keywords):
            return 'order_status'
        
        # Payment patterns - check before greeting
        payment_keywords = ['payment', 'pay', 'momo', 'mobile money', 'card', 'transfer', 'how to pay', 'pay with']
        if any(keyword in message for keyword in payment_keywords):
            return 'payment_methods'
        
        # Contact support patterns - check before greeting
        contact_keywords = ['contact', 'support', 'customer service', 'phone', 'email', 'call you', 'speak to', 'human']
        if any(keyword in message for keyword in contact_keywords):
            return 'contact_support'
        
        # Product inquiry patterns - check before greeting
        product_keywords = ['product', 'products', 'catalog', 'what do you sell', 'what do you have', 'items', 'in stock']
        if any(keyword in message for keyword in product_keywords):
            return 'product_inquiry'
        
        # Thanks patterns - check before greeting
        thanks_keywords = ['thank', 'thanks', 'appreciate', 'grateful']
        if any(keyword in message for keyword in thanks_keywords):
            return 'thanks'
        
        # Greeting patterns - check LAST
        greeting_words = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'howdy', 'what\'s up']
        message_words = message.split()
        if len(message_words) <= 3:
            if any(word in message for word in greeting_words):
                return 'greeting'
        else:
            first_word = message_words[0].lower()
            if first_word in ['hello', 'hi', 'hey']:
                return 'greeting'
        
        return None
    
    def get_all_intents(self) -> list:
        """Get list of all available intent tags."""
        if not self.intents_data:
            return []
        
        intents = []
        for intent in self.intents_data.get('intents', []):
            tag = intent.get('tag', '')
            if tag:
                intents.append(tag)
        
        return intents
    
    def get_response(self, intent_tag: str) -> str:
        """Get random response for intent."""
        if not self.intents_data:
            return helpers.get_random_response(settings.FALLBACK_MESSAGES)
        
        for intent in self.intents_data.get('intents', []):
            if intent.get('tag') == intent_tag:
                responses = intent.get('responses', [])
                if responses:
                    return helpers.get_random_response(responses)
        
        return helpers.get_random_response(settings.FALLBACK_MESSAGES)