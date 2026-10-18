---
name: property-development-orchestrator
description: Orchestrate Iris property research, acquisition, owner-occupier and investment-development analysis through the minimum applicable Skill path.
metadata:
  product: Iris Console
  version: 0.13.0
  portable: true
---

# Property Development Orchestrator

## Purpose

Route a property request through the minimum useful client-context, evidence, pricing, acquisition or strategy Skills.

The orchestrator has two distinct paths:

1. **Owner-occupier acquisition**
2. **Investment / development strategy analysis**

Owner occupation is not a fourth investment strategy.

## Common entry flow

```text
Reuse ClientProfile / FinancialSnapshot
        ↓
client-profile-onboarding only for missing material fields
        ↓
create provisional AcquisitionContext / AcquisitionTarget
        ↓
property-research
        ↓
resolve PropertyEntityType
        ↓
route entity scope
        ↓
load applicable AssumptionSet(s) only when a downstream model needs them
```

# Entity Scope Routing

## SINGLE_PROPERTY

For a resolved specific property:

```text
property-research
↓
property-market-analysis
↓
acquisition-price-assessment [MARKET]
↓
owner-occupier or investment/development branch
```

## PROPERTY_COMPLEX + SPECIFIC_PROPERTY

If the requested unit/property is resolved, run the normal single-property flow for that PropertyRef while retaining complex context.

## PROPERTY_COMPLEX + ANY_UNIT_IN_COMPLEX

Continue with:

```text
property-research
↓
ComplexProfile
↓
property-market-analysis [COMPLEX]
↓
ComplexAcquisitionProfile
↓
report
```

Do not run property-specific AcquisitionPriceAssessment or strategy models until a specific candidate property is selected.

## PROPERTY_COMPLEX + UNKNOWN_UNIT_IN_COMPLEX

Continue with complex-level market analysis.

Use new evidence from the user or sources to narrow:

- candidatePropertyIds[];
- unit archetypes;
- likely acquisition/rent ranges.

Do not stop merely because the unit number is not yet known.

Do not silently choose an arbitrary unit.

## PROPERTY_COMPLEX + COMPLEX_AS_WHOLE

Before whole-complex modelling, verify that the intended acquisition subject is actually the whole complex and obtain sufficient ownership/title evidence.

A shared street address does not imply common saleability.

## UNRESOLVED

Request the minimum identifier needed to resolve the entity.

Do not run market/acquisition/strategy modelling against an unresolved entity.

After a resolved specific-property MARKET pass, route by AcquisitionContext / analysis objective.

# Branch A — Owner-occupier acquisition

Use when:

```text
intendedOccupancy = OWNER_OCCUPIER
```

and the user is primarily asking about buying/carrying the property as a home.

```text
MARKET AcquisitionPriceAssessment
        ↓
purchase-assistance-assessment when relevant
        ↓
property-due-diligence as required
        ↓
owner-occupier-acquisition
        ↓
OwnerOccupierAcquisitionResult
        ↓
CanonicalDemoReport + AnalysisContext snapshot
        ↓
html-report-renderer
```

Do **not** run property-strategy-assessment or Strategy Comparison by default.

Do not produce Income / Replacement / Subdivision merely because those Skills exist.

If the user explicitly asks about future investment/development optionality, run that as a separate analytical branch.

## Owner-occupier acquisition rules

- use FinancialSnapshot rather than inferring borrowing capacity;
- use PurchaseAssistanceAssessment where relevant;
- compare ExpectedAcquisitionRange with FundingSupportedPriceCeiling;
- do not call the funding ceiling a valuation;
- do not claim lender approval;
- do not generate investment return metrics by default;
- do not require Acquisition Price Assessment [FINAL] unless strategy models are also run.

# Branch B — Investment / development

Use when:

- intendedOccupancy = INVESTMENT_FROM_SETTLEMENT; or
- intendedOccupancy = DEVELOPMENT_FOR_PROFIT; or
- the user explicitly requests strategy analysis.

