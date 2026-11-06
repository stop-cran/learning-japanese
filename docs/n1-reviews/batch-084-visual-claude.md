# Batch 084 凜: final visual-confirmation report

I found no actionable defect in either new article: both are CLEAN for correctness, scoped coverage and rendered comprehensibility. All the article text was legible across the screenshots, with no blank areas, replacement boxes or collapsed look-alike characters. The one gap is small-size rendering of the variant 凛, which I could only partly confirm.

## Snapshot
- **Teaching content:** 030b144a6aeefc6fe77f76683219832db91bef4f, unchanged according to the packet.
- **Evidence:** HEAD a445a3f154afd5833fa99ba0c6abe13379402e1f; native envelope 53b6819b22787a2517cd0ad14aa855d357cbc70a, content version 74b87b47347b78c1.
- I did not check Git, the hashes or upstream sources myself.

## Scope
- **Model and session:** Claude Opus 5.5 (claude-opus-5.5), continuing the original Batch 084 session. This is a follow-up visual check that depends on my earlier reports, not a new blind language review.
- **What I read:** 26 single `view` calls, one per turn. The first was the complete `batch-084-visual-source-packet.txt`, with no truncation shown. The other 25 were these PNGs:
  - quiz and session screens: curated-on-done, curated-On-feedback, curated-On-question, meaning-question, meaning-feedback, selection;
  - drawing screens: drawing-trace, drawing-feedback, drawing-recall-feedback;
  - font panels 1–3;
  - kanji article: kanji-01, -03, -06, -12, -18;
  - word article: word-02, -03, -07, -09, -12;
  - navigation: word-kanji-backlink, word-reverse, word-system-back-to-kanji.
- **Unverified mapping:** the host says these 25 stand for all 42 captures after removing exact-byte duplicates. I did not verify that mapping. word-forward and the second system-back capture were not served separately.
- **Image size:** each image came back at about 900×2000 and may have been downscaled. I judged only those returned pixels and claim nothing about the original full-resolution bytes.
- **Earlier reports:** the dictionary findings from my initial review and reconciliation stand as written. This stage did not re-review the dictionary families.

## Verdicts

| Article | Correctness | Scoped coverage | Rendered comprehensibility |
|---|---|---|---|
| `kanji\凜.md` | CLEAN | CLEAN | CLEAN |
| `words\凜.md` | CLEAN | CLEAN | CLEAN |

CLEAN means I found no established actionable defect in scope. It is not a guarantee of exhaustive correctness, a native-speaker check, or evidence that the articles help learners.

## Findings
**Proven defects:** none.

What the screenshots confirm:
- **Readings:**
  - The table lists リン (on) then きびし.い (kun), in source order.
  - It says "Only リン is selected… no selected kun questions".
  - The reading quiz offered only リン, against ジュン/オウ/ジョウ.
  - The きびし.い row is marked source-only, and the 凜しい/厳しい paragraph says it is a bounded evidence limit, not a claim the form cannot exist.
  - The table is clipped at the right edge in single frames, but across kanji-01, -03, -06 and -12 every cell's text is present, and the "Scroll sideways" note explains it.
- **Facts and notes:** both are shown in full.
  - The facts line shows 15 strokes, radical 冫 ("the two left-hand marks, no. 15") and "N1 (community list)".
  - The mnemonic is labelled "invented memory aid, not a verified historical or phonetic explanation".
  - The notes say grade 9 means a name-use kanji, not name-only usage.
- **Shapes:**
  - The large 凜 (quiz prompts, tracing guide, stroke panels) clearly has the two 冫 marks, 亠, 回 and a 禾 bottom.
  - 禾 and 示 are clearly different in all four font families.
  - The notes explain the 禾 versus 示 contrast and that the two are different characters for typing and card identity. 凛 and 稟 are plain text.
- **Word article:**
  - The 凜と / 凜とした + noun constructions are explained, with the warning against treating it as an ordinary な-adjective, the point that とした does not have to mean an earlier change, and the qualified taru-adjective / adverb classification.
  - Both Daijisen examples have kana and translations, and the morning example is identified as a noun phrase.
  - The 寒い/厳しい/澄む/冷静 comparisons and the rank/moral/"strict" cautions are legible, as are the scope note on the tense-atmosphere sense and the sources line (JMdict 1564320, Daijisen, Seisen).
