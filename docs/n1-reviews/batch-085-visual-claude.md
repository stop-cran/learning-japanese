# Batch 085: dependent visual confirmation, final report

## Snapshot
- **Evidence HEAD:** 6921ddbd75e93e43974d2e9340f41c7f8848e626, as stated in the host's source packet.
- **Teaching content:** my initial snapshot a7512a5e plus the 努力 exclusion in `words\凝らす.md`. The packet gives that as commit 29a53380, content envelope 1d2e3290 and content version 0c514711ae8d3212.
- **Article hashes in the packet:** 凝 41ea4033…, 凝固 e156f599…, 凝る 14ee1bf1…, revised 凝らす 40d5f79a…, 固 3ec01320…. They match the earlier packets.
- **Build tested:** test-only Android build 1c1b7bf4 on top of unchanged production f9b59a2. This is not the latest app main.
- **Not independently checked:** I verified none of this with Git or upstream sources.

## Scope
- **Model and session:** Claude Opus 5.5 (`claude-opus-5.5`). This is the original session resumed after a context summary, and it is a dependent confirmation, not a new blind review.
- **Reads:** 24 serial `view` calls, one per resource, with `forceReadLargeFiles=true` and no `view_range`. There were no denials, shell, edits, delegation, parallel calls or unassigned reads.
  - **Source packet:** read in full, with no truncation marker.
  - **15 sheets:** 14 × 6 + 3 = 87 frames, matching the stated 87 originals. I didn't compare this against a separate file listing.
  - **8 focused originals:** font panels 1–3, drawing-feedback, kanji-20, effort-13, curated-Kun-feedback and absorbed-14.
- **Image resolution:** the sheets are thumbnails, and the tool may have resized every image again. So this was 87 frames at reduced resolution plus 8 originals at closer to full resolution, not 87 full-resolution reads. Small kana, link underlines, labels where stroke numbers overlap, and fine Brush-style strokes were only just readable.

## Verdicts
CLEAN means no actionable defect was established in what I observed for this scope. It is not exhaustive certification. "Comprehensibility" here means the rendered text reads clearly on the emulator; it is not native-speaker certification.

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\凝.md` | CLEAN | CLEAN | CLEAN |
| `words\凝固.md` | CLEAN | CLEAN | CLEAN |
| `words\凝る.md` | CLEAN | CLEAN | CLEAN |
| `words\凝らす.md` | CLEAN | CLEAN | CLEAN |

- **Changed 固 Common words bullet:** CLEAN.
  - I saw it rendered fresh in solid-back-to-reused-kanji and solid-changed-bullet: "凝固 ぎょうこ — coagulation; solidification". The link resolves and the reading and gloss are correct.
  - The rest of 固 was not reviewed fresh; it is unchanged baseline content.

## Findings
**Proved defects: none new.**

**Earlier finding (not new):** the 凝らす/努力 quiz exclusion.
- Minor; quiz coverage; `words\凝らす.md:4,8`.
- **Resolved** by my textual confirmation, high confidence.
- This visual run shows no regression, but it doesn't directly show the exclusion working, because no 努力 choice appears in any captured quiz.

**What the pixels support:**
- **Rendered text:** the Japanese, kana, examples and English translations all match the source in every article. None of the cut-off text I saw was lost content; it was screen edges or table scrolling.
- **Readings table:**
  - The "Scroll sideways" hint is always shown.
  - Between the unscrolled and scrolled frames, every cell can be read. kanji-26 and -27 show the end of the こご.る cell ("usually written in kana as こごる").
- **Glyphs:**
  - All 39 Han characters appear in all four font families. There are no blank glyphs or tofu boxes.
  - The lookalikes stay distinct: 凝/疑, 准/隹, 冫 versus 隹, 冗/凹, 凍/凝, 固/硬.
  - The whole words 凝固, 凝る and 凝らす render correctly.
  - In Mincho and Textbook, 隹 looks heavier, which suggests a fallback font. That is a typeface change only, and I can't tell from pixels which font supplied it.
- **Meaning quiz:** the choices are congeal; become absorbed / quasi-; associate rank / superfluous; redundant / concave; sunken, with no padding choices.
- **Reading quizzes:**
  - On'yomi: ギョウ against ジュン / オウ / ジョウ.
  - Kun'yomi: こる against こい / こずえ / へこむ. こらす is not offered as a separate answer.
  - The feedback screens show all six readings. The done screen shows 2 of 2 correct.
- **Selection screen:** "N1 · 117 cards"; readings 2 due, meaning 1 due, drawing 1 new.
- **Drawing:**
  - Trace stage, then feedback ("not graded", "Well drawn!"), then recall give-up ("Here is the kanji"), with 16 numbered strokes.
  - "Handwriting model not available" is consistent with the run being offline.
- **Navigation:** forward, reverse and system-back work for all three words.

## Optional
These are unchanged from my earlier reports; none is required:
- `凝る.md:23`: the "despite ending in る" wording.
- `凝る.md`: an Nに凝る example for "be particular about", such as 家のつくりに凝る. It is still absent in the rendered article.
- `凝らす.md:51`: JMdict flags 懲らす as "dated"; the article doesn't say so.
- `凝らす.md:49`: 凝らせる is also the causative of こる.
- `凝固.md:41`: repeats the "not ice" point from line 22.
- `固.md:40`: uses an em dash where its neighbours use " - ". The rendered app confirms this; it is cosmetic.

One new cosmetic observation:
- **Possible spacing gap:** before "（くふうをこらす）" in the Meaning section of 凝らす, seen only on sheet 5 thumbnails.
- **Correction:** in my resource-22 note I said the gap doesn't appear in effort-13. That frame doesn't contain the sentence at all, so the gap remains unverified at full resolution.
- **Unrelated to this batch:** the drawing screen says both "not graded" and "Graded by stroke shapes only". That wording is shared across the app, so it is not a batch finding.

## Limits
**My earlier unknowns:**

| Unknown | Status | Basis |
|---|---|---|
| Font and glyph rendering | Partially resolved | Emulator pixels only; the fallback font is not identified; the 40 historical fallback characters were inherited, not re-inspected |
| Default four-choice quiz exposure | Resolved for the default pools | Pixels plus packet route data |
| Regenerated manifest | Partially resolved | Content import is consistent with the packet's single import and zero problems; I never saw the manifest itself |
| Quiz safety in larger or random pools | Unresolved | Words such as 専念 and 頑張る, and complete families, were not checked |
| Drawing | Partially resolved | Injected reference strokes only; no human handwriting or ML Kit |
| Stroke order and direction | Not certified | Labels overlap at this resolution |

**Outstanding gates, separate from the above:**
- physical phone, general release, current-main integration, publication, CI and immutable ZIP;
- whole-set coverage and owner progress;
- native-speaker review and corpus checks;
- measured learning effectiveness.
