# Day 12: Inventory Constraints and Pricing Recommendations

**Date:** 23 October 2026

## Objective
Apply an inventory-level constraint to the Day 11 pricing scenarios, rank scenarios by inventory-constrained estimated revenue, and produce a transparent pricing recommendation prototype with documented assumptions and warnings.

## Tasks Completed
- Loaded the validated Day 10 DML results and Day 11 simulator output from JSON files.
- Checked all reliability conditions before producing recommendations.
- Examined Inventory Level definition, documented timing ambiguity.
- Applied a provisional inventory cap (195 units for this product-store observation).
- Computed inventory-constrained units and revenue for each scenario.
- Ranked scenarios by inventory-constrained estimated revenue (descending).
- Produced a baseline comparison table.
- Produced two visualisations: unconstrained vs capped units bar chart, and revenue ranking bar chart.
- Documented active warnings, assumptions, and limitations.

## Actual Results

**Baseline observation (P0001, Store S001):**
- Price: $55.13 | Units: 173 | Revenue: $9,537.49
- Inventory Level: 195 (timing uncertain — cap applied provisionally)
- DML θ (Spec 1): +0.010699 (p = 0.4899, NOT statistically significant)

**Active Warnings (all raised):**
1. DML coefficient NOT statistically significant (p ≈ 0.49). Revenue rankings are highly uncertain.
2. Coefficient shifts 282% when Inventory Level added as control — highly sensitive to control set.
3. Inventory Level timing is unknown — cap is PROVISIONAL.
4. Unit cost unavailable — revenue ranking ≠ profit ranking.

**Inventory constraint result:** No scenario exceeded the provisional cap of 195 units (maximum estimated units ≈ 173.1). The inventory cap did not bind in any scenario, so capped and uncapped estimates are identical.

| Rank | Scenario | Price ($) | Units (capped) | Revenue (capped) ($) | Rev Change (%) |
|---|---|---|---|---|---|
| 1 | +10% | 60.64 | 173.1 | 10,494.82 | +10.04% |
| 2 | +5% | 57.89 | 173.0 | 10,016.07 | +5.02% |
| 3 | 0% (baseline) | 55.13 | 173.0 | 9,537.49 | 0.00% |
| 4 | −5% | 52.37 | 173.0 | 9,059.07 | −5.02% |
| 5 | −10% | 49.62 | 172.9 | 8,580.81 | −10.03% |

**Baseline vs Top-Ranked (Rank 1):**

| Metric | Baseline (0%) | Top-ranked (+10%) |
|---|---|---|
| Price ($) | 55.13 | 60.64 |
| Est. Units | 173.0 | 173.1 |
| Est. Revenue ($) | 9,537.49 | 10,494.82 |
| Rev Change ($) | 0.00 | +957.33 |
| Rev Change (%) | 0.00% | +10.04% |

## Key Findings
1. The +10% price scenario is ranked first by estimated revenue. This is **entirely driven by the price increase** — not by any meaningful demand response — because θ ≈ 0.
2. The inventory cap (195 units) did not bind for any scenario. Estimated demand is well below the cap in all cases.
3. Both the DML estimate and the ranking are **scientifically unreliable** given the non-significance of the coefficient and its extreme sensitivity to control selection.
4. The ranking order is deterministic given the inputs, but the inputs themselves are uncertain.

## Limitations and Assumptions
1. **Linear demand approximation:** Valid only locally near the baseline price; results are unreliable far from it.
2. **Statistically insignificant coefficient:** p ≈ 0.49. Any direction of demand response is plausible given the data.
3. **Control sensitivity:** The coefficient switches sign and magnitude significantly between Spec 1 and Spec 2.
4. **Inventory timing unknown:** The inventory cap is provisional. We cannot confirm whether Inventory Level represents available stock at the time of sale.
5. **No unit costs:** Revenue maximisation ≠ profit maximisation. The top-ranked scenario may generate less profit if variable costs are high.
6. **Missing confounders:** Promotions, competitor prices, holidays, and other demand drivers are absent.
7. **Single product-store:** Results apply to P0001 at S001 only; generalisation is not supported.
8. **Research prototype:** This notebook is a demonstration of a pricing workflow, not a production system. No automatic pricing decision should be made based on these outputs.

## Next Steps
- Collect unit cost data to enable profit-based ranking.
- Investigate data sources for promotions, competitor prices, and demand drivers.
- Consider richer demand models that account for non-linearity.
- Validate causal assumptions (e.g., instrument search, placebo tests) before reporting causal interpretation.
- Extend analysis to more product-store combinations.
