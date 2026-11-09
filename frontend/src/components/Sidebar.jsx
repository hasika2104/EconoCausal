import React from 'react';
import {
  LayoutDashboard,
  BarChart3,
  LineChart,
  SlidersHorizontal,
  Sparkles,
  UploadCloud,
  Home,
  ShieldCheck,
  ChevronRight,
  TrendingUp,
  Bot,
  FileText,
  HelpCircle,
  Database,
  X
} from 'lucide-react';
import { translations } from '../utils/translations';

export default function Sidebar({ currentPage, onNavigate, lang = 'en', isOpen, onClose }) {
  const t = translations[lang] || translations.en;

  const menuItems = [
    { id: 'landing', label: t.nav_landing, icon: Home, category: 'Overview' },
    { id: 'dashboard', label: t.nav_dashboard, icon: LayoutDashboard, category: 'Analytics', badge: '73.1k' },
    { id: 'upload', label: t.nav_upload, icon: UploadCloud, category: 'Data Tools', badge: 'CSV/Excel' },
    { id: 'eda', label: t.nav_eda, icon: BarChart3, category: 'Analytics' },
    { id: 'causal', label: t.nav_causal, icon: LineChart, category: 'Causal Engine', badge: 'Spec 1 & 2' },
    { id: 'simulation', label: t.nav_simulation, icon: SlidersHorizontal, category: 'Decision Engine' },
    { id: 'assistant', label: t.nav_assistant, icon: Bot, category: 'Decision Engine', badge: 'AI Chat' },
    { id: 'recommendations', label: t.nav_recommendations, icon: Sparkles, category: 'Decision Engine', badge: '100 SKUs' },
    { id: 'reports', label: t.nav_reports, icon: FileText, category: 'Reporting', badge: 'PDF/XLS' },
    { id: 'help', label: t.nav_help, icon: HelpCircle, category: 'Help & Docs' },
  ];

  const categories = ['Overview', 'Analytics', 'Data Tools', 'Causal Engine', 'Decision Engine', 'Reporting', 'Help & Docs'];

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 bg-slate-900/30 backdrop-blur-xs z-40 md:hidden"
        />
      )}

      <aside
        className={`fixed md:sticky top-0 left-0 h-screen w-64 bg-white border-r border-slate-200/90 flex flex-col shadow-xs z-50 select-none transition-transform duration-200 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
      >
        {/* Brand Header */}
        <div className="p-5 border-b border-slate-100 flex items-center justify-between">
          <div
            className="flex items-center gap-2.5 cursor-pointer"
            onClick={() => {
              onNavigate('landing');
              onClose?.();
            }}
          >
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-700 to-emerald-500 flex items-center justify-center text-white shadow-md shadow-emerald-700/20">
              <TrendingUp className="w-5 h-5 stroke-[2.5]" />
            </div>
            <div>
              <div className="font-black text-slate-900 tracking-tight leading-tight text-base flex items-center gap-1.5">
                EconoCausal
                <span className="text-[10px] px-1.5 py-0.2 rounded font-bold bg-emerald-100 text-emerald-800">AI</span>
              </div>
              <div className="text-[10px] text-slate-400 font-medium tracking-tight">
                {t.brand_subtitle}
              </div>
            </div>
          </div>

          {/* Mobile close button */}
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-600 md:hidden"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation Sections */}
        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-5">
          {categories.map((cat) => {
            const items = menuItems.filter((item) => item.category === cat);
            if (items.length === 0) return null;

            return (
              <div key={cat} className="space-y-1">
                <div className="px-3 text-[10px] font-bold tracking-wider text-slate-400 uppercase mb-1">
                  {cat}
                </div>
                {items.map((item) => {
                  const Icon = item.icon;
                  const isActive = currentPage === item.id || (item.id === 'upload' && currentPage === 'dataset');

                  return (
                    <button
                      key={item.id}
                      onClick={() => {
                        onNavigate(item.id);
                        onClose?.();
                      }}
                      className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all group ${
                        isActive
                          ? 'bg-emerald-50 text-emerald-800 shadow-2xs'
                          : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                      }`}
                    >
                      <div className="flex items-center gap-2.5 truncate">
                        <Icon
                          className={`w-4 h-4 shrink-0 transition-colors ${
                            isActive
                              ? 'text-emerald-700 stroke-[2.4]'
                              : 'text-slate-400 group-hover:text-slate-600'
                          }`}
                        />
                        <span className="truncate">{item.label}</span>
                      </div>

                      <div className="flex items-center gap-1 shrink-0">
                        {item.badge && (
                          <span
                            className={`text-[9px] px-1.5 py-0.5 rounded-full font-bold ${
                              isActive
                                ? 'bg-emerald-200/80 text-emerald-900'
                                : 'bg-slate-100 text-slate-500'
                            }`}
                          >
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

        {/* Footer info badge */}
        <div className="p-4 border-t border-slate-100 bg-slate-50/70 text-xs">
          <div className="flex items-center gap-2 text-slate-700 font-semibold mb-1">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Double ML Verified</span>
          </div>
          <div className="text-[10px] text-slate-400">
            ATE θ = +0.0107 [95% CI] • HC3 Robust SEs
          </div>
        </div>
      </aside>
    </>
  );
}
