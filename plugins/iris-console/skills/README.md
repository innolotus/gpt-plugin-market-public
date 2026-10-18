# Iris Console Skills

## Purpose

Iris Console uses a strategy-first property underwriting Skill package with progressive client profiling, evidence-state handling and explicit acquisition-price semantics.

The user should not need to know which Skill to call.

Start with `iris`. Hosts may expose it as `/iris`; explicit Skill invocation
uses `$iris`. Legacy `area`, `property` and `profile` subcommands are translated
by this thin entry Skill and then delegated to the maintained domain pipeline.

## Mandatory rules

Every Skill must:

- distinguish FACT, CALCULATION, INFERENCE, ASSUMPTION and UNKNOWN;
- preserve EvidenceState separately from confidence;
- retain provenance;
- surface material unknowns/conflicts;
- reuse available client context;
- avoid asking optional profile fields prematurely;
- load applicable versioned AssumptionSet(s) instead of hiding defaults in prompts;
- preserve EffectiveAssumptionSet overrides;
- use timed DevelopmentCashFlow for development IRR / peak debt / peak equity;
- distinguish unleveredProjectIrr from leveredEquityIrr;
- declare ReturnBasis / TaxTreatment for material financial outputs;
- use deterministic calculation tools for arithmetic/financial modelling;
- discover purchase-assistance programs from the static policy registry;
- verify time-sensitive government policy before using it;
- respect [../SOURCE_POLICY.md](../SOURCE_POLICY.md).

Domain Skills produce semantic objects. They do not hand-write presentation HTML.

For every material user-facing report, the orchestrator must first assemble and validate the `CanonicalDemoReport`, then pass it to `html-report-renderer`. The HTML is the default reading view; the canonical YAML/JSON remains the audit and replay source.

## Primary decision pipeline

```text
iris
        ↓
client-profile-onboarding / reuse existing context
        ↓
property-research
        ↓
property-market-analysis
        ↓
acquisition-price-assessment [MARKET]
        ↓
load/build EffectiveAssumptionSet(s)
        ↓
purchase-assistance-assessment when relevant
        ↓
property-strategy-assessment
        ↓
┌────────────────────────┬──────────────────────────┬───────────────────────────┐
│ income-investment      │ replacement-development  │ subdivision-development   │
└────────────┬───────────┴────────────┬─────────────┴─────────────┬─────────────┘
             └────────────────────────┼────────────────────────────┘
                                      ↓
                       acquisition-price-assessment [FINAL]
                                      ↓
                             strategy-comparison
                                      ↓
                       CanonicalDemoReport validation
                                      ↓
                         html-report-renderer
```

## Client-context / acquisition Skills

| Skill | Question |
|---|---|
| client-profile-onboarding | What is the minimum client context needed and what can be reused? |
| owner-occupier-acquisition | What upfront cash, funding boundary, repayments and ownership costs apply if the client buys this home to occupy? |

## Entry Skill

| Skill | Question |
|---|---|
| iris | Which area, property or profile workflow did the user request, and where should it be delegated? |

## Pricing / Decision Skills

| Skill | Question |
|---|---|
| acquisition-price-assessment | What market/acquisition range is supported, and what maximum price can each strategy support? |
| purchase-assistance-assessment | Do current owner-occupier / first-home programs change upfront cash or financing? |
| property-strategy-assessment | What economic uses of this asset are worth modelling? |
| income-investment | What happens if the property is bought, rented and held? |
| replacement-development | Does demolishing and rebuilding one asset create value? |
| subdivision-development | Can subdivision / multi-dwelling development create enough value? |
| strategy-comparison | How do viable strategies compare on capital, price gap, time, return, risk and uncertainty? |
| property-development-orchestrator | Which context, evidence, pricing, assistance and strategy Skills should run? |

## Evidence-support Skills

