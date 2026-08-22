import type { Metadata } from "next";
import "./globals.css";
import Header from "@/components/Header";

export const metadata: Metadata = {
  title: "LaunchGood Ops Copilot · Command Center",
  description: "Executive human-in-the-loop operations copilot for reviewing campaign risk, policy grounding, and evidence.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-navy-950 text-slate-100 min-h-screen flex flex-col antialiased selection:bg-brand-teal selection:text-white">
        <Header />
        <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-8">
          {children}
        </main>
        <footer className="border-t border-navy-800 bg-navy-950 py-6 text-center text-xs text-slate-500">
          <p>LaunchGood Ops Copilot · Prototype v0.2 · AI prepares the decision; humans own the consequence.</p>
        </footer>
      </body>
    </html>
  );
}
