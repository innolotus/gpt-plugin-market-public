# Iris Console Strategy Model

## 1. Purpose

This document defines the property-investment strategy model used by Iris Console.

A property is an asset with multiple possible future states, and the appropriate analysis depends on both asset evidence and client context.

## 2. Owner occupation is not a strategy archetype

Owner occupation describes acquisition/use intent.

It should not be added to the strategy list beside:

- Income Investment;
- Replacement Development;
- Subdivision Development.

For a pure owner-occupier request, use `owner-occupier-acquisition` and do not run Strategy Comparison by default.

A client may separately ask:

> If I buy this to live in now, what future investment/development optionality does it have?

That is a second analytical branch, not proof that owner occupation itself is an investment strategy.

## 3. Client context before strategy

Strategy selection consumes:

### ClientProfile

Relatively stable preferences such as investor type, objective, horizon, risk tolerance, development capability and target return.

### FinancialSnapshot

Time-sensitive funding information such as available cash, deposit and lender pre-approval.

### AcquisitionContext

Intent for the specific property:

- owner occupy;
- investment from settlement;
- development for profit;
- target purchase price;
- desired strategy where supplied.

Do not infer a permanent client trait from one AcquisitionContext.

## 4. Evidence before strategy

Strategy selection should not consume unresolved evidence as though it were confirmed.

Material assertions use EvidenceState:

- CONFIRMED
- CONFLICTED
- STALE
- UNVERIFIED
- UNKNOWN

If unresolved evidence must be used for scenario modelling, convert the selected scenario value to an explicit ASSUMPTION and preserve the original EvidenceState.

## 5. Acquisition price before and after strategy

Iris uses a two-pass acquisition-price model.

### MARKET pass

Answers:

- what broad market range is supported;
- what transaction range the current campaign may support.

It produces:

- MarketValueRange;
- ExpectedAcquisitionRange.

### FINAL pass

After strategy models answer:

- what price each strategy can support under explicit targets/assumptions.

It produces:

- StrategyMaximumPrice;
- gap against ExpectedAcquisitionRange.

Example:

```text
Expected acquisition: $1.15m–$1.18m
Subdivision maximum:  $1.07m

Result:
MARKET_ABOVE_STRATEGY_LIMIT
```

That result means the strategy economics do not support the current market expectation under stated assumptions. It does not mean the property is universally overvalued.

## 6. Progressive profiling

Do not require a fully completed profile before property research.

Examples:

- general market analysis may need only MINIMUM profile context;
- financing may require FINANCING_READY;
- assistance may require ASSISTANCE_READY;
- developer capital constraints may require DEVELOPMENT_READY.

## 7. Investor types

### Individual / non-professional investor

Typical objectives:

- rental income;
- manageable debt;
- long-term capital growth;
- equity accumulation;
- limited project complexity.

Default candidate:

- Income Investment.

### Professional investor / small developer

Typical objectives:

- active value creation;
- planning / land utility;
- project margin;
- IRR;
- capital recycling.

Default candidates:

- Replacement Development where building utility is low;
- Subdivision Development where land/planning utility is strong;
- temporary rent/hold where it improves project timing.

## 8. Asset utility model

### Building Utility

Consider habitability, condition, age, remaining economic life, near-term CapEx, layout and value destroyed by demolition.

Age alone never determines demolition.

### Rental Utility

Consider current/estimated rent, vacancy, operating cost, maintenance burden and holding-cost offset.

### Land Utility

Consider land area, frontage, shape, access, easements, slope, services and location.

### Development Utility

Consider planning capacity, subdivision potential, dwelling yield, precedents and planning/title/infrastructure constraints.

## 9. Strategy archetypes

### Income Investment

```text
Acquire → Rent → Hold → Debt reduction + rent growth + capital growth → Exit / continue
```

Key outputs include:

- cash required;
- loan / LVR;
- yield;
- annual cash flow;
- equity;
- leveraged IRR;
- break-even / StrategyMaximumPrice where target constraints exist.

### Replacement Development

```text
Acquire low-improvement-value asset → Demolish → Build one replacement asset → Sell / hold
```

Key question:

> Does finished single-asset value justify all acquisition/replacement/holding costs?

### Subdivision Development

```text
Acquire → Planning / subdivision → Demolish where required → Create multiple assets → Sell / hold
```

Key question:

> Can land/planning utility convert one acquisition into multiple economically valuable assets?

## 10. Temporary hold is a phase

```text
Acquire → Rent temporarily → Obtain approvals → Develop
```

This is a project phase, not a fourth strategy.

## 11. Development finance timing

Development return depends on when capital is deployed and recovered.

Replacement/Subdivision models therefore use a DevelopmentCashFlow timeline.

Do not collapse financing into one opaque `financeAndHolding` value when calculating IRR.

Distinguish:

- `unleveredProjectIrr` — project return before financing flows;
- `leveredEquityIrr` — equity return after financing effects.

If a lender facility/drawdown structure is not sufficiently defined, leveredEquityIrr must remain UNKNOWN.

Peak debt and peak equity at risk are separate decision dimensions.

## 12. Strategy eligibility

Each strategy must produce:

- ELIGIBLE
- ELIGIBLE_WITH_CONSTRAINTS
- INSUFFICIENT_EVIDENCE
- NOT_ECONOMICALLY_SUPPORTED
- NOT_APPLICABLE

Eligibility is not a purchase recommendation.

## 13. Strategy comparison

Do not compare unlike strategies only by nominal ROI.

Compare:

- capital required;
- duration;
- cash-flow profile;
- debt exposure;
- execution complexity;
- planning risk;
- construction risk;
- market risk;
- liquidity;
- appropriate return metrics;
- acquisition-price gap;
- downside sensitivity;
- unresolved evidence.

## 14. Decision language

Prefer:

- worth modelling further;
- economically plausible;
- weak under current assumptions;
- market above strategy-supported price;
- blocked by unknowns;
- not supported by available evidence.

Do not convert this into an unsupported command to buy or develop.
