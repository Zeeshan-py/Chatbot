'use client';

import React from 'react';

interface Permission {
  execute: boolean;
  analyze: boolean;
  monitor: boolean;
}

interface SystemControlsProps {
  permissions: Permission;
  setPermissions: (permissions: Permission) => void;
}

export default function SystemControls({
  permissions,
  setPermissions,
}: SystemControlsProps) {
  const togglePermission = (key: keyof Permission) => {
    setPermissions({
      ...permissions,
      [key]: !permissions[key],
    });
  };

  return (
    <div className="border border-border rounded bg-gradient-to-b from-background to-background/50 p-4 h-fit">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-border">
        <h3 className="font-bold text-accent text-sm">SYSTEM CONTROL</h3>
      </div>

      <div className="space-y-3">
        {[
          { key: 'execute' as const, label: 'Execute', icon: '⚡' },
          { key: 'analyze' as const, label: 'Analyze', icon: '◆' },
          { key: 'monitor' as const, label: 'Monitor', icon: '◉' },
        ].map(({ key, label, icon }) => (
          <div
            key={key}
            className="flex items-center gap-3 p-2 rounded border border-border/50 hover:border-accent/50 transition cursor-pointer group"
            onClick={() => togglePermission(key)}
          >
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                togglePermission(key);
              }}
              className={`w-5 h-5 rounded border-2 flex items-center justify-center transition ${
                permissions[key]
                  ? 'bg-accent/20 border-accent'
                  : 'border-border/50 group-hover:border-accent/30'
              }`}
            >
              {permissions[key] && (
                <span className="text-xs text-accent font-bold">✓</span>
              )}
            </button>
            <span className="text-xs font-mono text-foreground/80 flex-1">
              {icon} {label}
            </span>
            <span
              className={`text-xs ${
                permissions[key] ? 'text-green-500' : 'text-muted'
              }`}
            >
              {permissions[key] ? 'ON' : 'OFF'}
            </span>
          </div>
        ))}
      </div>

      {/* Memory Status */}
      <div className="mt-4 pt-4 border-t border-border space-y-2">
        <h4 className="text-xs font-bold text-primary">MEMORY</h4>
        <div className="space-y-2">
          {[
            { label: 'CPU', value: 45 },
            { label: 'RAM', value: 62 },
            { label: 'Storage', value: 38 },
          ].map(({ label, value }) => (
            <div key={label}>
              <div className="flex justify-between mb-1">
                <span className="text-xs text-muted font-mono">{label}</span>
                <span className="text-xs text-primary font-mono">{value}%</span>
              </div>
              <div className="w-full h-1 bg-border rounded overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-primary to-accent transition-all duration-500"
                  style={{ width: `${value}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Status Indicator */}
      <div className="mt-4 pt-4 border-t border-border">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <span className="text-xs text-muted font-mono">All Systems Nominal</span>
        </div>
      </div>
    </div>
  );
}
