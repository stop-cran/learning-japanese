# N2 expansion notes

## Scope and evidence

The [source snapshot](n2-source-snapshot.json) fixes the kanjiapi.dev N2 community set retrieved on 2026-10-21:
367 characters, including the existing cards for 珍 and 短. The expansion therefore needs 365 additions, not an assumed
generic N2 count. Modern JLPT does not publish an exhaustive kanji syllabus.

The baseline is `7a92dde23107173af8aabef51971dbc66b754a93`. Existing cards and word identities are preserved.
Use existing word articles where useful; add supporting articles only where needed. A kanji's level does not establish
a word's vocabulary level. Dictionary readings and senses must respect spelling, reading and sense restrictions.
Per-batch records under [n2-batch-sources](n2-batch-sources) retain the inspected metadata and dictionary entries.

The canonical [format](content-format.md), [authoring checks](../.github/instructions/content-structure.instructions.md),
[review guidance](../.github/copilot-instructions.md) and [JLPT policy](jlpt-levels.md) apply; this note does not replace them.

## Observed authoring pitfalls

- Candidate dictionary examples need inspection: an existing filename can teach a different reading or lexical identity.
  For example, the companion 仲間 なかま is not the historical 仲間 ちゅうげん.
- Adding a kanji card activates link checks in existing word articles that declare that kanji. Link the existing substantive
  component explanation; a new card's forward link to the word does not satisfy that separate check.
- Dictionary inclusion is not evidence of everyday frequency. Preserve unusual source readings without manufacturing
  ordinary examples. The pilot retains the unmatched readings of 並 and 乱 as character-dictionary-only lookup information.
- Inspect non-initial positions before declaring a reading source-only. The pilot's word-initial candidate heuristic
  missed 胡乱 うろん for 乱's ロン. Candidate discovery now also considers word-final matches; a kana match is still not
  proof of character-by-character reading allocation. The proposed 乱りに example does not by itself establish `みだ.る`.
- Keep spelling, pronunciation and register qualifications separate. JMdict's rare-spelling flag on 依る does not make
  よる a rare pronunciation; missing priority flags do not prove that a word is rare. Batch records retain spelling and
  reading priorities separately, with their union used only for candidate navigation.
- Preserve evidence for additional pairs asserted in notes, not only the reading-table examples. The pilot now records
  仏語 ぶつご, 乳房 ちぶさ and 依存 いそん explicitly. For external dictionaries, inspect the exact headword and any notation
  guide needed to interpret symbols; the 乾 usage notes cite the entries and Daijisen's outside-Joyo reading marker.
- The current validator enforces explained kunyomi only for N5/N4. N2 needs an explicit metadata-to-reading-table audit,
  even after structural validation passes.
- Three curated wrong answers avoid default four-choice fallback for new cards. Review the meanings, not just title strings.
  The pilot also gives existing 下 and 長 a third wrong answer because new low/long-time answers could otherwise appear
  as defensible random fallback choices.
- Use labelled modern-shape mnemonics when historical or phonetic analysis has not been established. Keep canonical radical
  metadata and explain visible variants rather than replacing the indexing radical.
- Batch 02's 傾く かたぶく has an outdated-reading flag, not an outdated-spelling flag. Keep the two annotation
  types separate, just as for rare spelling versus rare pronunciation.
- A successful dictionary URL can resolve to the wrong headword: the 刷く page on Kotobank resolved to はだく,
  and 凍る resolved to こおる, not the outstanding こごる reading. The inspected Kanjipedia はく entry
  permits 刷く only for light brush application, not its separate sweeping sense.
- New supporting vocabulary also needs quiz review. Batch 02 adds direct exclusions for the overlapping labels of
  兆候/印/現れ, 児童/子/子供, 兵士/武士, 冊子/本/書物 and 刊行/出版/発行.
  These are declared pairs on the new cards, not transitive groups or unrestricted substitution rules.
- A title-only overlap search is navigation, not a semantic audit. Batch 02's initial search missed plural
  "symptoms" and サイン's secondary sign/indication sense. Inspect relevant article meanings and ordinary
  number-neutral uses, then add direct pairs: a shared exclusion through 本 does not exclude 冊子/図書.
- Distinguish a useful alternate-reading clarification from an incorrect-reading finding. Batch 02's
  兵法 ひょうほう was valid before adding へいほう; dictionary order alone does not establish relative frequency.
- Batch 03's 卒える is flagged as a search-only spelling. Such an index form is not an ordinary example merely because
  it occurs in a dictionary record. Exclude search-only forms from Common words and label any retained index evidence.
- Verify the written okurigana boundary as well as the whole-word kana. 効き目 ききめ and 勢み はずみ do not establish
  that a single 効 or 勢 ordinarily spells the entire reading. For 卒's `お.わる`, Kanjipedia explicitly lists 卒わる;
  JMdict's different rare spelling 卒る does not by itself demonstrate that boundary.
- Automatic word links must match the article's primary reading, not just its filename. Batch 03's 包む くるむ
  must not link to the existing つつむ article; 大勢 たいせい must not link as though it were おおぜい.
- The current candidate cache retains only spellings containing selected N2 characters. Its missing non-N2 aliases
  are an extraction limit, not evidence that those spellings or independent entries are absent from JMdict.
