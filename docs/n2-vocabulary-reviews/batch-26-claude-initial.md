## Snapshot
The frozen commit is `54389ef6c76d3ca5f14c89bc8ad04ee59fe1f9dd` (parent `00af0a49f284c19ebe75aae35a4aaea6177381b8`). I reviewed committed content only, but I had file tools and no Git execution. So I couldn't confirm the files on disk match that commit or recompute the receipt's hashes.

## Scope
- **Model:** claude-opus-5.5 (Claude family).
- **Read in full:** the 19 new articles, `肯定.md` (assessed only for its claimed source mapping, senses 1-2 and the added `jlpt: 2`), the nine-file related patch, and the eight changed kanji cards in context plus `肯.md`.
- **Mappings:** all twenty TSV rows N2:502-521.
- **Evidence packet:** the twenty principal JMdict families, the author's comparison-card label list and the author's planned quiz exclusions.
- **Other cards checked:** こっち, こちら, ビル and 一般 read in full, plus the titles and `quiz_exclusions` of all related cards.
- **Not read:** all forbidden files, including `batch-26.json`. I did not search outside `words\`, `kanji\` and the allowed evidence.

## Verdicts
Each cell gives correctness / scoped coverage / comprehensibility.

| Article | Verdict | Article | Verdict |
|---|---|---|---|
| 孝行 | CLEAN / CLEAN / CLEAN | 公正 | CLEAN / CLEAN / CLEAN |
| 交差 | CLEAN / CLEAN / CLEAN | 功績 | CLEAN / CLEAN / CLEAN |
| 講師 | CLEAN / CLEAN / CLEAN | 光線 | CLEAN / CLEAN / CLEAN |
| 工事 | CLEAN / CLEAN / CLEAN | 高層 | CLEAN / CLEAN / **NEEDS FIX** (`F2`) |
| 公式 | CLEAN / CLEAN / CLEAN | 構造 | CLEAN / CLEAN / CLEAN |
| 口実 | CLEAN / CLEAN / CLEAN | 交替 | CLEAN / CLEAN / CLEAN |
| こうして | CLEAN / CLEAN / **NEEDS FIX** (`F1`) | 耕地 | CLEAN / CLEAN / CLEAN |
| 校舎 | CLEAN / CLEAN / CLEAN | 交通機関 | CLEAN / CLEAN / CLEAN |
| 公衆 | CLEAN / CLEAN / CLEAN | 校庭 | CLEAN / CLEAN / CLEAN |
| 香水 | CLEAN / CLEAN / CLEAN | | |

**Reused 肯定:** CLEAN. The body teaches senses 1-2 (affirmation, and the logic sense "affirmative") at the source spelling and reading. Only `jlpt: 2` was added.

**Kanji changes:** all eight are CLEAN.
- 講, 香, 線, 層 and 造 link the new words at the correct readings, and their source footers add the right entry IDs.
- 績 links 功績; 替 links 交替 (meaning, readings, common words); 耕 links 耕地 (readings, common words).
- 孝, 舎, 衆, 功 and 斯 have no kanji cards, so they correctly stay unlinked metadata.

**Twenty mappings (N2:502-521):** all CLEAN on correctness, coverage and comprehensibility.
- 高層 selects sense 2 (high altitude) and openly teaches sense 1 (high-rise) as an additional meaning.
- 講師 senses 3-4 (part-time teacher, cram-school tutor) are qualified.
- こうして is mapped to its usual kana form; the rare kanji spelling 斯うして is only mentioned.
- 交替 is mapped with the obsolete reading こうだい correctly not taught.

## Findings
**F1 — Minor, comprehensibility (quiz labels), high confidence**
- **Where:** `words\こうして.md:4,9,45-46`; `words\こっち.md:4`; `words\こちら.md:4`.
- **Problem:** こうして's title is "thus; in this way", こっち's is "this way" and こちら's is "this way; this person". In English, "this way" usually means "in this manner", so a learner could reasonably accept either title. None of the three cards excludes the others. The article itself warns about this confusion at lines 45-46, but the quiz never shows that warning.
- **Evidence:** the author's comparison-card list includes both こちら and こっち (packet lines 29703-29713), yet the planned exclusions for こうして (31634-31645) omit them.
- **Fix:** add こっち and こちら to こうして's `quiz_exclusions`.

**F2 — Minor, comprehensibility (quiz labels), medium confidence**
- **Where:** `words\高層.md:4,9,16-18,21`; `words\ビル.md:4`.
- **Problem:** 高層's title is "high-rise", which in English is also a noun for a tall building. Its body describes "a tall, many-storied building", and JMdict's sense 1 includes "multistory" (packet line 1426). ビル's title is "multistory building". A learner could reasonably accept either, and neither card excludes the other.
- **Evidence:** ビル does not appear in the author's comparison-card list.
- **Fix:** add ビル to 高層's `quiz_exclusions`.

## Optional
- **交替:** teach the transitive frame 選手を交代/交替する, which JMdict marks as transitive. Also note that 交代 is the more frequent spelling (marked ichi1/news1/nf03 versus ichi1 for 交替).
- **高層:** teach the common atmospheric compounds 高層大気 and 高層気流.
- **孝行:** replace "not simply an instruction to obey" with "not merely obedience". Line 16 says "This is a noun" even though 孝行する and 孝行な are taught.
- **Other small additions:** the "plantation" gloss for 耕地, adverbial 公式に, and excluding 越える/越す from 交差 for consistency with 渡る (all three are glossed "cross over").

## Limits
- I couldn't verify the files against the commit or check any hashes.
- The evidence packet is a selection, not the whole dictionary. The author's lookup receipts were not re-retrieved.
- The example sentences were not checked against a corpus or a native speaker. In particular, the naturalness of 高層の大気 versus 高層大気 is unconfirmed because the Weblio and Kotobank lookups failed.
- The search for overlapping quiz titles was a title grep over `words\`, not an exhaustive meaning-by-meaning check.
