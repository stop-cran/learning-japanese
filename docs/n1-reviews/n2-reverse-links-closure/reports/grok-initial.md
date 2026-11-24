Snapshot: 3cbc312e31506bb099b599c7025030f44e820c0e, based on 6e1e0342c91d9d6ba88fee577abd9e638dd645d3. Packet text only; no uncommitted tree checked.

Scope: Added primary on-reading cells, Common words bullets, four notes, and new JMdict ids on kanji/保.md, 案.md, 派.md, 結.md, 第.md, read against the nine linked word cards. Assigned facets: comprehensibility (phone clarity and concision) and scoped coverage. Reviewer: Grok 4.7 (grok-4.7). Correctness, quiz safety, and manifest consistency were not assigned.

Verdicts:
- 保: comprehensibility CLEAN; scoped coverage CLEAN; correctness UNVERIFIED
- 案: comprehensibility CLEAN; scoped coverage CLEAN; correctness UNVERIFIED
- 派: comprehensibility CLEAN; scoped coverage CLEAN; correctness UNVERIFIED
- 結: comprehensibility CLEAN; scoped coverage CLEAN; correctness UNVERIFIED
- 第: comprehensibility CLEAN; scoped coverage CLEAN; correctness UNVERIFIED

Findings: none.

All nine reverse links appear in both the primary on-row and Common words, with readings matching words.txt: 保健 ほけん, 保証 ほしょう, 案外 あんがい, 答案 とうあん, 立派 りっぱ, 結局 けっきょく, 結構 けっこう, 結論 けつろん, 落第 らくだい. New ids 1513410, 1603500, 1154820, 1449550, 1551790, 1254730, 1254760, 1255020, and 1548810 match those cards and jmdict.xml. Glosses match the word titles or a shorter first gloss. 保.md:44 correctly keeps ホウ off 保健 and 保証. 派.md:41 correctly explains ぱ and blocks a literal parse. 結.md:49 correctly separates けっこん, けっか, けっきょく, けっこう from けつろん without inventing ケ. 第.md:41 correctly says 落第 is not the ordinal prefix. Notes are one phone-length bullet each. Bullets, not the table cells, are the scannable form.

Optional:
- 結.md:30 is the longest new cell because it repeats the けっ/けつ rule already stated more clearly at 結.md:49. Nonblocking trim: end the cell at 結論 けつろん - conclusion. If the clause stays, it is accurate for the five words shown; it is not a general rule for unlisted 結 compounds.
- 案.md:44 still names only 案内 and 提案. Optional parity with 保.md:44: add 案外 and 答案. Not required: the row shows アン, and the same note already says practice selects アン.
- A 結構 "not literal" note like 派.md:41 is optional. The gloss is on the word, and words/結構.md already says not to derive "fine; sufficient" from the characters.

Limits: No device, native-speaker, or external-page check. Phone judgment is from text length only. README and content-format links were not opened. Full JMdict and the git tree were not opened. checks.txt was read, not re-run. Pre-existing prose, front matter, and word files were not re-reviewed except where an addition depended on them.
