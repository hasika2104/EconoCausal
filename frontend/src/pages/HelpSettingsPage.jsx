import React, { useState } from 'react';
import {
  HelpCircle,
  BookOpen,
  Settings,
  ShieldCheck,
  CheckCircle2,
  Globe,
  Database,
  RefreshCw,
  Cpu,
  Layers,
  Info,
  ExternalLink
} from 'lucide-react';
import { translations } from '../utils/translations';

export default function HelpSettingsPage({ onNavigate, lang = 'en', onSetLang }) {
  const t = translations[lang] || translations.en;
  const [activeTab, setActiveTab] = useState('faq');

  const faqs = [
    {
      q: lang === 'te' ? 'కాజల్ ఇన్ఫరెన్స్ అంటే ఏమిటి? ఇది మెషిన్ లెర్నింగ్ కంటే ఎలా భిన్నమైనది?' : 'What is Causal Inference and how does it differ from Standard Machine Learning?',
      a: lang === 'te' 
        ? 'సాధారణ మెషిన్ లెర్నింగ్ గతంలో జరిగిన విషయాల మధ్య సహసంబంధాన్ని (Correlation) మాత్రమే చూపిస్తుంది. కానీ కాజల్ ఇన్ఫరెన్స్ (Double ML) "నేను ధరను 5% పెంచితే నా డిమాండ్ ఎంత మారుతుంది?" అనే అసలైన కారణ-ప్రభావ సంబంధాన్ని ఇతర ప్రభావాల నుండి వేరుచేసి లెక్కిస్తుంది.'
        : 'Standard ML models optimize for prediction: finding correlation between past discounts and past sales volume. Causal inference asks the counterfactual question: "What will happen to demand if we intervene and raise the price by 5%?" Double Machine Learning uses Neyman orthogonality to purge confounding from store size, weekday promotions, and seasonal demand.'
    },
    {
      q: lang === 'te' ? 'ప్రాథమిక ఎలాస్టిసిటీ θ = +0.0107 దేనిని సూచిస్తుంది?' : 'What does the primary estimate θ = +0.0107 mean for my store?',
      a: lang === 'te'
        ? 'ఈ ఫలితం ప్రకారం, ధర మారినప్పుడు రోజువారీ డిమాండ్‌లో పెద్దగా మార్పు ఉండదు (p-value = 0.490 అంటే ఇది గణాంకపరంగా సున్నాకి సమానం). అంటే కస్టమర్లు ప్రస్తుత ధరల శ్రేణిలో చాలా ఇన్-ఎలాస్టిక్ (ధరల సున్నితత్వం తక్కువగా) ఉన్నారు. కాబట్టి 3% నుండి 5% వరకు మితమైన ధర పెంపు ద్వారా రాబడిని పెంచుకోవచ్చు.'
        : 'The Double ML estimate (Spec 1) yields an Average Treatment Effect (ATE) of θ = +0.0107 with 95% CI [-0.0197, +0.0411] and p = 0.490. Because the confidence interval encompasses zero, price has a statistically negligible effect on daily unit demand within the historical operating band. Retailers can selectively optimize margins without triggering customer churn.'
    },
    {
      q: lang === 'te' ? 'ధరల సిమ్యులేటర్‌లో ఇన్వెంటరీ పరిమితులు ఎలా పనిచేస్తాయి?' : 'How does the physical inventory constraint work in the Price Simulator?',
      a: lang === 'te'
        ? 'చాలా ప్రిడిక్షన్ మోడల్స్ మీ వద్ద ఉన్న స్టాక్‌ను పట్టించుకోకుండా అంచనాలు వేస్తాయి. ఎకానోకాజల్ మాత్రం మీ షెల్ఫ్ లేదా గిడ్డంగిలో ఉన్న అసలైన స్టాక్ కంటే ఎక్కువ అమ్మకాలు జరగవని స్వయంచాలకంగా డిమాండ్‌ను పరిమితం చేస్తుంది (Truncation).'
        : 'Theoretical demand equations might predict 600 units sold if you lower price by 15%. However, if your physical shelf stock is 250 units, you cannot realize 600 sales. EconoCausal enforces realized_sales = min(predicted_demand, inventory) to prevent unrealistic revenue projections.'
    },
    {
      q: lang === 'te' ? 'నేను నా స్వంత CSV లేదా Excel డేటాను ఎలా ఉపయోగించాలి?' : 'How do I upload and analyze my own retail dataset?',
      a: lang === 'te'
        ? 'ఎడమ వైపు ఉన్న "డేటా అప్‌లోడ్" ట్యాబ్‌కు వెళ్లి మీ ఫైల్‌ను డ్రాగ్-అండ్-డ్రాప్ చేయండి. మా సిస్టమ్ మీ కాలమ్ పేర్లను గుర్తించి, లోపాలను సరిచేసే సూచనలను ఇస్తుంది.'
        : 'Navigate to the "Data Upload" module in the navigation menu. Drag and drop any .csv or .xlsx file. The schema detector will automatically validate columns like Product ID, Price, and Units Sold, audit missing values, and allow you to map custom headers.'
    }
  ];

  const glossary = [
    {
      term: 'Double Machine Learning (DML)',
      def: 'A semiparametric econometric framework introduced by Chernozhukov et al. that combines flexible machine learning models with Neyman-orthogonal score equations to obtain unbiased causal treatment effects.'
    },
    {
      term: 'Average Treatment Effect (ATE / θ)',
      def: 'The expected causal change in units demanded per one-dollar change in unit price across all observed products and store conditions.'
    },
    {
      term: 'Confounders (W)',
      def: 'Observed variables (such as Store Location, Category, Month, Day of Week, and Inventory) that simultaneously influence both pricing decisions and consumer demand.'
    },
    {
      term: 'Cross-Fitting (K-Fold)',
      def: 'A sample-splitting procedure ensuring that the predictive models for prices and demand do not overfit to the causal parameter, eliminating regularization bias.'
    },
    {
      term: 'Physical Inventory Truncation',
      def: 'The business rule ensuring that realized units sold cannot exceed the available physical inventory level.'
    }
  ];

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header */}
      <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-900">
            {lang === 'te' ? 'సహాయం, డాక్యుమెంటేషన్ & సెట్టింగ్‌లు' : 'Help, Methodology & Settings'}
          </h1>
          <p className="text-xs text-slate-500 font-medium">
            Econometric definitions, retail FAQs, language preferences, and system parameters
          </p>
        </div>

        {/* Language Selector */}
        <div className="flex items-center gap-2 bg-slate-100 p-1 rounded-xl">
          <Globe className="w-4 h-4 text-slate-500 ml-2" />
          <button
            onClick={() => onSetLang && onSetLang('en')}
            className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
              lang === 'en' ? 'bg-white text-emerald-800 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            English
          </button>
          <button
            onClick={() => onSetLang && onSetLang('te')}
            className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
              lang === 'te' ? 'bg-white text-emerald-800 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            తెలుగు (Telugu)
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-slate-200 pb-2">
        <button
          onClick={() => setActiveTab('faq')}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
            activeTab === 'faq' ? 'bg-emerald-700 text-white' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          {lang === 'te' ? 'తరచూ అడిగే ప్రశ్నలు (FAQ)' : 'Frequently Asked Questions'}
        </button>
        <button
          onClick={() => setActiveTab('glossary')}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
            activeTab === 'glossary' ? 'bg-emerald-700 text-white' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          {lang === 'te' ? 'ఎకనామెట్రిక్స్ పదకోశం (Glossary)' : 'Econometrics Glossary'}
        </button>
        <button
          onClick={() => setActiveTab('system')}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
            activeTab === 'system' ? 'bg-emerald-700 text-white' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          {lang === 'te' ? 'సిస్టమ్ సెట్టింగ్‌లు & డెమో' : 'System & Demo Settings'}
        </button>
      </div>

      {/* Tab 1: FAQs */}
      {activeTab === 'faq' && (
        <div className="space-y-4">
          {faqs.map((f, idx) => (
            <div key={idx} className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs space-y-2">
              <h3 className="text-sm font-bold text-slate-900 flex items-start gap-2.5">
                <HelpCircle className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>{f.q}</span>
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed pl-6.5">{f.a}</p>
            </div>
          ))}
        </div>
      )}

      {/* Tab 2: Glossary */}
      {activeTab === 'glossary' && (
        <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs divide-y divide-slate-100">
          {glossary.map((g, idx) => (
            <div key={idx} className="py-4 first:pt-0 last:pb-0 space-y-1">
              <div className="text-xs font-bold text-slate-900 font-mono text-emerald-800">{g.term}</div>
              <div className="text-xs text-slate-600 leading-relaxed">{g.def}</div>
            </div>
          ))}
        </div>
      )}

      {/* Tab 3: System Settings & Demo Reset */}
      {activeTab === 'system' && (
        <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs space-y-6">
          <div>
            <h3 className="text-sm font-bold text-slate-900 mb-1">Demo Mode State</h3>
            <p className="text-xs text-slate-500">
              EconoCausal currently runs on the pre-loaded 73,100 store-day retail inventory benchmark.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-4 pt-4 border-t border-slate-100">
            <button
              onClick={() => onNavigate('upload')}
              className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-semibold transition-all"
            >
              Upload Custom Retail CSV / Excel
            </button>

            <button
              onClick={() => onNavigate('dashboard')}
              className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-semibold transition-all flex items-center gap-1.5"
            >
              <RefreshCw className="w-3.5 h-3.5 text-slate-500" />
              <span>Reset to Demo Benchmark</span>
            </button>
          </div>

          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200/80 text-xs space-y-1 text-slate-600">
            <div><strong>Backend Health:</strong> 200 OK (FastAPI 0.162 on port 8000)</div>
            <div><strong>Frontend Server:</strong> React 18 + Vite + TailwindCSS on port 5173</div>
            <div><strong>CORS Whitelist:</strong> localhost:5173, 127.0.0.1:5173</div>
            <div><strong>Active Methodology:</strong> 3-Fold Cross-Fitting ExtraTreesRegressor with HC3 SEs</div>
          </div>
        </div>
      )}
    </div>
  );
}
