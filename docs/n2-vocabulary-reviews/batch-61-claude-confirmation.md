I found no regressions and no new defect in the article content. The author misstated the evidence for the どける spelling claim, and two inherited quiz-guard gaps remain.

## Snapshot
I reviewed corrected commit **b76948a5da23c6267098c80359cf81e836e28a8a**; its parent is **c28c421695f83aac0494994c604792fa8c0f277d**. correction-snapshot.json reports `cleanCommittedContent: true`. My file tools cannot run Git, hash, manifest or cleanliness checks, and I did not inspect .git. Those checks were run by the author, not by me.

## Scope
**Model:** claude-opus-5.5 (claude family). Read-only, with no edits, agents or delegation.

**Read in full this turn:**
- correction-snapshot.json and the whole correction.patch: 10 files under words\ only, with no kanji or mapping files.
- All ten changed articles: 特長, 特定, 特売, 都心, どっと, 整う, 留まる, どなる, とこや and 止まる.
- correction-families-01 and -02. I counted 29 families and 90 senses (17/48 and 12/42).
- The いい rendering: eight separate dictionary entries, 11 senses. Only entry 2820690 has "ready; prepared"; the other seven are archaic or literary words that happen to share the sound, and I kept them apart.
- The 吠える rendering: one entry, 3 senses.
- All three old-body chunks, 20 articles: いる, ストップ, 立ち止まる, 入る, 良い, いい, 機能, 都市, 準備, 用意, 支度, 泊まる, 宿泊, 特殊, 吠える, 利益, 味噌, 終わる, 終える, 中.
- The TSV header and rows N2:1202–1221 (lines 1202–1221).
- words\退ける.md, which is unchanged.

**Partial reads:**
- corrected-review-evidence.json: only the 2850084 records (lines 2009–2052 and 24435–24478) and two grep hits (lines 134 and 3380).
- Front matter of 飛ぶ, 飛行, 止む, 止める, 停止, 中止, 飛び出す, 居る, 特別, 独特, 格別, 一定, 指定 and 具体.
- A search of words\ for `quiz_distractors` conflicts (none found).
- A kanji\ glob confirming that the 屋, 調, 止 and 留 cards exist.

**Carried over from my first review:**
- Full reads of the other nine unchanged articles and all three kanji cards.
- The five two-way word/kanji link pairs.
- The Daijisen captures, read in my first review from public-bodies.txt, which I am not permitted to read this turn.

**Not read:**
- The rest of corrected-review-evidence.json.
- frozen-snapshot.json and related.patch were not reread.

**Depth caveat:** my first review read few older articles in full. I did not catch the 止む and 飛行 quiz gaps then. Because the two reviewers read to different depths, the reviews cannot be used to rank the models.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1202 特色 | words\特色.md | First-review full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1203 特長 | words\特長.md | Full reread; changed | CLEAN | CLEAN | CLEAN |
| N2:1204 特定 | words\特定.md | Full reread; changed | CLEAN | CLEAN | CLEAN |
| N2:1205 特売 | words\特売.md | Full reread; changed | CLEAN | CLEAN | CLEAN |
| N2:1206 溶け込む | words\溶け込む.md | First-review full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1207 溶ける | words\溶ける.md (reused) | First-review full read; unchanged | CLEAN (only jlpt:2 added) | CLEAN | CLEAN |
| N2:1208 退ける (どける) | words\退ける.md | Full reread; unchanged | CLEAN (on different grounds; see R1) | CLEAN | CLEAN |
| N2:1209 床の間 | words\床の間.md | First-review full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1210 床屋 → とこや | words\とこや.md (reused) | Full reread; changed | CLEAN | CLEAN | CLEAN |
| N2:1211 所々 | words\所々.md | First-review full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1212 都心 | words\都心.md | Full reread; changed | CLEAN | CLEAN | CLEAN |
| N2:1213 戸棚 | words\戸棚.md | First-review full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1214 とっくに | words\とっくに.md | First-review full read; unchanged | CLEAN (JMdict only) | CLEAN | CLEAN |
| N2:1215 どっと | words\どっと.md | Full reread; changed | CLEAN | CLEAN | CLEAN |
| N2:1216 整う | words\整う.md | Full reread; changed | CLEAN | CLEAN | CLEAN |
| N2:1217 留まる (とどまる) | words\留まる.md | Full reread; changed | CLEAN | CLEAN | CLEAN |
| N2:1218 どなる | words\どなる.md | Full reread; changed | CLEAN | CLEAN | CLEAN |
| N2:1219 飛び込む | words\飛び込む.md | First-review full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1220 跳ぶ → 飛ぶ | words\飛ぶ.md (unchanged reuse at N5) | First-review full read; unchanged | CLEAN for the 跳ぶ/hopping mapping only; old 飛ぶ/飛行 quiz gap remains | CLEAN | CLEAN |
| N2:1221 留まる (とまる) → 止まる | words\止まる.md (reused) | Full reread; changed | CLEAN for the batch additions only; old 止まる/止む quiz gap remains | CLEAN | CLEAN |

**Kanji links: CLEAN (carried over).** The patch touches no kanji files. The five pairs (溶/溶け込む, 溶/溶ける, 床/床の間, 床/床屋 via とこや, 戸/戸棚) remain as judged in my first review. The new 屋, 調 and 止 links point to cards that exist, and none of them needs a matching link back from the kanji card.

**Baseline preservation: CLEAN.**
- The patch changes only `quiz_exclusions` lines in front matter. No word ID, reading, title, level or kanji list changes.
- とこや keeps N4, its kana ID and `kanji: []`.
- 止まる's front matter and baseline lines 1–33 are unchanged; the edits are in the batch-added lines 35–47.
- 溶ける and 飛ぶ are not in the patch.

