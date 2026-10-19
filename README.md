# GPT Plugin Market Public

Public, repository-owned Codex plugin marketplace for InnoLotus plugins.

## Add the marketplace

```bash
codex plugin marketplace add innolotus/gpt-plugin-market-public --ref main
```

From a local checkout, `codex plugin marketplace add .` registers that checkout
instead of the Git-backed marketplace.

## Available plugins

| Plugin | Version | Purpose |
|---|---|---|
| `banyan-knowledge-lite` | 0.1.3 | BK connection plus setup, recall, capture and lifecycle skills |

The bundled BKL connection targets the **InnoLotus OLS01 installation**, not
your automatically discovered installation. Read the
[BKL configuration and migration guide](docs/bkl-companion.md) before connecting
or sending knowledge. Self-hosted users can generate a configured local Plugin;
users with an existing MCP connection can use the skills-only release instead.

After registering this marketplace, install its BKL package:

```bash
codex plugin add banyan-knowledge-lite@gpt-plugin-market-public
```

The public repository publishes Plugin/skill source only. It does not publish
the private BK Lite product source, deploy BK, register user accounts or grant
access to an installation. Plugin release assets include checksums and an exact
source receipt. This is Git marketplace distribution, not a submission to the
OpenAI universal public directory.

## Iris Console has moved

Iris Console 0.1.2 is now distributed through the
[public marketplace](https://github.com/Lab-Cubes/labcubes-plugin-market/tree/main/plugins/iris-console).
Register that marketplace and install from its identifier:

```bash
codex plugin marketplace add Lab-Cubes/labcubes-plugin-market --ref main
codex plugin add iris-console@labcubes-plugin-market
```

## Repository map

- `.agents/plugins/marketplace.json` is the ordered marketplace catalog.
- `plugins/<name>/plugin.json` is the portable Agent Plugins manifest.
- `.codex-plugin/plugin.json` and `.mcp.json` retain Codex compatibility overlays.
- `plugins/banyan-knowledge-lite/skills/` owns the four portable BK workflows.
- `scripts/bkl_packages.py` validates, configures and exports BKL packages.
- `tests/` and `.github/workflows/bkl-companion.yml` gate companion releases.
- `docs/bkl-companion.md` explains trust boundaries, migration and validation.
- Plugin source paths in the catalog remain relative to the repository root.

## Add or update a plugin

Use the Codex `plugin-creator` scaffold with this repository as the plugin and
marketplace destination. Each catalog entry must declare its relative source,
installation policy, authentication policy and category. Keep the marketplace
identifier `gpt-plugin-market-public`; changing it affects existing installations.

Validate the manifest, catalog and Skill metadata after every change. Plugin
releases must be traceable to validated source and must not contain credentials,
private keys, customer data or private profiles. Follow the applicable
InnoLotus security and review standards before merging.
