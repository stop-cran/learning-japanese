## Snapshot
The frozen commit is **76fedcbf56ba9efaf1ccc6e6c9ca60e478ca22db** (parent fc77da2dede8066a36e614156994fcd93362dfb7). I reviewed committed content only. My file tools can't run Git, so I did not check the snapshot hashes or the clean-tree status myself; I relied on the author's frozen-snapshot.json.

## Scope
- **Model:** claude-opus-5.5 (Claude family). No agents and no edits.
- **Rules read:**
  - `.github\copilot-instructions.md`
  - `.github\instructions\content-structure.instructions.md`
  - `docs\content-format.md:18-103`
- **Articles read in full:** all 19 assigned articles.
- **Kanji edits:** I read `related.patch` and the complete `kanji\農.md`, `巻.md`, `村.md` and `濃.md`.
- **Source data:** the TSV header and rows 1282-1301, matched by exact ID only.
- **Private files read:**
  - frozen-snapshot.json and related.patch
  - review-mappings/principals/labels/components.jsonl
  - public-bodies.txt lines 1-130 and 160-345 only
- **Existing words articles:** I read `ぬれる.md` and `嫁.md` in full. For about 60 others I read only the title and quiz_exclusions lines.
- **Outside source:** Kotobank, which gave 精選版日本国語大辞典 for 濃度, 女房 and 俄. This is a second authority besides Daijisen.
- **Not read:**
  - review-evidence.json and public-bodies.json
  - family-inspection-01..08 and old-body-inspection-01..10
  - all supplement-family and supplement-old-body files
  - confusable-words.md, jlpt-levels.md and both snapshot JSON files in docs

## Verdicts
Cells are Correctness / Coverage / Comprehensibility.

| Row | Article | Correctness | Coverage | Comprehensibility |
|---|---|---|---|---|
| N2:1282 女房 | words\女房.md | NEEDS FIX (B65-02) | NEEDS FIX (B65-03) | CLEAN |
| N2:1283 睨む | words\睨む.md | CLEAN | CLEAN | CLEAN |
| N2:1284 煮る | words\煮る.md | CLEAN | CLEAN | CLEAN |
| N2:1285 俄 | words\俄.md | NEEDS FIX (B65-04) | CLEAN | CLEAN |
| N2:1286 縫う | words\縫う.md | CLEAN | CLEAN | CLEAN |
| N2:1287 濡らす | words\濡らす.md | NEEDS FIX (B65-01) | CLEAN | CLEAN |
| N2:1288 ねじ | words\ねじ.md | NEEDS FIX (B65-05) | CLEAN | CLEAN |
| N2:1289 捩る | words\捩る.md | CLEAN | CLEAN | CLEAN |
| N2:1290 ネックレス | words\ネックレス.md | CLEAN | CLEAN | CLEAN |
| N2:1291 熱する | words\熱する.md | CLEAN | CLEAN | CLEAN |
| N2:1292 寝間着 | words\寝間着.md | CLEAN | CLEAN | CLEAN |
| N2:1293 寝巻 | words\寝間着.md | CLEAN | CLEAN | CLEAN |
| N2:1294 狙い | words\狙い.md | CLEAN | CLEAN | CLEAN |
| N2:1295 狙う | words\狙う.md | CLEAN | CLEAN | CLEAN |
| N2:1296 年度 | words\年度.md | CLEAN | CLEAN | CLEAN |
| N2:1297 農産物 | words\農産物.md | CLEAN | CLEAN | CLEAN |
| N2:1298 農村 | words\農村.md | CLEAN | CLEAN | CLEAN |
| N2:1299 濃度 | words\濃度.md | CLEAN | CLEAN | CLEAN |
| N2:1300 農薬 | words\農薬.md | CLEAN | CLEAN | CLEAN |
| N2:1301 能率 | words\能率.md | CLEAN | CLEAN | CLEAN |

**Row notes:**
- **ねじ and ネックレス:** both have `kanji: []`, which matches their empty raw kanji fields.
- **寝巻 (N2:1293):** the shared 寝間着 article meets the source-alias policy. It teaches the spelling (line 16), gives a 寝巻き example (22), links 巻 (35) and adds a note (51).
- **濃度's "brightness" gloss:** neither JMdict 1469970 nor Daijisen supports it. 日国 sense ② "色の深さ。物体が光を吸収する程度" (depth of colour; how much light an object absorbs) is the closest attested meaning, and it means darkness rather than brightness. So the article's denial at line 47 is correct.
- **Primary-kanji links:** every existing primary kanji is linked from the word side. Kanji without cards (房, 睨, 煮, 俄, 縫, 濡, 捩, 狙, 率) are not invented.

**Kanji edits, baseline and mappings:**
- **農: CLEAN.** The ノウ reading row (line 30) and Common words (37-39) add 農産物/農村/農薬. The footer (46) adds 1470710, 1470730 and 1470780.
- **村: CLEAN.** The ソン row (28) and Common words (35) add 農村 のうそん. The footer (43) adds 1470730.
- **濃: CLEAN.** The ノウ row (30) and Common words (36) add 濃度. The footer (43) already had 1469970.
- **巻: CLEAN.** 寝巻 is in the まき row (31) and 寝巻き in the ま.き row (32), both linking to 寝間着.md. Common words (39), a note (44) and footer entry 1360040 (48) are added. The reverse 巻 link is at 寝間着.md:35.
- **Baseline preservation: CLEAN.** Headers and front matter on all four cards are kept.
- **Mappings: CLEAN.** All 20 mappings have the correct article, entry and senses, and these match the article footers.

