---
name: game-guide-hub
description: Keep all of a player's game guides in one private "Game Guides" hub page — a shelf of game cards that opens each guide inside the page, with a dropdown when a game has several guides (DLC, NG+). Builds new guides through the game-guide skill and adds them, syncs guides that already exist, and removes them. Use when the player mentions their guide hub, "Game Guides", หน้ารวม, a page with all their guides, adding a guide to the hub, or syncing/upgrading old guides — or invokes this skill by name. A plain request to make or update one guide belongs to game-guide, not here.
license: MIT
compatibility: Needs the game-guide skill (same plugin). Full hub as an Artifact in Claude Code signed in with a claude.ai account; elsewhere a local game-guides/index.html. Python 3 runs the build script; without it, build the page by hand from assets/hub-template.html.
metadata:
  contract: "1"
---

# Game guide hub

A player who uses `game-guide` for long enough ends up with a pile of separate
guide pages. This skill turns the pile into one place: a private page titled
**Game Guides**, one card per game, each guide opening inside the page.

It never writes guide content itself. Guides come from the `game-guide` skill
(installed from the same plugin it may be addressed as `game-guides:game-guide`),
and the only thing this skill reads from a guide is what the output contract
promises: the folder `game-guides/<slug>/`, and the `guide-meta` block inside
its `index.html`. The contract lives in the `game-guide` skill at
`references/output-contract.md`; read it once if you have not.

## Before anything: is `game-guide` here?

If the `game-guide` skill is not available, stop and tell the player it is
needed and how to get it (it ships in the same plugin; on claude.ai both skills
are uploaded separately). This skill cannot build or upgrade a guide without it.

## Where the hub lives

Everything is under `game-guides/` in the working directory:

```
game-guides/
├── hub.json            {url, contract, mode, published, removed}
├── index.html          the hub page (built by the script — do not hand-edit)
├── hollow-knight/      one folder per guide, written by game-guide
│   ├── index.html
│   └── maps/…
└── elden-ring--shadow-of-the-erdtree/
```

The hub Artifact publishes `index.html` as the page and every guide file as a
supporting file **at the same relative path** (`hollow-knight/index.html`,
`hollow-knight/maps/greenpath.png`). One page, one set of paths, whether it is
opened as an Artifact or from disk.

### Finding the hub in a later session

1. Read `game-guides/hub.json`. If it has a `url`, that is the hub.
2. Otherwise, if the Artifact tool is available, `list` the player's artifacts
   and look for the title **Game Guides** (the title is the same in every
   language; the page's own text follows the player's language).
3. Several matches, or none: ask the player — use one of them, or create a new
   hub.

Before republishing to a `url`, `read` it first; the tool refuses a publish to
a URL this conversation has not read.

If the hub exists only as an Artifact (new machine, deleted folder), rebuild the
local folder from it before changing anything: `read` the hub's published files
into `game-guides/`, then carry on as normal.

## The three jobs

### New guide — `/game-guide-hub <game>`

1. Hand the request to `game-guide`, with everything the player said. Let it run
   its own interview and research; do not duplicate them.
2. When it has written `game-guides/<slug>/`, build and publish the hub (below).
3. Tell the player both links: the guide on its own, and the hub.

### Sync — `/game-guide-hub sync`

Brings the hub up to date with what is on disk, and with any guide URLs the
player gives you (read each into `game-guides/<slug>/` first).

1. Run the build script. Its report sorts guides into:
   - **ok** — in the hub.
   - **needs_upgrade** — built before the contract existed (no `guide-meta`, a
     fragment instead of a full document, base64 images). List them and offer
     to upgrade; on a yes, hand each one to `game-guide` as an update ("bring this
     guide to the current output contract, change nothing else"). The hub never
     edits a guide page itself — the page belongs to `game-guide`.
   - **too_new** — the guide uses a newer contract than this skill knows. Skip it
     and tell the player to update this skill.
   - **broken** — say what is wrong (the report says) and skip it.
2. After any upgrades, build again and publish.

A guide made with plain `/game-guide` lands in `game-guides/` like any other, so
`sync` is also how those join the hub.

### Remove — `/game-guide-hub remove <slug>`

Run the build with `--remove <slug>`, then publish. The guide's folder and its
own Artifact are left alone; only the hub forgets it. `--restore <slug>` undoes
it.

## Build and publish

```bash
python <this skill>/scripts/build_hub.py game-guides --lang <player's language>
```

- `--lang` picks the page's interface strings; `en` and `th` are built in. For
  any other language, write a small JSON file translating the English keys
  (see `STRINGS["en"]` in the script) and pass it with `--strings file.json`.
- The script writes `game-guides/index.html` and `hub.json`, and prints a JSON
  report. `report.files` is exactly the supporting-file map to publish: only the
  files that changed since the last publish, and `null` for files to remove.

Then:

1. **Artifact tool available** — publish `game-guides/index.html`:
   - first time: no `url`, `icon: "book"`, description in the player's language
     along the lines of "All my game guides in one place";
   - afterwards: pass the hub `url` (after a `read`) and omit `icon`;
   - `files`: `report.files`, with keys as given and values as the local paths.
   Then run the script again with `--set-url <hub url> --mark-published`: it
   records the URL in `hub.json` and the published file hashes, so the next
   publish sends only changes.
2. **No Artifact tool** — the local `game-guides/index.html` is the hub. It
   opens straight from disk. Tell the player where it is. If a later session
   has the Artifact tool, offer to publish it.

**Without Python**, build the page by hand: copy `assets/hub-template.html` to
`game-guides/index.html`, replace `lang="__LANG__"` with the player's language,
and replace `/*__HUB_MANIFEST__*/{}` with
`{"strings": {...}, "guides": [...]}` — strings as in the script, one guide
object per contract-v1 guide with `slug, game, variant, title, lang, summary,
game_version, updated` (plus `artifact_url` when its `guide-meta.artifact.url`
exists), newest `updated` first. Publish every guide file as a supporting file.

## When you hand over

- The hub link (and the guide's own link, after a new guide).
- What changed: added, refreshed, removed, and anything skipped with the reason.
- If `report.image_warning` is true: one line saying some guides carry images
  from the studio or a wiki, which is fine in a private page but should come out
  before a guide or the hub is shared publicly.

## What this skill does not do

- Write or edit guide content — that is `game-guide`'s job, always.
- Share the hub. It is private; sharing is the player's call, from the page's
  Share menu.
- Merge several players' guides into one hub. Each player's hub is their own.
