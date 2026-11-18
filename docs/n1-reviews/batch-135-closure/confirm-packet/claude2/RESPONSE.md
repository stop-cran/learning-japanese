# Author's statement for the reviewer of `reports-135\confirm-claude.md`

This statement answers only the points in YOUR confirmation report. Your report had no Findings; its Optional points are
numbered 1 to 3, and this statement calls them CO1, CO2 and CO3 in that order. The statement is the author's claim about
what changed and why. Verify each claim against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and
independent sources; do not rely on this text as evidence. Card line numbers refer to the revised cards in this packet;
other line numbers refer to the named file in this packet. Four of the 15 cards changed (彫 巡 救 履) and the other eleven
did not (see `CHANGES.md`). Give a disposition for each of CO1, CO2 and CO3.

## Optional points

### CO1: 巡's kun-reading question always offered かわ, みち and -たち

Author action: **changed**, though the new card is not a shape look-alike.

- `巡.md:13`: `distractors` is now `[川, 道, 見]` (it was `[川, 道, 達]`). 見's kun readings are み.る, み.える and
  み.せる, all ending in る like めぐる, and none of them is among 巡's excluded keys.
- The めぐる question now always offers かわ and みち plus one of みる, みえる and みせる (`checks\reading-options.txt`
  lines 126-128; `checks\reading-exposure.txt` line 145: 3 outcomes, 5 drawable wrong options). Two of the three wrong
  options are still nouns, so the question is easier than one with three verb-shaped options. It is no longer answerable
  from the shape of the options alone.
- **Why not a shape look-alike.** The replacement had to be a starter card, so that the three curated cards still fill
  every wrong slot in the Starter session, where the earlier revision had removed the fallback. Among the 118 starter
  cards, only 道 and 達 have 辶 and only 川 has 巛, and none of the three has a kun reading ending in る. 見 was chosen for
  its readings. `巡.md:49` now says `[見](見.md), "see, look," is not similar in shape; its kun readings みる, みえる and
  みせる end in る, as めぐる does.` 達 stays in that bullet as a look-alike.
- **Still safe.** 川, 道 and 見 fill all three wrong slots of both prompts in the N1 stack, the All stack and the Starter
  session, and the fallback is never consulted (`checks\reading-exposure.txt` lines 132-134, 138-140 and 145-147).
  まわる, offered by 回, cannot be drawn in any pool, nor in a Starter session that also borrows 回 (lines 148 and 150).
  The ジュン question now offers せん, one of どう and とう, and けん (`checks\reading-options.txt` lines 116-118).
- **Meaning options** are now `river | road, way | see, look` (`checks\quiz-safety.txt` line 15; 0 errors and 0
  warnings, line 57).

To verify: that みる, みえる and みせる are fair wrong answers for めぐる, and that "see, look" is a fair wrong meaning for
"go around; patrol; tour".

### CO2: 履 line 36, "its historical spelling of 草's ソウ"

Author action: **changed**, with different wording from your suggestion.

- `履.md:36` now reads `Daijisen spells it ザウ in historical kana, the voiced form of サウ, which is the historical spelling
  of ソウ, the on reading of 草.` (it read `..., the voiced form of サウ, its historical spelling of 草's ソウ.`).
- The suggested "Daijisen's historical spelling" was not used because the same sentence already starts "Daijisen spells
  it ザウ"; naming Daijisen twice in one sentence read heavily. The rest of line 36 is unchanged.
- Support (earlier confirmation packet): `evidence\daijisen-草.txt` line 7 (`［音］ ソウ （ サウ ）`) and
  `evidence\daijisen-草履.txt` line 7 (`ぞう‐り〔ザウ‐〕【草履】`).

To verify: that the clause is now unambiguous.

### CO3: 救 line 49 and 巡 line 37 described what the quiz does

Author action: **changed.** Both sentences now state a fact about the three chosen cards, not about the quiz's output.

- `救.md:49`: `..., so they are not asked, and none of the three look-alike cards chosen to supply this card's wrong
  answers, 敬, 球 and 教, is read グ, ク or たすける. For that reason, 求, which is also read グ, is not among them.` (it
  read `..., and this card's quiz does not offer them as wrong answers either. For that reason, 求, which is also read
  グ, is not among the look-alike kanji this card's quiz uses for wrong answers.`).
- `巡.md:37` now ends `..., and none of the three cards chosen to supply this card's wrong answers, 川, 道 and 見, is read
  まわる.` (it ended `..., so this card's quiz does not offer まわる as a wrong answer.`).
