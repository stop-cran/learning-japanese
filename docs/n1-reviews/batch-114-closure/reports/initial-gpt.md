# B114 independent first content review

Run: N1-B114-GPT-001. One independent pass, comprising selection and extension review; no edits or confirmation round.

Snapshot: `8c2bdc27e5d556e639a4d0e9239ae5f2009c400f`.
Base: `0485c873d2ac636373c7bdf739df97ff66f9160f`.
Packet: `C:\Users\stop-\n1-kanji-workspace\review-packets\batch-114-8c2bdc27`.
The supplied packet-checksum-file digest is `eb6b1042060f561cd6ff49054d0e11533c15008ea0f6bbc064b07614b1701e15`; I did not open that file or independently hash the packet.

Reviewer: GPT-6.1 Sol, model ID `gpt-6.1-sol`, as identified by the serving runtime. No other reviewer, agent, session history, author rationale or review report was consulted.

## Scope and verdict

Scope: all fifteen new kanji cards, all fifteen stroke JSONs, the fifteen link-only word changes and complete changed articles, the supplied rubric/contracts, ten check logs, complete extracted KANJIDIC2 records and 65 matched JMdict families, neutral source metadata/provenance/component evidence, all 1,221 indexed titles, all 45 curated slots represented by 41 comparison cards, and 47 extension cards: 37 D candidates and ten E targets.

**Overall: NEEDS FIX.** Three meaning-choice exclusion gaps are established below. This is not a demonstrated failure of the current default four-choice quiz: the supplied curated meaning options are distinct. Missing direct guards matter when these comparison cards can participate in fallback or caller-selected pools. No live Android failure was reproduced.

| Facet | Verdict | Basis |
| --- | --- | --- |
| Correctness | UNVERIFIED | Core meanings, selected readings and textual stroke metadata are supported; some supplementary source claims and exact modern community-level membership remain outside the evidence actually opened. See L3-L5. No contradicted core spelling/reading pair was established. |
| Scoped coverage | NEEDS FIX | The taught room/bureau, gathering/results and supernatural senses require the additional direct quiz comparisons in F1-F3. Practical teaching coverage otherwise needs no manufactured vocabulary expansion. |
| Consistency / quiz safety | NEEDS FIX | F1-F3 are missing direct exclusions. All 45 supplied curated meaning slots are defensibly wrong for their assigned target. Reading safety is established only within the supplied model's bounds, not universally. |
| Comprehensibility | CLEAN | Long vowels, compound allocation, physical versus figurative senses, and mnemonic versus historical claims are usefully distinguished. CLEAN is limited to inspected teaching, not native acceptance or exhaustive historical accuracy. |

Verdicts below distinguish a supported core from an unverified supplementary claim; an unresolved consequential claim is not promoted to CLEAN merely because checks passed.

## Read accounting

Core chain segments read, once each, in order:
**1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40**.

Extension chain segments read, once each, in order:
**1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11**.

No chain segment was re-viewed. Every segment was opened as a single explicitly named absolute file, without a range. The kickoff instruction file was read once in full. The report has one authorized complete readback after its single creation.

I read `evidence/title-index.txt` **source lines 1-1221**: lines 1-584 in core segment 30, lines 585-1221 in segment 31. Source line 1 is **`一 one`**; source line 1221 is **`齢 age; years lived`**. Both headers identify SHA-256 `7241a3ea93227a7298b51d6a4d14753302594c83e59e7455533b6d8956d99d8f`.

Three optional public fetches, all during phase 1:

| URL | Reason and evidence actually returned |
| --- | --- |
| https://www.weblio.jp/content/寮 | Requested character/noun senses, including offices and temple accommodation. The tool returned only a 500-character site-navigation preview and an oversized-output file notice. I did not open that temporary file. This fetch did **not** verify the dictionary heading. |
| https://www.weblio.jp/content/碁 | Returned Daijisen's character heading with ゴ and キ and the separate き and ご lexical headings. This independently supports the additional キ reading, not universal quiz safety. |
| https://www.weblio.jp/content/魅 | Returned Daijisen's み character heading: supernatural beings and captivating attraction. I distinguish it from the separately attributed Wiktionary and other dictionary content also returned. |

The reasons and URLs were stated publicly immediately before each call. No web search, browser, script, shell, build or temporary-file read was used.

## Findings

### F1 - Missing direct room and bureau comparisons for 寮

**Severity:** Moderate. **Facets:** scoped coverage; consistency/quiz safety. **Confidence:** high for the four listed pairs.

**Locations:** `snapshot/kanji/寮.md:1-15,23-30,61-68`; `repo/kanji/房.md:1-15,23-25`; `repo/kanji/庁.md:1-11,21-22`; `repo/kanji/部.md:1-11,21-25`; `repo/kanji/課.md:1-11,21-22`; `evidence/jmdict-families.xml:1047-1088` (entry 1554230).

寮 explicitly teaches residential quarters and historical bureau/tea-room uses. The complete JMdict family supports a government department beneath a ministry and a tea-ceremony room, with the historical qualifications preserved. Actual comparison labels are 房 **room; tassel; bunch**, 庁 **government agency**, 部 **section; department**, and 課 **lesson; organizational division**. These broad room/organizational-unit options can fit the corresponding 寮 senses, even though the Japanese institutional names are not freely interchangeable.

Neither side of **寮-房, 寮-庁, 寮-部, 寮-課** declares the pair. 寮's existing 室/局/署/府 guards do not exclude these further cards; 房's 室/部 guards likewise do not make an indirect chain effective.

**Impact:** two defensible meaning choices can be available in a pool containing one of these direct candidates. The supplied three curated options do not expose this in the default meaning question.

**Remedy:** declare each of these four direct pairs once, on either card, retaining the qualified sense distinctions and existing exclusions. This finding does not equate a ritsuryo bureau with a modern ministry, or a dormitory with every institution.

### F2 - Missing gathering and useful-result comparisons for 穫

**Severity:** Moderate. **Facets:** scoped coverage; consistency/quiz safety. **Confidence:** high.

**Locations:** `snapshot/kanji/穫.md:1-15,23-30,56-64`; `repo/kanji/集.md:1-11,21-23`; `repo/kanji/拾.md:1-11,21-22,29-32`; `repo/kanji/績.md:1-11,21-22,30-36`; `repo/kanji/利.md:1-11,21-24`; `evidence/jmdict-families.xml:493-531` (entry 1330510).

