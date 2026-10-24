# Batch-42 correction recheck (N2:822–N2:841): F1 resolved, no regressions

## Snapshot
I reviewed corrected commit `416bae390072e79df4dbf7cf8e161ce4fe9500cd`, committed content only. Its recorded parent is my original snapshot `1c55dc75c503046de66d6cf41e73bbe25c96fc62`, as required. I had file tools only, with no Git or commands. The parent link, hashes, clean-tree claim and equivalence checks are the author's own; I could not reproduce them.

## Scope
- **Model and session:** claude-opus-5.5 (Claude family), continuing my own initial review. I made no edits and used no agents.
- **New reads this session:**
  - the correction receipt and the full correction patch
  - all nine affected cards in full: 推定, 水平, ずっと, 厚かましい, 地平線, and kanji 蒸, 筒, 筆, 線
  - the comparison articles 計算, 予定 and 線, in full
  - `corrections-comparison-reading.txt`, with the complete 1252140 and 1543240 entries
  - `extra-comparison-reading.txt`, with the complete 1391780 entry for 線
  - TSV rows N2:821–841
  - front matter and key lines of 水曜日, 水滴, 水平線 and ずうずうしい
  - searches of the format docs for `quiz_exclusions` behaviour and link rules
  - searches of `words\` for titles containing "estimat", "level", "horizontal" or "line", and for `quiz_distractors`
  - a search of `corrected-review-evidence.json` for its adjudications and for any quiz-guard rationale; none is present
- **Fetches:** Two Kotobank lookups for ずうっと. One returned 404, and the other two (an ID guess and a site search) returned unrelated content.
- **Carried over from my initial review:** judgments on the 17 unchanged rows (15 new articles plus 水曜日 and 水滴). I did not reread those bodies this time, beyond the front-matter checks above.

## Verdicts
Facets are correctness / scoped coverage / comprehensibility.

| Row | Article | Status | Verdict |
|---|---|---|---|
| N2:822 | 水蒸気 | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:823 | 水素 | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:824 | 垂直 | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:825 | 推定 | new; **reassessed** (two exclusions added) | CLEAN / CLEAN / CLEAN |
| N2:826 | 水滴 | reuse, metadata only; inherited | CLEAN / CLEAN / CLEAN |
| N2:827 | 水筒 | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:828 | 随筆 | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:829 | 水分 | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:830 | 水平 | new; **reassessed** (線 exclusion added) | CLEAN / CLEAN / CLEAN |
| N2:831 | 水平線 | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:832 | 水曜日 | reuse, unchanged; inherited | CLEAN / CLEAN / CLEAN |
| N2:833 | ずうずうしい | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:834 | ずっと | reuse; **reassessed** (`ずっと.md:27`) | CLEAN / CLEAN / CLEAN |
| N2:835 | 末っ子 | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:836 | スカーフ | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:837 | 図鑑 | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:838 | 杉 | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:839 | 好き嫌い | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:840 | 好き好き | new; inherited | CLEAN / CLEAN / CLEAN |
| N2:841 | 透き通る | new; inherited | CLEAN / CLEAN / CLEAN |

**Reassessed rows:**
- **推定 and 水平:** Only the `quiz_exclusions` line changed; the teaching text is identical. The new targets 計算, 予定 and 線 all exist. None is a repeat or a self-reference, and none overlaps a `quiz_distractors` entry. Per `content-format.md:85-86`, one declaration excludes the pair in both directions.
- **ずっと:** Metadata is unchanged (jlpt 3, exclusions [常に, いつも]), as is the selection of senses 1–3.

**Four kanji revisions (蒸, 筒, 筆, 線): CLEAN / CLEAN / CLEAN.**
- Each source-entry line gains exactly one ID, in sorted position:
  - 1371660 for 水蒸気 on 蒸
  - 1371910 for 水筒 on 筒
  - 1372790 for 随筆 on 筆
  - 1372060 for 水平線 on 線
- These match TSV rows 822, 827, 828 and 831.
- The links in each card's reading row and Common words list are still there, at ジョウ, トウ, ヒツ and セン respectively. Front matter is unchanged.

**Two backlinks: CLEAN / CLEAN / CLEAN.**
- `厚かましい.md:32` now reads `[図々しい](ずうずうしい.md)`. The target article teaches the 図々しい spelling, and it already links back to 厚かましい.
- `地平線.md:28` now links `[水平線](水平線.md)`. 水平線 already links back at line 29.
- The wording is unchanged, and the front matter (jlpt 2 and 3, no exclusions) is unchanged. Both follow the relative-`.md` link rule in `content-structure.instructions.md:55`.

**Twenty mappings: all CLEAN / CLEAN / CLEAN.**
- TSV rows 822–841 are unchanged: source spellings, readings, raw glosses (including the blank one at 834), entry IDs, senses, levels and notes.
- 水曜日 (N2:832) still keeps source 水曜 at 1372180:1 and the article's own entry 1372190:1 at N5, and `水曜日.md:27` still teaches 水曜 (すいよう).
- 水滴 (N2:826) remains a metadata-only reuse.
- The easier levels (N5 水曜日, N3 ずっと) are preserved.
- Row 834 is now CLEAN because F1 is resolved.

## Findings
**F1 (`ずっと.md:27`) is resolved.**
- **New text:** "ずうっと writes a lengthened う sound, like ずーっと. This sound stretching can add emphasis; it does not create a separate word. Use ずっと as the ordinary spelling. JMdict indexes ずうっと as a search-only form for lookup, rather than its main spelling."
- **What it fixes:** The paragraph now states the long-vowel pronunciation and relates it to ずーっと. The emphasis claim is hedged ("can") and is not attributed to JMdict. The search-only flag is kept and explained without jargon.
- **Evidence:**
  - Principal reading lines 106–107: the entry lists ずっと, ずーっと and ずうっと (search-only), and its sense-1 note reads "ずーっと is emphatic".
  - ずうっと and ずーっと spell the same lengthened pronunciation.
- **On the author's qualification:** I partly accept it. The original paragraph never explicitly stated a short pronunciation. Its defect was an imprecise "spelling" label and an incomplete explanation, not a false rule. My initial correctness NEEDS FIX was arguably stronger than the comprehensibility and coverage gap I demonstrated. Either way, the issue is fixed.
- **Confidence:** high.

**My original optional suggestions:**
- **Adopted and verified correct:** the four kanji source-entry IDs and the two backlinks.
- **Not adopted, and still optional:** a 水筒/入れ物 exclusion, a 好き嫌い/嫌い exclusion, extra examples, the legal/passive uses of 推定, the 蓼食う虫も好き好き proverb, the の forms of 垂直/水平, and the redundant hiragana after katakana. None of these is a defect.

**The new exclusions came from the other reviewer; I did not identify them initially.** All three are acceptable and none is excessive:
- **推定/計算 (well supported):** 1252140 sense 2 includes "estimation", and `計算.md` itself teaches the estimation and take-into-account extension. So "estimation; inference" is a genuinely ambiguous English label for a 計算 prompt.
- **推定/予定 (weaker but defensible):** 1543240 sense 1 includes "expectation" and "estimate", but the 予定 article does not teach that meaning. It is a conservative, low-cost guard.
- **水平/線 (defensible, low cost):** 1391780 sense 6 is "level". The 線 article teaches only senses 1, 2 and 4 under the title "line", so the clash in English labels is mild. The teaching was not changed to equate 線 with horizontal.

**New regression findings:** none.

## Optional
- The 水筒/入れ物 and 好き嫌い/嫌い exclusions are consistency polish only.
- The remaining examples and usage additions are nonblocking:
  - an example sentence for 水曜
  - 推定される and 推定無罪
  - the note that 透 is read す(く) in 透き通る
  - the 好き好き proverb
  - the の forms of 垂直/水平
- The parenthetical (ずうずうしい) after the new link in `厚かましい.md:32` is harmless.

## Limits
- I verified no Git, commit or hash claims. I am treating the working-tree files as the committed content, as the author's receipt asserts.
- I found no fresh monolingual dictionary entry describing ずうっと as emphatic: Kotobank failed or was irrelevant, and Weblio earlier gave only corpus examples. The hedged "can add emphasis" rests on JMdict's note on ずーっと plus the spelling equivalence.
- No quiz draws were actually run; the exclusion assessment is based on titles and articles only.
- The 17 unchanged-row judgments carry over from my initial review and were not reread this session.
- I only searched `corrected-review-evidence.json`; I did not read it in full.
- This is not a native-speaker certification.
