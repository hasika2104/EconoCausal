import React from 'react';
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  ExternalLink,
  Activity,
  Menu,
  Globe,
  SlidersHorizontal,
  Bot
} from 'lucide-react';
import { translations } from '../utils/translations';

export default function Navbar({ currentPage, onNavigate, lang = 'en', onSetLang, onToggleSidebar }) {
  const t = translations[lang] || translations.en;

  const pageTitles = {
    landing: lang === 'te' ? 'ప్లాట్‌ఫారమ్ అవలోకనం & ఆర్కిటెక్చర్' : 'Platform Overview & Architecture',
    dashboard: lang === 'te' ? 'రిటైల్ పెర్ఫార్మెన్స్ డాష్‌బోర్డ్' : 'Retail Performance Dashboard',
    upload: lang === 'te' ? 'డేటా అప్‌లోడ్ & క్వాలిటీ ఆడిట్' : 'Data Ingestion & Schema Validator',
    dataset: lang === 'te' ? 'డేటా అప్‌లోడ్ & క్వాలిటీ ఆడిట్' : 'Data Ingestion & Schema Validator',
    eda: lang === 'te' ? 'అమ్మకాల సమగ్ర విశ్లేషణ (EDA)' : 'Exploratory Sales Analytics (EDA)',
    causal: lang === 'te' ? 'కాజల్ ధర ప్రభావ విశ్లేషణ (Double ML)' : 'Causal Price Impact Analysis (Double ML)',
    simulation: lang === 'te' ? 'ఇంటరాక్టివ్ డైనమిక్ ప్రైసింగ్ సిమ్యులేటర్' : 'Interactive Constrained Price Simulator',
    assistant: lang === 'te' ? 'AI రిటైల్ ప్రైసింగ్ అసిస్టెంట్' : 'AI Retail Pricing Assistant',
    recommendations: lang === 'te' ? 'AI ప్రొడక్ట్ ప్రైసింగ్ ఇంజిన్' : '100-SKU AI Recommendation Engine',
    reports: lang === 'te' ? 'ఎగ్జిక్యూటివ్ రిపోర్ట్ జనరేషన్' : 'Executive Business Report Generation',
    help: lang === 'te' ? 'సహాయం, డాక్యుమెంటేషన్ & సెట్టింగ్‌లు' : 'Help, Methodology & Settings'
  };

  return (
    <header className="h-16 bg-white border-b border-slate-200/90 px-4 md:px-8 flex items-center justify-between sticky top-0 z-30 shadow-2xs">
      <div className="flex items-center gap-3">
        {/* Mobile Hamburger */}
        <button
          onClick={onToggleSidebar}
          className="p-1.5 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 md:hidden"
        >
          <Menu className="w-5 h-5" />
        </button>

        <h1 className="text-sm md:text-base font-bold text-slate-800 tracking-tight">
          {pageTitles[currentPage] || pageTitles.dashboard}
        </h1>

        <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-[11px] font-semibold">
          <Activity className="w-3 h-3 text-emerald-600 animate-pulse" />
          <span>{t.live_badge}</span>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Language Switcher */}
        <div className="flex items-center bg-slate-100 p-0.5 rounded-lg text-xs font-semibold">
          <button
            onClick={() => onSetLang && onSetLang('en')}
            className={`px-2 py-1 rounded-md transition-all ${
              lang === 'en' ? 'bg-white text-emerald-800 shadow-2xs' : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            EN
          </button>
          <button
            onClick={() => onSetLang && onSetLang('te')}
            className={`px-2 py-1 rounded-md transition-all ${
              lang === 'te' ? 'bg-white text-emerald-800 shadow-2xs' : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            తెలుగు
          </button>
        </div>

        {/* Quick Action Button */}
        {currentPage === 'landing' ? (
          <button
            onClick={() => onNavigate('dashboard')}
            className="flex items-center gap-1.5 px-3.5 py-1.5 bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg text-xs font-semibold shadow-xs transition-all"
          >
            <span>{t.btn_open_dashboard}</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        ) : (
          <button
            onClick={() => onNavigate('assistant')}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 rounded-lg text-xs font-semibold transition-all"
          >
            <Bot className="w-3.5 h-3.5 text-emerald-700" />
            <span className="hidden sm:inline">Ask AI Analyst</span>
          </button>
        )}
      </div>
    </header>
  );
}
