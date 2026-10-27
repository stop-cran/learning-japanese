## Snapshot
I reviewed frozen commit `9f6464f5255dd6ece56e4c949a7a3102ae38fbcb`, committed files only. I had file tools but could not run Git. I read the working tree on the author's word that it is clean and matches the snapshot. I could not check HEAD, the diff from baseline `d84e80eefe300d2eb93a2762c641952c6351d0d7`, or the 56-file scope.

## Scope
- **Reviewer:** claude-opus-5.5 (family claude). I worked alone, made no edits and used no other agents.
- **Assigned pages:** I read all 17 completely: `kanji\` 玉 瓶 甘 畜 略 畳 療 皮 皿 省 県 砂 硬 磨 祈, plus `words\家畜.md` and `words\略語.md`.
- **Related edits:** All 19 linked passages were checked in context; every link points to the correct card.
  - I read four of these articles in full: `words\県`, `硬貨`, `硬い` and `玉`.
  - Other pages read for comparison: `words\都`, `ほぼ`, `上手い`, the title and distractor lines of the older kanji cards, and a check of `docs\confusable-words.md`.
- **Evidence:** I read all of `batch-15.json`. I fetched one public page, Kotobank's 玉砂利 entry.
- **Not covered:**
  - the 15 stroke JSON files (converter output, not reviewed)
  - `manifest.json`
  - running the validator
  - the unchanged teaching text in the 19 related articles
  - `content-format.md` outside lines 18–109
- **Not read, as instructed:** the authoring notes, review files and other reviewers' output.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 玉 | NEEDS FIX (F1) | CLEAN | CLEAN |
| 瓶 | CLEAN | CLEAN | CLEAN |
| 甘 | CLEAN | NEEDS FIX (F3) | CLEAN |
| 畜 | CLEAN | CLEAN | CLEAN |
| 略 | CLEAN | NEEDS FIX (F2) | CLEAN |
| 畳 | CLEAN | CLEAN | CLEAN |
| 療 | CLEAN | CLEAN | CLEAN |
| 皮 | CLEAN | CLEAN | CLEAN |
| 皿 | CLEAN | CLEAN | CLEAN |
| 省 | CLEAN | CLEAN | CLEAN |
| 県 | CLEAN | CLEAN | CLEAN |
| 砂 | CLEAN | CLEAN | CLEAN |
| 硬 | CLEAN | NEEDS FIX (F4) | CLEAN |
| 磨 | CLEAN | CLEAN | CLEAN |
| 祈 | CLEAN | CLEAN | CLEAN |
| 家畜 | CLEAN | CLEAN | CLEAN |
| 略語 | CLEAN | CLEAN | CLEAN |

**What checks out:**
- **Metadata:** All 15 cards match the source record for strokes, grade tag, radical and number, and readings.
- **Readings:** There are 46 reading rows: 38 have real word examples and 8 are honestly labelled source-only (略 5, 畳 2, 県 1).
- **Spelling and reading restrictions are respected:**
  - すな is restricted to 砂 or 沙.
  - 略 as a spelling of ほぼ and 磨る are both flagged as rare kanji forms.
  - 畳む is usually written in kana.
  - The うまい entry and its senses are handled correctly.
- **Radicals:** Variant forms are explained (礻, 疒, 瓦, 石 at the bottom).
- **Distractors:** 44 of the 45 are semantically wrong, as required.
- **Word quiz:**
  - The `quiz_exclusions: [牛]` on 家畜 is justified: JMdict glosses 家畜 as "cattle", which is 牛's title.
  - 動物, ペット and 馬 follow the existing precedent for broader or narrower words, so no exclusion is needed.
  - 略語 overlaps with no other title.
  - No older two-choice card picks up a new synonym through the fallback.
- **Links:** Every new kanji has a useful linked word article.
- **External check:** Kotobank's Digital Daijisen gives 玉砂利 as 粒が丸く、やや大きい砂利 ("gravel with rounded, fairly large grains"), so the card's claim is confirmed.

## Findings
**F1. Minor. Correctness (quiz). `kanji\玉.md:11`, also lines 28 and 42**
- **Claim:** The distractor 王, whose title is "king" (`kanji\王.md:3`), is not clearly wrong for 玉.
  - JMdict entry 1921990, the 玉 ぎょく word the card uses for its ギョク row (line 28), has sense 7 "king (of the junior player)" (shogi, abbreviation).
  - So "king" is a defensible answer, and one of the three required wrong options is arguably correct.
- **Remedy:**
  - Replace 王 with an existing look-alike that is clearly wrong in meaning, such as 国 "country" or 全 "whole; complete".
  - Optionally, have the Note on line 42 mention the shogi use.
- **Evidence:** `batch-15.json:626-628` (entry) and lines 726–741 (sense 7).
- **Confidence:** Medium. The sense is real but specialized.

**F2. Minor. Scoped coverage (linking). `kanji\略.md:29, 44`**
- **Claim:**
  - ほぼ is introduced in the readings table and discussed in a Note, but it is not linked.
  - `words\ほぼ.md` exists, uses the same entry 1551940, and records 略 as a rare spelling (line 25).
  - This breaks the linking rule in `content-structure.instructions.md:20-21, 55`.
- **Remedy:** Link `[ほぼ](../words/ほぼ.md)`.
- **Confidence:** High.

**F3. Minor. Scoped coverage. `kanji\甘.md:43-44`**
- **Claim:**
  - The Notes discuss the うまい entry 1310460 and its skilled sense associated with 上手い, but do not link it.
  - `words\上手い.md` teaches exactly that entry, read うまい.
- **Remedy:** Link `[上手い](../words/上手い.md)`.
- **Confidence:** High.

**F4. Minor. Scoped coverage. `kanji\硬.md:39`**
- **Claim:**
  - The spelling comparison names 固い and 堅い as plain text, although `words\固い.md` and `words\堅い.md` both exist.
  - Only the kanji 固 is linked.
- **Remedy:** Link both word articles. Leave the unchanged plain mention in `words\硬い.md` alone.
- **Evidence:** All three spellings are entry 1257110 (`batch-15.json:4190`, `4361`, `4616`).
- **Confidence:** High.

## Optional
- **玉:**
  - In line 41, "Its separate ギョク row" has an unclear "its"; say "This card's ギョク row".
  - Consider noting that 玉 appears as a 王-shaped component in 球, 理 and 現.
- **Repeated wording:** Each of these rows says the same thing twice:
  - 甘 line 32: "usually-kana … (usually written in kana)"
  - 磨 line 32: "rare kanji spelling … (rare kanji spelling)"
- **瓶 line 43:** Entry 1194870 also lists はながめ and かへい as readings of 花瓶. はながめ contains the voiced form がめ of the かめ reading, so it could be acknowledged.
- **磨 line 42:** Could link `[する](../words/する.md)` where it contrasts the irregular verb する ("do").
- **畜 line 39:** Cites entries 1120990, 1231490, 1451470 and 1457390, which are not used on the card. Drop them or say they support the 家畜 comparisons.
- **Latent title overlaps:** These pairs share meaning words but never appear in the same quiz today. Recheck if distractors or quiz sizes change.
  - 略 / 省: omit
  - 玉 / 球: ball
  - 畳 / 折: fold
  - 療 / 治: heal
  - 磨 / 研: polish
  - 祈 / 願, 望, 希: wish
  - 県 / 府: prefecture
  - 畜 / 牛
  - 硬 / 固
  - 皿 / 版: plate

## Limits
- I could not run Git, so the snapshot, baseline diff, file scope, the claim that the 19 related edits only added links, and the claim that no older card changed are all unverified.
- I did not review the stroke JSON files or the manifest, or run the validator.
- I inferred quiz behaviour (fallback, reverse direction, larger quiz sizes) from the docs; I did not run it.
- `batch-15.json` is selected evidence. My Jisho lookup for 略く failed, so it settles nothing either way; the card's source-only はぶ.く row is honestly qualified regardless.
- Judgments of naturalness are mine, not a native speaker's.
