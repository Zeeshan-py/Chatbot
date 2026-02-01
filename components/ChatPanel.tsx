'use client';

import React, { useEffect, useRef } from 'react';
import { UIMessage } from 'ai';

interface ChatPanelProps {
  messages: UIMessage[];
  input: string;
  setInput: (value: string) => void;
  onSendMessage: (message: string) => void;
  status: string;
}

export default function ChatPanel({
  messages,
  input,
  setInput,
  onSendMessage,
  status,
}: ChatPanelProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      onSendMessage(input);
      setInput('');
    }
  };

  const getMessageText = (message: UIMessage): string => {
    if (!message.parts || !Array.isArray(message.parts)) return '';
    return message.parts
      .filter((p): p is { type: 'text'; text: string } => p.type === 'text')
      .map((p) => p.text)
      .join('');
  };

  return (
    <div className="flex flex-col gap-4 h-full border border-border rounded bg-gradient-to-b from-background to-background/50">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="w-16 h-16 rounded border-2 border-primary/30 flex items-center justify-center mb-4">
              <span className="text-3xl">▲</span>
            </div>
            <h2 className="text-xl font-bold text-primary mb-2">FRIDAY Ready</h2>
            <p className="text-sm text-muted max-w-xs">
              Define your goal and FRIDAY will create a comprehensive action plan
            </p>
          </div>
        ) : (
          <>
            {messages.map((message, idx) => (
              <div
                key={idx}
                className={`animate-fade-in ${
                  message.role === 'user' ? 'flex justify-end' : 'flex justify-start'
                }`}
              >
                <div
                  className={`max-w-xs px-4 py-3 rounded border ${
                    message.role === 'user'
                      ? 'bg-primary/20 border-primary text-foreground'
                      : 'bg-accent/10 border-accent text-foreground'
                  }`}
                >
                  <p className="text-sm">{getMessageText(message)}</p>
                </div>
              </div>
            ))}
            {status === 'streaming' && (
              <div className="flex justify-start">
                <div className="bg-accent/10 border border-accent rounded px-4 py-3">
                  <div className="flex gap-2 items-center">
                    <div className="w-2 h-2 rounded-full bg-accent animate-pulse"></div>
                    <span className="text-xs text-muted font-mono">Processing...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="border-t border-border p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Define your goal for FRIDAY..."
            className="flex-1 bg-background/50 border border-border rounded px-3 py-2 text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/50 transition"
            disabled={status === 'streaming'}
          />
          <button
            type="submit"
            disabled={status === 'streaming' || !input.trim()}
            className="px-4 py-2 bg-primary text-background font-semibold rounded hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed transition duration-200 text-sm glow"
          >
            {status === 'streaming' ? '⟳' : '▶'}
          </button>
        </div>
      </form>
    </div>
  );
}
