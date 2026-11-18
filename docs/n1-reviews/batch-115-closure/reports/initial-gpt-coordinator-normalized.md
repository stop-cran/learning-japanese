# B115 initial review — N1-B115-GPT-001

## Overall verdict
Verdict: NEEDS FIX

Snapshot: f36cd819dcf6ac8b4a3ee8ee29b6e750cd6f09ab; base: c7a7c8a75eec766d4d66ee172763e119075726ee. This is one independent, read-only first review in two phases, not a correction confirmation. Six findings concern direct meaning-choice exclusions. Correctness also has the bounded unresolved source claim described in L2.

## Facet verdicts
### Correctness
Verdict: UNVERIFIED
Basis: The complete supplied character records and 41 word families support the principal meanings, metadata and selected word readings. Fresh Daijisen reads support 康's health/readings and the classical 宇宙 explanation. The ancient 寸 reading き remains an unverified learner-visible assertion, rather than a reading established by the evidence opened here (L2).
### Scoped coverage
Verdict: CLEAN
Basis: All eight new cards retain and explain their complete frozen on/kun inventories, provide a linked selected-reading example, and distinguish the principal meaning branches without requiring exhaustive historical vocabulary. All eight word backlinks and the narrow 標 edit were compared with their complete destination articles. This is bounded textual coverage, not publication or device acceptance.
### Consistency/quiz safety
Verdict: NEEDS FIX
Basis: The full title index and actual comparison cards establish missing direct pairs in F1-F6. Existing exclusions cannot protect these pairs transitively. The curated meaning options themselves are defensible wrong answers; reading fallback evidence is limited to the supplied Python model.
### Comprehensibility
Verdict: CLEAN
Basis: Explicit modern-shape mnemonic labels, readable kana/glosses, whole-word sound-change explanations and contextual contrasts avoid invented etymology and constituent readings. O1 identifies a small attribution ambiguity, not a blocking comprehension defect.

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30; no re-views.
Extension chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10; no re-views.
I read evidence/title-index.txt source lines 1-1229 in full. Line 1 is "一 one" and line 1229 is "齢 age; years lived". The chain identifies its SHA-256 as 5e1df249d3913e11231f376ee7668c9ecf2151ae5bcdd729a187d4c64d6a09a2. This was an index screen, not a full read of all 1229 cards.
All 24 C card copies were read, including repo/kanji/康.md, whose supplied source hash equals the new snapshot/kanji/康.md hash. The other already-required comparison card was snapshot/kanji/標.md.
All ten check logs, the eight stroke JSON files, complete changed articles, unchanged ちょっと, and the supplied source-metadata, KANJIDIC2, JMdict, dictionary-index, Joyo-row, shape and provenance evidence were read through these chains.
Three web_fetch calls were made, each preceded by a public URL-and-purpose statement: https://www.weblio.jp/content/康 twice, then https://www.weblio.jp/content/宇宙 once. The first returned only a short displayed preview and a temporary-output notice; that temporary file was not opened. The smaller second response displayed the complete relevant 康 Daijisen heading and numbered senses. The third displayed the 宇宙 Daijisen entry and its classical-account supplement. The remaining truncated webpage tails were not read.