The taught action is gathering crops; the taught secondary compound sense is a useful gain or result. 集 displays **gather**, 拾 **pick up; gather**, 績 **achievements; results**, and 利 **benefit; advantage**. Their opened bodies support collecting objects, gathering, activity results and benefits respectively. JMdict's 収穫 family independently retains harvest/ingathering and fruits/gain/result/returns as separate senses.

Neither side declares **穫-集, 穫-拾, 穫-績, 穫-利**. The existing 収/採/取 and 得/果/実 pairs cannot protect these unlisted direct comparisons. This is not a claim that bare 穫 translates every occurrence of collecting, benefit or results; the finding follows the crop-gathering and productive-result senses this card actually teaches, using the same distinction its existing guards already protect.

**Impact:** unguarded broad labels can compete with the target in applicable fallback/custom pools. 程/秋/科 remain sound default meaning distractors.

**Remedy:** add the four direct exclusions once each. Preserve the noun-versus-する distinction for figurative 収穫; no change to raw readings or supporting vocabulary is requested.

### F3 - Missing direct supernatural comparison for 魅

**Severity:** Moderate. **Facets:** scoped coverage; consistency/quiz safety. **Confidence:** high.

**Locations:** `snapshot/kanji/魅.md:1-15,23-30,54-60`; `repo/kanji/怪.md:1-14,21-22,30-31,37-41`; Daijisen's **み【魅】** heading at https://www.weblio.jp/content/魅, fetched in this pass.

魅 teaches both captivating attraction and a supernatural spirit/monster sense. The fetched Daijisen heading verifies that secondary sense. 怪 displays **suspicious; uncanny** and its actual body describes uncanny beings, with 怪物 and 妖怪 examples. The uncanny choice therefore overlaps the supernatural sense of 魅, not merely a shared component or topic.

Neither **魅-怪** endpoint declares a guard. The existing 魅-妖 pair is insufficient: exclusions are symmetric but not transitive, and 妖's comparison with 怪 is not a substitute for this direct pair.

**Impact:** a defensible uncanny meaning can compete with 魅 in an applicable pool. This is not exposed by 未/妹/末 in the supplied default meaning choices.

**Remedy:** declare 魅-怪 once while preserving the differences among suspicion, supernatural beings and personal allure. I do not extend this finding automatically to 美 or 神: their displayed beauty/deity meanings require different evidence.

## Per-new-card results

All fifteen cards preserve the single frozen on-reading and empty kun inventory. Their selected on-reading has its own linked word row. KANJIDIC2, source metadata, Joyo text and JMdict jointly support the core allocations listed here. All full correctness verdicts retain the unverified modern community-membership limitation in L4.

