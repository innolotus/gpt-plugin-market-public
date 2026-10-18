# Iris Console Contracts

## 1. Purpose

All Iris Console Skills use shared semantic contracts so the same reasoning can later move into Iris/Ivy without redefining what the data means.

For the current Console-demo phase these are **semantic contracts**, not a requirement for a backend or database.

## 2. Evidence classes

Every material statement must be one of:

| Class | Meaning |
|---|---|
| FACT | Directly supported by a source. |
| CALCULATION | Deterministically derived from explicit inputs. |
| INFERENCE | Reasoned conclusion from evidence. |
| ASSUMPTION | Model input not established as fact. |
| UNKNOWN | Required information is absent, inaccessible or unresolved. |

UNKNOWN must never silently become FACT.

## 3. EvidenceState

Classification answers **what kind of statement is this?**

EvidenceState answers **what is the current evidential state of the assertion?**

These are independent dimensions.

Supported states:

| State | Meaning |
|---|---|
| CONFIRMED | Current evidence from the appropriate authority/source set supports the assertion with no unresolved material conflict. |
| CONFLICTED | Material current sources disagree. Preserve the disagreement. |
| STALE | Evidence was usable but is outside the required freshness window for the current decision. |
| UNVERIFIED | A claim/observation exists but has not been independently or authoritatively verified where verification matters. |
| UNKNOWN | The required fact cannot currently be established from approved evidence. |

Important examples:

```text
classification = FACT
state = CONFLICTED
```

means:

> It is a fact that Source A reports X and Source B reports Y; the underlying property fact remains unresolved.

```text
classification = FACT
state = STALE
```

means:

> The source fact was valid at its observation time but is too old for the current use.

Do not convert CONFLICTED, STALE or UNVERIFIED into CONFIRMED merely by lowering confidence.

## 4. MaterialAssertion<T>

Use a material assertion wrapper where multiple sources, freshness or conflict matter.

```text
MaterialAssertion<T>
├── value
├── classification
├── state
├── confidence
├── supportingEvidenceIds[]
├── conflictingEvidenceIds[]
├── observedAt
├── effectiveFrom
├── effectiveTo
├── retrievedAt
└── notes
```

If `state = CONFLICTED`, `value` may be null/unresolved and the competing values remain in the linked evidence.

If `state = UNKNOWN`, do not invent a placeholder value for downstream calculations.

## 5. Common result envelope

```json
{
  "result": {},
  "evidence": [],
  "calculations": [],
  "inferences": [],
  "assumptions": [],
  "unknowns": [],
  "warnings": [],
  "confidence": {
    "overall": "LOW|MEDIUM|HIGH",
    "notes": []
  }
}
```

## 6. Provenance-aware profile values

Client/profile facts may use:

```text
ProfileValue<T>
├── value
├── source
├── verified
├── observedAt
├── effectiveAt
├── expiresAt
└── notes
```

Suggested source values:

- USER_DECLARED
- DOCUMENT_VERIFIED
- LENDER_PREAPPROVAL
- AUTHORITATIVE_SOURCE
- LICENSED_MARKET_SOURCE
- SYSTEM_DERIVED

Do not treat USER_DECLARED as independently verified merely because it is stored in the profile.

## 7. ClientProfile

ClientProfile contains relatively stable client identity/preferences required for property analysis.

It does **not** contain property-specific purchase intent.

Recommended fields:

```text
clientProfileId
version
createdAt
updatedAt
basicProfile
investmentPreferences
purchaseEligibilityFacts
```

### BasicProfile

Keep this minimal.

Examples:

```text
preferredJurisdiction
householdType
```

Do not collect unrelated personal details merely because a profile exists.

### InvestmentPreferences

```text
investorType
primaryObjective
holdingHorizon
riskTolerance
developmentCapability
targetReturn
preferredStrategies
constraints
```

Possible investor types:

- INDIVIDUAL_INVESTOR
- PROFESSIONAL_INVESTOR
- SMALL_DEVELOPER
- OWNER_OCCUPIER
- UNSPECIFIED

Possible development capability values:

- NONE
- BEGINNER
- EXPERIENCED
- PROFESSIONAL
- UNKNOWN

## 8. PurchaseEligibilityFacts

Store client facts only, not policy conclusions.

Recommended fields:

```text
firstHomeBuyerStatus
priorPropertyOwnership
citizenshipOrResidency
applicantCount
singleParentOrGuardianStatus
taxableIncome
householdIncome
currentPropertyOwnership
```

Only request these progressively when a relevant assistance pathway may apply.

Do NOT persist conclusions such as:

```text
eligibleFor5PercentScheme = true
```

Eligibility must be recalculated from:

```text
PurchaseEligibilityFacts
+
AcquisitionContext
+
Property context
+
Current policy snapshot
```

## 9. FinancialSnapshot

FinancialSnapshot represents the client's financial position at a point in time.

Recommended fields:

```text
financialSnapshotId
clientProfileId
snapshotVersion
observedAt
effectiveAt
expiresAt

availableCash
availableDeposit
lenderPreApproval
borrowingCapacity
existingDebt
preferredLvr
loanPreference
interestRateAssumption
```

