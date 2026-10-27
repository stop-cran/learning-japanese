## Snapshot
- Frozen commit: **84a79c01fe6b2b669652802823ca0fc09c25fe98** (parent de119b3a59865e9470227deff7505a54a0ef63a3). I reviewed committed content only.
- I had file tools only and could not run Git or compute hashes. So the commit identity, the clean-tree flag, file hashes and the evidence-packet hash (47734229…) are what the author recorded, not things I checked.

## Scope
- **Model:** claude-opus-5.5 (claude family), working alone and read-only. No agents, no edits.
- **Read in full:**
  - all nineteen new articles;
  - the whole body of 越える.md, checked only for 超える/こえる senses 1–2 and its three added lines (not a new review of the whole card);
  - the six-file related patch and the five kanji files;
  - TSV rows N2:522–541;
  - the required guides (copilot-instructions, content-structure, content-format.md:18–119).
- **Read from the evidence packet:** all principal entry families, the component records, the Daijisen inspection receipts, the quiz declarations and the existing comparison labels. Also the もみじ (2857870), 黄葉 (2857872) and 合理的 (1285380) entries.
- **Also checked:** the existing cards 務め, 勤め, 義務 and 公立, plus a keyword search of titles under words\.
- **Not done:**
  - comparisonEntryFamilies (packet lines 2616–22503) was searched, not read through;
  - no forbidden files were opened;
  - no native-speaker or corpus check of example sentences.

## Verdicts

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 高度 | CLEAN | CLEAN | CLEAN |
| 高等 | CLEAN | CLEAN | CLEAN |
| 合同 | CLEAN | NEEDS FIX | NEEDS FIX |
| 後輩 | CLEAN | CLEAN | CLEAN |
| 公表 | CLEAN | CLEAN | CLEAN |
| 鉱物 | CLEAN | CLEAN | CLEAN |
| 公務 | NEEDS FIX (quiz exclusions) | CLEAN | CLEAN |
| 項目 | CLEAN | CLEAN | CLEAN |
| 紅葉 | CLEAN | CLEAN | CLEAN |
| 合理 | CLEAN | CLEAN | CLEAN |
| 交流 | CLEAN | CLEAN | CLEAN |
| 合流 | CLEAN | CLEAN | CLEAN |
| 効力 | CLEAN | CLEAN | CLEAN |
| コース | CLEAN | CLEAN | CLEAN |
| コーラス | CLEAN | CLEAN | CLEAN |
| 焦がす | CLEAN | CLEAN | CLEAN |
| 国王 | CLEAN | CLEAN | CLEAN |
| 国籍 | CLEAN | CLEAN | CLEAN |
| 国立 | CLEAN | CLEAN | CLEAN |

- **Reused 越える (N2:535):** CLEAN on all three facets.
  - Both spellings are in JMdict 1593070, and the reading こえる has no spelling restriction.
  - The body already teaches 超える ("exceed") with an example. The three added lines link 超 accurately.
  - Title, `[越]` metadata, exclusions and the easier jlpt 3 level are unchanged.
- **Kanji edits:** all five CLEAN on all three facets.
  - 鉱 adds 鉱物; 紅 adds 紅葉/こうよう; 効 adds 効力 (each with its footer entry ID).
  - 籍 links its existing 国籍 example.
  - 超 links both 超える examples to 越える.md at the reading こえる.
  - The missing kanji cards 輩, 項 and 焦 appear as unlinked metadata, which is correct.
- **Mappings N2:522–541:** all twenty CLEAN on all three facets.
  - In N2:530 (紅葉), the source's "(Japanese) maple" gloss doesn't match the こうよう entry. The article documents this and teaches maple under もみじ (2857870, sense 1), which matches the entry data.
  - The 交流 "intercourse" gloss and the 鉱物 rare form 礦物 are handled with proper qualifications.

## Findings

**B27-01 — Minor — 合同: unclear wording and the merger use is never plainly taught (comprehensibility, scoped coverage)**
- **Where:** words\合同.md:16–22 and 44–49.
- **Problem:** The mapped sense 1 includes "incorporation; amalgamation; merger; fusion". The only place the article teaches this is lines 45–46: "the source's incorporation or merger glosses are not restricted to merely cooperating while staying separate." That sentence is a double negative and refers to "source glosses" the learner never sees. Both examples show cooperation (合同で, 合同して大会を開く), never a merger.
- **Impact:** A learner may read 合同 only as "joint" and miss the merging meaning.
- **Fix:** Replace lines 45–46 with a plain statement, such as "合同 can also mean merging into one body," and add a merger example (e.g., 二つの政党が合同して新党を作った).
- **Evidence:** packet entry 1285140, sense 1 glosses.
- **Confidence:** medium-high.

**B27-02 — Minor — 公務: two plausible "duty" distractors are not excluded (correctness, quiz)**
- **Where:** words\公務.md:9.
- **Problem:**
  - The card excludes 仕事 "work; job" as a broader overlap.
  - But it does not exclude 務め "duty; responsibility" (words\務め.md:4) or 勤め "work; duty; religious service" (words\勤め.md:4), which overlap even more directly with "official public duties".
  - Neither of those cards excludes 公務.
- **Impact:** The content-format rule (docs\content-format.md:95) calls for an exclusion when a learner could reasonably accept either title as the answer for either word. Both cards meet that test, so a learner who picks "duty" for 公務 would be marked wrong.
- **Fix:** Add 務め and 勤め to 公務's quiz_exclusions. 義務 "duty; obligation" is a borderline case.
- **Confidence:** medium.

## Optional
- The 高度/高等 exclusions of 良い, いい, 偉い and 立派 (and 優秀/優れる on 高度) are weakly supported by the meanings. The same goes for コース excluding 選択 and 予定.
- The 国立 title "nationally established institution" reads like a noun naming an institution. The body clarifies it, and it mirrors 公立's existing title "public institution".
- "An 項目" (項目.md:42, 44): the repo is inconsistent about "a"/"an" before Japanese words, so this is style, not a defect.
- Some example phrasing could be more natural (both unverified):
  - 合理を重んじる → 合理性を重んじる
  - 効力を持ちます → 効力を生じる
- A もみじ autumn-leaves example could be added to 紅葉.
- Borderline title overlaps: 国籍 vs 市民 "citizen…"; 合理 vs 訳 "reason; sense".
- 越える.md mentions 越す without linking it (this predates the batch).

## Limits
- The Daijisen receipts and the packet's equivalence to the source are the author's claims.
- The Weblio and goo lookups for 合同 did not return the Daijisen text: the Weblio page loaded without it, and goo failed with a DNS error.
- The title-collision search was keyword-based, so it may have missed overlapping titles.
- Example naturalness and register have not been checked against a corpus or by a native speaker.
