# Research rules

The guide's value is that its numbers are right. A player who finds one wrong
count stops trusting the whole page, and rightly so — they cannot tell which
other numbers were guessed.

## Source hierarchy

1. **The game's main wiki** — usually the most complete on mechanics and item
   stats. Fextralife, Fandom, and dedicated per-game wikis all qualify. Fandom
   often blocks automated fetches; if it 403s, use another source rather than
   fighting it.
2. **A completionist site** — PowerPyx, trophy/achievement guides, checklist
   sites. These are stronger than wikis on *counts* and *locations*, which is
   exactly what the scarcity spine needs.
3. **The community** — Steam discussions, subreddit wikis, GameFAQs. Useful for
   "is this actually good", useless for exact numbers.
4. **Patch notes and the official site** — the only authority on what changed.

A transient 502 or timeout from a wiki CDN is not a dead source. Retry once
before switching.

## Two sources per number

Any number that appears in the guide — a total, a cap, a cost, a scaling grade —
should be seen in two places. When they agree, state it plainly. When they
disagree, write the range and say the sources disagree:

> Legion Caliber: 16 in the base game (one source lists 17)

This costs one clause and buys the reader the ability to check for themselves.
Silently averaging or picking the prettier number is the one thing not to do.

## Hunt the scarcity structure first

Before reading anything about builds, find out what the game rations. Useful
searches:

- `all <resource> locations <game>` — gives you the total and the route at once
- `<game> missable` / `point of no return` — the timing spine
- `how many <upgrade material> in <game>` — the budget
- `<game> can you get everything in one playthrough` — usually answers several
  scarcity questions in one page
- `<game> best <system> order` — what the community converged on, useful as a
  sanity check against your own reasoning

Write these down as you go with the source next to each. The verification pass
in the main workflow reads these notes back, and it only works if they exist.

**Keep a second list beside it: the proper nouns that would spoil.** Every
character, boss, region, item and ending name you meet that gives away something
about the story goes on it, as you meet it. The verification pass greps the
finished page against this list to prove none of them leaked outside a `.spoil`
span, and that check is exactly as good as the list is complete. Building it
costs nothing while you are already reading; it cannot be reconstructed
afterwards, because by then you have stopped noticing which names are spoilers.

## When research comes up empty

New releases, early-access titles, small-studio games, and games whose community
writes in a language you are not searching in can all leave you with almost
nothing. This is the most dangerous point in the whole workflow: the guide
format has slots, slots invite filling, and plausible-looking numbers are very
easy to produce.

The rule is absolute: **an unsourced number never goes on the page.** Not
hedged, not "roughly", not "around 20". A reader cannot tell a hedge from a
guess once it is sitting next to twenty real figures, and one invented total
poisons every other number on the page.

What to do instead, in order:

1. **Widen before giving up.** Steam discussions, the subreddit and its wiki, a
   publicly indexed Discord, patch notes, the developer's own posts. Then search
   in the game's original language — a Japanese, Chinese or Korean wiki is often
   years ahead of the English one, and machine translation is good enough for
   numbers and item tables.
2. **Downgrade the guide to what you can support.** Four solid tabs beat ten
   padded ones. Structural advice survives without numbers — "this genre rations
   X, watch for it, here is the symptom" is still useful — while specific counts
   do not.
3. **Say it on the page, not only in chat.** One line at the top: which parts
   are well sourced, which are thin, how many sources exist. Players calibrate
   on this and do not punish a guide for being honest about its limits.
4. **Tell them what would fix it.** "No completionist guide exists for this game
   yet; when one appears, ask me to update this page" turns a gap into a plan
   and sets up the update path.

A guide that says "nobody has counted these yet" is doing its job. A guide that
guesses is worse than no guide, because the player will act on it.

## Sourcing the fixed tabs

These tabs need their own search passes, because none of them is well served by
wiki pages.

**For "before you start":**

- `<game> difficulty can you change later`
- `<game> best settings first playthrough` — filters to settings that change the
  experience, rather than a graphics benchmark
- `<game> character creation permanent` / `<game> can you change appearance`
- `<game> should I play the DLC first` / `<game> DLC when to start`
- `<game> map type which should I pick` / `<game> world settings explained`
- `<game> multiple save slots` / `<game> should I make a second save`
- The game's own options menu, if it is visible in any video — half this tab is
  sitting there and needs no search at all

**For "things I wish I knew":**

- `<game> things I wish I knew before playing`
- `<game> beginner mistakes` / `<game> what I did wrong`
- `<game> tips reddit` — threads surface the habits nobody writes into wikis
- Mixed and negative Steam reviews — people describe precisely what confused
  them, which is the same material stated as complaint rather than tip
- Compare what you find against the game's own tutorial. Anything the tutorial
  already covers gets cut, however popular the tip is.

**For "do this or lose it forever":**

- `<game> missable` / `<game> permanently missable`
- `<game> point of no return`
- `<game> can you get everything in one playthrough`
- `<game> mutually exclusive` — catches faction, romance and achievement forks
- `<game> should I save or use <consumable>`
- Trophy and achievement guides — these are written by people who lost things,
  so they document one-way doors more carefully than any wiki

**For the NPC questline sweep** — run this on every game, including the ones
where you expect nothing:

- `<game> NPC questline order` / `<game> quest order guide`
- `<game> <npc role> questline steps`
- `<game> how to not miss questlines` / `<game> quest failed why`
- `<game> does killing <boss> break quests` — the world-progress dependency,
  phrased the way players actually ask it
- Dedicated quest-order pages, which for souls-likes beat the wiki's per-NPC
  pages because they resolve the ordering conflicts *between* chains

Take the steps from one source that gives the whole chain in order. Stitching a
chain together out of several per-NPC pages is where step ordering silently goes
wrong, and a wrong order in this tab costs the player exactly the thing the tab
exists to protect.

If several passes turn up nothing, that is a real result. Confirm it with a
direct search (`<game> anything missable`, `<game> missable quests`) and then
say so in the guide rather than quietly leaving the tab thin.

## Counting is a real check, not a formality

When a source gives both a total and a list, add the list up. Discrepancies are
extremely common — a list of "16 locations" that sums to 15 usually means one
location holds two, and finding which one is a genuine improvement over what
the source said.

Do the same for any plan the guide proposes: if you lay out a spend order,
total it and confirm it fits the budget you stated three paragraphs earlier.

## Version drift

Numbers change between patches, and guides on the web rarely say which patch
they describe. Ask the player their version, note in the footer which patch your
sources appear to describe, and flag anything you know changed recently.

Free collaboration or promotional items are a common trap: they may not be
obtainable on all platforms or on saves created after a certain date. If the
guide leans on one, tell the player to check their inventory before planning
around it.

## What not to research

Story. Do not read plot summaries, ending explanations, or character pages
beyond what a mechanical question requires. It is easier to keep a guide
spoiler-safe when the writer has not loaded the spoilers in the first place, and
mechanical pages (item stats, upgrade materials, system explainers) rarely
contain them.