| Skill | Question |
|---|---|
| property-research | What property is this and what evidence exists? |
| property-market-analysis | What comparable/market evidence exists and how reliable/relevant is it? |
| planning-development-analysis | What development paths appear possible or constrained? |
| property-due-diligence | What material risks and unknowns remain? |
| policy-impact-analysis | What policy change may affect the asset or strategy? |
| property-monitoring | What materially changed since the prior observation? |

## Presentation Skill

| Skill | Question |
|---|---|
| html-report-renderer | How is the validated canonical report delivered as responsive HTML without changing its meaning? |

Individual domain Skills remain presentation-agnostic. When a domain Skill is invoked directly and the user requests a full report, complete its semantic output first and then route the result through the shared renderer.

## Evidence rule

Confidence and EvidenceState are different.

Do not silently average or choose between conflicting sources.

Do not feed unresolved material values into models as confirmed facts.

When scenario modelling is useful, convert chosen scenario inputs into explicit ASSUMPTIONS.

## Assumption rule

Do not hard-code modelling defaults inside a Skill when the value belongs in a maintained AssumptionSet.

Base sets are immutable and versioned.

Per-run overrides may come from:

- user;
- client organisation;
- source-derived scenario evidence;
- maintained defaults.

An override remains ASSUMPTION unless independently established as FACT.

If a field is marked `requiredInput: true`, do not fabricate a default merely to complete the model.

## Acquisition-price rule

Never collapse:

- asking/guide;
- MarketValueRange;
- ExpectedAcquisitionRange;
- break-even price;
- StrategyMaximumPrice;

into one generic `acquisitionPrice`.

Strategy models must retain the actual `modelAcquisitionPrice` used.

## Profile rule

Stable preferences belong in ClientProfile.

Time-sensitive funding belongs in FinancialSnapshot.

Property-specific intent belongs in AcquisitionContext.

Purchase-assistance facts should be requested only when relevant.

## Development-finance rule

Replacement and subdivision models must not derive project IRR from a single aggregate finance/holding number.

Use a timed DevelopmentCashFlow series.

Distinguish:

- unleveredProjectIrr;
- leveredEquityIrr.

If financing assumptions are incomplete, do not invent a lender structure. Return leveredEquityIrr as UNKNOWN.

Do not compare levered and unlevered IRRs as though they were the same metric.

## Return-basis rule

Default financial outputs to PRE_TAX unless a defined tax model supports AFTER_TAX_ESTIMATE.

Do not imply that development profit or leveraged IRR is after-tax merely because some transaction taxes/costs are included.

Before comparing strategies, verify that their ReturnBasis values are compatible.

Preserve material GST / margin-scheme / income-tax / CGT / land-tax unknowns where relevant.

## Purchase-assistance registry rule

`purchase-assistance-assessment` must discover candidate programs from:

`../Policies/purchase-assistance-registry.yaml`

Do not hard-code the current program catalogue/thresholds in the Skill.

The registry may contain a current snapshot, but rules marked VERIFY_AT_EXECUTION must be checked from authoritative sources before live use.

Respect discoveryMode:

- AUTO_DISCOVER;
- CONDITIONAL_DISCOVER;
- EXPLICIT_DISCLOSURE_OR_REQUEST.

Do not proactively collect sensitive triggering facts merely to discover a program.

## Owner-occupier rule

Owner occupation is not a fourth investment strategy.

When the user's AcquisitionContext is OWNER_OCCUPIER and the objective is purchase feasibility:

- use the owner-occupier branch;
- use MARKET acquisition-price assessment;
- run purchase assistance where relevant;
- do not run Strategy Comparison by default;
- do not generate investment-return metrics unless separately requested.

FundingSupportedPriceCeiling is a funding boundary, not market value or lender approval.

## Strategy rule

Age does not select a strategy.

Reason over client context + Building/Rental/Land/Development Utility + market/planning evidence.

These are hypotheses to model, not automatic recommendations.
