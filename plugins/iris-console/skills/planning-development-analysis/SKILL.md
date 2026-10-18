---
name: planning-development-analysis
description: Analyse property planning controls, development opportunities, constraints and required verification without overstating approval potential.
metadata:
  product: Iris Console
  version: 0.1.0
  portable: true
---

# Planning & Development Analysis

## Purpose

Identify planning constraints, development opportunities and verification requirements for a property or site.

## Inputs

- PropertyProfile / PropertyRef;
- jurisdiction;
- planning evidence;
- optional target development concept.

## Procedure

1. Confirm site identity and jurisdiction.
2. Retrieve authoritative planning evidence where available.
3. Identify zone, overlays and relevant controls.
4. Identify physical/site constraints.
5. Identify plausible development scenarios.
6. Separate explicit planning rules from interpretation.
7. Record approvals, referrals and professional verification likely required.
8. Return a PlanningAssessment.

## Analyse where relevant

- zoning;
- overlays;
- minimum site area;
- frontage;
- building height;
- setbacks;
- site coverage;
- heritage;
- significant / regulated trees;
- flood;
- bushfire;
- contamination;
- access;
- subdivision;
- density;
- land use;
- nearby development applications;
- infrastructure constraints.

## Scenario output

Each scenario should include:

- scenario name;
- enabling evidence;
- blocking evidence;
- assumptions;
- planning uncertainty;
- next verification step.

Example decision language:

- PLAUSIBLE;
- PLAUSIBLE_WITH_CONSTRAINTS;
- HIGH_UNCERTAINTY;
- NOT_SUPPORTED_BY_CURRENT_EVIDENCE.

## Guardrails

Do not represent planning analysis as formal planning approval.

If required documents, title constraints, overlays or site measurements are unavailable, return UNKNOWN rather than "no constraint".
