---
name: bk-capture
description: Capture user-authorized knowledge or submit source-backed untrusted Claim proposals to Banyan Knowledge. Use when asked to record knowledge in BK; reading or discussing information alone does not authorize a write.
---

# Capture knowledge in BK

Operate only on the user's intended BK installation and explicit Project ID.
Use the tools and schemas actually exposed by the current connection. A skill
does not grant `bk.memory.write`, `bk.memory.propose` or `bk.project.write`.
Do not request a broader scope when a narrower authorized workflow is sufficient.

## Choose the correct write

- `memory.create` creates a trusted immutable Claim. Use it only after the user
  explicitly asks BK to remember the supplied knowledge. Retain a genuine source
  locator, the user's confirmation of the assertion, or both. A source is not
  mandatory for the user's own experience, decision or procedure.
- Set `userConfirmed=true` only when the user has actually affirmed the assertion
  being stored. An explicit "remember this: ..." supplying the user's own fact
  can provide that confirmation; "import/summarize this page" or approval of a
  tool call does not confirm every extracted assertion. Do not manufacture a
  confirmation, source, signature or citation to satisfy validation.
- `proposal.create` submits an untrusted, source-backed candidate for later
  administrator review; it does not create reviewed memory. Use it only when the
  user authorizes candidate submission and the tool is exposed. Lite requires
  `sourceLocator` for proposals. If neither a genuine locator nor user
  confirmation is available, keep a draft in the response and ask for the
  missing evidence/confirmation; do not invent a source or auto-promote it.
- Proposal acceptance/rejection belongs to the BK administrator UI, not an
  invented MCP review tool. Never replace missing proposal authority with trusted
  Claim creation or bypass review via the browser/API without authorization.

## Shape and submit

1. Preserve the user's meaning, language, conditions and uncertainty. Split
   independent assertions only when that fits the requested capture scope. Ask
   before storing a substantial inferred rewrite or an unapproved bulk import.
2. Choose the real category: `Fact`, `Experience`, `Decision`, `Procedure`, `Note`
   or `Reference`. `memoryArea` is an optional label, not a security boundary.
   Keep `assertion` and optional `content` within 8,000 characters each; retain
   the actual source locator (at most 2,048 characters) and optional source label.
   Do not store passwords, access tokens, recovery material or unrelated personal
   data as knowledge.
3. When relevant, search for an existing Claim in the same Project to avoid
   duplicates. If the request changes an existing Claim, use the separately
   authorized lifecycle workflow rather than pretending a duplicate insertion
   corrects the old Claim. Creating a Project also requires a separate request.
4. Generate one UUID `idempotencyKey` for the exact create/proposal payload. Keep
   it with that payload. After a lost response, an exact retry may reuse the
   same key; a changed assertion, Project, trust credential or category requires
   a new key. Do not retry forever or switch installations to obtain success.
5. Report success only from the tool result: Claim/proposal ID, Project and
   whether it is trusted memory or a pending proposal. If the result is unknown,
   say so; do not invent an ID or claim the write completed.

Normal capture through an Agent needs no BK generation service or embedding.
Do not silently record conversation turns, fetched content or task results just
because this skill is available. Respect the host's tool approvals without
adding repetitive confirmation when the user already clearly authorized the
exact ordinary capture and supplied its trust credential.