Each material field should use ProfileValue where useful.

Important:

- USER_DECLARED borrowing capacity is not lender approval.
- A lender pre-approval should preserve its expiry date and source.
- Do not infer borrowing capacity from unrelated user data.

## 10. AcquisitionContext

AcquisitionContext is property- and analysis-specific.

Recommended fields:

```text
acquisitionContextId
propertyId
acquisitionTarget
analysisObjective
intendedOccupancy
desiredStrategy
targetPurchasePrice
financingPreference
createdAt
```

Possible intendedOccupancy values:

- OWNER_OCCUPIER
- INVESTMENT_FROM_SETTLEMENT
- DEVELOPMENT_FOR_PROFIT
- TEMPORARY_OWNER_OCCUPIER
- UNKNOWN

`intendedOccupancy` belongs here rather than permanently in ClientProfile.

`propertyId` remains a convenience field for a resolved `SPECIFIC_PROPERTY` target. New flows should use `acquisitionTarget` so complex/unit scenarios do not have to pretend a single PropertyRef already exists.

## 11. Profile completeness

Recommended semantic states:

- MINIMUM
- FINANCING_READY
- ASSISTANCE_READY
- DEVELOPMENT_READY

Do not block general property/market analysis merely because optional financing or assistance fields are absent.

## 12. AnalysisContext

Each material report should carry a lightweight snapshot of the context used to produce it.

Recommended fields:

```text
analysisId
generatedAt

clientProfileId
clientProfileVersion
financialSnapshotId
financialSnapshotVersion
acquisitionContextId

sourceRegistryVersion
policyRegistryVersion
assumptionSetRefs[]
policySnapshotRefs[]
propertyObservationRefs[]
skillVersions[]
modelVersion
```

Historical report snapshots must not silently change when the user's current profile later changes.

## 13. EvidenceItem

```text
evidenceId
classification
state
claim
value
unit
sourceName
sourceType
sourceReference
observedAt
effectiveFrom
effectiveTo
retrievedAt
confidence
notes
```

Every material evidence item should have both `classification` and `state`.

## 14. PropertyRef

```text
propertyId
normalizedAddress
sourcePropertyIds
latitude
longitude
parcelId
titleReference
identityConfidence
```

## 15. PropertyProfile

Material fields may be plain values when uncontroversial or MaterialAssertion values when provenance/conflict matters.

Recommended fields:

```text
propertyRef
propertyType
landArea
buildingArea
bedrooms
bathrooms
parking
yearBuilt
apparentCondition
attributes
currentListingState
planningSummary
marketSummary
```

## 16. ListingObservation

```text
observationId
propertyId
source
sourceListingId
sourceReference
observedAt
listingStatus
priceDisplay
priceMin
priceMax
agent
agency
auctionDate
inspectionTimes
descriptionHash
mediaHash
confidence
```

A ListingObservation records what a source reported. It does not by itself resolve the canonical property/listing assertion.

## 17. MarketAssessment

Recommended fields:

```text
marketBoundary
subjectPosition
comparableSales[]
comparableListings[]
marketObservations[]
rentalEvidence[]
liquiditySignals[]
supplyDemandSignals[]
materialConflicts[]
unknowns[]
confidence
```

MarketAssessment supplies evidence to AcquisitionPriceAssessment; it does not silently choose the final acquisition price.

## 18. AcquisitionPriceAssessment

Acquisition price must separate market evidence from strategy economics.

Recommended fields:

```text
assessmentPhase
askingPrice
marketValueRange
expectedAcquisitionRange
campaignSignals[]
comparableEvidenceIds[]
strategyMaximumPrices[]
gapAnalysis[]
assumptions[]
unknowns[]
confidence
```

Supported phases:

- MARKET
- FINAL

### MarketValueRange

Broad evidence-backed market range.

This is not a certified valuation.

### ExpectedAcquisitionRange

Estimated transaction range under the current sale campaign / current market evidence.

May consider:

- asking / guide;
- auction/private treaty;
- listing status;
- days on market;
- price changes;
- current competing listings;
- recent comparable sales;
- market liquidity.

### StrategyMaximumPrice

```text
StrategyMaximumPrice
├── strategyType
├── maximumPrice
├── targetMetric
├── targetValue
├── derivedFromModel
├── assumptions
└── confidence
```

This answers:

> What is the highest acquisition price this strategy can support under the stated target/assumptions?

It is not the same as market value or expected transaction price.

### GapAnalysis

Compare strategy maximum price against expected acquisition range.

Example:

```text
expected acquisition: $1.15m–$1.18m
income strategy maximum: $1.03m

gap status: MARKET_ABOVE_STRATEGY_LIMIT
```

Possible gap states:

- WITHIN_STRATEGY_LIMIT
- PARTIALLY_OVERLAPPING
- MARKET_ABOVE_STRATEGY_LIMIT
- STRATEGY_LIMIT_UNKNOWN

### Two-pass rule

Avoid a circular dependency.

#### MARKET pass

Before strategy modelling, determine where possible:

