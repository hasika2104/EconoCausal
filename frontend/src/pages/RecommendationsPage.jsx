import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Search,
  Filter,
  CheckCircle,
  AlertTriangle,
  Clock,
  HelpCircle,
  TrendingUp,
  TrendingDown,
  RefreshCw,
  SlidersHorizontal,
  Layers,
  ShieldCheck,
  ChevronRight
} from 'lucide-react';
import MetricCard from '../components/MetricCard';
import { fetchRecommendations } from '../services/api';

export default function RecommendationsPage({ onNavigate }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters
  const [selectedStrategy, setSelectedStrategy] = useState('All');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedItem, setSelectedItem] = useState(null);

  const loadRecs = async () => {
    setLoading(true);
    try {
      const res = await fetchRecommendations({
        strategy: selectedStrategy,
        category: selectedCategory,
        product_id: searchQuery
      });
      setData(res);
      if (res.items && res.items.length > 0 && !selectedItem) {
        setSelectedItem(res.items[0]);
      }
    } catch (err) {
      console.error(err);
      setError('Failed to load AI pricing recommendations.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRecs();
  }, [selectedStrategy, selectedCategory, searchQuery]);

  if (loading && !data) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] text-slate-500 gap-3">
        <RefreshCw className="w-8 h-8 animate-spin text-emerald-600" />
        <span className="text-sm font-medium">Loading AI Pricing Recommendations...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <AlertTriangle className="w-5 h-5 shrink-0" />
          <div>
            <div className="font-semibold text-sm">Failed to load recommendations</div>
            <div className="text-xs mt-0.5">{error}</div>
          </div>
        </div>
        <button
          onClick={loadRecs}
          className="px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xs font-medium shrink-0 ml-4"
        >
          Retry
        </button>
      </div>
    );
  }

  const { summary, items } = data || { summary: {}, items: [] };

  const getStrategyBadge = (strat) => {
    if (strat.includes('Maintain')) {
      return { bg: 'bg-emerald-50 text-emerald-800 border-emerald-200', icon: CheckCircle };
    }
    if (strat.includes('Review inventory')) {
      return { bg: 'bg-amber-50 text-amber-800 border-amber-200', icon: AlertTriangle };
    }
    if (strat.includes('Collect more data')) {
      return { bg: 'bg-blue-50 text-blue-800 border-blue-200', icon: Clock };
    }
    if (strat.includes('increase')) {
      return { bg: 'bg-teal-50 text-teal-800 border-teal-200', icon: TrendingUp };
    }
    return { bg: 'bg-purple-50 text-purple-800 border-purple-200', icon: TrendingDown };
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">Product-Level AI Pricing Engine</h2>
        <p className="text-xs text-slate-500 mt-1">
          Automated commercial recommendations across 100 operating segments synthesizing DML elasticity, sales velocity, and inventory buffer ratios.
        </p>
      </div>

      {/* Summary KPI Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
        {summary?.strategies?.map((strat) => {
          const count = summary.strategy_counts[strat] || 0;
          const { bg, icon: Icon } = getStrategyBadge(strat);
          const isSelected = selectedStrategy === strat;

          return (
            <div
              key={strat}
              onClick={() => setSelectedStrategy(isSelected ? 'All' : strat)}
              className={`p-3.5 rounded-xl border transition-all cursor-pointer select-none ${
                isSelected
                  ? 'border-emerald-600 bg-emerald-50/50 shadow-xs ring-1 ring-emerald-600'
                  : 'border-slate-200/80 bg-white hover:border-slate-300'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <Icon className="w-4 h-4 text-slate-500" />
                <span className="text-base font-bold text-slate-900 font-mono">{count}</span>
              </div>
              <div className="text-[11px] font-semibold text-slate-700 leading-snug truncate" title={strat}>
                {strat}
              </div>
              <div className="text-[10px] text-slate-400 mt-0.5">
                {((count / (summary.total_segments || 100)) * 100).toFixed(0)}% of Catalog
              </div>
            </div>
          );
        })}
      </div>

      {/* Search and Filters Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs flex flex-wrap items-center gap-3">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search by Product SKU (e.g. P0001, P0015)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full text-xs bg-slate-50 border border-slate-200 rounded-lg pl-8 pr-3 py-1.5 text-slate-800 focus:outline-emerald-500"
          />
        </div>

        {/* Strategy filter */}
        <select
          value={selectedStrategy}
          onChange={(e) => setSelectedStrategy(e.target.value)}
          className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-700 focus:outline-emerald-500"
        >
          <option value="All">All Strategies ({summary.total_segments || 100})</option>
          {summary?.strategies?.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>

        {/* Category filter */}
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-700 focus:outline-emerald-500"
        >
          <option value="All">All Categories</option>
          {summary?.categories?.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        {(selectedStrategy !== 'All' || selectedCategory !== 'All' || searchQuery !== '') && (
          <button
            onClick={() => {
              setSelectedStrategy('All');
              setSelectedCategory('All');
              setSearchQuery('');
            }}
            className="text-xs text-emerald-700 hover:text-emerald-800 font-medium underline ml-auto"
          >
            Clear Filters
          </button>
        )}
      </div>

      {/* Main Content: Split List and Detail Drawer */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Side: Recommendations List (7 Cols) */}
        <div className="lg:col-span-7 bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
          <div className="p-4 border-b border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Showing {items.length} Operating Segments</span>
            <span className="font-medium text-slate-700">Click a SKU to inspect causal reasoning</span>
          </div>

          <div className="divide-y divide-slate-100 max-h-[620px] overflow-y-auto">
            {items.map((item) => {
              const { bg, icon: Icon } = getStrategyBadge(item.recommendation_strategy);
              const isSelected = selectedItem?.product_id === item.product_id && selectedItem?.category === item.category;

              return (
                <div
                  key={`${item.product_id}-${item.category}`}
                  onClick={() => setSelectedItem(item)}
                  className={`p-4 transition-all cursor-pointer hover:bg-slate-50/80 ${
                    isSelected ? 'bg-emerald-50/50 border-l-4 border-emerald-600' : ''
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-slate-900 text-xs">{item.product_id}</span>
                      <span className="px-2 py-0.5 rounded text-[10px] bg-slate-100 text-slate-600 font-medium">
                        {item.category}
                      </span>
                    </div>

                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold border flex items-center gap-1 ${bg}`}>
                      <Icon className="w-3 h-3" />
                      <span>{item.recommendation_strategy}</span>
                    </span>
                  </div>

                  <div className="grid grid-cols-3 gap-2 text-xs mt-2 text-slate-600">
                    <div>
                      <span className="text-[10px] text-slate-400 block">Current Price</span>
                      <span className="font-mono font-medium">${item.current_price.toFixed(2)}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-slate-400 block">Suggested Price</span>
                      <span className="font-mono font-bold text-slate-800">${item.suggested_price.toFixed(2)}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-slate-400 block">Inventory Buffer</span>
                      <span className="font-mono text-slate-700">{item.inventory_buffer_ratio.toFixed(2)}x</span>
                    </div>
                  </div>

                  <p className="text-[11px] text-slate-500 mt-2 line-clamp-2 leading-relaxed">
                    {item.recommendation_explanation}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Side: Detailed SKU Inspection Card (5 Cols) */}
        <div className="lg:col-span-5 space-y-4">
          {selectedItem ? (
            <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs p-6 space-y-5 sticky top-20">
              <div className="flex items-center justify-between pb-4 border-b border-slate-100">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-mono font-extrabold text-slate-900 text-base">{selectedItem.product_id}</h3>
                    <span className="px-2 py-0.5 rounded text-xs bg-emerald-100 text-emerald-800 font-medium">
                      {selectedItem.category}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400 mt-0.5">Granular Segment Dossier</div>
                </div>

                <button
                  onClick={() => onNavigate('simulation')}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg font-semibold shadow-xs transition-all"
                >
                  <SlidersHorizontal className="w-3.5 h-3.5" />
                  <span>Simulate</span>
                </button>
              </div>

              {/* Strategy Banner */}
              <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-200 space-y-1">
                <div className="text-[10px] font-bold uppercase text-slate-400 tracking-wider">
                  Recommended Action
                </div>
                <div className="text-xs font-bold text-slate-900">
                  {selectedItem.recommendation_strategy}
                </div>
                <div className="text-[11px] text-slate-600">
                  Target Price: <strong className="text-slate-900">${selectedItem.suggested_price.toFixed(2)}</strong> ({selectedItem.price_change_pct >= 0 ? '+' : ''}{selectedItem.price_change_pct}%)
                </div>
              </div>

              {/* Economic & Operational Metrics Grid */}
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-3 rounded-lg border border-slate-100 bg-slate-50/50">
                  <span className="text-[10px] text-slate-400 block">Baseline Velocity</span>
                  <span className="font-mono font-bold text-slate-800 text-sm">{selectedItem.baseline_units_sold} u/d</span>
                </div>
                <div className="p-3 rounded-lg border border-slate-100 bg-slate-50/50">
                  <span className="text-[10px] text-slate-400 block">Expected Revenue</span>
                  <span className="font-mono font-bold text-slate-800 text-sm">${selectedItem.expected_revenue.toLocaleString()}</span>
                </div>
                <div className="p-3 rounded-lg border border-slate-100 bg-slate-50/50">
                  <span className="text-[10px] text-slate-400 block">Inventory Buffer</span>
                  <span className="font-mono font-bold text-slate-800 text-sm">{selectedItem.inventory_buffer_ratio}x</span>
                </div>
                <div className="p-3 rounded-lg border border-slate-100 bg-slate-50/50">
                  <span className="text-[10px] text-slate-400 block">Stockout Binding Rate</span>
                  <span className="font-mono font-bold text-amber-700 text-sm">{selectedItem.inventory_binding_rate_pct}%</span>
                </div>
              </div>

              {/* Econometric Evidence */}
              <div className="space-y-1.5 text-xs">
                <span className="font-bold text-slate-800 flex items-center gap-1.5">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                  <span>DML Econometric Elasticity</span>
                </span>
                <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 font-mono text-[11px] space-y-1">
                  <div>Category θ: <strong>{selectedItem.dml_theta_used >= 0 ? '+' : ''}{selectedItem.dml_theta_used}</strong></div>
                  <div>p-value: <strong>{selectedItem.dml_p_value}</strong> ({selectedItem.dml_p_value < 0.05 ? 'Significant' : 'Inelastic'})</div>
                </div>
              </div>

              {/* Managerial Explanation */}
              <div className="space-y-1.5 text-xs">
                <span className="font-bold text-slate-800">Operational & Managerial Justification:</span>
                <p className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-slate-700 leading-relaxed text-[11px]">
                  {selectedItem.recommendation_explanation}
                </p>
              </div>

              {/* Inventory considerations */}
              <div className="space-y-1 text-xs">
                <span className="font-semibold text-slate-600">Stock Considerations:</span>
                <p className="text-[11px] text-slate-500 italic">
                  {selectedItem.inventory_considerations}
                </p>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-slate-200 p-8 text-center text-xs text-slate-400">
              Select a recommendation to inspect details.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
