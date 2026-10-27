## Snapshot: 3d66845af7cc97508b6a8d4348f0792e2cbdb9c6; committed content only

**Result: NEEDS FIX.** I found five missing direct quiz exclusions, one incorrect reading explanation, and one unnecessarily broad exclusion list. The twenty source associations and six kanji edits otherwise pass within the reviewed evidence.

Parent: `ba5b4d4cb75a542fe74572dfb1efff1fe0788693`.

I read `frozen-snapshot.json` first. It declares clean committed content, twenty new articles and no reused articles. **File tools cannot execute Git:** I could not independently establish commit membership, worktree cleanliness, addition-versus-rename history, or the supplied hashes/equivalence claims. The review treats the supplied files as the declared frozen committed snapshot; it makes no assessment of uncommitted changes.

## Scope: GPT-6.1 Sol — gpt-6.1-sol, family gpt

Read completely: all twenty assigned word articles; all six related kanji cards; `related.patch`; `.github\copilot-instructions.md`; `.github\instructions\content-structure.instructions.md`; `docs\content-format.md:18–126`; the permitted confusable-word and JLPT-policy documents; both repository snapshot JSON documents; and only N2:1022–N2:1041 from `docs\n2-vocabulary-sources.tsv`.

Private evidence reads comprised all twenty compact mappings, twenty complete principal families/33 senses, 34 component records, 150 label records, `principal-reading.txt`, all nine complete family-inspection renderings, and both public-body renderings. The nine family renderings cover the supplied **203-family/517-sense union, including the principals**, not all 295 captured identities. Only ranges **1–140 and 400–560** of the large aggregate `review-evidence.json` were read; I did not independently execute its equivalence or inspection checks.

I read **112 pre-existing word articles completely**: all 65 distinct pre-existing exclusion targets, plus these 47 additional comparisons/candidates:

粗, 近所, 周辺, 審判, 裁判, 批判, 成立, 終わり, 住宅, アパート, 家具, 棚, 引き出し, 井戸, 泉, 地理, 地盤, 生き生き, 地下, 石炭, 鉱石, 鉱物, 長期, 長短, 損得, 上級, 初級, 学年, 成績, 高度, 高等, 高級, 松, クラス, 順, 順番, 順々, 度, 加減, 保証, 満ちる, 辺, 辺り, 一, 詩, 抜く, 安心.

I also read `kanji\魚.md` completely. Scoped title searches and exact candidate/component existence checks were navigation, not substitutes for those body reads.

The twenty supplied public captures were inspected as **author captures**, not fresh retrievals. Fresh useful responses included Jisho lexical records for 粗, クラス, 詩 and 一; Kotobank lexical bodies for 近付ける, 段階, 断定 and 審判; and the 魚 reading record from KanjiAPI. Failed, irrelevant or nonlexical responses were not treated as dictionary verification.

No agents, delegation, edits, commands, or prohibited ledgers/reports were used.

## Verdicts: articles, mappings and kanji edits

`CLEAN` means no actionable defect established within this scope. Correctness includes the article’s own declarations; scoped coverage includes missing quiz safeguards. Comprehensibility is assessed separately from factual correctness.

All articles below are **new according to the frozen inventory**. Mapping notation is **JMdict entry; selected senses / additional pinned senses**, using one-based indices.

