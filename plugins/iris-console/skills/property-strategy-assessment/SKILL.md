---
name: property-strategy-assessment
description: Identify which income, replacement or subdivision strategies are sufficiently plausible and evidenced to model for a property.
metadata:
  product: Iris Console
  version: 0.2.0
  portable: true
---

# Property Strategy Assessment

## Purpose

Identify which asset-use strategies are worth modelling for a property and investor.

This Skill does not calculate final returns. It decides which strategy hypotheses deserve underwriting.

## Inputs

- ClientProfile
- AcquisitionContext
- FinancialSnapshot where materially relevant
- PropertyProfile
- available MarketAssessment
- available PlanningAssessment
- available DueDiligenceResult

## Required utility assessment

Assess:

### Building Utility

Consider:

- habitability;
- apparent condition;
- age;
- remaining economic life;
- major near-term CapEx;
- functional layout;
- renovation evidence;
- economic value destroyed by demolition.

### Rental Utility

Consider:

- current / estimated rent evidence;
- vacancy / management assumptions;
- operating cost;
- maintenance / CapEx burden;
- ability to produce holding income.

### Land Utility

Consider:

- land area;
- frontage;
- shape;
- access;
- easements;
- slope;
- services;
- location.

### Development Utility

Consider:

- planning capacity;
- subdivision potential;
- dwelling yield;
- development precedents;
- constraints and unknowns.

## Client fit

Use ClientProfile for relatively stable investor preferences/capability and AcquisitionContext for the intent of this specific property.

Do not infer a permanent investor intent from one property.

### Individual / non-professional investor

Default consideration:

- Income Investment.

Surface development optionality only where evidence makes it material.

### Professional investor / small developer

Consider:

- Replacement Development where Building Utility is low and the asset is effectively land-led.
- Subdivision Development where Land Utility and Development Utility are sufficiently strong.
- Temporary rent/hold as a project phase where appropriate.

## Strategy eligibility output

For each strategy:

- strategyType
- eligibility
- rationale
- requiredEvidence
- blockingUnknowns
- confidence

Do not include OWNER_OCCUPIER as a strategy type. Pure owner-occupier acquisition is handled by the separate acquisition branch.

Eligibility values:

- ELIGIBLE
- ELIGIBLE_WITH_CONSTRAINTS
- INSUFFICIENT_EVIDENCE
- NOT_ECONOMICALLY_SUPPORTED
- NOT_APPLICABLE

## Critical rule

Do not implement rules such as:

```text
age > 50 years → demolish
```

Age is one indicator of Building Utility, not a demolition instruction.

## Output

Return:

- AssetUtilityAssessment
- StrategyCandidate[]
- recommended modelling order
- blocking unknowns
- confidence
