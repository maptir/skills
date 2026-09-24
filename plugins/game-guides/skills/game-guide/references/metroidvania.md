# Metroidvania / search-action

Hollow Knight, Ori, Blasphemous, Axiom Verge, Prince of Persia: The Lost Crown,
Animal Well. Read `rpg.md` alongside this one for anything with charms, gear or
stat spending; this file covers what the map does to a guide.

## The genre's real scarcity is orientation, not items

Every other genre reference starts by hunting a fixed total. Do that here too —
these games ration upgrade materials as tightly as any RPG — but do not stop
there, because it is not what makes players put the game down.

A metroidvania hands out a large interconnected space and deliberately withholds
the instruction of where to go. That is the design working as intended, and it
is also the single largest source of wasted hours. **The player is not stuck
because they lack a resource; they are stuck because they cannot tell which of
forty doors is the one their new ability just opened.** A guide that lists every
collectible and never answers "where do I go next" has solved the easy problem.

So this genre earns a tab no other genre needs: a **per-area walkthrough with
the route drawn on the map**. `page-build.md` has the build mechanics under
"Area maps with the route drawn on them". This file decides what goes on them.

## Where the irreversible decisions hide

- **Traversal abilities are the real progression tree.** They are never missable
  and almost never optional, but their *order* is the whole shape of the run.
  Get the order right and the guide is useful before it lists a single item.
- **One-way drops and sequence gates.** A chute that dumps you into the next
  area with no way back, a door that only opens from the far side. Rarely
  permanent, frequently disorienting, and worth marking on the map.
- **Area-state changes.** Some games flood, infect, or reconfigure a region once
  the story advances; NPCs relocate and a few side rooms close. Check for this
  specifically — it is the genre's version of chapter-gating.
- **Shops that stock one of something.** Common here, and easy to walk past.
- **NPC chains keyed to world progress.** Run the sweep in SKILL.md §3c; this
  genre passes it more often than not.
- **Charm/badge/relic loadout caps.** A slot budget the player meets long before
  they meet the collection. See "Numbers to hunt".

## Numbers to hunt

Count of each traversal ability and the area each is in · the loadout slot
budget versus the total cost of everything equippable (the gap is usually the
guide's best single figure) · upgrade material totals against full-upgrade cost
· map-vendor cost per area · fast-travel node count and unlock cost · total
collectibles per area, because a per-area count is what lets a player decide
whether to sweep a region now or come back.

The comparison that carries a metroidvania guide: **what the map asks of you
versus what you can carry at that point.** State plainly which areas are
survivable early and which will flatten a player who wanders in on schedule but
under-equipped.

## The per-area walkthrough tab

One tab, not one tab per area — a rail with fourteen area tabs is a wall. Inside
it, an area switcher and one block per area holding:

- **The area's map, with numbered route pins.** Gold numbered pins for the order
  to walk it, a distinct style for exits, keyed to the step list below.
- **Four to seven steps**, each an action, not a description. "Open the stag
  station here first" beats "this area contains a stag station."
- **An exits strip**: every edge of the map and what lies through it. This is
  the highest-value two lines in the whole tab, because the lost player's actual
  question is "which way out leads somewhere new".
- **A "where people get lost here" line**, but only for the areas where they
  genuinely do. Writing one for all fourteen devalues the four that matter.
- **What gates the area** — the ability or key without which the player is
  wasting a trip.

Order the areas by the route the world expects, and number them in the switcher.
Put the ability-order table above the switcher so the two read as one answer.

## Advice traps

- **Do not turn the walkthrough into a room-by-room script.** These games are
  built to be explored; a guide that walks the player through every room removes
  the thing they paid for. Route and orientation, not a leash. The step list
  points at objectives and exits and leaves the rooms between them alone.
- **Pin precision you do not have is worse than no pin.** You can place exits
  and labelled sub-areas honestly; claiming a specific room's position on an
  abstract map usually means guessing. Place what you can verify, say on the
  page that pins mark order and direction rather than exact rooms, and let the
  step text carry the rest.
- **Do not reorder the world to be optimal.** Sequence breaks are real and some
  are widely known, but a first-run guide that routes through one leaves the
  player under-levelled and confused about why the game feels wrong. Mention the
  break, do not build the route on it.
- **"Come back later" needs a trigger, not a vibe.** Every deferred item gets
  the ability that unlocks it named next to it, so the player can search their
  own notes when they get it.
- **A walkthrough leaks progression spoilers the rest of the guide gates.** The
  step text is written while you hold the whole route in your head, and phrases
  like "this is where the game ends", "endgame item", "this unlocks the final
  boss" slide in as navigation notes. They are not. For anything the player
  cannot act on yet, the entire content is **"can't open this yet — come back
  later"**; naming what it becomes is a reveal the gate elsewhere on the page
  was built to prevent. Sweep every area block for this before publishing; it
  is a different pass from the `.spoil` grep, because these leaks carry no
  proper noun to search for.
- **Backtracking is the loop, so name the tool that makes it cheap.** Fast
  travel, map markers, a teleport unlock bought with the collectible currency —
  players routinely miss these for twenty hours. This belongs in "Things I wish
  I knew" at the top, not in a systems tab.
