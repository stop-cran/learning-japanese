**Snapshot:** `027e5581f5b99523ae5f819d830673c8958560f6`, based on `6121ea9e6593497b4a93fb1e9597868bc92a5e6e`; no uncommitted changes identified in the packet. **Three consequential findings:** two missing direct meaning-quiz exclusions and one dictionary sense narrowed too far. The scoped counts and reciprocal links reconcile.

**Scope:** One blind reviewer, GPT-6.2 Sol (`gpt-6.2-sol`). Read all 10 new kanji cards, all 8 new word cards, both reused word cards, and all 9 older-card diffs in full. The diff includes the full `子` article; the other six older kanji were reviewed only in the supplied hunks. Read `sources.json`, all 10 primary XML entries, all 81 supplied JMdict family records, `quiz.txt`, and `labels.txt`.

**Verdicts:** Correctness includes static consistency and quiz safety. Comprehensibility covers the reading and meaning distinctions in this assignment, not a separate teaching-style review.

| Card(s) | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| Kanji `媒`, `媛` | NEEDS FIX | CLEAN | CLEAN |
| Kanji `嫡`; older kanji `子` | NEEDS FIX | CLEAN | CLEAN |
| Kanji `姫`, `姻`, `娠`, `婆`, `婿`, `孔`, `孤` | CLEAN | CLEAN | CLEAN |
| Word `嫡子` | NEEDS FIX | NEEDS FIX | CLEAN |
| Words `姫`, `婚姻`, `妊娠`, `婿`, `媒体`, `才媛`, `孤独` | CLEAN | CLEAN | CLEAN |
| Reused words `おばあさん`, `穴` | CLEAN | CLEAN | CLEAN |
| Older kanji `体`, `妊`, `婚`, `才`, `独`, `瞳` — changed passages only | CLEAN | CLEAN | CLEAN |

**Findings**

1. **Medium · Meaning-quiz safety · `kanji/媒.md:3,14`.** Both `媒` and `旋` display the unqualified gloss **“mediate.”** Both exclude `介`, but neither excludes the other; exclusions are not transitive. Add `旋` to `媒`’s `quiz_exclusions`, preserving the existing entries, and update the pair audit. Evidence: `labels.txt:19,28` and `quiz.txt`. **High confidence** in the label collision; live co-occurrence was not verified.
2. **Medium · Meaning-quiz safety · `kanji/媛.md:3,14`.** The broad **“lady”** gloss overlaps directly with `嬢`’s **“young lady.”** The existing exclusions for `女` and `婦` do not cover that pair. Add `嬢` to `媛`’s `quiz_exclusions` and update the pair audit. This does not imply a `姫`–`嬢` exclusion: `姫`’s displayed gloss specifies noble birth. Evidence: `labels.txt:20,23`. **Moderate confidence** in the ambiguity; live co-occurrence was not verified.
3. **Medium · Meaning and scoped coverage · `words/嫡子.md:4,11,15`; `kanji/嫡.md:31,36`; `kanji/子.md:53`.** The unqualified gloss **“child of the principal wife”** presents a historical rendering as the entire second sense. JMdict 1422910 gives **“legitimate child”** separately from **“heir.”** Use “heir to a house; legitimate child” in the word title and linked glosses. Keep the principal-wife example, but identify it as a historical interpretation rather than the general definition. Evidence: `primary.xml`, entry 1422910, senses 1–2. **High confidence** in the mismatch.

**Counts and navigation:** The 10 supplied source rows map to 10 distinct word articles: 8 new and 2 reused. The 9 older changes are 7 kanji and 2 words. All **16 declared reciprocal pairs** have both relative links and the correct full-word reading in the supplied text. `瞳 → 孔` is a separate kanji-to-kanji link. The existing `words/穴 → kanji/穴` link is visible; its unchanged reverse is outside the packet. All **20 metadata readings** appear in the new kanji reading tables, and all **10 offered keys** match the curated projection. The **30 preset meaning distractors** are distinguishable; the two findings concern undeclared pairs outside those presets. The recorded exclusions reconcile to **20 kanji pairs and 12 word pairs**. The reuse evidence distinguishes spelling priority from shared reading priority: neither `お婆さん` nor `孔` inherits the priority tags of `お祖母さん` or `穴`.

**Optional:** Mark `孔`’s `あな` and `婆`’s `ばば` as outside the standard-use table, consistent with the packet’s Kanjipedia records. Keep `あな` as a valid practice reading; standard-use status and quiz eligibility are different.

**Limits:** `quiz.txt` reports no reachable reading collisions in its tested pools and two latent, unreachable `孔` keys (`のり`, `はなはだ`). I checked the static evidence, not the runtime pools. The supplied citation scan, manifest/content version, archive budget, and upstream source membership were not independently reproduced. No external pages, native review, device behavior, or whole-deck acceptance were verified.
