---
name: income-investment
description: Model an Australian residential income-investment strategy across acquisition, rent, cash flow, debt, equity and exit.
metadata:
  product: Iris Console
  version: 0.5.0
  portable: true
---

# Income Investment

## Purpose

Model the strategy:

```text
Acquire → Rent → Hold → Build equity → Exit / continue
```

This is the primary model for individual / non-professional investors and for assets whose existing improvement retains meaningful rental and economic utility.

## Inputs

Required or explicitly assumed:

- MARKET-phase AcquisitionPriceAssessment where available;
- one or more model acquisition-price scenarios;
- PurchaseAssistanceAssessment where relevant;
- FinancialSnapshot where client-specific financing is required;
- acquisition costs;
- deposit / LVR;
- lender loan terms;
- current/initial rent;
- vacancy;
- management;
- recurring operating expenses;
- maintenance allowance;
- capital growth assumption;
- rental growth assumption;
- holding horizon;
- exit cost assumptions;
- target return / cash-flow constraint where supplied;
- applicable versioned AssumptionSet / EffectiveAssumptionSet.

## Assumption-set rules

Load the active income-investment AssumptionSet from `Console/Assumptions/registry.yaml`.

Build an EffectiveAssumptionSet for the run.

Use override precedence:

1. USER_ASSUMPTION;
2. CLIENT_ORG_ASSUMPTION;
3. SOURCE_DERIVED_ASSUMPTION;
4. DEFAULT_ASSUMPTION.

Do not mutate the base AssumptionSet.

Do not silently invent values marked `requiredInput: true`.

Current mortgage rate should prefer current client/lender or explicit source-derived input rather than a static generic rate.

Every model result must identify:

- base assumption-set ID/version;
- overrides applied;
- effective material assumptions.

A user override remains ASSUMPTION unless independently established as FACT.

## Acquisition-price discipline

Do not treat `expectedAcquisitionRange` as a single guaranteed purchase price.

Prefer modelling one or more explicit scenarios, for example:

- expected-range low;
- expected-range midpoint/base;
- expected-range high;
- client target purchase price where supplied.

Each result must retain:

`modelAcquisitionPrice`

as the scenario input.

## Strategy maximum price

Where the client or versioned assumption set defines a target constraint, reverse-calculate the maximum acquisition price that still satisfies it.

Possible targets:

- minimum leveraged IRR;
- minimum cash-on-cash return;
- maximum annual cash deficit;
- maximum initial cash requirement;
- other transparent client-defined constraint.

Do not invent a target return merely to produce a maximum price.

If no target exists:

- return break-even/threshold metrics where meaningful;
- set StrategyMaximumPrice to UNKNOWN unless a documented default target is explicitly part of the assumption set.

## Financing rule

Do not default to 20% deposit.

Generate financing scenarios based on the buyer's actual intended use and current eligibility.

Owner-occupier assistance is not available for an investment-from-settlement strategy unless the current program explicitly permits that use.

## Evidence discipline

Separate:

- observed rent → FACT;
- advertised/agent rental appraisal → FACT about the appraisal;
- government program eligibility → FACT only when supported;
- future rent growth → ASSUMPTION;
- annual rental calculation → CALCULATION;
- sustainability conclusion → INFERENCE.

A material rent/value input with EvidenceState other than CONFIRMED must not be silently treated as confirmed.

If scenario modelling remains useful, convert the chosen scenario input into an explicit ASSUMPTION and preserve the unresolved evidence state.

## Acquisition cash calculation

Explicitly distinguish:

```text
Purchase Price
- Buyer Deposit
- Government Equity Contribution (if any)
= Lender Funding Requirement, subject to scheme/lender rules

Upfront Cash Required
= Buyer Deposit
+ Stamp Duty after relief
+ Legal / registration / inspection / other costs
- Cash Grant usable at settlement, where confirmed
```

A government guarantee is not cash.

## Return-basis and tax-treatment rules

Default:

```text
ReturnBasis = PRE_TAX
TaxModelStatus = NOT_MODELLED
```

Stamp duty/acquisition costs may be included while the overall model remains PRE_TAX.

Do not silently include:

- negative-gearing tax benefits;
- the client's marginal income-tax rate;
- CGT discount/treatment;
- depreciation/capital-works deductions;
- land-tax effects;

unless an explicit tax model is being used.

If one or more tax components are included but the model is incomplete:

```text
TaxModelStatus = PARTIALLY_MODELLED
ReturnBasis = PRE_TAX
```

Only use AFTER_TAX_ESTIMATE when a defined tax model explicitly supports it and all material included/excluded components are disclosed.

## Deterministic model

Project Years 1–10 where the horizon permits.

Each year should include:

- projected property value;
- gross rent;
- vacancy loss;
- operating expenses;
- maintenance / CapEx allowance;
- interest;
- principal repayment;
- net cash flow;
- loan balance;
- equity;
- cash-on-cash return;
- total return where defined.

Also calculate where inputs permit:

- initial cash required;
- gross yield;
- net yield;
- leveraged IRR;
- break-even rent;
- break-even acquisition price;
- StrategyMaximumPrice;
- rate / vacancy / growth sensitivity.

## Scenario model

Prefer at least:

- Conservative
- Base
- Optimistic

Where purchase assistance changes financing materially, compare eligible financing scenarios separately.

## Output

Return IncomeInvestmentResult plus:

- modelAcquisitionPrice;
- financingScenario;
- StrategyMaximumPrice where supported;
- purchase-assistance effects;
- assumptions;
- unknowns;
- sensitivities;
- evidence confidence;
- ReturnBasis;
- TaxTreatment;
- key failure conditions.

## Guardrails

Do not:

- infer borrowing capacity from unrelated personal information;
- apply owner-occupier benefits to an investment-from-settlement model;
- present PRE_TAX returns as after-tax outcomes;
- present modelled returns as guaranteed;
- call StrategyMaximumPrice a valuation or expected vendor acceptance price.