| Card and displayed title | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility | Evidence and independent disposition |
| --- | --- | --- | --- | --- | --- |
| 娯 - recreation; amusement | UNVERIFIED, core CLEAN | CLEAN | CLEAN within inspected comparisons/model | CLEAN | `snapshot/kanji/娯.md:23-42,46-64`; 娯楽/ごらく in JMdict 1269290 supports recreation/amusement and ゴ + ラク. Index enjoyment/pleasure candidates are 楽/遊/享/喜/快/幸, not music alone; 楽 was opened and its direct guard is justified. 誤/妹/妙 are not recreation labels. Additional Daijisen kun readings are unverified in this pass, L3. |
| 寮 - dormitory; quarters | UNVERIFIED, core CLEAN | NEEDS FIX | NEEDS FIX, F1 | CLEAN | `snapshot/kanji/寮.md:23-47,51-68`; 寮/りょう, 学生寮, 社員寮 and 寮生 are supported by complete families. Historical bureau, tea-room and villa flags are preserved. Room/department index candidates led to actual D/E reads; 房/庁/部/課 require direct guards. The grouped つかさ family's chiefly 官/司 usage does not prove an ordinary chief gloss for every 寮 occurrence. Temple accommodation remains unverified, L3. |
| 廊 - corridor; covered passage | UNVERIFIED, core CLEAN | CLEAN | CLEAN within inspected comparisons/model | CLEAN | `snapshot/kanji/廊.md:23-35,41-63`; 廊下/ろうか, 回廊/かいろう, 画廊/がろう and 廊/ろう are supported. The index's hall/path/pass-through/tower labels are distinguished; 館's hall guard is justified. Tower is a retained KANJIDIC2 gloss, explicitly not manufactured into modern usage. Twelve strokes agree with JSON/component evidence; alternate eleven is not a second drawn order. |
| 栓 - plug; stopper | UNVERIFIED, core CLEAN | CLEAN | CLEAN within inspected comparisons/model | CLEAN | `snapshot/kanji/栓.md:23-38,42-69`; JMdict 1956550 supports stopper/cork/plug/bung and tap/faucet/stopcock; linked 栓/せん is a transparent example. The index seal/close/pack/stop labels are accounted for as declared candidates; opened 封 is a justified direct guard. 障/停 name hindering/stopping, not the stopper object or flow-control fitting itself; no additional required pair established. Earplug and archaic ornament entries are kept separate. |
| 汽 - steam; vapor | UNVERIFIED, core CLEAN | CLEAN | CLEAN within inspected comparisons/model | CLEAN | `snapshot/kanji/汽.md:23-43,47-69`; キ + シャ is supported by 汽車/きしゃ and the Joyo extract. Dated and rural/non-electric senses stay local to the whole word. 汽水 is correctly brackish water. Index 蒸/気/雰 are direct candidates; 気 and 雰 were opened and the guards exist. 煙's smoke/fumes label is not steam; no further direct pair established. |
| 症 - symptoms; illness | UNVERIFIED, core CLEAN | CLEAN | CLEAN within inspected comparisons/model | CLEAN | `snapshot/kanji/症.md:23-30,41-70`; 症 is a medical suffix in JMdict 1351000; 症状/しょうじょう, 花粉症, 重症 and 症候群 support the selected examples. Index illness/state/condition candidates explain existing 病/患/状/態 guards; 病 was opened. 候's entire label specifies weather, and 療/診 concern treatment/examination, not symptoms. 況 names a situation/state of affairs rather than the medical symptom or illness; no added pair established from its actual label. |
| 砲 - cannon; gun | UNVERIFIED, core CLEAN | CLEAN | CLEAN for opened meaning options; broader reading safety UNVERIFIED | CLEAN | `snapshot/kanji/砲.md:23-46,50-64`; JMdict 1517560 supports the exact title; 鉄砲/てっぽう and Joyo support underlying ホウ despite compound っ/ぽう. Archaic つつ and nanori づつ are not added to frozen lexical practice. 射/撃 name firing actions, not the firearm. 銃 has no packet card. 大砲's baseball sense is supported, but the separate bare-砲 baseball assertion was not independently verified, L3. |
| 碁 - Go board game | UNVERIFIED, core CLEAN | CLEAN | CLEAN for inspected meanings/bounded pools; broader reading safety UNVERIFIED | CLEAN | `snapshot/kanji/碁.md:23-40,44-63`; JMdict 1270870/1155990 support ご and 囲碁. Index play/go/board candidates are not automatically synonyms: 盤 is a board/disc object, not the game, and English 行 go is movement. 棋 has no packet card. Daijisen independently verifies キ; the supplied model reports its latent wrong-choice risk, L5. |
| 磁 - magnetism; porcelain | UNVERIFIED, core CLEAN | CLEAN | CLEAN within inspected comparisons/model | CLEAN | `snapshot/kanji/磁.md:23-41,45-61`; 磁石/じしゃく and じせき retain ジ while 石 changes; 磁気 and 磁器 are distinct じき words in complete JMdict families. Index vessels/pulling are broader relationships, not porcelain or magnetism labels. Actual 器/引/吸 reads do not establish additional direct pairs. 陶 has no packet card. |
| 穀 - grain; cereals | UNVERIFIED, core CLEAN | CLEAN | CLEAN within inspected comparisons/model | CLEAN | `snapshot/kanji/穀.md:23-47,51-77`; 穀物/こくもつ, 穀類, 脱穀 and 雑穀 support コク and the grain category. Corn is not narrowed to maize; cereals are not breakfast food by definition. Index rice/seed/grain candidates justify 米 and 粒 guards, both opened. 穂's whole grain-bearing-head label is a plant part, and 飯's whole cooked-rice/meal label specifies prepared food. Neither is established as an extra grain/cereal synonym. Classical たなつもの and the beans statement remain unverified, L3. |
| 穫 - harvest; reap | UNVERIFIED, core CLEAN | NEEDS FIX | NEEDS FIX, F2 | CLEAN | `snapshot/kanji/穫.md:23-44,48-64`; 収穫/しゅうかく transparently allocates カク; its three complete senses retain harvest, useful results and catch. Index gather/results/benefit candidates are not exhausted by the existing list: 集/拾/績/利 require direct guards after actual-card inspection. 収 is already guarded. 秋 names the season, not reaping. |
| 糖 - sugar | UNVERIFIED, core CLEAN | CLEAN | CLEAN within inspected comparisons/model | CLEAN | `snapshot/kanji/糖.md:23-45,49-65`; 糖/とう and 砂糖/さとう, 糖分, 糖類 and 糖尿病 have matched entries. Index sweet/sweets/powder candidates were opened: 甘 names a taste, 菓 finished confectionery/snacks, 粉 flour/powder. Their complete labels are not sugar synonyms; no additional required guard established. Additional あめ is unverified, L3. |
| 紺 - navy blue | UNVERIFIED, core CLEAN | CLEAN | CLEAN within inspected comparisons/model | CLEAN | `snapshot/kanji/紺.md:23-28,38-62`; 紺/こん and 紺色/こんいろ are noun entries, not invented い-adjectives. 濃紺 and 紺青 have the listed entries; the varied pigment translations are not one invariant color code. Index blue/dark cues have declared guards; actual 青 is directly protected. 紅's complete deep-red title is not blue despite sharing “deep.” Purplish shade attribution remains unverified, L3. |
| 雰 - mist; atmosphere | UNVERIFIED, core CLEAN | CLEAN | CLEAN within inspected comparisons/model | CLEAN | `snapshot/kanji/雰.md:23-45,49-63`; KANJIDIC2 supports atmosphere/fog; 雰囲気/ふんいき supports the selected フン and ordinary ambience/aura senses. The irregular ふいんき flag and obsolete physical-atmosphere sense are correctly localized. Index 気/汽 are direct guarded comparisons; actual 雲/煙 concern clouds/smoke, not automatic mist synonyms. |
| 魅 - charm; bewitch | UNVERIFIED, core CLEAN | NEEDS FIX | NEEDS FIX, F3 | CLEAN | `snapshot/kanji/魅.md:23-43,47-73`; 魅力/みりょく supports ミ + リョク, and 魅する/みする is a special-class suru verb, not a new kun reading. Fetched Daijisen verifies the monster/spirit secondary sense. 妖 is already protected; actual 怪 requires its own pair. 美 and 神 do not automatically become guards from attraction/supernatural topics. |

The title scan also considered main/secondary cues absent from the displayed title: 寮 bureau/tea room/villa; 廊 hall/tower/gallery; 栓 tap/valve/bolt/cork; 砲 baseball and whole-word specialized uses; 磁 magnet/compass and porcelain; 穀 seeds/beans/corn; 穫 productive results/catch; 雰 aura/air; 魅 supernatural beings. Whole-word meanings were not indiscriminately allocated to the bare character. Missing or unread comparison evidence is recorded below rather than silently presumed safe.

## Curated C options: all 45 slots

The title-index column records semantic comparisons found in the full index, not verification of every pre-existing card's exclusion graph. Those comparisons are not defects in B114 unless they collide with the assigned new target. Source references here are the opened `repo/kanji/<character>.md` files, particularly title line 3 and reading metadata/table; all 41 were read in full through core segments 32-40.

