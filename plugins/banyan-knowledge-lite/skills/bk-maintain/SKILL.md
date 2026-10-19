---
name: bk-maintain
description: Correct, supersede or withdraw an existing Banyan Knowledge Claim using authorized two-phase lifecycle tools. Use for explicit BK maintenance requests, not capture, physical deletion or Pack administration.
---

# Maintain immutable BK Claims

Lifecycle governance is separate from ordinary capture and Project creation.
Require the actual `memory.transition.prepare` and `memory.transition.commit`
tools (remote scope `bk.memory.govern`). Do not broaden write authority or edit
SQLite, use an admin endpoint, or create a duplicate Claim as a substitute when
governance is missing. Explain the missing capability and the operator's normal
re-consent/admin route.

## Decide and preview

1. Confirm the user's intended installation, exact `projectId` and target Claim.
   Read it using `memory.get` with its `memoryId`; the lifecycle tools call that
   same identifier `claimId`. Do not select a target merely by similar text.
2. Act only on the authorized maintenance request. Choose `Correction` for an
   assertion that was wrong, `ChangedFact` when reality changed, or `Withdrawal`
   when it should no longer be current. Withdrawal is not physical erasure.
   Preserve the reason and historical distinction; ask if the intent is unclear.
3. Call prepare with the exact IDs, kind and reason. For Correction/ChangedFact,
   include the required replacement assertion, category and
   `replacementUserConfirmed`, plus genuine source information when available.
   Apply the same trust rules as capture: do not convert approval to edit into
   an invented confirmation of a new assertion. A Withdrawal must omit all
   replacement fields, including a false confirmation flag.
4. Inspect the returned Project, Claim, kind, predecessor/replacement assertions,
   `createsClaim`, expiry and opaque handle. Prepare is a preview, not a commit.
   Present the meaningful before/after change to the user. If their existing
   authorization does not unambiguously cover that exact effect, obtain approval
   before committing. Do not add a second confirmation loop when the request
   already explicitly authorized the exact effect and the preview matches it.

## Commit and reconcile

Commit only the exact returned, unexpired handle with the matching Project,
Claim and connection/actor. Do not log, persist in BK, publish or invent a handle.
If the preview differs, expires or becomes stale, do not commit it; read current
state and prepare again only within the user's authorized scope. Stop on
conflict or denial rather than automatically changing targets or kinds.

An uncertain commit may be retried only with the same exact handle and IDs
through the supported replay path. A new prepare is not an exact retry. Check
current state when uncertain and report ambiguity instead of creating another
transition. Keep retries bounded and stop if the outcome cannot be reconciled.

Report the committed transition and resulting lifecycle/linked Claim IDs from
the actual response. Existing Claims remain immutable and auditable. Do not
promise deletion, Pack activation/signing, permission administration or bulk
maintenance tools that are not exposed by the connection.
