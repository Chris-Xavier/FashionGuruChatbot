import re
import random
from typing import Dict, List, Tuple
from weather_service import WeatherService
from fashion_engine import FashionEngine

class FashionGuruChatbot:
    def __init__(self):
        self.weather_service = WeatherService()
        self.fashion_engine = FashionEngine()
        self.conversation_state = {}
        self.user_sessions = {}
        
        # Intent patterns for natural language understanding
        self.intent_patterns = {
            'greeting': [
                r'\b(hi|hello|hey|greetings)\b',
                r'\b(good\s+(morning|afternoon|evening))\b'
            ],
            'outfit_request': [
                r'\b(outfit|what.*wear|dress|clothing)\b',
                r'\b(recommend|suggest|advice).*\b(outfit|clothes|wear)\b',
                r'\b(help.*choose|pick.*outfit)\b'
            ],
            'weather_outfit': [
                r'\b(weather|temperature|rain|snow|hot|cold)\b.*\b(outfit|wear|dress)\b',
                r'\b(outfit|wear).*\b(weather|temperature|rain|snow|hot|cold)\b'
            ],
            'shopping_advice': [
                r'\b(buy|shop|purchase|need)\b.*\b(clothes|clothing|outfit)\b',
                r'\b(wardrobe|closet).*\b(buy|shop|need|add)\b',
                r'\b(shopping|buying).*\b(advice|help|suggest)\b'
            ],
            'style_advice': [
                r'\b(style|fashion|look)\b.*\b(advice|help|tips)\b',
                r'\b(how.*style|styling tips)\b'
            ],
            'wardrobe_analysis': [
                r'\b(analyze|check|review).*\b(wardrobe|closet)\b',
                r'\b(wardrobe|closet).*\b(analyze|check|review)\b'
            ],
            'goodbye': [
                r'\b(bye|goodbye|see you|thanks|thank you)\b',
                r'\b(that.*(all|enough)|done|finished)\b'
            ]
        }
        
        # Context keywords
        self.context_keywords = {
            'time': {
                'morning': ['morning', 'breakfast', 'am', 'early'],
                'afternoon': ['afternoon', 'lunch', 'pm', 'work'],
                'evening': ['evening', 'dinner', 'night', 'date']
            },
            'occasion': {
                'work': ['work', 'office', 'meeting', 'professional', 'business'],
                'casual': ['casual', 'everyday', 'relaxed', 'comfortable'],
                'formal': ['formal', 'fancy', 'elegant', 'dressy', 'party'],
                'date': ['date', 'romantic', 'dinner', 'special'],
                'workout': ['gym', 'exercise', 'workout', 'athletic', 'sports']
            },
            'weather_mentions': {
                'hot': ['hot', 'warm', 'sunny', 'summer'],
                'cold': ['cold', 'chilly', 'winter', 'freezing'],
                'rainy': ['rain', 'rainy', 'wet', 'umbrella'],
                'snowy': ['snow', 'snowy', 'blizzard']
            }
        }
    
    def process_message(self, message: str, user_id: str = 'default', location: str = None) -> Dict:
        """Process user message and return appropriate response"""
        message = message.lower().strip()
        
        # Initialize user session if needed
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                'wardrobe': [],
                'preferences': {},
                'location': location or 'New York'
            }
        
        # Update location if provided
        if location:
            self.user_sessions[user_id]['location'] = location
        
        # Detect intent
        intent = self._detect_intent(message)
        
        # Extract context
        context = self._extract_context(message)
        
        # Generate response based on intent
        if intent == 'greeting':
            return self._handle_greeting()
        elif intent == 'outfit_request':
            return self._handle_outfit_request(context, user_id)
        elif intent == 'weather_outfit':
            return self._handle_weather_outfit_request(context, user_id)
        elif intent == 'shopping_advice':
            return self._handle_shopping_advice(context, user_id)
        elif intent == 'style_advice':
            return self._handle_style_advice(context, user_id)
        elif intent == 'wardrobe_analysis':
            return self._handle_wardrobe_analysis(message, user_id)
        elif intent == 'goodbye':
            return self._handle_goodbye()
        else:
            return self._handle_general_fashion_help(message, user_id)
    
    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    return intent
        return 'unknown'
    
    def _extract_context(self, message: str) -> Dict:
        """Extract context information from message"""
        context = {
            'time_of_day': 'day',
            'occasion': 'casual',
            'weather_mentioned': None,
            'location_mentioned': None
        }
        
        # Extract time context
        for time_period, keywords in self.context_keywords['time'].items():
            if any(keyword in message for keyword in keywords):
                context['time_of_day'] = time_period
                break
        
        # Extract occasion context
        for occasion, keywords in self.context_keywords['occasion'].items():
            if any(keyword in message for keyword in keywords):
                context['occasion'] = occasion
                break
        
        # Extract weather mentions
        for weather_type, keywords in self.context_keywords['weather_mentions'].items():
            if any(keyword in message for keyword in keywords):
                context['weather_mentioned'] = weather_type
                break
        
        # Extract location mentions (simple city detection)
        city_pattern = r'\bin\s+([A-Z][a-zA-Z\s]{2,20})\b'
        city_match = re.search(city_pattern, message)
        if city_match:
            context['location_mentioned'] = city_match.group(1).strip()
        
        return context
    
    def _handle_greeting(self) -> Dict:
        """Handle greeting messages"""
        greetings = [
            "Hello! I'm your Fashion Guru! 👗 I'm here to help you look amazing every day!",
            "Hey there! Ready to elevate your style? I can help with outfits, shopping advice, and more!",
            "Hi! Welcome to your personal fashion assistant! Let's make you look fabulous!",
            "Hello! I'm excited to help you with all your fashion needs today!"
        ]
        
        tips = [
            "I can help you choose outfits based on weather and occasion.",
            "I can analyze your wardrobe and suggest what to buy next.",
            "I can give you style advice for any look you're going for.",
            "Just tell me what you need help with!"
        ]
        
        return {
            'response': random.choice(greetings),
            'suggestions': [
                "What should I wear today?",
                "Help me choose an outfit for work",
                "What should I buy for my wardrobe?",
                "Give me some style advice"
            ],
            'tip': random.choice(tips)
        }
    
    def _handle_outfit_request(self, context: Dict, user_id: str) -> Dict:
        """Handle general outfit requests"""
        location = self.user_sessions[user_id]['location']
        
        # Get weather data
        weather_data = self.weather_service.get_weather(location)
        weather_category = self.weather_service.get_weather_category(weather_data)
        
        # Get outfit recommendation
        recommendation = self.fashion_engine.get_outfit_recommendation(
            weather_category, 
            context['time_of_day'], 
            context['occasion'],
            user_id
        )
        
        # Format response
        outfit_text = self._format_outfit_response(recommendation)
        weather_text = f"Based on the weather in {location} ({weather_data['temperature']}°C, {weather_data['condition']})"
        
        return {
            'response': f"{outfit_text}\n\n{weather_text}",
            'outfit_details': recommendation,
            'weather_info': weather_data,
            'suggestions': [
                "Can you suggest different colors?",
                "What accessories would work?",
                "Any style tips for this outfit?"
            ]
        }
    
    def _handle_weather_outfit_request(self, context: Dict, user_id: str) -> Dict:
        """Handle weather-specific outfit requests"""
        location = context.get('location_mentioned') or self.user_sessions[user_id]['location']
        
        if context['weather_mentioned']:
            # Use mentioned weather condition
            mock_weather = {
                'hot': {'temperature': 30, 'condition': 'sunny'},
                'cold': {'temperature': 5, 'condition': 'cloudy'},
                'rainy': {'temperature': 18, 'condition': 'rainy'},
                'snowy': {'temperature': -2, 'condition': 'snowy'}
            }
            weather_data = mock_weather.get(context['weather_mentioned'], 
                                          self.weather_service.get_weather(location))
            weather_category = self.weather_service.get_weather_category(weather_data)
        else:
            # Get actual weather
            weather_data = self.weather_service.get_weather(location)
            weather_category = self.weather_service.get_weather_category(weather_data)
        
        recommendation = self.fashion_engine.get_outfit_recommendation(
            weather_category, 
            context['time_of_day'], 
            context['occasion'],
            user_id
        )
        
        outfit_text = self._format_outfit_response(recommendation)
        
        return {
            'response': f"{outfit_text}\n\n🌡️ Perfect for {weather_data['temperature']}°C and {weather_data['condition']} weather!",
            'outfit_details': recommendation,
            'weather_info': weather_data,
            'suggestions': [
                "What if the weather changes?",
                "Any layering tips?",
                "What about accessories for this weather?"
            ]
        }
    
    def _handle_shopping_advice(self, context: Dict, user_id: str) -> Dict:
        """Handle shopping and wardrobe advice requests"""
        analysis = self.fashion_engine.get_wardrobe_analysis(user_id)
        
        response_parts = [
            f"🛍️ **Shopping Analysis:**",
            f"• Wardrobe strength: {analysis['wardrobe_strength']}",
            f"• Shopping priority: {analysis['shopping_priority']}"
        ]
        
        if analysis['missing_essentials']:
            response_parts.append(f"• **Essential items to consider:** {', '.join(analysis['missing_essentials'][:3])}")
        
        if analysis['seasonal_suggestions']:
            response_parts.append(f"• **Seasonal additions:** {', '.join(analysis['seasonal_suggestions'][:3])}")
        
        response_parts.append("\n💡 **Shopping tip:** Start with versatile basics that mix and match easily!")
        
        return {
            'response': '\n'.join(response_parts),
            'analysis': analysis,
            'suggestions': [
                "Tell me about my wardrobe",
                "What colors should I buy?",
                "Help me plan a shopping budget"
            ]
        }
    
    def _handle_style_advice(self, context: Dict, user_id: str) -> Dict:
        """Handle style advice requests"""
        # Extract style preference from context or use default
        style_preference = context.get('style_mentioned', 'versatile')
        
        style_advice = self.fashion_engine.get_style_advice(style_preference)
        
        response_parts = [
            f"✨ **{style_advice['style']} Style Guide:**",
            f"• **Key combinations:** {', '.join(style_advice['combinations'][:2])}",
            f"• **Essential pieces:** {', '.join(style_advice['key_pieces'][:3])}",
            f"• **Style inspiration:** {style_advice['inspiration']}"
        ]
        
        return {
            'response': '\n'.join(response_parts),
            'style_details': style_advice,
            'suggestions': [
                "Show me outfit combinations",
                "What colors work for this style?",
                "Help me shop for this style"
            ]
        }
    
    def _handle_wardrobe_analysis(self, message: str, user_id: str) -> Dict:
        """Handle wardrobe analysis requests"""
        # Try to extract wardrobe items from message
        wardrobe_items = self._extract_wardrobe_items(message)
        
        if wardrobe_items:
            analysis = self.fashion_engine.get_wardrobe_analysis(user_id, wardrobe_items)
            response = f"👔 **Wardrobe Analysis Complete!**\n\nI've analyzed your {len(wardrobe_items)} items. {analysis['wardrobe_strength']}\n\n"
            
            if analysis['missing_essentials']:
                response += f"**Consider adding:** {', '.join(analysis['missing_essentials'][:3])}\n\n"
            
            response += f"**Shopping priority:** {analysis['shopping_priority']}"
        else:
            response = ("📝 **To analyze your wardrobe, tell me what you have!**\n\n"
                       "For example: 'I have 3 jeans, 5 t-shirts, 2 blazers, sneakers, and boots'\n\n"
                       "Or just start listing: 'jeans, white shirt, black dress...'")
        
        return {
            'response': response,
            'suggestions': [
                "I have jeans, t-shirts, and sneakers",
                "What should I buy next?",
                "Help me organize my closet"
            ]
        }
    
    def _handle_goodbye(self) -> Dict:
        """Handle goodbye messages"""
        goodbyes = [
            "You're going to look amazing! Have a fabulous day! ✨",
            "Thanks for chatting! Remember, confidence is your best accessory! 💫",
            "Goodbye! Can't wait to help you style more outfits soon! 👗",
            "See you later! Go out there and rock your style! 🌟"
        ]
        
        return {
            'response': random.choice(goodbyes),
            'suggestions': []
        }
    
    def _handle_general_fashion_help(self, message: str, user_id: str) -> Dict:
        """Handle general fashion-related queries"""
        helpful_responses = [
            "I'd love to help with that! Can you tell me more about what you're looking for?",
            "That sounds like a great fashion question! Could you give me a bit more detail?",
            "I'm here to help! Are you looking for outfit ideas, shopping advice, or style tips?",
            "Let me help you with that! What specifically would you like to know about fashion?"
        ]
        
        return {
            'response': random.choice(helpful_responses),
            'suggestions': [
                "Help me choose an outfit",
                "What should I wear to work?",
                "I need shopping advice",
                "Give me style tips"
            ]
        }
    
    def _format_outfit_response(self, recommendation: Dict) -> str:
        """Format outfit recommendation into readable text"""
        outfit = recommendation['outfit']
        
        response_parts = ["👔 **Perfect Outfit Recommendation:**"]
        
        if 'tops' in outfit:
            response_parts.append(f"• **Top:** {outfit['tops'].title()}")
        if 'bottoms' in outfit:
            response_parts.append(f"• **Bottom:** {outfit['bottoms'].title()}")
        if 'shoes' in outfit:
            response_parts.append(f"• **Shoes:** {outfit['shoes'].title()}")
        if 'accessories' in outfit:
            response_parts.append(f"• **Accessories:** {outfit['accessories'].title()}")
        if 'weather_extras' in outfit:
            response_parts.append(f"• **For the weather:** {', '.join(outfit['weather_extras']).title()}")
        
        response_parts.extend([
            f"\n🎨 **Color suggestion:** {recommendation['color_suggestion']}",
            f"💡 **Style tip:** {recommendation['style_tip']}"
        ])
        
        return '\n'.join(response_parts)
    
    def _extract_wardrobe_items(self, message: str) -> List[str]:
        """Extract wardrobe items from user message"""
        # Simple extraction - look for clothing-related words
        clothing_items = []
        
        # Common clothing terms
        clothing_terms = [
            'jeans', 'pants', 'trousers', 'shorts', 'skirt', 'dress',
            't-shirt', 'shirt', 'blouse', 'sweater', 'hoodie', 'jacket', 'coat', 'blazer',
            'shoes', 'boots', 'sneakers', 'sandals', 'heels', 'flats',
            'belt', 'watch', 'bag', 'purse', 'scarf', 'hat', 'gloves'
        ]
        
        # Extract items mentioned with numbers
        number_pattern = r'(\d+)\s+([a-zA-Z\s]+?)(?=[,\.\s]|$)'
        matches = re.findall(number_pattern, message.lower())
        
        for count, item in matches:
            for term in clothing_terms:
                if term in item:
                    for _ in range(int(count)):
                        clothing_items.append(term)
                    break
        
        # Extract items mentioned without numbers
        for term in clothing_terms:
            if term in message.lower() and term not in clothing_items:
                clothing_items.append(term)
        
        return clothing_items