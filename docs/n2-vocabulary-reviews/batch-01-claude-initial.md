## Snapshot
- **Commit:** `fe744d204feaeb554fce6df934cfafed81419be5`, parent `94a175cdc06f3c7d1d09cbd8891b2a5ef370b18f`, from the frozen receipt (`cleanCommittedContent: true`). I reviewed committed content only.
- **Git limit:** I have file tools only and cannot run Git. I could not confirm the commit identity, the clean tree or the per-file hashes. I read files as they are in the working tree and assumed they match the receipt.

## Scope
- **Model and method:** claude-opus-5.5 (Claude family), working alone and in sequence. I used no sub-agents and edited nothing.
- **Instructions and evidence read:**
  - The receipt, `.github\copilot-instructions.md`, `content-structure.instructions.md` and `docs\content-format.md` lines 18–112.
  - The related patch, `n2-vocabulary-sources.tsv` rows N2:2–21 and `n2-vocabulary-snapshot.json`.
  - All of `batch-01.json`: rows, complete entry families, and KANJIDIC records.
- **New articles:** all 17 read completely.
- **Related edits:**
  - The 明き alias paragraph in `空き.md` and the 預かる link in `預ける.md`.
  - The changed passages on all 10 kanji pages, each read as a whole file for context.
- **Reuse claims, specific claims only:**
  - `会う.md` lines 4, 7, 27, 31 and 33.
  - `赤ん坊.md` lines 3–7, 17 and 33.
