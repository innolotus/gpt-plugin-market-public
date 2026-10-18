# Iris Console Plugin

This directory is the source template for the private Iris Console Plugin. The
plugin archive is generated from the canonical `Console/` tree; the 18 Skills
and shared contracts are not duplicated here.

Build from the repository root:

```bash
python3 scripts/package-iris-plugin.py
```

The generated archive contains:

- the portable Agent Plugins 1.0 `plugin.json`;
- a synchronized `.codex-plugin/plugin.json` compatibility manifest;
- all 18 Iris Skills at the required `skills/<name>/SKILL.md` depth;
- shared Iris assumptions, contracts, evidence rules, policies, sources,
  report definitions and brand assets; and
- build provenance and payload checksums.

## Runtime capabilities

The base plugin works without a property-provider credential. Connected REA or
other approved property-data capabilities may be used when the host already
provides them. `grill-me` may enhance profile interviews when available; it is
not required for the onboarding workflow.

Local chart generation requires Node.js 20 or newer. Responsive HTML rendering
also requires `answer-me-with-html >=0.5.2 <0.6.0`. When the host cannot execute
local scripts, Iris must retain and return the canonical report rather than
claiming that HTML rendering succeeded.

No credentials, private profiles, test runs or third-party dependency source
are included in the archive.
