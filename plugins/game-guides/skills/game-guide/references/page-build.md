# Building the guide page

Load the `artifact-design` skill first if it is available; this file only covers
what is specific to game guides. Where that skill does not exist — outside
Claude Code, or in any agent without it — follow the design baseline below
instead. Either way, `output-contract.md` governs the page's edges: a full HTML
document, the `guide-meta` block, relative asset files, slug-prefixed storage.

## Design baseline (when `artifact-design` is not available)

Enough to make every guide legible and theme-safe; the page's character — its
palette, type pairing, glyphs — is still yours to choose per game.

- **Colour as tokens on `:root`**, never raw hex scattered through rules. Name
  them by role: `--bg --surface --ink --ink-soft --line --line-soft --accent
  --accent-soft --warn --good`.
- **Dark mode, both ways.** Redefine the tokens under
  `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { … } }`
  and again under `:root[data-theme="dark"] { … }`. Set `color-scheme` to match.
- **`body` gets an explicit `background: var(--bg); color: var(--ink)`** — a
  hub iframe or a bare browser tab supplies no background of its own.
- **Phone first.** At phone width keep a 16px side gutter, no horizontal page
  scroll (`overflow-x: auto` on wide tables inside a wrapper, `min-width: 0` on
  grid children), tap targets at least 40px tall.
- **Type.** Body 16–17px, line-height 1.55–1.65, measure about 70ch. Give every
  web font a system fallback (`font-family: "IBM Plex Sans Thai", system-ui,
  sans-serif`) — the page must read fine if Google Fonts never arrives.
- **Contrast.** Body text at 4.5:1 or better against its background in both
  themes; muted text still at 3:1 or better.
- **Motion.** Honour `prefers-reduced-motion: reduce` by dropping transitions.
- **Focus.** Every interactive element gets a visible `:focus-visible` outline in
  `--accent`.

Every example here is written in English. Write the page itself in whatever
language the player is using — headings, table headers, button labels and
`aria-label`s included. In-game proper nouns stay in the game's own language so
they match what is on screen and stay searchable.

## Naming

`<title>` is the game's name and nothing else — no subtitle, no dash, no
"Guide". These pages get revisited months later from a gallery, and the player
looks for the game. Put the description of what the page is into the publish
`description` instead, where the gallery renders it as the card's subtitle.

## Shape

One tabbed page. Tabs beat a long scroll here because a player consults a guide
mid-session with one hand — they want to land on "what do I spend this on" in a
single tap, not scroll past four sections they already read.

**Put the tab list in a vertical rail down the left, not a horizontal bar.**
These guides run ten-plus tabs with labels that cannot be shortened without
losing their point — "Do this or lose it forever" is the whole warning. A
horizontal bar at that count either wraps to two lines or becomes a scroller
where half the destinations sit off screen, so the reader is choosing from the
three tabs they can see rather than the twelve that exist. A vertical list shows
every label in full, all the time, and the reader scans one column instead of
hunting. It also gives the page a stable frame: the rail holds still while the
panel scrolls, so switching tabs never costs the reader their place.

Two-column grid, rail around 220px, panel taking the rest. The rail is sticky
with its own scroll so a long list never stretches the page.

```css
.wrap{display:grid; grid-template-columns:220px minmax(0,1fr); gap:28px;
      max-width:1100px; margin:0 auto; padding-block:24px}
.rail{position:sticky; top:0; align-self:start; max-height:100vh;
      overflow-y:auto; padding:8px 0}
.rail button{
  display:block; width:100%; text-align:left; border:0; background:none;
  font:inherit; color:var(--ink-soft); padding:9px 12px; border-radius:6px;
  border-left:2px solid transparent; cursor:pointer; line-height:1.3;
}
.rail button:hover{background:var(--line-soft); color:var(--ink)}
.rail button[aria-selected="true"]{
  color:var(--ink); font-weight:600;
  background:var(--accent-soft); border-left-color:var(--accent);
}
.rail button:focus-visible{outline:2px solid var(--accent); outline-offset:-2px}
```

