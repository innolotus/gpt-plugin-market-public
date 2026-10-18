---
name: html-report-renderer
description: Render a validated Iris CanonicalDemoReport as responsive offline HTML with Iris branding, evidence states and canonical charts.
metadata:
  product: Iris Console
  version: 0.5.2
  portable: false
---

# HTML Report Renderer

## Purpose

Render a completed Iris `CanonicalDemoReport` as a responsive, single-file HTML report with the `answer-me-with-html` skill.

This Skill is a presentation adapter. It must not research, calculate, resolve evidence conflicts or change the canonical report.

## Inputs

Required:

- a validated `CanonicalDemoReport`;
- the path or durable reference to its canonical YAML/JSON artifact;
- the report language.

Optional:

- a requested output path;
- an explicit light/dark mode or theme preference.

## Runtime dependency

Requires:

- Node.js 20 or newer;
- [`answer-me-with-html`](https://github.com/QingYunA/answer-me-with-html) 0.5.2 or a later compatible 0.5.x release;
- access to that Skill's bundled `scripts/am.mjs`, or an `am` command supplied by the host.
- the bundled deterministic chart generator at `scripts/render-charts.mjs`.

Discover the dependency from the active Skill environment or host configuration. Do not hard-code a user home directory. Do not install or update the dependency during an analysis run.

## Procedure

1. Confirm that the canonical report already exists and has a supported `ReportStatus`.
2. Read [../../Reports/html-rendering-profile.md](../../Reports/html-rendering-profile.md).
3. Resolve [../../Assets/Brand/iris-logo-mark-report.png](../../Assets/Brand/iris-logo-mark-report.png) and [../../Assets/Themes/iris-orange.json](../../Assets/Themes/iris-orange.json) to absolute paths.
4. Stage `iris-orange.json` as `themes/iris-orange.json` inside an isolated temporary `AM_HOME`. Do not mutate the user's global `answer-me-with-html` settings or themes.
5. Project only canonical fields into the extended Markdown draft defined by that profile, including the Iris logo, semantic icon language and up to three applicable canonical charts.
6. For each chart, prepare bounded JSON input with its canonical report reference, source field paths, unit, period, return basis and tax treatment. Generate charts into a new output directory with `scripts/render-charts.mjs`, then reference their absolute paths from Markdown so the renderer embeds them.
7. Preserve `UNKNOWN`, `CONFLICTED`, `UNVERIFIED`, missing values, ranges, return basis and tax treatment exactly. Never replace them with inferred values or zero. Keep an exact-value table adjacent to every chart.
8. Render with `answer-me-with-html` using `--no-open`, `template: sheet`, `theme: iris-orange`, `mode: light` and at most two desktop columns.
9. Verify that the renderer reports success, embeds the logo and charts, preserves readable icon labels, keeps every chart value traceable to canonical fields and writes a new HTML file.
10. Return the HTML as the primary reading artifact and the canonical report as the audit/replay artifact.

The normal command shape is:

```text
AM_HOME=<isolated-am-home> node <answer-me-with-html-skill>/scripts/am.mjs render <draft.md> \
  --no-open --template sheet --theme iris-orange --mode light -o <report.html>
```

Use the exact CLI location supplied by the active environment.

## Artifact result

Return a sibling presentation result without adding it to the canonical report payload:

```text
HtmlReportArtifact
  reportId
  presentationOf
  format = HTML
  status = RENDERED | UNAVAILABLE | FAILED
  path
  renderer = answer-me-with-html
  rendererVersion
  generatedAt
  canonicalReportReference
  draftReference
  warnings[]
  error
```

`presentationOf` is the canonical `reportId`. `warnings` records non-fatal presentation omissions such as an invalid chart specification. `error` is populated only for `UNAVAILABLE` or `FAILED`.

## Delivery

For a successful material report:

- give the core conclusion in one or two sentences;
- link the generated `.html` file directly;
- also retain or link the canonical YAML/JSON artifact;
- do not paste the full report into chat again.

If the user explicitly requests plain text, Markdown or raw structured output, respect that request.

## Failure behavior

If Node.js or `answer-me-with-html` is unavailable, or rendering fails:

1. keep the canonical report unchanged;
2. keep the generated Markdown draft when one exists;
3. set `HtmlReportArtifact.status` to `UNAVAILABLE` or `FAILED`;
4. return the canonical report plus a concise Markdown view;
5. state the rendering error visibly.

Do not mark the analysis `BLOCKED` only because presentation failed. Do not return a stale HTML file from an earlier run.

If one chart fails validation or generation, omit that chart, keep its exact canonical table, add a visible presentation note, and append a warning to `HtmlReportArtifact.warnings`. Do not change the analytical `ReportStatus` solely because a chart failed.

Treat a missing or unreadable Iris report logo as a presentation failure. Do not generate a replacement during an analysis run and do not fetch branding from a remote URL.

## Privacy and evidence guardrails

- Do not expose full private client or financial snapshots in the HTML by default.
- Show only decision-relevant summaries; keep the full permitted snapshot in the canonical artifact.
- Do not embed unrestricted third-party content.
- Preserve provenance links, observation dates and evidence state for material claims.
- Never treat HTML as the reproducibility bundle or source of truth.
- Never hand-write HTML, CSS or SVG when the renderer is available. The bundled `render-charts.mjs` is the only approved SVG producer; it exists because `answer-me-with-html` 0.5.x does not provide deterministic line, bar and donut charts.
- Chart generation accepts bounded JSON through standard input, writes only to the requested new output directory and must not read remote URLs or embed scripts, event handlers, external images or `foreignObject` content.
- Bar charts accept at most 48 category groups and four series. Dense axes sample visible category labels while preserving every value in the SVG description and required adjacent exact-value table. Values that cannot fit safely inside a bar are not drawn out of position.
- Donut charts accept at most eight mutually exclusive segments and compact long visible labels without changing their full accessible text.
