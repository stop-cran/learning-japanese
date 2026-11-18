# B114 independent first content review — run N1-B114-CLAUDE-001

Snapshot: 8c2bdc27e5d556e639a4d0e9239ae5f2009c400f (base 0485c873d2ac636373c7bdf739df97ff66f9160f); packet batch-114-8c2bdc27, SHA256SUMS.json eb6b1042…1e15 as stated in the run instruction (not re-hashed by me).
Scope: 15 new kanji cards (娯 寮 廊 栓 汽 症 砲 碁 磁 穀 穫 糖 紺 雰 魅), their 15 stroke JSONs, the 15 link-only changes to existing word articles (diffs/existing.diff + snapshot/words), the 45 curated distractor slots (41 distinct cards), 40 requested D cards and 10 requested E cards. Read-only. One reviewer.
Reviewer model: the runtime declares Claude Opus 5.5 (claude-opus-5.5). I cannot independently verify the execution model, so treat its identity as UNVERIFIED.

## Overall verdicts

| Facet | Verdict | Basis |
| --- | --- | --- |
| Correctness | CLEAN | I checked every metadata field, reading, stroke count and dictionary claim against KANJIDIC2/JMdict/Joyo rows and found no contradiction. Claims sourced only to Daijisen are UNVERIFIED (L4), but they are qualified secondary notes and are not consequential. |
| Scoped coverage | CLEAN | Each card covers its selected reading with a linked example, the practical compounds and the needed qualifications. Nothing required is missing. |
| Consistency / quiz safety | NEEDS FIX | F1–F3 are minor gaps in direct exclusion pairs, judged against the card set's own exclusion precedent. The structure, links, manifest and checks are clean. |
| Comprehensibility | CLEAN | Mnemonics are labelled as mnemonics. Whole-word cautions (娯楽 ラク, 廊下 ろうか, 鉄砲 てっぽう, 雰囲気 ふんいき) are clear. |

**Overall: NEEDS FIX** (minor; consistency/quiz-safety only).

## Findings

**F1 — Minor; consistency/quiz safety; snapshot/kanji/穀.md:15, 70-72; repo/kanji/穂.md:3.**
Claim: 穀 "grain; cereals" has no direct exclusion with 穂 "grain-bearing head". Both displayed labels use the head word *grain*, and 穂 *is* the ear or head of grain (穂.md body: "an ear or head of grain"). If 穂 is the prompt, the option "grain; cereals" is a defensible pick for a learner. 穀 already excludes 粒 "grain; small particle" on the strength of the shared English label alone (穀.md:66-69), and that semantic link is weaker than the one with 穂. 穀.md:70-72 discusses 穂 but neither excludes it nor gives a reason for the asymmetry.
Impact: none in the modelled N1/All pools, because the curated options for both cards fill all three slots (quiz-safety 3/3). The pair can still co-occur in fallback, custom or small pools, which the exclusion mechanism explicitly covers (content-format.md, Quiz authoring).
Remedy: add 穂 to 穀's quiz_exclusions (one direction is enough), and adjust the 穀.md:70-72 note to say the pair is excluded.
Evidence: title index lines 穀/穂/粒; 穂.md Meaning; 穀.md Notes.
Confidence: medium-high that the ambiguity is real and inconsistent with the 粒 precedent; low that it is learner-harmful in the default pools.

**F2 — Minor; consistency/quiz safety; snapshot/kanji/碁.md:15, 63-65; repo/kanji/盤.md:15 and Notes bullets 2-3.**
Claim: 碁 "Go board game" has `quiz_exclusions: []`. 盤 "board; disc" shares the displayed word *board*, and there is a real lexical link: 碁盤 ごばん "Go board" (JMdict 1270890, listed on the 碁 card itself). 盤's own text also records a game-stage sense. The repository's precedent is to exclude even a pure English-spelling overlap: 盤 excludes 乗 "ride; board" for exactly that reason. 碁/盤 has the same label overlap plus a genuine semantic connection.
Impact: if 盤 is the prompt, "Go board game" is a tempting near-answer, and the reverse holds when 碁 is the prompt. As in F1, live exposure is only in fallback/custom pools (碁 curated 3/3).
Remedy: add 盤 to 碁's quiz_exclusions (or declare it on 盤), or record in 碁's Notes why the pair is deliberately left open. 板 "plank; board" and 行 "go" are weaker label-only overlaps (see O1).
Confidence: medium.

