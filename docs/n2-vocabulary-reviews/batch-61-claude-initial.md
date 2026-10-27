## Snapshot
I reviewed commit **c28c421695f83aac0494994c604792fa8c0f277d**, whose parent is 45d3bbbc5c1a98a48fd3d00c4284d94692b96930. frozen-snapshot.json reports `cleanCommittedContent: true`. My file tools cannot run Git, so I could not confirm that the working tree matches this commit, and the hash and equivalence checks are the author's, not mine.

## Scope
**Model:** claude-opus-5.5 (claude family). The review was read-only, with no edits, agents or delegation.

**Repository files read:**
- .github\copilot-instructions.md, content-structure.instructions.md, docs\content-format.md:18-103 and docs\jlpt-levels.md.
- The TSV header and rows N2:1202–1221 only.
- All 16 new articles in full and all 4 reused bodies (溶ける, とこや, 飛ぶ, 止まる) in full.
- kanji\溶.md, 床.md and 戸.md in full, and a glob of kanji\ to see which cards exist.
- Comparison articles and front matter found by searching words\: 泊まる, 宿泊, 都市, 準備, 用意, 支度, 特殊, 味噌, 利益, 人物, 得意, 終わる, 終える, 中, 方々, ごろごろ, 各地, ずっと, 避ける, 吠える and 止める.

**Private files read:**
- frozen-snapshot.json, related.patch, review-mappings.jsonl, review-principals.jsonl, review-components.jsonl, review-labels.jsonl and public-bodies.txt.
- Selected ranges of review-evidence.json: around lines 117, 3372, 5878–5935 and 39509–39880, which cover the 1198910 adjudication and the access-limit notes.

**External sources:**
- ja.wiktionary とまる loaded: one heading 止まる・留まる・停まる, with no per-sense spelling split.
- The bunka.go.jp 異字同訓 PDF came back as unparsable binary.
- The weblio とまる page returned unrelated content, and kotobank returned 404.

**Not read:**
- family-inspection-01…11, the three comparison-reading files and public-bodies.json.
- The rest of review-evidence.json.
- docs\confusable-words.md and both docs snapshot JSONs.
- Lower-level TSV rows, which were not permitted.

## Verdicts
Cells are correctness / scoped coverage / comprehensibility. Nits (F6, F7) do not change a cell to NEEDS FIX.

| Row | Article | Verdict |
|---|---|---|
| N2:1202 特色 | words\特色.md | CLEAN / CLEAN / CLEAN (nit F6) |
| N2:1203 特長 | words\特長.md | CLEAN / CLEAN / CLEAN (nit F6) |
| N2:1204 特定 | words\特定.md | CLEAN / CLEAN / CLEAN |
| N2:1205 特売 | words\特売.md | CLEAN / CLEAN / CLEAN (nit F7) |
| N2:1206 溶け込む | words\溶け込む.md | CLEAN / CLEAN / CLEAN |
| N2:1207 溶ける | words\溶ける.md (reused, only jlpt:2 added) | CLEAN / CLEAN / CLEAN |
| N2:1208 退ける | words\退ける.md | CLEAN / CLEAN / CLEAN |
| N2:1209 床の間 | words\床の間.md | CLEAN / CLEAN / CLEAN |
| N2:1210 床屋 | words\とこや.md (reused) | CLEAN / **NEEDS FIX** (F5) / CLEAN |
| N2:1211 所々 | words\所々.md | CLEAN / CLEAN / CLEAN |
| N2:1212 都心 | words\都心.md | **NEEDS FIX** (F2) / CLEAN / CLEAN |
| N2:1213 戸棚 | words\戸棚.md | CLEAN / CLEAN / CLEAN |
| N2:1214 とっくに | words\とっくに.md | CLEAN / CLEAN / CLEAN (supported by JMdict only; see Limits) |
| N2:1215 どっと | words\どっと.md | CLEAN / CLEAN / CLEAN |
| N2:1216 整う | words\整う.md | **NEEDS FIX** (F3) / CLEAN / CLEAN |
| N2:1217 留まる (とどまる) | words\留まる.md | **NEEDS FIX** (F4, F1 at line 43) / CLEAN / CLEAN |
| N2:1218 どなる | words\どなる.md | CLEAN / CLEAN / CLEAN |
| N2:1219 飛び込む | words\飛び込む.md | CLEAN / CLEAN / CLEAN |
| N2:1220 跳ぶ | words\飛ぶ.md (reused, unchanged) | CLEAN / CLEAN / CLEAN |
| N2:1221 留まる (とまる) | words\止まる.md (reused) | **NEEDS FIX** / **NEEDS FIX** (F1) / CLEAN |

**Kanji edits (溶, 床, 戸): CLEAN.**
- The headers are unchanged.
- All five pairs appear at their actual readings: 溶け込む とけこむ, 溶ける とける, 床の間 とこのま, 床屋 とこや and 戸棚 とだな.
- Each new pair has a reading-row example, a Common words link and a matching footer ID: 1546090, 1349400, 1349410 and 1267050.
- The word-side links are substantive.

