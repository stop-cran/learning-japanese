## Snapshot
The frozen commit is `033d125b6c4aa4438587e603296d582f2750195d` (parent `6f9f96981807319a347cd3c202d2d94cfb48c92e`). I reviewed committed content only. I had file tools but no Git execution, so I couldn't verify the working tree or file hashes against the commit. I relied on the receipt's `cleanCommittedContent: true`.

## Scope
**Model:** claude-opus-5.5 (Claude family). I worked alone, read only, and did not delegate.

**What I read:**
- All 19 new articles, in full.
- The five related changes, in their surrounding context: 根.md:36,45; 書く.md:21,26; におい.md:33; kaeru article:131; confusable-words CW011:124.
- 替える.md, checked only for whether it teaches the 代える substitution meaning (sense 3).
- All 20 TSV mappings (N2:242-261) and all 20 main dictionary entries in batch-13.json.
- Selected comparison entries, the author's page-inspection records, the identity note and the source-access limits.

**Omissions:** I did not re-review unchanged teaching in the related files. I read batch-13.json in sections, not every comparison entry. I did not open any of the files I was told not to read.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 回転 | CLEAN | CLEAN | CLEAN |
| 解答 | CLEAN | CLEAN | CLEAN |
| 回答 | CLEAN | CLEAN | CLEAN |
| 外部 | CLEAN | CLEAN | CLEAN |
| 解放 | CLEAN | CLEAN | CLEAN |
| 開放 | CLEAN | CLEAN | CLEAN |
| 海洋 | CLEAN | CLEAN | CLEAN |
| 概論 | CLEAN | CLEAN | CLEAN |
| 帰す | NEEDS FIX (B13-01) | CLEAN | CLEAN |
| かえって | CLEAN | CLEAN | CLEAN |
| 返る | CLEAN | NEEDS FIX (B13-02) | NEEDS FIX (B13-02) |
| 家屋 | NEEDS FIX (B13-03) | CLEAN | CLEAN |
| 関わる | CLEAN | NEEDS FIX (B13-05) | NEEDS FIX (B13-04) |
| 書留 | CLEAN | CLEAN | CLEAN |
| 書き取り | CLEAN | CLEAN | CLEAN |
| 垣根 | CLEAN | CLEAN | CLEAN |
| 掻く | CLEAN | CLEAN | CLEAN |
| 嗅ぐ | CLEAN | CLEAN | CLEAN |
| 架空 | CLEAN | CLEAN | CLEAN |

**Related changes:** all five are CLEAN on all three facets. Every link target exists, and the 根 reciprocal example uses the actual reading かきね. 根 is the only N2 kanji with a card among this batch's kanji; 垣, 概, 掻, 嗅, 架 and 却 have no cards.

**Reuse claim:** CLEAN on all three facets. 替える.md:34-37 explicitly teaches 代える (かえる) as substituting a person or player, as a spelling tendency. The linked kaeru article adds the example 投手を代える.

**Mappings:**
- Correctness: CLEAN.
- Comprehensibility: CLEAN.
- Scoped coverage: NEEDS FIX for N2:253 only (via B13-02); the other rows are CLEAN.

The alternate spellings 却って, 係わる and 書取 are each taught explicitly. The 拘る-only sense and the かくう-only reading restriction are both stated correctly.

## Findings
**B13-01 (Minor; correctness)**
- **Where:** 帰す.md:21, "This reading is かえす, not きす."
- **Problem:** A separate literary verb 帰す (きす), a form of 帰する, does exist (e.g. 無に帰す, 水泡に帰す). Learners who meet it in N2 reading would be told it is an error.
- **Fix:** "For this send-home verb, read かえす; literary 帰す (きす) = 帰する, as in 水泡に帰す, is a different word."
- **Evidence:** Jisho (from JMdict) lists 帰す (きす) as "to come to (in the end); to end in", with 努力はすべて無に帰した.
- **Confidence:** high.

**B13-02 (Minor; scoped coverage and comprehensibility)**
- **Where:** 返る.md:4, 12, 23.
- **Problem:** The title promises "turn over", and N2:253 depends on 反る (かえる) for that sense. The article only names the sense abstractly, with no example sentence or compound.
- **Fix:** Add one attested example, such as 裾が返る or 軍配が返る. Alternatively, note that this sense usually appears in 裏返る and ひっくり返る.
- **Evidence:**
  - JMdict 1512150 sense 2, "to turn over", has no spelling restriction.
  - Daijisen (via Weblio) gives 「裾が―・る」 and 「軍配が―・る」 for this sense.
- **Confidence:** medium.

**B13-03 (Minor; quiz metadata)**
- **Where:** 家屋.md:4, 9 and 住宅.md:4, 9.
- **Problem:** "house; building" (家屋) and "housing; residence" (住宅) can each be accepted as the answer to the other word, but neither card excludes the other. 住宅 already excludes 家 ("house, home") for the same reason.
- **Fix:** Add 住宅 to 家屋's `quiz_exclusions`.
- **Confidence:** medium.

**B13-04 (Minor; comprehensibility)**
- **Where:** 関わる.md:19.
- **Problem:** 命に関わる is translated "a matter affecting someone's life", which reads like a change of lifestyle rather than a threat to life.
- **Fix:** "This is a life-or-death matter."
- **Confidence:** medium.

**B13-05 (Minor; links)**
- **Where:** 関わる.md:29.
- **Problem:** The 参加する comparison is plain text, although 参加.md exists and is already in this card's `quiz_exclusions`.
- **Fix:** Write it as [参加](参加.md)する.
- **Confidence:** high.

## Optional
- **帰す:19:** 客を帰す前に、お礼を言いました is a little unnatural; 客が帰る前に reads more naturally.
- **帰す and 送る:** "send home" vs "send; escort" could be read as overlapping; 送る has no comparison in 帰す.md. Low confidence.
- **解放:18:** 放す or 逃がす would be more idiomatic than 解放 for a bird.
- **開放:31:** the phrase "both are 'opening up'" is a stretch.
- **TSV N2:252:** typo "stagk".
- **根.md readings table:** could add 垣根 to the -ね row.

## Limits
- I had no Git access, so I couldn't verify hashes.
- I treated the author's inspection records (Nihongo Master, Kotobank, Japan Post) as claims, not as my own lookups. My own lookups were Jisho and Weblio. The Kotobank search and the goo dictionary fetches failed.
- The naturalness judgments are mine, not a native speaker's.
