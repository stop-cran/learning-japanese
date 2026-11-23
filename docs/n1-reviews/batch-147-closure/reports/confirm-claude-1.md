# Batch 147: confirmation review (Claude)

Snapshot: commit 99487bb5bef47b4e43be5b3223db7cb4dbb3bec1 (revised), compared with the reviewed snapshot 6a2323e7. Reviewer model: Claude, an Anthropic model. The exact version string is not available to me.

Scope:
- Read in full: this packet's `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `diffs\fix.patch` (all hunks), `diffs\changed-lines.txt`, and `evidence\README.md`, `QuizBuilder.kt` and `KanjiReadings.kt`.
- Read in full: the checks `quiz-safety.txt`, `reading-exposure.txt`, `link-targets.tsv`, `lint.txt`, `kanji-remarks.txt`, `budget.txt`, `vocabulary.txt`, `validate.txt` and `unittest.txt`, plus `evidence\meta-scan.txt`.
- `checks\reading-options.txt`: read lines 1-40 and 151-225 (穏 to 糧, and the summary), plus a grep.
- Read in full, every line: the ten revised cards 矢 砕 礎 秀 秘 稚 穏 穴 粋 糧 in `snapshot\kanji\`.
- My own initial report: read in full.
- From the original packet, read-only:
  - `evidence\jmdict-families.xml`, XML-extracted for entries 1589620 (温和/穏和), 1254480 (穴 あな), 1254490 (穴 けつ) and 2863360 (稚い).
  - `evidence\public-source\weblio-穏.txt`, grepped for the Daijisen character entry.
- Public web: English Wiktionary page for 卆, fetched and read.
- Not reopened: the unchanged cards 瞬 瞳 稼 稿 笛, the cards 基 密 透 and the word articles. For these I relied on my initial review and on the post-fix quiz audits.
- `evidence\Words.kt`: not opened. My reading of the excluded-key logic relies on `KanjiReadings.kt` and on the audit output.

Dispositions:
- C1 - RESOLVED - `秀.md:27` now puts 禾 at the top and 乃 below it. This matches the stroke order and the 透 card.
- C2 - RESOLVED - `粋.md:33` now describes a part that looks like 九 above 十 and calls it a simplified form of 卒, which is not itself written. Wiktionary 卆 confirms this: "Unorthodox variant of 卒", composition ⿱九十, 4 strokes. 米 (6) + 4 = 10, which matches `strokes: 10`.
- C3 - RESOLVED - `稚.md:40` now says: in 稚い, 稚 writes いとけな and い is the okurigana; in 稚けない, 稚 writes いとけ. JMdict 2863360 has the forms 稚い, 幼い, 稚けない and 幼けない.
- C4 - RESOLVED - `矢.md:27` now has "long sweeping stroke through the middle". At `:47`, 午 and 牛 have a long central stroke with crossing bars, and 天 has two bars with spreading lower strokes. All three descriptions are true of the shapes (矢 ㇒㇐㇐㇒㇏; 天 一一㇒㇏).
- C5 - RESOLVED - `礎.md:27` now quotes "grove; woodland" and `砕.md:49` quotes "perish; destroy; die out". `link-targets.tsv` shows both are equal to the titles.
- C6 - RESOLVED:
  - 方 恋 念 are removed from 矢, and 単 易 簡 悩 from 砕, in both the front matter and the Notes.
  - The remaining exclusions are real direct pairs.
  - All 15 batch cards fill 3/3 meaning slots from their curated distractors (`quiz-safety.txt`). The kanji that are no longer excluded (方 恋 念 単 易 簡 悩 熟 貯 備) are not in the list of 11 cards that use fallback options. So the removals change no option that is shipped today, and every option they could unlock is clearly wrong against the displayed titles.
- C7 - RESOLVED:
  - `穏.md:48` now gives the functional reason and warns future editors.
  - I verified it in `KanjiReadings.question()`: curated cards are added first, one random usable reading each. 木 (き/こ), 田 (た) and 花 (はな) give three distinct keys, none of them excluded for 穏, so `chosen` is full before the fallback runs.
  - `reading-exposure.txt:171-187` confirms all three are Starter-tagged and present in the N1 pool, the All pool and the Starter practice pool.
- O1 - RESOLVED - `砕.md:25` now reads "fine or small" without quotation marks.
- O2 - DECLINE ACCEPTED - this was optional extra vocabulary. The quizzed reading や is fully covered.
- O3 - RESOLVED - `秘.md:41` now has "kun, outside the official table". The Joyo table lists only ヒ and ひめる for 秘.
- O4 - PARTIALLY RESOLVED:
  - The 温和 half is fixed, and it is better than I asked. `穏.md:39` now quotes only the senses of 1589620 that 穏和 can carry, and says the climate sense is written 温和 only. JMdict confirms this: sense 1 has `stagk 温和`. The old text had attributed that 温和-only sense to 穏和.
  - The decline of the line 25 half rests on a false premise. RESPONSE says "The line 25 list is Daijisen's own", but the Daijisen entry (`weblio-穏.txt:6`) lists 「穏健・穏和／安穏・静穏・不穏・平穏」, which is six words including 静穏.
  - `穏.md:25` still says "Its examples are 穏健, 穏和, 安穏, 不穏 and 平穏", which presents five words as the complete list. The remaining fix is one word: write "include", or add 静穏.
- O5 - DECLINE ACCEPTED - this was polish on a paragraph about a different word that the card explicitly does not teach. The tags really are on senses 1-2 and the counter sense really is omitted, but neither misleads about 穴 あな.
- O6 - DECLINE ACCEPTED - the declared remark edit in 基 is correct as written. The missing quoted title is a matter of pattern consistency only.
- O7 - DECLINE ACCEPTED - this concerns a line outside the diff.

Verdicts:
- Correctness - NEEDS FIX: 穏 only, at `穏.md:25`, the O4 remainder above (minor; an incomplete source list stated as complete). Every changed hunk on the other nine changed cards is true, and was checked against JMdict, the Daijisen extract, the stroke structure and Wiktionary.
- Scoped coverage - CLEAN: no reading row, word or required explanation was lost in the revision.
- Consistency and quiz safety - CLEAN:
  - All 42 links on changed lines resolve, and each quoted gloss equals the target's title.
  - No exclusion is also listed as a distractor.
  - The post-fix meaning options of all 15 cards are three clearly wrong curated titles. I checked them by reasoning from `QuizBuilder.options` (curated first, symmetric `excluded`, unique titles) and from the card titles.
  - The reading prompts are unchanged and safe: 0 production hits and 0 padded-session hits.
  - One polish note on the new 穴/秘 exclusion is under Optional.
- Comprehensibility - CLEAN: the corrected mnemonics (秀, 粋, 矢) now describe what a learner sees on the screen. The new 穏 note is clear.

Confirmation: NEEDS FIX. The only open item is the O4 remainder: one word on `穏.md:25` ("include", or add 静穏). I established no new defect.

Findings: none new. The only open correctness item is the O4 remainder above, an earlier point and not a new finding.

Optional:
- 穴/秘 exclusion (`穴.md:14,50`):
  - The added pair is justified by a word sense, JMdict 1254480 sense 7 "good place not many people know about; well-kept secret", not by an overlap between the displayed titles ("hole; pit; cavity" against "secret; conceal").
  - That is the same kind of justification the author removed from 矢 ("(romantic) interest" → 恋), so the two cards now follow opposite policies.
  - It is harmless: both cards fill their options from curated distractors. Still, consider applying one policy to both.
- 粋 reading prompt スイ:
  - The curated distractor 米 contributes one random on reading from べい, まい and めえとる (`reading-options.txt:201`; `reading-exposure.txt:227` shows ベイ マイ メエトル). So the katakana option メエトル (the ateji reading of 米 for "metre") can be offered.
  - It is safe, because it is wrong for 粋, but it is an obvious giveaway for the learner.
  - This was not changed by the revision. The cause is the existing 米 card's quiz readings.
- `矢.md:27`: the "long sweeping stroke" is itself the left half of the "spreading strokes at the bottom". The image still works, but "and the stroke to its right as the tail" would be cleaner.
- `稚.md:40`: "the other JMdict spelling 稚けない" is not quite right, because JMdict also has 稚ない, a search-only form. "the JMdict spelling 稚けない" avoids the implication that there is only one other spelling.

Limits:
- I issued exactly one tool call per response, and no parallel calls, sub-agents or background jobs.
- I verified readings and senses mainly against the packet's pinned JMdict and Daijisen extracts. Live web verification was limited to Wiktionary's 卆 page.
- I did not live-check KANJIDIC2 for 米's reading メエトル. That point rests on the audit output.
- The dispositions on the unchanged cards' options rest on the post-fix `quiz-safety.txt` and `reading-exposure.txt` together with the app sources supplied. I did not re-run any audit.
- What the audits cannot show:
  - Whether a reading or meaning option is pedagogically odd but safe, such as メエトル.
  - Pools other than the N1, All and Starter-practice pools the audit models, such as a padded session that borrows several holder cards at once.
  - The behaviour of the Android JVM tests, which were not run.
- `evidence\jmdict-cited-entries.xml`, which the README describes as "(none)", is not in the packet. I used the original packet's JMdict families file instead.
