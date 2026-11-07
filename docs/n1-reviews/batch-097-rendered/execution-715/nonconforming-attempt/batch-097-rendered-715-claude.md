# Batch 097 rendered confirmation — 剣 kanji, 剣 つるぎ word, reused 真剣 and 真

I found no defects in the four assigned scopes or in the rendered and quiz checks. Every scope is CLEAN for correctness, coverage and comprehensibility.

## Snapshot
- **Content and archive:** content HEAD e75b4bb14ba5ee3183a973be7752033721a5246e; native full archive 83e5c090.
- **Teaching content:** reviewed teaching 1fa1ac69 is unchanged; version a066afceaf1f447a.
- **Native build:** native run 714 used a TEST-ONLY Android build, 1c1b7bf4, which keeps production f9b59a2. This is not the latest app main.
- **Teaching edits:** none happened during this review.

## Scope
- **Model and session:** claude-opus-5.5, my original session 3a0b6dd8. This is a dependent confirmation, not a fresh blind review.
- **Text read:** all 16 chunks, `batch-097-rendered-claude-packet-715-01..16.txt`, in order, one view call each, none truncated. They contained:
  - my original report;
  - both complete new articles and both complete reused articles, with the exact diff (words\真剣 line 27, kanji\真 line 37);
  - the main and comparison JMdict files and the public dictionary text;
  - the native assertions and quiz contract;
  - all 64 kanji answer-choice records;
  - the label dictionary and all 512 word-guard records;
  - the contact-sheet index.
- **Images viewed:** font panels 1–3 and contact sheets 01–13, covering all 52 remaining screenshots. The sheets are at reduced scale. I opened no original PNGs, because nothing at reduced scale was ambiguous enough to need it.
- **Left out of this packet:** the raw metadata and the 18 comparison article bodies. I reviewed those only in the initial session, and this is not a new review of all 137 JMdict families.

## Verdicts
Each part is rated for correctness, scoped coverage and text comprehensibility.

| Part | Correctness | Coverage | Comprehensibility |
|---|---|---|---|
| kanji\剣.md (new) | CLEAN | CLEAN | CLEAN |
| words\剣.md, つるぎ (new) | CLEAN | CLEAN | CLEAN |
| words\真剣.md line 27 (changed) | CLEAN | CLEAN | CLEAN |
| kanji\真.md line 37 (changed) | CLEAN | CLEAN | CLEAN |
| Bounded rendered and quiz checks | CLEAN | CLEAN | CLEAN |

## Findings
None proved. What the evidence shows:

- **Glyphs:** all 20 Han render in all four fonts, and the right-hand 刂 is visible in each. 剣, 剛, 剖 and 則 can be told apart. 刃 shows a 刄-style variant in three fonts, which is acceptable.
- **Reading quiz:** both ケン and つるぎ are asked, with Done "2 of 2 answers correct".
- **Drawing:** the stroke-trace screen showed "Well drawn!" with the note that grading used stroke shapes only, and give-up recall works.
- **Meaning quiz:** the wrong options are 剖, 剛 and 蚊 (mosquito). None of them could also be a correct answer.
- **Kanji answer choices (64 records):** none of the fallback labels means sword or blade. 矛 "spear; polearm" shares the weapon domain but is not an equivalent answer.
- **Word guards (512 records):** the four direct guards hold in every case — 剣 with 刀, 日本刀, 刃 and 真剣. I found no consequential ambiguity among the other options; the closest is 積極的 for 真剣, below.
- **Navigation:** all three reciprocal pairs work in all six directions, the one activated baseline pair works, and System Back returns correctly.
- **Text layout:** the articles wrap cleanly at phone width.

## Reconciliation
- **Resolved:** my hypothesis that fallback options could bring in 刃 or 刀. The guards hold, and the actual fallback is 蚊.
- **Partly resolved:** whether `kanji\口.md` exists. 口 renders as a link, but I did not check the file itself.
- **Unresolved, not a defect:** whether standalone 剣 is read けん more often than つるぎ. Both readings are presented as valid, so nothing needs to change.
- **New, not a defect:** 積極的 "proactive; active" appears in every 真剣 guard row. It is a related attitude word but not equivalent to serious/earnest.
- **Withdrawn:** none.
- **Kept as optional:** my original suggestions, listed below.

## Optional
- From the initial review: a sourced note on つるぎ vs けん register; clearer wording for the zoological senses; the clock-hand sense (短剣/長剣); the old forms 劍/劒.
- At its default position, the readings table cuts off "serious; earne…". The hint and the sideways-scrolled captures show the full text. Polish only.
- A stray mark near the top of some scrolled screens is most likely the cut-off bottom of the previous line. It is cosmetic and unconfirmed.

## Limits
- I did no independent Git or upstream checks, and no gaiji (non-standard characters in the dictionary source) were decoded.
- The screens came from an API 35 emulator. There is no physical-phone evidence and no human handwriting or ML Kit evidence; the ten injected reference strokes do not certify either.
- The contact sheets are reduced scale.
- I ran no native tests myself.
- I make no claim about learning effectiveness, a general release, the whole set or publication.
