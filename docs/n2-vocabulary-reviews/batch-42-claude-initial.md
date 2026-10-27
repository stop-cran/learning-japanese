# Batch-42 N2 vocabulary review (N2:822–N2:841)

## Snapshot
I reviewed frozen commit `1c55dc75c503046de66d6cf41e73bbe25c96fc62` (parent `42283503b9da8e70ae1f17628d1da121c3b93240`), committed content only. I had file tools but could not run Git, so I could not check the commit or the receipt hashes myself. The hashes are the author's own checks, not mine.

## Scope
- **Model:** claude-opus-5.5 (Claude family). I edited no files and delegated nothing.
- **New articles:** I read all 17 in full.
- **Reuse articles:** I read 水滴, 水曜日 and ずっと in full and checked their changes against the related patch.
- **Kanji cards:** I read 蒸, 筒, 筆 and 線 in full, plus the patch.
- **Mappings:** I compared TSV rows 822–841 with the mappings JSONL and principal-reading.txt.
- **Other evidence read:**
  - the 29 component records
  - the Digital Daijisen captures in public-bodies.txt
  - selected-families-05 (contains 水曜 1372180, 水曜日 1372190, 水平, 水平線, 随筆 and 杉) and part of selected-families-09
  - a search of extra-comparison-reading.txt
