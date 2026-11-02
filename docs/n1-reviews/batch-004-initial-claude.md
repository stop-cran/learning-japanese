I found no actionable defects in batch 004. All seven files are CLEAN on all three facets, and nothing was edited.

**Snapshot:** `bfea5052387e2327dac4e365ec11ccca1289b914` (base `c7b7bdc`), committed teaching only. I also read the separate evidence-only file `docs\n1-reviews\batch-004-input-metadata.json`. No uncommitted teaching was included.

**Scope:** One reviewer, Claude Opus 5.5, reading strictly one file at a time. Correctness, scoped coverage and phone comprehensibility were checked separately for each file.
- **Read in full:** `kanji\杉.md`, `kanji\桐.md`, `kanji\柳.md`, `words\桐.md`, `words\柳.md`, `words\川柳.md`, `words\杉.md` and the input metadata.
- **Dictionary packets:** both read in full. Together they hold all 23 JMdict families.
- **Distractor cards:** 形 村 羽 同 相 卵 印, plus `kanji\川.md`.
- **Comparison words:** 木 植物 植える 俳句 句 詩 茶, and `docs\content-format.md` lines 40–157.
- **Kotobank:** 桐人 (full page). Three pages were cut off by length limits, but the needed headings were visible: 桐油, 川柳 (the せんりゅう, かわやなぎ and かわやぎ headings plus Nipponica 川柳（短詩）) and 桐 (the きり and 字通 headings).
- **Not read:** お茶, 材木, 木材, 材料 and 植木; the Kotobank 柳 page.

**Verdicts** (correctness / scoped coverage / comprehensibility):
- `kanji\杉.md`: CLEAN / CLEAN / CLEAN
- `kanji\桐.md`: CLEAN / CLEAN / CLEAN
- `kanji\柳.md`: CLEAN / CLEAN / CLEAN
- `words\桐.md`: CLEAN / CLEAN / CLEAN
- `words\柳.md`: CLEAN / CLEAN / CLEAN
- `words\川柳.md`: CLEAN / CLEAN / CLEAN
- `words\杉.md` (changed passage only, line 23): CLEAN / CLEAN / CLEAN. The new `../kanji/杉.md` link is correct and completes the 杉 kanji ↔ word link pair.

**Key checks behind the verdicts:**
- **Metadata:** every on/kun list, stroke count, radical and grade matches KANJIDIC2 exactly, with full lists and order intact.
- **Unselected readings:** サン, トウ and ドウ each have their own reading row with a clearly marked unselected or source-only explanation.
  - ドウ is backed by 字通 【桐人】どうじん, 桐の木の木偶.
  - トウ is backed by JMdict 1240720 (桐油 tung oil). The 日本国語大辞典 heading きりあぶら (アブラギリ seeds) supports the note that this oil does not come from キリ.
- **Reading-key suitability:**
  - 杉 asks only すぎ; 桐 asks only きり. Each links to its own word article (JMdict 1373520 and 1240710).
  - 柳 asks リュウ (key りゅう) and やなぎ (key やなぎ).
    - リュウ comes from 川柳 せんりゅう (JMdict 1390110, news1), where 川 gives セン (on 川's card) and 柳 gives リュウ. That is a useful, correctly split prompt.
    - やなぎ comes from JMdict 1538490.
  - The keys match the mechanical projection. Disabling the on'yomi questions for 杉 and 桐 is justified.
- **Meaning distractors:** each displayed title is clearly wrong for its target:
  - 杉: 形 "shape; form", 村 "village", 羽 "feather; bird counter".
  - 桐: 同 "same, equal", 相 "mutual; aspect", 村 "village".
  - 柳: 卵 "egg; ovum", 印 "stamp; mark", 相 "mutual; aspect".
- **Word quiz exclusions:** these fit the displayed titles. Examples: 木 "tree; wood", 植物 "plant; vegetation" and 植える "plant" for 桐 and 柳; 俳句 "haiku", 詩, 句 and 柳 for 川柳. The 茶 and お茶 exclusions are cautious but harmless.
- **Dictionary claims:**
  - The 川柳 name origin (柄井川柳の号) and the 17-sound form are confirmed by Nipponica and 日本国語大辞典.
  - The note that 川柳 doesn't require a seasonal word matches 世界大百科事典 (季語や切字を要求せず).
  - The JMdict limits are stated correctly: ようりゅう only with the spelling 楊柳, the weeping-willow sense only for やなぎ/ヤナギ, かわやぎ marked archaic, the coarse-tea sense only for 川柳, and 椙 marked rare.
  - The 桐 wood uses (chests, the koto and biwa) are confirmed by 日本国語大辞典.

**Findings:** none.

**Optional:**
- `kanji\柳.md:42`: "印 … has a simpler left side" is vague. "印 lacks 木; it resembles only the 卯-like right part" would be clearer.
- `words\杉.md:9` (unchanged, reused): 杉 excludes only 木, while 桐 and 柳 also exclude 植物 and 植える. Adding those two would make the tree set consistent.
- `kanji\桐.md` and `words\桐.md`: JMdict 1586170 marks 梧桐/あおぎり as usually written in kana. The articles could say so.

**Limits:**
- The JMdict and KANJIDIC2 evidence is the frozen packets I was given; I didn't retrieve those myself. Only the Kotobank pages above were live fetches, three of them cut off by length.
- I didn't fetch the Kotobank 柳 page; JMdict covered those claims.
- Unchanged 杉 text and the unchanged comparison articles were not re-certified.
- This is a textual review only. It does not certify how the app actually builds questions or handles reading keys, real phone display, native-speaker judgement, or learning effectiveness.
