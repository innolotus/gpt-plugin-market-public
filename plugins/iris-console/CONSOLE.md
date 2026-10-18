# Iris Console

Iris Console is the GPT-native property investment and development decision console for Iris-B-RE.

The current phase is deliberately **Console-first**:

- no custom Iris backend dependency;
- Skills and semantic contracts live in GitHub;
- trusted sources are maintained as static repository configuration;
- client context is kept as a structured session/report snapshot;
- the Console is used primarily for demo, workflow validation and client delivery;
- backend/runtime implementation is deferred until Iris productization is explicitly approved.

The core question is:

> **What is the most economically sensible way to use this asset, for this client, under the available evidence?**

## Current execution model

```text
Client Context
  ├─ ClientProfile
  ├─ FinancialSnapshot
  └─ AcquisitionContext
        ↓
Load applicable AssumptionSet(s)
        +
Property / Listing
        ↓
Iris Console Skills
        ↓
Static trusted-source rules + approved tools/web sources
        ↓
Evidence with provenance + EvidenceState
        ↓
Versioned AssumptionSet(s)
        ↓
MARKET acquisition-price assessment
        ↓
Strategy analysis
        ↓
FINAL acquisition-price assessment
        ↓
Strategy comparison
        ↓
CanonicalDemoReport + AnalysisContext snapshot
        ↓
Responsive HTML report
```

## Progressive profiling

Use `client-profile-onboarding` to:

- reuse already-known profile facts;
- ask only for fields that materially change the current analysis;
- keep stable client preferences separate from property-specific intent;
- request first-home / assistance details only when relevant;
- keep financial information in a time-sensitive FinancialSnapshot.

See [Profile/README.md](Profile/README.md).

## Evidence discipline

Every material assertion should separate:

- statement class: FACT / CALCULATION / INFERENCE / ASSUMPTION / UNKNOWN;
- evidence state: CONFIRMED / CONFLICTED / STALE / UNVERIFIED / UNKNOWN;
- confidence;
- provenance and timestamps.

A source conflict is not merely "low confidence".

See [Evidence/README.md](Evidence/README.md).

## Versioned assumptions

Iris Console does not hide modelling defaults inside Skills.

Maintainer-managed sets live under:

- [Assumptions/README.md](Assumptions/README.md)
- [Assumptions/registry.yaml](Assumptions/registry.yaml)

Each strategy run builds an `EffectiveAssumptionSet` from:

```text
immutable base AssumptionSet
+
explicit overrides
=
EffectiveAssumptionSet
```

Supported override origins include:

- USER_ASSUMPTION;
- CLIENT_ORG_ASSUMPTION;
- SOURCE_DERIVED_ASSUMPTION;
- DEFAULT_ASSUMPTION.

A more specific override changes the model input, not its evidential class.

Some material fields intentionally have no static default. Missing build cost, mortgage rate, project duration or dwelling count should remain missing or become explicit scenario assumptions rather than fabricated values.

## Acquisition-price discipline

Iris separates:

1. **MarketValueRange** — what broad range the market evidence supports;
2. **ExpectedAcquisitionRange** — where the current campaign may transact;
3. **StrategyMaximumPrice** — the maximum price a particular strategy can economically support under explicit targets/assumptions.

The acquisition-price Skill runs twice:

```text
MARKET pass
→ market range / expected acquisition range

strategy models
→ break-even / target-return thresholds

FINAL pass
→ StrategyMaximumPrice + gap analysis
```

Do not merge those numbers into one generic "valuation".

## Timed development finance

Replacement and subdivision feasibility use an explicit DevelopmentCashFlow timeline.

The Console distinguishes:

- unleveredProjectIrr — project economics before financing flows;
- leveredEquityIrr — equity return after debt draw, interest and repayment.

If financing assumptions are incomplete, leveredEquityIrr remains UNKNOWN.

The model also tracks where inputs permit:

- total finance interest;
- peak debt;
- peak equity at risk;
- total equity contributed;
- project duration.

