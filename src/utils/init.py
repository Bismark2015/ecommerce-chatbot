"""
CS305 - Utilities Package
Author: Bismark Mankata
Date: January 2026

Utility functions for file operations, text processing, and helper methods.
"""

from .helpers import (
    # File operations
    load_json_file,
    save_json_file,
    
    # Text processing
    normalize_text,
    extract_order_number,
    extract_product_name,
    tokenize,
    
    # Response generation
    get_random_response,
    format_response,
    
    # Similarity and matching
    calculate_similarity,
    keyword_match,
    
    # Validation
    is_valid_email,
    is_valid_phone,
    
    # Formatting
    format_currency,
    format_order_status,
    
    # Debugging
    debug_log
)

__all__ = [
    # File operations
    'load_json_file',
    'save_json_file',
    
    # Text processing
    'normalize_text',
    'extract_order_number',
    'extract_product_name',
    'tokenize',
    
    # Response generation
    'get_random_response',
    'format_response',
    
    # Similarity and matching
    'calculate_similarity',
    'keyword_match',
    
    # Validation
    'is_valid_email',
    'is_valid_phone',
    
    # Formatting
    'format_currency',
    'format_order_status',
    
    # Debugging
    'debug_log'
]