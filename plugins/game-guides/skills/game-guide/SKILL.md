---
name: game-guide
description: Build a spoiler-safe, personalised "how to play this game" guide for a specific video game, delivered as a self-contained tabbed HTML page (published as an Artifact where available) — covering progression systems, builds, limited resources, missable content and the decisions a player cannot undo. Use this whenever someone is about to start (or restart) a game and wants to know how to play it well, asks for a beginner guide / build guide / "what should I know before playing X", wants a checklist of missable things, asks whether a quest or NPC can still be completed or has been locked out, asks what to spend a limited currency or upgrade material on, or asks you to plan a playthrough — even if they never say the word "guide". Also use it when they ask to update or extend a guide you previously built.
license: MIT
compatibility: Best in Claude Code signed in with a claude.ai account (local folder + Artifact with supporting files). Elsewhere it writes a local HTML file, or returns the HTML in chat when files cannot be written. Needs web access for research.
metadata:
  contract: "1"
---

# Game guide builder

A good game guide is not a feature dump. Wikis already list every item; that is
not what a player needs on the night they start playing. What they need is the
shape of the game's **irreversible decisions** and **scarce resources**, in the
order they will meet them, without being told what happens in the story.

That is the whole job. Everything below serves it.

## What makes these guides good

Three things, in priority order:

1. **The spine is scarcity, not content.** Almost every game has a small set of
   things that cannot be refilled or undone in one run: a currency with a fixed
   total, an upgrade material you can only spend once, a fork where picking A
   permanently locks B, a piece of content that vanishes when a chapter ends.
   Find those first. The guide is organised around them; the rest is trimming.

2. **Every recommendation carries its budget.** "Upgrade this early" is advice.
   "There are 25 of these in the whole game and full upgrades cost 56, so you
   will open 11 of 20 nodes — here is the order" is a guide. Players trust
   numbers they can verify against their own inventory.

3. **It respects what they have not seen yet.** A guide that spoils the game it
   is teaching has failed even if every fact is right.

## Workflow

### 1. Scope interview — short, then move

Ask up to four questions in a single batch, each with a recommended answer, then
start working. Use `AskUserQuestion` — it takes up to four questions at once and
makes each one a tap, which is exactly the shape this interview wants. Where
that tool is not available, ask them as one numbered list in a single message
with your recommendation marked on each. Do not interrogate; the player wants to
be playing.

The questions worth asking (adapt, drop any you can already infer):

- **Where are they?** Never played / played before and restarting / mid-run and
  stuck. This sets the spoiler line — someone restarting has already seen the
  story and may want the fast version.
- **Goal this run?** Finish the story quickly / collect most things but not 100%
  / full completion. This changes almost every recommendation downstream.
- **Version and edition?** Platform, patch, DLC owned. Numbers drift between
  patches and a guide quoting pre-patch values is worse than no guide.
- **Any direction already chosen?** A class, a faction, a starting character. If
  they have picked, build around it; if not, offer the choice as a tab rather
  than deciding for them.
- **Which language?** Only when you cannot infer it — and usually you can, since
  they just wrote to you in one. Ask it when the signals disagree, such as a
  player writing in one language whose game client runs in another. In-game
  proper nouns stay in the game's own language whatever they answer (see §4).

If they answer "just make it", pick the sensible defaults, say which you picked
in one line, and go.

### 1b. Asking again mid-build

The interview above is short on purpose, and it is the only batched one. But
building a guide surfaces questions that could not have been asked upfront —
they do not exist until the research is in. Those get asked when they appear,
not saved up and not guessed at.

Borrow the shape from the `grilling` skill: **one question at a time, each
carrying your recommended answer, then wait for it.** Use `AskUserQuestion` so
the options are one tap; where it is not available, ask in plain text with the
options listed and your recommendation marked — still one question per message.
Two questions in one message is a form, and a form gets skimmed and answered
wrong. What you do not borrow is the relentlessness —
grilling walks every branch of a design tree because the interview *is* the
deliverable. Here the guide is, and every question is time the player is not
playing.

**The rule that keeps this useful: never ask a question research can answer.**
Counts, costs, caps, locations, mechanics, whether something is missable — go
and find out. A guide that asks the player how many upgrade materials exist has
inverted its own job. Put to them only what *they* decide and you cannot.

Stop and ask when one of these lands:

- **The spoiler line is genuinely unclear.** They are mid-run and the research
  covers content ahead of them. Gate it, omit it, or both? You cannot infer how
  much they want to know about what is coming, and guessing wrong is
  unrecoverable in one direction.