- askingPrice;
- marketValueRange;
- expectedAcquisitionRange;
- campaignSignals.

`strategyMaximumPrices` may be empty.

#### FINAL pass

After strategy models produce break-even / target-return price limits:

- populate strategyMaximumPrices;
- calculate gapAnalysis;
- finalize acquisition-price decision support.

Do not pretend StrategyMaximumPrice is known before strategy economics are run.

## 19. PurchaseAssistanceAssessment

Purchase assistance consumes:

- PurchaseEligibilityFacts;
- FinancialSnapshot where relevant;
- AcquisitionContext;
- property context;
- current policy.

It must not create a second overlapping client profile.

Recommended output:

```text
policySnapshot[]
eligibilityByProgram[]
financingScenarios[]
stampDutyTreatment
grantTreatment
sharedEquityTreatment
minimumCashRequirement
lenderLoanAmount
effectiveLvr
governmentGuaranteeAmount
governmentEquityAmount
lmiTreatment
blockingUnknowns
verificationRequired
confidence
```

Assistance eligibility states:

- ELIGIBLE
- POTENTIALLY_ELIGIBLE
- INELIGIBLE
- NOT_APPLICABLE
- UNKNOWN

## 20. AssetUtilityAssessment

```text
buildingUtility
rentalUtility
landUtility
developmentUtility
buildingUtilityEvidence
rentalUtilityEvidence
landUtilityEvidence
developmentUtilityEvidence
materialUnknowns
```

Utility levels:

- LOW
- MEDIUM
- HIGH
- UNKNOWN

Property age may influence buildingUtility but must not determine strategy by itself.

## 21. StrategyCandidate

```text
strategyType
eligibility
rationale
requiredEvidence
blockingUnknowns
assumptions
modelReference
confidence
```

Strategy types:

- INCOME_INVESTMENT
- REPLACEMENT_DEVELOPMENT
- SUBDIVISION_DEVELOPMENT

Eligibility:

- ELIGIBLE
- ELIGIBLE_WITH_CONSTRAINTS
- INSUFFICIENT_EVIDENCE
- NOT_ECONOMICALLY_SUPPORTED
- NOT_APPLICABLE

## 22. IncomeInvestmentResult

Recommended fields:

```text
modelAcquisitionPrice
financingScenario
deposit
acquisitionCosts
grantAmount
stampDutyRelief
initialCashRequired
lenderLoanAmount
governmentGuaranteeAmount
governmentEquityAmount
effectiveLvr
initialRent
annualProjection[]
exitAssumptions
leveragedIrr
breakEvenMetrics
strategyMaximumPrice
returnBasis
taxTreatment
sensitivity
```

`modelAcquisitionPrice` is the price used for a scenario, not a claim that the property will transact at that price.

## 23. ReplacementDevelopmentResult

```text
modelAcquisitionPrice
effectiveLandCost
demolitionCost
buildCost
softCosts
developmentCashFlows[]
financeSummary
contingency
totalDevelopmentCost
finishedValue
profit
profitMargin
unleveredProjectIrr
leveredEquityIrr
breakEvenAcquisitionPrice
strategyMaximumPrice
returnBasis
taxTreatment
duration
sensitivity
```

## 24. SubdivisionDevelopmentResult

```text
modelAcquisitionPrice
proposedDwellingCount
siteYield
demolitionCost
subdivisionCost
civilAndServiceCosts
buildCost
softCosts
developmentCashFlows[]
financeSummary
contingency
totalDevelopmentCost
perDwellingGrv
totalGrv
profit
profitMargin
unleveredProjectIrr
leveredEquityIrr
residualLandValue
breakEvenAcquisitionPrice
strategyMaximumPrice
returnBasis
taxTreatment
duration
planningConfidence
sensitivity
```

## 25. StrategyComparison

```text
strategies[]
capitalRequired
duration
liquidityProfile
returnMetrics
riskProfile
keyAssumptions
blockingUnknowns
acquisitionPriceGapSummary
returnBasisCompatibility
taxBasisWarnings[]
decisionSummary
nextVerificationSteps
```

Do not collapse all strategies into one arbitrary score.

## 26. Confidence

Confidence describes evidence quality / applicability.

It does not replace EvidenceState.

- HIGH: authoritative/current/directly applicable.
- MEDIUM: credible but limited or indirect.
- LOW: incomplete or materially inferential.

A CONFLICTED assertion may still have HIGH confidence that a conflict exists.


## 27. Versioned AssumptionSet

Assumptions are explicit model inputs, not facts.

The current Console-demo phase uses maintainer-managed static sets under:

`Console/Assumptions/`

### AssumptionValue

```text
AssumptionValue<T>
├── key
├── value
├── unit
├── origin
├── requiredInput
├── sourceReference
├── sensitivity
└── notes
```

Supported origins:

- DEFAULT_ASSUMPTION
- USER_ASSUMPTION
- CLIENT_ORG_ASSUMPTION
- SOURCE_DERIVED_ASSUMPTION

Changing origin does not change the statement class: an assumption remains ASSUMPTION unless separately established as FACT by evidence.

