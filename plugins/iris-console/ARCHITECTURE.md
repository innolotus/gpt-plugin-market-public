# Iris Console Architecture

## 1. Scope

Iris Console is a GPT-native property investment and development decision harness.

The current demo phase must remain usable without a custom Iris backend.

## 2. Layer model

```text
User
  ↓
Iris Entry / Compatibility Adapter
  ├─ area → area-scoped market analysis
  ├─ property / natural language → orchestrator
  └─ profile → progressive client profiling
  ↓
Client Context Layer
  ├─ ClientProfile
  ├─ FinancialSnapshot
  └─ AcquisitionContext
  ↓
Property Development Orchestrator
  ↓
Property Identity Resolution Layer
  ├─ SINGLE_PROPERTY
  ├─ PROPERTY_COMPLEX
  └─ UNRESOLVED
  ↓
Evidence Layer
  ├─ Property Research
  ├─ Market Analysis
  ├─ Planning & Development
  ├─ Due Diligence
  ├─ Policy Impact
  └─ Monitoring
  ↓
Acquisition Price Layer [MARKET]
  ├─ MarketValueRange
  ├─ ExpectedAcquisitionRange
  └─ campaign signals
  ↓
Route by AcquisitionContext
  ├─ Owner-Occupier Acquisition Branch
  │    ├─ Purchase Assistance when relevant
  │    ├─ FundingSupportedPriceCeiling
  │    ├─ repayment scenarios
  │    └─ ownership cost
  │
  └─ Investment / Development Branch
       ↓
Versioned Assumption Layer
  ├─ immutable base AssumptionSet
  ├─ explicit overrides
  └─ EffectiveAssumptionSet
  ↓
Buyer / Financing Policy Layer
  ├─ Static Purchase Assistance Registry
  └─ Purchase Assistance Assessment when relevant
  ↓
Strategy Layer
  ├─ Property Strategy Assessment
  ├─ Income Investment
  ├─ Replacement Development
  └─ Subdivision Development
  ↓
Deterministic Calculation Tools
  ↓
Acquisition Price Layer [FINAL]
  ├─ StrategyMaximumPrice
  └─ market-vs-strategy gap analysis
  ↓
Strategy Comparison
  ↓
CanonicalDemoReport + AnalysisContext snapshot
  ↓
HTML Presentation Adapter
  ├─ fixed canonical-to-Markdown projection
  └─ answer-me-with-html renderer
  ↓
Responsive HTML reading view + canonical audit artifact
```

## 3. Client context layer

The current Console does not require persistent profile storage.

Instead it carries:

- ClientProfile;
- FinancialSnapshot;
- AcquisitionContext.

Use progressive profiling: ask only for fields that materially affect the current workflow.

## 4. Property identity resolution layer

An input address may resolve to:

- SINGLE_PROPERTY;
- PROPERTY_COMPLEX;
- UNRESOLVED.

A PropertyComplex is a valid resolved entity, not an error state.

If the user knows a specific unit, route to the normal property workflow.

If the user wants any unit or knows that one unit may sell but cannot identify which unit, retain an AcquisitionTarget scoped to the complex and continue with complex-level market analysis.

Do not run property-specific valuation, acquisition-price or strategy models until a specific PropertyRef is resolved.

Do not infer whole-complex ownership/saleability from a common address.

## 5. Evidence layer

Evidence-support Skills collect/normalize facts and observations.

Every material assertion should preserve:

- classification;
- EvidenceState;
- confidence;
- provenance;
- timestamps.

EvidenceState values:

- CONFIRMED;
- CONFLICTED;
- STALE;
- UNVERIFIED;
- UNKNOWN.

Do not reduce all evidence problems to a confidence score.

Source selection follows the static trusted-source registry under `Console/Sources/`.

## 6. Acquisition price layer

The pricing layer intentionally separates market evidence from strategy economics.

### MARKET pass

Consumes PropertyProfile + MarketAssessment + campaign evidence.

Produces:

- asking/guide evidence;
- MarketValueRange;
- ExpectedAcquisitionRange;
- campaign signals.

### FINAL pass

Runs after strategy models.

Consumes break-even/target-return price thresholds and produces:

- StrategyMaximumPrice by strategy;
- gap against ExpectedAcquisitionRange;
- decision support on whether current market expectation is economically compatible with each strategy.

This two-pass design avoids a circular dependency.

## 7. Owner-occupier acquisition branch

Owner occupation is not an investment strategy archetype.

When AcquisitionContext is OWNER_OCCUPIER and the analysis objective is purchase/carrying feasibility, the Console routes to `owner-occupier-acquisition`.

The branch consumes:

- FinancialSnapshot;
- MARKET AcquisitionPriceAssessment;
- PurchaseAssistanceAssessment where relevant;
- acquisition/loan assumptions;
- property due-diligence evidence where required.

Primary outputs include:

- upfront cash required;
- lender / government / buyer funding structure;
- FundingSupportedPriceCeiling;
- expected-acquisition vs funding gap;
- repayment scenarios;
- ownership carrying cost;
- blocking lender/policy/property unknowns.

It must not generate investment return metrics by default.

Investment/development Skills are a separate optional branch when the user explicitly asks for them.

## 8. Versioned assumption layer

The current Console stores maintainer-managed modelling assumptions under `Console/Assumptions/`.

