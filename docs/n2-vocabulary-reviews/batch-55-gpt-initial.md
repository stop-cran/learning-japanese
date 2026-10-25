## Snapshot: f467750c0645c7d3f0f07d24068f418a84887b0e; committed content only

**NEEDS FIX: four quiz-exclusion findings affecting four new articles.** No actionable defect was established in the assigned lexical coverage, Japanese explanations, or narrow reuse edits.

Read `batch-55-frozen-snapshot.json` first. It identifies parent `b005473a6a1dda6e0b52dd1f43c94bf7d7b22d75` and asserts clean, committed content. **File tools cannot execute Git:** I could not independently verify the commit, parent comparison, worktree cleanliness, or recorded hashes. The content verdicts below are conditional on the supplied frozen-snapshot provenance.

## Scope: GPT-6.1 Sol, model ID gpt-6.1-sol

This was a read-only review, with no agents, delegation, or edits.

**Assigned content:** completely read all eighteen new articles, reused `words\通じる.md` and `words\月日.md`, complete `kanji\貨.md`, and complete `batch-55-related.patch`. Reused articles were judged only for the requested source coverage and narrow additions—not as newly authored baseline teaching.

**Guidance and mappings:** read `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md`, `docs\content-format.md:18–126`, `docs\confusable-words.md`, `docs\jlpt-levels.md`, both permitted snapshot documents, and only the assigned twenty mappings in `docs\n2-vocabulary-sources.tsv`.

**Blind evidence:** completely read `review-mappings.jsonl`, `review-principals.jsonl`, `review-components.jsonl`, `review-labels.jsonl`, all nine `family-inspection-01.txt`–`09.txt` renderings, `supplement-comparison-reading.txt`, and both `public-bodies.txt` and `public-bodies.json`. Private filenames here use the supplied `batch-55-` prefix. Read only lines 1–180 of `review-evidence.json`; did not read `principal-reading.txt`, whose principal-family coverage was supplied by the complete JSONL.

The packet distinguishes twenty source principal families/56 senses from the additional retained 通じる teaching family: 21 teaching/source families/70 senses. The nine comparison renderings reportedly contain 221 families/669 senses, with six distinct supplemental families/16 senses, yielding the reported 227-family/685-sense union. These totals include the principals; they are not additional families. I read those renderings but did not computationally reproduce their counts or equivalence checks.

**Actual older comparison-body reads: 96 complete articles**, separate from the twenty assigned articles:

| Group | Articles |
|---|---|
| Scattering and initial comparisons | 届ける, 訳, 付く, 続く, 散らかす, 散らかる, 広がる, 落ちる, 消える, 解散, 配る |
| Addition, opportunity, paper, money | 加える, 加わる, 足す, 付ける, 補う, 増加, 機会, チャンス, きっかけ, 紙, お金, 金, 金銭, 現金, 硬貨, 紙幣, 札, 円, 銅貨 |
| Commuting, notification, interpreting, validity | 通う, 出勤, 通学, 知らせ, 知らせる, 伝える, 連絡, 報告, リポート, レポート, 掲示, 案内, 翻訳, 解釈, 読み, 有効, 効力, 成立, 妥当, 通る, 循環, 適用 |
| Passage, relationships, endpoints, physical actions | 廊下, 道, 道路, 交際, 付き合い, 交流, 従う, デート, 端, 末, 先, 終点, 終わり, 最後, 衝突, 当たる, 着く, 燃える, 光る, 刺す, 押す, 叩く, 打つ, 次 |
| Additional nonpair/secondary-sense comparisons | 働く, 勤める, 銀行, ノート, 気付く, 通過, 就く, 届く, 連れる, 連れ, 一緒, 通行, 通信, 効く, 効果, 働き, 便り, 受け取る, ぱらぱら, ぽつぽつ |

This includes the actual older bodies referenced by the new articles’ declared exclusions. The 131 label records were navigation evidence, not substitutes for body reads.

No prohibited ledgers, author-rationale source file, private-directory searches, or other reviewers’ reports were accessed.

## Verdicts: twenty source rows

**Correctness includes quiz-metadata semantics. Scoped coverage concerns the requested practical lexical scope, not exhaustive dictionary expansion.** CLEAN means no actionable defect established within this review.