**F3 — Minor; consistency/quiz safety; snapshot/kanji/寮.md:15, 62-69; repo/kanji/房.md:3, 15 and Notes.**
Claim: 寮 "dormitory; quarters" excludes 室 "room, chamber" because "room and accommodation uses connect with 室 and 館". It does not exclude 房 "room; tassel; bunch". 房 displays the same *room* label, and its own card documents a Daijisen dwelling sense: side room/dwelling, 僧房 "priests' temple quarters", 独房 "cell". The 寮 card itself cites Daijisen for temple accommodation for monks. On the card's stated basis, 房 is at least as close as 室.
Impact: same fallback-pool limitation as F1/F2.
Remedy: add 房 to 寮's quiz_exclusions, or explain the deliberate difference in the 寮 Notes. See also O2 (庁).
Confidence: medium.

No critical or major defect was found.

## Optional points

- **O1** — 碁: 板 "plank; board" (label-only *board*) and 行 "go" (English head word *go*, differing only in case) could also be guarded. The current text, "The label explicitly names the board game", is a defensible editorial choice; I am noting it for consistency, not as a defect.
- **O2** — 寮: the historical bureau sense is protected through 官 局 署 府, but 庁 "government agency" is left out. 府.md and 庁.md both say 府/庁 share administrative associations. If the bureau protection is kept, 庁 belongs with it. Either way, 寮's displayed title does not show the bureau sense, so the whole bureau set is conservative.
- **O3** — 穫: it excludes 取 "take" and 採 "pick; collect", but not 集 "gather" or 拾 "pick up; gather". Harvesting is gathering crops, so 集 is at least as close as 取. This is low risk, a consistency polish only.
- **O4** — 栓 excludes 判 "judge; seal", and 廊 excludes 塔 "tower; pagoda". These are conservative over-exclusions: 栓's displayed title has no *seal*, and the tower gloss is source-only. They are harmless (they only shrink fallback pools) and the cards disclose them. No change required.
- **O5** — Existing repo/kanji/気.md Notes says "汽 is steam only" and mentions 汽 unlinked. Now that the 汽 card exists, a link and a small wording adjustment ("steam; vapor"; 汽水 brackish water) would align the two. This card is outside the changed set, so it is not a B114 defect.
- **O6** — Metadata lines cite JMdict entries that are not shown in the card text: 砲 cites 1477900 発砲 and 寮 cites 1455860 独身寮. This is harmless provenance breadth.
- **O7** — 症.md glosses 重症 as "serious illness; severe condition". JMdict 1336310 gives only "serious illness". The extra gloss is reasonable but goes beyond the cited entry.

## Limits

- **L1** — I read only the chain inputs. I did not open the raw stroke SVGs, the binary Joyo PDF, the full manifest, repo/words beyond the 15 mapped articles, or any other packet asset. The Joyo evidence is the extracted text rows, not a fresh visual glyph check (廊 prints a variant glyph in brackets; I did not inspect it).
- **L2** — Stroke JSONs were checked only against card, evidence and contract text. All 15 strokeCount values match the card `strokes` and KANJIDIC2, and all use KanjiVG revision 70a0b7ae and schema 1. I make no visual geometry claim.
- **L3** — The reading-exposure log is a Python model of N1/All pools and a Starter session with one borrowed card. Custom or caller-built pools, multi-borrow Starter, Kotlin execution, native/phone acceptance and compatibility with installed APK 5c000bd (which predates quiz_exclusions, so F1–F3 and every existing exclusion are ignored there) are not established. JVM/emulator work remains on hold.
- **L4** — Statements sourced only to Digital Daijisen are UNVERIFIED in this pass, and I used no web_fetch. They are: 娯 たのしむ/たのしみ; 寮 temple-monk accommodation; 碁 キ; 糖 あめ; 砲 baseball heavy-hitter; 穀 beans and たなつもの; 紺 purplish cast; 雰 氛; 魅 spirit/monster sense; 栓 word 栓をする. All are presented as qualified recognition notes outside the frozen metadata and practice selections, so none is consequential. The checker's "card text" supplemental readings (娯 たのしむ, 碁 き, 糖 あめ, 穀 たなつもの) inherit this limit.
- **L5** — Candidates I noticed but did not read, because the phase-1 lists were final: 空 "sky; empty" and 風 (雰 atmosphere/air); 愛, 恋 (魅 attraction); 耕, 産 (穫); 爆 (砲); 黒, 緑 (紺); 盆 and 皿 (sense neighbours of 盤, for 碁). From their index titles alone they look harmless or remote, but I did not inspect them. Characters with no card at this commit (for example 銃, 霧, 疾, 獲, 陶, 藍, 惑, 誘, 棋) do not appear in the 1221-line index, so they are not current quiz collisions. Future additions of 銃 (gun), 霧 (fog/mist) and 獲 (catch) will need direct-pair checks against 砲, 雰 and 穫.
- **L6** — Checks are host/static evidence, not linguistic proof: lint 0/0, quiz-safety 0/0, linkplan 15/15/0 problems, validate 0 errors, unittest 431 OK, manifest and rebuild identical (8664, 20f92e77ce1686f0), budget within limits, vocabulary 2122/2431 pilot.

