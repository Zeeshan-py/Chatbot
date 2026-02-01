'use client';

import { useState, useEffect } from 'react';

interface ActionStep {
  id: number;
  title: string;
  description: string;
  status: 'pending' | 'running' | 'done' | 'error';
}

const defaultSteps: ActionStep[] = [
  { id: 1, title: 'Parse Goal', description: 'Analyzing user objective...', status: 'pending' },
  { id: 2, title: 'Create Plan', description: 'Breaking down into steps...', status: 'pending' },
  { id: 3, title: 'Execute', description: 'Running action steps...', status: 'pending' },
  { id: 4, title: 'Verify', description: 'Validating results...', status: 'pending' },
];

export default function ActionPlan() {
  const [steps, setSteps] = useState<ActionStep[]>(defaultSteps);

  useEffect(() => {
    const timer = setInterval(() => {
      setSteps((prev) =>
        prev.map((step, idx) => {
          if (idx === 0 && step.status === 'pending') {
            return { ...step, status: 'running' };
          }
          if (idx > 0 && prev[idx - 1]?.status === 'done' && step.status === 'pending') {
            return { ...step, status: 'running' };
          }
          if (step.status === 'running' && Math.random() > 0.7) {
            return { ...step, status: 'done' };
          }
          return step;
        })
      );
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'done':
        return 'bg-green-500/20 border-green-500/50 text-green-400';
      case 'running':
        return 'bg-primary/20 border-primary/50 text-primary animate-pulse-glow';
      case 'error':
        return 'bg-red-500/20 border-red-500/50 text-red-400';
      default:
        return 'bg-secondary/50 border-primary/20 text-muted-foreground';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'done':
        return '✓';
      case 'running':
        return '⚡';
      case 'error':
        return '✕';
      default:
        return '○';
    }
  };

  return (
    <div className="flex flex-col h-full bg-background border border-primary/10 rounded-lg overflow-hidden">
      <div className="bg-secondary/50 border-b border-primary/10 px-4 py-3">
        <h3 className="font-semibold text-foreground text-sm">ACTION PLAN</h3>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {steps.map((step, idx) => (
          <div
            key={step.id}
            className={`border rounded-lg p-3 transition-all animate-slide-in ${getStatusColor(step.status)}`}
          >
            <div className="flex items-start gap-3">
              <div className="text-lg font-bold flex-shrink-0 w-6 text-center">
                {getStatusIcon(step.status)}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-sm">{step.title}</p>
                <p className="text-xs opacity-75 mt-1">{step.description}</p>
              </div>
            </div>

            {/* Progress Bar */}
            {step.status === 'running' && (
              <div className="mt-3 h-1 bg-black/20 rounded-full overflow-hidden">
                <div className="h-full bg-primary animate-pulse" style={{ width: '60%' }}></div>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="bg-secondary/50 border-t border-primary/10 px-4 py-3 text-center">
        <p className="text-xs text-muted-foreground">
          {steps.filter((s) => s.status === 'done').length}/{steps.length} Complete
        </p>
      </div>
    </div>
  );
}
