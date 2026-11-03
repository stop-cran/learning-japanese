Snapshot: Commit `f093f464c35423f728e3a0e756bee358b061d65c` in the dedicated worktree. I included no uncommitted teaching and reviewed no changed reused passages.

Scope:
- **Reviewer:** one reviewer, Claude Opus 5.5 (`claude-opus-5.5`), working read-only with one tool call per response.
- **Teaching files:** `kanji\榛.md` and `words\榛.md`, every line, for correctness, scoped coverage and how clearly the text reads.
- **Guidance read in full:** `.github\copilot-instructions.md` (in ranges), `content-structure.instructions.md`, `docs\content-format.md` lines 42–148 and `docs\jlpt-levels.md` lines 1–110.
- **Source data:** `batch-013-input-metadata.json`, which contains the complete raw KANJIDIC2 character entry.
- **Dictionary packets:** all four read completely, 41 entries in total: main 9, comparisons 21, notes 10, supplement 1.
- **Comparison kanji:** 木, 棒, 春 and 稲, read in full.
- **Comparison words:** 木, 植物, 植える, 植木, 栗, 楠 and 実, read in full.
- **Searches:** `docs\confusable-words.md`, searched only for this batch's terms. Titles in `kanji\` and `words\`, searched for hazel/alder/shrub/bush/nut.
- **Kotobank pages fetched:** 榛, 榛の木 and 榛莽.

Verdicts:
- `kanji\榛.md`: correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.
- `words\榛.md`: correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.

Basis:
- **Metadata:** The card matches KANJIDIC2: 14 strokes, radical 75, grade 9, on readings シン, ハン and kun readings はしばみ, はり, in source order. The nanori はい and はる are correctly left out.
- **Reading questions:** `quizOnyomi: []` turns off on-reading questions but keeps the readings. `quizKunyomi: [はしばみ]` has its own table row and links to `words/榛.md`. That pairing is supported by JMdict 2066150 and the Daijisen and Nikkoku Seisenban はしばみ entries.
- **Readings not asked:**
  - シン is supported by 榛莽 しんぼう/しんもう (JMdict 2843048, marked archaic). Seisenban defines it as 群がり茂った草木。また、その場所 ("dense vegetation; also, such a place") and glosses 莽 as くさむら ("thicket").
  - ハン is supported by the whole word 榛の木 はんのき (JMdict 1362540). The card correctly calls it on only by source classification, without deriving it from the kana.
  - はり is supported by JMdict 2447960 (archaic) and Daijisen/Seisenban, which give はり as an old name (古名) for ハンノキ.
- **Plant identities:** Hazel (はしばみ, a deciduous shrub of the birch family, カバノキ科落葉低木) and alder (はんのき/はり) are kept apart. 西洋榛 is *Corylus avellana* (JMdict 2066760). Seisenban says Europe cultivates related species for their fruit, which fits "associated with cultivated hazelnuts."
- **Example sentences:** 葉は円形で先がとがり、縁に…ぎざぎざ ("round leaves, pointed tip, jagged edge") supports "rounded shape" and the note about the leaf edge. 実…食用 ("the nut is eaten") supports "Hazel nuts are edible." Both sentences and their kana are natural. The article itself notes that the entry 榛の実 is marked as a rare term; using the ordinary phrase 榛の実 in an example is still fine.
- **Shape mnemonics:** 木 + 秦 with a 禾-shaped lower part is accurate (秦 = Qin dynasty, JMdict 2100140). It is labelled as a mnemonic, not etymology. The contrasts with 棒 (奉-shaped right side), 春 (日 below) and 稲 (禾 on the left) are accurate.
- **Wrong-answer choices:**
  - The kanji card's distractor titles ("rod; stick", "spring season", "rice plant") cannot be defended as answers for 榛.
  - No other card's title contains hazel, alder, shrub or bush.
  - The word article's exclusions are each justified on their own: 木 (JMdict includes "shrub; bush"), 植物 ("plant"), 植える (its title is "plant") and 植木 (garden tree/plant).
  - 栗, 楠 and 実 have different ordinary meanings, so leaving them unexcluded is fine. No plant/nut exclusion group is forced.
  - `docs\confusable-words.md` has no applicable pair.
- **Links:** All relative links point to existing files.

Findings: None.

Optional:
1. `kanji\榛.md`, シン row (line 32): the compound 榛莽 is described ("榛 followed by a character meaning thicket") but never written, so a learner can't recognize it in text. Writing 榛莽 or 榛＋莽 with kana would help if the second character displays. This is not required; the reading is unselected and archaic.
2. `words\榛.md`: optionally note that kana はしばみ also has unrelated homophones: 鷂 (sparrowhawk, an alternative reading) and 端喰 (a carpentry cross-piece) (JMdict 2222390 and 2848515).
3. Optionally mention the alternative reading はりのき for 榛の木 (Daijisen). The card does not claim はんのき is the only reading.

Limits:
- **Kotobank extraction:**
  - The 字通 section of the 榛 page returned only a heading, with no body.
  - On the 榛莽 page, the Daijisen しんぼう heading body was not extracted (only しんもう), and one Seisenban citation contained an image-only character.
  - None of these gaps affected a conclusion.
- **Packets:** The dictionary packets are frozen supplied copies, not a fresh upstream retrieval.
- **Partial reads:** `docs\confusable-words.md` and the title inventory were searched, not read in full. The app's fallback wrong-answer pool was judged from titles only.
- **Not covered:** This is a text-only review. Nothing was run on an Android device or physical phone, and there was no native-speaker check or measurement of frequency or readability. Font support for 莽 was not checked.
- **Process:** I made exactly one tool call per response, with no tool overlap.
