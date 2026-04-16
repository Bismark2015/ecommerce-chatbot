# CS305 E-Commerce Chatbot

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/Tests-37%20passed-brightgreen.svg)](./tests)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent e-commerce support chatbot built for CS305 Artificial Intelligence course at [Your University].

## 📋 Features

| Requirement | Implementation |
|-------------|----------------|
| **Right Communication Channel** | Console interface + Flask Web API + Frontend chat widget |
| **Perfect Error Messages** | Progressive fallback handler with helpful suggestions |
| **Personalized Communication** | Name capture and personalized greeting/responses |

## 🤖 Capabilities

- **Order Tracking**: Check order status with `ORD-12345` format
- **Product Inquiries**: Browse product catalog and get details
- **FAQ Support**: Shipping, returns, payment methods, contact info
- **Smart Fallback**: Progressive help for misunderstood queries
- **Session Management**: Remembers user context during conversation

##  Architecture

ecommerce-chatbot/
├── app.py # Flask Web API
├── main.py # Console interface
├── config/ # Bot configuration
├── data/ # JSON data files (intents, products, orders)
├── src/
│ ├── nlp/ # Intent classification & entity extraction
│ ├── handlers/ # Response handlers (greeting, order, FAQ, fallback)
│ ├── personalization/ # User context & session management
│ ├── channels/ # Console & web channels
│ └── utils/ # Helper functions
└── tests/ # Unit tests (37/37 passing)



##  Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Bismark2015/cs305-ecommerce-chatbot.git
cd cs305-ecommerce-chatbot

# Install dependencies
pip install -r requirements.txt
