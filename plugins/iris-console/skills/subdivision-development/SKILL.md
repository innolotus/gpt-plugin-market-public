---
name: subdivision-development
description: Model subdivision or multi-dwelling development with timed costs, finance, sales, tax treatment and evidence constraints.
metadata:
  product: Iris Console
  version: 0.5.0
  portable: true
---

# Subdivision Development

## Purpose

Model:

```text
Acquire → Planning / subdivision → Demolish where required → Create multiple assets → Sell / Hold
```

This is the primary value-creation model for professional investors / small developers where land and planning utility may support multiple dwellings or titles.

## Inputs

- PropertyProfile;
- MARKET-phase AcquisitionPriceAssessment where available;
- PlanningAssessment;
- site dimensions / frontage where available;
- title / easement evidence where available;
- proposed development scenarios;
- model acquisition-price scenario(s);
- demolition cost where required;
- subdivision / civil / service costs;
- build area and cost;
- consultants / approvals;
- contingency;
- timed holding-cost assumptions;
- DevelopmentFinanceAssumptions where levered modelling is requested;
- comparable end-value evidence;
- project duration;
- client/default target project margin or IRR where explicitly defined;
- applicable versioned AssumptionSet / EffectiveAssumptionSet.

## Assumption-set rules

Load the active subdivision-development AssumptionSet from `Console/Assumptions/registry.yaml`.

Use maintained defaults only where defined.

The base set intentionally does not provide a generic dwelling count, build cost, project duration or GRV.

These must come from:

- planning/market evidence;
- explicit user/client assumptions;
- source-derived scenario assumptions.

Never derive a default dwelling count from land area alone.

Build an EffectiveAssumptionSet, preserve all overrides, and keep the base set immutable.

## Planning discipline

Do not infer:

```text
land area ÷ assumed minimum lot size = approved dwelling count
```

Planning feasibility must consider, where relevant:

- zone;
- overlays;
- minimum site area;
- frontage;
- site shape;
- access;
- parking;
- private open space;
- trees;
- easements;
- services;
- stormwater;
- title;
- referral / approval requirements.

A development scenario may be modelled as ASSUMPTION while planning remains unresolved, but must be labelled accordingly.

## Acquisition-price discipline

Each scenario must retain `modelAcquisitionPrice`.

Do not equate expected transaction price with the maximum economically supportable land/acquisition price.

## Strategy maximum price

Where a transparent target margin or IRR exists, reverse-calculate the maximum acquisition price that satisfies it.

If no target exists:

- return break-even acquisition price and project economics;
- set StrategyMaximumPrice to UNKNOWN unless a documented default target exists.

## Scenario generation

Where evidence supports it, compare plausible variants such as:

- retain + rear development;
- demolish + 2 dwellings;
- demolish + 3 dwellings;
- other site-specific configuration.

Do not create implausible density merely to maximise GRV.

## EvidenceState rules

Planning or title facts that are CONFLICTED, STALE, UNVERIFIED or UNKNOWN must remain visible.

Do not silently convert marketing claims such as "development potential" into confirmed planning capacity.

If financial scenario modelling is still useful before planning confirmation:

- mark dwelling count/site yield as ASSUMPTION;
- retain planning confidence;
- show the decision impact if the assumption fails.

## Timed development cash flow

Do not calculate development IRR from a single aggregate `financeAndHolding` number.

Build a DevelopmentCashFlow timeline for each scenario.

Recommended default granularity:

```text
MONTHLY
```

Include where relevant:

- acquisition / duty / transaction costs;
- planning and consultants;
- demolition;
- subdivision / civil / services;
- construction stages;
- rates/insurance/other holding costs;
- temporary rental income;
- marketing and sale costs;
- each dwelling's sale settlement proceeds;
- debt draw;
- interest;
- debt repayment;
- equity contribution.

For multiple dwellings, sale proceeds may occur in different periods.

Do not recognize sale proceeds merely because marketing has started.

### Unlevered vs levered return

Separate:

- `unleveredProjectIrr`;
- `leveredEquityIrr`.

Unlevered project IRR excludes financing flows.

Levered equity IRR is calculated from the equity cash-flow series after financing effects.

If financing structure is materially incomplete:

```text
leveredEquityIrr = UNKNOWN
```

Do not invent a lender facility or draw schedule.

### Construction timing

If no real builder draw schedule exists, use an explicit staged scenario from the EffectiveAssumptionSet or user/client assumption.

Do not place all construction cost at settlement by default.

## Return-basis and tax-treatment rules

Default project economics are:

```text
ReturnBasis = PRE_TAX
TaxModelStatus = NOT_MODELLED
```

Unless explicitly modelled, keep visible:

- GST treatment;
- GST margin-scheme applicability;
- income-tax/entity treatment;
- land tax;
- other material project tax effects.

Where applicability itself is unresolved, use UNKNOWN rather than EXCLUDED.

A raw feasibility profit, margin or IRR is not an after-tax developer return.

Only use AFTER_TAX_ESTIMATE when a defined tax model explicitly identifies the included components and assumptions.

## Deterministic calculations

For each scenario calculate where inputs permit:

- acquisition;
- demolition;
- subdivision / civil / services;
- construction;
- soft cost;
- contingency;
- timed holding costs;
- total finance interest;
- peak debt;
- peak equity at risk;
- total development cost;
- per-dwelling GRV;
- total GRV;
- profit;
- profit margin;
- unlevered project IRR;
- levered equity IRR where financing inputs permit;
- residual land value;
- break-even acquisition price;
- StrategyMaximumPrice;
- sensitivity to build cost, duration and GRV.

## Temporary hold

If the property can generate rent before development:

```text
Acquire → Rent during approval period → Develop
```

model rental as carrying-cost mitigation, not a fourth strategy.

## Output

Return SubdivisionDevelopmentResult for each plausible scenario plus:

- modelAcquisitionPrice;
- developmentCashFlows[];
- financeSummary;
- StrategyMaximumPrice where supported;
- planning confidence;
- assumptions;
- blocking unknowns;
- sensitivity;
- evidence confidence;
- ReturnBasis;
- TaxTreatment;
- next verification steps.

## Guardrails

Do not:

- present development potential as approval;
- present speculative dwelling counts as FACT;
- hide planning/infrastructure unknowns because the financial model looks attractive;
- call StrategyMaximumPrice a market valuation or vendor acceptance estimate;
- present PRE_TAX project economics as after-tax returns;
- report levered equity IRR when financing structure is materially unknown.
