# B113 independent first content review — run N1-B113-CLAUDE-009

Snapshot: fdec1c02f9b02f29659b56551cd0a1fd927cced1 (base c42d80306926e99ec6436c80c0574e3a858a4286; packet SHA256SUMS.json aea68d97bfc52944dc6e63fc309e47d08c328990c997cc73fb651ab6b73554d0). Committed packet content only, read through byte-exact chains. Model: the runtime identifies this agent as Claude Opus 5.5 (claude-opus-5.5); the execution-model identity is not independently verifiable from inside this pass.

## Scope

Read by chain, one view per segment, in order, no re-views:

- Required chain b113-claude-v4, segments 1-49 (each read once, in full; no truncated outputs). Appendix segments 50-56 (KanjiVG SVGs) were NOT read, by instruction.
- Extension chain b113-claude-m6a-ext, segments 1-10 (each read once, in full). The coordinator reported no nonexistent entries.
- No web_fetch calls were made (0 of 3 used). No other local file was opened.

Covered in the required chain: REVIEW.md; packet.json; rubric\copilot-instructions.md (1-274); rubric\content-structure.instructions.md (1-85); repo\docs\content-format.md lines 1-139 only; snapshot\kanji for the 15 new cards plus 応 and 統; snapshot\strokes for the 15 new kanji; diffs\existing.diff (1-420); all 30 changed snapshot\words articles; all eleven checks; evidence source-metadata.json, kanjidic2-records.xml, jmdict-families.xml, dictionary-index.json, joyo-rows.json, provenance.json; the title-index supplement (source lines 1-1206; confirmed line 1 is "一 one" and line 1206 is "齢 age; years lived"); all 45 curated C distractor cards.

Unread / partial: KanjiVG SVG appendix (segments 50-56); the binary Joyo PDF (only the extracted joyo-rows.json was read); content-format.md lines 140-1419; Digital Daijisen / Weblio pages (no fetch); all other repo\kanji and repo\words files not listed in the D/E table below.

### Phase-1 lists as sent (final; none nonexistent)

```
D1 種 - 系: kind/type grouping (系 "-type", 類 "kind; category" excluded)
D2 般 - 系: "kind; category" duplicates excluded 類 for system/type
D3 列 - 系, 隊: row/series/line (系列 series; 隊列 formation; 線/並/順 excluded)
D4 機 - 系: mechanism vs system
D5 話 - 討: talk/speak vs discuss (談 excluded)
D6 争 - 討: contend; dispute vs debate/attack
D7 評 - 討: appraise vs critique/examination (批 excluded)
D8 試 - 討: test vs examination (検討)
D9 想 - 討: thought/conception vs consideration (考 excluded)
D10 察 - 討: observe; infer vs examine/investigate
D11 破 - 討: break vs destroy/defeat (討つ)
D12 当 - 徹: hit; be on target vs "strike home" (打/撃 excluded)
D13 射 - 徹: shoot vs strike home/pierce (撃 "shoot" excluded)
D14 突 - 徹: thrust vs pierce
D15 済 - 徹: settle; finish vs completion (了 "completion; settling" excluded)
D16 終 - 徹: end; finish vs carry through to the end
D17 夕 - 徹: evening vs all night (晩 "evening; night" excluded)
D18 起 - 徹: wake vs sit up all night
D19 宿 - 徹: lodging vs all-night stay (泊 excluded)
D20 過 - 徹: go beyond vs pass through/reach all the way
D21 造 - 誕, 握: make; construct vs creation/making; form by hand (作 excluded)
D22 製 - 誕, 握: manufacture vs making; mold (作 excluded)
D23 始 - 誕: begin vs origin/coming into existence (元/原/創 excluded)
D24 和 - 寧: harmony vs peaceful
D25 尊 - 寧: revere; esteem vs courtesy (敬 excluded)
D26 拝 - 寧, 謝: bow in respect vs courtesy/thanks (礼 "bow; thanks" excluded)
D27 優 - 寧: gentle vs polite/peaceful
D28 困 - 謝: be in difficulty vs dated "be at a loss; be stumped"
D29 給 - 謝, 恩: pay; bestow vs remuneration (謝礼)/favor bestowed (恩給)
D30 辞 - 謝: resign vs decline (謝絶)
D31 否 - 謝: deny; negate vs refuse
D32 返 - 恩: give back; repay vs debt of gratitude/repaying a favor
D33 盤 - 盆: board; disc vs tray/platter
D34 編 - 縫: knit vs sew; stitch
D35 管 - 握: supervise vs control (御/治 excluded)
D36 扱 - 握: handle vs grip/handle (握り)
D37 防 - 援: defend vs save/protect (保 excluded)
D38 仕 - 援: serve, attend vs assist
D39 願 - 需: wish; petition vs request (求/頼 excluded)
D40 望 - 需, 飢: hope vs want/hunger for (欲 excluded)
E1 派 - 隊 "party" vs faction; 隊 excludes 党 but not 派; need text to decide consistency
E2 制 - 握 "control/dominate"; 握 excludes 御/治/圧 but not 制
E3 刺 - 縫 KANJIDIC "embroider"/stitch vs pierce (刺繍); decide whether 縫–刺 needed
E4 凌 - 慢 exclusion relies on 凌 meaning "endure" (我慢)
E5 節 - 慢 exclusion relies on 節 "restraint" sense
E6 負 - 慢/謝 exclusions rely on "bear a burden"/"lose" senses; also 恩 debt
E7 乏 - 飢 "scarce; lacking" vs shortage; also 需 need
```

