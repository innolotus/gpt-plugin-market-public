# Iris Console Canonical Demo Report

The Canonical Demo Report is the stable output envelope for Iris Console demo/validation runs.

The current Console phase has **no custom backend**, so IDs and version numbers alone are not sufficient for historical reproducibility.

A report must therefore preserve:

1. human-readable conclusions;
2. AnalysisContext identifiers/versions;
3. the minimum normalized snapshot payload needed to understand/reproduce the analysis later.

## Report principle

A report is not just prose.

It is:

```text
Decision Summary
+
Structured Results
+
Evidence / Assumptions / Unknowns
+
Reproducibility Bundle
```

## Subject entity

A report may describe:

- SINGLE_PROPERTY;
- PROPERTY_COMPLEX.

For a complex-level run, preserve `subjectEntity`, `subjectComplex` and `complexAnalysis`.

Do not force a complex into a fake PropertyRef merely to fill `subjectProperty`.

## Two report branches

### OWNER_OCCUPIER_ACQUISITION

Primary outputs:

- MarketValueRange / ExpectedAcquisitionRange;
- PurchaseAssistanceAssessment where relevant;
- FundingSupportedPriceCeiling;
- funding gap;
- repayment scenarios;
- ownership cost;
- blocking unknowns.

Do not add investment-return metrics by default.

### INVESTMENT_DEVELOPMENT

Primary outputs:

- MARKET AcquisitionPriceAssessment;
- AssetUtilityAssessment;
- StrategyCandidates;
- strategy models actually run;
- FINAL AcquisitionPriceAssessment;
- StrategyComparison;
- ReturnBasis / TaxTreatment;
- blocking unknowns.

## ReproducibilityBundle

Because the current Console has no persistence backend, the report should embed a compact reproducibility bundle.

Recommended contents:

- ClientProfile snapshot;
- FinancialSnapshot used;
- AcquisitionContext;
- sourceRegistryVersion;
- policyRegistryVersion;
- EffectiveAssumptionSet snapshots used;
- PolicySnapshot values used in calculations;
- normalized material Property/Listing observations;
- Skill versions;
- model/calculation version;
- generatedAt.

Do not embed unlimited raw third-party content.

Prefer normalized observations, hashes, references and derived values permitted by Source Policy.

## Report status

Supported statuses:

- COMPLETE
- PARTIAL
- BLOCKED

### COMPLETE

The requested analysis path completed and all required output sections exist.

This does **not** mean all evidence is known or that the investment/property is recommended.

### PARTIAL

Useful analysis exists, but one or more requested model sections could not be completed.

### BLOCKED

A material required input prevents the requested result.

Do not use vague statuses such as "mostly complete".

## Unknowns and conflicts

The report must keep these separate:

- materialUnknowns[];
- evidenceConflicts[];
- verificationRequired[].

UNKNOWN is not a negative finding.

CONFLICTED is not simply low confidence.

## Presentation

User-facing prose should be concise and decision-oriented.

Structured sections should remain available underneath for audit/replay.

A demo report should be understandable without requiring the reader to inspect the original chat.

For a material user-facing report, responsive HTML is the default reading view. Generate it only after the `CanonicalDemoReport` is assembled and validated.

The HTML is a derived presentation artifact, not the source of truth. The canonical YAML/JSON remains authoritative for audit, fixture assertions and replay.

Use the shared [HTML rendering profile](html-rendering-profile.md) through the `html-report-renderer` Skill. Do not make each domain Skill build its own page and do not hand-write HTML/CSS/SVG when the renderer is available. The only SVG exception is the repository's bounded, deterministic chart generator.

Every rendered report embeds the compact Iris logo from [../Assets/Brand](../Assets/Brand/README.md). The report remains a single offline HTML file.

The shared profile also defines a restrained monochrome icon vocabulary for panel headings and canonical status markers. Icons improve scanning but never replace text, evidence state or report meaning.

Reports use the Iris orange-white theme and may add validated local line, bar and donut charts when the canonical report contains compatible series or a real compositional whole. Charts never invent missing points, mix incompatible bases or replace the exact result tables.

If rendering is unavailable or fails, preserve the canonical report, return a concise Markdown view and show the rendering error. Do not silently return stale HTML and do not change the analytical `ReportStatus` because presentation failed.


### PROPERTY_COMPLEX

When the address resolves to a PropertyComplex and the target is ANY_UNIT_IN_COMPLEX or UNKNOWN_UNIT_IN_COMPLEX, a valid report may contain:

- ComplexProfile;
- AcquisitionTarget;
- unit archetypes;
- observed unit sale/rent ranges;
- candidate properties where known;
- material unknowns.

It should not contain a property-specific valuation/acquisition/strategy result until a specific unit is resolved.
