"""
CS305 - Artificial Intelligence
Utility Helper Functions
Author: Bismark Mankata
Date: January 2026
"""

import json
import os
import random
import re
from typing import Dict, List, Any, Optional

# ============================================
# FILE OPERATIONS
# ============================================

def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Safely load a JSON file and return its contents.
    
    Args:
        file_path: Full path to the JSON file
        
    Returns:
        Dictionary containing JSON data, or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path} - {e}")
        return None
    except Exception as e:
        print(f"Unexpected error loading {file_path}: {e}")
        return None


def save_json_file(file_path: str, data: Dict[str, Any]) -> bool:
    """
    Save data to a JSON file.
    
    Args:
        file_path: Full path to save the JSON file
        data: Dictionary to save
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")
        return False


# ============================================
# TEXT PROCESSING
# ============================================

def normalize_text(text: str) -> str:
    """
    Convert text to lowercase and remove extra whitespace.
    
    Args:
        text: Input string
        
    Returns:
        Normalized string
    """
    if not text:
        return ""
    return " ".join(text.lower().strip().split())


def extract_order_number(text: str) -> Optional[str]:
    """
    Extract order number in format ORD-12345 from text.
    
    Args:
        text: User input string
        
    Returns:
        Order number if found, None otherwise
    """
    # Pattern: ORD- followed by 5 digits
    pattern = r'ORD-\d{5}'
    match = re.search(pattern, text.upper())
    if match:
        return match.group()
    return None


def extract_product_name(text: str, products: List[Dict]) -> Optional[str]:
    """
    Try to find a product name in user input.
    
    Args:
        text: User input string
        products: List of product dictionaries
        
    Returns:
        Product name if found, None otherwise
    """
    text_lower = text.lower()
    for product in products:
        product_name = product.get('name', '').lower()
        if product_name in text_lower:
            return product.get('name')
    return None


def tokenize(text: str) -> List[str]:
    """
    Split text into individual words.
    
    Args:
        text: Input string
        
    Returns:
        List of words
    """
    # Remove punctuation and split on whitespace
    cleaned = re.sub(r'[^\w\s]', '', text.lower())
    return cleaned.split()


# ============================================
# RESPONSE GENERATION
# ============================================

def get_random_response(responses: List[str]) -> str:
    """
    Select a random response from a list.
    
    Args:
        responses: List of possible response strings
        
    Returns:
        A single random response
    """
    if not responses:
        return "I'm not sure how to respond to that."
    return random.choice(responses)


def format_response(template: str, **kwargs) -> str:
    """
    Fill in a template string with provided values.
    
    Example:
        format_response("Hello {name}", name="Bismark") -> "Hello Bismark"
    
    Args:
        template: String with {placeholders}
        **kwargs: Values to substitute
        
    Returns:
        Formatted string
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        return template.replace("{" + str(e).strip("'") + "}", "[Unknown]")
    except Exception:
        return template


# ============================================
# SIMILARITY AND MATCHING
# ============================================

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate simple word overlap similarity between two texts.
    
    Args:
        text1: First string
        text2: Second string
        
    Returns:
        Similarity score between 0.0 and 1.0
    """
    words1 = set(tokenize(text1))
    words2 = set(tokenize(text2))
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)


def keyword_match(text: str, keywords: List[str], min_matches: int = 1) -> bool:
    """
    Check if text contains at least min_matches keywords.
    
    Args:
        text: Input string to check
        keywords: List of keywords to look for
        min_matches: Minimum number of keywords required
        
    Returns:
        True if enough keywords match, False otherwise
    """
    text_lower = text.lower()
    matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
    return matches >= min_matches


# ============================================
# VALIDATION
# ============================================

def is_valid_email(email: str) -> bool:
    """Check if string is a valid email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str) -> bool:
    """Check if string is a valid Ghana phone number format."""
    # Ghana numbers: 02X, 05X, 02X XXX XXXX
    pattern = r'^0[2-5]\d{8}$'
    cleaned = re.sub(r'[\s-]', '', phone)
    return bool(re.match(pattern, cleaned))


# ============================================
# FORMATTING
# ============================================

def format_currency(amount: float, currency: str = "GHS") -> str:
    """Format a number as currency."""
    return f"{currency} {amount:,.2f}"


def format_order_status(order: Dict) -> str:
    """
    Format an order dictionary into a readable message.
    
    Args:
        order: Order dictionary from orders.json
        
    Returns:
        Formatted status message
    """
    status_messages = {
        "Pending": "Your order is pending confirmation.",
        "Processing": "Your order is being processed and packed.",
        "Shipped": f"Your order has been shipped! Tracking number: {order.get('tracking_number', 'Pending')}",
        "Delivered": "Your order has been delivered.",
        "Cancelled": "Your order was cancelled."
    }
    
    status = order.get('status', 'Unknown')
    message = status_messages.get(status, f"Status: {status}")
    
    if order.get('estimated_delivery'):
        message += f" Estimated delivery: {order['estimated_delivery']}"
    
    return message


# ============================================
# DEBUGGING
# ============================================

def debug_log(message: str, debug_mode: bool = False):
    """Print debug message if debug mode is enabled."""
    if debug_mode:
        print(f"[DEBUG] {message}")