# Batch 095: dependent rendered confirmation report

**Result:** I found no proved defects. 剖.md, 解剖.md and the added 解.md:39 stay CLEAN, and the bounded rendered/quiz scope is CLEAN. I'm adding one new low-severity hypothesis about the 解.md citation line, and I broke the one-call-per-response rule once.

## Snapshot
- Content HEAD: 86966dc49fb3a22014aea0dac2b568bc7045e56d.
- Native full archive: cc748347.
- Teaching content: 8c4e1650, unchanged. Content version: 463619d79972e9f2.
- The SHA256 hashes for 剖.md, 解剖.md and 解.md match my initial review.

## Scope
- **Model and session:** Claude Opus 5.5 (claude-opus-5.5), session ede78c28-e889-47b5-be0b-21533da61551. This is a dependent check, not a blind review.
- **Text read:** all 14 packet chunks, in order. Each was read whole with no line ranges; chunks 04–14 needed forceReadLargeFiles because they exceed 20 KB on disk. That covers my original report, the native receipt, all three articles, all 37 JMdict families, the public source text, the quiz contract, all 64 kanji-choice records, all 384 guard records, and the sheet bindings.
- **Images decoded:** all 4 font panels and all 14 contact sheets, which bind the 56 remaining PNGs. I didn't need any original full-size PNG; the reduced sheets were legible for every claim below.
- **Rule broken:** I viewed font panels 1 and 2 in a single response, which breaks the "exactly one view call per response" rule. Both images were fully decoded. Every other read was one call per response, in order.

## Verdicts
Each cell gives correctness / scoped coverage / comprehensibility.

| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 剖.md | CLEAN | CLEAN | CLEAN |
| 解剖.md | CLEAN | CLEAN | CLEAN |
| 解.md:39 (added passage) | CLEAN | CLEAN, see hypothesis H1 | CLEAN |
| Bounded rendered/quiz scope | CLEAN | CLEAN | CLEAN |

What the bounded rendered/quiz scope covers:
- **Glyphs:** 剖, 部, 倍 and 副 are clearly distinct in all four fonts. The standalone 亻, 刂 and 阝 use the same system fallback glyph in every font, but stay legible.
- **Reading quiz:** ボウ is the only correct answer and there is no kun question.
- **Meaning quiz:** the wrong options 冒 "brave danger; venture", 刈 "mow; reap" and 企 "plan; undertake" don't overlap with "dissect; split open". 刈 is a cutting action, but harvesting rather than opening something up.
- **Other N1 fallback options across the 64 kanji-choice records:** the closest neighbours are 削 "shave; sharpen; pare" and 刃 "blade". Neither is a defensible answer.
- **Word guards:** none of the 384 records shows a duplicate defensible answer. 診察 and 調査 never appear as options for 解剖.
- **Navigation and other screens:** both reciprocal pairs (剖/解剖 and 解/解剖), all four directions, and System Back all work. Both reading tables were captured scrolled left and right. Selection, drawing trace and recall are present.

## Findings
**Proved defects:** none.

**New hypothesis H1** (raised now; I did not flag it in the initial review)
- **Severity / facet:** Low; provenance and scoped coverage.
- **Location:** 解.md:50, the article's last line ("Vocabulary: JMdict, entries 1549910, 1198890, 1271310").
- **Claim:** 解.md:39 adds 解剖 to Common words, but this line doesn't cite 解剖's JMdict entry 1199270.
- **Impact:** minor. The 解剖 article carries its own provenance.
- **Possible fix:** add 1199270 to that line, if the format convention requires each listed word to be cited.
- **Evidence:** sheets 05–07 for the 解 article; sheets 09–10 for 解剖's provenance.
- **Confidence:** low that this is a defect, because the supplied material includes no rule requiring it.

## Reconciliation of my original items
- **Hypothesis: 診察/調査 overlap with 解剖.** Resolved within the bounded records, since neither appears as an option for 解剖. 調査 does appear among 分析's options, but that is a baseline pairing outside this batch. The 臨床診察 and 調査 distinctions are bounded by the sources, not unrestricted guarantees.
- **Hypothesis: clash with a 解体 card.** Withdrawn, because no 解体 card exists.
- **Optional (a)** and **optional (b)** remain optional.
- **Optional (c)** remains optional and is visible on screen: 剖's Common words gloss "analysis" while 解's says "figurative analysis".

## Optional
- (a) 剖.md:22, "to examine it", is slightly broader than the character-level sources.
- (b) Add 剖検 ぼうけん as a recognition-only ボウ example.
- (c) Make the 解剖 gloss wording consistent across the articles.
- In 解剖's 分析 note, 解剖 breaks across a line on screen. This is normal CJK line breaking.
- Out of scope: in 解's reading table, the unchanged "misunderstanding" cell breaks mid-word.

## Limits
- I didn't independently check Git or upstream sources, and I ran no native tests. The native evidence is the coordinator's receipt from an API 35 emulator. It used a test-only Android build (1c1b7bf4) that retains production f9b59a2 and is not the latest app main.
- I reviewed the contact sheets at reduced scale. Font hashes or hasGlyph checks don't prove legibility.
- The 10 injected reference strokes and the give-up recall/persistence don't certify human handwriting or MLKit recognition.
- The 384 guard records prove only the three specific guards: 解剖/分析, 解剖/分解 and 解剖/検査. They don't prove every other option is semantically safe.
- This makes no claim about a physical phone, a general release, the whole set, publication, or measured learning effect.
