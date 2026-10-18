---
name: iris
description: Start Iris Console workflows and preserve legacy /iris area, property and profile command compatibility.
metadata:
  product: Iris Console
  version: 0.1.0
  portable: true
---

# Iris Entry

## Purpose

Provide one stable conversational entrypoint for Iris Console while delegating
all domain work to the maintained Skills.

This Skill translates invocation syntax. It does not research properties,
calculate financial results or duplicate orchestration rules.

## Supported invocations

Treat these as equivalent entry forms when the host exposes slash commands or
explicit Skill invocation:

```text
/iris
$iris
/iris area "Lightsview, SA 5085"
/iris property "67 Bells Road, Glengowrie SA 5044"
/iris profile
```

A host that does not expose `/iris` may still invoke `$iris` or select the
`iris` Skill by name.

## Dispatch

### Bare entry

For `/iris` or `$iris` without a target:

1. reuse any ClientProfile, FinancialSnapshot and AcquisitionContext already in
   the active conversation or supplied report snapshot;
2. ask one concise question for the user's current intent or target; and
3. dispatch to the minimum applicable path below.

Do not present the user with a list of internal Skill names.

### `area <locality>`

Normalize the remaining text as an area reference. Require suburb/locality plus
state or postcode when needed to resolve ambiguity.

Route to `property-market-analysis` at area scope. Add other evidence Skills
only when the user's question needs them. Return area evidence and context; do
not fabricate a PropertyRef, parcel, dwelling attributes, property value,
property rent or site-specific planning conclusion.

### `property <target>`

Treat the remaining text as an address, listing URL, listing ID, PropertyRef or
PropertyComplex reference. Pass it as a provisional AcquisitionTarget to
`property-development-orchestrator`.

The orchestrator owns client-context reuse, entity resolution, branch routing,
canonical reporting and HTML presentation.

### `profile`

Route to `client-profile-onboarding`. Reuse known context and ask only for the
minimum missing facts that materially affect the user's current decision.

The current Console phase uses structured session/report snapshots; it does not
claim that a local profile is a cross-device account or backend record.

### Natural-language request

If text after `iris` is not a recognized subcommand, treat it as the user's
natural-language property request and route it through
`property-development-orchestrator`. Ask for clarification only when the target
or intended analysis branch cannot be inferred safely.

## Output

Return the selected branch's normal semantic output. For material reports,
retain the canonical YAML/JSON artifact and use `html-report-renderer` for the
default reading view unless the user asks for another format.

## Guardrails

- Do not create a second copy of orchestration, source, assumption, finance or
  report rules in this entry Skill.
- Do not turn an area request into a property-specific analysis.
- Do not treat invocation syntax as permission to access unavailable sources or
  mutate external systems.
- Preserve UNKNOWN, CONFLICTED, STALE and UNVERIFIED states through dispatch.
