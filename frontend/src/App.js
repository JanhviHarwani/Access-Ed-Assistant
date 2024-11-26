// src/App.js
import React from 'react';
import ChatWindow from './components/ChatWindow';

export default function App() {
  return (
    <div className="flex h-screen bg-gray-100">
      <div className="m-auto w-full max-w-4xl bg-white rounded-lg shadow-xl overflow-hidden">
        <div className="bg-indigo-600 p-4">
          <h1 className="text-2xl text-white font-bold">
            Accessibility Education Assistant
          </h1>
          <p className="text-indigo-100">
            Ask questions about making education accessible for visually impaired students
          </p>
        </div>
        <ChatWindow />
      </div>
    </div>
  );
}

