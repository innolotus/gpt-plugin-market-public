# Iris HTML Report Rendering Profile

## Contract

The responsive HTML report is a derived reading view of one validated `CanonicalDemoReport`.

The canonical YAML/JSON artifact remains the source of truth for audit, regression and replay. Rendering is read-only over canonical data and must not change analysis status, evidence state, assumptions, calculations or conclusions.

The default delivery for a material live or demo analysis is:

```text
CanonicalDemoReport (audit/replay source)
        ↓ fixed projection
answer-me-with-html Markdown draft
        ↓ renderer
responsive single-file HTML (primary reading view)
```

## Renderer profile

Use `answer-me-with-html` 0.5.2 or a later compatible 0.5.x release with Node.js 20 or newer. A successful smoke test against an older release covers only the exercised fixture and does not broaden this declared release range. An analysis run must not update the user's renderer installation.

Use these defaults:

```yaml
template: sheet
theme: iris-orange
mode: light
cols: 2
style: 80
```

Always render with `--no-open`. The caller decides how to present or host the resulting file.

The page must remain a single offline HTML file. Do not add CDN fonts, remote scripts, custom CSS, hand-authored SVG diagrams or a second UI framework. Static SVG charts produced by the repository's validated `render-charts.mjs` generator are the sole SVG exception and must be embedded by the renderer.

## Iris branding

Use the compact report asset at [../Assets/Brand/iris-logo-mark-report.png](../Assets/Brand/iris-logo-mark-report.png). Resolve it to an absolute filesystem path before building the Markdown draft so `answer-me-with-html` can embed it into the single-file report.

Place the logo once, directly after the frontmatter and before the first report panel:

```markdown
![](<absolute path to iris-logo-mark-report.png>)
```

The empty alternative text marks the image as decorative because the adjacent page title already identifies Iris. Do not add a duplicate caption, regenerate the logo per report, reference the high-resolution master or use a remote URL.

## Semantic icon language

Use restrained monochrome text symbols to help readers scan the report. Icons supplement text and never replace canonical labels.

Use this fixed panel vocabulary when the panel is present:

```text
◎   Decision summary
⌂   Subject and analysis scope
▦   Market or acquisition context
$   Owner-occupier, funding or strategy result
↔   Strategy or scenario comparison
⚠︎   Evidence, conflicts and unknowns
⚙︎   Assumptions and basis
ⓘ   Audit trail and disclaimers
```

Write each symbol between the panel letter and title, for example `## A ◎ Decision summary {span=2}`. Use no more than one symbol in a panel title and keep the full text label.

For tables that already expose a canonical evidence or eligibility state, use the renderer's text status markers:

- `ok CONFIRMED` or `ok VERIFIED`;
- `warn UNVERIFIED`, `warn UNKNOWN`, `warn PARTIAL` or `warn ELIGIBLE_WITH_CONSTRAINTS`;
- `no CONFLICTED` or `no BLOCKED`.

The visible label must remain exactly canonical. Do not add a positive icon to `ReportStatus: COMPLETE`, because completion does not mean recommendation. Do not add icons to every number or bullet, use multicolour emoji, load an icon library or encode meaning through an icon alone.

## Charts and quantitative visuals

Use one to three compact charts when the canonical report contains at least three comparable points. Charts support the decision and never replace the adjacent exact-value table.

Every chart specification must state its canonical report reference, exact source field paths, unit, period, `ReturnBasis` and `TaxTreatment`. Do not combine values with different units, periods, return bases or tax treatments in one scale.

Supported charts are:

- `line`: complete, ordered, continuous canonical series such as annual property value and loan balance. Reject missing points rather than interpolating or drawing across a gap;
- `bar`: up to 48 scenario/category groups and four series with the same unit and basis. Show a visible zero baseline and preserve signed negative values; sample visible x-axis labels when dense, omit an in-bar value label when it cannot fit safely, and retain every value in the accessible SVG plus adjacent exact table;
- `donut`: up to eight non-negative, mutually exclusive canonical parts of one explicit whole. Segment values must add exactly to that whole within numeric tolerance; compact long visible labels while preserving their full accessible text;
- renderer-native `timeline`: short ordered milestones when a quantitative line chart is unnecessary;
- renderer-native `limits`: only when the canonical report supplies a real ceiling, target, threshold or client constraint.

Use the orange brand palette for the primary series, line styles as a non-colour distinction for multiple series, and semantic green/red only for genuine positive/negative state. Every SVG requires an accessible title and description. The exact table provides the primary accessible numeric alternative.

For `OWNER_OCCUPIER_ACQUISITION`, prefer:

- repayment sensitivity across canonical interest-rate scenarios;
- a value-versus-limit view only when `FundingSupportedPriceCeiling` or another real funding limit exists.

For `INVESTMENT_DEVELOPMENT`, prefer:

- a complete annual value-versus-debt line chart;
- a purchase-price, interest-rate or growth sensitivity bar chart;
- a donut only for a real total such as mutually exclusive initial-cash components;
- mortgage-rate or capital-growth sensitivity;
- a value-versus-limit view only when `StrategyMaximumPrice`, target return or maximum acceptable cash deficit exists.

Never use the highest scenario as a fake limit. Never infer missing time-series points, smooth sparse evidence, hide negative signs, derive a midpoint that the canonical report does not contain, generate a donut from unrelated values or load a remote chart library. Omit the chart when its canonical series is incomplete or cannot pass validation.

