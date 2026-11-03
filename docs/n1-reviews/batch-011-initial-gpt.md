**Snapshot:** `69f0b3bd995c6071c1845a4e550c117d4233ae7d`; committed teaching only, with no uncommitted teaching included, as identified by the assigned task. Git identity and worktree cleanliness were not independently verified.

**Scope:** Independent initial, read-only review by GPT-6.1 Sol (`gpt-6.1-sol`). Reviewed correctness, scoped coverage and textual phone comprehensibility of all four complete teaching files: `kanji\梓.md`, `kanji\橘.md`, `words\梓.md`, `words\橘.md`. Checked every example and translation, metadata, reading tables and quiz subsets, labels, exclusions, substantive links, lexical/register qualifications and modern-shape mnemonics. No changed reused passages were assigned.

Read completely:
- `.github\copilot-instructions.md` and `.github\instructions\content-structure.instructions.md`; prescribed ranges of `docs\content-format.md` (42–148) and `docs\jlpt-levels.md` (1–105).
- `docs\n1-sources\batch-011-input-metadata.json`, including both complete raw KANJIDIC2 character elements.
- All four JMdict packets: primary, comparisons, supplement and notes—**71 complete families** across 30/26/12/3 entries, including every spelling, reading, restriction, sense and flag.
- Comparison kanji: 木・辛・新・村・橋・商・相・矛.
- Comparison words: 木・植物・植える・植木・果物・果実・実・柚・花・香り・印刷・出版.
- The complete `docs\confusable-words.md` inventory, including recovery of the initially truncated passage, and complete `docs\n1-source-snapshot.json`.

Independently fetched the four specified Kotobank URLs. Inspected actual dictionary headings and relevant bodies for 梓, 橘 and 上梓; recovered the 柑橘類 Daijisen and Seisenban headings and bodies through raw HTML after the simplified extraction omitted them. No other reviews or author-rationale records were read.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\梓.md` | CLEAN | CLEAN | CLEAN |
| `kanji\橘.md` | CLEAN | CLEAN | CLEAN |
| `words\梓.md` | CLEAN | CLEAN | CLEAN |
| `words\橘.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no actionable defect established within this bounded review, not exhaustive certification.

**Findings:** None.

The four sourced on/kun entries are preserved exactly and in order: 梓 **シ / あずさ**, 橘 **キツ / たちばな**. Each has an explanatory table row. Both empty `quizOnyomi` lists suppress questions without deleting readings; each selected kun reading has a directly supported, useful, reciprocally linked single-character word article.

The consequential lexical distinctions withstand inspection:
- JMdict 1152850 restricts its three plant senses to あずさ/アズサ, but leaves “printing block” unrestricted. Kotobank’s Daijisen **し** entry establishes the printing-block use; Seisenban **あずさ**, sense ⑥, independently establishes it under あずさ. Seisenban’s separate **し** botanical entry does not invalidate either documented use. The cards appropriately distinguish Japanese plant naming, Chinese reference and printing terminology.
- JMdict 1152860 supports the spirit bow and its possible woods; 2577100 supports the female-medium use. Seisenban confirms historical abbreviated bow/medium uses and the wood-for-bows connection. The learner-created bow sentence is natural and does not purport to document a particular historical event.
- JMdict 1226460 supports たちばな and *Citrus tachibana*. Seisenban distinguishes older edible mandarins from the wild evergreen plant with white flowers and bitter, strongly sour fruit. Its blossom, crest, aromatic-wood/incense and surname entries support the qualified recognition notes rather than unrestricted substitutions.
- JMdict 1212910/2831569 and the actual 柑橘類 dictionary bodies support the broader citrus category. The treatment of 枸橘 and 酢橘 correctly avoids extracting constituent readings from whole-word kana.

Both new kanji supply three distinct curated wrong answers, so the documented default four-choice quiz needs no fallback. Their actual displayed comparison labels and ordinary senses do not establish a competing correct answer.

Word exclusions directly protect the reviewed broad tree/plant, garden-tree and fruit/blossom overlaps. They do not rely on transitivity. No additional 梓/printing-activity, 橘/香り or 梓/橘/柚 exclusion was established: the actual labels and senses distinguish the printing tool from activities, a named aromatic material from fragrance generally, and different named plants from one another.

The examples, translations and kana support are clear. Botanical qualifications do not overwhelm the selected nouns, and the shape associations are explicitly mnemonics rather than unsupported etymology.

**Optional:** None.

**Limits:** Frozen JMdict/KANJIDIC2 packets were inspected, not freshly retrieved upstream or independently hash-verified. Kotobank’s simplified 上梓 extraction lacked the Daijisen body; its substantive Seisenban body supplied the relevant evidence. Initial oversized 柑橘類 responses were not fully visible; subsequent bounded extraction and raw-HTML reads recovered the relevant dictionary evidence. Other incidental page sections and raw HTML were not exhaustively inspected.

An inventory `rg` search and supplemental existence globs returned no matches; those results were not treated as proof of absence. Inventory coverage instead rests on complete file reads, and linked comparison targets were read directly. Broader automated link/import/stroke integrity was not tested.

This was textual review, not native-speaker certification, physical-phone execution or measured frequency/readability/effectiveness testing. No consequential linguistic claim remains unresolved in scope. Visible tool calls were serial, with no observed internal overlap; no broader process evidence was available. No files were edited, and no shell, delegation, commits or issues were used.
