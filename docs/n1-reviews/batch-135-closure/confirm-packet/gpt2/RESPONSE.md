# Author's statement for the reviewer of `reports-135\confirm-gpt.md`

This statement answers only the points in YOUR confirmation report. G5 is your report's own Findings label; your report
had no Optional points. The statement is the author's claim about what changed and why. Verify each claim against the
revised card text in `snapshot\kanji\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence.
Card line numbers refer to the revised cards in this packet; other line numbers refer to the named file in this packet.
Four of the 15 cards changed (彫 巡 救 履) and the other eleven did not (see `CHANGES.md`). Give a disposition for G5.

## Findings

### G5 (major): 彫 — える can be offered as a wrong kun reading in a padded Starter session

Author action: **changed**, by the second route your remedy names: safe curated providers available in every pool the
app builds, as was done for 巡. The pinned metadata of 彫 is unchanged (neither える nor えり is added to its readings),
and in the front matter only `distractors` (line 13) changed.

- **The finding reproduced.** With `--extra 彫=え.る` added and all earlier extras kept, the same audit run on `2ef25d33`
  (`evidence\reading-exposure-2ef25d33.txt`) shows the path you derived. 周, 影 and 掘 are not starter cards (lines
  190-192), so in the Starter session both 彫 prompts take all three wrong options from the fallback (lines 198 and 205;
  17 drawable wrong options for ほる). A Starter session that also borrows one holder card can offer える, and it can do so
  with either holder, 得 or 選 (line 208). The new summary line 400 counts this as 1 one-holder padded hit (see `CHANGES.md`
  on that line).
- **The change.** `彫.md:13`: `distractors` is now `[円, 高, 見]` (it was `[周, 影, 掘]`). All three are starter cards
  (`checks\reading-exposure.txt` lines 190-192), so they are in the N1 stack, the All stack and the Starter session.
- **Why the fallback is no longer reached.** In `evidence\KanjiReadings.kt`, the curated cards found in the pool are taken
  first (line 110). Each adds one random usable reading through `add` (lines 98-101), which accepts a key only while
  fewer than `count - 1` options are chosen (3 with the default `count = 4`, line 91) and the key is neither excluded
  nor already used. The keys of 円 (エン; まるい, まる, まど, まどか, まろやか), 高 (コウ; たかい, たか, だか, たかまる, たかめる) and 見 (ケン; みる, みえる, みせる)
  never repeat across the three cards and are not among 彫's excluded keys. So after line 110 all three wrong slots of
  both prompts are full, and lines 111 and 112 add nothing. This holds in any pool that contains 円, 高 and 見, whatever
  other cards are borrowed, which also covers the combinations of borrowed holders that the audit does not enumerate.
- **The audit after the change** (`checks\reading-exposure.txt`, 彫 block lines 189-214; the command on line 1 adds
  `彫=え.る`; line 2 says why):
  - チョウ: 1 outcome, 3 curated wrong options, in all three pools (lines 196-198).
  - ほる: 75 outcomes, 13 drawable wrong options, all curated, in all three pools; the fallback is never consulted
    (lines 203-205).
  - える (offered by 得 and 選) cannot be drawn in any pool, nor with either holder borrowed (lines 206 and 208). えり,
    the out-dated kana that JMdict 2265620 gives for the noun 彫り (line 193), offered by 領, cannot be drawn either
    (lines 209 and 211).
  - Summary: 0 production hits, 0 padded-session hits (line 399), 0 one-holder padded hits (line 400).
  - `checks\reading-options.txt` line 187 notes that える cannot be drawn from the full pool (lower closeness tier).
- **Card text.** `彫.md:41` (new paragraph) says that Daijisen has a separate headword える, ゑる in historical kana, for
  ▽彫る, first sense "to carve; to engrave", that ▽ means the official table does not list this reading of 彫, and that
  JMdict's entry for 彫り, also written 彫, gives ほり and the out-dated kana えり; neither reading is asked, and none of
  円, 高 and 見 is read える or えり. `彫.md:55` cites JMdict 2265620 and Digital Daijisen 彫る. Support:
  `evidence\daijisen-彫る.txt` line 7 (headword and sense １ `彫刻する`; ほ・る【彫る】 is line 9);
  `evidence\jmdict-cited-entries.xml` lines 6-21; the official table's 彫 row lists only チョウ and ほる
  (`evidence\joyo\p110.txt` lines 6-8).
- **Meaning options rechecked**, as your remedy asks: `checks\quiz-safety.txt` line 22, `yen, circle | high, expensive |
  see, look`, against the title "carve; engrave; sculpt"; 0 errors and 0 warnings (line 57). `quiz_exclusions`
  (`[刻, 削, 像]`) are unchanged, and none of 円, 高 and 見 is in them.
- **Disclosure.**
  - 円 and 高 are chosen for shape: 円 has the 冂 frame that holds the inside of 周, the left part of 彫, and 高 has 冂
    with 口 inside it at the bottom, much as 周 has 士 above 口 inside its frame (`彫.md:52`; `evidence\kanjivg\05468.svg`,
    `05186.svg` and `09ad8.svg`, line numbers in `CHANGES.md`).
  - 見 is not similar in shape, and line 52 says so. It was chosen because its kun readings みる, みえる and みせる all
    end in る, as ほる does, so every ほる question keeps at least one verb-shaped wrong option. A starter card was needed
    so that all three slots are filled in the Starter session too.
  - 周, 影 and 掘 are no longer meaning options. They remain in the look-alike bullet of the Notes (line 51), and the
    mnemonic (line 27) still uses 周. No card in `kanji\` lists more than three `distractors`, so they could not be kept
    beside the new three.
- **Not done.** No reading-quiz test was added. As in the earlier round, the content repository has no reading-quiz
  builder, and the Kotlin and JVM tests were not run.

To verify: that no allowed path in `evidence\KanjiReadings.kt` can now offer える or えり for 彫 in any pool that contains
円, 高 and 見; that the new paragraph on line 41 is accurate; and that the new meaning options are fair.

## Other limits in your report

No disposition is needed for these.

- **Combinations of borrowed holders.** For 彫 and 巡, the curated cards fill every wrong slot, so other borrowed cards,
  however many, cannot change their options (see G5 above). For cards whose Starter prompts still use the fallback, the
  audit still tries one extra holder at a time; it has no enumeration of combinations.
- **The attestation inventory.** The zero-hit result is still relative to its inventory: the KANJIDIC2 name readings,
  every Kanjipedia 外 reading of the 15 kanji, the readings of each kanji's single-kanji JMdict entries, and now 彫 える.
  The author did not search Daijisen for ▽ headwords of the other 14 kanji in this batch. From batch 136 on, the
  authoring notes will add that search and the single-kanji JMdict check as standing steps before a batch is frozen.
- **Not the app.** The audits are still Python ports of the Kotlin sources, not a run of the app or of the JVM tests.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk.

- **巡: one wrong-answer card replaced** (`巡.md:13`, `:37`, `:49`). `distractors` is now `[川, 道, 見]` (it was
  `[川, 道, 達]`). 見's kun readings みる, みえる and みせる end in る, as めぐる does, so the めぐる question now has a
  verb-shaped wrong option; with 達, the options were always かわ, みち and -たち. 見 is not similar in shape, and line 49
  says so; 達 stays in that bullet as a look-alike. Among the 118 starter cards, only 道 and 達 share 辶 with 巡 and only
  川 shares 巛, and none of them has a kun reading ending in る. 川, 道 and 見 are all starter cards and still fill all
  three wrong slots of both prompts in all three pools, so まわる, offered by 回, still cannot be drawn
  (`checks\reading-exposure.txt` lines 131-153). The meaning options are now `river | road, way | see, look`
  (`checks\quiz-safety.txt` line 15). Line 37 now ends `..., and none of the three cards chosen to supply this card's
  wrong answers, 川, 道 and 見, is read まわる.` instead of `..., so this card's quiz does not offer まわる as a wrong
  answer.`
- **救: one sentence reworded** (`救.md:49`). The bullet no longer says what the quiz does. It says that none of the three
  look-alike cards chosen to supply the wrong answers, 敬, 球 and 教, is read グ, ク or たすける, and that for that reason
  求 is not among them. `distractors` is unchanged.
- **履: one clause reworded** (`履.md:36`). `the voiced form of サウ, its historical spelling of 草's ソウ.` became `the
  voiced form of サウ, which is the historical spelling of ソウ, the on reading of 草.`

## Process notes

- `fb236071` is the second local version of this fix commit. The first, `3a13bb67`, had the same tree and differed only in
  the commit message; it was never published or reviewed.
- The audit tool gained one summary line (line 400) this round; see `CHANGES.md`.
