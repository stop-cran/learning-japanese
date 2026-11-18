# Batch 135 second revision: what changed from 2ef25d33 to fb236071

Revised snapshot: `fb236071b6355b28423581c96a35a8ca1084a193`, a child of the earlier revision
`2ef25d33ab16d928ac4f0a845b4d8f78005223da`, which was the subject of the earlier confirmation round. That revision is a
child of the initially reviewed snapshot `163b384e6cb8f75c06fe395f7b144cdd8b105673`. Nothing is published.

- Four of the 15 kanji cards changed: 彫, 巡, 救 and 履. The other eleven (博, 厳, 及, 姿, 弾, 恵, 憶, 我, 揚, 暇, 模) are
  unchanged, and so are all 15 stroke files, all titles, tags, metadata readings and `quiz_exclusions`. No word article
  changed in this revision.
- Front matter changed only in `distractors` (line 13) of 彫 and 巡.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot). The text at `2ef25d33`
  is in the earlier confirmation packet's `snapshot\kanji\`.
- `diffs\fix.patch` is the exact patch from `2ef25d33` to `fb236071`. `diffs\changed-lines.txt` lists the changed lines
  per file.
- Every quoted title in the new text was checked by script against the linked card's real `title:` (see
  `checks\link-targets.tsv`).
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. Earlier evidence
  stays in the earlier confirmation packet and the original packet.

| Card | Changed lines | Change |
| --- | --- | --- |
| 彫 | 13, 41, 52, 55 | Line 13: `distractors: [円, 高, 見]` (it was `[周, 影, 掘]`). Line 41 is a new paragraph, the last of the Readings section: `Two further readings are outside both KANJIDIC2 and the official table. Daijisen has a separate headword える, ゑる in historical kana, for a verb written ▽彫る whose first sense is "to carve; to engrave"; the ▽ mark means that the official table does not list this reading of 彫. JMdict's entry for the noun 彫り, also written 彫, "carving; engraving," gives ほり and, marked as an out-dated kana usage, えり. Neither reading is asked here, and none of the three cards chosen to supply this card's wrong answers, 円, 高 and 見, is read える or えり.` Line 52 is a new Notes bullet after the 周/影/掘 bullet: `[円](円.md), "yen, circle," has the 冂 frame that holds the inside of 周, and [高](高.md), "high, expensive," has 冂 with 口 inside it at the bottom, much as 周 has 士 above 口 inside its frame. [見](見.md), "see, look," is not similar in shape; its kun readings みる, みえる and みせる end in る, as ほる does. These three cards supply this card's wrong answers. All are different kanji.` Line 55 (Metadata): JMdict entry 2265620 is added to the entry list, and `The verb える: [Digital Daijisen, 彫る](https://www.weblio.jp/content/彫る).` is appended. Support: `evidence\daijisen-彫る.txt` line 7 (`え・る〔ゑる〕【 ▽ 彫る／ × 雕る／ × 鐫る】`, sense １ `彫刻する`); `evidence\jmdict-cited-entries.xml` (2265620: 彫り and 彫 at lines 6 and 9, ほり at 12, えり at 15 tagged `out-dated or obsolete kana usage` at 16, glosses at 20-21); the official table's 彫 row lists only チョウ and ほる (`evidence\joyo\p110.txt` lines 6-8; also the original packet's `evidence\joyo-pages.md` lines 584-590); `evidence\kanjivg\05468.svg` (周: 冂, marked `kvg:variant="true"`, lines 40-42, holding 吉, which is 士 at lines 45-48 over 口 at lines 50-53), `05186.svg` (円: 冂 at lines 40-42 holding strokes 3 and 4 at lines 44-46) and `09ad8.svg` (高: the bottom part 冋, line 51, is 冂 at lines 52-54 with 口 at lines 56-59). The 周/影/掘 Notes bullet (line 51) and the mnemonic (line 27) are unchanged. |
| 巡 | 13, 37, 49 | Line 13: `distractors: [川, 道, 見]` (it was `[川, 道, 達]`). Line 37 now ends `[Kanjipedia's character entry](https://www.kanjipedia.jp/kanji/0003246000) does list まわる as a kun reading outside the official table, and none of the three cards chosen to supply this card's wrong answers, 川, 道 and 見, is read まわる.` (it ended `..., so this card's quiz does not offer まわる as a wrong answer.`). Line 49 gains `[見](見.md), "see, look," is not similar in shape; its kun readings みる, みえる and みせる end in る, as めぐる does.` after the 道/達 sentence; 達 stays in the look-alike bullet. |
| 救 | 49 | `..., so they are not asked, and none of the three look-alike cards chosen to supply this card's wrong answers, 敬, 球 and 教, is read グ, ク or たすける. For that reason, 求, which is also read グ, is not among them.` (it read `..., so they are not asked, and this card's quiz does not offer them as wrong answers either. For that reason, 求, which is also read グ, is not among the look-alike kanji this card's quiz uses for wrong answers.`). `distractors` is unchanged. |
| 履 | 36 | `Daijisen spells it ザウ in historical kana, the voiced form of サウ, which is the historical spelling of ソウ, the on reading of 草.` (it read `..., the voiced form of サウ, its historical spelling of 草's ソウ.`). |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter on the 15 kanji cards and their 32 word articles: 0 errors, 7 warnings, all on unchanged word
  articles (6 say the Dictionary line cites no JMdict entry id, 1 says there is no Dictionary line). Same as at `2ef25d33`.
