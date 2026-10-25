## Snapshot
Frozen commit: `3d66845af7cc97508b6a8d4348f0792e2cbdb9c6`. Parent: `ba5b4d4cb75a542fe74572dfb1efff1fe0788693`. `cleanCommittedContent` is true and `reusedArticles` is empty.

I reviewed committed content only. My file tools can't run Git, so I couldn't check the commit, the hashes or the equivalence claims myself; the author ran those.

## Scope
**Model:** claude-opus-5.5, claude family. I worked alone, with no agents or edits.

**Read in full:**
- Instructions: `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md:18-126`.
- All 20 new articles.
- `related.patch` and the six complete kanji cards (階, 短, 炭, 鉱, 団, 編).
- Private files: frozen-snapshot, review-mappings, review-principals, review-components (34 records), review-labels (150 records), principal-reading.txt and public-bodies.txt (the author's Daijisen captures).
- The 20 assigned rows of `docs\n2-vocabulary-sources.tsv`.
- Old comparison bodies: `kanji\魚.md`, and `words\` 住宅, アパート, 家具, がんがん, ばりばり, 確実 and しっかり.

**Read in part:**
- `review-evidence.json`, lines 1–60 only.
- Titles and exclusions of about 40 other `words\` cards, found by grep and glob. These were labels only, not full bodies.

**Not read:** family-inspection-01 to 09, public-bodies.json, `docs\n2-vocabulary-snapshot.json`, `docs\n2-source-snapshot.json`, `docs\confusable-words.md` and `docs\jlpt-levels.md`. I made no fresh web fetches. I did not open any excluded ledgers or `batch-52.json`.

## Verdicts
All 20 rows map to new articles (`words\<word>.md`) at level 2, with matching JMdict IDs. Cells are correctness / scoped coverage / comprehensibility.

| ID | Article | Correct | Coverage | Comprehensible |
|---|---|---|---|---|
| N2:1022 | 足る | CLEAN | NEEDS FIX (B52-03) | CLEAN |
| N2:1023 | 段階 | CLEAN | CLEAN | CLEAN |
| N2:1024 | 短期 | CLEAN | CLEAN | CLEAN |
| N2:1025 | 炭鉱 | CLEAN | CLEAN | CLEAN |
| N2:1026 | 短所 | CLEAN | CLEAN | CLEAN |
| N2:1027 | たんす | CLEAN | NEEDS FIX (B52-03) | CLEAN |
| N2:1028 | 淡水 | NEEDS FIX (B52-01) | CLEAN | CLEAN |
| N2:1029 | 断水 | CLEAN | CLEAN | CLEAN |
| N2:1030 | 単数 | CLEAN | CLEAN | CLEAN |
| N2:1031 | 団地 | CLEAN | CLEAN | CLEAN |
| N2:1032 | 断定 | CLEAN | CLEAN | CLEAN |
| N2:1033 | 短編 | CLEAN | CLEAN | CLEAN |
| N2:1034 | 誓う | CLEAN | CLEAN | CLEAN |
| N2:1035 | 地下水 | CLEAN | CLEAN | CLEAN |
| N2:1036 | 近々 | CLEAN | NEEDS FIX (B52-03) | CLEAN |
| N2:1037 | 近付ける | CLEAN | CLEAN | CLEAN |
| N2:1038 | 近寄る | CLEAN | CLEAN | CLEAN |
| N2:1039 | 力強い | NEEDS FIX (B52-02) | CLEAN | CLEAN |
| N2:1040 | 千切る | CLEAN | CLEAN | CLEAN |
| N2:1041 | 地質 | CLEAN | CLEAN | CLEAN |

**Six kanji edits (階, 短, 炭, 鉱, 団, 編): CLEAN** for correctness, coverage and comprehensibility.
- All eight reciprocal pairs have a word link, the actual whole-word reading and a Common words entry.
- On 短, the existing plain-text 短所 and 短期 were turned into links rather than duplicated.
- 編 correctly notes that ヘン becomes ぺん in たんぺん.

**Baseline kanji metadata: CLEAN.** The changes only add body text. Front matter, readings, distractors and notes are untouched, and JMdict entry IDs were inserted in sorted order.

**Mappings: CLEAN.**
- All 20 TSV rows match review-mappings for entry, selected senses and additional senses.
- Source glosses support the sense choices: 単数 sense 2, 力強い sense 2, 近々 senses 1–2, 千切る senses 1–2.
- Additional senses rely on the public dictionary; no new JMdict sense numbers are invented (近付ける target state, 近寄る association, 団地 industrial estate).
- Restrictions are taught correctly: the shaft sense of 炭鉱 belongs to the 炭坑 spelling only, and the spatial sense of 近々 belongs to the ちかぢか reading only.
- Kanji without cards (淡, 誓) stay in metadata, and たんす correctly has `kanji: []`.

## Findings
**B52-01. Minor. Facet: reading explanation. `words\淡水.md:25`. Confidence: high.**
- **Claim:** The article says "the fish character is voiced to ぎょ here."
- **Problem:** ギョ is 魚's ordinary on reading (`kanji\魚.md` onyomi [ギョ]; 金魚 is きんぎょ), not a voiced form. Learners are taught a sound change that doesn't happen.
- **Fix:** Write "淡水魚 is たんすいぎょ, using 魚's on reading ギョ."

**B52-02. Minor. Facet: quiz_exclusions, one too many. `words\力強い.md:9`. Confidence: medium.**
- **Claim:** 力強い ("powerful; reassuring") excludes がんがん, whose title is "loud banging; a pounding headache" (`がんがん.md:4`).
- **Problem:** The only overlap is a casual body note, がんがん働く "working flat out" (`がんがん.md:28`). A learner wouldn't reasonably accept either title for the other word, so the exclusion just removes a valid wrong answer.
- **Fix:** Remove がんがん.
- 確か and 確実 ("certain; reliable") and しっかり are borderline. I'm not counting them as defects.

**B52-03. Minor. Facet: links to existing words. Confidence: high.**
- **Rule:** Words with existing cards should be linked where they are introduced or compared (`content-structure.instructions.md:20,55`).
- **Problem:** Three are left as plain text:
  - `足る.md:40`: 不足する. `words\不足.md` exists ("shortage; insufficiency").
  - `近々.md:41`: 遠く. `words\遠く.md` exists ("far away; distant place").
  - `たんす.md:45`: 押入れ. `words\押し入れ.md` exists ("built-in closet").
- **Fix:** Link all three with relative `.md` links.

## Optional
- **足る:** Consider mentioning noun + に足る (信頼に足る) and 足るを知る. Daijisen sense 2 supports 足るを知る; the noun pattern is not in the captured evidence.
- **短編, line 21:** 十分 can be read as じゅうぶん; writing 10分 avoids the ambiguity.
- **地下水, line 20:** この井戸から地下水をくみ上げています may read more naturally (low confidence).
- **千切る, lines 33–34:** The 千 card lists the kun reading ち, so ち + ぎる is a clearer split than ちぎ.
- **誓う:** Could add 神に誓う to show the addressee takes に.
- **Exclusions:** 短所 excludes 苦手 but not 下手, and 段階's exclusion of 程度 is borderline. 団地 has no exclusion against 住宅 or アパート; that matches baseline precedent, so it's optional.

## Limits
- I didn't run Git or any hash checks.
- The family-inspection files were unread, so ambiguity checks for answer choices rest on the 150 labels and about 40 titles. I read only eight old article bodies in full, not the author's 92.
- Daijisen evidence comes from the author's captures; I fetched nothing fresh.
- The naturalness judgments are not native-speaker certification.
