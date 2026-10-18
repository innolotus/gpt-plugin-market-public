# Iris Console Purchase Assistance Policies

This directory contains the **maintainer-managed static purchase-assistance registry** used by Iris Console during the Console-first demo phase.

The current Console does not require a policy backend.

Normal users do not select programs manually. The Console discovers candidate programs from the registry using:

- jurisdiction;
- intended occupancy;
- buyer/client facts already available;
- property type / new-vs-established status;
- current purchase price / price range;
- program discovery rules.

The Skill then verifies time-sensitive rules from the authoritative source before treating a program as currently applicable.

## Files

- `purchase-assistance-registry.yaml` — approved program catalogue, discovery rules, current snapshot metadata and authoritative source references.

## Design rule

The registry answers:

> What programs should Iris know exist, when should it consider them, and where must current rules be verified?

The Skill answers:

> Is this client/property currently eligible, and how does the program change the funding scenario?

Do not store permanent client facts such as:

```text
eligibleForHelpToBuy = true
```

Eligibility must be recomputed against the current registry + current authoritative policy + current AcquisitionContext.

## Verification

Every program has a `verificationPolicy`.

Typical value:

```text
VERIFY_AT_EXECUTION
```

This means the static registry may contain a current snapshot for demo convenience, but the Skill should verify material current values before using them in a live calculation.

Material values include:

- deposit minimum;
- property price cap;
- income threshold;
- grant amount;
- shared-equity percentage;
- residence requirement;
- contract/effective dates;
- participating-lender requirement;
- property type eligibility.

## Discovery modes

Supported discovery modes:

### AUTO_DISCOVER

The Console may consider the program automatically when non-sensitive available facts make it plausibly relevant.

Examples:

- first-home-buyer owner-occupier;
- new-home purchase in South Australia;
- Help to Buy where available facts suggest the price/income context may fit.

### CONDITIONAL_DISCOVER

Consider only when a non-sensitive triggering condition is already known.

Example:

- seniors downsizing relief when the client has already disclosed age/downsizing intent.

Do not ask unrelated users for age just to discover this program.

### EXPLICIT_DISCLOSURE_OR_REQUEST

Do not proactively ask the user for the triggering sensitive circumstance.

Only consider the program if:

- the user explicitly discloses the relevant circumstance; or
- the user explicitly asks about the program.

This applies to sensitive victim-survivor relief.

## Sensitive eligibility

A registry entry may include:

```text
sensitiveEligibility: true
```

The Console must not turn that into a speculative onboarding question.

The existence of a potentially beneficial program does not justify asking highly sensitive questions without a current reason.

## Program type

Programs are not interchangeable.

Supported semantic types include:

- GOVERNMENT_GUARANTEE
- SHARED_EQUITY
- CASH_GRANT
- STAMP_DUTY_RELIEF
- PUBLIC_LENDER_PRODUCT
- EX_GRATIA_RELIEF

A program may affect one or more funding components.

## Maintainer workflow

When a program changes:

1. verify the official current source;
2. update the registry snapshot;
3. increment `registryVersion`;
4. update `verifiedAt`;
5. preserve the program ID where the program is the same legal/product pathway;
6. retire programs rather than deleting historical meaning;
7. review affected fixtures/reports.

Do not bury current policy thresholds back inside a Skill.
