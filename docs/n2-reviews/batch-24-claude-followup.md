## Snapshot
- **Corrected commit:** ea3744200666795bc56f280dc3a89c9c135d118a.
- **Original commit:** 87860502861f01aebed7664f7ad5d6081425e277.
- **Baseline:** 483dd12e7c53315527dc861859231ad8bae7cc02.

I reviewed committed files only. I ran no Git commands, validator or manifest build. The author ran the remaining checks and I did not repeat them:
- clean worktree;
- 10-file correction scope and 60-file cumulative scope;
- validator with zero errors;
- 1,060-row source audit;
- contentVersion 67808719c130984e.

## Scope
- **Model:** claude-opus-5.5 (Claude family).
- **Diff:** n2-batch-24-fix.patch. It changes only the three teaching pages, and all three match it exactly.
- **Pages read in full:** kanji\階.md, kanji\領.md, kanji\零.md.
- **My original report:** docs\n2-reviews\batch-24-claude-initial.md.
- **Comparison pages:** words\階段.md, words\二階建て.md, words\零.md, words\ゼロ.md.
- **Source records checked in batch-24.json:**
  - externalSources and usageEvidence;
  - JMdict 2543170, which includes the gloss "stairs at the front of a noh stage";
  - JMdict 1588750, where the 領 spelling has no flag.
- **Pages fetched:**
  - Japanese Wiktionary pages for きざはし, 領 and 襟;
  - Kotobank 階-456625, which has both Daijisen and Nikkoku entries;
  - Kotobank えり-37518 (Nipponica).

I did not review any other pages again.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\階.md | CLEAN | CLEAN | CLEAN |
| kanji\領.md | CLEAN | CLEAN | CLEAN |
| kanji\零.md | CLEAN | CLEAN | CLEAN |

## Findings
**F1 (階 きざはし register): resolved.**
- Line 31 now labels the word "literary/archaic expression".
- Line 43 attributes that label to Wiktionary, which says 「階段」の古語ないし雅語的表現 in its modern-Japanese section. That line also points readers to 階段 for everyday stairs, keeps JMdict's absent rarity flag, and explicitly avoids a frequency claim.
- Line 42's noh-stage sense matches JMdict 2543170 and Nikkoku ③. Daijisen gives the stairs sense with no register label, as the author stated.
- No regression.

**F2 (領 えり spelling): resolved.**
- Lines 31 and 41 separate three things: 領 is a recognized spelling, 襟 is the standard writing, and neither point is a frequency claim.
- The jōyō point is verified: Wiktionary marks えり as in the jōyō table under 襟 but not under 領.
- Nipponica's えり article says 襟、衿、領とも書き. The biblical エリ entry on the same Kotobank page is not cited as evidence.
- No regression.

**Optional 3 (link ゼロ from 零): adopted, no regression.**
- Line 43 links the existing article and makes no claim that the two readings are interchangeable. This is consistent with words\ゼロ.md:33.
- The れい primary reading is unchanged, and no etymology was added.

**Optional 1, 2, 4, 5, 6, 7 and 8:** not adopted. They remain optional and are not reopened.

**New regressions:** none.

## Optional
- 領.md:41: "領えり" could take a separator, e.g. "領 (えり)", to match line 31.
- 階.md:48: the source link is labelled only "Digital Daijisen", but the same Kotobank page also contains Nikkoku, which carries the noh-stage sense. The label could name both dictionaries.

## Limits
- This was a bounded review of the changed passages only, not a new review of the whole batch.
- I ran no Git commands, validator or manifest build. I did not check the packet totals myself: 57 word/reading pairs, 58 records, 57 entry families and 38 reading rows.
- I did not check that the other 12 kanji pages, the 15 stroke files and the 22 links-only word articles are unchanged since the original review.
- I did not review stroke drawing paths, test the quiz at runtime, or measure how often any word is used.
- This is not a native-fluency certification.
