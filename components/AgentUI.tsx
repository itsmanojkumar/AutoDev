'use client';

import React, { useState } from 'react';
import axios from 'axios';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import ProjectPreview from './ProjectPreview';

export default function AgentUI() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [files, setFiles] = useState<Record<string, string> | null>(null);

  async function runAgent() {
    if (!prompt) return;
    setLoading(true);
    setLogs((l) => [...l, 'Sending prompt to AI...']);
    try {
      const base = process.env.NEXT_PUBLIC_AI_API_URL || 'http://localhost:8000/api';
      const res = await axios.post(`${base}/generate-ui`, { prompt });

      // Expect res.data.files = { 'src/pages/index.tsx': '...' }
      const data = res.data;
      if (data?.files) {
        setFiles(data.files);
        setLogs((l) => [...l, 'Files received from AI.']);
      } else if (data?.message) {
        setLogs((l) => [...l, `AI: ${data.message}`]);
      } else {
        setLogs((l) => [...l, 'No files returned.']);
      }
    } catch (err: any) {
      console.error(err);
      setLogs((l) => [...l, `Error: ${err?.message || 'Unknown'}`]);
    } finally {
      setLoading(false);
    }
  }

  async function downloadZip() {
    if (!files) return;
    const zip = new JSZip();
    Object.entries(files).forEach(([path, content]) => zip.file(path, content));
    const blob = await zip.generateAsync({ type: 'blob' });
    saveAs(blob, 'ai-generated-webapp.zip');
  }

  return (
    <div className="mt-6 space-y-4">
      <textarea
        aria-label="Describe the app you want"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder={`Example: "A Next.js e-commerce landing with Stripe checkout, product list, and contact form"`}
        className="w-full min-h-[140px] rounded border p-3"
      />

      <div className="flex gap-2">
        <button onClick={runAgent} disabled={loading} className="bg-indigo-600 text-white px-4 py-2 rounded disabled:opacity-60">
          {loading ? 'Generating...' : 'Generate app'}
        </button>
        <button onClick={downloadZip} disabled={!files} className="bg-slate-100 px-3 py-2 rounded">
          Download ZIP
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-2">
          <div className="bg-white border rounded p-4">
            <h3 className="font-semibold">Preview</h3>
            {!files ? (
              <div className="text-sm text-slate-500 mt-3">No preview yet. Generate an app to preview files.</div>
            ) : (
              <ProjectPreview files={files} />
            )}
          </div>
        </div>

        <div>
          <div className="bg-white border rounded p-4">
            <h3 className="font-semibold">Logs</h3>
            <div className="mt-2 text-xs text-slate-600">
              {logs.map((l, i) => (
                <div key={i} className="py-1">{l}</div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}