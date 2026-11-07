# Batch 093 visual follow-up review: 刑, 刑事 and the added 事 line

None of the 32 assigned screenshots shows a defect, so all three items stay CLEAN on correctness, coverage and readability on screen.

## Snapshot
- **Evidence version:** HEAD 66aea026e511368a236c0b427c880aa80ea7f02f.
- **Teaching content:** unchanged snapshot 27663944c7217a19e7de2f363e1b31a5f13452b6. I took this from the packet; I did not check it in Git.
- **Android build:** test-only build 1c1b7bf4, which still contains production code f9b59a2. It is not the latest app main.
- **Device:** API 35 emulator (emulator-5580), not a physical phone.

## Scope
- **Model:** claude-opus-5.5, original session c8c0a762-a31b-4dca-a1a0-bc010350ec18.
- **How I read:** one view call per message, in order, interpreting each result before the next.
  1. My own report, `docs\n1-reviews\batch-093-initial-claude.md`.
  2. The whole of `control\batch-093-visual-673-packet.txt`, which was not truncated.
  3. All 32 assigned screenshots from `execution-672`, in the listed order.
- **Not viewed:** the other 31 screenshots in that folder, the 184 single-character and 12 whole-word test-render (Paint) images, and any other reports.
- **Duplicates:** kanji-11 and kanji-12 look identical, as do kanji-19, kanji-20 and kanji-21. So do keiji-02 and keiji-05, and keiji-07, keiji-09 and keiji-11. ji-22 matches ji-system-back-to-kanji, and keiji-07 matches both kei-system-back-to-word and ji-system-back-to-word. These are not independent renderings.
- **Image size:** the tool may have resized the images.

## Verdicts
Wording and coverage verdicts are carried over from my text review; the screenshots revealed no reason to change them.

| Item | Correctness | Coverage | Readability on screen |
|---|---|---|---|
| `kanji\刑.md` | CLEAN (carried over) | CLEAN (carried over) | CLEAN |
| `words\刑事.md` | CLEAN (carried over) | CLEAN (carried over) | CLEAN |
| `kanji\事.md` line 37 | CLEAN (carried over) | CLEAN (carried over) | CLEAN |

**What the screenshots show for 刑:**
- The facts line reads 6 strokes, radical 刀 (no. 18) appearing as 刂 on the right, N1 (community list).
- "Sentence" is explained as a penalty, not a grammatical sentence.
- The shape mnemonic is labelled "Modern-shape mnemonic, not etymology" and says it does not establish history or a phonetic component.
- The reading row shows ケイ / on with the linked 刑事 entry. Sideways scrolling works, seen in kanji-09 versus kanji-11.
- The reading note covers the frozen KANJIDIC2 metadata, Digital Daijisen's ギョウ and 刑部省 ぎょうぶしょう, and says 刑事 is not read ぎょうじ.
- The four common words appear with kana: 刑事, 刑, 刑罰, 刑法.
- The notes compare 形/型, mention the older model/form senses, call でか a whole-word slang reading (not a kun reading), and rule out the "offender" meaning. The source lines are visible.

**What the screenshots show for 刑事:**
- The title is "police detective; criminal matters".
- The witness example, the criminal-case example and 刑事裁判 all have kana and English.
- The person versus modifier distinction is explained, along with the readings ケイ + ジ.
- 警官 and 探偵 are distinguished, 民事 is shown as the contrast, and "not an offender" is stated.
- The source line is JMdict entry 1249660, senses 1-2.

**What the screenshots show for 事 line 37:** "刑事 けいじ — police detective; criminal matters", rendered as a link.

## Findings
None proved.

Cosmetic observations, not defects:
- The fallback glyphs for 亅, 刂 and 彡 have a different weight from the surrounding text (font panels 1, 2 and 5).
- There is a slightly wider gap before 刂 in 刑's facts line and mnemonic (meaning-feedback, kanji-01). Both stay legible.
- In the Textbook font row of the test panel, 刑罰 wraps across two lines. That is the test panel's layout, not an article.

## Quiz, drawing and navigation evidence
- **Font panels:** all 46 in-scope characters are distinguishable in Gothic, Mincho, Textbook and Brush. That includes 刑/形/型 and 刀/刂/乃/凹/凸, plus the three whole words 刑事, 刑罰 and 刑法.
- **Meaning quiz (N1, 125 cards):** the choices were criminal punishment, concave; sunken, convex; protruding, and thereupon; possessive no. Only one is defensible.
- **Reading quiz:** the choices were トツ, ケイ, オウ and ナイ, with correct feedback for ケイ. The session ended at 1 of 1 correct, and no kun question was offered.
- **Drawing:** the six pinned strokes match the traced input. The trace screen says it is ungraded practice. The feedback says "Graded by stroke shapes only (handwriting model not available)". After giving up on recall, the screen shows "Here is the kanji".
- **Back navigation:** all four Back-button destinations rendered correctly (刑→刑事, 事→刑事, 刑事→刑, 刑事→事). The forward taps and offline status come from the supplied receipts, not from the screenshots.

## Reconciling my earlier limits
- My earlier gap on fallback wrong answers is closed only for the tested N1 and All setups: three curated wrong cards and zero fallback, shown for N1 and from the supplied record for All. Future custom pools and older clients are still uncertified.
- My earlier point that 文 could look like a defensible answer in broader pools is still open.

## Optional (kept from the text review)
- In `刑事.md` line 18, "is questioning a witness" fits 話を聞いています more closely than "is talking to a witness".
- Add a note that でか is often written デカ in katakana, and possibly a でか pointer in `刑事.md`.
- 乃, 凹 and 凸 are clear wrong answers but not very tempting ones.
- Low-confidence hypothesis: the word "older" in "older model/form senses" (`刑.md` line 45).

## Limits
- **Not checked:**
  - Git, upstream sources, the current app main, combined checks, CI, the public ZIP, publication or general release.
  - The fallback font face is unidentified.
- **Taken from the supplied record, not my own tests:**
  - The import of content snapshot 324b0bd9 (1116 kanji, 5070 words, zero problems).
  - The reading keys, and Full/Lite projections being equal.
  - The N1/All wrong-card counts, the four police-label guards and the inbound 探偵 guard.
  - The two run terminals ending at zero.
- **Not covered:** human handwriting, a working ML Kit model, a physical phone, a native-speaker check and measured learning effect. The 31 other screenshots were not viewed.
- **Carried over from the text review:** I did not count the 157 lexical dictionary entries one by one, and the 字通 gaiji extraction has gaps.
