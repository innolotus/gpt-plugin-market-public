---
name: client-profile-onboarding
description: Gather and reuse the minimum client profile, financial snapshot and acquisition context needed for property analysis.
metadata:
  product: Iris Console
  version: 0.1.0
  portable: true
---

# Client Profile Onboarding

## Purpose

Build the minimum useful client context for property analysis without turning Iris Console into a KYC questionnaire.

The Skill uses progressive profiling:

> ask only for information that materially changes the current analysis.

It manages three semantic objects:

- ClientProfile
- FinancialSnapshot
- AcquisitionContext

No backend persistence is required in the current Console-demo phase.

## When to use

Use at the beginning of a new client/session analysis when required profile/context facts are missing.

Reuse existing context when already available.

Do not restart onboarding for every property.

## Minimum-first behaviour

Start with the smallest useful set of questions.

Usually determine:

1. client/investor type or primary objective;
2. intended use of the current property;
3. whether client-specific funding constraints should be modelled.

Examples of useful high-level answers:

- owner occupier;
- individual buy-and-hold investor;
- professional investor / small developer.

Examples of current-property intent:

- live in it;
- rent from settlement;
- redevelop / subdivide;
- not decided yet.

## FinancialSnapshot behaviour

Only ask for financial data when the requested analysis needs client-specific funding.

Useful fields may include:

- available cash/deposit;
- lender pre-approval;
- borrowing capacity supplied by the user/lender;
- preferred LVR;
- relevant existing debt.

Do not infer borrowing capacity from unrelated user information.

If the user provides a bank/lender figure, preserve its source and expiry if known.

## Government-assistance eligibility

Do not ask every user for all first-home assistance fields.

Only expand PurchaseEligibilityFacts when:

- intended occupancy may be owner-occupier; and
- current property/purchase price could make an assistance pathway relevant; and
- the missing fact materially affects the result.

Examples:

- first-home-buyer status;
- prior property ownership;
- citizenship/residency;
- applicant count;
- income threshold facts.

Do not request sensitive eligibility details for a professional subdivision scenario where owner-occupier assistance is clearly irrelevant.

## AcquisitionContext rule

Property-specific intent belongs in AcquisitionContext.

Do not overwrite the stable ClientProfile merely because the user chooses a different strategy for another property.

Example:

```text
ClientProfile:
  investorType = INDIVIDUAL_INVESTOR

Property A AcquisitionContext:
  intendedOccupancy = OWNER_OCCUPIER

Property B AcquisitionContext:
  intendedOccupancy = INVESTMENT_FROM_SETTLEMENT
```

Both can be valid for the same client.

## Reuse and freshness

Reuse known profile facts unless:

- the value is missing;
- the user says it changed;
- it has expired;
- the new property requires a different AcquisitionContext.

Do not repeatedly ask:

> How much cash do you have?

if a current FinancialSnapshot already contains a usable value.

Instead, when material, confirm whether the existing snapshot should still be used.

## Completeness states

Use these semantic states:

### MINIMUM

Enough to start property/strategy analysis.

### FINANCING_READY

Enough to model client-specific acquisition funding.

### ASSISTANCE_READY

Enough to evaluate relevant purchase-assistance programs.

### DEVELOPMENT_READY

Enough to evaluate developer capital/return constraints where client-specific inputs are needed.

Do not block research/market analysis just because the profile is not fully FINANCING_READY.

## Output

Return:

- ClientProfile snapshot;
- FinancialSnapshot where available;
- AcquisitionContext;
- profileCompleteness;
- missingMaterialFields[];
- staleOrExpiredFields[];
- assumptions[];
- warnings[].

## Privacy / minimisation rules

- Ask only what the current workflow materially needs.
- Do not ask sensitive questions speculatively.
- Do not infer citizenship, family status, income or ownership history.
- Do not repeat sensitive details unnecessarily in the user-facing report.
- Treat user-declared facts as user-declared unless independently verified.

## Guardrails

Do not:

- merge property-specific intent into the stable profile;
- create permanent policy-eligibility conclusions in the profile;
- treat lender approval as guaranteed future borrowing capacity;
- block a general property analysis because optional profile fields are missing;
- fabricate missing profile values to complete a model.
