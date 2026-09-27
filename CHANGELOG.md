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

- **Where-lists are required**: every rationed thing the guide gives a total for gets a per-item list (where · how · needs · act · tick), with a verification check that each list's row count matches its total; per-area counts in walkthrough blocks; a currency tab (every permanent purchase, prices, total, spend order) for games whose currency is lost on death. Added after a Silksong guide shipped with totals but no locations.
- Shared **checklist table** component in `page-build.md` (multi-list, `data-key` per list); the checker validates `data-key` prefixes.
- **Tick boxes everywhere a thing can be collected or missed**: where-lists, the "Do this or lose it forever" table (key `<slug>:missables`) and the achievements list. One box per thing — walkthrough area blocks get a live tally (`data-area` / `data-tally`) instead of boxes, and other tabs link to the list. Checklist roots are any `[data-key]` element; boxes can sit in table rows, list items or `data-tick-row` cards (questline steps).
- **Export/import for ticks** (`.ticks-io`): ticks stay in `localStorage`, and a footer block copies every `<slug>:` key as text and restores it elsewhere — standalone copy, hub, another browser. Replaces the "runtime capability when available" advice for ticks, since a shared database on a link-shared page would mix every viewer's ticks. The checker errors on duplicate `data-key` roots, duplicate `data-ach` ids in a list and a mismatched `data-slug`, and warns when a page saves ticks without the block.
- Layout fix: the rail grid uses `minmax(0,1fr)` and `min-width:0` on its children — `1fr` let wide tables push every tab sideways on phones. The checker warns on the pattern, and the verification pass includes a 375px overflow check.

### game-guide-hub (new)
- Keeps every guide in one private **Game Guides** page: a card per game, guides open inside the page, a dropdown for a game's variants.
- `/game-guide-hub <game>`, `sync`, `remove`; legacy guides are handed to `game-guide` for upgrade, never edited by the hub.
- Publishes only changed files; falls back to a local `game-guides/index.html`.
