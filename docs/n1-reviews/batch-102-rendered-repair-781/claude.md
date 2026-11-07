# Batch 102 addendum: serial re-read of the two kun-reading screens (snapshot 54be1c9a)

**Bottom line:** both kun-reading screens are CLEAN, and these two serial re-reads are enough to close the parallel-view deviation. The original execution stays non-compliant, and I've corrected the two inaccurate wordings below.

## Snapshot
- **Model:** Claude Opus 5.5 (`claude-opus-5.5`), original session 112f8849.
- **Versions:** docs HEAD 1ae398f6; teaching snapshot 54be1c9a, unchanged; Android app bf30cdea.
- **This is a dependent, bounded repair.** It is not a new blind review and not a full re-read.

## Scope
- **Two new image opens, one per turn, never in parallel:**
  1. `n1-102-curated-kun-feedback.png`
  2. `n1-102-curated-kun-question.png`, opened only after the first result returned.
- **Image size:** the view tool showed 900×2000 renditions of the 1080×2400 sources. I make no claims about original-pixel detail.
- **Nothing else was read:** not the dossier, the other 41 PNGs, any text resource, or any repository file.
- **Inherited, not repeated:** the earlier five-resource and 43-image assessment. That session went through three context compactions and contained one parallel-call deviation.

## Verdicts (correctness / scoped coverage / comprehensibility)
- **kun-question screen: CLEAN / CLEAN / CLEAN.**
  - Shows "Kanji readings", "Attempts left: 1", the repeat-queue note, a large 劣, "Pick the kun'yomi", and the options おかす / つくる / ほたる / おとる, plus "I don't know".
  - おとる matches 劣's sourced kun reading おと.る. The other three are not readings of 劣 in the supplied KANJIDIC record, so they are defensibly wrong. That conclusion comes from the earlier session; the record was not re-read here.
- **kun-feedback screen: CLEAN / CLEAN / CLEAN.**
  - Shows "Correct! — kun'yomi" with ✓ おとる highlighted green, the other options greyed, and the line "inferior; worse: レツ、おとる", which matches the expected feedback.
  - Next and "I guessed" are present, and below them the 劣 article starts: 6 strokes, radical 力 no. 19 at the bottom, N1 (community list), and the 優劣 "not inferiority alone" sentence.
  - The kana and 劣 are readable at this rendition, with no tofu (blank placeholder boxes).

## Reconciliation
- **Original parallel-view deviation: resolved for these two images only.** The original execution is not accepted retroactively and remains non-compliant.
- **"Clock differences mean the 'identical' screenshots aren't byte-identical": withdrawn.**
  - Coordinator hash evidence shows the 43 files form 25 unique byte states, so 18 files are exact byte duplicates.
  - My earlier visual grouping also gave 25, but which files share a state rests on the coordinator's SHA hashes, not on new inspection of the other 41 images.
- **"功 merit (the opposite)": withdrawn as worded.**
  - The live labels were 劣 "inferior; worse", 冗 "superfluous; redundant", 蛍 "firefly" and 功 "merit; achievement".
  - 功 is defensibly wrong because "merit; achievement" does not mean "inferior; worse". I don't claim it is a lexical antonym of 劣.
- **Sampled semantics: partially resolved, as before.**
  - The assessment covers only the finite sample: 128 production option sets and 40 labels, backed by sources and dependent on the earlier session.
  - Unsampled random choices remain UNVERIFIED, and this is not a universal guarantee that random pools are safe.

## Findings
None proven.

## Optional
None new. The trace wording in the app UI is outside this scope.

## Limits
- Supplement status: the serial re-read of these two images provides the bounded supplement that was needed. No further image evidence is required to close this deviation. Acceptance of the two-family rendered closure is still the coordinator's decision.
- No Git or upstream verification and no new tests.
- Evidence is from an API 35 emulator, not a physical phone, and there was no native-speaker review.
- The installed font face was not identified.
- No graded handwriting or mastery, and no measured learning effect.
