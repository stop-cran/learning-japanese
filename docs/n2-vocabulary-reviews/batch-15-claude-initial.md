## Snapshot
**Commit:** `88300af9b018b8735962595c837167bcad9e03bf` (parent `e85977a13ce629196d3e2b922e376a26056a3473`), taken from the frozen receipt. I meant to review committed content only. I had file tools but could not run Git, so I couldn't confirm that the files on disk or the related patch match this commit, and I didn't recompute the receipt hashes.

## Scope
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`, claude family). Sequential, read-only, no delegation.
- **New articles:** I read all twenty completely.
- **Related edits:** I read the fifteen-file patch completely. I read the 固, 個, 片 and 傾 kanji cards in full and the other changed passages in context. I did not review unchanged teaching.
- **Mappings:** I checked N2:282–301 against the batch-15 rows, the principal JMdict entries, spelling and reading restrictions, and the selected senses. I spot-checked comparison entries rather than reading all 181.
- **Other evidence:**
  - Kotobank pages fetched: 片寄る (Nihon Kokugo Daijiten), 偏る (Digital Daijisen), 課税 and 固まり.
  - I compared English titles and exclusions across `words\`.
- **Not read:** none of the forbidden reports, notes, ledgers or receipts. Searches stayed inside the allowed paths.

## Verdicts
| Row | Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| N2:282 | 貸し出し | CLEAN | CLEAN | CLEAN |
| N2:283 | 過失 | CLEAN | CLEAN | CLEAN |
| N2:284 | 果実 | CLEAN | CLEAN | CLEAN |
| N2:285 | 貸間 | CLEAN | CLEAN | CLEAN |
| N2:286 | 貸家 | NEEDS FIX (B15-06) | CLEAN | NEEDS FIX (B15-01) |
| N2:287 | 個所 | NEEDS FIX (B15-04) | CLEAN | CLEAN |
| N2:288 | 過剰 | CLEAN | CLEAN | CLEAN |
| N2:289 | かじる | CLEAN | CLEAN | CLEAN |
| N2:290 | 課税 | CLEAN | CLEAN | CLEAN |
| N2:291 | 下線 | CLEAN | CLEAN | CLEAN |
| N2:292 | カセット | CLEAN | CLEAN | CLEAN |
| N2:293 | 加速 | CLEAN | CLEAN | CLEAN |
| N2:294 | 加速度 | CLEAN | CLEAN | CLEAN |
| N2:295 | 片仮名 | CLEAN | CLEAN | NEEDS FIX (B15-03) |
| N2:296 | 片付く | NEEDS FIX (B15-05) | CLEAN | CLEAN |
| N2:297 | 塊 | CLEAN | CLEAN | CLEAN |
| N2:298 | 固まる | CLEAN | CLEAN | CLEAN |
| N2:299 | 片道 | CLEAN | CLEAN | CLEAN |
| N2:300 | 傾く | CLEAN | CLEAN | CLEAN |
| N2:301 | 片寄る | CLEAN | NEEDS FIX (B15-02) | CLEAN |

**Related changes (15 files): CLEAN / CLEAN / CLEAN.**
- **Kanji cards:**
  - 個, 課, 税, 線, 片, 固 and 傾 now link the new words at the readings those words actually use. The 片 card's metadata also lists the new words' dictionary entry IDs.
  - The 固 card's 固まり → 塊 link is labelled as another spelling of 塊, and 塊 teaches that spelling.
  - The obsolete かたぶく reading on 傾 is correctly left unlinked.
- **Word articles:** the edits to 貸す, 片付ける, 噛む, 食べる, 往復, テープ, ラジオカセット and ラジカセ only add links on words they already mention, and every target teaches the linked spelling.

**Mappings N2:282–301: CLEAN / CLEAN / CLEAN, with qualifications.**
- Every row matches its source entry and selected senses.
- Spelling restrictions are respected: かしいえ applies only to 貸家/貸し家, and the noun sense of 個所 applies only to 箇所/個所.
- Spellings that dictionaries mark as search-only are not taught as normal alternatives (噛じる, 塊り, 片かな).
- 果実 sense 2 and 片付く sense 4 are explicitly left out of the lesson.
- The coverage note for 片寄る is B15-02.

## Findings
**B15-01 — Minor — comprehensibility — `words\貸家.md:21,25,33`**
- **Claim:** Line 21 correctly says かしいえ is an alternative reading for 貸家/貸し家. Line 25 then says "This is not カ + カ or the reading いえ of the standalone house word." Line 33 says "Keep the learner's main reading かしや separate from the independently recorded かしいえ spelling restrictions," which is dictionary jargon a learner can't parse.
- **Impact:** a learner gets contradictory guidance on whether 家 can be read いえ here.
- **Remedy:** at line 25, say that in the main reading かしや, 家 is read や; the less common かしいえ uses いえ. Replace line 33 with plain wording.
- **Evidence:** JMdict 1411170 in batch-15.json: かしや has no restriction; かしいえ is restricted to 貸家 and 貸し家.
- **Confidence:** high.

**B15-02 — Minor — scoped coverage — `words\片寄る.md:16,20,26,34`**
- **Claim:** the article only calls 偏る "another spelling" and tells learners to "learn the source spelling 片寄る". Its biased-view example uses 片寄った見方. It never says 偏る is the more common written form, especially for bias or imbalance.
- **Impact:** a learner may treat 片寄る as the default and under-learn the spelling they will meet most in writing (偏った考え方, 栄養が偏る).
- **Remedy:** add one sentence saying 偏る is the more frequent written form, especially for bias or imbalance, and that 片寄る also occurs. Present this as a tendency, not a rule. Consider using 偏った見方 in the third example.
- **Evidence:**
  - JMdict 1590420 lists 偏る first, with three frequency/priority markers (ichi1, news2, nf34); 片寄る has only ichi1.
  - Digital Daijisen's headword is 【偏る／片寄る】, with the examples 「―った考え方」, 「栄養が―る」 and 「―った税制」 (fetched).
- **Confidence:** medium. Frequency is inferred from dictionary priority tags and headword order, not corpus counts.

**B15-03 — Minor — comprehensibility — `words\片仮名.md:15,32`**
- **Claim:** "It is also usually written in kana" is confusing because of "also". Line 32's "does not require reading the kanji spelling aloud as a separate katakana-only pronunciation" exposes how the dictionary stores readings to the learner.
- **Impact:** a learner may wonder whether 片仮名 and カタカナ are pronounced differently.
- **Remedy:** state that the word is usually written カタカナ, that 片仮名 is the kanji spelling, and that both are pronounced かたかな.
- **Evidence:** JMdict 1511600 marks the word "usually kana", and its カタカナ reading has no kanji spelling.
- **Confidence:** medium-high.

**B15-04 — Minor — correctness (quiz) — `words\個所.md:4,9` ↔ `words\位置.md:4,9`**
- **Claim:** 個所 is titled "place; point; counted location" and 位置 is "position; location", but neither excludes the other. In a multiple-choice quiz, either title could be defended as correct for the other word.
- **Impact:** a quiz question could have two defensible answers.
- **Remedy:** add 位置 to the 個所 `quiz_exclusions`. One side is enough because exclusions apply both ways.
- **Evidence:** 位置.md already excludes 場所 "place, location" because of the same overlap. 位置 is not among the batch's comparison entries.
- **Confidence:** medium.

**B15-05 — Minor — correctness (quiz) — `words\片付く.md:4,9,20` ↔ `words\落ち着く.md:4,9,23`**
- **Claim:** 片付く is titled "be tidied; be settled" and teaches "問題が片付きました – was settled". 落ち着く is titled "calm down; settle" and teaches that an arrangement becomes settled. Neither excludes the other.
- **Impact:** in a quiz, either title could look correct for the other word.
- **Remedy:** add 落ち着く to the 片付く exclusions.
- **Evidence:** 落ち着く already excludes 決まる ("be decided; be settled") on this same "settled" overlap, and 片付く also excludes 決まる.
- **Confidence:** medium.

**B15-06 — Minor — correctness (quiz) — `words\貸家.md:4,9` ↔ `words\家屋.md:4,9`**
- **Claim:** 貸家 "house for rent" excludes only 家. 家屋 "house; building" is equally defensible as a broader correct answer, since a house for rent is a house.
- **Impact:** a quiz question could have two defensible answers.
- **Remedy:** add 家屋 to the 貸家 exclusions, and consider 住宅 "housing; residence".
- **Evidence:** the author already excluded 家 for this reason, and 家屋.md excludes 家, 宅, 住宅 and アパート.
- **Confidence:** medium.

## Optional
- **個所:** could note that dictionaries list 箇所 first and that it is common in general text.
- **塊.md:19:** 人が塊になって is supported by Nihon Kokugo Daijiten sense ② (一団), but ひとかたまりになって may be more idiomatic.
- **傾く.md:21:** 賛成に傾きました would be tighter. The English adds "the proposal", which isn't in the Japanese.
- **片寄る.md:18:** 片方に片寄って is redundant.
- **Wording that reads like reviewer or dictionary notes:** 課税.md:33 ("not an invented rule…") and 片寄る.md:26 ("cited entry does not impose…") could be rephrased as positive teaching.
- **Weak quiz overlaps (no change needed):** 固まる vs 固い/堅い, 傾く vs 坂, and 過失 vs 悪い "at fault" differ in part of speech.

## Limits
- **No Git:** commit identity, file hashes and the patch's fidelity to the commit are unverified.
- **Example naturalness:** judged against dictionary entries and my own knowledge. There was no corpus or native-speaker check.
- **Comparison and component evidence:** the 181 comparison entries were spot-checked, not read exhaustively. The kanji component evidence was partly read, and its KANJIDIC hashes were not recomputed.
- **Citations:** the Kotobank citations for 片仮名, 傾く and 片付く were not refetched. The author's lookup records were treated as claims to assess, not evidence; the 箇所 lookup only checked the headword.
- **Quiz behaviour:** taken from the content-format docs. I didn't run the app or tests.
- **Title-overlap scan:** keyword-based, so overlaps between differently worded titles could be missed.
