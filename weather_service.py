import requests
from config import Config

class WeatherService:
    def __init__(self):
        self.api_key = Config.WEATHER_API_KEY
        self.api_url = Config.WEATHER_API_URL
    
    def get_weather(self, city):
        """Get current weather for a city"""
        if not self.api_key:
            # Return mock data if no API key
            return {
                'temperature': 22,
                'condition': 'partly cloudy',
                'humidity': 65,
                'wind_speed': 10
            }
        
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.api_url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'temperature': round(data['main']['temp']),
                    'condition': data['weather'][0]['description'].lower(),
                    'humidity': data['main']['humidity'],
                    'wind_speed': round(data['wind']['speed'] * 3.6)  # Convert m/s to km/h
                }
        except Exception as e:
            print(f"Weather API error: {e}")
        
        # Fallback to mock data
        return {
            'temperature': 20,
            'condition': 'unknown',
            'humidity': 50,
            'wind_speed': 5
        }
    
    def get_weather_category(self, weather_data):
        """Categorize weather for outfit recommendations"""
        temp = weather_data['temperature']
        condition = weather_data['condition']
        
        # Temperature categories
        if temp < 5:
            temp_category = 'very_cold'
        elif temp < 15:
            temp_category = 'cold'
        elif temp < 25:
            temp_category = 'mild'
        elif temp < 30:
            temp_category = 'warm'
        else:
            temp_category = 'hot'
        
        # Weather condition categories
        rain_conditions = ['rain', 'drizzle', 'shower', 'thunderstorm']
        snow_conditions = ['snow', 'sleet', 'blizzard']
        cloudy_conditions = ['clouds', 'overcast', 'partly cloudy']
        
        if any(cond in condition for cond in rain_conditions):
            condition_category = 'rainy'
        elif any(cond in condition for cond in snow_conditions):
            condition_category = 'snowy'
        elif any(cond in condition for cond in cloudy_conditions):
            condition_category = 'cloudy'
        elif 'clear' in condition or 'sunny' in condition:
            condition_category = 'sunny'
        else:
            condition_category = 'neutral'
        
        return {
            'temperature_category': temp_category,
            'condition_category': condition_category,
            'temperature': temp,
            'condition': condition
        }