## Phase-1 D/E lists
D: D1 偉, D2 英, D3 著, D4 冠, D5 凌, D6 越, D7 勝, D8 抜, D9 労, D10 患, D11 悩, D12 害, D13 障, D14 辛, D15 時, D16 期, D17 浮, D18 記, D19 微, D20 量, D21 長, D22 程, D23 休, D24 快, D25 治, D26 暗, D27 薄, D28 雰, D29 示, D30 署, D31 章, D32 紙, D33 怖, D34 恐, D35 神, D36 術, D37 凝
E: E1 机, E2 高, E3 優, E4 表, E5 凶, E6 宇, E7 空, E8 健, E9 荒, E10 符
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 偉 | admirable; great | 卓 | Eminence versus outstanding greatness; repo/kanji/偉.md:19-22,32-42 explicitly teaches greatness, importance and excellence. | collision-needing-exclusion; F1 |
| D2 | 英 | English; outstanding | 卓 | The outstanding/excellent branch is explicit, independently of Britain; repo/kanji/英.md:19-22. | collision-needing-exclusion; F1 |
| D3 | 著 | write; remarkable | 卓 | Conspicuous, remarkable qualities overlap standing out; repo/kanji/著.md:19-21,34-41. | collision-needing-exclusion; F1 |
| D4 | 冠 | crown; peerless | 卓 | Foremost excellence is explicitly distinguished from headgear; repo/kanji/冠.md:21-25,46-47. | collision-needing-exclusion; F1 |
| D5 | 凌 | endure; surpass | 卓 | Surpassing/outdoing, not endurance, is the shared branch; repo/kanji/凌.md:21-26,37-47. | collision-needing-exclusion; F1 |
| D6 | 越 | cross over; exceed | 卓 | The displayed exceed branch overlaps excellence beyond others; crossing a mountain is not the reason; repo/kanji/越.md:3,19-22,40-42. | collision-needing-exclusion; F1 |
| D7 | 勝 | victory | 卓 | The requested superiority candidate actually displays winning; repo/kanji/勝.md:3,19-22,34-41. Metadata includes まさ.る and すぐ.れる at line 10 but does not itself prove ordinary use or its allocation. | harmless on the opened evidence; victory is not a demonstrated meaning of 卓, and further secondary-sense verification is limited by L5 |
| D8 | 抜 | extract | 卓 | The read card teaches extraction/removal, not excellence; repo/kanji/抜.md:19-22,34-39. 卓抜 alone does not allocate every whole-word gloss to 抜. | harmless on the opened evidence; no required pair established |
| D9 | 労 | labor; trouble | 厄 | Trouble/hardship is actually taught, not merely the presence of work; repo/kanji/労.md:19-22,31-37. | collision-needing-exclusion; F2 |
| D10 | 患 | be ill; suffer | 厄 | repo/kanji/患.md:19-21,38-39 ties the examples to illness. Misfortune can cause illness without meaning be ill. | harmless; consequence and condition are not sufficient evidence of interchangeable labels |
| D11 | 悩 | worry; be troubled | 厄 | repo/kanji/悩.md:19-21,31-45 describes experiencing/causing distress. The selected label denotes the response to trouble, rather than ill fortune itself. | harmless within the read scope; no direct pair established merely from the worry in 厄介's whole-word family |
| D12 | 害 | harm | 厄 | repo/kanji/害.md:19-22,34-37 concerns damage suffered. A calamity and its harmful consequence are related but not automatically the same meaning. | harmless within the read scope |
| D13 | 障 | obstruct; hinder | 厄 | repo/kanji/障.md:21-30,44-48 concerns obstruction and barriers, not bad luck. Its exclusions of 害 do not create a 厄 relation. | harmless; no transitive inference |
| D14 | 辛 | spicy; painful | 厄 | repo/kanji/辛.md:19-21,32-34 separates pain, hardship and flavor. A painful experience can accompany misfortune without painful being its lexical answer. | harmless within the read scope |
| D15 | 時 | time, hour | 宙 | Generic time in the displayed label matches the temporal sense explicitly retained in 宙; repo/kanji/時.md:3,19-23,35-42. | collision-needing-exclusion; F3, medium confidence because 宙 qualifies the classical context |
| D16 | 期 | period; term | 宙 | repo/kanji/期.md:19-23,35-38 specifies bounded periods and terms, unlike the classical past-to-present extent. | harmless; shared temporal topic alone does not require this pair |
| D17 | 浮 | float | 宙 | repo/kanji/浮.md:19-22,34-37 supplies the action in 宙に浮く; 宙 supplies the space in which it happens. | harmless; do not allocate 浮く's meaning to 宙 |
| D18 | 記 | record in writing | 宙 | repo/kanji/記.md:19-23,31-38 explicitly selects a written account; 宙's by-heart sense need not involve writing. | harmless; no direct displayed-label collision |
| D19 | 微 | minute; faint | 寸 | repo/kanji/微.md:21-27,64-73 explicitly teaches tiny/slight things and distinguishes the English time-unit homograph. | collision-needing-exclusion with 寸; F4 |
| D20 | 量 | quantity; amount | 寸 | repo/kanji/量.md:19-21,31-32,44 distinguishes an amount from the measuring operation; 寸 names a length unit or length/measurement. | harmless on the read evidence; a shared measuring verb does not make quantity/amount a demonstrated label for 寸 |
| D21 | 長 | long, chief | 寸 | repo/kanji/長.md:19-22,34-36 teaches long and chief. A length unit is not necessarily long; 寸 also explicitly means short/small. | harmless; no pair from sharing the stem length |
| D22 | 程 | extent | 寸 | repo/kanji/程.md:19-23,31-38 concerns degree, amount and span. The extent/plan gloss of 寸法 belongs to that whole word. | harmless on the read evidence; no unsupported transfer from 寸法 |
| D23 | 休 | rest | 康 | repo/kanji/休.md:19-23,29-37 teaches taking a break or being off work. That is distinct from soundness/peace as a state. | harmless on the read evidence; 小康's respite alone does not turn every 康 into rest |
| D24 | 快 | pleasant; agreeable | 康 | repo/kanji/快.md:19-21,31-32 concerns agreeable feelings; comfort overlaps descriptively but does not establish the displayed labels as health/peace synonyms. | harmless within the read scope |
| D25 | 治 | govern; heal | 康 | repo/kanji/治.md:19-22,34-44 concerns curing/recovering, rather than health itself; 小康 does not promise recovery. | harmless; process and state remain distinct |
| D26 | 暗 | dark | 漠 | repo/kanji/暗.md:19-23,35-36 teaches lack of light, not vague definition. Its memorization example also does not make dark a label for 宙. | harmless on the read evidence |
| D27 | 薄 | thin; dilute | 漠 | repo/kanji/薄.md:19-21,30-39 concerns thickness, concentration and fading. Indistinctness is not necessarily dilution. | harmless on the read evidence; secondary faintness merits the bounded limit in L5 |
| D28 | 雰 | mist; atmosphere | 漠 | repo/kanji/雰.md:21-30 distinguishes misty air from ambience. A vague idea or desert is neither mist nor atmosphere. | harmless; related haziness is not enough |
| D29 | 示 | indicate | 票 | repo/kanji/示.md:19-22,31-39 teaches showing/indicating, while 票's sign/label is the marked object. The shared component proves nothing semantic. | harmless on the read evidence; no automatic pair from 示 being excluded by 標 |
| D30 | 署 | sign; government office | 票 | The displayed unqualified English sign collides with 票's sourced sign sense, despite 署's signing-a-name use; repo/kanji/署.md:3,19-21,39-42. | collision-needing-exclusion; F5 |
| D31 | 章 | chapter; badge | 票 | repo/kanji/章.md:19-21,35-40 establishes chapters and insignia; it does not establish ballot/ticket or ordinary label as the same item. | harmless; identifying functions alone do not make badges and tickets synonyms |
| D32 | 紙 | paper | 票 | repo/kanji/紙.md:19-21,31-39 names a material and paper products; a ballot need not be paper. | harmless; material is not the vote |
| D33 | 怖 | frightening | 魔 | repo/kanji/怖.md:19-22,33-39 supports frightening, matching the complete bare 魔 entry's dreadful/terrible adjectival branch. | collision-needing-exclusion; F6 |
| D34 | 恐 | fear; awe | 魔 | repo/kanji/恐.md:19-22,31-38 distinguishes fear from something terrifying. The displayed fear/awe names an emotion, unlike 魔's dreadful modifier. | harmless on the displayed-label evidence; not inferred from the 怖 pair |
| D35 | 神 | deity | 魔 | repo/kanji/神.md:19-23,31-33,43-46 distinguishes a deity and mental spirit; neither category is automatically a demon. | harmless; no universal equation of supernatural beings |
| D36 | 術 | technique | 魔 | repo/kanji/術.md:19-23,34-40 teaches a general technique; in 魔術 the field is supplied by the whole compound. | harmless; technique does not by itself mean magic |
| D37 | 凝 | congeal; become absorbed | 魔 | repo/kanji/凝.md:21-26,37-38,58-60 concerns becoming absorbed or applying effort; bare 魔 has an obsessed-person suffix. | harmless on the read evidence; a person label and an absorption process are not automatically interchangeable |
| E1 | 机 | desk; writing table | 卓 | repo/kanji/机.md:19-21,38-40 confirms the actual furniture overlap. | already handled by 卓's direct 机 exclusion |
| E2 | 高 | high, expensive | 卓 | repo/kanji/高.md:19-22 confirms high/tall; expensive is not the reason. | already handled by 卓's direct 高 exclusion |
| E3 | 優 | gentle; superior | 卓 | repo/kanji/優.md:19-23,35-42 confirms excellence; gentleness is a separate branch. | already handled by 卓's direct 優 exclusion |
| E4 | 表 | surface; chart | 卓, 票 | repo/kanji/表.md:19-22,35-41 explicitly teaches a data table. | already handled for 卓 through its 表 exclusion; harmless for 票, since a chart is not a ballot |
| E5 | 凶 | ill fortune; evil | 厄, 魔 | repo/kanji/凶.md:21-25,49-52 separates ill fortune from evil, supporting the two direct comparisons independently. | already handled by both new cards' direct 凶 exclusions |
| E6 | 宇 | eaves; space | 宙 | repo/kanji/宇.md:3,19-21,29-34 supports space and the shared 宇宙 example. | already handled by 宙's direct 宇 exclusion |
| E7 | 空 | sky; empty | 宙 | repo/kanji/空.md:19-22,33-39,43-54 supports sky/available space; its read text does not establish the separate memory sense. | already handled for the demonstrated sky overlap; memory support instead comes from the bare 宙 dictionary family |
| E8 | 健 | healthy; robust | 康 | repo/kanji/健.md:21-26,38-43 establishes health directly, while preserving robustness distinctions. | already handled by 康's direct 健 exclusion |
| E9 | 荒 | rough; wild; laid waste | 漠 | repo/kanji/荒.md:19-21,30,43 supports a wasteland comparison, without claiming every desert was deliberately devastated. | already handled by 漠's direct 荒 exclusion |
| E10 | 符 | token; sign; charm | 票, 魔 | repo/kanji/符.md:19-21,31-36,41 supports sign/ticket and the displayed charm ambiguity. | already handled by 票 and 魔 independently; this does not establish a 票/魔 pair |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 卓 | CLEAN | CLEAN | NEEDS FIX | CLEAN | snapshot/kanji/卓.md:1-71; KANJIDIC2 卓 record; JMdict 1358530,1415580,1415590,1415610,1415660,1415690; F1; D1-D8 and E1-E4. |
| 厄 | CLEAN | CLEAN | NEEDS FIX | CLEAN | snapshot/kanji/厄.md:1-70; KANJIDIC2 厄 record; JMdict 1537810,1537820,1537870,1537910,1537930; F2; D9-D14 and E5. |
| 宙 | CLEAN | CLEAN | NEEDS FIX | CLEAN | snapshot/kanji/宙.md:1-70; JMdict 1171300,1426110,1893710,1956660,2272370; fetched Daijisen 宇宙 supplement; F3; D15-D18 and E6-E7. |
| 寸 | UNVERIFIED | CLEAN | NEEDS FIX | CLEAN | snapshot/kanji/寸.md:1-70; JMdict 1163930,1163940,1373700,1373750,1373810,1700300,1956530; unchanged ちょっと; F4 and L2. |
| 康 | CLEAN | CLEAN | CLEAN | CLEAN | snapshot/kanji/康.md:1-71; JMdict 1256170,1348080,2132790; fetched Daijisen 康 senses 1-2 and reading heading; D23-D25 and E8. |
| 漠 | CLEAN | CLEAN | CLEAN | CLEAN | snapshot/kanji/漠.md:1-68; JMdict 1278640,1475790,1593800,2843550; D26-D28 and E9; no new exclusion established from darkness, dilution or mist alone. |
| 票 | CLEAN | CLEAN | NEEDS FIX | CLEAN | snapshot/kanji/票.md:1-69; JMdict 1202910,1442410,1447320,1454610,1489320; F5; D29-D32, E4, E10 and required 標/印. |
| 魔 | CLEAN | CLEAN | NEEDS FIX | CLEAN | snapshot/kanji/魔.md:1-73; JMdict 1152510,1524130,1524220,1524230,1633990,1640830; F6, O1; D33-D37 and E5/E10. |

