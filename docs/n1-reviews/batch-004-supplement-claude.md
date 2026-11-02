Reading お茶 changes none of my verdicts, and I have no new findings. This is a same-snapshot follow-up that only adds the one comparison I hadn't read. It does not check a changed passage, it is not a third independent initial report, and it is not native-speaker or phone evidence.

**Snapshot:** `bfea5052387e2327dac4e365ec11ccca1289b914`, committed teaching only. There have been no teaching changes since my initial report, so there was no diff to review. The evidence-only file `docs\n1-reviews\batch-004-input-metadata.json` is unchanged and was not reread.

**Scope:** Claude Opus 5.5, reading one file per step, in the same session as the initial review.
- **Newly read:** `words\お茶.md`, in full (lines 1–33).
- **Reread:** my own report, `docs\n1-reviews\batch-004-initial-claude.md`.
- **Not reread:** `words\川柳.md` and the JMdict packet lines 181–218. I connected the comparison using my complete first-pass reads of both from earlier in this session.
- **Assessed:** how お茶 bears on `words\川柳.md` across correctness, scoped coverage and comprehensibility. The 杉 review stays limited to the changed backlink; I did not widen it into a full audit.

**What I checked:**
- **Titles:** お茶 has the title "tea", the same as 茶. 川柳 has "senryu; humorous short verse". Neither title could reasonably be accepted as the answer for the other word.
- **The exclusion is declared directly:** `words\川柳.md` front matter line 7 lists both 茶 and お茶. So 川柳 and お茶 are kept apart by their own pair, not by inference from the 茶 exclusion.
- **The tea sense belongs to a different reading:**
  - JMdict 1811520 has a sense 3, "high-quality coarse tea", limited to the spelling 川柳 but under the reading かわやなぎ.
  - The せんりゅう entry (1390110) has no tea sense.
  - `words\川柳.md` already says this tea sense belongs to a separate dictionary entry and is not pronounced せんりゅう. お茶 doesn't contradict that.
- **Effect of the exclusion:** removing お茶 as a choice for 川柳 is cautious but harmless. It takes one candidate out of the choice pool; it doesn't make the quiz ambiguous or teach anything wrong. The app treats exclusions as pairs only, so this one has no knock-on effects.
- **お茶 content:** its explanation of the polite prefix and its contrast with 紅茶 don't touch anything 川柳 or the other assigned articles claim.

**Verdicts** (correctness / scoped coverage / comprehensibility), all unchanged from the initial report:
- `kanji\杉.md`: CLEAN / CLEAN / CLEAN
- `kanji\桐.md`: CLEAN / CLEAN / CLEAN
- `kanji\柳.md`: CLEAN / CLEAN / CLEAN
- `words\桐.md`: CLEAN / CLEAN / CLEAN
- `words\柳.md`: CLEAN / CLEAN / CLEAN
- `words\川柳.md`: CLEAN / CLEAN / CLEAN. Reading お茶 confirms the direct exclusion and finds no defect.
- `words\杉.md` (changed passage only, line 23): CLEAN / CLEAN / CLEAN

**Findings:** none new.

**Optional:** the same three suggestions as before, unchanged.
- `kanji\柳.md:42`: "印 … has a simpler left side" is vague. "印 lacks 木; it resembles only the 卯-like right part" would be clearer.
- `words\杉.md:9` (unchanged, reused): 杉 excludes only 木, while 桐 and 柳 also exclude 植物 and 植える. Adding those two would make the tree set consistent.
- `kanji\桐.md` and `words\桐.md`: JMdict 1586170 marks 梧桐/あおぎり as usually written in kana. The articles could say so.

**Limits:**
- All initial read limits still stand. I still haven't read 材木, 木材, 材料, 植木 or the Kotobank 柳 page, and three Kotobank pages were cut off by length.
- The JMdict and KANJIDIC2 evidence is the frozen packets I was given, not my own live retrieval.
- I didn't reread 川柳.md or packet lines 181–218 in this follow-up.
- I didn't re-certify the unchanged 杉 text or the unchanged comparison articles, お茶 included, beyond how they bear on the batch.
- This is a textual review only. It does not certify how the app actually builds questions or handles reading keys, real phone display, native-speaker judgement, or learning effectiveness.
