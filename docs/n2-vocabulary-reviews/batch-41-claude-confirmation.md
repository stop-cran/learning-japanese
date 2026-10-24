## Snapshot
- **Corrected commit:** `d10d502fffb32af3a9a74c7ea30404f9bc68b4a4`. Its parent is the originally reviewed commit `f36e1e751aee9d9853bf113bc8d7f11f4734bf8f`.
- **Model:** claude-opus-5.5 (Claude family).
- **Basis:** committed content as described by the author's correction receipt. I used file tools only, so I did not confirm the commit, tree state or hashes myself.

## Scope
**Read in this pass**
- batch-41-correction-snapshot.json and batch-41-correction.patch, both complete.
- The five changed articles, complete: 芯, 申請, 人造, 人文科学, 神話.
- Existing comparison articles, complete: 天然, 応用, 芸術, 嘘, 適用.
- batch-41-corrections-comparison-reading.txt, complete (families 1180060 senses 1–2 and 1439580 senses 1–2).
- content-format.md lines 36–100, which hold the quiz rules.
- confirmation-evidence.json, in part:
  - quizDeclarations, the start of additionalComparisonEntryFamilies, and all of correctionEvidence (lines 21446–21560 and 21692–21980).
  - Complete family records 1253060 (芸術), 1437500 (適用) and the start of 1172400 (嘘).
- principal-reading.txt lines 5–11 (芯, JMdict 1595120 senses 1–4).
- public-bodies.txt lines 150–158 (the 人文科学 Daijisen capture).

**Carried over from the initial review, not re-read**
- The other fifteen articles, the five kanji edits and the twenty TSV selections. The patch changes only the N2:802 note.

**Accepted from the author's receipts only**
- A clean tree, manifest `67cdc8372132f347`, the regenerated coverage index, and the totals of 197 families, 473 senses, 150 labels and 94 bodies.
- I counted the declarations myself from currentQuizDeclarations: 17 articles and 59 directional exclusions (56 before + 3 added).

**Not read**
- corrections-comparisons.json and corrections-existing-bodies.txt (I read the repository files and the reading rendering instead).
- The rest of the confirmation evidence and any selected-families file.

**Correction to my initial disclosure**
- The author's record says my out-of-scope grep returned lines from five physical files (selected-existing-08, 13 and 14, among others), not "three files". I did not rely on them.

No reuses, no delegation, no forbidden files.

## Verdicts
Rows marked **R** were re-read in this pass; rows marked **I** carry over the initial review.

| Article | Basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| 芯 | R | CLEAN | CLEAN | CLEAN |
| 新幹線 | I | CLEAN | CLEAN | CLEAN |
| 真空 | I | CLEAN | CLEAN | CLEAN |
| 信ずる | I | CLEAN | CLEAN | CLEAN |
| 心身 | I | CLEAN | CLEAN | CLEAN |
| 申請 | R | CLEAN (was NEEDS FIX) | CLEAN | CLEAN |
| 人造 | R | CLEAN | CLEAN | CLEAN |
| 寝台 | I | CLEAN | CLEAN | CLEAN |
| 診断 | I | CLEAN | CLEAN | CLEAN |
| 侵入 | I | CLEAN | CLEAN | CLEAN |
| 人文科学 | R | CLEAN (was NEEDS FIX) | CLEAN | CLEAN |
| 人命 | I | CLEAN | CLEAN | CLEAN |
| 深夜 | I | CLEAN | CLEAN | CLEAN |
| 森林 | I | CLEAN | CLEAN | CLEAN |
| 親類 | I | CLEAN | CLEAN | CLEAN |
| 針路 | I | CLEAN | CLEAN | CLEAN |
| 神話 | R | CLEAN | CLEAN | CLEAN |
| 酢 | I | CLEAN | CLEAN | CLEAN |
| 水産 | I | CLEAN | CLEAN | CLEAN |
| 炊事 | I | CLEAN | CLEAN | CLEAN |

**Five kanji edits** (線/新幹線, 造/人造, 森/森林, 林/森林, 針/針路): CLEAN on all three facets, unchanged from the initial review. The correction patch does not touch kanji\; I did not re-read those files.

**Twenty mappings (N2:802–821):** CLEAN on all three facets.
- N2:802 changed in its source note only. The new text matches 芯.md: the two example sentences are pencil lead and candle wick, and plant pith appears in the Meaning text.
- All twenty identities, readings, levels and sense selections are unchanged; the TSV diff has a single note-only hunk.

## Findings
- **B41-Q-01 (申請/応用, 申請/適用): resolved.**
  - 申請.md line 9 now lists 応用 and 適用.
  - Titles: "application; formal request" vs "practical application" (JMdict 1180060 sense 1, "(practical) application") vs "application of a rule or method" (1437500 sense 1).
  - The quiz rules apply exclusions in both directions and between any two choices, so this static safeguard covers the bare-"application" overlap. It does not claim the Japanese words are interchangeable.
  - Not extending it to あてはめる ("apply a rule; fit into") or 塗る is correct: neither title is bare "application".
- **B41-Q-02 (人文科学/芸術): resolved.**
  - 人文科学.md line 9 adds [芸術], and lines 21–22 now separate academic "arts" from 芸術.
  - JMdict glosses 1369140 as "humanities; arts" and 1253060 as "art; the arts", so the exclusion is justified.
  - Daijisen describes 人文科学 as a category of study (学問の総称), which supports the clarification.
- **GPT41-01 (人造 links 天然): I agree.** 人造.md line 39 now links 天然.
  - The 天然 article (natural origin, with 人工 as its direct contrast) and JMdict 1439580 sense 1 (antonym 人工) support a materials contrast.
  - The two words are opposites with distinct titles, so no exclusion is needed.
- **GPT41-02 (神話 links 嘘): I agree.** 神話.md line 39 links 嘘 and keeps "not a neutral synonym".
  - The 嘘 title, "lie; falsehood", is distinct from "myth; mythology", so no exclusion is needed.
  - Lines 43–45 still deny that every use of 神話 implies deception.
- **芯 wording (optional suggestion, adopted):**
  - 芯.md line 46 now names pistil and stamen, matching JMdict 1595120 senses 3–4.
  - The pith gloss in sense 1, which the card selects, no longer looks contradicted.
- **Regressions:** none found. All new links point to existing files. No titles, readings, levels or earlier exclusions changed.

## Optional
- 人文科学.md lines 21–22: "not only 芸術" could read as if artistic practice is part of the humanities. "Rather than" would be crisper. This is defensible as written, so it is not a defect.
- I am not reopening the earlier optional points. They stay optional:
  - 芯's 命/身 exclusions and the undercooked-core use
  - 信ずる and 寝台 register (unverified)
  - 親類 usage notes
  - the 針路/科目 title overlap

## Limits
- I did not run Git, hash checks, validators or real quiz draws.
- I made no fresh web retrievals this pass. The Daijisen text came from the author's captures; my earlier fetches covered only 信ずる.
- I did not re-read all 197 families, 150 labels, 94 existing bodies or 40 components. Those totals are the author's figures.
- The fifteen unchanged articles and the kanji files were not re-read; their verdicts carry over.
- This is not native-speaker certification.