| Source ID | Exact article association | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| N2:1082 | `words\散らす.md` — new | NEEDS FIX — F004 | CLEAN | CLEAN |
| N2:1083 | `words\ちり紙.md` — new; raw 塵紙 | CLEAN | CLEAN | CLEAN |
| N2:1084 | `words\散る.md` — new | CLEAN | CLEAN | CLEAN |
| N2:1085 | `words\追加.md` — new | CLEAN | CLEAN | CLEAN |
| N2:1086 | `words\ついで.md` — new; raw 序で | CLEAN | CLEAN | CLEAN |
| N2:1087 | `words\通貨.md` — new | CLEAN | CLEAN | CLEAN |
| N2:1088 | `words\通勤.md` — new | CLEAN | CLEAN | CLEAN |
| N2:1089 | `words\通じる.md` — reused; raw 通ずる | CLEAN | CLEAN | CLEAN |
| N2:1090 | `words\通知.md` — new | NEEDS FIX — F001 | CLEAN | CLEAN |
| N2:1091 | `words\通帳.md` — new | CLEAN | CLEAN | CLEAN |
| N2:1092 | `words\通訳.md` — new | NEEDS FIX — F002 | CLEAN | CLEAN |
| N2:1093 | `words\通用.md` — new | NEEDS FIX — F003 | CLEAN | CLEAN |
| N2:1094 | `words\通路.md` — new | CLEAN | CLEAN | CLEAN |
| N2:1095 | `words\付き合う.md` — new; raw 付合う | CLEAN | CLEAN | CLEAN |
| N2:1096 | `words\突き当たり.md` — new | CLEAN | CLEAN | CLEAN |
| N2:1097 | `words\突き当たる.md` — new | CLEAN | CLEAN | CLEAN |
| N2:1098 | `words\月日.md` — reused; source つきひ | CLEAN | CLEAN | CLEAN |
| N2:1099 | `words\点く.md` — new | CLEAN | CLEAN | CLEAN |
| N2:1100 | `words\突く.md` — new | CLEAN | CLEAN | CLEAN |
| N2:1101 | `words\次ぐ.md` — new | CLEAN | CLEAN | CLEAN |

**Separate related-content and mapping judgments:**

| Surface | Judgment | Basis |
|---|---|---|
| 貨 reciprocal addition | CLEAN | Substantive 貨 link in 通貨; `kanji\貨.md:28` supplies 通貨 **つうか** under **カ**; line 36 adds it to Common words. |
| 貨 baseline metadata | CLEAN within supplied patch; independent Git preservation UNVERIFIED | The complete card and patch show no change to its N2 level, readings, strokes, radical, tags, title, or distractors. |
| Reused identities and easier level | CLEAN within supplied patch | 通じる retains its ID, primary つうじる, title and N3. 月日 retains its ID, primary つきひ and baseline がっぴ recognition. |
| Twenty mapping associations | CLEAN | Source IDs, readings, article associations, principal identities and selected/additional senses agree with the inspected content. This does not approve every meaning independently as N2. |
| Primary written-kanji metadata and links | CLEAN | Every primary written Han is retained; existing components have substantive word-side links. Missing 帳 remains in 通帳 metadata without a fabricated card. Kana-primary ついで and ちり紙 are handled appropriately. |

Important source distinctions are preserved: raw 付合う is search-only, while 付き合う is canonical; 塵紙/ちりがみ and 序で/ついで remain visibly taught; 序で and 次いで are not conflated. 通ずる’s empty **source-row gloss** is not treated as recovered compiler intent: its explicit crossreferences support reuse, and selected senses 1, 3 and 4 remain nonexhaustive author scope. The サ変 warning does not instruct regular ichidan conjugation of 通ずる.

Public-backed additions—including deposit currency, broader 通帳 transaction books and nonhuman 付き合う—are attributed without fabricated pinned sense numbers. Pointing/lighting homographs and the public つく/つつく headings are separated appropriately. No additional actionable exclusion excess was established; ordinary secondary senses justify otherwise nonobvious guards such as 点く/付く and 次ぐ/続く.

## Findings: four actionable quiz-metadata gaps

All four findings concern **English-label ambiguity**, not unrestricted interchangeability of the Japanese words. Under `docs\content-format.md:85–96`, guards are symmetric, apply between other choices too, and are nontransitive.

**F001 — Medium — Quiz correctness: missing 通知/届ける guard.**

**Location:** `words\通知.md:9`; comparison `words\届ける.md:4,19–21`. 通知’s exclusions omit 届ける, and 届ける declares no reverse guard. Its complete title is **“deliver; notify”**, and its body explicitly teaches notifying an authority, including notifying a company of an address change. 通知 likewise teaches notifying recipients of a change (`通知.md:16–20`). These are genuine notification meanings, not merely a shared communication topic. The distinct labels can therefore create defensible alternatives.

