// Configuration - UPDATE THIS URL AFTER DEPLOYING BACKEND
const API_URL = 'http://localhost:5000/api/chat';
const HEALTH_URL = 'http://localhost:5000/api/health';

// Generate unique session ID
const sessionId = 'user_' + Math.random().toString(36).substr(2, 9);

// DOM Elements
const chatWidget = document.getElementById('chatWidget');
const chatToggleBtn = document.getElementById('chatToggleBtn');
const chatHeader = document.getElementById('chatHeader');
const minimizeBtn = document.getElementById('minimizeBtn');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');

// State
let isOpen = false;
let isTyping = false;

// Toggle chat widget
chatToggleBtn.addEventListener('click', () => {
    isOpen = !isOpen;
    chatWidget.classList.toggle('open', isOpen);
    chatToggleBtn.style.display = isOpen ? 'none' : 'flex';
    
    if (isOpen) {
        messageInput.focus();
    }
});

chatHeader.addEventListener('click', (e) => {
    if (e.target === chatHeader || e.target.closest('.chat-header-left')) {
        // Only toggle if not clicking minimize button
        if (!e.target.closest('.minimize-btn')) {
            isOpen = false;
            chatWidget.classList.remove('open');
            chatToggleBtn.style.display = 'flex';
        }
    }
});

minimizeBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    isOpen = false;
    chatWidget.classList.remove('open');
    chatToggleBtn.style.display = 'flex';
});

// Send message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    messageInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add bot response
        addMessage(data.response, 'bot');
        
        // If user name was captured, update greeting
        if (data.user_name) {
            console.log('User identified:', data.user_name);
        }
        
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        addMessage('Sorry, I\'m having trouble connecting. Please try again later.', 'bot');
    }
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? 'You' : 'BS';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = text;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    if (isTyping) return;
    isTyping = true;
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot';
    typingDiv.id = 'typingIndicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = 'BS';
    
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    
    typingDiv.appendChild(avatar);
    typingDiv.appendChild(indicator);
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
    isTyping = false;
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Check API health on load
async function checkHealth() {
    try {
        const response = await fetch(HEALTH_URL);
        const data = await response.json();
        console.log('Chatbot API:', data);
    } catch (error) {
        console.warn('Backend not running locally. Deploy to Render for production.');
    }
}

checkHealth();