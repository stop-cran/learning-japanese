I've finished my confirmation review of the corrected snapshot. All three of my original findings are fixed, the 11 added guards hold up, and I found no regressions. I did find two pre-existing quiz-exclusion gaps that I missed in my first review: たちまち/一度に and ためらう/おどおど.

## Snapshot
- **Corrected commit:** `0e73b4e0028a0bb74940f2dbdc10e7890bb24ef9`
- **Parent:** `9de757c1fdaff0d2012091652d43247998307d29` (the authored snapshot)
- I reviewed committed content only. My file tools can't run Git, hash or cleanliness checks, and I did not inspect `.git`. The commit, `cleanCommittedContent: true` and the file hashes are the author's checks, and I did not repeat them.

## Scope
- **Model:** claude-opus-5.5 (Claude family). Read-only; no agents, delegation or edits.
- **Read in full this pass:**
  - `correction-snapshot.json` and `correction.patch`
  - The seven changed articles: たちまち, 妥当, 溜まる, 溜める, ためらう, だらしない, 例える
  - `kanji\袋.md`
  - `corrective-comparison-reading.txt`: all 14 families, 50 senses. These are おかげ, ぐずぐず, すっと, だらだら, 一瞬, 重なる (1335800), 瞬間, 成立, 適する, おもなる (1589400, written 重なる), 立つ, 例え, 頼る and ぐしゃぐしゃ.
  - `corrective-existing-reading.txt`: all 13 old article bodies.
  - `content-format.md:84-99` (the quiz_exclusions rule).
  - Five other existing articles in full: おどおど, 効力, 一度に, 一斉, さっさと.
- **Read in part:**
  - `corrected-review-evidence.json`: lines 24874-24910 and 25057-25320 (inspection volumes, current and added declarations, adjudications), plus 17900-17975 (JMdict 1609210, 一度に) and 22040-22066.
  - `principal-reading.txt`: lines 40-45 and 154-158.
