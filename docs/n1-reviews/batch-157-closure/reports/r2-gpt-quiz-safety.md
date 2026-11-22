Snapshot: commit 77ff93d987782a9277a4e1355b1b0e9bbf6a6c00; reviewer model not exposed
Scope: All 17 snapshot kanji cards, 10 word articles, 10 stroke JSON files, and seven diffs; checked pinned KANJIDIC2/JMdict evidence, title index, links, relevant repo articles, content format, and confusable-word guidance. Deepest facet: consistency and quiz safety.
Verdicts:
- Correctness: CLEAN
- Scoped coverage: NEEDS FIX
- Consistency and quiz safety: NEEDS FIX
- Comprehensibility: CLEAN
Findings:
1. Minor; consistency and quiz safety; snapshot/kanji/佐.md:14,23. The card says 佐 means “assistant or help,” but 助 (existing title “help; rescue”) is absent from quiz_exclusions. Because “help” is explicitly valid for 佐, 助 can be a defensible meaning-quiz answer, not a safely wrong distractor. Add 助 to the exclusions. Evidence: source-metadata.json gives 佐 meanings “assistant” and “help”; the card's line 23 repeats this; titles/kanji-titles.tsv gives 助 the title “help; rescue.” Confidence: high.
2. Minor; scoped coverage; snapshot/kanji/侯.md:34 and snapshot/kanji/俊.md:34. 王侯 and 俊英 are listed under “Common words,” but their pinned JMdict entries (1588830 and 1340880) carry only news2/spec2 priority tags; the packet's frequency rule explicitly says those tags alone do not qualify. This overstates their support as frequency-qualified common examples, especially for 侯, whose listed 諸侯 is untagged. Relabel these as lower-frequency/related terms or omit them from the common-word list; do not count them toward the frequency criterion. Evidence: evidence/jmdict-digest.tsv, rows for 侯/1588830 and 俊/1340880; the stated support-word frequency rule. Confidence: high on tag status; medium on editorial classification.
Optional: None.
Limits: Reviewed original example sentences for grammar and naturalness, not corpus frequency. Independently fetched the live Weblio Digital Daijisen entry for 侮る; other consequential lexical checks used the packet's pinned JMdict/KANJIDIC2 evidence and supplied public-dictionary extracts. Live dictionaries may differ from the pinned snapshots.