**Index and direct-pair assessment.** Each title sense and the supplied ordinary secondary senses were screened against the complete index, including table/chart, eminent/outstanding/remarkable/peerless/surpass, misfortune/trouble, space/sky/air/memory/time, small/minute/measure/length, health/ease/peace, desert/wide/vague/obscure, ballot/ticket/label/sign, and demon/magic/evil/dreadful/obsession. I did not treat a shared English stem or a compound containing both characters as sufficient by itself. The D/E table records the actual-card adjudications; excluded targets not read are separately limited in L4.

卓's 机/高/優/表 pairs are evidenced and handled. Its existing 台 and 超 guards are present, but do not imply any of the six missing F1 pairs. 厄's 凶 pair is handled; its 難/困/苦/悪 references do not transitively guard 労. 宙's 宇/空 guards are evidenced; the temporal label needs its own decision in F3 independently of 間. 寸/微 is absent in both directions even though both exclude 小/少/細. 康/健 is handled; none of the read comfort/rest/healing comparisons establishes an additional required pair. 漠/荒 is handled and 広 is already explicitly named; its other requested comparisons do not establish an unguarded displayed-label synonym. 票/標 and 票/印 are directly handled by 票, not by propagation through other sign cards. 魔/凶 and 魔/符 are handled; neither protects the dreadful/怖 pair.

