'use client';

import { useState, useRef, useEffect } from 'react';
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';
import ChatPanel from '@/components/ChatPanel';
import ActionPlan from '@/components/ActionPlan';
import SystemControls from '@/components/SystemControls';
import ActivityLog from '@/components/ActivityLog';
import Header from '@/components/Header';

export default function Home() {
  const [permissions, setPermissions] = useState({
    execute: true,
    analyze: true,
    monitor: true,
  });
  const [activityLog, setActivityLog] = useState<string[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  const { messages, input, setInput, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({
      api: '/api/chat',
    }),
  });

  useEffect(() => {
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      const timestamp = new Date().toLocaleTimeString();
      const logEntry = `[${timestamp}] ${lastMessage.role.toUpperCase()}: Message processed`;
      setActivityLog((prev) => [logEntry, ...prev].slice(0, 50));
    }
  }, [messages.length]);

  const handleSendMessage = async (text: string) => {
    setActivityLog((prev) => [
      `[${new Date().toLocaleTimeString()}] User input: ${text}`,
      ...prev,
    ].slice(0, 50));
    sendMessage({ text });
  };

  return (
    <div ref={containerRef} className="min-h-screen bg-background text-foreground overflow-hidden">
      <Header />
      
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 p-4 h-[calc(100vh-80px)]">
        {/* Left Panel - System Controls */}
        <div className="lg:col-span-1 flex flex-col gap-4 min-h-0">
          <SystemControls permissions={permissions} setPermissions={setPermissions} />
        </div>

        {/* Center Panel - Chat */}
        <div className="lg:col-span-2 flex flex-col gap-4 min-h-0">
          <ChatPanel
            messages={messages}
            input={input}
            setInput={setInput}
            onSendMessage={handleSendMessage}
            status={status}
          />
        </div>

        {/* Right Panel - Action Plan */}
        <div className="lg:col-span-1 flex flex-col gap-4 min-h-0">
          <ActionPlan messages={messages} />
        </div>
      </div>

      {/* Bottom Activity Log */}
      <div className="h-40 border-t border-border bg-background/50">
        <ActivityLog logs={activityLog} />
      </div>
    </div>
  );
}