**Baseline preservation: CLEAN.**
- 溶ける only gains `jlpt: 2`.
- とこや keeps its kana identity, its title and N4, and only adds the 床 link.
- 飛ぶ is unchanged, and its existing text already teaches the 跳ぶ spelling and hopping.
- In 止まる.md the front matter and lines 1–33 are kept; new text is at lines 35–47.

**Mappings: CLEAN for 19 rows; N2:1221 has a scope gap.**
- Every family and sense selection matches the principal records.
- The evidence confirms that 解ける 1198910 ("be solved; come loose") is a separate family from 溶ける 1546070. That 溶ける has no lower-level row is the author's check, not mine.
- N2:1221 maps to the source's own entry, 1310620:1–3, which is correct as an identity. However, its source gloss "(1) to be fixed" is not among the pinned senses. The public Daijisen とまる entry supports it (sense 4 画鋲ではうまく―らない; sense 5 目に―る), so the article has to teach it.

## Findings
**F1 — moderate; correctness and coverage; 止まる.md:35-36 and 42-43; 留まる.md:43**
- **Problem:** 止まる.md says that in the perching use "it uses 留", which presents 留 as *the* spelling for perching. Meanwhile, the source sense "to be fixed" gets only an abstract sentence, with no example and no 目に留まる.
- **Evidence:**
  - JMdict 1310620 has no sense-level spelling restriction, and 止まる (ichi1) is the primary spelling.
  - The Daijisen heading in public-bodies.txt (~302–330) is 止(ま)る／留(ま)る with no per-sense split, and its perching examples are written in kana.
  - ja.wiktionary also has a single heading with no split.
- **Fix:** Say that perching may also be written 留まる, with 止まる common. Add one fastened example (for example ボタンがうまく留まらない) and 目に留まる as a recognition item. Adjust 留まる.md:43 to match.
- **Confidence:** medium. The official 異字同訓 spelling guide could not be read.

**F2 — minor; quiz; 都心.md:9**
- **Problem:** 都市 is missing from the exclusions. Its title "city; urban center" is close to 都心's "city center; downtown", and 都心.md:36 itself contrasts the two. No other article declares the guard.
- **Fix:** Add 都市.
- **Confidence:** medium-high.

**F3 — minor; quiz; 整う.md:9**
- **Problem:** 準備, 用意 and 支度 are missing from the exclusions. Their titles ("preparation(s); getting ready") overlap with 整う's "be ready", and line 21 uses 準備が整う. 整備 already excludes all three.
- **Fix:** Add all three.
- **Confidence:** medium.

**F4 — minor; quiz; 留まる.md:9**
- **Problem:** 泊まる ("stay overnight") is missing, although the title is "remain; stay" and 滞在 is already excluded. Line 46 itself contrasts overnight lodging.
- **Fix:** Add 泊まる.
- **Confidence:** medium.

**F5 — minor; component link; とこや.md:23**
- **Problem:** kanji\屋.md exists, but 屋 is plain text on the line this batch edited.
- **Fix:** Link it as [屋](../kanji/屋.md).
- **Confidence:** high.

**F6 — nit; quiz excess; 特色.md:9, 特長.md:9, 整う.md:9, 都心.md:9**
- **Problem:** Some exclusions are not justified by the titles or bodies:
  - 利益 and 味噌 for 特色 and 特長; 味噌.md teaches only "miso paste".
  - 終わる and 終える for 整う.
  - 中 for 都心.
- **Impact:** These shrink the pool of quiz choices without preventing a real ambiguity.
- **Fix:** Drop them, or justify them in the body.
- **Confidence:** medium-low. The ミソ "selling point" sense could partly justify 味噌.

**F7 — nit; comprehensibility; 特売.md:30**
- **Problem:** "not トク + マイ" contrasts with マイ, which is not a reading of 売.
- **Fix:** Delete it, or contrast 売 (バイ) with 買 (バイ) instead.
- **Confidence:** medium.

## Optional
- Consider excluding 特殊 for 特定 (low priority; the titles "specific" and "special" differ).
- Consider 宿泊 for 留まる and 吠える for どなる.
- Note that 所々 is usually written in kana and has the reading しょしょ.
- Note that 疾っくに is rare, and that 調う and 斉う are flagged rare in JMdict.
- Mention Daijisen's note that the ど in どなる is onomatopoeic.
- Soften "usually written どける" (退ける.md:17).
- Remove the どと contrast in どっと.md.

## Limits
- The public とっくに endpoint returned nothing; that row rests on JMdict alone.
- The 19 public captures all come from one dictionary service (weblio Daijisen).
- I could not verify the official 異字同訓 guide.
- The lower-level checks for 溶ける, and all hash and equivalence checks, are the author's, not mine.
- "Usually written" frequency claims are unmeasured.
- This is not a native-speaker certification, and the files listed as not read could hold quiz evidence I have not seen.
