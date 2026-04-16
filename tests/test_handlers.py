"""
CS305 - Handlers Tests
Author: Bismark Mankata
Date: January 2026

Unit tests for the chatbot handlers.
"""

import os
import sys
import unittest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.handlers import (
    GreetingHandler,
    OrderHandler,
    FAQHandler,
    FallbackHandler
)
from config import settings


class TestGreetingHandler(unittest.TestCase):
    """Test cases for GreetingHandler."""
    
    def setUp(self):
        self.handler = GreetingHandler()
    
    def test_can_handle_greeting(self):
        """Test that handler recognizes greeting intent."""
        self.assertTrue(self.handler.can_handle('greeting'))
        self.assertFalse(self.handler.can_handle('order_status'))
        self.assertFalse(self.handler.can_handle('unknown'))
    
    def test_basic_greeting(self):
        """Test basic greeting response."""
        response = self.handler.handle("hello", "greeting")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    
    def test_personalized_greeting(self):
        """Test personalized greeting with user name."""
        context = {'user_name': 'Bismark'}
        response = self.handler.handle("hello", "greeting", context)
        self.assertIn('Bismark', response)
    
    def test_name_capture(self):
        """Test name extraction from introduction."""
        test_cases = [
            ("my name is Bismark", "Bismark"),
            ("i am Kwame", "Kwame"),
            ("I'm Ama", "Ama"),
            ("call me Kofi", "Kofi")
        ]
        
        for message, expected_name in test_cases:
            with self.subTest(message=message):
                context = {}
                response = self.handler.handle(message, "greeting", context)
                self.assertIn(expected_name, response)
                self.assertEqual(context.get('user_name'), expected_name)
    
    def test_priority(self):
        """Test handler priority."""
        self.assertEqual(self.handler.get_priority(), 10)


class TestOrderHandler(unittest.TestCase):
    """Test cases for OrderHandler."""
    
    def setUp(self):
        self.handler = OrderHandler()
    
    def test_can_handle_order(self):
        """Test that handler recognizes order intents."""
        self.assertTrue(self.handler.can_handle('order_status'))
        self.assertTrue(self.handler.can_handle('order_number_provided'))
        self.assertFalse(self.handler.can_handle('greeting'))
    
    def test_ask_for_order_number(self):
        """Test prompt for order number."""
        response = self.handler.handle("track my order", "order_status")
        self.assertIsInstance(response, str)
        self.assertIn('order number', response.lower())
    
    def test_order_lookup_with_number(self):
        """Test order lookup with valid order number."""
        response = self.handler.handle("where is ORD-12345", "order_number_provided")
        self.assertIsInstance(response, str)
        self.assertIn('ORD-12345', response)
    
    def test_order_not_found(self):
        """Test order lookup with invalid order number."""
        response = self.handler.handle("where is ORD-99999", "order_number_provided")
        self.assertIsInstance(response, str)
        self.assertIn('couldn', response.lower())
    
    def test_priority(self):
        """Test handler priority."""
        self.assertEqual(self.handler.get_priority(), 8)


class TestFAQHandler(unittest.TestCase):
    """Test cases for FAQHandler."""
    
    def setUp(self):
        self.handler = FAQHandler()
    
    def test_can_handle_faq(self):
        """Test that handler recognizes FAQ intents."""
        faq_intents = ['return_policy', 'shipping_info', 'payment_methods', 
                       'contact_support', 'thanks', 'help', 'goodbye']
        
        for intent in faq_intents:
            with self.subTest(intent=intent):
                self.assertTrue(self.handler.can_handle(intent))
        
        self.assertFalse(self.handler.can_handle('greeting'))
        self.assertFalse(self.handler.can_handle('order_status'))
    
    def test_return_policy_response(self):
        """Test return policy response."""
        response = self.handler.handle("return policy", "return_policy")
        self.assertIsInstance(response, str)
        self.assertIn('day', response.lower())
    
    def test_shipping_info_response(self):
        """Test shipping info response."""
        response = self.handler.handle("shipping cost", "shipping_info")
        self.assertIsInstance(response, str)
        self.assertTrue('GHS' in response or 'shipping' in response.lower())
    
    def test_payment_methods_response(self):
        """Test payment methods response."""
        response = self.handler.handle("how to pay", "payment_methods")
        self.assertIsInstance(response, str)
    
    def test_help_response(self):
        """Test help response."""
        response = self.handler.handle("help", "help")
        self.assertIsInstance(response, str)
    
    def test_thanks_response(self):
        """Test thanks response."""
        response = self.handler.handle("thank you", "thanks")
        self.assertIsInstance(response, str)
    
    def test_priority(self):
        """Test handler priority."""
        self.assertEqual(self.handler.get_priority(), 5)


class TestFallbackHandler(unittest.TestCase):
    """Test cases for FallbackHandler."""
    
    def setUp(self):
        self.handler = FallbackHandler()
    
    def test_can_handle_anything(self):
        """Test that fallback handler can handle any intent."""
        self.assertTrue(self.handler.can_handle('unknown'))
        self.assertTrue(self.handler.can_handle('greeting'))
        self.assertTrue(self.handler.can_handle('any_intent'))
    
    def test_fallback_response(self):
        """Test fallback response."""
        response = self.handler.handle("asdfghjkl", "unknown")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    
    def test_progressive_help(self):
        """Test progressive help after multiple fallbacks."""
        context = {'session_id': 'test_session'}
        
        # First fallback
        response1 = self.handler.handle("blah", "unknown", context)
        self.assertIn('Tip:', response1)
        
        # Second fallback
        response2 = self.handler.handle("blah", "unknown", context)
        
        # Third fallback should trigger detailed help
        response3 = self.handler.handle("blah", "unknown", context)
        self.assertIn('I can help you with', response3)
    
    def test_reset_fallback_count(self):
        """Test resetting fallback count."""
        session_id = 'test_session'
        context = {'session_id': session_id}
        
        self.handler.handle("blah", "unknown", context)
        self.assertEqual(self.handler.get_fallback_count(session_id), 1)
        
        self.handler.reset_fallback_count(session_id)
        self.assertEqual(self.handler.get_fallback_count(session_id), 0)
    
    def test_priority(self):
        """Test handler priority."""
        self.assertEqual(self.handler.get_priority(), 0)


def run_tests():
    """Run all handler tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestGreetingHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestOrderHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestFAQHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestFallbackHandler))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("HANDLER TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✅ All handler tests passed!")
    else:
        print("\n❌ Some handler tests failed!")
        
        for failure in result.failures:
            print(f"\nFAILURE: {failure[0]}")
            print(failure[1][:500])
        
        for error in result.errors:
            print(f"\nERROR: {error[0]}")
            print(error[1][:500])
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)