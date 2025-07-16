#!/usr/bin/env python3
"""
Simple test script for Fashion Guru Chatbot
Tests core functionality without requiring a full test framework
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot import FashionGuruChatbot
from fashion_engine import FashionEngine
from weather_service import WeatherService

def test_chatbot_basic_functionality():
    """Test basic chatbot functionality"""
    print("🧪 Testing Fashion Guru Chatbot...")
    
    chatbot = FashionGuruChatbot()
    
    # Test greeting
    response = chatbot.process_message("hello", "test_user")
    assert 'response' in response
    assert 'Fashion Guru' in response['response'] or 'fashion' in response['response'].lower()
    print("✅ Greeting test passed")
    
    # Test outfit request
    response = chatbot.process_message("what should I wear today?", "test_user")
    assert 'response' in response
    assert 'outfit' in response['response'].lower() or 'wear' in response['response'].lower()
    print("✅ Outfit request test passed")
    
    # Test weather-based outfit
    response = chatbot.process_message("what should I wear in cold weather?", "test_user", "London")
    assert 'response' in response
    print("✅ Weather-based outfit test passed")
    
    # Test shopping advice
    response = chatbot.process_message("I need shopping advice", "test_user")
    assert 'response' in response
    assert 'shopping' in response['response'].lower() or 'wardrobe' in response['response'].lower()
    print("✅ Shopping advice test passed")

def test_fashion_engine():
    """Test fashion engine functionality"""
    print("\n🧪 Testing Fashion Engine...")
    
    engine = FashionEngine()
    
    # Test outfit recommendation
    weather_category = {
        'temperature_category': 'mild',
        'condition_category': 'sunny',
        'temperature': 20,
        'condition': 'sunny'
    }
    
    recommendation = engine.get_outfit_recommendation(weather_category)
    assert 'outfit' in recommendation
    assert 'style_tip' in recommendation
    print("✅ Outfit recommendation test passed")
    
    # Test wardrobe analysis
    analysis = engine.get_wardrobe_analysis("test_user", ["jeans", "t-shirt", "sneakers"])
    assert 'wardrobe_size' in analysis
    assert analysis['wardrobe_size'] == 3
    print("✅ Wardrobe analysis test passed")
    
    # Test style advice
    style_advice = engine.get_style_advice("casual")
    assert 'style' in style_advice
    assert 'key_pieces' in style_advice
    print("✅ Style advice test passed")

def test_weather_service():
    """Test weather service functionality"""
    print("\n🧪 Testing Weather Service...")
    
    service = WeatherService()
    
    # Test weather data (will use mock data without API key)
    weather = service.get_weather("New York")
    assert 'temperature' in weather
    assert 'condition' in weather
    print("✅ Weather service test passed")
    
    # Test weather categorization
    category = service.get_weather_category(weather)
    assert 'temperature_category' in category
    assert 'condition_category' in category
    print("✅ Weather categorization test passed")

def run_all_tests():
    """Run all tests"""
    try:
        test_chatbot_basic_functionality()
        test_fashion_engine()
        test_weather_service()
        print("\n🎉 All tests passed! Fashion Guru Chatbot is working correctly.")
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)