Semantics are the standard tab pattern — `role="tablist"` on the rail, each
button `role="tab"` with `aria-selected` and `aria-controls`, each panel
`role="tabpanel"` and `hidden` unless active. Two things change because the
orientation does: set `aria-orientation="vertical"` on the tablist, and bind
**Up/Down** rather than Left/Right, plus Home and End.

```js
const tabs = [...document.querySelectorAll('.rail [role=tab]')];
const select = i => {
  tabs.forEach((t, n) => {
    const on = n === i;
    t.setAttribute('aria-selected', on);
    t.tabIndex = on ? 0 : -1;
    document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
  });
  window.scrollTo(0, 0);
  document.querySelector('.rail')?.classList.remove('open');
  const now = document.querySelector('.railbar .now');
  if (now) now.textContent = tabs[i].textContent;
};
tabs.forEach((t, i) => t.addEventListener('click', () => select(i)));
document.querySelector('.rail').addEventListener('keydown', e => {
  const i = tabs.indexOf(document.activeElement);
  if (i < 0) return;
  const to = e.key === 'ArrowDown' ? i + 1 : e.key === 'ArrowUp' ? i - 1
           : e.key === 'Home' ? 0 : e.key === 'End' ? tabs.length - 1 : null;
  if (to === null) return;
  e.preventDefault();
  const n = (to + tabs.length) % tabs.length;
  tabs[n].focus(); select(n);
});
document.querySelector('.railbar .menu')?.addEventListener('click', () =>
  document.querySelector('.rail').classList.toggle('open'));
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') document.querySelector('.rail').classList.remove('open');
});
```

**Below 760px the rail cannot stay a rail.** It would eat half a phone screen,
and phones are where these guides actually get read. Collapse it into a sticky
bar showing the current tab's name plus a menu button; tapping opens the same
tablist as a full-width overlay, and picking an entry closes it (the `select`
handler above already does the closing). Only the presentation changes, so the
semantics and the keyboard behaviour survive intact.

```html
<div class="railbar"><button class="menu" aria-label="Section menu">☰</button><span class="now"></span></div>
```

```css
.wrap > *{min-width:0}  /* a grid child sized to its widest table overflows the phone */
@media (max-width:760px){
  .wrap{grid-template-columns:minmax(0,1fr); gap:0}
  .railbar{position:sticky; top:0; z-index:21; display:flex; gap:12px;
           align-items:center; background:var(--bg); padding:12px 0;
           border-bottom:1px solid var(--line-soft)}
  .rail{position:fixed; inset:0; z-index:20; background:var(--bg);
        max-height:100vh; padding:64px 16px 16px; display:none}
  .rail.open{display:block}
  .rail button{padding:14px 12px; font-size:1.05rem}
}
@media (min-width:761px){ .railbar{display:none} }
```

Ten to twelve tabs is comfortable in a rail — more than a horizontal bar can
hold, which is part of why the rail is worth the extra markup. Past fifteen the
reader is scanning rather than choosing, and two tabs should merge.

Once the list passes about eight entries, group it: a hairline rule or a small
muted caps label at the seams, with the pre-start and orientation tabs at the
top, the systems in the middle, and the lists and warnings at the bottom. A flat
twelve-item column reads as a wall; three groups of four reads as a map.

## The spoiler gate

Default behaviour. Hidden text is blurred and unreadable until tapped, and the
surrounding sentence reads correctly without it.

```html
<span class="spoil" tabindex="0" role="button" aria-label="Tap to reveal spoiler">boss name</span>
```

```css
.spoil{
  background:var(--line-soft); border-radius:2px; padding:0 4px;
  color:transparent; text-shadow:0 0 8px var(--ink);
  cursor:pointer; transition:color .15s, text-shadow .15s;
}
.spoil.open{color:inherit; text-shadow:none; background:var(--accent-soft)}
.spoil:focus-visible{outline:2px solid var(--accent); outline-offset:2px}
@media (prefers-reduced-motion:reduce){.spoil{transition:none}}
```

