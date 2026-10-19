---
name: bk-setup
description: Connect or troubleshoot Banyan Knowledge Lite, check MCP capabilities, and select an explicit Project. Use for BK setup or missing tools, not general Agent configuration.
---

# Set up Banyan Knowledge Lite

BK is an Agent-facing governed Claim system, not a Wiki or an automatic
conversation-memory service. Its `memory.*` tools read or capture governed
knowledge. Do not confuse it with the separate Banyan Memory product.

## Connection and capability checks

- Inspect the actual enabled BK connection and discovered tools first. A Plugin
  manifest, cached grant, or installed skill is not proof of a working connection.
  Tool names may be host-namespaced; use the supplied input schemas.
- The distributed connection targets the InnoLotus OLS01 installation. Before
  connecting or sending knowledge, establish that this is the user's intended
  BK. For a different installation, use its operator-supplied MCP URL and the
  repository's configuration/export procedure. Do not edit an installed cache or
  silently fall back to a public instance. If the user already has a working BK
  MCP connection, the skills-only pack avoids a duplicate connection.
- Remote OAuth uses the BK web login and exact consent, not a third-party social
  account or the bootstrap/recovery administrator. Never ask for a password,
  token, recovery secret, or API key in chat. Let the host run its login flow.
- Local loopback MCP exposes six read-only tools. Remote OAuth always requires
  `bk.memory.read`. Optional independent scopes are `bk.memory.write` for trusted
  capture, `bk.memory.propose` for untrusted proposals, `bk.memory.govern` for
  lifecycle prepare/commit, and `bk.project.write` for Project creation.
  `offline_access` enables refresh, not additional tool authority.
- Use the narrow scope set needed for the requested work. Missing tools require
  deliberate reconnect/re-consent; refreshing an old grant cannot add authority.
  Do not broaden write scope to compensate for a missing Project/governance tool.
  Client approval policy remains host-owned; neither skills nor OAuth scopes
  mean bypass permission. Do not add another standalone MCP entry just to change
  approvals for a Plugin-owned connection.

## Bind the Project

1. Use `project.get` for an explicitly supplied Project ID, or `project.resolve`
   for an operator-provided exact binding namespace/key. Do not infer a binding
   key from a repository, directory, URL, customer name, or fuzzy match.
2. Otherwise use `project.list` and let the user select when the intended Project
   is ambiguous. Names are labels, not authority. Preserve the returned ID and
   the selected installation for subsequent calls.
3. A missing Project is not permission to create one. Use `project.create` only
   when requested and exposed. It is non-idempotent: after an indeterminate
   result, inspect the list and resolve uncertainty before another attempt.

Report the selected installation, Project and available task-relevant tools.
Distinguish disabled endpoint, transport failure, login required, insufficient
scope, and absent Project rather than treating all as an empty knowledge base.
No embedding or generation service is required for ordinary tool-based capture
and baseline retrieval. Do not install models as a connection repair.