Nonexistent entries: none.

### Every D/E card read (extension chain)

| Card | Displayed title | Related new card | Reason requested | Disposition |
| --- | --- | --- | --- | --- |
| 種 | seed; kind | 系 | kind/type | Harmless vs displayed "lineage; system"; mirrors 系–類 rationale (O3) |
| 般 | general; kind; category | 系 | kind/category | Harmless; same "kind; category" as excluded 類 (O3) |
| 列 | row; queue | 系, 隊 | series/formation | Harmless; "queue" is not squad/lineage |
| 機 | mechanism; opportunity | 系 | mechanism/system | Harmless |
| 話 | talk, speak | 討 | discuss | **Collision needing exclusion** (F1); starter-tagged (種 none) |
| 争 | contend; dispute | 討 | debate/attack | **Collision needing exclusion** (F1) |
| 評 | appraise; reputation | 討 | critique/examination | Borderline; 評 itself excludes 批/論/議; optional (O4) |
| 試 | test; try | 討 | examination | Harmless (test ≠ consider) |
| 想 | thought; conception | 討 | consideration | Borderline parity with excluded 考; optional (O4) |
| 察 | observe; infer | 討 | examine/investigate | Borderline parity with excluded 査/調/診; optional (O4) |
| 破 | tear; break | 討 | destroy/defeat | Harmless vs displayed "attack; discuss" |
| 当 | hit; be on target | 徹 | "strike home" | Harmless vs displayed title; inconsistent with 徹's own 打/撃 rationale (O2) |
| 射 | shoot; shine into | 徹 | shoot/pierce | Harmless; same O2 inconsistency |
| 突 | thrust; sudden | 徹 | pierce | Harmless |
| 済 | settle; finish | 徹 | completion | Harmless; parity with 了 noted (O2) |
| 終 | end; finish | 徹 | carry to the end | Harmless |
| 夕 | evening | 徹 | all night | Harmless; parity with 晩 noted (O2) |
| 起 | wake; rise | 徹 | sit up all night | Harmless |
| 宿 | lodging | 徹 | overnight stay | Harmless |
| 過 | exceed; go beyond | 徹 | pass through | Harmless |
| 造 | make; construct | 誕, 握 | making | Harmless vs displayed titles; parity with excluded 作 (O5) |
| 製 | manufacture; made of | 誕, 握 | making | Harmless (its own card already excludes 作/造/産/創) |
| 始 | begin, start | 誕 | origin | Borderline; parity with excluded 創/元 (O5) |
| 和 | harmony; Japanese style | 寧 | peace | Borderline-plausible collision; teaches 平和 peace (O1) |
| 尊 | revere; esteem | 寧 | courtesy | Borderline; parity with excluded 敬 (O1) |
| 拝 | worship; bow in respect | 寧, 謝 | courtesy/thanks | Borderline; parity with excluded 礼 (O1) |
| 優 | gentle; superior | 寧 | polite/gentle | Harmless-borderline |
| 困 | be in difficulty | 謝 | dated "be at a loss" | Harmless (dated sense not displayed); see O2 |
| 給 | pay; bestow | 謝, 恩 | remuneration/bestow | Harmless |
| 辞 | words; resign | 謝 | decline | Harmless ("resign" ≠ refuse) |
| 否 | deny; negate | 謝 | refuse | Harmless |
| 返 | give back; repay | 恩 | repay a favor | Harmless (repaying ≠ the favor) |
| 盤 | board; disc | 盆 | tray/platter | Borderline; both 皿-key flat vessels; 盤 itself excludes 皿/板 (O6) |
| 編 | knit; compile | 縫 | knit vs sew | Harmless (distinct craft; 縫う article contrasts 編む) |
| 管 | pipe; supervise | 握 | control | Harmless |
| 扱 | handle; deal with | 握 | handle | Harmless |
| 防 | defend; ward off | 援 | save/protect | Harmless |
| 仕 | serve, attend | 援 | assist | Harmless |
| 願 | wish; petition | 需 | request | Borderline parity with excluded 頼/求 (O7) |
| 望 | hope | 需, 飢 | want | Harmless |
| 派 (E) | faction; school of thought | 隊 | party/faction | Already handled for 系 (系 declares 派); 隊–派 unhandled but parity only with 党 (O8) |
| 制 (E) | system; regulate | 握 | control | Harmless vs displayed "grip; grasp"; already paired with 系 |
| 刺 (E) | pierce; prick | 縫 | embroider | Harmless; already paired with 徹 |
| 凌 (E) | endure; surpass | 慢 | endurance of 我慢 | Already handled; confirmed "endure" (凌.md:2,20-22). Over-cautious vs displayed 慢 title, harmless |
| 節 (E) | joint; season; restraint | 慢 | restraint | Already handled; "restraint" sense confirmed (節.md:2,24) |
| 負 (E) | lose; bear a burden | 慢, 謝 | bear/lose | Already handled; senses confirmed (負.md:2,20-22) |
| 乏 (E) | scarce; lacking | 飢 | shortage | Already handled; confirmed (乏.md:2,20-23) |

