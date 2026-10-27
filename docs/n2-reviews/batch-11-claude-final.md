## Snapshot
c81161be3a918430076da745d079fca534a520e8, committed files only; the previous reviewed snapshot was d47b7bcdf38197653989bf160bb744bd70b8fd51. I had file tools only, no Git. The seven-file commit, the zero validator errors and the deterministic manifest are the author's claims; I did not check them independently. The single added line in the diff matches the current words\極める.md:8.

## Scope
- **Model:** claude-opus-5.5 (claude family). Worked sequentially; no edits and no delegation.
- **Read:**
  - my follow-up report, docs\n2-reviews\batch-11-claude-followup.md;
  - the complete diff in n2-batch-11-final-correction.diff (one hunk, one changed line);
  - words\極める.md and words\選ぶ.md in full;
  - JMdict entry 1254180 in batch-11.json, lines 2546-2730: sense 1, the per-sense restriction fields, the entry spellings and spelling info, and the reading details.
- **Applied from earlier in this session:** the content-format.md:84-96 exclusion rules and the app's prompt and label behaviour.
- **Not read:** the other committed files (preserved reports, contributor documentation, manifest), unchanged batch pages, unrelated candidate pairs, and the other family's report and the ledgers.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| words\極める.md | CLEAN | CLEAN | CLEAN |

## Findings
**The 極める/選ぶ pair is a justified direct exclusion.**
- **Where the ambiguity arises:** the Japanese-to-English quiz shows the written form 極める without a reading.
  - JMdict 1254180 lists 極める as an unflagged spelling (batch-11.json:2709-2715).
  - Its reading きめる has no spelling restriction and is not kana-only.
  - Sense 1 has empty spelling and reading restrictions, and its glosses include "to choose".
  - So "choose", 選ぶ's title (選ぶ.md:4), is a directly valid answer for the written 極める. One applicable gloss is enough, even among eleven.
- **The other presentations are not ambiguous:**
  - In English-to-Japanese, options show the reading (極める (きわめる), 選ぶ (えらぶ)).
  - A 選ぶ prompt in Japanese-to-English never makes "reach an extreme; take to the limit" correct.
  - Because exclusions are symmetric, those presentations only lose distractors that were never ambiguous, which is harmless.
- **Withdrawn claim:** my follow-up called this pair "borderline" because the app teaches only "decide; settle" for きめる. That framing was too weak and is withdrawn. Confidence: high.

**No regression found.**
- **Valid reference:** words\選ぶ.md exists with `word: 選ぶ`.
- **Article unchanged:** the page's teaching identity is intact. The title, reading, tags and prose are unchanged, and the article still teaches きわめる and separates きめる (lines 46-48).
- **Pairwise only:** the new exclusion is not transitive. It does not imply 決める/選ぶ, which is out of scope.
- **Pool size:** removing one candidate leaves the large score-7 candidate pool unaffected.

## Optional
None.

## Limits
- I did not verify the Git contents, the validator result or the manifest myself.
- How exclusion-aware app versions behave is taken from content-format.md, not from app code.
- batch-11.json is selected evidence, not the full JMdict.
- No native-speaker or linguistic certification.
