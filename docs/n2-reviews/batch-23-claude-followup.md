## Snapshot
- **Corrected commit:** `b32b498c77ab63d635e63b573603882f423772d1`, read from `n2-batch-23-corrected-snapshot.json`.
- **Original commit:** `ba36c794cd3cff027e3b1bf8c6a7c6f2de800dd8`.
- **Baseline:** `5297e4f594f6587cb1d48abfb4e271cea3e83e10`.
- I reviewed committed file contents only.
- I had file tools only and ran no Git commands. The clean worktree, the 9-file and 58-file scopes, the validator result, the 1,022-row audit and manifest version `e59e527490d48a92` were all checked by the author. I did not repeat those checks.

## Scope
- **Model:** claude-opus-5.5, claude family.
- **Read in full:** my original report `docs\n2-reviews\batch-23-claude-initial.md`, the fix patch `n2-batch-23-fix.patch`, `kanji\門.md` and `words\鉱石.md`.
- **Evidence I inspected:**
  - In `docs\n2-batch-sources\batch-23.json`: the full 鳴門 record (entry 1753350, lines 4501–4635), the 門 と record (1266970), the 門 entry list and external-source text, and the `newWordArticles` section.
  - Comparison pages: the front matter of `words\石.md` and `words\採掘.md`, and the title and kunyomi of `kanji\戸.md`.
  - The format rules on links in `content-structure.instructions.md` and `content-format.md`.
  - Kotobank 鳴門 (`%E9%B3%B4%E9%96%80-590222`), fetched now. Kotobank 戸 (`%E6%88%B8-61194`), fetched during my original review.
- **Not inspected:**
  - The seven non-teaching files in the 9-file correction scope.
  - `docs\n2-source-snapshot.json`.
  - The body of `words\門.md`.
  - All other batch pages. This was not a full-batch re-review.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\門.md` | CLEAN | CLEAN | CLEAN |
| `words\鉱石.md` | CLEAN | CLEAN | CLEAN |

## Findings
**B23-R-01 (the 門 と row glossed as "shutter"): resolved.**
- `門.md:32` now gives 鳴門 なると as a "strait with roaring tides".
- This matches pinned JMdict 1753350 sense 1: "strait with a roaring tidal ebb and flow", with no spelling restriction and the note "from 鳴門海峡".
- It also matches Daijisen なる‐と【鳴▽門／鳴戸】 sense 1, which describes the eddying, roaring strait.
- 鳴門 is a complete common noun, not just a place name or a name reading. In it, 門 does supply と.
- Note line 43 keeps the food sense and the place-name senses separate from this gloss.
- Note line 44 states the source disagreement honestly:
  - JMdict leaves "shutter" unrestricted for 門.
  - Daijisen marks the fitting sense as 戸.
  - It advises using 戸 for an everyday door, which Daijisen and JMdict both support.
  - It makes no claim that the 門 spelling is rare.
- The Kotobank link at line 48 points to the 戸 page I verified. The earlier guessed URL that redirected to an unrelated entry is not cited anywhere.
- The new entry ID 1753350 appears in the metadata at line 46.
- Confidence: high.

**Optional 鉱石 links: adopted and verified.**
- `鉱石.md:18` links [採掘]. That page exists as さいくつ "mining", a transitive する verb that takes を, so 鉱石を採掘します is correct.
- `鉱石.md:28` links [石]. That page exists as いし "stone; pebble".
- Prose and metadata are unchanged.

**Optional 逆鱗 and 門出/門松 examples: not adopted.** These were only suggestions, so no defect is being deferred.

**Regressions:** none established.
- The rows for モン and かど, the front matter, the distractors (間, 問, 聞) and the rest of 鉱石 are unchanged in the patch.
- `batch-23.json` contains 74 records with distinct entries across 69 families, plus 2 separate `newWordArticles` references. That agrees with the author's 74 and 69.

## Optional
- The 門 note could link [戸](戸.md), which exists as "door; counter for households".
- 鉱石 is the only word page I found with a link inside an example sentence. It is allowed and does no harm.

## Limits
- This review covered only the changed passages.
- I did not run Git, the validator or the manifest builds.
- I did not independently check the 73-pair count, the unchanged 39 readings, the metadata, the 15 stroke files or the 19 older files that only gained links.
- I did not review stroke drawing paths, test the quiz at runtime, or certify the Japanese as a native speaker would.