```text
MARKET AcquisitionPriceAssessment
        ↓
purchase-assistance-assessment only when relevant
        ↓
other evidence-support Skills as needed
        ↓
property-strategy-assessment
        ↓
eligible strategy models
        ↓
acquisition-price-assessment [FINAL]
        ↓
strategy-comparison
        ↓
CanonicalDemoReport + AnalysisContext snapshot
        ↓
html-report-renderer
```

## Why Acquisition Price Assessment runs twice for strategy analysis

### MARKET pass

Before strategy modelling, establish:

- asking/guide evidence;
- MarketValueRange;
- ExpectedAcquisitionRange;
- campaign signals.

### FINAL pass

After strategy models:

- collect StrategyMaximumPrice values;
- compare them with ExpectedAcquisitionRange;
- produce gap analysis.

Do not derive strategy maximum prices before strategy economics exist.

## Client-context rules

Reuse existing ClientProfile / FinancialSnapshot before asking.

Ask only for facts that materially affect the current decision.

Property-specific occupancy/strategy intent belongs in AcquisitionContext.

## Assumption-set rules

For every model actually run:

1. select the active base AssumptionSet;
2. apply relevant user/client/source-derived overrides;
3. create an EffectiveAssumptionSet;
4. preserve base ID/version + overrides in AnalysisContext.

Do not ask users to configure generic defaults.

Only ask for a missing `requiredInput` when it materially blocks the requested analysis.

## EvidenceState rules

Do not silently collapse CONFLICTED, STALE, UNVERIFIED or UNKNOWN evidence into CONFIRMED values.

When a model needs a value despite unresolved evidence:

1. choose an explicit scenario value;
2. classify it as ASSUMPTION;
3. preserve the original EvidenceState;
4. run sensitivity where material.

## Purchase-assistance registry rules

When purchase assistance is relevant:

1. load the active static Purchase Assistance Registry;
2. preserve `policyRegistryVersion`;
3. discover candidate programs according to discoveryMode;
4. verify material current rules from authoritative sources;
5. run only relevant program evaluations;
6. preserve PolicySnapshot/evidence references.

Do not ask the user to select programs.

Do not proactively ask sensitive trigger questions for EXPLICIT_DISCLOSURE_OR_REQUEST programs.

## Development-finance rules

For Replacement and Subdivision:

1. build a timed DevelopmentCashFlow series;
2. separate holding cost from financing interest;
3. calculate unleveredProjectIrr from project cash flows;
4. calculate leveredEquityIrr only when financing assumptions are sufficient;
5. preserve peak debt, peak equity at risk and total finance interest;
6. do not fabricate lender-approved facilities or drawdowns.

## Return-basis rules

Before strategy comparison:

1. ensure every strategy result declares ReturnBasis;
2. preserve TaxTreatment;
3. default to PRE_TAX when no defined tax model exists;
4. prevent direct return ranking across incompatible tax bases.

The current Console is not a tax-advice engine.

## Example — owner-occupier first-home buyer

1. reuse/onboard client context;
2. AcquisitionContext = OWNER_OCCUPIER;
3. property-research;
4. property-market-analysis;
5. acquisition-price-assessment [MARKET];
6. purchase-assistance-assessment;
7. property-due-diligence as required;
8. owner-occupier-acquisition;
9. report funding gap / repayments / ownership costs / unknowns.

Do not run investment strategy models unless requested.

## Example — individual investor buying to rent

1. reuse/onboard minimum profile;
2. AcquisitionContext = INVESTMENT_FROM_SETTLEMENT;
3. property-research;
4. property-market-analysis;
5. acquisition-price-assessment [MARKET];
6. property-due-diligence as required;
7. property-strategy-assessment;
8. income-investment using explicit acquisition-price scenarios;
9. acquisition-price-assessment [FINAL];
10. strategy-comparison if another strategy is materially plausible.

## Example — professional investor evaluating a split site

