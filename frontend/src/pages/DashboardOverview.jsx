import React, { useState, useEffect } from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend
} from 'recharts';
import {
  Package,
  ShoppingCart,
  DollarSign,
  TrendingUp,
  Activity,
  Layers,
  Filter,
  RefreshCw,
  AlertCircle
} from 'lucide-react';
import MetricCard from '../components/MetricCard';
import { fetchDashboard } from '../services/api';

export default function DashboardOverview({ onNavigate }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters state
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedStore, setSelectedStore] = useState('All');
  const [selectedRegion, setSelectedRegion] = useState('All');
  const [selectedProduct, setSelectedProduct] = useState('All');

  const loadDashboard = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchDashboard({
        category: selectedCategory,
        store: selectedStore,
        region: selectedRegion,
        product: selectedProduct
      });
      setData(res);
    } catch (err) {
      console.error(err);
      setError('Failed to load dashboard data. Ensure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, [selectedCategory, selectedStore, selectedRegion, selectedProduct]);

  if (loading && !data) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] text-slate-500 gap-3">
        <RefreshCw className="w-8 h-8 animate-spin text-emerald-600" />
        <span className="text-sm font-medium">Loading genuine retail analytics...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 flex items-center gap-3">
        <AlertCircle className="w-5 h-5" />
        <div>
          <div className="font-semibold text-sm">Failed to connect to backend API</div>
          <div className="text-xs mt-0.5">{error}</div>
        </div>
      </div>
    );
  }

  const { kpis, filters, charts } = data;

  return (
    <div className="space-y-6 pb-12">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">Executive Retail Dashboard</h2>
          <p className="text-xs text-slate-500 mt-1">
            Empirical multi-store retail metrics synthesized from 73,100 transactions and Double Machine Learning outputs.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={loadDashboard}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-600 hover:text-slate-900 bg-white border border-slate-200 rounded-lg shadow-xs hover:bg-slate-50 transition-all"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs flex flex-wrap items-center gap-3">
        <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-500 mr-2">
          <Filter className="w-3.5 h-3.5 text-emerald-600" />
          <span>Filters:</span>
        </div>

        {/* Category filter */}
        <div className="flex items-center gap-1.5">
          <label className="text-xs text-slate-500">Category:</label>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-700 focus:outline-emerald-500"
          >
            <option value="All">All Categories</option>
            {filters?.categories?.map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>

        {/* Region filter */}
        <div className="flex items-center gap-1.5">
          <label className="text-xs text-slate-500">Region:</label>
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-700 focus:outline-emerald-500"
          >
            <option value="All">All Regions</option>
            {filters?.regions?.map((reg) => (
              <option key={reg} value={reg}>{reg}</option>
            ))}
          </select>
        </div>

        {/* Store filter */}
        <div className="flex items-center gap-1.5">
          <label className="text-xs text-slate-500">Store:</label>
          <select
            value={selectedStore}
            onChange={(e) => setSelectedStore(e.target.value)}
            className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-700 focus:outline-emerald-500"
          >
            <option value="All">All Stores</option>
            {filters?.stores?.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        {/* Product filter */}
        <div className="flex items-center gap-1.5">
          <label className="text-xs text-slate-500">Product:</label>
          <select
            value={selectedProduct}
            onChange={(e) => setSelectedProduct(e.target.value)}
            className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-700 focus:outline-emerald-500"
          >
            <option value="All">All Products</option>
            {filters?.products?.map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
        </div>

        {(selectedCategory !== 'All' || selectedRegion !== 'All' || selectedStore !== 'All' || selectedProduct !== 'All') && (
          <button
            onClick={() => {
              setSelectedCategory('All');
              setSelectedRegion('All');
              setSelectedStore('All');
              setSelectedProduct('All');
            }}
            className="text-xs text-emerald-700 hover:text-emerald-800 underline ml-auto font-medium"
          >
            Reset All
          </button>
        )}
      </div>

      {/* KPI Cards Strip */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <MetricCard
          title="Total Products"
          value={kpis.total_products}
          subtitle="Active SKUs in Catalog"
          icon={Package}
          badgeText="Catalog"
          badgeType="neutral"
        />
        <MetricCard
          title="Total Sales Units"
          value={kpis.total_sales_units.toLocaleString()}
          subtitle="Observed Volume"
          icon={ShoppingCart}
          badgeText="Empirical"
          badgeType="success"
        />
        <MetricCard
          title="Average Price"
          value={`$${kpis.avg_price.toFixed(2)}`}
          subtitle="Catalog-wide Mean"
          icon={DollarSign}
          badgeText="$10 - $100 range"
          badgeType="neutral"
        />
        <MetricCard
          title="Average Demand"
          value={`${kpis.avg_demand.toFixed(1)} u/d`}
          subtitle="Daily Store Velocity"
          icon={Activity}
          badgeText="Daily mean"
          badgeType="neutral"
        />
        <MetricCard
          title="Estimated Price Effect"
          value={`θ = ${kpis.dml_theta >= 0 ? '+' : ''}${kpis.dml_theta.toFixed(4)}`}
          subtitle={`p = ${kpis.dml_p_value.toFixed(3)} (Inelastic)`}
          icon={TrendingUp}
          badgeText="DML Spec 1"
          badgeType={kpis.is_significant ? 'success' : 'info'}
          tooltip="Double ML Treatment Effect: Estimated change in units sold per $1 price change, controlling for store, product, category, region and time."
        />
        <MetricCard
          title="Total Gross Revenue"
          value={`$${(kpis.total_revenue / 1e6).toFixed(1)}M`}
          subtitle="Across 73.1k transactions"
          icon={Layers}
          badgeText="Realized"
          badgeType="success"
        />
      </div>

      {/* Charts Grid: Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Monthly Trend (2 columns) */}
        <div className="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-800">Monthly Demand & Sales Volume Trend</h3>
              <p className="text-xs text-slate-400">Total units sold aggregated by calendar month (2022 - 2024)</p>
            </div>
            <span className="text-xs px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 font-medium border border-emerald-200">
              Units Sold
            </span>
          </div>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={charts.monthly_trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorDemand" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#16a34a" stopOpacity={0.25}/>
                    <stop offset="95%" stopColor="#16a34a" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="period" tick={{ fontSize: 11, fill: '#64748b' }} />
                <YAxis tick={{ fontSize: 11, fill: '#64748b' }} tickFormatter={(val) => `${(val / 1000).toFixed(0)}k`} />
                <RechartsTooltip
                  formatter={(val) => [val.toLocaleString(), 'Units Sold']}
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
                />
                <Area type="monotone" dataKey="units_sold" stroke="#16a34a" strokeWidth={2} fillOpacity={1} fill="url(#colorDemand)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Revenue by Category (1 column) */}
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-800">Revenue by Category</h3>
              <p className="text-xs text-slate-400">Gross volume breakdown</p>
            </div>
            <span className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-medium">
              5 Sectors
            </span>
          </div>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={charts.category_breakdown} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="category" tick={{ fontSize: 11, fill: '#64748b' }} />
                <YAxis tick={{ fontSize: 11, fill: '#64748b' }} tickFormatter={(val) => `$${(val / 1e6).toFixed(0)}M`} />
                <RechartsTooltip
                  formatter={(val) => [`$${(val / 1e6).toFixed(2)}M`, 'Revenue']}
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
                />
                <Bar dataKey="revenue" fill="#059669" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Charts Grid: Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Price vs Demand Empirical Decile Curve */}
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-800">Observed Price vs Demand Relationship</h3>
              <p className="text-xs text-slate-400">Average units sold across $10 price decile bins</p>
            </div>
            <span className="text-xs px-2 py-0.5 rounded bg-blue-50 text-blue-800 font-medium border border-blue-200">
              Empirical Mean
            </span>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={charts.price_demand_curve} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="bin" tick={{ fontSize: 10, fill: '#64748b' }} />
                <YAxis domain={['auto', 'auto']} tick={{ fontSize: 11, fill: '#64748b' }} />
                <RechartsTooltip
                  formatter={(val) => [`${val} units/day`, 'Avg Daily Demand']}
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
                />
                <Line type="monotone" dataKey="avg_demand" stroke="#2563eb" strokeWidth={2.5} dot={{ r: 4, fill: '#2563eb' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <p className="text-[11px] text-slate-500 mt-2 italic text-center">
            Notice how raw observational demand remains flat across prices (~136 units/day), confirming price inelasticity.
          </p>
        </div>

        {/* Regional Performance Breakdown */}
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-800">Regional Performance Distribution</h3>
              <p className="text-xs text-slate-400">Total sales volume and revenue across market territories</p>
            </div>
            <span className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-medium">
              4 Regions
            </span>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={charts.regional_breakdown} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="region" tick={{ fontSize: 11, fill: '#64748b' }} />
                <YAxis tick={{ fontSize: 11, fill: '#64748b' }} tickFormatter={(val) => `$${(val / 1e6).toFixed(0)}M`} />
                <RechartsTooltip
                  formatter={(val) => [`$${(val / 1e6).toFixed(2)}M`, 'Revenue']}
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
                />
                <Bar dataKey="revenue" fill="#0d9488" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Top Product Performance Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
        <div className="p-5 border-b border-slate-100 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-800">Top Performing Products</h3>
            <p className="text-xs text-slate-400">Highest grossing SKUs ranked by realized revenue</p>
          </div>
          <button
            onClick={() => onNavigate('recommendations')}
            className="text-xs text-emerald-700 hover:text-emerald-800 font-semibold"
          >
            View AI Recommendations →
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-slate-100 text-slate-500 font-semibold uppercase tracking-wider text-[11px]">
              <tr>
                <th className="py-3 px-4">Product ID</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4 text-right">Avg Price</th>
                <th className="py-3 px-4 text-right">Units Sold</th>
                <th className="py-3 px-4 text-right">Gross Revenue</th>
                <th className="py-3 px-4 text-center">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {charts.product_performance?.map((prod) => (
                <tr key={prod.product_id} className="hover:bg-slate-50/70 transition-colors">
                  <td className="py-3 px-4 font-mono font-medium text-slate-900">{prod.product_id}</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-slate-100 text-slate-700">
                      {prod.category}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right font-medium">${prod.avg_price.toFixed(2)}</td>
                  <td className="py-3 px-4 text-right font-medium">{prod.units_sold.toLocaleString()}</td>
                  <td className="py-3 px-4 text-right font-bold text-slate-900">${(prod.revenue / 1e6).toFixed(2)}M</td>
                  <td className="py-3 px-4 text-center">
                    <button
                      onClick={() => onNavigate('simulation')}
                      className="px-2.5 py-1 text-[11px] bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded font-medium transition-colors"
                    >
                      Simulate
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
