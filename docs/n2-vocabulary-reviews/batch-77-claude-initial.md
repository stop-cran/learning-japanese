I found no blocking defects. One article needs a fix: 包帯 (N2:1538) teaches 包帯する with a body-part を-object without any qualification. A committed mapping note also needs a spacing fix. The other 19 articles, the eight kanji patches, the component links and all ten reciprocal pairs check out.

## Snapshot
Frozen commit **d30143529a24516ba47ea82f15c0c3d66a1a98ad** (parent a1a8b73757e760d15d12a1af85511a49b0ac519b). This review covers committed content only. My file tools cannot run Git. That means I could not independently check the hash, that the working tree matches the commit, or that no older article changed. I rely on the frozen receipt (cleanCommittedContent: true; 20 new articles, 0 reused).

## Scope
- **Model:** claude-opus-5.5 (claude family). Reads were serial, with no edits or delegation.
- **Read in full:**
  - The three instruction files: `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md` lines 18–103.
  - All 20 assigned articles and all 8 kanji bodies, plus `related.patch`.
  - Mappings (lines 1–10 and 11–20), principals (1–10 and 11–20), components (1–17 and 18–34, all 34 records) and labels (1–90, 91–180, 181–268 EOF).
  - `public-bodies.txt` and `supplement-public-bodies.txt` (22 captures) and `supplement-comparison-reading.txt` (3 families, 6 senses).
  - The TSV header (line 1) and rows 1522–1541 only.
