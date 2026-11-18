# Author's statement for the reviewer of `reports-112-gpt\initial-gpt.md`

This statement answers only the points in YOUR initial report. F1 to F6 are your report's own labels. Your Optional
section says "None", so no optional point is answered. **L1** is the second bullet of your Limits section (custom and
caller-built pools, multiple borrowed Starter cards, actual Kotlin draws, native execution, phone acceptance and older
installed-client compatibility), together with the last sentence of your Findings preamble (`their actual Kotlin/custom-pool
exposure was not executed`). **L2** is the other Limits bullets (the first and the third to the seventh). The statement is
the author's claim about what changed and why. Verify each claim against the revised card text in `snapshot\kanji\`,
`diffs\fix.patch` and independent sources; do not rely on this text as evidence. Line numbers refer to the revised cards in
this packet. Eight of the 15 cards changed (妙 就 展 微 態 盤 診 障) and the other seven did not (see `CHANGES.md`). Give a
disposition for each of F1, F2, F3, F4, F5, F6 and L1; L2 needs none.

## Findings

All six findings were remedied in the way you proposed: by direct pairs, each declared once, on the batch card's side. No
counterpart card changed, and no exclusion was added between two counterparts, so no group or clique was formed. Author's
script over all 1,191 cards at the revised snapshot: no counterpart lists its batch card in `quiz_exclusions` or
`distractors`; no batch card lists a counterpart in `distractors`; every counterpart still has three `distractors`. The
three wrong options shown for every one of the 15 cards are unchanged (`checks\quiz-safety.txt` is the same as in the
original packet). One declaration guards both directions: `excluded(a, b)` in `evidence\QuizBuilder.kt` (line 26) is true
if either card lists the other.

### F1 (moderate): 妙 leaves ordinary skill answers eligible

Author action: **changed, as proposed.**

- `妙.md:14`: `quiz_exclusions: [奇, 変, 美, 優, 微, 若, 珍, 技, 腕]`; 技 and 腕 are the additions (the list ended at 珍).
- `妙.md:67-69` is a new Notes bullet: `- JMdict also gives the word 妙 みょう a skill or cleverness sense, which overlaps
  [技](技.md), skill/technique, and [腕](腕.md), arm/skill. These direct comparisons are excluded from meaning choices too.`
  The sense is sense 3 of JMdict 1528490 (`evidence\jmdict-cited-entries.xml`), "cleverness; adroitness; knack; skill",
  already cited in the Metadata line (line 76).
- The skill explanation is kept: lines 23-25 are unchanged (`wonderfully skillful and fine`, `a clever touch`). `技.md`
  (`skill; technique`, `[支, 持, 抜]`) and `腕.md` (`arm; skill`, `[肩, 服, 胸]`) are unchanged.

To verify: that both pairs are declared and the new bullet is accurate.

### F2 (moderate): 就 omits the undertaking and completion overlaps

