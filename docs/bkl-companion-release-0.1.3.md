# BK Lite companion 0.1.3

Companion release for **Banyan Knowledge Lite 0.1.2-beta.2.2**. Plugin versions
are independent of the Lite server version. The four shared skills cover setup,
Project-scoped recall, explicitly authorized Claim capture/proposals, and
two-phase immutable lifecycle governance.

- Full Plugin: `banyan-knowledge-lite-plugin-0.1.3.zip`. Preserves the existing
  `banyan-knowledge-lite` identity and OLS01 MCP connection. The packaged OAuth
  scope set remains read + trusted Claim write + Project write + refresh; no
  proposal/governance scopes are silently added.
- Skills only: `banyan-knowledge-skills-0.1.3.zip`. Same four skills, with no MCP
  connection. Use this instead when you already have an authorized BK connection.
- Adjacent SHA-256 files verify archive integrity; `bkl-companion-receipt.json`
  records both hashes and the exact public marketplace source revision.

The full Plugin connects to the **InnoLotus OLS01 installation**, not an
automatically discovered personal installation. For your own BK URL, generate
a new local marketplace with the repository's configuration tool; it defaults
to read-only authority. Local HTTP is supported only through the explicit
loopback read-only profile. No credentials are packaged or copied.

Install from `innolotus/gpt-plugin-market-public`, or follow the
[configuration and migration guide](https://github.com/innolotus/gpt-plugin-market-public/blob/main/docs/bkl-companion.md).
Installing from this repository does not update a separately installed personal
Plugin automatically; select one source and disable the old duplicate only when
the replacement is verified. New scopes require explicit OAuth re-consent.

Server-side authorization and Agent Host approval policy remain authoritative.
Source-only and package validation are not proof of end-to-end OAuth or skill
selection in every host. Claude and other hosts may reuse the skills, but their
native Plugin/authentication adapters are not certified by this release.