**C options: title agreement, meaning and readings.** All following displayed titles agree with their entries in evidence/title-index.txt:1-1229. I assessed them as choices for the specified new target, not as an independent historical or full-corpus review of these older cards.

For 卓, 日 "sun, day", 車 "car, vehicle", 十 "ten" are wrong meanings for table/eminent, and mutually distinct. Their full on lists are ニチ/ジツ, シャ, ジュウ/ジッ/ジュッ, none タク or the supplemental ショク (repo/kanji/日.md:1-11,30-40; repo/kanji/車.md:1-11,25-30; repo/kanji/十.md:1-11,25-32). 日's English sun does not collide with 寸's explicitly qualified "sun (length unit)" merely because those English letters match; 日 is not a curated option for 寸.

For 厄, 厚 "thick; cordial", 原 "original; plain", 印 "stamp; mark" are distinct wrong meanings; 厄介's care/dependence sense must not be reassigned to 厄 to manufacture a cordiality collision. Their on lists コウ, ゲン, イン do not overlap ヤク (repo/kanji/厚.md:1-11,19-32; repo/kanji/原.md:1-11,19-31; repo/kanji/印.md:1-11,19-34). 印 is separately a valid 票 comparison, already guarded, not an E request.

For 宙, 宅 "residence", 守 "guard; obey", 定 "determine; settle" are wrong meanings. In 宙に浮く, the unsettled sense of the whole expression does not make settle a meaning of 宙; polarity and lexical boundaries matter. Their on lists タク, シュ/ス, テイ/ジョウ do not overlap チュウ (repo/kanji/宅.md:1-11,19-30; repo/kanji/守.md:1-11,19-33; repo/kanji/定.md:1-11,19-34).