See [DevelopmentFinance/README.md](DevelopmentFinance/README.md).

## Return basis

Every material profit/return metric must declare:

- `ReturnBasis = PRE_TAX | AFTER_TAX_ESTIMATE`;
- TaxModelStatus;
- material included / excluded / unknown tax components.

PRE_TAX is the default.

Including stamp duty or another transaction cost does not make a model AFTER_TAX_ESTIMATE.

Strategies with incompatible tax bases must not be directly ranked by IRR/profit.

See [Tax/README.md](Tax/README.md).

## Property complexes

An address may resolve to a single PropertyRef or a PropertyComplex.

For multi-unit buildings/groups, Iris can keep the complex as the resolved entity and represent the acquisition target as:

- SPECIFIC_PROPERTY;
- ANY_UNIT_IN_COMPLEX;
- UNKNOWN_UNIT_IN_COMPLEX;
- COMPLEX_AS_WHOLE.

A missing unit number does not automatically stop analysis.

For ANY_UNIT / UNKNOWN_UNIT targets, Iris may continue with complex-level unit archetypes, sale/rent observations and acquisition ranges while avoiding property-specific valuation/strategy claims.

## Purchase-assistance registry

Purchase-assistance programs are maintained as static GitHub configuration:

- [Policies/README.md](Policies/README.md)
- [Policies/purchase-assistance-registry.yaml](Policies/purchase-assistance-registry.yaml)

The policy registry answers:

> What programs exist, when should Iris consider them, and which rules must be verified?

The trusted-source registry answers:

> Which source is authoritative for verifying those rules?

Normal users do not configure either registry.

Material current thresholds are verified at execution time before being treated as current FACT.

## Owner-occupier acquisition path

Owner occupation is an acquisition / financing path, not a fourth investment strategy.

For a normal owner-occupier request:

```text
Client Context
↓
Property Research
↓
Market Analysis
↓
Acquisition Price Assessment [MARKET]
↓
Purchase Assistance when relevant
↓
Due Diligence as required
↓
Owner-Occupier Acquisition
↓
Funding / repayment / ownership-cost decision support
```

The owner-occupier model may produce a `FundingSupportedPriceCeiling` from known financing inputs.

That ceiling is not:

- market value;
- StrategyMaximumPrice;
- lender approval;
- a guarantee of affordability.

The investment/development strategy branch only runs if the user asks for it or it is materially part of the stated objective.

See [OwnerOccupier/README.md](OwnerOccupier/README.md).

## Strategy-first model

Primary strategy archetypes:

1. **Income Investment** — buy, rent and hold.
2. **Replacement Development** — acquire an asset whose existing improvement has little economic utility, demolish it and rebuild a single dwelling.
3. **Subdivision Development** — acquire land/development potential, subdivide and create multiple saleable or rentable assets.

A property may support more than one strategy. Iris compares plausible paths rather than forcing one too early.

Property age is an input to Building Utility, not a demolition rule.

## Core reasoning chain

```text
ClientProfile / FinancialSnapshot
        ↓
AcquisitionContext
        +
Property / Listing
        ↓
Property Research
        ↓
Property Market Analysis
        ↓
Acquisition Price Assessment [MARKET]
        ↓
Purchase Assistance when relevant
        ↓
Asset Utility / Planning / Due Diligence
        ↓
Strategy Assessment
        ↓
┌────────────────────┬────────────────────────┬─────────────────────────┐
│ Income Investment  │ Replacement Development│ Subdivision Development │
└─────────┬──────────┴────────────┬───────────┴─────────────┬───────────┘
          ↓                       ↓                         ↓
      Hold model             project model              project model
          └───────────────────────┼─────────────────────────┘
                                  ↓
                 Acquisition Price Assessment [FINAL]
                                  ↓
                         Strategy Comparison
                                  ↓
                        Report / AnalysisContext
```

## Active Skill package

