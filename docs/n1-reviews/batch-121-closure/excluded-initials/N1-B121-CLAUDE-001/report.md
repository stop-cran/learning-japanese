# B121 initial review — N1-B121-CLAUDE-001

## Overall verdict
Verdict: NEEDS FIX

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: Metadata (14 strokes, radical 彳/60, grade 4, on トク, no kun, five nanori), the Joyo トク/道徳 assignment, the JMdict profit cross-reference, the 徳利 ateji flag, 徳行 とっこう, the source-only おしえ and the title senses all match the supplied KANJIDIC2, JMdict, Joyo-row and Weblio evidence; the stroke JSON matches the 14-stroke count and KanjiVG revision; the single 道徳 wrapper targets ../kanji/徳.md with no other change.

### Scoped coverage
Verdict: CLEAN
Basis: The card covers the virtue/benevolence senses, the profit cross-reference to 得, the only on-reading with one linked dictionary-supported word (道徳), and explains why no kun or name reading is selected; no required distinction for the stated scope is missing.

### Consistency/quiz safety
Verdict: NEEDS FIX
Basis: The direct pairs 徳/幸 and 徳/愛 are not declared on either endpoint although 徳's displayed "benevolence" and its blessing sense overlap them on exactly the grounds this card uses to exclude 福 and 恩, and that the existing 恩 card uses to exclude 幸 and 愛 (F1).

### Comprehensibility
Verdict: CLEAN
Basis: The mnemonic is clearly labelled as non-etymological, readings are given with kana, and the Notes separate the moral sense from the profit sense and qualify each comparison; no misleading or unclear passage was established.

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 (each read once, in order; no re-views)
Extension chain: 1, 2, 3, 4, 5, 6 (each read once, in order; no re-views)
Title index evidence/title-index.txt source lines 1-1241 were read in full (core segments 19-20); line 1 is "一 one" and line 1241 is "齢 age; years lived".
REVIEW.md was read first (segment 1). repo/docs/content-format.md was read only for lines 1-139. The one supplied Weblio extract (evidence/external-snapshots/01-extract.txt, lines 1-192) and its manifest were read; they are the only external sources used.

