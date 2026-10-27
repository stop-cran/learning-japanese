# Snapshot
Commit **bc40a3a045024123d13d384bc98ee982d085da28** (parent af44683f827c09cd1c6bee07d5c88f774bd1c5cf). I reviewed committed content only. I had file tools but could not run Git, so I could not confirm myself that the working tree matches this commit. I relied on the frozen receipt (`cleanCommittedContent: true`) and the related patch as supplied.

# Scope
- **Model:** claude-opus-5.5, Claude family. I worked alone and in sequence, with no delegation and no edits.
- **New articles:** I read all 19 completely, plus the relevant evidence: TSV lines 382–401, the batch-20 rows and principal families, componentEvidence, receipts and quizDeclarations.
- **Related edits:** I read the actual four-file patch and checked it in context: 講.md:35 and 42, 清.md:33, 40 and 48, 境.md:37 and 45, 漁業.md:5.
- **漁業 reuse:** I checked only the new `jlpt: 2` and that the fishing-industry meaning is taught (lines 15–22). I did not re-review its unchanged teaching.
- **Mappings:** all 20 (N2:382–401).
- **Not covered:**
  - I skipped quizGuardRationale, except one accidental line (see Limits) and the forbidden documents.
  - I only spot-checked the comparison families.
  - This is not a native-speaker certification.

# Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| きっかけ | CLEAN | CLEAN | CLEAN |
| ぎっしり | CLEAN | CLEAN | CLEAN |
| 基盤 | CLEAN | CLEAN | CLEAN |
| 客席 | CLEAN | CLEAN | CLEAN |
| 客間 | CLEAN | CLEAN | CLEAN |
| ギャング | CLEAN | CLEAN | CLEAN |
| キャンパス | CLEAN | CLEAN | CLEAN |
| 休業 | CLEAN | CLEAN | CLEAN |
| 休講 | CLEAN | CLEAN | CLEAN |
| 休息 | CLEAN | CLEAN | CLEAN |
| 給与 | NEEDS FIX (B20-03) | CLEAN | CLEAN |
| 休養 | CLEAN | CLEAN | CLEAN |
| 清い | CLEAN | CLEAN | CLEAN |
| 強化 | CLEAN | CLEAN | CLEAN |
| 境界 | CLEAN | CLEAN | CLEAN |
| 行事 | CLEAN | CLEAN | CLEAN |
| 恐縮 | NEEDS FIX (B20-02) | NEEDS FIX (B20-01) | CLEAN |
| 教養 | CLEAN | CLEAN | CLEAN |
| 行列 | CLEAN | CLEAN | CLEAN |

For 給与 and 恐縮, "Correctness: NEEDS FIX" refers only to quiz_exclusions metadata. The teaching text itself is correct.

**Related edits: all CLEAN on all three facets.**
- 講.md adds 休講 under Common words and entry 1227780 to the metadata line.
- 境.md adds 境界 and entry 1235960.
- 清.md links 清い on its きよ.い row and under Common words; entry 1378140 was already in the metadata line.
- 漁.md already linked 漁業 at ギョ.
- 基, 盤, 養 and 縮 have no cards and are correctly left unlinked. Because the N2 kanji set is complete, they are not N2 kanji.

**漁業 reuse:** CLEAN for the scoped claim only (`jlpt: 2` plus the fishing-industry meaning).

**Mappings:** 19 are CLEAN on all three facets. N2:398 (恐縮) needs a coverage fix (B20-01).
- Additional senses are taught: 基盤 platform, 客席 audience, ギャング gangster, 給与 pay, 行列 matrix.
- 強化's psychology sense is stated without an example, which is adequate for an additional sense.

