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
  Database
} from 'lucide-react';

export default function LandingPage({ onNavigate }) {
  return (
    <div className="space-y-12 pb-12">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-white border border-slate-200/80 rounded-2xl p-8 md:p-12 shadow-xs">
        <div className="absolute top-0 right-0 -mr-16 -mt-16 w-96 h-96 bg-emerald-50 rounded-full blur-3xl opacity-60 pointer-events-none" />
        <div className="absolute bottom-0 right-1/4 -mb-16 w-64 h-64 bg-teal-50 rounded-full blur-2xl opacity-40 pointer-events-none" />

        <div className="relative max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold mb-6">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Empirical Retail Econometrics & Causal ML</span>
          </div>

          <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 tracking-tight leading-[1.15] mb-6">
            Smarter Pricing Decisions Through <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-700 to-teal-600">Causal AI</span>
          </h1>

          <p className="text-base md:text-lg text-slate-600 leading-relaxed mb-8">
            Standard machine learning models mistake historical correlations for true customer price sensitivity, leading to severe margin dilution. <strong>EconoCausal</strong> isolates the true causal price elasticity using <strong>Double Machine Learning (DML)</strong>, enforcing physical inventory constraints and business guardrails to deliver auditable pricing recommendations.
          </p>

          <div className="flex flex-wrap items-center gap-4">
            <button
              onClick={() => onNavigate('dashboard')}
              className="flex items-center gap-2.5 px-6 py-3 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-sm font-semibold shadow-md shadow-emerald-700/20 transition-all transform hover:-translate-y-0.5"
            >
              <span>Explore Dashboard</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={() => onNavigate('causal')}
              className="flex items-center gap-2 px-6 py-3 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 rounded-xl text-sm font-semibold transition-all shadow-xs"
            >
              <span>Learn How DML Works</span>
            </button>
          </div>
        </div>

        {/* Highlight Stats Strip */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-12 pt-8 border-t border-slate-100">
          <div>
            <div className="text-2xl font-bold text-slate-900">73,100</div>
            <div className="text-xs text-slate-500 font-medium mt-0.5">Store-Day Records Cleaned</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-900">18 Specs</div>
            <div className="text-xs text-slate-500 font-medium mt-0.5">DML Robustness Checks</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-900">+0.0107</div>
            <div className="text-xs text-slate-500 font-medium mt-0.5">Estimated Primary ATE (θ)</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-900">100 SKUs</div>
            <div className="text-xs text-slate-500 font-medium mt-0.5">AI Product Recommendations</div>
          </div>
        </div>
      </section>

      {/* The Core Retail Problem Card: Correlation vs Causality */}
      <section className="bg-white rounded-2xl border border-slate-200/80 p-8 shadow-xs">
        <div className="max-w-3xl mb-6">
          <div className="text-xs font-semibold uppercase tracking-wider text-emerald-700 mb-1">
            The Business Problem
          </div>
          <h2 className="text-2xl font-bold text-slate-900">
            The Predictive Trap in Traditional Retail Pricing
          </h2>
          <p className="text-sm text-slate-600 mt-2">
            Why optimizing prices on standard regression models causes unintended revenue loss and customer defection.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-5 rounded-xl border border-amber-200/80 bg-amber-50/50">
            <div className="flex items-center gap-2 text-amber-900 font-bold text-sm mb-3">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <span>Standard Supervised ML (The Trap)</span>
            </div>
            <ul className="space-y-2.5 text-xs text-slate-700 leading-relaxed">
              <li className="flex items-start gap-2">
                <span className="text-amber-600 font-bold">✕</span>
                <span><strong>Models Correlations:</strong> Captures E[Sales | Price], mistaking high sales of luxury goods for positive price elasticity.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-amber-600 font-bold">✕</span>
                <span><strong>Ignores Confounders:</strong> Stores with higher footfall naturally charge higher prices and sell higher volume.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-amber-600 font-bold">✕</span>
                <span><strong>Disregards Stockouts:</strong> Misses that sales are physically bounded by inventory availability on shelves.</span>
              </li>
            </ul>
          </div>

          <div className="p-5 rounded-xl border border-emerald-200/80 bg-emerald-50/50">
            <div className="flex items-center gap-2 text-emerald-900 font-bold text-sm mb-3">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Double Machine Learning (EconoCausal)</span>
            </div>
            <ul className="space-y-2.5 text-xs text-slate-700 leading-relaxed">
              <li className="flex items-start gap-2">
                <span className="text-emerald-700 font-bold">✓</span>
                <span><strong>Residualizes Confounders:</strong> Partial-outs store, product, category, region, and calendar fixed effects.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-700 font-bold">✓</span>
                <span><strong>Unbiased Treatment Effect:</strong> Estimates orthogonal price elasticity with Neyman orthogonality.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-700 font-bold">✓</span>
                <span><strong>Hard Inventory Constraints:</strong> Enforces Sales = min(Demand, Inventory) to prevent phantom volume gains.</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* 4 Feature Pillars */}
      <section className="space-y-6">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-emerald-700 mb-1">
            System Architecture
          </div>
          <h2 className="text-2xl font-bold text-slate-900">
            Comprehensive Analytical & Decision Pipeline
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Card 1 */}
          <div 
            onClick={() => onNavigate('eda')}
            className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-xs hover:border-emerald-300 hover:shadow-md transition-all cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-lg bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-700 mb-4 group-hover:scale-105 transition-transform">
              <BarChart3 className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 text-base mb-1.5 flex items-center justify-between">
              <span>Exploratory EDA</span>
              <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600 transition-colors" />
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Deep dive into price/demand distributions, correlation matrices, seasonal seasonality, and missing variable analysis.
            </p>
          </div>

          {/* Card 2 */}
          <div 
            onClick={() => onNavigate('causal')}
            className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-xs hover:border-emerald-300 hover:shadow-md transition-all cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-lg bg-teal-50 border border-teal-100 flex items-center justify-center text-teal-700 mb-4 group-hover:scale-105 transition-transform">
              <Cpu className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 text-base mb-1.5 flex items-center justify-between">
              <span>Double ML (DML)</span>
              <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-teal-600 transition-colors" />
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Orthogonalized causal estimation isolating θ = 0.0107 across 18 specifications with HC3 confidence intervals.
            </p>
          </div>

          {/* Card 3 */}
          <div 
            onClick={() => onNavigate('simulation')}
            className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-xs hover:border-emerald-300 hover:shadow-md transition-all cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-lg bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-700 mb-4 group-hover:scale-105 transition-transform">
              <SlidersHorizontal className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 text-base mb-1.5 flex items-center justify-between">
              <span>Price Simulator</span>
              <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600 transition-colors" />
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Interactive counterfactual scenario engine testing candidate price changes subject to physical stock limits.
            </p>
          </div>

          {/* Card 4 */}
          <div 
            onClick={() => onNavigate('recommendations')}
            className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-xs hover:border-emerald-300 hover:shadow-md transition-all cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-lg bg-teal-50 border border-teal-100 flex items-center justify-center text-teal-700 mb-4 group-hover:scale-105 transition-transform">
              <Sparkles className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 text-base mb-1.5 flex items-center justify-between">
              <span>AI Recommendations</span>
              <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-teal-600 transition-colors" />
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Granular SKU recommendations across 100 segments with uncertainty indicators and managerial explanations.
            </p>
          </div>
        </div>
      </section>

      {/* Methodology Section */}
      <section className="bg-white rounded-2xl border border-slate-200/90 p-8 md:p-10 shadow-xs">
        <div className="max-w-3xl mb-8">
          <div className="text-xs font-semibold uppercase tracking-wider text-emerald-700 mb-1">
            Econometric Foundation
          </div>
          <h2 className="text-2xl md:text-3xl font-bold tracking-tight text-slate-900">
            Robinson's Partially Linear Double Machine Learning
          </h2>
          <p className="text-sm text-slate-600 mt-2">
            Formulation of the causal identification framework used in the EconoCausal production pipeline:
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
          <div className="bg-emerald-50/50 p-5 rounded-xl border border-emerald-200/80 space-y-2.5">
            <div className="text-emerald-900 font-bold text-sm">Step 1: Outcome Residualization</div>
            <div className="font-mono bg-white border border-emerald-100 p-2.5 rounded text-emerald-950 font-semibold shadow-xs">
              Y = g(W) + U<br/>
              U = Y - E[Y | W]
            </div>
            <p className="text-slate-600 leading-relaxed">
              Trains ExtraTreesRegressor on observed confounders W to predict sales Y, leaving residual demand U.
            </p>
          </div>

          <div className="bg-emerald-50/50 p-5 rounded-xl border border-emerald-200/80 space-y-2.5">
            <div className="text-emerald-900 font-bold text-sm">Step 2: Treatment Residualization</div>
            <div className="font-mono bg-white border border-emerald-100 p-2.5 rounded text-emerald-950 font-semibold shadow-xs">
              P = m(W) + V<br/>
              V = P - E[P | W]
            </div>
            <p className="text-slate-600 leading-relaxed">
              Trains second regressor to predict pricing P from W, extracting exogenous price variation V.
            </p>
          </div>

          <div className="bg-emerald-50/50 p-5 rounded-xl border border-emerald-200/80 space-y-2.5">
            <div className="text-emerald-900 font-bold text-sm">Step 3: Orthogonal Estimation</div>
            <div className="font-mono bg-white border border-emerald-100 p-2.5 rounded text-emerald-950 font-semibold shadow-xs">
              U = θ · V + ε<br/>
              θ = Cov(V, U) / Var(V)
            </div>
            <p className="text-slate-600 leading-relaxed">
              Regresses residual demand on residual price with 3-fold cross-fitting to obtain unbiased treatment effect θ.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
