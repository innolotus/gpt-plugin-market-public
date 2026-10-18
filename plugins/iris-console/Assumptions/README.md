# Iris Console Assumption Sets

This directory contains the **maintainer-managed, versioned modelling assumptions** used by Iris Console in the current demo phase.

Assumptions are not facts.

They exist to make modelling repeatable when a required future-looking/model input is not directly established by evidence.

## Design goals

- zero-config defaults where reasonable;
- explicit provenance;
- versioned and immutable base sets;
- safe user/client overrides;
- reproducible reports;
- no hidden numbers inside Skills.

## Files

- `registry.yaml` — available assumption sets and status.
- `SA_RESIDENTIAL_INCOME_2026Q4-v1.yaml` — income-investment defaults.
- `SA_REPLACEMENT_DEVELOPMENT_2026Q4-v2.yaml` — active replacement-development defaults with timed-finance semantics.
- `SA_SUBDIVISION_DEVELOPMENT_2026Q4-v2.yaml` — active subdivision-development defaults with timed-finance semantics.
- `SA_OWNER_OCCUPIER_ACQUISITION_2026Q4-v1.yaml` — owner-occupier acquisition/repayment defaults.
- superseded versions remain in the directory for reproducibility.

## Important distinction

An AssumptionSet may contain:

1. a usable default value;
2. a target/threshold used only for model interpretation;
3. a required-input marker when a generic default would be misleading.

Do not fabricate a numerical value merely to make every field non-null.

Examples:

- generic vacancy allowance can have a default;
- construction cost per square metre should often remain property/project-specific;
- current mortgage rate should prefer a FinancialSnapshot or explicit source-derived assumption over a static default.

## Assumption origin

Supported origins:

- `DEFAULT_ASSUMPTION`
- `USER_ASSUMPTION`
- `CLIENT_ORG_ASSUMPTION`
- `SOURCE_DERIVED_ASSUMPTION`

A base YAML file normally contains DEFAULT_ASSUMPTION values.

At runtime/demo execution, a Skill may build an EffectiveAssumptionSet by overlaying more specific values.

## Override precedence

Use this precedence unless a Skill explicitly documents a stricter rule:

```text
USER_ASSUMPTION
        ↓
CLIENT_ORG_ASSUMPTION
        ↓
SOURCE_DERIVED_ASSUMPTION
        ↓
DEFAULT_ASSUMPTION
```

This is precedence for model input selection, not evidence authority.

A user assumption can override a default for a scenario, but it does not become FACT.

## Immutability

Never edit an existing version in-place to change modelling meaning.

If a maintained default changes materially:

1. create a new version;
2. update `registry.yaml`;
3. mark the old version SUPERSEDED if appropriate;
4. retain old versions for report reproducibility.

Example:

```text
SA_RESIDENTIAL_INCOME_2026Q4-v1
→ SA_RESIDENTIAL_INCOME_2026Q4-v2
```

Historical reports that used v1 still refer to v1.

## EffectiveAssumptionSet

A report/model run should preserve:

- baseAssumptionSetId;
- baseAssumptionSetVersion;
- appliedOverrides[];
- effectiveValues;
- generatedAt.

Example:

```text
Base:
  mortgageInterestRate = 6.00%
  origin = DEFAULT_ASSUMPTION

Override:
  mortgageInterestRate = 5.72%
  origin = USER_ASSUMPTION
  source = lender quote supplied by user

Effective:
  mortgageInterestRate = 5.72%
```

Do not rewrite the base set.

## Sensitivity

A default value is not a prediction.

Material assumptions should define or recommend a sensitivity range where useful.

For example:

- interest rate;
- vacancy;
- rent growth;
- capital growth;
- construction cost;
- GRV;
- project duration.

The Skill should show decision sensitivity instead of pretending the base assumption is certain.


## Development-finance assumptions

The active development assumption sets use monthly cash-flow granularity by default.

They intentionally do not invent:

- finance rate;
- lender facility limit;
- debt drawdown rule;
- construction draw schedule;
- sales settlement schedule;
- project duration.

Those values must come from explicit financing/project assumptions or supported source-derived scenarios.

If financing structure is incomplete:

- unleveredProjectIrr may still be calculated when project timing/cost/revenue inputs are sufficient;
- leveredEquityIrr must remain UNKNOWN.

When development-finance semantics change materially, create a new AssumptionSet version rather than editing a historically used base set.
