# Batch 53 independent review: N2:1042–N2:1061 (claude-opus-5.5)

Four low-severity defects found. Three are missing quiz exclusions (チップ/端, 地帯/ベルト, 着々/徐々に) and one is an unlinked word (酸性 in 中性). Everything else is clean within what I read, including the two kanji edits, the unchanged 超 card and the twenty mappings.

## Snapshot
- Frozen commit: **d67609747e671278f9a6a4e973ea0a0832a8cad8**. Parent: 6f5e4cdeb1de5be236364fde7ed1b3e6e95453a1. `cleanCommittedContent: true`.
- I reviewed committed content only. My file tools cannot run Git, so I could not confirm that the working tree matches the commit. I took that equality on the snapshot's word.

## Scope
**Model:** claude-opus-5.5 (Claude family). Read-only; no edits, agents or delegation.

**Read completely:**
- All 18 new articles.
- Both reused cards: words\ちゃわん.md and words\超過.md.
- kanji\帯.md, kanji\象.md and kanji\超.md.
- From the private batch-53 files: frozen-snapshot.json, related.patch, review-mappings/components/principals/labels.jsonl, principal-reading.txt, all twelve family-inspection files (01–12, read with forceReadLargeFiles) and supplemental-comparison-reading.txt.
- .github\copilot-instructions.md, .github\instructions\content-structure.instructions.md and docs\content-format.md:18-126.

**Read partially:** review-evidence.json, lines 1–80 only.

**Other checks:**
- **Comparison cards:** I checked existing words\ cards mainly by title and quiz_exclusions, using globs and greps. The only comparison body I read in full was words\ベルト.md.
- **Link targets:** every word link target I checked exists. The kanji with no card (縮, 旬, 抽, 彫, 碗) are correctly left as plain text.
- **Web:** one fresh retrieval, the Jisho API entry for ベルト (JMdict-derived, version not pinned). The Jisho HTML page returned nothing usable.

**Not read:**
- public-bodies.json and public-bodies.txt.
- The rest of review-evidence.json.
- docs\n2-vocabulary-snapshot.json, docs\n2-vocabulary-sources.tsv and docs\n2-source-snapshot.json. My mapping checks therefore rest on the blind JSONL copy, not the repository TSV.
- docs\confusable-words.md and docs\jlpt-levels.md.
- All forbidden ledgers and batch-53.json.

## Verdicts
Correctness covers claims and metadata. Scoped coverage covers required senses, links and exclusions. Comprehensibility covers how clearly the article teaches.

| ID | Article | Status | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1042 | 知人 | new | CLEAN | CLEAN | CLEAN |
| N2:1043 | 地帯 | new | CLEAN | NEEDS FIX (B53-C-02) | CLEAN |
| N2:1044 | 縮む | new | CLEAN | CLEAN | CLEAN |
| N2:1045 | 縮める | new | CLEAN | CLEAN | CLEAN |
| N2:1046 | 縮れる | new | CLEAN | CLEAN | CLEAN |
| N2:1047 | チップ | new | CLEAN | NEEDS FIX (B53-C-01) | CLEAN |
| N2:1048 | 地点 | new | CLEAN | CLEAN | CLEAN |
| N2:1049 | 地名 | new | CLEAN | CLEAN | CLEAN |
| N2:1050 | 茶色い | new | CLEAN | CLEAN | CLEAN |
| N2:1051 | 着々 | new | CLEAN | NEEDS FIX (B53-C-03) | CLEAN |
| N2:1052 | ちゃわん (source 茶碗) | reused N5 | CLEAN | CLEAN | CLEAN |
| N2:1053 | 中間 | new | CLEAN | CLEAN | CLEAN |
| N2:1054 | 中旬 | new | CLEAN | CLEAN | CLEAN |
| N2:1055 | 抽象 | new | CLEAN | CLEAN | CLEAN |
| N2:1056 | 中世 | new | CLEAN | CLEAN | CLEAN |
| N2:1057 | 中性 | new | CLEAN | NEEDS FIX (B53-C-04) | CLEAN |
| N2:1058 | 中途 | new | CLEAN | CLEAN | CLEAN |
| N2:1059 | 中年 | new | CLEAN | CLEAN | CLEAN |
| N2:1060 | 超過 | reused; N2/provenance edit only | CLEAN | CLEAN | CLEAN |
| N2:1061 | 彫刻 | new | CLEAN | CLEAN | CLEAN |

