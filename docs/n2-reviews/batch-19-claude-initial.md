## Snapshot
Frozen commit `42a8e121fad9901d0738f130164809fb926bc46c` (baseline `ccc1f7dd951e07be4dbb3f5fb80463ad9ca6c89f`, 51 files, clean worktree per the snapshot file). Committed files only. I had file tools but no Git, so I couldn't confirm that the working tree matches this commit. I read the files as they are on disk.

## Scope
- **Model:** claude-opus-5.5 (Claude family). Sequential review; no delegation and no edits.
- **Rules read:** `.github\copilot-instructions.md`, `content-structure.instructions.md` and `docs\content-format.md:18-109`.
- **Read in full:** the 15 kanji cards (脳 腕 腰 膚 臓 臣 舟 航 般 芸 荒 荷 菓 菜 著) and the 4 new word articles (脳, 皮膚, 舟, 荒れる).
- **Related edits:** I checked the changed link passages in 腕, 腰, 心臓, 大臣, 航空, 一般, 芸術, 荷物, お菓子, 菓子, 著者 and 野菜. All 12 links resolve to existing cards, the passages read coherently, and the stale 菜 clause in 野菜 is gone.
- **Evidence:** `batch-19.json` metadata, primaryWords, and the records relied on, including complete records for every word cited in the findings. I also searched kanji/word titles, distractors and exclusions across `kanji\` and `words\`, and checked `docs\confusable-words.md` (only CW057 is relevant, and it doesn't affect these pages). Public checks: Wiktionary 脳, and jisho (JMdict data) for 脳裏 and 腕を上げる.
- **Omitted:**
  - stroke-file drawing paths
  - unchanged text of the 12 related articles
  - all forbidden ledgers, reports and other reviewers' output
  - searches outside the permitted paths

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\脳 | CLEAN | CLEAN | NEEDS FIX (B19-1) |
| kanji\腕 | CLEAN | CLEAN | CLEAN |
| kanji\腰 | CLEAN | CLEAN | CLEAN |
| kanji\膚 | CLEAN | CLEAN | CLEAN |
| kanji\臓 | CLEAN | CLEAN | CLEAN |
| kanji\臣 | CLEAN | CLEAN | CLEAN |
| kanji\舟 | CLEAN | CLEAN | CLEAN |
| kanji\航 | CLEAN | CLEAN | CLEAN |
| kanji\般 | CLEAN | CLEAN | NEEDS FIX (B19-2) |
| kanji\芸 | CLEAN | CLEAN | CLEAN |
| kanji\荒 | CLEAN | CLEAN | CLEAN |
| kanji\荷 | CLEAN | CLEAN | CLEAN |
| kanji\菓 | CLEAN | CLEAN | CLEAN |
| kanji\菜 | CLEAN | CLEAN | CLEAN |
| kanji\著 | CLEAN | CLEAN | CLEAN |
| words\脳 | CLEAN | CLEAN | CLEAN |
| words\皮膚 | CLEAN | CLEAN | CLEAN |
| words\舟 | CLEAN | CLEAN | CLEAN |
| words\荒れる | CLEAN | CLEAN | CLEAN |

**What I verified across all pages:**
- **Metadata:** all 15 cards match the source exactly for stroke count, radical and number, grade and readings.
- **Source-only readings:** 脳 ドウ/のうずる, 臓 はらわた, and 芸 う.える/のり/わざ are all honestly qualified.
- **Examples:** each realizes the indicated reading and respects restrictions. For example, 小舟 こぶね, 舟橋 ふなばし and 荒野 こうや fit their restrictions. The 膚 spelling of はだ is flagged as a rare kanji form while the reading itself is unrestricted, and the card says exactly that.
- **Distractors:** all 45 are existing cards and semantically wrong. No new title activates a direct-synonym risk in any older two-choice card.
- **Word-quiz exclusions:**
  - 脳 excludes 頭, 知能, 心 and 精神.
  - 皮膚 excludes 肌 and 皮.
  - 舟 excludes 船, ボート, ヨット, 風呂 and お風呂; the bath words are justified because the dictionary's unrestricted tub/vat sense also covers 舟.
  - 荒れる excludes 暴れる, 混乱 and 狂う.
  - All four lists are adequate; the remaining candidates are not direct synonyms.

## Findings
**B19-1 — Minor — comprehensibility — `kanji\脳.md:3,14` (taught content at :20, :38-40)**
- **Claim:** the title and heading read "brain; memory", but nothing on the card teaches, explains or exemplifies "memory". The linked word article says "brain; mind".
- **Impact:** the quiz answer label teaches a sense learners can't connect to any taught word.
- **Evidence:**
  - The dictionary entry for 脳 (1470380) gives "brain" and "brains, mind".
  - Wiktionary's Japanese senses are brain, head and chief.
  - JMdict, via jisho, glosses 脳裏 as "one's mind".
  - "Memory" appears to come only from the character dictionary (KANJIDIC2) gloss, which is not a correctness defect.
- **Remedy:** retitle to "brain" or "brain; mind" (no other kanji title collides), or keep "memory" and explain it, for example with 脳裏.
- **Confidence:** medium-high.

**B19-2 — Minor — comprehensibility — `kanji\般.md:39` (examples at :20, :32-33)**
- **Claim:** the note "The source on reading is ハン; 一般 has the established reading いっぱん, not いちはん" is garbled ("source on reading"). It also never explains why both common words, 一般 いっぱん and 全般 ぜんぱん, show パン when the only listed reading is ハン.
- **Impact:** learners can't connect ハン to ぱん.
- **Remedy:** reword to say KANJIDIC2's on reading ハン becomes パン in 一般 いっぱん and 全般 ぜんぱん, while 諸般 しょはん keeps ハン.
- **Evidence:** the metadata lists the on reading as ハン only; the readings table illustrates it with 諸般 alone.
- **Confidence:** high.

## Optional
- **般 title:** "general; kind; category" contains 類's whole title "kind; category". Neither is in the other's quiz and 類 has three distractors, so this is nonblocking. "general; overall" would be clearer.
- **`words\野菜.md:30`:** "菜 is part of the spelling." is a leftover after the clause removal and adds nothing.
- **荒 card:** could link the existing `words\嵐.md` in its 荒らし note, and could give a register cue for すさぶ/すさむ once that is sourced.
- **舟 distractor:** 缶 "tin can; container" sits loosely near the tub/vat sense. Low risk.

## Limits
- **No Git:** the snapshot match is unverified, and I couldn't confirm that the other 11 related articles changed only by links.
- **Stroke files:** drawing paths not reviewed (converter output).
- **Exclusion targets:** the dictionary records for 頭, 知能, 心, 精神, 暴れる, 混乱, 狂う, 船, ボート, ヨット, 風呂, お風呂, 皮 and 肌 were not all opened in full. Those judgments rest on the existing articles' answer labels plus the new words' complete records.
- **Kotobank:** the 脳 lookup returned only encyclopedic anatomy text, so it is evidence on neither side.
- **Unverified:** the register of すさぶ/すさむ, and whether the example sentences sound natural (no native-speaker certification).
