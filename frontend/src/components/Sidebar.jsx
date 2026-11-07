import React from 'react';
import {
  LayoutDashboard,
  BarChart3,
  LineChart,
  SlidersHorizontal,
  Sparkles,
  Database,
  Home,
  ShieldCheck,
  ChevronRight,
  TrendingUp,
  Cpu
} from 'lucide-react';

export default function Sidebar({ currentPage, onNavigate }) {
  const menuItems = [
    { id: 'landing', label: 'Landing Page', icon: Home, category: 'Main' },
    { id: 'dashboard', label: 'Dashboard Overview', icon: LayoutDashboard, category: 'Analytics', badge: 'Real Data' },
    { id: 'eda', label: 'Exploratory Data Analysis', icon: BarChart3, category: 'Analytics' },
    { id: 'causal', label: 'Causal Impact (DML)', icon: LineChart, category: 'Econometrics', badge: 'Spec 1 & 2' },
    { id: 'simulation', label: 'Price Simulation', icon: SlidersHorizontal, category: 'Decision Engine' },
    { id: 'recommendations', label: 'AI Recommendations', icon: Sparkles, category: 'Decision Engine', badge: '100 SKUs' },
    { id: 'dataset', label: 'Dataset Explorer', icon: Database, category: 'Data Tools' },
  ];

  const categories = ['Main', 'Analytics', 'Econometrics', 'Decision Engine', 'Data Tools'];

  return (
    <aside className="w-64 bg-white border-r border-slate-200/90 flex flex-col h-screen sticky top-0 shadow-sm z-30 select-none">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2.5 cursor-pointer" onClick={() => onNavigate('landing')}>
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-700 to-emerald-500 flex items-center justify-center text-white shadow-md shadow-emerald-700/20">
            <TrendingUp className="w-5 h-5 stroke-[2.5]" />
          </div>
          <div>
            <div className="font-extrabold text-slate-900 tracking-tight leading-tight text-base flex items-center gap-1.5">
              EconoCausal
              <span className="text-[10px] px-1.5 py-0.2 rounded font-semibold bg-emerald-100 text-emerald-800">AI</span>
            </div>
            <div className="text-[11px] text-slate-400 font-medium tracking-tight">Retail Decision Support</div>
          </div>
        </div>
      </div>

      {/* Navigation Sections */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-6">
        {categories.map((cat) => {
          const items = menuItems.filter(item => item.category === cat);
          if (items.length === 0) return null;

          return (
            <div key={cat} className="space-y-1">
              <div className="px-3 text-[11px] font-semibold tracking-wider text-slate-400 uppercase mb-1">
                {cat}
              </div>
              {items.map((item) => {
                const Icon = item.icon;
                const isActive = currentPage === item.id;

                return (
                  <button
                    key={item.id}
                    onClick={() => onNavigate(item.id)}
                    className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium transition-all group ${
                      isActive
                        ? 'bg-emerald-50 text-emerald-800 font-semibold shadow-xs'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <Icon className={`w-4 h-4 transition-colors ${
                        isActive ? 'text-emerald-700 stroke-[2.2]' : 'text-slate-400 group-hover:text-slate-600'
                      }`} />
                      <span>{item.label}</span>
                    </div>

                    <div className="flex items-center gap-1">
                      {item.badge && (
                        <span className={`text-[10px] px-1.5 py-0.5 rounded-full font-medium ${
                          isActive ? 'bg-emerald-200/70 text-emerald-900' : 'bg-slate-100 text-slate-500'
                        }`}>
                          {item.badge}
                        </span>
                      )}
                      {isActive && <ChevronRight className="w-3.5 h-3.5 text-emerald-700" />}
                    </div>
                  </button>
                );
              })}
            </div>
          );
        })}
      </div>

      {/* Causal Verification Badge & Footer Info */}
      <div className="p-4 border-t border-slate-100 bg-slate-50/70 text-xs">
        <div className="flex items-center gap-2 text-slate-700 font-medium mb-1">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>Validated DML Model</span>
        </div>
        <p className="text-[11px] text-slate-500 leading-snug">
          Robinson's partially linear model with HC3 standard errors & 73.1k transactions.
        </p>
      </div>
    </aside>
  );
}
