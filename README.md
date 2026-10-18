# GPT Plugin Market Public

Public, repository-owned Codex plugin marketplace for InnoLotus plugins.

## Add the marketplace

```bash
codex plugin marketplace add innolotus/gpt-plugin-market-public --ref main
```

From a local checkout, `codex plugin marketplace add .` registers that checkout
instead of the Git-backed marketplace.

## Available plugins

No plugins are currently listed in this marketplace.

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