1. reuse/onboard investor/developer profile;
2. AcquisitionContext = DEVELOPMENT_FOR_PROFIT;
3. property-research;
4. property-market-analysis;
5. acquisition-price-assessment [MARKET];
6. planning-development-analysis;
7. property-due-diligence;
8. property-strategy-assessment;
9. subdivision-development;
10. other strategies only when independently plausible;
11. acquisition-price-assessment [FINAL];
12. strategy-comparison.

## Canonical report rules

Every material demo analysis should produce a CanonicalDemoReport.

Because the current Console has no persistence backend, the report must preserve a compact ReproducibilityBundle.

Do not rely only on IDs that point to ephemeral conversation state.

Embed the minimum normalized snapshots used for the analysis:

- ClientProfile;
- FinancialSnapshot where used;
- AcquisitionContext;
- EffectiveAssumptionSet(s);
- material PolicySnapshot(s);
- material Property/Listing observations.

Also preserve:

- sourceRegistryVersion;
- policyRegistryVersion;
- Skill versions;
- model/calculation version;
- generatedAt.

Do not copy unrestricted raw third-party content into the report.

## HTML presentation handoff

After the canonical report is assembled and validated, invoke `html-report-renderer` for every material user-facing report unless the user explicitly requests plain text, Markdown or raw structured output.

The renderer consumes the completed canonical report as read-only input. It must not:

- research or calculate new values;
- alter `ReportStatus`;
- resolve conflicts;
- replace unknowns;
- change assumptions, ReturnBasis or TaxTreatment.

Deliver responsive HTML as the primary reading view and retain the canonical YAML/JSON as the audit/replay artifact.

If the HTML renderer is unavailable or fails, return the canonical report plus a concise Markdown view and a visible rendering error. Presentation failure alone does not change the analysis to `BLOCKED`.

## Complex-level output

For ANY_UNIT_IN_COMPLEX / UNKNOWN_UNIT_IN_COMPLEX return:

- PropertyComplex / ComplexProfile;
- AcquisitionTarget;
- known candidate PropertyRefs;
- complex-level MarketAssessment / ComplexAcquisitionProfile;
- unit archetypes and observed ranges where supported;
- material unknowns;
- verificationRequired;
- CanonicalDemoReport.

Do not include property-specific StrategyCandidates or AcquisitionPriceAssessment until a specific property is resolved.

## Output

Return only the objects relevant to the selected branch.

### Owner-occupier branch

- ClientProfile snapshot;
- FinancialSnapshot;
- AcquisitionContext;
- profileCompleteness;
- skills invoked;
- AssumptionSet references;
- policyRegistryVersion;
- MARKET AcquisitionPriceAssessment;
- PurchaseAssistanceAssessment where relevant;
- OwnerOccupierAcquisitionResult;
- material unknowns/conflicts;
- AnalysisContext;
- CanonicalDemoReport;
- HtmlReportArtifact;
- next verification steps.

### Investment/development branch

- ClientProfile snapshot;
- FinancialSnapshot where available;
- AcquisitionContext;
- profileCompleteness;
- skills invoked;
- AssumptionSet references;
- policyRegistryVersion;
- MARKET AcquisitionPriceAssessment;
- PurchaseAssistanceAssessment where relevant;
- AssetUtilityAssessment;
- StrategyCandidates;
- strategy results;
- FINAL AcquisitionPriceAssessment;
- StrategyComparison where applicable;
- ReturnBasis / TaxTreatment summary;
- material unknowns/conflicts;
- AnalysisContext;
- CanonicalDemoReport;
- HtmlReportArtifact;
- next verification steps.

## Guardrails

Do not bypass Source Policy.

Do not infer borrowing capacity.

Do not silently resolve a PropertyComplex to an arbitrary unit.

Do not treat a valid PropertyComplex as UNRESOLVED merely because the specific unit is not yet selected.

Do not call FundingSupportedPriceCeiling or StrategyMaximumPrice a certified valuation.

Do not call either of them the price a vendor will accept.

Do not create permanent policy eligibility conclusions in ClientProfile.

Do not convert attractive economics into claims of planning approval, lender approval or guaranteed performance.
