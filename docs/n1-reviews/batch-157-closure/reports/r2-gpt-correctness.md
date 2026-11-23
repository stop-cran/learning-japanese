Snapshot: commit 77ff93d9 (77ff93d987782a9277a4e1355b1b0e9bbf6a6c00); reviewer model unavailable
Scope: All candidate files in snapshot\kanji\*.md, snapshot\words\*.md, and snapshot\strokes\*.json; all seven supplied diffs; candidate title inventories; mechanical-checks.md; review/content-format rules; pinned KANJIDIC2 and complete JMdict family/digest evidence; relevant repo link/title context and public dictionary entries. Correctness examined deepest.
Verdicts:
- correctness: CLEAN — all reviewed files.
- scoped coverage: NEEDS FIX — kanji\俊.md:34 and kanji\侯.md:34; CLEAN elsewhere.
- consistency and quiz safety: CLEAN — all reviewed files.
- comprehensibility: CLEAN — all reviewed files.
Findings:
1. Minor; scoped coverage; snapshot\kanji\俊.md:34 and snapshot\kanji\侯.md:34. The “Common words” lists present 俊英 and 王侯 as common supporting examples, but their pinned JMdict priority tags are only news2/spec2, which do not meet this batch’s stated support-word frequency criterion. This overstates their suitability as common examples. Remedy: qualify them as less-common/historical, or replace them with qualifying examples where available. Evidence: evidence\jmdict-digest.tsv entries 1340880 (俊英: news2, spec2) and 1588830 (王侯: news2, spec2); INSTRUCTIONS.md frequency rule. Confidence: high.
Optional: None.
Limits: The supplied mechanical report says N1 lint was not rerun on this revision; I did not run it. The repo export was used only for relevant links/titles and referenced context, not as a full-corpus linguistic review. No app/device acceptance was assessed.
