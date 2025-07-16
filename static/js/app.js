// Fashion Guru Chatbot JavaScript Application

class FashionGuruChat {
    constructor() {
        this.messagesContainer = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.chatForm = document.getElementById('chat-form');
        this.sendButton = document.getElementById('send-button');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.locationInput = document.getElementById('location-input');
        
        this.isTyping = false;
        this.messageHistory = [];
        
        this.init();
    }
    
    init() {
        // Event listeners
        this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
        this.messageInput.addEventListener('input', () => this.handleInputChange());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSubmit(e);
            }
        });
        
        // Focus on input
        this.messageInput.focus();
        
        // Auto-resize input
        this.messageInput.addEventListener('input', this.autoResizeInput.bind(this));
    }
    
    handleSubmit(e) {
        e.preventDefault();
        
        if (this.isTyping) return;
        
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        this.sendMessage(message);
    }
    
    handleInputChange() {
        const hasText = this.messageInput.value.trim().length > 0;
        this.sendButton.disabled = !hasText || this.isTyping;
    }
    
    autoResizeInput() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }
    
    async sendMessage(message) {
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        this.handleInputChange();
        
        // Show typing indicator
        this.showTyping();
        
        try {
            // Get location
            const location = this.locationInput.value.trim() || 'New York';
            
            // Send message to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    location: location
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Hide typing indicator
            this.hideTyping();
            
            // Add bot response
            this.addBotResponse(data);
            
        } catch (error) {
            console.error('Error:', error);
            this.hideTyping();
            this.addMessage(
                "I'm sorry, I'm having trouble connecting right now. Please try again!",
                'bot',
                ['Try again', 'Help me with an outfit', 'What should I wear?']
            );
        }
    }
    
    addMessage(content, sender, suggestions = []) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const textP = document.createElement('p');
        textP.textContent = content;
        messageContent.appendChild(textP);
        
        // Add suggestions if provided
        if (suggestions.length > 0) {
            const suggestionsDiv = document.createElement('div');
            suggestionsDiv.className = 'suggestions';
            
            suggestions.forEach(suggestion => {
                const btn = document.createElement('button');
                btn.className = 'suggestion-btn';
                btn.textContent = suggestion;
                btn.onclick = () => this.sendSuggestion(suggestion);
                suggestionsDiv.appendChild(btn);
            });
            
            messageContent.appendChild(suggestionsDiv);
        }
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Store in history
        this.messageHistory.push({
            content,
            sender,
            timestamp: new Date().toISOString()
        });
    }
    
    addBotResponse(data) {
        // Format the response content
        let content = data.response || "I'm not sure how to help with that. Could you try asking in a different way?";
        
        // Add bot message with suggestions
        this.addMessage(content, 'bot', data.suggestions || []);
        
        // If there's weather info, you could add it as a separate message or incorporate it
        if (data.weather_info) {
            console.log('Weather info received:', data.weather_info);
        }
        
        // If there are outfit details, log them for potential future use
        if (data.outfit_details) {
            console.log('Outfit details received:', data.outfit_details);
        }
    }
    
    sendSuggestion(suggestion) {
        this.messageInput.value = suggestion;
        this.sendMessage(suggestion);
    }
    
    showTyping() {
        this.isTyping = true;
        this.typingIndicator.style.display = 'block';
        this.sendButton.disabled = true;
        this.messageInput.disabled = true;
        this.scrollToBottom();
    }
    
    hideTyping() {
        this.isTyping = false;
        this.typingIndicator.style.display = 'none';
        this.messageInput.disabled = false;
        this.handleInputChange();
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 100);
    }
    
    // Utility method to format messages with markdown-like styling
    formatMessage(text) {
        // Simple formatting for bold text
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Format bullet points
        text = text.replace(/^• (.*$)/gim, '<div class="bullet-point">• $1</div>');
        return text;
    }
}

// Global function for suggestion buttons in initial message
function sendSuggestion(suggestion) {
    if (window.fashionChat) {
        window.fashionChat.sendSuggestion(suggestion);
    }
}

// Initialize the chat application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.fashionChat = new FashionGuruChat();
});

// Service Worker registration for potential offline functionality
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}