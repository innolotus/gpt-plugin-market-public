# GPT Plugin Market Public

Repository-owned Codex plugin marketplace. The catalog is initialized and has no plugins yet.

## Repository map

- `.agents/plugins/marketplace.json` is the ordered marketplace catalog.
- `plugins/<plugin-name>/` will hold each plugin when one is added. Do not create an empty plugin as a placeholder.

## Add a plugin

Use the Codex `plugin-creator` scaffold with this repository as the plugin and marketplace destination. Each plugin needs a `.codex-plugin/plugin.json` manifest. Its catalog entry must point to `./plugins/<plugin-name>` and declare installation policy, authentication policy, and category. Review those values and the plugin's code before listing it.

Validate the manifest and catalog after each addition. The marketplace identifier must remain `gpt-plugin-market-public`; changing it affects existing installation references.

## Use locally

From this repository root, run `codex plugin marketplace add .` to register this marketplace in your Codex environment. Registration changes local Codex configuration and is optional for editing the catalog. Once plugins are listed, use `codex plugin list` to check discovery.

Do not commit credentials, private keys, or customer data. Follow the applicable InnoLotus security and review standards for plugin changes.
