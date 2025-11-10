'use client';

import React from 'react';
import { LiveProvider, LivePreview, LiveError } from 'react-live';
import * as ReactLib from 'react';
import * as ReactDOMLib from 'react-dom';

interface ProjectPreviewProps {
  files: Record<string, string>;
}

export default function ProjectPreview({ files }: ProjectPreviewProps) {
  // pick the first .tsx/.jsx file from files
  const frontendFile = Object.entries(files).find(([path]) =>
    path.endsWith('.tsx') || path.endsWith('.jsx')
  );

  const code = frontendFile ? frontendFile[1] : "() => (<div>No preview</div>)";

  return (
    <div className="border rounded p-4 bg-slate-50">
      <LiveProvider code={code} scope={{ React: ReactLib, ReactDOM: ReactDOMLib }}>

        <LiveError className="text-red-600 text-sm mt-2" />
        <div className="mt-2 border-t pt-2">
          <LivePreview />
        </div>
      </LiveProvider>

      {/* optional backend display */}
      {files['backend/main.py'] && (
        <div className="mt-4">
          <h4 className="font-semibold text-sm mb-1">Backend (FastAPI)</h4>
          <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto">
            {files['backend/main.py']}
          </pre>
        </div>
      )}
    </div>
  );
}
