'use client';

import { useState, useEffect } from 'react';

interface LogEntry {
  id: number;
  timestamp: string;
  level: 'info' | 'success' | 'warning' | 'error';
  message: string;
}

const initialLogs: LogEntry[] = [
  { id: 1, timestamp: '14:23:01', level: 'info', message: 'FRIDAY OS Initialized' },
  { id: 2, timestamp: '14:23:02', level: 'success', message: 'All systems online' },
  { id: 3, timestamp: '14:23:03', level: 'info', message: 'Groq API Connected' },
];

export default function ActivityLog() {
  const [logs, setLogs] = useState<LogEntry[]>(initialLogs);

  useEffect(() => {
    const timer = setInterval(() => {
      const messages = [
        'Analyzing input...',
        'Processing language model...',
        'Generating action plan...',
        'Verifying execution steps...',
        'System check complete...',
      ];
      const levels: Array<'info' | 'success' | 'warning' | 'error'> = ['info', 'success', 'warning'];
      
      const newLog: LogEntry = {
        id: Date.now(),
        timestamp: new Date().toLocaleTimeString(),
        level: levels[Math.floor(Math.random() * levels.length)],
        message: messages[Math.floor(Math.random() * messages.length)],
      };

      setLogs((prev) => [newLog, ...prev.slice(0, 9)]);
    }, 3000);

    return () => clearInterval(timer);
  }, []);

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'success':
        return 'text-green-400';
      case 'warning':
        return 'text-yellow-400';
      case 'error':
        return 'text-red-400';
      default:
        return 'text-primary';
    }
  };

  return (
    <div className="bg-background border border-primary/10 rounded-lg overflow-hidden flex flex-col">
      <div className="bg-secondary/50 border-b border-primary/10 px-4 py-3">
        <h3 className="font-semibold text-foreground text-sm">ACTIVITY LOG</h3>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-2 font-mono text-xs">
        {logs.map((log) => (
          <div key={log.id} className="flex gap-3 animate-fade-in">
            <span className="text-muted-foreground flex-shrink-0 w-20">[{log.timestamp}]</span>
            <span className={`font-semibold flex-shrink-0 w-12 ${getLevelColor(log.level)}`}>
              [{log.level.toUpperCase()}]
            </span>
            <span className="text-muted-foreground flex-1">{log.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
