## Snapshot
`d04bcfce3419f3bea7158281ff32ba65f32ffdad` (parent `7b18d016f6228355b174ee61f992abb29c706342`). This review covers committed content only. I could use file tools but could not run Git. I read the files on disk and could not confirm that they are byte-identical to the commit or check any recorded hashes. The receipt states `cleanCommittedContent: true`.

## Scope
- **Model:** claude-opus-5.5 (Claude family).
- **New articles:** I read all 18 in full.
- **Reused articles:** 上下 and 商店 got a narrow check only: their claimed じょうげ and shop coverage, plus the added `jlpt: 2`. This was not a whole-article review.
- **Kanji:** I read all six edited cards (極, 賞, 毒, 蒸, 署, 防) in full, along with the 8-file related patch.
- **Mappings:** I checked TSV rows N2:762–781 against all 20 complete families in the principal reading file.
- **Comparison words:** I read titles and exclusions for linked and excluded words, and searched words\ for English-label overlaps. I read 起す, 生じる, 戸, 始まり, 無くなる and 原因 in full.
- **Public captures:** I inspected entries for 生ずる, 小数, 焦点, 小便, 消防署, 正味, 正面, 生じる, 分数, 少数, 滅菌, 尿 and 正面切って. I did not open the entries for the other 13 headwords.
- **MHLW:** I read the capture and fetched the page myself.
- **Own fetches:** Kotobank 焦点 (Nikkoku, Nipponica, Sekai Daihyakka). The Weblio 焦点 page did not render its text, and the first Kotobank lookup returned an unrelated word. I treat both as limits, not evidence.
- **Not read:** most of the review-evidence JSON (component evidence and the receipt sections), the author comparison files, n2-vocabulary-snapshot.json and n2-source-snapshot.json.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 消極的 | CLEAN | CLEAN | CLEAN |
| 賞金 | CLEAN | CLEAN | CLEAN |
| 障子 | NEEDS FIX (C-01) | CLEAN | CLEAN |
| 商社 | CLEAN | CLEAN | CLEAN |
| 乗車 | CLEAN | CLEAN | CLEAN |
| 上旬 | NEEDS FIX (C-02) | CLEAN | CLEAN |
| 生ずる | NEEDS FIX (C-04) | CLEAN | NEEDS FIX (C-06) |
| 小数 | CLEAN | CLEAN | CLEAN |
| 焦点 | NEEDS FIX (C-05) | CLEAN | CLEAN |
| 消毒 | CLEAN | CLEAN | CLEAN |
| 勝敗 | CLEAN | CLEAN | CLEAN |
| 蒸発 | NEEDS FIX (C-03) | CLEAN | CLEAN |
| 賞品 | CLEAN | CLEAN | CLEAN |
| 勝負 | CLEAN | CLEAN | CLEAN |
| 小便 | CLEAN | CLEAN | CLEAN |
| 消防署 | CLEAN | CLEAN | CLEAN |
| 正味 | CLEAN | CLEAN | CLEAN |
| 正面 | CLEAN | CLEAN | CLEAN |

- **Six kanji edits:** CLEAN on all three facets. The seven primary pairs are 極 キョク/消極的, 賞 ショウ/賞金 and 賞品, 毒 ドク/消毒, 蒸 ジョウ/蒸発, 署 ショ/消防署, and 防 ボウ/消防署. Each sits at the correct reading in both the reading table and Common words, and existing metadata is untouched.
- **Two narrow reuses:** CLEAN within the narrow check. The only change to each is `jlpt: 2`.
  - 上下 covers selected senses 1–2, plus 上下関係 (sense 4) and 上下セット (sense 6).
  - 商店 covers sense 1, shop.
- **Twenty mappings:** CLEAN on all three facets. The entry IDs and selected senses match the families.
  - 正面: the raw gloss "honesty" is not in the pinned family, and the article explicitly declines to teach it.
  - 小数 and 小便: their additional senses are labelled as additional.