Distribution metadata is defined in [skill-pack.json](skill-pack.json). Build the credential-free zip with `scripts/package-iris-skill-pack.py` from the repository root.

The installable Agent Plugin uses the source template at `plugins/iris-console`
and the same canonical Console content. Build its credential-free archive with
`scripts/package-iris-plugin.py`; this preserves shared files such as
`SOURCE_POLICY.md` while exposing all Skills at `skills/<name>/SKILL.md`.

### Entry skill

- `iris` is the stable user-facing entrypoint and compatibility adapter.

Where the host exposes slash commands, `/iris`, `/iris area <locality>`,
`/iris property <target>` and `/iris profile` remain supported. Hosts that use
explicit Skill invocation can call `$iris`. The entry Skill delegates property
work to `property-development-orchestrator` and does not duplicate domain logic.

### Client-context / acquisition / orchestration skills

- `client-profile-onboarding`
- `purchase-assistance-assessment`
- `owner-occupier-acquisition`
- `property-development-orchestrator`

### Pricing / strategy skills

- `acquisition-price-assessment`
- `property-strategy-assessment`
- `income-investment`
- `replacement-development`
- `subdivision-development`
- `strategy-comparison`

### Evidence-support skills

- `property-research`
- `property-market-analysis`
- `planning-development-analysis`
- `property-due-diligence`
- `policy-impact-analysis`
- `property-monitoring`

## Trusted sources

Normal users do not configure sources.

The static registry lives under:

- [Sources/README.md](Sources/README.md)
- [Sources/trusted-sources.yaml](Sources/trusted-sources.yaml)
- [Sources/source-authority.yaml](Sources/source-authority.yaml)

## Documents

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [CONTRACTS.md](CONTRACTS.md)
- [STRATEGY_MODEL.md](STRATEGY_MODEL.md)
- [SOURCE_POLICY.md](SOURCE_POLICY.md)
- [Profile/README.md](Profile/README.md)
- [Evidence/README.md](Evidence/README.md)
- [Assumptions/README.md](Assumptions/README.md)
- [Tax/README.md](Tax/README.md)
- [DevelopmentFinance/README.md](DevelopmentFinance/README.md)
- [OwnerOccupier/README.md](OwnerOccupier/README.md)
- [Policies/README.md](Policies/README.md)
- [Sources/README.md](Sources/README.md)

## Canonical demo report

Material demo runs should output a CanonicalDemoReport.

Because the current phase has no backend, the report embeds a compact ReproducibilityBundle containing the normalized snapshots and versions used by the analysis.

See:

- [Reports/README.md](Reports/README.md)
- [Reports/canonical-demo-report-template.yaml](Reports/canonical-demo-report-template.yaml)
- [Reports/html-rendering-profile.md](Reports/html-rendering-profile.md)
- [Tests/EXECUTION.md](Tests/EXECUTION.md)

The validated canonical YAML/JSON is the audit and replay source. A shared `html-report-renderer` Skill projects it into a responsive single-file HTML reading view through `answer-me-with-html`. Domain Skills remain presentation-agnostic.

The Console host must provide [`answer-me-with-html`](https://github.com/QingYunA/answer-me-with-html) 0.5.2 or a later compatible 0.5.x release and Node.js 20 or newer. Analysis runs discover the configured renderer but never install or update it themselves.

Iris report branding lives in [Assets/Brand](Assets/Brand/README.md), with the orange-white report theme in [Assets/Themes](Assets/Themes/README.md). The renderer embeds the compact logo and any validated canonical line, bar or donut charts into each offline HTML report.

Fixture definitions being present does not mean they have passed. PASS/FAIL belongs to actual validation runs.

## Product principle

Iris Console should not produce a plausible-looking report merely from a listing.

It should preserve:

```text
Client Context
+
Evidence
+
Assumptions
→ Market Price Context
→ Strategy
→ Model
→ Strategy Price Limits
→ Comparison
→ Decision Support
```

The current Console validates these domain semantics without prematurely implementing the future Iris backend.
