'use client';

import React, { useEffect, useRef } from 'react';

interface ActivityLogProps {
  logs: string[];
}

export default function ActivityLog({ logs }: ActivityLogProps) {
  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'auto' });
  }, [logs]);

  return (
    <div className="flex flex-col h-full bg-background p-4">
      <div className="flex items-center justify-between mb-3 pb-2 border-b border-border">
        <h3 className="font-bold text-primary text-sm">ACTIVITY LOG</h3>
        <span className="text-xs text-muted font-mono">{logs.length} events</span>
      </div>

      <div className="flex-1 overflow-y-auto font-mono text-xs space-y-1">
        {logs.length === 0 ? (
          <div className="text-muted/50">Waiting for activity...</div>
        ) : (
          logs.map((log, idx) => (
            <div
              key={idx}
              className="text-muted hover:text-foreground/70 transition animate-slide-in"
            >
              <span className="text-primary">{log.split(']')[0]}]</span>
              <span>{log.split(']').slice(1).join(']')}</span>
            </div>
          ))
        )}
        <div ref={logsEndRef} />
      </div>
    </div>
  );
}