## Responsive layout

Treat the report as a trust-first investment brief, not a marketing landing page.

- Use no more than two columns on desktop.
- Let the renderer collapse panels to one column on narrow screens.
- Give the decision summary, strategy comparison and wide evidence tables a full row with `{span=2}`.
- Prefer tables with three columns or fewer so their full meaning remains visible on a phone.
- Split wider comparisons into cost and return tables, or into compact per-scenario panels. Do not rely on page-level horizontal scrolling.
- Keep labels short enough to scan on a phone.
- Prefer key-value blocks and short tables over long prose.
- Use the `iris-orange` theme in light mode by default and preserve printable contrast. A validated dark token set remains available for future explicit dark-mode output.
- Do not add non-essential motion.

## Required projection

Every HTML view must expose the following canonical fields when present.

### Header metadata

- report title;
- normalized address or subject entity;
- `ReportStatus`;
- analysis branch;
- generated timestamp;
- report ID.

### Decision summary

- headline;
- strongest supported conclusion;
- key findings;
- conditions that would change the conclusion.

Use a `callout` component. `COMPLETE` means the requested path completed, not that the property is recommended. Show `PARTIAL` and `BLOCKED` prominently.

### Subject and scope

Use a `kv` component for:

- entity type;
- normalized address;
- jurisdiction;
- PropertyRef or PropertyComplex scope;
- AcquisitionTarget;
- profile completeness when material.

For a complex-level report, state whether the target is a specific property, any unit, an unknown unit or the whole complex. Never imply that complex-level evidence describes a specific unit.

### Price and branch result

For `OWNER_OCCUPIER_ACQUISITION`, show only applicable values such as:

- MarketValueRange;
- ExpectedAcquisitionRange;
- FundingSupportedPriceCeiling;
- funding gap;
- repayment scenarios;
- ownership costs;
- purchase assistance;
- blocking unknowns.

For `INVESTMENT_DEVELOPMENT`, show only applicable values such as:

- MarketValueRange and ExpectedAcquisitionRange;
- strategy eligibility;
- model acquisition price;
- StrategyMaximumPrice;
- gap to market expectation;
- cash flow, yield, profit and IRR outputs;
- ReturnBasis and TaxTreatment.

Do not display a null value as `$0`, `0%`, `no risk` or `not applicable`. Display `UNKNOWN`, `NOT MODELLED` or the canonical state.

### Evidence and uncertainty

Provide separate panels for:

- material evidence;
- evidence conflicts;
- material unknowns;
- verification required.

Each decisive claim should retain its source, observation date, geography and evidence state. Use direct Markdown links when a permitted source URL exists.

Never merge `CONFLICTED` evidence into one preferred number without a canonical resolution. Never present `UNKNOWN` as a negative finding.

### Assumptions and reproducibility

Summarize:

- EffectiveAssumptionSet IDs and versions;
- material overrides and their origins;
- source and policy registry versions;
- Skill/model versions;
- ReturnBasis and TaxTreatment;
- canonical report reference.

Do not copy the complete private ClientProfile or FinancialSnapshot into the reading view. The canonical artifact retains permitted reproducibility data.

### Disclaimers

Render the canonical disclaimers in one concise final panel. At minimum distinguish the report from:

- certified valuation;
- lender approval;
- legal advice;
- tax advice;
- personalised financial advice.

## Recommended panel order

Use three to eight panels. Omit panels with no applicable canonical content rather than filling them with invented text.

```text
A  ◎ Decision summary           full row
B  ⌂ Subject and analysis scope
C  ▦ Market / acquisition context
D  $ Owner-occupier or strategy result
E  ↔ Strategy comparison        full row when present
F  ⚠︎ Evidence, conflicts and unknowns
G  ⚙︎ Assumptions and basis
H  ⓘ Audit trail and disclaimers
```

## Draft frontmatter

Use this shape and fill it only from the canonical report:

```yaml
---
template: sheet
theme: iris-orange
mode: light
style: 80
cols: 2
lang: en
title: <canonical report title>
subtitle: <normalized address and report status>
report-id: <report ID>
branch: <analysis branch>
generated: <generated timestamp>
---
```

Set `lang` to the user's report language. Use `zh` for Simplified Chinese and `en` for English.

## Validation before delivery

Confirm all of the following:

- the HTML `report-id` matches the canonical report;
- the Iris logo appears once and is embedded in the HTML;
- each rendered core panel uses at most one approved semantic symbol and retains its text title;
- canonical evidence and eligibility labels remain visible beside any status marker;
- every chart value and label maps to a canonical field, scenario or explicit constraint;
- charts retain signed values, visible axes/baselines, units, period, ReturnBasis and TaxTreatment;
- donut segments are mutually exclusive and equal their canonical whole;
- each chart has an adjacent exact-value table and an accessible title and description;
- the displayed `ReportStatus` and branch match the canonical report;
- all displayed numbers exist in the canonical report;
- units, currency, dates, ranges, ReturnBasis and TaxTreatment are preserved;
- conflicts, unknowns and verification requirements remain visible;
- no private snapshot fields or unrestricted source content leaked into the page;
- the generated file is new, non-empty and opens as HTML;
- the file contains no remote chart scripts, fonts or assets;
- the report remains readable at desktop and narrow mobile widths.

If any check fails, do not deliver the HTML as successful. Preserve the canonical report and follow the renderer Skill's visible fallback behavior.
