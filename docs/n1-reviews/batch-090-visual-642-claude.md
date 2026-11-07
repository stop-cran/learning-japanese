# Batch 090 visual follow-up report: 刀 and 日本刀

The screenshots establish no defects. All six items stay CLEAN in all three areas checked: correctness, scoped coverage and on-screen readability.

## Snapshot
- Frozen signed HEAD is `8308d49fce923789c9b2126ff71b0b581a44c849`. The teaching content is unchanged from the original snapshot `e044e953133548dd37fdf1dba449de2f4ee7575f`; the packet's teaching diff between the two is empty.
- This is a dependent follow-up in my original session (`63fa1d59…`). It adds to my initial text report and does not replace it.

## Scope
- **Model:** Claude Opus 5.5 (`claude-opus-5.5`). Only the `view` tool was used, one call per response, in order.
- **Text reads (2):**
  1. My own `docs\n1-reviews\batch-090-initial-claude.md`.
  2. The entire `control\batch-090-visual-642-packet.txt`, read with `forceReadLargeFiles`. No truncation marker appeared.
- **Image reads (14):**
  - Contact sheets `inspection\contact-01.png` through `contact-11.png`, covering all 64 captures. These are resized by the tool.
  - The three original Compose font panels: `retry1\n1-090-font-panel-1.png`, `-2.png` and `-3.png`.
  - No other original captures were opened.
  - Part of this session's earlier context was summarised. My notes on contact-01 to contact-04 come from that summary.
- **Items assessed:**
  - New `kanji\刀.md` and new `words\日本刀.md`.
  - Four changed lines in reused articles: `words\刀.md:24`, `words\剃刀.md:25`, `kanji\日.md:48` and `kanji\本.md:37`.
  - Unchanged legacy articles were not assessed and are not approved.

## Verdicts
Text correctness is inherited from my initial review unless an image shows otherwise. None did.

| Item | Correctness | Scoped coverage | Readable on screen |
|---|---|---|---|
| `kanji\刀.md` (new) | CLEAN (inherited) | CLEAN | CLEAN |
| `words\日本刀.md` (new) | CLEAN (inherited) | CLEAN | CLEAN |
| `words\刀.md:24` | CLEAN (inherited) | CLEAN | CLEAN |
| `words\剃刀.md:25` | CLEAN (inherited) | CLEAN | CLEAN |
| `kanji\日.md:48` | CLEAN (inherited) | CLEAN | CLEAN |
| `kanji\本.md:37` | CLEAN (inherited) | CLEAN | CLEAN |

CLEAN means no established actionable defect. It does not mean the content is exhaustively correct.

### What the screenshots show

**刀 kanji card (complete article)**
- The header reads "Strokes 2 · radical 刀 (no. 18) · N1 (community list)".
- The mnemonic is labelled "Modern-shape mnemonic, not etymology".
- **Reading table:**
  - It is clipped on a static screen, but scrolled captures `kanji-11`, `-14`, `-17` and `-18` expose every row in full.
  - Readings appear in source order, each on its own row: トウ (on) → 日本刀, かたな (kun) → 刀, そり ("kun, source-only here").
  - The そり row says no independently allocated word example is established here. It does not call そり nonexistent or archaic.
  - The 剃刀/かみそり paragraph says the kana ending そり is not by itself evidence that 刀 supplies that reading.
- **Notes:**
  - 力 "crosses", while in 刀 the stroke "starts inside".
  - 乃, 凹 and 凸 are contrasted with 刀's sword/blade meaning.
  - The とう-only scalpel and engraving-tool senses do not carry over to かたな.

**日本刀 word article (complete article)**
- It covers the traditional-sword meaning.
- It includes both neutral museum/photo example sentences with readings and translations.
- It notes the を/の particle usage.
- It explains 日本 as the country name, "not as a new literal 'sun + book'".
- It gives both にほんとう and にっぽんとう with no frequency ranking and "not as a general rule".
- It distinguishes the katana subtype and the ナイフ/包丁/剃刀 tools.
- Its curvature claim is hedged.

**Four changed passages**
- Each renders with a working link.
- Forward, backlink, reverse and system-back screens complete for all five pairs, across the 刀, 剃刀, 日 and 本 routes.

**Quizzes**
- **Meaning question:** "sword; blade" appears against "thereupon; possessive no" (乃), "concave; sunken" (凹) and "convex; protruding" (凸). The answer is marked Correct!.
- **Reading questions:**
  - The on question offers トウ/オウ/ナイ/トツ, and トウ is correct.
  - The kun question offers へこむ/でこ/かえで/かたな, and かたな is correct.
  - The result reads "2 of 2". そり is not asked, though it appears in the raw reference feedback line.
- **Selection screen:** "N1 · 122 cards".

**Drawing**
- The reference shows two strokes, with stroke 2 starting inside the hook.
- After the injected trace, the feedback says "Well drawn!" with the shape-only notice "handwriting model not available".
- The recall give-up screen shows the answer strokes.

**Font panels**
- All 18 scoped Han render in Gothic, Mincho, Textbook and Brush (panels 1 and 2).
- In panel 3, 力's slanting stroke rises above the top bar, while 刀's starts at or below it, in all four fonts.
- 乃, 凹 and 凸 are clearly distinct.
- The glyphs are small, about 40 px, but distinguishable.
- Gothic and Mincho look very similar, which may mean a shared fallback font. There is no requirement for the fonts to look uniform.

## Findings
- **Proved defects:** none.
- **Hypotheses:** possible overlap with "sword"/"blade" cards outside the packet. This is unchanged from my initial review, with low confidence.

## Optional
- Line breaks split kana inside words, such as "と|う-only" and "にっぽんと|う". This is cosmetic, but a non-breaking construction would help.
- My earlier suggestions stand:
  - Harmonise 刀.md:44 "starts inside" with 力.md "starts on it".
  - Note that the knife-money sense is also とう-only.
  - Add a hedged, cited pictograph origin.
  - Add plain-text トウ compounds such as 短刀 たんとう and 木刀 ぼくとう.

## Limits
- **Fallback limit:** my earlier "fallback unverified" limit is closed only for the tested N1 (122) and All (1113) pools. Three curated wrong answers and zero fallback options are pictured for N1; the All pool is a supplied receipt only. Future custom pools and old clients remain uncertified.
- **Supplied receipts, not my tests:**
  - The content-sync receipt for the full archive (`40bc5a55`).
  - Full/Lite agreement and the persisted progress keys.
  - The two native terminal success cases.
- **Test build:** the test-only Android build `1c1b7bf4` keeps production `f9b59a2` and is not the latest app main.
- **Images:** contact sheets are resized by the tool. The original font panels are small.
- **Font probes:** the 72 individual + 4 whole-word Paint probes are recycled hashes. They are not 76 exported PNGs, I did not view them, and no fallback face was identified.
- **Device:** API 35 emulator only. No physical phone, native-speaker, human-handwriting or offline ML Kit evidence, and no measured learning effectiveness.
- **Reading key:** にっぽんとう is explanatory text, not a second word-quiz key.
- **Not done:** no independent Git or upstream dictionary retrieval.
- **My original report stands:** its provenance and read limits are preserved, including the unconfirmed packet byte/line counts and the 194-family count.
- **Later gates still open:** current main, combined checks, CI, public ZIP, publication, phone, general release and the whole set.
