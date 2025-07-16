from flask import Flask, render_template, request, jsonify, session
from chatbot import FashionGuruChatbot
from config import Config
import uuid

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the chatbot
chatbot = FashionGuruChatbot()

@app.route('/')
def index():
    """Main chat interface"""
    # Generate a unique session ID for each user
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        message = data['message'].strip()
        location = data.get('location', 'New York')
        
        if not message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get user ID from session
        user_id = session.get('user_id', 'anonymous')
        
        # Process the message
        response = chatbot.process_message(message, user_id, location)
        
        return jsonify(response)
    
    except Exception as e:
        app.logger.error(f"Chat error: {str(e)}")
        return jsonify({
            'response': "I'm sorry, I encountered an error. Please try again!",
            'suggestions': ["Help me choose an outfit", "What should I wear?"]
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Fashion Guru Chatbot'})

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)