## Snapshot
**Commit:** `787b93e13814f9f2052f641645fad70e6962007d` (parent `6c66db7f90abc63b28fa7aa376eb78fe12a189ce`), taken from the frozen receipt. I reviewed committed content only.

I only had file tools and could not run Git or compute hashes. So I could not confirm that the files I read match that commit. I relied on the receipt's `cleanCommittedContent: true` statement.

## Scope
- **Model:** claude-opus-5.5 (claude family).
- **Instructions read:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md:18-126`.
- **New articles:** I read all 19 in full.
- **捜す reuse:** I read the whole of `words\捜す.md` and checked the front matter of `探す.md`. It stays at N4 (jlpt 4) with the title "look for".
- **Kanji edits:** I read the seven-file patch and the full current text of 混, 再, 祭, 採, 材 and 逆.
- **Mappings:** I read TSV rows 582-601 and the header.
- **Evidence JSON:** I read rows, entryFamilies, newArticles/provenance, existingComparisonLabels, actualEntryInspections, quizDeclarations, the external-recognition sections and sourceAccessLimits. I did targeted reads of entries 1054850, 1258500, 1290360, 1593650 and 1593670.
- **Other checks:**
  - Kanji levels and the 7 missing kanji files (献, 催, 促, 災, 裁, 縫, 遡) confirmed.
  - Every link target exists.
  - I grepped all `words\` titles and exclusion lists for overlapping English labels.
- **Not read:** componentEvidence (1501-2480), inspectedComponentRecords (16010-16985) and most of comparisonEntryFamilies. I checked component claims against the `kanji\` files directly instead.
- **Not done:** no forbidden files, no app/quiz execution, no tests.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 混合 | NEEDS FIX (B30-C1) | CLEAN | CLEAN |
| コンセント | CLEAN | CLEAN | CLEAN |
| 献立 | CLEAN | NEEDS FIX (B30-C2) | CLEAN |
| こんばんは | CLEAN | CLEAN | CLEAN |
| サークル | CLEAN | CLEAN | CLEAN |
| 在学 | CLEAN | CLEAN | CLEAN |
| 再三 | CLEAN | CLEAN | CLEAN |
| 祭日 | CLEAN | CLEAN | CLEAN |
| 催促 | CLEAN | CLEAN | CLEAN |
| 採点 | CLEAN | CLEAN | CLEAN |
| 災難 | CLEAN | CLEAN | CLEAN |
| 裁縫 | CLEAN | CLEAN | CLEAN |
| 材木 | CLEAN | CLEAN | CLEAN |
| サイレン | CLEAN | CLEAN | CLEAN |
| 逆さ | CLEAN | CLEAN | CLEAN |
| 逆さま | CLEAN | CLEAN | CLEAN |
| 遡る | CLEAN | CLEAN | CLEAN |
| 酒場 | CLEAN | CLEAN | CLEAN |
| さきおととい | CLEAN | CLEAN | CLEAN |

**捜す reuse: CLEAN / CLEAN / CLEAN.**
- The only change is `jlpt: 2`.
- JMdict 1593670 has no spelling restrictions on either sense.
- Sense 1 (search for, look for, seek) is taught by 鍵を捜しています ("I am looking for the keys").
- Additional sense 2 (search through a place) is taught by 部屋を捜しました ("I searched the room").
- JMdict's 探す/捜す note is correctly presented as a tendency, not a rule.
- The title, existing exclusions and 探す's N4 (jlpt 4) level are unchanged.

**Six kanji edits: CLEAN / CLEAN / CLEAN.**
- Each kanji now links its new word at the actual reading: 混合 コン, 再三 サイ, 祭日 サイ, 採点 サイ, 材木 ザイ, 逆さ さか.さ.
- 逆さま is added to 逆's common words.
- Each metadata line cites the new entry ID. In 祭.md, 1295310 was already cited, so no change was needed.
- 逆.md avoids inventing a separate さかさま reading for 逆.

**Twenty mappings:**
- **Correctness:** CLEAN for all 20. Entry IDs, senses, the 1593670:2 additional sense and the article paths all match.
- **Coverage:** CLEAN for 19. N2:584 (献立) is NEEDS FIX because its selected sense 2 is only mentioned in the article (B30-C2).
- **Comprehensibility:** CLEAN. The notes honestly qualify the raw consent/concentric (コンセント), "looking over" (採点) and "make retroactive" (遡る) glosses.

**Quiz exclusions:** No missing or excessive exclusion is established. The 15 exclusions for サークル are supported by JMdict's "group with a common interest" gloss. The consent-related exclusions for コンセント are supported by the consent homograph the article teaches. The 返す/返る exclusions for 逆さ and 逆さま rest on JMdict's ordinary "turn over / upside down" senses.

## Findings
**B30-C1**
- **Severity:** Minor
- **Facet:** correctness (naturalness)
- **Location:** `words\混合.md:19`
- **Claim and impact:** 空気はいくつかの気体の混合です presents 混合 as the word for a physical substance ("Air is a mixture of several gases"). For a substance, natural Japanese uses 混合物 or 混合気体. Learners may copy this marked pattern.
- **Remedy:** Write 空気はいくつかの気体の混合物です (…こんごうぶつです), or replace the sentence with an example about the act of mixing.
- **Evidence:**
  - JMdict 1290360 sense 1 glosses mixing/mixture/meld, so the English is supported.
  - Kotobank's Heibonsha 世界大百科事典 entry heads 混合 as "mixing; blending" (the operation). It links 混合物 separately for the mixture itself.
- **Confidence:** medium. This is not a native-speaker certification.

**B30-C2**
- **Severity:** Minor
- **Facet:** scoped coverage
- **Location:** `words\献立.md:21`; `docs\n2-vocabulary-sources.tsv:584`
- **Claim and impact:** The mapping selects sense 2 ("program, programme, schedule"), which covers two of the three raw glosses. The article only says the dictionary "also records a broader program or schedule sense" and gives no context, explanation or example. "Program" is ambiguous in English, so learners cannot recognize this use when they meet it.
- **Remedy:** Add one sentence explaining the non-meal arrangement/schedule use, with a sourced example and its reading.
- **Evidence:**
  - JMdict 1258500 sense 2 glosses program/programme/schedule.
  - The article's two examples are both about meals.
- **Confidence:** high that no usage is shown. The exact remedy wording is still unverified.

## Optional
- **混合:** Add an intransitive が example. Optionally recognize the 男女混合 ("mixed-sex") use.
- **逆さま:** Mention JMdict's rare 倒 spelling. In 逆.md, 逆さま could also be listed beside the さか reading row.
- **Borderline title overlaps worth watching, but not established ambiguity:**
  - 祭日 vs 祭/お祭り ("festival").
  - サイレン's "signaling sound" vs 合図 ("signal; cue").
  - こんばんは vs 晩 ("evening; night"), given that おはよう already excludes 朝 and 午前.

## Limits
- **Git and hashes:** I could not run Git or check hashes.
- **External sources:**
  - These Daijisen claims are the author's assertions, not checked by me:
    - コンセント's separate consent heading
    - 採点's "assigned score" sense
    - サイレン's mythological heading
    - the overlap between 祭日 and 祝日
  - My Weblio fetches returned only page chrome or the Wikipedia メニュー article, and one Kotobank lookup was irrelevant.
  - I did not check that the cited Weblio links resolve.
- **Evidence and testing:**
  - Some evidence sections were not read (see Scope).
  - No quiz simulation or build was run.
  - Naturalness judgments are my own as a reviewer, not native-speaker certification.
