// src/components/ChatWindow.js
import React, { useState, useRef, useEffect } from 'react';
import ChatInput from './ChatInput';
import ReactMarkdown from 'react-markdown';
// eslint-disable-next-line import/no-unresolved
import { Book, Calendar, Loader, Users } from 'lucide-react';
const QuickActionButton = ({ icon: Icon, title, description, onClick }) => (
  <button
    onClick={onClick}
    className="w-full p-6 bg-gray-900/30 rounded-lg border border-gray-800 hover:border-cyan-500/50 transition-all duration-300 hover:shadow-lg group text-left"
  > {/* Increased padding from p-4 to p-6 */}
    <div className="flex items-center space-x-4"> {/* Increased spacing between icon and text */}
      <Icon className="w-6 h-6 text-cyan-500 group-hover:scale-110 transition-transform" /> {/* Increased icon size */}
      <div>
        <h3 className="text-lg font-semibold text-cyan-500/90 mb-1">{title}</h3> {/* Added margin bottom */}
        <p className="text-sm text-gray-400 leading-relaxed">{description}</p> {/* Added relaxed line height */}
      </div>
    </div>
  </button>
);
export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    // Add user message to chat
    const newMessages = [
      ...messages,
      { role: 'user', content: message }
    ];
    setMessages(newMessages);
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          history: messages,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      setMessages([
        ...newMessages,
        { role: 'assistant', content: data.response }
      ]);
    } catch (error) {
      console.error('Error:', error);
      setMessages([
        ...newMessages,
        { 
          role: 'assistant', 
          content: 'I apologize, but I encountered an error. Please try again.'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };
  const quickActions = [
    {
      icon: Book,
      title: "Accessibility Tools",
      description: "Learn about assistive technologies and tools",
      message: "What accessibility tools are available for visually impaired students?"
    },
    {
      icon: Calendar,
      title: "Teaching Strategies",
      description: "Discover effective teaching methods",
      message: "How can I as a teacher help students who are visually impaired learn better?"
    },
    {
      icon: Users,
      title: "Classroom Adaptation",
      description: "Tips for creating inclusive classrooms",
      message: "How can I adapt my classroom for visually impaired students?"
    }
  ];

  return (
    <div className="flex flex-col h-[calc(100vh-11rem)]">
      <div className="flex-1 overflow-y-auto p-8 space-y-8">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-6 py-4 shadow-lg ${
                message.role === 'user'
                  ? 'bg-cyan-600 text-white'
                  : 'bg-gray-900/50 text-gray-100 border border-gray-800'
              } transition-all duration-300 hover:scale-[1.01]`}
            >
              <ReactMarkdown className="prose prose-invert prose-sm max-w-none">
                {message.content}
              </ReactMarkdown>
            </div>
          </div>
        ))}
        {messages.length === 0 && (
            <div className="space-y-6 animate-fade-in"> {/* Added more vertical spacing */}
            <p className="text-gray-400 text-sm px-1">
              Ask questions about making education accessible for visually impaired students
            </p>
            <div className="grid gap-5"> {/* Increased gap between buttons */}
              {quickActions.map((action, index) => (
                <QuickActionButton
                  key={index}
                  icon={action.icon}
                  title={action.title}
                  description={action.description}
                  onClick={() => handleSendMessage(action.message)}
                />
              ))}
            </div>
          </div>
        )}
        {loading && (
          <div className="flex justify-start animate-fade-in">
            <div className="bg-gray-900/50 rounded-lg px-6 py-4 shadow-lg border border-gray-800">
              <div className="flex space-x-2">
                <Loader className="w-5 h-5 animate-spin text-cyan-500" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="p-6 border-t border-gray-800 bg-gray-900/30">
        <ChatInput onSendMessage={handleSendMessage} disabled={loading} />
      </div>
    </div>
  );
}