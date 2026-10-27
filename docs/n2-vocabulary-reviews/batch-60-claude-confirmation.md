# Batch-60 corrected confirmation review (claude-opus-5.5)

## Snapshot
- **Corrected commit:** 1a6ce2c0d34933b13655bad293db5fad6db6b07e.
- **Parent:** d4f6a3e42f752c696ecaa808ea08e7a1b3eb4e00, the authored snapshot. The original parent of that snapshot was 32ac78a1c12f9ea2813b8075036347ac7893f93f.
- **Source:** these values come from correction-snapshot.json, which I read first. It states committed content only.
- **Not verified by me:** my file tools cannot run Git, hash or cleanliness checks, and I did not look inside `.git`. Those checks are the author's.

## Scope
- **Model:** claude-opus-5.5 (claude family). Read-only throughout: no edits, agents or delegation.
- **Read completely this turn:**
  - correction-snapshot.json and the complete correction.patch.
  - reconciliation-comparison-reading.txt: all 13 families and 24 senses.
  - correction-existing-reading.txt: all 12 older articles (苦情, 文句, 不平, 役, 役割, 損害, 格別, 避ける, 丸い, 酸っぱい, ストーブ, 義務).
  - All seven changed articles: 投書, 当番, 溶かす, 特殊, 退く, 尖る, 灯油. Each matches the patch exactly.
  - The TSV header and rows N2:1182–1201.
  - The full words\訴える.md, for a possible quiz clash.
- **Partial checks this turn:**
  - A search of words\ titles for "complain", "duty", "special" and "loss" clashes.
  - A search of the four kanji cards confirming all six reciprocal pairs (灯/灯台, 灯/灯油, 油/灯油, 童/童話, 溶/溶かす, 溶/溶く), including reading rows, Common words lists and source-entry footers.
  - The front matter of どきどき (`jlpt: 2` and unchanged exclusions).
  - A check that no よける reading card exists in words\.
  - A bounded look at corrected-review-evidence.json, from line 28799 only.
- **Inherited from my initial complete reads:** the 13 unchanged articles (including the reused どきどき body), the four kanji cards and all twenty mappings. No regression signal was found.
- **Not read:** the large corrected derivative and most of the evidence JSON.
- **Older-article depth:** my initial review fully read 4 older articles. This turn added 12 full reads; 役, 避ける and ストーブ overlap earlier partial or full reads.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1182 | words\当日.md | Inherited from initial full read | CLEAN | CLEAN | CLEAN |
| N2:1183 | words\投書.md | Full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1184 | words\登場.md | Inherited from initial full read | CLEAN | CLEAN | CLEAN |
| N2:1185 | words\どうせ.md | Inherited from initial full read | CLEAN | CLEAN | CLEAN |
| N2:1186 | words\どうぞよろしく.md | Inherited from initial full read | CLEAN | CLEAN | CLEAN |
| N2:1187 | words\灯台.md | Inherited from initial full read | CLEAN | CLEAN | CLEAN |
| N2:1188 | words\盗難.md | Inherited from initial full read | CLEAN | CLEAN | CLEAN |
| N2:1189 | words\当番.md | Full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1190 | words\等分.md | Inherited from initial full read | CLEAN | CLEAN | CLEAN |
| N2:1191 | words\透明.md | Inherited from initial full read | CLEAN | CLEAN | CLEAN |
| N2:1192 | words\灯油.md | Full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1193 | words\東洋.md | Inherited from initial full read | CLEAN | CLEAN | CLEAN |
| N2:1194 | words\童話.md | Inherited from initial full read | CLEAN | CLEAN | CLEAN |
| N2:1195 | words\通り掛かる.md | Inherited from initial full read | CLEAN | CLEAN | CLEAN |
| N2:1196 | words\溶かす.md | Full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1197 | words\尖る.md | Full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1198 | words\どきどき.md | Reused article; only `jlpt: 2` added; body inherited, front matter rechecked | CLEAN | CLEAN | CLEAN |
| N2:1199 | words\溶く.md | Inherited from initial full read | CLEAN | CLEAN | CLEAN |
| N2:1200 | words\退く.md | Full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1201 | words\特殊.md | Full reread, corrected | CLEAN | CLEAN | CLEAN |