Author action: **changed, with all five proposed pairs, plus three more** (担, 職 and 位; see "Changes that do not answer a
point" below).

- `就.md:14`: `quiz_exclusions: [着, 付, 任, 定, 成, 始, 去, 発, 学, 企, 承, 担, 職, 位, 了, 完, 済]`; the list ended at 学.
- `就.md:74-75` begin a new bullet: `- "Undertake" also appears in the titles of [企](企.md), plan/undertake, and
  [承](承.md), accept/undertake.` The bullet ends at line 78 with `These comparisons are also excluded; the complete words
  still differ in use.`
- `就.md:79-82` are a new bullet: `- The completion side shown by 成就 also overlaps [了](了.md), completion/settling,
  [完](完.md), complete, and [済](済.md), settle/finish. They are excluded from meaning choices as well; this does not make
  就 a substitute for those characters in their own words.`
- The completion sense is kept: lines 29-31 (`成就 じょうじゅ, fulfillment or successful completion`; JMdict 1375720
  "fulfillment; fulfilment; realization; realisation; completion", `evidence\jmdict-cited-entries.xml`) and the ジュ row at
  line 43 are unchanged. The ジュ reading is still not selected for reading questions, as before.
- 企 `plan; undertake`, 承 `accept; undertake`, 了 `completion; settling`, 完 `complete` and 済 `settle; finish` are
  unchanged, and none lists 就. 就's own `distractors` are `[京, 秋, 州]` (`checks\quiz-safety.txt`, line 8).

To verify: that the five proposed pairs are declared, that the completion sense is preserved, and that 就 keeps three
defensible wrong options.

### F3 (moderate): 展 and 敷 can both accept the spreading answer

Author action: **changed, as proposed.**

- `展.md:14`: 敷 is added at the end of `quiz_exclusions`, which now reads `[開, 広, 伸, 張, 延, 示, 観, 見, 転, 敷]` (it
  ended at 転).
- `展.md:66-67` are a new bullet: `- Spreading something out flat also overlaps [敷](敷.md), spread/lay out. That direct
  meaning comparison is excluded too.`
- No transitive group: `敷.md` is unchanged (`spread; lay out`, `quiz_exclusions: [布, 普, 散, 床]`, `distractors: [放, 敬,
  敗]`), and no exclusion was added between 敷 and any card in 展's list.

To verify: that the pair is declared and that the bullet does not imply a transitive group.

### F4 (moderate): 微 leaves the "slight" answer from 軽 eligible

Author action: **changed, as proposed.**

- `微.md:14`: `quiz_exclusions: [細, 小, 少, 薄, 弱, 分, 軽]`; 分 and 軽 are the additions (the list ended at 弱). For 分, see
  "Changes that do not answer a point" below.
- `微.md:65-67` are a new bullet: `- A slight degree also overlaps [軽](軽.md), lightweight/slight; both characters appear in
  軽微 けいび, slight or insignificant. That direct comparison is excluded too, without claiming that 微 means light in
  weight.` 軽微 けいび is JMdict 1615650, glossed "slight; little; insignificant" (`evidence\jmdict-cited-entries.xml`);
  the Metadata line (line 80) now ends `1260660, 1590290 and 1615650.`
- `軽.md` is unchanged: `lightweight; slight`, `[経, 怪, 重]`.

To verify: that the pair is declared and that lines 65-67 do not claim that 微 means light in weight.

### F5 (moderate): 診 omits the general inspection answer of 査

Author action: **changed, as proposed.**

- `診.md:14`: `quiz_exclusions: [察, 調, 試, 見, 観, 判, 査]`; 査 is the addition (the list ended at 判).
- `診.md:58-59`: the existing overlap bullet now begins `- [察](察.md), [調](調.md), [試](試.md) and [査](査.md) have
  examination or investigation meanings;` (it named only 察, 調 and 試). The rest of that bullet is unchanged.
- The medical-specific explanation is kept: lines 23-27, lines 43-44 (`Its spelling specifies medical examination, not
  every ordinary act of seeing.`) and line 61 are unchanged. `査.md` is unchanged: `investigate; inspect`, `[昔, 担, 昼]`.

To verify: that the pair is declared and that the card still does not equate diagnosis with every investigation.

### F6 (moderate): 障 leaves the barrier answer from 関 eligible

Author action: **changed, as proposed.**

- `障.md:14`: `quiz_exclusions: [害, 防, 関]` (it read `[害, 防]`).
- `障.md:61-63`: the overlap bullet gains `The barrier sense also overlaps [関](関.md), whose title includes "barrier."`
  before its unchanged closing sentence, `These direct meaning comparisons are excluded from choices, not treated as
  identical in every compound.`
- The barrier and partition text taught through 障子 (lines 28-30) is unchanged. `関.md` is unchanged: `involve; barrier`,
  `[開, 間, 問]`.

To verify: that the pair is declared and the added sentence is accurate.

## Limits

### L1: custom pools, multi-borrow Starter, Kotlin draws, older clients (your second Limits bullet)

The revision adds meaning-quiz exclusions, so the part of the bullet that bears on them is the actual Kotlin draws and their
custom-pool exposure, which your Findings preamble also names. The packet now carries the app's meaning-quiz source,
`evidence\QuizBuilder.kt`, taken from the Android checkout at commit `10d98d0`, which contains `2edbf36` ("Honor explicit
kanji meaning pair exclusions"). In it, `excluded(a, b)` (line 26) is true if either card lists the other, and `tryAdd`
(lines 28-32) returns without choosing a candidate excluded against the target or against any option already chosen
(line 30). The curated `distractors` are looked up in `all`, the pool passed in, so a curated card missing from the pool is
skipped (line 34); the fallback candidates are the other cards of the same pool, shuffled and then ordered by shared tags
(lines 35-36). Both go through `tryAdd`. The field's documented contract (original packet, `repo\docs\content-format.md`,
lines 102-107) says the same for All, level and custom pools, and that a small pool may yield fewer choices. The file does
not show how the app builds `all` for a given pool, so the author makes no claim about which cards any pool holds.

The reading side of the bullet is unchanged by this revision: no reading, reading selection, distractor or title changed,
and `quiz_exclusions` do not affect reading prompts (`content-format.md` line 107). `checks\reading-exposure.txt` is the
same as for the reviewed snapshot (line 236: 0 production hits, 0 padded-session hits, 11 latent collisions), with the
same limits: the app's reading-quiz sources are not supplied in either packet, and multiple borrowed Starter cards, custom
pools for reading prompts, native execution and phone acceptance remain unverified. The Android JVM tests were not run for
this revision either (see `CHANGES.md`). Older installed clients: `quiz_exclusions` are not enforced by older APKs
(`content-format.md` lines 109-112), including the `5c000bd` APK named in your fourth Limits bullet, so the six remedies do
not protect those builds; no claim is made about any installed build.

To verify and answer: whether reading `QuizBuilder.kt` settles the meaning-quiz part of the bullet for the new pairs, what
still cannot be shown, and a disposition for L1 itself: `RESOLVED` (nothing remains open), or a statement of what remains.

### L2: other limits in your report

Your first bullet (the bounded reading-audit pools), third (the eleven latent reading entries), fourth (the `5c000bd` APK;
see the end of L1), fifth (host check outputs read, not rerun), sixth (dictionary lookups verify the inspected sense) and
seventh (local access confined to the packet): no action is claimed and no disposition is needed.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk. Each states what the author claims and why.

- `微.md:14` and `:68-71`: 分 was added to 微's `quiz_exclusions`, and a new bullet reads `- Here English "minute" means
  tiny, not the unit of time associated with [分](分.md). That card's title is "minute, part"; the shared English spelling
  is excluded from meaning choices without treating the Japanese meanings as interchangeable.` 微's title is `minute;
  faint` and 分's is `minute, part`; the two titles share the English word "minute" in different senses. 微's title is
  unchanged: KANJIDIC2 gives 微 "delicate", "minuteness" and "insignificance" (`evidence\kanjidic2-records.xml` in the
  original packet). `分.md` is unchanged (`[今, 半, 木]`, no `quiz_exclusions`).
- `就.md:14` and `:75-78`: 担, 職 and 位 were also added to 就's `quiz_exclusions`, and the "Undertake" bullet continues
  `[担](担.md), shoulder/take on, overlaps taking on a responsibility. [職](職.md), employment/post, and [位](位.md),
  rank/position, overlap the position sense.` The card teaches the position sense at lines 23-25 (`就 concerns taking up a
  position or beginning an activity.`; 就職 obtaining employment; 就任 assuming a particular post). 担 `shoulder; take on`,
  職 `employment; post` and 位 `rank; position` are unchanged, and none lists 就.
- `態.md:62-63`: the Notes bullet now reads `- JMdict also lists 態 as an additional spelling in the entries headed by 体
  (てい), 形 (なり) and 様 (ざま).` It read `- Dictionaries also have separate 態 entries read てい, なり and ざま.` In JMdict
  1409160, 2138450 and 1410750 (`evidence\jmdict-cited-entries.xml`) the first kanji form is 体, 形 or 様 and 態 is the
  second; the 態 form carries no information tag. The three ids were already in the Metadata line (line 71), and line 64,
  `They are not alternate pronunciations to insert into 態度 or 状態;`, is unchanged.
- `盤.md:14` and `:63-65`: 乗 was added to 盤's `quiz_exclusions` (`[板, 皿, 台, 基, 岩, 乗]`), and a new bullet reads
  `- English "board" here is a flat object, not boarding a vehicle as in [乗](乗.md), ride/board. The shared English
  spelling is excluded from meaning choices; it is not a shared Japanese meaning.` The titles `board; disc` and `ride;
  board` share the English word in two different senses. `乗.md` is unchanged (`[来, 東, 重]`).