- `unittest.txt`: 436 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes (3201 of 3336 reviewed prompts, stage pilot).
  `manifest.txt`: `manifest.json` regenerated (8816 files), rebuild idempotent, tracked tree clean.
- The Android app's JVM tests that read the real content and the Kotlin reading-audit cross-check were not run for this
  revision either, so there is no `jvm.txt`.
- `link-targets.tsv`: every link on a changed line, with the existence of its target, the target's `title:` and whether the
  gloss quoted after the link equals that title.
- `quiz-safety.txt`, `reading-options.txt` and `reading-exposure.txt`: see the next section.

## Quiz mechanics the changes rely on

- Meaning quiz (`evidence\QuizBuilder.kt`): options are the curated `distractors` in order, skipping any that is excluded
  against the target or an already chosen option; other cards are added only when fewer than three survive.
  `checks\quiz-safety.txt` shows the new meaning options: 巡 `river | road, way | see, look` (line 15) and 彫
  `yen, circle | high, expensive | see, look` (line 22). 周, 影 and 掘 are no longer meaning options for 彫; they remain
  in its Notes (line 51). No card in `kanji\` lists more than three `distractors`, so the author did not add 円, 高 and 見
  beside them.
- Reading quiz (`evidence\KanjiReadings.kt`, `KanjiReadingQuiz`; `evidence\Words.kt` for `ReadingOptions.mutations`):
  `quiz_exclusions` affect only the meaning quiz. Each curated `distractors` card in the pool offers one random usable
  reading of the asked kind (skipped if it is empty, excluded or a duplicate); remaining slots are filled from other
  cards' readings in closeness tiers, highest tier first. The excluded readings are the target's own readings and their
  sound-change variants.
- `checks\reading-exposure.txt` enumerates the pools the app builds: the N1 and All stacks (1,277 cards each) and the
  Starter practice session (the 118 starter cards plus the borrowed target), and for each attested but unlisted reading
  also tries a Starter session that borrows one extra holder card. The command (line 1) uses the same `--extra` readings
  as the earlier round plus `彫=え.る`, the Daijisen headword える (the tool labels `--extra` readings `(card text)`).
  - Summary (line 399): 0 production hits, 0 padded-session hits, 26 latent collisions (25 in the earlier round's audit,
    which did not add える; the new one is 彫 える, offered by 得 and 選).
  - Line 400 is new this round: the audit tool now also counts the one-holder cases, which it previously reported only
    per reading. 0 one-holder padded hits, and 3 for KANJIDIC2 name-only readings: 恵 へい (lines 241-243) and み (lines
    244-246), and 我 か (lines 305-307). Their per-reading lines are identical in the `2ef25d33` run below.
  - 彫 (lines 189-214): 円, 高 and 見 are all starter cards (lines 190-192) and fill all three wrong slots of both prompts
    in the N1 stack, the All stack and the Starter session, so the fallback is never consulted (lines 196-198 and
    203-205). える, offered by 得 and 選, and えり (JMdict 2265620, line 193), offered by 領, cannot be drawn in any pool,
    nor in a Starter session that also borrows any single holder card (lines 206-211).
  - 巡 (lines 131-153): 川, 道 and 見 are all starter cards (lines 132-134) and fill all three wrong slots of both prompts
    in all three pools (lines 138-140 and 145-147). まわる, offered by 回, cannot be drawn in any pool, including a
    Starter session that also borrows 回 (lines 148 and 150). The めぐる prompt now has 5 drawable wrong options (line 145),
    always かわ and みち plus one of みる, みえる and みせる (`checks\reading-options.txt` lines 126-128).
  - The same command run with the same tool on `2ef25d33` (`evidence\reading-exposure-2ef25d33.txt`) differs only in the
    巡 and 彫 blocks, the commit named on line 1 and line 400. There, 彫's curated 周, 影 and 掘 are not starter cards (lines
    190-192), so in the Starter session both 彫 prompts take all three wrong options from the fallback (lines 198 and
    205), and a Starter session that also borrows 得 or 選 can offer える for ほる (line 208); line 400 counts this as 1
    one-holder padded hit. In the N1 and All stacks the ほる prompt also had one open slot, because 掘's only kun reading,
    ほ.る (line 192), is the target's own (lines 203-204).
- `checks\reading-options.txt` is the older superset audit with the same added readings. It reports `1 problem(s)` (line
  348): 巡 まわる from 回 (line 132), because it does not model that the three curated options already fill every slot
  (lines 126-128), as in the earlier round. For 彫 it notes that える cannot be drawn from the full pool (line 187).
- Neither audit runs the app's own code or random generator; both are the author's Python ports of the Kotlin sources in
  `evidence\`. Sampled seeds are a sanity check; the enumerations are the result.

## Process notes

- The audit tool (`reading_exposure.py`) is the author's local script and is not under version control. This round's
  only change to it is the second summary line (line 400); the per-reading lines are produced as before.
- `fb236071` is the second local version of this fix commit. The first, `3a13bb67`, had the same tree and differed only in
  the commit message; it was never published or reviewed.
