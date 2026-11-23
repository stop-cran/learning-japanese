# Author's statement for the reviewer of `reports-139\initial-gpt.md`

This statement answers only the points in YOUR initial report: G1 is your report's own Findings label, and Optional 1
to 3 are the numbered items of its Optional section. The statement is the author's claim about what changed and why.
Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this
text as evidence. Card line numbers refer to the revised cards in this packet; other line numbers refer to the named file
in this packet unless the original packet is named. Four of the 15 cards changed (嫁 嬢 宣 峠), the other eleven did
not, one line of the word article 宴会 changed, and no stroke file changed (see `CHANGES.md`). Give a disposition for
G1 and for Optional 1 to 3.

## Findings

### G1 (minor): 峠 — distinguish a mountain pass from passing through

Author action: **changed** as you proposed.

- `峠.md:14`: `quiz_exclusions: [頂, 山, 旬]`. 通 and 経 are removed; the 頂, 山 and 旬 exclusions stay. Neither 通 nor 経
  has a `quiz_exclusions` list, so the pairs 峠–通 and 峠–経 are now excluded by neither side (the app excludes a pair
  when either card lists the other, `evidence\QuizBuilder.kt` line 26).
- `峠.md:48` no longer names 通 and 経 or the sense "pass": it now reads `[頂](頂.md), "summit; receive," [山](山.md),
  "mountain," and [旬](旬.md), "ten days; peak season," overlap the senses "peak" and "mountain" that 峠 and its word
  carry. … Do not treat "peak" as exclusive to any one character.`
- `峠.md:49` is a new Notes bullet that states the distinction: `A mountain pass is 峠. Passing through a place is a
  different idea, expressed by verbs such as 通る とおる, to go by or through a place, and 経る へる, for time to pass or
  to go through a place. English "pass" covers both ideas, so [通](通.md), "pass through; commute," and [経](経.md),
  "pass through; sutra," remain ordinary wrong options for 峠.`
- `峠.md:51` (Metadata; line 50 before) adds entries 1433030 (通る) and 1251110 (経る), because the card now names
  both words.
- Support: `evidence\jmdict-cited-entries.xml`, entries 1433030 and 1251110; `checks\link-targets.tsv` for the titles
  of 頂, 山, 旬, 通 and 経. `checks\quiz-safety.txt` is identical to the original packet's
  `evidence\audits\quiz-safety.txt`; 峠's three curated distractors (岸, 島, 上) still fill all three wrong slots of
  its meaning question, so 通 and 経 become possible wrong options only in pools where a curated slot is unavailable.

## Optional points

| Item | Author action | Where | Reason |
| --- | --- | --- | --- |
| Optional 1 (shorten reference inventories) | **declined** for this batch | 密, 宣, 審, 屈, 属, 寂 (unchanged except as listed in `CHANGES.md`) | As you note, each card presents its main idea first and labels the later material as reference. Published N1 cards from earlier batches use the same layout, with reference bullets of similar length (for example `節.md`, `隔.md`, `請.md` and `義.md` in the original packet's `repo\kanji\`). 密's bullet is the longest of them, and trimming only this batch would leave the format uneven. Splitting or moving such inventories is a format change for all N1 cards, recorded for a later format pass rather than made here. |
| Optional 2 (崩: selected readings versus scheduled questions) | **declined** | `崩.md:40` (unchanged) | "Practice selects くず.れる and くず.す" names the readings selected in the card's metadata, which you confirmed are both taught correctly. "Practice selects" is the wording used in 184 kanji cards for exactly that metadata, and no card describes how the app schedules readings that share a stem (`ReadingCard.quizReadings`). Explaining that app behaviour on one card would make 崩 read differently from every other card with paired verbs; if it is worth explaining, it belongs in app or format documentation. |
| Optional 3 (keep the English-homonym rationale explicit) | **no action needed** | — | Agreed. The G1 change follows this direction: the 峠 exclusions that rested only on English "pass" are removed, and the remaining 頂, 山 and 旬 exclusions are stated by sense. 宴's 党 note is unchanged. |

## Limits in your report

No disposition is needed. The Android JVM content tests and the Kotlin reading-audit cross-check were not run for this
revision either (see `CHANGES.md`).

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk. They answer the other reviewer's points.

- **宣 のたまう register** (`宣.md:40`): the のたま.う row now adds `JMdict notes it was originally respectful and is
  nowadays often used sarcastically`. Support: `evidence\jmdict-cited-entries.xml`, entry 2842102.
- **宣 kun readings** (`宣.md:31`, `:57`): the sense paragraph names the character entry's kun readings のべる, のる and
  のたまう, says that JMdict has 宣べる only as a rarely used spelling of 述べる and that its one word writing のべ with 宣
  as the main spelling is 宣べ伝える, and says that JMdict has no entry writing のる with 宣. Line 57 (Metadata) adds
  entries 1340820 and 2096040. Support: the original packet's `evidence\public-source\weblio-宣.txt` line 6;
  `evidence\jmdict-cited-entries.xml`, entries 1340820 and 2096040; the original packet's
  `evidence\jmdict-families.xml`.
- **嫁 "wife"** (`嫁.md:23`): the third sense is now said to be marked Kansai dialect in JMdict. Support:
  `evidence\jmdict-cited-entries.xml`, entry 1191680.
- **嬢 related forms** (`嬢.md:47`, `:51`): a new Notes bullet names お嬢様, 嬢ちゃん and 嬢さん (じょうさん, and the
  Kansai-dialect honorific とうさん), calling only the first sense of お嬢様 polite language, as JMdict marks it. Line
  51 (Metadata) adds entries 1694880, 2836096, 2230740 and 2216510. Support: those four entries in
  `evidence\jmdict-cited-entries.xml`.
- **宴会 character note** (`words/宴会.md:32`): `the kind of gathering:` now reads `the kind of gathering. The on
  readings are`, so the reading line `エン + カイ.` no longer follows a colon. Your report found that the 20 word diffs
  contain only the declared link wrapping and the four declared remark changes; that still holds, because the declared
  remark edit for 宴会 now covers this line (`evidence\word-remarks.json`, `checks\linkplan.txt`: 0 problems).
- **Reading-audit extras.** The original packet says the audits' `--extra` readings include every kun reading in the
  Daijisen character entries, but 宗 たっとぶ and 宣 のる were missing. Both are now included, and no hit or collision
  count changed. Details: `evidence\extras-correction.txt` and `CHANGES.md`, "Reading audits."

## Process notes

- `3b6f9727` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `a47efe9a`. Three
  earlier local versions of it were replaced before this packet was built and were neither reviewed nor published.
  - `c2b9973b` glossed 通る and 経る in quotation marks with partial JMdict glosses. It said that JMdict has 宣べる only
    as a rare spelling without mentioning 宣べ伝える, and it called both senses of お嬢様 polite language.
  - `8530c8bb` fixed only the 通る/経る wording.
  - `2dacd6e5` fixed the 宣べ伝える and お嬢様 points but left 宴会 unchanged.
- The checks in `checks\` were run on the committed revision.
