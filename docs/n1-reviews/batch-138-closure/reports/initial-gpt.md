Snapshot: `b6020f9e490298de1756e33c51bf9ce314132f4e` — batch 138. Reviewer: OpenAI GPT-family model; the exact serving model/version identifier is not exposed to me. Independent, blind review.

Scope:

Packet root: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-138-b6020f9e`. Facets 3 and 4 received the deepest examination. All four facets were considered for every new card. Existing articles were read for change integrity and surrounding context, not treated as an invitation to rewrite unrelated material.

**Packet files opened and extent of inspection**

Names grouped beneath a directory identify individual files, not a directory scan.

- **Full text:** `INSTRUCTIONS.md`; `mechanical-checks.md`.
- **Full text, `snapshot\kanji\`:** `噴.md`, `垂.md`, `垣.md`, `執.md`, `堅.md`, `塊.md`, `墨.md`, `壁.md`, `壊.md`, `奏.md`, `契.md`, `奨.md`, `奪.md`, `妨.md`, `威.md`, `張.md`.
- **Full text, `snapshot\words\`:** `噴水.md`, `噴火.md`, `垂直.md`, `垣根.md`, `執筆.md`, `堅い.md`, `塊.md`, `墨.md`, `壁.md`, `壊す.md`, `壊れる.md`, `契約.md`, `奨学金.md`, `奪う.md`, `妨げる.md`, `威張る.md`, `演奏.md`.
- **Full text, `diffs\`:** `kanji__張.md.diff`, `words__噴水.md.diff`, `words__噴火.md.diff`, `words__垂直.md.diff`, `words__垣根.md.diff`, `words__執筆.md.diff`, `words__堅い.md.diff`, `words__塊.md.diff`, `words__墨.md.diff`, `words__壁.md.diff`, `words__壊す.md.diff`, `words__壊れる.md.diff`, `words__契約.md.diff`, `words__奨学金.md.diff`, `words__奪う.md.diff`, `words__妨げる.md.diff`, `words__威張る.md.diff`, `words__演奏.md.diff`.
- **Full JSON parsed and checked programmatically, `snapshot\strokes\`:** `噴.json`, `垂.json`, `垣.json`, `執.json`, `堅.json`, `塊.json`, `墨.json`, `壁.json`, `壊.json`, `奏.json`, `契.json`, `奨.json`, `奪.json`, `妨.json`, `威.json`. Checked counts, stroke records, coordinates and ordered start/end/direction summaries for all fifteen. `垂.json` was also read directly in full.
- **Full text:** `evidence\source-metadata.json`; `evidence\joyo-pages.md`; `evidence\kanjipedia-outside-readings.json`; `evidence\daijisen-heads.txt`; `evidence\okurigana-scan.txt`.
- **Full text, `evidence\audits\`:** `quiz-safety.txt`, `reading-exposure.txt`, `reading-options.txt`, `kanji_remarks.py`.
- **Full text, `evidence\app-code\`:** `QuizBuilder.kt`, `KanjiReadings.kt`.
- **Full captured text, `evidence\public-source\`:** `weblio-噴.txt`, `weblio-垂.txt`, `weblio-垣.txt`, `weblio-執.txt`, `weblio-堅.txt`, `weblio-塊.txt`, `weblio-墨.txt`, `weblio-壁.txt`, `weblio-壊.txt`, `weblio-奏.txt`, `weblio-契.txt`, `weblio-奨.txt`, `weblio-奪.txt`, `weblio-妨.txt`, `weblio-威.txt`. The 垣 capture lacks the substantive character entry; I fetched that entry independently.
- **Full XML parsed, selective human inspection:** `evidence\kanjidic2-records.xml` — raw lines 1–32, all fifteen target records' metadata/readings, and relevant comparison meanings; `evidence\jmdict-families.xml` — raw lines 1–42, condensed complete cited families for all fifteen cards, and detailed relevant entries, including restrictions and register flags.
- **Full TSV parsed, selective inspection:** `evidence\jmdict-digest.tsv` — initial lines and priority-bearing examples for every target; `titles\kanji-titles.tsv` — title uniqueness, referenced titles and relevant presence/absence checks; `titles\word-titles.tsv` — read programmatically, with only its initial structure inspected, not a corpus-wide semantic review.
- **Full text:** `repo\kanji\魅.md`.
- **Partial text:** `rubric\copilot-instructions.md`, lines 1–270 and heading inventory; `repo\docs\content-format.md`, lines 1–139 and 274–289 and heading inventory; `repo\docs\confusable-words.md`, lines 1–39 and 308–334 and heading inventory; `evidence\provenance.json`, lines 1–75.
- **Hash only:** `packet-manifest.json`. SHA-256 matched the supplied value: `25d66ae4756bcc10cb638b1cf77828a1513e461cccca49bb797d21ee4a2aa415`.

**Independent public verification**

I inspected actual Kanjipedia character entries for 噴, 垂, 垣, 執, 塊, 墨, 壁, 壊, 奏, 契, 奨, 奪, 妨 and 威. The 堅 request failed; its actual Digital Daijisen entry on Weblio was inspected instead. Live Daijisen entries for 垣 and 垂 supplied additional checks, and the actual kanjiapi.dev 塊 record independently confirmed ケ.

Actual Jisho dictionary API entries were inspected for these searches, with some broader responses read only through the relevant complete entries: `噴*`, `垂*`, `垣`, `執*`, `執る`, `堅い`, `手堅い`, `塊`, `墨`, `壁`, `壊*`, `奏*`, `演奏`, `契*`, `奨*`, `奪う`, `妨*`, `威*`, `垂んとす`, `雨垂れ`. These covered the changed words and the reading/sense/register questions most consequential to the teaching. Spelling-specific and sense-specific register qualifications were checked against pinned JMdict, not inferred from an API entry's overall common-word flag.

Verdicts:

- **Correctness: CLEAN** — no actionable factual defect established within the inspected evidence.
- **Scoped coverage: CLEAN** — every metadata reading is represented or explicitly qualified; no consequential common-usage omission established.
- **Consistency and quiz safety: NEEDS FIX** — two missing direct meaning-exclusion pairs permit ambiguous restricted-pool questions: G1 and G2.
- **Comprehensibility: CLEAN** — the core explanations are understandable and honest; optional shortening is separated below.

Per-card verdicts and practice checks:

| Card | Correctness | Coverage | Quiz safety | Comprehensibility | Selected readings | Three authored meaning distractors |
|---|---|---|---|---|---|---|
| 噴 | CLEAN | CLEAN | CLEAN | CLEAN | フン | 口・古・買 |
| 垂 | CLEAN | CLEAN | CLEAN | CLEAN | スイ | 郵・乗・重 |
| 垣 | CLEAN | CLEAN | NEEDS FIX — G1 | CLEAN | かき | 坂・城・埋 |
| 執 | CLEAN | CLEAN | CLEAN | CLEAN | シツ | 報・幸・熱 |
| 堅 | CLEAN | CLEAN | CLEAN | CLEAN | かた.い | 臣・監・基 |
| 塊 | CLEAN | CLEAN | CLEAN | CLEAN | かたまり | 魅・城・場 |
| 墨 | CLEAN | CLEAN | CLEAN | CLEAN | すみ | 墓・型・堂 |
| 壁 | CLEAN | CLEAN | NEEDS FIX — G1 | CLEAN | かべ | 辛・基・坂 |
| 壊 | CLEAN | CLEAN | CLEAN | CLEAN | こわ.す・こわ.れる | 均・埋・塔 |
| 奏 | CLEAN | CLEAN | CLEAN | CLEAN | ソウ | 春・天・実 |
| 契 | CLEAN | CLEAN | CLEAN | CLEAN | ケイ | 大・天・分 |
| 奨 | CLEAN | CLEAN | CLEAN | CLEAN | ショウ | 美・奥・奇 |
| 奪 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN | うば.う | 集・隼・雑 |
| 妨 | CLEAN | CLEAN | CLEAN | CLEAN | さまた.げる | 姉・始・旅 |
| 威 | CLEAN | CLEAN | CLEAN | CLEAN | イ | 成・歳・減 |

The distractor characters identify their source cards: the quiz actually displays those cards' English titles. I assessed those titles and ordinary secondary senses in both directions. All forty-five authored target/distractor pairings are defensibly wrong; the shared components make even the simpler or less similar options plausible. I found no established invalid edge among the sixty-nine declared exclusion entries. The problem is the two omitted direct edges below, not a demand for transitive exclusion cliques.

**Correctness and coverage checks**

- All fifteen cards match the pinned stroke counts, radicals/numbers, grades and complete on/kun lists. Their practice subsets have linked examples. Titles are unique in the title index. Links and quoted linked-card titles checked out. Section order, headings, language/level tags and modern-shape mnemonic labelling are consistent with the relevant format contract. No unsupported historical derivation or erroneous component/stroke-arithmetic claim was established.
- **噴:** フン, nonquizzed ふ.く, the official-table treatment of 噴く versus 吹く, and the outside-table ホン/は.く discussion are supported. The card does not confuse dictionary attestation with practice selection.
- **垂:** The five metadata kun forms are individually accounted for. The treatment of 雨垂れ, archaic 垂んとす, dictionary しだれる/しずる, and the official table's separate reading rows is supported. None of those kun forms is represented as currently quizzed.
- **執:** シュウ is a real, useful reading in its illustrated words, although only シツ is selected. 執る とる and the Joyo note referring to 取る/採る are accurately distinguished. KANJIDIC2's name-only し does not become an ordinary on/kun reading merely because an audit can offer that sound.
- **垣 and 堅:** The qualifications on エン, ケン and -がた.い are defensible. 手堅い supports the voiced suffix example. Meaning comparisons do not require treating every fence, boundary or kind of hardness as interchangeable.
- **塊, 墨, 壁 and 壊:** カイ/ケ and つちくれ; ボク/モク; ヘキ/がけ; and カイ/エ/やぶ.る are appropriately separated from their selected practice readings. The source-only qualification on 塊 つちくれ is about the evidence/example available here, not a claim that the reading does not exist. The medical readings 壊死 えし and 壊疽 えそ are legitimate.
- **奏 and 契:** Reporting to a ruler is a genuine 奏 sense, so the second title sense is not an invented extension of musical performance. かな.でる and ちぎ.る are legitimate but unselected. 契's キツ/ケツ are outside-table dictionary readings; セツ requires its separate proper-name context, not an invented ordinary on-reading attributed to Kanjipedia.
- **奨, 奪, 妨 and 威:** The qualifications on ソウ/すす.める, ダツ/タツ, ボウ/ホウ and おど.す/おど.し/おど.かす are supported. The 威 spellings' rarity and the whole-word reading of 威張る are not confused with an unrestricted productive reading rule. 奨学金's loan-related sense is not incorrectly excluded.

**Changes to existing files**

All seventeen word diffs change exactly one line by adding the intended kanji link; no other text changes. Each link resolves to the intended new card, and the surrounding explanation remains coherent. `snapshot\kanji\張.md:59` is the sole changed 張 line: 威 is linked with its exact title, “intimidate; authority; dignity”; the statement that 緊 and 拡 still have no cards is true against the title index. The three existing `Dictionary:` lint warnings do not establish a defect in these link-wrap changes.

**Actual reading-option safety**

The complete exposure audit reports zero production hits, zero Starter padded-session hits and zero one-holder padded hits. Its eight latent collisions are 噴 ほん/はく, 塊 ほど, 壁 がけ, 契 きつ/けつ/せつ and 奪 とる. These are normalized audit keys, not a claim that on'yomi labels display in hiragana.

I checked the tiering against `KanjiReadings.kt`: an available reading is not necessarily a drawable wrong option. In the audited shipped pools the relevant slots/closeness ordering prevent these latent candidates from appearing. The two `reading-options.txt` HIT labels, 噴 ほん and 契 けつ, ignore already-filled curated slots and therefore do not demonstrate current production collisions. 執 し being drawable in Starter is not a second ordinary on/kun answer: the cited evidence is explicitly name-only.

壊's two selected forms share a stem; normal scheduling retains one reading card for that stem, as the format documents. This is not evidence that the second metadata selection was silently mistaken for an independent scheduled stem.

Findings:

1. **G1 — Minor; facet 3; `snapshot\kanji\垣.md:14,23,48`; `snapshot\kanji\壁.md:3,14,55`. Missing direct 垣–壁 exclusion.**

   **Claim and impact:** 垣's own explanation explicitly gives the ordinary second sense “barrier; wall,” while 壁's displayed title is exactly “wall; barrier.” Neither exclusion list contains the other character. Consequently a supported restricted meaning pool can present two defensible answers to 垣. This is not an observed collision in the default full-pool four-choice simulation.

   **Reproduction:** Applying the supplied `QuizBuilder.kt` rules to the four-card pool `{垣, 壁, 噴, 契}`, targeting 垣, offers `fence; hedge`, `wall; barrier`, `erupt; spout; gush`, and `pledge; vow; agreement`, regardless of shuffling. None of the target's authored distractors is in that pool, so fallback necessarily admits 壁. The reverse target also admits 垣; the strongest demonstrated semantic ambiguity is the 垣-target direction.

   **Remedy:** Declare the direct pair on either card; one declaration suffices because the client applies exclusions symmetrically. Keep the useful prose distinction. The documented behavior permits fewer choices rather than restoring an excluded card.

   **Evidence:** JMdict entry **1204780**, second sense, and **1509290**, barrier sense; independently inspected [Jisho 垣 entry](https://jisho.org/api/v1/search/words?keyword=%E5%9E%A3) and [Daijisen 垣 entry](https://www.weblio.jp/content/%E5%9E%A3); `repo\docs\content-format.md:102–106` explicitly covers custom pools and direct symmetric exclusion; `QuizBuilder.kt` admits the pair. A read-only faithful small-pool model reproduced the choices and removed the competing option after adding the edge in memory.

   **Confidence:** High for the missing edge, dictionary overlap and conditional builder result. Impact is restricted-pool dependent.

2. **G2 — Minor; facet 3; `snapshot\kanji\奪.md:14,23,48`; context `repo\kanji\魅.md:3,14`. Missing direct 奪–魅 exclusion for the ordinary attention-capturing sense.**

   **Claim and impact:** 奪う has an ordinary, unmarked second sense including “to fascinate,” “to captivate,” and “to charm.” The card itself teaches that sense. 魅's displayed title is “charm; bewitch,” but neither card excludes the other. Thus a restricted question targeting 奪 can reject a defensible secondary-meaning answer. This does not invalidate 魅 as a distractor for 塊.

   **Reproduction:** For the pool `{奪, 魅, 噴, 契}`, targeting 奪, the builder offers `snatch; rob; deprive`, `charm; bewitch`, `erupt; spout; gush`, and `pledge; vow; agreement`. The three authored 奪 distractors are absent. The reverse target also admits 奪, but I am not claiming that 魅 means “rob” or “deprive”; one-direction ambiguity suffices for the symmetric protection.

   **Remedy:** Add the single direct 奪–魅 exclusion, without extending it into an unrelated clique or deleting the correctly taught secondary sense.

   **Evidence:** Pinned JMdict **1416340**, sense 2, expressly includes “to charm,” without a rare/archaic qualification; independently inspected [Jisho 奪う entry](https://jisho.org/api/v1/search/words?keyword=%E5%A5%AA%E3%81%86); the exact 魅 title and exclusions in the contextual card; the same documented fallback/exclusion rules as G1. The read-only model reproduced the pairing and its removal after an in-memory direct edge.

   **Confidence:** High for the ordinary secondary sense and conditional builder result. No default-pool failure is alleged.

Optional:

- **Nonblocking phone-reading polish:** Shorten or relocate the extended Daijisen sense/compound inventories, especially in 垂, 執, 墨 and 威. Preserve the central explanation, concrete modern-shape mnemonic, selected-reading example and essential contrasts near the top; place uncommon historical or specialist inventories in a compact source note. The current qualifications are generally accurate, so this is not a request to erase rare readings or a factual finding.
- Retain the eight latent reading collisions as future regression cases if reading pools, curated candidates or quiz size change. Their current non-reachability is not a universal safety guarantee for arbitrary hypothetical pools.

Limits:

- This is a blind packet review. I did not consult another reviewer, author rationale, another checkout/report, a sub-agent, another session or a background job. Tool calls were serial, one per investigative response; no parallel tool-call violation occurred.
- Three early oversized tool results were truncated and produced tool-managed spill locations. I did not open those unauthorized paths. Relevant evidence was subsequently inspected in bounded reads. I created no scratch files.
- The custom-pool reproductions are faithful read-only Python models of the supplied meaning builder, not executed Kotlin or a demonstrated sequence of phone UI gestures. Their relevance rests on the explicit custom-pool contract. Default full-pool meaning questions were not shown to fail.
- Reading-safety conclusions concern the supplied shipped-stack, Starter-padding and one-holder-padding pools. The audit itself demonstrates risks in smaller hypothetical pools that the shipped stacks do not build. I do not certify every possible future/custom reading pool.
- All stroke JSON data were parsed and their ordered geometric summaries inspected; I did not independently fetch every original KanjiVG curve, render every animation or test handwriting interaction on a device.
- Public dictionary checks supplement the frozen dictionaries rather than replacing them. Not every incidental compound was separately fetched live; the pinned complete families supplied the remaining lexical checks. Failed Kanjipedia 堅 and initial HTTP requests were not treated as successful verification; alternative actual entries were used where needed.
- No Android build, JVM content suite or Kotlin cross-check was run by this reviewer. Their stated absence in the packet is not reported as a content defect or a newly discovered release blocker.
- CLEAN means no actionable defect established within the stated scope, not exhaustive linguistic or device certification. The only intended persistent change is this report.
