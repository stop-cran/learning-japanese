## Snapshot
- **Commit:** `2ca51500880851eae1d5cd3e6eef9ff7165d1329`, parent `fe744d204feaeb554fce6df934cfafed81419be5`, taken from the revised receipt (`cleanCommittedContent: true`). I reviewed committed content only.
- **Git limit:** I have file tools only and cannot run Git. I could not confirm the commit identity, the clean state, the file hashes or the diff hash. I did confirm by reading that the working-tree files contain every added line of the supplied patch.

## Scope
- **Model and method:** claude-opus-5.5 (Claude family), working alone and in sequence, with no edits.
- **Changed passages checked:** all eight quiz exclusions (line 9 of each file), the 相 link (`あいかわらず.md:27`), the 示す link (`挙げる.md:35`) and the two rewritten warnings in `飽くまで.md` (lines 29–30 and 41–42). I read each file in full for context.
- **Comparison cards read:** いつも, 普段, うんざり, 示す, 収める, 得る, 味, 疑わしい and やはり, plus `kanji\相.md`. I also checked the titles of たいてい, 普通, やっぱり and まだ.
- **Evidence read:** the `batch-01.json` reviewEvidence section and the JMdict entries for あいかわらず (1401310), あきれる (1515580), 飽くまで (1518320), 味わう (1527010), 曖昧 (1567920) and 挙げる (2864818). I also fetched the Kotobank 曖昧 page (Nihon Kokugo Daijiten).
- **Prior findings:** I rechecked my own F1–F3 and the related optional items.
- **Not done:** no full rereview of the unchanged pilot, and none of the prohibited documents or reports were read.

## Verdicts
These cover only the changed passages.

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| あいかわらず | CLEAN | CLEAN | CLEAN |
| あきれる | CLEAN | CLEAN | CLEAN |
| 曖昧 | CLEAN | CLEAN | CLEAN |
| 挙げる | CLEAN | CLEAN | CLEAN |
| 味わう | CLEAN | CLEAN | CLEAN |
| 飽くまで | CLEAN | CLEAN | CLEAN |

## Findings
**My original findings**
- **F1, あきれる and うんざり: resolved.** `あきれる.md:9` now excludes うんざり. The article teaches "fed up" at lines 16 and 21. JMdict 1515580 sense 1 includes "to be fed up", and うんざり's quiz title is "fed up; weary of something".
- **F2, あいかわらず and いつも: resolved.** `あいかわらず.md:9` now excludes いつも. JMdict glosses あいかわらず as "as usual; as always"; いつも's title is "always; usually" (JMdict 1188890: sense 1 "always", sense 3 "usual").
  - The added 普段 exclusion is a direct pair, not a transitive one. JMdict 1497180 glosses 普段 as "usual" (sense 1) and "usually… always" (sense 2), against the title "as usual; as before".
- **F3, 飽くまで wording: resolved.**
  - Lines 41–42 now warn about the right thing: あくまで is not a substitute for やはり ("as expected"). Calling JMdict's "after all" gloss part of "the limiting sense" is accurate (sense 2: "after all; it must be remembered; only; purely; simply").
  - Lines 29–30 no longer suggest that some uses mean "until bored". The wording is clumsy (see Optional).
- **Optional 相 link: resolved.** The link at line 27 is valid, and the 相 kanji card teaches the あい- reading.

**New exclusions, checked independently**
Each one is supported by the displayed quiz titles and an ordinary sense, not by a transitive or shared-topic inference.
- **曖昧 / 疑わしい:** the Nihon Kokugo Daijiten entry gives sense ③ as 「怪しげな、疑わしいさま」 ("suspicious-seeming, doubtful"). Sense ② also gives 「確かでないさま」 ("not certain"). The card teaches the separate shady sense at lines 37–39. JMdict sense 2 ("shady; disreputable") supports this more weakly. Confidence: medium-high.
- **挙げる / 示す:** JMdict 2864818 sense 1 includes "to show; to display". The 示す card teaches 例を示す ("present an example"). Confidence: high.
- **挙げる / 収める and 挙げる / 得る:** sense 11 is "to earn… to achieve… to obtain". The article teaches it at line 24 with 成果を挙げる ("achieve results") and cites it. 収める's title is "put away; achieve", and 得る's is "obtain; gain". Confidence: high.
- **味わう / 味:** JMdict 1527010 sense 1 is "to taste", and 味's title is "taste, flavor". The two words also share a kanji, which makes 味 a likely automatic quiz choice. Confidence: high.

**Minimality and regressions**
- No titles, readings, levels or kanji metadata changed.
- All eight exclusion targets exist under their exact word IDs.
- No card declares the reverse of a new pair.
- No card lists any of these six words as a quiz distractor.
- **New regressions:** none.

## Optional
- **`飽くまで.md:29–30`:** "derive… as an instruction" is not idiomatic. Suggested wording: "Do not read it literally as 'until one gets bored.'"
- **`あいかわらず.md:27`:** give the reading, 相 (あい).
- **たいてい ("usually; most") and 普通 ("ordinary; usually; local train"):** both also contain "usually". They are weaker matches than 普段 and are not required.
- **Unchanged earlier suggestions:** an あきれる/うんざり contrast line, the phrase あきれて物が言えない, and 挫折を味わう as an example for 味わう.

## Limits
- **Git:** commit identity, file hashes and diff hash are unverified.
- **Other changed files:** I did not compare the rest of `batch-01.json` or `manifest.json` with the parent commit.
- **Tools:** I did not run the validator or the build.
- **Quiz behavior:** taken from the format documentation, not the app's code.
- **Judgements:** these are scoped editorial assessments, not native-speaker certification.
