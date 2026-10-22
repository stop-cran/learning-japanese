## Snapshot
Corrected commit `1b89f7a33464626af211a75bf51529df8ae45edc`; original frozen snapshot `71dd9a70dcda63c2a0619f79eae8fbfcfcfb897a`; baseline before the batch `8df545e4faeca74bd0e27e08e5d03123e4d5065a`. Committed files only. I ran no Git, validator, audit or manifest commands. The commit identity, clean worktree, eight-file scope, zero validator errors, 733-row audit and manifest `37863624e7d74dfb` are the author's checks, which I did not reproduce.

## Scope
- **Reviewer:** claude-opus-5.5 (Claude family), one sequential reviewer; no edits, commands or delegation.
- **Read:**
  - my own `docs\n2-reviews\batch-16-claude-initial.md`;
  - the full two-page patch `n2-batch-16-fix.patch`, which changes only `kanji\祭.md:11` and `kanji\筆.md:41`;
  - `kanji\祭.md` and `kanji\筆.md` in full.
- **Also inspected:** `kanji\禁.md` (full), `kanji\察.md:1-20`, `kanji\際.md` (full), `kanji\登.md:1-12`, `docs\content-format.md:30-50`, and the 祭 and 禁 KANJIDIC records in `batch-16.json:46-77`. I also used JMdict 1526360 in `batch-16.json:3863-3929`, which I read in full earlier in this session, and `words\万年筆.md:31`.
- **Public pages fetched:** Oxford Learner's Dictionaries entries for "observe" and "occasion".
- **Not read:** forbidden ledgers and other reviewers' reports.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\祭.md | CLEAN | CLEAN | CLEAN |
| kanji\筆.md | CLEAN | CLEAN | CLEAN |

## Findings
My original report had no findings, so only the optional items and the author's 察 change need a disposition.

- **祭 distractor 察 → 禁 (`kanji\祭.md:11`): resolved.** My original review did not raise this.
  - I confirmed the evidence myself. Oxford's "observe" sense 5 reads "to celebrate festivals, birthdays, etc." 祭's pinned KANJIDIC meanings include "celebrate" and "ritual". So the label "observe; infer" (察) carried a real, if low, English-label ambiguity. My original CLEAN overlooked it, and I accept the correction.
  - The replacement is safe. 禁 is labelled "prohibit; ban", and its pinned meanings are "prohibition, ban, forbid". None of these overlap 祭's meanings, and I found no English homograph. 禁 is an existing card, not 祭 itself, and it shares the 示 key (no. 113) with 祭, so it still makes a useful visual contrast.
  - No stale mention of 察 remains in 祭.md, and nothing else on the page changed.
- **Original O1 (`kanji\筆.md:41`): resolved.**
  - The new note limits the ヒツ comparison to the 万年筆 article's まんねんひつ reading and adds that JMdict also records まんねんぴつ and まんねんふで.
  - That matches JMdict 1526360: all three readings are listed, none has a spelling restriction, and none is marked kana-only.
  - The note makes no frequency claim, and it is now consistent with `words\万年筆.md:31` ("This card teaches the reading まんねんひつ").
- **Original O2 (counter for land plots): still optional, not adopted.** I accept the author's reason: this is a focused brush-and-writing page.
- **Original O3 (算 history): still optional, not adopted.** It is outside this correction scope.
- **Regressions:** none found.

## Optional
- **祭's remaining distractor 際 ("edge; occasion"), unchanged and not a regression.** Oxford's "occasion" sense 2 is "a special event, ceremony or celebration". A festival is an occasion in that sense, but no pinned 祭 meaning is a synonym of "occasion". "Edge" and 際's "on that occasion" sense also point away from festival. I therefore rate this weaker than the observe case and do not treat it as a defect. Keeping 際 also preserves a useful comparison: it shares the reading サイ and contains 祭's shape.

## Limits
- This was a bounded review of the changed passages, not a new full-batch review.
- I ran no Git or validator commands, so the snapshot identity and the eight-file scope are not independently verified.
- I did not review stroke paths and did not test the quiz in the app; the quiz assessment comes from titles plus `docs\content-format.md:41-47`.
- This is not native-fluency certification, and I made no frequency judgment about まんねんぴつ or まんねんふで.
