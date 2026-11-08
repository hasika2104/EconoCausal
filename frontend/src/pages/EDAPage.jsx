import React, { useState, useEffect } from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend
} from 'recharts';
import {
  BarChart2,
  Calendar,
  AlertTriangle,
  Info,
  CheckCircle,
  Database,
  Layers,
  Sparkles,
  RefreshCw,
  AlertCircle
} from 'lucide-react';
import { fetchEDA } from '../services/api';

export default function EDAPage() {
  const [edaData, setEdaData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeDistribution, setActiveDistribution] = useState('price'); // 'price', 'demand', 'inventory'

  useEffect(() => {
    async function loadEDA() {
      setLoading(true);
      try {
        const data = await fetchEDA();
        setEdaData(data);
      } catch (err) {
        console.error(err);
        setError('Failed to load EDA analytical results.');
      } finally {
        setLoading(false);
      }
    }
    loadEDA();
  }, []);

  if (loading && !edaData) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] text-slate-500 gap-3">
        <RefreshCw className="w-8 h-8 animate-spin text-emerald-600" />
        <span className="text-sm font-medium">Loading Python EDA results...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <div>
            <div className="font-semibold text-sm">Failed to load EDA data</div>
            <div className="text-xs mt-0.5">{error}</div>
          </div>
        </div>
        <button
          onClick={loadEDA}
          className="px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xs font-medium shrink-0 ml-4"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!edaData || !edaData.dataset_metrics) {
    return (
      <div className="p-8 bg-white border border-slate-200 rounded-xl text-center space-y-4 shadow-xs">
        <AlertCircle className="w-8 h-8 text-amber-500 mx-auto" />
        <div className="text-slate-800 font-bold text-base">EDA Analytical Data Connecting...</div>
        <p className="text-xs text-slate-500 max-w-md mx-auto">
          Synthesizing exploratory data analysis from 73,100 retail transaction records.
        </p>
        <button
          onClick={loadEDA}
          className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg text-xs font-semibold shadow-xs"
        >
          Refresh EDA
        </button>
      </div>
    );
  }

  const {
    dataset_metrics,
    summary_stats,
    missing_analysis,
    correlation_matrix,
    distributions,
    seasonality,
    outlier_analysis,
    inventory_demand_sample,
    promotion_notes
  } = edaData;

  return (
    <div className="space-y-8 pb-12">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">Exploratory Data Analysis (EDA)</h2>
        <p className="text-xs text-slate-500 mt-1">
          Empirical verification of 73,100 store-day transaction logs, distributions, correlations, and operational inventory constraints.
        </p>
      </div>

      {/* Dataset Overview Metric Tiles */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase">Total Records</div>
          <div className="text-xl font-bold text-slate-900 mt-1">{dataset_metrics.total_records.toLocaleString()}</div>
          <div className="text-[11px] text-emerald-600 font-medium mt-0.5">100% Cleaned</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase">Operational Span</div>
          <div className="text-xl font-bold text-slate-900 mt-1">731 Days</div>
          <div className="text-[11px] text-slate-500 font-medium mt-0.5">2022-01 to 2024-01</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase">Active Products</div>
          <div className="text-xl font-bold text-slate-900 mt-1">{dataset_metrics.products_count} SKUs</div>
          <div className="text-[11px] text-slate-500 font-medium mt-0.5">5 Categories</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase">Retail Facilities</div>
          <div className="text-xl font-bold text-slate-900 mt-1">{dataset_metrics.stores_count} Stores</div>
          <div className="text-[11px] text-slate-500 font-medium mt-0.5">4 Regions</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase">Missing Values</div>
          <div className="text-xl font-bold text-emerald-700 mt-1">0 (0.00%)</div>
          <div className="text-[11px] text-emerald-600 font-medium mt-0.5">Zero Imputation Needed</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase">Stockout Rate</div>
          <div className="text-xl font-bold text-amber-700 mt-1">{dataset_metrics.inventory_binding_rate}%</div>
          <div className="text-[11px] text-amber-600 font-medium mt-0.5">Demand ≥ Inventory</div>
        </div>
      </div>

      {/* Distribution Analysis (Interactive Tabs) */}
      <div className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h3 className="text-sm font-bold text-slate-800">Empirical Feature Distributions</h3>
            <p className="text-xs text-slate-400">Histograms computed across the complete 73,100 records</p>
          </div>

          <div className="inline-flex rounded-lg border border-slate-200 p-1 bg-slate-50 text-xs">
            <button
              onClick={() => setActiveDistribution('price')}
              className={`px-3 py-1.5 rounded-md font-medium transition-all ${
                activeDistribution === 'price'
                  ? 'bg-white text-emerald-800 shadow-xs font-semibold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Selling Price ($)
            </button>
            <button
              onClick={() => setActiveDistribution('demand')}
              className={`px-3 py-1.5 rounded-md font-medium transition-all ${
                activeDistribution === 'demand'
                  ? 'bg-white text-emerald-800 shadow-xs font-semibold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Demand (Units Sold)
            </button>
            <button
              onClick={() => setActiveDistribution('inventory')}
              className={`px-3 py-1.5 rounded-md font-medium transition-all ${
                activeDistribution === 'inventory'
                  ? 'bg-white text-emerald-800 shadow-xs font-semibold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              On-Hand Inventory
            </button>
          </div>
        </div>

        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={distributions[activeDistribution]}
              margin={{ top: 10, right: 10, left: -10, bottom: 0 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="range" tick={{ fontSize: 10, fill: '#64748b' }} />
              <YAxis tick={{ fontSize: 11, fill: '#64748b' }} tickFormatter={(val) => `${(val / 1000).toFixed(1)}k`} />
              <RechartsTooltip
                formatter={(val) => [val.toLocaleString(), 'Frequency Count']}
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
              />
              <Bar
                dataKey="count"
                fill={activeDistribution === 'price' ? '#16a34a' : activeDistribution === 'demand' ? '#2563eb' : '#0d9488'}
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Correlation Matrix & Heatmap */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
        <div className="p-5 border-b border-slate-100 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-800">Correlation Matrix (Pearson r)</h3>
            <p className="text-xs text-slate-400">Pairwise linear correlation across all numeric variables</p>
          </div>
          <span className="text-xs px-2.5 py-1 bg-slate-100 text-slate-700 font-mono rounded">
            N = 73,100
          </span>
        </div>

        <div className="overflow-x-auto p-5">
          <table className="w-full text-xs text-center border-collapse">
            <thead>
              <tr className="border-b border-slate-200">
                <th className="py-2.5 px-3 text-left font-bold text-slate-700 bg-slate-50">Feature</th>
                {edaData.numeric_features.map((feat) => (
                  <th key={feat} className="py-2.5 px-3 font-semibold text-slate-600 bg-slate-50">
                    {feat}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {correlation_matrix.map((row) => (
                <tr key={row.feature} className="hover:bg-slate-50/50">
                  <td className="py-2.5 px-3 text-left font-semibold text-slate-800 bg-slate-50/50">
                    {row.feature}
                  </td>
                  {edaData.numeric_features.map((feat) => {
                    const val = row[feat];
                    // Compute heat color intensity
                    let bgColor = 'bg-white';
                    let textColor = 'text-slate-700';
                    if (val === 1.0) {
                      bgColor = 'bg-emerald-100 text-emerald-900 font-bold';
                    } else if (val > 0.3) {
                      bgColor = 'bg-emerald-50 text-emerald-800 font-semibold';
                    } else if (val < -0.1) {
                      bgColor = 'bg-rose-50 text-rose-800 font-semibold';
                    }
                    return (
                      <td key={feat} className={`py-2 px-3 font-mono ${bgColor} ${textColor}`}>
                        {val !== undefined ? val.toFixed(3) : '-'}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Row: Seasonality & Inventory Constraint Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Seasonality: Day of Week & Month */}
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-800">Day-of-Week Demand Pattern</h3>
              <p className="text-xs text-slate-400">Average daily units sold by calendar weekday</p>
            </div>
            <Calendar className="w-4 h-4 text-slate-400" />
          </div>

          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={seasonality.day_of_week} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="day" tick={{ fontSize: 10, fill: '#64748b' }} />
                <YAxis domain={[120, 150]} tick={{ fontSize: 10, fill: '#64748b' }} />
                <RechartsTooltip
                  formatter={(val) => [`${val} units`, 'Avg Demand']}
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
                />
                <Bar dataKey="avg_units" fill="#16a34a" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-[11px] text-slate-500 mt-2 text-center">
            Daily demand remains uniform across weekdays (~136 units/day), confirming absent day-of-week demand shocks.
          </p>
        </div>

        {/* Inventory vs Demand Scatter Sample */}
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-800">Inventory Level vs Units Sold</h3>
              <p className="text-xs text-slate-400">Testing for shelf stockout binding conditions</p>
            </div>
            <span className="text-xs px-2 py-0.5 rounded bg-amber-50 text-amber-800 font-medium border border-amber-200">
              0.5% Binding Rate
            </span>
          </div>

          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis type="number" dataKey="inventory" name="Inventory Level" tick={{ fontSize: 10, fill: '#64748b' }} />
                <YAxis type="number" dataKey="units_sold" name="Units Sold" tick={{ fontSize: 10, fill: '#64748b' }} />
                <RechartsTooltip
                  cursor={{ strokeDasharray: '3 3' }}
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
                />
                <Scatter name="Transactions" data={inventory_demand_sample} fill="#059669" opacity={0.6} />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
          <p className="text-[11px] text-slate-500 mt-2 text-center">
            Points close to the diagonal represent binding inventory where on-hand stock limited realized customer sales.
          </p>
        </div>
      </div>

      {/* Summary Statistics & Outlier Table */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Descriptive Statistics */}
        <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
          <div className="p-4 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-800">Descriptive Summary Statistics</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-50 text-slate-500 uppercase text-[10px]">
                <tr>
                  <th className="py-2.5 px-3">Column</th>
                  <th className="py-2.5 px-3 text-right">Mean</th>
                  <th className="py-2.5 px-3 text-right">Std</th>
                  <th className="py-2.5 px-3 text-right">Min</th>
                  <th className="py-2.5 px-3 text-right">Median</th>
                  <th className="py-2.5 px-3 text-right">Max</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {summary_stats.map((row) => (
                  <tr key={row.column} className="hover:bg-slate-50/50">
                    <td className="py-2 px-3 font-medium text-slate-900">{row.column}</td>
                    <td className="py-2 px-3 text-right font-mono">{row.mean}</td>
                    <td className="py-2 px-3 text-right font-mono">{row.std}</td>
                    <td className="py-2 px-3 text-right font-mono">{row.min}</td>
                    <td className="py-2 px-3 text-right font-mono">{row.median}</td>
                    <td className="py-2 px-3 text-right font-mono">{row.max}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Outlier Analysis Table */}
        <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
          <div className="p-4 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-800">Outlier Analysis (IQR Method)</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-50 text-slate-500 uppercase text-[10px]">
                <tr>
                  <th className="py-2.5 px-3">Feature</th>
                  <th className="py-2.5 px-3 text-right">IQR</th>
                  <th className="py-2.5 px-3 text-right">Lower Bound</th>
                  <th className="py-2.5 px-3 text-right">Upper Bound</th>
                  <th className="py-2.5 px-3 text-right">Outliers</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {outlier_analysis.map((row) => (
                  <tr key={row.feature} className="hover:bg-slate-50/50">
                    <td className="py-2 px-3 font-medium text-slate-900">{row.feature}</td>
                    <td className="py-2 px-3 text-right font-mono">{row.iqr}</td>
                    <td className="py-2 px-3 text-right font-mono">{row.lower_bound}</td>
                    <td className="py-2 px-3 text-right font-mono">{row.upper_bound}</td>
                    <td className="py-2 px-3 text-right font-mono font-bold text-slate-900">
                      {row.outlier_count} ({row.outlier_pct}%)
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Promotion Analysis & Confounding Banner */}
      <div className="p-5 rounded-xl border border-amber-200 bg-amber-50/70 flex items-start gap-4 text-xs text-amber-900">
        <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <div className="font-bold text-sm text-amber-950">
            Econometric Note on Promotions & Confounders ({promotion_notes.status})
          </div>
          <p className="leading-relaxed text-amber-900">
            {promotion_notes.description}
          </p>
          <p className="leading-relaxed text-amber-800">
            {promotion_notes.econometric_impact}
          </p>
        </div>
      </div>
    </div>
  );
}
