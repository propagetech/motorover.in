/**
 * AI Travel Assistant Component
 * Chat interface for tour recommendations
 */

export function initAITravelAssistant() {
  const assistantContainer = document.querySelector('.ai-assistant');
  if (!assistantContainer) return;
  
  setupChatInterface(assistantContainer);
}

function setupChatInterface(container) {
  container.innerHTML = `
    <div class="ai-assistant__chat">
      <div class="ai-assistant__header">
        <h3>AI Travel Assistant</h3>
        <button class="ai-assistant__close" onclick="this.closest('.ai-assistant').classList.remove('ai-assistant--open')">×</button>
      </div>
      <div class="ai-assistant__messages" id="ai-messages"></div>
      <div class="ai-assistant__input">
        <input type="text" id="ai-input" placeholder="Ask me about tours..." class="form__input">
        <button class="btn btn--primary" onclick="window.aiAssistant?.sendMessage()">Send</button>
      </div>
    </div>
    <button class="ai-assistant__toggle" onclick="document.querySelector('.ai-assistant').classList.toggle('ai-assistant--open')">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
      </svg>
    </button>
  `;
  
  const messagesContainer = container.querySelector('#ai-messages');
  const input = container.querySelector('#ai-input');
  
  // Add welcome message
  addMessage(messagesContainer, 'assistant', 'Hello! I can help you find the perfect tour. Tell me about your preferences - budget, dates, destinations, or experience level.');
  
  window.aiAssistant = {
    sendMessage: async () => {
      const message = input.value.trim();
      if (!message) return;
      
      addMessage(messagesContainer, 'user', message);
      input.value = '';
      
      // Show typing indicator
      const typingId = addTypingIndicator(messagesContainer);
      
      try {
        const response = await getAIResponse(message);
        removeTypingIndicator(messagesContainer, typingId);
        addMessage(messagesContainer, 'assistant', response);
      } catch (error) {
        removeTypingIndicator(messagesContainer, typingId);
        addMessage(messagesContainer, 'assistant', 'Sorry, I encountered an error. Please try again.');
      }
    },
  };
  
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      window.aiAssistant.sendMessage();
    }
  });
}

async function getAIResponse(message) {
  // In production, this would call OpenAI API or similar
  // For now, return a simple response based on keywords
  
  const lowerMessage = message.toLowerCase();
  
  if (lowerMessage.includes('budget') || lowerMessage.includes('price') || lowerMessage.includes('cost')) {
    return 'We have tours across different budget ranges. Our motorcycle tours start from ₹2,50,000 and car tours from ₹1,80,000. Would you like to see tours in a specific price range?';
  }
  
  if (lowerMessage.includes('date') || lowerMessage.includes('when')) {
    return 'We have tours scheduled throughout the year. Popular destinations like Kyrgyzstan have multiple dates. Which month are you planning to travel?';
  }
  
  if (lowerMessage.includes('beginner') || lowerMessage.includes('easy')) {
    return 'For beginners, I recommend our car tours or motorcycle tours with basic off-roading. Tours like Georgia and Northern Europe are great starting points.';
  }
  
  if (lowerMessage.includes('adventure') || lowerMessage.includes('challenging')) {
    return 'For adventure seekers, check out our Silk Route motorcycle tour or South Africa tours. These include challenging off-road sections and breathtaking landscapes.';
  }
  
  return 'That sounds interesting! Could you tell me more about your preferred destination, travel dates, or budget? This will help me recommend the perfect tour for you.';
}

function addMessage(container, role, text) {
  const messageEl = document.createElement('div');
  messageEl.className = `ai-message ai-message--${role}`;
  messageEl.innerHTML = `<p>${text}</p>`;
  container.appendChild(messageEl);
  container.scrollTop = container.scrollHeight;
}

function addTypingIndicator(container) {
  const typingEl = document.createElement('div');
  typingEl.className = 'ai-message ai-message--assistant ai-typing';
  typingEl.id = 'typing-indicator';
  typingEl.innerHTML = '<p>Thinking...</p>';
  container.appendChild(typingEl);
  container.scrollTop = container.scrollHeight;
  return 'typing-indicator';
}

function removeTypingIndicator(container, id) {
  const typingEl = container.querySelector(`#${id}`);
  if (typingEl) {
    typingEl.remove();
  }
}

export default { initAITravelAssistant };
