# Output contract (version 1)

What every guide must be at its edges. Inside the page — layout, tabs, colours,
fonts, scripts — is the guide's own business. At the edges it follows these
rules, so the same bytes work as an Artifact, as a file opened from disk, and as
one guide among many inside a hub (the `game-guide-hub` skill reads nothing but
what this file promises).

The version is `1`. Anything that changes a rule below changes the number.

## 1. A complete HTML document

```html
<!doctype html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hollow Knight</title>
  …styles…
</head>
<body>
  …page…
  <script type="application/json" id="guide-meta">{ … }</script>
</body>
</html>
```

- `lang` is the language the page is written in, and matches `guide-meta.lang`.
- `<title>` is the game's name and nothing else (see SKILL.md §4).
- Artifact hosts will wrap a fragment for you. Do not rely on it: a local file
  or a hub iframe gets no wrapper.

## 2. `guide-meta`

One `<script type="application/json" id="guide-meta">` block, anywhere in the
document. It is plain JSON — no comments, no trailing commas.

| Field | Required | Type | Meaning |
|---|---|---|---|
| `contract` | yes | integer | `1` |
| `slug` | yes | string | The guide's identity. Lowercase `a-z`, `0-9`, `-`; a variant adds a `--suffix` |
| `game` | yes | string | Slug of the base game. Guides with the same `game` are grouped together |
| `variant` | yes | string | Label for this guide among its game's guides, in the page language — "Main game", "DLC: …", "NG+" |
| `title` | yes | string | The game's exact name |
| `lang` | yes | string | BCP 47 tag, e.g. `th`, `en`, `ja` |
| `summary` | yes | string | One sentence saying what this guide is. Also the Artifact description |
| `game_version` | yes | string | Patch the numbers describe. `"unknown"` when the sources do not say — never a guess |
| `updated` | yes | string | ISO date of the last change, `YYYY-MM-DD` |
| `spoiler_gate` | yes | boolean | `true` unless the player said they have finished the game |
| `sources` | yes | array | `[{"name": "…", "url": "…"}]` — the sources the numbers came from |
| `created` | no | string | ISO date the guide was first built |
| `platform` | no | string | e.g. `PC`, `PS5`, `Switch` |
| `dlc` | no | array of strings | DLC the guide covers |
| `player_profile` | no | object | `{"experience": "…", "goal": "…"}` from the scope interview |
| `image_credits` | no* | array | `[{"files": "maps/*", "from": "…", "rights": "…"}]` |
| `disputed` | no | array of strings | Numbers where sources disagree, one line each |
| `artifact` | no | object | `{"url": "…"}` once published as an Artifact |

\* `image_credits` is required whenever the page ships images you did not draw.

Do not add a tab list, an asset list or design details — they can be read off
the page and the folder, and a second copy only drifts.

Example:

```json
{
  "contract": 1,
  "slug": "hollow-knight",
  "game": "hollow-knight",
  "variant": "เกมหลัก",
  "title": "Hollow Knight",
  "lang": "th",
  "summary": "คู่มือเล่นรอบแรก ไม่มีสปอยล์เนื้อเรื่อง เน้นงบ Pale Ore ชาร์ม และเควสต์ NPC ที่พลาดได้",
  "game_version": "1.5",
  "updated": "2026-09-21",
  "spoiler_gate": true,
  "sources": [{"name": "Hollow Knight Wiki", "url": "https://hollowknight.wiki/"}],
  "platform": "PC",
  "player_profile": {"experience": "never played", "goal": "collect most, not 100%"},
  "image_credits": [{"files": "maps/*", "from": "hollowknight.wiki", "rights": "© Team Cherry"}]
}
```

## 3. One guide or two?

- **Updating** a guide keeps its `slug`. Overwrite the same folder, bump
  `updated`, republish the same Artifact URL.
- **100% completion** is the "100% and achievements" tab every guide already
  has, not a new guide.
- **A DLC, or a genuinely different kind of run**, gets its own guide: a new
  `slug` with a `--` suffix (`elden-ring--shadow-of-the-erdtree`), the same
  `game`, and its own `variant`. The hub shows these as a dropdown under one
  game.

## 4. Files

```
game-guides/
└── <slug>/
    ├── index.html
    ├── maps/…      (only if the guide has area maps)
    └── images/…    (only if the guide ships images it did not draw inline)
```

- Every asset is referenced by a **relative** path under the guide's folder —
  `maps/greenpath.png`, never `/maps/…`, never `https://…`.
- **No base64 images.** Icons you draw stay inline as SVG `<symbol>`s; any raster
  image is a file. An icon sprite may point at files:
  `<symbol id="i-quartz" viewBox="0 0 64 64"><image href="images/quartz.png" width="64" height="64"/></symbol>`.
- `localStorage` keys start with the slug and a colon: `hollow-knight:quest-ticks`.
  Guides share an origin inside a hub, and un-prefixed keys collide.
- The only external request allowed is Google Fonts, and the page must read
  fine if it fails to load — always give a system-font fallback.
- No wording that assumes where the page lives ("this is a private page",
  "tell Claude and I will fix it"). The same page may be an Artifact, a file on
  disk, or a frame inside a hub.
- Warn the player when the assets together pass 10 MB; an Artifact page tops
  out at 16 MB.

## 5. Publishing

Do every tier that is available, in order:

1. **File system** → write `game-guides/<slug>/` under the working directory.
   Always, when you can write files.
2. **Artifact tool** → publish `index.html` with the assets as supporting files
   (`files: {"maps/greenpath.png": "game-guides/<slug>/maps/greenpath.png", …}`),
   title = the game's name, description = `summary`. When updating, pass the
   existing URL and `read` it first. Put the URL into `guide-meta.artifact.url`
   and save the local copy again.
3. **Neither** → return the full HTML in the reply, and say that images cannot
   travel that way.

## 6. Checklist

`scripts/check_guide.py <folder-or-index.html>` runs these for you. By hand:

- [ ] Starts with `<!doctype html>`; `<html lang>` present and equal to `guide-meta.lang`
- [ ] `<meta charset>` and `<meta name="viewport">` present
- [ ] Exactly one `guide-meta` block, valid JSON, every required field present and typed right, `contract` is `1`
- [ ] `slug` matches the folder name
- [ ] No `data:image` anywhere
- [ ] Every `src` / `href` asset path is relative and the file exists
- [ ] Every `localStorage` key starts with `<slug>:`
- [ ] No external URL other than `fonts.googleapis.com` / `fonts.gstatic.com` is loaded (links the reader clicks are fine)
- [ ] Images you did not draw ⇒ `image_credits` is not empty