### AssumptionSet

```text
assumptionSetId
version
jurisdiction
strategyType
modelType
status
effectiveFrom
maintainedAt
assumptions{}
notes[]
```

Exactly one of `strategyType` or `modelType` should identify the primary model scope. Strategy-specific sets use `strategyType`; non-strategy models such as owner-occupier acquisition may use `modelType`.

Base AssumptionSets are immutable once used in a report.

If a maintained default changes materially, create a new version rather than rewriting the old version.

### AssumptionOverride

```text
key
value
unit
origin
sourceReference
reason
appliedAt
```

Recommended input precedence:

```text
USER_ASSUMPTION
        ↓
CLIENT_ORG_ASSUMPTION
        ↓
SOURCE_DERIVED_ASSUMPTION
        ↓
DEFAULT_ASSUMPTION
```

This precedence selects the model input. It is not a source-authority hierarchy.

### EffectiveAssumptionSet

A model run should retain:

```text
baseAssumptionSetId
baseAssumptionSetVersion
appliedOverrides[]
effectiveValues{}
generatedAt
```

The base set must remain unchanged.

Example:

```text
Base mortgage rate: 6.00% DEFAULT_ASSUMPTION
User lender quote:   5.72% USER_ASSUMPTION
Effective input:     5.72%
```

The effective input is still an ASSUMPTION unless the underlying evidence is separately classified as FACT.

### Required-input rule

Some inputs should deliberately have no generic default.

Examples may include:

- current borrower mortgage rate;
- project-specific construction cost;
- demolition/remediation cost;
- project duration;
- proposed subdivision dwelling count;
- end-value/GRV where no suitable market evidence exists.

When `requiredInput = true` and no explicit/source-derived value exists:

- do not invent one;
- return the input as missing;
- ask the user only if it materially blocks the current analysis; or
- run clearly-labelled scenario assumptions where useful.

### Sensitivity rule

A default is not a prediction.

Material assumptions should carry sensitivity ranges or scenario guidance where practical, especially for:

- interest rate;
- vacancy;
- rent growth;
- capital growth;
- build cost;
- GRV;
- project duration.

Reports should preserve both the base set version and applied overrides.

When multiple strategy models run, AnalysisContext should carry one AssumptionSetRef per effective set used.


## 28. ReturnBasis and TaxTreatment

Every material return/profit result must state its tax basis.

### ReturnBasis

Supported values:

- PRE_TAX
- AFTER_TAX_ESTIMATE

PRE_TAX is the default unless an explicit tax model is intentionally applied.

AFTER_TAX_ESTIMATE may only be used when the included tax components, assumptions and material exclusions are explicitly identified.

### TaxModelStatus

Supported values:

- NOT_MODELLED
- PARTIALLY_MODELLED
- MODELLED_ESTIMATE

### TaxComponentStatus

Supported values:

- INCLUDED
- EXCLUDED
- UNKNOWN
- NOT_APPLICABLE

### TaxTreatment

Recommended fields:

```text
returnBasis
taxModelStatus
components[]
materialAssumptions[]
materialUnknowns[]
adviceBoundary
```

Each component may include:

```text
taxType
status
amount
calculationReference
assumptions[]
notes
```

Possible taxType values may include:

- STAMP_DUTY
- LAND_TAX
- GST
- GST_MARGIN_SCHEME
- INCOME_TAX
- CAPITAL_GAINS_TAX
- DEPRECIATION
- CAPITAL_WORKS_DEDUCTION
- OTHER

The presence of one included tax component does not automatically make the entire model AFTER_TAX_ESTIMATE.

Example:

> stamp duty is included in acquisition cost, but personal income tax and CGT are not modelled.

This remains PRE_TAX.

### IncomeInvestmentResult addition

IncomeInvestmentResult should include:

```text
returnBasis
taxTreatment
```

Default:

```text
returnBasis = PRE_TAX
taxModelStatus = NOT_MODELLED
```

Do not silently assume negative gearing, marginal tax rate, CGT discount, depreciation or land-tax benefits.

### ReplacementDevelopmentResult addition

ReplacementDevelopmentResult should include:

```text
returnBasis
taxTreatment
```

Default development profit/margin/IRR is PRE_TAX.

Unless explicitly modelled, GST, margin scheme and entity/income-tax treatment must remain visible as UNKNOWN or EXCLUDED according to the scenario.

### SubdivisionDevelopmentResult addition

SubdivisionDevelopmentResult should include:

```text
returnBasis
taxTreatment
```

Default development profit/margin/IRR is PRE_TAX.

Do not describe project profit as after-tax proceeds unless a defined tax model supports that statement.

### StrategyComparison tax-basis rule

StrategyComparison should include:

```text
returnBasisCompatibility
taxBasisWarnings[]
```

Do not directly rank return metrics across incompatible tax bases.

Examples:

- PRE_TAX vs PRE_TAX → comparable on tax basis;
- AFTER_TAX_ESTIMATE vs AFTER_TAX_ESTIMATE with compatible assumptions → potentially comparable;
- PRE_TAX vs AFTER_TAX_ESTIMATE → not directly comparable on return metrics.

