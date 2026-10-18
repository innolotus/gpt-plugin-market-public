# Iris Console Return Basis and Tax Treatment

This directory documents the tax-boundary semantics used by Iris Console.

Iris Console is not a tax-advice product in the current demo phase.

The purpose of these rules is simpler:

> every return/profit metric must say what tax basis it represents.

## ReturnBasis

Supported values:

- `PRE_TAX`
- `AFTER_TAX_ESTIMATE`

### PRE_TAX

The metric is calculated before personal/entity income tax and other taxes not explicitly included in the model.

This is the default basis for Iris Console unless a documented tax model is intentionally applied.

### AFTER_TAX_ESTIMATE

The metric includes an explicit estimate of relevant tax effects.

This label may only be used when:

- the included tax components are identified;
- the assumptions are explicit;
- the user's/entity structure required by the estimate is known or explicitly assumed;
- material excluded/unknown tax components remain disclosed.

Do not use `AFTER_TAX_ESTIMATE` merely because one tax component happened to be included.

## TaxModelStatus

Supported values:

- `NOT_MODELLED`
- `PARTIALLY_MODELLED`
- `MODELLED_ESTIMATE`

### NOT_MODELLED

No meaningful tax model has been applied.

Default ReturnBasis should normally be PRE_TAX.

### PARTIALLY_MODELLED

One or more tax components are included, but the result is not a complete after-tax estimate.

ReturnBasis remains PRE_TAX unless the model explicitly satisfies the AFTER_TAX_ESTIMATE requirements.

### MODELLED_ESTIMATE

A defined tax model has been applied sufficiently to present an AFTER_TAX_ESTIMATE.

This still does not make the output tax advice.

## Tax components

A TaxTreatment may describe components such as:

- stamp duty / transaction duty;
- land tax;
- GST;
- GST margin scheme;
- income tax;
- capital gains tax;
- depreciation / capital works deductions;
- other project/entity-specific tax effects.

Stamp duty can be included in acquisition cost while the overall return still remains PRE_TAX.

That distinction matters.

## Component status

Each material tax component should be one of:

- `INCLUDED`
- `EXCLUDED`
- `UNKNOWN`
- `NOT_APPLICABLE`

If applicability itself is uncertain, use UNKNOWN rather than quietly choosing EXCLUDED.

## Development rule

Development profit is PRE_TAX by default.

Unless explicitly modelled, state:

- GST treatment = UNKNOWN or EXCLUDED as appropriate to the scenario;
- margin scheme = UNKNOWN unless established;
- income tax/entity treatment = UNKNOWN;
- project profit is not an after-tax profit.

Do not present a raw feasibility profit as money available to the developer after tax.

## Income-investment rule

Income Investment is PRE_TAX by default.

Rental cash flow, leveraged IRR and exit proceeds must not silently assume:

- negative gearing benefit;
- personal marginal tax rate;
- CGT discount;
- depreciation benefit;
- land-tax treatment;

unless an explicit model includes them.

## Strategy comparison rule

Do not directly rank strategies on return metrics with different ReturnBasis values.

Preferred behaviour:

1. compare PRE_TAX with PRE_TAX; or
2. compare AFTER_TAX_ESTIMATE with AFTER_TAX_ESTIMATE using compatible tax assumptions; or
3. state that tax-basis mismatch prevents direct return comparison.

Capital, duration, planning risk and other non-tax dimensions may still be compared.

## Advice boundary

Tax-related outputs are scenario estimates only.

When tax materially changes the decision, the report should identify professional tax/accounting review as a verification step rather than manufacturing certainty.