- The new 彫 paragraph (`彫.md:41`, below) follows the same rule.
- Each sentence stays true however the fallback behaves, as long as the card's `distractors` are unchanged; if they
  change, the sentence names them and changes with them.

To verify: that neither card still makes a claim about the quiz's output.

## Other limits in your report

No disposition is needed for these.

- **The 巡 まわる HIT in `reading-options.txt`.** It is still there (line 132; `1 problem(s)`, line 348), for the same
  reason as before: that audit does not model that the three curated options fill every slot. `reading-exposure.txt`
  lines 148 and 150 show まわる cannot be drawn.
- **恵 info item.** Unchanged (`checks\reading-exposure.txt` line 227 for ケイ). This round the audit also counts the
  one-holder cases on a new summary line (line 400): 0 for attested readings, and 3 for KANJIDIC2 name-only readings
  (恵 へい and み for the エ prompt, lines 241-246, and 我 か, lines 305-307). The per-reading lines are unchanged.
- **Audits are not the app.** The JVM tests and the Kotlin reading-audit cross-check were not run for this revision
  either.
- **Files not opened.** This packet adds three KanjiVG files (`evidence\kanjivg\`) that support the new 彫 shape claims
  below.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk.

- **彫: a reading outside the official table, and new wrong-answer cards** (`彫.md:13`, `:41`, `:52`, `:55`).
  - Digital Daijisen has a separate headword える, ゑる in historical kana, for ▽彫る, first sense 彫刻する "to carve"
    (`evidence\daijisen-彫る.txt` line 7; ほ・る【彫る】 is line 9). ▽ marks a reading the official table does not list;
    the table's 彫 row has only チョウ and ほる (`evidence\joyo\p110.txt` lines 6-8). JMdict 2265620, 彫り, also written
    彫, gives ほり and the out-dated kana えり (`evidence\jmdict-cited-entries.xml` lines 6-21).
  - The audit now treats える as attested for 彫 (`checks\reading-exposure.txt` line 1, `--extra 彫=え.る`; line 2 says
    why). Run with the same command on `2ef25d33` (`evidence\reading-exposure-2ef25d33.txt`): 周, 影 and 掘 were not
    starter cards (lines 190-192), so both 彫 prompts took all three wrong options from the fallback in the Starter session
    (lines 198 and 205), and a Starter session that also borrows 得 or 選 could offer える for ほる (line 208; line 400
    counts it as 1 one-holder padded hit). In the N1 and All stacks the ほる prompt also had one open slot, because 掘's
    only kun reading is ほ.る, the target's own (lines 192 and 203-204).
  - `彫.md:13`: `distractors` is now `[円, 高, 見]`. All three are starter cards (`checks\reading-exposure.txt` lines
    190-192); their readings never repeat and none is excluded, so they fill all three wrong slots of both prompts in every
    pool, and the fallback is never consulted (lines 196-198 and 203-205; `evidence\KanjiReadings.kt` lines 98-101 and
    110-112). える and えり cannot be drawn in any pool, nor with any single holder borrowed (lines 206-211). Line 399: 0
    production hits, 0 padded-session hits and 26 latent collisions (25 last round; the new one is 彫 える). Line 400: 0
    one-holder padded hits.
  - `彫.md:41` is a new paragraph on える and えり; it ends `Neither reading is asked here, and none of the three cards
    chosen to supply this card's wrong answers, 円, 高 and 見, is read える or えり.` `彫.md:55` cites JMdict 2265620 and
    Digital Daijisen 彫る.
  - `彫.md:52` is a new Notes bullet. 円 and 高 are chosen for shape (the 冂 frame of 周, the left part of 彫;
    `evidence\kanjivg\05468.svg`, `05186.svg` and `09ad8.svg`, line numbers in `CHANGES.md`). 見 is not similar in shape,
    and the bullet says so; it gives every ほる question a wrong option ending in る.
  - Meaning options are now `yen, circle | high, expensive | see, look` (`checks\quiz-safety.txt` line 22). 周, 影 and 掘
    remain in the look-alike bullet (line 51), and the mnemonic (line 27) still uses 周. No card in `kanji\` lists more
    than three `distractors`, so they could not be kept beside the new three.
  - The pinned metadata of 彫 is unchanged; neither える nor えり was added to its readings.

## Process notes

- `fb236071` is the second local version of this fix commit. The first, `3a13bb67`, had the same tree and differed only in
  the commit message; it was never published or reviewed.
- The audit tool gained one summary line (line 400) this round; see `CHANGES.md`.
- The author did not search Daijisen for ▽ headwords of the other 14 kanji in this batch. From batch 136 on, the
  authoring notes will add that search and the single-kanji JMdict check as standing steps before a batch is frozen.
