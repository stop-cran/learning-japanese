# Batch 48 N2 vocabulary review: N2:942–N2:961

Most of the batch is sound. I found six low-to-minor defects across six rows. None of them is blocking, and the mappings, the six kanji-card edits, the six link-only edits and the 備える reuse are all clean.

## Snapshot
- **Commit:** `614bbb8394118e9e38ebb7b8c6ca2011a62be4bb` (parent `2cd95674fa935003357fbd11e0f2ddf2121d9a11`), as given in the frozen receipt; committed content only.
- **Git and hash checks:** these are the author's. My file tools can't run Git, so I couldn't confirm them.

## Scope
**Model:** claude-opus-5.5 (family claude). Read-only: no edits, agents or delegation.

**Read in full:**
- The three guidance files: `.github\copilot-instructions.md`, `content-structure.instructions.md` and `content-format.md:18-126` (plus a grep of it for the quiz-exclusion rules).
- All 19 new articles, the reused `備える.md`, the six kanji cards and the six link-only articles.
- Rows N2:942–961 of `docs\n2-vocabulary-sources.tsv`.

**Private files read:** frozen-snapshot, review-mappings, review-principals, principal-reading, review-components, review-labels (207), related.patch, public-bodies.txt and character-public-bodies.txt. I also ran grep on exact private file paths, never on the directory.

