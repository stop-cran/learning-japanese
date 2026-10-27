**Snapshot:** Corrected commit `f97be4e9b16d7aba1282551c4afe9610a21806f7`, whose parent is `1347683020fb124c01d8279169a855e60b33ab10`. I reviewed committed content only, through the current working-tree files, the correction receipt and the correction patch. I have no Git execution, so I could not confirm the commit identity, the clean tree or any hash myself; those are the author's assertions. The one hash cross-check I could make is that `docs\n2-vocabulary-snapshot.json:34` (`coverageIndexSha256` `865593f5…`) matches the TSV hash recorded in the receipt.

**Scope:** I am claude-opus-5.5, claude family, working alone with no edits. I read in full:
- My own initial report and the correction receipt.
- Patch lines 1–24 (the N2:552 row) and 1923–2140 (the snapshot, TSV and eight article diffs).
- All eight changed articles.
- Comparison articles 掛ける, 備える, マスター, 詳しい, 勘, 生物, 生き物, kanji 様, じりじり and 料理, plus the headers of 擦る, 焦げる, 掻く and コック.
- From the evidence derivative: the complete `correctionEvidence`, the N2:552 row, and these entry families:
  - all senses: 1006000, 1127970, 1175300, 1210590, 1244960, 1264980, 1351730, 1360920, 1378590, 1379430 and 1399970;
  - selected senses: 1207610 senses 1–2 and 10–12, and 1567390 senses 1–4.
- TSV rows N2:551 and N2:552.
- The relevant rules (content-structure lines 15–24 and earlier quiz rules).

I also independently re-fetched Daijisen 越す and the pinned N2 CSV.

This is not a second full review of the seventeen new cards. The other 19 mappings did not change in the diff, so I carried them over from my initial review.

**Verdicts:** Columns are correctness / scoped coverage / comprehensibility.

| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| ごくろうさま | CLEAN | CLEAN | CLEAN |
| ごちそうさま | CLEAN | CLEAN | CLEAN |
| 腰掛ける | CLEAN | CLEAN | CLEAN |
| こしらえる | CLEAN | CLEAN | CLEAN |
| 越す (batch-28 edits only) | CLEAN | CLEAN | CLEAN |
| 心得る | CLEAN | CLEAN | CLEAN |
| 心当たり | CLEAN | CLEAN | CLEAN |
| 個体 | CLEAN | CLEAN | CLEAN |
| N2:552 mapping | **NEEDS FIX** (source_note text only; the sense-4 selection is correct) | CLEAN | CLEAN |
| Evidence derivative / correctionEvidence | CLEAN | CLEAN | CLEAN |

On the evidence derivative: the corrected record matches TSV line 552, the original record is preserved, and the declaration count reconciles to 67 (63 plus 小遣い's 4).

All seven new exclusion pairs are justified and not excessive:
- **腰掛ける/掛ける:** JMdict 1207610:11 gives "to take a seat; to sit", which makes "sit down" a defensible answer in the 掛ける quiz.
- **こしらえる/備える:** both labels contain "prepare", supported by 1567390:3 and 1244960:2.
- **心得る/マスター:** "have a command of" sits next to "master a skill".
- **心得る/詳しい:** "know" sits next to "knowledgeable" (1351730:2).
- **心当たり/勘:** "inkling" sits next to "hunch".
- **個体/生物:** both labels contain "organism".
- **個体/生き物:** "creature" is close to "individual organism". This pair stands on its own, not by transitivity through 生物/生き物.

**Findings:**
- **B28-01 (こしらえる building claim): resolved.**
  - こしらえる.md:26 now teaches 家をこしらえる, which matches the house-building example in Daijisen ①.
  - The claim at line 54 and additional sense 1567390:2 are now supported.
- **B28-02 (N2:552 sense selection): resolved.**
  - TSV:552 now selects 1175300:4, which carries JMdict's note "often 超す".
  - Senses 1, 2, 3 and 5 are now additional 越す teaching. The N3 level and the article's identity are unchanged.
- **B28-03 (越す spelling prose): resolved.**
  - 越す.md:29 and 31–34 now give guidance that matches the Daijisen marks I fetched myself: ① (越す, including 難関を越す), ③ and ⑥㋐ are written 越す, and the quantity sense ② is unmarked.
  - The "tides or audience approval" sentence is gone.
- **Optional hypotheses:**
  - 備える, 生物, マスター/詳しい and 勘: adopted and resolved. The new comparison prose for each is accurate.
  - 焦げる/じりじり: withdrawn. 1006000:3 is "scorchingly (of the sun)", which does not share a charring sense.
  - コック/料理: withdrawn. One is a person, the other an activity or dish.
  - 擦る/掻く: withdrawn. 1399970 covers scratch, perspire and shovel, with no applicable overlap with rubbing.
  - 心得ました register and the こしらえる citation: no defect.
- **Adopted changes from the other family:** the 腰掛ける/掛ける pair and the two 様 links are correct. The links follow content-structure line 20 ("Link an existing card at the substantive introduction or comparison"), and the empty kanji arrays are correctly kept.
- **B28-C04 (new regression)**
  - Severity: Low. Facet: correctness (provenance).
  - Location: docs\n2-vocabulary-sources.tsv:552, `source_note` column. The same text is in the canonical batch-28.json N2:552 `sourceNote` (correction patch line 19).
  - Claim: the note says "Raw crossing, tide-over, passing-time and audience-related glosses retained."
  - Evidence: the pinned CSV row I fetched is `1175300,こす,超す,"to cross,to pass,to tide over"`, which has no audience-related gloss. The pre-correction note did not mention an audience gloss.
  - Impact: none on learners. It could mislead future reviewers about what the source row says.
  - Remedy: state "Raw 'to cross, to pass, to tide over' gloss retained unchanged."
  - Confidence: high.

**Optional:**
- Change コック's "tap valve" to "tap; valve".
- 越す.md:42 is unchanged from before batch 28. Its "the source list's audience-related gloss" sentence could say which list it means, since the N2 row has no such gloss.
- Link the 越す mentions in kanji\越.md (outside the batch).

**Limits:**
- No Git or hash execution; the receipt hashes and the clean-tree status are taken on trust.
- From the canonical patch's appended evidence (lines 25–1922), I saw only lines surfaced by a targeted search (1687–1717 and 1864, all adjudication or record text). I read no quiz rationale.
- 1207610 senses 3–9 and 13 onward, 1379440 and 1554310 were not read in the derivative.
- I did not re-fetch Daijisen 拵える or 腰掛ける in this phase; I rely on my initial-phase fetch and JMdict.
- The こちらこそ public lookup failure remains a limit.
- No app draws were run; there is no native-speaker or corpus certification, and the source is a community list, not an official JLPT syllabus.
