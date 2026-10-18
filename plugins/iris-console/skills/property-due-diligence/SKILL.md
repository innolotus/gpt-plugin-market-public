---
name: property-due-diligence
description: Produce a structured property due-diligence register covering material risks, evidence gaps and verification actions.
metadata:
  product: Iris Console
  version: 0.1.0
  portable: true
---

# Property Due Diligence

## Purpose

Produce a structured due-diligence register for acquisition, investment or development decisions.

## Inputs

- PropertyProfile;
- planning evidence;
- market evidence;
- available title / legal / technical documents;
- target strategy.

## Review areas

Where relevant:

- title and ownership evidence;
- easements and encumbrances;
- planning;
- heritage;
- flood;
- bushfire;
- contamination;
- trees;
- utilities;
- access;
- development applications;
- infrastructure;
- building condition evidence;
- tenancy / rental evidence;
- finance assumptions;
- tax assumptions;
- market and exit assumptions.

## Procedure

1. Build the checklist for the target strategy.
2. Mark each item as VERIFIED, FLAGGED, UNKNOWN or NOT_APPLICABLE.
3. Link every VERIFIED or FLAGGED item to evidence.
4. Distinguish absence of evidence from evidence of absence.
5. Prioritise follow-up tasks.
6. Return a DueDiligenceResult.

## Output groups

- Red flags;
- Yellow flags;
- Unknowns;
- Verification required;
- Documents required;
- Professional advice required;
- Cleared items with evidence.

## Critical rule

```text
UNKNOWN != NO ISSUE
```

## Guardrails

Do not claim legal, engineering, valuation, tax or planning certainty beyond the available evidence.

Do not mark an issue "clear" solely because a web search did not reveal it.
