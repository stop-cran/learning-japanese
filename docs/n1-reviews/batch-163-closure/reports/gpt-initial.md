**Two direct meaning-quiz exclusions are missing:** 奮–鼓 and 奔走–苦心. The packet supports both ambiguity findings, but does not show that either pair was presented in a live quiz.

**Snapshot:** `b89b7a459db5f06a35fd690a7a5f535a5fdeb4dd`; packet-reported content version `f53cb073d97a67b6`. One blind, read-only reviewer: GPT-6.2 Sol (`gpt-6.2-sol`). No edits made; commit and worktree provenance were not independently verified.

**Scope and counts:** Read 20 full cards: 10 new kanji, nine new words, and the reused `words/一.md`. Reviewed seven existing kanji at diff scope only, for eight changed existing articles including `一`. Checked all 10 source mappings against `primary.xml`, the 32 kanji reading rows against `sources.json` and the supplied dictionary evidence, and all 71 family records across the five JSONL files. The 10 curated kanji keys match the frontmatter and projection: eight on, two kun. All 17 required reciprocal pairs are present in both directions, with the correct whole-word readings. The 壱 link intentionally reuses 一 at いち, preserves its N5 identity, and does not inherit 一’s spelling-priority tags.

| Cards | Correctness¹ | Scoped coverage | Comprehensibility |
|---|---|---|---|
| Kanji: 壱、奈、奉、奔、奴、如、妃、妄、妊 | CLEAN | CLEAN | CLEAN |
| Kanji: 奮 | NEEDS FIX | CLEAN | CLEAN |
| Words: 奈良、奉仕、奮う、奴、欠如、王妃、妄想、妊婦、一 | CLEAN | CLEAN | CLEAN |
| Word: 奔走 | NEEDS FIX | CLEAN | CLEAN |
| Existing kanji, changed lines only: 仕、婦、想、欠、王、良、走 | CLEAN | CLEAN | CLEAN |

¹ Includes static quiz safety. Live quiz behavior is **UNVERIFIED**.

**Findings**

1. **Moderate · meaning quiz · `kanji/奮.md:3,14` · High confidence.** 奮 displays “rouse; summon one's energy”; 鼓 displays “drum; rouse.” Either choice can defend the unqualified “rouse” gloss. `labels.txt` shows that both exclude 励, but neither excludes the other; direct exclusions are not transitive. **Remedy:** add `鼓` to 奮’s `quiz_exclusions`.
2. **Moderate · meaning quiz · `words/奔走.md:4,8` · Medium confidence.** 苦心 displays “painstaking effort; taking pains,” a plausible answer for the effort half of 奔走’s “working hard to get things done; running about.” JMdict `1522100` explicitly includes “making every effort” and “efforts,” so the overlap is not limited to literal running. Both cards exclude 努力, but neither excludes the other. **Remedy:** add `苦心` to 奔走’s `quiz_exclusions`; retain the distinction between making arrangements and taking pains in the teaching text.

**Optional:** Cite JMdict `2138590` directly on `words/一.md` for the added 壱万円 example. The packet already supports the claim, and the linked 壱 card cites that entry.

**Limits:** The 30 listed kanji distractor slots showed no actionable ambiguity within their explicit sets. The label extract is partial, and the reading audit supplies a summary rather than candidate traces, so I could not reproduce its four reported latent collisions or verify either quiz’s live option selection. Navigation was checked in the supplied text, not in the app. Manifest, archive, and upstream source hashes were not independently verified. No external pages, native-speaker judgments, or device behavior were verified.
