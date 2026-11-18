# Author's statement for the reviewer of `reports-135\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 to G4 are your report's own Findings labels. Your
Optional bullets had no labels; here they are OA, OB and OC, in the order they appear in your report. GR is the
"Add a regression" sentence that ends the remedies of G1 and G2. The statement is the author's claim about what changed
and why. Verify each claim against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and independent sources;
do not rely on this text as evidence. Card line numbers refer to the revised cards in this packet; other line numbers
refer to the named file in this packet. Nine of the 15 cards
changed (博 履 巡 弾 恵 憶 揚 救 模) and the other six did not (see `CHANGES.md`). Give a disposition for each of G1, G2,
G3, G4, GR, OA, OB and OC.

## Findings

### G1 (major): 救 — グ can be offered as a wrong answer to the キュウ question

Author action: **changed**, by the first route of your remedy: the curated provider was replaced. The pinned KANJIDIC2
metadata of 救 is unchanged; only `distractors` (line 13) changed.

- `救.md:13`: `distractors` is now `[敬, 球, 教]` (it was `[求, 球, 教]`). 敬, which also has 攵 at the right, has the on
  readings ケイ and キョウ (`checks\reading-exposure.txt` line 331), so it offers ケイ or キョウ, never ぐ.
- `救.md:48`: 敬 "respect; honor" is added to the look-alike bullet. 求 stays there, and the mnemonic (line 27) still names
  求 as the shape at the left.
- `救.md:49` (new bullet): Kanjipedia marks the on readings グ and ク and the kun reading たすける as outside the official
  table; they are not in KANJIDIC2 or the card's metadata, so they are not asked, and the quiz does not offer them as
  wrong answers; for that reason 求, which is also read グ, is not a curated wrong-answer card. Source:
  `evidence\kanjipedia-救.txt` line 6.
- Replacement and fallback paths, as your remedy asks (`checks\reading-exposure.txt`, 救 block, lines 330-358; this round
  the audit treats every Kanjipedia 外 reading of the 15 kanji as attested, `evidence\kanjipedia-outside-readings.json`):
  - キュウ prompt, N1 and All stacks: 敬, 球 and 教 give 2 outcomes (球's キュウ is excluded, and 敬 can repeat 教's
    キョウ), and the fallback fills the remaining one or two slots; 41 drawable wrong options (lines 337-338).
  - ぐ (offered by 供, 具, 工 and 求) and く (offered by 久, 九 and ten other cards) cannot be drawn in the N1 stack, the
    All stack or the Starter session, nor in a Starter session that also borrows any single holder card (lines 340-345).
  - すくう prompt: the three curated cards fill every wrong slot in the N1 and All stacks, and たすける (offered by 助 and
    賛) cannot be drawn in any of the three pools, nor with either holder borrowed (lines 350-355).
  - 敬, 球 and 教 are not starter cards, so in the Starter session both prompts take all three wrong options from the
    fallback (lines 339 and 352), as they did at the reviewed snapshot with 求, 球 and 教.
- Before and after: the same command run on the reviewed snapshot (`evidence\reading-exposure-163b384e.txt`) reports
  ぐ as a production hit in the N1 and All stacks, offered by 供, 具, 工 and 求 (line 338), which confirms your finding.

To verify: that no allowed path in `evidence\KanjiReadings.kt` can now offer ぐ, く or たすける for 救, and that 敬 is a
fair look-alike for the meaning quiz (`checks\quiz-safety.txt` line 37: `respect; honor | ball; sphere | teach,
instruct`).

### G2 (major): 巡 — the fallback can offer まわる as a wrong answer to the めぐる question

Author action: **changed**, by the second route of your remedy: curated providers that fill all three kun slots.

- `巡.md:13`: `distractors` is now `[川, 道, 達]` (it was `[順, 川, 純]`). 道 "road, way" and 達 "reach, plural suffix" have
  the same 辶 as 巡 (line 49 adds them to the look-alike bullet; 順 and 純 stay there as kanji also read ジュン).
- 川, 道 and 達 are all starter cards (`checks\reading-exposure.txt` lines 132-134), so they are in all three pools the
  audit checks. In the N1 stack, the All stack and the Starter session they fill all three wrong slots of both the ジュン
  and the めぐる prompt, and the fallback is never consulted (lines 138-140 and 145-147). まわる, offered by 回, cannot be
  drawn in any of these pools, nor in a Starter session that also borrows 回 (lines 148 and 150).
