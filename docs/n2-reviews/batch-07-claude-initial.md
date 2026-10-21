## Snapshot
860f2cdc0f63e420ebc83e6e2a719cc66d1f58a6, committed files only. I had file tools but could not run Git. I read the files on disk and did not independently verify the commit identity, the clean worktree, the diff against baseline 52077285b9ca0f43adea4e1c9cd56e096b72ca6b, or the 56-file count; those rely on the author's confirmation. I made no edits.

## Scope
- **Model:** claude-opus-5.5 (Claude family), working alone and in order, with no delegation.
- **Guidance read:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md:18-109`, plus lines 36-46 and 76-87 again for citation.
- **New pages, read in full:** all 15 kanji cards and `words\巻く.md`, `words\干す.md`, `words\庁.md`.
- **Evidence read in full:** `docs\n2-batch-sources\batch-07.json`, including all 53 dictionary records and the Kotobank record.
- **Distractors:** checked the titles of all 45 targets plus 犬, and every existing kanji card whose title overlaps a new one.
- **大 edit:** checked the changed line in `kanji\大.md` and the titles of all 20 legacy two-choice cards.
- **Word titles:** searched titles under `words\` for overlaps with the three new word titles. I searched `docs\confusable-words.md` only for the relevant words.
- **Related edits:** read all 17 related word articles, but assessed only the component-link passages.
- **Public checks:** Jisho API for 布地 and 布く, and Kotobank for 希う.
- **Not reviewed:**
  - drawing paths in the 15 stroke files;
  - `manifest.json` and validator runs;
  - the unchanged parts of the 17 related articles;
  - the app source code;
  - files I was told not to read.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\島.md | CLEAN | CLEAN | CLEAN |
| kanji\州.md | CLEAN | CLEAN | CLEAN |
| kanji\巨.md | CLEAN | CLEAN | CLEAN |
| kanji\巻.md | CLEAN | CLEAN | CLEAN |
| kanji\布.md | NEEDS FIX (B07-F1) | NEEDS FIX (B07-F2) | CLEAN |
| kanji\希.md | CLEAN | CLEAN | CLEAN |
| kanji\帯.md | CLEAN | CLEAN | CLEAN |
| kanji\帽.md | CLEAN | CLEAN | CLEAN |
| kanji\幅.md | CLEAN | CLEAN | CLEAN |
| kanji\干.md | CLEAN | CLEAN | CLEAN |
| kanji\幼.md | CLEAN | CLEAN | CLEAN |
| kanji\庁.md | CLEAN | CLEAN | CLEAN |
| kanji\床.md | CLEAN | CLEAN | CLEAN |
| kanji\底.md | CLEAN | CLEAN | CLEAN |
| kanji\府.md | CLEAN | CLEAN | CLEAN |
| words\巻く.md | NEEDS FIX (B07-F3) | CLEAN | CLEAN |
| words\干す.md | CLEAN | CLEAN | CLEAN |
| words\庁.md | CLEAN | CLEAN | CLEAN |

- **Kanji data:** every card's readings, strokes, radical and radical number, and grade tag match the source record.
- **Distractors:** all 45 are existing cards with wrong meanings, and every new kanji links to a useful word article.
- **大 edit:** `kanji\大.md:11` now lists [小, 人, 犬], three valid options. This stops the automatic fill from adding 巨 "huge; gigantic", which would be a second correct answer. Of the 20 legacy cards (only two curated wrong options, so the app fills a third automatically), none would get a new title as a defensible answer. The edit is clean.
- **Related links:** all 17 component links match their kanji cards. 毛 and 徹 have no cards and correctly stay unlinked.

## Findings
**B07-F1 — Minor — Correctness — `kanji\布.md:31, 34, 48`**
- **Claim:** Row 31 pairs 布く しく with sense 1 of entry 1497020, "to spread out (e.g. a futon); to lay out". The source does not attach the 布く spelling to that sense. It notes "sometimes written as 布く" only on sense 3 (impose widely or promulgate), sense 5 (lay railway tracks) and sense 6 (deploy troops).
- **Impact:** Learners link the 布 spelling to laying out a futon, the one sense where it isn't documented. They also miss the spread/promulgate link that fits the card's "distribute" meaning.
- **Remedy:** Gloss with senses 3, 5 and 6, say JMdict notes these are sometimes written 布く, and keep the search-only and standard-spelling 敷く qualifications. No new example is needed.
- **Evidence:** `batch-07.json:1759-1891`. Line 1763 marks 布く as a "search-only kanji form". Sense 1 (glosses at 1779-1780) has an empty info note. The 布く note appears at lines 1821, 1854 and 1871. The Jisho API search for 布く returns headword 敷く しく with the same notes.
- **Confidence:** High.

**B07-F2 — Minor — Scoped coverage (homograph) — `kanji\布.md:32, 47`**
- **Claim:** The card shows 布地 only as きれじ. The usual reading of 布地 is ぬのじ, a separate common dictionary entry. The きれじ entry's main spelling is 切れ地, with 布地 listed last.
- **Impact:** Learners are likely to read 布地 as きれじ by default.
- **Remedy:** Add: "布地 is usually read ぬのじ; きれじ is a less common reading of this spelling (usually written 切れ地)."
- **Evidence:** `batch-07.json:1896-1950` (entry 2859268): no priority flags, and sense 3 is marked rare. The Jisho API search for 布地 returns 布地 ぬのじ marked common first. Its second result is 切れ地/裂地/切地/布地 きれじ, which cross-references 布地 ぬのじ. The batch file omits non-N2 spellings by design, so it cannot show this.
- **Confidence:** High.

**B07-F3 — Minor — Correctness (quiz answer labels) — `words\巻く.md:4, 8`; `words\風.md:4`**
- **Claim:** 巻く is titled "wind; coil; roll up" (the verb), and 風 is titled just "wind" (the noun). The app removes only exactly matching titles, and neither article excludes the other. An English-to-Japanese question "wind" (for 風) that offers 巻く has two defensible answers, and so does the reverse question.
- **Why it can happen:** Both words are wago and share the wago tag, which the guidance lists as a factor in choosing quiz options.
- **Remedy:** Add 風 to 巻く's `quiz_exclusions`; one side is enough.
- **Evidence:** `content-format.md:79-87`; the front matter of both files; `docs\confusable-words.md` has no entry for this pair.
- **Confidence:** Medium-high. The overlap is certain, but how often the two are chosen together depends on the app's weighting, which I did not inspect.

## Optional
- **O1:** 干す "hang out to dry; air" against 空気 "air; atmosphere" and 大気 "atmosphere; air". The noun labels mostly disambiguate, but "air out" or an exclusion would remove the residual overlap.
- **O2:** 巻く against くるくる "spinning; coiling around" overlaps partially; an exclusion is worth considering.
- **O3:** `words\干す.md` cites "senses 1-2" but describes draining (sense 2) as not the focus. Citing sense 1 would be more precise.
- **O4:** 庁's "庁の職員に相談した" uses standalone 庁, which the dictionary supports. A full agency name such as 気象庁 would read more naturally in isolation.
- **O5:** 政府 against 庁 is distinguishable as it stands; no action needed.

## Limits
- I couldn't run Git, so the snapshot identity, the clean worktree, the baseline diff and the 56-file count are unverified.
- I didn't review drawing paths in the 15 stroke files, which came from the pinned converter, or `manifest.json`.
- I didn't inspect the app's quiz-option code, so B07-F3's frequency is inferred from documented factors.
- Kanji metadata was compared with the batch file, not raw KANJIDIC2.
- The Kotobank lookup for 布く returned a 404; that is a limit, not evidence. The 希う record matched its live page.
- The naturalness of example sentences was judged non-natively; nothing here is native-speaker certification.
