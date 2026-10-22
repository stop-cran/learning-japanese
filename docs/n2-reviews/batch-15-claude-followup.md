## Snapshot
I reviewed revised commit `356a4582d1ea1d335474b8cdc6e3d07b5878c43a`, committed files only. My original blind review was of `9f6464f5255dd6ece56e4c949a7a3102ae38fbcb`. I had file tools only, with no Git and no ability to run anything. So I could not confirm HEAD, the clean status, the 12-file scope, or the patch's match to the commit. I relied on the author for those.

## Scope
- **Reviewer:** claude-opus-5.5 (family claude), resuming session 98ba540b-efbf-4d9f-9b8f-a2d96b0bb813. I worked alone and made no edits.
- **Read:**
  - The supplied patch, which touches five teaching files.
  - All five revised pages in full: `kanji\玉.md`, `甘.md`, `略.md`, `硬.md` and `磨.md`. Every changed hunk matches the post-patch text of the patch.
  - My archived `docs\n2-reviews\batch-15-claude-initial.md`.
- **Evidence checked:**
  - `batch-15.json`: lines 1–60 and 400–440 (玉 metadata and the new `externalSources` record), entry 1921990 (lines 626–760), entry 1240530 (761–1085) and entry 1310460 (1854–1968).
  - Link targets: `words\ほぼ`, `上手い`, `固い`, `堅い`, `する`, and `kanji\全`.
  - Kotobank's 玉 page, fetched 2026-10-22.
- **Not re-read:**
  - The other 10 cards, `words\家畜`, `words\略語` and the 19 link-only passages. The author says these are unchanged; I did not verify that.
  - The stroke files, `manifest.json`, the validator, and any other files among the 12 in the correction. I only checked the `batch-15.json` sections listed above.
  - The forbidden reports and authoring notes.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 玉 | CLEAN | CLEAN | CLEAN |
| 甘 | CLEAN | CLEAN | CLEAN |
| 略 | CLEAN | CLEAN | CLEAN |
| 硬 | CLEAN | CLEAN | CLEAN |
| 磨 | CLEAN | CLEAN | CLEAN |

Reading rows on these five cards are unchanged: 玉 4, 甘 5, 略 7 (5 source-only), 硬 2, 磨 3.

## Findings
**F1 (玉 distractor): resolved.**
- `kanji\玉.md:11` now uses distractors `[全, 主, 生]`.
- 全's title is "whole; complete" (`kanji\全.md:3`). That meaning does not appear in KANJIDIC's 玉 meanings ("jewel, ball", `batch-15.json:39-42`), in entry 1240530 senses 1–17, or in entry 1921990 senses 1–7.
- 全 still works as a look-alike: its own card describes a "王-shaped stack" (`kanji\全.md:20`).
- The new Note at line 42 is accurate:
  - JMdict 1921990 sense 7 gives "king (of the junior player)", tagged as an abbreviation (`batch-15.json:726-741`).
  - The fetched Daijisen entry ぎょく【玉】 sense 5 reads 将棋の駒の「玉将」の略.
  - The new citation at line 46 points to that same headword and sense, and it is recorded in `batch-15.json:419-422`.
- Confidence: high.

**F2 (略 link to ほぼ): resolved.**
- `kanji\略.md:44` now links `../words/ほぼ.md`.
- That article covers entry 1551940 and says 略 is a rare spelling (`words\ほぼ.md:25`).
- Linking the Note rather than the table row satisfies the rule to link "at the substantive introduction or comparison".
- Confidence: high.

**F3 (甘 link to 上手い): resolved.**
- `kanji\甘.md:44` now links `../words/上手い.md`, which covers entry 1310460 read うまい.
- The card keeps the source's hedges:
  - "especially associated with 上手い and 巧い" matches sense 1 info "esp. 上手い, 巧い" (`batch-15.json:1882-1884`).
  - "especially associated with 旨い, 美味い and 甘い" (line 43) matches sense 2.
  - It keeps the caveat that not every spelling suits every sense.
- Confidence: high.

**F4 (硬 links to 固い and 堅い): resolved.**
- `kanji\硬.md:39` now links both word articles.
- Both targets are entry 1257110 and teach tendencies rather than absolute rules (`words\固い.md:29`, `words\堅い.md:27`).
- The card keeps "not a strict one-spelling/one-meaning division".
- Confidence: high.

**Adopted polish (from my original Optional notes):**
- `玉.md:41` now says "This card's separate ギョク row".
- `甘.md:32` and `磨.md:32` no longer repeat their labels. Each keeps one flag: "(usually written in kana)" and "(rare kanji spelling)".
- `磨.md:42` links `../words/する.md`, the irregular "do" (entry 1157170). The godan verb 磨る する (entry 1595910) stays separate.

**Regressions:** none found within this scope.

## Optional
- **Polish (nonblocking), `玉.md:42`:** "their meanings" follows a sentence that names both 王 and 主. "玉 and 王 are not completely disjoint in meaning" would make clear that 主 is not included.
- **Your declined items:**
  - **Components and 花瓶 readings:** I accept these as declined, since the 瓶 claim is limited to the linked かびん article.
  - **畜 citations:** I accept the shared-packet rationale and withdraw the suggestion.
- **Shared answer words:** pairs like 略/省 "omit" and 玉/球 "ball" are unchanged and still cannot appear in the same quiz.

## Limits
- **No Git or execution:** I could not confirm the commit, the 12-file scope, zero validator errors, the 225 additions and 701 reading rows, manifest determinism (version `b2f9502a329d51e7`), or the claims that the other pages are unchanged.
- **Not reviewed:** the stroke files, the manifest, and the runtime quiz behaviour, which I inferred from the docs.
- **Snapshot evidence:** the Kotobank check reflects the page as fetched on 2026-10-22.
- **Not a native-speaker certification.**
