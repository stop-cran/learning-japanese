# Initial correctness and scoped-coverage review

**Snapshot:** `bac3477e5323fad11c54e2f2bd424cd5c3693096`, based on
`e824da99c8a19479bfede4e6fbe88b1f21a4180b`. The committed candidate was reviewed read-only.

**Scope:** All nine new word articles were checked for readings, senses and source claims against
`batch-161-jmdict.xml`; cited JMdict entry IDs in those articles and the 囚, 圏, 坑, 坪, 培, 堀,
堕, 堤 and 堪 kanji cards were checked. Condensed readings tables, common words and notes of those
nine cards were read, but not their full bodies. The 嚇 card was checked only at its header. Reused
article diffs, manifest, stroke files, progress JSON and Digital Daijisen/Kotobank pages were not
reviewed. 人/内/威/落/道/防/養, 低下, 教養 and 待ち合わせる were not viewed.

**Verdicts**

- Correctness: CLEAN.
- Scoped coverage: NEEDS FIX (two Low items).
- Comprehensibility: UNVERIFIED (not assigned).

**Findings**

1. **Low, coverage — `words/たえる.md`:** The article named hardship endurance and a “fit or
   worthy” sense, but illustrated only 高温に堪える. JMdict 1211310 includes bearing/withstanding
   senses and a “be fit for / be equal to” sense. Add a hardship example and an example of the worthy
   construction, each with a gloss.
   **Evidence:** Only one example appeared; the worthy sense was asserted but not demonstrated.
   **Confidence:** Medium.
2. **Low, coverage — `words/坪.md`:** The only example, 坪は面積の単位です, defined the unit but
   did not show it with a quantity. Add a numeral-plus-坪 example.
   **Evidence:** JMdict 1433840 defines the traditional land-area unit; the example contained no
   number.
   **Confidence:** Medium-low.

**Optional:** The article could note that 耐える is more often written for the たえる sense than
堪える. This was not established with frequency evidence in the review.

**Limits:** Claims outside the JMdict snapshot, including the legal-history and reading-history
claims in 囚人, were not checked. Reused-article edits, the 嚇 card body, quiz fields and independent
naturalness were outside scope.
