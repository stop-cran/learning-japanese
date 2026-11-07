# Batch 099 dependent guard/rendered confirmation (native 741, packet 742)

The new `quiz_exclusions: [冗]` line works as intended: none of the 64 recorded answer sets for 剰 now show 冗. All three teaching passages stay CLEAN, and I found no new defect. This applies only to clients that understand the guard; older apps ignore it.

## Snapshot
- **Content:** HEAD 1ff076b1, archive 749ea11b, contentVersion 39eb4a86902c6dec.
- **Android:** bf30cdea, run on an API 35 emulator (not a phone).
- **Teaching text:** unchanged since 70dfe334. The only content change is one line in `kanji\剰.md`: `quiz_exclusions: [冗]`, which is now line 14.

## Scope
- **Model and session:** Claude Opus 5.5 (`claude-opus-5.5`), session 2ac79fdb-83fc-485d-8f64-6c5d7b473973.
- **What I read this round:** one `view` call per turn, each finished before the next:
  1. my own 734 report;
  2. the whole 742 packet in one forced read (no truncation seen);
  3. font panels 1 and 2;
  4. contact sheets 01–10, covering 39 screenshots.
- **My earlier 734 report** said its reads were serial, but they were not (up to 9 calls overlapped). That report stays as it was; I am not claiming it complied.
- **Provenance:**
  - The 64 answer sets and the mechanical checks (224 guard checks, 896 word-guard checks, host tests) come from the coordinator's summary of the raw run files. I did not open the raw route JSON.
  - Dictionary text is the committed excerpts, not a fresh lookup. I did no Git or upstream checking.

## Verdicts

| Passage | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| New 剰 card (with guard) | CLEAN | CLEAN | CLEAN |
| Exact 過剰 change (line 25) | CLEAN | CLEAN | CLEAN |
| Exact 過 change (line 41) | CLEAN | CLEAN | CLEAN |

- **Guarded fallback meaning choices: CLEAN** for compatible clients in the sampled pools.
  - The pairing is justified by meaning: the 冗員/剰員 spelling pair, the rare 冗語/剰語 pair, the KANJIDIC2 glosses "superfluous" vs "surplus", and 字通's 贅疣 ("useless thing") for 剰.
  - The guard follows the format rules: exact character ID, no overlap with the distractors 乗/剣/則, and one declaration counts for both directions.
  - None of the 64 sets shows 冗. The 35 labels that do appear (e.g. "allot; fill", "frugal; thrifty", "enjoy; receive benefits") are not defensible answers for 剰.
- **UNVERIFIED** for old clients and for custom pools that were not sampled.
- **Glyphs: CLEAN, with limits.**
  - All 12 characters and both words (過剰, 剰え) are legible in all four fonts.
  - 剰 and 剩 can be told apart at panel size.
  - In the Textbook font, 剩 and 刂 still fall back to a heavier face; that is a cosmetic font mismatch.
- **Rendered screens: CLEAN, with limits.** I saw:
  - N1 selection with 131 cards;
  - the default meaning quiz: remainder; surplus amount / pig; pork / sword; double-edged blade / cocoon;
  - the reading quiz offering ジョウ only, with no kun questions;
  - the 11-stroke trace and recall give-up screens;
  - both changed passages, forward and reverse links, and system Back.

## Findings
None proved.

## Optional
1. Earlier suggestion, still standing: say which dictionary "the character dictionary" means in the あま.る row (now line 34).
2. Earlier suggestion, still standing: add JMdict 1196170 to the 過.md citation line.
3. Earlier suggestion, still standing: reading-quiz feedback lists all readings (ジョウ、あまつさえ、あまり、あまる) without marking which are reference-only. This is the app's behaviour, not the card's.
4. New: the Textbook fallback face for 剩/刂, and 剩 vs 剰 being hard to tell apart in small body text.
5. Earlier suggestion, still standing: optionally mention that 乗/乘 is the phonetic component.

## How earlier findings now stand
| Earlier item | Status |
|---|---|
| N099-FALLBACK-JOU (冗 offered as a wrong answer for 剰) | **Resolved** for compatible clients in the sampled pools. Old clients and unsampled pools: limit, not a content defect. |
| 余 fallback hypothesis | Withdrawn; 余 is absent from all 64 sets. |
| 乗/ジョウ in the reading quiz | Partially resolved; the reading choices seen were ヨウ/ジョウ/ジュウ/ケン. |
| "Eleven pinned paths" limit | Unresolved (as before, I could only identify 10). |
| No UI/font evidence | Partially resolved (emulator only). |
| 733/734 serial-read claim | Contradicted; preserved and not accepted retroactively. |

## Limits
- **Emulator only** (`phoneEvidence:false`). I cannot identify the actual font faces.
- **Drawing:** strokes were injected by the test, and the handwriting model was unavailable.
- **Thumbnails:** contact-sheet thumbnails limit how much detail I can see. The reading table is spread across sideways-scroll positions rather than shown whole in one frame.
- **Contact-sheet captions:** the captions show □ in place of the kanji. This is a problem in how the sheets were made, not in the app.
- **Pools:** the pools are sampled, not exhaustive, and this is not universal synonym detection.
- **No certification** for phones, native speakers, learning outcomes or the full card set, and no credit as a new blind review.