| New target | Actual curated titles, in slot order | Title-index / ordinary-meaning check | Reading comparison |
| --- | --- | --- | --- |
| 娯 | 誤 mistake; error / 妹 younger sister / 妙 strange; exquisite | Error and kinship are not amusement; exquisite/strange is not recreation. 妙's index neighbors include 奇/変/珍 and 美/優/微, not a free recreation meaning. | 誤 explicitly has ゴ, so it cannot supply ゴ as a wrong reading. 妹 マイ and selected 妙 ミョウ differ. |
| 寮 | 察 observe; infer / 寧 polite; peaceful / 案 proposal; draft plan | Observation, courtesy/peace and proposals are not quarters. Index comparisons include 観/見 for 察, 安/平/静/敬 for 寧, and 企/計/策 for 案; none makes these labels housing. | サツ / selected ネイ / selected アン differ from リョウ. |
| 廊 | 庭 garden; yard / 床 floor; bed / 府 urban prefecture; administration | Garden (compare 園), floor/bed and prefectural administration are not a connecting passage. 府's administrative sense overlaps 寮, not 廊; 寮-府 is already declared. | テイ / ショウ / フ differ from ロウ. |
| 栓 | 全 whole; complete / 松 pine tree / 村 village | Completion/whole index neighbors 完/総 do not name a stopper; pine and village are distinct. 木/町 are related tree/settlement cues, not closure meanings. | No literal セン in these full on lists (ゼン / ショウ / ソン). The supplied model nevertheless reports two curated reading choices and fallback; I do not infer its normalization algorithm from that count. |
| 汽 | 河 river; watercourse / 池 pond; reservoir / 海 sea, ocean | 河-川 and 海-洋 are index overlaps among water features; none is steam/vapor. 池's battery sense does not change its displayed pond label. | カ / チ / カイ differ from キ. |
| 症 | 正 correct, proper / 政 politics / 床 floor; bed | Correctness, politics and floor/bed do not mean symptoms. 真/直 and government-related labels are index neighbors, not medical alternatives. | All three full metadata lists include ショウ. Matching readings must be suppressed, not presented as three wrong ショウ answers. The bounded log shows alternative selections/fallback rather than universal curated availability. |
| 砲 | 包 wrap; enclose / 砂 sand / 硬 hard; stiff | 包's index overlap with 囲/括 and 硬's with 固 do not name a gun. Sand and hardness are not firearm meanings. | 包 has ホウ; 砂 サ/シャ and 硬 コウ differ. The model filters matching choices and may fall back. |
| 碁 | 目 eye / 日 sun, day / 田 rice field | Eye, sun/day and rice field are not Go. Secondary item/point, time, and field uses do not make these game names; index 点/時/畔 are comparisons, not Go answers. | モク/ボク, ニチ/ジツ and デン differ from ゴ and from the externally verified キ. |
| 磁 | 硬 hard; stiff / 研 polish; study closely / 砂 sand | Material hardness, polishing/study and sand are not magnetism or porcelain. Index 固/磨/学/究 share some comparison senses but are not required new-target meaning alternatives on that basis. | コウ / ケン / サ・シャ differ from ジ. |
| 穀 | 殿 palace; lord / 投 throw / 段 step; level | Palaces/lords, throwing and stages are not grain. Index 主/長, and 階/級, have comparison senses, not grain. | デン・テン / トウ / ダン・タン differ from コク. |
| 穫 | 程 extent / 秋 autumn / 科 department; course | Extent, a season and an academic/institutional division are not harvesting. Index 度/幅, and 部/課, provide comparisons; season/action remains distinct. | テイ / シュウ / カ differ from カク. |
| 糖 | 米 rice grain / 数 number / 類 kind; category | Rice is not sugar; counts and categories are not ingredients. 米 overlaps 穀/粒/飯 distinctions but is already protected against 穀. Index 号 and 種/般/型 concern numbers or kinds, not sugar. | ベイ・マイ・メエトル / スウ・ス・サク・ソク・シュ / ルイ differ from トウ. |
| 紺 | 紅 crimson; deep red / 給 pay; bestow / 結 tie; join; conclude | The whole red label is distinct from navy blue; payment and joining are not colors. Index 赤; 払/与/授/贈; 接/連/括 provide pre-existing comparisons, not blue meanings. | Selected/full candidates コウ・ク / キュウ / selected ケツ differ from コン. |
| 雰 | 分 minute, part / 雪 snow / 晴 clear skies | Minute/part, snow and clear skies are not mist/ambience. 分's secondary feelings in 気分 do not make its entire displayed label atmosphere. Index 微/秒 and 明/冴 provide comparisons, not a generic atmospheric synonym. | 分's full on list includes フン; 雪 セツ and 晴 セイ differ. The model filters matching selection outcomes and may fall back. |
| 魅 | 未 not yet / 妹 younger sister / 末 end; tip | Negation-in-time, kinship and an ending/extremity are not charm or supernatural beings. Index 不 and 終/了 provide comparisons, not attraction meanings. | 未 includes ミ; 妹 マイ and 末 マツ/バツ differ. Matching selections require filtering/fallback, as modeled. |

Thus all 45 **meaning** slots are CLEAN for the assigned new target. Shared correct readings on some C cards are a separate issue; they do not make those meaning distractors defective. The model reports zero target-reading hits in its specified pools, not proof about all future configurations.

## Phase-1 requests, verbatim

Each D entry was checked against the supplied global eligibility reference: no new card, C distractor, or any new card's existing exclusion target was requested as D. E contains only eligible existing targets, excluding C cards and new cards.

```text
D1 居 - 寮: dwell; residential quarters
D2 房 - 寮: room; residential quarters and tea room
D3 院 - 寮: institutional accommodation
D4 庁 - 寮: government bureau or office
D5 省 - 寮: government department or ministry
D6 部 - 寮: institutional department or section
D7 課 - 寮: organizational division or department
D8 首 - 寮: chief or head in the complete つかさ family
D9 長 - 寮: chief or head in the complete つかさ family
D10 泊 - 寮: lodging; staying overnight
D11 寝 - 寮: sleeping accommodation
D12 障 - 栓: obstructing or blocking an opening
D13 停 - 栓: stopping or halting flow
D14 煙 - 汽 雰: vapor; mist; visible airborne plume
D15 雲 - 雰: misty atmospheric moisture
D16 美 - 魅: attractive quality; charm
D17 神 - 魅: supernatural spirit or being
D18 候 - 症: condition; symptoms in 症候群
D19 況 - 症: condition or situation
D20 療 - 症: illness and medical condition
D21 診 - 症: medical examination of symptoms
D22 銃 - 砲: gun; firearm
D23 射 - 砲: shooting; gun discharge
D24 撃 - 砲: shooting; gun discharge
D25 棋 - 碁: Go or board game in the complete ご family
D26 盤 - 碁: board; game board
D27 陶 - 磁: porcelain; ceramics
D28 器 - 磁: porcelain ware; vessel
D29 引 - 磁 魅: attraction; drawing or pulling toward
D30 吸 - 磁 魅: attraction; drawing in
D31 穂 - 穀: grain-bearing head; grain
D32 飯 - 穀: rice; cereal grain
D33 集 - 穫: gather; collect a harvest
D34 拾 - 穫: pick up; gather
D35 績 - 穫: results; fruitful achievement
D36 利 - 穫: gain; beneficial return
D37 甘 - 糖: sweetness; sugar
D38 菓 - 糖: sweets; confectionery
D39 粉 - 糖: powdered food substance; sugar
D40 怪 - 魅: supernatural being; bewitching or uncanny quality
E1 楽 - Verify the existing enjoyment label against 娯 and the declared direct exclusion.
E2 室 - Verify the room label against 寮's accommodation and tea-room senses.
E3 館 - Verify the hall and building label against both 寮 and 廊 and their declared pairs.
E4 封 - Verify seal or close against 栓's stopper sense and its existing guard.
E5 病 - Verify illness against 症's displayed illness sense.
E6 粒 - Verify grain or particle against 穀's displayed grain sense.
E7 収 - Verify collect or store against 穫's gathering sense and the existing pair.
E8 青 - Verify blue against 紺's narrower navy-blue title.
E9 気 - Verify air, spirit and atmosphere against 汽 and 雰 and their direct guards.
E10 妖 - Verify bewitching and supernatural senses against 魅 and its existing exclusion.
```

