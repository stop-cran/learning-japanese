# SAME082 corrected-runtime visual confirmation: final report

All four scoped items are CLEAN on every facet, there are no findings, and 082-V1 is resolved for the default four-choice N1 meaning quiz on emulator evidence.

## Snapshot

- **Evidence HEAD:** 86c77107638e0adf2aa2752c50533124c389b371.
- **Corrected teaching snapshot:** 9ce870d190d5c519d65ed20b118de64371350c0c.
- **Native archive:** e108bbeb, content version d82e7fefe3898a70.
- **Builds:** test-only Android 1c1b7bf4, which preserves production f9b59a2. It is not the latest app main.
- **Native execution:** attempt 565.
- **Earlier artifacts:** the old 559/560/561 runs are historical and not used here as corrected acceptance.

## Scope

- **Model:** Claude Opus 5.5 (claude-opus-5.5).
- **What I read:** 29 resources, one `view` call each, with no rereads, shell, edits, delegation or parallel calls:
  - R1 was the complete source packet `batch-082-visual-source-packet.txt`, read with forceReadLargeFiles and no view range.
  - R2–R29 were 28 original PNGs from `batch-082-native-corrected\attempt-565\`. These are the host's byte-group representatives for 51 captures; I did not see the other 23 captures directly.
- **Image size:** every frame arrived at about 900×2000, which may be downscaled. I can't claim full-resolution bytes and did not verify any hashes.
- **Compressed history:** my notes on R1–R6 come from summarized session history, not my original wording. Those notes say R1's `execution.json` lists 53 PNGs while the host states 51 captures, and I did not reconcile the two.
- **Items assessed:**
  - new `kanji\准.md`
  - new `words\准教授.md`
  - the 准教授 Common words bullet in `kanji\教.md:39`
  - the successor paragraph and link in `words\助教授.md:16`
- **Context only:** the 冴, 冶, 隼 and 教 cards were supplied as background, not given a new whole-card review.
- **Inherited conclusions:**
  - My earlier textual review and visual pass.
  - My choice-reconciliation report and changed-metadata confirmation.
  - The source-level 082-V1 correction verdict.
  - The prior all-40 font evidence.

## Verdicts

Each facet below is CLEAN. That means no actionable defect was established within scope; it is not exhaustive certification.

| Item | Correctness | Scoped coverage | Bounded visual comprehensibility |
|---|---|---|---|
| New 准.md | CLEAN | CLEAN | CLEAN |
| New 准教授.md | CLEAN | CLEAN | CLEAN |
| 教.md:39 bullet | CLEAN | CLEAN | CLEAN |
| 助教授.md:16 successor paragraph and link | CLEAN | CLEAN | CLEAN |

### What the pixels showed

**准.md:**
- Header: "quasi-; associate rank", 10 strokes, key radical 冫 (no. 15), N1 (community list).
- Rank and approval senses: the rank sense, plus 批准 ひじゅん for the approval sense. The text warns it is not a "half-professor" or "trainee".
- Mnemonic: qualified as a modern-shape aid, not etymology.
- Readings: a single on-reading ジュン linked to 准教授. The note says the source record has no kun-readings without denying other dictionaries' readings.
  - The sideways-scrolling table is signposted; R14 showed it unscrolled and R15 shifted, and together they cover all columns.
- Common words: 准教授 and 批准.
- 準 shape and spelling: 準 has 氵 and a lower 十, while 准 has 冫 and no 十. The spellings are not freely interchangeable, and 準教授 is noted as recognized with 准教授 as the current title.
- The 集/進/難 lookalike note is unchanged and complete, and the metadata and source links appear.
- Runtime flows:
  - The on-reading quiz showed a single valid answer.
  - Tracing and recall drawing ran with ten reference strokes, graded by shape only, and the screen said "handwriting model not available".
  - The N1 selection screen showed 114 cards.

**准教授.md:**
- Meaning: a rank below 教授 with teaching and research duties, and not a personal helper.
- Two original examples (彼女は大学の准教授です。 and 田中准教授の講義を聞きました。) have correct kana, particles and English, and read naturally.
- The note on 田中先生 versus 先生 as a rank is present.
- How the kanji combine: 准 modifies the head 教授; 教 contributes teaching and 授 contributes imparting; the readings are ジュン+キョウ+ジュ.
- Comparisons:
  - 助教授 is the former title, replaced in April 2007.
  - 助教 is a separate rank and 助手 does not identify the role.
  - 教授 and 先生 are explained separately.
  - None of these is presented as an antonym.
- Usage: a noun, not 准教授する; no international equivalence or automatic promotion is implied; the JMdict spelling 準教授 is mentioned; sources are listed.

**教.md:39:** the bullet reads exactly "[准教授] じゅんきょうじゅ – associate professor", with the link.

**助教授.md:16:** the paragraph says the rank was "renamed [准教授] (じゅんきょうじゅ)… in April 2007". This is the first linked mention; the later Synonyms mention is unlinked, as scoped.

**Fonts (R8–R10):**
- All 34 scoped Han rendered in the Gothic, Mincho, Textbook and Brush families, as did the whole word 准教授.
- No blank or replacement boxes appeared.
- No lookalikes collapsed into each other:
  - 冴 has 牙 on the right and 冶 has 台.
  - 隼 has 隹 over 十.
  - 准 has 冫 and no 十, while 準 has 氵 and 十.
  - Standalone 冫 shows two marks and 氵 shows three.
- 辶, 隹, 冫 and 氵 look the same across families. That fits a fallback face, which is a typeface change, not a defect.

**Navigation:** the pixels show only end states. That 准↔准教授 and 教↔准教授 (four directions), 助教授↔准教授 (two directions) and System Back all work rests on the supplied route and assertions.

## Findings

None.

## 082-V1 runtime reconciliation

**Resolved** for the default four-choice N1 meaning quiz on this emulator evidence.

- **Pixels (R19 question, R20 feedback):** exactly four untruncated labels: "clear; sharp-minded", "quasi-; associate rank", "falcon" and "smelt; work metals". There is no "imitate; emulate", no 倣 and no tag-based fallback, and only one label fits 准 within the existing source scope.
- **Supplied evidence:** the mapping of those labels to 冴/准/隼/冶 and the route order rest on the supplied native assertions and route data.
- **Not shown in pixels:** the All-stack quiz was not captured, so it rests on the supplied, content-level evidence only.
- **Still open:**
  - The rare imitation sense of 准える (なぞらえる) remains recognized. Its rarity is not disproof, and ordinary frequency or learner impact is not established.
  - Custom, partial, larger or future pools remain uncertified, including the earlier hypothesis about 準 in a larger pool.
  - The new distractors also feed the on-reading quiz (ヤ appeared there); that quiz was not ambiguous.

## Optional (carried forward, not findings)

- The 准 readings row could add 批准, and the card could add 准看護師 or 准尉 as rank examples.
- Standalone 授 in 准教授's "How the kanji combine" is not linked.
- App UX:
  - The trace screen shows "Downloading the handwriting model…" while offline.
  - A loading state appeared in the teardown screen tree.
- The reading じゅんきょうじゅです wraps mid-word; this is layout only.
- The 准 Notes compare 集/進/難, not the quiz distractors 冴/冶/隼. This is consistent with the scoped diff; a lookalike note for 冴/冶 is optional.
- The earlier withdrawn claim about 準's curated distractors stays unverified.

## Limits

- **Pixels versus supplied evidence:** these items were supplied as execution evidence and not observed in the stills:
  - the sync counts: 1094 kanji, 5050 words and 114 N1 cards; version d82e7fef; zero problems; parser epoch 1
  - the single archive request
  - both test cases ending with status 0 and no skips
  - the API 35 read-only emulator-5580, with the helper stopped
  - Full and Lite modes, the quiz key and the persisted good-answer logs
  - the injected drawing strokes and the grade saved on Next
  - System Back and offline behaviour
  - the synthetic seeding, with no owner progress
- **Inherited without rerun:** the 563 host run (3+1+5, no skips) and the 564 compile.
- **No independent verification:** I did not check Git, upstream or hashes, and did no fresh dictionary lookup.
- **Fonts:**
  - Cmap absence is not glyph failure.
  - Pixels, Paint.hasGlyph and raster hashes do not identify the fallback face.
  - The 136 individual and 4 whole-word Paint assertions are not 140 PNG reads.
  - Inline 冫 and 氵 marks and fine stroke detail were only marginally resolvable at the size received.
- **Drawing:** the strokes were injected by the test. This is not human handwriting, successful recall, ML Kit recognition or a model download.
- **Not established:** physical-phone rendering, native-speaker certification and learning effectiveness.
- **Still outstanding:** final combined-main integration, publication, CI, an immutable ZIP, phone and general release, and whole-set acceptance.
- **Preserved limits:** the original OOM, denial, source, citation, lookup, read-depth and process limits are unchanged.