**Minimal remedy:** add `届ける` to 通知’s exclusions; preserve both explanations.

**Exact lexical evidence:** complete entry **1457210:2**, `batch-55-family-inspection-06.txt:33–37`, includes “to notify,” “to file notice” and “to give notice”; 通知 **1433470:1** supplies notification/reporting. **Confidence: high.**

**F002 — Medium — Quiz correctness: unguarded “interpretation” alternatives for 通訳.**

**Location:** `words\通訳.md:9,45–47`; comparisons `words\解釈.md:4,9,15–18,43` and `words\読み.md:4,9,16–21`. The complete older titles are **“interpretation”** and **“reading; interpretation”**. Neither is guarded against 通訳. The body correctly distinguishes understanding from interlanguage interpreting, but the quiz does not display that prose: unqualified English **interpretation** is itself a supported gloss for 通訳. Consequently, a 通訳 question can offer both its precise title and another defensible English interpretation label; the reverse English prompt is also underspecified. 解釈/読み’s existing mutual protection does not protect either from 通訳.

**Minimal remedy:** add `解釈` and `読み` to 通訳’s exclusions, without changing the useful semantic distinction.

**Exact lexical evidence:** complete **1433560:1–2**, `batch-55-family-inspection-05.txt:64–68`, explicitly glosses sense 1 **“interpretation (i.e. oral translation)”** and sense 2 “interpreter.” **Confidence: high for 解釈; medium-high for 読み’s compound label.**

**F003 — Medium — Quiz correctness: missing 通用/働く guard.**

**Location:** `words\通用.md:9,22–26`; comparison `words\働く.md:4,15–31`. 働く’s complete title is **“work”**, with no reverse exclusion. 通用 explicitly teaches **“That excuse will not work here”** and extends this to an excuse, idea or method working. Thus “work” remains a defensible English answer for 通用 despite 働く’s employment-focused article. This is not an inference that employment and validity are synonymous: it is an overlap in the displayed English label, reinforced by an ordinary nonemployment sense of 働く.

**Minimal remedy:** add `働く` to 通用’s exclusions.

**Exact lexical evidence:** complete **1433570:2** explicitly includes “to work (of an excuse, trick, etc.)”; complete **1451150:2** includes functioning, effectiveness and “to work (i.e. … works),” in `batch-55-family-inspection-05.txt:70–75,140–146`. **Confidence: high.**

**F004 — Medium — Quiz correctness: missing 散らす/広がる guard.**

**Location:** `words\散らす.md:9,16–23`; comparison `words\広がる.md:4,15–18`. 広がる’s complete title is **“spread out; extend”**, with no reverse exclusion. English **spread out** can be transitive as well as intransitive, and is defensible for 散らす’s distribution over an area. The source directly supplies “to spread” for 散らす. Explaining the Japanese transitivity distinction in the bodies does not disambiguate the unqualified English option shown in a quiz. The existing 散らす/散る and 散る/広がる guards do not transitively supply this missing pair.

**Minimal remedy:** add `広がる` to 散らす’s exclusions; retain the Japanese transitivity teaching.

**Exact lexical evidence:** complete **1303460:2** in `batch-55-review-principals.jsonl` includes “to disperse,” “to distribute,” **“to spread”**; complete **1602360:1**, `batch-55-family-inspection-08.txt:19–22`, supplies “to spread (out)” and “to extend.” **Confidence: medium-high.**

## Optional: none

No additional senses, new cards, broad exclusion cliques, or unrelated baseline rewrites are necessary to address these findings.

## Limits: provenance and independent verification

The frozen commit association, clean-state assertion, hashes and derivative-equivalence checks remain **independently UNVERIFIED**. The supplied patch supports narrow baseline preservation, but cannot replace an independently executed parent/commit comparison.

This was not a complete inspection of all 235 captured identities or the entire word corpus. The author’s reported 120 old-body reads are not my scope; mine is the 96 explicitly listed above. No automated quiz generation or runtime behavior was independently exercised.

The twenty public captures provide relevant lexical bodies from **one dictionary service**, not twenty independent dictionaries or fresh reviewer retrievals. Fresh English-dictionary retrieval attempts at Cambridge, Merriam-Webster and Collins failed with HTTP 520/403 responses and supplied no corroboration; the findings rely on the inspected Japanese lexical records and actual article labels instead.

No measured-frequency, pitch-accent, compiler-intent or native-speaker-certification claim is made. CLEAN is bounded to the inspected content and requested scope.
