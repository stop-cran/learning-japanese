Snapshot: `28831314c9b8203cf7dd66c4eec16f23ef0fef22` — batch 140. Reviewer: GitHub Copilot; the underlying model name/version is not exposed to this reviewer. Packet-manifest SHA-256 independently matched `91e88965347d04f2c44cae51b787f1fa39260d3fd6da1c8ddb01e5d95a059c10`.

Scope:

Reviewed all 15 new kanji cards, all 15 stroke files, and all 24 existing-file diffs. Facets 3 and 4 received the deepest attention. Paths below are relative to the supplied packet, not to another checkout.

**Files read in full:**

- `INSTRUCTIONS.md`; `mechanical-checks.md`.
- `snapshot\kanji\嵐.md`, `巣.md`, `帳.md`, `幕.md`, `幣.md`, `序.md`, `弁.md`, `往.md`, `径.md`, `徐.md`, `従.md`, `徴.md`, `志.md`, `怠.md`, `恨.md` — each filename after the first has the same `snapshot\kanji\` prefix.
- `diffs\kanji__慢.md.diff`.
- `diffs\words__お弁当.md.diff`, `words__半径.md.diff`, `words__嵐.md.diff`, `words__巣.md.diff`, `words__幕.md.diff`, `words__弁当.md.diff`, `words__往復.md.diff`, `words__徐々に.md.diff`, `words__従う.md.diff`, `words__従って.md.diff`, `words__従兄弟.md.diff`, `words__従姉妹.md.diff`, `words__怠ける.md.diff`, `words__怠る.md.diff`, `words__恨み.md.diff`, `words__恨む.md.diff`, `words__意志.md.diff`, `words__手帳.md.diff`, `words__特徴.md.diff`, `words__直径.md.diff`, `words__紙幣.md.diff`, `words__通帳.md.diff`, `words__順序.md.diff` — all under `diffs\`.
- `evidence\source-metadata.json`; `evidence\joyo-pages.md`; `evidence\kanjipedia-outside-readings.json`; `evidence\daijisen-heads.txt`; `evidence\okurigana-scan.txt`.
- `evidence\audits\quiz-safety.txt`; `evidence\audits\reading-exposure.txt`; `evidence\audits\reading-options.txt`; `evidence\audits\kanji-remarks.json`; `evidence\audits\word-remarks.json`; `evidence\audits\kanji_remarks.py`.
- `evidence\app-code\QuizBuilder.kt`; `evidence\app-code\KanjiMeaningMetadata.kt`.
- `repo\kanji\徒.md`; `repo\kanji\律.md`; `repo\kanji\待.md`.

**Files read completely by structured checks, with the following inspection limits:**

- `snapshot\strokes\嵐.json`, `巣.json`, `帳.json`, `幕.json`, `幣.json`, `序.json`, `弁.json`, `往.json`, `径.json`, `徐.json`, `従.json`, `徴.json`, `志.json`, `怠.json`, `恨.json` — all under `snapshot\strokes\`. Every stroke record and coordinate array was parsed and checked; 嵐 was also inspected as raw JSON.
- `titles\kanji-titles.tsv`; `titles\word-titles.tsv`: complete structured reads for title uniqueness, referenced labels, readings and word availability; selected rows inspected as text.
- `evidence\kanjidic2-records.xml`: complete XML parse and inspection of all 15 relevant character records; opening lines also read as text.
- `evidence\jmdict-families.xml`: complete XML parse for family membership, example written-form/reading pairs and quoted-gloss checks. Selected entries and restrictions were inspected directly, including 1179760, 1309050, 1335290, 1335310, 1345580, 1345590, 1345600, 1400400, 1524750, 1595480, 1747330, 2018930, 2231620, 2427730, 2464210, 2789910 and 5239369. This was not a line-by-line human reading of the whole XML.
- `evidence\jmdict-digest.tsv`: complete structured read for priority-tagged family entries; opening 45 lines and selected common-word rows inspected as text.
- `packet-manifest.json`: full bytes read for the hash only; its contents were not substantively reviewed.

**Files read in part:**

- `snapshot\kanji\慢.md`: lines 66–90, including the changed bullet and surrounding Notes.
- The following `snapshot\words\` files: their complete “How the kanji combine” sections, nearby preceding text and the beginning of the next section, with diff additions checked against the snapshots: `お弁当.md`, `半径.md`, `嵐.md`, `巣.md`, `幕.md`, `弁当.md`, `往復.md`, `徐々に.md`, `従う.md`, `従って.md`, `従兄弟.md`, `従姉妹.md`, `怠ける.md`, `怠る.md`, `恨み.md`, `恨む.md`, `意志.md`, `手帳.md`, `特徴.md`, `直径.md`, `紙幣.md`, `通帳.md`, `順序.md`.
- `rubric\copilot-instructions.md`: visible opening 100 lines.
- `repo\docs\content-format.md`: relevant lines 71–139 and 274–289, plus heading inspection.
- `repo\docs\confusable-words.md`: opening 90 lines.
- `evidence\provenance.json`: opening 45 lines.
- `evidence\app-code\KanjiReadings.kt`: lines 1–155.

**Independent public verification:**

- Actual Digital Daijisen entries on `https://www.weblio.jp/content/` for all 15 characters, plus their public KANJIDIC-derived reading panels. These were entry inspections, not search snippets.
- Actual dictionary-entry passages for 嵐気, 卵巣, 巣くう, 手帳, 通帳, 幕府, 紙幣, 序で, 弁える, 花弁, 弁当, お弁当, 往く, 往ぬ, 往復, 半径, 直径, 徐々に, おもむろに, 従う, 従って, 従兄弟, 従姉妹, 従事, 従容, 意志, 志す, シリング, 特徴, 順序, 怠る, 怠ける, 恨む, 恨み, 恨めしい, and 徒. The separate 従三位 page provided non-Daijisen corroboration; its reading was additionally checked in the character entry and pinned JMdict.
- All 15 public KanjiVG SVGs at revision `70a0b7ae0c18ceb5cb358274b029cce0234a43bc`, under `https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/`.

