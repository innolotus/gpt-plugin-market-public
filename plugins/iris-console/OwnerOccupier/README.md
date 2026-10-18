# Iris Console Owner-Occupier Acquisition

Owner-occupier purchase analysis is an **acquisition / financing path**, not a fourth property-investment strategy.

The core question is:

> Can this client acquire and carry this property for owner occupation under the stated financing, assistance and cost assumptions?

It does not attempt to calculate investment returns from living in the property.

## Boundary with strategy analysis

For a normal owner-occupier acquisition request:

```text
Client Context
↓
Property Research
↓
Market Analysis
↓
Acquisition Price Assessment [MARKET]
↓
Purchase Assistance Assessment
↓
Due Diligence as required
↓
Owner-Occupier Acquisition
↓
Acquisition / funding decision support
```

Do not run Income / Replacement / Subdivision merely because those Skills exist.

Run investment/development strategy analysis only when:

- the user explicitly asks for it; or
- development/income optionality is materially part of the user's objective.

Owner occupation and future development optionality can coexist, but they are separate analytical questions.

## FundingSupportedPriceCeiling

This is the maximum purchase price supported by the **known financing inputs** in the current scenario.

It may use:

- available cash/deposit;
- lender pre-approval / borrowing-capacity figure supplied by the user or lender;
- government shared equity where eligible;
- cash grant where settlement timing permits;
- acquisition costs and stamp duty;
- financing constraints.

It must not:

- infer borrowing capacity from income;
- assume a lender will approve the modelled amount;
- count a government guarantee as cash;
- ignore transaction costs.

Possible status:

- CONFIRMED_INPUTS
- USER_DECLARED_INPUTS
- PARTIAL_INPUTS
- UNKNOWN

The result is a funding boundary, not market value.

## Price-gap interpretation

Compare:

```text
ExpectedAcquisitionRange
vs
FundingSupportedPriceCeiling
```

Possible states:

- WITHIN_KNOWN_FUNDING
- PARTIALLY_OVERLAPPING
- ABOVE_KNOWN_FUNDING
- FUNDING_CEILING_UNKNOWN

Example:

```text
Expected acquisition: $850k–$880k
Known funding ceiling: $835k

Result:
ABOVE_KNOWN_FUNDING
```

This means the currently modelled funding inputs do not support the expected acquisition range.

It does **not** mean:

- the client can never buy the property;
- a lender will definitely refuse;
- the market value is $835k.

## Monthly carrying cost

Where inputs permit, estimate:

- principal + interest repayment;
- council rates;
- water;
- building/contents insurance where relevant;
- strata/body corporate where relevant;
- land tax only where applicable;
- maintenance allowance where explicitly modelled;
- other material ownership costs.

Do not mix lifestyle utilities/food/transport into property carrying cost unless the user explicitly wants a household-budget analysis.

## Repayment scenarios

Prefer explicit scenarios such as:

- current lender/pre-approval rate;
- +1% rate stress;
- +2% rate stress;

where useful.

Do not call this a formal lender serviceability test.

A lender may use buffers, expense benchmarks and policy rules not represented here.

## Purchase assistance

PurchaseAssistanceAssessment runs upstream.

The owner-occupier model may consume:

- deposit requirements;
- government guarantee treatment;
- shared equity;
- grant;
- stamp-duty treatment;
- LMI treatment.

A government guarantee is not a cash contribution.

## Output discipline

The result should focus on:

- expected acquisition range;
- upfront cash requirement;
- funding structure;
- funding-supported ceiling where known;
- monthly repayment;
- monthly/annual ownership cost;
- remaining cash buffer where known;
- assistance effects;
- lender/policy unknowns;
- property due-diligence unknowns.

Do not produce investment IRR, cash-on-cash return or rental yield unless the user separately requests an investment analysis.

## Advice boundary

This is acquisition scenario modelling.

It is not:

- lender approval;
- regulated credit advice;
- financial advice;
- legal advice;
- tax advice;
- a certified property valuation.