The coordinator reported these nonexistent entries, verbatim; no substitutes were requested or read:

```text
D22 銃 - 砲: gun; firearm
D25 棋 - 碁: Go or board game in the complete ご family
D27 陶 - 磁: porcelain; ceramics
```

## Every D/E card actually read

All displayed titles below are the actual frontmatter titles, checked against the neutral index. Citations refer to complete cards reached through the extension chain. “Harmless” means no required direct pair established for the supported displayed/ordinary senses; it does not endorse every historical assertion in the comparison card.

| ID / character | Displayed title | Related new card | Reason, evidence, disposition |
| --- | --- | --- | --- |
| D1 居 | be present; dwell | 寮 | `repo/kanji/居.md:21-24,37-40`: presence/residing versus an accommodation noun. **Harmless** on these supported labels; 寮's conservative 住 guard is not a transitive requirement for every dwelling-related verb. |
| D2 房 | room; tassel; bunch | 寮 | `repo/kanji/房.md:23-25`: room/dwelling/temple quarters, matching 寮's room uses. **Collision needing exclusion**, F1; neither side lists the pair. |
| D3 院 | institution | 寮 | `repo/kanji/院.md:21-22,31-36`: hospitals, schools, temples. Institutional association alone is not an attested generic institution meaning for 寮. **Harmless** on inspected labels; no automatic broad-category guard. |
| D4 庁 | government agency | 寮 | `repo/kanji/庁.md:21-22,34-38`: government office/agency versus 寮's supported historical bureau. **Collision needing exclusion**, F1. |
| D5 省 | ministry; omit | 寮 | `repo/kanji/省.md:21-22,30-32`: ministry is not the bureau beneath a ministry specified in JMdict 1554230. **Harmless**; the shared government topic does not erase rank/organization distinctions. |
| D6 部 | section; department | 寮 | `repo/kanji/部.md:21-25`: organizational section/department, also a room compound. **Collision needing exclusion** for the supported bureau/department meaning, F1; not an allocation of へや to ブ. |
| D7 課 | lesson; organizational division | 寮 | `repo/kanji/課.md:21-22,29-36`: organizational section/division can describe the taught bureau. **Collision needing exclusion**, F1; lesson meaning itself does not overlap. |
| D8 首 | neck | 寮 | `repo/kanji/首.md:21-23,38-45`: actual label is a body part, not chief/official. **Harmless** for displayed choices. Grouping 首 with 寮 in つかさ is not enough to turn “neck” into quarters. |
| D9 長 | long, chief | 寮 | `repo/kanji/長.md:20-22,29,40`: chief is real for 長. **Harmless for established ordinary 寮 senses**; whether 寮 carries the complete つかさ family's chief sense as a useful independent character gloss is **UNVERIFIED**, not a required pair inferred from shared entry membership. See L3. |
| D10 泊 | stay overnight; anchor | 寮 | `repo/kanji/泊.md:21-22,29-32,44`: lodging is an action, not a dormitory/quarters label. **Harmless** on the full displayed wording; not every accommodation-related activity is synonymous. |
| D11 寝 | lie down; sleep | 寮 | `repo/kanji/寝.md:21-24,31-38`: sleeping/lying down versus accommodation. **Harmless**; 寝室 does not allocate “dormitory” to 寝. |
| D12 障 | obstruct; hinder | 栓 | `repo/kanji/障.md:23-31,60-64`: obstruction/barrier, not a stopper, cork or tap fitting. **Harmless**; shared blocking function alone does not establish the noun meaning. |
| D13 停 | halt; stopping | 栓 | `repo/kanji/停.md:21-22,30-32,43-44`: stopping actions/outages, not a stopper or valve object. **Harmless**; the existing 止 guard is not a transitive argument. |
| D14 煙 | smoke | 汽, 雰 | `repo/kanji/煙.md:21-22,37-39`: smoke/fumes, not steam or mist by generic plume appearance. **Harmless**; no semantic interchangeability established. |
| D15 雲 | cloud | 雰 | `repo/kanji/雲.md:21-22,35-37`: clouds/ominous indications, not an automatic mist/ambience synonym. **Harmless** on the supplied whole label. |
| D16 美 | beauty | 魅 | `repo/kanji/美.md:21-24,37`: beauty/beautiful, not a dictionary proof that charm or supernatural being means beauty. **Harmless** on established target senses; attraction can involve beauty without equating the labels. |
| D17 神 | deity | 魅 | `repo/kanji/神.md:21-23,31-33`: god/deity and separate mind/spirit compounds. **Harmless**: the fetched 魅 monster/spirit sense does not establish deity as its gloss. |
| D18 候 | weather conditions | 症 | `repo/kanji/候.md:21-22,38-39`: the label's qualifier is essential. **Harmless**; weather conditions are not medical symptoms, and 症候群 does not erase the displayed qualifier. |
| D19 況 | situation; circumstances | 症 | `repo/kanji/況.md:21-22,29,39-43`: state of affairs/circumstances, not a medical illness/symptom. **Harmless** on these actual labels; a generic shared “condition” search clue is not a demonstrated competing answer. |
| D20 療 | heal; cure | 症 | `repo/kanji/療.md:21-22,36-39`: treatment rather than illness manifestations. **Harmless**; even treatment is not guaranteed cure. |
| D21 診 | diagnose; examine medically | 症 | `repo/kanji/診.md:23-27,39-43`: examination/assessment rather than symptoms. **Harmless**; a symptom is not a diagnosis. |
| D23 射 | shoot; shine into | 砲 | `repo/kanji/射.md:23-27,41-44`: firing/launching/light, not the gun object. **Harmless**; no firearm label supplied. |
| D24 撃 | shoot; strike | 砲 | `repo/kanji/撃.md:23,31-33,41-44`: shooting/striking, not cannon/gun. **Harmless**; shared weapons topic alone is insufficient. |
| D26 盤 | board; disc | 碁 | `repo/kanji/盤.md:23-31,54-60`: supporting board/disc and related uses, not the Go game itself. **Harmless**; “board game” does not mean just a board. |
| D28 器 | vessel; instrument | 磁 | `repo/kanji/器.md:23-25,35-37,54`: container/tool/ability, not a specified porcelain material or magnetism. **Harmless**; 磁器's second character does not duplicate its first. |
| D29 引 | pull; draw | 磁, 魅 | `repo/kanji/引.md:21-24,34-39,45-47`: pulling and citation, not magnetism or charm. **Harmless** on the actual labels; attraction as a physical/figurative process is not proof of either target's substance/quality gloss. |
| D30 吸 | inhale; suck in | 磁, 魅 | `repo/kanji/吸.md:21-22,30-34`: inhaling/sucking/absorbing, not magnetism or bewitchment. **Harmless**; no new pair merely from inward direction. |
| D31 穂 | grain-bearing head | 穀 | `repo/kanji/穂.md:23,39-40`: the full label and body specify a plant part, not grain as food/category. **Harmless**; the shared “grain” stem is qualified. |
| D32 飯 | cooked rice; meal | 穀 | `repo/kanji/飯.md:21-22,29-36`: cooked food/meal, distinguished from raw 米. **Harmless** for 穀's seed-crop/grain category; 米's broader English rice comparison does not make exclusions transitive. |
| D33 集 | gather | 穫 | `repo/kanji/集.md:21-23,32-36`: gathering/collecting objects. **Collision needing exclusion**, F2. |
| D34 拾 | pick up; gather | 穫 | `repo/kanji/拾.md:21-22,29-32`: gathering, including picking things up. **Collision needing exclusion** for crop gathering, F2, not for the formal-ten sense. |
| D35 績 | achievements; results | 穫 | `repo/kanji/績.md:21-22,30-41`: results from activities, not school grades exclusively. **Collision needing exclusion** for taught fruitful results, F2. |
| D36 利 | benefit; advantage | 穫 | `repo/kanji/利.md:21-24,30-36`: benefits/profit/usefulness. **Collision needing exclusion** for taught useful gain/returns, F2, without claiming every harvest is financial profit. |
| D37 甘 | sweet; pamper | 糖 | `repo/kanji/甘.md:21-22,29-33,42-44`: taste/indulgence, not sugar itself. **Harmless** on supported target senses; the unverified source-only 糖 あめ claim is not used to manufacture a sweets pair. |
| D38 菓 | confectionery; sweets | 糖 | `repo/kanji/菓.md:21-22,36-38`: prepared sweets/snacks, including nonsweet snacks, not the ingredient sugar. **Harmless**. |
| D39 粉 | flour; powder | 糖 | `repo/kanji/粉.md:21-22,31-34,38-42`: material form/flour, not sugar. **Harmless**; some sugar being powdered is not a synonym. |
| D40 怪 | suspicious; uncanny | 魅 | `repo/kanji/怪.md:21-22,30-31,37-41` plus fetched Daijisen 魅. **Collision needing exclusion** for uncanny/supernatural beings, F3. |
| E1 楽 | music, enjoyment, ease | 娯 | `repo/kanji/楽.md:21-22,32-39`: enjoyment is a direct ordinary overlap. **Already handled** by 娯 line 14; not an assertion that all music/ease is recreation. |
| E2 室 | room, chamber | 寮 | `repo/kanji/室.md:21-22,30-36`: room/chamber fits qualified room uses. **Already handled** by 寮 line 14. |
| E3 館 | hall; large building | 寮, 廊 | `repo/kanji/館.md:21-22,30-37`: building/inn accommodation and English hall ambiguity. **Already handled** by each new card's line 14, as separate direct pairs. |
| E4 封 | seal; close | 栓 | `repo/kanji/封.md:21-22,34`: closure/seal comparison. **Already handled** by 栓 line 14; not a universal equivalence of a bottle stopper and every seal. |
| E5 病 | illness | 症 | `repo/kanji/病.md:21-22,31-40`: exact illness overlap. **Already handled** by 症 line 14. |
| E6 粒 | grain; small particle | 穀 | `repo/kanji/粒.md:21-22,31-37`: grain/individual particle. **Already handled** by 穀 line 14; materials and category/unit distinctions remain. |
| E7 収 | collect; store | 穫 | `repo/kanji/収.md:21-23,29-37`: collecting/obtaining. **Already handled** by 穫 line 14; no transitive protection for 集/拾. |
| E8 青 | blue, green | 紺 | `repo/kanji/青.md:30-31,35-39`: broad blue includes the narrower shade comparison. **Already handled** by 紺 line 14; green uses are not all navy. |
| E9 気 | spirit, air | 汽, 雰 | `repo/kanji/気.md:21-23,29-33,44`: air/vapor/atmosphere and feeling. **Already handled** by 汽 and 雰 line 14 independently; キ sharing does not make compounds interchangeable. |
| E10 妖 | bewitching; supernatural | 魅 | `repo/kanji/妖.md:21-23,31-32,43-45` and fetched Daijisen 魅: allure and supernatural beings. **Already handled** by 魅 line 14; not transitive protection against 怪. |

