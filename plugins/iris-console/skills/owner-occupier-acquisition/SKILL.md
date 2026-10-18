---
name: owner-occupier-acquisition
description: Model owner-occupier upfront cash, purchase assistance, funding boundaries, repayments and ownership costs.
metadata:
  product: Iris Console
  version: 0.1.0
  portable: true
---

# Owner-Occupier Acquisition

## Purpose

Model an owner-occupier acquisition without pretending owner occupation is an investment strategy.

The Skill answers:

> Under the available client, property, policy and financing inputs, what does acquiring and carrying this home look like?

## When to use

Use when:

```text
AcquisitionContext.intendedOccupancy = OWNER_OCCUPIER
```

and the user's objective is acquisition / purchase feasibility / ownership cost.

Do not run investment/development strategies by default.

## Inputs

Use where available:

- ClientProfile;
- FinancialSnapshot;
- AcquisitionContext;
- PropertyProfile;
- MARKET-phase AcquisitionPriceAssessment;
- PurchaseAssistanceAssessment;
- DueDiligenceResult where relevant;
- owner-occupier AssumptionSet / EffectiveAssumptionSet;
- lender/pre-approval inputs supplied by the user/lender.

## Acquisition-price scenarios

Do not treat ExpectedAcquisitionRange as a guaranteed purchase price.

Model explicit scenarios such as:

- expected-range low;
- expected-range midpoint/base;
- expected-range high;
- user target price.

Each scenario must retain:

```text
modelAcquisitionPrice
```

## Upfront cash calculation

Distinguish:

```text
purchase price
buyer deposit
lender loan
government guarantee
government shared equity
cash grant
stamp duty / relief
legal / registration / inspection costs
LMI where applicable
```

A government guarantee is not cash.

Suggested structure:

```text
Purchase Funding
= Buyer Cash Contribution
+ Lender Loan
+ Government Equity Contribution (if any)

Upfront Cash Required
= Buyer Deposit / Cash Contribution
+ Stamp Duty after relief
+ Legal / registration / inspection / other settlement costs
+ LMI paid upfront where applicable
- Confirmed Cash Grant usable for settlement
```

Do not double-count a grant or shared-equity contribution.

## FundingSupportedPriceCeiling

Where sufficient inputs exist, calculate a funding-supported ceiling from:

- available cash usable for settlement;
- known lender pre-approval / borrowing-capacity amount;
- government shared equity where eligible;
- eligible grant usable for settlement;
- acquisition-cost model;
- scheme/property price caps.

Do not infer borrowing capacity from salary/income.

Do not treat lender pre-approval as guaranteed final approval.

Return a provenance/status value:

- CONFIRMED_INPUTS
- USER_DECLARED_INPUTS
- PARTIAL_INPUTS
- UNKNOWN

## Funding gap

Compare:

```text
ExpectedAcquisitionRange
vs
FundingSupportedPriceCeiling
```

Return:

- WITHIN_KNOWN_FUNDING
- PARTIALLY_OVERLAPPING
- ABOVE_KNOWN_FUNDING
- FUNDING_CEILING_UNKNOWN

Do not call FundingSupportedPriceCeiling a valuation or vendor-acceptance estimate.

## Repayment model

Where lender terms are known or explicitly assumed, calculate:

- principal + interest repayment;
- payment frequency;
- loan term;
- interest rate;
- loan balance projection where useful.

Use deterministic calculation tools.

If interest rate is missing, do not silently invent one.

Use an explicit scenario assumption only when useful and disclose it.

## Ownership carrying cost

Where inputs permit, estimate:

- mortgage repayment;
- council rates;
- water;
- insurance;
- strata/body corporate;
- maintenance allowance where explicitly assumed;
- land tax only if applicable;
- other property-specific ownership cost.

Keep mortgage principal repayment distinguishable from economic expense where presenting detailed breakdowns.

## Stress scenarios

Where useful, include transparent repayment stress scenarios, for example:

- base rate;
- base +1%;
- base +2%.

This is not a lender serviceability assessment.

Do not infer formal serviceability or approval from the stress model.

## Purchase assistance

Consume PurchaseAssistanceAssessment where relevant.

Owner-occupier programs remain subject to:

- current policy eligibility;
- property eligibility;
- scheme caps;
- lender participation;
- final lender approval;
- ongoing occupancy obligations.

## Output

Return OwnerOccupierAcquisitionResult including:

- modelAcquisitionPrice;
- expectedAcquisitionRange;
- financingScenario;
- buyerCashContribution;
- lenderLoanAmount;
- governmentGuaranteeAmount;
- governmentEquityAmount;
- grantAmount;
- stampDutyTreatment;
- acquisitionCosts;
- initialCashRequired;
- effectiveLvr;
- fundingSupportedPriceCeiling;
- fundingCeilingStatus;
- fundingGapStatus;
- repaymentScenarios[];
- ownershipCostSummary;
- cashBufferAfterSettlement where known;
- assistanceSummary;
- blockingUnknowns[];
- verificationRequired[];
- warnings[];
- confidence.

## Guardrails

Do not:

- infer borrowing capacity from income;
- guarantee lender approval;
- call a government guarantee cash;
- apply owner-occupier assistance to an ineligible investment/development context;
- produce investment-return metrics by default;
- treat FundingSupportedPriceCeiling as market value;
- claim the client can "afford" the property in a regulated credit-advice sense.
