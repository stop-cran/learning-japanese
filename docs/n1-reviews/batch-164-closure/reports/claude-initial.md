**Snapshot:** 027e5581f5b99523ae5f819d830673c8958560f6, based on 6121ea9e. I reviewed the packet files only. They carry no line numbers, so I cite sections instead of lines.

**Scope:** One blind, read-only reviewer: Claude Sonnet 5.5 (`claude-sonnet-5.5`). No other reviewers were used, so this is not a multi-family review. I read each of these in full, one view at a time:
- rubric.txt and snapshot.txt
- kanji-1 to kanji-4 and words-1 to words-3
- reused-word.txt and changed.txt
- primary.xml (10 entries)
- sources.json
- quiz.txt and labels.txt
- families-1 to families-6 (81 entries)

My facets are correctness (readings, senses, grammar) and scoped coverage. Comprehensibility was not assigned, so I label it UNVERIFIED.

**Verdicts** (comprehensibility is UNVERIFIED for every card)

| Card | Correctness | Coverage |
|---|---|---|
| kanji 姫, 姻, 娠, 媒, 媛, 孤, 嫡 | CLEAN | CLEAN |
| kanji 婆 | NEEDS FIX (F2) | CLEAN |
| kanji 孔 | NEEDS FIX (F2, F4) | CLEAN |
| kanji 婿 | CLEAN | CLEAN |
| word 姫, 婚姻, 媒体, 才媛, 孤独, 嫡子 | CLEAN | CLEAN |
| word 婿 | NEEDS FIX (F1) | CLEAN |
| word 妊娠 | NEEDS FIX (F3) | NEEDS FIX (F3) |
| おばあさん (changed sentence) | CLEAN | CLEAN |
| 穴 (changed sentence) | NEEDS FIX (F4) | CLEAN |
| changed kanji 体, 妊, 婚, 才, 独, 瞳 | CLEAN (additions only) | CLEAN |
| changed kanji 子 | UNVERIFIED (F6) | CLEAN |

**Findings**

- **F1 – Moderate – correctness – words/婿.md** (Meaning, example 2, Dictionary line). Confidence: medium.
  - The card says 婿 "can also mean the groom". Its only groom example is 花婿, which is a separate JMdict entry (1194980) that the card does not cite.
  - JMdict 1531160 sense 1 is "husband; groom". The card silently drops "husband" while citing "senses 1–2".
  - Impact: learners may read the example as standalone 婿 = groom.
  - Remedy: say the example shows the compound 花婿 (はなむこ, 1194980), or supply an attested standalone example. Add that JMdict's "husband" gloss is not taught and that 夫 is the ordinary word for husband.
  - Evidence: primary.xml 1531160, families-1 1194980.

- **F2 – Minor – correctness – kanji/孔.md, kanji/婆.md** (reading tables). Confidence: high on the inconsistency, medium on its impact.
  - Sibling cards flag キ, ク, テキ and ひめ as outside the standard-use table. The Kanjipedia "outside" lists in sources.json also cover 孔 あな and 婆 ばば. These two are not flagged. ばあ is in KANJIDIC2 only.
  - The only quizzed readings (孔 あな, 婆 ばあ) are non-table readings. The standard readings コウ and バ are not quizzed, and the cards do not say so.
  - Remedy: add "outside the standard-use table" to 孔 あな and 婆 ばば. For ばあ, state that it comes from KANJIDIC2 and お婆さん only. Optionally do the same for 媒 なこうど, where Kanjipedia lists なかだち instead.

- **F3 – Minor – correctness and coverage – words/妊娠.md**
  - Correctness (Distinctive meaning): 姉は妊婦だ is a constructed contrast and is not shown to be natural. Remedy: replace it with an attested pattern, or flag it as constructed and say 妊婦 usually labels a category.
  - Coverage: JMdict 1467350 is vs/vi and glosses "conception". The card shows only 妊娠している, and its claim "not … a stage" sits uneasily with that gloss. Remedy: add 妊娠する/妊娠した ("become pregnant") against している ("be pregnant").
  - Native naturalness is unverified. Confidence: medium-low.

- **F4 – Minor – correctness – kanji/孔.md, words/穴.md** (the 孔 spelling statements). Confidence: medium.
  - JMdict 1254480 lists 孔 with no priority tag and no sense restriction. "For a physical opening" is a teaching choice, not a dictionary restriction. A spelling list supports recognition only.
  - Remedy: say 孔 is an uncommon, unprioritized spelling to recognize while writing 穴, and label the physical-opening limit as advice.

- **F6 – Minor – process – changed.txt, kanji/子.md.** The diff replaces the whole file. By eye I found no text change beyond the 嫡子 bullet and the Metadata line, so this looks like line-ending churn. Remedy: confirm with a whitespace-insensitive diff and restore the original line endings.

**Optional**
- 嫡 title: "heir" is absent from the KANJIDIC meanings in sources.json ("legitimate wife; direct descent"). It comes from the 嫡子 word sense.
- 正嫡: JMdict lists せいちゃく first; the card leads with せいてき.
- 嫡子 example 1 (次男 as 嫡子) can also be read as the "legitimate child" sense.
- 孤独 vs 寂しい is contrasted only by part of speech. A nuance contrast would teach more, but the packet has no source for one.
- 婿: add 婿養子/入り婿. Also, 嫁 "from the other side" is vague; say "a son's wife".
- 孔: 孔雀 (くじゃく) is a more familiar ク example. This is from general knowledge, not packet-verified.
- 才媛 and bare 婆 may carry register or gender connotations. The packet has no source for this.
- Cross-facet quiz-safety: exclusions are declared one way only, for example 孤→独, 孔→穴, 姻→婚 and 姫→媛, and older cards are unchanged. Overlapping labels (孔 and 穴; 孤 and 独 "alone") would be ambiguous if the generator is not symmetric. Another reviewer should confirm.

**Limits**
- I saw only the diffs for the older changed cards, not the full text.
- I opened no external pages (Kanjipedia, Daijisen), only the extracts in sources.json.
- I did not verify that relative link targets exist (婚約, 新聞, distractor kanji), or how the quiz generator treats exclusions.
- No native, device or whole-deck verification was done.
- Naturalness judgments are my own and unverified.
