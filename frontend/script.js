const chatBox = document.getElementById('chat-box');
const form = document.getElementById('chat-form');
const input = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');

// Generate a random session ID for this user session
const sessionId = 'session_' + Math.random().toString(36).substring(2, 10);
const API_URL = 'http://localhost:8000/api/chat';

function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Format the markdown content locally before appending 
function formatMarkdown(text) {
    if (typeof marked !== 'undefined') {
        return marked.parse(text);
    }
    // Fallback if marked is not loaded
    return text.replace(/\n/g, '<br>');
}

function appendMessage(sender, content, isHtml = false) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender === 'user' ? 'user-msg' : 'ai-msg'}`;
    
    let avatarIcon = sender === 'user' ? '👤' : '🤖';
    let avatarClass = sender === 'user' ? 'user-avatar' : 'ai-avatar';
    
    let bodyContent = isHtml ? content : formatMarkdown(content);

    msgDiv.innerHTML = `
        <div class="avatar ${avatarClass}">${avatarIcon}</div>
        <div class="bubble">${bodyContent}</div>
    `;
    
    chatBox.appendChild(msgDiv);
    scrollToBottom();
    return msgDiv;
}

function showThinking() {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message ai-msg id-thinking';
    msgDiv.innerHTML = `
        <div class="avatar ai-avatar">🤖</div>
        <div class="bubble">
            <div class="thinking">
                <div class="think-dot"></div>
                <div class="think-dot"></div>
                <div class="think-dot"></div>
            </div>
        </div>
    `;
    chatBox.appendChild(msgDiv);
    scrollToBottom();
    return msgDiv;
}

function removeThinking() {
    const thinkingNodes = document.querySelectorAll('.id-thinking');
    thinkingNodes.forEach(node => node.remove());
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userMessage = input.value.trim();
    if (!userMessage) return;

    // 1. Add user message to UI
    appendMessage('user', userMessage);
    input.value = '';
    
    // 2. Show thinking indicator
    showThinking();
    
    try {
        // 3. Send request to FastAPI backend
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: userMessage,
                session_id: sessionId
            })
        });

        const data = await response.json();
        
        // 4. Remove thinking & display AI response
        removeThinking();
        if (data.response) {
            appendMessage('ai', data.response);
        } else {
            appendMessage('ai', "Sorry, I received an empty response from the server.");
        }
        
    } catch (error) {
        removeThinking();
        console.error('Error fetching from API:', error);
        appendMessage('ai', `⚠️ Error connecting to the server backend. Is the FastAPI server running on port 8000?\n\nError details: ${error.message}`);
    }
});
