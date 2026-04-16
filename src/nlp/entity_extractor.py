"""
CS305 - Entity Extractor
Author: Bismark Mankata
Date: January 2026
"""

import os
import sys
import re
from typing import Optional, Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import settings
from src.utils import helpers


class EntityExtractor:
    """Extracts entities from user messages."""
    
    def __init__(self):
        self.products_data = None
        self.product_names = []
        self._load_products()
    
    def _load_products(self):
        """Load product catalog."""
        self.products_data = helpers.load_json_file(settings.PRODUCTS_FILE)
        if self.products_data:
            for product in self.products_data.get('products', []):
                name = product.get('name', '')
                if name:
                    self.product_names.append(name.lower())
    
    def extract_order_number(self, text: str) -> Optional[str]:
        """Extract order number ORD-12345."""
        return helpers.extract_order_number(text)
    
    def extract_product_name(self, text: str) -> Optional[str]:
        """Extract product name from catalog."""
        text_lower = text.lower()
        for product_name in self.product_names:
            if product_name in text_lower:
                for product in self.products_data.get('products', []):
                    if product.get('name', '').lower() == product_name:
                        return product.get('name')
        return None
    
    def extract_quantity(self, text: str) -> Optional[int]:
        """Extract quantity number."""
        numbers = re.findall(r'\b\d+\b', text)
        if numbers:
            return int(numbers[0])
        return None
    
    def extract_phone_number(self, text: str) -> Optional[str]:
        """Extract Ghana phone number."""
        pattern = r'0[2-5]\d{8}'
        match = re.search(pattern, text)
        return match.group() if match else None
    
    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address."""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(pattern, text)
        return match.group() if match else None
    
    def extract_name(self, text: str) -> Optional[str]:
        """Extract person's name from introduction."""
        name_indicators = ['my name is', 'i am', "i'm", 'call me']
        text_lower = text.lower()
        
        for indicator in name_indicators:
            if indicator in text_lower:
                parts = text_lower.split(indicator)
                if len(parts) > 1:
                    name_part = parts[1].strip()
                    name_part = re.sub(r'[^\w\s]', '', name_part)
                    words = name_part.split()
                    if words:
                        return words[0].capitalize()
        return None
    
    def extract_all(self, text: str) -> Dict[str, Any]:
        """Extract all entities."""
        return {
            'order_number': self.extract_order_number(text),
            'product_name': self.extract_product_name(text),
            'quantity': self.extract_quantity(text),
            'phone_number': self.extract_phone_number(text),
            'email': self.extract_email(text),
            'name': self.extract_name(text)
        }