- **Sources conflict on a number the plan is built on.** Printing the range
  handles display; when 16 versus 17 changes the spend order, the fork is
  theirs. Offer both plans in one line each.
- **Research contradicts the goal they gave.** They said finish quickly, and the
  game turns out to wall off a third of itself behind a detour. That trade is
  not yours to make quietly.
- **Two builds genuinely both work and feel completely different.** `rpg.md`
  says do not crown one — but when they gave no direction and the two are far
  apart in how they play, one question beats guessing, and beats a tab that
  refuses to choose.
- **The sources are too thin to support the guide.** Ship it thin now, or widen
  the search first? Their time, their call.
- **The game is a hybrid and the candidate spines disagree.** Which scarcity the
  guide organises around changes every tab. If reading two genre references does
  not settle it, ask.
- **Completion needs more than one playthrough.** "Collect most things" means
  something different when the game wants three runs.

Do not stop for: which tabs to build, how to lay the page out, permission to
proceed, anything the scope interview already answered, or anything one search
would settle.

**Cap it at two or three stops across the whole build**, and fold anything that
surfaced in the same research pass into one moment rather than interrupting
three times.

**When they said "just make it", stop asking entirely.** Turn every one of these
into a stated assumption: pick the sensible answer, keep building, and list what
you assumed when you hand the page over. Same for a player who has clearly
walked away. Never leave a guide unfinished waiting on an answer — build
everything the question does not block, and ask alongside the delivery instead
of before it.

### 2. Research — two sources per number

Read `references/research.md` before starting. The short version:

- Prefer the game's main wiki plus one completionist/trophy site; those two
  disagree often enough to be worth cross-checking, and where they disagree the
  honest move is to print the range and say the sources conflict. Never
  silently pick one — a confidently wrong count is the failure mode players
  punish hardest.
- Hunt specifically for the scarcity structure: totals, caps, one-time choices,
  chapter lockouts, points of no return. Search terms like "all X locations",
  "missable", "point of no return", "how many X in the game".
- Note the patch the sources describe. Say so in the page footer.
- **When the sources are not there, say so and shrink the guide.** New,
  early-access, small-studio and non-English-community games often have no wiki
  worth the name. This is the highest-risk moment in the workflow, because the
  guide format has slots, slots invite filling, and plausible numbers are easy
  to produce. Do not. The rules are in `references/research.md` under "When
  research comes up empty".

### 3. Find the spine before writing anything

Pick the genre reference that fits and read it — it tells you where that genre
hides its irreversible decisions:

| Genre | Reference |
|---|---|
| RPG / JRPG / CRPG / action-RPG | `references/rpg.md` |
| Metroidvania, search-action | `references/metroidvania.md` |
| Management, city-builder, 4X, colony sim | `references/management.md` |
| Roguelite, deckbuilder, extraction | `references/roguelite.md` |
| Sim, survival, crafting, farming, exploration | `references/sim-survival.md` |
| Gacha, live-service, gear-chase | `references/gacha.md` |

Most games are hybrids. Read two references and take what applies rather than
forcing the game into one mould. If the game fits none of them cleanly, work
from the same underlying question anyway: *what can this player spend, choose,
or walk past exactly once?*

One caveat on that question, because it has an assumption buried in it: it
expects a **fixed total** to exist and be findable. In live-service games it
does not. The budget there is a rate — income per patch cycle — and the windows
close on a calendar, so "how many are there" has no answer and every
recommendation has to carry a date instead. If the game you are guiding runs on
a patch cycle, read `gacha.md` before deciding the spine, even when another
reference also fits.

Then decide the tab list. Tabs are not a fixed template — they come from what
this particular game actually makes you decide. A deckbuilder has no
"amulets" tab and a colony sim has no "boss rewards" tab. What generalises is
that each tab should answer a question the player will actually ask, in the
order they will ask it.

Three tabs are always there regardless of genre, because every player asks
these three questions about every game:

- **"Before you start"** — first tab, read before the game launches
- **"Things I wish I knew"** — third, right after the loop tab
- **"Do this or lose it forever"** — at the end

All three are covered in their own section below; build them for every guide,
even when one of them comes out short.

Between them, tabs come from what this particular game makes you decide. A
reliable order, dropping whatever does not apply:

1. **Before you start** — always, first
2. **The loop and the budget** — the routine to repeat, the scarce-resource
   budget. Name the tab for what it holds. "Start here" says nothing about its
   contents and, sitting directly under "Before you start" in the rail, leaves
   the reader with two signposts and no way to tell them apart.
