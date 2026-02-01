'use client';

import React, { useState, useEffect } from 'react';
import { UIMessage } from 'ai';

interface Step {
  id: string;
  text: string;
  status: 'pending' | 'running' | 'done' | 'error';
}

interface ActionPlanProps {
  messages: UIMessage[];
}

export default function ActionPlan({ messages }: ActionPlanProps) {
  const [steps, setSteps] = useState<Step[]>([]);

  useEffect(() => {
    if (messages.length > 0) {
      const lastUserMessage = [...messages]
        .reverse()
        .find((m) => m.role === 'user');

      if (lastUserMessage) {
        const newSteps = generateStepsFromMessage(lastUserMessage);
        if (newSteps.length > 0) {
          setSteps(newSteps);
        }
      }
    }
  }, [messages]);

  const generateStepsFromMessage = (message: UIMessage): Step[] => {
    const text = getMessageText(message);
    const keywords = text.split(' ').filter((w) => w.length > 3).slice(0, 3);
    
    return keywords.length > 0
      ? keywords.map((_, idx) => ({
          id: `step-${idx}`,
          text: `Execute step ${idx + 1}`,
          status: idx === 0 ? 'running' : 'pending',
        }))
      : [];
  };

  const getMessageText = (message: UIMessage): string => {
    if (!message.parts || !Array.isArray(message.parts)) return '';
    return message.parts
      .filter((p): p is { type: 'text'; text: string } => p.type === 'text')
      .map((p) => p.text)
      .join('');
  };

  const updateStepStatus = (stepId: string, status: Step['status']) => {
    setSteps((prev) =>
      prev.map((step) => (step.id === stepId ? { ...step, status } : step))
    );
  };

  useEffect(() => {
    if (steps.length === 0) return;

    const interval = setInterval(() => {
      setSteps((prev) => {
        const updated = [...prev];
        const runningIdx = updated.findIndex((s) => s.status === 'running');

        if (runningIdx === -1) return prev;

        if (Math.random() > 0.3) {
          updated[runningIdx].status = 'done';
          if (runningIdx + 1 < updated.length) {
            updated[runningIdx + 1].status = 'running';
          }
        }

        return updated;
      });
    }, 2000);

    return () => clearInterval(interval);
  }, [steps.length]);

  return (
    <div className="border border-border rounded bg-gradient-to-b from-background to-background/50 p-4 flex flex-col h-full">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-border">
        <h3 className="font-bold text-primary text-sm">ACTION PLAN</h3>
        <span className="text-xs text-accent font-mono">
          {steps.filter((s) => s.status === 'done').length}/{steps.length}
        </span>
      </div>

      <div className="flex-1 overflow-y-auto space-y-2">
        {steps.length === 0 ? (
          <div className="h-full flex items-center justify-center text-center">
            <div>
              <p className="text-xs text-muted">No plan yet</p>
              <p className="text-xs text-muted/70 mt-1">Send a goal to generate steps</p>
            </div>
          </div>
        ) : (
          steps.map((step) => (
            <div key={step.id} className="group">
              <div className="flex items-start gap-3 p-2 rounded border border-border/50 hover:border-primary/50 transition">
                <div className="mt-1">
                  {step.status === 'pending' && (
                    <div className="w-4 h-4 rounded border border-muted/50"></div>
                  )}
                  {step.status === 'running' && (
                    <div className="w-4 h-4 rounded border-2 border-primary border-t-transparent animate-spin"></div>
                  )}
                  {step.status === 'done' && (
                    <div className="w-4 h-4 rounded border-2 border-green-500 bg-green-500/20 flex items-center justify-center">
                      <span className="text-xs">✓</span>
                    </div>
                  )}
                  {step.status === 'error' && (
                    <div className="w-4 h-4 rounded border-2 border-red-500 bg-red-500/20 flex items-center justify-center">
                      <span className="text-xs">✕</span>
                    </div>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-mono text-foreground/80 truncate">
                    {step.text}
                  </p>
                  <p className="text-xs text-muted/60 mt-1">
                    {step.status === 'running' && 'In progress...'}
                    {step.status === 'done' && 'Completed'}
                    {step.status === 'pending' && 'Awaiting...'}
                    {step.status === 'error' && 'Failed'}
                  </p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
