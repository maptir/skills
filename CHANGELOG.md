# Changelog

## game-guides 1.0.0 — unreleased

First packaged release.

### game-guide
- Output contract v1 (`references/output-contract.md`): every guide is a complete HTML document with an embedded `guide-meta` block, relative asset files (no base64), slug-prefixed `localStorage`, host-neutral wording.
- Publishes in tiers: local `game-guides/<slug>/` folder → Artifact (when available) → HTML in the reply.
- DLC or separate runs become variant guides (`<game>--<suffix>`); 100% completion stays a tab in the existing guide.
- Upgrades older guides to the contract when updating them.
- `artifact-design` / `artifact-diagramming` are optional; `page-build.md` carries a design baseline for when they are absent.
- `scripts/check_guide.py` checks a guide against the contract.
- Image-credit warning on delivery when a guide ships studio or wiki images.
- New fixed tab **"100% and achievements"** in every guide, last in the rail: platform total, missables (linked to "Do this or lose it forever"), playthroughs, time to 100%, a roadmap, the grouped list with persisted ticks, and the rarest by global unlock rate. Hidden achievements are spoiler-gated.

### game-guide-hub (new)
- Keeps every guide in one private **Game Guides** page: a card per game, guides open inside the page, a dropdown for a game's variants.
- `/game-guide-hub <game>`, `sync`, `remove`; legacy guides are handed to `game-guide` for upgrade, never edited by the hub.
- Publishes only changed files; falls back to a local `game-guides/index.html`.