Verdicts:

- **Correctness: NEEDS FIX** — G1, limited to quotation/source fidelity in 幕 and 徐. No substantive wrong Japanese reading, meaning or stroke geometry was established.
- **Scoped coverage: CLEAN** — every metadata reading is represented or explicitly qualified; no consequential common-use omission was established.
- **Consistency and quiz safety: CLEAN** — no demonstrated ambiguous correct option or reachable reading collision in the inspected sessions.
- **Comprehensibility: NEEDS FIX** — G2, the front-loaded reference catalogues in 弁 and 従.

Per-card verdicts and principal checks:

| Card | Correctness | Coverage | Quiz safety | Comprehensibility | Principal observations |
|---|---|---|---|---|---|
| 嵐 | CLEAN | CLEAN | CLEAN | CLEAN | あらし versus unquizzed ラン is clear; 山/風 mnemonic is expressly modern-shape, not a weather restriction or etymology. |
| 巣 | CLEAN | CLEAN | CLEAN | CLEAN | す, ソウ and すくう accounted for; 家 exclusion has a real dwelling overlap, not just a loose visual association. |
| 帳 | CLEAN | CLEAN | CLEAN | CLEAN | とばり and whole-word 蚊帳かや distinguished from チョウ; book/record exclusions are defensible. |
| 幕 | NEEDS FIX: G1 | CLEAN | CLEAN | CLEAN | マク/バク, 幕府 and source-only とばり distinguished; two reading-option fallback slots are not themselves a defect. |
| 幣 | CLEAN | CLEAN | CLEAN | CLEAN | ヘイ alone is tested; ぬさ, みてぐら and archaic まい are not conflated with ordinary money vocabulary. |
| 序 | CLEAN | CLEAN | CLEAN | CLEAN | Both metadata representations of ついで covered; opportunity/occasion sense distinguished from order/preface. |
| 弁 | CLEAN | CLEAN | CLEAN | NEEDS FIX: G2 | Old-form grouping, ベン/ヘン, source-only kun readings, 花弁 and whole-word bento treatment checked. |
| 往 | CLEAN | CLEAN | CLEAN | CLEAN | オウ distinguished from rare 往く spellings and historical/source-only readings; いにしえ not taught as an ordinary bare-character word. |
| 径 | CLEAN | CLEAN | CLEAN | CLEAN | ケイ has diameter examples; みち, こみち, さしわたし and ただちに are appropriately qualified rather than all presented as everyday words. |
| 徐 | NEEDS FIX: G1 | CLEAN | CLEAN | CLEAN | Original deliberate/unhurried おもむろに sense and the disputed modern sudden sense are accurately separated. |
| 従 | CLEAN | CLEAN | CLEAN | NEEDS FIX: G2 | ジュウ/ショウ/ジュ and したがう/したがえる/より distinguished; cousin readings treated as whole-word readings; ひろい marked archaic. |
| 徴 | CLEAN | CLEAN | CLEAN | CLEAN | チ is a music term, not an ordinary alternative for 特徴; しるし and levy/recruitment senses checked. |
| 志 | CLEAN | CLEAN | CLEAN | CLEAN | シリング treated as a historical spelling association, not normal native vocabulary; こころざす/こころざし covered. |
| 怠 | CLEAN | CLEAN | CLEAN | CLEAN | おこたる and なまける separated; タイ present but not falsely advertised as tested. |
| 恨 | CLEAN | CLEAN | CLEAN | CLEAN | うらむ, うらめしい and コン covered; resentment/regret/blame contrasts are defensible. |

