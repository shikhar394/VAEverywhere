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
    { content: "Hi! How can I help you today?", role: 'assistant' }
  ]);
  const [input, setInput] = useState('');
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

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    const userMessage = { content: input, role: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const requestMessages = [...messages, userMessage].map(msg => ({
        content: String(msg.content),  // Ensure content is a string
        role: String(msg.role)         // Ensure role is a string
      }));
      
      const requestBody = {
        messages: requestMessages
      };
      
      console.log("Request body:", JSON.stringify(requestBody, null, 2));
      
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.warn('API Error Status:', response.status);
        console.warn('API Error Response:', errorText);
        console.warn('API Error Response:', response);
      }
      
      debugger;
      const data = await response.json();
      const assistantMessage = {
        content: data.response || data.message, // Handle both possible response formats
        role: 'assistant'
      };
      setMessages(prev => [...prev, assistantMessage]);
      
      // If you need to debug, log the message directly
      console.log("New assistant message:", assistantMessage);
      console.log("Current messages:", [...messages, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        content: 'Sorry, there was an error processing your request.',
        role: 'assistant'
      }]);
    } finally {
      setIsLoading(false);
    }
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
            message={message.content}
            isUser={message.role === 'user'}
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
            value={input}
            onChange={(e) => setInput(e.target.value)}
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