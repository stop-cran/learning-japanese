# Batch 101 review: rendered confirmation of the 功 article and three navigation links

## Snapshot
- The evidence was captured at signed HEAD 69f542a1bc0b30ee0fba20f45f02aadcd9c30ce5. The teaching content is from snapshot 7f275e0de16fe3a4588fac1845af5af80d487415.
- The packet reports that teaching and runtime content did not change between the initial review and HEAD.

## Scope
- **Model:** Claude Opus 5.5 (claude-opus-5.5). I used only `view`, with one call per message and no batching.
- **Fresh reads:**
  - My own initial report, `batch-101-initial-claude.md`, read in full.
  - `control\batch-101-rendered-769-packet.txt`, read in full with no truncation shown.
- **Images:** all 26 listed PNGs, in order:
  - the 3 font panels;
  - the 8 contact sheets, which map 31 route captures and are downscaled 2×2;
  - the 15 standalone originals.
- **Images not opened separately:** the other route captures in the `native\` folder. The contact sheets were legible enough without them.
- **Inherited, not re-read:** `batch-101-initial-packet.txt`, which holds the 122 JMdict families, 18 raw records and the public dictionary text.
- **Scale:** each standalone PNG displayed at about 900×2000. I cannot confirm that this is the device's native resolution.

## Verdicts
The textual verdicts are inherited from my initial review, which found them CLEAN. The rendered verdicts are fresh.

| Scope | Correctness | Scoped coverage | Rendered comprehensibility |
|---|---|---|---|
| `kanji\功.md` (new) | CLEAN (inherited; nothing in the captures contradicts it) | CLEAN (inherited) | CLEAN |
| `words\功績.md:28` | CLEAN (inherited) | CLEAN | CLEAN (koseki-components: 功 is linked next to 績 and legible) |
| `words\成功.md:28` | CLEAN (inherited) | CLEAN | CLEAN (seiko-components: 功 is linked at the line end and legible) |
| `kanji\成.md:38` | CLEAN (inherited) | CLEAN | CLEAN (sei-new-reciprocal: the 成功 bullet is linked) |

What the captures show:

- **Fonts.** All 19 scoped Han characters appear in Gothic, Mincho, Textbook and Brush across the three panels. 功 can be told apart from 加, 幼, 刀, 工 and 力 in every font. 力 and 刀 remain distinct even in Brush, where only 力's stroke crosses the top. 功績, 成功 and 功徳 are legible.
- **Reading table.** Article-07 (unscrolled) and article-08/13 (scrolled sideways) together show every cell:
  - the コウ row with the 功績 and 成功 links;
  - the ク row: 功徳, "Recognition only.";
  - the いさお row: "Dated noun; recognition only.";
  - the full note saying that いさお is not merely a name reading.

  The clipping at the right edge comes only from the intended horizontal scroll.
- **Meaning quiz.** The default N1 options are 松 pine tree / 功 merit; achievement / 刀 sword; blade / 梨 pear tree. Each wrong choice is clearly wrong against the target and does not overlap with the other options.
- **Reading quiz.** The options are コウ, リョウ, ジョウ and トウ, so neither ク nor any kun reading is offered. The session completed with "1 of 1" correct.
- **Drawing.** The trace screen shows 5 numbered strokes. The feedback screen says the drawing was graded by stroke shape only.

## Reconciling my earlier concerns
- **Fallback options.** My initial limit was that the real fallback could not be checked, because the curated choices 加 and 幼 are outside N1. The pictured N1 options are 刀 (curated) plus two production fallbacks, 松 and 梨.
- **Sampled labels.** Across the 64 receipt samples, every fallback label defends as wrong for "merit; achievement":
  - 剛 "sturdy" and 凌 "endure; surpass" are close but distinct from merit.
  - 幹 is labelled "tree trunk; main part" only, without its "talent" sense.
  - None of the 13 guarded kanji appears in any sample.

  This settles only the tested configurations (16 seeds × 4 pools). Future pools are not covered.
- **The ク note.** I withdraw my earlier suggestion to say "mainly". "Valid reading in religious compounds" makes no exclusivity claim.

## Findings
None proved.

## Optional
- **Feedback reference line** (curated-on-feedback.png). The reference line lists "コウ、ク、いさお" with no recognition-only qualifier, unlike the article. This is generic app UI and the article directly below explains it.
- **績 article** (seki-counterpart-reciprocal.png, legacy, outside scope). It glosses 功績 as "meritorious service", while the new card says "meritorious contribution". Both are acceptable.
- **Carried over from my initial review:**
  - The いさお row could note that JMdict lists 勲 first.
  - Omitting Jitsu's 形声 (phonetic 工) analysis is acceptable.

## Limits
- **Device:** an emulator (API 35, font scale 1). No physical phone was tested.
- **Contact sheets:** downscaled, and several captures share identical hashes.
- **Recall capture:** it shows an empty "Your drawing" box with "Here is the kanji", which is a reveal state rather than a drawn recall. Grading was shape-only because the handwriting model was unavailable. This does not show human handwriting or MLKit working.
- **Supplied receipts, not my tests:** the 2912, 2496 and 896 guard checks, the import counts and SystemBack/offline. The six legacy 功績 word-guard titles remain UNVERIFIED.
- **成 reading-table cell:** never captured scrolled sideways. It is outside the change at line 38.
- **Still open:** independent Git or upstream verification, current main, CI, the public ZIP, publication, the phone check and whole-set release gates. No learning effect was measured.