For 寸, 村 "village", 付 "attach", 寺 "Buddhist temple" are distinct wrong meanings despite the shared component. ソン, フ, ジ do not overlap スン (repo/kanji/村.md:1-11,19-30; repo/kanji/付.md:1-11,19-34; repo/kanji/寺.md:1-11,19-30). These readings also do not supply the claimed ancient き, whose source verification is L2.

For 康, 庫 "storehouse", 床 "floor; bed", 庭 "garden; yard" are distinct wrong meanings. Resting in a bed is not the meaning health. コ/ク, ショウ, テイ do not overlap ordinary コウ (repo/kanji/庫.md:1-11,19-31; repo/kanji/床.md:1-11,19-31; repo/kanji/庭.md:1-11,19-32). 庫's コ does coincide with a 康 nanori in evidence/kanjidic2-records.xml:364-368; names are explicitly outside this review's ordinary-reading contract, so I do not call that a demonstrated ordinary-reading defect.

For 漠, 漢 "Chinese, Sino-", 暮 "dusk; livelihood", 湖 "lake" are distinct wrong meanings. Darkness at dusk and vague outlines are associated phenomena, not synonymous labels. カン, ボ, コ do not overlap バク (repo/kanji/漢.md:1-11,19-31; repo/kanji/暮.md:1-11,19-34; repo/kanji/湖.md:1-11,19-31). 暮's legacy full on metadata retains ボ even though its table focuses on kun examples; this batch did not introduce that older-card structure.

For 票, 栗 "chestnut", 要 "necessity; essentials", 祭 "festival; ritual; worship" are distinct wrong meanings. 栗's selected on list is empty, while 要 supplies ヨウ and 祭 サイ, neither ヒョウ (repo/kanji/栗.md:1-14,26-33; repo/kanji/要.md:1-11,19-35; repo/kanji/祭.md:1-11,19-33). Thus the third wrong on-reading must come from fallback, not from an invented 栗 reading.

For 魔, 摩 "rub; chafe", 鹿 "deer", 康 "health; well-being" are distinct wrong meanings. 摩 selects マ, identical to the answer, and must not become a wrong reading; 鹿 has no selected on reading, leaving only 康's コウ as a curated wrong on reading (repo/kanji/摩.md:1-14,29-37; repo/kanji/鹿.md:1-14,30-42; repo/kanji/康.md:1-14,38-47). Meaning exclusions do not govern this reading behavior. The supplied model explicitly reports two fallback slots for 魔, not three usable curated wrong readings.

**Reading and lexical evidence.** Every new card has one full on reading and no frozen kun reading; the explicit quiz subsets preserve that inventory and select the supported compound reading. Joyo text rows corroborate タク, ヤク, チュウ, スン, コウ, バク, ヒョウ, マ (evidence/joyo-rows.json:5-78). JMdict confirms the selected spellings/readings, including やっかい and すんぽう. The っ in 卓球 and 厄介, both long vowels in 投票, and ぴょう in 伝票 are taught as whole-word or contextual changes, not fabricated independent source readings.