```js
document.addEventListener('click', e => {
  const s = e.target.closest('.spoil');
  if (s) s.classList.toggle('open');
});
document.addEventListener('keydown', e => {
  if ((e.key === 'Enter' || e.key === ' ') && e.target.classList?.contains('spoil')) {
    e.preventDefault(); e.target.classList.toggle('open');
  }
});
```

Add a "reveal everything" toggle in the header for players who finish the game
and come back. One checkbox that adds a class to `<body>`, with a CSS rule that
opens every `.spoil`, is enough.

Write the sentence so it survives the blur:

> **Good:** Beating the third major boss gives you <span class="spoil">Puppet String</span> — spend it on this caliber
> **Bad:** You need <span class="spoil">Puppet String from Scrapped Watchman, then spend it on the caliber</span>

The second one hides the instruction, not the spoiler.

**Why `minmax(0,1fr)` and not `1fr`:** `1fr` means `minmax(auto,1fr)`, so the
column grows to fit its widest child. Guides are full of wide children — tables
with a `min-width`, timelines, maps — each safely inside its own
`overflow-x:auto` wrapper, and a `1fr` column still widens the whole page around
them. Two guides shipped with every tab scrolling sideways on phones for exactly
this reason.

## Checklist tables

Where-lists, the missables table and the achievements tab share one component:
a table with a tick box per row, a running "12 / 48" counter, and ticks
persisted per list. Every list sits in its own root with a `data-key` of the
form `<slug>:<list>` and a short `data-label` ("Mask", "Fleas") used by the area
tallies below, and one script serves every root on the page.

```html
<div class="ach" data-key="hollow-knight-silksong:masks" data-label="Mask">
  <div class="ach-stat ach-prog"><b data-ach-count>0 / 20</b><span>ticks live in this browser only</span></div>
  <div class="ach-tw"><table>…
    <tr data-area="moss-grotto"><td class="ck"><input type="checkbox" data-ach="masks-1" aria-label="Mask Shard 1"></td> … </tr>
  …</table></div>
</div>

<!-- inside an area block of the walkthrough tab: filled in live from the lists -->
<p class="tally" data-tally="moss-grotto"></p>
```

```js
(function () {
  var roots = [].slice.call(document.querySelectorAll('[data-key]'));
  function tally() {                                  // "Mask 1/2 · Fleas 0/3" per area block
    [].forEach.call(document.querySelectorAll('[data-tally]'), function (el) {
      var area = el.getAttribute('data-tally'), parts = [];
      roots.forEach(function (root) {
        var bs = root.querySelectorAll('[data-area="' + area + '"] input[data-ach]'), n = 0;
        if (!bs.length) return;
        [].forEach.call(bs, function (b) { if (b.checked) n++; });
        parts.push((root.getAttribute('data-label') || '') + ' ' + n + '/' + bs.length);
      });
      el.textContent = parts.join(' · ');
    });
  }
  roots.forEach(function (root) {
    var KEY = root.getAttribute('data-key'), state = {};
    try { state = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { state = {}; }
    var boxes = [].slice.call(root.querySelectorAll('input[data-ach]'));
    var out = root.querySelector('[data-ach-count]');
    function paint() {
      var n = 0;
      boxes.forEach(function (b) {
        if (b.checked) n++;
        var row = b.closest('tr, li, [data-tick-row]');
        if (row) row.classList.toggle('done', b.checked);
      });
      if (out) out.textContent = n + ' / ' + boxes.length;
    }
    boxes.forEach(function (b) {
      var k = b.getAttribute('data-ach');
      if (state[k]) b.checked = true;
      b.addEventListener('change', function () {
        state[k] = b.checked;
        try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
        paint(); tally();
      });
    });
    root.addEventListener('click', function (e) {   // "see how not to miss it" links to another tab
      var g = e.target.closest ? e.target.closest('[data-goto]') : null;
      var t = g && document.getElementById(g.getAttribute('data-goto'));
      if (t) t.click();
    });
    paint();
  });
  tally();
})();
```

The root is any element with a `data-key`; `.ach` is only the table styling.
Tables are the usual shape, but a list item or a card works too: put the box in
the `<li>`, or in a card marked `data-tick-row` — a questline card gets one box
per step or per quest this way.

