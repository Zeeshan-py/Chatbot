'use client';

import type React from 'react';
import Header from '@/components/Header';
import ChatPanel from '@/components/ChatPanel';
import ActionPlan from '@/components/ActionPlan';
import SystemControls from '@/components/SystemControls';
import ActivityLog from '@/components/ActivityLog';

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground overflow-hidden flex flex-col">
      <Header />
      
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-4 p-4 min-h-0">
        {/* Left Panel - System Controls */}
        <div className="lg:col-span-1 min-h-0">
          <SystemControls />
        </div>

        {/* Center Panel - Chat */}
        <div className="lg:col-span-2 min-h-0">
          <ChatPanel />
        </div>

        {/* Right Panel - Action Plan */}
        <div className="lg:col-span-1 min-h-0">
          <ActionPlan />
        </div>
      </div>

      {/* Bottom Activity Log */}
      <div className="h-40 border-t border-primary/10">
        <ActivityLog />
      </div>
    </div>
  );
}