- **Partial read:** `review-evidence.json`, lines 1–60 only.
- **Families actually inspected:** 23 families / 34 senses (20 principal families / 28 senses, plus 3 supplemental families / 6 senses), not the 310-family union or the 497 prepared families.
- **Older bodies read in full:** only 小包, 対策 and 広々. Other quiz neighbors were judged from the 268 label records and from title searches in `words\`.
- **Not read:** family-inspection 01–11, old-body-inspection 01–17, related-kanji-inspection 01–02, `public-bodies.json` and `supplement-public-bodies.json`.
- **Other checks:** I confirmed which kanji cards and words exist with glob/grep inside `words\` and `kanji\` only.
- **Web:** kotobank 包帯 gave Daijisen plus the abridged Nihon Kokugo Daijiten. A wrong kotobank ID returned 保留, which is irrelevant. The Weblio 包帯 page was encyclopedia content and did not verify anything.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1522 | 別荘 | CLEAN | CLEAN | CLEAN | Holiday home is taught. JMdict sense 2 (prison, colloquial) is qualified as recognition only. |
| N2:1523 | 別々 | CLEAN | CLEAN | CLEAN | 別々に, 別々の/な and 別別 are covered. Line 40 wording is polish (see Optional). |
| N2:1524 | ベテラン | CLEAN | CLEAN | CLEAN | Matches Daijisen その道に熟達した人. Excluding 名人 and 博士 is sound. |
| N2:1525 | ヘリコプター | CLEAN | CLEAN | CLEAN | Daijisen confirms the short form ヘリ. ヘリコプタ is search-only and correctly not promoted. |
| N2:1526 | 編集 | CLEAN | CLEAN | CLEAN | Transitive use and the video sense are supported. Excluding 編む is sound. |
| N2:1527 | 便所 | CLEAN | CLEAN | CLEAN | べんじょ is correctly chosen over the historical びんしょ heading. The register note is hedged. |
| N2:1528 | ペンチ | CLEAN | CLEAN | CLEAN | 《pinchersから》 is supported. ニッパー and プライヤー stay plain text, which is correct because no cards exist. |
| N2:1529 | 望遠鏡 | CLEAN | CLEAN | CLEAN | 鏡 has no kanji card, so it is not linked. |
| N2:1530 | 方角 | CLEAN | CLEAN | CLEAN | The thought-direction and method senses match Daijisen senses 4–5. |
| N2:1531 | 箒 | CLEAN | CLEAN | CLEAN | Usually written in kana; 帚 is recognized. The historical ははき is not imported. |
| N2:1532 | 方言 | CLEAN | CLEAN | CLEAN | The social-group extension matches Daijisen sense 3. アクセント is distinguished. |
| N2:1533 | 坊さん | CLEAN | CLEAN | CLEAN | "Familiar and respectful" plus the boy sense match Daijisen. The boy-word exclusions are justified by that sense. |
| N2:1534 | 防止 | CLEAN | CLEAN | CLEAN | Transitive use matches 「非行を―する」. The チェック sense 4 caveat is supported. |
| N2:1535 | 方針 | CLEAN | CLEAN | CLEAN | Sense 2 (needle, the original meaning) is not taught as modern use. The 対策 pair is borderline (see Limits). |
| N2:1536 | 包装 | CLEAN | CLEAN | CLEAN | Wrapping, outer wrapper and packing are all covered. 小包's body separates the parcel from wrapping. |
| N2:1537 | 法則 | CLEAN | CLEAN | CLEAN | Both senses match Daijisen. 方則 is recognized. |
| N2:1538 | 包帯 | UNVERIFIED | NEEDS FIX | CLEAN | B77-01 |
| N2:1539 | 膨大 | CLEAN | CLEAN | CLEAN | The spelling restriction on the する sense is handled correctly. 広々 is borderline (see Limits). |
| N2:1540 | 包丁 | CLEAN | CLEAN | CLEAN | Raw 庖丁 is correctly mapped to 包丁 and 庖丁 is recognized. The mapping note has a separate issue (B77-02). |
| N2:1541 | 方程式 | CLEAN | CLEAN | CLEAN | The figurative sense matches Daijisen sense 2. The method-word exclusions are justified. |

- **Kanji and baseline preservation (8): CLEAN.** The patch only adds content, and front matter and unrelated passages are intact.
  - 編, 防, 針 and 則 gained links only; their entry IDs were already listed.
  - 角 gained 方角 with the ガク note and ID 1516950.
  - 包 gained 包装, 包帯 and 包丁 (with 庖丁) and IDs 1515510, 1603360 and 1515530.
  - 装 gained ID 1515510, and 帯 gained ID 1603360.
- **Component links: CLEAN.** Every existing card is linked. 荘, 鏡, 坊, 膨, 丁 and 箒 have no cards and correctly stay plain. Every primary written kanji appears in the `kanji:` metadata.
- **Reciprocal N2 links: CLEAN.** All ten required pairs are linked in both directions.
- **Mappings:** 19 are CLEAN. N2:1540 needs a fix for comprehensibility only (B77-02). Entries and selected senses match the TSV and JMdict.

## Findings
- **B77-01**
  - Severity: Low–Medium. Facet: correctness / scoped coverage.
  - Location: `words\包帯.md:8, 16, 35–37`.
  - Claim/impact: The article teaches 包帯する with the body part as the を-object (腕を包帯する) as an ordinary production pattern. It never teaches the everyday 〜に包帯をする.
  - Remedy: Add 〜に包帯をする (for example 頭に包帯をしている). Mark 包帯する as listed in JMdict but less common, or replace that pattern with 傷口に包帯を巻く.
  - Evidence: The Daijisen capture lists 包帯 as a noun only, with no (スル). The abridged Nihon Kokugo Daijiten on kotobank shows 〘名詞〙 only. Only JMdict gives n, vs, vt.
  - Confidence: Medium.
- **B77-02**
  - Severity: Low. Facet: mapping comprehensibility.
  - Location: `docs\n2-vocabulary-sources.tsv:1540` (identity_note).
  - Claim/impact: The note reads "share1515530 andほうちょう", which garbles the identity statement.
  - Remedy: Change it to "share entry 1515530 and reading ほうちょう". Optionally add the same spacing to "sense4" (line 1534) and "Sense2" (line 1535).
  - Evidence: Committed TSV row 1540.
  - Confidence: High.

## Optional
- 別々.md:40: rewrite as "Before a verb, use 別々に, not bare 別々."
- 防止.md:37: change to "after the noun naming the unwanted event."
- ペンチ.md:29–30: simplify the wording about 鋏. Optionally note that ペンチ is a Japanese-made loanword (wasei).
- 便所.md:37: optionally add that トイレ is the everyday default and 便所 can sound blunt.

## Limits
- Git verification was not possible. I relied on the receipt for the commit match and for no older article changing.
- Whether 腕を包帯する is natural is unresolved.
- JMdict entry 1118730 (ヘリ) was not inspected.
- The private `teachingSpelling: "庖丁"` field in the mapping derivative has unclear meaning. It is not in committed content.
- These borderline quiz pairs are not established as defects: 方針/対策, 膨大/広々, 包装/小包, 法則/支配 (which share only the English word "rule"), and the weak but harmless 防止 exclusions of ストップ and ブレーキ.
- Quiz judgments for most neighbors rest on titles and labels, not full bodies.