Other dimensions such as capital required, duration, planning risk and complexity may still be compared.

### Advice boundary

TaxTreatment exists to state modelling scope, not to provide tax advice.

If tax treatment materially changes the decision and is not adequately modelled, add professional tax/accounting verification to next steps.


## 29. DevelopmentCashFlow

Development finance must support time-based cash flows.

An aggregate `financeAndHolding` number may be shown as a summary, but it must not be the sole finance representation when unlevered project IRR, levered equity IRR, peak debt or peak equity are calculated.

### DevelopmentCashFlow

```text
cashFlowId
scenarioId
period
date
phase
category
description

cashIn
cashOut

debtDraw
debtRepayment
interest
equityContribution

classification
assumptionReference
evidenceReference
notes
```

At least one of `period` or `date` should be present.

Recommended default period granularity:

- MONTHLY

Use actual dates when sufficiently reliable dates are available.

### DevelopmentPhase

Suggested values:

- SETTLEMENT
- PRE_APPROVAL_HOLD
- PLANNING_APPROVAL
- DEMOLITION
- SUBDIVISION_AND_CIVIL
- DESIGN_AND_APPROVAL
- CONSTRUCTION
- MARKETING
- SETTLEMENT_OF_SALES
- HOLD_AFTER_COMPLETION
- OTHER

### DevelopmentCashFlowCategory

Suggested values:

- ACQUISITION
- STAMP_DUTY_AND_TRANSACTION
- DEMOLITION
- REMEDIATION
- CONSULTANTS
- PLANNING_AND_APPROVALS
- SUBDIVISION
- CIVIL_AND_SERVICES
- CONSTRUCTION
- CONTINGENCY
- RATES_AND_UTILITIES
- INSURANCE
- LAND_TAX
- RENTAL_INCOME
- OTHER_HOLDING_COST
- MARKETING_AND_SELLING
- SALE_PROCEEDS
- TAX_COMPONENT
- OTHER

### DevelopmentFinanceAssumptions

```text
periodGranularity
financeRate
interestCalculationMethod
interestTreatment
debtFacilityLimit
acquisitionDebtAssumption
constructionDebtAssumption
equityContributionRule
drawdownRule
repaymentRule
notes
```

Do not imply that modelled debt is lender-approved.

### InterestTreatment

Supported semantic values:

- PAID_CURRENTLY
- CAPITALISED
- MIXED
- UNKNOWN

### DevelopmentFinanceSummary

```text
totalProjectCost
totalHoldingCost
totalFinanceInterest
peakDebt
peakEquityAtRisk
totalEquityContributed
totalSaleProceeds
projectProfit
projectMargin
unleveredProjectIrr
leveredEquityIrr
duration
```

### IRR basis

Development return metrics must distinguish:

```text
unleveredProjectIrr
leveredEquityIrr
```

`unleveredProjectIrr` is calculated from project operating/development cash flows before financing flows.

`leveredEquityIrr` is calculated from equity cash flows after debt draw, interest and repayment effects.

If financing structure is unknown, leveredEquityIrr must be UNKNOWN rather than inferred.

The model must preserve the timing/period convention used.

Do not substitute simple profit/cost ratios for IRR.

### ReplacementDevelopmentResult update

Replace reliance on aggregate `financeAndHolding` with:

```text
developmentCashFlows[]
financeSummary
```

An aggregate finance/holding summary may remain for display, but the timed series is the source for IRR/peak-debt/peak-equity calculations.

### SubdivisionDevelopmentResult update

Replace reliance on aggregate `financeAndHolding` with:

```text
developmentCashFlows[]
financeSummary
```

For multi-sale scenarios, individual sale proceeds may occur in different periods.

### Timing assumptions

Project timing is frequently an ASSUMPTION.

Planning duration, construction duration, sale timing and staged build-cost timing must retain their assumption origin unless supported by direct evidence.

Do not fabricate exact dates merely to create a timeline.


## 30. OwnerOccupierAcquisitionResult

Owner-occupier acquisition is an acquisition/financing path, not a fourth investment strategy.

It must not be represented as:

```text
StrategyCandidate(strategyType = OWNER_OCCUPIER)
```

### FundingSupportedPriceCeiling

```text
FundingSupportedPriceCeiling
├── maximumPrice
├── status
├── availableCashUsed
├── lenderFundingUsed
├── governmentEquityUsed
├── grantUsed
├── acquisitionCostAllowance
├── policyOrSchemeCaps[]
├── assumptions[]
├── verificationRequired[]
└── notes
```

Supported status values:

- CONFIRMED_INPUTS
- USER_DECLARED_INPUTS
- PARTIAL_INPUTS
- UNKNOWN

This is the maximum purchase price supported by the currently known/modelled funding inputs.

It is not:

- MarketValueRange;
- ExpectedAcquisitionRange;
- StrategyMaximumPrice;
- lender approval;
- a regulated statement that the client can afford the property.

A government guarantee must not be counted as cash or equity.

### OwnerOccupierFundingGap

Compare:

```text
ExpectedAcquisitionRange
vs
FundingSupportedPriceCeiling
```

