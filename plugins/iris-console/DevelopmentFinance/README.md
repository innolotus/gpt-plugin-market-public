# Iris Console Development Finance Timeline

This directory defines the demo-phase semantics for timed development cash flow.

The purpose is to replace the coarse pattern:

```text
financeAndHolding = one aggregate number
```

with an explicit project timeline.

Iris Console does not need a custom finance backend in the current phase. The Skill may use deterministic calculation tools, but the inputs, timing assumptions and outputs must be explicit.

## Core principle

Development IRR is time-sensitive.

The model must know not only **how much** money moves, but approximately **when** it moves.

Recommended default granularity:

```text
MONTHLY
```

Use actual dates only when reliable project dates exist.

Do not fabricate an exact construction schedule merely to make the model look detailed.

## Timeline phases

A development scenario may include phases such as:

- SETTLEMENT
- PRE_APPROVAL_HOLD
- PLANNING_APPROVAL
- DEMOLITION
- SUBDIVISION_AND_CIVIL
- DESIGN_AND_APPROVAL
- CONSTRUCTION
- MARKETING
- SETTLEMENT_OF_SALES
- HOLD_AFTER_COMPLETION

Not every project needs every phase.

## DevelopmentCashFlow

Each cash-flow entry should identify:

```text
period
date
phase
category
description

cashIn
cashOut

debtDraw
debtRepayment
interest
equityContribution

sourceOrAssumption
notes
```

At least one of `period` or `date` must be present.

## Cash-flow categories

Recommended categories include:

- ACQUISITION
- STAMP_DUTY_AND_TRANSACTION
- DEMOLITION
- REMEDIATION
- CONSULTANTS
- PLANNING_AND_APPROVALS
- SUBDIVISION
- CIVIL_AND_SERVICES
- CONSTRUCTION
- CONTINGENCY
- RATES_AND_UTILITIES
- INSURANCE
- LAND_TAX
- RENTAL_INCOME
- OTHER_HOLDING_COST
- MARKETING_AND_SELLING
- SALE_PROCEEDS
- TAX_COMPONENT
- OTHER

Do not hide financing interest inside a generic project-cost bucket if the model is calculating interest from debt balances.

## Debt and equity

The timeline should separately track:

```text
equityContribution
debtDraw
interest
debtRepayment
```

so the model can calculate:

- outstanding debt by period;
- peak debt;
- cumulative equity contributed;
- peak equity at risk;
- total interest;
- timing of capital deployment.

Do not infer lender approval from a modelled debt draw.

A debt draw is a scenario assumption unless supported by an actual financing facility.

## Interest

Interest must be calculated from an explicit finance-rate assumption and an explicit debt-balance methodology.

The model should disclose:

- finance rate;
- whether interest is paid or capitalised;
- calculation period;
- debt balance used for interest calculation.

Do not both:

1. calculate interest from the debt timeline; and
2. include the same interest again inside an aggregate `financeAndHolding`.

That would double-count finance cost, a surprisingly popular way to manufacture terrible projects.

## Holding costs

Holding costs should be separate from financing interest.

Examples:

- council rates;
- water;
- insurance;
- land tax where modelled;
- utilities/security;
- temporary maintenance.

If the existing property is rented during approvals, rental income belongs in the same timeline and may offset holding cost.

## Construction timing

Where no detailed construction draw schedule exists:

- do not assume all build cost occurs at settlement;
- use an explicit staged/scenario allocation;
- mark the allocation as ASSUMPTION;
- sensitivity-test duration and timing when material.

A generic staged allocation may be used only when the active AssumptionSet or user/client scenario explicitly defines it.

## Sales / exit

Sale proceeds should appear when the model assumes settlement occurs, not when marketing begins.

For multi-dwelling development, sale proceeds may occur in different periods.

Debt repayment should be modelled against sale/settlement timing where the scenario requires it.

## IRR basis

Do not use an unqualified `project IRR` field. Development reports must name the
cash-flow basis explicitly:

- `unleveredProjectIrr` is calculated from project operating/development cash
  flows before debt draw, interest, debt repayment and equity funding flows;
- `leveredEquityIrr` is calculated from the investor equity cash-flow series
  after debt draw, interest and repayment effects.

If the financing structure is incomplete, keep `leveredEquityIrr` UNKNOWN.
Do not substitute one basis for the other or rank them as equivalent.

Do not calculate either IRR from:

```text
total profit / total cost
```

That is not IRR. Humanity has invented enough ratios already.

## Required outputs

Where inputs permit, calculate:

- project duration;
- total project cost excluding sale proceeds;
- total finance interest;
- peak debt;
- peak equity at risk;
- total equity contributed;
- project profit;
- project margin;
- unlevered project IRR;
- levered equity IRR where financing inputs permit;
- break-even acquisition price;
- StrategyMaximumPrice where target return exists.

## Evidence / assumption discipline

Timing is often an assumption.

Preserve whether each material timing/input is:

- FACT;
- ASSUMPTION;
- CALCULATION.

A planning approval date, construction duration or sales settlement period must not silently become FACT merely because it is placed on a timeline.