- Web-search generated prose can disagree with its own citation URLs. In batch 03, a purported 副作用 URL resolved
  to 文七元結. Inspect the fetched headword and actual definition; do not treat the generated quotation as dictionary evidence.
- A bound counter needs a usable count, not only the isolated dictionary suffix and a warning. Both batch 03 reviewers
  requested concrete 匹 forms; the correction gives 一匹, 二匹 and 三匹 with kana and separate pronunciation evidence.
- The equality family needs direct exclusions beyond 同じ. Both batch 03 reports raised 匹敵/同様 and 匹敵/同一,
  albeit with different severity. A shared exclusion through 同じ would not protect either pair.
- A part-of-speech observation should identify its sense when the word has others. 勢い is a noun in the force/momentum
  sense discussed on its card; JMdict also records an adverb sense. The clarification does not require teaching every sense.
- Compare each named neighbor on its own relevant dimension. Batch 03's first 匹敵 correction distinguished matching
  from 同一's identity but not from 同様's contextual similarity. The revised comparison contrasts reaching a level
  (`Bに匹敵する`) with kind or manner (`Bと同様`), without claiming their meanings can never overlap.
- Missing exact standalone matches are not missing bound-stem examples. Batch 04 uses 双子 ふたご for 双's ふた.
  A broader spelling search also finds rare 双ぶ ならぶ despite the source's undotted reading, while 双つ ふたつ
  is search-only and remains index evidence. Inspect the written kana instead of trusting the candidate heuristic.
- A legacy component explanation may mention only the complete word, as with 布団. Link 団 inside that existing
  spelling at its substantive introduction rather than manufacturing an isolated meaning or rewriting the article.
- Recheck two-distractor fallbacks as overlapping characters arrive. Batch 04 adds a third curated wrong answer to
  毎, because the new 各 card's each/every answer could otherwise be defensible in a fallback choice.
- A selected spelling can hide a useful alternative. Following batch 04 review, the full pinned JMdict entry for
  巧咲 was inspected and its spellings 巧笑/巧咲 retained. Explain the alternative without treating dictionary order
  as a frequency ranking, or an alternative spelling as an invalid word.
- Separate a whole-word ateji label from a claim about each character's purely phonetic role. Batch 04's 布団 note
  now states the source's whole-spelling label without inventing a component-by-component derivation.
- Narrowing an overbroad technical explanation should not remove the term's only learner-facing gloss. The first
  batch 04 団 correction did that to "ateji"; the follow-up restores a short qualified explanation while retaining
  the whole-word versus component-role distinction.
- An occurrence of a kana sequence is not a character-reading allocation. Batch 05 does not use the えん in
  圧延 あつえん as evidence for 圧's エン, or the くま within 奥まる おくまる as evidence for 奥's くま.
  Unestablished readings remain qualified lookup information rather than manufactured examples.
- Identical spelling does not imply identical primary reading or sense restrictions. Batch 05 keeps 埋める
  うめる separate from うずめる, and restricts 埋まる's vacancy/debt senses to うまる. Its 塩 link teaches しお,
  not the separately documented chemical noun えん.
- Preserve sensitive-usage labels even when the example is needed only for a character reading. The ショウ row
  of 姓 identifies 百姓's farmer sense as sensitive and its separate derogatory sense, not as neutral farm vocabulary.

## Review and checkpoint protocol

Work in the source snapshot's batches, sequentially. Checkpoint content and regenerated manifests before review, then
commit confirmed fixes and their reconciliation. Git author and committer are `stop-cran`.

Each batch receives independent GPT and Claude review of the same frozen snapshot, files, facets and evidence.
Run one short-lived reviewer process at a time and confirm exit before starting another; there is no explicit agent-unload
tool in this environment. Initial reports stay blind to one another and to the author's preferred adjudication.
Record actual models and review limits in the [review ledger](n2-review.md).

Reconcile against evidence, not votes. Retain the initial reports and mark findings resolved, partially resolved, unresolved,
withdrawn or optional. Review changed passages for regressions. Compare model contributions only after deduplicating
equivalent observations across findings, optional suggestions, limits and per-card notes.

## Current limits

Source records and structural checks are not native-speaker certification or exhaustive historical analysis.
Dual-model usefulness is an observation about the reviewed sample, not proof that model bias has been eliminated.
The first four batches' initial and changed-passage GPT/Claude reports are preserved in the review ledger. They found
complementary issues, but also supplied unsupported frequency inferences and optional expansions. Neither family caught
every issue established across the reviewed sample. Both confirmed the final corrected passages without an actionable
remaining defect in that scope; this coverage does not yet extend to the remaining 305 additions.
Those pending additions include the 15 drafted batch 05 cards and 290 not yet authored.

Reviewer file permissions are separate from tool permissions: `--allow-all-tools` alone did not authorize a diff in the
parent session's artifact directory. The event record showed a noninteractive path-approval failure, not content exclusion.
Grant only that artifact directory with `--add-dir`. Reviewer session IDs can be recovered from the local session store
for same-task follow-up; `--resume` and `--trust-folder` cannot be combined. Exit each resumed process before the next.