Supported states:

- WITHIN_KNOWN_FUNDING
- PARTIALLY_OVERLAPPING
- ABOVE_KNOWN_FUNDING
- FUNDING_CEILING_UNKNOWN

### RepaymentScenario

```text
scenarioName
loanAmount
interestRate
loanTermYears
repaymentFrequency
principalAndInterestPayment
interestOnlyPayment
classification
assumptions[]
notes
```

Do not imply lender serviceability approval from a repayment scenario.

### OwnershipCostSummary

```text
mortgageRepayment
councilRates
water
insurance
strataOrBodyCorporate
landTax
maintenanceAllowance
otherOwnershipCosts[]
totalPeriodicCashOutflow
period
```

Principal repayment should remain distinguishable from economic expense when a detailed breakdown is shown.

### OwnerOccupierAcquisitionResult

```text
modelAcquisitionPrice
expectedAcquisitionRange
financingScenario

buyerCashContribution
lenderLoanAmount
governmentGuaranteeAmount
governmentEquityAmount
grantAmount

stampDutyTreatment
acquisitionCosts
initialCashRequired
effectiveLvr

fundingSupportedPriceCeiling
fundingCeilingStatus
fundingGapStatus

repaymentScenarios[]
ownershipCostSummary
cashBufferAfterSettlement

assistanceSummary
blockingUnknowns[]
verificationRequired[]
warnings[]
confidence
```

Do not include investment-return metrics such as:

- investment IRR;
- cash-on-cash return;
- rental yield;

unless a separate investment analysis is explicitly requested.

### Orchestration rule

For a pure owner-occupier acquisition request:

```text
Client Context
→ Property Research
→ Market Analysis
→ Acquisition Price Assessment [MARKET]
→ Purchase Assistance Assessment when relevant
→ Due Diligence as required
→ Owner-Occupier Acquisition
→ Owner-occupier decision support
```

The FINAL strategy-price pass is not required unless investment/development strategy models are also run.

### Advice boundary

OwnerOccupierAcquisitionResult is scenario modelling only.

It must not claim:

- lender approval;
- formal serviceability;
- regulated credit advice;
- financial advice;
- certified valuation.


## 31. PurchaseAssistanceRegistry

The Console-demo phase uses a static registry under:

`Console/Policies/purchase-assistance-registry.yaml`

The registry defines which programs Iris should know exist, how they are discovered and where current rules must be verified.

It does not store permanent client eligibility conclusions.

### PurchaseAssistanceProgramDefinition

```text
programId
name
jurisdiction
programType
secondaryProgramType
status
discoveryMode
sensitiveEligibility
verificationPolicy
authoritativeSourceIds[]
applicability
discoveryTriggers[]
currentSnapshot
materialRulesToVerify[]
notes[]
```

### ProgramType

Suggested values:

- GOVERNMENT_GUARANTEE
- SHARED_EQUITY
- CASH_GRANT
- STAMP_DUTY_RELIEF
- PUBLIC_LENDER_PRODUCT
- EX_GRATIA_RELIEF

A program's type controls how it affects financing.

Examples:

- GOVERNMENT_GUARANTEE is not cash;
- SHARED_EQUITY is not a grant;
- CASH_GRANT is not lender debt;
- STAMP_DUTY_RELIEF reduces transaction cost rather than purchase price.

### ProgramStatus

Suggested values:

- ACTIVE
- SUSPENDED
- CLOSED_TO_NEW_APPLICATIONS
- SUPERSEDED
- RETIRED

Do not evaluate a non-active program as currently available without explicit current evidence.

### DiscoveryMode

Supported values:

- AUTO_DISCOVER
- CONDITIONAL_DISCOVER
- EXPLICIT_DISCLOSURE_OR_REQUEST

#### AUTO_DISCOVER

The Console may consider the program from ordinary available client/property facts.

#### CONDITIONAL_DISCOVER

The Console should only consider the program when its non-sensitive trigger is already known.

Do not collect extra client facts merely to discover every possible niche program.

#### EXPLICIT_DISCLOSURE_OR_REQUEST

The Console must not proactively ask for the triggering sensitive circumstance.

Use only when the user explicitly discloses the relevant fact or asks about the program.

### Sensitive eligibility

If:

```text
sensitiveEligibility = true
```

the Console must apply data minimisation.

Do not turn a potentially beneficial policy into a speculative sensitive onboarding question.

### VerificationPolicy

Typical value:

```text
VERIFY_AT_EXECUTION
```

A static `currentSnapshot` may support demo routing and provisional scenarios, but material values must be checked against the authoritative current source before being used as current FACT in a live assessment.

Material values may include:

- deposit minimum;
- grant amount;
- income threshold;
- shared-equity percentage;
- property price cap;
- residence requirement;
- property-type eligibility;
- participating-lender requirement;
- effective/contract dates.

### PurchaseAssistanceProgramEvaluation

Recommended fields:

```text
programId
programRegistryVersion
status
eligibilityState
applicableBenefitTypes[]
verifiedRules[]
assumedRules[]
blockingUnknowns[]
authoritativeEvidenceIds[]
verificationRequired[]
notes[]
```

