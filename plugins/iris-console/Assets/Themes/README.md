# Iris Report Theme

`iris-orange.json` is the repository-owned `answer-me-with-html` theme for Iris reports.

It defines the orange-white MVP brand direction while retaining semantic green, red and warning colours for evidence and decision states. Light mode is the report default; the dark tokens are maintained and checked so an explicit dark rendering remains usable.

The renderer stages this file into an isolated temporary `AM_HOME/themes` directory and selects it by the stable name `iris-orange`. Do not copy it into, or overwrite, a developer's global theme directory during an analysis run.

Validate changes with:

```text
node <answer-me-with-html-skill>/scripts/am.mjs theme check Console/Assets/Themes/iris-orange.json --no-open
```

Theme tokens control presentation only. They must not change evidence state, chart values or semantic status labels.