3. **Things I wish I knew** — always
4. **Pick your build/approach** — the real options with trade-offs, not one
   blessed path
5. **The main progression system** — how it works, then the spend order
6. **Walk it area by area** — whenever the game's own difficulty is knowing
   where to go next: one tab holding the ability order, an area switcher, and
   per area a map with the route pinned on it. Mandatory for metroidvanias, and
   worth building for any open or maze-like world the player says they get lost
   in (see `references/metroidvania.md`)
7. Whatever other systems the game hangs its decisions on (one tab each)
8. **NPC questlines** — whenever the game has chains that advance on world
   progress rather than on a quest log (see 3c)
9. **Irreversible choices** — the forks, laid out so both sides are visible
10. **Route / collection lists** — where the limited things are
11. **Do this or lose it forever** — always
12. **Completion** — only if they asked for it

**Budget: twelve tabs.** Three fixed plus a questline tab leaves about eight for
everything else, and `references/page-build.md` puts the rail's hard ceiling at
fifteen. Games with many systems blow straight through that, so when the list
runs long, merge in this order and stop as soon as it fits:

1. **Small systems merge first.** Two systems that feed one decision become one
   tab. A system the player can safely ignore on a first run gets a line in
   "Things I wish I knew" saying exactly that, and no tab at all — saying which
   systems are noise is real advice, not a concession to the tab budget.
2. **Route folds into the collection list.** A route is an ordering of the same
   places; one tab holds the list and the order together. Where a "walk it area
   by area" tab exists it has already absorbed the route, and the ability-order
   table belongs inside it rather than in a tab of its own — but it never
   absorbs the collection lists, because a player sweeping for the last four
   collectibles wants them in one list, not spread across fourteen area blocks.
3. **Completion appends to "Do this or lose it forever"** instead of standing
   alone — unless they asked for full completion, in which case it stays and
   something else merges.
4. **The three fixed tabs never merge, and the questline tab never merges into
   the missables table.** That last merge destroys the chain ordering, which is
   the entire reason the questline tab exists.

### 3b. The three tabs every guide has

Three tabs exist in every guide regardless of genre.
`references/fixed-tabs.md` holds the quality bar and the render spec for each —
read it when you lay out the tab list. What has to be settled here is only which
of them a given fact belongs to, because they cover adjacent ground:

| The thing is… | It goes in |
|---|---|
| Set in a pre-game menu or character creation, before the world exists | Before you start |
| A one-way door met during play | Do this or lose it forever |
| A mechanic the game never explains | Things I wish I knew |
| The routine repeated every session, and the budget | The loop and the budget |

When something genuinely fits two, put it where the player is standing when they
need it, and cross-reference rather than duplicating.

Build all three even when one comes out short. A thin "Do this or lose it
forever" is a finding about the game, not a gap in the guide, and
`fixed-tabs.md` says how to write it so it reads that way.

### 3c. NPC questlines — sweep every game, tab it when it earns one

Run this check on every guide regardless of genre. Most games fail it and that
costs one search; the games that pass it are the ones where this single category
produces more "I lost it and never knew" than everything else combined.

**The check:** does the game have NPC or companion chains that advance on
**world progress** — a boss killed, an area entered, a chapter turned — rather
than on a quest log the player can consult?

**If yes,** the guide gets a questline tab, and `references/fixed-tabs.md` has
what each chain needs and how to keep it spoiler-safe. The souls-like family is
the archetype, but the same shape turns up in immersive sims, CRPGs with
companion arcs, and any game where an NPC relocates or disappears when the world
state moves. Why the missables table cannot absorb it: a questline is an ordered
chain, not one event; its deadlines are keyed to world progress rather than to a
clock; and in these games there is usually no in-game tracking at all, so the
guide *is* the quest log.

**If no,** do not make a tab. Confirm it with a direct search rather than from
memory, and if the answer is itself interesting — a game that deliberately lets
you return to everything — put one line in "Do this or lose it forever" saying
so.

### 4. Build the page

Read `references/output-contract.md` first — it fixes what every guide must be
at its edges (a complete HTML document, the embedded `guide-meta` block, where
files go, how it is published) so that the page works as an Artifact, as a local
file, and inside a hub of guides. Then read `references/page-build.md` for the
page structure, the spoiler gate, the diagram approach and how icons work, and
`references/fixed-tabs.md` for how each fixed tab renders. If the
`artifact-design` skill is available, load it before writing the file; if it is
not, follow the design baseline in `page-build.md`.

