'use client';

import { useState } from 'react';

interface Control {
  id: string;
  label: string;
  enabled: boolean;
  icon: string;
}

export default function SystemControls() {
  const [controls, setControls] = useState<Control[]>([
    { id: 'execute', label: 'Execute', enabled: true, icon: '⚙️' },
    { id: 'analyze', label: 'Analyze', enabled: true, icon: '🔍' },
    { id: 'monitor', label: 'Monitor', enabled: true, icon: '📊' },
    { id: 'learn', label: 'Learn', enabled: true, icon: '🧠' },
  ]);

  const [resources] = useState({
    cpu: 45,
    memory: 62,
    storage: 28,
  });

  const toggleControl = (id: string) => {
    setControls((prev) =>
      prev.map((c) => (c.id === id ? { ...c, enabled: !c.enabled } : c))
    );
  };

  return (
    <div className="flex flex-col h-full bg-background border border-primary/10 rounded-lg overflow-hidden">
      <div className="bg-secondary/50 border-b border-primary/10 px-4 py-3">
        <h3 className="font-semibold text-foreground text-sm">SYSTEM CONTROL</h3>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Permissions */}
        <div className="space-y-2">
          <p className="text-xs font-semibold text-primary uppercase">Permissions</p>
          <div className="space-y-2">
            {controls.map((control) => (
              <button
                key={control.id}
                onClick={() => toggleControl(control.id)}
                className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg border transition-all ${
                  control.enabled
                    ? 'bg-primary/10 border-primary/50 hover:bg-primary/20'
                    : 'bg-secondary/50 border-primary/10 hover:bg-secondary/70 opacity-50'
                }`}
              >
                <span className="text-lg">{control.icon}</span>
                <span className="text-sm font-medium flex-1 text-left">{control.label}</span>
                <div className={`w-4 h-4 rounded border-2 flex items-center justify-center ${
                  control.enabled ? 'bg-primary border-primary' : 'border-primary/30'
                }`}>
                  {control.enabled && <span className="text-white text-xs">✓</span>}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Resources */}
        <div className="space-y-3 pt-4 border-t border-primary/10">
          <p className="text-xs font-semibold text-primary uppercase">Resources</p>
          
          {[
            { label: 'CPU', value: resources.cpu, icon: '⚡' },
            { label: 'Memory', value: resources.memory, icon: '💾' },
            { label: 'Storage', value: resources.storage, icon: '📦' },
          ].map((resource) => (
            <div key={resource.label} className="space-y-1">
              <div className="flex items-center justify-between text-xs">
                <span className="text-muted-foreground flex items-center gap-1">
                  <span>{resource.icon}</span>
                  {resource.label}
                </span>
                <span className="text-foreground font-semibold">{resource.value}%</span>
              </div>
              <div className="h-2 bg-secondary/50 rounded-full overflow-hidden border border-primary/10">
                <div
                  className="h-full bg-gradient-to-r from-primary to-primary-dark transition-all"
                  style={{ width: `${resource.value}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-secondary/50 border-t border-primary/10 px-4 py-3">
        <p className="text-xs text-muted-foreground text-center">v2.4.1 | All Systems Ready</p>
      </div>
    </div>
  );
}