## Read record

- **Core chain:** segments 1–40, read once each in order, with no re-views.
- **Extension chain (b114-N1-B114-CLAUDE-001-extension):** segments 1–11, read once each in order, with no re-views.
- **Title index:** I read evidence/title-index.txt source lines 1–1221 (core segments 30–31). Line 1 is "一 one" and line 1221 is "齢 age; years lived".
- **C cards:** all 41 distinct distractor cards were read in core segments 32–40.

### Phase-1 lists as sent (all existed; Missing entries: none)

- D1 穂 - 穀: grain
- D2 行 - 碁: English head word go
- D3 盤 - 碁: board
- D4 板 - 碁: board
- D5 石 - 碁, 磁: stones / magnet stone
- D6 煙 - 汽, 雰: smoke vs steam/vapor/mist
- D7 雲 - 雰: cloud vs mist
- D8 曇 - 雰: cloudy weather vs mist
- D9 湿 - 雰, 汽: damp vs mist/vapor
- D10 甘 - 糖: sweet vs sugar
- D11 菓 - 糖: sweets vs sugar
- D12 粉 - 糖, 穀: powder/flour
- D13 停 - 栓: stopping vs stopper
- D14 経 - 廊: pass through vs passage
- D15 途 - 廊: route vs passage
- D16 候 - 症: weather conditions vs condition
- D17 痛 - 症: pain
- D18 熱 - 症, 汽: fever/heat
- D19 況 - 症: circumstances
- D20 療 - 症: heal
- D21 撃 - 砲: shoot
- D22 射 - 砲: shoot
- D23 筒 - 砲: tube/barrel
- D24 兵 - 砲: troops
- D25 武 - 砲: military
- D26 器 - 磁, 砲: vessel/instrument
- D27 引 - 磁, 魅: draw/attract
- D28 拾 - 穫: gather
- D29 集 - 穫: gather
- D30 美 - 魅: beauty
- D31 怪 - 魅: uncanny
- D32 好 - 魅: liking
- D33 芸 - 娯: performance
- D34 休 - 娯: rest
- D35 湯 - 汽: hot water
- D36 泊 - 寮: stay overnight
- D37 居 - 寮: dwell
- D38 房 - 寮: room/quarters
- D39 庁 - 寮: bureau sense
- D40 深 - 紺: deep
- E1 遊
- E2 判
- E3 符
- E4 妖
- E5 塔
- E6 亭
- E7 粒
- E8 実
- E9 状
- E10 気

The reasons are as in the phase-1 message.

### Every D/E card read

