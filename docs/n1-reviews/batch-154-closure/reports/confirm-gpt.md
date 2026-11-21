Snapshot: e5c945d6d3f83b97145100528e448747424fded5, compared with f8f3db8c9ae7d88d72cdc3d8eaae84c8f736ca5f. Reviewer: OpenAI GPT-family model; the exact model/version identifier is not exposed to me.

Scope:

Independent confirmation, with no other review consulted. Paths below are relative to `confirm-154-gpt` unless prefixed `original`, meaning the allowed `batch-154-f8f3db8c` packet.

- Read in full: `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `diffs\fix.patch`, `diffs\changed-lines.txt`, and my `reports-154\initial-gpt.md`.
- Read all seven revised cards in full: `snapshot\kanji\随.md`, `隣.md`, `雄.md`, `項.md`, `飽.md`, `飾.md`, `黙.md`. Checked every changed hunk for correctness, scoped coverage, consistency/quiz safety and beginner comprehensibility, including its unchanged surrounding text.
- Read the eight unchanged batch cards in full from `original\snapshot\kanji`: 隠 雷 霧 顕 飼 驚 鬼 鮮, for current quiz context. Compared the seven old/new front-matter blocks directly: only the stated exclusion additions differ.
- Read in full: `checks\quiz-safety.txt`, `checks\reading-exposure.txt`, `checks\reading-options.txt`, `checks\link-targets.tsv`; `evidence\README.md`, `jmdict-cited-entries.xml`, `daijisen-aku.txt`, `QuizBuilder.kt`, `KanjiMeaningMetadata.kt`, `meta-scan.txt`. Read `KanjiReadings.kt:1–240` and the relevant `ReadingOptions` implementation in `Words.kt:216–240`.
- Original context: `rubric\copilot-instructions.md:1–180`; `repo\docs\content-format.md:86–205`; relevant Joyo-table extracts, especially PDF pages 55, 84, 88, 141, 148, 150 and 157; the 項 component/stroke-type block in `evidence\kanjivg-components.txt`; the 黙 portion of `kanjipedia-outside-readings.json`; the complete supplied Daijisen extracts for the seven changed characters; and JMdict entry 1357160 in `jmdict-families.xml`.
- Read `original\repo\kanji\追.md`, `側.md`, `辺.md` in full. Read the opening metadata of every distinct curated meaning/reading option card: 逆 離 導 探 示 捕 遠 奥 裏 弱 鈍 柔 霜 虹 雲 氷 嵐 星 額 頂 預 淡 退 滅 捨 洗 迷 恥 祝 汚 削 壊 悲 怒 喜 仏 猿 熊 腐 濁 叫 走 踊. Also checked metadata for 近 週 返 内 右 左 込 道 工 貝 目 八, and the first 30 lines of the unchanged word targets 飽くまで, 飾る and 飾り.
- Independently retrieved the actual public Kanjipedia entries linked by all seven changed cards, and the actual [Digital Daijisen 飽く entry](https://www.weblio.jp/content/%E9%A3%BD%E3%81%8F). Inspected their relevant readings, 外 marks, definitions and register note, not search snippets. Read the opening 28 lines of `packet-manifest.json`.

Changed-hunk checks:

- **随:14,38,45,56,60:** JMdict 1372800 supports ずいぶん, “very; considerably” and the kana-use qualification. Entry 1432410 sense 1 exactly supports the new 追う quotation. Eleven exclusions are present, including 追, with no removals or distractor conflict; both added source IDs exist.
- **隣:14,32,41,44,49–50,54:** JMdict 1598830 supports 隣り合う となりあう and both quoted glosses; official-table PDF p. 157 places it under となる. Entry 2163190 marks the bare verb archaic. The revised row distinguishes these rather than implying the compound is archaic. Entries 1512080, 1403830, 1555830 and 1555850 substantiate the new exclusion quotations. Seven exclusions and the added IDs agree.
- **雄:39–40,45,61:** Entries 1174680 and 1542540 support both new readings and glosses. PDF p. 150 actually gives 雄大, 英雄 and 雌雄 under ユウ; entry 1312940 supports 雌雄. The additions connect the title's “hero” to an accessible example without changing the selected reading or requiring another word article.
- **項:25:** The pinned component evidence gives 工 on the left, 頁 on the right, strokes 4–5 as horizontal then left-falling, and 貝 containing 目 over 八. The revision is an accurate modern-shape description, explicitly not etymology. All four linked component titles match.
- **飽:33–34,56:** Entry 1518280 sense 2 contains the quoted lavish-use gloss and the note “often intransitively as 〜に飽かして”. The supplied and live Daijisen entries both support the modern-standard/written-style distinction. “For this verb” scopes the qualification to 飽く; “Also” introduces the separately described adverb. Entry 1518320 supports its glosses and spelling/kana flags. No new claim makes everyday あくまで literary.
- **飾:23:** Entry 1357210 numbers the quoted meanings exactly as 1, 2 and 4; sense 3 is genuinely intervening material, not silently renumbered. The unchanged Kanjipedia quotations on that changed line also match its live entry, and entry 1357160 supports 飾り.
- **黙:34,39–40,44,54:** Live Kanjipedia marks もだす 外. Entry 2866687 supports its literary/formal qualification; entries 1431810 and 1154700 support the added compounds and readings. PDF p. 148 gives 暗黙 and 沈黙 among モク examples. The added Metadata ID is correct.

These changes introduce no contradictory reading selection, unsupported formation claim, broken changed-line link or necessary prerequisite omission. The explanations remain understandable despite reference density.

Meaning-option check for all 15 cards:

| Target | Three displayed wrong titles checked |
|---|---|
| 随 | reverse; opposite / separate; detach / guide; conduct |
| 隠 | search / indicate / capture |
| 隣 | far / interior; depths / reverse side; lining |
| 雄 | weak; frail / dull; blunt / soft; supple |
| 雷 | frost / rainbow / cloud |
| 霧 | ice; freeze / storm; tempest / star; celestial point |
| 項 | forehead; frame; sum / summit; receive / deposit; entrust |
| 顕 | pale; faint; plain; unsalted / withdraw; retreat / perish; destroy; die out |
| 飼 | capture / discard; abandon / wash |
| 飽 | get lost; be unsure / shame / celebrate; congratulate |
| 飾 | dirty; defile / shave; sharpen; pare / break; destroy; demolish |
| 驚 | sadness / anger / rejoice |
| 鬼 | Buddha; Buddhism / monkey / bear (animal) |
| 鮮 | rot; decay; spoil / pale; faint; plain; unsalted / muddy; cloudy; impure; voiced |
| 黙 | shout; exclaim / run / dance; hop |

I found no defensibly correct distractor among these titles when checked against the targets' ordinary senses, including secondary senses discussed on the cards. Shared weather, emotions, animal care or compounds do not themselves create synonymy. In particular, 項's nape sense does not mean forehead or summit, and 鬼's deceased-spirit sense does not make the displayed “Buddha; Buddhism” a gloss for 鬼.

The three added pairs were evaluated directly, not transitively:

- **随/追:** “follow” is an ordinary sense of 追う, so the two displayed labels are unsafe together. The new note quotes the relevant first sense truthfully and correctly identifies お.う on 追.
- **隣/側:** locational 側 そば means beside/right next to, making the displayed “side” and “next door; adjoining” insufficiently exclusive. The note accurately limits its justification to this sense and preserves the kana-use qualification.
- **隣/辺:** accept the exclusion as a direct, broad locational overlap: 辺's “vicinity” covers the neighbouring area expressed by 隣, including its ordinary neighbouring/neighbourhood uses. This does not equate every vicinity with the immediately adjacent house. The note truthfully quotes 辺り and 隣人; it does not claim that “edge” and “next door” are interchangeable or derive this pair merely through 町.

The counterpart options also remain defensibly wrong: 追 has 近 “near”, 週 “week”, 返 “give back; repay”; 側 has 内 “within, inner”, 右 “right”, 左 “left”; 辺 has 返, 込 “crowded; included”, 道 “road, way”. Neither a direction/compound partner nor a shared movement component establishes a correct alternative meaning.

`QuizBuilder.options` tests exclusions in both directions against the target and between chosen options, before admitting curated or fallback cards. Thus a single declaration blocks each added pair in either direction, including my original reduced-pool examples. It does not infer a transitive exclusion or restore an excluded option to reach four choices. No added pair also appears in either side's curated distractors.

Reading-option check for all 15 prompts:

The following are the actual curated candidate readings after respecting each option card's quiz-selection metadata. Alternatives separated by `/` are randomized possibilities from the same card, not simultaneous guaranteed choices.

| Target and correct displayed reading | Curated wrong-reading candidates |
|---|---|
| 随 ズイ | ギャク/ゲキ; リ; ドウ |
| 隠 かくす | さぐる/さがす; しめす; とらえる/とらわれる/とる/つかまえる/つかまる |
| 隣 となり | とおい; おく/おくまる/くま; うら |
| 雄 ユウ | ジャク; ドン; ジュウ/ニュウ |
| 雷 かみなり | しも; にじ; くも/ぐも |
| 霧 きり | こおり/ひ/こおる; あらし; ほし/ぼし |
| 項 コウ | ガク; チョウ; ヨ |
| 顕 ケン | タン; タイ; メツ |
| 飼 かう | とらえる/とらわれる/とる/つかまえる/つかまる; すてる; あらう |
| 飽 あきる | まよう; はじる/はじ/はじらう/はずかしい; いわう |
| 飾 かざる | けがす/けがれる/けがらわしい/よごす/よごれる/きたない; けずる; こわす/こわれる |
| 驚 おどろく | かなしい/かなしむ; いかる/おこる; よろこぶ/よろこばす |
| 鬼 おに | ほとけ; さる; くま |
| 鮮 セン | タン; two remaining slots use fallback |
| 黙 だまる | さけぶ; はしる; おどる |

These readings are not alternate readings of their targets in the inspected sources. The app preserves the attachment dash in displayed `-ぐも` and `-ぼし`; the table above gives their comparison keys.

`KanjiReadingQuiz` uses selected readings for candidate cards, but protects all target on/kun metadata, with kana folding, dot/dash removal and the implemented sound-change mutations. Meaning exclusions do not protect reading questions. Same-stem grouping explains the single selected prompts on 飽 and 飾; their other metadata readings remain protected.

鮮 really needs fallback: 腐 and 濁 disable on questions, despite having full on metadata. Its セン and protected variants cannot pass the candidate filter. The inspected audit's attested extras あたらしい and すくない are not drawable on candidates. No new wrong-reading collision was established in the inspected curated or reported fallback sets.

Dispositions:

- G1 - RESOLVED - 随:14,45,56,60 adds and documents 追 correctly; JMdict 1432410 and the actual reciprocal exclusion test support the fix.
- G2 - RESOLVED - 隣:14,44,50,54 adds and documents 側 correctly; JMdict 1403830/1555830 and the actual reciprocal exclusion test support the fix. The additional 辺 pair is acceptable as assessed above.
- GO1 - RESOLVED - 飽:33–34,56 supplies the lavish-use gloss and accurately scopes the independently verified Daijisen register note to the verb, not the adverb.
- GO2 - RESOLVED - 雄:39 adds the requested 英雄 example with its sourced reading/gloss; 雄大 and the named Joyo examples are also accurate.
- GO3 - DECLINE ACCEPTED - Shortening was optional editorial polish, not an established defect. The unchanged source-by-source Notes format is consistent within the inspected sample; broader style revision is unnecessary for this confirmation.

Verdicts:

- Correctness: CLEAN — all seven revised cards; no new actionable defect established.
- Scoped coverage: CLEAN — all seven revised cards; no card differs.
- Consistency and quiz safety: CLEAN — all 15 batch cards within the reviewed options and inspected client mechanics; 随 and 隣 no longer differ adversely.
- Comprehensibility: CLEAN — all seven revised cards; no card differs. Reference density remains nonblocking.

Confirmation: CONFIRMED — every response item is RESOLVED or DECLINE ACCEPTED, and no new actionable defect was established.

Findings: none.

Optional: none newly established.

Limits:

- Exact model/version identity is unavailable. The identification above does not claim a particular numbered GPT release.
- This is a changed-hunk confirmation, not a fresh exhaustive re-sourcing of every unchanged claim or previously reviewed asset. All changed quotations and source attributions were checked against actual supplied entries/extracts or public entries. The official PDF itself was not freshly downloaded/rendered; its supplied page extracts support the cited row claims.
- I inspected audit outputs against app code and actual option-card metadata; I did not regenerate them, scan the corpus, execute Kotlin/JVM tests, or run the app on a phone. Source accuracy, runtime acceptance of this exact installed build and measured beginner usability are different claims.
- The zero production/base-padded hits do not prove safety for every smaller pool or borrowing combination. The exposure report retains eight latent collisions: 隠 お/なまる; 雄 かつ/ゆ/よう; 飼 かい; 飽 あき; 飾 しか. It also reports three one-holder cases for name-only readings: 雄 ゆ, 雄 よう, 飼 かい. These are unchanged, previously considered cases, not new findings.
- Reading audits depend on their supplied attestation inventory and modeled pools. `reading-options.txt` omits some single-kanji lexical readings that `reading-exposure.txt` includes, such as 雷 なるかみ, 鬼 しこ and 黙 しじま. Neither audit discovers every dictionary reading. Sampling 100/200 seeds is not exhaustive runtime execution; the exposure report itself shows sampling missed some analytically drawable options.
- Meaning checks cannot establish semantic uniqueness merely through distinct titles or a zero-warning result. The revised exclusions require an exclusion-aware client; older clients ignore them. Unexamined fallback meaning pairs and arbitrary future content are not certified.
- The information-only meta-scan's substring matches do not establish missing learner prerequisites or citation defects by themselves. I did not expand unchanged vocabulary gaps into new findings.
- All tool calls were serial, exactly one per tool-using response. No agents, other sessions, background jobs, recursive listings, helper scripts, corpus scans or deliberate temporary files were used. An oversized combined read was automatically captured by the tool; that capture was not opened, and unseen output was not counted as reviewed. Only the requested report file was created.
- CLEAN means no actionable defect established within this stated scope, not exhaustive correctness.
