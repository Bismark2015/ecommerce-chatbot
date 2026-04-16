"""
CS305 - FAQ Handler
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


class FAQHandler(BaseHandler):
    """Handles frequently asked questions."""
    
    def __init__(self):
        super().__init__()
        self.name = "faq_handler"
        self.priority = 5
        self.intents = [
            'return_policy', 'shipping_info', 'product_inquiry',
            'payment_methods', 'contact_support', 'thanks', 'help', 'goodbye'
        ]
        self.intents_data = None
        self.products_data = None
        self._load_data()
    
    def _load_data(self):
        self.intents_data = helpers.load_json_file(settings.INTENTS_FILE)
        self.products_data = helpers.load_json_file(settings.PRODUCTS_FILE)
    
    def can_handle(self, intent: str) -> bool:
        return intent in self.intents
    
    def handle(self, user_input: str, intent: str, context: Optional[Dict[str, Any]] = None) -> str:
        response = self._get_response_from_intents(intent)
        
        if not response:
            response = self._get_fallback_response(intent)
        
        if context and context.get('user_name') and intent not in ['thanks', 'goodbye']:
            if len(response) < 150:
                response = f"{response.split('.')[0]}, {context['user_name']}."
        
        return response
    
    def _get_response_from_intents(self, intent: str) -> str:
        if not self.intents_data:
            return ""
        for intent_data in self.intents_data.get('intents', []):
            if intent_data.get('tag') == intent:
                responses = intent_data.get('responses', [])
                if responses:
                    return helpers.get_random_response(responses)
        return ""
    
    def _get_fallback_response(self, intent: str) -> str:
        fallbacks = {
            'return_policy': f"We offer {settings.RETURN_POLICY['return_window_days']}-day returns. Items must be {settings.RETURN_POLICY['condition_required']}.",
            'shipping_info': f"Standard: {settings.SHIPPING['standard']['days']} (GHS {settings.SHIPPING['standard']['cost']}). Express: {settings.SHIPPING['express']['days']} (GHS {settings.SHIPPING['express']['cost']}). Free shipping over GHS {settings.SHIPPING['free_shipping_threshold']}!",
            'product_inquiry': "We offer electronics, clothing, and home goods. What are you looking for?",
            'payment_methods': "We accept Mobile Money, Visa, Mastercard, and bank transfer.",
            'contact_support': f"Contact us at {settings.SUPPORT_PHONE} or {settings.SUPPORT_EMAIL}. Hours: {settings.BUSINESS_HOURS}.",
            'thanks': random.choice(["You're welcome!", "My pleasure!", "Happy to help!"]),
            'help': "I can help with: Order tracking, Returns, Shipping, Products, Payments, and Support. What would you like to know?",
            'goodbye': random.choice(["Goodbye!", "Take care!", "See you next time!"])
        }
        return fallbacks.get(intent, "How can I help you?")