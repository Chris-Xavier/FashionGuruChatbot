import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fashion-guru-secret-key-2025'
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
    WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'