| Card | Displayed title | Related new card | Reason requested | Disposition |
| --- | --- | --- | --- | --- |
| 穂 | grain-bearing head | 穀 | shared *grain* | **Needs exclusion (F1)** |
| 行 | go | 碁 | English *go* | Harmless; optional (O1) |
| 盤 | board; disc | 碁 | *board*, 碁盤 | **Needs exclusion or rationale (F2)** |
| 板 | plank; board | 碁 | *board* | Harmless label overlap (O1) |
| 石 | stone | 碁, 磁 | Go stones, 磁石 | Harmless: component/compound, not the meaning |
| 煙 | smoke | 汽, 雰 | plume/vapor | Harmless: distinct substance, cards contrast it |
| 雲 | cloud | 雰 | mist | Harmless: distinct, 雰 card contrasts it |
| 曇 | cloud over; cloudy weather | 雰 | mist | Harmless |
| 湿 | damp, moist | 雰, 汽 | moisture | Harmless |
| 甘 | sweet; pamper | 糖 | sweet/sugar | Harmless: 糖 card states the substance vs taste distinction |
| 菓 | confectionery; sweets | 糖 | sweets | Harmless: ingredient vs product, card contrasts it |
| 粉 | flour; powder | 糖, 穀 | powder/flour | Harmless |
| 停 | halt; stopping | 栓 | stop stem | Harmless: action vs object |
| 経 | pass through; sutra | 廊 | passage | Harmless |
| 途 | route; course | 廊 | passage | Harmless |
| 候 | weather conditions | 症 | conditions | Harmless: 症's title lacks *condition*, card explains it |
| 痛 | pain; hurt | 症 | symptom | Harmless |
| 熱 | heat; fever | 症, 汽 | fever/heat | Harmless |
| 況 | situation; circumstances | 症 | condition | Harmless |
| 療 | heal; cure | 症 | health | Harmless |
| 撃 | shoot; strike | 砲 | shooting | Harmless: action vs weapon, card explains it |
| 射 | shoot; shine into | 砲 | shooting | Harmless |
| 筒 | cylinder; tube | 砲 | barrel, つつ | Harmless |
| 兵 | soldier; troops | 砲 | military | Harmless |
| 武 | military; warrior | 砲 | military | Harmless |
| 器 | vessel; instrument | 磁, 砲 | porcelain ware/weapon | Harmless |
| 引 | pull; draw | 磁, 魅 | attraction | Harmless |
| 拾 | pick up; gather | 穫 | gather | Harmless; consistency polish (O3) |
| 集 | gather | 穫 | gather | Borderline; optional (O3) |
| 美 | beauty | 魅 | appeal | Harmless: 魅 card says charm is not just beauty |
| 怪 | suspicious; uncanny | 魅 | supernatural | Harmless: 魅's displayed title lacks the monster sense |
| 好 | liking; favorable | 魅 | appeal | Harmless |
| 芸 | art; performance; craft | 娯 | entertainment | Harmless |
| 休 | rest | 娯 | recreation | Harmless |
| 湯 | hot water | 汽 | steam | Harmless |
| 泊 | stay overnight; anchor | 寮 | lodging | Harmless |
| 居 | be present; dwell | 寮 | dwelling | Harmless |
| 房 | room; tassel; bunch | 寮 | room/quarters | **Needs exclusion or rationale (F3)** |
| 庁 | government agency | 寮 | bureau sense | Optional (O2) |
| 深 | deep | 紺 | deep blue | Harmless: 紺 displays "navy blue" |
| 遊 (E) | play | 娯; 碁 note | exclusion/rationale | Already handled for 娯; harmless for 碁 |
| 判 (E) | judge; seal | 栓 | seal | Already handled (conservative, O4) |
| 符 (E) | token; sign; charm | 魅 | charm | Already handled, justified |
| 妖 (E) | bewitching; supernatural | 魅 | bewitch | Already handled, justified |
| 塔 (E) | tower; pagoda | 廊 | tower gloss | Already handled (conservative, O4) |
| 亭 (E) | pavilion; restaurant building | 寮 | tea pavilion | Already handled, justified (KANJIDIC "tea pavillion") |
| 粒 (E) | grain; small particle | 穀 | grain | Already handled; it is the precedent for F1 |
| 実 (E) | reality; fruit | 穀, 穫 | seed/fruit | Already handled, justified |
| 状 (E) | condition; form | 症 | condition | Already handled, justified |
| 気 (E) | spirit, air | 汽, 雰 | air/vapor | Already handled, justified (O5 on its text) |

### C cards (41 distinct; title, defensibility, reading overlap)

