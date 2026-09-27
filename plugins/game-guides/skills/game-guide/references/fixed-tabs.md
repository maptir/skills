# The fixed tabs

Quality bars for the four tabs every guide has, plus the questline tab when a
game earns one. SKILL.md decides *whether* each of these exists and what belongs
in which; this file decides what makes each one good. Read it when you lay out
the tab list, before writing.

Examples here are in English. Write the page in the player's language.

## "Before you start"

Everything decided before the game is running, plus everything that stops being
actionable the moment it is. This tab has a short shelf life by design — the
reader opens the guide before clicking New Game, acts on it, and never needs it
again. That is exactly why it is a tab and not a block inside the loop tab: a
player consulting the guide mid-run should be able to skip it from the label.

Sweep these, in this order:

- **Difficulty and mode.** Which one, and — the part guides skip — whether it
  can be changed later. Many can. Say so.
- **World, seed and map generation.** Locked for the save's whole life in most
  management, survival and farming games, and often the single biggest
  determinant of how the run goes.
- **Character creation.** What is cosmetic, what is mechanical, what is
  permanent. Class or origin belongs here only as far as "pick now vs pick
  later"; the build reasoning itself belongs in the build tab.
- **Version, patch and DLC state.** Whether DLC content is injected from the
  start (and whether that unbalances a first run), whether to install it later,
  and which patch the guide's numbers assume.
- **Mods, if the game has a scene.** Only the ones that must go in before the
  first save, and only quality-of-life ones — never content mods on a first run.
- **Settings worth fixing once.** FOV, motion blur, subtitle size, key rebinds,
  autosave frequency, accessibility options. Cheap to set, infuriating to
  discover forty hours in.
- **Save slot strategy.** In a game with heavy missables or branching endings,
  "keep a second save before chapter N" is the highest-value sentence on the
  page. Say whether the game even allows manual slots.

**Every genre has content here**, including the ones that look like they do not.
A roguelite still has a starting character, a seeded/unseeded choice and the
expectation that losing is normal; a linear action game still has save slots and
a difficulty that may or may not be changeable mid-run. If a game genuinely
locks nothing before launch, say that in one line and keep the settings, save
and version rows.

### Rendering it

A table, and the last column does the work:

| Setting | What to pick | Changeable later? |
|---|---|---|

That column is the point of the tab: most pre-start anxiety is *am I locking
myself in*, and for about half of these rows the honest answer is no, you are
not. Answering it removes real friction, and no wiki ever answers it, because it
is not a fact about the game — it is a fact about the worry.

Use the same three-state pill there as in the missables table — changeable
freely, changeable at a cost, locked for this save — so the two tables teach one
vocabulary rather than two. Put the locked rows first; they are the reason the
tab exists. Keep the whole thing short enough to act on in one sitting, because
that is literally how it is read: guide open on a phone, game sitting on the
title screen.

## "Things I wish I knew"

A ranked list of what a new player would otherwise learn the hard way. Aim for
eight to fifteen entries; the count follows what actually clears the bar.

**The bar: the game does not teach it.** If a tutorial popup, tooltip or the
controls screen already says it, cut it — repeating the tutorial wastes the
reader's attention on the one list they are most likely to read. What belongs
here is the mechanic the game mentions once and never explains, the interaction
nobody notices for ten hours, the habit experienced players formed and never
wrote down.

Rank by **how much time or frustration it saves**, not by how clever it sounds.
The entry that saves an hour goes above the entry that saves ten seconds even if
the second one is more interesting.

Include reassurances, not only warnings. "You cannot permanently ruin your
character — respec is cheap" is worth as much as any optimisation tip, and
almost never appears in wikis, because reassurance is invisible to people who
already know. New players are carrying anxiety the guide can simply remove.

Shape each entry as a claim plus a consequence: the bolded thing they should
know, then one line on why it matters or what to do instead. Anything needing a
paragraph belongs in its own tab with a pointer from here.

Good hunting grounds: community "things I wish I knew before playing" threads,
beginner-mistake videos, and — underrated — negative and mixed reviews, where
people describe exactly what confused them.

### Rendering it

A numbered list, not a table — it is read top to bottom once, and numbering
makes the ranking visible. Bold the claim, follow with one muted line of
consequence. Keep every entry to two lines at the rendered width; anything
longer is a tab of its own with a pointer here.

`page-build.md` has the CSS under "The ranked list", including the grid trap
that silently renders the whole list one word per line. Copy it rather than
writing the layout fresh.

## "Do this or lose it forever"

The list of one-shot actions and closing windows. Sweep these categories
deliberately rather than trusting recall; each is a place games hide one-way
doors:

- **Choices made once at the start** — mode, difficulty, character creation,
  world settings. Note which of these can actually be changed later; many can.
- **Exclusive trades and rewards** — one currency, two possible rewards
- **Timed or chapter-gated content** — quests, shops and events that vanish when
  progress advances
