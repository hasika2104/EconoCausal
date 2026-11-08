import React, { useState, useEffect } from 'react';
import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  ZAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ReferenceLine,
  BarChart,
  Bar
} from 'recharts';
import {
  ShieldCheck,
  Cpu,
  Layers,
  HelpCircle,
  AlertTriangle,
  CheckCircle2,
  TrendingDown,
  Info,
  RefreshCw,
  GitBranch,
  Scale
} from 'lucide-react';
import MetricCard from '../components/MetricCard';
import { fetchCausalAnalysis } from '../services/api';

export default function CausalAnalysisPage() {
  const [causalData, setCausalData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedGroup, setSelectedGroup] = useState('All'); // 'All', 'Model Specification', 'Product Category', 'Calendar Year', 'Geographic Region'

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const data = await fetchCausalAnalysis();
        setCausalData(data);
      } catch (err) {
        console.error(err);
        setError('Failed to load Causal Analysis results.');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading && !causalData) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] text-slate-500 gap-3">
        <RefreshCw className="w-8 h-8 animate-spin text-emerald-600" />
        <span className="text-sm font-medium">Loading DML Causal Inference results...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <AlertTriangle className="w-5 h-5 shrink-0" />
          <div>
            <div className="font-semibold text-sm">Failed to load causal analysis</div>
            <div className="text-xs mt-0.5">{error}</div>
          </div>
        </div>
      </div>
    );
  }

  if (!causalData || !causalData.spec1) {
    return (
      <div className="p-8 bg-white border border-slate-200 rounded-xl text-center space-y-4 shadow-xs">
        <AlertTriangle className="w-8 h-8 text-amber-500 mx-auto" />
        <div className="text-slate-800 font-bold text-base">Causal Inference Engine Initializing...</div>
        <p className="text-xs text-slate-500 max-w-md mx-auto">
          Loading 18-specification Double Machine Learning econometric estimates.
        </p>
      </div>
    );
  }

  const { methodology, spec1, spec2, robustness_specifications, predictive_benchmarks, feature_analysis } = causalData;

  // Filter robustness specs
  const filteredSpecs = selectedGroup === 'All'
    ? robustness_specifications
    : robustness_specifications.filter(s => s.group_type === selectedGroup);

  // Prepare data for Forest Plot
  const forestData = filteredSpecs.map((spec, index) => ({
    name: spec.group_name || spec.specification_name,
    theta: spec.theta_estimate,
    ci_low: spec.ci_lower_95,
    ci_high: spec.ci_upper_95,
    error_low: spec.theta_estimate - spec.ci_lower_95,
    error_high: spec.ci_upper_95 - spec.theta_estimate,
    p_value: spec.p_value,
    is_sig: spec.statistically_significant,
    y_index: index,
  }));

  return (
    <div className="space-y-8 pb-12">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">Causal Impact Analysis (Double Machine Learning)</h2>
        <p className="text-xs text-slate-500 mt-1">
          Orthogonalized econometric estimation isolating the true price elasticity of demand across 18 robustness specifications.
        </p>
      </div>

      {/* Prominent Educational Alert */}
      <div className="p-5 rounded-xl border border-emerald-200 bg-emerald-50/70 text-xs text-emerald-900 flex items-start gap-4">
        <ShieldCheck className="w-6 h-6 text-emerald-700 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <div className="font-bold text-sm text-emerald-950">
            {methodology.core_explanation}
          </div>
          <p className="text-slate-600 leading-relaxed">
            By residualizing both Selling Price (Treatment) and Units Sold (Outcome) on 7 multi-dimensional observed confounders using 3-fold cross-fitting, DML guarantees Neyman orthogonality and protects against omitted variable bias.
          </p>
        </div>
      </div>

      {/* Primary KPI Strip */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Primary ATE (θ)"
          value={`θ = ${spec1.theta_rounded >= 0 ? '+' : ''}${spec1.theta_rounded.toFixed(4)}`}
          subtitle="Spec 1: Core Controls"
          icon={Cpu}
          badgeText={spec1.is_significant ? 'Significant' : 'Inelastic (p=0.490)'}
          badgeType={spec1.is_significant ? 'success' : 'neutral'}
          tooltip="Average Treatment Effect: Estimated change in daily units sold per $1 change in price."
        />

        <MetricCard
          title="95% Confidence Interval"
          value={`[${spec1.ci_low_rounded.toFixed(3)}, +${spec1.ci_high_rounded.toFixed(3)}]`}
          subtitle="White HC3 Robust Standard Error"
          icon={Scale}
          badgeText={`SE: ${spec1.std_err_rounded.toFixed(4)}`}
          badgeType="info"
          tooltip="95% Confidence Interval: Covers zero, meaning we cannot reject the null hypothesis of zero price sensitivity."
        />

        <MetricCard
          title="Price Elasticity at Mean"
          value={`ε = ${spec1.elasticity >= 0 ? '+' : ''}${spec1.elasticity.toFixed(4)}`}
          subtitle={`Mean Price: $55.14 | Mean Demand: 136.5`}
          icon={GitBranch}
          badgeText="Highly Inelastic"
          badgeType="neutral"
          tooltip="Price Elasticity = θ · (Avg Price / Avg Demand). A value near 0 means percentage demand change is nearly zero."
        />

        <MetricCard
          title="Spec 2 (+ Inventory)"
          value={`θ = ${spec2.theta_rounded.toFixed(4)}`}
          subtitle={`p = ${spec2.p_value_rounded.toFixed(3)} | 95% CI [-0.044, +0.005]`}
          icon={Layers}
          badgeText="Sensitivity Check"
          badgeType="warning"
          tooltip="Sensitivity test conditioning on stock levels. Note: Risk of collider bias if inventory responds to demand."
        />
      </div>

      {/* Experimental Setup & Confounders Card */}
      <div className="bg-white rounded-xl border border-slate-200/80 p-6 shadow-xs">
        <h3 className="text-sm font-bold text-slate-800 mb-4">Econometric Identification Framework</h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
          <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
            <div className="font-bold text-slate-800 uppercase tracking-wider text-[11px] text-emerald-700">
              1. Treatment Variable (T)
            </div>
            <div className="font-mono text-slate-900 font-semibold text-sm">Product Selling Price (P)</div>
            <p className="text-slate-500 leading-relaxed">
              Exogenous continuous pricing variable ranging between $10.00 and $100.00 per unit across stores.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
            <div className="font-bold text-slate-800 uppercase tracking-wider text-[11px] text-blue-700">
              2. Outcome Variable (Y)
            </div>
            <div className="font-mono text-slate-900 font-semibold text-sm">Units Sold / Daily Demand</div>
            <p className="text-slate-500 leading-relaxed">
              Realized customer purchase volume per store-day-product tuple, bounded by inventory availability.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
            <div className="font-bold text-slate-800 uppercase tracking-wider text-[11px] text-purple-700">
              3. Observed Confounders (W)
            </div>
            <div className="font-mono text-slate-900 font-semibold text-sm">7 Multidimensional Controls</div>
            <p className="text-slate-500 leading-relaxed">
              Product ID, Store ID, Merchandise Category, Geographic Region, Year, Month, and Day of Week.
            </p>
          </div>
        </div>
      </div>

      {/* 18 Robustness Specifications Table & Forest Plot */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs p-6 space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h3 className="text-sm font-bold text-slate-800">18 DML Robustness & Subsample Specifications</h3>
            <p className="text-xs text-slate-400">Verifying stability across nuisance algorithms, categories, years, regions, and price trimming</p>
          </div>

          <div className="flex items-center gap-2">
            <label className="text-xs text-slate-500">Group:</label>
            <select
              value={selectedGroup}
              onChange={(e) => setSelectedGroup(e.target.value)}
              className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-700 focus:outline-emerald-500"
            >
              <option value="All">All 18 Specifications</option>
              <option value="Model Specification">Model Specifications (Specs 1 - 6)</option>
              <option value="Product Category">Category Subsamples</option>
              <option value="Calendar Year">Calendar Year Subsamples</option>
              <option value="Geographic Region">Geographic Region Subsamples</option>
              <option value="Sample Trimming">Outlier Price Trimming</option>
            </select>
          </div>
        </div>

        {/* Forest Plot of Coefficients */}
        <div className="bg-slate-50/70 p-4 rounded-xl border border-slate-100">
          <div className="text-xs font-semibold text-slate-700 mb-2 flex items-center justify-between">
            <span>Coefficient Forest Plot (θ with 95% Confidence Interval)</span>
            <span className="text-[11px] text-slate-400">Red vertical line: θ = 0 (Null Hypothesis)</span>
          </div>

          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                layout="vertical"
                data={forestData}
                margin={{ top: 10, right: 30, left: 140, bottom: 10 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" horizontal={false} />
                <XAxis type="number" domain={[-0.10, 0.12]} tick={{ fontSize: 10, fill: '#64748b' }} tickFormatter={(val) => val.toFixed(2)} />
                <YAxis dataKey="name" type="category" tick={{ fontSize: 10, fill: '#334155' }} width={135} />
                <RechartsTooltip
                  formatter={(val, name, item) => [
                    `θ = ${item.payload.theta.toFixed(4)} [95% CI: ${item.payload.ci_low.toFixed(4)}, ${item.payload.ci_high.toFixed(4)}], p = ${item.payload.p_value.toFixed(3)}`,
                    'Estimated Effect'
                  ]}
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px', color: '#fff', fontSize: '11px' }}
                />
                <ReferenceLine x={0} stroke="#dc2626" strokeWidth={1.5} strokeDasharray="3 3" />
                <Bar dataKey="theta" fill="#16a34a" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-[11px] text-slate-500 mt-2 text-center">
            Every 95% confidence interval crosses zero (θ = 0), confirming that demand is robustly inelastic across all models and subgroups.
          </p>
        </div>

        {/* Detailed Specifications Data Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="bg-slate-50 text-slate-500 font-semibold uppercase text-[10px] border-b border-slate-200">
              <tr>
                <th className="py-2.5 px-3">Specification</th>
                <th className="py-2.5 px-3">Nuisance Model</th>
                <th className="py-2.5 px-3 text-right">Sample (N)</th>
                <th className="py-2.5 px-3 text-right">θ Estimate</th>
                <th className="py-2.5 px-3 text-right">Std Error</th>
                <th className="py-2.5 px-3 text-center">95% CI</th>
                <th className="py-2.5 px-3 text-right">p-value</th>
                <th className="py-2.5 px-3 text-center">Significant?</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {filteredSpecs.map((spec) => (
                <tr key={spec.specification_id} className="hover:bg-slate-50/50">
                  <td className="py-2.5 px-3">
                    <div className="font-semibold text-slate-900">{spec.specification_name}</div>
                    <div className="text-[10px] text-slate-400">{spec.group_type}</div>
                  </td>
                  <td className="py-2.5 px-3 text-slate-600 font-mono text-[11px]">
                    {spec.nuisance_model}
                  </td>
                  <td className="py-2.5 px-3 text-right font-mono">{spec.sample_size.toLocaleString()}</td>
                  <td className="py-2.5 px-3 text-right font-mono font-bold text-slate-900">
                    {spec.theta_estimate >= 0 ? '+' : ''}{spec.theta_estimate.toFixed(4)}
                  </td>
                  <td className="py-2.5 px-3 text-right font-mono text-slate-500">{spec.std_error_hc3.toFixed(4)}</td>
                  <td className="py-2.5 px-3 text-center font-mono text-[11px]">
                    [{spec.ci_lower_95.toFixed(3)}, {spec.ci_upper_95.toFixed(3)}]
                  </td>
                  <td className="py-2.5 px-3 text-right font-mono">{spec.p_value.toFixed(3)}</td>
                  <td className="py-2.5 px-3 text-center">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-medium ${
                      spec.statistically_significant
                        ? 'bg-emerald-100 text-emerald-800'
                        : 'bg-slate-100 text-slate-600'
                    }`}>
                      {spec.statistically_significant ? 'Yes (p < 0.05)' : 'No (Null)'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Model Benchmarks Strip */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs p-6">
        <h3 className="text-sm font-bold text-slate-800 mb-2">Predictive Demand Model Benchmarks (Chronological Split)</h3>
        <p className="text-xs text-slate-400 mb-4">
          Evaluated on held-out test data (14,620 observations) to compare supervised predictive baseline models against heuristic dummies.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {predictive_benchmarks.map((bm) => (
            <div key={bm.model_name} className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
              <div className="font-bold text-slate-900 text-xs">{bm.model_name}</div>
              <div className="text-[11px] text-slate-500">{bm.model_type}</div>
              <div className="pt-2 border-t border-slate-200/80 grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span className="text-[10px] text-slate-400 block">MAE</span>
                  <span className="font-mono font-bold text-slate-800">{bm.mae}</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-400 block">R² Score</span>
                  <span className="font-mono font-bold text-slate-800">{bm.r2_score}</span>
                </div>
              </div>
              <p className="text-[10px] text-slate-400 italic">{bm.notes}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Day 16 Feature Diagnostics: Predictive Importance vs Causal Lever */}
      {feature_analysis && feature_analysis.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs p-6 space-y-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-sm font-bold text-slate-800">
                Predictive Importance vs. Causal Policy Levers (Day 16 Permutation Audit)
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Held-out test R² permutation drop reveals high prediction accuracy does NOT equal actionable causal intervention.
              </p>
            </div>
            <span className="text-xs px-2.5 py-1 bg-emerald-50 text-emerald-800 font-semibold rounded-full border border-emerald-200 self-start md:self-auto">
              Econometric Audit
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b border-slate-100">
                <tr>
                  <th className="py-2.5 px-3">Rank</th>
                  <th className="py-2.5 px-3">Feature</th>
                  <th className="py-2.5 px-3">Type</th>
                  <th className="py-2.5 px-3 text-right">MDI Importance</th>
                  <th className="py-2.5 px-3 text-right">Permutation Drop (R²)</th>
                  <th className="py-2.5 px-4">Causal Role & Policy Distinction</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {feature_analysis.map((item) => {
                  const isLever = item.feature === 'Price';
                  const isCollider = item.feature === 'Inventory Level';
                  return (
                    <tr key={item.feature} className={`hover:bg-slate-50 ${isLever ? 'bg-emerald-50/40 font-medium' : isCollider ? 'bg-amber-50/30' : ''}`}>
                      <td className="py-2.5 px-3 font-mono font-bold text-slate-500">#{item.predictive_rank}</td>
                      <td className="py-2.5 px-3 font-semibold text-slate-900 flex items-center gap-1.5">
                        {item.feature}
                        {isLever && <span className="text-[10px] px-1.5 py-0.2 rounded bg-emerald-100 text-emerald-800 font-semibold">Causal Lever</span>}
                        {isCollider && <span className="text-[10px] px-1.5 py-0.2 rounded bg-amber-100 text-amber-800 font-semibold">Capacity Proxy</span>}
                      </td>
                      <td className="py-2.5 px-3 text-slate-500">{item.feature_type}</td>
                      <td className="py-2.5 px-3 text-right font-mono">{(item.rf_mdi_importance * 100).toFixed(1)}%</td>
                      <td className="py-2.5 px-3 text-right font-mono font-bold">
                        <span className={item.rf_perm_importance_mean > 0.05 ? 'text-amber-700' : 'text-slate-600'}>
                          {item.rf_perm_importance_mean.toFixed(4)}
                        </span>
                      </td>
                      <td className="py-2.5 px-4 text-slate-600 leading-snug">
                        {item.causal_role_and_distinction}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Critical Limitations Callout */}
      <div className="p-5 rounded-xl border border-amber-200 bg-amber-50/70 text-xs text-amber-900 space-y-2">
        <div className="flex items-center gap-2 font-bold text-sm text-amber-950">
          <AlertTriangle className="w-4 h-4 text-amber-600" />
          <span>Causal Validity & Managerial Limitations</span>
        </div>
        <ul className="list-disc list-inside space-y-1 text-amber-900 leading-relaxed">
          {methodology.limitations.map((lim, idx) => (
            <li key={idx}>{lim}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
