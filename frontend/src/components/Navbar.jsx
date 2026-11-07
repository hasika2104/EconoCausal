import React from 'react';
import { Sparkles, ArrowRight, ShieldCheck, ExternalLink, Activity } from 'lucide-react';

export default function Navbar({ currentPage, onNavigate }) {
  return (
    <header className="h-16 bg-white border-b border-slate-200/80 px-6 flex items-center justify-between sticky top-0 z-20 shadow-xs">
      <div className="flex items-center gap-3">
        <h1 className="text-base font-bold text-slate-800 capitalize tracking-tight flex items-center gap-2">
          {currentPage === 'landing' && 'Overview & Architecture'}
          {currentPage === 'dashboard' && 'Retail Performance Dashboard'}
          {currentPage === 'eda' && 'Exploratory Data Analysis (EDA)'}
          {currentPage === 'causal' && 'Causal Impact Analysis (Double ML)'}
          {currentPage === 'simulation' && 'Interactive Dynamic Pricing Simulator'}
          {currentPage === 'recommendations' && 'Product-Level AI Pricing Engine'}
          {currentPage === 'dataset' && 'Dataset Explorer & Schema Inspector'}
        </h1>

        <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-100 text-emerald-800 text-xs font-medium">
          <Activity className="w-3.5 h-3.5 text-emerald-600 animate-pulse" />
          <span>Live API Connected</span>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {currentPage === 'landing' ? (
          <button
            onClick={() => onNavigate('dashboard')}
            className="flex items-center gap-2 px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg text-xs font-semibold shadow-sm transition-all"
          >
            <span>Open Dashboard</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        ) : (
          <button
            onClick={() => onNavigate('simulation')}
            className="flex items-center gap-1.5 px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-medium transition-all"
          >
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            <span>Simulate Scenario</span>
          </button>
        )}
      </div>
    </header>
  );
}
