---
name: property-monitoring
description: Detect material changes in a property, listing, market, planning environment or policy context against prior observations.
metadata:
  product: Iris Console
  version: 0.1.0
  portable: true
---

# Property Monitoring

## Purpose

Detect material changes in a property, listing, market, planning environment or policy context without regenerating an entire analysis from scratch.

## Inputs

- entity to monitor;
- previous observations;
- current permitted evidence;
- materiality rules.

## Change types

Examples:

- PRICE_CHANGED
- LISTING_CREATED
- LISTING_REMOVED
- RELISTED
- STATUS_CHANGED
- AGENT_CHANGED
- AUCTION_CHANGED
- PROPERTY_DETAILS_CHANGED
- PLANNING_CHANGED
- DEVELOPMENT_APPLICATION_CHANGED
- MARKET_CHANGED
- POLICY_CHANGED
- INFRASTRUCTURE_CHANGED

## Procedure

1. Load the prior baseline.
2. Acquire current permitted evidence.
3. Compare normalized observations.
4. Ignore cosmetic/non-material changes where configured.
5. Create ChangeEvents for material differences.
6. Assess likely impact.
7. Identify whether downstream re-analysis is required.

## Output

Return:

- ChangeEvent[];
- unchanged material facts where useful;
- impact notes;
- re-analysis recommendations;
- unknowns;
- confidence.

## Guardrails

Do not treat missing current data as proof that a prior fact is no longer true.

Do not overwrite history.

Monitoring should be incremental and provenance-aware.
