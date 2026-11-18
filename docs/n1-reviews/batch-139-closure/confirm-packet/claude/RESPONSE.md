# Author's statement for the reviewer of `reports-139\initial-claude.md`

This statement answers only the points in YOUR initial report. C1 and C2 are your report's own Findings labels, and O1 to
O4 are your Optional labels. The statement is the author's claim about what changed and why. Verify each claim against
the revised text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence. Card
line numbers refer to the revised cards in this packet; other line numbers refer to the named file in this packet unless
the original packet is named. Four of the 15 cards changed (嫁 嬢 宣 峠), the other eleven did not, one line of the word article 宴会 changed, and no
stroke file changed (see `CHANGES.md`). Give a disposition for each of C1, C2 and O1 to O4, and say whether the new
evidence resolves the 岬 limit described below.

## Findings

### C1 (minor): 宣 — the のたまう register

Author action: **changed.**

- `宣.md:40`, the のたま.う row, now reads `宣う のたまう - to say; to be pleased to say (honorific; usually written in
  kana; JMdict notes it was originally respectful and is nowadays often used sarcastically); no word article yet, not
  selected for questions here` (the parenthesis ended `usually written in kana)`).
- Support: `evidence\jmdict-cited-entries.xml`, entry 2842102 (宣う, 曰う; のたまう, のたもう; the sense note
  `originally respectful language; nowadays oft. used sarcastically`).

### C2 (minor): 嫁 — the dialect tag on "wife"

Author action: **changed** as you proposed.

- `嫁.md:23` now reads `its third sense, which JMdict marks as Kansai dialect, is "wife."` (it read `its third sense is
  "wife."`).
- Support: `evidence\jmdict-cited-entries.xml`, entry 1191680 (嫁 よめ; sense 3 "wife" carries the Kansai-ben dialect
  tag).

## Optional points

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| O1 | **changed** | `嬢.md:47`, `:51` | A new Notes bullet: `Related forms in JMdict: お嬢様 おじょうさま, "(another's) daughter," marked polite language, and "young lady (of pampered upbringing)"; 嬢ちゃん じょうちゃん, "young girl; young lady"; and 嬢さん じょうさん, "(another's) daughter; young lady." 嬢さん read とうさん is a Kansai-dialect honorific, "daughter (of a good family)."` JMdict marks only the first sense of お嬢様 as polite language, so "polite" is attached to that sense alone. Line 51 (Metadata, line 50 before) adds entries 1694880, 2836096, 2230740 and 2216510. Support: `evidence\jmdict-cited-entries.xml`, those four entries. |
| O2 | **changed** | `宣.md:31`, `:57` | The sentence now names the readings: `The character entry gives the kun readings のべる, のる and のたまう; only のたまう is a KANJIDIC2 reading.` It continues: `JMdict has 宣べる only as a rarely used spelling of 述べる のべる, "to state; to express; to say"; its one word that writes のべ with 宣 as the main spelling is 宣べ伝える のべつたえる, "to proclaim (e.g. gospel)." JMdict has no entry writing のる with 宣.` (it read `Of the kun readings in the character entry, only のたまう is a KANJIDIC2 reading.`). Line 57 (Metadata) adds entries 1340820 and 2096040. Support: the original packet's `evidence\public-source\weblio-宣.txt` line 6 (`［訓］のべる のる のたまう`); `evidence\jmdict-cited-entries.xml`, entries 1340820 (述べる; 宣べる is a `rarely used kanji form`) and 2096040 (宣べ伝える); the original packet's `evidence\jmdict-families.xml` for the absence of のる written with 宣 (it holds every JMdict entry that writes any kanji of the batch). |
| O3 | **changed** | `words/宴会.md:32` | Line 32 now ends `the kind of gathering. The on readings are`, so line 33, `エン + カイ.`, no longer follows a colon. This is your proposed wording. The batch had already edited this paragraph, so the change stays within the batch. The declared remark edit for 宴会 in `evidence\word-remarks.json` now covers this line, and `checks\linkplan.txt` reports 0 problems. 平日 and 閉会 still use the colon form; they are outside the batch and are left as they are. |
| O4 | **no change** | `峠.md` title | You found the title acceptable as it stands; it stays `mountain pass; peak; climax`. |

## Limits in your report

- **岬's Daijisen character entry.** `evidence\weblio-岬-character.txt` is the Digital Daijisen character entry for 岬
  on its Weblio page, re-extracted because the first Daijisen block on that page is a word entry. It contains the
  headword `こう【 ▽ 岬】` with `［音］ コウ （ カフ ）（漢） ［訓］ みさき`, one sense, `みさき。「 岬角 ( こうかく )」`,
  and the word entry `み‐さき【岬／ ▽ 崎】 … 海や湖などに 細長く 突き出て いる 陸地`. The three claims you could not
  verify are at `岬.md:23` and `:25`, unchanged. Please check them against this file.
- No disposition is needed for the other limits. The Android JVM content tests and the Kotlin reading-audit cross-check
  were not run for this revision either (see `CHANGES.md`).
- "Card text" in the audits' provenance labels: you assumed correctly. It is the tools' label for a reading supplied
  through `--extra`, not a claim about card prose (`evidence\extras-correction.txt`, first paragraph).

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk.

- **峠–通 and 峠–経** (`峠.md:14`, `:48`, `:49`, `:51`). 通 and 経 are removed from 峠's `quiz_exclusions`. Their titles,
  "pass through; commute" and "pass through; sutra," are not meanings of a mountain pass, and 峠's title is not a
  meaning of either; they shared only the English word "pass." The Notes bullet at line 48 no longer names them, and a
  new bullet at line 49 sets the two ideas apart. Line 51 (Metadata) adds entries 1433030 (通る) and 1251110 (経る).
  The 頂, 山 and 旬 exclusions stay. Neither 通 nor 経 has a `quiz_exclusions` list, so both pairs are now unexcluded.
  Support: `evidence\jmdict-cited-entries.xml`, entries 1433030 and 1251110; `checks\link-targets.tsv` for the titles.
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
