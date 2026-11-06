## Batch 083 visual confirmation (凌, 凌ぐ, 凌駕): final report

All three new articles come out CLEAN on all three facets, with no findings, and the 074 choice issue is resolved for the default four-choice N1 and All quiz. One gap: no frame shows the top (title, reading and anything above "Meaning") of either word article.

### Snapshot
- **Evidence HEAD:** 2f24c5c456ea7a026762f6c6c95b2bcdcebb337b.
- **Reviewed teaching commit:** 7cc896f488ae5315046453777aae6768b9ff18e8.
- **Native build:** envelope 867fe8be, content version 6dfe6a1e287ce5df, run attempt 578.
- All hashes and identities are as given in the packets. I did not check Git, upstream sources or hashes myself, and I don't know the uncommitted state.

### Scope
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), the original batch-083 reviewer, continuing my own work. This is a dependent visual confirmation, not a new blind review of the wording or the dictionaries.
- **What I read:** 32 single-view turns, one resource each.
  - Resource 1 was `docs\n1-reviews\batch-083-visual-source-packet.txt`. It came back complete, with no truncation marker and nothing denied.
  - Resources 2–32 were the 31 original PNGs in `attempt-578\`, which stand for all 56 captures after identical files were removed (deduplication was the host's; I did not check it).
  - Nothing was denied or missing. I made no extra reads and used no other tools.
- **Image limits:**
  - Every PNG came back at about 900×2000 px and may have been resized. I make no claims about full-resolution bytes or hashes.
  - The font panels were legible enough to identify each glyph, but too small to judge fine stroke detail.
  - The top lines of some frames sat under the app bar, and table columns were cut off at the edges. In each case another frame showed that content in full.

### Verdicts
| Article | Correctness | Scoped coverage | Bounded visual comprehensibility |
|---|---|---|---|
| `kanji\凌.md`, including the changed choice | CLEAN | CLEAN | CLEAN |
| `words\凌ぐ.md` | CLEAN | CLEAN | CLEAN (see coverage limit) |
| `words\凌駕.md` | CLEAN | CLEAN | CLEAN (see coverage limit) |

CLEAN means I found no actionable defect within scope. It is not an exhaustive certification.

### Findings
None. What the pixels showed:

**凌 article**
- I saw the whole article across the kanji-01/03/09/11/17 frames, the backlink frames and the System Back frames.
- The metadata on screen is right: 10 strokes, radical 冫 (no. 15), "N1 (community list)".
- The two meanings, enduring or getting through and surpassing, are kept apart. The text says 凌駕 means surpassing, not weather shelter.
- The mnemonic is labelled as an "invented memory scene, not a historical derivation or a verified explanation of the sound".
- The readings table:
  - The screen tells the learner to scroll sideways.
  - リョウ/on links to 凌駕 ("surpassing; outdoing"); しの.ぐ/kun links to 凌ぐ ("endure; surpass").
  - Read across frames, every column is complete. The dash I wondered about in kanji-01 is just off-screen, as kanji-11 shows.
- The note says grade 9 does not make these ordinary readings name readings.
- The notes cover:
  - ぐ versus 忍ぶ's ぶ.
  - 陵 with 阝 versus two 冫 marks; the rare spelling 陵駕 is not a free swap.
  - 准, 冶 and 次 compared via 隹, 台 and 欠. Keeping 次 in the notes is fine even though it is no longer a quiz option.
- The source line and links are present.

**凌ぐ article**
- The meaning has two parts: endure, keep out or get through; and surpass or outdo.
- Examples, with kana and translations:
  - 風雨を凌ぐ (ふううをしのぐ), "shelter from wind and rain".
  - 前作を凌ぐ傑作 (ぜんさくをしのぐけっさく), "a masterpiece surpassing the previous work".
- Grammar: takes を; a transitive godan verb ending in ぐ. The forms しのぎます, しのいで, しのいだ and しのがない are shown.
- 忍ぶ is contrasted: しのいで versus しのんで.
- The "Distinctive meaning" section imposes no rule about temporary, permanent or formal use.
- Synonyms (こらえる, 我慢, 凌駕) are qualified as partial overlaps.
- Sources: JMdict 1554200 and Daijisen.

**凌駕 article**
- It is a noun and a する-verb that takes を.
- Example: 前作を凌駕する売れ行き (ぜんさくをりょうがするうれゆき). The text says it compares sales, not artistic quality.
- How the kanji combine: 凌 is read リョウ; 駕 (plain text, ガ) has a "rising above others" sense. The text warns against reading in 駕's vehicle meaning.
- Synonyms:
  - 凌ぐ is noted for its extra uses.
  - 優れる is correctly called intransitive.
  - 上回る suits numerical comparisons and is not an unrestricted substitute.
- 陵駕 is described as a rare spelling, not a rare pronunciation and not a free swap.
- Sources include Daijisen's 駕 entry, sense 2.

**Changed quiz choice**
- The meaning question and its feedback show exactly four options in the live order:
  - smelt; work metals (冶)
  - endure; surpass (凌)
  - clear; sharp-minded (冴)
  - quasi-; associate rank (准)
- There is no 次 and no random filler option.
- As shown, "clear; sharp-minded" is clearly wrong for 凌. I am not claiming there is no overlap with 冴える's undisplayed "excel at" sense, or with 冴え's "skillfulness".
- The selection screen shows "N1 · 115 cards".

**Reading quizzes**
- On'yomi question (2 attempts left): リョウ/ジュン/ヤ/リュウ. Kun'yomi question (1 attempt left): さえる/しおり/しか/しのぐ.
- Both feedback screens are correct, followed by "Session complete, 2 of 2 answers correct."
- None of the wrong options is a reading of 凌.

**Drawing**
- The tracing screen shows strokes numbered 1–10. Strokes 1–2 are 冫, which matches the stroke data.
- The feedback screen shows the injected strokes and "Practice only: not graded".
- The give-up recall screen shows a blank drawing and the reference strokes.
- The app honestly shows first "Downloading the handwriting model…" and then "handwriting model not available".

**Fonts**
- All 30 scoped Han characters and the whole words 凌ぐ and 凌駕 render in all four faces (Gothic, Mincho, Textbook, Brush). There are no blanks or replacement boxes.
- 凌 and 陵 stay distinct, as do 准, 冶, 冴, 次 and 凌.
- The standalone components 冫, 夌, 阝 and 隹 visibly fall back to a gothic-looking face; this is clearest in Textbook. That is only a change of typeface, not a defect.

**Navigation**
- The pixels match 凌⇄凌ぐ and 凌⇄凌駕 in both directions, plus the word comparison links.
- That those returns came from System Back, and that the run was offline, comes from the supplied route data, not from pixels.

**Earlier "All · 0 cards" anomaly**
- The 5:43 selection frame shows N1 with 115 cards loaded.
- So the "All · 0 cards" screen tree was most likely dumped after the scenario finished, in the test's cleanup step. The pixels don't prove when it was taken.

### 083-NATIVE-574-CHOICE
- **Text:** resolved, as I said before. 冴 (N1) replaces 次 (N3), so all three planned wrong answers are available in the N1 and All stacks.
- **Run time:** resolved for the default four-choice quiz in N1 and All, based on the supplied evidence.
  - Attempt 578 reports OK (2 tests): both named native cases passed.
  - QuizBuilder's exact IDs and titles are reported for the 115-card and 1,095-card stacks, with no random filler.
  - The pixels independently confirm the four displayed options in one live question.
- **History:** the original attempt-574 failure is kept on record, not erased. The 麟 fallback captured then is not claimed to be ambiguous.
- **Not claimed:** safety of the All UI path, custom, padded, partial or larger stacks, or reverse questions.

### Optional (carried forward)
- `words\凌ぐ.md:20`: "keep out wind and rain" would be closer to JMdict than "shelter from". The current wording is visible on screen and is not wrong.
- `words\凌ぐ.md:15–17`: could mention sense 3, "defy; slight". Not required.
- **Legacy, not this batch:** `冴.md:13` still lists 次 (N3), so a 冴 question in the N1 stack will get a fallback option in the same way.
- **Legacy, not this batch:** extra-practice padding (`QuizViewModel.pad`) adds only the borrowed cards to the option pool, so curated distractors may be missing there.
- **App UI wording, outside scope:** "Practice only: not graded" next to "Graded by stroke shapes only" reads slightly contradictory.
- **Line breaking:** the conjugation list in 凌ぐ breaks between し and のぎます. This is normal Japanese line breaking.

### Limits
- **Word-article tops not seen:** no frame shows the 凌ぐ or 凌駕 heading, reading line or anything above "Meaning". I saw the title and gloss only in the app bar, so this part is not visually confirmed. My earlier text review covered it.
- **Supplied evidence, not pixels:** reading keys りょう/しのぐ being saved, the Full/Lite and raw-source data, the saved logs, the import counts (1,095/5,052/115, zero problems), the content version, the QuizBuilder ID assertions, System Back, offline mode, the emulator configuration, the test-only Android build 1c1b7bf4, the inherited HOST577 compile checks, and the 120 individual + 8 whole-word Paint checks. Those Paint checks are not 128 PNG reads.
- **Inherited, not freshly inspected:** the earlier all-40-font check.
- **Font limits:** pixels and hashes do not identify which fallback face is used, and a character missing from a font's character map is not a glyph failure.
- **Drawing:** the strokes were injected by the test. This is not human handwriting, successful recognition, ML Kit or a model download.
- **Device:** emulator only (API 35, emulator-5580). No physical phone, latest-main or native-speaker claims, and no evidence about learning effectiveness.
- **Publication still outstanding:** merge with current main, the combined checks, the signed owner push, remote CI, the exact immutable ZIP, owner issue 60, physical-phone testing, general release and the whole-set review.
- **Earlier limits still apply:** I checked no sources or upstream data myself; byte and line totals were unconfirmed; title uniqueness across the corpus was not checked; production code was read only in the excerpts supplied.