**Meaning options and exclusions.** I judged the displayed English titles, not merely the Japanese characters, and considered the reverse semantic comparison as well. The complete simulation supplies all three curated distractors for every new target:

| Target | Curated distractors checked | Direct exclusions checked |
|---|---|---|
| 嵐 | 岩 岸 崩 | 風 騒 乱 |
| 巣 | 果 単 栄 | 家 |
| 帳 | 帽 幅 帯 | 録 籍 記 誌 冊 本 巻 |
| 幕 | 墓 暮 募 | 劇 演 布 終 末 |
| 幣 | 中 内 南 | 貨 金 札 供 贈 |
| 序 | 広 庁 預 | 順 番 整 始 緒 初 |
| 弁 | 台 去 算 | 話 言 語 詞 論 議 別 飯 |
| 往 | 住 注 待 | 行 出 去 旅 昔 旧 古 |
| 径 | 役 彼 怪 | 道 路 途 |
| 徐 | 余 途 徒 | 遅 悠 |
| 従 | 徒 律 待 | 循 則 守 応 準 屈 追 供 仕 副 |
| 徴 | 微 徹 徳 | 兆 符 印 標 症 収 採 税 召 募 |
| 志 | 売 声 忘 | 意 望 希 願 欲 祈 標 決 定 |
| 怠 | 始 治 念 | 慢 |
| 恨 | 限 銀 快 | 憎 苦 責 怒 |

No listed distractor was established as an alternative correct answer to its target's displayed title. Similar wrong options do not by themselves create a second correct answer. The weaker exclusions still have direct grounds: abbreviated bento for 弁/飯; ending/close for 幕/終/末; aim or resolve for 志/標/決/定; accompaniment, compliance or secondary status for 従's comparisons; bitterness or blame for 恨/苦/責. They should not be read as claims that every member of an exclusion list is synonymous with every other member.

For 従/徒 specifically, 徒's group, disciple and penal senses do not establish that its displayed “on foot” title also answers “follow; obey; subordinate.” I found no sufficient basis for a collision finding. 幣's three distractors are semantically safe, although visually less convincing than the strongest sets.

**Reading-option reachability.** The complete exposure audit reports no production hits, no padded Starter hits and no one-holder padded hits; its four latent collisions are not four demonstrated quiz failures. The separate options audit explicitly ignores slots already filled by curated candidates.

- 幣's latent まい can be offered by 埋/妹/枚/毎/米 in the broader candidate inventory, but 中/内/南 fill the three wrong slots in the inspected pools. The options audit's HIT label therefore does not establish exposure.
- 弁 とく and 従 ひろい remain latent fallback candidates, not demonstrated displayed options.
- 志 じん is a name reading, not an omitted ordinary on/kun reading that must be taught here.
- For 幕 マク, 墓 contributes no selected on reading and 暮/募 collapse to the same ボ key. Two fallback slots are consequently expected. Both マク and バク are protected; the inspected fallback inventory establishes no unsafe answer.
- Duplicate or unavailable curated reading keys in 往, 徐, 従 and 怠 likewise explain fallback without establishing ambiguity.

Omission of 幣's additional dictionary readings ぜに/にきて does not create missing metadata coverage or a demonstrated quiz fault. The cards are not required to reproduce every reading from every dictionary.

**Metadata, links and strokes.** All 15 cards' pinned grade, radical, stroke count and reading lists matched the supplied metadata. Selected quiz readings are metadata subsets and have linked word examples. New titles were unique in the title index; checked links resolved to their intended cards. Joyo reading/example claims matched the supplied official-table extracts, including its front matter. Modern-shape mnemonics were labelled as such and their component descriptions were defensible.

All 149 stroke records had the expected identity, order, type and coordinate structure. Against the pinned public KanjiVG paths, every stored point was within approximately 0.071 viewBox units of its corresponding path; endpoints also matched within that distance. This supports the geometry as well as merely the stroke counts.

**Existing-file changes.** All 24 supplied diffs matched the declared scope: 21 link-wrap-only word edits, the two additional sentence removals in 半径 and 往復, and the single 慢 bullet edit. Each added link addresses its intended new card. Snapshot passages contain the diff additions and remain coherent. Removing the obsolete “no card” statements is correct; 慢's remaining statement about 緩 is supported by the title inventory. No unrelated change was visible in these diffs. The four unchanged Dictionary-line warnings are not findings.

Findings:

**G1 — minor; facet 1, correctness/source fidelity; `snapshot\kanji\幕.md:62` and `snapshot\kanji\徐.md:48`.**

