# maptir/skills

Claude skills, packaged as a Claude Code plugin marketplace. Each plugin is one topic; install only what you want.

| Plugin | Skills | What it does |
|---|---|---|
| [`game-guides`](plugins/game-guides) | `game-guide`, `game-guide-hub` | Spoiler-safe, personalised guides for a specific game — built around its scarce resources and the choices you can't undo — plus a private hub page that keeps every guide in one place. |

## Install

### Claude Code (recommended)

```
/plugin marketplace add maptir/skills
/plugin install game-guides@maptir-skills
```

Both skills install and update together. From a plugin they are addressed as `/game-guides:game-guide` and `/game-guides:game-guide-hub`; Claude also picks them up from plain requests ("make me a guide for Hades II").

### claude.ai (web, desktop, mobile)

1. Download `game-guide.zip` and `game-guide-hub.zip` from the latest [release](https://github.com/maptir/skills/releases).
2. Upload **both** under Customize → Skills (code execution must be on). The hub needs `game-guide` to build guides.

### Other agents that read `SKILL.md` (Codex, Cursor, Gemini CLI, …)

Copy `plugins/game-guides/skills/game-guide/` (and `game-guide-hub/` if you want the hub) into your agent's skills folder.

## What works where

| Where you run it | `game-guide` | `game-guide-hub` |
|---|---|---|
| Claude Code signed in with a claude.ai account (CLI or desktop app) | Local folder + private Artifact, with map/image files | Private **Game Guides** Artifact |
| claude.ai chat / Cowork (paid plans) | Artifact; image files may not be supported there | Expected to work; not yet verified |
| Claude Code on an API key, Bedrock or Vertex; Agent SDK | Local `game-guides/<slug>/index.html` | Local `game-guides/index.html` (opens from disk) |
| Claude API Skills container, other agents | Local HTML file, or the HTML in the reply | Local hub page if files can be written |

The scripts (`check_guide.py`, `build_hub.py`) use Python 3's standard library only. Without Python the skills fall back to written checklists.

## What you get

- **Guides are yours.** The MIT licence covers the skills; the guides they produce belong to whoever made them.
- **Guides are private by default.** An Artifact is visible only to you until you share it. If a guide carries images from a game's studio or a wiki (area maps, item art), the skill tells you — credit is not permission, so take them out before sharing a guide publicly.
- **One stable format.** Every guide follows the [output contract](plugins/game-guides/skills/game-guide/references/output-contract.md) (version 1), which is what lets the hub read guides it did not build.

## Versioning

Plugins use semver. The guide output contract has its own integer version; a contract change is always a plugin **major** release. See [CHANGELOG](CHANGELOG.md).

## Licence

[MIT](LICENSE)
