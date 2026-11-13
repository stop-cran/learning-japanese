# Author's statement for the reviewer of `reports-114\initial-gpt.md`

This statement answers only the points in YOUR initial report. F1, F2, F3, O1 and L1 to L6 are your report's own labels.
The statement is the author's claim about what changed and why. Verify each claim against the revised card text in
`snapshot\kanji\`, `diffs\fix.patch` and the evidence; do not rely on this text as evidence. Line numbers refer to the
revised cards in this packet. 6 of the 15 cards changed (寮 穫 魅 穀 碁 症); the other nine did not (see `CHANGES.md`).
Give a disposition for each of F1, F2 and F3. O1 (none) and L1 to L6 need none; see the notes at the end.

## Pair mechanics (applies to F1-F3)

Every pair added in this revision is declared once, on the batch card's side; no counterpart card changed, and no
exclusion was added between two counterparts. Author's script over all 1,221 cards at the revised snapshot: no
counterpart lists its batch card in `quiz_exclusions` or `distractors`; no batch card lists a counterpart in
`distractors`; no card lists both members of a new pair in `distractors`; every counterpart still has three
`distractors`. `excluded(a, b)` in `evidence\QuizBuilder.kt` (line 26) is true if either card lists the other, and `tryAdd`
(lines 28-32) refuses a candidate excluded against the target or against an option already chosen, for curated and
fallback candidates alike (lines 34-36). `checks\quiz-safety.txt` is byte-identical to the original packet's copy: the
three wrong options shown for each of the 15 cards in the modelled pools did not change.

## Findings

### F1 (moderate): missing direct room and bureau comparisons for 寮

Author action: **changed, as proposed: all four pairs are declared** (寮-房, 寮-庁, 寮-部, 寮-課).

- `寮.md:14` now reads `quiz_exclusions: [宿, 宅, 住, 家, 室, 房, 館, 亭, 官, 局, 署, 府, 庁, 部, 課]` (it read
  `[宿, 宅, 住, 家, 室, 館, 亭, 官, 局, 署, 府]`).
- `寮.md:62-64`: `Room and accommodation uses connect with [室](室.md), [房](房.md) and [館](館.md); the tea-pavilion sense
  connects with [亭](亭.md). The buildings and their uses still differ.`
- `寮.md:65-70`: `Historical official or bureau senses overlap [官](官.md), [局](局.md), [署](署.md), [府](府.md) and
  [庁](庁.md). A bureau beneath a ministry also overlaps the organizational units [部](部.md) and [課](課.md). These direct
  comparisons are excluded from choices; the exclusion does not equate every modern institution or authorize swapping its
  name.`
- Evidence in `evidence\jmdict-cited-entries.xml`: 寮 JMdict 1554230 (sense 2: archaic "bureau (government department
  beneath a ministry under the ritsuryō system)"; sense 3: archaic "tea-ceremony room"), and 房 ぼう JMdict 2222290
  ("chamber; room; cell (prison); atrium", "home of a monk; monk").

To verify: that the four pairs are declared, that the new wording keeps the historical qualification, and that it does
not equate a ritsuryō bureau with a modern ministry.

### F2 (moderate): missing gathering and useful-result comparisons for 穫

Author action: **changed, as proposed: all four pairs are declared** (穫-集, 穫-拾, 穫-利, 穫-績).

- `穫.md:14` now reads `quiz_exclusions: [刈, 収, 採, 取, 集, 拾, 得, 利, 捕, 果, 実, 績]` (it read
  `[刈, 収, 採, 取, 得, 捕, 果, 実]`).
- `穫.md:58-61`: `[刈](刈.md) overlaps reaping; [収](収.md), [採](採.md), [取](取.md), [集](集.md) and [拾](拾.md) overlap
  gathering or taking in. 刈 retains a cutting action, so it is not every method of harvesting.`
- `穫.md:62-66`: `In the extended uses of 収穫, gains connect with [得](得.md) and [利](利.md), a catch with [捕](捕.md),
  and fruitful results with [果](果.md), [実](実.md) and [績](績.md). These compound-context comparisons are excluded from
  choices without licensing arbitrary substitutions of the characters.`
- The noun-versus-する bullet (`穫.md:67-68`) and all readings and word rows are unchanged.

To verify: that the four pairs are declared and the bullets do not claim that bare 穫 means collecting, benefit or
results in general.

### F3 (moderate): missing direct supernatural comparison for 魅

Author action: **changed, as proposed.**

- `魅.md:14` now reads `quiz_exclusions: [妖, 怪, 符]` (it read `[妖, 符]`).
- `魅.md:60-64`: `[妖](妖.md) overlaps bewitching attraction and supernatural beings; [怪](怪.md), suspicious/uncanny,
  overlaps the supernatural sense. [符](符.md) also displays charm, but its talisman sense differs from personal appeal.
  These comparisons are excluded to avoid ambiguous English choices, not treated as unrestricted substitutions.` (Line 63
  said `Both comparisons` before.)

To verify: that the pair is declared and the text keeps suspicion, supernatural beings and personal allure distinct.

## Optional

O1 was "none"; nothing to answer.

## Limits

No action is claimed, and no disposition is needed. Notes:

- L1: 銃, 棋 and 陶 still have no card at the revised snapshot; nothing was added for them.
- L2: none of the unread candidates in your L2 tables was added as an exclusion. 板 "plank; board" is now linked from
  `碁.md:62` (see below) but not excluded.
- L3 and L4: no sentence they name changed, and no level, provenance or asset claim changed.
- L5: the revision adds meaning-quiz exclusions only; no reading, reading selection or distractor changed.
  `checks\reading-exposure.txt` is byte-identical to the original packet's `checks\reading-exposure-final.txt`;
  `checks\reading-options.txt` is new in this round and was produced at the revised snapshot. No Kotlin, JVM, native,
  phone or emulator execution occurred. Installed APK `5c000bd` predates `quiz_exclusions`, so none of the new pairs
  protects that build.
- L6: unchanged.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk. Each states what the author claims and
why.

- `穀.md:14` and `:68-72`: 穂 "grain-bearing head" was added: the 穂 bullet now continues `Like the rice plant, its
  displayed grain wording is close enough that the pair is excluded from choices.` "The rice plant" is 稲, already
  excluded and named at lines 61-63. The unchanged sentence on the 禾 indexing key and the Nelson 殳 classification is
  now its own bullet (lines 71-72). The author's reason: 穀 already excludes 粒 for the shared grain label, and 穂, the
  ear of grain, is at least as close.
- `碁.md:14` and `:59-62`: 盤 "board; disc" was added (the list was empty): `[盤](盤.md), board/disc, names the Go board
  itself, as in 碁盤 ごばん. Because it is the game's own equipment and the title also says board, this direct pair is
  excluded from choices; the game and its board remain different meanings. [板](板.md), plank, is not that equipment.`
  碁盤 is JMdict 1270890 ("Go board"); bare 盤 ばん is JMdict 1482420, sense 1 "board (in shogi, go, chess, etc.)". The
  unchanged bullet at lines 65-67 still says that a shared game-related topic alone is not an exclusion rule; the author's
  claim is that 盤 is the game's own board and also shares the displayed word board. 板 is named but not excluded.
- `症.md:50`: the Common words gloss `重症 じゅうしょう - serious illness; severe condition` now reads `serious illness`,
  matching JMdict 1336310 (supplied in `evidence\jmdict-cited-entries.xml`).
