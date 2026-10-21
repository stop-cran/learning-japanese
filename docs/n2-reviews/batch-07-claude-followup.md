## Snapshot
cce24eef4c57704c3a40fbc490fa80dc694bec50, clean committed files only (original snapshot 860f2cdc0f63e420ebc83e6e2a719cc66d1f58a6). I had file tools only and could not run Git. Commit identity, clean status and diff provenance rest on the author's confirmation; I read the files on disk and checked them against the supplied diff.

## Scope
- **Model:** claude-opus-5.5, Claude family; worked alone and in order, read-only.
- **Read in full:** `n2-batch-07-corrections.diff` (three files), `kanji\布.md`, `words\巻く.md`, `words\干す.md`, and my original report.
- **Evidence:** `batch-07.json` lines 1-20, 478-500, 1615-1660, 1795-2045 and the packet's full list of meanings for 巻く/干す/庁, plus a count confirming 54 records. Also `docs\content-format.md:36-46, 60-130`.
- **Related pages:**
  - front matter and the relevant lines of `kanji\干.md`, `kanji\巻.md`, and the 風, くるくる, ぐるぐる, 包む, 乾く, 布 and 生地 word articles;
  - `scenes\くるくる.json` and `scenes\ぐるぐる.json` (picture-quiz files);
  - all word titles containing "air" or "dry", from the earlier search.
- **Not reviewed:** the other 15 new pages and all older teaching text (unchanged from the initial review), `manifest.json`, validator output, and the app's code for choosing quiz options.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\布.md | CLEAN | CLEAN | CLEAN |
| words\巻く.md | NEEDS FIX (B07-R1) | CLEAN | CLEAN |
| words\干す.md | CLEAN | CLEAN | CLEAN |

## Findings
**B07-R1 — Minor — Correctness (quiz answer labels) — `words\巻く.md:8`**
- **Claim:** The correction excludes くるくる because "coiling around" partly overlaps 巻く's title "wind; coil; roll up". ぐるぐる has the same overlap: its title is "round and round; winding around" (`words\ぐるぐる.md:4`). Its own exclusion list, [くるくる, 回り], does not include 巻く. Exclusions only work pair by pair, so excluding 巻く/くるくる and くるくる/ぐるぐる still leaves 巻く/ぐるぐる allowed together (`content-format.md:86`).
- **Picture quiz:** Exclusions also apply to picture questions (`content-format.md:127`). ぐるぐる's quiz-eligible scene "winding-string-around-box" shows hands winding string around a box. If 巻く is offered with that picture, it is a defensible answer.
- **Threshold:** The documented rule for adding an exclusion is met (`content-format.md:94-96`).
- **Remedy:** Change `words\巻く.md:8` to `quiz_exclusions: [包む, 風, くるくる, ぐるぐる]`.
- **Evidence:** `scenes\ぐるぐる.json` (scene id winding-string-around-box, quizEligible true); `words\ぐるぐる.md:4, 8, 20`. Both words are tagged wago.
- **Confidence:** Medium. The overlap is certain; how often the two appear together depends on app code I didn't inspect.

**Original findings, reconciled:**
- **B07-F1: resolved.** Line 31 now glosses 布く with the meanings the source ties to that spelling (promulgate, lay railway tracks, deploy troops). Line 48 states that this spelling is noted only for senses 3, 5 and 6, not for spreading a futon, and that 敷く is the main spelling. The "search-only" qualification is kept. The packet matches: lines 1799-1800, the notes at 1823/1860/1877, sense 1's empty notes at 1814-1823, and the spelling list at 1941-1953. There's no regression.
- **B07-F2: resolved.** Line 47 adds the separate reading ぬのじ (entry 1591910, packet 1621-1655), the spelling 切れ地, and an explicit "do not assume" warning. The packet's own cross-reference (line 1982) supports this.
  - I withdraw my earlier proposed wording "usually read ぬのじ". ぬのじ has newspaper-frequency flags (news1, nf22), but missing flags on きれじ don't establish a relative ranking.
  - Correcting my original evidence: in the pinned record, 布地 is the fourth of five spellings, followed by the search-only きれ地, not "listed last".
  - The entry list at line 52 now includes 1591910, matching packet line 489.
- **B07-F3: resolved.** 風 is added to the exclusions. All targets exist, there are no duplicates or self-references, and none of the targets lists 巻く as a curated distractor.

## Optional
- **O1 and O2:** adopted. The 干す title "hang out to dry; air out" now reads clearly as a verb, so it no longer competes with the noun titles 空気, 大気, 冷房, 気温 and 航空. No other title contains "air out", and the heading is updated to match.
  - The くるくる exclusion is also supported by its quiz-eligible "winding-ribbon" scene.
- **O3:** withdrawn. Citing senses 1-2 for 干す is justified because the body mentions draining.
- **New O6:** `kanji\干.md:29, 36` still gloss 干す as "air; dry". This is unchanged and not a quiz label; aligning it to "air out" would be cosmetic.
- **New O7:** the 布 table row for きれ (line 32) could add "(also ぬのじ)" so the warning is visible without reading the Notes. In line 48, "sense 1's futon example" would read more clearly than "its futon example".

## Limits
- I couldn't run Git, so commit identity, status and diff provenance are unverified.
- I didn't check `manifest.json` or run the validator.
- B07-R1's real-world frequency depends on app code I didn't inspect.
- I didn't consult raw JMdict beyond the packet. My public checks of 布く and 布地 came from the original session.
- Naturalness was judged by a non-native reader; this is not native-speaker certification.
