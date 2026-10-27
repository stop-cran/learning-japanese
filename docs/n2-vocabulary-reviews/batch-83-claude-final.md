## Snapshot

- **Final commit:** 72ca9f6dd4674f48e01af3912161a1972d890efe.
- **Parent:** fefa0999ef3171b8fd54f5609376ddd4f714e227.
- **Changed since parent:** only `words/巡る.md`. The edit adds `見物` and `サークル` to its quiz exclusions.
- **Basis:** committed content only.
- **Hash limitation:** file tools cannot run Git or compute hashes. All hashes, the clean-content flag and the unchanged-mapping claims are reported by the author, not checked by me.

## Scope

- **Model:** claude-opus-5.5 (family claude), in the original session.
- **Fresh reads this turn:** 41 calls, each awaited before the next, no file read twice.
  - The 40 required reads:
    - final-snapshot, final.patch, final-dossier, final-comparison-families (1260000, 1054850) and runtime-evidence
    - all 20 word articles in full
    - kanji 刺, 詞, 印 and 群
    - 利益, 見物 and サークル
    - correction-older-01 to -04 and benefit-comparisons
    - both instruction files, and content-format.md lines 18–103
  - One bounded title search of `words\` for now / current / present / benefit / bless / abound / circle / sightsee / tour.
- **Carried forward, not reread:**
  - From the initial session: 20 mappings, 20 principals, 28 components, 268 labels, the TSV header and rows 1642–1661, public-bodies.txt, canonical-public-bodies.txt, related.patch, the older bodies (恩恵, 現在, 望む, 土産), 創作 lines 1–12, and the Kotobank page for 目覚ます.
  - From the first confirmation: correction-snapshot, correction.patch, correction-reconciliation, and the 30 correction principal/comparison records. These include 1535320/1535330, 巡る sense 2 "to circle", 望む sense 3 "command (a view of)", and 1631840.
- **Not read:**
  - family-inspection and old-body-inspection files, supplemental files, review-evidence, the JSON public-body files, and the full blind or source packets
  - the current 回る, 目標, 命じる and 後輩 articles
  - manifest.json
- **Concurrency history:**
  - Initial review: at most 1 call outstanding for GPT, 4 for Claude. My initial report's claim of one call at a time was wrong.
  - First confirmation: at most 1 for GPT, 2 for Claude. Claude made 381 calls, was interrupted and produced no report. No out-of-memory cause is inferred from that.
  - The reviewer processes themselves ran one after another.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1642 | 紫 | CLEAN | CLEAN | CLEAN | Colour, plant and soy-sauce uses kept apart; white-flower qualification (Daijisen). |
| N2:1643 | 群れ | CLEAN | CLEAN | CLEAN | Reused card: jlpt 2 present, 12 exclusions intact, link to 群. |
| N2:1644 | 姪 | CLEAN | CLEAN | CLEAN | 姪の子 caution now follows 姪っ子 (lines 30–31). No regression. |
| N2:1645 | 名作 | CLEAN | CLEAN | CLEAN | Evaluative meaning; 傑作/作品/古典 guards are sound. |
| N2:1646 | 名刺 | CLEAN | CLEAN | CLEAN | Daijisen explanation of 刺; contrast with the homophone 名詞. |
| N2:1647 | 名詞 | CLEAN | CLEAN | CLEAN | Notes the 代名詞 framework difference; sentence role not tied to the word class. |
| N2:1648 | 名所 | CLEAN | CLEAN | CLEAN | Not the old などころ uses; 目印 distinction. |
| N2:1649 | 命ずる | CLEAN | CLEAN | CLEAN | サ変 forms explained; 順序 and 望む distinctions; unchanged. |
| N2:1650 | 迷信 | CLEAN | CLEAN | CLEAN | Evaluative force stated as a quality of the word. |
| N2:1651 | 名物 | CLEAN | CLEAN | CLEAN | 名物教師 (local-character use) supported by Daijisen. |
| N2:1652 | めいめい | CLEAN | CLEAN | CLEAN | Source spelling 銘々 recognised; luggage wording revised (line 24); no regression. |
| N2:1653 | 目上 | CLEAN | CLEAN | CLEAN | Relational term; the "social superior" qualifier is kept. |
| N2:1654 | メーター | CLEAN | CLEAN | CLEAN | Overlap with メートル given as a tendency, not a rule. |
| N2:1655 | 恵まれる | CLEAN | CLEAN | CLEAN | 恩恵 and 利益 guards present; Nに pattern taught. |
| N2:1656 | 巡る | CLEAN | CLEAN | CLEAN | 見物 and サークル added; 28 unique exclusions, no self-reference; distinct from 回る/まわる. |
| N2:1657 | 目指す | CLEAN | CLEAN | CLEAN | Mnemonic labelled as a learning aid, not etymology. |
| N2:1658 | 目覚まし | CLEAN | CLEAN | CLEAN | Source spelling 目覚し recognised under the same めざまし entry. |
| N2:1659 | 目下 | CLEAN | CLEAN | CLEAN | めした/1535320 kept; separate もっか/1535330; 現在 and 今 guards. |
| N2:1660 | 目印 | CLEAN | CLEAN | CLEAN | 目標 navigation use not denied; separate もくひょう entry. |
| N2:1661 | 目立つ | CLEAN | CLEAN | CLEAN | Intransitive; noticer vs. noticed explained. |

**Separate assessments:**
- **Mappings (CLEAN, carried forward):** all four special cases hold.
  - 銘々 maps to めいめい, 1532810.
  - 目覚し maps to 目覚まし, 1535340.
  - 目下 maps to めした, 1535320; the raw gloss is kept and openly contrasted.
  - 巡る (1342050) and 目印 (1535300) stay separate from 回る (1604300) and 目標 (1535650).
- **Components (CLEAN):** every written kanji appears in each card's metadata.
  - No links are invented for 紫, 姪, 恵 or 巡.
  - めいめい correctly has an empty kanji list.
- **Reciprocal links (CLEAN):** 名刺↔刺 (1531550), 名詞↔詞 (1531570), 目印↔印 (1535300) and 群れ↔群 (1247510) all link both ways and cite the entry.
- **Kanji preservation (CLEAN):** I read the current content fresh. The comparison against the pre-batch kanji cards is carried forward from related.patch.
- **群れ reuse (CLEAN):** the current card matches my initial record. The comparison against the original baseline is carried forward plus the author-reported hash.

## Findings

- **B83-C1: RESOLVED.**
  - **Severity and facet:** Moderate; correctness (quiz).
  - **Location:** 目下.md:9 and 39–43.
  - **Claim:** written-only prompts let a learner read 目下 as もっか ("at present; now"). The new guards fix that quiz ambiguity. The めした identity was already correct and is unchanged.
  - **Evidence:** in WordQuizPrompt, the Japanese-to-English prompt shows only the written word, and the reading appears only in a dialog the user opens. WordOptionLabel shows Japanese answer options as written labels. The 現在 and 今 card titles are in correction-older-01.
  - **Confidence:** high.
- **B83-C2: RESOLVED.**
  - **Severity and facet:** Minor; correctness.
  - **Location:** 恵まれる.md:9.
  - **Claim:** 恩恵 ("benefit; blessing") overlaps directly with "be blessed with". 利益 overlaps on its bare "benefit" label, its sense 2 ("benefit, advantage") and the English verb sense "to benefit". The りやく-only sense 3 is not relied on. No edit to 利益.md is needed, because exclusions apply in both directions.
  - **Confidence:** high for 恩恵; moderate for 利益.
- **B83-C3: WITHDRAWN (my earlier removal recommendation).**
  - **Location:** 巡る.md:9.
  - **Claim:** the 丸, 円 and 輪 titles each contain a bare "circle", and JMdict 1342050 itself glosses 巡る as "to circle". Japanese-to-English options show only the bare titles, so these guards should stay.
  - **Confidence:** moderate–high.
- **B83-C4: WITHDRAWN.**
  - **Location:** 命ずる.md:9 and 43–44.
  - **Claim:** 1519630 sense 3 is "command (a view of)", and the 望む card teaches 海を望む部屋. The 命ずる title contains a bare "command". Keep the guard and the body's distinction between the two uses.
  - **Confidence:** moderate–high.
- **B83-R1: RESOLVED (agree).**
  - **Severity:** Low.
  - **Location:** 巡る.md:9 and 21; 見物.md:4 and 15.
  - **Claim:** 1260000 sense 1 ("sightseeing", transitive) and 京都を見物する match the touring use in 古い寺を巡りました.
  - **Reasoning:** this is a separately checked direct pair. It is not inherited through 観光, since exclusions do not chain.
  - **Confidence:** moderate.
- **B83-R2: RESOLVED (agree).**
  - **Severity:** Low.
  - **Location:** 巡る.md:9; サークル.md:4, 9 and 21.
  - **Claim:** the title "club; circle" contains a bare "circle"; 1054850 sense 2 is "circle (shape)".
  - **Reasoning:** this follows the same English-label reasoning as C3. It does not rely on topic similarity or treat the Japanese noun and verb as the same word.
  - **Confidence:** moderate.

**Regressions in the five revised cards:** none found. The two newly added exclusion targets (見物, サークル) exist as files. The other targets are carried forward.

**Remaining actionable defects:** none.

## Optional

- **目下, wider search:** the title search also found ひとまず ("for now; for the time being"), さて ("well then; now") and 現状 ("current state"). None is shown to be a defensible もっか answer. No change; low confidence.
- **Dispositions I agree with:**
  - The 利益 guard is borderline but harmless.
  - Leave くるり out ("a quick turn around" is one compact turn).
  - The 目上/優れる suggestion is withdrawn.
  - 名作/創作 needs no change, and the 名物/特徴 guard stays.
  - The めいめい/各々 guard is redundant because their titles are identical.
  - Expanding 命ずる production examples (人にVように命ずる) is deferred.

## Limits

- **No Git or hashes:** I could not run Git or compute hashes.
- **Not checked:** the validator and manifest were not run or read, and no actual quiz was run. The app-code excerpts are the author's capture, not a direct read of GitHub.
- **Dictionaries:**
  - I did not fetch the American Heritage entries the dossier cites. My acceptances rest on JMdict glosses and ordinary English usage.
  - Daijisen via Weblio was the only public authority, and the 目覚し page extraction had failed earlier.
- **Carried-forward evidence:** this was not reread.
- **Native speaker:** this review is not native-speaker certification.
- **Consequential unresolved claims:** none.