**Comparison titles and guards:** checked with grep and glob in `words\` and `kanji\` only. I didn't read old comparison articles like 調査, 昔 or 急行 in full.

**Not read:** review-evidence.json, the public-bodies/alias/character JSON files, the alias txt, additional-comparison-reading, selected-families-01..08, both snapshot JSONs, `confusable-words.md`, `jlpt-levels.md`. I read none of the forbidden files.

**Web:** I made no fresh dictionary fetches.

## Verdicts
Cells are correctness / scoped coverage / comprehensibility.

| Row | Article | Verdicts |
|---|---|---|
| 942 | 総理大臣 (new) | CLEAN / CLEAN / CLEAN |
| 943 | 送料 (new) | CLEAN / CLEAN / CLEAN |
| 944 | 属する (new) | CLEAN / CLEAN / NEEDS FIX (B48-04) |
| 945 | 続々 (new) | NEEDS FIX (B48-01) / CLEAN / NEEDS FIX (B48-01) |
| 946 | 速達 (new) | CLEAN / CLEAN / CLEAN |
| 947 | 測定 (new) | CLEAN / CLEAN / CLEAN |
| 948 | 測量 (new) | NEEDS FIX (quiz guard, B48-06) / CLEAN / CLEAN |
| 949 | 速力 (new) | CLEAN / CLEAN / CLEAN |
| 950 | 素質 (new) | CLEAN / CLEAN / CLEAN |
| 951 | 祖先 (new) | CLEAN / NEEDS FIX (B48-02) / CLEAN |
| 952 | そそっかしい (new) | CLEAN / CLEAN / CLEAN |
| 953 | 率直 (new; normalized from source 卒直) | CLEAN / CLEAN / CLEAN |
| 954 | 備える (reused, N3) | CLEAN / CLEAN / CLEAN |
| 955 | そのうえ (new) | CLEAN / CLEAN / CLEAN |
| 956 | そのころ (new) | NEEDS FIX (B48-03) / CLEAN / CLEAN |
| 957 | そのため (new) | CLEAN / CLEAN / CLEAN |
| 958 | そのほか (new) | CLEAN / CLEAN / CLEAN |
| 959 | 蕎麦 (new) | CLEAN / CLEAN / CLEAN |
| 960 | 剃る (new) | CLEAN / CLEAN / NEEDS FIX (B48-05) |
| 961 | それなのに (new) | CLEAN / CLEAN / CLEAN |

- **Kanji edits (総, 臣, 測, 量, 麦, 卒): CLEAN.**
  - The reciprocal pairs are present at the real readings: 総 ソウ, 臣 ジン, 測 ソク (測定 and 測量), 量 リョウ, each with a Common-words entry.
  - 麦 uses a qualified whole-word そば row and says it is not 麦=ば.
  - 卒 has the 卒直 alias note only (line 52), not a primary pair.
- **Old link-only edits (首相, ぞくぞく, 側, 先祖, 子孫, うどん): CLEAN.**
- **備える reuse: CLEAN.**
  - Word, reading, title, N3 level, wago type and `[備]` metadata are unchanged, and the original teaching is kept.
  - Possession sense 3 is added at lines 25–32, rare 具える is recognized at 39–42, and sense 4 is not taught.
  - Only the citation changed (line 56).
- **Mappings: CLEAN.**
  - Raw fields are kept, including blank glosses on 956 and 961 and the raw 卒直 spelling.
  - Sense choices match the dictionary data: 954 uses senses 1–3 at article level 3; 959 uses sense 2 with 1 and 3 as additions; 950 uses senses 1 and 2; 955 and 958 use their full sense ranges.
  - 素, 属, 蕎, 剃 and 率 have no kanji cards and correctly stay as metadata only.

## Findings
- **B48-01 — Minor; correctness and clarity — `words\続々.md:29-31`.**
  - **Problem:** "Learn that established whole reading rather than automatically voicing every compound containing 続" implies that 続 is normally unvoiced and gets voiced here.
  - **Evidence:** 続's on-reading is already ゾク (the KANJIDIC data in principal-reading line 34 lists ゾク first; compare 連続, 相続). ぞくぞく is just ゾク+ゾク, so nothing is voiced.
  - **Fix:** say it is ゾク repeated, and delete the voicing sentence.
  - **Confidence:** high.
- **B48-02 — Minor; scoped coverage — `words\祖先.md:16-17, 34-35, 42-43`.**
  - **Problem:** the article limits 祖先 to "a family line" and presents 先祖 only as a reversed-order synonym. Learners get no usage difference between the two.
  - **Evidence:** the captured Daijisen 祖先 entry has sense 3, 一族のもと, with the example 「人類の祖先」 ("ancestors of humankind"). JMdict 1396820's single sense is just "ancestor".
  - **Fix:** add the species or group-origin use (e.g., 人類の祖先). Optionally add the tendency that 先祖 is the everyday household word (ご先祖様, 先祖代々); that part is my own usage knowledge, not in the captured evidence.
  - **Confidence:** moderate.
- **B48-03 — Minor; example naturalness — `words\そのころ.md:20`.**
  - **Problem:** 「十年前、そのころ私は大阪に住んでいました。」 stacks two references to the same time in one clause, which is awkward. It also doesn't show その pointing back to an earlier sentence.
  - **Fix:** use something like 「十年前のことです。そのころ、私は大阪に住んでいました。」
  - **Confidence:** moderate; not native-certified.
- **B48-04 — Low; clarity — `words\属する.md:43-44`.**
  - **Problem:** "The dictionary also records a separate reading しょくする with different uses" has no clear source, since the JMdict entry the article cites lists only ぞくする. It also doesn't say しょくする is rare or literary, and "different uses" is partly wrong.
  - **Evidence:** in Daijisen, the しょくする headword is marked ▽ (a non-standard reading for the kanji), and its sense 1 is glossed as 「所属する。ぞくする。」
  - **Fix:** attribute it to Daijisen, describe it as a rare literary reading mostly used like 嘱する ("to entrust"), and say ぞくする is the modern reading.
  - **Confidence:** moderate.
- **B48-05 — Low; pronunciation register — `words\剃る.md:30-33`.**
  - **Problem:** する is presented neutrally as "an alternative dictionary reading".
  - **Evidence:** the Daijisen そる entry, which the article itself cites, says 「なまって『する』ともいう」: する is a corrupted, colloquial pronunciation of そる.
  - **Fix:** describe する as a colloquial or regional variant pronunciation.
  - **Confidence:** moderate.
- **B48-06 — Low; quiz guard — `words\測量.md:9`.**
  - **Problem:** 測量 ("surveying; measurement") and 調査 ("investigation; survey") have no exclusion in either direction. A learner going from English "survey" to Japanese could reasonably pick either.
  - **Evidence:** the article's own lines 32–33 acknowledge the English "survey" overlap.
  - **Fix:** add 調査 to 測量's `quiz_exclusions`; one side is enough, because exclusions apply in both directions.
  - **Confidence:** low to moderate; this is a borderline case.

## Optional
- The kanji-card footer lines ("Word pairs: JMdict entries …") don't list the new entries 1401820, 1404570, 1404590 and 1238460. I found no rule requiring them, so this is not a defect.
- そのため says その為 is "the" kanji spelling, but JMdict also lists 其の為 and 其のため.
- 素質's exclusions of 人物 and カラー are arguably more than needed, but harmless.
- そのころ vs 昔 ("the old days") is a possible but weak quiz-guard candidate.
- 蕎麦 could mention that KANJIDIC lists そば as a kun reading of 蕎.

## Limits
- I made no fresh dictionary retrievals. Dictionary claims rest on the author's public captures and the JMdict data in the private files.
- The public extractions failed for そのころ, そのため and そのほか, so for those rows only JMdict backs the claims.
- I didn't read the selected-families, review-evidence, alias or additional-comparison files, either snapshot JSON, `confusable-words.md` or `jlpt-levels.md`. Absence claims are limited to what grep and glob showed in `words\` and `kanji\`.
- No native-speaker certification: the naturalness judgments (B48-03 and the CLEAN example cells) are my own reading.
- I haven't checked the author's hash and equivalence results or the read counts they report.
