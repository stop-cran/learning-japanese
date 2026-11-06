# Batch 078 visual confirmation: 冗, 冗談 and 談:37

I found no actionable defect in scope. All nine verdicts are CLEAN.

## Snapshot
- **Evidence HEAD:** `9ed58b037d40d7506ec9dc14ea4ee2ecb7f110f3`
- **Reviewed teaching:** `02b9634acda285bd60d00884479dee2a29ccb6e2`
- **Native envelope:** `7fb6c46374f2464648130f2473fabcb9137bb7d4`
- **Model:** Claude Opus 5.5 (`claude-opus-5.5`), one reviewer.
- I did not check Git or any upstream source myself. Hashes, the instrumentation result and the ContentSync result are coordinator-supplied evidence.

## Scope
- **Packet:** I read `batch-078-visual-source-packet.txt` in one full view. There was no truncation marker. It includes 冗.md, the revised 冗談.md, 談.md, `N1Batch078NativeTest.kt`, the instrumentation output, the route JSON, the article tree and the font-raster JSON.
- **Screenshots:** I viewed all 24 PNGs one at a time, in the listed order, and none failed to load.
  - The other 19 of the original 43 captures are aliases. I did not view them as separate pixels.
  - Some route steps exist only as test assertions, for example the 談 counterpart capture and 冗談 captures 03–14. For those steps I rely on the supplied assertions.
- **In scope:** the whole new 冗 card, the whole reused 冗談 article, and only line 37 of 談. The rest of 談 was context. Lexical conclusions are carried over from my earlier reviews; I did not reread the 78 dictionary families.

## Verdicts

| Assignment | Correctness | Scoped coverage | Bounded visual comprehensibility |
|---|---|---|---|
| New 冗 | CLEAN | CLEAN | CLEAN |
| Reused 冗談 (complete, revised) | CLEAN | CLEAN | CLEAN |
| Changed 談:37 | CLEAN | CLEAN | CLEAN |

### What the screenshots show
- **N1 selection:** "N1 · 110 cards". Meaning shows 1 due, Drawing 1 new and Readings 1 due, which reflects the test's seeded setup.
- **Meaning quiz:**
  - The choices are Japanese cedar, suspicious; uncanny, ceremony; formal conduct, and superfluous; redundant. None of the wrong choices overlaps in meaning with the right one, and feedback shows "Correct!".
  - The 元/兄/見 choices did not appear in this run. That matches the test's seeding and the coordinator's assertion, and it says nothing about safety in random choice pools.
- **Reading quiz:** the only question is "Pick the on'yomi". The choices are ホウ, ジョウ (marked correct), ジュウ and トウ, and none of the wrong ones matches ジョウ. There is no kun question, and Done shows "1 of 1 answers correct".
  - The full and Lite raw values (on ジョウ, kun empty) and the じょう quiz key come from the route JSON, not the pixels. The card text agrees: one on reading, no kun readings.
- **冗 article:**
  - The header, the facts line (冖 no. 14, community N1) and the labelled modern-shape mnemonic are legible.
  - The readings table clips the Typical-words cell in some captures, but there is a "Scroll sideways to read all columns" hint. The scrolled captures (kanji-12/14) show the full "冗談 じょうだん — joke; jest".
  - Common words, Notes (冗長性, "not useless", not a funny/harmless guarantee), the 元/兄/口/見/目/冖/几 comparison and the citations, including "Digital Daijisen: 冗.", all render fully.
- **冗談 article:**
  - Both examples are legible, with kana and English, as are the 冗談を言う, 冗談です and 冗談で言った lines.
  - The 冗 and 談 component links show, and the readings are ジョウ+ダン.
  - The corrected literal-versus-conversational rejection wording and the "entry 2403910" citation display exactly as in the packet.
- **談:37:** the new "冗談 じょうだん — joke; jest" line appears under Common words as a link.
- **Fonts:**
  - All 27 scoped characters appear in Gothic, Mincho, Textbook and Brush, with no blank or replacement box. The focused characters (冗, 元, 兄, 見, 冖, 几, 口, 目) and the whole words show no misleading lookalike.
  - 冖 and 几 render in a visibly different fallback face. That is not a defect, and I do not identify which font it is.

## Findings
None.

My original F1 (冗談.md:45, the overstated "not joking" claim) is **resolved**. The corrected text is visible on screen at what is now lines 45–47. I keep the part of my remedy I withdrew earlier: the supplied evidence does not show that the polite 冗談ではありません also works as a protest, and the article does not claim it does.

## Optional
These all remain optional, with the coordinator's reasons accepted:
- Add the "redundancy" sense to the 冗長 gloss.
- Rephrase "Learn the meaning of each compound" (still visible at the meaning-feedback screen).
- Change "pretended move" to "pretended house move" (still visible in 冗談-09).
- Add a short gloss for 几.

New observations, also optional:
- In the drawing screens, the stroke-number labels 3 and 4 sit close together. This is how the app places labels, not a content issue.
- 談's Vocabulary citation lists only JMdict 1401210 and 1198760, not 1355540 for the added 冗談 line. That source is cited in 冗談.md, so I don't treat it as a defect.

## Limits

### Earlier limits, reconciled
- **冖/几 rendering** (not in the bundled fonts' character maps): **partially resolved.** The screenshots show them legible in all four families and inline in articles, but only on the API 35 emulator (port 5580), not a physical phone. Raster hashes and `Paint.hasGlyph` don't certify readability.
- **Quiz safety:** **partially resolved.** It holds only for the choices actually shown. Random and larger choice pools, including the 余 "surplus" card appearing as a fallback, remain unverified.
- **Native and runtime behaviour:** **partially resolved**, by emulator pixels plus supplied assertions:
  - Navigation, all four link directions, system Back and offline state come from the test fixture and the route JSON (`passed: true`, `offline: true`, `phoneEvidence: false`). A still screenshot can't prove navigation, saved progress or offline state.
  - The whole ContentSync result (1090/5046/110, version `8e06edf2b0857b26`, problems 0, epoch 1) is supplied evidence, not run by me.
  - Progress was seeded in a disposable test setup. The grades actually exercised in this run were meaning, a reading grade of 3, an ungraded trace and a give-up recall grade of 1.
  - The final article tree shows a "Loading…" state captured after the test finished. I treat it as a capture quirk, not a demonstrated defect.

### Still outstanding
- **Drawing:** the four strokes were injected from the reference data as touch input, and "handwriting model not available" was displayed. This is not human handwriting, successful recall, ML Kit recognition or a model download.
- **Unverified:** native speakers, a physical phone, general release, the whole card set, final integrated publication, upstream and Git sources, and articles that weren't supplied (ジョーク, からかう).
