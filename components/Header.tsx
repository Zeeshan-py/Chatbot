'use client';

export default function Header() {
  return (
    <header className="bg-background border-b border-primary/20 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-primary-dark flex items-center justify-center animate-pulse-glow">
            <span className="text-white font-bold text-lg">F</span>
          </div>
          <div>
            <h1 className="text-xl font-bold text-foreground">FRIDAY OS</h1>
            <p className="text-xs text-muted-foreground">Artificial Intelligence Agent</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right">
            <p className="text-sm font-semibold text-primary">ACTIVE</p>
            <p className="text-xs text-muted-foreground">All Systems Operational</p>
          </div>
          <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse"></div>
        </div>
      </div>
    </header>
  );
}
