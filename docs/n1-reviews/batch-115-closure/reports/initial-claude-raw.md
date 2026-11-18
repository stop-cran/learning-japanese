# B115 initial review — N1-B115-CLAUDE-004

## Overall verdict

Verdict: NEEDS FIX

## Facet verdicts

### Correctness

Verdict: CLEAN
Basis: Readings, grades, strokes, radicals, JLPT tags and cited word senses of all eight new cards (卓 厄 宙 寸 康 漠 票 魔) match evidence/source-metadata.json:1-193, evidence/kanjidic2-records.xml:1-577, evidence/joyo-rows.json:1-79, evidence/jmdict-families.xml:1-1069 and evidence/shape-evidence.json:1-82. KANJIDIC2 old-JLPT values for 宙 and 康 are not a defect because the cards state the community N1 list.

### Scoped coverage

Verdict: CLEAN
Basis: Each new card covers its Joyo on reading with linked or dictionary-backed words; the link-only edits in diffs/existing.diff:1-126 to 食卓 厄介 宇宙 寸法 健康 砂漠 投票 悪魔 and 標 are correct, and the reported linkplan covers 8/8 pairs.

### Consistency/quiz safety

Verdict: NEEDS FIX
Basis: Two new cards omit quiz_exclusions for existing cards whose displayed titles overlap as closely as targets the same cards already exclude: 卓 lacks 英, 冠 and 越 (F1) and 寸 lacks 微 (F2). All C distractors are clearly distinct and all ten E exclusion targets are justified.

### Comprehensibility

Verdict: CLEAN
Basis: Titles, mnemonics (labelled as non-etymological), reading tables and Notes are clear and appropriately qualified on all eight cards.

## Segments read

- Core chain: 30/30 segments in order, b115-initial-v1, ending at END OF CHAIN.
- Extension chain: 11/11 segments in order, b115-N1-B115-CLAUDE-004-extension, ending at END OF CHAIN.
- Title index confirmed: evidence/title-index.txt has 1229 lines; line 1 is "一 one" and line 1229 is "齢 age; years lived".

## Phase-1 D/E lists

- D: D1 偉, D2 英, D3 冠, D4 越, D5 著, D6 板, D7 盤, D8 害, D9 危, D10 患, D11 険, D12 損, D13 運, D14 浮, D15 界, D16 星, D17 匁, D18 秒, D19 分, D20 微, D21 粒, D22 軽, D23 福, D24 幸, D25 快, D26 治, D27 療, D28 砂, D29 野, D30 乾, D31 雰, D32 薄, D33 投, D34 選, D35 択, D36 紙, D37 片, D38 神, D39 術, D40 奇
- E: E1 机, E2 表, E3 超, E4 気, E5 間, E6 細, E7 計, E8 札, E9 符, E10 魅
- Missing entries: none

## D/E cards read

| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 偉 | admirable; great | 卓 | eminence/greatness overlap | Moderate overlap; noted in O1 |
| D2 | 英 | English; outstanding | 卓 | "outstanding" vs "eminent" | Collision; F1 |
| D3 | 冠 | crown; peerless | 卓 | "peerless" vs "eminent" | Collision; F1 |
| D4 | 越 | cross over; exceed | 卓 | parallels excluded 超 "exceed; surpass" | Collision; F1 |
| D5 | 著 | write; remarkable | 卓 | "remarkable" vs "eminent" | Moderate; noted in O1 |
| D6 | 板 | plank; board | 卓 | "board" vs "table" | Distinguishable; clean |
| D7 | 盤 | board; disc | 卓 | "board" vs "table" | Distinguishable; clean |
| D8 | 害 | harm | 厄 | harm vs calamity | Moderate; O3 |
| D9 | 危 | danger | 厄 | danger vs calamity | Distinguishable; clean |
| D10 | 患 | be ill; suffer | 厄 | suffering | Distinguishable; clean |
| D11 | 険 | steep; perilous | 厄 | peril | Distinguishable; clean |
| D12 | 損 | loss; damage | 厄 | damage vs calamity | Moderate; O3 |
| D13 | 運 | carry; luck | 厄 | luck vs misfortune | Distinguishable; clean |
| D14 | 浮 | float | 宙 | 宙に浮く context | Distinguishable; clean |
| D15 | 界 | world, boundary | 宙 | world vs space | Distinguishable; clean |
| D16 | 星 | star; celestial point | 宙 | astronomical field | Distinguishable; clean |
| D17 | 匁 | monme (3.75 g) | 寸 | traditional unit | Mass vs length; clean |
| D18 | 秒 | second as a time unit | 寸 | unit | Time vs length; clean |
| D19 | 分 | minute, part | 寸 | small part | Distinguishable; clean |
| D20 | 微 | minute; faint | 寸 | "minute" (tiny) vs "small" | Collision; F2 |
| D21 | 粒 | grain; small particle | 寸 | contains "small" | Distinguishable by "grain"; O2 |
| D22 | 軽 | lightweight; slight | 寸 | "slight" vs "small" | Moderate; O2 |
| D23 | 福 | good fortune | 康 | 幸福 well-being | Moderate; O4 |
| D24 | 幸 | happiness; good fortune | 康 | happiness vs well-being | Moderate; O4 |
| D25 | 快 | pleasant; agreeable | 康 | comfort | Distinguishable; clean |
| D26 | 治 | govern; heal | 康 | health field | Distinguishable; clean |
| D27 | 療 | heal; cure | 康 | health field | Distinguishable; clean |
| D28 | 砂 | sand | 漠 | 砂漠 | Distinguishable; clean |
| D29 | 野 | open field | 漠 | open land | Distinguishable; clean |
| D30 | 乾 | dry; desiccate | 漠 | arid | Distinguishable; clean |
| D31 | 雰 | mist; atmosphere | 漠 | haziness vs vague | Distinguishable; clean |
| D32 | 薄 | thin; dilute | 漠 | faintness | Distinguishable; clean |
| D33 | 投 | throw | 票 | 投票 | Distinguishable; clean |
| D34 | 選 | choose | 票 | election | Distinguishable; clean |
| D35 | 択 | select; opt for | 票 | choice | Distinguishable; clean |
| D36 | 紙 | paper | 票 | slip of paper | Distinguishable; clean |
| D37 | 片 | one-sided; sheet | 票 | sheet vs slip | Distinguishable; clean |
| D38 | 神 | deity | 魔 | supernatural being | Distinguishable; clean |
| D39 | 術 | technique | 魔 | 魔術 | Distinguishable; clean |
| D40 | 奇 | strange; extraordinary | 魔 | uncanny | Distinguishable; clean |
| E1 | 机 | desk; writing table | 卓 | "table" | Exclusion justified |
| E2 | 表 | surface; chart | 卓 | 表 ひょう table sense | Exclusion justified |
| E3 | 超 | exceed; surpass | 卓 | surpassing vs eminent | Exclusion justified |
| E4 | 気 | spirit, air | 宙 | air vs midair/space | Exclusion justified |
| E5 | 間 | interval, between | 宙 | space/gap | Exclusion justified |
| E6 | 細 | slender; fine; detailed | 寸 | smallness | Exclusion justified |
| E7 | 計 | measure; plan | 寸 | measurement | Exclusion justified |
| E8 | 札 | tag; banknote | 票 | slip/ticket | Exclusion justified |
| E9 | 符 | token; sign; charm | 票, 魔 | token; charm | Exclusion justified |
| E10 | 魅 | charm; bewitch | 魔 | bewitch vs magic | Exclusion justified |

## Per-card results

| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 卓 | CLEAN | CLEAN | NEEDS FIX (F1) | CLEAN | snapshot/kanji/卓.md:1-71; repo/kanji/英.md:1-43; repo/kanji/冠.md:1-55; repo/kanji/越.md:1-46 |
| 厄 | CLEAN | CLEAN | CLEAN | CLEAN | snapshot/kanji/厄.md:1-70 |
| 宙 | CLEAN | CLEAN | CLEAN | CLEAN | snapshot/kanji/宙.md:1-70 |
| 寸 | CLEAN | CLEAN | NEEDS FIX (F2) | CLEAN | snapshot/kanji/寸.md:1-70; repo/kanji/微.md:1-82 |
| 康 | CLEAN | CLEAN | CLEAN | CLEAN | snapshot/kanji/康.md:1-71 |
| 漠 | CLEAN | CLEAN | CLEAN | CLEAN | snapshot/kanji/漠.md:1-68 |
| 票 | CLEAN | CLEAN | CLEAN | CLEAN | snapshot/kanji/票.md:1-69; snapshot/kanji/標.md:1-58 |
| 魔 | CLEAN | CLEAN | CLEAN | CLEAN | snapshot/kanji/魔.md:1-73 |

## Findings

### F1: 卓 quiz_exclusions omit 英, 冠 and 越

- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: snapshot/kanji/卓.md:1-71; repo/kanji/英.md:1-43; repo/kanji/冠.md:1-55; repo/kanji/越.md:1-46; repo/kanji/超.md:1-43
- Evidence: 卓 "table; eminent" excludes 優 and 超 "exceed; surpass" for the eminence sense, but not 英 "English; outstanding", 冠 "crown; peerless" or 越 "cross over; exceed". "Outstanding" and "peerless" are near-synonyms of "eminent", and 越 shares "exceed" with the excluded 超 (超.md even links 超える/超す to the 越える/越す word articles). A meaning quiz could offer two equally defensible English answers.
- Required change: Add 英, 冠 and 越 to 卓's quiz_exclusions (or narrow the displayed title so the eminence sense no longer collides), and add a Notes line for these comparisons as done for 優 and 超.

### F2: 寸 quiz_exclusions omit 微

- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: snapshot/kanji/寸.md:1-70; repo/kanji/微.md:1-82; repo/kanji/細.md:1-48
- Evidence: 寸 "sun (length unit); small" excludes 小, 少, 細 and 短 for smallness, but not 微 "minute; faint", whose English "minute" means tiny. 微 itself excludes 細, 小, 少 and 軽 on exactly this smallness overlap. Offering "minute; faint" beside "sun (length unit); small" is as ambiguous as the already-excluded 細 "slender; fine; detailed".
- Required change: Add 微 to 寸's quiz_exclusions and mention the comparison in its Notes.

## Optional points

### O1: 偉 and 著 also approach 卓's "eminent"

- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: medium
- Citations: repo/kanji/偉.md:1-43; repo/kanji/著.md:1-48; snapshot/kanji/卓.md:1-71
- Evidence: 偉 "admirable; great" and 著 "write; remarkable" overlap the eminence sense less directly than F1's targets.
- Suggestion: Consider excluding them together with the F1 change.

### O2: 軽 and 粒 near 寸's "small"

- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: medium
- Citations: repo/kanji/軽.md:1-47; repo/kanji/粒.md:1-45; snapshot/kanji/寸.md:1-70
- Evidence: 軽 "lightweight; slight" (which 微 excludes for slight degree) and 粒 "grain; small particle" contain smallness cues, though each has a distinguishing first gloss.
- Suggestion: Consider excluding 軽.

### O3: 害 and 損 near 厄's "calamity"

- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: repo/kanji/害.md:1-45; repo/kanji/損.md:1-51; snapshot/kanji/厄.md:1-70
- Evidence: "harm" and "loss; damage" are adjacent to "misfortune; calamity" given that 厄 already excludes 苦 and 困.
- Suggestion: Consider excluding 害.

### O4: 幸 and 福 near 康's "well-being"

- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: repo/kanji/幸.md:1-50; repo/kanji/福.md:1-46; snapshot/kanji/康.md:1-71
- Evidence: 幸 "happiness; good fortune" and 福 "good fortune" relate to well-being via 幸福, while 康 already excludes broad comfort targets such as 安 and 楽.
- Suggestion: Consider excluding 幸.

### O5: Reverse exclusions on existing cards

- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: repo/kanji/魅.md:1-74; repo/kanji/微.md:1-82; diffs/existing.diff:1-126
- Evidence: 魅 excludes 妖, 怪 and 符 but not the new 魔, and 微 does not exclude 寸; the diff does not add reciprocal exclusions. Whether the quiz applies exclusions symmetrically was not visible in the chain.
- Suggestion: Confirm symmetric handling, or add 魔 to 魅 and 寸 to 微.

### O6: Reduced reading-quiz distractor pools for 票 and 魔

- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/票.md:1-69; snapshot/kanji/魔.md:1-73; repo/kanji/栗.md:1-47; repo/kanji/鹿.md:1-64; repo/kanji/摩.md:1-51
- Evidence: 栗 and 鹿 have no quiz on reading and 摩 shares マ, so 票 keeps 2 of 3 and 魔 1 of 3 curated distractors in the reading quiz.
- Suggestion: Consider one replacement shape distractor with a distinct on reading.

## Limits

- L1: Raw stroke SVGs, the Joyo PDF (only its recorded SHA-256 in evidence/provenance.json:1-47) and any packet assets outside the two chains were not read.
- L2: Possible related characters not in the deck per evidence/title-index.txt:1-1229 (for example 災, 禍, 鬼, 霊, 尺, 曖) were not reviewed as cards.
- L3: Empty exact-query arrays for 康 and 康健 in evidence/dictionary-index.json:1-125 were treated as non-proof of absence per provenance; the cited JMdict entries are present.
- L4: Check results (lint, validate, linkplan, unit tests, manifest, budget, reading exposure) were accepted as reported in the core chain and not re-run.
- L5: Quiz-engine semantics for exclusion symmetry were not visible; O5 is conditional on them.
- L6: Execution model identity is self-reported (Claude Opus 5.5) and unverified.
- L7: No D/E entries were missing; 0 web_fetch calls were used.