- **NPC questlines** — chains that advance on world progress rather than on a
  quest log. Big enough in some games to need their own tab; see below
- **Consumed uniques** — an item that can be spent for a small benefit or saved
  for a large one
- **Mutually exclusive allegiances** — factions, companions, romances, endings
- **Points of no return** — where the game stops letting you back out, and what
  it should be checked against before you cross
- **Achievement conflicts** — two trophies that cannot happen on the same save

Give each entry: what triggers the loss · what you lose · when the window shuts
· whether it comes back in NG+ or another run. Order by when the player meets it
so the tab doubles as a timeline.

Add the signal that tells them they are close. "The game asks you to confirm
before boarding the ship" is more useful than "there is a point of no return in
chapter 9".

**A short list is a finding, not a failure.** Some games — many survival,
sandbox and sim games — genuinely lock almost nothing. When that is true, say so
plainly at the top of the tab and explain what the game rations instead. Telling
a player "you can relax, this game does not take things away from you; what it
takes is time" is one of the most useful sentences a guide can contain, and
padding the tab with fake stakes to look thorough would destroy it.

### Rendering it

A table, because the reader scans it looking for the row that matches where they
currently are:

| ✓ | Where | What you miss | What you lose | Get it back? |
|---|---|---|---|---|

Order rows by when the player meets them, so the table reads as a timeline. Use
a pill in the last column with three distinct states — recoverable this run,
recoverable only in a new run, and gone for good on this save — and keep the
colours consistent with the rest of the page's warning vocabulary.

The tick column means "dealt with or safely past", and it is the checklist
component from `page-build.md` under the key `<slug>:missables`, with the same
"12 / 30" counter. A player twenty hours in uses it to find the first unticked
row — the next window still open. When a row *is* a where-list item (a shard
sold by a vendor who leaves), it gets no box of its own: the cell links to the
tab holding that list, so the item is ticked in one place only.

When the game locks almost nothing, open the tab with a short paragraph saying
so and naming what it rations instead, then show whatever small table remains.
An honest near-empty tab is worth more than a padded one; the player reads it
and relaxes, which is a real outcome.

## "100% and achievements"

The last tab, in every guide. It answers "what would it take to get
everything?" — asked by the completionist on day one and by everyone else the
moment they enjoy the game enough to want more. Build it even when the player
said their goal is the story: the tab is cheap to skip, and the one thing it
protects them from — a missable achievement already gone by the time they care
— cannot be fixed later.

What it holds, in this order:

- **The headline numbers.** Total achievements/trophies on the player's
  platform, how many are missable, the minimum number of playthroughs, whether
  a difficulty setting is required, and the typical time to 100% from a
  completionist site. Say which platform the list is for; Steam, PlayStation
  and Xbox lists differ.
- **The roadmap.** The order that gets everything in the fewest runs: what to
  do on the first playthrough (always including every missable), what to clean
  up after the credits or in NG+, and what to leave for last (grinds, hardest
  difficulty, online). Three to five stages; each names the stage's
  achievements by count, not by list.
- **The list itself**, grouped by type — story (unmissable), missable,
  collectible, cumulative/grind, difficulty, online — with each group's count
  shown so the groups visibly add up to the total.
- **The rarest few** by global unlock percentage when the platform publishes
  it, with one line on why each is rare. That is where players actually get
  stuck, and it is worth more than any tier of difficulty rating.
- **What the game counts as 100% in-game**, if it has its own completion
  percentage, and how it differs from the achievement list — they often do not
  match, and players chasing one assume the other.

**Missables live in two places on purpose.** The row with trigger, window and
signal lives in "Do this or lose it forever", because that is where the player
is when the window shuts. Here, the achievement carries a missable marker and a
link to that row — never a second copy of the instructions, which would drift.