EligibilityState remains:

- ELIGIBLE
- POTENTIALLY_ELIGIBLE
- INELIGIBLE
- NOT_APPLICABLE
- UNKNOWN

### Registry / client separation

Never store:

```text
ClientProfile.eligibleForProgramX = true
```

as a stable client fact.

Eligibility is computed from:

```text
PurchaseAssistanceProgramDefinition
+
current authoritative policy
+
PurchaseEligibilityFacts
+
FinancialSnapshot
+
AcquisitionContext
+
Property context
```

### AnalysisContext

Material purchase-assistance analyses should preserve:

- policyRegistryVersion;
- evaluated program IDs;
- PolicySnapshot references;
- authoritative evidence references where applicable.

This allows a historical report to identify which program catalogue/policy snapshot was used.


## 32. CanonicalDemoReport

The current Console phase has no custom persistence backend.

Therefore a report must preserve both:

- AnalysisContext identifiers/versions;
- the minimum normalized snapshot payload needed for historical interpretation/replay.

IDs alone are not sufficient if their underlying data only existed in conversation state.

### ReportStatus

Supported values:

- COMPLETE
- PARTIAL
- BLOCKED

Do not use vague completion states such as "mostly complete".

### CanonicalDemoReport

Recommended structure:

```text
reportId
reportSchemaVersion
status
branch
generatedAt
title

decisionSummary
subjectProperty
clientContext
evidenceSummary
acquisitionPrice

ownerOccupierResult
investmentDevelopment

financeAndTax
assumptions

reproducibilityBundle
disclaimers
```

### ReproducibilityBundle

Recommended fields:

```text
analysisContext
embeddedSnapshots
```

The embedded snapshot set should contain the minimum necessary normalized data used by the report:

```text
clientProfile
financialSnapshot
acquisitionContext
effectiveAssumptionSets[]
policySnapshots[]
propertyObservations[]
```

Do not embed unlimited raw third-party material.

Preserve only normalized/permitted observations required for interpretation or replay.

### Demo-stage reproducibility rule

A report is reproducible enough for the Console-demo phase when a future reviewer can identify:

- which client/profile state was used;
- which acquisition intent was used;
- which source registry version was used;
- which policy registry version was used;
- which effective assumptions were used;
- which material evidence observations were used;
- which PolicySnapshots were used;
- which Skill/model versions produced the result.

Historical reports must not rely solely on mutable current chat state.

### HtmlReportArtifact

`HtmlReportArtifact` is a derived presentation result, not part of the canonical analytical payload.

Recommended fields:

```text
reportId
presentationOf
format
status
path
renderer
rendererVersion
generatedAt
canonicalReportReference
draftReference
error
```

Supported presentation statuses:

- RENDERED
- UNAVAILABLE
- FAILED

The artifact must identify the canonical `reportId` through `presentationOf` and retain a reference to the canonical YAML/JSON source.

HTML rendering must not change `ReportStatus`, calculations, assumptions, evidence state, ReturnBasis or TaxTreatment. If rendering fails, return the canonical artifact and a concise Markdown view with a visible error.

## 33. FixtureValidationResult

Regression fixture execution state is separate from fixture definition state.

### FixtureExecutionMode

Supported values:

- REGRESSION_FROZEN
- LIVE_DEMO_VALIDATION

#### REGRESSION_FROZEN

Uses normalized fixture evidence without refreshing the live property.

Purpose:

- deterministic semantic regression.

#### LIVE_DEMO_VALIDATION

Uses current approved sources/tools and current registry rules.

Purpose:

- validate current real-world Console execution.

Do not mix these modes in one run.

### FixtureValidationStatus

Supported values:

- NOT_RUN
- PASS
- FAIL
- BLOCKED

A fixture being READY_FOR_EXECUTION does not mean PASS.

### FixtureValidationResult

Recommended fields:

```text
runId
executionMode
startedAt
completedAt
sourceCommitSha

fixtureId
fixturePath
fixtureSchemaVersion

status

expectedSkillPath[]
actualSkillPath[]
missingExpectedSteps[]
unexpectedMaterialSteps[]

assertionResults[]
prohibitedOutcomeResults[]

structuredOutput
canonicalReport

errors[]
notes[]
```

### AssertionResult

```text
path
operator
expected
actual
passed
notes
```

Assertions evaluate structured semantic output, not prose wording.

### ProhibitedOutcomeResult

```text
outcomeId
occurred
evidence
```

Any prohibited outcome occurrence causes FAIL.

### BLOCKED rule

Use BLOCKED when execution itself cannot proceed because of an invalid fixture/schema or unavailable required execution capability.

Do not use BLOCKED merely because the fixture contains UNKNOWN evidence.

UNKNOWN may be the correct semantic result being tested.


## 34. PropertyComplex and AcquisitionTarget

A human-readable street address does not always identify one independently transactable property.

Examples include:

- unit/apartment complexes;
- townhouse groups;
- retirement villages;
- community-title groups;
- commercial/industrial complexes.