| Source ID | Associated article — new | Correctness | Scoped coverage | Comprehensibility | Mapping |
|---|---|---|---|---|---|
| N2:1022 | `words\足る.md` | CLEAN | CLEAN | CLEAN | 1404750; 1 / 2,3 |
| N2:1023 | `words\段階.md` | CLEAN | NEEDS FIX — F01 | CLEAN | 1419950; 1,2 / 3,4 |
| N2:1024 | `words\短期.md` | CLEAN | CLEAN | CLEAN | 1418640; 1 / — |
| N2:1025 | `words\炭鉱.md` | CLEAN | CLEAN | CLEAN | 1597260; 1 / 2 |
| N2:1026 | `words\短所.md` | CLEAN | NEEDS FIX — F02 | CLEAN | 1418760; 1 / — |
| N2:1027 | `words\たんす.md` | CLEAN | CLEAN | CLEAN | 1418990; 1 / — |
| N2:1028 | `words\淡水.md` | NEEDS FIX — F03 | CLEAN | CLEAN | 1418460; 1 / — |
| N2:1029 | `words\断水.md` | CLEAN | CLEAN | CLEAN | 1419660; 1 / — |
| N2:1030 | `words\単数.md` | CLEAN | NEEDS FIX — F04 | CLEAN | 1417670; 2 / 1 |
| N2:1031 | `words\団地.md` | CLEAN | CLEAN | CLEAN | 1419300; 1 / — |
| N2:1032 | `words\断定.md` | CLEAN | NEEDS FIX — F05 | CLEAN | 1419740; 1 / 2 |
| N2:1033 | `words\短編.md` | CLEAN | NEEDS FIX — F06 | CLEAN | 1597300; 1 / — |
| N2:1034 | `words\誓う.md` | CLEAN | CLEAN | CLEAN | 1381210; 1 / — |
| N2:1035 | `words\地下水.md` | CLEAN | CLEAN | CLEAN | 1622630; 1 / — |
| N2:1036 | `words\近々.md` | CLEAN | CLEAN | CLEAN | 1578110; 1,2 / — |
| N2:1037 | `words\近付ける.md` | NEEDS FIX — F07 | CLEAN | CLEAN | 1242520; 1,2 / — |
| N2:1038 | `words\近寄る.md` | CLEAN | CLEAN | CLEAN | 1242230; 1 / — |
| N2:1039 | `words\力強い.md` | CLEAN | CLEAN | CLEAN | 1554940; 2 / 1 |
| N2:1040 | `words\千切る.md` | CLEAN | CLEAN | CLEAN | 1389020; 1,2 / 3 |
| N2:1041 | `words\地質.md` | CLEAN | CLEAN | CLEAN | 1421130; 1 / — |

F07 also affects 近寄る through symmetric exclusion behavior, but its remedy is entirely in `近付ける.md`; no defect requiring an edit to `近寄る.md` itself was established.

**Mappings, separately:** each of the twenty associations above is **CLEAN for correctness, scoped coverage and comprehensibility**. Source spellings/readings and IDs are retained. In particular:

- 単数 correctly anchors grammatical sense **2**, and 力強い correctly anchors reassuring sense **2**.
- 炭鉱’s additional shaft sense remains restricted to **炭坑**.
- 団地’s industrial-estate use, 近付ける’s target-state extension and 近寄る’s personal-association use are public-backed additions without fabricated pinned sense numbers.
- 地質’s **じしつ** fabric identity, 2828178, is separated from geological **ちしつ** and is not assigned N2.
- The raw “cut up fine” wording for 千切る is appropriately taught through tearing/plucking, not promoted into an obligatory knife-mincing definition.

These are lexical/mapping judgments, not closure of the repository’s draft review status.

| Related kanji passage | Reciprocal examples checked | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| `kanji\階.md:30,36` | 段階 — だんかい | CLEAN | CLEAN | CLEAN |
| `kanji\短.md:28,35–37` | 短期 — たんき; 短所 — たんしょ; 短編 — たんぺん | CLEAN | CLEAN | CLEAN |
| `kanji\炭.md:28,34` | 炭鉱 — たんこう | CLEAN | CLEAN | CLEAN |
| `kanji\鉱.md:30,37` | 炭鉱 — たんこう | CLEAN | CLEAN | CLEAN |
| `kanji\団.md:30,40` | 団地 — だんち | CLEAN | CLEAN | CLEAN |
| `kanji\編.md:30,39` | 短編 — たんぺん | CLEAN | CLEAN | CLEAN |