## Verdicts

Overall: NEEDS FIX (one minor consistency/quiz-safety defect on 討; everything else CLEAN within the inspected scope, with optional polish).

| Card | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility |
| --- | --- | --- | --- | --- |
| 慢 | CLEAN | CLEAN | CLEAN | CLEAN |
| 縫 | CLEAN | CLEAN | CLEAN | CLEAN |
| 飢 | CLEAN | CLEAN | CLEAN | CLEAN |
| 恩 | CLEAN | CLEAN | CLEAN | CLEAN |
| 盆 | CLEAN | CLEAN | CLEAN | CLEAN |
| 誕 | CLEAN | CLEAN | CLEAN | CLEAN |
| 隊 | CLEAN | CLEAN | CLEAN | CLEAN |
| 需 | CLEAN | CLEAN | CLEAN | CLEAN |
| 系 | CLEAN | CLEAN | CLEAN | CLEAN |
| 徹 | CLEAN | CLEAN | CLEAN | CLEAN |
| 討 | CLEAN | CLEAN | NEEDS FIX (F1) | CLEAN |
| 謝 | CLEAN | CLEAN | CLEAN | CLEAN |
| 握 | CLEAN | CLEAN | CLEAN | CLEAN |
| 寧 | CLEAN | CLEAN | CLEAN (O1 borderline) | CLEAN |
| 援 | CLEAN | CLEAN | CLEAN (O9 hypothesis) | CLEAN |
| 応, 統 edits | CLEAN | CLEAN | CLEAN | CLEAN |
| 30 word backlinks | CLEAN | CLEAN | CLEAN | CLEAN |
| Stroke JSONs | CLEAN (counts only; SVG appendix unread) | — | CLEAN | — |

Claims depending on Digital Daijisen character entries (not fetched) are UNVERIFIED within this pass; see L3. They do not affect the verdicts above because each card keeps them as attributed source statements and none drives a selected reading.

## Findings

**F1 — Minor; consistency / quiz safety; snapshot\kanji\討.md:15 (quiz_exclusions), 討.md:68-71 (discussion note).**
討's displayed title is "attack; discuss" (討.md:3). The card excludes [談](談.md) "converse; consult", 議 "deliberate; debate" and 論 "argument; discourse" for the discussion sense, and 攻/戦/撃/打 for attack, but not:
- 話 "talk, speak" (repo\kanji\話.md:3) — "talk" is an ordinary near-synonym of the displayed "discuss", at least as close as the excluded 談 "converse".
- 争 "contend; dispute" (repo\kanji\争.md:3) — "dispute" overlaps the displayed "discuss"/debate and "contend" overlaps "attack" (争.md:20-21 explicitly covers arguing and competing).

