---
name: strategy-comparison
description: Compare compatible property strategies across price, capital, time, return, risk and uncertainty without collapsing them into a misleading score.
metadata:
  product: Iris Console
  version: 0.3.0
  portable: true
---

# Strategy Comparison

## Purpose

Compare economically plausible uses of a property without forcing unlike strategies or incompatible tax bases into one misleading score.

## Inputs

Any available strategy results:

- IncomeInvestmentResult
- ReplacementDevelopmentResult
- SubdivisionDevelopmentResult[]

Also consume:

- ClientProfile;
- FinancialSnapshot where relevant;
- AcquisitionContext;
- AssetUtilityAssessment;
- MarketAssessment;
- PlanningAssessment;
- DueDiligenceResult;
- FINAL AcquisitionPriceAssessment.

## Comparison dimensions

Compare at least:

- initial capital required;
- debt / funding requirement;
- acquisition-price gap;
- duration;
- cash-flow profile;
- liquidity;
- execution complexity;
- planning risk;
- construction risk;
- market / exit risk;
- maintenance risk;
- principal return metrics;
- tax/return basis;
- downside sensitivity;
- unresolved unknowns.

## Metric discipline

Use metrics appropriate to each strategy.

Income Investment:

- cash-on-cash;
- annual cash flow;
- 10-year equity;
- leveraged IRR.

Development:

- project margin;
- unlevered project IRR;
- levered equity IRR where available;
- profit;
- residual land value;
- duration.

Do not compare nominal 10-year ROI directly with an 18-month development ROI and call the larger number "better".

## Development finance comparability

For development strategies distinguish:

- unleveredProjectIrr;
- leveredEquityIrr;
- peakDebt;
- peakEquityAtRisk;
- totalFinanceInterest.

Do not compare one strategy's levered equity IRR with another strategy's unlevered project IRR as if they were the same metric.

If a financing structure is absent, keep leveredEquityIrr UNKNOWN and compare unlevered economics plus capital/risk dimensions.

## ReturnBasis compatibility

Before ranking return metrics, inspect each strategy's ReturnBasis and TaxTreatment.

### Compatible examples

```text
PRE_TAX vs PRE_TAX
```

can be compared on tax basis, subject to other model differences.

```text
AFTER_TAX_ESTIMATE vs AFTER_TAX_ESTIMATE
```

may be compared only when tax assumptions and scope are materially compatible.

### Incompatible example

```text
PRE_TAX vs AFTER_TAX_ESTIMATE
```

must not be directly ranked by IRR/profit.

Return:

```text
returnBasisCompatibility = INCOMPATIBLE
```

and explain the mismatch.

Other dimensions such as capital required, duration, liquidity, planning risk and execution complexity may still be compared.

## Tax uncertainty

If development GST, margin scheme, income-tax/entity treatment or other material tax effects are UNKNOWN, preserve those unknowns in comparison.

Do not reward a strategy simply because its unmodelled tax burden makes its headline profit look larger.

## User-fit interpretation

The same asset may produce different conclusions for:

- an individual investor;
- a professional investor;
- a small developer.

Strategy fit must consider capability and objective, not return alone.

## Output

Return StrategyComparison with:

- strategies modelled;
- key economics;
- development finance summary where applicable;
- acquisition-price gap summary;
- ReturnBasis by strategy;
- returnBasisCompatibility;
- taxBasisWarnings[];
- key risks;
- key unknowns;
- investor/client fit;
- strongest strategy under stated assumptions where comparison is valid;
- conditions that would change the ranking;
- next verification steps.

## Decision language

Prefer:

- strongest under current assumptions;
- strongest on a PRE_TAX basis;
- economically plausible;
- worth further feasibility;
- weak under current assumptions;
- return metrics not directly comparable due to tax-basis mismatch;
- blocked by material unknowns.

Avoid unsupported:

- guaranteed best option;
- guaranteed return;
- certain approval;
- must buy / must develop.

## No opaque score

Do not collapse the result into a single 0–100 score unless a client explicitly defines a transparent scoring framework.
