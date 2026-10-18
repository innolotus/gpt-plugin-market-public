# Iris Console Evidence Semantics

## Why EvidenceState exists

Confidence alone is not enough.

Examples:

- two current approved sources disagree;
- a sale record is old but historically valid;
- an agent states a land size that has not been checked against formal records;
- the required fact cannot be obtained.

Those situations require different handling even if all might otherwise be described as "low confidence".

## EvidenceState

### CONFIRMED

The assertion is supported by the appropriate current source set and has no unresolved material conflict.

### CONFLICTED

Approved/current evidence materially disagrees.

Do not silently pick one value.

Report the competing values and identify what evidence could resolve the conflict.

### STALE

The evidence is outside the freshness requirement for the current use.

A stale observation may still be historically correct.

Do not use a stale current-listing status as if it were current.

### UNVERIFIED

A claim exists but authoritative/independent confirmation is missing where verification matters.

Examples:

- agent-stated site area not checked against title/cadastral source;
- marketing claim of development potential;
- user-provided estimate without supporting document.

### UNKNOWN

The fact cannot currently be established.

UNKNOWN is not FALSE and is not "no issue".

## Precedence behaviour

EvidenceState is not a global ranking system.

Use the FactType authority rules in `Console/Sources/source-authority.yaml`.

Examples:

- an agent statement does not override PlanSA on statutory planning rules;
- Domain and REA disagreement on live listing status should remain CONFLICTED until freshness/primary evidence resolves it;
- a current formal title can resolve a secondary-source title discrepancy.

## Calculation rule

Do not feed a material CONFLICTED, STALE, UNVERIFIED or UNKNOWN value into a deterministic model as though it were CONFIRMED.

If modelling is still useful:

1. make the selected value an explicit ASSUMPTION;
2. preserve the unresolved evidence state;
3. run sensitivity/scenarios where material;
4. identify the decision impact.
