# Batch 45 follow-up confirmation: the 成立/効力 guard is justified, and nothing actionable remains

The only change adds 効力 to 成立's quiz exclusions. The evidence supports it, it closes my one open issue (N1), and I found no regressions. Read-only; I used file tools only and did not run Git.

## Snapshot
- **Commit:** aa5c94c85e6be5b6a847b302945d24d2d9bf434e.
- **Parent:** the receipt gives 5911eeab48dd93455a75ee54cab7b86113ac1266, which is the first-correction commit I reviewed last turn.
- **Committed content only:** the receipt says "cleanCommittedContent: true".
- **Not reproduced:** the receipt lists `changedContentAndMappingFiles: [words/成立.md]`. Its hashes and its claim that every other file is unchanged come from the author's checks; I cannot reproduce them with file tools.

## Scope
- **Model:** claude-opus-5.5 (Claude family), resuming my own batch-45 review session.
- **Read in full this turn:**
  - the follow-up receipt and the one-line patch;
  - `words\成立.md` and `words\効力.md`;
  - the complete follow-up comparison rendering (JMdict 1275250).
- **Read in part this turn:**
  - `followupEvidence` and the 成立 declarations in the evidence file, lines 37825-37935;
  - 1375880 in the principal reading (line 41, all three senses);
  - the `quiz_exclusions` definition in `docs\content-format.md:67`.
- **Inherited, not reread this turn:**
  - the other nineteen new cards, including the five cards and 角 that I reread in full last turn;
  - the six kanji edits and the eight old-word edits;
  - the twenty source mappings.

## Verdicts

| Source | Article | Review basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:882 | 青少年 | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:883 | 整数 | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:884 | 清掃 | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:885 | 生存 | inherited (first confirmation) | CLEAN | CLEAN | CLEAN |
| N2:886 | 生長 | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:887 | 政党 | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:888 | 生年月日 | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:889 | 性能 | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:890 | 整備 | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:891 | 成分 | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:892 | 性別 | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:893 | 正方形 | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:894 | 正門 | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:895 | 成立 | **reassessed; full reread this turn** | CLEAN | CLEAN | CLEAN |
| N2:896 | 西暦 | inherited (first confirmation) | CLEAN | CLEAN | CLEAN |
| N2:897 | 背負う | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:898 | 赤道 | inherited (first confirmation) | CLEAN | CLEAN | CLEAN |
| N2:899 | せっかく | inherited (first confirmation) | CLEAN | CLEAN | CLEAN |
| N2:900 | 接近 | inherited (initial review) | CLEAN | CLEAN | CLEAN |
| N2:901 | 接する | inherited (first confirmation) | CLEAN | CLEAN | CLEAN |

**成立:** apart from the new 効力 exclusion on line 9, the body, title and metadata are identical to the version I reviewed last turn. The earlier correctness issue (N1) is resolved.

These three groups are inherited from last turn and were not reread here; the receipt asserts the files are unchanged:
- **Six kanji edits (角, 清, 掃, 党, 門, 接):** CLEAN / CLEAN / CLEAN. The reciprocal reading-row and Common words links, and the 接 small-っ note, were confirmed last turn.
- **Eight old-word edits (青年, 小数, 誕生日, 性, 四角, 四角い, 門, 成長):** CLEAN / CLEAN / CLEAN. The link lines were confirmed last turn; the 成長 comparison judgment comes from the initial review.
- **Twenty mappings, N2:882-N2:901:** CLEAN / CLEAN / CLEAN, from the initial review. The patch changes no mapping.

## Findings
**Earlier findings:**
- **F1** (せっかく exclusions for 苦心, 一生懸命, 機会 and チャンス): resolved at the first confirmation.
- **F2** (the 折角 horn-breaking account in せっかく and 角): resolved at the first confirmation.
- **F3** (西暦 period-word exclusions): resolved by the author's alternative remedy. I withdrew my "add 世紀" remedy last turn and keep that position.
- **F4** (赤道 links to 緯度 and 熱帯): resolved at the first confirmation.
- **F5** (生存 link to 死亡): resolved at the first confirmation.
- **The optional 接する ひざを接する example:** resolved at the first confirmation.
- **N1** (the 成立/効力 exclusion): **resolved** by this patch; details below.

**N1 detail:**
- **The overlap is real.**
  - 成立.md:4 is "formation; conclusion; validity", and 効力.md:4 is "efficacy; validity; potency". Both contain "validity" with no qualifier.
  - JMdict 1375880:3 is "being valid (of a theory, argument, etc.)", and 1275250:1 is "effect; efficacy; validity; potency".
  - A learner can't tell the two titles apart by the shared word.
- **The guard was needed explicitly.** Both cards already exclude 有効, but exclusions do not chain from one pair to another, so that does not keep 成立 and 効力 apart.
- **One declaration is enough.** The docs (content-format.md:67) say listed words "must not appear together as quiz choices", so a declaration on 成立 alone covers both cards. Repeating it on 効力 is not required.
- **The declaration is valid.** 効力 is an existing exact word ID, it is not repeated or self-referencing, and neither card has a `quiz_distractors` list it could conflict with.
- **It is not over-broad.** It removes one distractor pair whose labels genuinely overlap. It does not claim the two words can be swapped in Japanese: legal force versus an argument holding are still distinct.

**New consequential regressions:** none.

## Optional
None new. I accept the author's decision not to change 接's "deal with" gloss: it is accurate and is not a word-quiz title. My earlier optional items remain nonblocking and unadopted.

## Limits
- I did not run Git. The commit, the parent and the claim that no other file changed come from the author's receipt and patch.
- I did not fetch any web pages.
- I did not reread the nineteen inherited cards, the kanji and old-word files, or the TSV mappings this turn.
- My check for overlapping English titles last turn searched `title:` lines only, so overlaps in other wording could be missed.
- The 141-body, 217-label and 352-family/900-sense totals count the author's inspection, not mine.
- CLEAN is not certification by a native speaker or of the app's runtime behaviour.
