---
name: replacement-development
description: Model acquisition, demolition, replacement construction, finance, holding and exit for a one-for-one development strategy.
metadata:
  product: Iris Console
  version: 0.5.0
  portable: true
---

# Replacement Development

## Purpose

Model:

```text
Acquire low-improvement-value asset → Demolish → Build one replacement asset → Sell / Hold
```

This strategy is appropriate to test when the existing building has little economic utility relative to the underlying land and expected replacement value.

## Typical triggers

Evidence may include:

- uninhabitable condition;
- severe structural/building-system obsolescence;
- repair/renovation cost approaching replacement economics;
- market evidence that the property is effectively trading as land;
- existing improvement contributes little to acquisition value.

Age alone is not a trigger.

## Inputs

- MARKET-phase AcquisitionPriceAssessment where available;
- model acquisition-price scenario(s);
- evidence of existing improvement utility;
- demolition / remediation cost;
- site works;
- build area / specification;
- construction cost;
- consultant / design / approval costs;
- contingency;
- timed holding-cost assumptions;
- DevelopmentFinanceAssumptions where levered modelling is requested;
- sale or hold assumptions;
- finished-value / GRV evidence;
- project duration;
- client/default target project margin or IRR where explicitly defined;
- applicable versioned AssumptionSet / EffectiveAssumptionSet.

## Assumption-set rules

Load the active replacement-development AssumptionSet from `Console/Assumptions/registry.yaml`.

Use the static defaults only for fields that actually define a maintained default.

Project-specific fields such as construction, demolition/remediation, finance rate and duration may intentionally be `requiredInput: true`.

For those fields:

- prefer explicit user/client/project evidence;
- otherwise use a clearly-labelled SOURCE_DERIVED_ASSUMPTION where supportable;
- otherwise leave missing or model explicit scenarios;
- never invent a value merely to complete the feasibility table.

Build and retain an EffectiveAssumptionSet without modifying the base set.

A client/user override changes the scenario input, not its evidential class.

## Acquisition-price discipline

Use `modelAcquisitionPrice` for each scenario.

Do not equate:

- expected market acquisition price;
- land value;
- break-even acquisition price;
- strategy maximum price.

They answer different questions.

## Strategy maximum price

Where a transparent target project margin or IRR exists, reverse-calculate the maximum acquisition price that satisfies it.

If no target exists, return:

- break-even acquisition price;
- scenario economics;

and set StrategyMaximumPrice to UNKNOWN unless a versioned default target is defined.

## Core test

```text
Finished single-asset value
vs
Acquisition + demolition + rebuild + soft + holding + transaction cost
```

The model must explicitly recognise economic value destroyed by demolition.

## EvidenceState rules

Do not treat:

- unverified build cost;
- conflicted finished-value evidence;
- stale sale comparables;
- unknown remediation/asbestos/site cost;

as confirmed inputs.

If a scenario must proceed, convert the chosen value to ASSUMPTION and run sensitivity where material.

## Timed development cash flow

Do not model project finance as a single opaque `financeAndHolding` input when calculating development IRR.

Build a DevelopmentCashFlow timeline.

Recommended default granularity:

```text
MONTHLY
```

The timeline should place, where relevant:

- acquisition and transaction costs;
- planning/design/consultant spend;
- demolition/remediation;
- construction draw stages;
- rates/insurance/other holding costs;
- temporary rental income;
- marketing/selling costs;
- sale proceeds;
- debt draw;
- interest;
- debt repayment;
- equity contribution.

Do not fabricate exact dates. Use period-based scenario timing when dates are unknown.

### Unlevered vs levered return

Always distinguish:

- `unleveredProjectIrr`;
- `leveredEquityIrr`.

Unlevered project IRR uses project cash flows before financing flows.

Levered equity IRR uses the equity cash-flow series after debt draw, interest and repayment.

If finance rate, facility/drawdown assumptions or repayment rules are insufficient:

```text
leveredEquityIrr = UNKNOWN
```

Do not back-solve a fictional lender facility merely to make levered IRR appear.

### Interest discipline

If interest is calculated from the debt timeline, do not also include the same interest in another aggregate finance-cost input.

Holding costs and finance interest are different categories.

## Return-basis and tax-treatment rules

Default project economics are:

```text
ReturnBasis = PRE_TAX
TaxModelStatus = NOT_MODELLED
```

Unless explicitly modelled, disclose material tax components such as:

- GST;
- GST margin-scheme applicability;
- income-tax/entity treatment;
- land tax;
- other project-specific tax treatment.

Use UNKNOWN where applicability/treatment is unresolved.

Including stamp duty or one transaction tax in project cost does not make the profit AFTER_TAX_ESTIMATE.

Do not describe project profit as money available to the developer after tax unless a defined tax model supports that statement.

## Deterministic calculations

Where inputs permit:

- effective land acquisition cost;
- demolition/remediation;
- build cost;
- soft cost;
- timed holding costs;
- total finance interest;
- peak debt;
- peak equity at risk;
- total development cost;
- finished value;
- profit;
- profit margin;
- unlevered project IRR;
- levered equity IRR where financing inputs permit;
- break-even acquisition price;
- StrategyMaximumPrice;
- break-even build cost;
- sensitivity to finished value.

## Decision states

- ECONOMICALLY_PLAUSIBLE
- MARGINAL
- WEAK
- INSUFFICIENT_EVIDENCE
- NOT_APPLICABLE

## Output

Return ReplacementDevelopmentResult plus:

- modelAcquisitionPrice;
- developmentCashFlows[];
- financeSummary;
- StrategyMaximumPrice where supported;
- reason existing improvement is treated as low utility;
- assumptions;
- unknowns;
- sensitivity;
- evidence confidence;
- ReturnBasis;
- TaxTreatment;
- next verification steps.

## Guardrails

Do not:

- assume demolition merely because the building is old;
- value a finished new dwelling from one nearby sale;
- omit the economic value destroyed by demolition;
- call StrategyMaximumPrice a market valuation;
- present PRE_TAX development profit as after-tax proceeds;
- report levered equity IRR when financing structure is materially unknown.