- **Meaning quiz:** the four choices are exactly 凜, 准, 冗 and 凹 ("dignified; bracing cold", "quasi-; associate rank", "superfluous; redundant", "concave; sunken"), with no filler from other cards. The N1 selection screen shows 116 cards.
- **Links and offline:** the screens are consistent with links working in both directions and with system Back keeping the scroll position. Offline mode is shown honestly ("handwriting model not available"). The fact that each screen came from a particular navigation step rests on the route evidence and filenames, not the pixels.

**Carried forward from earlier reports:**
- **C1 (the word article says "JMdict also recognizes 凛", though JMdict lists 凛 first, with newspaper-frequency tags):** OPTIONAL. Shown at word-02, -07 and -09. I still disagree mildly with the wording; low impact on learners.
- **C2 (possible overlap with 涼しい):** WITHDRAWN.
- **C3 (quiz exposure):**
  - The default quiz is RESOLVED: confirmed both in the packet and on screen.
  - Larger, random, custom, padded or reverse quiz pools remain UNVERIFIED and are not claimed safe.

## Observations on app behaviour (optional, not article defects)
1. **Reading feedback:** after the on-reading question, the feedback line reads "dignified; bracing cold: リン、きびしい". It shows the source-only kun with no qualifier, unlike the article. This is low severity and app-level; at most, consider marking or omitting non-selected readings there. The meaning-quiz feedback shows the title only.
2. **Drawing wording:** "Practice only: this attempt is not graded" sits next to "Graded by stroke shapes only", which could read as contradictory. Wording only.
3. **Model download message:** the tracing screen showed "Downloading the handwriting model (first use only)…" while offline. Later screens say "not available". This was a transient status; there is no claim of a successful download.

My original optional suggestions remain optional: briefly explain the taru adjective (凜たる), add an attested 凜と + verb example, mention 凜々しい (りりしい), and simplify the "strict" sentence.

## Limits and how the earlier rendering uncertainty settled
- **Resolved:**
  - The 凜 glyph renders as 禾-bottomed at large size, with the two 冫 marks visible.
  - All 28 scoped Han render in Gothic, Mincho, Textbook and Brush across the three panels, with no blank areas or replacement boxes.
  - Typeface fallback to a Gothic-like face for 冫, 凛, 凜 and 稟 in Textbook and Brush is a typeface change only.
  - Article scroll states and table columns are complete when judged together, and the whole-word wraps (冷/静, 寒/い, the Textbook た) keep all the text.
- **Partially resolved:** 凛 versus 凜 at small and body-text sizes.
  - Panel 3 shows them as distinct with moderate confidence; panel 1 was too small to decide.
  - 凛 never appeared at large size, so its 示 bottom is confirmed only at small size, supported by the within-family raster-hash difference, which is not proof of readability.
  - Some stroke-number labels (13–15) were crowded, and fine strokes of 険 and 鷹 at panel size were unresolved.
- **Unresolved:** safety in larger or custom quiz pools (C3); real handwriting recognition (the strokes were injected from reference data, and the ML Kit model was unavailable); human handwriting.
- **Evidence I relied on but did not see in pixels:** the fixture, route, persisted-log and curation evidence. That includes the claim that two tests passed on run 587, the inherited host and compile results, the synthetic progress data, and the 1096/5053/116 content counts.
- **Not established, and separate from this review:**
  - Hardware: no physical phone or native-font check on a device; the test device was an API 35 emulator.
  - Release steps: latest-main merge, combined checks, signing, owner push, remote CI, public ZIP hashes, archive guards and owner issue 60.
  - Scope: general release and the whole N1 set.
  - Learning effectiveness: not measured.
  - My own checks: no independent Git, hash or upstream lookups.
- **Process:** no reads were denied or missing within the 26 resources I was assigned; I made no edits and reread nothing.