All C titles match the index. None is a defensible meaning answer for its new card.

Reading overlaps are excluded mechanically from reading options:
- 誤 ゴ for 娯
- 正, 政, 床 ショウ for 症
- 包 ホウ for 砲
- 分 フン for 雰
- 未 ミ for 魅

The other C cards with semantic proximity are acceptable:
- 床 "floor; bed" for 症: bed is not illness.
- 秋 "autumn" for 穫: season vs action; the card says so.
- 紅 "crimson; deep red" for 紺: a different colour.
- 米 "rice grain" for 糖: rice is not sugar. 米 is a C card here and separately excluded by 穀; that is not a conflict.
- 府 for 廊: it is also excluded by 寮; no conflict.
- 河, 池, 海 for 汽: water bodies, not steam.
- 雪, 晴 for 雰: snow and clear skies are not mist.

目 "eye" for 碁 is a simple shape contrast. The Go-term use of 目 is not its displayed meaning.

## Per-card results (new cards)

For each card I checked:
- metadata against KANJIDIC2 and source-metadata (stroke count, grade, radical, on'yomi, empty kun'yomi);
- that quizOnyomi is a single selected reading with a linked example row;
- that quizKunyomi is [];
- the Joyo row;
- the stroke JSON count.

All 15 pass these checks.

| Card | Title vs index | Exclusions judged | Result |
| --- | --- | --- | --- |
| 娯 | unique | 楽 遊 享 喜 快 幸 justified | CLEAN |
| 寮 | unique | lodging/room/bureau set justified; 房 missing; 庁 optional | NEEDS FIX (F3) |
| 廊 | unique | 堂 館 (hall) and 路 道 通 justified; 塔 conservative | CLEAN |
| 栓 | unique | 封 閉 詰 止 justified; 判 conservative | CLEAN |
| 汽 | unique | 蒸 気 justified; 雰 pair declared on 雰 | CLEAN |
| 症 | unique | 病 患 状 態 justified; 候 harmless and explained | CLEAN |
| 砲 | unique; no gun/cannon competitor in index | [] adequate at this commit | CLEAN |
| 碁 | unique | [] leaves 盤 open | NEEDS FIX (F2) |
| 磁 | unique; no magnet/porcelain competitor | [] adequate | CLEAN |
| 穀 | shares *grain* with 粒 (excluded) and 穂 (not) | 米 麦 稲 種 粒 実 justified; 穂 missing | NEEDS FIX (F1) |
| 穫 | unique; 刈 *reap* excluded | set justified; 集/拾 optional | CLEAN |
| 糖 | unique | [] adequate; 甘/菓 harmless | CLEAN |
| 紺 | unique | 青 濃 暗 justified | CLEAN |
| 雰 | unique | 気 汽 justified | CLEAN |
| 魅 | 符 shares *charm* (excluded) | 妖 符 justified | CLEAN |

Card-specific correctness observations, all CLEAN against the packet evidence:
- 廊's alternative 11-stroke annotation matches KANJIDIC2.
- 寮's つかさ restriction matches JMdict 2251080 (stagk 司).
- 汽車's dated and rural senses match JMdict 1222700.
- 雰囲気's obsolete physical-atmosphere sense and ふいんき irregular flag match JMdict 1505070.
- 収穫's catch sense matches JMdict 1330510 sense 3.
- 鉄砲's sumo/pufferfish senses match JMdict 1438010.
- 碁's 棊/棋 spellings match JMdict 1270870.
- 磁石's じせき reading matches JMdict 1317080.
- Mnemonics are labelled as such and agree with the KanjiVG component trees.
- KanjiVG's phon annotations are not asserted, and the cards stay structure-unclassified. That is conservative and acceptable.

## Word-article link changes

diffs/existing.diff contains exactly 15 hunks, each changing one line. In each hunk a plain new-kanji mention in "How the kanji combine" is wrapped as `[X](../kanji/X.md)`. All 15 targets are the correct new card, with relative paths inside kanji/. The surrounding text, front matter (including jlpt and quiz_exclusions) and readings are unchanged. The snapshot articles match the diff. linkplan reports 15/15 with 0 problems.

Verdict: CLEAN.
