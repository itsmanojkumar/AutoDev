import React from 'react';

export default function FloatingActions({ children }: { children?: React.ReactNode }) {
  return (
    <div className="fixed right-6 bottom-6">
      <div className="bg-white border rounded shadow p-2">{children}</div>
    </div>
  );
}