C-source exclusions also inspected: `repo/kanji/府.md:3,21,36` supports 寮's existing administrative comparison, and `repo/kanji/米.md:3,21-22,42-45` supports 穀's existing rice-grain comparison. The new-card 汽/雰 pair is declared on 雰; it is effective symmetrically without duplication. These were not requested as E.

## Word changes and stroke references

**All fifteen link-only changes: CLEAN.** `diffs/existing.diff:1-195` contains exactly one wrapping link per mapped word introduction, with no changed Japanese spelling, kana reading, gloss, sentence, metadata, exclusion or level. Complete post-change articles were read; the wrapper points to the intended new kanji and each new kanji links back to that mapped article.

| Changed word | New target | Reading verified against the complete matched family |
| --- | --- | --- |
| 娯楽 | 娯 | ごらく, 1269290 |
| 寮 | 寮 | りょう, 1554230 |
| 廊下 | 廊 | ろうか, 1560670 |
| 栓 | 栓 | せん, 1956550 |
| 汽車 | 汽 | きしゃ, 1222700 |
| 症状 | 症 | しょうじょう, 1351030 |
| 鉄砲 | 砲 | てっぽう, 1438010 |
| 碁 | 碁 | ご, 1270870 |
| 磁石 | 磁 | じしゃく, with additional じせき, 1317080 |
| 穀物 | 穀 | こくもつ, 1287280 |
| 収穫 | 穫 | しゅうかく, 1330510 |
| 砂糖 | 糖 | さとう, 1291600 |
| 紺 | 紺 | こん, 1290590 |
| 雰囲気 | 雰 | ふんいき, with irregular ふいんき separately flagged, 1505070 |
| 魅力 | 魅 | みりょく, 1528150 |

