## Snapshot
The frozen commit is `11d1b0ae8caf19e6aac628e1774a9f21d8ab503e`, with parent `8df57903f716932690acdff28f84b6e285924d94`. The receipt says the reviewed content is committed and clean. I had file tools only and could not run Git, so I could not confirm that the files on disk match that commit or check the receipt's hashes. Everything below was read from the files on disk, on the assumption that they match the commit.

## Scope
- **Model:** claude-opus-5.5 (Claude family). I worked sequentially and edited nothing.
- **New articles:** I read all 18 completely.
- **Related changes:** I read the full nine-file patch and checked each change in context: 各, 角 and 算 kanji cards, 各地, 火山, 積む, 級, アクセサリー and 能力. I did not re-review unchanged teaching in those files.
- **Existing-article claims:** For 各地 and 火山 I checked only that the existing article teaches the source spelling, reading and meaning, and that the edit adds only `jlpt: 2` (plus, for 火山, a link to 火口).
- **Source mappings:** I checked all 20 rows (N2:262–281) against the TSV, the batch rows and the dictionary entries.
- **Other material read:** the repository rules, content-format lines 18–119, jlpt-levels.md and confusable-words.md (searched for this batch's words). I also read every word named in a `quiz_exclusions` list, plus 立場, 位, 断る, 可 and 被る.
- **Not read (forbidden):** the excluded notes, review files and receipts listed in the brief.

## Verdicts

Each cell is correctness / scoped coverage / comprehensibility.

| Article | Correctness | Coverage | Comprehensibility |
|---|---|---|---|
| 各自 | CLEAN | CLEAN | CLEAN |
| 拡充 | CLEAN | CLEAN | CLEAN |
| 学術 | CLEAN | CLEAN | CLEAN |
| 拡張 | CLEAN | CLEAN | CLEAN |
| 角度 | NEEDS FIX (R01) | CLEAN | CLEAN |
| 学年 | NEEDS FIX (R03) | CLEAN | CLEAN |
| 学部 | CLEAN | CLEAN | CLEAN |
| 格別 | CLEAN | CLEAN | CLEAN |
| 確率 | CLEAN | CLEAN | CLEAN |
| 学力 | CLEAN | CLEAN | CLEAN |
| 掛け算 | CLEAN | CLEAN | CLEAN |
| 可決 | CLEAN | CLEAN | CLEAN |
| 火口 | CLEAN | CLEAN | CLEAN |
| 下降 | NEEDS FIX (R02) | CLEAN | CLEAN |
| 重なる | CLEAN | CLEAN | CLEAN |
| 重ねる | CLEAN | CLEAN | CLEAN |
| 飾り | CLEAN | CLEAN | CLEAN |
| かしこまりました | CLEAN | CLEAN | CLEAN |

**Related changes: all nine are CLEAN.**
- The kanji cards 各, 角 and 算 each add the new word to their common-words list at the actual reading:
  - 各 → 各自 かくじ
  - 角 → 角度 かくど
  - 算 → 掛け算 かけざん, with a note on the voicing
  - Each card also updates its dictionary citation. Earlier readings, including 算's そろ note, are kept.
- These five links each point at a comparison that is already taught:
  - 火山 → 火口
  - 積む → 重ねる (stacking)
  - 級 → 学年 (school year)
  - アクセサリー → 飾り
  - 能力 → 重ねる (the 練習を重ねて example)

**Existing-article claims: 各地 and 火山 are CLEAN.** 各地 already teaches かくち as "various places / all parts", with 日本各地 and 世界各地. 火山 already teaches かざん as "volcano". Neither file had a `jlpt` field before.

**Mappings: all 20 are CLEAN** for spelling, reading and meaning.
- **Coverage gaps the TSV already discloses:**
  - 拡張: its computing "escape (ESC)" sense is not taught.
  - 火口: the source gloss "origin of a fire" belongs to the separate word ひぐち, and the article keeps that apart rather than moving the meaning to かこう.
- **Dictionary interpretations the TSV already discloses:**
  - 重ねる: the source gloss "add" is read as stacking or accumulating, not arithmetic addition.
  - 角度: the "viewpoint" meaning is not a separate JMdict sense.
- **Second meanings I confirmed in Kotobank:**
  - 角度 has a figurative "viewpoint" meaning (Seisenban ②).
  - 学部 has an "undergraduate division, as opposed to graduate school" meaning (Seisenban ②).
- **掛け算:** the claim that 掛ける's multiplication sense is "usually written かける" is correct; JMdict 1207610 sense 9 is marked as usually written in kana.

## Findings

**B14-R01 — Minor — correctness (quiz exclusions) — `words\角度.md:4,9`; `words\立場.md:4,9,13-14`**
- **Claim and impact:** 角度 is titled "angle; viewpoint" and 立場 is titled "position; standpoint", but neither card excludes the other. "Viewpoint" and "standpoint" are near-synonyms in English. 立場 is tagged `perspective` and explicitly teaches "the standpoint from which they understand an issue". 角度 teaches 別の角度から考える, which is close to 立場から考える. A learner could reasonably accept either title for either word, in both quiz directions.
- **Remedy:** add 立場 to `quiz_exclusions` in 角度.md.
- **Evidence:** the titles and bodies above; content-format.md:95, which defines when an exclusion is needed; and the batch's own guard for 角度/釣る, which protects a label overlap of the same kind.
- **Confidence:** medium-high.

**B14-R02 — Minor — correctness (quiz exclusions) — `words\下降.md:4,9`; `words\断る.md:4`**
- **Claim and impact:** 下降 is titled "descent; decline" and 断る is titled "refuse; decline". The exact word "decline" appears in both, as a noun in one and a verb in the other, and there is no exclusion. The batch excludes the same kind of noun/verb overlap for 角度/釣る ("angle") and 飾り/飾る ("ornament"). It excludes 可決/通行 for a shared "passage" label, so this omission is inconsistent.
- **Remedy:** add 断る to `quiz_exclusions` in 下降.md.
- **Evidence:** both titles; batch-14.json lines 15598, 15600 and 15602 (the stated reasons for those other exclusions).
- **Confidence:** medium.

**B14-R03 — Minor — correctness (quiz exclusions) — `words\学年.md:4,9`; `words\位.md:4,9,15`**
- **Claim and impact:** 学年 is titled "school year; grade" and 位 is titled "rank; grade", and 位 teaches "a grade or level". 学年 already excludes 成績 because of the "grade" overlap, and 級 ("class; rank; level"). 位 sits in the same bucket but is not excluded, so a "grade" ambiguity remains in both quiz directions.
- **Remedy:** add 位 to `quiz_exclusions` in 学年.md.
- **Evidence:** both titles; 位.md line 15; batch-14.json line 15599, which gives the reason for the 学年/成績 exclusion.
- **Confidence:** medium.

## Optional
- **飾り.md:15:** the article says 飾り "also appears as the final element of words naming decorations" but gives no example. Adding 髪飾り (かみかざり) or 首飾り (くびかざり) would make that usable.
- **飾り.md:25:** "an 飾り" should read "a 飾り".
- **火口.md:4:** the title gives "boiler burner" equal weight with "crater". I checked Kotobank myself: Seisenban's かこう entry defines only the volcanic opening, and lists the burner-like meanings under ひぐち. JMdict does support the boiler-burner sense at かこう, and the body says so accurately. Consider showing it as a secondary or specialised sense.
- **Possible extra quiz exclusions (low confidence):**
  - かしこまりました with 分かる ("to understand", against "understood") or with 確か ("certain")
  - 可決 with 可 ("acceptable; permitted", against "approval")

## Limits
- **No Git:** I could not confirm that the files on disk match the frozen commit, or check the receipt's file hashes and patch hash.
- **Dictionary checks I fetched myself:** 角度, 学部, 格別, かしこまりました, 火口, 拡張 and 拡充 on Kotobank.
- **Author-only evidence:** the inspection receipts for 学術 and 学力 rest on the author's account. JMdict independently supports their core meanings.
- **Comparison entries:** I read the batch's comparison entries only where needed (for example, 掛ける 1207610). I did not read every comparison entry in full.
- **Easier levels for 各地 and 火山:** I inferred that neither word sits at N3–N5 from their missing `jlpt` fields and jlpt-levels.md's statement that lower-level coverage is complete. I did not search the lower-level TSVs, because they are not on the allowed list.
- **Naturalness:** example sentences were judged by me, not certified by a native speaker.
- **Quiz overlaps:** the search used title keywords across words\, so it is not exhaustive.