Impact: in the full N1/All pools the curated 計/村/寺 fill all three slots (checks\quiz-safety.txt:38), so neither card is drawn there. They can be drawn wherever the app falls back for 討: custom pools and, for 話, the padded Starter practice session — 話 is tagged `starter` (話.md:6) and REVIEW.md:93-94 states Starter sessions fill from the fallback. A learner then sees two defensible answers. Remedy: add 話 and 争 to 討's quiz_exclusions (direct pairs) and extend the note at 討.md:68-71, or document why they are judged distinct. Evidence: titles from the index (title-index lines for 話/争/談/議/論) and the cards cited. Confidence: medium-high for 話, medium for 争. Drawability in the Starter session is inferred from REVIEW.md and tags; actual Kotlin draws are unverified (L1).

No other established defect was found. Specifically verified as correct: all fifteen cards' strokes, grade tags, radicals/numbers, on/kun metadata against kanjidic2-records.xml/source-metadata.json; Joyo statements against joyo-rows.json (e.g. 討.md:54-56 "うつ, with 討つ and 敵討ち ... 打つ and 撃つ"; 謝 陳謝/平謝り; 寧 安寧/丁寧); every cited JMdict sense, POS, restriction and flag that is present in jmdict-families.xml (e.g. 飢える かつえる restricted to 飢える/餓える; 謝る dated senses; 寧ろ usually kana; 盆 untagged "family; household" and slang sense; 系 colloquial "-type; -ish"; 握る four senses; 握手 sense 2; 隊 "body/unit", 部隊 "force"); every cited JMdict entry ID on the 15 cards exists in the families file; stroke JSON strokeCount equals card strokes for all 15; each selected quiz reading has its own row and linked word article, and unselected kun readings (寧 むし.ろ) are explained; transitivity/conjugation class statements (縫う, 討つ, 握る, 謝る godan; 飢える ichidan intransitive); 30 backlinks use correct `../kanji/X.md` paths and the single remark edit (words\応援.md:30-32) correctly removes the stale "no card" sentence, matching checks\linkplan-verify.txt; 応/統 diffs only add the 援/系 links. Distractor/exclusion overlap: none within any card. C distractors: all 45 titles match the index, all are meaning-indefensible for their target, and reading overlaps are only the ones REVIEW.md and quiz-safety.txt already disclose (談 ダン vs 誕 タン; 凡 and 掲 with empty quizKunyomi).

## Optional

- **O1 (寧):** 和 "harmony; Japanese style" teaches 平和 "peace" (和.md:20); "harmony" is plausibly read as "peaceful" for 寧 "polite; peaceful". Similarly 尊 "revere; esteem" parallels the excluded 敬 "respect; honor", and 拝 "worship; bow in respect" parallels the excluded 礼 "bow; thanks". Consider adding 寧–和 at least; 尊/拝 only for parity.
- **O2 (pun-based / dated-sense exclusions):** several authored pairs rest on an English word in a non-displayed source gloss rather than on an ordinary meaning: 誕–寝 ("lie", 誕.md:69-72), 隊–秒 ("unit", 隊.md:67-71), 援–根 ("rooting") and 援–貯 ("save") (援.md:72-76,66-68), 徹–家/帰 ("strike home", 徹.md:84-87), 系–校/級 ("school"), 系–封 and 寧–封/親 ("close"), and 謝–失/損/敗/負 via dated 謝る senses. content-format.md:94 asks for pairs from displayed labels and ordinary meanings. Impact is low (over-exclusion only shrinks the pool; the notes do label the shared-word cases), but the rationale is applied unevenly: by the same logic 当 "hit; be on target" and 射 "shoot" would be at least as close to "strike home" as 家/帰, 済 to 了, 夕 to 晩, and 困 "be in difficulty" closer to "be at a loss" than 失 "lose; loss". Consider pruning the homograph-only pairs or stating the policy once.
- **O3 (系):** 類 "kind; category" is excluded, but 種 "seed; kind" and 般 "general; kind; category" are not. All three are harmless against the displayed "lineage; system"; either drop 系–類 or add the parallels for consistency.
- **O4 (討):** 評 "appraise" (which itself excludes 批/論/議), 想 "thought; conception" (parity with excluded 考) and 察 "observe; infer" (parity with excluded 査/調/診; 診 itself excludes 察) are borderline; lower priority than F1. Also 思 "think, feel" (C card, distractor of 恩) is at parity with the excluded 考 for 討.
- **O5 (誕):** 始 "begin, start" is about as close to "birth" as the excluded 創 "originate; create" / 元 "origin"; 造 "make; construct" mirrors the excluded 作 for the "making" gloss of 誕生. Both harmless vs the displayed title.
- **O6 (盆):** 盤 "board; disc" is the other 皿-key flat vessel/board character (盤.md:27-29 records a vessel sense) and itself excludes 皿/板; a 盆–盤 pair is defensible but not required.
- **O7 (需):** 願 "wish; petition" parallels the excluded 頼 "request; rely" (願.md:47 compares them); low priority.
- **O8 (隊):** 派 "faction; school of thought" parallels the excluded 党 "political party; faction"; either both or neither.
- **O9 (援, hypothesis):** the curated distractor 授 "grant; impart; teach" (援.md:13) always appears; English "grant" can be read as a grant of aid, and 援助 includes financial support (words\援助.md:17). Probably harmless because 授's title is clearly verbal (impart/teach), but a different 扌 look-alike (e.g. 捨, 拾) would remove the doubt.
- **O10 (縫):** 縫 excludes 針 "needle; pin" as the sewing tool (縫.md:61-63) but not 糸 "thread; yarn", the sewing material. Harmless (curated 縮/練/緒 fill N1/All), parity only.
- **O11 (new-card pair 恩–援):** "favor" vs "aid; assistance" (a favor can be help). Not declared by either card; low-probability ambiguity.
- **O12:** checks\lint.txt warns that five batch words (体系, 必需品, 応援, 縫う, 飢える) have Dictionary lines without an inline entry id; these lines are unchanged by this batch (ID on the following line) and are pre-existing format noise.