## Phase-1 D/E lists
D: D1 財, D2 幸, D3 格, D4 品, D5 偉, D6 道, D7 美, D8 愛, D9 厚, D10 礼, D11 豊, D12 賢, D13 性, D14 能, D15 宝, D16 謝, D17 才
E: E1 恩, E2 優, E3 正, E4 人, E5 享, E6 教, E7 福, E8 富, E9 尊, E10 敬
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 財 | wealth; property | 徳 | Daijisen word sense 4 of 徳 is 富・財産 (evidence/external-snapshots/01-extract.txt:25-26) | Harmless: that sense is illustrated only by a Genji quotation (01-extract.txt:26) and the character-level money sense is もうけ/profit (01-extract.txt:18), which 利/得 cover; 財.md:20 teaches wealth/assets only. Pair not declared on either endpoint; see O2 on the precautionary 富 exclusion. |
| D2 | 幸 | happiness; good fortune | 徳 | 徳 means めぐみ・恩恵・加護 (01-extract.txt:23); 幸's title contains the exact "good fortune" label of excluded 福 (幸.md:3) | Collision needing exclusion (F1). 恩.md:14 excludes 幸 on the blessing sense; pair not declared on either endpoint. |
| D3 | 格 | rank; character | 徳 | 徳 as すぐれた品性 (01-extract.txt:22) vs "character" | Harmless: 格.md:20 and 格.md:42 define character as neutral personality/qualities (性格) or standing, not moral excellence; 徳's sources gloss evaluative virtue. Not declared. |
| D4 | 品 | goods, refinement | 徳 | 品性-type refinement/dignity | Harmless: 品.md:20 gives refinement or dignity of manner; no supplied 徳 sense glosses refinement, elegance or goods. Not declared. |
| D5 | 偉 | admirable; great | 徳 | KANJIDIC2 "commanding respect" (evidence/kanjidic2-records.xml:56-59); 徳の高い "respectable" | Unresolved borderline: 偉.md:20-21 praises conduct as admirable, close to "commanding respect"; 尊/敬 are excluded on that basis but 偉 is not. Not declared; see O1. |
| D6 | 道 | road, way | 徳 | 道徳 morality; 道 widened to principle (道.md:22) | Harmless: no supplied 徳 sense is road, way or method; 道's principle sense appears only via compounds. Not declared. |
| D7 | 美 | beauty | 徳 | 美徳 "virtue" | Harmless: 美.md:20 is aesthetic beauty; 美徳's virtue meaning belongs to the whole word (JMdict 1486600) and 徳 has no beauty sense. Not declared. |
| D8 | 愛 | love | 徳 | 徳's displayed "benevolence"; 愛 covers affection and care (愛.md:20-21) | Collision needing exclusion (F1). 恩.md:14 excludes 愛 because its benevolence/affection sense overlaps "love"; 徳 displays "benevolence" directly. Not declared on either endpoint. |
| D9 | 厚 | thick; cordial | 徳 | 厚意 kindness (厚.md:20) vs benevolence | Borderline: cordial treatment is a manner, benevolence a disposition; 恩's exclusion set does not include 厚. Not declared; see O1. |
| D10 | 礼 | bow; thanks | 徳 | courtesy/proper conduct; thanks | Harmless: 礼.md:20 covers bow, manners and gratitude; no supplied 徳 sense means thanks or a bow (報徳 is a whole word). Not declared. |
| D11 | 豊 | bountiful; abundant | 徳 | wealth/abundance | Harmless: 豊.md:20 is abundance; 徳's wealth sense is classical only (01-extract.txt:25-26). Not declared. |
| D12 | 賢 | wise; intelligent | 徳 | moral excellence vs wisdom | Harmless: 賢.md:20 is wisdom/judgment; JMdict pairs 知徳/才徳 as "knowledge and virtue" (evidence/jmdict-families.xml:1986-2542), treating them as distinct. Not declared. |
| D13 | 性 | nature; gender | 徳 | Daijisen sense 5 天性 (01-extract.txt:27-28) | Harmless: sense 5 is illustrated only by a classical quotation; 性.md:20 teaches personality/sex. Not declared. |
| D14 | 能 | ability; capacity | 徳 | Daijisen sense 5 innate ability (01-extract.txt:27) | Harmless: same classical sense; 能.md:20 teaches ability/possibility. Not declared. |
| D15 | 宝 | treasure; valuables | 徳 | treasure/wealth | Harmless: 宝.md:20 is treasure/gems; no 徳 treasure sense in supplied evidence. Not declared. |
| D16 | 謝 | apologize; thank | 徳 | gratitude (報徳) | Harmless: 謝.md:3 and its exclusions (謝.md:14) concern apology/thanks/refusal; 徳 has no such sense. Not declared. |
| D17 | 才 | talent | 徳 | innate ability; 才徳 | Harmless: 才.md:20 is talent; 才徳 "intelligence and virtue" treats them as distinct, and the ability sense of 徳 is classical. Not declared. |
| E1 | 恩 | favor; debt of gratitude | 徳 | card claims 恩 includes benevolence | Already handled: declared on 徳 (徳.md:14); 恩.md:29-30 supports いつくしみ benevolence. 恩.md:14 also supplies the 幸/愛 precedent for F1. |
| E2 | 優 | gentle; superior | 徳 | card claims kindness | Already handled: declared on 徳 (徳.md:14); 優.md:20-21 teaches kindness in 優しい. |
| E3 | 正 | correct, proper | 徳 | card claims proper conduct | Already handled: declared (徳.md:14); 正.md:20 judges conduct against a standard. |
| E4 | 人 | person | 徳 | virtuous-person sense | Already handled, precautionary: Daijisen kanji sense すぐれた人格者 (01-extract.txt:16); 人.md:3 "person" is a weak overlap; over-exclusion is harmless. |
| E5 | 享 | enjoy; receive benefits | 徳 | blessing/benefit overlap | Already handled: declared (徳.md:14); 享.md:20 enjoying benefits overlaps 徳's 恩恵 and profit senses. |
| E6 | 教 | teach, instruct | 徳 | source-only おしえ | Already handled, precautionary: 漢字辞典 lists おしえ (01-extract.txt:140-192); 教.md:20 is teaching. |
| E7 | 福 | good fortune | 徳 | blessing | Already handled: declared (徳.md:14); 福.md:20 names a blessing, matching 徳 sense めぐみ (01-extract.txt:23). |
| E8 | 富 | wealth; abundance | 徳 | wealth | Already handled: declared (徳.md:14) on the classical 富・財産 sense (01-extract.txt:25); see O2. |
| E9 | 尊 | revere; esteem | 徳 | commanding respect | Already handled: declared (徳.md:14); KANJIDIC2 "commanding respect" (kanjidic2-records.xml:59); 尊.md:20. |
| E10 | 敬 | respect; honor | 徳 | commanding respect | Already handled: declared (徳.md:14); 敬.md:20. |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 徳 | CLEAN | CLEAN | NEEDS FIX | CLEAN | KANJIDIC2, JMdict 2080970/1454490/1454240/1454660/1661670, Joyo row, Weblio extract, stroke JSON, shape evidence, 道徳 diff; F1, O1, O2, O3 |

