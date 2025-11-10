'use client';
import * as React from 'react';
import AgentUI from 'components/AgentUI'; // ✅ using alias for safety

export default function Home() {
  return (
    <div className="space-y-8">
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 items-start">
        <div className="md:col-span-2">
          <h1 className="text-3xl font-bold">
            AI Web Agent — build web applications instantly
          </h1>
          <p className="mt-2 text-slate-600">
            Describe the app you want, choose options, and the agent will generate scaffolded code and a downloadable ZIP.
          </p>
          <AgentUI />
        </div>

        <aside className="bg-white border rounded p-4">
          <h3 className="font-semibold">Tips</h3>
          <ul className="mt-2 list-disc ml-5 text-sm text-slate-600">
            <li>Be specific: frameworks, pages, API integrations and auth.</li>
            <li>Pick templates: admin dashboard, landing page, e-commerce.</li>
            <li>Use the Preview to inspect generated files before downloading.</li>
          </ul>
        </aside>
      </section>

      <section>
        <h2 className="text-xl font-semibold">Recent projects</h2>
        <p className="text-sm text-slate-600 mt-1">
          Your latest generated apps will appear here (this demo stores nothing).
        </p>
      </section>
    </div>
  );
}
