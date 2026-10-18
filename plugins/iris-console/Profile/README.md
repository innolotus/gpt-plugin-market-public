# Iris Console Client Profile

This directory defines the **demo-phase client context format** used by Iris Console.

There is no profile database in the current phase.

The profile exists as a structured session/report snapshot so the Console can:

- avoid repeatedly asking the same questions;
- tailor financing and strategy analysis;
- request sensitive eligibility information only when relevant;
- make reports reproducible;
- later migrate the same semantics into Iris product storage.

## Three different concepts

Do not merge these.

### ClientProfile

Relatively stable client preferences and eligibility facts.

Examples:

- investor type;
- investment objective;
- holding horizon;
- risk tolerance;
- development capability;
- first-home-buyer facts where relevant.

### FinancialSnapshot

Time-sensitive financial information.

Examples:

- available cash;
- deposit;
- bank pre-approval;
- borrowing capacity;
- existing debt.

A FinancialSnapshot may expire.

### AcquisitionContext

The intent for one property / analysis.

Examples:

- owner-occupy this property;
- buy and rent from settlement;
- buy for subdivision;
- target purchase price.

The same user may have multiple AcquisitionContexts over time.

## Progressive profiling

Do not present the user with a long onboarding form.

Ask only what is needed to make the current decision materially better.

Suggested initial questions are usually limited to:

1. What best describes your goal: owner-occupier, individual investor, professional investor/developer?
2. What do you intend to do with this property?
3. Do you have a cash/deposit amount or lender pre-approval you want Iris to use?

Only ask first-home/eligibility questions when:

- the user is or may be an owner-occupier; and
- the property/purchase context makes an assistance program potentially relevant.

Do not ask sensitive fields merely to make the profile look complete.

## Reuse

If a fact is already available in the active profile/context, reuse it.

Do not ask the same question again unless:

- the value is missing;
- the value is stale/expired;
- the current property requires a different AcquisitionContext;
- the user indicates the value changed.

## Report snapshots

A report should include enough AnalysisContext to identify which:

- profile version;
- financial snapshot;
- acquisition context;
- source-registry version;
- assumption set(s) and applied overrides;

were used.

This is a demo-stage snapshot, not backend persistence.