- **Kanji cards 灯, 油, 童, 溶 and the six reciprocal pairs:** CLEAN. The cards are unchanged and the pair links at the real whole-word readings are present (rechecked this turn).
- **Baseline preservation:** CLEAN. Identities, readings, titles, kanji and levels are unchanged. No existing exclusions changed, and the 避ける card still teaches the さける reading.
- **Mappings and TSV:** CLEAN. The TSV was reread and the article associations and selected senses are unchanged. The mapping judgments are inherited.

## Findings
**Dispositions of my original findings:**
- **F1 (投書 should exclude 苦情): RESOLVED.** 投書.md:9 now excludes 苦情, 文句 and 不平.
  - All three have a complaint sense (苦情 1244520:1, 文句 1505260:1, 不平 1494790:1), and their titles name a complaint. 投書's title includes "written complaint", so a quiz could show two correct-looking answers.
  - The additions from GPT's review (文句, 不平) are supported. No transitive inference was relied on.
- **F2 (当番 should exclude 役): RESOLVED.** 当番.md:9 now excludes 役 (1537970:1, "role; duty") and 役割 (1538000:1, "role; allotted duties").
  - **My 義務 consideration is withdrawn.** The full 義務 family (1225900:1) and its article teach obligation under a law, agreement or moral responsibility. That is not a rota turn or the person on duty.
  - Some contextual overlap remains (duty rotas can feel like obligations), but a direct quiz guard is not established.
- **F3 (退く wrongly said 避ける covers moving clear): RESOLVED.** 退く.md:38–40 now says the linked card is さける (avoiding a situation or question) and keeps the physical-avoidance よける reading separate. This matches 1583260 senses 1 and 4, which are restricted to よける.
  - The 避ける guard was removed from 退く.md:9. Their titles no longer collide, and the baseline 避ける identity is preserved.
  - No よける card exists, so leaving it unlinked is correct.
- **F4 (missing comparison links): RESOLVED.** 尖る.md:40 links [丸い], 尖る.md:46 links [酸っぱい], and 灯油.md:25 links [ストーブ].
  - No shape-antonym or sour-taste guard was added, which is correct.
  - ストーブ's article leaves the fuel unspecified, so no "every heater uses kerosene" claim is implied.

**Other author adjudications:**
- **GPT-03 (溶かす excludes 損害), 溶かす.md:9: acceptable.** 1546040:3 is colloquial financial loss, and the 損害 article (1406710:1) teaches monetary loss. This sits alongside the existing 損 guard and does not imply the constructions are interchangeable.
- **GPT-04 (特殊 excludes 格別), 特殊.md:9: acceptable.** 1205490:1 is the special/particular adjectival sense, and the 格別 article says it need not imply praise.
- **灯油 fuel qualifier (灯油.md:42–43): accurate.** "In this modern fuel sense" correctly allows for the historical lamp-oil sense (Daijisen とう‐ゆ sense 1, 灯火用の油).
- **登場 vs 入口/玄関: confirmed not established.** They share only the English word "entrance".

**Regressions:** none found. The diff is exactly seven guard additions, one removal, three links and one qualifier. The new links resolve to existing cards and no front-matter identity fields changed.

**New defects:** none.

## Optional
- 退く.md:39–40: "moving out of the way" could be split into "sidestepping" and "moving something aside" to reflect that よける sense 4 is transitive.
- 投書 vs 訴える ("appeal; complain; sue"): only a weak overlap. One is a verb, and "letter to the editor" disambiguates. I don't think a guard is needed.
- 特殊 vs 特に: they share only the English word "particular", and 特殊 has no adverb sense. Not established.
- Polish: the wording at どうせ.md:36, and the unusual line break after 灯油.md:42 (it renders fine).
- Possible additions from my initial review: 灯台下暗し, 昔話/おとぎ話, 通りがかり, and のく/どける/どかす.

## Limits
- Hash, Git, manifest and cleanliness checks were done by the author; I could not run them.
- I did not read the corrected derivative or most of corrected-review-evidence.json. My judgments on the 13 unchanged articles and the mappings are inherited from my initial full reads, not fresh rereads.
- My full reads of older articles total 4 from the initial review plus 12 this turn, with overlap. This is not an exhaustive check for confusable words.
- The 19 public captures come from one dictionary service, not 19 independent dictionaries. The どうぞよろしく endpoint returned no definition, and I fetched nothing new.
- No runtime quiz draws, native-speaker certification or frequency measurement.
