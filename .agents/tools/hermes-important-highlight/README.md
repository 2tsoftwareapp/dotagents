# Hermes Desktop important highlight

Source plugin for Hermes Desktop that registers the `::important{...}` directive to render a highlighted key point inside an assistant response.

## Installation

Copy `plugin.js` into `$HERMES_HOME/desktop-plugins/important-highlight/plugin.js` (usually `~/.hermes/desktop-plugins/important-highlight/plugin.js`). Keep the directory name identical to the plugin `id`. If the target directory already exists, do not overwrite it; review and merge manually.

The desktop app loads the plugin automatically within a few seconds. If it does not appear, use ⌘K → **Reload desktop plugins**. The plugin must be enabled under Capabilities → Plugins.

To let the agent use the syntax in the current project, copy the bundled `SKILL.md` into `<project>/.agents/skills/hermes-important-highlight/SKILL.md` and mark the repository as trusted through Hermes' Skills mechanism if needed. Hermes loads project skills only from trusted repositories.

## Try it

```markdown
::important{text="Back up the database before running migrations."}
```

The directive can sit inside a paragraph; the plugin renders a separate block at that position. If the directive is not registered, Hermes keeps the content as plain text.
