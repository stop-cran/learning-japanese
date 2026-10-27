## Snapshot
- **Corrected commit:** `d3d03f731f67767185c435ba7bcad0087b74bc5c` (from `batch-65-correction-snapshot.json`, read first).
- **Parent:** `76fedcbf56ba9efaf1ccc6e6c9ca60e478ca22db`.
- **Basis:** committed content only. File tools cannot run Git, hash or cleanliness checks, and I did not inspect `.git`. The snapshot's `cleanCommittedContent: true`, its hashes and the coverage-index update were all produced by the author; I did not verify them myself.

## Scope
- **Model:** claude-opus-5.5, family claude. Read-only; no edits, agents or delegation.
- **Read fresh in this phase:**
  - `batch-65-correction-snapshot.json`
  - the complete `batch-65-correction.patch` (nine `words\` files, TSV row 1282, snapshot JSON hash)
  - all nine changed bodies in full: 女房, 睨む, 熱する, 濡らす, 俄, ねじ, 縫う, 濃度, 狙う. I reread 女房, 俄 and 濡らす a second time; all nine match the patch.
  - `batch-65-correction-families-01.txt`, complete: 12 families / 31 senses (1345420, 1569880, 1350600, 1467730, 1599920, 1585010, 1467610, 1467620, 1191680, 1281170, 1586430, 1599930)
  - `batch-65-correction-old-bodies-01.txt`, complete: 嫁, 考慮, 暖まる, 焼く, ぬれる
  - `batch-65-correction-public.json`: two receipts, both pointing to my own initial-session Kotobank returns for 女房 and 俄, not new fetches by the author
  - the TSV header (line 1) and exactly N2:1282–1301, found by exact-ID grep; I did not read 1302
  - `docs\content-format.md:18-103`
- **Checks in this phase:**
  - All 15 link and guard targets exist (glob).
  - Title, `quiz_exclusions` and `quiz_distractors` lines for those 15 files.
  - A scan of all of `words\` found no `quiz_distractors` entry that collides with a new exclusion in either direction.
  - Grep spot-checks of the reciprocal links in 農, 村, 濃 and 巻.
  - One-line `sourceNote` snippets from `corrected-review-evidence.json`.
- **Not read:**
  - The `correctionEvidence` block of `corrected-review-evidence.json`. It contains `initialNativeReports`, which may hold the other reviewer's output. I checked the revised lists and note directly in the articles, patch and TSV instead.
  - I did not reread `frozen-snapshot.json`, `related.patch` or the `.github` instructions in this phase; those judgments are inherited.
  - No new web fetches.
- **Inherited from my initial full reads (bodies unchanged per the patch):**
  - ten new articles: 煮る, 捩る, ネックレス, 寝間着, 狙い, 年度, 農産物, 農村, 農薬, 能率
  - four kanji cards: 農, 巻, 村, 濃
  - mappings and principals
  - Kotobank returns: 女房 page 110666 (日国 ③, "多少とも卑しめた気持"), 俄 page 110746, 濃度
- **Initial read-depth limit:** in the first session I did not read the 23 bounded family/older-body chunks. Only 嫁 and ぬれる were read as complete older bodies; my roughly 60 other scans were titles and exclusions only. This phase adds complete 考慮, 暖まる and 焼く.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1282 女房 | words\女房.md | Fresh full reread + patch + 1345420 + 嫁 body + inherited 日国 ③ | CLEAN | CLEAN | CLEAN |
| N2:1283 睨む | words\睨む.md | Fresh full reread + 1569880 + 考慮 body | CLEAN | CLEAN | CLEAN |
| N2:1284 煮る | words\煮る.md | Inherited initial full read (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1285 俄 | words\俄.md | Fresh full reread + 1599920 + 1599930 + inherited Kotobank | CLEAN | CLEAN | CLEAN |
| N2:1286 縫う | words\縫う.md | Fresh full reread | CLEAN | CLEAN | CLEAN |
| N2:1287 濡らす | words\濡らす.md | Fresh full reread + 1467610 + 1467620 + ぬれる body | CLEAN | CLEAN | CLEAN |
| N2:1288 ねじ | words\ねじ.md | Fresh full reread + 1585010 | CLEAN | CLEAN | CLEAN |
| N2:1289 捩る | words\捩る.md | Inherited initial full read (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1290 ネックレス | words\ネックレス.md | Inherited initial full read (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1291 熱する | words\熱する.md | Fresh full reread + 1467730 + 1350600 + 1586430 + 焼く/暖まる bodies | CLEAN | CLEAN | CLEAN |
| N2:1292 寝間着 | words\寝間着.md | Inherited initial full read (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1293 寝巻 | words\寝間着.md | Inherited initial full read (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1294 狙い | words\狙い.md | Inherited initial full read (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1295 狙う | words\狙う.md | Fresh full reread | CLEAN | CLEAN | CLEAN |
| N2:1296 年度 | words\年度.md | Inherited initial full read (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1297 農産物 | words\農産物.md | Inherited initial full read (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1298 農村 | words\農村.md | Inherited initial full read (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1299 濃度 | words\濃度.md | Fresh full reread + inherited Kotobank 濃度 | CLEAN | CLEAN | CLEAN |
| N2:1300 農薬 | words\農薬.md | Inherited initial full read (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1301 能率 | words\能率.md | Inherited initial full read (unchanged) | CLEAN | CLEAN | CLEAN |

- **Five primary reciprocal pairs: CLEAN.** Inherited, and the links were spot-checked again by grep this phase.
  - 農/農産物 のうさんぶつ, 農/農村 のうそん and 農/農薬 のうやく: `kanji\農.md:30, 37-39`; footer IDs 1470710, 1470730 and 1470780 at :46.
  - 村/農村 のうそん: `kanji\村.md:28, 35`; footer 1470730 at :43.
  - 濃/濃度 のうど: `kanji\濃.md:30, 36`; footer 1469970 at :43.
  - The word-side links are inherited from my initial reads.
- **巻 alias: CLEAN.**
  - 寝巻 and 寝巻き are both read ねまき, and both link to `words\寝間着.md` (`kanji\巻.md:31-32, 39, 44`); footer 1360040 at :48.
  - 寝間着 links back to 巻 (inherited).
  - Primary metadata stays 寝/間/着, without 巻. No missing character card is fabricated.
- **Related kanji 農/巻/村/濃: CLEAN.** Unchanged by the correction, and the existing headers are preserved.
- **Baseline preservation: CLEAN within scope.** The patch touches only the nine new articles, TSV row 1282 and the snapshot hash. No other word or kanji files change, and no title, reading, level or primary-kanji field changes. Git and hash proof was produced by the author, not me.
- **Mappings: CLEAN.**
  - All twenty associations, selected senses and additional senses match my initial judgments.
  - Only the row 1282 `source_note` changed. The original note is kept as the evidence file's `sourceNote` (line 28).
  - The raw kanji fields for ねじ and ネックレス are still empty.
  - The raw "brightness" gloss is preserved as provenance but not taught.

## Findings
**My original findings**
- **B65-01 (濡らす/ぬれる): RESOLVED.** Confidence lowered from high to medium.
  - `words\濡らす.md:9` adds ぬれる.
  - Lines 30-33 and 47-50 still teach make-wet versus get-wet (タオルを濡らした / タオルがぬれた), so no meaning is lost.
  - I accept that my "get the book wet" translation and the 湿る or 開く/開ける analogies do not by themselves prove the pair. I assert no universal causative/inchoative rule.
  - The guard rests on two things: the titles "make wet; moisten" and "get wet" share the lexeme "wet", and ぬれる's own body says English "wet" can be transitive. Under `content-format.md:95` (a learner could reasonably accept either title), I find the guard defensible and conservative. I would not dispute treating it as borderline or optional.
  - The 湿る link at :41 is accurate.
- **B65-02 (女房/嫁): RESOLVED.**
  - :9 now reads `[家内, 奥さん, 夫人, 嫁]`.
  - The guard is supported by 1191680:3 "wife (Kansai-ben)" and by 嫁's body, which teaches the "wife" use.
  - Removing 妻 is correct: both titles are exactly "wife", so they need no guard (`content-format.md:96`). 妻.md has no exclusions, so behavior does not change.
  - This is not a transitive extension through 妻 (:87).
- **B65-03 (女房 register): RESOLVED.**
  - :16 says "especially a husband referring to his own wife".
  - :45-46 say "can carry a somewhat disparaging tone; its effect depends on the speaker and context", with no claim that every use is insulting.
  - :35 calls 妻 the "safer starting choice".
  - The :53-54 footer correctly points to page 110666, sense 3. The earlier 111396 URL (a neutron-reactor page) does not appear anywhere.
  - This matches 日国 ③ "多少とも卑しめた気持" and Daijisen "多く、夫が自分の妻をさしていう". It does not overclaim a humble or self-deprecating category.
- **B65-04 (俄 attachment): RESOLVED.**
  - :19-20 record にわかに, にわかな/にわかの and direct compounds; :29 warns they are not freely interchangeable.
  - These match 1599920:1 (adj-na/adj-no) and :2 (prefix/adj-na).
  - The unverified にわかな思いつき example is gone. The new にわか雨が降り出しました / "A sudden shower started." is natural and supported by 1599930.
  - The :58 compound footer and the :45 準備 link are fine.
- **B65-05 (ねじ spelling): RESOLVED.**
  - :29 now reads "This article uses hiragana ねじ; katakana ネジ is also recorded", with no frequency claim.
  - I withdraw my earlier "also common" suggestion: entry order and priority tags do not prove frequency.

**Author adjudications not raised in my report**
- **G65-02 (睨む/考慮): SUPPORTED.** 1569880:5 "to take into consideration" overlaps directly with 考慮's title "consideration; taking into account". The :52 link is substantive, and no neighboring exclusions were copied from 考慮.
- **G65-03 (熱する/焼く and 熱する/暖まる): SUPPORTED, with one caveat.**
  - 1350600:3 "to heat; to heat up" and 1586430 "warm up; get warm" support the two guards, which are consistent with the existing 暖める guard.
  - Caveat: the existing 焼く body (title "bake; grill") does not teach the heating sense. The guard therefore rests on the dictionary record, not on what 焼く's own article teaches. This is not a defect.
  - The 冷ます link (:43) is fine.

**Regressions and new defects**
- **Six new links** (冷ます, 湿る, 編む, 薄める, 諦める, 準備): all six targets exist, and none expands a comparison word's meaning.
- **Regression check: none found.**
  - Front matter shape is intact, and no new exclusion collides with a `quiz_distractors` entry in either direction.
  - Titles, readings, levels and kanji arrays are unchanged.
  - The row 1282 note accurately scopes the claim.
- **New actionable defects:** none.

## Optional
- **女房:** "In modern wife-use" (:45) could read more smoothly as "When it means 'wife' today".
- **濃度:** an optical-density / colour-depth recognition note (日国 ②), kept clear of "brightness". The other reviewer raised this too, and the :47 denial of "brightness" is correct.
- **ねじ:** list 捩子 as a rare form.
- **村.md:40:** the note wording could be tightened.
- **寝間着:** a ね + ま + き morpheme mapping.
- **煮る:** a 茹でる contrast.
- **女房:** mention the にょうぼ variant.
- **焼く.md:** its body could eventually teach the heating sense.
- **Unverified exclusion lists:** the broad lists (俄 15 items; 狙う 考える/望む; 縫う 抜ける/通る) are not certified globally safe.
- **Unproven borderline pairs:** 狙う–睨む, 年度–学期 and 女房–主婦 are not established in either direction.
- None of these is a defect.

## Limits
- Git, hash, cleanliness and manifest checks were all run by the author, not me.
- All twenty public captures come from one authority (Daijisen via Weblio). The 日国 女房 ③ and 俄 evidence comes from my own initial-session Kotobank returns. Neither counts as independent multi-dictionary confirmation.
- I did not read the `correctionEvidence` / `initialNativeReports` block.
- The ten unchanged articles and four kanji cards are judged on inherited initial reads, not fresh rereads in this phase.
- My older-body coverage is narrower than GPT's: I read complete bodies only for 嫁, ぬれる, 考慮, 暖まる and 焼く, and none of the 23 original chunks.
- There were no live quiz draws, native-speaker certification, measured frequency or exhaustive synonym audit.
- The B65-01 guard is a judgment call under `content-format.md:95`, not a proven substitution.
- The deferred batch-61 debt (飛ぶ/飛行, 止まる/止む) is outside this scope.