The complete 卓 family restricts the offering-table/incense-burner senses to しょく and its counter sense to たく (evidence/jmdict-families.xml:364-405); the card preserves these distinctions. 一寸/いっすん and usually-kana ちょっと belong to separate entries, with rare spellings and kana-only alternatives retained rather than silently redistributed (evidence/jmdict-families.xml:37-143; repo/words/ちょっと.md:15-24). 厄払い uses the ordinary listed spelling, not its search-only aliases. 砂漠 retains 沙漠 as a rare alternative. 漠 and 漠然 retain their と/たる grammar. 魔術's stage-magic sense is distinct from sorcery, and 悪魔's Christianity/Buddhism fields are sense-local, not claims about every fictional demon. No missing exact 康 or 康健 dictionary query was treated as proof of linguistic impossibility.

**Existing changes.** diffs/existing.diff:20-126 contains exactly eight wrappers adding the new character links, with no word metadata, identity, reading, level, existing word exclusion, example or other prose change. They agree with the full articles at snapshot/words/食卓.md:24, snapshot/words/厄介.md:25, snapshot/words/宇宙.md:27-30, snapshot/words/寸法.md:29-32, snapshot/words/健康.md:29-31, snapshot/words/砂漠.md:26-29, snapshot/words/投票.md:24 and snapshot/words/悪魔.md:24. The new cards reciprocally link their declaring words in their selected reading rows. checks/linkplan.txt:1 independently reports eight expected pairs and eight added links.

The 標 edit adds its component link to 票 and removes only the now-false assertion that 票 lacks a card (diffs/existing.diff:1-19; snapshot/kanji/標.md:27,53). Its identity, full/selected readings and prior exclusions are unchanged. ちょっと is supporting unchanged evidence, not a ninth modified or new word article. The present chain does not authorize a full review of every older article linked incidentally from these pages.

**Stroke and check evidence.** All eight stroke JSON records name the expected character, schema 1, the common KanjiVG revision 70a0b7ae0c18ceb5cb358274b029cce0234a43bc and counts 8/4/8/3/11/13/11/21. Their visible ordered IDs agree with those counts and with the cards, KANJIDIC2 and evidence/shape-evidence.json:1-82. Radical metadata is consistent; 漠 explains 水/氵. The prose labels its component pictures as mnemonics and does not deny the existence of phonetic components merely because the field is omitted. These are textual/structural observations, not fresh geometric acceptance.

The logs report zero lint/validation errors, 431 successful unit tests, identical manifest/rebuild summary versions 8c5b266340bd34bc with 8680 runtime files, and a local budget estimate of 8702 entries and 45998990 inflated bytes (checks/lint.txt:1-2; checks/validate.txt:1; checks/unittest.txt:13-17; checks/manifest.txt:1; checks/manifest-rebuild.txt:1; checks/budget.txt:1). Vocabulary coverage remains 2122/2431 at pilot stage (checks/vocabulary.txt:1), not a claim of complete N1 coverage. None of these is linguistic proof or evidence of an exact published archive test.

## Findings
### F1: 卓 is missing six direct excellence comparisons
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: snapshot/kanji/卓.md:3; snapshot/kanji/卓.md:14; snapshot/kanji/卓.md:23-25; snapshot/kanji/卓.md:56-60; repo/kanji/偉.md:1-22; repo/kanji/偉.md:32-42; repo/kanji/英.md:1-22; repo/kanji/著.md:1-21; repo/kanji/著.md:34-41; repo/kanji/冠.md:1-25; repo/kanji/冠.md:46-47; repo/kanji/凌.md:1-26; repo/kanji/凌.md:37-47; repo/kanji/越.md:1-22; repo/kanji/越.md:40-42; repo/docs/content-format.md:102-118
- Evidence: 卓's displayed eminent and explicit standing-out/excellence branch overlap 偉's great/outstanding, 英's outstanding/excellent, 著's remarkable, 冠's foremost/peerless, and the surpass/exceed branches of 凌 and 越. The English furniture branch does not remove these alternative defensible descriptions. None of the six comparison cards declares 卓; 卓 names only 机, 台, 高, 優, 超 and 表. In particular, excluding 優 or 超 does not exclude other excellence cards.
- Required change: Add direct pairs 卓/偉, 卓/英, 卓/著, 卓/冠, 卓/凌 and 卓/越 on either endpoint, preserving existing guards. Treat these as semantic-choice protection, not a claim that their Japanese compounds are freely interchangeable.

### F2: 厄 lacks the direct trouble comparison with 労
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: medium
- Citations: snapshot/kanji/厄.md:3; snapshot/kanji/厄.md:14; snapshot/kanji/厄.md:23-27; snapshot/kanji/厄.md:54-57; repo/kanji/労.md:1-22; repo/kanji/労.md:31-37; evidence/jmdict-families.xml:708-729; evidence/jmdict-families.xml:731-770; repo/docs/content-format.md:95-118
- Evidence: 厄 teaches misfortune/adversity and its trouble contribution, while 労 actually displays trouble and teaches 苦労 as hardship. Trouble is a plausible broad English answer for the misfortune/trouble branch of 厄, not merely a shared work-related topic. Neither endpoint guards the pair; the existing 苦/困/難 guards do not apply transitively. This finding does not equate the care sense of the complete 厄介 word with labor.
- Required change: Add the direct 厄/労 exclusion, retaining the existing exclusions and the distinction between misfortune, labor and receiving care.