## Findings
- **B39-C-01 · Minor · Correctness (quiz) · words\障子.md:9 (also :29)**
  - **Claim:** The card excludes ドア ("door") but not 戸 ("door; especially a traditional door"). A shoji is a traditional sliding door, so a learner could reasonably accept 戸's title for 障子. 戸.md:28 itself contrasts 障子.
  - **Fix:** Add 戸 to the exclusions.
  - **Confidence:** Medium-high.
- **B39-C-02 · Minor · Correctness (quiz) · words\上旬.md:9**
  - **Claim:** The card excludes 始め ("beginning; start") but not 始まり, which has the exact same title (始まり.md:4). Exclusions are not transitive, so the gap is real.
  - **Fix:** Add 始まり, or drop the whole beginning-word set consistently.
  - **Confidence:** High on the inconsistency.
- **B39-C-03 · Minor · Correctness (quiz) · words\蒸発.md:9**
  - **Claim:** The card excludes 消える but not 無くなる ("go missing; run out"; its body at 無くなる.md:15 says "go missing, disappear"). That label fits 蒸発's taught "unexplained disappearance" sense.
  - **Fix:** Add 無くなる.
  - **Confidence:** Medium.
- **B39-C-04 · Minor · Correctness (quiz) · words\生ずる.md:9**
  - **Claim:** The title "arise; produce; cause" overlaps 原因 ("cause"), and English "cause" can be read as a noun or a verb. 原因 is not excluded, even though seven weaker candidates are.
  - **Fix:** Add 原因. Optionally consider 及ぼす ("…cause an effect").
  - **Confidence:** Medium.
- **B39-C-05 · Minor · Correctness (etymology) · words\焦点.md:25**
  - **Claim:** The article says the focused-sunlight/burning association "is a learning association, not a historical derivation." Its own cited Daijisen says the opposite: 「黒い紙が焦げるところからいう」. The Kotobank sources I fetched agree:
    - Nikkoku: 「黒紙を置くと焦げるところから」, glossed as a translation of focus.
    - Nipponica: 「…燃え始めるところから、焦点という名が生じた」.
    - Sekai Daihyakka: 「これが焦点の名の由来である」.
  - **Impact:** Learners are told that a documented naming origin is only a mnemonic.
  - **Fix:** State that dictionaries explain the name by paper scorching at a lens's focal point, or delete the negative clause.
  - **Confidence:** High.
- **B39-C-06 · Low · Comprehensibility · words\生ずる.md:29**
  - **Claim:** The display text "[起す](起す.md) (おこす) can describe causing it" shows the shorter spelling. The target card is titled "wake someone up" and tells learners to write 起こす (起す.md:15); it mentions the "cause" sense only in passing (~:34).
  - **Fix:** Display 起こす (おこす), still linking to 起す.md.
  - **Confidence:** Medium.

## Optional
- 小便.md:19: 「この検査では小便を調べます」 is grammatical, but 尿 (or 検尿) is more usual for a medical test, as the article itself notes. A non-medical example would be better.
- The exclusions 小便→トイレ and 正面→面 are weakly supported but harmless.
- The existing 生じる.md (out of scope) has the same title and the same 原因 overlap as C-04.
- 戸.md:28 could link to the new 障子 card (out of scope).
- 商社 could link to 輸入.

## Limits
- I could not run Git, so committed-content equality, all hashes and the patch's identity with the commit are unverified.
- The public captures are the author's, not my own retrievals. Only MHLW and Kotobank 焦点 were fetched independently. Weblio 焦点 did not render, the first Kotobank lookup was unrelated, and the 正面切って capture is empty and not positive evidence.
- Most of the evidence JSON, the comparison renderings and both snapshot JSONs were not read. Comparison-family conclusions rest on the principal families plus existing card titles.
- CLEAN verdicts mean no actionable defect was found in scope. They are not native-speaker certification.