Style the table like the page's other tables; give the tick column ~34px, strike
through the name of a ticked row at reduced opacity, and keep counts and
percentages in the mono numeral face. `scripts/check_guide.py` verifies that
every `data-key` starts with the slug, that no key is used by two roots, and that
no `data-ach` repeats inside one root.

**One box per thing.** An item appears in several places — its where-list, an
area block, a missables row, an achievement — but it is ticked in exactly one:
its where-list. Everywhere else shows a live count (`data-tally`) or a
`data-goto` link to the tab that holds the list, never a second box. (Point
`data-goto` at a tab button, never at a checkbox — the script clicks its
target.) Two boxes for one Mask Shard drift apart within a
session and the player stops trusting both.

**Area tallies replace hand-written counts.** Give each where-list row a
`data-area` (the area block's id) and put a `data-tally` line in the block; the
script fills it. A static "masks 2 · fleas 3" line cannot show what the player
has already picked up.

### Moving ticks between browsers

Ticks live in `localStorage`, which belongs to one browser and one page origin:
the same guide opened standalone and inside a hub are two separate stores, and
clearing site data wipes both. Every guide with at least one tick box ships one
export/import block, in the footer:

```html
<details class="ticks-io" data-slug="hollow-knight">
  <summary>Back up or move your ticks</summary>
  <p>Ticks are saved in this browser only. Export copies them as text; paste
     that text into this guide somewhere else and press Import.</p>
  <textarea rows="3" spellcheck="false" aria-label="Ticks as text"></textarea>
  <div class="io-row"><button type="button" data-io="export">Export</button>
    <button type="button" data-io="import">Import</button> <span data-io-msg role="status"></span></div>
</details>
```

```js
[].forEach.call(document.querySelectorAll('.ticks-io[data-slug]'), function (box) {
  var slug = box.getAttribute('data-slug'), pre = slug + ':';
  var ta = box.querySelector('textarea'), msg = box.querySelector('[data-io-msg]');
  function say(t) { if (msg) msg.textContent = t; }
  box.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-io]') : null;
    if (!b) return;
    if (b.getAttribute('data-io') === 'export') {
      var data = {};
      try {
        for (var i = 0; i < localStorage.length; i++) {
          var k = localStorage.key(i);
          if (k && k.indexOf(pre) === 0) data[k] = localStorage.getItem(k);
        }
      } catch (err) { say('Storage is unavailable here'); return; }
      ta.value = JSON.stringify({ guide: slug, v: 1, data: data });
      ta.select();
      try { navigator.clipboard.writeText(ta.value).then(function () { say('Copied'); }, function () { say('Select the text and copy it'); }); }
      catch (err) { say('Select the text and copy it'); }
    } else {
      var d;
      try { d = JSON.parse(ta.value); } catch (err) { say('That is not backup text'); return; }
      if (!d || d.guide !== slug || !d.data || typeof d.data !== 'object') { say('That text belongs to another guide'); return; }
      var n = 0;
      try {
        Object.keys(d.data).forEach(function (k) {
          if (k.indexOf(pre) === 0 && typeof d.data[k] === 'string') { localStorage.setItem(k, d.data[k]); n++; }
        });
      } catch (err) { say('Storage is unavailable here'); return; }
      say('Imported ' + n + ' list(s), reloading');
      setTimeout(function () { location.reload(); }, 400);
    }
  });
});
```

It exports every key under the guide's slug, so questline ticks written by
older code are carried too. Import replaces the lists it contains and leaves
the others alone; it never touches another guide's keys, which matters inside a
hub where every guide shares one store. Do not reach for a shared runtime
database instead: on a page shared by link, every viewer would read and write
the same ticks.

## The ranked list

"Things I wish I knew" and most of the short rule-lists in these guides are a
numbered list where a bolded claim sits above a muted consequence line, with the
number in its own gutter. Use this:

```css
ol.ranked{list-style:none; counter-reset:r; padding:0; margin:0}
ol.ranked > li{counter-increment:r; display:grid;
               grid-template-columns:30px minmax(0,1fr); gap:12px;
               padding:13px 0; border-bottom:1px solid var(--line-soft)}
ol.ranked > li::before{content:counter(r); grid-column:1; color:var(--accent)}
ol.ranked > li > b{grid-column:2; font-weight:600}
ol.ranked > li > span{grid-column:2; color:var(--ink-soft)}
```

**`::before` is a grid item.** That is the whole reason for the explicit
`grid-column` on every child. A two-column track with a counter `::before` and
two real children has *three* items, so the third lands in an implicit third
column sized to min-content — and a paragraph in a min-content column renders
one word per line, top to bottom, for the entire list. It looks like a font or
RTL failure rather than a layout one, so it is easy to misdiagnose.

The same trap fires anywhere a counter or icon pseudo-element shares a grid with
real children. When a grid's children are not all direct siblings you placed by
hand, either pin each one with `grid-column` or wrap the content in a single
element so the grid only ever sees the items you counted.

## Area maps with the route drawn on them

Built when `metroidvania.md` is in play, or any time the player says they keep
getting lost. The figure is the game's own area map with your numbered route
pins on top, and it is the only place in these guides where a real game asset
beats anything you could draw.

**Getting the maps.** Game wikis publish two variants per area: a clean one that
matches the in-game map screen, and an annotated one with the wiki's own icons
for benches, collectibles, NPCs and shops. Prefer the annotated one — it is
accurate work you do not have to redo, and the reader cross-references it
against their own map. Fall back to the clean one where no annotated version
exists, and say so under that map.

MediaWiki serves thumbnails at `…/images/thumb/a/ab/Name.png/300px-Name.png`;
strip `thumb/` and the trailing `NNNpx-…` segment for the original. Asking for a
width larger than the original 404s, so take the original rather than guessing a
size. Send a normal user agent and a referer — wiki CDNs reject bare requests.

**Publish them as supporting files, not data URIs.** The CSP blocks external
hosts, which is why hotlinking fails, but files published alongside the page are
same-origin and load normally. Pass them in `files` (`"maps/greenpath.png"`) and
reference the published path from the page. A dozen area maps run 3–6 MB; as
data URIs that is a page approaching its own size cap for no reason, while as
supporting files the HTML stays small and each map is fetched only when its
`<img loading="lazy">` scrolls in. Keep them in the guide folder as
`game-guides/<slug>/maps/*.png` so the local copy and a hub carry them too.
Credit the wiki and the studio in the footer and in `guide-meta.image_credits`;
the delivery message carries the share-publicly line (SKILL.md §6).

**The overlay.** Percentage-positioned pins over a relatively-positioned image,
so they hold their place at every width:

```css
.mapwrap{position:relative; display:block; border-radius:10px; overflow:hidden; line-height:0}
.mapwrap img{display:block; width:100%; height:auto}
.pin{position:absolute; transform:translate(-50%,-50%); width:26px; height:26px;
     border-radius:50%; background:var(--accent); color:#14100a; text-align:center;
     line-height:26px; font-size:.82rem; font-weight:600;
     box-shadow:0 0 0 2px #fff, 0 2px 6px rgba(0,0,0,.7)}
.pin.exit{background:#e8eaf0; box-shadow:0 0 0 2px var(--accent), 0 2px 6px rgba(0,0,0,.7)}
```

```html
<span class="pin" style="left:36%;top:55%">2</span>
<span class="pin exit" style="left:4%;top:69%">A</span>
```

Two pin vocabularies, and only two: **numbers for the order to walk it**,
**letters for exits**. The number pins key to a numbered step list under the
map; the letter pins key to an exits strip naming what lies through each edge.
Both need the white/gold double ring — these maps are near-black, and a flat
coloured dot vanishes into them.

**Place only what you can actually verify.** Map edges and exits are reliable
because the corridors are visible and the wiki's area page lists the
connections. Sub-areas printed on the map itself are reliable because you can
read them. A specific room's position on an abstract layout usually is not, and
a pin that sends a player to the wrong side of a region costs more than the pin
saved. Put a line under the legend saying pins mark order and direction rather
than exact rooms, and let the step text carry the precision instead. Four to
seven pins per map; past that the map is doing the step list's job badly.

**One tab, an area switcher inside it.** Fourteen areas cannot each have a rail
tab. Put a chip row at the top of the panel as a nested `role="tablist"` with
Left/Right plus Home/End, one `role="tabpanel"` article per area, and number the
chips so the switcher itself teaches the route order.

## Tab contents

`references/fixed-tabs.md` holds the render spec for the three fixed tabs and
for the questline tab — list versus table, which column carries the weight, how
the cards are shaped. Read it alongside this file; it assumes the shell
described here.

## Diagrams

Load `artifact-diagramming` when the page needs figures and the skill is
available; otherwise draw them as inline SVG with `currentColor` strokes and the
colour tokens, a `<title>` for each figure, and text at least 12px. Game guides
earn figures in specific places:

- **The budget** — what you have versus what full upgrades cost, as two bars.
  This single figure carries the guide's whole thesis.
- **A fork** — one input, two outcomes, one of them locked. Draw the lock.
- **A timing window** — when something becomes available and when it closes,
  on a line, with the closing event named.
- **A loop** — the routine the player repeats per area or per run, with the step
  people skip marked.
- **Where the limited resource lives** — a horizontal bar per region. This makes
  "half of it is in the back third of the game" visible instantly, which changes
  how a player paces their spending.

Skip decorative diagrams. A box labelled with a system's name teaches nothing a
heading does not.

## Icons

Hand-drawn line SVGs in a hidden sprite (`<symbol>` + `<use>`), stroked in
`currentColor` so they follow the theme. Two sizes: one for section headings,
one inline for table rows.

Group by category rather than drawing one per item — a spear glyph shared by
every polearm reads as a deliberate system, while sixty near-identical bespoke
glyphs read as noise and cost far more to make. Categories worth having:
weapon/tool classes, effect types (damage, defence, utility, healing), and
resource types.

Emoji as section markers looks generated; draw the glyphs.

## Embedding real art (only when asked)

Artifact pages run under a CSP that blocks external hosts, so `<img src="https://…">`
silently fails. Download the files and ship them with the page instead.

If the player asks for it:

1. Find the image URL from the item's wiki page rather than guessing filenames.
2. Download with a normal user agent and a referer header; wiki CDNs reject bare
   requests.
3. Prefer the small/thumbnail variant — a 200px PNG is usually 5–20 KB.
4. Ship every image as a **file in the guide folder**, never as base64 — maps
   and screenshots under `maps/`, item art under `images/` — and publish them as
   supporting files. **Small glyphs that repeat across tabs** still get paid for
   once: one `<symbol>` per icon holding
   `<image href="images/quartz.png" width="64" height="64"/>`, referenced with
   `<use href="#i-quartz">` wherever it appears. Base64 bloats the HTML (one
   guide carried 55 icons as 823 KB of text, 81% of its file) and the output
   contract forbids it.
5. Credit the wiki and the studio in the footer, and list the files in
   `guide-meta.image_credits` so the delivery message can carry the
   share-publicly line.

Verify at the end that every `<use href="#…">` resolves to a symbol that exists,
that every `src` / `href` points at a file that exists in the guide folder, and
drop symbols nothing references. `scripts/check_guide.py` checks the paths.

## Saved state

When the page remembers something — ticked quests, a chosen build — use
`localStorage` with keys that start with the slug: `hollow-knight:quest-ticks`.
Guides share an origin inside a hub, and a bare `quest-ticks` from two guides
would overwrite each other. Wrap every access in `try/catch`; storage can be
unavailable, and the page must still work without it. Any page that saves
ticks also carries the export/import block from "Checklist tables".

## Footer

State the sources, the patch the numbers appear to describe, and — when
relevant — the art credit. A guide that says where its numbers came from is one
the player can check and correct.

Write it so it is true wherever the page is opened: no "this is a private page",
no "tell Claude and I will fix it". If a number is unconfirmed, say so and say
what would confirm it; the player knows how to ask for an update.
