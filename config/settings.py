"""
E-Commerce Chatbot Configuration
Author: Bismark Mankata
Date: January 2026
"""

# ============================================
# BOT IDENTITY CONFIGURATION
# ============================================

BOT_NAME = "ShopBot"
SHOP_NAME = "Bismark's Store"
VERSION = "1.0.0"

# ============================================
# PERSONALIZATION SETTINGS (Requirement #3)
# ============================================

# Whether to remember user's name during session
REMEMBER_USER_NAME = True

# Personalized greeting template
PERSONALIZED_GREETING = "Welcome back, {name}! How can I help you today?"
FIRST_TIME_GREETING = "Hello! I'm {bot_name} from {shop_name}. What's your name?"

# ============================================
# FILE PATHS
# ============================================

import os

# Get the absolute path to the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data file paths
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
INTENTS_FILE = os.path.join(DATA_DIR, "intents.json")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")

# ============================================
# CHATBOT BEHAVIOR SETTINGS
# ============================================

# Confidence threshold for intent matching (0.0 to 1.0)
CONFIDENCE_THRESHOLD = 0.3

# Maximum number of fallback attempts before suggesting help
MAX_FALLBACK_ATTEMPTS = 3

# ============================================
# ERROR MESSAGES (Requirement #2)
# ============================================

FALLBACK_MESSAGES = [
    "I'm not sure I understand. Could you rephrase that?",
    "I didn't quite catch that. Type 'help' to see what I can do.",
    "Sorry, I'm still learning. Can you try asking differently?",
    "I don't have an answer for that yet. Is there something else I can help with?"
]

ERROR_MESSAGES = {
    "file_not_found": "Error: Could not load {file_name}. Please check the file path.",
    "invalid_json": "Error: {file_name} contains invalid JSON format.",
    "order_not_found": "I couldn't find an order with number {order_number}. Please check and try again.",
    "product_not_found": "I couldn't find '{product_name}' in our catalog. Would you like to see our available products?"
}

# ============================================
# CHANNEL CONFIGURATION (Requirement #1)
# ============================================

# Currently supported channels: "console"
# Future: "web", "whatsapp", "messenger"
ACTIVE_CHANNEL = "console"

# ============================================
# DISPLAY SETTINGS
# ============================================

# Console display width for formatting
CONSOLE_WIDTH = 60

# Show debug information (set to False for production)
DEBUG_MODE = True

# ============================================
# BUSINESS INFORMATION
# ============================================

BUSINESS_HOURS = "Monday - Friday, 9:00 AM - 6:00 PM GMT"
SUPPORT_PHONE = "0546309080"
SUPPORT_EMAIL = "mccarthygoodnews@gmail.com"
WEBSITE = "https://github.com/Bismark2015/Luxury-Carpet.git"

# ============================================
# SHIPPING CONFIGURATION
# ============================================

SHIPPING = {
    "standard": {
        "days": "3-5 business days",
        "cost": 20.00,
        "currency": "GHS"
    },
    "express": {
        "days": "1-2 business days",
        "cost": 50.00,
        "currency": "GHS"
    },
    "free_shipping_threshold": 500.00
}

# ============================================
# RETURN POLICY CONFIGURATION
# ============================================

RETURN_POLICY = {
    "return_window_days": 30,
    "condition_required": "Unused, original packaging, tags attached",
    "refund_method": "Original payment method",
    "processing_time": "5-7 business days"
}

# ============================================
# UTILITY FUNCTION
# ============================================

def get_config_summary():
    """Returns a formatted summary of current configuration."""
    return f"""
========================================
  CS305 CHATBOT CONFIGURATION
========================================
Bot Name:      {BOT_NAME}
Shop Name:     {SHOP_NAME}
Version:       {VERSION}
Channel:       {ACTIVE_CHANNEL}
Debug Mode:    {DEBUG_MODE}

Data Files:
  Intents:     {os.path.basename(INTENTS_FILE)}
  Products:    {os.path.basename(PRODUCTS_FILE)}
  Orders:      {os.path.basename(ORDERS_FILE)}

Business Info:
  Phone:       {SUPPORT_PHONE}
  Email:       {SUPPORT_EMAIL}
  Hours:       {BUSINESS_HOURS}
========================================
"""

# ============================================
# VALIDATION (Runs when file is imported)
# ============================================

def validate_config():
    """Checks that all required files exist."""
    missing_files = []
    
    if not os.path.exists(INTENTS_FILE):
        missing_files.append("intents.json")
    if not os.path.exists(PRODUCTS_FILE):
        missing_files.append("products.json")
    if not os.path.exists(ORDERS_FILE):
        missing_files.append("orders.json")
    
    if missing_files:
        print(f"WARNING: Missing data files: {', '.join(missing_files)}")
        print(f"Expected location: {DATA_DIR}")
        return False
    return True

# Auto-validate on import
_CONFIG_VALID = validate_config()