- `巡.md:37` adds: Kanjipedia lists まわる as a kun reading outside the official table, so this card's quiz does not offer
  まわる as a wrong answer. Source: `evidence\kanjipedia-巡.txt` line 6.
- Before and after: the same command run on the reviewed snapshot (`evidence\reading-exposure-163b384e.txt`) reports
  まわる as a production hit in the N1 and All stacks, offered by 回 (line 148), which confirms your finding. As you note,
  回 in `quiz_exclusions` does not affect the reading quiz; it is kept there for the meaning quiz.
- The meaning options are now `river | road, way | reach, plural suffix` (`checks\quiz-safety.txt` line 15).

To verify: that no allowed path can now offer まわる for 巡, and that 道 and 達 are fair meaning-quiz look-alikes.

### G3 (minor): 博 — the mnemonic adds a dot that 甫 already has

Author action: **changed.**

- `博.md:27` now reads `At the right is 甫, which has no card here, standing over [寸](寸.md), "sun (length unit); small";
  the dot at the top right is part of 甫 itself.` The phrase `a shape like 甫 with an extra dot` is gone; the
  modern-shape disclaimer is unchanged.
- Support: `evidence\kanjidic2-甫.xml` line 20 (7 strokes); `evidence\kanjivg\0752b.svg` (甫, 7 paths); in
  `evidence\kanjivg\0535a.svg` the group 尃 (line 44) holds 甫 (lines 45-59, strokes 3 to 9, the dot being stroke 9 at
  lines 56-57) over 寸 (lines 61-65, strokes 10 to 12).
- Disclosure: KanjiVG marks this 甫 `kvg:variant="true"` and 尃 `kvg:phon="尃"`, and also tags strokes 3 to 8 (甫
  without its dot) and 寸 as parts 1 and 2 of 専 (lines 46 and 60). Your remedy said "a 甫-like seven-stroke shape"; the
  card names 甫 directly, because the component is the same seven strokes, dot included. It still makes no claim about
  formation or sound.

To verify: that line 27 is accurate, and whether naming 甫 directly, instead of "甫-like", is acceptable given the
KanjiVG variant flag.

### G4 (minor): 弾 — the sense catalog is a wall of text

Author action: **changed**, as your remedy describes.

- `弾.md:25-33`: a one-line intro, then five short bullets, one per Daijisen sense, each with one example and its kana
  (弾奏 だんそう, 弾指 だんし, 弾圧 だんあつ "besides 弾劾", 弾力 だんりょく, 爆弾 ばくだん), then one sentence on the
  counter use with a pointer to the Notes.
- `弾.md:67`: the other ten examples (弾琴, 連弾, 糾弾, 指弾, 弾性, 弾丸, 弾薬, 実弾, 銃弾, 砲弾) with their kana and
  glosses, and the two JMdict counter glosses, are a "For reference" bullet at the end of the Notes, after the core
  teaching content. Nothing was dropped or added; only trailing punctuation changed (`CHANGES.md`).
- The reading table, including its rare-reading qualifications, is unchanged.

To verify: that the new layout is readable on a phone and that line 67 keeps every example and gloss of the old line 25.

## GR: "Add a regression" (G1 and G2 remedies)

Author action: **declined.**

- The reading-option builder is the Android app's Kotlin code (`evidence\KanjiReadings.kt`). The content repository has
  no reading-quiz builder or simulator to attach a regression to: its `tools\validate.py` checks the form of the quiz
  fields (for example, that `quizOnyomi` and `quizKunyomi` readings come from the card's readings and that `distractors`
  names existing cards) but never builds a question or its wrong options. There is no JDK in the author's environment,
  so a Kotlin test could not be run.
- The lasting check is the audit: `checks\reading-exposure.txt` enumerates every outcome of both questions in the N1
  stack, the All stack and the Starter practice session, with the Kanjipedia 外 readings added, and
  `evidence\reading-exposure-163b384e.txt` shows the same command reporting both hits on the reviewed snapshot. The audit
  is the author's Python port of the Kotlin sources, not the app's own code (`CHANGES.md`).
