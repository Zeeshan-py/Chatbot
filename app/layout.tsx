import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FRIDAY OS - AI Agent Control Center",
  description: "Advanced AI control center with real-time action planning and execution",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-background text-foreground">{children}</body>
    </html>
  );
}
