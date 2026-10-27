## Snapshot
Commit **88560e5b110c4e8b78922c8e3efedecbd1c99559**, from `batch-49-frozen-snapshot.json`. Its parent is 43e848bc…, as stated, and the receipt records committed content only. My file tools cannot run Git, so the commit, the clean state and all hash/equivalence checks are as the author executed them. I did not verify them myself.

## Scope
- **Model:** claude-opus-5.5, Claude family.
- **Read in full:**
  - The three governing documents, with `docs\content-format.md` limited to lines 18–126 plus 80–100.
  - The receipt, `related.patch`, `review-mappings.jsonl`, `principal-reading.txt`, `review-components.jsonl`, `kanjipedia.txt`, `selected-families-01.txt` and `additional-comparison-reading.txt`.
  - All 19 new articles, `大小.md`, and the four kanji cards.
  - TSV lines 962–981 and both snapshot JSON files.
- **Read in part:**
  - `review-evidence.json`, lines 1–60.
  - `public-bodies.txt`: Daijisen sections for 逸れる, 揃う, 揃える, 存じる, 存ずる, 体系, 太鼓, 対策, 大して, 大小 and 大層, found by grep on that exact file.
  - Front matter (title, exclusions and tags) of about 130 existing comparison or exclusion-target words in `words\`.
  - A grep of `docs\confusable-words.md`.
- **Fetched:** kotobank 対策 and 対照, and weblio 対策 and 対照.
- **Not read:** `review-labels.jsonl`, `review-principals.jsonl`, `selected-families-02` to `-10`, `public-bodies.json` and `kanjipedia.json`. I did not read any prohibited ledger or `batch-49.json`, and I did not glob or search the private directory.

## Verdicts
| Row | Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| 962 | 逸れる (new) | CLEAN | CLEAN | NEEDS FIX (B49-04) |
| 963 | 揃う (new) | NEEDS FIX (B49-01) | CLEAN | CLEAN |
| 964 | 揃える (new) | NEEDS FIX (B49-01) | CLEAN | CLEAN |
| 965 | 算盤 (new) | CLEAN | CLEAN | CLEAN |
| 966 | 存じる (new) | CLEAN | CLEAN | CLEAN |
| 967 | 存ずる (new, blank raw gloss) | CLEAN | CLEAN | CLEAN |
| 968 | 損得 (new) | CLEAN | CLEAN | CLEAN |
| 969 | 田んぼ (new, source 田ぼ) | CLEAN | CLEAN | CLEAN |
| 970 | 第一 (new) | CLEAN | CLEAN | CLEAN |
| 971 | 大学院 (new) | CLEAN | CLEAN | CLEAN |
| 972 | 大工 (new) | CLEAN | CLEAN | CLEAN |
| 973 | 体系 (new) | CLEAN | CLEAN | CLEAN |
| 974 | 太鼓 (new) | NEEDS FIX (B49-02) | CLEAN | NEEDS FIX (B49-05) |
| 975 | 対策 (new) | CLEAN (one claim UNVERIFIED, see Limits) | CLEAN | CLEAN |
| 976 | 大して (new) | CLEAN | CLEAN | CLEAN |
| 977 | 対照 (new) | CLEAN | CLEAN | CLEAN |
| 978 | 大小 (reused) | CLEAN | CLEAN | CLEAN |
| 979 | 体制 (new) | CLEAN | CLEAN | CLEAN |
| 980 | 体積 (new) | CLEAN | CLEAN | CLEAN |
| 981 | 大層 (new) | NEEDS FIX (B49-03) | CLEAN | CLEAN |

**Kanji edits: all four CLEAN.**
- **算:** the separately qualified そろばん whole-word row is at line 32 and the common-word entry at line 42. The source-only そろ row and its caveat (lines 31 and 34) are preserved.
- **損:** 損得 is added to the ソン row (line 30) and to Common words (line 40).
- **照:** 対照 is added to the ショウ row (line 30) and to Common words (line 39).
- **層:** 大層 is added to the ソウ row (line 28), to Common words (line 35) and to Notes (line 41).

**大小 preservation: CLEAN.** The patch adds only `jlpt: 2` and the citation at line 47 ("senses 1-2"). Identity, title, reading, kanji, the original body and the absent exclusions are all unchanged, and the article is not labelled as new.

**Mappings: CLEAN.** All twenty rows match. Raw fields are preserved, including the TSV spelling 田ぼ and 存ずる's blank gloss. The selections total 36 of the 41 family senses; the five unselected senses are 大小 senses 3–6 and 体制 sense 3.

## Findings
- **B49-01 · Low · quiz guard · `揃う.md:9`, `揃える.md:9`**
  - **Issue:** this transitivity pair shares a kanji and the same type, but neither card excludes the other.
  - **Impact:** in a quiz on 揃える, the option "be complete; be all present; match" overlaps with its matching sense, and "assemble a full set" overlaps with 揃う's "be complete". Shared kanji raises how often the two appear as choices together (`content-format.md:81-82`).
  - **Evidence:** the guidance names 開く/開ける as a pair that needs an exclusion (`content-format.md:95-96`), and those two cards exclude each other.
  - **Fix:** add 揃える to 揃う's exclusions.
  - **Confidence:** medium.
- **B49-02 · Low · quiz guard · `太鼓.md:1-9`**
  - **Issue:** the card has no exclusions, but 楽器 ("musical instrument") excludes 笛, ピアノ, ギター and other instruments (`楽器.md:9`) and shares the music/noun tags.
  - **Impact:** "musical instrument" is a reasonably acceptable answer for 太鼓. The Daijisen text defines it as 打楽器の一.
  - **Fix:** `quiz_exclusions: [楽器]`.
  - **Confidence:** medium-high.
- **B49-03 · Low · excessive guard · `大層.md:9`**
  - **Issue:** ずっと's title, "the whole time; much more", shares no sense with 大層; none of 大層's senses 1–4 is temporal or comparative (`principal-reading.txt:178-181`). The list appears to be copied from うんと's list, which is transitive reasoning.
  - **Fix:** remove ずっと.
  - **Confidence:** medium.
- **B49-04 · Low · comprehensibility · `逸れる.md:24-25`**
  - **Issue:** the sentence "それた道 … not a command to change someone else's direction" uses an unattested collocation and contrasts it with an imperative nobody suggested. Daijisen's examples are 弾がそれる and 話が脇道へそれる (`public-bodies.txt:9-11`).
  - **Fix:** use 道をそれる or 脇道にそれる instead.
  - **Confidence:** medium.
- **B49-05 · Low · comprehensibility · `太鼓.md:35-37`**
  - **Issue:** "the source list's loose English gloss" refers to a list the learner cannot see.
  - **Fix:** rephrase as "some word lists gloss 太鼓 as 'tambourine'; the word for a tambourine is タンバリン."
  - **Confidence:** medium.

## Optional
- 体制 and 政府 could exclude each other, since "regime" and "government" overlap. 対策 and 予防 ("precaution") are a weaker candidate pair.
- `大して.md:45-46` calls 大層 "ordinary", while 大層 itself says it can sound formal or old-fashioned. Aligning the wording would help.
- 逸れる could add the を pattern, as in 的をそれる.
- The 大小 body's "not 'big and small' as two things" could be softened to fit sense 2.

## Limits
- I did not verify anything with Git.
- **対策 「(スル)」:** my weblio fetch returned only Wikipedia, and kotobank's Daijisen section was empty. Nikkoku seisen gives 〘名詞〙 only. The claim matches only the author's capture.
- **対照:** my kotobank fetch confirmed the (スル) label and the example 訳文を原文と対照する.
- I read the bodies of existing words only for a few cards. For the rest I checked front matter, so a guard someone else considers missing may remain.
- I did not read the labels, the principals JSONL, or selected families 02–10.
- None of this certifies naturalness as a native speaker would judge it.