## Limits

- **L1:** Reading/meaning audits model only full N1/All pools and Starter sessions with one borrowed target (REVIEW.md:76-81). Custom or caller-built pools, multi-borrow Starter sessions, actual Kotlin draws, native/phone acceptance and compatibility with installed APK 5c000bd (which predates quiz_exclusions) are unverified; JVM/emulator work is on hold. F1's Starter drawability of 話 is inferred, not executed.
- **L2:** Latent reading collisions disclosed by checks\reading-exposure.txt are accepted as modeled only: notably 援 おん (Wiktionary-derived, not on the card) is drawable for the エン prompt in a padded Starter session that also borrows 恩 (a card in this same batch), 温 or 音 (reading-exposure.txt:202-209). Not drawable in N1/All; actual app behavior unverified.
- **L3:** Digital Daijisen / Weblio character-entry claims (e.g. 慢 filing 我慢 under conceit, 慢.md:30-32; 需 もとめる, 徹 とおる/とおす, 討 たずねる, 寧 ニョウ, 援 たすける/ひく and the 捐/掩 note, 飢 饑 interchangeability, 恩 めぐみ/いつくしみ/情け glosses) were not fetched and remain UNVERIFIED in this pass; none is used for a selected reading. 水飢饉 (飢.md:26, words\飢饉.md) is not in jmdict-families.xml; only the JMdict "chronic shortage (e.g. of water)" sense was verified.
- **L4:** KanjiVG SVG appendix (segments 50-56) and the binary Joyo PDF were not read; stroke JSON stroke order/shape was not compared with the SVG source, only counts and source revision.
- **L5:** content-format.md beyond line 139 was not read (by design of the chain).
- **L6:** Identified but unread collision candidates (outside my 40/10 caps): 局 "bureau; office" (隊 divisions, parity with 部/科/課), 賛 "approve; praise" (援 support), 関 "involve; barrier" and 続 "continue" (系 connection/series), 結 "tie; join; conclude" (縫 sewing together), 食 "eat, food" (飢; the card explicitly declines it at 飢.md:63-64), 起's peers 眠, 守 "guard; obey" (援 save/protect; read only as a C card, harmless for 謝), 担 "shoulder; take on" (援 support; read as C card, judged harmless), 宅 "residence" (盆 household parity with 家), 頼/協/支 (援/握 senses; E-eligible but not requested), 派's sibling 流 "flow" (系 school). All were judged from index titles only.
- **L7:** The index confirms several plausible synonym kanji have no card in this tree and therefore cannot collide (e.g. 恵, 救, 扶, 佐, 護, 拒, 請, 慰, 貫, 透, 把, 掌, 執, 穏, 泰, 慎, 耐, 忍, 堪, 誇, 怠, 惰, 餓, 班, 陣, 源, 筋, 縁, 審, 慮, 伐, 征, 襲).
- **L8:** Execution-model identity: reported by the runtime as Claude Opus 5.5; not independently verifiable.