All eight primary pairs have substantive word-side links, linked reading-row examples and Common words entries. Existing plain-text 短所/短期 examples were linked rather than duplicated. 編 retains canonical **ヘン**, with **ぺん** explained for the whole word rather than invented as an independent metadata reading.

**Baseline metadata preservation: CLEAN within the supplied patch.** None of the six front-matter metadata blocks changes there. All Han in the twenty primary written word forms are represented in word metadata; existing components receive substantive links, while missing 淡 and 誓 cards are retained in metadata without invented links. Independent parent-to-commit preservation remains subject to the Git limitation.

## Findings: seven actionable items

**F01 — Moderate; scoped coverage / quiz ambiguity — missing 段階–クラス guard.**

**Location:** `words\段階.md:9`; comparison `words\クラス.md:4,26–30`.

**Claim/impact:** クラス is not confined to a school group: its complete article explicitly includes category/rank. That ordinary graded-class use overlaps 段階’s selected level/rank/grade sense, so the displayed “class; group” and “stage; graded level” labels can produce a defensible alternative answer. Neither article declares this pair.

**Minimal remedy:** add `クラス` to 段階’s exclusions. Do not expand this into a general school/level clique.

**Exact evidence:** complete pinned JMdict 1419950, sense 2 (“level; rank; grade; gradation”); the complete クラス article’s rank use; the fresh [段階 dictionary body](https://kotobank.jp/word/段階-563700), which defines its graded-order use.

**Confidence:** medium-high.

**F02 — Moderate; scoped coverage / quiz ambiguity — missing 短所–粗 guard.**

**Location:** `words\短所.md:9,16–18`; comparison `words\粗.md:4,9,16–21,29`.

**Claim/impact:** 粗’s displayed “flaw; fault” and its explicitly taught faults in people or work overlap 短所’s shortcomings. Neither endpoint excludes the other. Their existing links through 欠点/欠陥/弱点 do not supply transitive protection.

**Minimal remedy:** add `粗` to 短所’s exclusions; one declaration protects both directions and their appearance among other choices.

**Exact evidence:** complete pinned 1418760:1; complete 粗 article; fresh [Jisho response for 粗](https://jisho.org/api/v1/search/words?keyword=粗), specifically the **あら** lexical record’s flaw/fault/defect meaning—not the separate そ reading or fish-only material.

**Confidence:** high.

**F03 — Minor; correctness / reading explanation — 魚 is not voiced into ギョ here.**

**Location:** `words\淡水.md:25`.

**Claim/impact:** “the fish character is voiced to ぎょ here” incorrectly presents the reading as a compound-induced voicing change. **ギョ is 魚’s ordinary on-reading.** The supplied whole-word reading たんすいぎょ is correct.

**Minimal remedy:** replace the explanation with “魚 uses its on-reading ギョ here,” or simply retain the whole-word reading without a sound-change claim.

**Exact evidence:** `kanji\魚.md` lists `onyomi: [ギョ]` and the ギョ reading row; the fresh [KanjiAPI 魚 record](https://kanjiapi.dev/v1/kanji/魚) likewise returns `on_readings: ["ギョ"]`.

**Confidence:** high.

**F04 — Moderate; scoped coverage / quiz ambiguity — missing 単数–一 guard.**

**Location:** `words\単数.md:9,16,24–26`; comparison `words\一.md:4,15–17`.

**Claim/impact:** The additional general single/one sense is deliberately taught, not merely inferred from the grammatical singular. Consequently 一’s displayed “one” can be accepted for 単数. Protecting 一つ does not protect 一, and their titles are not exactly equal.

**Minimal remedy:** add `一` to 単数’s exclusions while preserving the explanation that 単数 is not an ordinary object counter.

**Exact evidence:** complete pinned 1417670:1 (“single; one”), distinguished from selected grammar sense 2; complete 一 article; fresh [一 lexical response](https://jisho.org/api/v1/search/words?keyword=一), including the いち numeral record.

**Confidence:** high.

**F05 — Moderate; scoped coverage / quiz ambiguity — missing 断定–審判 guard.**

**Location:** `words\断定.md:4,9,16`; comparison `words\審判.md:4,9,16–21`.

**Claim/impact:** 審判’s complete title and body include a judgment/decision, not only a referee or umpire. Its unqualified English “judgment” is a defensible answer for 断定’s definite judgment. The existing 判断 edges do not exclude this direct pair.

**Minimal remedy:** add `審判` to 断定’s exclusions. This does not imply that every judicial, critical or decision-related word needs the same guard.

**Exact evidence:** complete pinned 1419740:1; complete 審判 article, especially 審判を下す; fresh [審判](https://kotobank.jp/word/審判-82448) and [断定](https://kotobank.jp/word/断定-564470) lexical bodies under 精選版 日本国語大辞典.

**Confidence:** medium-high.

**F06 — Moderate; scoped coverage / quiz ambiguity — missing 短編–詩 guard.**

**Location:** `words\短編.md:9,16`; comparison `words\詩.md:4,15–20`.

**Claim/impact:** 短編 explicitly includes a short poem, supported by its complete selected family. Thus 詩’s “poem; poetry” can answer 短編 in that sense. The existing prose/film guards do not protect the poetry use. This is actual meaning overlap, not merely a shared literature category.

**Minimal remedy:** add `詩` to 短編’s exclusions; keep its present practical title and poem recognition.

**Exact evidence:** pinned 1597300:1 includes “short poem”; the supplied Daijisen body includes short 詩歌 works; complete 詩 article and fresh [詩 lexical response](https://jisho.org/api/v1/search/words?keyword=詩).

**Confidence:** high.

**F07 — Minor; correctness / excessive quiz exclusions — 近付ける’s list suppresses distinct causative labels.**

**Location:** `words\近付ける.md:4,9,16–27,46–49`.

**Claim/impact:** All four listed alternatives—接近, 寄る, 迫る and 近寄る—have approaching/drawing-near labels, whereas this article deliberately displays **“bring close; let approach.”** Those labels preserve the causative distinction. The complete comparison bodies do not establish “bring close; let approach” as a meaning of their approaching uses; 迫る’s separate pressing-for sense does not supply it either. Sharing proximity is insufficient grounds to suppress these contrasts.

**Minimal remedy:** remove those four exclusions, retaining the useful body comparisons and particle/transitivity explanations.

**Exact evidence:** complete pinned 1242520:1–2 and the [fresh 近付ける dictionary body](https://kotobank.jp/word/近付ける-565297), including its bring/let-near and target-state meanings; `words\寄る.md:16,32–39`; `words\接近.md:15–19`; `words\迫る.md:16–20`; `words\近寄る.md:16–18,48–49`. The source gloss “associate with” alone does not make the currently displayed causative labels interchangeable with intransitive approaching.

**Confidence:** medium-high.

## Optional: none

No nonblocking expansion is necessary to satisfy the assigned teaching scope. I have not requested exhaustive extra senses, reciprocal examples for every component, or exclusion cliques based on shared categories, homophony or synonym chains.

## Limits: verification boundaries

Git history, committed-file identity, clean-tree status, hashes, rendering equivalence and historical preservation of easier levels remain **UNVERIFIED independently**. Current IDs/levels were inspected, and the supplied related patch preserves baseline kanji metadata; those observations do not replace an executed Git comparison.

The selected family union and 112 old-body reads are substantial but not a whole-corpus ambiguity certification. Unrendered captured identities were not treated as absent. Fresh dictionary responses were not assigned pinned snapshot sense numbers. The failed exact extraction of 近日中 supplies no positive verification and was not relied upon.

Some fresh Weblio responses contained Wikipedia material, unrelated readings or no lexical body; Kotobank/Cambridge requests also failed in places. Those failures were not counted as verification. Public-body captures support their particular definitions, not relative-frequency claims, and this review is not native-speaker certification.