**Kanji and mapping checks:**
- **帯 edit: CLEAN.** 地帯 ちたい is in the タイ row at line 28 and in Common words at line 39. Entry 1421360 is added to the line-46 metadata.
- **象 edit: CLEAN.** 抽象 ちゅうしょう is in the ショウ row at line 30 and in Common words at line 39. Entry 1426190 is added at line 46.
- **超 (unchanged): CLEAN.** 超過 ちょうか already appears at line 28 (チョウ row) and line 34 (Common words), and entry 1429410 is at line 43. related.patch has no hunk for 超.
- **Baseline metadata: CLEAN.** The kanji, title, jlpt, tags and strokes of all three cards are unchanged; the patch touches only the rows, Common words and the entry list.
- **ちゃわん: CLEAN.** It keeps jlpt 5 and `kanji: []`, and teaches 茶碗/茶わん as "rice bowl" and tea bowl.
- **超過: CLEAN.** The patch changes only line 5 (`jlpt: 2`) and the provenance line at line 42. The original body and exclusions are retained.
- **Readings:** All three reciprocal pairs use actual whole-word readings. No individual character readings were invented.
- **New-word kanji metadata: CLEAN.** Every written Han character is listed, including the cardless 縮, 旬, 抽 and 彫.
- **Mappings: CLEAN, checked against the blind derivative.**
  - The cited sense numbers match the complete inspected families: 1077740 senses 1–3 (tip) and 2850287 senses 1, 2 and 4 (chip), with the chip family attributed separately.
  - The other entries also match: 1425030/1425050/2059610 for 中途, 1424710 senses 1–3 for 中性, and 1337570 senses 1–3 for 縮める.
  - No invented pinned sense numbers for additional uses.

## Findings
- **B53-C-01 — Low — quiz exclusions — words\チップ.md:9 (and :48-50, :52)**
  - **Problem:** 端 is missing from the exclusions. Its title "edge; end; tip" (words\端.md:4) is a reasonable answer for チップ, which teaches the ballpoint-pen "tip" sense (1077740 sense 3).
  - **Inconsistency:** The card already excludes 先端 ("tip; leading edge") and 先. 端 excludes only [縁, 先].
  - **Rule:** content-format.md:95-99.
  - **Remedy:** Add 端 to チップ's quiz_exclusions.
  - **Confidence:** medium.
- **B53-C-02 — Low — quiz exclusions — words\地帯.md:9**
  - **Problem:** ベルト is missing from the exclusions. The 地帯 title is "area; zone; belt" (:4) and the ベルト title is "belt" (words\ベルト.md:4). ベルト excludes only [帯].
  - **Evidence:** JMdict ベルト sense 3 is "belt, zone, area" (fresh Jisho API retrieval). 地帯.md:40 itself warns that its English "belt" is geographical. Either title is therefore a defensible answer.
  - **Remedy:** Add ベルト to 地帯's quiz_exclusions.
  - **Confidence:** medium.
- **B53-C-03 — Low — quiz exclusions — words\着々.md:9**
  - **Problem:** 徐々に ("gradually; by degrees", which excludes only [だんだん]) is missing.
  - **Inconsistency:** だんだん ("gradually") is already excluded and compared at :37. "Step by step" and "by degrees" overlap, and the inspected JMdict entry 1345600 for 徐々 includes "steady".
  - **Remedy:** Add 徐々に to 着々's quiz_exclusions.
  - **Confidence:** medium.
- **B53-C-04 — Low — links — words\中性.md:36**
  - **Problem:** 酸性 (さんせい) is plain text, but words\酸性.md exists ("acidity; acidic"). The same section links 男性 and 女性 at :38.
  - **Remedy:** Change it to `[酸性](酸性.md)`.
  - **Confidence:** high that the card exists; medium that a link is required.

## Optional
- **抽象.md:20:** The する example is academic; a brief register note would help.
- **中性.md:44:** Sense 2 (sexlessness/androgyny) has no example, for instance with 中性的.
- **地点.md:20:** 集合地点 would read more naturally than 集合する地点.
- **縮れる:** Could name a Japanese term for straight hair as a contrast.
- **中世:** Could mention 古代 and 近世.
- **超過.md:42:** The provenance sentence is learner-facing meta-text; consider rewording it.

## Limits
- Most comparison-card bodies were checked only by title and exclusions. I did not systematically search for missing exclusions beyond title greps.
- Mapping rows were checked against the blind JSONL, not the repository TSV or the docs snapshots.
- I did not read public-bodies, so claims based on the public dictionary (for example 茶色い's "broader brown" sentence) are UNVERIFIED by me.
- The author's public captures came from a single service. The failed 賭け札 and 雕刻 extractions verify nothing.
- My only fresh retrieval was Jisho's ベルト entry, which is not version-pinned.
- I did not judge whether learner-facing provenance lines are an accepted convention.
- Example naturalness is a non-native assessment, not a native-speaker certification.
