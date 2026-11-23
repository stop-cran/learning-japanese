Snapshot: commit 4f8ebea7 (parent 5c04be73); reviewer model: Claude (Anthropic); I can't name the exact version.

Scope: INSTRUCTIONS.md, CHANGES.md, RESPONSE.md and diffs\changed-lines.txt in full. Revised kanji\吟.md and words\太后.md, words\吟味.md in full. Ledger lines 29, 78, 947 and 952 (426-427 only through CHANGES.md). evidence: jmdict-cited-entries.xml (1243390, 1474270, 1607070, 1607100), jmdict-scan-c2.txt (叔 section), joyo\p75 and p162 (叔 lines), b156-selection.json, rule-7058679348.md, daijisen-kotobank.json (太后, 皇太后, 太皇太后, 吟味, 吟), QuizBuilder.kt (lines 15-45), KanjiReadings.kt (lines 70-125), app-code-SOURCES.json. checks: quiz-safety.txt (lines 1-40) and reading-exposure.txt (lines 130-175). The 験 title came from the earlier packet's CHANGES.md. I computed Git blob ids of the three app files. I did not read fix.patch, link-targets.tsv, reading-options.txt, word-quiz.txt or the other cards in full, and did not re-read the nine unchanged cards.

Dispositions:
O1 - RESOLVED - words\太后.md:15 now separates 太皇太后 (先々代の天皇の皇后) from 皇太后 (前天皇の皇后). It gives the "birth mother" clause as a narrower sense, which fits Daijisen's また alternative. "Two reigns back" renders 先々代 correctly. Daijisen 太后 = 太皇太后 or 皇太后 matches line 22 of the evidence.
O2 - RESOLVED (change accepted) - 験 ("test; verify") is added to quiz_exclusions (line 14) and named with its title in Notes (line 42). The exclusion is symmetric (QuizBuilder.kt line 26). It never competes with the curated 二 自 社. It only matters in fallback or custom pools, and the card's Notes list every other exclusion in the same way. The overlap is at the level of the senses, not the two displayed titles: "recite poetry; chant" vs "test; verify" don't directly overlap. Still, the card's Notes already frame the neighbours as overlapping "the sense of examining something closely", and 験 is no weaker than 検 or 査 there. Optional over-exclusion, not a defect.
O3 - RESOLVED (no change; accepted) - the author took no action, and I raised no defect.
Other-review change 1 (吟/験) - covered under O2.
Other-review change 2 (吟味 line 24) - RESOLVED/ACCEPTED - Daijisen sense 3 is 詩歌を吟じてその趣を味わうこと, marked 《3が原義》. JMdict 1243390 sense 4 has misc archaic, s_inf "orig. meaning", and gloss "reciting and appreciating traditional poetry". Each quoted statement is attributed to the right source.
Other-review change 3 (叔 exception, ledger lines 29, 78, 952) - ACCEPTED, with the minor note in Finding 1. Details below.
Other-review change 4 (reading-option correction, line 947) - ACCEPTED - KanjiReadings.kt line 100 is the add() guard (excluded keys, and used.add drops a repeated reading). Line 110 is the curated pass (one random reading per curated card) and line 111 is the closeness fallback. 二 gives ニ or ジ, 自 gives ジ or シ and 社 gives シャ, so 1 of 4 outcomes has a shared ジ. reading-exposure.txt lines 138-150 give 61 (4+57) drawable wrong options for the N1 and All stacks and 27 (4+23) for Starter, with deficit 0/1 and no exposure hit. The three app files' Git blob ids (computed by me) equal app-code-SOURCES.json: 492a43c3…, 47ce071b… and 9c8b2c82…

叔 check details:
- JMdict 1607070 and 1607100: the spellings 叔父 and 叔母 carry ichi1/news1 (ke_pri). おじ and おば carry the re_pri. しゅくふ and しゅくぼ carry re_restr to 叔父 and 叔母 and no tag.
- 伯叔 (1474270) is untagged, with glosses "brothers; one's father's brothers".
- Joyo p75 lists シュク with 伯叔, 叔父(おじ) and 叔母(おば). p162 lists 叔父 and 叔母 among the appendix whole-word readings.
- The scan lists every other 叔 spelling as untagged (叔世, 大叔父, 叔父さん and the rest).
- b156-selection.json says 伯仲 was kept because "伯父 and 伯母 are tagged only for their whole-word readings おじ and おば", and that "All three review families accepted these row decisions".
- Rule point 2 says "preferring a spelling with ... tags; where none exists, an untagged word may be used with a justification".
Line 78 states the letter-of-the-rule position, the reasons, the B156 precedent and the fallback (叔父 しゅくふ) accurately, and every factual statement checks out. A disclosed exception awaiting the owner's decision is acceptable in a published batch. Point 2 is a preference, B156 has the same precedent, the content is unchanged either way, and the fallback is a small swap. I don't judge that the batch must switch to the fallback now.

Verdicts:
- correctness: CLEAN (吟, 太后, 吟味, ledger lines)
- scoped coverage: CLEAN
- consistency and quiz safety: CLEAN (験 exclusion is a real, symmetric pair and not also a distractor; options in quiz-safety.txt are unchanged: 吟 gets 二 自 社; all 10 cards have 3/3 curated meaning options; reading-exposure shows 0 hits)
- comprehensibility: CLEAN (太后 line 15 and 吟味 line 24 are plain for a phone reader; the ledger is not learner-facing)

Confirmation: CONFIRMED

Findings: none that block. One minor wording note:
1. Minor, consistency; docs\n1-sources\batch-159-progress.json lines 29, 78 and 952. They say the exception was "reported to the owner" (past tense), but CHANGES.md says the owner "will be asked" on issue #60. Also line 78 says "the tags in those entries belong to the whole-word readings おじ and おば", yet the same entries carry ichi1/news1 on the spellings 叔父 and 叔母 (ke_pri), as the line itself says ("both ichi1/news1"). Remedy: make sure the report to the owner is actually posted before publication, or write "to be reported"; and write "the tags are shared with the whole-word readings" or similar. Confidence: high on the evidence; low on the impact.

Optional: none beyond the 験 comment under O2.

Limits: I could not check the Joyo PDF itself, only the author's pdfplumber extracts. I could not verify the 験 title ("test; verify") against its card; it came from the earlier packet's CHANGES.md. I could not verify that the owner report exists (issue #60 was not opened). The audits cannot show what a real user sees in a given quiz session, only the modelled pools. I issued one tool call per response throughout and did not use sub-agents. The manifest and Kotlin tests were not run by me.