The evidence supports fifteen declared pairs, fifteen distinct reused articles and fifteen added links; no new word/article file was created. Existing word study labels and exclusions remain unchanged. This review does not extend reciprocal-link obligations to every incidental word mention.

**Stroke JSON textual consistency: CLEAN; fresh visual geometry: UNVERIFIED.** Every JSON is source line 1, schemaVersion 1, the correct character, `viewBox [0,0,109,109]`, the same KanjiVG revision `70a0b7ae0c18ceb5cb358274b029cce0234a43bc`, and sequential IDs through its declared count. Counts are 娯 10, 寮 15, 廊 12, 栓 10, 汽 7, 症 10, 砲 10, 碁 13, 磁 14, 穀 14, 穫 18, 糖 16, 紺 11, 雰 12, 魅 15, agreeing with card metadata and `evidence/shape-evidence.json:1-152`. Frozen classical radical numbers, source grades and full reading inventories agree with the complete KANJIDIC2 records.

Modern component descriptions are consistent with the supplied component-tree text, including 水/氵, 廊's 邑-side form, 穀's classical 禾 versus separate Nelson annotation, and compressed 糸. The mnemonic language makes no new etymology claim. KanjiVG `phon=` annotations do not force historical phonetic claims into cards deliberately using `structure-unclassified`. Coordinates were read, not rendered or freshly matched to SVG/PDF glyphs.

## Mechanical evidence

All ten supplied logs were read, not rerun:

- `checks/lint.txt:1-2`: fifteen kanji and fifteen words; zero errors/warnings.
- `checks/quiz-safety.txt:1-44`: the actual curated meaning labels and reading-choice deficits; zero reported structural problems.
- `checks/linkplan.txt:1`: fifteen changed articles/pairs/added links, zero remark edits/problems.
- `checks/reading-exposure-final.txt:1-238`: Python-model reachability and 100 sampled seeds per specified prompt/pool; zero modeled N1/All hits, zero modeled padded-session hits, one latent 碁/キ collision.
- `checks/unittest.txt:18-22`: 431 tests and OK, as supplied historical execution evidence.
- `checks/validate.txt:1`: zero errors.
- `checks/manifest.txt:1` and `checks/manifest-rebuild.txt:1`: matching 8,664 runtime files and content version `20f92e77ce1686f0`.
- `checks/budget.txt:1`: local estimate 8,686 entries, 45,953,599 inflated bytes, 30,854,676 local-ZIP bytes; not an exact immutable public GitHub ZIP test.
- `checks/vocabulary.txt:1`: 2,122/2,431 reviewed prompts, stage pilot; not complete vocabulary-help acceptance.

These establish supplied static/model evidence, not fresh execution, linguistic proof, exact publication integrity, physical-phone acceptance or compatibility with installed APK `5c000bd`.

## Optional points

**O1: none.** No unrelated vocabulary, mnemonic expansion, new historical analysis or routine wording polish is required to address the demonstrated gaps.

## Limits

### L1 - Missing requested comparison cards

