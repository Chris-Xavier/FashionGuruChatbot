import random
from typing import Dict, List, Tuple

class FashionEngine:
    def __init__(self):
        self.wardrobe_db = {}  # User wardrobes stored here (in real app, use database)
        self.outfit_rules = self._load_outfit_rules()
        self.shopping_suggestions = self._load_shopping_suggestions()
        self.style_combinations = self._load_style_combinations()
    
    def _load_outfit_rules(self) -> Dict:
        """Load outfit recommendation rules based on weather and occasion"""
        return {
            'very_cold': {
                'tops': ['heavy coat', 'wool sweater', 'thermal underwear', 'scarf'],
                'bottoms': ['thick jeans', 'thermal leggings', 'wool pants'],
                'shoes': ['insulated boots', 'warm boots', 'winter shoes'],
                'accessories': ['warm hat', 'gloves', 'thick scarf', 'thermal socks']
            },
            'cold': {
                'tops': ['jacket', 'sweater', 'cardigan', 'hoodie', 'light scarf'],
                'bottoms': ['jeans', 'thick leggings', 'corduroy pants'],
                'shoes': ['boots', 'closed-toe shoes', 'sneakers'],
                'accessories': ['light scarf', 'beanie', 'light gloves']
            },
            'mild': {
                'tops': ['light sweater', 'long sleeve shirt', 'blouse', 'light cardigan'],
                'bottoms': ['jeans', 'chinos', 'leggings', 'midi skirt'],
                'shoes': ['sneakers', 'flats', 'ankle boots', 'loafers'],
                'accessories': ['light jacket (optional)', 'crossbody bag']
            },
            'warm': {
                'tops': ['t-shirt', 'tank top', 'light blouse', 'short sleeve shirt'],
                'bottoms': ['shorts', 'light pants', 'skirt', 'capris'],
                'shoes': ['sandals', 'canvas shoes', 'light sneakers'],
                'accessories': ['sunglasses', 'hat', 'light bag']
            },
            'hot': {
                'tops': ['tank top', 'light t-shirt', 'crop top', 'sleeveless blouse'],
                'bottoms': ['shorts', 'light skirt', 'linen pants', 'short dress'],
                'shoes': ['sandals', 'flip-flops', 'breathable sneakers'],
                'accessories': ['sunglasses', 'sun hat', 'light scarf (for AC)']
            },
            'rainy': {
                'additional': ['umbrella', 'raincoat', 'waterproof shoes', 'rain boots']
            },
            'snowy': {
                'additional': ['snow boots', 'waterproof jacket', 'extra warm layers']
            }
        }
    
    def _load_shopping_suggestions(self) -> Dict:
        """Load shopping suggestions based on wardrobe gaps"""
        return {
            'essentials': {
                'tops': ['white button-down shirt', 'black t-shirt', 'navy sweater', 'versatile blazer'],
                'bottoms': ['dark jeans', 'black trousers', 'neutral skirt'],
                'shoes': ['black dress shoes', 'white sneakers', 'comfortable boots'],
                'accessories': ['watch', 'neutral belt', 'classic bag']
            },
            'seasonal': {
                'spring': ['light cardigan', 'floral dress', 'light jacket', 'comfortable flats'],
                'summer': ['sundress', 'linen shirt', 'sandals', 'swimwear'],
                'fall': ['warm sweater', 'ankle boots', 'scarf', 'layering pieces'],
                'winter': ['heavy coat', 'warm boots', 'gloves', 'thermal wear']
            },
            'occasion': {
                'work': ['professional blazer', 'dress pants', 'blouses', 'dress shoes'],
                'casual': ['comfortable jeans', 'casual t-shirts', 'sneakers', 'hoodies'],
                'formal': ['cocktail dress', 'suit', 'dress shoes', 'elegant accessories'],
                'workout': ['athletic wear', 'sports bra', 'workout shoes', 'gym bag']
            }
        }
    
    def _load_style_combinations(self) -> Dict:
        """Load style combination suggestions"""
        return {
            'casual_chic': ['jeans + blazer + sneakers', 'midi dress + denim jacket + flats'],
            'professional': ['trousers + blouse + blazer', 'pencil skirt + button-down + pumps'],
            'bohemian': ['flowy dress + ankle boots + layered jewelry', 'wide-leg pants + crop top + kimono'],
            'minimalist': ['black pants + white top + simple accessories', 'neutral dress + clean-line coat'],
            'sporty': ['leggings + oversized sweater + sneakers', 'joggers + crop top + bomber jacket']
        }
    
    def get_outfit_recommendation(self, weather_category: Dict, time_of_day: str = 'day', 
                                occasion: str = 'casual', user_id: str = None) -> Dict:
        """Generate outfit recommendation based on weather, time, and occasion"""
        temp_category = weather_category['temperature_category']
        condition_category = weather_category['condition_category']
        
        # Get base outfit for temperature
        base_outfit = self.outfit_rules.get(temp_category, self.outfit_rules['mild'])
        
        # Add weather-specific items
        additional_items = []
        if condition_category in ['rainy', 'snowy']:
            additional_items.extend(self.outfit_rules.get(condition_category, {}).get('additional', []))
        
        # Adjust for time of day
        if time_of_day == 'evening':
            # Evening adjustments
            if 't-shirt' in base_outfit['tops']:
                base_outfit['tops'] = [item for item in base_outfit['tops'] if item != 't-shirt']
                base_outfit['tops'].extend(['blouse', 'nice shirt'])
        
        # Adjust for occasion
        if occasion == 'work':
            professional_items = self.shopping_suggestions['occasion']['work']
            # Replace casual items with professional ones
            base_outfit['tops'] = [item for item in base_outfit['tops'] if 't-shirt' not in item and 'tank top' not in item]
            base_outfit['tops'].extend(['blouse', 'button-down shirt'])
        
        # Select random items from each category
        selected_outfit = {}
        for category, items in base_outfit.items():
            if items:
                selected_outfit[category] = random.choice(items)
        
        # Add weather-specific items
        if additional_items:
            selected_outfit['weather_extras'] = random.sample(additional_items, min(2, len(additional_items)))
        
        return {
            'outfit': selected_outfit,
            'weather_info': f"For {weather_category['temperature']}°C and {weather_category['condition']} weather",
            'style_tip': self._get_style_tip(selected_outfit),
            'color_suggestion': self._get_color_suggestion(weather_category)
        }
    
    def _get_style_tip(self, outfit: Dict) -> str:
        """Generate a style tip based on the outfit"""
        tips = [
            "Layer your pieces for easy adjustment throughout the day.",
            "Choose one statement piece and keep the rest simple.",
            "Make sure your shoes are comfortable if you'll be walking a lot.",
            "Add a pop of color with accessories to brighten your look.",
            "Consider the fit - well-fitted clothes always look better.",
            "Don't forget to check yourself in the mirror before leaving!",
            "Confidence is your best accessory - wear it with pride!"
        ]
        return random.choice(tips)
    
    def _get_color_suggestion(self, weather_category: Dict) -> str:
        """Suggest colors based on weather and season"""
        temp = weather_category['temperature']
        condition = weather_category['condition']
        
        if temp > 25:  # Hot weather
            return "Light colors like white, pastels, and soft blues to stay cool"
        elif temp < 10:  # Cold weather
            return "Darker colors like navy, black, and deep jewel tones for warmth"
        elif 'rain' in condition:
            return "Darker colors that won't show water spots as much"
        elif 'sunny' in condition:
            return "Bright, cheerful colors to match the sunny weather"
        else:
            return "Neutral colors that work well in any weather"
    
    def get_wardrobe_analysis(self, user_id: str, wardrobe_items: List[str] = None) -> Dict:
        """Analyze user's wardrobe and suggest shopping items"""
        if wardrobe_items:
            self.wardrobe_db[user_id] = wardrobe_items
        
        current_wardrobe = self.wardrobe_db.get(user_id, [])
        
        # Analyze what's missing from essentials
        missing_essentials = []
        for category, items in self.shopping_suggestions['essentials'].items():
            for item in items:
                if not any(wardrobe_item.lower() in item.lower() for wardrobe_item in current_wardrobe):
                    missing_essentials.append(item)
        
        # Get seasonal suggestions
        seasonal_suggestions = self.shopping_suggestions['seasonal']['spring']  # Default to spring
        
        return {
            'wardrobe_size': len(current_wardrobe),
            'missing_essentials': missing_essentials[:5],  # Top 5 missing items
            'seasonal_suggestions': seasonal_suggestions[:3],  # Top 3 seasonal items
            'wardrobe_strength': self._calculate_wardrobe_strength(current_wardrobe),
            'shopping_priority': self._get_shopping_priority(missing_essentials)
        }
    
    def _calculate_wardrobe_strength(self, wardrobe: List[str]) -> str:
        """Calculate how complete the wardrobe is"""
        essential_categories = ['shirt', 'pants', 'shoes', 'jacket']
        covered_categories = sum(1 for category in essential_categories 
                               if any(category in item.lower() for item in wardrobe))
        
        if covered_categories >= 3:
            return "Strong - You have most essentials covered!"
        elif covered_categories >= 2:
            return "Good - You have some key pieces, but could use more basics."
        else:
            return "Needs work - Consider building your wardrobe with essential basics."
    
    def _get_shopping_priority(self, missing_items: List[str]) -> str:
        """Determine shopping priority based on missing items"""
        if not missing_items:
            return "Low - Your wardrobe seems well-stocked!"
        elif len(missing_items) > 8:
            return "High - Focus on building your essential wardrobe."
        else:
            return "Medium - A few key pieces would complete your wardrobe."
    
    def get_style_advice(self, style_preference: str) -> Dict:
        """Get advice for specific style preferences"""
        style_lower = style_preference.lower()
        
        for style, combinations in self.style_combinations.items():
            if style in style_lower or any(word in style_lower for word in style.split('_')):
                return {
                    'style': style.replace('_', ' ').title(),
                    'combinations': combinations,
                    'key_pieces': self._get_key_pieces_for_style(style),
                    'inspiration': f"For {style.replace('_', ' ')} style, focus on {self._get_style_focus(style)}"
                }
        
        # Default advice
        return {
            'style': 'Versatile Classic',
            'combinations': ['neutral colors + classic cuts', 'mix textures for interest'],
            'key_pieces': ['well-fitted jeans', 'white button-down', 'classic blazer'],
            'inspiration': "Build a timeless wardrobe with versatile pieces that mix and match easily."
        }
    
    def _get_key_pieces_for_style(self, style: str) -> List[str]:
        """Get key pieces for specific styles"""
        style_pieces = {
            'casual_chic': ['blazer', 'dark jeans', 'white sneakers', 'simple jewelry'],
            'professional': ['tailored pants', 'blouses', 'blazer', 'dress shoes'],
            'bohemian': ['flowy dresses', 'ankle boots', 'layered jewelry', 'kimono'],
            'minimalist': ['neutral basics', 'clean lines', 'simple accessories'],
            'sporty': ['athleisure pieces', 'sneakers', 'hoodies', 'leggings']
        }
        return style_pieces.get(style, ['versatile basics', 'classic pieces'])
    
    def _get_style_focus(self, style: str) -> str:
        """Get focus description for styles"""
        focus_map = {
            'casual_chic': 'combining comfort with sophistication',
            'professional': 'polished, tailored pieces that command respect',
            'bohemian': 'flowing fabrics, earthy tones, and artistic flair',
            'minimalist': 'clean lines, neutral colors, and quality basics',
            'sporty': 'comfortable, functional pieces with athletic influence'
        }
        return focus_map.get(style, 'timeless, versatile pieces')