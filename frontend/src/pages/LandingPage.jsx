import React from 'react';
import {
  ArrowRight,
  TrendingUp,
  ShieldCheck,
  Cpu,
  BarChart3,
  SlidersHorizontal,
  Sparkles,
  Layers,
  AlertTriangle,
  CheckCircle2,
  HelpCircle,
  Database,
  FileSpreadsheet,
  LineChart,
  Bot,
  Store,
  DollarSign,
  PieChart,
  Globe,
  Lock,
  BookOpen
} from 'lucide-react';
import { translations } from '../utils/translations';

export default function LandingPage({ onNavigate, lang = 'en', onSetLang }) {
  const t = translations[lang] || translations.en;

  const howItWorksSteps = [
    {
      step: '01',
      title: lang === 'te' ? 'డేటా అప్‌లోడ్ & వ్యాలిడేషన్' : 'Data Ingestion & Quality Audit',
      desc: lang === 'te' 
        ? 'CSV లేదా Excel ఫైల్‌ను అప్‌లోడ్ చేయండి. ఆటోమేటిక్ లోపం గుర్తింపు మరియు కాలమ్ మ్యాపింగ్ చేయబడుతుంది.' 
        : 'Upload sales records via CSV or Excel. The engine scans for missing values, duplicates, and aligns schema automatically.'
    },
    {
      step: '02',
      title: lang === 'te' ? 'కాజల్ DML విశ్లేషణ' : 'Double Machine Learning Isolation',
      desc: lang === 'te'
        ? 'స్టోర్, కేటగిరీ, సీజన్ మరియు ఇన్వెంటరీ కారకాలను నియంత్రించి అసలైన ధర సున్నితత్వాన్ని లెక్కిస్తుంది.'
        : 'Orthogonal residualization separates actual consumer price elasticity from store location, seasonality, and promotional noise.'
    },
    {
      step: '03',
      title: lang === 'te' ? 'ఇంటరాక్టివ్ ధర సిమ్యులేషన్' : 'Constrained Pricing Simulation',
      desc: lang === 'te'
        ? 'వివిధ ధరలను పరీక్షించండి. ఇన్వెంటరీ పరిమితులు మరియు లాభ మార్జిన్‌లను తక్షణమే సరిపోల్చండి.'
        : 'Experiment with price changes while respecting shelf stock limits, confidence bounds, and unit profitability.'
    },
    {
      step: '04',
      title: lang === 'te' ? 'AI సిఫార్సులు & నివేదికలు' : 'Actionable Decisions & Reporting',
      desc: lang === 'te'
        ? 'ప్రతి వస్తువుకు అనువైన ధర సిఫార్సులు మరియు ఆడిట్ చేయదగిన ఎగ్జిక్యూటివ్ నివేదికలను పొందండి.'
        : 'Receive SKU-level pricing strategies with audit logs, and export multi-sheet Excel, CSV, or PDF reports.'
    }
  ];

  const keyFeatures = [
    {
      icon: LineChart,
      title: lang === 'te' ? 'కాజల్ ఇన్ఫరెన్స్ ఇంజిన్' : 'Causal Price Impact Engine',
      desc: lang === 'te' ? 'Double ML (DML) ద్వారా ధర మార్పుల అసలైన డిమాండ్ ప్రభావాన్ని లెక్కిస్తుంది.' : 'State-of-the-art Double ML isolates true elasticity across 73,100+ store-day observations with 95% confidence intervals.'
    },
    {
      icon: SlidersHorizontal,
      title: lang === 'te' ? 'ఇంటరాక్టివ్ ధరల సిమ్యులేటర్' : 'Dynamic Scenario Simulator',
      desc: lang === 'te' ? 'ధరలను మార్చి డిమాండ్, రాబడి మరియు లాభాలను ముందుగానే ఊహించండి.' : 'Compare -10%, -5%, +5%, +10% price moves with automated shelf inventory constraint truncation.'
    },
    {
      icon: Bot,
      title: lang === 'te' ? 'AI రిటైల్ ప్రైసింగ్ అసిస్టెంట్' : 'AI-Powered Pricing Assistant',
      desc: lang === 'te' ? 'మీ అమ్మకాలపై ప్రశ్నలు అడగండి, నిజమైన గణాంకాలతో తక్షణ సమాధానాలు పొందండి.' : 'Ask natural language questions about revenue leaders, 5% price shock consequences, and demand trends.'
    },
    {
      icon: Sparkles,
      title: lang === 'te' ? '100 SKU నిర్ణయాల సిఫార్సులు' : 'Automated SKU Recommendations',
      desc: lang === 'te' ? 'ఇన్వెంటరీ మరియు ఎలాస్టిసిటీ ఆధారంగా ప్రతి వస్తువుకు సురక్షితమైన ధర సూచనలు.' : 'Auditable product-level advice balancing stock velocity, margins, and historical price volatility guardrails.'
    },
    {
      icon: FileSpreadsheet,
      title: lang === 'te' ? 'డేటా ఆడిట్ & క్లీనింగ్ టూల్' : 'Data Quality & Schema Mapper',
      desc: lang === 'te' ? 'లోపాలు ఉన్న డేటాను గుర్తించి సరిచేస్తుంది మరియు శుభ్రపరిచిన ఫైల్‌ను డౌన్‌లోడ్ చేసుకోవచ్చు.' : 'Auto-detects missing fields, invalid values, negative stock, and exports cleaned ready-to-analyze datasets.'
    },
    {
      icon: Database,
      title: lang === 'te' ? 'డెమో మోడ్ & ఎగ్జిక్యూటివ్ రిపోర్ట్స్' : 'Multi-Format Executive Reports',
      desc: lang === 'te' ? 'వన్-క్లిక్ డెమో మోడ్ మరియు ఎక్సెల్ / పీడీఎఫ్ రిపోర్ట్ ఎగుమతి సదుపాయం.' : 'Instant exploration with benchmark retail data, and one-click multi-tab Excel and printable executive reports.'
    }
  ];

  const retailerBenefits = [
    {
      title: lang === 'te' ? 'నష్టాలను నివారించండి (Prevent Margin Dilution)' : 'Eliminate Costly False Promotions',
      desc: lang === 'te'
        ? 'డిస్కౌంట్లు నిజంగా అమ్మకాలను పెంచుతాయో లేదో తెలుసుకోండి. అనవసరమైన ఆఫర్లతో మార్జిన్లను కోల్పోకండి.'
        : 'Stop discounting high-velocity products whose volume was driven by seasonality rather than price cuts.'
    },
    {
      title: lang === 'te' ? 'స్టాక్-అవుట్ సమస్యలను ఆపండి (Inventory Safeguards)' : 'Inventory-Aware Optimization',
      desc: lang === 'te'
        ? 'మీ వద్ద ఉన్న స్టాక్ కంటే ఎక్కువ డిమాండ్ వచ్చినప్పుడు ఉత్పన్నమయ్యే కొరతను ముందే హెచ్చరిస్తుంది.'
        : 'Unlike unconstrained AI models, EconoCausal caps simulated sales at physical warehouse availability.'
    },
    {
      title: lang === 'te' ? 'ఆడిట్ చేయదగిన నిర్ణయాలు (Transparent & Auditable)' : 'Auditable, Regulated Decision Support',
      desc: lang === 'te'
        ? 'బ్లాక్-బాక్స్ మోడల్స్ కాకుండా స్పష్టమైన అంచనాలు మరియు పరిమితులతో నిర్ణయాలు తీసుకోండి.'
        : 'Every recommendation includes statistical p-values, standard errors, and clear business guardrails.'
    },
    {
      title: lang === 'te' ? 'అందరికీ సులభమైన ఇంటర్‌ఫేస్ (Accessible for All)' : 'Built for Business Owners & Analysts',
      desc: lang === 'te'
        ? 'కోడింగ్ లేదా డేటా సైన్స్ జ్ఞానం అవసరం లేదు. గ్రాఫ్‌లు మరియు సాధారణ వివరణలతో సులభంగా అర్థమవుతుంది.'
        : 'Zero coding required. Clean charts, plain-English KPI explanations, and bilingual Telugu/English support.'
    }
  ];

  return (
    <div className="space-y-16 pb-16">
      {/* 1. Header / Tagline Hero Card */}
      <section className="relative overflow-hidden bg-white border border-slate-200/90 rounded-3xl p-8 md:p-14 shadow-sm">
        {/* Soft emerald background glows */}
        <div className="absolute top-0 right-0 -mr-20 -mt-20 w-[420px] h-[420px] bg-emerald-100/60 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 right-1/3 -mb-20 w-80 h-80 bg-teal-100/40 rounded-full blur-3xl pointer-events-none" />

        <div className="relative max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold mb-6">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>{lang === 'te' ? 'ఎంటర్‌ప్రైజ్ కాజల్ AI ప్లాట్‌ఫారమ్' : 'Enterprise AI-Powered Retail Pricing Platform'}</span>
          </div>

          <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 tracking-tight leading-[1.18] mb-6">
            {t.hero_title_1}{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-700 via-teal-700 to-emerald-600">
              {t.hero_title_highlight}
            </span>
          </h1>

          <p className="text-base md:text-lg text-slate-600 leading-relaxed mb-8">
            {t.hero_desc}
          </p>

          <div className="flex flex-wrap items-center gap-4">
            <button
              onClick={() => onNavigate('dashboard')}
              className="flex items-center gap-2.5 px-6 py-3.5 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-sm font-semibold shadow-md shadow-emerald-700/20 transition-all transform hover:-translate-y-0.5"
            >
              <span>{t.btn_get_started}</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={() => onNavigate('dashboard')}
              className="flex items-center gap-2 px-6 py-3.5 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 rounded-xl text-sm font-semibold transition-all shadow-xs"
            >
              <Store className="w-4 h-4 text-emerald-600" />
              <span>{t.btn_try_demo}</span>
            </button>

            <button
              onClick={() => onNavigate('simulation')}
              className="flex items-center gap-2 px-6 py-3.5 bg-emerald-50 hover:bg-emerald-100/80 text-emerald-800 border border-emerald-200 rounded-xl text-sm font-semibold transition-all"
            >
              <SlidersHorizontal className="w-4 h-4 text-emerald-700" />
              <span>{t.btn_simulate}</span>
            </button>
          </div>
        </div>

        {/* Highlight Stats Strip */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-12 pt-8 border-t border-slate-100">
          <div className="bg-slate-50/80 p-4 rounded-xl border border-slate-100">
            <div className="text-2xl font-black text-slate-900">73,100</div>
            <div className="text-xs text-slate-500 font-medium mt-1">
              {lang === 'te' ? 'స్టోర్-రోజు రికార్డులు' : 'Store-Day Observations'}
            </div>
          </div>
          <div className="bg-slate-50/80 p-4 rounded-xl border border-slate-100">
            <div className="text-2xl font-black text-slate-900">+0.0107</div>
            <div className="text-xs text-slate-500 font-medium mt-1">
              {lang === 'te' ? 'ప్రాథమిక కాజల్ ప్రభావం (θ)' : 'Primary DML Elasticity (θ)'}
            </div>
          </div>
          <div className="bg-slate-50/80 p-4 rounded-xl border border-slate-100">
            <div className="text-2xl font-black text-slate-900">18 Specs</div>
            <div className="text-xs text-slate-500 font-medium mt-1">
              {lang === 'te' ? 'రోబస్ట్‌నెస్ టెస్టులు' : 'Model Robustness Specs'}
            </div>
          </div>
          <div className="bg-slate-50/80 p-4 rounded-xl border border-slate-100">
            <div className="text-2xl font-black text-slate-900">100 SKUs</div>
            <div className="text-xs text-slate-500 font-medium mt-1">
              {lang === 'te' ? 'AI ధరల సిఫార్సులు' : 'Product Pricing Strategies'}
            </div>
          </div>
        </div>
      </section>

      {/* 2. Core Business Problem: Correlation vs Causality */}
      <section className="bg-white rounded-3xl border border-slate-200/90 p-8 md:p-12 shadow-xs">
        <div className="max-w-3xl mb-8">
          <div className="text-xs font-bold uppercase tracking-wider text-emerald-700 mb-2">
            {lang === 'te' ? 'రిటైల్ సమస్య విశ్లేషణ' : 'The Retail Pricing Challenge'}
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold text-slate-900">
            {lang === 'te' ? 'సాంప్రదాయ మెషిన్ లెర్నింగ్ ఎందుకు తప్పుదారి పట్టిస్తుంది?' : 'Why Standard ML Fails in Retail Pricing'}
          </h2>
          <p className="text-sm md:text-base text-slate-600 mt-2">
            {lang === 'te' 
              ? 'సాధారణ ప్రిడిక్షన్ మోడల్స్ సహసంబంధాన్ని (Correlation) కారణం (Causation)గా భావించి అనవసర డిస్కౌంట్లతో వ్యాపార రాబడిని తగ్గిస్తాయి.'
              : 'Standard predictive regression mistakes promotional discounts and weekend foot traffic for customer price sensitivity, causing margin dilution.'}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-6 rounded-2xl border border-amber-200 bg-amber-50/60">
            <div className="flex items-center gap-2.5 text-amber-900 font-bold text-base mb-4">
              <AlertTriangle className="w-5 h-5 text-amber-600" />
              <span>{lang === 'te' ? 'సాధారణ ప్రిడిక్టివ్ మోడల్ (The Trap)' : 'Traditional Predictive ML (The Trap)'}</span>
            </div>
            <ul className="space-y-3 text-xs md:text-sm text-slate-700 leading-relaxed">
              <li className="flex items-start gap-2.5">
                <span className="text-amber-600 font-bold text-base leading-none">✕</span>
                <span><strong>Confounder Bias:</strong> Observes higher sales on weekends when stores ran promotions, and falsely claims lower prices drove the volume.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="text-amber-600 font-bold text-base leading-none">✕</span>
                <span><strong>No Physical Safeguards:</strong> Suggests dropping prices to sell 500 units even if shelf inventory is strictly capped at 200 units.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="text-amber-600 font-bold text-base leading-none">✕</span>
                <span><strong>Margin Erosion:</strong> Leads retailers into unnecessary price wars and price erosion.</span>
              </li>
            </ul>
          </div>

          <div className="p-6 rounded-2xl border border-emerald-200 bg-emerald-50/60">
            <div className="flex items-center gap-2.5 text-emerald-900 font-bold text-base mb-4">
              <CheckCircle2 className="w-5 h-5 text-emerald-600" />
              <span>{lang === 'te' ? 'ఎకానోకాజల్ DML పరిష్కారం' : 'EconoCausal Double ML (The Solution)'}</span>
            </div>
            <ul className="space-y-3 text-xs md:text-sm text-slate-700 leading-relaxed">
              <li className="flex items-start gap-2.5">
                <span className="text-emerald-700 font-bold text-base leading-none">✓</span>
                <span><strong>Causal Residualization:</strong> Controls for store size, location, calendar cycles, and category baselines before measuring price sensitivity.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="text-emerald-700 font-bold text-base leading-none">✓</span>
                <span><strong>Physical Inventory Constraints:</strong> Automatically truncates demand simulations at actual warehouse supply.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="text-emerald-700 font-bold text-base leading-none">✓</span>
                <span><strong>Auditable Confidence Bounds:</strong> Reports 95% statistical confidence intervals and warns when price changes extrapolate beyond historical bounds.</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* 3. How It Works (4 Steps) */}
      <section className="space-y-8">
        <div className="text-center max-w-2xl mx-auto">
          <div className="text-xs font-bold uppercase tracking-wider text-emerald-700 mb-2">
            {lang === 'te' ? 'ఇది ఎలా పనిచేస్తుంది?' : 'Step-by-Step Architecture'}
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold text-slate-900">
            {lang === 'te' ? 'డేటా నుండి నిర్ణయాల వరకు 4 దశలు' : 'How EconoCausal Drives Decisions'}
          </h2>
          <p className="text-sm text-slate-600 mt-2">
            {lang === 'te' ? 'సాధారణ వ్యాపారులకు మరియు విశ్లేషకులకు సులభమైన వర్క్‌ఫ్లో.' : 'A transparent, auditable pipeline taking you from raw CSV/Excel tables to verified pricing actions.'}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {howItWorksSteps.map((step) => (
            <div key={step.step} className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs relative">
              <div className="text-xs font-black text-emerald-700 bg-emerald-50 w-9 h-9 rounded-xl flex items-center justify-center mb-4">
                {step.step}
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-2">{step.title}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">{step.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 4. Key Platform Features */}
      <section className="space-y-8">
        <div className="text-center max-w-2xl mx-auto">
          <div className="text-xs font-bold uppercase tracking-wider text-emerald-700 mb-2">
            {lang === 'te' ? 'ప్రధాన ఫీచర్లు' : 'Platform Capabilities'}
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold text-slate-900">
            {lang === 'te' ? 'ఆధునిక AI మరియు కాజల్ టెక్నాలజీ' : 'Comprehensive Pricing Toolset'}
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {keyFeatures.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <div key={idx} className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-xs hover:border-emerald-300 transition-all group">
                <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center mb-4 group-hover:bg-emerald-700 group-hover:text-white transition-all">
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-slate-900 mb-2">{feat.title}</h3>
                <p className="text-xs text-slate-600 leading-relaxed">{feat.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* 5. Benefits for Retailers & Business Owners */}
      <section className="bg-gradient-to-br from-emerald-800 to-teal-900 rounded-3xl p-8 md:p-12 text-white shadow-md">
        <div className="max-w-3xl mb-8">
          <div className="text-xs font-bold uppercase tracking-wider text-emerald-300 mb-2">
            {lang === 'te' ? 'వ్యాపార ప్రయోజనాలు' : 'Why Retailers Choose EconoCausal'}
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold">
            {lang === 'te' ? 'మీ రిటైల్ వ్యాపారానికి గరిష్ట లాభం' : 'Engineered for Real-World Retail Realities'}
          </h2>
          <p className="text-sm md:text-base text-emerald-100 mt-2">
            {lang === 'te' ? 'అంచనాలు మాత్రమే కాదు, ఆచరణాత్మకమైన వ్యాపార పరిష్కారాలు.' : 'Moving beyond theoretical curves to practical, profit-safe pricing execution.'}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {retailerBenefits.map((ben, idx) => (
            <div key={idx} className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/15">
              <h3 className="text-base font-bold text-white mb-2">{ben.title}</h3>
              <p className="text-xs md:text-sm text-emerald-100/90 leading-relaxed">{ben.desc}</p>
            </div>
          ))}
        </div>

        <div className="mt-10 pt-8 border-t border-white/20 flex flex-wrap items-center justify-between gap-4">
          <div className="text-xs text-emerald-200">
            {lang === 'te' ? 'ఉచితంగా డెమో ప్రారంభించండి. క్రెడిట్ కార్డు అవసరం లేదు.' : 'Ready to explore? Try the interactive live demo immediately.'}
          </div>
          <button
            onClick={() => onNavigate('dashboard')}
            className="px-6 py-3 bg-white text-emerald-900 hover:bg-emerald-50 rounded-xl text-xs font-bold shadow-md transition-all flex items-center gap-2"
          >
            <span>{t.btn_get_started}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </section>

      {/* 6. Footer Navigation Links */}
      <footer className="pt-8 border-t border-slate-200 flex flex-col md:flex-row items-center justify-between text-xs text-slate-500 gap-4">
        <div>
          © {new Date().getFullYear()} <strong>EconoCausal</strong>. {t.footer_text}
        </div>
        <div className="flex items-center gap-6">
          <button onClick={() => onNavigate('help')} className="hover:text-emerald-700 transition-colors">
            {lang === 'te' ? 'సహాయం & మార్గదర్శిని' : 'Documentation & FAQ'}
          </button>
          <button onClick={() => onNavigate('reports')} className="hover:text-emerald-700 transition-colors">
            {lang === 'te' ? 'నివేదికలు' : 'Reports'}
          </button>
          <button onClick={() => onNavigate('assistant')} className="hover:text-emerald-700 transition-colors">
            {lang === 'te' ? 'AI అసిస్టెంట్' : 'AI Assistant'}
          </button>
        </div>
      </footer>
    </div>
  );
}