銃, 棋 and 陶 have no `repo/kanji` card in the original packet, as reported above. Their dictionary relationships are visible in complete families (銃/砲 つつ, 棋/碁 ご, and 磁器's 陶器 cross-reference), but no actual displayed label/frontmatter exists here to adjudicate a current card pair. This is not a request to create them or to substitute another card. No existing missing-card exclusion is recommended.

### L2 - Identified but unread comparisons

The following existing exclusion candidates were visible in the original eligibility reference and title index but were not requested because E was capped at ten. Their original direct declarations were seen on the new card; their comparison-card bodies/frontmatter were **not** opened. Consequently, this report does not certify the necessity, minimality or complete semantic adequacy of every existing guard.

| Related new card | Unread existing targets | Reason for relevance and limit |
| --- | --- | --- |
| 娯 | 遊, 享, 喜, 快, 幸 | Play, enjoyment, rejoicing, pleasure and happiness cues; only 楽 was selected as E evidence. |
| 寮 | 宿, 宅, 住, 家, 亭, 官, 局, 署 | Lodging/residence, pavilion and government-office comparisons; 室/館 were selected, 府 was already C. |
| 廊 | 堂, 路, 道, 通, 塔 | Hall/passage/path/tower cues; only 館 was E. The retained tower gloss is qualified, not freshly established usage. |
| 栓 | 閉, 詰, 止, 判 | Shutting/packing/stopping and the English seal ambiguity; only 封 was E. |
| 汽 | 蒸 | Direct steam cue; 気 was E and 雰 was a required new card. |
| 症 | 患, 状, 態 | Illness and broad condition/state; only 病 was E. |
| 穀 | 麦, 稲, 種, 実 | Particular crops, seed and fruit senses; 粒 was E, 米 was C. |
| 穫 | 刈, 採, 取, 得, 捕, 果, 実 | Reaping/gathering, gains/catch and fruitful results; only 収 was E. |
| 紺 | 濃, 暗 | Deep/dark cues; only 青 was E. |
| 魅 | 符 | English charm/talisman ambiguity; only 妖 was E. |

Additional new-target candidates noticed from the full index or later source reading but not included in the final capped D list:

| Unread candidate(s) | Related target(s) | Reason and disposition limit |
| --- | --- | --- |
| 頭 | 寮 | “head” cue in complete つかさ family; ordinary applicability to 寮 is not established by grouping. D included 首/長, not 頭. |
| 屋, 庫, 蔵 | 寮 | Roof/building/storage cues; related spaces rather than demonstrated dormitory synonyms. Actual texts unread, no required pair concluded. |
| 僚, 公 | 寮 | Colleague/official cues; institution/person distinctions require actual text. Unread, not a synonym conclusion. |
| 途, 経 | 廊 | Route/pass-through index cues; actual cards unread. Existing 路/道/通 guards do not establish all further pairs. |
| 空, 風, 情, 感 | 雰 | Sky/air, style and mood/feeling search cues; not automatically atmosphere/ambience meanings. Actual texts unread. |
| 兵, 軍, 武, 発, 爆 | 砲 | Military, emission and explosion cues, plus the read 発砲 family; likely subject/action distinctions, not demonstrated gun labels. Actual texts unread. |
| 行 | 碁 | English movement “go,” explicitly not the Go board game. Index title read, card unread; no pair inferred from the English homograph. |
| 板, 皿, 瓶 | 磁 | Objects potentially made from porcelain; material/object distinction is not automatic synonymy. Actual texts unread. |
| 耕, 農, 漁, 産, 積, 功, 豊, 財, 貨, 貯 | 穀, 穫 | Farming/fishing, production, accumulation, achievements, abundance and gain/storage cues. Actual texts unread; no additional exclusions concluded from the index or mnemonic association alone. |

For the C-title index comparisons noted in the C table, pre-existing comparison candidates not otherwise opened include 奇, 変, 珍, 優, 微, 観, 見, 安, 平, 静, 敬, 企, 計, 策, 園, 完, 総, 木, 町, 川, 洋, 真, 直, 囲, 括, 固, 点, 時, 畔, 磨, 学, 究, 主, 階, 級, 度, 幅, 号, 種, 般, 型, 赤, 払, 与, 授, 贈, 接, 連, 秒, 冴, 不, 終 and 了. Their **indexed labels** were read; their actual cards were not. They explain why a C label is not unique across all old cards, but do not establish a new-target defect or certify those old cards' global fallback safety. This review did not expand into a fresh corpus-wide repair of the C cards.

No phase-2 addition to D or E was requested. Later candidates remain limits rather than silently read evidence.

### L3 - Supplementary linguistic evidence not independently opened

The failed oversized 寮 fetch verified no dictionary heading. Temple accommodation, the supplementary 寮 つかさ character-reading attribution, and ordinary applicability of the complete つかさ chief/head sense remain unverified. JMdict's office/official and historical bureau/tea-room/villa senses were read; its religious officiant sense is explicitly restricted to 司 and must not be assigned to 寮.

No public heading was fetched for 娯's extra たのしむ/たのしみ, 穀's たなつもの/beans, 糖's あめ, 紺's purplish shade, or the separate bare-砲 baseball/home-run assertion. Card citations and the exposure adapter's “card text” labels are not independent verification of these supplemental assertions. The matched 大砲 baseball sense supports that whole word, not automatically every bare-砲 use. These are unverified claims, not demonstrated falsehoods or authority to erase frozen metadata.

Other public character headings and arbitrary compounds beyond the 65 exported families were not fetched. Empty exact-character dictionary queries do not prove impossibility. No frequency or blanket modern-naturalness claim is inferred from dictionary inclusion; the read model examples remain ordinary noun/construction examples, not invented rare collocations.

### L4 - Exact level/publication/asset evidence outside the chain

The full current kanjiapi N1 membership list was not an allowed chain input. `repo/docs/jlpt-levels.md` and `evidence/provenance.json:5-9` identify its policy and pinned hash, but hashes/source-row numbers alone do not independently demonstrate these fifteen characters' exact modern community-set membership. KANJIDIC2's historical JLPT field is not silently treated as the modern source. The cards consistently say community list, not official exam syllabus; their precise modern membership is UNVERIFIED in this access scope.

Unread assets include **all raw stroke SVGs**, the **binary Joyo PDF**, `SHA256SUMS.json`, the full runtime manifest and every other packet asset not represented in the permitted chains. Joyo cached text rows were read, not fresh PDF glyphs. The packet's original files were never opened directly. Source hashes and snapshot identity are supplied evidence, not independently recomputed attestations.

The published 210 N1 additions plus six N2 placements remain historical publication totals supplied in `REVIEW.md:69-71`; these fifteen drafts are not additional deliveries. No push, merge, archive acceptance or manifest-runtime completeness check was performed.

### L5 - Reading model and client/native limits

The external 碁 heading independently verifies キ outside the frozen metadata. `checks/reading-exposure-final.txt:131-136` reports candidate holders and example tiny-pool risks, with no modeled draw in its N1/All or stated Starter configurations. This is a **latent** risk, not a reproduced live-app failure. The standard ご practice example remains correct; an alternative attested reading does not invalidate it.

The model covers full N1/All and explicitly described Starter/borrowed configurations, not arbitrary custom/caller-built pools, multi-borrow Starter behavior, missing accepted content, actual Kotlin draws, native execution or phone acceptance. The log's “production” and “not a pool the app builds” phrases are not universal caller claims. Zero sampled/model hits do not certify unmodeled configurations or protection of every supplementary reading absent from the frozen inventory.

No JVM/Gradle/emulator/ADB work, build, device test or fresh geometry inspection was done. Compatibility with installed APK `5c000bd`, which predates kanji exclusions, remains UNVERIFIED. Content depending on the declared and recommended guards requires an exclusion-aware client; this report does not claim the older APK enforces them.

### L6 - Process boundaries

All conclusions are from evidence opened during this pass. No prior review/reconciliation/audit artifact, author inspection summary, changed checkout, other packet or session history was opened or searched. The automatically produced oversized web-output notice did not authorize its temporary file as an input, and that file was not read. The generic completion reminders received while awaiting the coordinator did not trigger tools, a retry or another pass.

This report is the sole intentional write. It is not a fix, confirmation round, universal linguistic certificate or acceptance of the pending resource/publication gates.
