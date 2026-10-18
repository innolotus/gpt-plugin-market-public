# GPT Plugin Market Public

Public, repository-owned Codex plugin marketplace for InnoLotus plugins.

## Add the marketplace

```bash
codex plugin marketplace add innolotus/gpt-plugin-market-public --ref main
```

From a local checkout, `codex plugin marketplace add .` registers that checkout
instead of the Git-backed marketplace.

## Available plugins

### Iris Console 0.1.2

Iris Console provides evidence-aware Australian property research, acquisition,
investment and development workflows through 18 coordinated Skills.

```bash
codex plugin add iris-console@gpt-plugin-market-public
```

The base plugin contains no credentials or private client profiles. Connected
property-data providers and `grill-me` are optional enhancements rather than
hard dependencies.

## Repository map

- `.agents/plugins/marketplace.json` is the ordered marketplace catalog.
- `plugins/<name>/.codex-plugin/plugin.json` is each installable plugin manifest.
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
