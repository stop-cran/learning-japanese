## Snapshot
- **Frozen commit:** `c53e61946e7229fafbf9401901cfbebe48c2c19e`; parent `a5be09f25b54da66e35037028d4e171b726ec5fb`.
- `.git\HEAD` points to `refs/heads/jlpt-n2-vocabulary`, and that ref contains the frozen commit.
- **Limit:** I cannot run Git or recompute hashes. I reviewed the files on disk and assumed they match the committed content. The receipt's "hashes verified" statement is the author's claim, not my check.

## Scope
- **Model:** claude-opus-5.5 (claude family), a fresh process working through the batch in order, no delegation or file edits.
- **New articles:** I read all 15 in full: 納める, 治める, 惜しい, お辞儀, おしゃれ, おじゃまします, 教わる, おだいじに, 落ち着く, 御手洗, お出かけ, お手伝いさん, おどかす, 落とし物 and おとなしい.
- **Related edits:** I read the eight-file patch and the changed passages in context (I read 収める.md in full). I read the committed CW005 row. The CW005 diff itself is not in the patch, so I could only assess the row as it now stands.
- **Reuse claims:** I read おじさん.md, 一昨日.md and 一昨年.md in full.
- **Source evidence:**
  - TSV rows N2:182–201.
  - From batch-10.json: the source rows, the principal JMdict families, the relevant comparison families and the inspection receipts.
  - Quiz checks: a regex survey of titles and exclusions in `words\`.
  - My own Kotobank lookups for 収める, 治める and 御手洗.
- **Not covered:**
  - I did not recheck unchanged teaching in the related files.
  - I did not hash-check `n2-vocabulary-snapshot.json` or `n2-source-snapshot.json`.
  - I did not read any forbidden documents.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 納める | CLEAN | CLEAN | CLEAN |
| 治める | CLEAN | NEEDS FIX (B10-01) | CLEAN |
| 惜しい | CLEAN | CLEAN | CLEAN |
| お辞儀 | CLEAN | CLEAN | CLEAN |
| おしゃれ | CLEAN | CLEAN | CLEAN |
| おじゃまします | CLEAN | CLEAN | CLEAN |
| 教わる | CLEAN | CLEAN | CLEAN |
| おだいじに | CLEAN | CLEAN | CLEAN |
| 落ち着く | NEEDS FIX (B10-02) | CLEAN | CLEAN |
| 御手洗 | CLEAN | CLEAN | CLEAN |
| お出かけ | NEEDS FIX (B10-04) | CLEAN | CLEAN |
| お手伝いさん | NEEDS FIX (B10-05) | CLEAN | CLEAN |
| おどかす | CLEAN | CLEAN | CLEAN |
| 落とし物 | CLEAN | CLEAN | CLEAN |
| おとなしい | NEEDS FIX (B10-03) | CLEAN | CLEAN |

**Other items, all clean on all three facets:**
- **Eight related edits:**
  - 治.md: the reading-table and common-word links match.
  - 元気でね: the お大事に label points to おだいじに, which explicitly teaches お大事に.
  - 収める, 忘れ物, 教える, 礼 and 習う: the new links and the new 教わる bullet are accurate.
  - 手伝い: the new お手伝いさん line is accurate.
- **CW005:** adding 教わる fits the "who gives and who receives instruction" question. Only the committed row was assessed.
- **Five reuse claims:**
  - おじさん.md explicitly teaches 伯父さん (older uncle), 叔父さん (younger uncle) and 小父さん (unrelated man), matching JMdict senses 1 and 2.
  - 一昨日 teaches おととい, and 一昨年 teaches おととし.
- **Twenty mappings:** every source spelling is explicitly taught: 御辞儀, 落着く, お出掛け, 落し物, お洒落, お邪魔します, 脅かす and 大人しい. 御手洗 is correctly read みたらし with the shrine sense.
  - The problem source glosses are handled correctly:
    - 納める's "obtain/reap" belongs to 収める (sense 3).
    - おどかす's "coerce" is not in the JMdict senses.
    - "Middle-aged gentleman" is limited to 小父さん.

## Findings
**B10-01** — Minor; scoped coverage; `words\治める.md:35` (also lines 19 and 31; `words\落ち着く.md:39`)
- **Claim:** The spelling advice pairs 納める with taxes and 収める with achieving results, and gives 治める as the spelling for calming a disturbance. Its example is 二人の争いを治める. It never says that 収める is also a standard spelling for settling disputes. Learners told not to pick a spelling by sound alone may treat 争いを収める or 丸く収める as wrong. 落ち着く.md:39 likewise names only 治める.
- **Remedy:** Add one sentence such as "収める is also common for settling disputes or calming feelings (争いを収める, 丸く収める); 治める is distinctive for governing." Optionally mention 収める at 落ち着く.md:39 too.
- **Evidence:**
  - JMdict 1589090 sense 8 ("to subdue; to suppress; to settle") has no spelling restriction and cross-references 治める・2 (batch-10.json:1497–1515).
  - Digital Daijisen 【収める／納める】 sense 4 gives 「紛争を―・める」 and 「怒りを―・める」.
  - Digital Daijisen 【治める】 sense 1 says 「収める4」に同じ, with 「丸く―・める」.
- **Confidence:** high that the advice is incomplete; medium on how much it affects learners.

**B10-02** — Minor; correctness (quiz metadata); `words\落ち着く.md:4,9`; `words\冷静.md:4,33`
- **Claim:** 落ち着く ("calm down; settle") and 冷静 ("calm; composed") are not excluded from appearing together. A learner could reasonably accept either title for either word: 冷静.md:23 teaches 冷静になる as "regain composure," and 冷静.md:33 itself names the overlap with 落ち着く. The new card excludes weaker matches (静か, 安心) but not this one.
- **Remedy:** Add 冷静 to 落ち着く's quiz exclusions.
- **Confidence:** high.

**B10-03** — Minor; correctness (quiz); `words\おとなしい.md:4,9,21`; `words\利口.md:4,17`; `words\そっと.md:4`
- **Claim:** "well-behaved" appears in both おとなしい's title and 利口's title ("clever; sensible; well-behaved"). 利口.md:17 teaches the well-behaved child or pet meaning, the same use as おとなしい's dog example. In addition, そっと ("gently; quietly") overlaps with おとなしく待つ, "wait quietly" (line 21). Neither pair is excluded on either card.
- **Remedy:** Add 利口, and probably そっと.
- **Confidence:** high for 利口; medium for そっと.

**B10-04** — Minor; correctness (quiz); `words\お出かけ.md:4,9,16`; `words\遠足.md:4,16`
- **Claim:** "outing" appears in both お出かけ's title and 遠足's title ("school outing; field trip"). 遠足.md:16 defines it as "an outing or excursion," and JMdict 1338475 sense 2 makes お出かけ an outing. The card excludes 旅 and 旅行 on a weaker basis but not 遠足. デート ("date; romantic outing") is a weaker case of the same overlap.
- **Remedy:** Add 遠足, and consider デート.
- **Confidence:** medium.

**B10-05** — Minor; correctness (quiz); `words\お手伝いさん.md:4,9,24`; `words\助手.md:4,9`
- **Claim:** お手伝いさん ("maid; domestic helper") and 助手 ("assistant; helper") share "helper" and are not excluded. 助手 already excludes 手伝い because of that label. Line 24 itself warns that お手伝いさん is not a label for every assistant, which is exactly the confusion this pairing invites.
- **Remedy:** Add 助手.
- **Confidence:** medium-low.

## Optional
- **御手洗:**
  - Mention 手水舎 (ちょうずや/てみずや) as the usual modern name for the shrine basin.
  - Mention みたらし団子, the reading's most common everyday use; 精選版 sense ③ supports it.
  - Consider whether the type should be `jukujikun` rather than `wago`.
- **Weaker label overlaps worth a look:**
  - おどかす with ぎょっと or びっくり ("startle" vs "startled").
  - 教わる with 就く ("study under").
  - おだいじに with お見舞い ("get well").
  - おじゃまします with あの ("excuse me").
- **落ち着く:** its exclusion of 納める is a stretch (no shared title label). This only shrinks the distractor pool and is not a defect.
- **お出かけ.md:34:** the sentence "does not mean 'Are you outside already?' in every situation" reads oddly; consider rewording.
- **Links and inventory:** link 御.md to 御手洗 and お辞儀, and link 教.md to 教わる. Consider an おさめる spelling row (収める/納める/治める) in confusable-words.md.

## Limits
- I could not run Git. That the working tree matches the commit, and the receipt's hashes, are unverified.
- My Bunka-chō 異字同訓 lookup timed out, so B10-01 rests on JMdict and Digital Daijisen only.
- The author's Kotobank receipts for 御出掛, 御手伝いさん and 教わる are not my own lookups. I independently fetched only 御手洗, 収める and 治める.
- The CW005 diff was not visible.
- Unchanged teaching in the related files was not rechecked (for example, 収める.md's お収めください).
- The quiz-overlap survey used title regexes and may miss differently worded overlaps.
- Naturalness judgements are not native-speaker certified (for example, the おどかす threat example and the 御手洗 example's register).
