'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

const ChatMessage = ({ message, isUser }: { message: string; isUser: boolean }) => (
  <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
    <div
      className={`rounded-lg px-4 py-2 max-w-[70%] ${
        isUser 
          ? 'bg-blue-500 text-white' 
          : 'bg-gray-100 text-gray-900'
      }`}
    >
      {message}
    </div>
  </div>
);

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { text: "Hi! How can I help you today?", isUser: false }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      (messagesEndRef.current as HTMLElement).scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Simple response generator - replace with actual API call
  const generateBotResponse = async (userMessage: string) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const responses = [
      "I understand. Can you tell me more about that?",
      "That's interesting! How does that make you feel?",
      "Let me think about that for a moment...",
      "I see what you mean. What would you like to know more about?",
      "Could you elaborate on that?"
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    if (!inputMessage.trim()) return;

    // Add user message
    const userMessage = { text: inputMessage, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');    
    setIsLoading(true);

    // Generate and add bot response
    const botResponse = await generateBotResponse(inputMessage);
    setMessages(prev => [...prev, { text: botResponse, isUser: false }]);
    setIsLoading(false);
  };

  return (
    <div className="flex flex-col h-screen w-full max-w-2xl mx-auto bg-white rounded-lg shadow-lg">
      {/* Chat header */}
      <div className="px-6 py-4 bg-gray-50 border-b rounded-t-lg">
        <h2 className="text-xl font-semibold text-gray-800">Chat Assistant</h2>
      </div>

      {/* Messages container */}
      <div className="flex-1 p-6 overflow-y-auto">
        {messages.map((message, index) => (
          <ChatMessage
            key={index}
            message={message.text}
            isUser={message.isUser}
          />
        ))}
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-gray-100 text-gray-900 rounded-lg px-4 py-2">
              <div className="flex gap-2">
                <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce" />
                <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce [animation-delay:0.2s]" />
                <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce [animation-delay:0.4s]" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input form */}
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
};

export default Chatbot;