Three things specific to this kind of page:

- **Title the page with the game's name, exactly and only.** `Len's Island`, not
  `Bridgewater Field Notes`; `Lies of P`, not `Krat Field Manual`. Evocative
  titles read well in isolation and fail at the one job that matters here: a
  player scanning a gallery of guides months later needs to spot the game they
  are about to play, and they will search for its name, not for a phrase you
  invented. A game's title is already specific and distinctive — it is the
  strongest possible name for the page. Skip subtitles and appended explainers
  too; the one-sentence publish `description` is where "spoiler-free starter
  guide for a first run" belongs, and the gallery shows it directly under the
  title. If the player ever has two guides for the same game, differentiate
  them in that description rather than by decorating the title.
- **Write in the player's language** — the one settled in the scope interview,
  or the one they wrote to you in. Every part of the page follows it: headings,
  table headers, button labels, `aria-label`s. Keep in-game proper nouns in the
  game's own language — they need to match what is on screen and what wikis are
  searchable by.
- **Numbers get their own visual weight.** Budgets, totals and costs are the
  reason the page exists; put them in tables and small charts, not buried in
  sentences.

### 5. Verification pass — do this every time, it always finds something

Before handing over, re-read what you wrote against your research notes and
check specifically for:

- **Totals that do not sum.** If a table lists locations for a resource, add them
  up and compare to the stated total. Mismatches are the most common error and
  the easiest to catch.
- **Claims you inferred rather than read.** Anything you reasoned your way to
  ("so this must scale off X") needs a source or a hedge.
- **Internal contradictions.** A cost quoted differently in two tabs; a plan
  that spends more than the budget allows; advice in one tab that a rule in
  another tab forbids.
- **Names you never verified exist.** Item and ability names are easy to
  half-remember. If a name never appeared in a source, say so or drop it.
- **Map pins you placed from memory.** For every pin, name what told you where
  it goes — a visible corridor at that edge, a label printed on the map, the
  wiki's connection list. Pins failing that test get moved to the step text.
  Then confirm every image path you reference was actually published.

Then two checks that are not about numbers, and are not optional:

- **Read the gated sentences, not the whole page.** A sentence can only fail the
  gate if it contains one, so read just the sentences holding a `.spoil` span,
  each with the span's text struck out. If what remains no longer carries the
  instruction, that is a redaction rather than a gate — rewrite it so the span
  holds only the identity. Mandatory on every guide that has a gate, which is
  every guide except one for a player who said they have finished the game.
- **Grep the visible layer against your spoiler list.** Take the proper nouns
  you set aside during research and search the finished page for each. Every
  occurrence must sit inside a `.spoil` span. This catches the opposite failure
  — a name that leaked into visible text — and it is a string search rather than
  a reading pass, so it costs almost nothing and there is no excuse to skip it.
  Most hits come from the questline tab.
- **Confirm the questline sweep ran.** Either the guide has a questline tab, or
  you can name the search that told you the game has none. Quietly skipping this
  is how the highest-loss category goes missing.
- **Check the contract.** Run `scripts/check_guide.py game-guides/<slug>` when
  Python is available; otherwise walk the checklist at the end of
  `references/output-contract.md` by hand. It catches a missing `guide-meta`
  field, a base64 image, an absolute asset path or an un-prefixed
  `localStorage` key — mechanical slips that break the page inside a hub.

Then tell the user plainly what you corrected. Finding four errors in your own
draft and saying so builds more trust than a clean-looking guide that is wrong.

### 6. Publish — every tier that is available

`references/output-contract.md` has the detail. In short, in this order:

1. **If you can write files**, write `game-guides/<slug>/index.html` plus its
   assets under the working directory. Always — this is the portable copy.
2. **If the Artifact tool is available**, publish the page with its assets as
   supporting files, the game's name as the title and `summary` as the
   description. Write the returned URL into `guide-meta.artifact.url` and save
   the local copy again.
3. **If neither is possible**, return the complete HTML in the reply.

Tell the player where the guide ended up. If `guide-meta.image_credits` is not
empty, add one line: the images belong to the studio or wiki, they are fine in
a private page, and they should come out before the page is shared publicly.

## Spoiler discipline

**The gate is mandatory, not a default.** Every guide ships with reveal-on-click
unless the player has explicitly said they have already finished the game. "They
did not ask for spoiler protection" is not an exemption — a player about to
start a game cannot know which facts would have spoiled it for them, which is
precisely why the guide decides this and not them.

Reveal-on-click means the guide reads completely at a glance without exposing
story, and anything that would spoil sits behind a blur the reader taps when
they want it.

What to hide:

- Character, boss, region and item **proper nouns** that reveal story content —
  a boss's name often gives away who they turn out to be
- Anything about **who** someone is, **why** something happens, or how a plot
  thread resolves
- Late-game and post-game content the player has not reached
- Ending conditions and choice consequences — hide the outcome names, keep the
  mechanical instruction visible

What stays visible:

- Systems, numbers, budgets, costs, caps
- Positional references: "the third major fight", "the swamp region", "the
  chapter after you unlock fast travel"
- Anything the game itself puts on the menu screen before you play

Write the **visible layer so it stands alone**. A reader who never opens a single
blur should still be able to follow the whole guide. The hidden text adds
precision (which boss, which NPC), not the instruction itself. Getting this
right is the difference between a spoiler-safe guide and a redacted one.

The only exemption is a player who says they have already finished the game.
Then skip the gating and say in one line that you are skipping it and why —
never skip it silently, and never infer "they have probably played it" from
anything short of them saying so. Someone restarting a game is still covered by
the gate for anything they might not have reached.

Whatever they say, the closed-blur read in the verification pass still runs
whenever a gate exists.

## Fetching real game art

Draw the icons yourself by default — small line SVGs, one per item category. It
looks deliberate, costs nothing, and sidesteps the question entirely.

If the player explicitly asks for real item art, it is their call and you can do
it: artifact pages cannot hotlink external images (the CSP blocks it), so
download from the game's wiki and ship the files with the page as files under
`images/` or `maps/` — never as base64 — credit the wiki and the studio in the
footer, and record them in `guide-meta.image_credits`. A credit is not
permission: studio art is rarely licensed for reuse, so the delivery message
says the page should lose those images before it is shared publicly (see §6).
Do not do this unprompted, and do not do it at a scale that turns the
page into a redistribution of a wiki's image library.

**Area maps are the exception that proves the rule.** For a player who says they
keep getting lost, the game's own map with a route drawn on it is the answer to
their question, and no glyph you draw substitutes for it — so fetch those
without waiting to be asked a second time, and publish them as supporting files
rather than inlining them. `references/page-build.md` has the sourcing, the pin
overlay and the honesty rule about how precisely you may place a pin.

## Updating an existing guide

Guides get revisited — a new question, a correction, a system the player only
now cares about. Keep the same `slug`: overwrite `game-guides/<slug>/`, bump
`guide-meta.updated`, and republish the same artifact URL rather than creating a
second page; a guide that lives at one link is a guide they can bookmark.

**What counts as the same guide.** Adding 100% completion to a guide is a new
Completion tab, not a new guide. A DLC or a separate kind of run that deserves
its own guide gets a new `slug` with a suffix (`elden-ring--shadow-of-the-erdtree`),
the same `game`, and its own `variant` label — `references/output-contract.md`
has the rules.

**Upgrading an older guide.** A guide built before the output contract existed
has no `guide-meta`, may be an HTML fragment rather than a full document, and
may embed images as base64. When asked to update one — or when a hub hands one
over for upgrade — bring it to the current contract as part of the update: wrap
it in a full document with `lang`, infer the `guide-meta` fields from the page
(title, footer sources, patch, dates) and show the player what you inferred,
move embedded images out to files, prefix `localStorage` keys with the slug
while carrying existing saved values over, and replace host-specific footer
wording. Change nothing else unless asked.

When new research contradicts what the page says, fix the page and say what
changed. Players act on these numbers.

Re-run the checks that the change touches, not the whole verification pass: if
you changed a number, re-total the table it belongs to and any plan that spends
it; if you added content the player has not reached, the two spoiler checks in
§5 run again on what you added.

**Games on a patch cycle age differently.** A single-player guide stays true
until a balance patch, which may never come. A live-service guide starts
drifting on a schedule — new banners, new units, changed income, an event shop
that no longer exists — so its numbers have a shelf life measured in weeks. For
those guides:

- **Put the expiry on the page**, next to the patch note in the footer: which
  cycle the numbers describe and roughly when they stop being true.
- **Treat the calendar tab as the first thing to re-check**, because it is the
  first thing to go stale and the one the player acts on soonest.
- **Do not quietly refresh a tier list without saying so.** The player may have
  already spent on your last recommendation; tell them what changed and whether
  it invalidates what they did, which it usually does not.
