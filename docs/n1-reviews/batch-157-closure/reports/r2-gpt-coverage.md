Snapshot: 77ff93d987782a9277a4e1355b1b0e9bbf6a6c00; reviewer model not exposed
Scope: All 17 snapshot kanji cards, all 10 word cards, all 10 new stroke files, and seven modified-card diffs; checked pinned KANJIDIC2/source metadata, JMdict frequency rows and relevant full entries, titles, links, quiz exclusions, format/rubric, and relevant public dictionary entries. Scoped coverage was the deepest facet.
Verdicts:
- Correctness: CLEAN — reviewed snapshot files; front matter/readings match pinned metadata, and checked word senses, register, examples, and comparisons are supported.
- Scoped coverage: NEEDS FIX — kanji/俊.md and kanji/倫.md (findings 1–2).
- Consistency and quiz safety: CLEAN — reviewed snapshot files; titles, required kanji links, reading examples, and declared exclusions are coherent.
- Comprehensibility: CLEAN — reviewed snapshot files; explanations are concise and learner-facing.
Findings:
1. Minor; scoped coverage; snapshot/kanji/俊.md:31–34. 俊英 is listed under “Common words,” but pinned JMdict entry 1340880 has only news2/spec2 (nf37), which does not meet the packet’s support-word frequency rule. This overstates the word’s frequency for N1 study. Remedy: remove it from this list or label it explicitly as a less-common/specialized example. Evidence: evidence/jmdict-digest.tsv:272 and the full entry in evidence/jmdict-families.xml; Weblio/Digital Daijisen confirms the word’s talent/excellence sense. Confidence: high.
2. Minor; scoped coverage; snapshot/kanji/倫.md:31–37. The common-word coverage presents 倫理 alone, but the pinned family also contains 不倫 (news1 nf18), a frequent, distinct everyday use meaning impropriety/affair. This leaves an important common use of 倫 absent from an N1 card whose listed usage otherwise centers on ethics. Remedy: add 不倫 as a plain-text example with a concise sense/register qualification, or explain the deliberate scope. Evidence: evidence/jmdict-digest.tsv:480 and entry 1495370 in evidence/jmdict-families.xml; Weblio/Digital Daijisen’s 不倫 entry confirms the sense. Confidence: high.
Optional: None.
Limits: JMdict priority tags are corpus indicators, not a universal learner-frequency scale. Public dictionary checks were selective; no native-phone rendering or runtime quiz test was performed. Pinned dictionary inputs may differ from current online editions.
