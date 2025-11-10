import 'styles/globals.css';
import * as React from 'react';
import Header from 'components/Header';

export const metadata = {
  title: 'AI Web Agent',
  description: 'Generate web apps with an AI agent — frontend',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen flex flex-col">
          <Header />
          <main className="flex-1 container mx-auto px-4 py-8">{children}</main>
          <footer className="border-t py-4 text-center text-sm text-slate-500">Built with ❤️ — AI Agent Frontend</footer>
        </div>
      </body>
    </html>
  );
}