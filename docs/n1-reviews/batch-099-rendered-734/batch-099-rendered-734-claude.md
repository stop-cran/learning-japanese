**Snapshot:** The teaching content is unchanged from the signed snapshot `70dfe334`. The packet also names content HEAD `a580bb1c`, Android build `1c1b7bf4`, and native run 733, which imported archive `17a4bbb9` once on an emulator (`sdk_gphone64_x86_64`, API 35). There is no phone evidence (`phoneEvidence:false`). I did not check Git or upstream sources myself.

**Scope:** Claude Opus 5.5 (`claude-opus-5.5`), continuing my original batch-099 session as a dependent follow-up. Tool reads were serial:
- the whole rendered packet, in one `view` with `forceReadLargeFiles=true` (it ended cleanly, so I saw no truncation);
- then `n1-099-font-panel-1.png`, `n1-099-font-panel-2.png`, and `sheet-01.png` through `sheet-10.png`, in that order.

I used only my own earlier findings, not any other reviewer's report. The JMdict and KANJIDIC2 extracts were selected by the coordinator from frozen packets. The two `source-evidence.json` files appear only as their top-level keys.

**Verdicts:**

| Item | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| New `kanji\剰.md` | CLEAN | CLEAN | CLEAN |
| Exact `words\過剰.md` line 25 change | CLEAN | CLEAN | CLEAN |
| Exact `kanji\過.md` line 41 addition | CLEAN | CLEAN | CLEAN |

- **Fallback meaning choice N099-FALLBACK-JOU:** **NEEDS FIX**, but only as a later app check; the articles themselves need no change. See finding 1.
- **Glyphs and rendered screens:** **CLEAN**, judged from these emulator screenshots, with the limits listed below.

**Findings:**

1. **Minor; quiz meaning; outside the current authorization.**
   - **Where:** `n1-099-article-route.json`, pool `randomN1Subset`, seeds 4 and 7. `kanji\剰.md` line 3 ("remainder; surplus amount") appears with `kanji\冗.md` line 3 ("superfluous; redundant").
   - **Claim:** Both characters' ordinary meanings centre on more than is needed. The supplied JMdict families confirm a shared word written either way:
     - 冗員/剰員 is one word, "superfluous staff; excess personnel".
     - 冗語 has the rare variant spelling 剰語.
     - KANJIDIC2 gives 剰 "surplus" and 冗 "superfluous". The 字通 entry glosses 剰 as 贅疣（無用のもの）, a useless thing.
     - 剰.md itself teaches 過剰 as "more than is needed".
   - **Why it matters:** A learner who knows 過剰 can reasonably accept "superfluous" for 剰, so this distractor is not clearly wrong. The ambiguity is real but limited: the exact title is always among the choices, and 冗 appeared in only 2 of 16 random-subset seeds.
   - **What I checked:** All 64 supplied choice sets (N1, All, bounded custom and random subset; 16 seeds each). No other fallback title overlaps 剰's meaning. 充 ("allot; fill") and 享 ("enjoy; receive benefits") are about filling or receiving, not excess.
   - **Not established:** That the two characters are freely interchangeable, how often each spelling is used, or the reverse direction (剰 offered in 冗's quiz).
   - **Minimal remedy:** Record this as an open app requirement for pairwise kanji exclusions. The content contract has no such field today, and adding one is outside issue60. Do not change either title. If wanted, a content-only mitigation is a Notes line in 剰.md comparing it with 冗 via 冗員/剰員. That helps the learner after feedback but does not prevent the ambiguity.
   - **Confidence:** high that the meanings overlap; medium on how much it affects learning.
   - **Credit:** the coordinator's packet raised this question; my original review did not.

2. **No proved defects in the articles or in what the screenshots show.**
   - **Article rendering:** The full 剰 article renders in order, through the metadata line at the end.
   - **Reading table:** At the default scroll position the Typical words column is cut off on the right (for example "kanji spelling o"). Screens kanji-11 and kanji-14 show the same rows shifted, where that text is complete but the Reading column is cut instead ("ading", "ョウ"). The "Scroll sideways to read all columns." hint is shown. This is how the table display works for long rows; it is not a content error.
   - **Links and Back:** In the screenshots, these links work in both directions: 剰 → 過剰, 過剰 → 剰, 過 → 過剰 and 過剰 → 過. Back screens show return in each case.
   - **Quiz and drawing:**
     - The reading quiz is on'yomi only. Its options are リュウ, ジュウ, ケン and ジョウ, with no kun question.
     - The default meaning options are 剰, 奇, 剣 and 享.
     - Tracing shows 11 numbered strokes in the KanjiVG order.
     - The drawing-from-memory screen shows the give-up path ("Here is the kanji").
     - The N1 selection screen shows 131 cards.
   - **Glyphs:** All 12 Han characters and the two words render in Gothic, Mincho, Textbook and Brush (panel rows 乗余刀刂則剣剰剩去字通過 and 剰剩乗余剣則刀刂過過剰剰え). In the Textbook row, one form, most likely the old 剩, and the separate 刂 render in a heavier substitute font. I saw no missing glyphs or garbled characters.

**Optional:**
- In body text, 剰 and 剩 look almost identical. The older-form note at line 49 could say briefly which part differs, but only once a source verifies that description.
- The long kun rows (lines 31–33) could move from the table into prose to reduce sideways scrolling.
- After the reading question, the feedback lists unqualified あまつさえ、あまり、あまる. This is existing app behaviour, and the article text below it qualifies those readings.
- Carried over from my first review: name the source at line 33 ("the character dictionary"), add JMdict entry 1196170 to `kanji\過.md` line 50, and note that sources call 乗 the phonetic part (still not needed).

**Reconciliation with my original review:**
- **"No proved defects" in the three changed passages:** confirmed, now also against the rendered screens.
- **Hypothesis that fallback could pair 剰 with 余:**
  - Withdrawn for the 64 supplied pools, where 余 never appears.
  - Still unverified for other custom pools.
  - Replaced by the 冗 overlap above (unresolved; app gate).
- **Hypothesis about 乗 sharing ジョウ in the reading quiz:** partially resolved. The one reading quiz shown had distinct options, but that is a single exposure.
- **Optional items:** still optional.
- **Limit "eleven pinned generated paths":** unresolved; this packet doesn't address it.
- **Limit "no native or UI evidence":** partially resolved by emulator screenshots; phone evidence is still missing.

**Limits:**
- **Not verified independently:** Git history, hashes, upstream dictionaries, and whether the fallback faces were actually identified.
- **Taken from the packet, not seen:** offline operation, saved progress and drawing grades come from JSON fields; the screenshots don't show them.
- **Image limits:** Contact sheets are thumbnails, so fine stroke detail and the 剰/剩 difference can't be judged reliably at body size.
- **Drawing input:** The strokes were injected by the test, not drawn by hand. The handwriting model was unavailable.
- **Not covered:**
  - phone hardware;
  - review by a native speaker;
  - measured learning results;
  - the reverse 冗-quiz exposure;
  - the safety of every possible filtered or custom pool.
