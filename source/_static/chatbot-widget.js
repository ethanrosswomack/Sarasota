/**
 * Voyagers AI Chatbot Widget
 * A beautiful purple/green themed chat interface
 */

(function() {
  'use strict';

  const API_BASE = window.location.origin.replace(':5000', ':8080');
  
  let chatOpen = false;
  let conversationHistory = [];

  /**
   * Create chat widget HTML
   */
  function createChatWidget() {
    const chatHTML = `
      <div id="voyagers-chatbot" class="chatbot-container closed">
        <!-- Chat Button -->
        <button id="chat-toggle-btn" class="chat-toggle-btn" aria-label="Open AI Assistant">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
          </svg>
          <span class="chat-badge">AI</span>
        </button>
        
        <!-- Chat Window -->
        <div id="chat-window" class="chat-window">
          <div class="chat-header">
            <div class="chat-header-content">
              <h3>🔮 Voyagers AI Assistant</h3>
              <p>Ask me about the Guardian Alliance, Amenti, or any Voyagers topics</p>
            </div>
            <button id="chat-close-btn" class="chat-close-btn" aria-label="Close chat">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          
          <div id="chat-messages" class="chat-messages">
            <div class="chat-message assistant">
              <div class="message-content">
                👋 Welcome! I'm your AI guide to the Voyagers material. Ask me anything about:
                <ul style="margin-top: 0.5em; padding-left: 1.5em;">
                  <li>The Sphere of Amenti and the Halls of Amenti</li>
                  <li>Guardian Alliance and the rescue mission</li>
                  <li>Root Races and human origins</li>
                  <li>Keylontic Science and DNA activation</li>
                  <li>Time cycles and ascension mechanics</li>
                </ul>
              </div>
            </div>
          </div>
          
          <div class="chat-input-container">
            <textarea 
              id="chat-input" 
              class="chat-input" 
              placeholder="Ask about Voyagers content..."
              rows="1"
            ></textarea>
            <button id="chat-send-btn" class="chat-send-btn" aria-label="Send message">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
        </div>
      </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', chatHTML);
  }

  /**
   * Add CSS styles
   */
  function addStyles() {
    const style = document.createElement('style');
    style.textContent = `
      .chatbot-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 10000;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      }
      
      .chat-toggle-btn {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #7cd992, #5bc978);
        border: none;
        box-shadow: 0 4px 20px rgba(92, 201, 120, 0.4);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #1a0f2e;
        transition: all 0.3s ease;
        position: relative;
      }
      
      .chat-toggle-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 25px rgba(92, 201, 120, 0.6);
      }
      
      .chat-badge {
        position: absolute;
        top: -5px;
        right: -5px;
        background: #9fe6ad;
        color: #1a0f2e;
        font-size: 10px;
        font-weight: bold;
        padding: 2px 6px;
        border-radius: 10px;
        border: 2px solid #1a0f2e;
      }
      
      .chatbot-container.closed .chat-window {
        display: none;
      }
      
      .chatbot-container.open .chat-toggle-btn {
        display: none;
      }
      
      .chat-window {
        width: 380px;
        max-width: calc(100vw - 40px);
        height: 600px;
        max-height: calc(100vh - 100px);
        background: linear-gradient(135deg, #2a1b3d, #1a0f2e);
        border-radius: 16px;
        border: 1px solid rgba(126, 217, 146, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        display: flex;
        flex-direction: column;
        overflow: hidden;
      }
      
      .chat-header {
        background: linear-gradient(135deg, #3d2952, #2a1b3d);
        padding: 16px;
        border-bottom: 1px solid rgba(126, 217, 146, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
      }
      
      .chat-header h3 {
        margin: 0;
        color: #9fe6ad;
        font-size: 18px;
        text-shadow: 0 0 10px rgba(159, 230, 173, 0.3);
      }
      
      .chat-header p {
        margin: 4px 0 0 0;
        color: #c5b8d9;
        font-size: 13px;
      }
      
      .chat-close-btn {
        background: none;
        border: none;
        color: #c5b8d9;
        cursor: pointer;
        padding: 4px;
        border-radius: 4px;
        transition: all 0.2s;
      }
      
      .chat-close-btn:hover {
        background: rgba(126, 217, 146, 0.1);
        color: #9fe6ad;
      }
      
      .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }
      
      .chat-messages::-webkit-scrollbar {
        width: 6px;
      }
      
      .chat-messages::-webkit-scrollbar-track {
        background: rgba(26, 15, 46, 0.5);
      }
      
      .chat-messages::-webkit-scrollbar-thumb {
        background: rgba(126, 217, 146, 0.3);
        border-radius: 3px;
      }
      
      .chat-message {
        display: flex;
        flex-direction: column;
        max-width: 85%;
      }
      
      .chat-message.user {
        align-self: flex-end;
      }
      
      .chat-message.assistant {
        align-self: flex-start;
      }
      
      .message-content {
        padding: 12px 16px;
        border-radius: 12px;
        line-height: 1.5;
        font-size: 14px;
      }
      
      .chat-message.user .message-content {
        background: linear-gradient(135deg, #7cd992, #5bc978);
        color: #1a0f2e;
      }
      
      .chat-message.assistant .message-content {
        background: rgba(61, 41, 82, 0.6);
        color: #e8dff5;
        border: 1px solid rgba(126, 217, 146, 0.2);
      }
      
      .message-sources {
        font-size: 11px;
        color: #9fe6ad;
        margin-top: 6px;
        padding-left: 16px;
      }
      
      .chat-input-container {
        padding: 12px;
        background: rgba(42, 27, 61, 0.8);
        border-top: 1px solid rgba(126, 217, 146, 0.2);
        display: flex;
        gap: 8px;
      }
      
      .chat-input {
        flex: 1;
        background: rgba(26, 15, 46, 0.8);
        border: 1px solid rgba(126, 217, 146, 0.3);
        border-radius: 8px;
        padding: 10px 12px;
        color: #e8dff5;
        font-size: 14px;
        resize: none;
        font-family: inherit;
        max-height: 120px;
      }
      
      .chat-input:focus {
        outline: none;
        border-color: #7cd992;
        box-shadow: 0 0 10px rgba(124, 217, 146, 0.2);
      }
      
      .chat-send-btn {
        background: linear-gradient(135deg, #7cd992, #5bc978);
        border: none;
        border-radius: 8px;
        width: 44px;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        color: #1a0f2e;
        transition: all 0.2s;
      }
      
      .chat-send-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(92, 201, 120, 0.4);
      }
      
      .chat-send-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
      
      .typing-indicator {
        display: flex;
        gap: 4px;
        padding: 12px 16px;
      }
      
      .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #7cd992;
        animation: typing 1.4s infinite;
      }
      
      .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
      }
      
      .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
      }
      
      @keyframes typing {
        0%, 60%, 100% {
          opacity: 0.3;
          transform: scale(0.8);
        }
        30% {
          opacity: 1;
          transform: scale(1);
        }
      }
      
      @media (max-width: 480px) {
        .chat-window {
          width: calc(100vw - 40px);
          height: calc(100vh - 80px);
          bottom: 20px;
          right: 20px;
        }
      }
    `;
    document.head.appendChild(style);
  }

  /**
   * Toggle chat window
   */
  function toggleChat() {
    const container = document.getElementById('voyagers-chatbot');
    chatOpen = !chatOpen;
    
    if (chatOpen) {
      container.classList.remove('closed');
      container.classList.add('open');
      document.getElementById('chat-input').focus();
    } else {
      container.classList.remove('open');
      container.classList.add('closed');
    }
  }

  /**
   * Add message to chat
   */
  function addMessage(content, isUser, sources = null) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${isUser ? 'user' : 'assistant'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    messageDiv.appendChild(contentDiv);
    
    if (sources && sources.length > 0) {
      const sourcesDiv = document.createElement('div');
      sourcesDiv.className = 'message-sources';
      sourcesDiv.textContent = '📚 Sources: ' + sources.map(s => 
        `${s.volume} Ch${s.chapter}`
      ).join(', ');
      messageDiv.appendChild(sourcesDiv);
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  /**
   * Show typing indicator
   */
  function showTyping() {
    const messagesContainer = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'chat-message assistant';
    typingDiv.innerHTML = `
      <div class="message-content typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>
    `;
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  /**
   * Hide typing indicator
   */
  function hideTyping() {
    const typing = document.getElementById('typing-indicator');
    if (typing) typing.remove();
  }

  /**
   * Send message to API
   */
  async function sendMessage(message) {
    const sendBtn = document.getElementById('chat-send-btn');
    const input = document.getElementById('chat-input');
    
    sendBtn.disabled = true;
    showTyping();
    
    try {
      const response = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message })
      });
      
      if (!response.ok) {
        throw new Error('Failed to get response');
      }
      
      const data = await response.json();
      hideTyping();
      addMessage(data.response, false, data.sources);
      
    } catch (error) {
      hideTyping();
      addMessage('Sorry, I encountered an error. Please try again.', false);
      console.error('Chat error:', error);
    } finally {
      sendBtn.disabled = false;
      input.value = '';
      input.style.height = 'auto';
    }
  }

  /**
   * Handle send button click
   */
  function handleSend() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    addMessage(message, true);
    conversationHistory.push({ role: 'user', content: message });
    sendMessage(message);
  }

  /**
   * Initialize chatbot
   */
  function init() {
    addStyles();
    createChatWidget();
    
    // Event listeners
    document.getElementById('chat-toggle-btn').addEventListener('click', toggleChat);
    document.getElementById('chat-close-btn').addEventListener('click', toggleChat);
    document.getElementById('chat-send-btn').addEventListener('click', handleSend);
    
    const input = document.getElementById('chat-input');
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    });
    
    // Auto-resize textarea
    input.addEventListener('input', function() {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