**Spoilers.** Hidden achievements exist because their names or conditions spoil
something. Keep the visible layer to the category and what to do ("beat the
optional boss in the fourth area without resting"), and gate the achievement's
name and anything naming a story character, ending or late area. Ending-based
achievements say "one per ending — N endings" visibly and gate each ending's
name. The spoiler checks in SKILL.md §5 apply here like anywhere else.

**When the game has no achievement system** (some console-exclusive, older or
DRM-free releases), say so in one line and build the tab around the game's own
completion measure — a percentage, a journal, a collection screen. When it has
neither, say that the game has no formal 100% and list the closest thing
players chase.

### Rendering it

- A **stat row** at the top: total · missable · playthroughs · time to 100%. The
  missable count uses the warning colour and links down to the missable group.
- The **roadmap** as a short numbered list (real sequence, so numbering is
  earned), one stage per item.
- The **list** as one table per group, or one table with a group column and a
  filter — whichever keeps the reader's current group on one screen:

| ✓ | Achievement | How | Missable? |
|---|---|---|---|

  The name column holds a `.spoil` span for hidden achievements. The last column
  uses the same three-state pill as "Do this or lose it forever" and links to
  the matching row there.
- A **checkbox per achievement**: the checklist component under
  `<slug>:achievements`, with a line saying the ticks live in that browser only
  and pointing at the export/import block. Show a running "12 / 48" beside the
  stat row. An achievement that *is* a where-list total ("all Mask Shards")
  still gets its box here — the achievement and the items are different things
  to tick.
- Keep global percentages in a mono numeral column; they are data, not prose.

## Where-lists

Not a tab of their own — the lists that live inside the progression, collection
and completion tabs. Every rationed thing the guide gives a total for gets one:
health upgrades, resource-meter upgrades, weapon-upgrade materials, slot
unlocks, rescuables, keys. The first Hollow Knight guide earned its trust with
these (masks and vessel fragments one per row); a guide that only prints "20
exist" has told the player what the pause menu already says.

What each list carries:

| ✓ | # | Where | How | Needs | Act / chapter |
|---|---|---|---|---|---|

- **Where** — area plus a positional hint ("east of the bench", "behind the
  breakable wall above the village"), never a room-by-room route.
- **How** — found / bought for N from a vendor *role* / wish or quest reward /
  boss drop. Vendor and NPC names that spoil go behind the gate; roles stay
  visible.
- **Needs** — the ability, key or event that must come first. This column is
  what turns the list into a plan: the player filters it by what they already
  have.
- **Act / chapter** — so a player at the end of act 1 knows that holding 6 of 20
  is normal, not a failure. Put that sentence above the list when the split is
  lopsided.
- **A tick box per row**, persisted under `<slug>:<list>`; see "Checklist tables"
  in `page-build.md`, which the missables table and the achievements tab use
  too. This is the one place the item is ticked.
- **Row count equals the stated total**, or the list says why not ("21 rows:
  rows 4 and 5 are either/or").

Late-game rows follow the walkthrough rule: the visible layer says the act and
"needs an ability you get later"; the sub-area, NPC and reward names go behind
the gate.

When the game has area blocks (a walkthrough tab), add one line to each block
counting what that area holds from each list — "Mask 1/2 · Spool 0/1 · Fleas
2/3". It is the number a player uses to decide whether to sweep an area now.
Build it as a live tally (`data-area` on the rows, `data-tally` in the block;
`page-build.md`, "Checklist tables") so it counts what they have picked up, and
put no tick boxes in the area block itself.

## The questline tab

Built only when the sweep in SKILL.md §3c comes back positive — the game has NPC
chains that advance on world progress rather than on a quest log.

What each chain needs:

- **Who, by role and place** — "the merchant first met outside the second area",
  not the name. The name goes behind the spoiler gate.
- **Every step, as an action** — where to go, who to talk to, what to exhaust.
  "Talk until the dialogue repeats" is a genre-wide mechanic most new players
  never learn; state it once at the top of the tab rather than in every step.
- **The deadline for each step**, expressed as the world event that closes it:
  "before killing the third area's boss".
- **What breaks it** — the common accidental failures. Killing the NPC, resting
  at the wrong moment, advancing an area early, selling something.
- **Reward type, not reward name** — "a spell", "a weapon" stays visible so the
  player can decide whether to care; the name is gated.
- **Whether NG+ or a second character gets it back.**

**Keeping it spoiler-safe.** This is the hardest content in the guide to gate,
because with these characters the name, the destination and the outcome *are*
the story. The rule that makes it work: **the instruction is visible, the
identity and the consequence are gated.** A reader who never opens a single blur
must still be able to complete every chain by following the steps. Never state
how a chain ends in the visible layer — and do not put the ending in the gated
layer either unless the player asked for it. They need the steps, not the payoff.

### Rendering it

Not a table — a chain does not fit in rows. One card per NPC, each holding an
ordered step list, because the reader follows it a step at a time with the game
running next to them.

Head the tab with the genre mechanic stated once: talk until the dialogue
repeats, and talk again after every world-state change. More losses come from
not knowing that rule than from missing any particular step.

Each card:

- **Heading: the role and where they are first met.** The name is a `.spoil`
  span beside it, never the heading itself — a heading has to survive the blur,
  or the reader cannot find the card they are looking for.
- **Steps as an ordered list**, one line each: the action, then the deadline as
  a world event in muted text. Number them; the player is tracking a position.
- **A "breaks if" line** in the page's warning style.
- **A reward line** with the type in plain text and the name gated.

Give each step a checkbox. A questline tab is the one part of a guide read
across many sessions, so persisted ticks are worth more here than anywhere else
on the page. Persist them in `localStorage` under `<slug>:quests`, wrapped in
try/catch, with a line saying the ticks live only in that browser and pointing
at the export/import block (`page-build.md`, "Moving ticks between browsers").
Not a shared runtime database: on a page shared by link every viewer would tick
the same boxes.

Order cards by when the player first meets each NPC, then put one compact figure
above them: a horizontal line of the game's major milestones with every chain's
deadlines marked against it. That figure is what makes "three of these all close
at the same boss" visible, which no amount of prose does.