- **Supporting checks:**
  - Card titles and quiz exclusions in `words\` and `kanji\`, using targeted searches.
  - One Weblio fetch about 足跡. One Kotobank fetch returned an unrelated entry and was discarded.
- **Omissions:**
  - I did not read any forbidden document or other reviewer output.
  - I did not review unchanged teaching beyond the passages above.
  - I did not run the validator or the build.
  - I did not read `docs\confusable-words.md` or `docs\n2-source-snapshot.json`.

## Verdicts
Missing quiz exclusions are counted under correctness, because the quiz would mark a defensible answer as wrong.

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| あいかわらず | NEEDS FIX (F2) | CLEAN | CLEAN |
| アイデア | CLEAN | CLEAN | CLEAN |
| アイディア | CLEAN | CLEAN | CLEAN |
| 曖昧 | CLEAN | CLEAN | CLEAN |
| 扇ぐ | CLEAN | CLEAN | CLEAN |
| 青白い | CLEAN | CLEAN | CLEAN |
| あきれる | NEEDS FIX (F1) | CLEAN | CLEAN |
| アクセント | CLEAN | CLEAN | CLEAN |
| 欠伸 | CLEAN | CLEAN | CLEAN |
| 飽くまで | CLEAN | CLEAN | NEEDS FIX (F3) |
| 明け方 | CLEAN | CLEAN | CLEAN |
| 揚げる | CLEAN | CLEAN | CLEAN |
| 挙げる | CLEAN | CLEAN | CLEAN |
| 憧れる | CLEAN | CLEAN | CLEAN |
| 足跡 | CLEAN | CLEAN | CLEAN |
| 味わう | CLEAN | CLEAN | CLEAN |
| 預かる | CLEAN | CLEAN | CLEAN |

**Related edits:** all clean on every facet.
- **`空き.md` lines 34–36:** clean. The JMdict entry for 空き (1609010) lists 明き with no flags and no reading restrictions, and its senses 1–3 match the uses taught. The card keeps N3, the spelling 空き and `kanji: [空]`, and links 明.
- **`預ける.md`:** the relative link inside the existing 預かる comparison is clean.
- **Ten kanji pages:** clean. Each new link points to the correct word at its real reading:
  - 伸 and 欠 → 欠伸, marked as a whole-word reading.
  - 方, in the -がた row → 明け方.
  - 明 → 明け方 and 明き.
  - 青 and 白 → 青白い.
  - 足, in the あし row → 足跡; 跡 → 足跡.
  - 味 あじ.わう → 味わう; 預 あず.かる → 預かる.

  No invented readings for individual kanji appear. The N2 kanji 伸, 跡 and 預 each get a reciprocal link to the new word.

**Reuse claims:** both clean.
- **会う:** line 27 explicitly teaches 遭う あう for unwanted events, with 事故に遭う, and line 31 contrasts the spellings. This matches the JMdict entry for 会う (1198180), senses 1–2. The card stays N5.
- **赤ん坊:** the card teaches あかんぼう, "baby; infant", citing the JMdict entry for 赤ん坊 (1383310), sense 1. That reading is restricted to the 赤ん坊 spelling. The card stays N4.

## Findings
**F1. あきれる and うんざり can both be correct quiz answers**
- **Severity:** Minor. **Facet:** correctness (quiz metadata).
- **Location:** `あきれる.md` lines 9, 16 and 21; `うんざり.md` lines 4, 8 and 19.
- **Claim and impact:** あきれる's own text teaches "fed up" twice: in the Meaning section (line 16) and in example 2, 同じ言い訳ばかりで、もうあきれています = "I'm fed up…" (line 21). うんざり's title is "fed up; weary of something", and its line 19 example is almost the same sentence. Neither card excludes the other. A learner who followed the articles could pick either answer in either quiz direction and be marked wrong.
- **Remedy:** add うんざり to あきれる's `quiz_exclusions`. Exclusions apply both ways, so one side is enough. Optionally, add one line of contrast: あきれる is stunned disapproval of something absurd; うんざり is weariness from repetition.
- **Evidence:** the JMdict entry for あきれる (1515580), sense 1, includes the glosses "disgusted, exasperated, fed up".
- **Confidence:** medium-high.

**F2. あいかわらず and いつも are not excluded from each other**
- **Severity:** Minor. **Facet:** correctness (quiz metadata).
- **Location:** `あいかわらず.md` lines 4, 9 and 16–17; `いつも.md` lines 4, 9 and 31.
- **Claim and impact:** あいかわらず's title is "as usual; as before", and its gloss includes "as ever". いつも's title is "always; usually", and its article teaches いつもの as "the usual". Neither card excludes the other; いつも excludes only たいてい. Given the prompt "as usual; as before", choosing いつも (as in いつも通り, "as usual") is defensible.
- **Remedy:** add いつも to あいかわらず's `quiz_exclusions`. 普段 ("usually; everyday") is a weaker candidate.
- **Evidence:** the JMdict entry for あいかわらず (1401310), sense 1, glosses "as always". The repository already excludes similar adverbs of habit from each other: 普段 excludes いつも, たいてい and 普通.
- **Confidence:** medium.

**F3. Two misleading sentences in 飽くまで**
- **Severity:** Minor. **Facet:** comprehensibility.
- **Location:** `飽くまで.md` lines 29–30 and 41–42.
- **Claim and impact:**
  - Line 30, "It does not mean 'until bored' in every sentence", implies that some modern uses do mean "until bored". JMdict's senses do not support that.
  - Lines 41–42 tell the reader not to "treat the English gloss 'after all' as a universal replacement for やはり". The subject is wrong: the warning should be against equating あくまで with やはり. As written, this garbles the distinction behind the やはり/やっぱり exclusions.
- **Remedy:**
  - Line 30: "It does not mean 'until bored.'"
  - Lines 41–42: "JMdict's 'after all' gloss for sense 2 does not make あくまで a substitute for やはり 'as expected'; it limits how a statement should be taken."
- **Evidence:** the JMdict entry for 飽くまで (1518320). Sense 1: to the end, stubbornly, to the utmost. Sense 2: after all, only, purely, simply.
- **Confidence:** high that the wording is confusing.

## Optional
These are non-blocking:
- **あいかわらず:** also link [相](../kanji/相.md) in the kanji section. The card exists; only 変 is linked now.
- **アイディア line 18:** "Preserve that spelling when reading this card" is unclear. Optionally note that アイデア carries more frequency tags in JMdict (ichi1 and gai1, against gai1 only).
- **扇ぐ:** mention the 煽ぐ spelling and the homophone 仰ぐ.
- **足跡 lines 30–31:** replace "not a mandatory on-reading combination" with a note that the そくせき reading is typical for the figurative sense "career; achievements" (足跡を残す). Weblio's Wikipedia excerpt supports this. The batch's JMdict record does not include that sense, so its absence is not a defect.
- **味わう:** 挫折を味わう or 敗北を味わう would be more idiomatic "experience" examples.
- **あきれる:** add the set phrase あきれて物が言えない.
- **明.md:** the new Common-words bullets use "-" where older bullets use "—".

## Limits
- **Git:** commit identity, clean state and file hashes are unverified. Commit and hash values come from the receipt.
- **Validator:** `tools/validate.py` was not run, so the frontmatter schema and link checking are not verified.
- **Naturalness:** these are judgements, not native-speaker certification.
- **Dictionary evidence:** limited to the selected batch JMdict records plus one public page. Absence from the selected records does not prove absence from the dictionary.
- **預ける's citation:** I did not verify its citation of JMdict entry 1544990, which is unchanged text.
- **Quiz overlap:** I checked with targeted title searches. It is not an exhaustive pairwise audit.
- **Unchanged teaching:** in `会う`, `赤ん坊`, `空き`, `預ける` and the kanji pages, I did not review content beyond the passages listed in Scope.
