I found no actionable defect in either article. Each file gets CLEAN on all three facets for the text I read. Physical-phone checking is still outstanding.

**Snapshot:** Frozen commit `4a76569419b95c0e5d1823e1c62320066e127459`. No uncommitted teaching was included. Git was not run, so I did not check the commit or worktree state myself.

**Scope:** One reviewer, Claude Opus 5.5 (`claude-opus-5.5`). I read every file serially, one tool call at a time:
- **Guides:** `.github\copilot-instructions.md` lines 1–160 and 161–218, `content-structure.instructions.md`, `docs\content-format.md` lines 42–148, `docs\jlpt-levels.md` lines 1–110.
- **Teaching files:** all of `kanji\鯉.md` and `words\鯉.md`.
- **Metadata:** `batch-022-input-metadata.json`, including the raw KANJIDIC2 element.
- **Dictionary packets:** `batch-022-jmdict.xml` (lines 1–200 and 201–370, 18 families), `batch-022-comparisons-jmdict.xml` (lines 1–200 and 201–285, 10 families), `batch-022-supplement-jmdict.xml` (lines 1–26, 1 family). That is 29 families.
- **Comparison kanji:** `魚`, `理`, `量`, `恋`.
- **Comparison words:** `魚`, `恋`, `池`, `泳ぐ`, `量`, `金魚`.
- **Confusable pairs:** one scoped search of `docs\confusable-words.md`.
- **External source:** the Kotobank page via web_fetch.

**Verdicts:**
- **`kanji\鯉.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`words\鯉.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

Basis:
- **Metadata:** matches KANJIDIC2 exactly: 18 strokes, radical 195, grade 9, readings リ and こい, meaning "carp". The grade-9 note as name-use kanji (人名用漢字) is supported by 字通's 人名用漢字 label.
- **Reading choices:** リ is kept in the metadata but not quizzed. Its only packet word, 養鯉, is marked rare in JMdict (1914730). こい is quizzed, with a linked row to the word article.
- **Ordinary meaning:** JMdict 1271650 gives "common carp / koi carp", with コイ as a kana-only form. Seisenban sense ① calls 鯉 a freshwater fish (コイ科の淡水魚), with a dark grey wild form and bred varieties such as ニシキゴイ. That supports the "not only ornamental" claim.
- **Related words:** 錦鯉 にしきごい (1241360) and the 鯉のぼり / Children's Day explanation (1592910) match their entries.
- **"Containing 鯉 doesn't mean carp":** supported by 海緋鯉 (goatfish) and 伊勢鯉 (mullet).
- **Mnemonic:** clearly labelled as not etymology, and the shape descriptions of 理 and 量 are accurate.
- **Quiz choices:** the kanji distractors are "reason, logic", "quantity; amount" and "romantic love; longing". None is a defensible answer for "carp", so the default four-choice quiz needs no fallback. The 鯉 ↔ 魚 exclusion is a sensible guard between "fish" and the narrower "carp". 恋 is a homophone and 金魚 is "goldfish"; neither needs an exclusion. `confusable-words.md` lists no applicable pairs.
- **Examples:** 池に鯉がいます and 鯉が泳いでいます are natural, and their translations and particle notes are accurate.
- **Links and level:** links work in both directions, and the word article correctly has no `jlpt` level.

**Findings:** None.

**Optional:**
1. 字通 classifies 鯉 as 形声 (phono-semantic), with 里 as the sound element. A hedged, cited note could replace `structure-unclassified` later. Etymology is outside this batch's scope, and the current labelled mnemonic is fine.
2. The kanji card could say "traditionally flown", matching the word article's wording for 鯉のぼり.

**Limits:**
- **Kotobank:** the デジタル大辞泉 and 動植物名よみかた辞典 bodies were empty in the extraction. 字通's old-form glyphs are images I couldn't read. Only the Seisenban and 字通 bodies were actually read.
- **Packets:** these are frozen copies, not a fresh upstream lookup.
- **Confusable pairs:** checked by search only, not by reading the whole list.
- **Phone and native checks:** this was a text-only review. Font coverage, fresh Android, combined-main, CI and public ZIP checks, and physical-phone acceptance remain outstanding.
- **Process:** no overlapping tool calls.
