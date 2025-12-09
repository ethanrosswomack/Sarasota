/**
 * Voyagers AI Chatbot Widget
 * A beautiful purple/green themed chat interface
 */

(function() {
  'use strict';

  // === Backend API endpoint ===
  // Primary: custom domain for the Worker
  const API_URL = "https://sphinx.aetherintelligence.net/ask";
  // Fallback (while wiring DNS/custom domain): uncomment if needed
  // const API_URL = "https://sphinx-aether-api.omniversalmail.workers.dev/ask";

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
        line-height
