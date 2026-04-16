"""
CS305 - NLP Module
Author: Bismark Mankata
Date: January 2026

Natural Language Processing module for intent classification and entity extraction.
"""

from .intent_classifier import IntentClassifier
from .entity_extractor import EntityExtractor

__all__ = [
    'IntentClassifier',
    'EntityExtractor'
]