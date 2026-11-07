import React, { useState, useEffect } from 'react';
import {
  SlidersHorizontal,
  DollarSign,
  TrendingUp,
  Package,
  Layers,
  AlertTriangle,
  CheckCircle2,
  RefreshCw,
  Info,
  Scale,
  Sparkles,
  ArrowRight
} from 'lucide-react';
import MetricCard from '../components/MetricCard';
import { fetchProducts, simulatePrice } from '../services/api';

export default function PriceSimulationPage() {
  const [products, setProducts] = useState([]);
  const [selectedProductId, setSelectedProductId] = useState('P0001');
  const [currentPrice, setCurrentPrice] = useState(55.13);
  const [proposedPrice, setProposedPrice] = useState(60.64);
  const [inventoryLevel, setInventoryLevel] = useState(195.0);
  const [costPerUnit, setCostPerUnit] = useState('');
  const [specification, setSpecification] = useState('spec1');

  const [simulationResult, setSimulationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingProducts, setLoadingProducts] = useState(true);

  // Load catalog products
  useEffect(() => {
    async function loadCatalog() {
      setLoadingProducts(true);
      try {
        const res = await fetchProducts();
        if (res.products && res.products.length > 0) {
          setProducts(res.products);
          const first = res.products[0];
          setSelectedProductId(first.product_id);
          setCurrentPrice(first.mean_price);
          setProposedPrice(round2(first.mean_price * 1.05));
          setInventoryLevel(first.mean_inventory);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoadingProducts(false);
      }
    }
    loadCatalog();
  }, []);

  const round2 = (val) => Math.round(val * 100) / 100;

  // When product dropdown changes
  const handleProductChange = (prodId) => {
    setSelectedProductId(prodId);
    const prod = products.find(p => p.product_id === prodId);
    if (prod) {
      setCurrentPrice(prod.mean_price);
      setProposedPrice(round2(prod.mean_price * 1.05));
      setInventoryLevel(prod.mean_inventory);
    }
  };

  const handlePresetScenario = (pct) => {
    setProposedPrice(round2(currentPrice * (1 + pct)));
  };

  // Run simulation
  const handleRunSimulation = async () => {
    setLoading(true);
    try {
      const payload = {
        product_id: selectedProductId,
        current_price: parseFloat(currentPrice),
        proposed_price: parseFloat(proposedPrice),
        inventory_level: parseFloat(inventoryLevel),
        cost_per_unit: costPerUnit !== '' ? parseFloat(costPerUnit) : null,
        specification: specification
      };
      const res = await simulatePrice(payload);
      setSimulationResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Run initial simulation on product selection
  useEffect(() => {
    if (currentPrice && proposedPrice) {
      handleRunSimulation();
    }
  }, [selectedProductId, specification]);

  return (
    <div className="space-y-8 pb-12">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">Interactive Price Scenario Simulator</h2>
        <p className="text-xs text-slate-500 mt-1">
          Counterfactual pricing decision support combining Double Machine Learning sensitivity with operational shelf inventory caps.
        </p>
      </div>

      {/* Simulator Control Board */}
      <div className="bg-white rounded-xl border border-slate-200/80 p-6 shadow-xs">
        <div className="flex items-center justify-between mb-5 pb-4 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <SlidersHorizontal className="w-4 h-4 text-emerald-600" />
            <h3 className="text-sm font-bold text-slate-800">Scenario Parameter Controls</h3>
          </div>
          <span className="text-xs px-2.5 py-1 bg-emerald-50 text-emerald-800 font-medium rounded-full border border-emerald-200">
            Causal Engine Active
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Product selector */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-600">Select Product (SKU):</label>
            <select
              value={selectedProductId}
              onChange={(e) => handleProductChange(e.target.value)}
              className="w-full text-xs bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-800 focus:outline-emerald-500 font-medium"
            >
              {products.map((p) => (
                <option key={p.product_id} value={p.product_id}>
                  {p.product_id} — {p.category} (${p.mean_price.toFixed(2)})
                </option>
              ))}
            </select>
            <div className="text-[11px] text-slate-400">Loads product category and baseline history</div>
          </div>

          {/* Current Price (Baseline) */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-600">Current Price ($):</label>
            <div className="relative">
              <span className="absolute left-3 top-2 text-xs text-slate-400">$</span>
              <input
                type="number"
                step="0.1"
                value={currentPrice}
                onChange={(e) => setCurrentPrice(e.target.value)}
                className="w-full text-xs bg-slate-50 border border-slate-200 rounded-lg pl-7 pr-3 py-2 text-slate-800 font-mono"
              />
            </div>
            <div className="text-[11px] text-slate-400">Baseline observational selling price</div>
          </div>

          {/* Proposed Price */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-600">Proposed New Price ($):</label>
            <div className="relative">
              <span className="absolute left-3 top-2 text-xs text-slate-400">$</span>
              <input
                type="number"
                step="0.1"
                value={proposedPrice}
                onChange={(e) => setProposedPrice(e.target.value)}
                className="w-full text-xs bg-white border border-emerald-300 rounded-lg pl-7 pr-3 py-2 text-slate-900 font-mono font-bold focus:outline-emerald-500"
              />
            </div>
            {/* Quick preset buttons */}
            <div className="flex items-center gap-1 mt-1.5">
              {[-0.10, -0.05, 0.00, 0.05, 0.10].map((pct) => (
                <button
                  key={pct}
                  onClick={() => handlePresetScenario(pct)}
                  className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 hover:bg-emerald-100 hover:text-emerald-800 text-slate-600 transition-colors"
                >
                  {pct >= 0 ? `+${pct * 100}%` : `${pct * 100}%`}
                </button>
              ))}
            </div>
          </div>

          {/* Inventory Cap */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-600">Inventory Level (Units):</label>
            <input
              type="number"
              value={inventoryLevel}
              onChange={(e) => setInventoryLevel(e.target.value)}
              className="w-full text-xs bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-800 font-mono"
            />
            <div className="text-[11px] text-slate-400">Physical stock ceiling (Sales ≤ Inventory)</div>
          </div>
        </div>

        {/* Second Row: Optional Cost & Specification */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6 pt-5 border-t border-slate-100 text-xs">
          <div>
            <label className="font-semibold text-slate-600 block mb-1.5">Unit Procurement Cost (Optional):</label>
            <div className="relative">
              <span className="absolute left-3 top-2 text-slate-400">$</span>
              <input
                type="number"
                step="0.5"
                placeholder="Enter COGS to evaluate profit"
                value={costPerUnit}
                onChange={(e) => setCostPerUnit(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-7 pr-3 py-2 text-slate-800 font-mono"
              />
            </div>
            <div className="text-[10px] text-slate-400 mt-1">If blank, top-line revenue is displayed</div>
          </div>

          <div>
            <label className="font-semibold text-slate-600 block mb-1.5">DML Specification:</label>
            <select
              value={specification}
              onChange={(e) => setSpecification(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-800 font-medium"
            >
              <option value="spec1">Spec 1: Core Controls (Primary θ = +0.0107)</option>
              <option value="spec2">Spec 2: With Inventory Control (θ = -0.0195)</option>
            </select>
            <div className="text-[10px] text-slate-400 mt-1">Spec 1 recommended for unconfounded sensitivity</div>
          </div>

          <div className="flex items-end">
            <button
              onClick={handleRunSimulation}
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 py-2 px-4 bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg font-semibold text-xs shadow-sm transition-all"
            >
              {loading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
              <span>Run Scenario Simulation</span>
            </button>
          </div>
        </div>
      </div>

      {/* Simulation Results Display */}
      {simulationResult && (
        <div className="space-y-6">
          {/* Extrapolation Warning Alert if any */}
          {simulationResult.simulation.extrapolates && (
            <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-amber-900 text-xs flex items-center gap-3">
              <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
              <span>
                <strong>Extrapolation Warning:</strong> The proposed price (${simulationResult.simulation.proposed_price.toFixed(2)}) falls outside the observed empirical price bounds ($10.00 – $100.00). Projections may carry high variance.
              </span>
            </div>
          )}

          {/* Side-by-Side Comparison Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              title="Price Delta"
              value={`$${simulationResult.simulation.proposed_price.toFixed(2)}`}
              subtitle={`From $${simulationResult.baseline.price.toFixed(2)} (${simulationResult.simulation.price_change_pct >= 0 ? '+' : ''}${simulationResult.simulation.price_change_pct}%)`}
              icon={DollarSign}
              badgeText={`${simulationResult.simulation.price_change_pct >= 0 ? '+' : ''}$${simulationResult.simulation.price_delta.toFixed(2)}`}
              badgeType={simulationResult.simulation.price_delta >= 0 ? 'success' : 'neutral'}
            />

            <MetricCard
              title="Realized Sales"
              value={`${simulationResult.simulation.realized_sales.toFixed(1)} u/d`}
              subtitle={`Baseline: ${simulationResult.baseline.demand.toFixed(1)} u/d`}
              icon={Package}
              badgeText={simulationResult.simulation.is_inventory_binding ? 'Capped by Stock' : 'Unconstrained'}
              badgeType={simulationResult.simulation.is_inventory_binding ? 'warning' : 'neutral'}
              tooltip="Realized sales equals min(Predicted Demand, Inventory Level)."
            />

            <MetricCard
              title="Estimated Daily Revenue"
              value={`$${simulationResult.simulation.estimated_revenue.toLocaleString()}`}
              subtitle={`Baseline: $${simulationResult.baseline.revenue.toLocaleString()}`}
              icon={TrendingUp}
              badgeText={`${simulationResult.simulation.revenue_change_pct >= 0 ? '+' : ''}${simulationResult.simulation.revenue_change_pct}%`}
              badgeType={simulationResult.simulation.revenue_change_pct >= 0 ? 'success' : 'warning'}
            />

            <MetricCard
              title="Revenue Change ($)"
              value={`${simulationResult.simulation.revenue_change_dollars >= 0 ? '+' : ''}$${simulationResult.simulation.revenue_change_dollars.toLocaleString()}`}
              subtitle={`95% CI: [$${simulationResult.simulation.ci_low_revenue.toLocaleString()}, $${simulationResult.simulation.ci_high_revenue.toLocaleString()}]`}
              icon={Scale}
              badgeText={simulationResult.simulation.revenue_change_dollars >= 0 ? 'Expansion' : 'Contraction'}
              badgeType={simulationResult.simulation.revenue_change_dollars >= 0 ? 'success' : 'warning'}
            />
          </div>

          {/* Profit Section (Only if COGS provided) */}
          {simulationResult.profit_analysis ? (
            <div className="bg-emerald-50/70 border border-emerald-200 rounded-xl p-5 shadow-xs">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-700" />
                  <h4 className="text-xs font-bold text-emerald-950 uppercase tracking-wider">
                    Profitability & Margin Impact (Unit Cost: ${simulationResult.profit_analysis.unit_cost.toFixed(2)})
                  </h4>
                </div>
                <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800">
                  Margin: {simulationResult.profit_analysis.margin_current_pct}% → {simulationResult.profit_analysis.margin_proposed_pct}%
                </span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
                <div>
                  <div className="text-slate-500">Baseline Profit:</div>
                  <div className="text-base font-bold text-slate-800 font-mono mt-0.5">
                    ${simulationResult.profit_analysis.baseline_profit.toLocaleString()}
                  </div>
                </div>
                <div>
                  <div className="text-slate-500">Proposed Profit:</div>
                  <div className="text-base font-bold text-emerald-800 font-mono mt-0.5">
                    ${simulationResult.profit_analysis.proposed_profit.toLocaleString()}
                  </div>
                </div>
                <div>
                  <div className="text-slate-500">Profit Dollar Change:</div>
                  <div className={`text-base font-bold font-mono mt-0.5 ${simulationResult.profit_analysis.profit_change_dollars >= 0 ? 'text-emerald-700' : 'text-rose-700'}`}>
                    {simulationResult.profit_analysis.profit_change_dollars >= 0 ? '+' : ''}${simulationResult.profit_analysis.profit_change_dollars.toLocaleString()}
                  </div>
                </div>
                <div>
                  <div className="text-slate-500">Profit Percentage Change:</div>
                  <div className={`text-base font-bold font-mono mt-0.5 ${simulationResult.profit_analysis.profit_change_pct >= 0 ? 'text-emerald-700' : 'text-rose-700'}`}>
                    {simulationResult.profit_analysis.profit_change_pct >= 0 ? '+' : ''}{simulationResult.profit_analysis.profit_change_pct}%
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl text-slate-600 text-xs flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Info className="w-4 h-4 text-slate-400" />
                <span>
                  <strong>Profit Assessment Note:</strong> Dataset contains no unit cost (COGS). Revenue changes are shown above. Enter a unit cost in the control panel to view net margin and profit projections.
                </span>
              </div>
            </div>
          )}

          {/* Multi-Scenario Grid Table */}
          <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
            <div className="p-4 border-b border-slate-100 flex items-center justify-between">
              <div>
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                  Multi-Scenario Sensitivity Matrix (±15% Range)
                </h4>
                <p className="text-[11px] text-slate-400">Comparing candidate price steps subject to physical inventory cap ({simulationResult.baseline.inventory} units)</p>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-slate-50 text-slate-500 font-semibold uppercase text-[10px] border-b border-slate-100">
                  <tr>
                    <th className="py-2.5 px-4">Scenario</th>
                    <th className="py-2.5 px-4 text-right">Price</th>
                    <th className="py-2.5 px-4 text-right">Raw Demand</th>
                    <th className="py-2.5 px-4 text-right">Realized Sales</th>
                    <th className="py-2.5 px-4 text-right">Est. Revenue</th>
                    <th className="py-2.5 px-4 text-right">Rev Change ($)</th>
                    <th className="py-2.5 px-4 text-right">Rev Change (%)</th>
                    <th className="py-2.5 px-4 text-center">Stockout?</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-slate-700">
                  {simulationResult.multi_scenario_grid?.map((row) => {
                    const isCurrent = row.scenario === '+0%';
                    return (
                      <tr key={row.scenario} className={`hover:bg-slate-50/70 ${isCurrent ? 'bg-emerald-50/40 font-semibold' : ''}`}>
                        <td className="py-2.5 px-4 font-mono font-medium text-slate-900">
                          {row.scenario} {isCurrent && <span className="text-[10px] text-emerald-700">(Baseline)</span>}
                        </td>
                        <td className="py-2.5 px-4 text-right font-mono">${row.price.toFixed(2)}</td>
                        <td className="py-2.5 px-4 text-right font-mono">{row.predicted_demand.toFixed(1)}</td>
                        <td className="py-2.5 px-4 text-right font-mono font-bold">{row.realized_sales.toFixed(1)}</td>
                        <td className="py-2.5 px-4 text-right font-mono">${row.estimated_revenue.toLocaleString()}</td>
                        <td className={`py-2.5 px-4 text-right font-mono ${row.revenue_change_dollars >= 0 ? 'text-emerald-700' : 'text-slate-500'}`}>
                          {row.revenue_change_dollars >= 0 ? '+' : ''}${row.revenue_change_dollars.toLocaleString()}
                        </td>
                        <td className={`py-2.5 px-4 text-right font-mono font-bold ${row.revenue_change_pct >= 0 ? 'text-emerald-700' : 'text-slate-500'}`}>
                          {row.revenue_change_pct >= 0 ? '+' : ''}{row.revenue_change_pct}%
                        </td>
                        <td className="py-2.5 px-4 text-center">
                          {row.inventory_binding ? (
                            <span className="px-1.5 py-0.5 rounded text-[10px] bg-amber-100 text-amber-800 font-medium">Binding</span>
                          ) : (
                            <span className="px-1.5 py-0.5 rounded text-[10px] bg-slate-100 text-slate-500">Normal</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
