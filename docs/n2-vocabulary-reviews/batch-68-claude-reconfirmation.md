## Snapshot
I found no actionable defects in this followup. Both findings I raised last turn (B68-OPUS-06 and -07) are resolved. All three additional guards are justified, the attribution change is accurate and I found no regressions.

- New commit: **bb580c4a64a2cf52149e524b1d6e8674a4230591**
- Parent: **2776efdbf960a682f258bc60141d0983c1727612**
- Committed content only, taken from followup-snapshot.json (`cleanCommittedContent: true`). It lists four changed content and mapping files: `words\ばつ.md`, `words\甚だしい.md`, `words\バック.md` and `docs\n2-vocabulary-sources.tsv`.
- File tools can't run Git, hash or cleanliness checks, and I did not inspect `.git`. The author's hashes and coverage-index checksum are unverified.

## Scope
**Model:** claude-opus-5.5 (family claude). Read-only; no edits, agents or delegation.

**Fresh complete reads this turn:**
- followup-snapshot.json and the complete followup.patch.
- followup-mappings.jsonl (20 records), review-principals.jsonl (20 complete families) and review-components.jsonl (31 records).
- followup-families.txt: 12 families, 27 senses — 1098760, 1099100, 1226960, 1240180, 1370010, 1429410, 1484930, 1956100, 2029650, 2252690, 2436470 and 2814060.
- followup-old-bodies.txt: 非常に, 極, ド, 超過 and 逆. I also read `words\超過.md` directly; it matches the chunk.
- `words\ばつ.md`, `words\甚だしい.md`, `words\バック.md`.
- `docs\n2-vocabulary-sources.tsv`: line 1 and lines 1342–1361 only.
- Title and exclusion lines of 逆さ and 逆さま, plus a filename glob showing each new guard target exists as an article file.
- My own live fetches, with no saved hash: Weblio Daijisen ばつ (`dictCode=SGKDJ`) and Kotobank ばつ-602173.

**Inherited from my complete reads at 2776efdb, not reread now:**
- 17 word articles: 肌着, 果たして, 鉢, 発揮, 発射, 発想, 発電, 発売, 派手, 話し合い, 話しかける, 話し中, 花火, 花嫁, 放れる, 羽, ばね.
- The four kanji cards: 肌, 羽, 根, 放.
- Full `words\着る.md` and the six corrective chunks.
- That these are unchanged rests on the patch and the snapshot's changed-file list, not on Git.
- From the initial review: the mixed-reading convention and the 鉢多羅 assessment.

**Not read:** followup-completed-evidence.json (allowlisted but not required), the large master derivative, and the earlier chunks (no longer allowlisted).

**Corrections to my previous report:**
- I gave the earlier older-body chunk split as 7+7+7; the author says 7+8+6. I can't recheck it now, but the 21-article total is unaffected.
- My Scope contained a garbled line about "着.る"; the file actually read was `words\着る.md`.

## Verdicts
"Inherited" means a complete read at 2776efdb, unchanged since. For every row, the TSV row, mapping record and principal family were reread fresh this turn.

| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1342 | words\肌着.md | Inherited body; 1476500 fresh | CLEAN | CLEAN | CLEAN |
| N2:1343 | words\果たして.md | Inherited body; 1600780 fresh | CLEAN | CLEAN | CLEAN |
| N2:1344 | words\鉢.md | Inherited body; 1477090 fresh | CLEAN | CLEAN | CLEAN |
| N2:1345 | words\ばつ.md | Fresh full reread; patch; 2197150; Daijisen and Seisenban fetched | CLEAN | CLEAN | CLEAN |
| N2:1346 | words\発揮.md | Inherited body; 1477250 fresh | CLEAN | CLEAN | CLEAN |
| N2:1347 | words\バック.md | Fresh full reread; patch; 1098760, 1099100, 1226960, 2814060; 逆 body | CLEAN | CLEAN | CLEAN |
| N2:1348 | words\発射.md | Inherited body; 1477490 fresh | CLEAN | CLEAN | CLEAN |
| N2:1349 | words\発想.md | Inherited body; 1477660 fresh | CLEAN | CLEAN | CLEAN |
| N2:1350 | words\発電.md | Inherited body; 1477750 fresh | CLEAN | CLEAN | CLEAN |
| N2:1351 | words\発売.md | Inherited body; 1477810 fresh | CLEAN | CLEAN | CLEAN |
| N2:1352 | words\派手.md | Inherited body; 1471140 fresh | CLEAN | CLEAN | CLEAN |
| N2:1353 | words\話し合い.md | Inherited body; 1600910 fresh | CLEAN | CLEAN | CLEAN |
| N2:1354 | words\話しかける.md | Inherited body; 1562300 fresh | CLEAN | CLEAN | CLEAN |
| N2:1355 | words\話し中.md | Inherited body; 1600920 fresh | CLEAN | CLEAN | CLEAN |
| N2:1356 | words\甚だしい.md | Fresh full reread; patch; 1370010, 1484930, 1240180, 2252690, 1429410; four comparison bodies | CLEAN | CLEAN | CLEAN |
| N2:1357 | words\花火.md | Inherited body; 1194580 fresh | CLEAN | CLEAN | CLEAN |
| N2:1358 | words\花嫁.md | Inherited body; 1194570 fresh | CLEAN | CLEAN | CLEAN |
| N2:1359 | words\放れる.md | Inherited body; 1516540 fresh | CLEAN | CLEAN | CLEAN |
| N2:1360 | words\羽.md | Inherited body; 1171680 fresh | CLEAN | CLEAN | CLEAN |
| N2:1361 | words\ばね.md | Inherited body; 1099490 fresh | CLEAN | CLEAN | CLEAN |

