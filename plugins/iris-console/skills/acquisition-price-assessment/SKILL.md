---
name: acquisition-price-assessment
description: Assess evidence-backed market value, expected acquisition range and strategy-supported maximum price for a property purchase.
metadata:
  product: Iris Console
  version: 0.2.0
  portable: true
---

# Acquisition Price Assessment

## Purpose

Separate three questions that must not be collapsed:

1. What market range is supported by the evidence?
2. What price range is this property likely to transact at under the current campaign?
3. What maximum price can each strategy economically support?

The Skill runs in two phases to avoid circular reasoning.

## Inputs

For MARKET phase:

- PropertyProfile;
- ListingObservation[];
- MarketAssessment;
- current listing/campaign evidence;
- approved comparable evidence;
- material EvidenceStates.

For FINAL phase:

- existing MARKET-phase AcquisitionPriceAssessment;
- eligible strategy results;
- client target-return constraints where supplied;
- versioned assumptions.

## Phase 1 — MARKET

Run after property-market-analysis and before strategy financial modelling.

### Determine Asking Price / Guide

Record the current listing guide as evidence.

Do not treat it as value.

If sources disagree, preserve EvidenceState = CONFLICTED.

### Determine MarketValueRange

Use appropriate evidence such as:

- recent comparable sales;
- condition;
- land/site utility;
- property type;
- location/micro-location;
- sale timing;
- automated estimates as supporting evidence only.

This is a market evidence range, not a certified valuation.

### Determine ExpectedAcquisitionRange

Estimate the likely transaction range for the current campaign.

May consider:

- asking / guide;
- auction or private treaty;
- days on market;
- listing changes;
- under-offer/contract status;
- competing listings;
- comparable sales;
- market liquidity.

If evidence is too weak, return UNKNOWN or a deliberately broad range.

Do not create false precision.

### MARKET output

Return AcquisitionPriceAssessment with:

- assessmentPhase = MARKET;
- askingPrice;
- marketValueRange;
- expectedAcquisitionRange;
- campaignSignals;
- comparableEvidenceIds;
- unknowns;
- confidence.

Leave `strategyMaximumPrices` empty until strategy economics are run.

## Owner-occupier branch

A pure owner-occupier acquisition analysis does not need a StrategyMaximumPrice.

Use the MARKET pass to establish:

- MarketValueRange;
- ExpectedAcquisitionRange;
- campaign evidence.

Then let `owner-occupier-acquisition` compare ExpectedAcquisitionRange with its separate `FundingSupportedPriceCeiling`.

Do not misuse StrategyMaximumPrice as a buyer affordability/funding limit.

Run the FINAL phase only when investment/development strategy models are actually being compared.

## Phase 2 — FINAL

Run after eligible strategy models.

Each strategy should supply, where possible:

- break-even acquisition price; and/or
- maximum price meeting the relevant target metric.

Examples:

### Income Investment

Maximum acquisition price may be derived from a stated target such as:

- minimum leveraged IRR;
- maximum acceptable annual cash deficit;
- minimum cash-on-cash return;
- client-defined constraint.

### Replacement Development

Maximum acquisition price may be derived from:

- minimum project margin;
- minimum unlevered project IRR, or a separately identified levered equity IRR target when financing inputs permit;
- finished-value assumptions;
- build/holding assumptions.

### Subdivision Development

Maximum acquisition price may be derived from:

- target project margin;
- explicitly identified unlevered project IRR or levered equity IRR target;
- GRV;
- development cost;
- project duration.

Do not invent a target return if none exists.

If no client target exists, report break-even / model thresholds separately and mark StrategyMaximumPrice as UNKNOWN unless a documented default assumption set defines the target.

## Gap analysis

For each eligible strategy compare:

```text
ExpectedAcquisitionRange
vs
StrategyMaximumPrice
```

Possible states:

- WITHIN_STRATEGY_LIMIT
- PARTIALLY_OVERLAPPING
- MARKET_ABOVE_STRATEGY_LIMIT
- STRATEGY_LIMIT_UNKNOWN

Example:

```text
Expected acquisition: $1.15m–$1.18m
Subdivision maximum:  $1.07m

Gap:
MARKET_ABOVE_STRATEGY_LIMIT
```

This means the current market expectation is above what the model supports under stated assumptions.

It does not mean the property is universally "overvalued".

## Evidence-state rules

- Do not silently resolve conflicting asking/listing statuses.
- Do not use stale campaign evidence as current without re-verification.
- Do not convert an agent guide into CONFIRMED market value.
- If a material input remains unresolved but scenario modelling is useful, promote the chosen scenario value to ASSUMPTION and label it.

## Output

Return:

- AcquisitionPriceAssessment;
- market evidence summary;
- strategy maximum prices where available;
- gap analysis;
- material conflicts;
- unknowns;
- assumptions;
- confidence.

## Guardrails

Never:

- call an automated estimate a formal valuation;
- equate asking price with fair value;
- equate expected transaction price with strategy maximum price;
- claim a strategy maximum price is what the vendor will accept;
- fabricate comparables or campaign history;
- hide a large gap between market expectation and strategy economics.
