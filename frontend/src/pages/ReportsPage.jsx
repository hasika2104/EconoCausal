import React, { useState, useEffect } from 'react';
import {
  FileSpreadsheet,
  Download,
  Printer,
  FileText,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  TrendingUp,
  BarChart3,
  Sparkles,
  Info
} from 'lucide-react';
import { fetchReportSummary, getReportExportUrl } from '../services/api';

export default function ReportsPage({ onNavigate, lang = 'en' }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadSummary() {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchReportSummary();
        setSummary(data);
      } catch (err) {
        console.error(err);
        setError('Failed to fetch report summary.');
      } finally {
        setLoading(false);
      }
    }
    loadSummary();
  }, []);

  const handlePrint = () => {
    window.print();
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] text-slate-500 gap-3">
        <RefreshCw className="w-8 h-8 animate-spin text-emerald-600" />
        <span className="text-sm font-medium">Generating executive analytics report...</span>
      </div>
    );
  }

  if (error || !summary) {
    return (
      <div className="p-8 bg-red-50 border border-red-200 rounded-2xl text-red-800 text-sm">
        {error || 'Report unavailable.'}
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-6xl mx-auto print:p-0">
      {/* Action Bar */}
      <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4 print:hidden">
        <div>
          <h1 className="text-xl font-bold text-slate-900">
            {lang === 'te' ? 'ఎగ్జిక్యూటివ్ రిపోర్ట్ జనరేషన్' : 'Executive Pricing & Causal Report'}
          </h1>
          <p className="text-xs text-slate-500 font-medium">
            Generated on {summary.generated_at} • Audited with Double ML Econometrics
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <a
            href={getReportExportUrl('excel')}
            download
            className="flex items-center gap-2 px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-semibold shadow-sm transition-all"
          >
            <FileSpreadsheet className="w-4 h-4" />
            <span>Download Multi-Tab Excel (.xlsx)</span>
          </a>

          <a
            href={getReportExportUrl('csv')}
            download
            className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 rounded-xl text-xs font-semibold shadow-2xs transition-all"
          >
            <Download className="w-4 h-4 text-emerald-600" />
            <span>Export CSV</span>
          </a>

          <button
            onClick={handlePrint}
            className="flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-semibold transition-all"
          >
            <Printer className="w-4 h-4" />
            <span>Print / Save as PDF</span>
          </button>
        </div>
      </div>

      {/* Printable Report Paper Container */}
      <div className="bg-white border border-slate-200 rounded-3xl p-8 md:p-12 shadow-sm space-y-10 print:border-none print:shadow-none print:p-0">
        {/* Report Header */}
        <div className="border-b border-slate-200 pb-6 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
          <div>
            <div className="inline-flex items-center gap-2 text-emerald-700 text-xs font-bold uppercase tracking-wider mb-2">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>EconoCausal Business Intelligence Report</span>
            </div>
            <h2 className="text-2xl md:text-3xl font-extrabold text-slate-900 tracking-tight">
              Retail Demand & Causal Elasticity Audit
            </h2>
            <p className="text-xs text-slate-500 mt-1">
              Scope: 73,100 Store-Day Observations • 20 SKUs • 4 Categories • 4 Regions
            </p>
          </div>
          <div className="text-right text-xs text-slate-500">
            <div><strong>Report Date:</strong> {summary.generated_at}</div>
            <div><strong>Model Version:</strong> DML ExtraTrees-3Fold-HC3</div>
          </div>
        </div>

        {/* Section 1: Executive KPI Summary */}
        <section className="space-y-4">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <span className="w-6 h-6 rounded-lg bg-emerald-100 text-emerald-800 text-xs flex items-center justify-center font-bold">1</span>
            <span>Executive Business KPIs</span>
          </h3>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
              <div className="text-xs text-slate-500 font-medium">Total Revenue</div>
              <div className="text-lg font-bold text-slate-900 mt-1">
                ${summary.kpis.total_revenue?.toLocaleString()}
              </div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
              <div className="text-xs text-slate-500 font-medium">Total Units Sold</div>
              <div className="text-lg font-bold text-slate-900 mt-1">
                {summary.kpis.total_units_sold?.toLocaleString()}
              </div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
              <div className="text-xs text-slate-500 font-medium">Average Selling Price</div>
              <div className="text-lg font-bold text-slate-900 mt-1">
                ${summary.kpis.avg_price?.toFixed(2)}
              </div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
              <div className="text-xs text-slate-500 font-medium">Products (SKUs)</div>
              <div className="text-lg font-bold text-slate-900 mt-1">
                {summary.kpis.product_count}
              </div>
            </div>
            <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200">
              <div className="text-xs text-emerald-800 font-medium">DML Elasticity (θ)</div>
              <div className="text-lg font-bold text-emerald-900 mt-1">
                +{summary.causal_dml.ate_theta?.toFixed(4)}
              </div>
            </div>
          </div>
        </section>

        {/* Section 2: Causal Inference vs Predictive Analytics */}
        <section className="space-y-4">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <span className="w-6 h-6 rounded-lg bg-emerald-100 text-emerald-800 text-xs flex items-center justify-center font-bold">2</span>
            <span>Causal Price Effect Analysis (Double Machine Learning)</span>
          </h3>

          <div className="p-6 rounded-2xl border border-slate-200 bg-slate-50/70 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
              <div>
                <span className="text-slate-500">Primary ATE (θ):</span>
                <div className="font-mono font-bold text-sm text-slate-900 mt-0.5">
                  +{summary.causal_dml.ate_theta?.toFixed(4)}
                </div>
              </div>
              <div>
                <span className="text-slate-500">95% Confidence Interval:</span>
                <div className="font-mono font-semibold text-xs text-slate-900 mt-0.5">
                  [{summary.causal_dml.ci_95?.[0]?.toFixed(4)}, {summary.causal_dml.ci_95?.[1]?.toFixed(4)}]
                </div>
              </div>
              <div>
                <span className="text-slate-500">Statistical P-Value:</span>
                <div className="font-mono font-semibold text-xs text-slate-900 mt-0.5">
                  {summary.causal_dml.p_value?.toFixed(3)} (Not Significant)
                </div>
              </div>
              <div>
                <span className="text-slate-500">Sample Size:</span>
                <div className="font-mono font-semibold text-xs text-slate-900 mt-0.5">
                  {summary.causal_dml.n_observations?.toLocaleString()} records
                </div>
              </div>
            </div>

            <div className="p-4 bg-white rounded-xl border border-slate-200 text-xs text-slate-700 leading-relaxed">
              <strong className="text-emerald-800">Econometric Conclusion:</strong> {summary.causal_dml.interpretation}
            </div>
          </div>
        </section>

        {/* Section 3: Flagship Revenue Generators */}
        <section className="space-y-4">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <span className="w-6 h-6 rounded-lg bg-emerald-100 text-emerald-800 text-xs flex items-center justify-center font-bold">3</span>
            <span>Top Revenue Contributing SKUs</span>
          </h3>

          <div className="overflow-x-auto rounded-xl border border-slate-200">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Product ID</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Average Price</th>
                  <th className="py-3 px-4">Units Sold</th>
                  <th className="py-3 px-4">Total Revenue</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {summary.top_revenue_products?.map((prod) => (
                  <tr key={prod.product_id} className="hover:bg-slate-50/60">
                    <td className="py-3 px-4 font-mono font-bold text-slate-900">{prod.product_id}</td>
                    <td className="py-3 px-4">{prod.category}</td>
                    <td className="py-3 px-4">${prod.avg_price?.toFixed(2)}</td>
                    <td className="py-3 px-4">{prod.units?.toLocaleString()}</td>
                    <td className="py-3 px-4 font-bold text-slate-900">${prod.revenue?.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Section 4: AI Recommendations Sample */}
        <section className="space-y-4">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <span className="w-6 h-6 rounded-lg bg-emerald-100 text-emerald-800 text-xs flex items-center justify-center font-bold">4</span>
            <span>Audited AI Pricing Recommendations (Sample)</span>
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {summary.recommendations_summary?.sample_recommendations?.map((rec, idx) => (
              <div key={idx} className="p-4 rounded-xl border border-slate-200 bg-white shadow-2xs">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-slate-900 text-xs font-mono">{rec.product_id} ({rec.category})</span>
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-100 text-emerald-800">
                    {rec.strategy}
                  </span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">{rec.suggested_action}</p>
                {rec.revenue_impact_pct && (
                  <div className="mt-2 text-[11px] font-semibold text-emerald-700">
                    Projected Revenue Delta: {rec.revenue_impact_pct}%
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* Section 5: Methodology & Business Limitations */}
        <section className="space-y-4 pt-4 border-t border-slate-200">
          <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider text-slate-500">
            Methodology, Safeguards & Limitations
          </h3>
          <ul className="space-y-2 text-xs text-slate-600 leading-relaxed list-disc list-inside">
            {summary.methodology_and_limitations?.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
}