# Findings
**B20-01 — Minor — scoped coverage**
- **Location:** words\恐縮.md:16–23 and 35.
- **Problem:** The source gloss "shame" and the selected JMdict sense 2 ("feeling ashamed (e.g. of an error)", "feeling embarrassed (e.g. by someone's compliments, hospitality)") are never taught as a positive use. The article teaches gratitude and the request preface. Line 35 mentions embarrassment only as a contrast with 恥ずかしい; "not just wrongdoing" hints at the use but doesn't teach it.
- **Learning impact:** Learners may not understand common uses such as お褒めいただき恐縮です or apologizing for one's own mistake.
- **Remedy:** Add one sentence and an example of this abashed, self-effacing use.
- **Evidence:** batch-20.json:298 (Waller definition "shame,very kind of you,sorry to trouble"); batch-20.json:1242–1246 (sense 2 glosses); Kotobank Seisenban ② 「…申訳なく思うこと。恐れ入って身を小さくすること」 (fetched).
- **Confidence:** Moderate.

**B20-02 — Minor — correctness (quiz metadata)**
- **Location:** words\恐縮.md:4 and 9.
- **Problem:** The exclusions leave out 恩 ("favor; debt of gratitude"; 恩.md:15 teaches "a sense of obligation"; it has no exclusions). They also leave out 申し訳 ("apology; excuse"). The card already excludes the gratitude words (感謝, 御礼, 礼, 有難い) and the apology words (すみません, ごめんなさい). Exclusions are not transitive, so those don't cover 恩 or 申し訳.
- **Learning impact:** "feeling obliged" or "apologetic" could reasonably be accepted for 恩 or 申し訳, and the reverse.
- **Remedy:** Add 恩 and 申し訳 to 恐縮's quiz_exclusions.
- **Evidence:** content-format.md:86–88 and 95–96; Seisenban defines 恐縮 ② using 申訳なく思う.
- **Confidence:** Moderate for 恩, low-to-moderate for 申し訳.

**B20-03 — Minor — correctness (quiz metadata)**
- **Location:** words\給与.md:4 and 9.
- **Problem:** 納める ("pay taxes; deliver goods", N2) is not excluded in either direction. 給与 already excludes 払う and 支払う because of the "pay" ambiguity. 納める.md:9 already excludes 払う, 支払う, 供給 and 支払.
- **Learning impact:** "pay; provision of money or goods" plausibly describes 納める: paying money due and delivering goods (納める.md:16).
- **Remedy:** Add 納める to 給与's quiz_exclusions.
- **Evidence:** content-format.md:86–88 and 95–96; Wiktionary (ja) 給与 sense 2: 金品などを支給すること.
- **Confidence:** Moderate.

# Optional
- 行事.md:4: "function" also appears in 機能's title ("function; feature"). Consider excluding 機能 or retitling to "social function". The other glosses in each title already make the meaning clear.
- 休講.md:9: Consider excluding おやすみ. That would match the existing 休み exclusion and 休業/休息/休養's exclusion of おやすみ. The risk is low because おやすみ's title includes "good night".
- 客間 / 応接: both titles use "reception"; consider an exclusion.
- きっかけ: Wiktionary (ja) lists a theatrical "cue" sense (a signal for acting, music or lighting in kabuki). Teaching it would cover the source gloss "cue"; if added, also exclude 合図.
- キャンパス.md:31: "the university" is supported, but "university life" isn't directly supported. Consider trimming.
- Other polish:
  - 境's キョウ reading row could use 境界 as its example.
  - 強化's psychology sense could use an example.

# Limits
- **No Git:** I couldn't execute Git, so I relied on the receipt for the commit's identity and cleanliness, and I didn't regenerate the patch.
- **Accidental read:** one grep hit batch-20.json:17813, inside quizGuardRationale, about 行列. I had already assessed 行列, and no finding depends on that line.
- **Comparison families:** I spot-checked these and did not read them all.
- **Web lookups:**
  - Weblio returned only its page footer for きっかけ, which counts as a failed lookup, not evidence.
  - Wiktionary (ja), a community source, was used for きっかけ, キャンパス and 給与.
  - The author's Kotobank/Weblio receipts for 休養, 客間, 行事, 基盤, 教養 and 行列 were not re-fetched.
- **Quiz checks:** I didn't execute the app's quiz candidate-selection weighting.
- **Naturalness:** my naturalness judgments are a reviewer's, not a native speaker's.
