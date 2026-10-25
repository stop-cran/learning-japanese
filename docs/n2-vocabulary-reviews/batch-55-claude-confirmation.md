# Batch-55 corrected snapshot: confirmation review (claude-opus-5.5)

## Snapshot
- **Corrected commit:** `cab666775db68a2cf5233ca1f8f4d13a1ff7bb40`
- **Parent (authored snapshot):** `f467750c0645c7d3f0f07d24068f418a84887b0e`
- I reviewed committed content only. My file tools cannot run Git, hash or cleanliness checks, and I did not inspect `.git`. The commit identity, the clean state and the `coverageIndexSha256` value (`9033d6e6…`, now at `docs\n2-vocabulary-snapshot.json:34`) all rest on the author's own checks.

## Scope
**Model:** claude-opus-5.5 (claude family). The review was read-only, with no edits, agents or delegation.

**Private files read this turn** (only the eight on this turn's allowlist):
- `correction-snapshot.json`, read completely and first.
- `correction.patch`, read completely.
- `correction-comparisons-compact.txt`, read completely with forceReadLargeFiles. I counted 22 families and 97 senses myself.
- `correction-existing-reading.txt`, read completely: 10 old bodies (届ける, 解釈, 読み, 働く, 広がる, 当たる, 通行, 届く, せっかく, 散らかる).
- `correction-public-reading.txt`, read completely: the 通ずる, 通用 and 突く/つつく captures.
- `corrected-review-evidence.json`, lines 31437–31610 only: `currentQuizDeclarations`, `directQuizExclusionAdditions`, `sourceNoteClarifications`, `additionalSenseRecognition` and `inspectionVolumes`. I did not read the rest.
- `frozen-snapshot.json` and `related.patch` were read in the initial turn and not reread.

**Articles reread completely on disk:**
- The eight changed articles: 散らす, 通知, 通訳, 通用, 突く, 通じる, 通路, 突き当たる.
- Two unchanged articles: 通貨 and ついで.

**Mappings and related checks:**
- I read all twenty TSV rows N2:1082–1101 and the snapshot hash line.
- I read `kanji\貨.md` completely and spot-checked `words\月日.md` by grep only.
- I summed `currentQuizDeclarations`: 17 articles, 88 pairs.
  - On-disk exclusions match for 9 of the 17 articles: the 7 changed new articles plus 通貨 and ついで.
  - The other 8 come from the derivative and the patch.

**Extra comparison reads:**
- Full bodies of words\ 通過, 至る, 達する, 効く and 働き.
- A title grep over words\*.md.
- One Weblio fetch for 働く, which returned only license boilerplate. It is not evidence.

**Inherited without rereading** (initial complete reads; unchanged according to the author's patch and changed-file list): ちり紙, 散る, 追加, 通勤, 通帳, 付き合う, 突き当たり, 点く, 次ぐ, and 月日's narrow edit.

**Initial limits retained:**
- One `.github` search in the initial turn also returned lines from unassigned `.github\agents` files. I did not rely on them.
- `review-evidence.json` was read only partially in the initial turn, and `public-bodies.json` was not read.
- Most initial comparison judgments were made from titles only.

## Verdicts

| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1082 | words\散らす.md (new) | Full reread (changed) | CLEAN | CLEAN | CLEAN |
| N2:1083 | words\ちり紙.md (new; raw 塵紙) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1084 | words\散る.md (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1085 | words\追加.md (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1086 | words\ついで.md (new; raw 序で) | Full reread (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1087 | words\通貨.md (new) | Full reread (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1088 | words\通勤.md (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1089 | words\通じる.md (reused; raw 通ずる) | Full reread (changed narrow edit) | CLEAN | CLEAN | CLEAN |
| N2:1090 | words\通知.md (new) | Full reread (changed) | CLEAN | CLEAN | CLEAN |
| N2:1091 | words\通帳.md (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1092 | words\通訳.md (new) | Full reread (changed) | CLEAN | CLEAN | CLEAN |
| N2:1093 | words\通用.md (new) | Full reread (changed) | CLEAN | CLEAN | NEEDS FIX (B55-07) |
| N2:1094 | words\通路.md (new) | Full reread (changed) | CLEAN | CLEAN | CLEAN |
| N2:1095 | words\付き合う.md (new; raw 付合う) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1096 | words\突き当たり.md (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1097 | words\突き当たる.md (new) | Full reread (changed) | CLEAN | CLEAN | CLEAN |
| N2:1098 | words\月日.md (reused; つきひ) | Inherited initial read + grep spot-check | CLEAN | CLEAN | CLEAN |
| N2:1099 | words\点く.md (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1100 | words\突く.md (new) | Full reread (changed) + TSV row | CLEAN | CLEAN | CLEAN |
| N2:1101 | words\次ぐ.md (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |

The N2:1098 verdict covers only the narrow edit (N2 level and provenance). B55-06 sits outside it.

**Reciprocal kanji 貨/通貨 (unchanged): CLEAN.**
- The カ reading row has 通貨 つうか at `貨.md:28`.
- Common words lists it at `貨.md:36`.
- Source 1433050 is cited at `貨.md:43`.
- 通貨.md links 貨.

**Baseline preservation: CLEAN.**
- 通じる keeps primary つうじる, its title, jlpt 3 and the 1983740 senses 1, 3 and 4 recognition line. It has no new guards.
- 月日 keeps つきひ, jlpt 2 and the 1255780/1609580 provenance at line 36. Its line 29 is unchanged.
- The 貨 front matter and the old comparison bodies are untouched.

**Mappings: CLEAN.**
- I read all twenty rows. According to the patch, the only change is in N2:1100:
  - `additional_senses` is now `1456890:3;1456895:1,2`.
  - The note is clarified and explicitly assigns no N2 level to つつく. The derivative also records `additionalN2Assignment: false`.
- The article cites the same recognition at `突く.md:56`.
- The source fields, primary senses, levels and other cells are unchanged.

## Findings

**Original findings**

- **B55-01 (通訳 / 解釈, 読み): RESOLVED.**
  - `通訳.md:9` now excludes 解釈 and 読み, and the body at lines 37–39 already distinguishes them.
  - The overlap is real: 1433560:1 glosses "interpretation (i.e. oral translation)", 1199010:1 "interpretation", and 1456130:3 also "interpretation".
  - The existing 解釈↔読み guard does not chain into this pair. Both reviewers raised 読み, so shared attribution is correct.
- **B55-02 (通知 / 届ける): RESOLVED.**
  - Covered by `通知.md:9` and `:40-41`.
  - 1457210:2 means "notify / file notice (to the authorities)", and the old 届ける body teaches 住所の変更を会社に届けました.
  - The new line is accurate.
- **B55-03 (突く / つつく): RESOLVED.**
  - `突く.md:48-51` matches 1456895:1-2 and the Daijisen つつく entry, senses 1 and 2 (「何度も軽く突く」, 「モズがカキを―・く」).
  - "Typically" and "Their uses overlap" present a tendency, not a rule. The light-poke example stays valid within 1456890:2, which includes "nudge".
  - The TSV additional recognition is correctly scoped.
- **B55-04 (通用 に construction): RESOLVED.**
  - `通用.md:28-31` uses the captured 「世界に―する新技術」 with correct selective kana and a reasonable English rendering.
  - で is kept at line 18, and line 31 blocks overgeneralization. No Daijisen sense number is pinned.
- **B55-05 (通じる サ変): RESOLVED.**
  - `通じる.md:38-46` glosses サ変 as an irregular class and cites the captured 「冗談が―・じない」.
  - It points learners to the 通じます/通じた/通じて/通じない forms. It does not regularize 通ずる as an ichidan verb and does not change N3.
- **B55-06 (月日/日月 claim overbroad): DEFERRED, accepted.**
  - `月日.md:29` is unchanged baseline text. I record it as future optional baseline work, not as certified clean.

**GPT findings and guard decisions**

- **F001 and F002:** the same as B55-02 and B55-01 above.
- **F003 (通用/働く): guard accepted.**
  - 1433570:2 has "to work (of an excuse, trick)", and 1451150:2 has "function; be effective; work". 働く's title is "work".
  - The guard is fine, but the body line it added is not (B55-07 below).
- **F004 (散らす/広がる): accepted.**
  - 1303460:2 includes "to spread", and 1602360:1 is "to spread (out)". `散らす.md:39` notes that 広がる is intransitive.
- **My optional guard hypotheses:**

  | Pair | Decision | Evidence |
  |---|---|---|
  | 突く/当たる | Accepted | 1456890:2 "hit, strike" vs 1448810:1-2; disclaimer at `突く.md:41` |
  | 通路/通行 | Accepted | 1433600:1 vs 1433180:1; the contrast at `:45-46` agrees with the 通行 body |
  | 通用/通貨 | Accepted | 1433570:1 "currency"; accurate contrast at `:57-59` |
  | 突き当たる/届く | Accepted, qualified | Reach/arrive per 1457200:1-2. The same bare-"reach" reasoning applies at least equally to 至る ("reach; arrive at a stage"; この道は山頂に至る) and more weakly to 達する. Not established as a defect (see Optional). |

- **ついで/せっかく and 散らす/散らかる: author's decline accepted.**
  - The titles are qualified ("with effort…", "be untidy…").
  - Both opportunity words already exclude 機会/チャンス/きっかけ.
  - 散らかす is guarded with 散らす, and 散る/散らかる is guarded.
- **散らす ます-stem wording: resolved** (`散らす.md:31`).

**Regression check**
- All changed text matches the patch and is accurate, except B55-07.
- The derivative's `sourceNoteClarifications` and `additionalSenseRecognition` match TSV row 1100.

**New finding**

- **B55-07: 通用's new 働く line reads like a synonym without a contrast.**
  - Severity: low. Facet: comprehensibility. Location: `words\通用.md:46-48`. Confidence: medium.
  - **Claim:** the line "働く also has a functioning sense behind English 'work'" comes after the overlap disclaimer at line 46, sits under Synonyms, and gives no contrast. Read beside the article's own example at `:22-23` (その言い訳はここでは通用しません, "will not work"), it suggests 働く can express that use. A learner could write the unnatural その言い訳は働きません.
  - **Evidence:**
    - The two senses differ: 1451150:2 is "function; operate; be effective", while 1433570:2 is "be accepted; work (of an excuse)".
    - The other new comparison lines each carry a contrast (`突く.md:41`, `突き当たる.md:43`, `通路.md:45-46`, `通用.md:58-59`).
    - 効く.md, outside the batch, explicitly qualifies 働く as a non-substitute.
  - **Minimal remedy:** add a clause such as "…but that sense describes something operating or functioning; an excuse or idea being accepted uses 通用する." Alternatively, move the line above line 46.

## Optional
- 突き当たる: consider guarding 至る, and weakly 達する, on the same reasoning as 届く.
- 通用: 働き ("work; functioning") and 効く ("take effect; be effective") have work/effect label overlap comparable to 働く.
- 通路: 通過 ("passage through; passing") is comparable to 通行, but weaker.
- 通訳: 受け取る ("receive; interpret") is weak.
- 突く: optionally note that 当たる is intransitive.
- 通じる: tighten the syntax of lines 41–42 ("The public dictionary classifies it as サ変…; this does not mean…").
- Still optional from the initial review:
  - 付き合う を/に patterns.
  - The 序 spelling for ついで.
  - The 衝く/撞く spellings of 突く.
  - 次ぐ adverb/conjunction wording.
  - The N2:1086 comparison wording; 1316390:1 is visible separately and is not an established mismatch.
  - ついで/せっかく and 散らす/散らかる guards.
  - B55-06 baseline wording.

## Limits
- Git, hash and cleanliness checks, and the unchanged status of the ten inherited articles, rest on the author's checks, patch and changed-file list.
- I read only the `correctionEvidence` segment of the corrected derivative. The frozen snapshot and related.patch were not reread.
- I summed the 88 pairs from the derivative, but verified them against on-disk files for only 9 of the 17 articles.
- The three public bodies are the author's original captures from one service, not fresh retrievals. My only fresh fetch (働く) failed to return the dictionary text, so B55-07's usage judgment rests on JMdict and the repository bodies.
- There is no native-speaker certification and no runtime quiz draw. Guard judgments compare labels; they do not measure actual learner confusion.
- 月日 is inherited plus a grep spot-check only.
- Initial-scope limits are retained: the `.github` search deviation, partial `review-evidence.json`, unread `public-bodies.json`, and title-only comparisons.
- The 227/685/120 counts are the author's assertions.