### F3: 宙's retained time sense is not guarded against 時
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: medium
- Citations: snapshot/kanji/宙.md:3; snapshot/kanji/宙.md:14; snapshot/kanji/宙.md:54-57; evidence/source-metadata.json:65-72; repo/kanji/時.md:1-23; repo/kanji/時.md:35-42; repo/docs/content-format.md:102-118
- Evidence: The source explicitly includes interval of time, and the new card teaches 宙 as time extending from past to present in the classical 宇宙 account. The actual 時 label contains generic time, not only clock hour. The warning that 宙 is not an ordinary replacement in clock time narrows usage but does not make the unqualified English time answer false for the explicitly retained sense. The freshly read Daijisen 宇宙 supplement supports the temporal account. Neither card directly excludes the other. Confidence is medium because this branch is contextually qualified rather than the modern card's primary focus.
- Required change: Add a direct 宙/時 guard while retaining the valuable classical-versus-clock-time distinction; do not rely on the separate 間 exclusion or erase the sourced temporal explanation.

### F4: 寸 and 微 remain eligible together despite explicit smallness
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: snapshot/kanji/寸.md:3; snapshot/kanji/寸.md:14; snapshot/kanji/寸.md:23-26; snapshot/kanji/寸.md:58-61; repo/kanji/微.md:1-27; repo/kanji/微.md:64-73; evidence/jmdict-families.xml:945-962; repo/docs/content-format.md:102-118
- Evidence: 寸 displays small and teaches smallness; 微 displays minute and explicitly explains that as very small or tiny. This is a direct semantic overlap, not the unrelated English minute time-unit homograph. Both cards exclude several common smallness targets, but neither lists the other, and shared 小/少/細 exclusions are not transitive.
- Required change: Add the direct 寸/微 pair on either card, preserving both the unit explanation and existing smallness exclusions.

### F5: 票's sign sense collides with the displayed English sign on 署
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: snapshot/kanji/票.md:3; snapshot/kanji/票.md:14; snapshot/kanji/票.md:23-26; snapshot/kanji/票.md:53-55; evidence/source-metadata.json:159-164; repo/kanji/署.md:1-21; repo/kanji/署.md:39-42; repo/docs/content-format.md:102-118
- Evidence: 票's supplied character senses include sign, and the card explicitly teaches a sign/label branch. 署's actual English title begins sign without specifying the verb sense, even though its prose correctly teaches signing a name. Thus the English choice is defensible for the preserved 票 sense. This is an English-label ambiguity, not evidence that a ballot is a signature. Neither endpoint excludes the other; excluding 標, 印 or 符 does not protect this additional sign pair.
- Required change: Add the direct 票/署 exclusion, or make the displayed signing label unambiguously verbal and re-evaluate the resulting exact label. Preserve the Japanese distinction and existing direct guards.

### F6: 魔's ordinary dreadful branch leaves 怖 as a defensible wrong answer
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: snapshot/kanji/魔.md:3; snapshot/kanji/魔.md:14; snapshot/kanji/魔.md:23-31; evidence/jmdict-families.xml:856-887; repo/kanji/怖.md:1-22; repo/kanji/怖.md:33-43; repo/docs/content-format.md:108-118
- Evidence: The complete bare 魔 family has a separate, unflagged no-modifier sense glossed dreaded, terrible, awful and dreadful. 怖's actual displayed title is frightening, supported by its scary/fear examples. This establishes a lexical alternative, not merely the stereotype that demons cause fear. Neither card excludes the other. 魔's 妖/魅/怪/悪/凶/符 guards do not cover 怖, and the person-obsessed suffix is a separate sense.
- Required change: Add the direct 魔/怖 exclusion based on this ordinary secondary sense, without making every supernatural or fear-related character part of a transitive exclusion group.

## Optional points
### O1: Make the source of the religious sense labels explicit
- Facet: Comprehensibility
- Severity: optional
- Confidence: high
- Citations: snapshot/kanji/魔.md:64-66; snapshot/words/悪魔.md:13-34; evidence/jmdict-families.xml:17-35
- Evidence: The linked 悪魔 article does distinguish a fictional being from figurative description, but it does not itself label Christianity/Satan and Buddhism/Māra. Those separately labelled senses are in JMdict. The pronoun Its after the article reference can be read as attributing those labels to the linked article rather than to the word's dictionary entry.
- Suggestion: Say explicitly that JMdict labels those two senses separately. No expansion of the older 悪魔 article or universal religious comparison is needed.