Base AssumptionSets are versioned and immutable once used.

A strategy run creates an EffectiveAssumptionSet by applying explicit overrides without modifying the base set.

Override precedence is:

```text
USER_ASSUMPTION
→ CLIENT_ORG_ASSUMPTION
→ SOURCE_DERIVED_ASSUMPTION
→ DEFAULT_ASSUMPTION
```

This chooses a model input. It does not convert assumptions into facts.

High-risk/project-specific inputs may intentionally be marked as required with no default.

When multiple strategies run, AnalysisContext must retain each AssumptionSet reference and applied overrides.

## 9. Purchase-assistance layer

Purchase assistance is evaluated only when relevant to AcquisitionContext.

The assessment consumes:

- current static Purchase Assistance Registry;
- client eligibility facts;
- property context;
- current authoritative policy evidence.

Owner-occupier benefits must not be applied to an investment-from-settlement purchase.

## 10. Purchase-assistance registry

The current Console maintains program discovery metadata under `Console/Policies/`.

The registry defines:

- known active programs;
- program type;
- discovery mode;
- sensitivity rules;
- current snapshot metadata;
- authoritative source IDs;
- rules that must be re-verified.

The registry does not replace authoritative policy sources.

Program rules marked `VERIFY_AT_EXECUTION` must be checked against the trusted source registry / authoritative source before live use.

Sensitive programs may require explicit disclosure/request rather than proactive questioning.

AnalysisContext should retain `policyRegistryVersion` for reproducibility.

## 11. Strategy Skills

Strategy Skills model a defined asset-use path.

They consume:

- explicit acquisition-price scenario(s);
- evidence;
- assumptions;
- financing where relevant.

Each strategy result should retain `modelAcquisitionPrice`.

Where a transparent target exists, strategy models may derive StrategyMaximumPrice.

## 12. Deterministic calculations

Arithmetic and financial modelling should use deterministic tools where available.

Examples:

- acquisition costs;
- loan/amortisation;
- rental cash flow;
- IRR;
- development cost;
- GRV;
- margin;
- residual land value;
- reverse-calculated acquisition thresholds.

A custom .NET calculation backend is out of scope for the current demo phase.

## 13. Timed development-finance layer

Replacement and subdivision models use DevelopmentCashFlow timelines rather than a single aggregate finance/holding input.

The timeline separates:

- project cash in/out;
- debt draw/repayment;
- interest;
- equity contribution;
- sale proceeds.

Development return metrics distinguish:

- unleveredProjectIrr;
- leveredEquityIrr.

When financing structure is insufficient, leveredEquityIrr remains UNKNOWN.

Timed cash flow is also the basis for:

- total finance interest;
- peak debt;
- peak equity at risk;
- total equity contributed;
- duration.

The current Console may calculate these using deterministic tools; no custom backend is required.

## 14. Return-basis layer

Each strategy result must declare ReturnBasis and TaxTreatment.

Default:

```text
ReturnBasis = PRE_TAX
TaxModelStatus = NOT_MODELLED
```

Only a defined tax model may produce AFTER_TAX_ESTIMATE.

Strategy Comparison must verify tax-basis compatibility before ranking return metrics.

The current Console records tax modelling scope; it does not attempt to provide comprehensive tax advice.

## 15. Report reproducibility

Every material demo run should produce a CanonicalDemoReport.

Because the current Console has no persistence backend, AnalysisContext IDs/versions alone are not sufficient for historical replay if the underlying values lived only in conversation state.

The report therefore includes a compact ReproducibilityBundle with:

- AnalysisContext identifiers/versions;
- embedded ClientProfile snapshot;
- embedded FinancialSnapshot where used;
- embedded AcquisitionContext;
- EffectiveAssumptionSet snapshots;
- material PolicySnapshots;
- normalized material Property/Listing observations;
- source-registry version;
- policy-registry version;
- Skill/model versions;
- generated timestamp.

Do not embed unrestricted raw third-party material.

Prefer normalized observations, permitted references and hashes.

Later changes to live context must not rewrite old report meaning.

Regression execution and live demo validation use the same structured report envelope, but different evidence modes:

- REGRESSION_FROZEN;
- LIVE_DEMO_VALIDATION.

The user-facing HTML report is a derived view over this envelope. A single shared presentation adapter projects canonical fields into the `answer-me-with-html` Markdown format and renders a responsive, offline HTML file.

The adapter is read-only over the canonical report. It cannot research new facts, calculate new values, resolve conflicts or replace unknowns. Its failure does not change the analytical report status; the Console falls back to the canonical artifact plus a concise Markdown view.

The HTML view minimizes private client data and unrestricted third-party content. The canonical artifact retains the permitted reproducibility bundle.

## 16. Property and listing identity

A Property is the real-world asset.

A ListingObservation is what a source reported at a point in time.

One Property can have multiple source observations.

Do not use a listing ID as permanent property identity.

## 17. Future productization

When Iris productization is approved, the same semantic contracts may move into persistent services for profiles, source resolution, calculators, monitoring and report storage.

Do not implement those services in the current Console-demo phase.

## 18. Non-goals

Iris Console is not:

- a property scraping product;
- a backend platform in the current phase;
- a certified valuation product;
- a single opaque property score;
- a database replica of REA or Domain;
- a substitute for formal valuation, legal, tax, planning, lending or financial advice.
