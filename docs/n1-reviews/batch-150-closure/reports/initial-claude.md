# Batch 150: initial blind review (reviewer 1)

Reviewer model: Claude (Anthropic), Claude-family model running as a GitHub Copilot agent. I worked alone and read-only, with one tool call per response throughout.

## Snapshot

- Commit: `2dd9d46bca2aa4cc2b439d08c2ef36e6d9067a41` (batch 150)
- Kanji: 葬 蒔 蓄 薦 虚 融 衆 街 衝 裁 裂 裸 覆 視 覧
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-150-2dd9d46b`. I took the packet-manifest sha256 (`2b49b3f4f4c31756d984e28dfaf6e69fdfb6a1670764201e7b21f614fb7354f3`) as given; I did not recompute it.

## Scope

**Unit under review:**
- the 15 new cards in `snapshot\kanji\`;
- the 15 files in `snapshot\strokes\`;
- the 18 modified word articles, each a one-line link wrap (`diffs\`).

**Packet files opened**

*Read in full:*
- `INSTRUCTIONS.md`
- `mechanical-checks.md`
- `snapshot\kanji\` 葬 蒔 蓄 薦 虚 融 衆 街 衝 裁 裂 裸 覆 視 覧, all 15. Several were re-read in part afterwards (mnemonic and Notes lines).
- `snapshot\strokes\` all 15 JSON files. 視.json was printed raw; the other 14 were parsed for revision, schema, stroke count, stroke types and point counts.
- `diffs\` all 18. I printed the hunks and changed lines in full; context lines only as the hunks show them.
- `evidence\kanjivg-components.txt`
- `evidence\source-metadata.json`
- `evidence\kanjipedia-outside-readings.json`
- `evidence\okurigana-scan.txt`
- `evidence\public-source\` all 15 Weblio (Digital Daijisen) extracts.

*Read in part:*
- `evidence\kanjidic2-records.xml`: the records for the 15 kanji, extracted.
- `evidence\jmdict-families.xml`: the entries cited by the cards, extracted by id or headword.
- `evidence\jmdict-digest.tsv`: header and lines 1–15.
- `evidence\joyo-pages.md`: the rows for all 15 kanji found by grep, plus re-reads of the 視, 覧, 衆 and 裁 rows. The front matter (pp. 2–3) was not read.
- `evidence\audits\reading-exposure.txt`: head, the "attested … offered by" lines and the totals.
- `evidence\audits\reading-options.txt`: head and section headers.
- `titles\kanji-titles.tsv`: filtered rows for every exclusion, distractor and candidate-missing kanji I judged.
- `repo\docs\content-format.md`: the heading list and lines 86–154 (Kanji card, Quiz authoring, Curated reading questions).

*Not opened:*
- `evidence\kanjivg-svgs.txt` (the component file was sufficient);
- `evidence\daijisen-heads.txt`;
- `evidence\audits\quiz-safety.txt`, `word-remarks.json`, `kanji-remarks.json`, `kanji_remarks.py`;
- `evidence\app-code\`;
- `rubric\` (if present), `titles\word-titles.tsv`;
- the full texts of `snapshot\words\*` beyond the diff hunks;
- any other `repo\` file.

**Public web sources**
- Live Kanjipedia pages for 葬 蒔 薦 虚 融 衆 街 衝 裁 裂 裸 覆 視 覧, 14 of 15. I fetched each page and read the reading list (with 外/中/高 marks) and the numbered senses.
- Digital Daijisen: I relied on the packet's Weblio extracts rather than live pages.
- JMdict: checked through the packet extracts (pinned snapshot) and my own knowledge of the public entries.

## Verdicts

| Facet | Overall | Per-card differences |
| --- | --- | --- |
| 1 Correctness | **CLEAN** for the card content. One minor provenance defect is in the audit evidence, not in a card (C1). | None of the 15 cards has an established correctness defect. Wording polish on 虚 and 薦 is in Optional. |
| 2 Scoped coverage | **CLEAN** | Optional coverage gaps: 衝 (衝撃, 衝動), 虚 (虚偽, 空虚), 覧 (一覧), 裂 (破裂). None is a defect under the scoped rule. |
| 3 Consistency and quiz safety | **CLEAN** | Optional exclusion-consistency notes on 街 (径), 衝 (攻) and 覆 (転). |
| 4 Comprehensibility | **CLEAN** | Optional polish on the 融 and 覧 mnemonics (unexplained 鬲 and 𠂉) and on the 裸 image. |

The 18 word diffs are CLEAN on all facets: each changes exactly one line and is a link wrap only.

### What I verified (basis for CLEAN)

**Front matter, all 15 cards.** Each card's grade, strokes, radical and number, on and kun lists (and nanori where cited) match KANJIDIC2 and source-metadata.json.
- quizOnyomi and quizKunyomi are exact subsets of the full lists.
- Each selected reading has its own Readings row, which links an existing word article.
- 蒔 is correctly treated as outside the Joyo table.

**Stroke files, all 15.**
- schemaVersion 1 and KanjiVG revision 70a0b7ae.
- strokeCount equals the number of strokes and matches the card.
- The stroke-type sequences equal kanjivg-components.txt exactly.

**Readings.** I checked every reading row against KANJIDIC2, the Joyo rows in joyo-pages.md, live Kanjipedia (including its 外 and 高 marks) and the Daijisen extracts.

Kanjipedia marks:
- 外: 覆 フ・フウ; 薦 こも/しく/しきりに; 融 とおる; 衝 つく; 覧 みる; 視 みる; 裂 きれ; 衆 おおい; 街 ちまた.
- 高: 覆 くつがえす/くつがえる.
- 中: 街 カイ.

Labels that depend on JMdict spellings:
- 視 み.る is labelled kun, supported by the full JMdict spelling 視る in 1259290.
- 覧 み.る is labelled source-only because 覧る is only a search-only form in that entry.
- The two labels are consistent and accurately explained.

Other reading labels:
- 裁 た.つ is separated from 断つ, matching the Joyo ⇔ note 断つ，絶つ.
- 虚 コ is supported by 虚空 and 虚無僧.
- 衆 シュ is supported by 衆生, which is the Joyo example.
- 街 カイ is supported by 街道.
- 裸 はだし is correctly treated as a whole-word reading of 裸足.
- 裂 -ぎ.れ is supported by 古代裂れ.
- 覆 フウ is matched to the covering sense, as Daijisen gives 〈フウ〉おおう.

**Example words.** Every JMdict id on the Metadata lines resolves to the cited word. Every quoted English gloss I checked is an exact JMdict gloss, among them:
- 1402130 葬る "to bury; to inter; to entomb";
- 1456890 突く "to push; to thrust";
- 1546070 溶ける;
- 1259290 見る/観る/視る/覧る;
- 1270760 ご覧/御覧;
- 1175380 閲覧;
- the ids for 推薦, 謙虚, 金融, 公衆, 衝突, 裁判, 裁縫, 裂く, 裸, 覆う, 無視, 重視, 展覧会 and 街角.

Quoted KANJIDIC2 meanings are exact. Examples: 薦 "recommend; mat; advise; encourage; offer", 視 "regard as", 虚 "untruth", 裸 "naked; nude; uncovered".

**Meaning statements (lead g).** All are true and fairly sourced:
- 薦: Kanjipedia ① すすめる and ② こも。敷物。しとね, with こも marked 外.
- 虚: "false", supported by Kanjipedia ② うそ and KANJIDIC2 "untruth".
- 融: "circulate", supported by Kanjipedia ③ とおる。通じる。流通する and 金融.
- 衝: "thrust", supported by JMdict 突く sense 2 and Kanjipedia ① つく; つく is marked 外.
- 視: regard-as, supported by Kanjipedia ② みなす (重視) and KANJIDIC2 "regard as".
- 覆: "repeat", supported by Kanjipedia ③ くりかえす。かさねる, 類 復.
- 裂: きれ (cloth), supported by Kanjipedia, where it is marked 外.

**Joyo claims.** Every claim about what the Joyo table prints matches joyo-pages.md: the reading rows, the examples, the ⇔ notes (for example 裁 たつ ⇔ 断つ，絶つ, and 街 まち cross-referencing 町) and the bracketed forms 視（視）, 覧（覽）.

**Mnemonics (lead f).** All 15 are labelled "Modern-shape mnemonic, not etymology" and end with a no-historical-claim disclaimer. Quoted titles are exact card titles. Every component, position and stroke statement is true against kanjivg-components.txt:
- 薦: 广 and 灬, with the middle strokes outside any group.
- 衆: 血 with 皿 inside it, and 亻 below.
- 街 and 衝: split by 行, with 圭 = 土 over 土 and 重 between.
- 裁: 𢦏, with three top strokes and the 戈 part on the right, around 衣.
- 覧: 臣 (strokes 1–7), 𠂉 (8–9), stroke 10 outside any group, 見 (11–17).
- 虚: 虍 over 业.
- 融: 鬲 plus 虫.
- 視: 礻, original 示, beside 見.
- 蓄: 艹 over 畜, with the crown compared to 草.

**Reading-audit accounting (lead e).**
- The 4 latent collisions in reading-exposure.txt are all KANJIDIC2 name readings: 蒔 まい (参, 舞), 蒔 まき (巻), 街 また (復) and 視 み (味 未 美 魅).
- None of these readings is selected for a quiz, and the app protects all full readings of the target. So none of them can appear as a wrong option on its own card's question.
- I agree with 0 production hits, 0 padded-session hits and no HIT in reading-options.
- Daijisen name readings that were not passed as extras (薦 しげ/のぶ; 融 あき/すけ/とお/ながし/みち/よし; 衆 とも/ひろ/もり/もろ; 衝 つぎ/みち/もり/ゆく; 視 よし; 覧 かた/ただ) do not match the quiz on-readings of any curated option card for those targets. All six cards quiz on'yomi only.

**Diffs (18).** Each diff:
- changes exactly one line;
- wraps the first bare mention of the new kanji as `[X](../kanji/X.md)`, pointing to the intended card;
- leaves the prose unchanged and does not touch a `Dictionary:` line.

The 4 lint warnings (公衆, 葬式, 蓄える, 街角) concern lines the diffs do not touch, so they are context only.

**Meta scan.** No listed Metadata id is wrong. Every statement a card attributes to JMdict has its entry id on the Metadata line. The listed fragments and source-attributed words are as described in the brief.

**Exclusions and distractors (leads a–c).** I judged each pair against the displayed titles in kanji-titles.tsv.
- Every exclusion is a direct pair with stated evidence; none is a transitive-only clique.
- The borderline pairs are defensible as genuine two-answer risks for an English learner: 衝/戦 and 衝/争 (衝突 "conflict"), 衆/組, 衆/公, 視/捜, 覧/仰, 覆/秘, 裂/爆, 葬/悔 and 薦/献/供. Over-exclusion only removes options.
- Within the batch, 視/覧 and 裁/裂 are excluded. The pairs 蓄/衆, 葬/蒔, 覆/裸 and 虚/裸 are distinguishable in both directions from their titles.
- All 45 distractors are plausible yet defensibly wrong in both directions, including 氷 "ice; freeze" vs "melt", 法 vs "judge", 寺 vs "funeral", 教 vs "recommend/advise", 縫 vs "tear apart" and 掘 vs "sow seeds".

**Structure.** Section order and headings are the same across all 15 cards and follow content-format.md's Kanji card rules (front matter, title line, Meaning and origin, Readings, Common words, Notes, Metadata). Each card has 3 distractors with no overlap with its exclusions.

## Findings

**C1 (minor; audit evidence, not card content): extra readings carry the wrong provenance label.**
`evidence\audits\reading-exposure.txt` labels several extra readings passed to the audit as coming from "(card text)":
- 葬 ほうぶる;
- 裂 れっぱく;
- 覆 おいかぶさる;
- 視 しする;
- 虚 きょをつく and きょをつかれる.

None of these strings appears in the corresponding card. Their actual source is `evidence\okurigana-scan.txt` (JMdict-derived okurigana parses, for example 1402130's alternate reading ほうぶる and 2039960 覆いかぶさる).

The counts and the collision accounting are unaffected. However, a reader of the audit is told that the card text makes claims it does not make.

*Fix:* label these readings with their real source (okurigana scan / JMdict id).

No established defect was found in any of the 15 cards, the 15 stroke files or the 18 word diffs.

## Optional

Polish only; none of these is a defect.

**Quotations and wording**
- **O1 (虚).** The card quotes Daijisen as 邪心をもたない. The packet extract has 邪心を持たない, and the live Kanjipedia ③ is worded similarly. Use the source's exact kanji/kana if the text is presented as a quotation.
- **O2 (薦), two points:**
  - JMdict's "[see also: 推奨]" is a cross-reference, not a gloss. If it appears inside gloss quotes, present it as a cross-reference.
  - The exclusion line renders Kanjipedia's ② as こも・敷物; the source punctuation is こも。敷物。しとね.

**Exclusion consistency** (the author's own evidence would justify these extra pairs; their absence is safe enough)
- **O3 (街).** 道/路/途 are justified from JMdict's みち entry, which also has the spelling 径. 径 ("diameter; path"; KANJIDIC2 also "path") is not excluded. "path" against "street; town" is a weak two-answer risk.
- **O4 (衝).** 撃 is excluded on the strength of JMdict's "to attack", but 攻 ("attack; go on the offensive") is not. Either exclude 攻 too, or note why "attack" is only a weak sense of 衝.
- **O5 (覆).** The "overturn" sense (転覆) sits next to 転 ("turn; roll"). This is low risk; consider whether 転 belongs with 倒/翻.
- **O6 (葬).** 墓 ("grave; tomb") is defensibly distinct from "bury; funeral". I note it only because 埋 is excluded.

**Coverage**
- **O7 (衝).** 衝撃 (shock; impact) and 衝動 (impulse) are very common and are absent from Common words (衝撃 appears only in an exclusion line). Daijisen's 難読 衝立 ついたて is not mentioned either.
- **O8 (虚).** Only 謙虚 is a Common word. 虚偽 and 空虚 (Joyo examples) would show the "false" and "empty" senses the title promises.
- **O9 (覧 / 裂).** Consider 一覧 (a Joyo example) for 覧 and 破裂 for 裂.

**Comprehensibility**
- **O10 (融 / 覧).** The mnemonics name 鬲 and 𠂉 without saying what they look like or mean. A short gloss would help an N5–N4 reader (鬲 "tripod cauldron"; 𠂉 a small hooked "person-like" shape).
- **O11 (裸).** The image of clothing peeled away "from a fruit" mixes two pictures. A simpler "clothing taken off" scene would be more concrete.
- **O12 (C1 related).** The okurigana scan's parses お.いかぶさる (for 覆いかぶさる) and the particle-bearing きょ.をつく / きょ.をつかれる are harmless as audit extras. Normalising them would make the evidence easier to read.

## Limits

**Tool-call discipline.** I issued exactly one tool call per response and no parallel calls. I used no sub-agents, background jobs, recursive listings or corpus scans.

**Not run at this snapshot (known packet limits, not findings).** The Android JVM content tests and the Kotlin cross-check of the reading audit.

**Sources not checked live.**
- I did not live-fetch Kanjipedia for 蓄. Its readings were checked against KANJIDIC2, the Joyo row and the Daijisen extract.
- I did not live-fetch Digital Daijisen; I relied on the packet's Weblio extracts.

**Packet files not opened, and their effect.**
- joyo-pages.md was read only at the relevant rows, so the front matter (pp. 2–3) was not read.
- daijisen-heads.txt was not opened. Daijisen name-reading claims were checked against the Weblio extracts instead.
- quiz-safety.txt was not opened. My meaning-quiz judgments come from the titles TSV and the cards.
- kanjivg-svgs.txt was not opened. Component statements were verified against kanjivg-components.txt only.
- content-format.md was read only for the Kanji card sections, so section order was judged against that section and the cards' uniform structure.

**Assumptions.**
- An exclusion is acceptable when the displayed titles give a plausible two-answer risk for an English speaker. Over-exclusion is therefore judged far less harmful than a missing exclusion.
- "Common words" coverage is scoped, so omissions are Optional unless a card misdescribes a word.
