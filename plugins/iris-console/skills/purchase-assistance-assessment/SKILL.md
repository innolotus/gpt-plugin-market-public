---
name: purchase-assistance-assessment
description: Discover and assess current Australian purchase-assistance programs that may change deposit, cash, LVR or financing outcomes.
metadata:
  product: Iris Console
  version: 0.3.0
  portable: true
  time_sensitive: true
---

# Purchase Assistance Assessment

## Purpose

Discover and evaluate current purchase-assistance programs that may materially change:

- minimum deposit;
- upfront cash required;
- lender loan amount;
- effective LVR;
- LMI treatment;
- government guarantee;
- shared equity;
- cash grant;
- stamp duty;
- acquisition feasibility.

The Skill does **not** own the program catalogue.

Use:

`Console/Policies/purchase-assistance-registry.yaml`

as the maintained program registry.

## Critical boundary

Do not apply owner-occupier assistance to:

- INVESTMENT_FROM_SETTLEMENT; or
- DEVELOPMENT_FOR_PROFIT;

unless the current program explicitly permits that use.

Do not suggest artificial occupancy or other behaviour designed to obtain assistance contrary to program requirements.

## Procedure

### 1. Load registry

Load the active PurchaseAssistanceRegistry and preserve its `registryVersion`.

### 2. Discover candidate programs

Use:

- jurisdiction;
- AcquisitionContext;
- property type / new-vs-established state;
- purchase-price context;
- already-known PurchaseEligibilityFacts;
- program discoveryMode.

Do not ask for every eligibility fact for every program.

### 3. Respect discovery mode

#### AUTO_DISCOVER

May be considered automatically when ordinary available facts make the program plausibly relevant.

#### CONDITIONAL_DISCOVER

Only consider when the triggering non-sensitive condition is already known.

Do not ask an unrelated client for age or other optional details just to discover a niche program.

#### EXPLICIT_DISCLOSURE_OR_REQUEST

Do not proactively ask for the triggering sensitive circumstance.

Only evaluate if:

- the user explicitly discloses it; or
- the user explicitly asks about the program.

### 4. Verify current material rules

If `verificationPolicy = VERIFY_AT_EXECUTION`, verify material current rules using the authoritative source IDs defined in the registry and Source Policy.

A static currentSnapshot is a routing/demo aid, not permanent truth.

Before using a time-sensitive value as current FACT, verify where material:

- deposit minimum;
- grant amount;
- income threshold;
- property price cap;
- shared-equity percentage;
- property type;
- residence requirement;
- participating-lender requirement;
- effective/contract date;
- current program status.

### 5. Evaluate eligibility

Evaluate each candidate separately.

Use:

- ELIGIBLE
- POTENTIALLY_ELIGIBLE
- INELIGIBLE
- NOT_APPLICABLE
- UNKNOWN

Do not force UNKNOWN into INELIGIBLE merely because a field is missing.

### 6. Generate financing scenarios

Only generate materially relevant scenarios.

Keep distinct:

- buyer deposit / cash contribution;
- lender loan;
- government guarantee;
- government equity;
- cash grant;
- stamp-duty relief;
- LMI treatment.

Never merge all assistance into one generic "government contribution".

## Program-type calculation semantics

### GOVERNMENT_GUARANTEE

A guarantee supports the lender.

It is **not**:

- buyer cash;
- purchase-price contribution;
- government equity.

### SHARED_EQUITY

Government/provider equity reduces the amount funded by buyer cash + lender loan.

It creates an ongoing equity interest/obligation according to the current program terms.

Do not call it a grant.

### CASH_GRANT

A grant may reduce net buyer cash requirement only when:

- eligibility is supported; and
- payment timing makes it usable for the relevant settlement/progress payment.

### STAMP_DUTY_RELIEF

Reduces or removes eligible duty.

It does not reduce the contractual purchase price.

### PUBLIC_LENDER_PRODUCT

A public-lender product may change:

- minimum deposit;
- loan structure;
- shared-equity availability;
- fee/LMI treatment.

Program eligibility is separate from loan approval.

### EX_GRATIA_RELIEF

Evaluate only under the registry's discovery/sensitivity rules.

Do not proactively collect sensitive triggering facts.

## Buyer / property facts

Only request fields needed by candidate programs.

Possible fields include:

- intendedOccupancy;
- firstHomeBuyerStatus;
- priorPropertyOwnership;
- citizenshipOrResidency;
- applicantCount;
- singleParentOrGuardianStatus;
- taxableIncome;
- householdIncome;
- availableDeposit;
- propertyType;
- newOrEstablished;
- purchasePrice;
- lenderValuation;
- postcode / jurisdiction;
- principalResidenceIntent;
- otherPropertyOwnership;
- desiredLoanStructure.

Do not infer missing sensitive facts.

## Downstream owner-occupier use

When AcquisitionContext is OWNER_OCCUPIER, feed evaluated scenarios into `owner-occupier-acquisition`.

The downstream model may use:

- deposit;
- lender loan;
- government guarantee;
- shared equity;
- grant;
- duty treatment;
- LMI treatment.

It must still not infer lender approval or general affordability.

## Output

Return PurchaseAssistanceAssessment including:

- policyRegistryVersion;
- candidateProgramIds[];
- evaluatedPrograms[];
- policySnapshot[];
- eligibilityByProgram[];
- financingScenarios[];
- stampDutyTreatment;
- grantTreatment;
- sharedEquityTreatment;
- minimumCashRequirement;
- lenderLoanAmount;
- effectiveLvr;
- governmentGuaranteeAmount;
- governmentEquityAmount;
- lmiTreatment;
- assumptions;
- blockingUnknowns;
- verificationRequired;
- confidence.

## Guardrails

Do not:

- hard-code a permanent list of current policy thresholds inside this Skill;
- guarantee eligibility;
- infer lender approval;
- infer borrowing capacity from income;
- apply owner-occupier programs to ineligible investment/development use;
- use stale registry snapshots as current FACT without required verification;
- ask speculative sensitive questions merely to discover additional programs;
- conceal ongoing occupancy/equity/program obligations.
