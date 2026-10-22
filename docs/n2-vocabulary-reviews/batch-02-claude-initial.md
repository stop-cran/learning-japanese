## Snapshot
Commit **a0423388624ed50b0a348ad6f7dd7c212b3850b9** (parent 04aed4865849ea4b8362dd1dff068d8066f2f681), committed content only. I had file tools but no Git, so I couldn't confirm that the working-tree files match this commit or check the receipt's hashes.

## Scope
- **Reviewer:** claude-opus-5.5 (Claude family), working sequentially with no delegation and no edits.
- **New articles:** all 14 read in full.
- **Evidence read:**
  - TSV rows N2:22–41 and the vocabulary snapshot.
  - The relevant records in batch-02.json, including entries 1218360, 1612620, 1586430 and 1586440.
  - docs\jlpt-levels.md lines 37–95.
- **Related edits:** the full patch, plus the changed passages in context on 名, 温, 戸, 危, 編, 物, 雨, 甘, 厚 and 圧, and the four articles that only gained `jlpt: 2`.
- **Reuse claims:** あちこち (for source あちらこちら), 怪しい, 余る, 暴れる, 編む and 脂.
- **Other pages read:** link targets and comparison pages, and title/exclusion searches across `words\`.
- **Not covered:** unchanged teaching on these pages, the app's actual quiz-candidate scoring (not run), native-speaker certification, and any forbidden documents.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 暖まる | UNVERIFIED (B02-CL-03) | CLEAN | NEEDS FIX (B02-CL-03) |
| 暖める | UNVERIFIED (B02-CL-03) | CLEAN | CLEAN |
| あたりまえ | NEEDS FIX (B02-CL-02) | CLEAN | CLEAN |
| 厚かましい | CLEAN | CLEAN | CLEAN |
| 圧縮 | CLEAN | CLEAN | CLEAN |
| 宛名 | CLEAN | CLEAN | CLEAN |
| あてはまる | CLEAN | CLEAN | CLEAN |
| あてはめる | NEEDS FIX (B02-CL-01) | CLEAN | CLEAN |
| あぶる | CLEAN | CLEAN | CLEAN |
| あふれる | CLEAN | CLEAN | CLEAN |
| 雨戸 | CLEAN | CLEAN | CLEAN |
| 甘やかす | CLEAN | CLEAN | CLEAN |
| 編物 | CLEAN | CLEAN | CLEAN |
| 危うい | CLEAN | CLEAN | CLEAN |

**Related edits**
- **Ten kanji cards: CLEAN on all three facets.** The links point to real articles. Readings are given for whole words, with no invented reading for a single character (雨戸 is shown as あま + と voiced to ど). The links from 温 to the 暖まる/暖める articles are allowed, because both articles explicitly teach the 温 spelling.
- **余る, 暴れる, 編む and 脂 (`jlpt: 2` added): CLEAN.** The patch adds the field without removing an earlier one, and N5–N3 coverage is complete, so no easier level is being overridden.

**Reuse claims: all six CLEAN on all three facets.**
- **あちこち:** it explicitly names あちらこちら as a form of the same expression, and that dictionary entry has no reading restrictions.
- **怪しい:** already N2; covers suspicious and doubtful (senses 1–7).
- **余る, 暴れる, 脂:** teach sense 1 under the source spelling and reading.
- **編む:** teaches senses 1–2.

## Findings
**B02-CL-01: あてはめる and 適用 are not excluded from each other in quizzes**
- **Severity / facet / confidence:** Moderate; correctness of quiz metadata; high confidence.
- **Where:** words\あてはめる.md:4, 8, 9 and words\適用.md:4, 8.
- **Claim and learning impact:** The titles are "apply a rule; fit into" and "application of a rule or method". Both cards carry the `rules` tag, and neither excludes the other. 適用's pattern 規則を…に適用する ("apply a rule to …") is nearly the same as あてはめる's example この規則を…にあてはめる. In either quiz direction, a learner who answers correctly could be marked wrong.
- **Remedy:** add 適用 to あてはめる's `quiz_exclusions`. Exclusions apply in both directions, so one side is enough.
- **Evidence:** existing cards already exclude verb–noun pairs like this, for example 暴れる excludes both 戦い and 戦う.

**B02-CL-02: あたりまえ and もちろん are not excluded from each other**
- **Severity / facet / confidence:** Minor; correctness of quiz metadata; medium confidence.
- **Where:** words\あたりまえ.md:9 and :41; words\もちろん.md:4.
- **Claim and learning impact:** The article itself translates あたりまえでしょう as "of course", which is もちろん's exact title. A learner who picks "of course" for あたりまえ would be marked wrong for using the article's own translation.
- **Remedy:** add もちろん to あたりまえ's `quiz_exclusions`.
- **Evidence:** the overlap comes directly from the English labels, not just a shared topic. The two cards share no tag, so this pair is less likely to appear together than B02-CL-01.

**B02-CL-03: No guidance on when to write 暖 versus 温**
- **Severity / facet / confidence:** Minor; comprehensibility; medium confidence.
- **Where:**
  - words\暖まる.md:27–29 ("Learn the spelling with its context").
  - Body examples at 暖まる.md:20 and :41–42, and 暖める.md:21.
  - The 温 kanji card (kanji\温.md:33–34 and 42–43) links to these articles for 温まる/温める.
- **Claim and learning impact:** The articles never say which context favours which character. 暖まる has no example using 温 at all, and both articles use 暖 for warming the body or hands (体が暖まる, 手を暖める). Elsewhere the repo teaches the tendency: the 暖かい article and confusable-words entry CW038 say 暖 for air and weather, 温 for food, drinks and kindness. I believe 温 is the more common spelling for the body, but could not verify this, hence UNVERIFIED for correctness.
- **Remedy:** add one hedged line to each article (暖 tends to be used for rooms, air and weather; 温 for food and drink, and often the body), linking 暖かい. If that preference is confirmed, consider switching the body example to 温.

## Optional
- **あてはまる:** mention 適用される as a near-synonym. The quiz overlap with 適用 is weak, so I'm not reporting it as a defect.
- **あてはめる:44:** the sentence "Whether a rule can appropriately be applied…" is vague and could be clarified.
- **危うい:24–25:**
  - Say that the dictionary's first sense usually appears as 危ういところ.
  - Add 危ういところで助かった ("was saved just in time") and the related adverb 危うく ("nearly").
  - Note that 危うい is more formal than 危ない.
- **暖める:** "warm; heat up" shares the label "warm" with 暖かい "warm; mild"; "warm something up" would be clearer.
- **温 card:42–43:** "the linked article also teaches 暖まる" reverses which spelling is the main headword.
- **Smaller additions:**
  - **編物:** say that 編み物 is the more common spelling.
  - **あふれる:** add a figurative example such as 涙があふれる.
  - **あちこち:** add a register note (あちらこちら is fuller; あっちこっち is casual).
  - **厚かましい:** the first example, "…なんて、厚かましいです", is slightly stiff in register.

## Limits
- Without Git I couldn't verify the hashes, that committed content matches the files read, or what the four level-only files said at the parent commit beyond the patch.
- The 暖/温 spelling preference for the body is unverified. The 異字同訓 PDF couldn't be read as text, Kotobank and Weblio gave no usage note, goo was unreachable, and DuckDuckGo search was CAPTCHA-blocked.
- I didn't run the app's quiz-candidate selection, so how often these pairs would actually appear together is inferred, not measured.
- These verdicts are not a native-speaker certification.