Do not force:

```text
Address = one PropertyRef
```

### PropertyEntityType

Supported values:

- SINGLE_PROPERTY
- PROPERTY_COMPLEX
- UNRESOLVED

A base address may resolve with HIGH confidence to `PROPERTY_COMPLEX` even when the specific unit/lot is not yet known.

That is not an identity failure.

### PropertyComplex

```text
complexId
normalizedAddress
sourceComplexIds{}
propertyCount
propertyRefs[]
sharedSiteAttributes
sharedPlanningContext
titleStructure
identityConfidence
evidenceIds[]
notes[]
```

`propertyRefs[]` may contain partial unit references where source evidence supports them.

Do not infer legal title structure from map appearance, mailboxes or building form.

If not formally verified:

```text
titleStructure = UNKNOWN
```

### PropertyRef update

A PropertyRef may additionally retain:

```text
complexId
unitIdentifier
lotIdentifier
```

where known.

A PropertyRef represents one independently analysed property/unit/lot, not the entire complex unless the entire complex is itself the legal acquisition subject.

### AcquisitionTarget

```text
targetType
complexId
propertyId
candidatePropertyIds[]
selectionState
selectionEvidenceIds[]
notes[]
```

Supported `targetType` values:

- SPECIFIC_PROPERTY
- ANY_UNIT_IN_COMPLEX
- UNKNOWN_UNIT_IN_COMPLEX
- COMPLEX_AS_WHOLE

### AcquisitionTarget.selectionState

Supported values:

- RESOLVED
- PARTIALLY_RESOLVED
- OPEN_SET
- UNKNOWN

Examples:

#### Specific known unit

```text
targetType = SPECIFIC_PROPERTY
propertyId = unit-7
selectionState = RESOLVED
```

#### Known complex, unknown selling unit

```text
targetType = UNKNOWN_UNIT_IN_COMPLEX
complexId = complex-3-grandview
propertyId = null
selectionState = PARTIALLY_RESOLVED
```

#### User wants any suitable unit in the complex

```text
targetType = ANY_UNIT_IN_COMPLEX
complexId = complex-3-grandview
propertyId = null
selectionState = OPEN_SET
```

### Complex-level facts vs unit facts

Keep separate:

- ComplexFact;
- UnitFact;
- SharedFact.

Examples:

ComplexFact:

- property count;
- common address;
- common driveway/access;
- shared site context.

UnitFact:

- unit bedrooms;
- internal area;
- parking;
- unit-specific sale/rent history;
- unit-specific title reference.

SharedFact:

- suburb/location context;
- planning zone where genuinely common;
- nearby amenity context.

Do not promote one unit's attributes to the whole complex.

### ComplexProfile

```text
complexRef
knownProperties[]
unitArchetypes[]
sharedFacts[]
unitFactSummaries[]
currentListings[]
historicalUnitObservations[]
materialUnknowns[]
confidence
```

A ComplexProfile describes the group without pretending all units are identical.

### Complex-level analysis

When `targetType` is `ANY_UNIT_IN_COMPLEX` or `UNKNOWN_UNIT_IN_COMPLEX`, Iris may continue with a complex-level analysis rather than stopping.

It may produce:

- ComplexProfile;
- unit archetypes;
- unit-level evidence distribution;
- historical/current unit observations;
- broad acquisition/rent ranges by archetype;
- candidate-unit constraints;
- material unknowns.

It must not produce a property-specific MarketValueRange, ExpectedAcquisitionRange or strategy model for an unidentified unit.

### ComplexAcquisitionProfile

Recommended fields:

```text
complexRef
targetType
unitArchetypes[]
observedUnitSales[]
observedUnitRentals[]
candidatePropertyIds[]
preferredUnitCharacteristics[]
archetypeAcquisitionRanges[]
archetypeRentalRanges[]
materialUnknowns[]
verificationRequired[]
confidence
```

This supports questions such as:

> I want to buy any suitable unit in this complex if one becomes available.

without inventing which unit is for sale.

### COMPLEX_AS_WHOLE

Use `COMPLEX_AS_WHOLE` only when the user intends to acquire/analyse the whole complex as one acquisition subject.

Do not assume all units are jointly saleable merely because they share one street address.

Formal ownership/title evidence may be required.

### Orchestration rule

```text
Address
→ Property Research
→ PropertyEntityType

SINGLE_PROPERTY
→ normal property workflow

PROPERTY_COMPLEX + SPECIFIC_PROPERTY resolved
→ normal property workflow for the selected unit

PROPERTY_COMPLEX + ANY_UNIT_IN_COMPLEX
→ complex-level market/acquisition profile

PROPERTY_COMPLEX + UNKNOWN_UNIT_IN_COMPLEX
→ complex-level market/acquisition profile
→ progressively narrow candidates as new unit facts arrive

PROPERTY_COMPLEX + COMPLEX_AS_WHOLE
→ verify whole-complex acquisition subject before whole-complex modelling

UNRESOLVED
→ request the minimum identifier needed to continue
```

The existence of a PropertyComplex must not be treated as an error merely because a specific unit is not yet selected.
