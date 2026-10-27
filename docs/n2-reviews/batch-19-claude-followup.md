**Snapshot:** I reviewed corrected commit `a1368845a79c8a659a60fed732b6d0a1c155a4c6` against original snapshot `42a8e121fad9901d0738f130164809fb926bc46c`, using committed files only. I had file tools but could not run Git or the validator, so I did not confirm that the files on disk match the corrected commit. The clean worktree, 14-file scope, zero validator errors, 848-row audit and manifest `cbcc13ceec6bbbe2` are the author's checks; I did not reproduce them.

**Scope:**
- **Model:** claude-opus-5.5 (claude family).
- **Pages read in full:**
  - `kanji\脳.md`
  - `kanji\舟.md`
  - `kanji\般.md`
  - `kanji\荒.md`
  - `words\脳.md`
  - `words\舟.md`
  - `words\荒れる.md`
- **Diff:** the actual `n2-batch-19-fix.patch` and my original report, `docs\n2-reviews\batch-19-claude-initial.md`.
- **Comparison pages:**
  - Kanji: `kanji\服`, `kanji\申`.
  - Words: 気, 胸, 腹, ケース, 箱, 飛行機, かさかさ, 嵐 and ざらざら.
- **Pinned records** (`docs\n2-batch-sources\batch-19.json`):
  - The comparison words: 1221520 (気), 1237820 (胸), 1501110 (腹), 1047880 (ケース), 1585650 (箱), 1485470 (飛行機) and 1037130 (かさかさ).
  - The new words' own entries: 1602800 (船/舟) and 1281490 (荒れる).
- **Searches:** I searched only kanji distractor lines and `words\` title lines for "mind", "rough", container and boat labels.
- **Public pages:**
  - Kotobank 精選版 日本国語大辞典 ふね【船・舟・槽】: verified.
  - Jisho ざらざら (JMdict): verified.
- **Not read:** forbidden ledgers, authoring notes and other reviewers' reports.

**Verdicts:**

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\脳 | CLEAN | CLEAN | CLEAN |
| kanji\舟 | CLEAN | CLEAN | CLEAN |
| kanji\般 | CLEAN | CLEAN | CLEAN |
| kanji\荒 | CLEAN | CLEAN | CLEAN |
| words\脳 | CLEAN | CLEAN | CLEAN |
| words\舟 | CLEAN | CLEAN | CLEAN |
| words\荒れる | CLEAN | NEEDS FIX | CLEAN |

**Findings:**

**B19-1 — Resolved.**
- `kanji\脳.md:3,14` now read "brain; mind". This matches line 20, the word article and JMdict 1470380, and the card does not call KANJIDIC2's "memory" gloss false.
- The swap from 胸 to 服 "clothing" (`:11`) is semantically wrong for the target, as a distractor should be. No kanji card uses 脳 as a distractor. 心 is the only other kanji title containing "mind", and the two cards never appear as each other's distractors.

**B19-2 — Resolved.** `kanji\般.md:39` is now grammatical and explains ハン→パン only for 一般 and 全般, with 諸般 keeping ハン. It does not claim a general sound rule.

**Optional suggestions adopted — both resolved:**
- **舟 distractor:** 缶 became 申 "humbly say" (`kanji\舟.md:11`), which is semantically wrong for 舟.
- **嵐 link:** added at `kanji\荒.md:47`. The link resolves, and 嵐 あらし is titled "storm; tempest".

**Optional suggestions not adopted — remain optional:**
- Retitling 般.
- Removing `野菜.md:30`.
- A register cue for すさぶ/すさむ. I agree that missing register flags do not establish a register.

**New exclusions — each verified against an applicable pinned sense:**
- **気:** 1221520, sense 1.
- **胸:** 1237820, sense 6.
- **腹:** 1501110, sense 3.
- **ケース / 箱:** 1047880 and 1585650.
- **槽 (tub/vat/trough):** 1602800 sense 2, plus the Kotobank sense [1]②(ロ)(ホ).
- **Seaplane:** 1602800 sense 1, restricted to 船/舟.
- **かさかさ:** 1037130, sense 1.
- The new prose limits each overlap and does not suggest the words can be swapped freely.
- My earlier gap about other container labels is now closed: the only "bath; bathtub" overlap was already excluded through 風呂 and お風呂.

**B19-C1 — Minor; scoped coverage; `words\荒れる.md:8,48-50`. This is not a regression.**
- **Problem:** The かさかさ fix covers the rough-skin overlap, but ざらざら (`words\ざらざら.md:4,7`), titled "rough and gritty", is still not excluded.
  - Both answer labels use "rough" in the tactile sense.
  - 荒れる's own skin example (`:20`) translates the verb as "get rough".
  - Exclusions are not transitive, so ざらざら excluding かさかさ does not cover 荒れる.
- **Remedy:**
  - Add ざらざら to `quiz_exclusions`; one side is enough because exclusions are symmetric.
  - Optionally extend lines 48-50 and cite JMdict 1005420.
- **Evidence:**
  - 1281490: "to become rough (of skin); to get chapped" (`batch-19.json:5228-5229`).
  - JMdict 1005420, sense 1 (via Jisho): "rough (touch, voice, etc.); coarse; gritty".
- **Confidence:** medium. The label overlap is established. That 肌がざらざら is a natural collocation is my judgment, not fetched evidence. My original review missed this.

**Regressions:** none found.

**Optional:**
- The seaplane rationale for excluding 飛行機 is accurate and limited, but thin.
- 荒's citation could add 嵐's entry; the 嵐 article already cites its own source.
- かまう "mind; be concerned" shares the English word "mind" with 脳 "brain; mind" only as a verb/noun homograph. I have not established this as a defect.

**Limits:**
- This is a bounded review of changed passages only.
- I executed no Git, validator or manifest checks.
- I did not review the stroke drawing paths in full.
- I did no runtime quiz testing, so I cannot say whether automatic scoring would actually pair 荒れる with ざらざら.
- I give no native-fluency certification.
- Several fetches failed or returned irrelevant pages: a Kotobank page reached through a wrong ID, an empty Kotobank search, an unrelated Weblio page and an empty Jisho sentence search. These are limits, not evidence either way.