**Mappings: CLEAN.** TSV rows 1202–1221 match my first-review table exactly: same article, entry, selected senses and additional senses. N2:1221's raw gloss "to be fixed" is now covered by the fixed-in-place teaching.

## Findings
**My first-review findings**
- **F1: resolved** (止まる.md:35-36, 44, 46; 留まる.md:42-45).
  - Perching is now presented as possible with 留, not as the only spelling.
  - The Daijisen fixed-in-place example 画鋲ではうまく留まらない and the phrase 目に留まる have been added.
  - The cross-reference in 留まる.md is consistent and keeps the two readings separate.
  - I withdraw my earlier suggestion that 止まる is "common" for perching. Shared dictionary headings and spelling priority do not show how often each spelling is used per sense.
- **F2: resolved.** 都心.md:9 now excludes 都市.
- **F3: withdrawn.**
  - 準備, 用意 and 支度 name the act of preparing, while 整う describes the resulting ready state.
  - The bodies confirm this: 準備ができました, 用意ができた, and 準備が整う at 整う.md:21. Each quiz direction has a single best answer.
  - The new guards follow the same principle: they cover state words meaning "be ready" (いい, 良い, 入る).
- **F4: resolved.** 留まる.md:9 now excludes 泊まる and 宿泊 ("stay" overlaps "overnight stay"), and line 48 still says the article does not mean overnight lodging.
- **F5: resolved.** とこや.md:23 now links 屋.
- **F6: mostly withdrawn.**
  - 終わる/終える are justified by 整う sense 4 ("completed") and the article's own "preparations ... are complete".
  - 利益 is justified by its sense 2 ("benefit; advantage") against 特長's "merit".
  - 味噌 is weak but defensible: sense 3 means "key point; good part", usually written ミソ.
  - 中 on 都心 remains the weakest guard. Its titles ("inside; middle" against "city center; downtown") give a clear best answer, and 中心 and 真ん中 already cover "center". This is harmless excess and not a defect.
- **F7: resolved.** トク + マイ (特売.md:30) and どと (どっと.md, old line 29) were deleted. My earlier alternative of contrasting 売 with 買 was poor because both are read バイ; deletion was the right fix.

**Optional candidates from my first review:** 特定/特殊 (特定.md:9) and どなる/吠える (どなる.md:9, based on 吠える sense 3 "yell; shout" about people) are justified.

**Changes proposed by the GPT reviewer:**
- **留まる + いる, ストップ, 立ち止まる:** justified. いる has sense 2 "to stay". The written form 留まる is also a dictionary spelling of とまる "stop", and Daijisen records a stopping use of とどまる.
- **整う + いい, 良い:** justified (sense 2 "ready; prepared").
- **整う + 入る:** defensible but the weakest guard. Its "be ready" sense (12) is limited to tea or coffee, and the 入る article does not teach it.
- **特長 + 機能:** justified. 特長 is routinely rendered "features" for products, and 機能.md teaches "useful feature".
- **Links 屋, 調, 止:** substantive. Kanji lists still describe only the primary spelling.
- **Inherited quiz gaps:** confirmed by titles.
  - Neither 止まる ("to stop, come to a halt") nor 止む ("cease; let up") excludes the other.
  - Neither 飛ぶ ("fly; soar") nor 飛行 ("flight; flying") excludes the other.
  - The author's decision not to fix them in this batch is acceptable, because the batch did not cause them and its edits do not touch them. However, 止まる sense 2 ("cease") is one of N2:1221's mapped senses, so I have qualified that row's CLEAN.
  - A single exclusion on either side is enough to fix each one later, since exclusions apply in both directions (content-format.md:86).

**Regressions:** none found.
- I checked for duplicate IDs, self-references and missing targets in the new exclusion lists and found none.
- No `quiz_distractors` conflict exists.
- All link targets exist.
- The change counts match the patch: 12 new guards, 3 links and 2 deletions.

**New**
- **R1 — evidence misstatement, nit; no article change** (corrected-review-evidence.json:2030-2052 and 24456-24478; 退ける.md:17).
  - The author says 退ける (2850084) carries an explicit "usually written in kana" label. Both pinned records show `misc: []`, so there is no such label.
  - The wording "usually written どける" still has support elsewhere. Daijisen writes the heading ▽退ける, and どける is not an official (jōyō) reading of 退.
  - **Fix:** correct the stated basis; optionally soften the wording to "commonly written in kana".
  - **Confidence:** high that the label claim is wrong; medium on the frequency.

## Optional
- 止まる: add "perching may also be written 止まる". This is a statement about which spellings exist, not how often they are used.
- 整う: note that JMdict marks 調う and 斉う as rarely used kanji forms.
- 所々: mention the kana tendency and the reading しょしょ.
- Note that 疾っくに is rare.
- Mention the onomatopoeic ど in どなる.
- Weak quiz-guard candidates: 都心/都会, 留まる/停止 and 特定/特別.
- Remaining disagreements: 都心/中 and 整う/入る are weak, low-harm guards.

## Limits
- Git, hash, manifest, baseline-identity and lower-level JLPT checks were run by the author, not by me.
- The 止まる/止む and 飛ぶ/飛行 quiz gaps remain unfixed. I am not claiming the whole corpus is quiz-clean.
- I could not read the official guide to kanji for same-reading words (異字同訓), so I could not check which spelling it recommends for perching.
- The Daijisen claims rest on my first-review reading of a single dictionary service.
- The とっくに public lookup failed, so that row relies on JMdict alone.
- I did not reread the unchanged articles or kanji cards apart from 退ける.
- I ran no live quiz draws, measured no frequencies, did no exhaustive synonym audit and have no native-speaker certification.
