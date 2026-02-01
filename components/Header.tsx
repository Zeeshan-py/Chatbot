import React from 'react';

export default function Header() {
  return (
    <header className="border-b border-border bg-background/80 backdrop-blur-sm p-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-10 h-10 rounded border-2 border-primary bg-primary/10 flex items-center justify-center glow">
              <span className="text-primary font-bold text-lg">F</span>
            </div>
            <div className="absolute inset-0 rounded border-2 border-primary animate-pulse-glow"></div>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-primary">FRIDAY OS</h1>
            <p className="text-xs text-muted">Advanced AI Agent Control Center</p>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
            <span className="text-sm text-muted">System Online</span>
          </div>
          <div className="text-xs text-muted font-mono">
            {new Date().toLocaleTimeString()}
          </div>
        </div>
      </div>
    </header>
  );
}