## Findings
### F1: Missing direct exclusions 徳/幸 and 徳/愛
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: medium
- Citations: snapshot/kanji/徳.md:3; snapshot/kanji/徳.md:14; snapshot/kanji/徳.md:44; evidence/external-snapshots/01-extract.txt:22-23; repo/kanji/恩.md:14; repo/kanji/恩.md:29-30; repo/kanji/幸.md:3; repo/kanji/愛.md:20-21; repo/kanji/福.md:3
- Evidence: 徳 displays "virtue; benevolence" and Daijisen gives めぐみ・恩恵・神仏などの加護 as sense 2. The card excludes 福 "good fortune" and 恩 on these blessing/benevolence grounds, yet 幸's title "happiness; good fortune" repeats 福's exact label, and 愛 "love" covers affection and care. The existing 恩 card excludes both 幸 (blessing) and 愛 (benevolence/affection) on the same senses. Neither 徳/幸 nor 徳/愛 is declared on either endpoint (徳.md:14; the 幸 and 愛 frontmatter has no quiz_exclusions). The curated options 休/本/木 do not currently expose them, but tag/random fallback in level and custom pools can.
- Required change: Add 幸 and 愛 to 徳's quiz_exclusions (or record a source-backed reason why the 恩 precedent does not apply to 徳), then revalidate and rebuild the manifest.

## Optional points
### O1: Consider 徳/偉 and 徳/厚
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: evidence/kanjidic2-records.xml:56-59; repo/kanji/偉.md:20-21; repo/kanji/厚.md:20; snapshot/kanji/徳.md:14
- Evidence: KANJIDIC2 glosses 徳 "commanding respect", the basis for the declared 尊/敬 exclusions; 偉 "admirable; great" praises conduct and is arguably closer to that sense than the respecting actions of 尊/敬. 厚's cordial/kindness sense (厚意) partly overlaps "benevolence". The supplied evidence does not settle whether learners would treat these as defensible answers.
- Suggestion: Decide on and record a disposition for 徳/偉 and 徳/厚; excluding 偉 would be the more consistent with the 尊/敬 rationale.

### O2: Precautionary wealth exclusion is not applied evenly
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: medium
- Citations: evidence/external-snapshots/01-extract.txt:25-26; snapshot/kanji/徳.md:14; repo/kanji/財.md:3; repo/kanji/富.md:3
- Evidence: The wealth sense of 徳 is supported only by a classical Genji quotation, yet 富 "wealth; abundance" is excluded while 財 "wealth; property" is not.
- Suggestion: Either note in the card that the 富 exclusion is precautionary for a classical sense, or apply it evenly to 財.

### O3: Curated distractors are weak shape contrasts
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/徳.md:13; snapshot/kanji/徳.md:47; rubric/content-structure.instructions.md:97-99; evidence/title-index.txt:345-357
- Evidence: 休/本/木 are N5 starter cards and the card concedes they are "loose contrasts, not the closest shapes", while the rubric asks for easily confused kanji. The index contains several 彳 cards (for example 待, 律, 徒, 復, 徹) that are semantically distinct from 徳. The current options are meaning-safe and share no reading with トク (checks/quiz-safety.txt).
- Suggestion: Consider closer-shaped, semantically distinct 彳 distractors such as 徹 or 復, after checking their meanings and readings.

## Limits
- L1: The raw stroke SVGs, raw Weblio HTML response, binary Joyo PDF and every packet asset outside the two chains were not opened; the stroke JSON was checked only for count, revision and consistency with the card, with no visual geometry claim.
- L2: repo/docs/content-format.md was read only for lines 1-139.
- L3: Only one external snapshot (Weblio 徳) was supplied. No independent source was available for learner perception of 偉/厚 overlap (O1), so that question remains unresolved.
- L4: Automated checks (lint, quiz-safety, reading-exposure, validate, manifest, budget) are host/static evidence. They do not establish native/phone acceptance, Kotlin behavior, custom or multi-borrow Starter pools, or compatibility with installed APK 5c000bd, which predates quiz_exclusions.
- L5: Identified but unrequested candidates, judged low risk and unread: 好 (favorable), 寧 (polite), 清/純 (pure), 栄 (glory), 英 (outstanding), 情 (emotion), 儀 (formal conduct), 康 (well-being), 効 (efficacy), 賞 (reward). No 善, 仁, 恵, 慈 or 益 card exists in the title index.
- L6: The runtime identifies the execution model as Claude Opus 5.5, but this was not independently verified.
- L7: Source line numbers for extension cards were derived from each chain's printed segment-to-source line mapping; broad JMdict ranges are cited where exact entry lines were not individually counted.