**Edited kanji cards (inherited; not touched by the followup): CLEAN.** 肌, 羽, 根 and 放 keep their headers, and 放 remains N3.

**Primary/alias reciprocal pairs: CLEAN.** The pairs are inherited; the component readings were reconfirmed this turn in KANJIDIC: 肌 はだ, 羽 はね, 根 ね, 放 はな.れる.
- 肌 ↔ 肌着 はだぎ, footer 1476500.
- 羽 ↔ 羽 はね and 根 ↔ 羽根 はね, both pointing to stable `words\羽.md`, footer 1171680.
- 放 ↔ 放れる はなれる, footer 1516540.

**Baseline preservation: CLEAN.** The followup touches no baseline article, exclusion or kanji card. 花火 still gains only `jlpt: 2`, and 羽 keeps N3 (inherited). The N2:1360 mapping still has article level 3, `teachingSpelling: 羽根`, selected senses 4–5 and additional senses 1–2; sense 5 is restricted to the 羽根 spelling.

**Mappings: all 20 CLEAN.** The TSV rows and mapping records match field for field: IDs, raw forms, blank fields, glosses, entries, paths, levels, and selected and additional senses. Raw 果して, 話合い, 話し掛ける, 話中, ｘ and 羽根 all appear as spellings in their families.

## Findings
**B68-OPUS-06 (stale N2:1345 note): RESOLVED.**
- `docs\n2-vocabulary-sources.tsv:1345` and the new mappings record now both say "Provisionally grouped as kango following the tentative 罰点 connection; tagged etymology-uncertain. This is not a verified etymology or settled historical type."
- The diff changes only that field.

**B68-OPUS-07 (甚だしい guards): RESOLVED.**
- `words\甚だしい.md:9` now includes 非常に and 極.
- 非常に: its title "extremely" (1484930:1 very / extremely / exceedingly) competes with "extreme; excessive", especially since the article teaches the adverb 甚だしく.
- 極: one precision point. JMdict 1240180:1 glosses only "quite; very", and the 極 article shows ごく can intensify smallness (ごく少し). The guard is therefore justified by 極's displayed title "very; extremely", which meets the test at content-format.md:95, rather than by deep semantic overlap.
- The guard targets only the stable 極 (ごく). 極 (きょく, 1956100) and はたて (2436470) are correctly not carried over.

**甚だしい/ド: concur.** ド's title "extreme; very; emphatic prefix" shares the leading gloss "extreme" (2252690:1 extreme / ultra / very much). "Emphatic prefix" only partly disambiguates, and the guard costs little. The musical ド (2029650) is not involved.

**甚だしい/超過: concur.** "Excess; exceeding a limit" (1429410:1) and "excessive" compete in both quiz directions. Adjective versus noun is not an exemption. The edge is justified on its own, not inferred through 過剰.

**バック/逆: concur, on the reversed-direction facet specifically.**
- バック's title contains "reverse movement" (1098760:4 going backwards / reversing; :5 reverse gear). 逆 is "reverse; opposite" (1226960:1), and its article teaches 逆の方向, "opposite direction".
- Either title could be accepted for either word, so this is more than token overlap.
- The guard doesn't equate the two: 逆's own body still says 逆に is "not literal backward movement". さか (2814060) is not this identity.

**Source attribution: accurate.**
- `words\ばつ.md:18`, "JMdict also records fullwidth ｘ", matches the ｘ spelling in 2197150.
- My own fetches this turn show Daijisen's cross-mark heading 《「罰点(ばってん)」からか》 and Seisenban's 「ばってん（罰点）」からできた語か. Both hedge, which verifies line 25's plural "dictionaries tentatively connect".
- Daijisen's 「―をつける」 supports the article's example sentence.
- Kotobank's Daijisen ばつ headings are the unrelated circumstances, vatu and Batu entries and were not conflated.

**B68-OPUS-01 to -05: still resolved.** I reconfirmed 01, 02 and 05 in fresh rereads; 03 (ばね/春) and 04 (話し中/忙しい) are inherited.

**Regressions:** none. Each new exclusion target exists as an article file, and no exclusion list contains a duplicate or self-reference. No title, reading, level, kanji or teaching prose changed beyond the ばつ attribution wording.

**New actionable defects:** none.

## Optional
- バック/逆さ ("upside down; reversed") is not established as a competitor: "upside down" and inversion differ from moving backwards.
- 話し中/会話 is still not established.
- Still deferred without objection: the Xも甚だしい pattern, 羽's N3 counter-provenance wording and a hanetsuki gloss, and a 話し合う note. A ばね/泉 guard remains unnecessary.

## Limits
- **ばつ's historical origin and word type are unverified.** Both dictionaries hedge, and kango is accepted only as explicitly qualified provisional teaching.
- **Freshness:** only three articles, the TSV rows, the compact files and the two followup chunks were read fresh. Seventeen word articles and four kanji cards are inherited from my reads at 2776efdb. That they are unchanged relies on the author's patch and changed-file list.
- **No reviewer Git, hash or cleanliness certification.** I did not read followup-completed-evidence.json or the coverage index.
- **Public evidence:** the frozen captures come from one authority, Digital Daijisen via Weblio. My live Weblio and Kotobank fetches (2026-10-25) have no saved hash and may differ from the frozen captures.
- **Quiz checks:** judgments rest on titles plus the bodies actually read, with no live quiz draws. This is not an exhaustive synonym audit, and there is no native-speaker or frequency certification.
- The inherited batch-61 quiz debt remains deferred.
