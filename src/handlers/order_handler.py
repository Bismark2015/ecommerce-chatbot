"""
CS305 - Order Handler
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


class OrderHandler(BaseHandler):
    """Handles order status and tracking requests."""
    
    def __init__(self):
        super().__init__()
        self.name = "order_handler"
        self.priority = 8
        self.intents = ['order_status', 'order_number_provided']
        self.orders_data = None
        
        self.ask_order_number_responses = [
            "I can help you track your order. Please provide your order number (format: ORD-12345).",
            "Let me check that for you. What's your order number?",
            "I'd be happy to check your order status. May I have your order number?",
            "Sure! Could you share your order number? It starts with 'ORD-' followed by 5 digits."
        ]
        
        self._load_orders()
    
    def _load_orders(self):
        self.orders_data = helpers.load_json_file(settings.ORDERS_FILE)
    
    def can_handle(self, intent: str) -> bool:
        return intent in self.intents
    
    def handle(self, user_input: str, intent: str, context: Optional[Dict[str, Any]] = None) -> str:
        order_number = helpers.extract_order_number(user_input)
        
        if order_number:
            order_info = self._find_order(order_number)
            if order_info:
                return self._format_order_response(order_info, context)
            else:
                return f"I couldn't find order {order_number}. Please check and try again."
        
        if context is not None:
            context['awaiting_order_number'] = True
        
        return random.choice(self.ask_order_number_responses)
    
    def _find_order(self, order_number: str) -> Optional[Dict[str, Any]]:
        if not self.orders_data:
            return None
        order_number = order_number.upper().strip()
        for order in self.orders_data.get('orders', []):
            if order.get('order_number', '').upper() == order_number:
                return order
        return None
    
    def _format_order_response(self, order: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> str:
        status = order.get('status', 'Unknown')
        order_num = order.get('order_number', 'Unknown')
        tracking = order.get('tracking_number')
        estimated = order.get('estimated_delivery', '')
        items = order.get('items', [])
        total = order.get('total', 0)
        order_date = order.get('order_date', '')
        
        lines = []
        
        if context and context.get('user_name'):
            lines.append(f"Thanks for your patience, {context['user_name']}!")
            lines.append("")
        
        lines.append(f"Order: {order_num}")
        lines.append(f"Date: {order_date}")
        lines.append(f"Status: {status}")
        
        if tracking:
            lines.append(f"Tracking: {tracking}")
        if estimated:
            lines.append(f"Estimated Delivery: {estimated}")
        
        lines.append(f"Items: {len(items)} item(s)")
        lines.append(f"Total: GHS {total:,.2f}")
        lines.append("")
        
        status_messages = {
            'Pending': "Your order is awaiting confirmation.",
            'Processing': "Your order is being prepared for shipping.",
            'Shipped': "Your order is on its way!",
            'Delivered': "Your order has been delivered.",
            'Cancelled': "This order was cancelled."
        }
        
        if status in status_messages:
            lines.append(status_messages[status])
        
        return "\n".join(lines)
    
    def get_confidence(self, user_input: str) -> float:
        if helpers.extract_order_number(user_input):
            return 0.95
        order_keywords = ['order', 'track', 'status', 'package', 'where is my']
        user_lower = user_input.lower()
        matches = sum(1 for kw in order_keywords if kw in user_lower)
        if matches >= 2:
            return 0.8
        elif matches >= 1:
            return 0.6
        return 0.0