All four articles came out CLEAN on all three facets, with no findings. Both snapshot reads succeeded and I read all 19 packet parts in full.

**Snapshot**
- Model: Claude Opus 5.5 (`claude-opus-5.5`).
- `C:\Users\stop-\n1-kanji-workspace\rollout-recovered\batch-108-review-9955ac\.git` returned `gitdir: C:/Users/stop-/n1-kanji-workspace/auditor-compatibility-isolated/.git/worktrees/batch-108-review-9955ac`.
- `C:\Users\stop-\n1-kanji-workspace\auditor-compatibility-isolated\.git\worktrees\batch-108-review-9955ac\HEAD` returned exactly `9955ac122d1b4f1084f702d3d6d5afeb82d35e3a`, a detached HEAD.
- Neither read was denied. I can't see whether an approval prompt was shown.
- The original denial and the UNACCEPTED initial report still stand as they were.

**Scope**
- Packet parts 01–19 were read with one `view` per response, in order, with `forceReadLargeFiles=true`. None was reread and I saw no truncation; each part continued exactly where the previous one ended.
- Reviewed: the four affected articles, the exact teaching diff, the comparison and legacy-context articles, and the batch JMdict and comparison families with their restrictions. I also checked the KANJIDIC2 records for 勧, the comparison kanji and the overlap set, the Daijisen extracts and receipts, the input metadata, the KanjiVG SVG and stroke JSON, and the public rules.
- No other report, adjudication, shell, edit or delegation was used.

**Verdicts**
| Article | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji/勧.md` (new) | CLEAN | CLEAN | CLEAN |
| `words/勧告.md` (new) | CLEAN | CLEAN | CLEAN |
| `words/勧める.md` (reused N3) | CLEAN | CLEAN | CLEAN |
| `kanji/告.md` (reused N3) | CLEAN | CLEAN | CLEAN |

**What was checked**
- **勧 metadata:** 13 strokes, radical 力 (no. 19) on the right, grade 8 and JLPT 1 all match KANJIDIC2 and the SVG.
- **勧 readings:** カン/ケン and すす.める match the source. The two selected readings each have their own row and a linked word. ケン is clearly marked as kept from the source but not practised, without calling it invalid.
- **勧 shape notes:** The 隹-like lower left matches the SVG's 隹 group. The mnemonic is labelled as a mnemonic, and the article avoids any origin claim even though KanjiVG tags the left side as phonetic 雚.
- **勧告 sources:** かんこく, noun and transitive する-verb, matches JMdict 1210970. 辞職を勧告する is quoted from Daijisen. Both examples are natural and correctly translated, and the カン + コク split is right.
- **勧める spellings:** The diff only adds a quiz-exclusion line and a link. Sense 2 has no spelling restriction (it is "esp. 薦める"), so 本を勧める is valid with 勧. The article's claim that 薦める doesn't cover the encourage and offer senses (1 and 3) is correct.
- **告:** The new 勧告 bullet is accurate, and the unchanged content is consistent.
- **Kanji distractors:** 観 (view; observe), 確 (certain) and 権 (authority; rights) are clearly different in meaning, including their secondary KANJIDIC senses. The shape comparisons are accurate.
- **Kanji exclusions:** 励, 供 (offer), 勉 (encourage in KANJIDIC2) and 支 (support) are reasonable direct guards for "recommend; encourage".
- **Word exclusions:** Every exclusion on the new 勧告 and on 勧める is supported by an overlapping English label or sense. Exclusions declared on other cards against 勧める already cover those pairs in both directions.
- **Reciprocal links:** All six directions are present with correct readings: 勧/勧める, 勧/勧告 and 告/勧告.

**Findings:** none.

**Optional**
- `kanji/告.md:37`: putting "告 has the on reading コク here" after the gloss's semicolons could read as part of the meaning. A dash or parentheses would separate it.
- These are tentative, not established defects:
  - 相談's title ("consultation; asking for advice") next to 勧告 in English→Japanese quizzes. The asking-versus-giving roles differ, so I don't treat it as a needed exclusion.
  - 募 ("recruit; solicit") as a tag fallback for 勧. Daijisen and KANJIDIC2 give 勧 no "solicit" meaning.

**Limits**
- I didn't recompute the SHA-256 hashes; the packet bytes were taken as qualified.
- The packet labels name the original authoring paths. I didn't compare them against the current branch, as instructed.
- These are text judgments from the supplied sources only, with no fresh dictionary lookups. Native font and UI, actual quiz pools and fallback runs, both word directions, drawing, Back and offline behaviour, and phone acceptance are later gates.
