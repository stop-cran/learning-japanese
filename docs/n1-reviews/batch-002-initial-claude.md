I found three minor defects across `kanji\稲.md`, `words\水稲.md` and `words\稲.md`. The other six files are clean, and all four kanji keep their full KANJIDIC2 metadata exactly.

**Snapshot:** 9fee5174f695d5cbc1a45752e633c9622b011e38, committed teaching only (base 560c9dd). Added evidence-only input: `docs\n1-reviews\batch-002-input-metadata.json`, plus the three frozen JMdict packets. No uncommitted teaching was reviewed.

**Scope:** Model: Claude Opus 5.5. I reviewed all three facets for each of the nine in-scope files.
- **Read in full:** the 4 kanji cards, the 5 word articles (稲 is checked only for how its changed sentence fits in), the 3 XML packets (19 families: 14+2+3), the metadata JSON, and the word articles くだらない, 屑, 塵 and 米.
- **Read in part:**
  - `content-format.md` lines 40–157.
  - ご飯 and 木 lines 1–12.
  - A grep of title and on/kun readings in the 12 required distractor cards (I did not read their bodies).
  - A grep of overlapping titles across `words\` and `kanji\`.
  - A glob confirming 耳, 水 and 米 kanji cards and `strokes\稲.json` exist, and a grep of that file, which has no component data.
- **Not read:** distractor card bodies, older comparison articles, and anything else.
- **Process breach:** I read 桑.md and 芋.md in one parallel call, against the serial-only instruction. All other calls were serial.

**Verdicts** (correctness / scoped coverage / comprehensibility)
- `kanji\稲.md`: **NEEDS FIX** / CLEAN / CLEAN
- `kanji\穂.md`: CLEAN / CLEAN / CLEAN
- `kanji\桑.md`: CLEAN / CLEAN / CLEAN
- `kanji\芋.md`: CLEAN / CLEAN / CLEAN
- `words\稲穂.md`: CLEAN / CLEAN / CLEAN
- `words\水稲.md`: CLEAN / **NEEDS FIX** / CLEAN
- `words\桑.md`: CLEAN / CLEAN / CLEAN
- `words\芋.md`: CLEAN / CLEAN / CLEAN
- `words\稲.md` (changed passage, line 24): CLEAN / **NEEDS FIX** / CLEAN. The new link `../kanji/稲.md` is correct and sits where 稲 is first explained. The coverage fix is only for the shared quiz exclusion in Finding 2.

**Reading metadata audit:** Every reading matches KANJIDIC2 exactly, in order, and has its own Readings row.
- 稲: on [トウ, テ], kun [いね, いな-]
- 穂: on [スイ], kun [ほ]
- 桑: on [ソウ], kun [くわ]
- 芋: on [ウ], kun [いも]
- Stroke counts, radicals, grade 8 and N1 also match.
- テ is marked as source-only. スイ, ソウ and ウ each have a correctly split example:
  - 出穂 (しゅつ+すい): 1779070
  - 桑園 (そう+えん): 1247070
  - 海芋 (かい+う), usually written in kana: 1772660
- Quiz selections are exact subsets of the full lists.

**Are the actual quiz keys suitable?** Yes.
- 稲 とう: 水稲 = 水 スイ + 稲 トウ (1371310). Suitable.
- 稲 いね: the 稲 word (1167820). Suitable.
- 稲 いな: the bound form in 稲穂 = いな + ほ (1167920, with 穂 ほ from 1514780). It is a distinct stem from いね, so it is a separate, useful key.
- 穂 ほ: from 稲穂. Suitable.
- 桑 くわ and 芋 いも: from their own word articles. Suitable.
- The empty on-reading lists for 穂, 桑 and 芋 are justified; the cards explain each omitted on reading.

**Findings**
1. **Minor; correctness;** `kanji\稲.md:24`.
   - **Claim:** the mnemonic says "claw-like strokes above the 日 shape". The lower right of 稲 is 旧 (a vertical stroke plus 日), not 日.
   - **Impact:** a learner may picture or write the component one stroke short.
   - **Remedy:** say "above the 旧 shape (日 with a vertical stroke on its left)".
   - **Evidence:** KANJIDIC2 gives 14 strokes. 禾 (5) + 爫 (4) + 旧 (5) = 14, while 日 would give 13. The component breakdown is from my own knowledge, not a supplied source.
   - **Confidence:** medium-high.
2. **Minor; scoped coverage (word quiz);** `words\水稲.md:4`, with `words\稲.md:4`.
   - **Claim:** 水稲 is itself a kind of rice plant. JMdict 1371310 gives "wet-land rice", and its counterpart 陸稲 (1585100) is glossed "dry land rice plant". The article also calls 稲 "the broader plant word" (`水稲.md:27`).
   - **Impact:** when the quiz shows "rice plant", both 稲 and 水稲 are defensible answers. Sharing the 稲 kanji and the agriculture tag makes it likely they appear together.
   - **Remedy:** add `quiz_exclusions: [稲]` to 水稲. One direction is enough.
   - **Confidence:** medium. This is a whole-versus-kind overlap, so you may judge a single best answer acceptable.

**Other checks (no defect)**
- The 12 distractor titles are defensibly wrong for each kanji, including against secondary senses of 穂 (tip, crest, scion) and 芋 (bumpkin, worthless thing).
- Kanji titles are unique.
- Every kanji card and its word articles link to each other, including the reused 稲.
- The 芋 exclusions of くだらない and 屑 are defensible. 塵 ("rubbish; garbage") does not need one, because 芋's "dud / worthless thing" sense is not discarded refuse.
- 2-way links between the existing 水 card and 水稲 are outside this scope.

**Optional**
- 桑/木: "tree; wood" overlaps 桑 in the same whole-versus-kind way. It is less likely to come up, since the two share no kanji or tag.
- `kanji\桑.md`: 桑園 has no frequency tags but is listed under "Common words". It could appear only in the Readings table.
- `words\水稲.md`: could add that 陸稲 is also read おかぼ (1585100).
- `words\芋.md`: "dismissive" is the article's own word; JMdict tags only the yokel/bumpkin sense as derogatory.

**Limits**
- Dictionary evidence is the supplied frozen extracts, not live retrieval.
- The 旧 component identification is unsourced, as noted above.
- Quiz keys are mechanical projections. I did not verify in the app how keys from different kanji interact, for example 干 ほ.す and 穂 ほ.
- This is a textual review only: no native-speaker, physical-phone, font or measured-learning certification.