- From batch 136 on, the authoring notes will make it a standing step to fetch the Kanjipedia readings of every new kanji
  and run this audit with them before freezing a batch.

## Optional points

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| OA | **partly changed** | `弾.md:25-33`, `:67` | Only 弾 was compressed (G4). The sense paragraphs of 博 (704 characters), 厳 (739), 履 (838), 恵 (742), 揚 (829) and 模 (751) are unchanged; 弾's was 1,050. As you note, their central ideas are already stated clearly; rewriting six more reviewed, correct paragraphs in a confirmation round adds regression risk for a style gain. The author will record the 弾 layout in the authoring notes as the preferred form for long sense lists in later batches. |
| OB | **changed** | `巡.md:39`, `恵.md:40`, `揚.md:40` | Each now says that the reading `supplies the one question for that stem, shown as` めぐる, めぐむ or あげる (they read `supplies the めぐ question` for 巡 and 恵, and `so the あ question comes from あ.げる` for 揚). The displayed form matches `ReadingKey.display` in `evidence\KanjiReadings.kt` (lines 31-35), which drops the okurigana dot. |
| OC | **changed for this batch** | `evidence\kanjipedia-outside-readings.json`; `checks\reading-exposure.txt`, `checks\reading-options.txt` | Both audits now also treat as attested every reading Kanjipedia marks as outside the official table (外) for the 15 kanji, passed with `--extra` (line 1 of each file; the tool labels them `(card text)`). Every other Kanjipedia reading of the 15 kanji is already in the card's metadata, so it is excluded as the target's own reading. Result: 0 production hits, 0 padded-session hits, 25 latent collisions. Other public dictionaries are not parsed. The audit tool does not fetch Kanjipedia itself; the author fetches the entries with a separate script, and the authoring notes will make this a standing step from batch 136 on (see GR). |

## Other limits in your report

No disposition is needed for these.

- You could not see your model identifier. The closure record will take it from the author's session record of your run
  (`gpt-6.1-sol`).
- G1 and G2 were analytical reachability proofs. The before-and-after audits in this packet reach the same results for
  the reviewed snapshot; they too are Python ports, not a run of the app or of Kotlin tests, which were again not run.
- kanjiapi.dev returned HTTP 403 for you. This round the packet supplies the pinned KANJIDIC2 record of 甫 and the
  KanjiVG files of 博 and 甫 (`evidence\README.md`).

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk.

- **憶: the Joyo table's 臆 row** (`憶.md:25`, `:49`). After the existing JMdict sentence (臆説, 臆念, and 臆測 as a rarely
  used spelling of 憶測), line 25 now adds that the official Joyo table gives 臆 its own row, with オク and the examples
  臆説, 臆測 and 臆病 おくびょう, "cowardly; timid; easily frightened," and notes that 臆説 and 臆測 are also written 憶説
  and 憶測, "so the table accepts both spellings." Line 49 adds JMdict entry 1182790 (臆病). Support:
  `evidence\joyo\p18.txt` lines 45-47; `evidence\jmdict-cited-entries.xml` (1182750 at lines 4-19, 1182790 at 23-45,
  1589020 at 49-70).
- **履: the ぞう of 草履** (`履.md:36`, `:51`). Line 36 now says `The ぞう belongs to 草: Daijisen spells it ザウ in
  historical kana, the voiced form of サウ, its historical spelling of 草's ソウ.` and uses `accordingly` instead of
  `which is why` for the Joyo table's appendix listing. Line 51 adds Digital Daijisen links for 草履 and 草. Support:
  `evidence\daijisen-草履.txt` line 7 and `evidence\daijisen-草.txt` line 7.
- **模: 相模 and 酸模** (`模.md:36`). `Both are learned here as whole words.` became `Each is read as a whole word, so its
  reading is not split between its kanji.`

## Process notes

- `2ef25d33` is the third local version of the fix commit; the two earlier ones (`bf9262a0`, `7e178bfd`) were never
  published or reviewed. `diffs\fix.patch` is the whole change from the reviewed snapshot `163b384e`.
- An earlier local draft used 返 and 送 instead of 道 and 達 for 巡. They are not starter cards, so the Starter session
  still had to use the fallback; they were replaced before this snapshot.
