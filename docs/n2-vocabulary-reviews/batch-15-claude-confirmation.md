## Snapshot
I reviewed corrected commit `3491d8cb71d19115fcbfe8450b10097cac434110`, whose parent is `88300af9b018b8735962595c837167bcad9e03bf`. Both hashes come from the author's receipt; I had no Git, so I could not confirm them or recompute any hashes.
- The changed sections of the files on disk match the patch where I compared them.
- The manifest entries for 片寄る, 貸家 and 過剰 match the receipt hashes. That only shows the two author-produced records agree; it doesn't prove the files are correct.
- The patch does not include `manifest.json`, so I could not confirm it was regenerated.

## Scope
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), working alone and read-only.
- **Read in full:** my original report, the receipt, the patch, all eleven changed articles and the eleven comparison cards (済む, 落ち着く, 済ませる, 具体, 位置, 家屋, 住宅, 宅, 建物, 出す, 不足).
- **Packet (`batch-15.json`):**
  - I read the dictionary records for 済む (1295070), 貸家 (1411170), 片仮名 (1511600), 片寄る (1590420), 固まる (1266550), 片付く (1511770), 個所 (1590250) and 塊 (1590410).
  - I read both new sections in full (lines 19687–20790).
  - A count check found 21 matches: the 10 new dictionary records plus 11 references to them. None of the ten duplicates an entry already in the packet.
- **Also checked:** the readings on the 貸 kanji card.

## Verdicts
**All eleven articles: correctness CLEAN, scoped coverage CLEAN, comprehensibility CLEAN.**

| Article | What I checked |
|---|---|
| 固まる (`:9`, `:37`) | The firm-plan sense (dictionary sense 2) overlaps 済む's "be settled" and 落ち着く's settled-arrangement sense (sense 4). Both new exclusions are justified. |
| 片付く (`:9`, `:36`) | 落ち着く overlaps on "settle". 済ませる's "finish" (senses 1 and 3) is not marked for transitivity in English. The article still says 片付く is intransitive (`:16`) and that 片付ける is its transitive partner (`:28`). |
| 塊 (`:9`, `:36`) | The article teaches the "embodiment" sense (sense 3), which matches 具体's title. The original example 人が塊になって is unchanged. |
| 個所 (`:9`, `:35`) | Shares "place" with 位置 (sense 1). |
| 貸家 (`:9`, `:25`, `:33`) | 家屋, 住宅, 宅 (sense 1, house/home) and 建物 are all broader correct answers for "house for rent". 家屋 already excludes the other three, so this is a consistent group. The new 家 reading wording follows the かしいえ spelling restriction. |
| 貸し出し (`:25`, `:35`), 過剰 (`:29`, `:35`) | The new 出す and 不足 links point to existing cards, and the comparison citations were added. |
| 片仮名 (`:15`, `:32`) | Clear, with no dictionary jargon. "Usually written in kana" is backed by the dictionary's usually-kana note. |
| 片寄る (`:18`, `:20`, `:26`, `:34`) | The examples are natural and no claims about frequency or a strict spelling split were added. With no spelling restriction on any sense, both spellings can cover every sense. |
| 傾く (`:21`) | 賛成に傾く is a natural collocation, and the translation no longer adds a proposal. |
| 課税 (`:33`) | The roles are stated correctly. |

**Packet additions: CLEAN, CLEAN, CLEAN.**
- The new records are complete, keep the spelling and sense qualifications, and list the senses each card cites.
- Each pair or link cites the correct entry and senses, and the stated limits are accurate.

## Findings
- **B15-01 (貸家 reading and jargon): resolved.** Line 25 now separates や in かしや from いえ in かしいえ, and line 33 is in plain language.
- **B15-02 (偏る frequency): resolved, with my frequency remedy withdrawn.**
  - Learners can now recognise 偏る: line 20 uses 偏った見方, and line 34 says to recognise both spellings.
  - My evidence was dictionary headword order and priority tags, which do not measure frequency. The claim is unproven, not established.
- **B15-03 (片仮名): resolved.**
- **B15-04 (個所/位置): resolved.**
- **B15-05 (片付く/落ち着く): resolved.** The added 済ませる exclusion is also correct.
- **B15-06 (貸家/家屋, and 住宅 as suggested): resolved.** The added 宅 and 建物 exclusions are justified for the same reason.
- **Earlier optional suggestions:** the 傾く, 片寄る:18, 課税:33 and 片寄る:26 suggestions are resolved. The 箇所 note and ひとかたまり remain optional. The weak overlaps I noted need no action.

**I found no regressions and no actionable defects.**

## Optional
- **片寄る:18–20:** the examples now show 片寄る for physical imbalance and 偏る for bias, which hints at the split that line 26 rules out. Noting that 片寄った見方 is also possible would show this.
- **貸家:25:** "neither reading is カ + カ" is odd, because 貸's on reading is タイ. This wording was there before the correction.
- **Still optional:** the 箇所 note and ひとかたまり.

## Limits
- I could not run Git, compute hashes or check that the manifest was regenerated.
- I did not re-fetch the dictionary sources; the new records were compared against the cards.
- I did not mechanically check that the JSON is valid, and I did not run the validator or the app.
- I did not re-scan for other unprotected housing, place or "settled" titles.
- Naturalness was not checked by a native speaker.
