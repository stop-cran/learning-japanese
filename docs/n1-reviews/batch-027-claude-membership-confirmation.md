I withdraw the open N1 membership limit from my original report: 鳩 is in the frozen N1 list. Teaching verdicts, findings and optional items are unchanged.

**Snapshot:** same frozen commit `9030d709018268d80be335165f0ff70c1de60d2e`. You said the teaching diff is empty; I didn't run git, so I took that as given.

**Scope:** Claude Opus 5.5 (`claude-opus-5.5`), same session. I read these in full, one call at a time:
- `docs\n1-reviews\batch-027-initial-claude.md` (my original report).
- `docs\n1-sources\community-list-20261102.json` (the frozen list, one line).
- `docs\n1-source-snapshot.json` lines 1–105.

I answered only the membership question; this is not a new teaching review.

**Verdicts:** The only change is that 鳩's N1 label is now confirmed against the named source. All six verdicts stay CLEAN:
- `kanji\鳩.md`: correctness, scoped coverage and comprehensibility CLEAN.
- `words\鳩.md`: correctness, scoped coverage and comprehensibility CLEAN.

**Findings/disposition:**
- **Membership:** 鳩 appears exactly once in the frozen list, between "鯨" and "鳳" (`..."鯨","鳩","鳳"...`).
- **Source:** The snapshot gives `communitySource` as `https://kanjiapi.dev/v1/kanji/jlpt-1`, retrieved 2026-11-02, with 1,232 members.
- **Withdrawn limit:** My original limit said membership was unconfirmed and that the label rested on the old KANJIDIC2 `jlpt` 1. That is withdrawn.
  - The earlier search ran against the summary snapshot, which has no character inventory. Not finding 鳩 there never showed it was absent.
  - The snapshot also says old JLPT labels "are not transported into teaching metadata". The card's `jlpt: 1` therefore rests on the kanjiapi.dev N1 list, not on KANJIDIC.
- **Other findings:** none, as before.

**Optional:** unchanged, items 1–4 from the original report.

**Limits:**
- **File identity:** The snapshot hashes an input called `n1-kanji-source-20261102.json` (7,393 bytes, SHA-256 `889faaef…`). The file I read is `community-list-20261102.json`. I can't compute hashes or byte counts, so I haven't confirmed the two files are byte-identical. I also didn't count the list to check it really has 1,232 entries. The hash and the coordinator's mechanical audit are your assertions, not my own check.
- **No fresh download:** I didn't fetch kanjiapi.dev again, so this confirms membership in the frozen copy only.
- **Carried over from the original report:**
  - Twice in the first review I issued two reads in one response, against the one-call rule.
  - I searched `confusable-words.md` only for bird terms rather than reading it all.
  - I checked only the default four-choice kanji quiz.
  - The JMdict and KANJIDIC2 packets were supplied copies, and I fetched only the Kotobank 鳩 and 鳩首 pages myself.
  - Phone, native font, Android, combined-main, CI and public-ZIP checks are still outstanding.
