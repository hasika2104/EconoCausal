import React from 'react';
import { ShieldAlert, Info, Github } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="mt-12 border-t border-slate-200 bg-white py-6 px-6 text-xs text-slate-500">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <span className="font-bold text-slate-700">EconoCausal</span>
          <span>—</span>
          <span>AI-Integrated Retail Pricing & Causal Decision Support System</span>
        </div>

        <div className="flex items-center gap-6">
          <div className="flex items-center gap-1.5 text-slate-500">
            <Info className="w-3.5 h-3.5 text-emerald-600" />
            <span>Double Machine Learning (DML) Spec 1 & 2 Integration</span>
          </div>
          <span className="text-slate-400">© 2026 EconoCausal</span>
        </div>
      </div>
    </footer>
  );
}
