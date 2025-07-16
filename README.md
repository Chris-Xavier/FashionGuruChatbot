# Fashion Guru Chatbot 👗

A fully functional AI-powered chatbot specifically designed to give you all the fashion advice you could dream of! From helping you design the perfect outfit based on weather and occasion, to providing personalized shopping recommendations based on your existing wardrobe.

## Features ✨

- **Smart Outfit Recommendations**: Get outfit suggestions based on:
  - Current weather conditions
  - Time of day (morning, afternoon, evening)
  - Occasion (work, casual, formal, date, workout)
  - Your personal style preferences

- **Weather Integration**: Real-time weather data integration for location-based outfit recommendations

- **Wardrobe Analysis**: Analyze your existing wardrobe and get suggestions for:
  - Missing essential items
  - Seasonal additions
  - Shopping priorities

- **Style Advice**: Get personalized style tips for different looks:
  - Casual Chic
  - Professional
  - Bohemian
  - Minimalist
  - Sporty

- **Interactive Chat Interface**: Beautiful, responsive web interface with:
  - Real-time messaging
  - Quick suggestion buttons
  - Location customization
  - Mobile-friendly design

## Quick Start 🚀

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Chris-Xavier/FashionGuruChatbot.git
   cd FashionGuruChatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys if desired
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage Examples 💬

Try asking the Fashion Guru:

- "What should I wear today?"
- "Help me choose an outfit for a work meeting"
- "What should I wear in cold rainy weather?"
- "I need shopping advice for my wardrobe"
- "Give me some casual chic style tips"
- "I have jeans, t-shirts, and sneakers - what should I buy next?"

## Configuration ⚙️

### Weather API (Optional)
To get real-time weather data:

1. Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api)
2. Add your API key to the `.env` file:
   ```
   WEATHER_API_KEY=your-api-key-here
   ```

Without an API key, the chatbot will use mock weather data and still provide great outfit recommendations!

## Technology Stack 🛠️

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Weather API**: OpenWeatherMap (optional)
- **Styling**: Custom CSS with Font Awesome icons
- **NLP**: Pattern-based intent recognition

## Project Structure 📁

```
FashionGuruChatbot/
├── app.py                 # Main Flask application
├── chatbot.py            # Core chatbot logic and NLP
├── fashion_engine.py     # Fashion recommendation engine
├── weather_service.py    # Weather API integration
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── templates/           # HTML templates
│   ├── index.html      # Main chat interface
│   ├── 404.html        # Error pages
│   └── 500.html
└── static/             # Static assets
    ├── css/
    │   └── style.css   # Styling
    └── js/
        ├── app.js      # Frontend JavaScript
        └── sw.js       # Service worker
```

## Contributing 🤝

Contributions are welcome! Here are some ways you can contribute:

- Add new fashion knowledge and outfit combinations
- Improve the natural language processing
- Add new features like outfit photo upload
- Enhance the UI/UX design
- Add more comprehensive testing

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- OpenWeatherMap for weather data API
- Font Awesome for beautiful icons
- The open-source community for inspiration and tools

---

Made with ❤️ for fashion lovers everywhere!
