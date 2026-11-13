# Author's statement for the reviewer of `reports-114\initial-claude.md`

This statement answers only the points in YOUR initial report. F1, F2, F3, O1 to O7 and L1 to L6 are your report's own
labels. The statement is the author's claim about what changed and why. Verify each claim against the revised card text
in `snapshot\kanji\`, `diffs\fix.patch` and the evidence; do not rely on this text as evidence. Line numbers refer to the
revised cards in this packet. 6 of the 15 cards changed (寮 穫 魅 穀 碁 症); the other nine did not (see `CHANGES.md`).
Give a disposition for each of F1, F2, F3 and O1 to O7. L1 to L6 need none; see the notes at the end.

## Pair mechanics (applies to F1-F3, O2 and O3)

Every pair added in this revision is declared once, on the batch card's side; no counterpart card changed, and no
exclusion was added between two counterparts. Author's script over all 1,221 cards at the revised snapshot: no
counterpart lists its batch card in `quiz_exclusions` or `distractors`; no batch card lists a counterpart in
`distractors`; no card lists both members of a new pair in `distractors`; every counterpart still has three
`distractors`. `excluded(a, b)` in `evidence\QuizBuilder.kt` (line 26) is true if either card lists the other, and `tryAdd`
(lines 28-32) refuses a candidate excluded against the target or against an option already chosen, for curated and
fallback candidates alike (lines 34-36). `checks\quiz-safety.txt` is byte-identical to the original packet's copy: the
three wrong options shown for each of the 15 cards in the modelled pools did not change.

## Findings

### F1 (minor): 穀 should exclude 穂

Author action: **changed, as proposed.**

- `穀.md:14` now reads `quiz_exclusions: [米, 麦, 稲, 穂, 種, 粒, 実]` (穂 added after 稲).
- `穀.md:68-70`: the 穂 bullet keeps `[穂](穂.md) is the grain-bearing head, a part of a plant, not a synonym for all
  grain.` and now continues `Like the rice plant, its displayed grain wording is close enough that the pair is excluded
  from choices.` "The rice plant" is 稲, named at lines 61-63 and already excluded.
- `穀.md:71-72`: the unchanged sentence about the 禾 indexing key and the Nelson 殳 classification, which used to close
  the 穂 bullet, is now its own bullet.

To verify: that the pair is declared and the note now says so without calling 穂 a synonym for all grain.

### F2 (minor): 碁 should exclude 盤

Author action: **changed, as proposed (on 碁's side).**

- `碁.md:14` now reads `quiz_exclusions: [盤]` (it was empty).
- `碁.md:59-62` are a new bullet: `[盤](盤.md), board/disc, names the Go board itself, as in 碁盤 ごばん. Because it is the
  game's own equipment and the title also says board, this direct pair is excluded from choices; the game and its board
  remain different meanings. [板](板.md), plank, is not that equipment.`
- Evidence in `evidence\jmdict-cited-entries.xml`: 碁盤 ごばん is JMdict 1270890 ("Go board"); bare 盤 ばん is JMdict
  1482420, whose sense 1 is "board (in shogi, go, chess, etc.)".
- The unchanged bullet at lines 65-67 still says `A shared game-related topic alone is not an exclusion rule.` The author's
  claim is that 盤 is excluded for more than a shared topic: it names the game's own board and shares the displayed word
  board.

To verify: that the new bullet is accurate, that it does not contradict lines 65-67, and that the pair is declared.

### F3 (minor): 寮 should exclude 房

Author action: **changed, as proposed.**

- `寮.md:14` gains 房 after 室 (together with 庁, 部 and 課; see O2 and "Changes that do not answer a point").
- `寮.md:62-64` now read `Room and accommodation uses connect with [室](室.md), [房](房.md) and [館](館.md); the
  tea-pavilion sense connects with [亭](亭.md). The buildings and their uses still differ.`
- 房 ぼう is JMdict 2222290 ("chamber; room; cell (prison); atrium", "home of a monk; monk"), supplied in
  `evidence\jmdict-cited-entries.xml` as context for the room and monk-dwelling senses your F3 cites from 房's card.

To verify: that 房 is declared and named in the room clause.

## Optional

### O1: 碁 against 板 and 行

Author action: **declined, partly addressed in text.** 板 "plank; board" is now named and distinguished in the new 盤
bullet (`碁.md:62`: `[板](板.md), plank, is not that equipment.`) but is not excluded: the author treats 板 as a
label-only overlap on the word board, without the equipment link that 盤 has through 碁盤. 行 is not added: "go" and the
game name Go differ in meaning, and the unchanged bullet at `碁.md:65-66` already says the English movement verb go is not
this meaning. Your report called the current text a defensible editorial choice.

To answer: DECLINE ACCEPTED or DECLINE REJECTED, with the reason.

### O2: 寮 against 庁

Author action: **changed, as suggested.** `寮.md:14` gains 庁; `寮.md:65-66` now read `Historical official or bureau senses
overlap [官](官.md), [局](局.md), [署](署.md), [府](府.md) and [庁](庁.md).`

### O3: 穫 against 集 and 拾

Author action: **changed, as suggested.** `穫.md:14` gains 集 and 拾 after 取; `穫.md:58-61` now list `[収](収.md),
[採](採.md), [取](取.md), [集](集.md) and [拾](拾.md)` as overlapping gathering or taking in.

### O4: 栓/判 and 廊/塔 over-exclusions

Author action: **no change**, as your report recommended. Both exclusions remain and only shrink fallback pools.

### O5: 気.md says "汽 is steam only"

Author action: **deferred.** 気.md is outside this batch and was not edited in this revision. The point is recorded as a
separate later fix (link 汽 and adjust the wording), not part of batch 114.

To answer: whether deferral is acceptable for this batch.

### O6: Metadata lines cite JMdict entries not shown in the text

Author action: **declined.** The Metadata line records the word families consulted for the card (砲: 1477900 発砲; 寮:
1455860 独身寮); listing a consulted family that is not displayed is provenance, not a claim made in the text. Your report
called this harmless. No Metadata line changed.

To answer: DECLINE ACCEPTED or DECLINE REJECTED.

### O7: 症's gloss of 重症

Author action: **changed, as suggested.** `症.md:50` now reads `重症 じゅうしょう - serious illness`, matching JMdict
1336310 (supplied in `evidence\jmdict-cited-entries.xml`).

## Limits

No action is claimed, and no disposition is needed. Notes:

- L1, L2 and L6: unchanged. No stroke file, Joyo row or check script changed; the checks in `checks\` were rerun at the
  revised snapshot.
- L3: the revision adds meaning-quiz exclusions only; no reading, reading selection or distractor changed, and
  `checks\reading-exposure.txt` is byte-identical to the original packet's `checks\reading-exposure-final.txt`. No Kotlin,
  JVM, native, phone or emulator execution occurred. Installed APK `5c000bd` predates `quiz_exclusions`, so the new pairs do
  not protect that build.
- L4: no Daijisen-only statement changed; they remain unverified in the author's evidence too.
- L5: none of 空, 風, 愛, 恋, 耕, 産, 爆, 黒, 緑, 盆 or 皿 was added. 銃, 霧, 獲, 棋 and 陶 still have no card at the
  revised snapshot.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk.

- `寮.md:14` and `:66-67`: 部 "section; department" and 課 "lesson; organizational division" were added: `A bureau beneath
  a ministry also overlaps the organizational units [部](部.md) and [課](課.md).` JMdict 1554230 (寮) sense 2 is a
  historical government department beneath a ministry (supplied in `evidence\jmdict-cited-entries.xml`). The author's
  reason: once 庁 is excluded for the bureau sense, the organizational-unit labels sit just as close.
- `穫.md:14` and `:62-64`: 利 "benefit; advantage" joins the gains clause and 績 "achievements; results" the results
  clause of the 収穫 bullet. The author's reason: the bullet already excludes 得 for gains and 果/実 for fruitful results,
  and these two labels name the same senses.
- `魅.md:14` and `:60-61`: 怪 "suspicious; uncanny" was added: `[怪](怪.md), suspicious/uncanny, overlaps the
  supernatural sense.` Line 63 now says `These comparisons` instead of `Both comparisons`. The author's reason: 魅's card
  teaches a supernatural spirit or monster sense, and 怪's card describes uncanny beings (怪物, 妖怪); the existing 妖
  exclusion does not cover 怪, because exclusions are not transitive.