- **Quiz checks:** I checked titles and `quiz_exclusions` for about 40 comparison articles by searching `words\`, and searched `docs\confusable-words.md` (no batch hits) and `docs\jlpt-levels.md`.
- **Outside lookups:** Jisho and Weblio for ずうっと.
- **Not read:**
  - review-evidence.json
  - the labels JSONL
  - public-bodies.json
  - selected-families-01–04, 06–08 and 10 (searched only, for 水曜日/1372190)
  - the snapshot JSONs
  - most of the 60 article bodies the author inspected

## Verdicts
Facets are correctness / scoped coverage / comprehensibility.

| Row | Article | Status | Verdict |
|---|---|---|---|
| N2:822 | 水蒸気 | new | CLEAN / CLEAN / CLEAN |
| N2:823 | 水素 | new | CLEAN / CLEAN / CLEAN |
| N2:824 | 垂直 | new | CLEAN / CLEAN / CLEAN |
| N2:825 | 推定 | new | CLEAN / CLEAN / CLEAN |
| N2:826 | 水滴 | reuse (only `jlpt: 2` added) | CLEAN / CLEAN / CLEAN |
| N2:827 | 水筒 | new | CLEAN / CLEAN / CLEAN |
| N2:828 | 随筆 | new | CLEAN / CLEAN / CLEAN |
| N2:829 | 水分 | new | CLEAN / CLEAN / CLEAN |
| N2:830 | 水平 | new | CLEAN / CLEAN / CLEAN |
| N2:831 | 水平線 | new | CLEAN / CLEAN / CLEAN |
| N2:832 | 水曜日 (source 水曜) | reuse, unchanged | CLEAN / CLEAN / CLEAN |
| N2:833 | ずうずうしい | new | CLEAN / CLEAN / CLEAN |
| N2:834 | ずっと (source ずうっと) | reuse | **NEEDS FIX** / CLEAN / **NEEDS FIX** (F1) |
| N2:835 | 末っ子 | new | CLEAN / CLEAN / CLEAN |
| N2:836 | スカーフ | new | CLEAN / CLEAN / CLEAN |
| N2:837 | 図鑑 | new | CLEAN / CLEAN / CLEAN |
| N2:838 | 杉 | new | CLEAN / CLEAN / CLEAN |
| N2:839 | 好き嫌い | new | CLEAN / CLEAN / CLEAN |
| N2:840 | 好き好き | new | CLEAN / CLEAN / CLEAN |
| N2:841 | 透き通る | new | CLEAN / CLEAN / CLEAN |

**N2:832 (水曜日):** 水曜/すいよう (entry 1372180) and 水曜日/すいようび (entry 1372190) are separate, valid entries. `水曜日.md:27` explicitly teaches 水曜 (すいよう) as the shortened form, and the article stays at N5.

**N2:834 (ずっと):** The entry (1006380) and senses 1–3 are correct, and the N3 metadata and guards are unchanged. Not selecting sense 4 is consistent with the blank source gloss.

**Kanji edits:** All four are CLEAN on all three facets. Each adds a link in the correct on-reading row and in Common words, and front matter is unchanged:
- 蒸: 水蒸気 at ジョウ
- 筒: 水筒 at トウ
- 筆: 随筆 at ヒツ
- 線: 水平線 at セン

**All twenty mappings:** Entry IDs, sense indices, article levels and the additional sense `1372180:1` agree with the principal evidence, and easier levels are kept.
- Correctness: CLEAN for all rows except 834, which is NEEDS FIX through F1.
- Coverage and comprehensibility: CLEAN for all rows.

## Findings
**F1 — Minor. Facets: correctness and comprehensibility. File: `words\ずっと.md:27`.**
- **Problem:** The paragraph calls ずうっと "a spelling associated with ずっと". The only lengthened form it describes as emphatic is ずーっと. It also uses dictionary jargon a learner won't understand: "same dictionary family" and "search-only kana form".
- **What is actually true:** ずうっと is a lengthened pronunciation (zuutto), not just a different spelling of short ずっと. It is the same stretched sound as ずーっと, written with う instead of ー.
- **Learner impact:** A learner may think ずうっと is pronounced like short ずっと or carries no emphasis, which mixes up a spelling variant with a pronunciation variant.
- **Minimal fix:** Replace the paragraph with something like: "You may also see ずうっと, which spells the same stretched pronunciation as ずーっと (with a long う). It has the same meanings as ずっと; the lengthening adds emphasis. Use ずっと as the ordinary form."
- **Evidence:**
  - principal-reading.txt:106 lists ずっと, ずーっと (spec1) and ずうっと (marked "search-only kana form").
  - principal-reading.txt:107 has the sense 1 note "ずーっと is emphatic".
  - Standard kana spelling: ずう is a long u sound.
  - Weblio corpus examples (夜中じゅう、ずうっと) show emphatic-duration use.
- **Confidence:** medium-high on the spelling-versus-pronunciation point; medium on the emphasis point.

## Optional
- **Kanji source lines:** The JMdict source-entry lists were not updated with the new entries: 1371660 at `蒸.md:48`, 1371910 at `筒.md:45`, 1372790 at `筆.md:48` and 1372060 at `線.md:51`. 筒, 筆 and 線 previously listed every linked word's entry; I found no documented rule requiring this.
- **Quiz exclusions:** Two pairs are inconsistent with how the author handled broader terms elsewhere. Neither creates a real ambiguity, because the target title is more specific.
  - 水筒 does not exclude 入れ物 ("container; receptacle") or ケース ("case; container").
  - 好き嫌い excludes 好き but not 嫌い ("disliked, dislike").
- **Backlinks:** `厚かましい.md:32` mentions 図々しい and `地平線.md:28` mentions 水平線, both in plain text; these could now link to the new articles.
- **Small additions:**
  - an example sentence for 水曜
  - 推定 in the passive (〜と推定される) and the legal sense (推定無罪)
  - a note that 透 is read す(く) in 透き通る
  - the proverb 蓼食う虫も好き好き
  - the の-forms of 垂直/水平
- **Redundant readings:** The hiragana after katakana words is unnecessary: エッセイ (えっせい) at `随筆.md:27` and マフラー (まふらー) at `スカーフ.md:26`.

## Limits
- This is not a native-speaker certification. The Daijisen captures were made by the author; I did not fetch them myself.
- Of the selected-family files I read only file 05 and part of file 09 (the rest I only searched), and I did not read the review-evidence JSON, the labels JSONL or public-bodies.json.
- I checked quiz exclusions only against titles found by targeted searches, not every possible quiz candidate.
- I could not find a fresh monolingual dictionary entry describing ずうっと's emphasis; F1's emphasis point relies on JMdict and kana spelling rules.
- I verified no Git history or hashes.
