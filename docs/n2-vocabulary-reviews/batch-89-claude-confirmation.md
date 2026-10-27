## Snapshot
- **Revised commit:** `5454ac0d909fda31211029db015c916ead73884e`.
- **Parent:** `af76f9749ff054e09d47489cb9fda30709bef104`, which is the snapshot I originally reviewed.
- **Content:** committed content only, as described by the author.
- **What I could not check:** I made no tool calls in this confirmation. The commit identity, clean state, hashes, validator and manifest results, and the claim that only six files changed are the author's statements. I did not check them myself.

## Scope
**Model:** claude-opus-5.5, family claude. This confirmation is deliberately not blind.

**My own reads in the original review:**
- 12 calls were started and 10 returned successfully.
- The last two (a housing-title search and a reread of 寮) were issued together, so two calls were outstanding at once, which broke the one-call rule. Both were interrupted and returned nothing.
- My earlier report, written after the interruption, used no tool calls. This confirmation also uses none.

**Supplied evidence read for this confirmation:**
- the six-file correction diff and the author's adjudication;
- both original reports;
- the 20 mappings and all 20 current articles;
- 12 complete older word cards and the 6 unchanged kanji cards, plus the original kanji patch;
- the 25 component records, the complete dictionary families, the 248 comparison labels, the format contract and the 23 public dictionary entries.

This is supplied evidence, not my own retrieval. The author's counts of what they read are their own, not my read depth.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1762 | words/来日.md | CLEAN | CLEAN | CLEAN | B89-01 resolved: hedged note on arrivals from abroad, contrast with 帰国 |
| N2:1763 | words/落第.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1764 | words/ラッシュアワー.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1765 | words/欄.md | CLEAN | CLEAN | CLEAN | Unchanged; the 段 exclusion is supported by sense 6 of 段, "column (of print)" |
| N2:1766 | words/ランチ.md | CLEAN | CLEAN | CLEAN | B89-02 resolved: business use noted for recognition only |
| N2:1767 | words/ランニング.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1768 | words/乱暴.md | CLEAN | CLEAN | CLEAN | B89-03 resolved; a paragraph break is optional polish |
| N2:1769 | words/理科.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1770 | words/利害.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1771 | words/リズム.md | CLEAN | CLEAN | CLEAN | 調子 exclusion supported: its dictionary sense 1 and its card both include rhythm |
| N2:1772 | words/リットル.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1773 | words/リボン.md | CLEAN | CLEAN | CLEAN | テープ and 帯 exclusions supported (strip, band and printing-tape senses) |
| N2:1774 | words/略す.md | CLEAN | CLEAN | CLEAN | 抜く exclusion supported: its sense 2 and card teach "omit/skip" |
| N2:1775 | words/流域.md | CLEAN | CLEAN | CLEAN | B89-04 (also reported by GPT) resolved: 範囲 removed; the other five exclusions remain |
| N2:1776 | words/寮.md | CLEAN | CLEAN | CLEAN | GPT-03 resolved; this closes my interrupted 住まい/住居 question |
| N2:1777 | words/両側.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1778 | words/漁師.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1779 | words/領事.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1780 | words/領収.md | CLEAN | CLEAN | CLEAN | GPT-01 resolved: 集金 pair strong; 集める pair a defensible cautious choice |
| N2:1781 | words/臨時.md | CLEAN | CLEAN | CLEAN | Unchanged |

**Separate assessments:**
- **Source mappings:** CLEAN and unchanged. Each article cites the selected senses.
- **Older words and kanji left untouched:** CLEAN within the supplied diff. The diff touches only six assigned word files. Each word's title, reading, kanji list and level are unchanged.
- **Components:** CLEAN. No card was invented for 第, 欄, 寮, 臨, 帰国 or 猟師.
- **Reciprocity:** CLEAN. All seven pairs are present in the unchanged kanji cards and the current articles: 乱/乱暴, 暴/乱暴, 略/略す, 域/流域, 漁/漁師, 領/領事 and 領/領収.
- **Regressions:** none found.

**Final: ACCEPT**

## Findings
No actionable defect remains. How each earlier finding was reconciled:

- **B89-01 (来日) — Minor; scoped coverage; resolved at words/来日.md:24-26 and 46.**
  - The new lines cover arrivals from abroad, mainly foreign visitors, and contrast ordinary 帰国 for returning home.
  - "Typically" and "especially" avoid an absolute nationality rule.
  - Evidence: the Daijisen らいにち heading (外国人が日本に来ること) and dictionary entry 1548200, sense 1. 帰国 has no card, so plain text with a kana reading is correct.
  - Confidence: high.
