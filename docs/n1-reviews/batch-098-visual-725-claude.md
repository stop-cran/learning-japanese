# Batch 098 rendered confirmation: 剤.md, 洗剤.md:28 and 洗.md:38

**Result:** All three passages are confirmed as they render, with no findings. The captures turned up no defects, and I propose no edits. My textual verdicts from the initial review carry over unchanged.

## Snapshot
- **Teaching content:** 233d3add2b90fcb98f9706b8901aa936fc6e56e7. The packet's teaching diff from the initial review to the evidence HEAD is empty.
- **Evidence HEAD:** 7e03dede82cd517518b7debb8918ff0390477b78.
- **Supplied receipts (not my own tests):**
  - Android test-only snapshot 1c1b7bf4, which retains production f9b59a2. It is not the latest app main.
  - Archive cefedeb6, imported once: 1121 kanji, 5073 words, 130 N1 cards, 0 problems, contentVersion 0cbdc2723b0433f2, reading parser epoch 1.
  - Emulator API 35, default font scale 1, offline. Two terminal success cases, no skips. Helper 5580 stopped.

## Scope
- **Model:** claude-opus-5.5, original session d41cdccb, view tool only, one call per message.
- **Read in full:**
  - My original report.
  - The entire visual-725 packet: route JSON, contact-sheet index, receipt and diff.
- **Images:** all 23 listed PNGs, viewed serially in order.
  - 3 original font panels.
  - 12 contact sheets covering 45 route captures. Each frame on these sheets is a resized copy.
  - 8 additional original-resolution captures.
- **Not viewed:** other originals. None were needed for legibility.

## Verdicts
Ratings are correctness / scoped coverage / rendered comprehensibility. "Textual" means carried over from my initial review.

| Passage | Correctness | Coverage | Rendered comprehensibility |
|---|---|---|---|
| New kanji\剤.md | CLEAN (textual) | CLEAN (textual) | CLEAN |
| words\洗剤.md:28 (component links) | CLEAN (textual) | CLEAN (textual) | CLEAN |
| kanji\洗.md:38 (洗剤 common-word line) | CLEAN (textual) | CLEAN (textual) | CLEAN |

**剤.md, rendered**
- The whole article is visible across the captures, from the header (10 strokes, radical 刀 no. 18 shown as right-hand 刂, N1 community list) through the metadata and provenance line.
- The mnemonic is labelled "not etymology".
- The reading table scrolls sideways. Unscrolled and scrolled captures together show all five rows in source order (ザイ, スイ, セイ, かる, けず.る), each with its complete source-only qualifier.
- The two qualifying paragraphs are visible, including the 刈る and 削る pointers and the statement that those words don't make 剤 an alternative spelling. There is no invented spelling 剤る.
- All four common words are visible, plus the 薬, 製剤, 推進剤 and 粘剤 ねり notes.

**洗剤.md:28 and 洗.md:38, rendered**
- 洗剤.md:28 shows both the 洗 and 剤 links. The soap nuance and the せっけん guard text are intact.
- 洗.md:38 renders as "洗剤 せんざい — detergent; cleaning agent", with the link.

## Runtime confirmation
- **Fonts:** In all four fonts (Gothic, Mincho, Textbook, Brush), 剤, 済, 剛 and 則 can be told apart, and 刀, 刂, 氵 and 洗 are visible. The standalone 刂 and 氵 look the same in every face, consistent with fallback rendering. I did not identify the fallback font.
- **Reading quiz:**
  - The on'yomi question offers ゴウ, ザイ, バイ, ツイ. Neither スイ nor セイ is a choice, and there is no kun question.
  - Feedback: "Correct! — on'yomi", then Session complete, 1 of 1, Done.
  - The full reference reading list in the feedback is not offered as answer keys.
- **Meaning quiz:** The pictured N1 choices are 冶 "smelt; work metals", 剤, 刑 "criminal punishment" and 剛 "sturdy; unyielding strength". None of the three distractors could also count as correct.
- **Drawing:**
  - The trace screen showed "Downloading the handwriting model".
  - The recall capture was a give-up ("Here is the kanji").
  - Trace feedback read "Well drawn!", graded by stroke shape only, with the handwriting model unavailable.
- **Navigation:** Forward, reverse, backlink and SystemBack captures are present for both 剤↔洗剤 and 洗↔洗剤.

## Findings
None established.

**My initial hypotheses, reconciled with the evidence:**
- **薬 overlapping 剤 in quiz pools:** 薬 is absent from every sampled pool, and no sampled label overlaps "medicinal preparation; chemical agent".
  - Pools sampled: N1, All, bounded custom and random N1 subset, 16 seeds each.
  - Status: closed for the tested samples only. It stays UNVERIFIED for the wider and future pools.
- **Wrong-choice exposure of 済, 剛 and 則:**
  - Default N1 screen: only 剛 appears, plus production fallbacks.
  - All and custom pools: 剛, 済 and 則.
  - None of the 35 sampled labels, nor the pictured 冶, could also count as correct.
- **Older app versions ignoring the quiz reading selection:** the tested build offers only ざい. Other app versions remain unverified.
- **Direct word guards (128 checks):** none of the sampled distractors could also count as correct.
  - The closest are 掃除 "cleaning", 清掃 "cleaning; cleanup", 洗濯 "laundry" and 雑巾 "cleaning cloth". They are activities or tools, not cleaning agents.
  - Sample safety is not proof for the whole pool.

## Optional
- 剤.md:51 could say outright that the 斉 block sits on the right in 済 but on the left in 剤. This carries over from my initial review.
- The reading feedback lists ザイ、スイ、セイ、かる、けずる without qualification. A short "reference readings" label would help, though the article directly below explains each one.
- On narrow screens, せんざい breaks mid-word after 洗剤. This is cosmetic.

## Limits
- **Contact sheets are resized.** Some captures share a hash and so are duplicates. These are 48 captures, not 48 independent renderings.
- **The 84 Paint probes are not viewed images.** I did not judge legibility from hashes, hasGlyph or cmap.
- **The top of the 洗剤 article was not captured.** Its title, primary reading, N2 metadata and first example are not shown. I relied on the packet text for those.
- **Link targets were not checked.** 刈る, 削る and 刀 render as links, but their target pages weren't captured.
- **No real drawing evidence.** The strokes were injected and recognition was by shape only. This is not human handwriting, a successful ML Kit result or a phone test.
- **No independent verification.** I did no Git, upstream or CI checks and measured no learning effectiveness. Only bounded test configurations are covered.
- **Remaining gates:** combined current-main checks, CI, public ZIP, publication, phone, general release and whole-set gates.