- **Searches:**
  - Labels JSONL, for specific candidate words.
  - TSV rows N2:1002-1021.
  - The relevant rows in 畳.md and 線.md.
  - Title and exclusion lines of the 13 unchanged articles.
  - Title searches across `words\` for overlaps with each new guard's meaning.
- **Inherited without fresh full rereads:** the 13 unchanged articles (助かる, 但し, 畳む, 立ち止まる, 建つ, 発つ, 脱線, 頼もしい, 足袋, ダブル, だます, ダム, ため息) and the 畳 and 線 cards. I keep my initial judgments for these. The patch doesn't touch them, and their titles and exclusions match what I recorded.
- **Not read:** family-inspection files 01-10 in full, `public-bodies.json`, and the rest of the corrected evidence. I read no forbidden ledgers, reports, scripts or `batch-51.json`.
- **Web:** I made one fresh fetch (jisho.org, おどおど). It returned only page navigation, so it is not evidence.
- **Guard count:** my own count gives 47 guards on the 13 unchanged cards and 55 on the 7 changed cards. That is 102 across 18 cards, up from 91, with 11 additions and no removals. This matches the author's `currentQuizDeclarations`.

## Verdicts

| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1002 | words\助かる.md (new) | Inherited; title and exclusions re-checked | CLEAN | CLEAN | CLEAN |
| N2:1003 | words\但し.md (new) | Inherited; title and exclusions re-checked | CLEAN | CLEAN | CLEAN |
| N2:1004 | words\畳む.md (new) | Inherited; title and exclusions re-checked | CLEAN | CLEAN | CLEAN |
| N2:1005 | words\立ち止まる.md (new) | Inherited; title and exclusions re-checked | CLEAN | CLEAN | CLEAN |
| N2:1006 | words\たちまち.md (new) | Full reread | NEEDS FIX (B51-C1) | CLEAN | CLEAN |
| N2:1007 | words\建つ.md (new) | Inherited; title and exclusions re-checked | CLEAN | CLEAN | CLEAN |
| N2:1008 | words\発つ.md (new) | Inherited; title and exclusions re-checked | CLEAN | CLEAN | CLEAN |
| N2:1009 | words\脱線.md (new) | Inherited; title and exclusions re-checked | CLEAN | CLEAN | CLEAN |
| N2:1010 | words\妥当.md (new) | Full reread | CLEAN | CLEAN | CLEAN |
| N2:1011 | words\例える.md (new) | Full reread | CLEAN | CLEAN | CLEAN |
| N2:1012 | words\頼もしい.md (new) | Inherited; title and exclusions re-checked | CLEAN | CLEAN | CLEAN |
| N2:1013 | words\足袋.md (new) | Inherited; title and exclusions re-checked | CLEAN | CLEAN | CLEAN |
| N2:1014 | words\ダブル.md (new) | Inherited; title and exclusions re-checked | CLEAN | CLEAN | CLEAN |
| N2:1015 | words\だます.md (new) | Inherited; title and exclusions re-checked | CLEAN | CLEAN | CLEAN |
| N2:1016 | words\溜まる.md (new) | Full reread | CLEAN | CLEAN | CLEAN |
| N2:1017 | words\ダム.md (new) | Inherited; title and exclusions re-checked | CLEAN | CLEAN | CLEAN |
| N2:1018 | words\ため息.md (new; source spelling 溜息) | Inherited; title and exclusions re-checked | CLEAN | CLEAN | CLEAN |
| N2:1019 | words\ためらう.md (new) | Full reread | NEEDS FIX (B51-C2) | CLEAN | CLEAN |
| N2:1020 | words\溜める.md (new) | Full reread | CLEAN | CLEAN | CLEAN |
| N2:1021 | words\だらしない.md (new) | Full reread | CLEAN | CLEAN | CLEAN |

**Kanji edits and reciprocity**
- **袋: CLEAN.** The final source list (line 50) now includes 1404920, in numeric order. The whole-word たび row (33), the 足袋 entry under Common words (41) and the Note (48) are unchanged, so no 袋び or 足た reading is invented.
- **畳: CLEAN (inherited, spot-checked).** Line 30 links 畳む in the たた.む row, line 39 lists it under Common words, and line 47 lists 1356780.
- **線: CLEAN (inherited, spot-checked).** Line 30 adds 脱線 だっせん to the セン row, line 45 adds it to Common words, and line 53 lists 1416560.

**Baseline preservation: CLEAN.** The patch touches only line 9 of the seven word articles and line 50 of 袋.md. No front matter, existing word cards, component links or teaching text changed.

**Mappings: CLEAN.** I re-checked TSV rows N2:1002-1021. Entries, sense numbers, additional senses, the 溜息 to ため息 normalization and the unchanged raw glosses are all as before. The evidence file records no mapping changes.

## Findings

**My original findings**
- **B51-F1 (例える/例え): resolved.** 例え is now excluded (`例える.md:9`). This rests on 例え's title "example; analogy; metaphor" and JMdict 1597120 sense 2 (simile, metaphor), not a blanket noun/verb rule. No regression.
- **B51-F2 (たちまち/一瞬): resolved** (`たちまち.md:9`). 一瞬's article teaches 一瞬で "in an instant", and JMdict 1163340 lists it as noun and adverb.
- **B51-F3 (袋 source list): resolved** (`袋.md:50`).

**The other reviewer's eight pairs: all accepted.** Each overlap is backed by an actual title or old article body, not just a shared topic:
- **たちまち/すっと:** JMdict 1006140 sense 1 includes "all of a sudden", and すっと's article mentions that rendering. さっさと already excludes すっと along with the same speed words.
- **妥当/成立:** 成立's title includes "validity", and its article teaches 議論は成立しません ("the argument does not hold").
- **妥当/適する:** 適する is titled "suit; be suitable for"; 妥当 already excludes 適当 ("suitable").
- **溜まる/重なる and 溜める/重なる:** JMdict 1335800 sense 2 includes "to accumulate", and 重なる's article describes accumulating.
  - The transitive/intransitive difference is consistent with 溜める already excluding 溜まる, 積もる and 集まる.
  - Exclusions don't chain, so the indirect 重ねる/積もる route would not have covered these pairs.
- **ためらう/ぐずぐず:** JMdict 1004040 sense 1 includes "hesitantly", and ぐずぐず's article says "Delaying or hesitating".
- **だらしない/ぐしゃぐしゃ:** "messy" overlaps "sloppy", and JMdict 2097580 sense 3 is untidiness that isn't wet.
- **だらしない/だらだら:** JMdict 1007510 sense 4 includes "slovenly; lazily", consistent with the existing 怠ける guard.

**The author's own addition, 妥当/立つ: acceptable, not an excess.** JMdict 1597040 sense 13 literally includes "to be valid… to be logical… to be reasonable", matching 妥当's title words. It is the weakest addition at the title level, since 立つ's title and article are about posture, but it costs only one distractor.

**The author's declined pairs: accepted, within stated bounds.**
- **建つ/立つ:** sense 2 (standing or being situated) is not "be built", and 立つ's own article separates 建つ.
- **たちまち/瞬間:** 瞬間's article teaches a point in time, with no rapid-result pattern like 一瞬で.
- **頼もしい/頼る and 助かる/おかげ:** no consequential issue established. The parity question between 手伝い and おかげ is still only an optional observation.

**Regressions: none found.**
- All 11 targets are existing articles with exact titles.
- No card excludes itself, no entry is duplicated and nothing was removed.
- The evidence file's current declarations match the files.
- The teaching text in the seven changed articles is unchanged.

**B51-C1 · Minor · quiz exclusions · new (I missed this in my first review)**
- **Where:** `words\たちまち.md:9` and `:43`; `words\一度に.md:4`, which has no exclusions in lines 1-9.
- **Problem:** 一度に's title is exactly "all at once". The たちまち article itself says "English 'all at once' here can mean suddenly" (line 43).
  - In a quiz on たちまち, "all at once" could appear as a wrong answer that a learner could reasonably accept, and the reverse also holds.
  - This overlap is stronger than the accepted すっと guard.
- **Evidence:**
  - JMdict 1288480 sense 2 glosses: "suddenly; all of a sudden; all at once" (`principal-reading.txt:45`).
  - The N2:1006 source gloss ends "all at once" (`principal-reading.txt:40`).
  - JMdict 1609210 (一度に) is an adverb with the single gloss "all at once" (`corrected-review-evidence.json` ~17935-17946).
  - The author's inspection set includes 一度に (`labels.jsonl:34`, evidence line 2693), but no adjudication covers this pair.
  - 一斉 excludes 一度に, but exclusions don't chain, so that doesn't cover たちまち.
- **Fix:** add 一度に to たちまち's quiz_exclusions.
- **Confidence:** medium-high.

**B51-C2 · Low · quiz exclusions · new**
- **Where:** `words\ためらう.md:4` and `:9`.
- **Problem:** おどおど's title is "timidly and hesitantly" (`おどおど.md:4`), and it excludes only 緊張 (`:8`).
  - Its article teaches "timid, nervous, hesitant behavior" (`:15`) and "The boy hesitantly gave his name" (`:18`).
  - The accepted ぐずぐず guard was justified by a gloss alone; its title, "dawdling; grumbling; unsettled", doesn't even mention hesitation. おどおど's overlap is in the title itself, so it is stronger.
  - Existing guards already cross parts of speech (たちまち/急, たちまち/一瞬, ためらう/ぐずぐず).
- **Evidence:** おどおど appears in neither the labels JSONL nor the corrected evidence, so it was outside the author's inspected set.
- **Fix:** add おどおど to ためらう's quiz_exclusions.
- **Confidence:** medium.

## Optional
- **妥当/効力** ("efficacy; validity; potency"): shares the word "validity" with 成立 and 有効. 効力 is mainly about efficacy or legal force, so this pair isn't established.
- **たちまち/一斉** ("all at once; simultaneous"): weaker than B51-C1. "simultaneous" separates the meaning, and the たちまち article contrasts 一斉 by name.
- **たちまち/さっさと** ("quickly; without hesitation"): さっさと excludes the same cluster of speed words, but it has no "suddenly" sense.
- **TSV note for N2:1006:** it still reads as dismissing 一瞬, which now conflicts with the current guard. Refreshing the wording later would help; no mapping change is needed.
- **Parity questions that remain optional:** 頼もしい/頼る, and 助かる/おかげ versus 手伝い.

## Limits
- Git, the validator, hashes and live quiz draws were not run. The patch is the author's artifact, though my rereads match it.
- The 13 unchanged articles and the 畳 and 線 cards are inherited judgments, not fresh full reads.
- I still haven't fully read family-inspection files 01-10 or `public-bodies.json`, and I read only the correction section of the corrected evidence. Records I didn't read don't prove anything is absent.
- For おどおど I have no JMdict record in the permitted evidence, and my web fetch failed. B51-C2 therefore rests on the repository article alone.
- B51-C1 and B51-C2 are editorial judgments about titles. They are not native-speaker certification.
- The author's counts (227 families, 116 article bodies, 185 labels) are not my actual reads.
- My first review missed 一度に even though its label was among the ones I read.
