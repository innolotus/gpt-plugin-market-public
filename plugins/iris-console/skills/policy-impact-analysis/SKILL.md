---
name: policy-impact-analysis
description: Analyse how policy, regulation, rates, migration, tax or infrastructure changes affect a property or investment thesis.
metadata:
  product: Iris Console
  version: 0.1.0
  portable: true
---

# Policy Impact Analysis

## Purpose

Analyse how a policy, regulatory, interest-rate, migration, tax or infrastructure change may affect property markets, development feasibility or a specific property thesis.

## Core model

```text
Baseline
   ↓
What changed
   ↓
Who / what is affected
   ↓
Transmission mechanism
   ↓
Short-term effects
   ↓
Medium-term effects
   ↓
Property / project relevance
```

## Inputs

- policy or announcement;
- previous state;
- new state;
- jurisdiction;
- effective date;
- optional property / market scope.

## Procedure

1. Establish the previous baseline.
2. Identify the exact change.
3. Separate announcement date from effective date.
4. Identify directly affected groups.
5. Model plausible transmission mechanisms.
6. Link the change to market or development variables.
7. Record competing mechanisms and uncertainty.
8. Return a PolicyImpactAssessment.

## Output

Include:

- before;
- after;
- affected entities;
- direct impacts;
- indirect impacts;
- time horizon;
- affected geographies/property types;
- supporting evidence;
- contradicting evidence;
- confidence;
- monitoring triggers.

## Guardrails

Do not convert correlation into causation.

Do not assume a policy is in force merely because it was announced.

Distinguish FACT about the policy from INFERENCE about market impact.