## Limits
- L1: This is bounded textual review of the immutable chain-delivered snapshot. Raw KanjiVG SVGs, the binary Joyo PDF and all other packet assets outside the core/extension chains were unread. No packet file was opened directly. Source headers and hashes identify the supplied evidence; I did not recompute hashes, regenerate strokes, render geometry or inspect fresh PDF glyphs.
- L2: snapshot/kanji/寸.md:45 asserts that Daijisen records ancient 寸 き. Neither the supplied KANJIDIC2 record nor the complete JMdict 寸 family establishes that pronunciation. The reading audit repeats it with the helper label card text, which is not independent lexical verification. The exact Daijisen 寸 entry was not fetched, so this consequential source-only reading assertion is UNVERIFIED, not rejected as false. The modern unit, approximate 3.03 cm and selected スン are supported separately.
- L3: The three permitted fetches were exhausted. The first 康 fetch produced a tool-managed temporary file but exposed only a short preview; I neither requested a scratch artifact nor opened or searched that temporary file. The second fetch actually exposed 康's health, peace and supplemental やすい/やすらか heading; the third exposed the 宇宙 classical supplement. Their remaining webpage tails and the other public character-entry pages were unread. Fetched 康 also lists a large-road sense; I did not turn that specialized branch into an unrequested historical-completeness requirement.
- L4: Existing exclusion targets whose full cards were not requested/read are 台, 超, 難, 困, 苦, 悪, 天, 気, 間, 覚, 小, 少, 短, 細, 計, 測, 安, 平, 寧, 楽, 和, 静, 凪, 広, 札, 券, 妖, 魅, 怪. Their titles were read in the full index and their exact guards in the new cards, but that is not full secondary-sense adjudication. 標 and 印 were read in the core, not omitted or misclassified as E; all ten actual E requests were fulfilled.
- L5: Additional identified but unread comparison candidates are 軽 for 寸's slight/small branch; 識 and 知 for 宙's knowledge/memory branch; 強, 剛, 勁 and 力 for possible 康 soundness/robustness comparisons surfaced by 健; 道, 路 and 通 for the specialized large-road 康 sense exposed after selection. They are not silently covered by another exclusion and were not added after the final D/E list. No defect is asserted from their index titles alone. The read 微/漠 and 薄/漠 faintness relation, and 勝/抜 excellence beyond the passages actually read, would need additional lexical allocation evidence before promoting them into further direct-pair findings. They remain limits, not claims of comprehensive synonym safety.
- L6: The reading audit models N1 and All shipped pools and Starter borrowing under its stated restricted scenarios, with exact modeled reachability and 100 sampled seeds. It reports zero modeled ordinary-reading hits and four latent collisions, not universal runtime safety (checks/reading-exposure-final.txt:1-8,10-25,43-58,61-80,82-97,114-144). Some lines additionally try one holder at a time; this does not establish arbitrary multi-borrow Starter behavior. Custom/caller-built pools, current Kotlin execution, JVM/Gradle tests, emulator/native/phone acceptance and compatibility with installed APK 5c000bd remain unverified. I ran none of those operations; JVM/emulator work remains on hold.
- L7: checks/reading-exposure-final.txt:1 reports 75 preserved families, whereas the chain's dictionary packet contains 41 complete families. I read the supplied 41 and the audit output; I did not independently reconstruct the audit's larger source collection. Nanori coincidences, such as 康/庫 コ and the reported 寸 ス, are explicitly distinct from ordinary on/kun defects.
- L8: The supplied checks are historical host outputs, not fresh execution by this reviewer. Matching manifest summary lines are not a fresh per-entry hash comparison, and the budget estimate is not exact public-ZIP acceptance. Source-row IDs and provenance were read; the raw frozen kanjiapi membership file was not. Modern community labels are not inferred from old KANJIDIC JLPT numbers. These eight drafts do not increase the stated published total of 225 N1 additions plus six N2 study placements.
- L9: The C reads were scoped to actual title agreement, defensibility as options, reading overlap and directly relevant comparisons. They do not certify all historical claims or all old-card reading tables, nor the rest of the 5083-word corpus. No content was edited, no confirmation round was performed, and no other review, rationale or session history was consulted.
- L10: The runtime identifies this reviewer as GPT-6 Astra, model ID gpt-6-astra. This is the execution identity available in this session, not an independently inspected provider billing log. No additional reviewer or delegated agent was used.
