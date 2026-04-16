"""
CS305 - Intent Classifier Tests
Author: Bismark Mankata
Date: January 2026

Unit tests for the IntentClassifier class.
"""

import os
import sys
import unittest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.nlp.intent_classifier import IntentClassifier
from config import settings


class TestIntentClassifier(unittest.TestCase):
    """Test cases for IntentClassifier."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        cls.classifier = IntentClassifier()
    
    def setUp(self):
        """Set up before each test."""
        self.classifier = TestIntentClassifier.classifier
    
    def test_greeting_intent(self):
        """Test greeting intent classification."""
        test_cases = [
            "hello",
            "hi there",
            "hey",
            "good morning",
            "good afternoon"
        ]
        
        for message in test_cases:
            with self.subTest(message=message):
                intent, confidence = self.classifier.classify(message)
                self.assertEqual(intent, 'greeting')
                self.assertGreaterEqual(confidence, 0.5)
    
    def test_goodbye_intent(self):
        """Test goodbye intent classification."""
        test_cases = [
            "bye",
            "goodbye",
            "see you",
            "quit",
            "exit"
        ]
        
        for message in test_cases:
            with self.subTest(message=message):
                intent, confidence = self.classifier.classify(message)
                self.assertEqual(intent, 'goodbye')
    
    def test_order_status_intent(self):
        """Test order status intent classification."""
        test_cases = [
            "where is my order",
            "track my package",
            "order status",
            "track order",
            "where is my package"
        ]
        
        for message in test_cases:
            with self.subTest(message=message):
                intent, confidence = self.classifier.classify(message)
                self.assertEqual(intent, 'order_status')
    
    def test_order_number_provided_intent(self):
        """Test order number detection."""
        test_cases = [
            "where is ORD-12345",
            "track ORD-67890",
            "order ORD-11111 status",
            "ORD-54321"
        ]
        
        for message in test_cases:
            with self.subTest(message=message):
                intent, confidence = self.classifier.classify(message)
                self.assertEqual(intent, 'order_number_provided')
                self.assertGreaterEqual(confidence, 0.9)
    
    def test_return_policy_intent(self):
        """Test return policy intent classification."""
        test_cases = [
            "what is your return policy",
            "how do I return an item",
            "refund policy",
            "money back",
            "can I return this"
        ]
        
        for message in test_cases:
            with self.subTest(message=message):
                intent, confidence = self.classifier.classify(message)
                self.assertEqual(intent, 'return_policy')
    
    def test_shipping_info_intent(self):
        """Test shipping info intent classification."""
        test_cases = [
            "shipping cost",
            "delivery time",
            "how long does shipping take",
            "shipping options",
            "when will it arrive"
        ]
        
        for message in test_cases:
            with self.subTest(message=message):
                intent, confidence = self.classifier.classify(message)
                self.assertEqual(intent, 'shipping_info')
    
    def test_product_inquiry_intent(self):
        """Test product inquiry intent classification."""
        test_cases = [
            "what products do you have",
            "tell me about your products",
            "product information",
            "catalog",
            "what do you sell"
        ]
        
        for message in test_cases:
            with self.subTest(message=message):
                intent, confidence = self.classifier.classify(message)
                self.assertEqual(intent, 'product_inquiry')
    
    def test_payment_methods_intent(self):
        """Test payment methods intent classification."""
        test_cases = [
            "how can I pay",
            "payment methods",
            "do you accept mobile money",
            "payment options",
            "momo payment"
        ]
        
        for message in test_cases:
            with self.subTest(message=message):
                intent, confidence = self.classifier.classify(message)
                self.assertEqual(intent, 'payment_methods')
    
    def test_help_intent(self):
        """Test help intent classification."""
        test_cases = [
            "help",
            "what can you do",
            "capabilities",
            "how do you work",
            "options"
        ]
        
        for message in test_cases:
            with self.subTest(message=message):
                intent, confidence = self.classifier.classify(message)
                self.assertEqual(intent, 'help')
    
    def test_thanks_intent(self):
        """Test thanks intent classification."""
        test_cases = [
            "thank you",
            "thanks",
            "appreciate it",
            "thank you so much"
        ]
        
        for message in test_cases:
            with self.subTest(message=message):
                intent, confidence = self.classifier.classify(message)
                self.assertEqual(intent, 'thanks')
    
    def test_contact_support_intent(self):
        """Test contact support intent classification."""
        test_cases = [
            "contact support",
            "customer service",
            "speak to human",
            "phone number",
            "email address"
        ]
        
        for message in test_cases:
            with self.subTest(message=message):
                intent, confidence = self.classifier.classify(message)
                self.assertEqual(intent, 'contact_support')
    
    def test_unknown_intent(self):
        """Test unknown intent classification."""
        test_cases = [
            "asdfghjkl",
            "xyz123",
            "blah blah blah",
            "random text here"
        ]
        
        for message in test_cases:
            with self.subTest(message=message):
                intent, confidence = self.classifier.classify(message)
                self.assertEqual(intent, 'unknown')
                self.assertLess(confidence, 0.5)
    
    def test_empty_message(self):
        """Test empty message handling."""
        intent, confidence = self.classifier.classify("")
        self.assertEqual(intent, 'unknown')
        self.assertEqual(confidence, 0.0)
        
        intent, confidence = self.classifier.classify("   ")
        self.assertEqual(intent, 'unknown')
        self.assertEqual(confidence, 0.0)
    
    def test_get_response(self):
        """Test getting response for an intent."""
        response = self.classifier.get_response('greeting')
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        
        # Test unknown intent
        response = self.classifier.get_response('nonexistent_intent')
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    
    def test_get_all_intents(self):
        """Test getting all available intents."""
        intents = self.classifier.get_all_intents()
        self.assertIsInstance(intents, list)
        self.assertIn('greeting', intents)
        self.assertIn('goodbye', intents)
        self.assertIn('help', intents)


def run_tests():
    """Run all tests and print results."""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIntentClassifier)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        
        for failure in result.failures:
            print(f"\nFAILURE: {failure[0]}")
            print(failure[1])
        
        for error in result.errors:
            print(f"\nERROR: {error[0]}")
            print(error[1])
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)