- **B89-02 (ランチ) — Minor; comprehensibility; resolved at words/ランチ.md:35-39 and 42.**
  - **Correction to my original report:** I wrongly gave 2854169 as the ローンチ entry; 2854169 is the boat entry. The ローンチ entry (2448600) lists ローンチ, ラウンチ and ロンチ, not ランチ. So only the Daijisen cross-reference supports ランチ for a business launch: ランチ【launch】 sense 2 points to ローンチ.
  - The revision presents that as recognition only, with no frequency claim and no N2 claim. I accept the author's "partially supported" verdict, because the original text was narrowly framed.
  - Confidence: high.
- **B89-03 (乱暴) — Minor; coverage and comprehensibility; resolved at words/乱暴.md:26-31.**
  - 人に乱暴する is a correct construction: an intransitive する verb with the person marked by に.
  - The caution is supported by the dictionary entry (sense 1 includes "assault"; sense 3 is sexual assault) and by Daijisen's example 「―されたと訴える」. It makes no claim about how often the assault reading is used.
  - Part of my original remedy, pointing learners to 乱暴な運転, was redundant because the example already existed; I withdraw that part.
  - Confidence: high on structure. Naturalness is not native-certified.
- **B89-04 / B89-GPT-02 (流域) — Minor; quiz exclusions; resolved at words/流域.md:9.**
  - 範囲's dictionary sense is extent/scope, and its card has no basin sense. The 流域 body never mentioned 範囲, so nothing is left stale.
  - Confidence: medium-high.
- **B89-GPT-03 (寮) — resolved at words/寮.md:9.**
  - The 住居 card explicitly allows boarding accommodation as a residence. 住宅's dictionary sense is residence/housing, and 住まい's is dwelling/residence.
  - This is the same observation as my unverified 住まい/住居 hypothesis, now settled. The body does not need to mention the three words.
  - Confidence: medium; this is an editorial judgment.
- **B89-GPT-01 (領収) — resolved at words/領収.md:9.**
  - 集金 ("money collection"; its card's membership-fee example parallels 領収's): confidence high.
  - 集める: medium. It has one broad collect/gather sense, and its card mentions gathering money. Because English "collect" covers receiving a payment, this is a defensible cautious exclusion, not an excessive one.
- **My original Limits, now closed:**
  - 調子, 抜く, テープ, 帯 and 段 exclusions are supported by their complete dictionary families and cards. I withdraw my "possible excess" concern about 調子.
  - I agree 滞在 needs no exclusion with 来日: the 来日 card separates the arrival from the stay.
  - My earlier comparison of title-search matches was based on notes. It is now confirmed against the exact exclusion lists: for example, 乱暴 excludes 荒い, 激しい and 暴れる, and 略す excludes 省く, 省略 and 略語.
- **Author's handling of my optional suggestions:**
  - 略す: I agree. My wording "the godan form of 略する" was loose. Daijisen calls 略す a 五段化 (godan development) of サ変 略する, which is not a conjugated form. I withdraw the unqualified wording.
  - 両側: I agree to withdraw the claim that りょうそく is less common. The current neutral "also recorded" is enough.

## Optional
- **乱暴:** add a paragraph break before "The adjective can criticize…" so that sentence does not read as part of the assault caution. Optionally mention 暴力を振るう for plainly physical violence.
- **ランチ:** optionally state the business-launch recognition more directly, and add a boat-sense example.
- **欄:** the linked 段 card teaches only senses 1–4. Optionally cite sense 6 of 段 (entry 1633690) next to the printing-column claim.
- **臨時:** the adverbial 臨時に (Daijisen: 「―に作業員を雇う」), and GPT's smoother translation of 臨時休業.
- **Other expansions, if wanted:** 通勤ラッシュ, 及第/不合格, リッター, "fisher", 投書欄, register notes, and a mention of 住居/住宅 in the 寮 body.

## Limits
- **Unchecked by me:** I made no tool calls and did no public retrieval in this confirmation. Git state, hashes, the validator, the manifest and runtime quiz behaviour remain the author's statements.
- **Original process:** two calls were outstanding at once in the original review, and its report was written after context compaction.
- **Open hypothesis (low):** 寮/宿泊 ("lodging; overnight stay") may need an exclusion. I did not have 宿泊's card or dictionary family.
- **Not certified by native speakers:** the naturalness of 読者欄 and 人に乱暴してはいけません, and how often 乱暴 is used for assault.
- **Pair coverage:** I compared quiz exclusions against the 248 labels and the supplied cards and dictionary families, not every one of the 435 families. This is not an exhaustive corpus check.
- **Bias:** this confirmation was not blind and does not measure bias reduction.