## Findings
- **B65-01**
  - **Severity and facet:** Minor; quiz exclusions.
  - **Location:** words\濡らす.md:9.
  - **Problem:** ぬれる (title "get wet") is not excluded. 濡らす's own example (23-24) translates as "Please do not get the book wet", so both answers can look right.
  - **Fix:** add ぬれる to 濡らす's quiz_exclusions.
  - **Evidence:**
    - ぬれる.md has the title "get wet" and no exclusions.
    - 濡らす.md:32-35 pairs the two verbs itself.
    - content-format.md uses the 開く/開ける pair as its example of a pair that needs a guard.
    - 湿る.md:9 already excludes ぬれる.
  - **Confidence:** High.
- **B65-02**
  - **Severity and facet:** Minor; quiz exclusions.
  - **Location:** words\女房.md:9.
  - **Problem:** 嫁 is not excluded. 女房's title "wife" is identical to 妻's, and 嫁 already guards against 妻 because it teaches a "wife" use. Guards are not transitive, so 嫁 can still appear as a wrong choice for the "wife" prompt.
  - **Fix:** add 嫁 to 女房's quiz_exclusions.
  - **Evidence:** 嫁.md:9 has `quiz_exclusions: [妻]`; 嫁.md:39-42 teaches the "wife" use.
  - **Confidence:** Medium-high.
- **B65-03**
  - **Severity and facet:** Minor; register and coverage.
  - **Location:** words\女房.md:16, 25 and 35-38.
  - **Problem:** The article doesn't say that 女房 is usually a husband talking about his own wife, or that it has a somewhat self-deprecating tone. It also doesn't explain how it differs from 妻, the neutral word.
  - **Fix:** add 1-2 sentences covering the typical speaker, the humbling tone and 妻 as the neutral choice.
  - **Evidence:**
    - Daijisen (public-bodies.txt:33): "多く、夫が自分の妻をさしていう" (mostly a husband referring to his own wife).
    - 日国 ③: "現代では、多少とも卑しめた気持をもっていい、自分の妻のことをいう場合に多く用いられる" (in modern use, said with a somewhat belittling feeling, mostly of one's own wife).
    - This contradicts the TSV note's claim that a register label would be unsupported.
  - **Confidence:** Medium-high.
- **B65-04**
  - **Severity and facet:** Minor; how にわか attaches to a following word.
  - **Location:** words\俄.md:19 and 23-27.
  - **Problem:** "Use にわかな before a noun" leaves out にわかの, which JMdict records (sense 1 is adj-na and adj-no). The only example of にわか before a noun, にわかな思いつき, has unverified naturalness.
  - **Fix:** mention both な and の, and replace or verify the example.
  - **Evidence:**
    - JMdict principal record 1599920, sense 1.
    - 日国 cites 「俄の道心」, a historical example.
  - **Confidence:** Medium.
- **B65-05**
  - **Severity and facet:** Minor; a claim about which spelling is usual.
  - **Location:** words\ねじ.md:29.
  - **Problem:** Calling ねじ "the usual kana spelling" is not supported by the sources.
  - **Fix:** use wording such as "hiragana ねじ; katakana ネジ is also common".
  - **Evidence:** JMdict 1585010 lists ネジ first, with priority tag spec1; ねじ has ichi2.
  - **Confidence:** Medium.

## Optional
- **濃度:** add a short note on colour or print density, citing 日国 ②. On the 濃 card, consider restoring "density" to the gloss.
- **村.md:40:** the note mentions only 村長, but the ソン row now also has 農村.
- **ねじ.md:30:** add 捩子 to the list of rare spellings and link it to 捩る.
- **寝間着:** note how ね+ま+き maps onto 寝/間/着.
- **俄:** add にわか雨.
- **Unlinked existing articles:**
  - 冷ます (熱する.md:44)
  - 湿る (濡らす.md:42)
  - 編む (縫う.md:39)
  - 薄める (濃度.md:42)
  - 諦める (狙う.md:44)
  - 準備 (俄.md:43)
- **Exclusions that do no harm:**
  - 熱する: 熱い
  - 俄: すっと and さっさと
  - 縫う: 針 and 抜ける
  - 煮る: 作る and こしらえる
  - 狙う: 考える and 望む
- **煮る:** add a 茹でる contrast.
- **女房:** mention the にょうぼ variant.

## Limits
- I couldn't run Git, and the snapshot hashes are the author's own.
- The family and old-body inspection files are unread. Apart from ぬれる and 嫁, I judged older articles' quiz pairs from titles only.
- Possible quiz pairs I did not establish as needing guards:
  - 狙う–睨む
  - 熱する–熱 and 熱する–騒ぐ
  - 年度–学期
  - 狙う–目標 and 狙う–対象
  - 能率–効果, 能率–きびきび and 能率–さくさく
  - 煮る–ぐつぐつ and 煮る–ことこと
  - 女房–主婦
- No native speaker checked whether the examples sound natural.
- The Weblio captures are all one dictionary (Daijisen). The only other authority I used is Kotobank.