- **Claim and impact:** The quoted English glosses “covering cloth” and “slow, unhurried” are explanatory paraphrases, not actual English glosses in the cited JMdict entries, KANJIDIC2 meanings, or exact cited card titles. Their meanings are defensible; the defect is the owner's explicit requirement that double-quoted glosses be source-real. As written, the distinction between sourced wording and the author's explanatory English is lost.
- **Remedy:** Remove the quotation marks from these two paraphrases, or replace them with actual cited gloss wording. No Japanese reading, exclusion or title needs changing for this finding.
- **Evidence:** 幕's cited JMdict 1524750 has “curtain,” “act (in a play),” “end,” and “close,” among other senses; its KANJIDIC2 meanings are “curtain,” “bunting,” and “act of play.” Neither supplies “covering cloth.” 徐's KANJIDIC2 meanings are “gradually,” “slowly,” “deliberately,” and “gently”; its cited JMdict entries include “slowly,” “without haste,” “calmly,” “gently,” and “deliberately,” but not “slow, unhurried.” The public Daijisen senses support the explanations, not those purported source-exact English strings.
- **Confidence:** High for the narrow quotation-contract defect; this is not a finding of false Japanese semantics.

**G2 — minor; facet 4, comprehensibility; `snapshot\kanji\弁.md:25–39` and `snapshot\kanji\従.md:25–34`.**

- **Claim and impact:** The practical reading table and mnemonic are preceded by a dictionary-entry catalogue disproportionate to the stated N5–N4 phone audience. 弁 walks through all eleven Daijisen senses, including a historical cap and braiding; 従 introduces six ジュウ senses, three ショウ senses, an ancient alliance, court ranks and an archaic prefix before its learning table. There are approximately 378 whitespace-separated words before 弁's Readings heading and 455 before 従's. This is a concrete front-loading/wall-of-text issue, not a demand to remove legitimate rare-reading coverage.
- **Remedy:** Keep the existing central explanation, then reach the mnemonic and practical reading table promptly. Compress the sense inventories or relocate their genuinely useful remainder to short reference bullets after the core teaching. Preserve every metadata-reading row and the important qualifications about old forms, whole-word readings and what is not quizzed.
- **Evidence:** The cited source passages and their placement in the full cards; the packet's explicit “beginner on a phone,” “no wall of text” and “no padding” requirements. Both cards already have later Notes reference material, so exhaustive introductory catalogues are not necessary to preserve source coverage.
- **Confidence:** High on the observed placement and volume; medium-high on the learning impact. Severity is minor because the opening central ideas are accurate and understandable.

Optional:

- 幣's 中/内/南 set has relatively weak visual discrimination value: broad enclosing shapes and vertical strokes are doing most of the work. Consider stronger look-alikes only if their displayed meanings remain safely wrong and their reading options remain safe; do not casually replace a collision-free set.
- If shortening 弁's catalogue, a common example such as 弁護士 would be a more useful trade for an esoteric example than adding still more vocabulary. Its absence is not a separate coverage defect.
- 徐 could explicitly connect the metadata dot in おもむ.ろに with the alternative spelling 徐ろに while explaining why its principal example uses 徐に. Both spellings are already acknowledged; this would reduce a beginner's decoding effort.

Limits:

- Independent, blind and read-only review: no other reviewer report, author rationale, checkout, session or agent was accessed. All tool calls were serial, with one call per tool-using assistant turn; no parallel calls, sub-agents or background jobs were used.
- Some oversized tool outputs were truncated and automatically spooled by the execution tool. I did not open those spool paths. Relevant passages were reread in bounded output; the Scope distinctions above do not claim full human inspection of truncated material.
- This was static packet/source review, not a rendered phone or Android runtime test. I did not run the known-unavailable JVM content tests or Kotlin audit cross-check, and do not report their absence as defects.
- The meaning and reading simulations are supplied evidence, checked against the inspected builder logic; I did not rebuild the app or independently reproduce every possible arbitrary user-selected session. A latent fallback candidate is not asserted to be impossible under every conceivable future pool.
- Independent public checks covered every card's reading inventory and the consequential word/reading/register distinctions listed in Scope. I did not independently browse every obscure compound's separate dictionary page; the pinned JMdict families support the remaining family/example checks.
- Public Weblio reading panels sometimes differ from the pinned KANJIDIC2 data. They were corroboration, not grounds for silently replacing the snapshot's metadata or demanding all additional online readings.
- `kanjiapi.dev` returned HTTP 403 for all 15 attempted character lookups. A Jisho 従容 request exposed no usable entry. Neither was treated as verification; actual Weblio entries and the pinned sources supplied the checks instead.
- Stroke geometry was checked numerically against the pinned source, not reviewed as rendered animation or handwriting instruction.
- The supplied diffs, snapshots, inventories and audit results support the stated change-scope conclusion; no separate Git repository history was available or accessed.
- “CLEAN” means no actionable defect established within these bounds, not exhaustive dictionary completeness. G1 is a narrow quotation-contract issue, and G2 is a beginner-presentation issue; neither establishes a production quiz failure.
