import React from 'react';


export default function Header() {
    return (
        <header className="bg-white border-b">
            <div className="container mx-auto px-4 py-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-pink-500 rounded flex items-center justify-center text-white font-bold">AI</div>
                    <div>
                        <div className="font-semibold">AI Web Agent</div>
                        <div className="text-xs text-slate-500">Scaffold web applications from prompts</div>
                    </div>
                </div>
                <nav className="flex items-center gap-3">
                    <a className="text-sm text-slate-600 hover:text-slate-900" href="#">Docs</a>
                    <a className="text-sm text-slate-600 hover:text-slate-900" href="#">Pricing</a>
                    <button className="bg-indigo-600 text-white text-sm px-3 py-1 rounded">Sign in</button>
                </nav>
            </div>
        </header>
    );
}