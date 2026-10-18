---
name: property-market-analysis
description: Assess property comparables, rent, supply, demand and trend evidence while preserving relevance, freshness and conflicts.
metadata:
  product: Iris Console
  version: 0.3.0
  portable: true
---

# Property Market Analysis

## Purpose

Assess how a property or development opportunity sits within its relevant market using comparable, rental, supply, demand and trend evidence.

This Skill supplies market evidence to `acquisition-price-assessment`.

It does **not** silently choose the final acquisition price.

## Inputs

- PropertyProfile, ComplexProfile or area reference;
- AcquisitionTarget where available;
- property/unit type where known;
- analysis horizon;
- optional investor/developer strategy;
- available comparable and market evidence.

## Procedure

1. Define the relevant market boundary.
2. Gather permitted comparable sales/listings and market observations.
3. Separate asking prices from transacted evidence.
4. Compare like-for-like attributes where possible.
5. Analyse market trend and liquidity indicators.
6. Identify supply/demand or rental-market signals.
7. Detect contradictory, stale or unverified evidence.
8. Produce a MarketAssessment.

## Relevant evidence may include

- recent comparable sales;
- current comparable listings;
- median prices;
- median rents;
- gross yields;
- days on market;
- vacancy;
- sales volume;
- listing volume;
- auction indicators;
- property-type-specific trends.

## Complex-level market analysis

When the resolved entity is a PropertyComplex and the target is:

- ANY_UNIT_IN_COMPLEX; or
- UNKNOWN_UNIT_IN_COMPLEX;

do not force a single-property MarketAssessment.

Instead produce a ComplexAcquisitionProfile / complex-level market view using:

- observed unit sales;
- observed unit rents;
- unit configurations;
- unit archetypes;
- known size/bedroom/parking distributions;
- current or historical listings within the complex;
- nearby comparable complexes where useful.

A complex-level analysis may produce ranges **by unit archetype**.

It must not produce one property-specific MarketValueRange or ExpectedAcquisitionRange until a specific property/unit is identified.

If candidate unit facts narrow materially, progressively refine candidatePropertyIds / unitArchetypes.

## Comparable discipline

A comparable should explain why it is comparable.

Relevant dimensions may include:

- micro-location;
- land area;
- property type;
- bedrooms;
- condition;
- development potential;
- sale timing;
- frontage / site utility.

Suburb median values are context, not direct property valuations.

## EvidenceState rules

For material market evidence use the EvidenceState semantics.

Examples:

- recent settled sale with reliable source → CONFIRMED;
- conflicting sold price/status → CONFLICTED;
- old listing used only for historical context → STALE for current-market use;
- agent-stated rent not independently checked → UNVERIFIED where verification matters;
- missing comparable evidence → UNKNOWN.

Do not resolve source conflict merely by averaging values.

## Output

Return MarketAssessment for a resolved specific property, or ComplexAcquisitionProfile / complex-level market assessment for an open complex target.

For a specific property, return MarketAssessment including:

- marketBoundary;
- subjectPosition;
- comparableSales[];
- comparableListings[];
- marketObservations[];
- rentalEvidence[];
- liquiditySignals[];
- supplyDemandSignals[];
- materialConflicts[];
- unknowns[];
- confidence.

Also return supporting EvidenceItems with classification and EvidenceState.

## Boundary with Acquisition Price Assessment

Property Market Analysis answers:

> What market evidence do we have and how comparable/relevant is it?

Acquisition Price Assessment answers:

> What market/value/acquisition range does that evidence support, and how does it compare with strategy economics?

Do not duplicate the second responsibility here.

## Guardrails

Never:

- present an asking price as a comparable sale;
- imply precision unsupported by evidence;
- hide weak comparable quality;
- convert an automated estimate into a certified valuation;
- manufacture a final acquisition price merely because downstream Skills need a number.
