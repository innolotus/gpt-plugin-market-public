# Iris Console Trusted Sources

This directory contains the **maintainer-managed static trusted-source registry** used by Iris Console during the demo / GPT-native phase.

Normal users do not add, remove or rank data sources.

The Console should behave as zero-config:

1. determine the FactType required by the active Skill;
2. read the preferred source order from `source-authority.yaml`;
3. use an available approved source/tool;
4. use the configured fallback only when permitted;
5. preserve conflicts instead of silently choosing the more convenient value.

## Files

- `trusted-sources.yaml` — approved source definitions, access constraints, freshness and licensing notes.
- `source-authority.yaml` — FactType-specific preferred/fallback order and conflict-resolution policy.

`source-authority.yaml` records routing intent, while each source's
`supportedFactTypes` records its declared capability vocabulary. Packaging
surfaces a lexical mismatch between those two lists as an alignment warning.
Until the registry defines whether `supportedFactTypes` is exhaustive or
provides aliases, that warning alone must not be treated as proof that a source
lacks the real capability or that runtime routing failed.

## Maintainer workflow

Source changes are repository changes.

When adding, changing or retiring a source:

1. verify the official source and current access terms;
2. update `trusted-sources.yaml`;
3. update any affected FactTypes in `source-authority.yaml`;
4. increment `registryVersion`;
5. update `verifiedAt`;
6. review whether existing reports/fixtures depend on the old source semantics.

Do not expose these files as a normal user preference surface.

## Authority principle

Authority is scoped to the fact being established.

Examples:

- PlanSA is authoritative for South Australian planning policy.
- RevenueSA is authoritative for South Australian stamp duty and state first-home concessions.
- RBA is authoritative for the cash-rate target.
- ABS is authoritative for official Census/demographic statistics.
- Authorised market-data sources are appropriate for current listings, market estimates and comparables.

A government source is not automatically authoritative for a live agent listing, and a property portal is not authoritative for statutory planning rules.

## User-provided evidence

User-provided reports, pre-approvals, builder quotes, titles, inspections and appraisals may be highly relevant.

They are supplementary evidence unless the document itself is an authoritative source for the fact being asserted.

Example:

- a formal title search supplied by the user may be authoritative title evidence;
- an agent rental appraisal is evidence of the agent's appraisal, not a guaranteed market rent;
- a builder quote is strong project-cost evidence for that quote/specification, not a universal construction-cost benchmark.
